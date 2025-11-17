"""
Machine Learning Data Collector for TradingView Screener

This module provides automated data collection capabilities optimized for ML pipelines.
"""
from __future__ import annotations

__all__ = ['MLDataCollector']

import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import TYPE_CHECKING, Any, Optional, Callable
import logging

from tradingview_screener import Query, Column

if TYPE_CHECKING:
    import pandas as pd
    from typing import Literal

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MLDataCollector:
    """
    Automated data collector for machine learning pipelines.

    Features:
    - Automated scheduled data collection
    - Multiple storage formats (CSV, Parquet, SQLite)
    - Historical data batching
    - Data validation and quality checks
    - Configurable queries for reproducible experiments

    Example:
        >>> from tradingview_screener.ml_collector import MLDataCollector
        >>> from tradingview_screener import col
        >>>
        >>> collector = MLDataCollector(
        ...     output_dir='data/market_data',
        ...     format='parquet'
        ... )
        >>>
        >>> # Define your query
        >>> query = (Query()
        ...     .select('name', 'close', 'volume', 'market_cap_basic',
        ...             'relative_volume_10d_calc', 'RSI', 'MACD.macd')
        ...     .where(
        ...         col('market_cap_basic') > 1_000_000_000,
        ...         col('volume') > 100_000
        ...     )
        ...     .order_by('volume', ascending=False)
        ...     .limit(500)
        ... )
        >>>
        >>> # Collect data once
        >>> df = collector.collect_once(query, dataset_name='high_volume_stocks')
        >>>
        >>> # Or schedule automated collection
        >>> collector.schedule_collection(
        ...     query=query,
        ...     dataset_name='high_volume_stocks',
        ...     interval_minutes=60,
        ...     max_collections=24  # Run for 24 hours
        ... )
    """

    def __init__(
        self,
        output_dir: str | Path = 'data',
        format: Literal['csv', 'parquet', 'sqlite'] = 'parquet',
        timestamp_format: str = '%Y%m%d_%H%M%S',
        add_collection_metadata: bool = True,
        validate_data: bool = True,
        cookies: dict | None = None,
    ):
        """
        Initialize the ML Data Collector.

        Args:
            output_dir: Directory to save collected data
            format: Storage format (csv, parquet, or sqlite)
            timestamp_format: Format for timestamps in filenames
            add_collection_metadata: Add metadata columns (collection_time, data_freshness)
            validate_data: Perform data quality checks
            cookies: TradingView session cookies for real-time data
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.format = format
        self.timestamp_format = timestamp_format
        self.add_collection_metadata = add_collection_metadata
        self.validate_data = validate_data
        self.cookies = cookies

        logger.info(f"MLDataCollector initialized: output_dir={output_dir}, format={format}")

    def collect_once(
        self,
        query: Query,
        dataset_name: str = 'market_data',
        save: bool = True,
        callbacks: list[Callable[[pd.DataFrame], pd.DataFrame]] | None = None,
    ) -> pd.DataFrame:
        """
        Collect data once using the provided query.

        Args:
            query: TradingView Query object
            dataset_name: Name for this dataset
            save: Whether to save the data to disk
            callbacks: Optional list of data transformation functions

        Returns:
            DataFrame with collected data
        """
        logger.info(f"Starting data collection for dataset: {dataset_name}")
        collection_time = datetime.now()

        # Execute query
        try:
            total_count, df = query.get_scanner_data(cookies=self.cookies)
            logger.info(f"Collected {len(df)} rows (total available: {total_count})")
        except Exception as e:
            logger.error(f"Failed to collect data: {e}")
            raise

        # Add metadata
        if self.add_collection_metadata:
            df['collection_timestamp'] = collection_time
            df['collection_unix'] = int(collection_time.timestamp())
            df['dataset_name'] = dataset_name

        # Apply custom transformations
        if callbacks:
            for callback in callbacks:
                try:
                    df = callback(df)
                    logger.debug(f"Applied transformation: {callback.__name__}")
                except Exception as e:
                    logger.warning(f"Callback {callback.__name__} failed: {e}")

        # Validate data
        if self.validate_data:
            self._validate_dataframe(df, dataset_name)

        # Save data
        if save:
            filepath = self._save_data(df, dataset_name, collection_time)
            logger.info(f"Data saved to: {filepath}")

        return df

    def schedule_collection(
        self,
        query: Query,
        dataset_name: str,
        interval_minutes: int = 60,
        max_collections: int | None = None,
        callbacks: list[Callable[[pd.DataFrame], pd.DataFrame]] | None = None,
        on_error: Literal['stop', 'continue', 'retry'] = 'continue',
        max_retries: int = 3,
    ) -> list[pd.DataFrame]:
        """
        Schedule periodic data collection.

        Args:
            query: TradingView Query object
            dataset_name: Name for this dataset
            interval_minutes: Minutes between collections
            max_collections: Maximum number of collections (None = infinite)
            callbacks: Optional list of data transformation functions
            on_error: How to handle errors ('stop', 'continue', 'retry')
            max_retries: Maximum retry attempts on failure

        Returns:
            List of collected DataFrames
        """
        logger.info(
            f"Starting scheduled collection: dataset={dataset_name}, "
            f"interval={interval_minutes}min, max_collections={max_collections}"
        )

        collected_data = []
        collection_count = 0

        try:
            while max_collections is None or collection_count < max_collections:
                retry_count = 0
                success = False

                while not success and retry_count <= max_retries:
                    try:
                        df = self.collect_once(
                            query=query,
                            dataset_name=dataset_name,
                            save=True,
                            callbacks=callbacks,
                        )
                        collected_data.append(df)
                        collection_count += 1
                        success = True

                        logger.info(
                            f"Collection {collection_count} completed. "
                            f"Next collection in {interval_minutes} minutes."
                        )

                    except Exception as e:
                        retry_count += 1
                        logger.error(
                            f"Collection failed (attempt {retry_count}/{max_retries}): {e}"
                        )

                        if on_error == 'stop':
                            raise
                        elif on_error == 'retry' and retry_count <= max_retries:
                            time.sleep(30)  # Wait before retry
                            continue
                        else:  # 'continue'
                            break

                # Wait for next collection
                if max_collections is None or collection_count < max_collections:
                    time.sleep(interval_minutes * 60)

        except KeyboardInterrupt:
            logger.info("Collection interrupted by user")

        logger.info(f"Scheduled collection completed. Total collections: {collection_count}")
        return collected_data

    def collect_batch(
        self,
        queries: dict[str, Query],
        callbacks: dict[str, list[Callable]] | None = None,
    ) -> dict[str, pd.DataFrame]:
        """
        Collect data from multiple queries in batch.

        Args:
            queries: Dictionary mapping dataset names to Query objects
            callbacks: Optional dictionary mapping dataset names to callback lists

        Returns:
            Dictionary mapping dataset names to DataFrames
        """
        logger.info(f"Starting batch collection for {len(queries)} datasets")
        results = {}

        for dataset_name, query in queries.items():
            try:
                dataset_callbacks = callbacks.get(dataset_name) if callbacks else None
                df = self.collect_once(
                    query=query,
                    dataset_name=dataset_name,
                    save=True,
                    callbacks=dataset_callbacks,
                )
                results[dataset_name] = df
            except Exception as e:
                logger.error(f"Failed to collect {dataset_name}: {e}")

        logger.info(f"Batch collection completed. Successful: {len(results)}/{len(queries)}")
        return results

    def _save_data(
        self,
        df: pd.DataFrame,
        dataset_name: str,
        timestamp: datetime,
    ) -> Path:
        """Save DataFrame to disk in the specified format."""
        timestamp_str = timestamp.strftime(self.timestamp_format)

        if self.format == 'csv':
            filepath = self.output_dir / f"{dataset_name}_{timestamp_str}.csv"
            df.to_csv(filepath, index=False)

        elif self.format == 'parquet':
            filepath = self.output_dir / f"{dataset_name}_{timestamp_str}.parquet"
            df.to_parquet(filepath, index=False, engine='pyarrow')

        elif self.format == 'sqlite':
            import sqlite3
            filepath = self.output_dir / f"{dataset_name}.db"
            conn = sqlite3.connect(filepath)
            # Use timestamp as table name suffix for versioning
            table_name = f"{dataset_name}_{timestamp_str}".replace('-', '_').replace(':', '_')
            df.to_sql(table_name, conn, if_exists='replace', index=False)
            conn.close()

        else:
            raise ValueError(f"Unsupported format: {self.format}")

        return filepath

    def _validate_dataframe(self, df: pd.DataFrame, dataset_name: str) -> None:
        """Perform data quality checks."""
        issues = []

        # Check for empty DataFrame
        if df.empty:
            issues.append("DataFrame is empty")

        # Check for missing values
        missing_pct = (df.isnull().sum() / len(df) * 100).round(2)
        high_missing = missing_pct[missing_pct > 50]
        if not high_missing.empty:
            issues.append(f"High missing values: {high_missing.to_dict()}")

        # Check for duplicate rows
        dup_count = df.duplicated().sum()
        if dup_count > 0:
            issues.append(f"Found {dup_count} duplicate rows")

        # Check for constant columns
        constant_cols = [col for col in df.columns if df[col].nunique() <= 1]
        if constant_cols:
            issues.append(f"Constant columns: {constant_cols}")

        # Log issues
        if issues:
            logger.warning(f"Data quality issues in {dataset_name}:")
            for issue in issues:
                logger.warning(f"  - {issue}")
        else:
            logger.info(f"Data validation passed for {dataset_name}")

    def load_historical_data(
        self,
        dataset_name: str,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        combine: bool = True,
    ) -> pd.DataFrame | list[pd.DataFrame]:
        """
        Load previously collected historical data.

        Args:
            dataset_name: Name of the dataset to load
            start_date: Filter data collected after this date
            end_date: Filter data collected before this date
            combine: Whether to combine all files into one DataFrame

        Returns:
            Combined DataFrame or list of DataFrames
        """
        logger.info(f"Loading historical data for: {dataset_name}")

        # Find matching files
        pattern = f"{dataset_name}_*"
        if self.format == 'csv':
            files = list(self.output_dir.glob(f"{pattern}.csv"))
        elif self.format == 'parquet':
            files = list(self.output_dir.glob(f"{pattern}.parquet"))
        elif self.format == 'sqlite':
            # SQLite stores all versions in one DB
            logger.warning("SQLite historical loading requires table name specification")
            return pd.DataFrame()
        else:
            files = []

        # Filter by date if specified
        if start_date or end_date:
            filtered_files = []
            for file in files:
                # Extract timestamp from filename
                try:
                    ts_str = file.stem.replace(f"{dataset_name}_", "")
                    file_date = datetime.strptime(ts_str, self.timestamp_format)

                    if start_date and file_date < start_date:
                        continue
                    if end_date and file_date > end_date:
                        continue

                    filtered_files.append(file)
                except ValueError:
                    continue
            files = filtered_files

        logger.info(f"Found {len(files)} files matching criteria")

        # Load files
        dataframes = []
        for file in sorted(files):
            try:
                if self.format == 'csv':
                    df = pd.read_csv(file)
                elif self.format == 'parquet':
                    df = pd.read_parquet(file)
                dataframes.append(df)
            except Exception as e:
                logger.error(f"Failed to load {file}: {e}")

        if not dataframes:
            logger.warning("No data loaded")
            return pd.DataFrame()

        if combine:
            combined = pd.concat(dataframes, ignore_index=True)
            logger.info(f"Loaded {len(combined)} total rows from {len(dataframes)} files")
            return combined
        else:
            return dataframes
