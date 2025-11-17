"""
Feature Engineering Utilities for Machine Learning Pipelines

This module provides feature engineering and data preprocessing utilities
optimized for financial ML models.
"""
from __future__ import annotations

__all__ = [
    'add_returns',
    'add_log_returns',
    'add_price_momentum',
    'add_volume_features',
    'add_volatility',
    'add_technical_flags',
    'normalize_features',
    'create_lagged_features',
    'handle_missing_values',
    'remove_outliers',
    'create_target_variable',
]

from typing import TYPE_CHECKING, Optional, Literal
import logging

if TYPE_CHECKING:
    import pandas as pd
    import numpy as np

logger = logging.getLogger(__name__)


def add_returns(
    df: pd.DataFrame,
    price_column: str = 'close',
    periods: list[int] = [1, 5, 10, 20],
    suffix: str = '_return',
) -> pd.DataFrame:
    """
    Calculate price returns over multiple periods.

    Args:
        df: Input DataFrame
        price_column: Column containing price data
        periods: List of periods for return calculation
        suffix: Suffix for new column names

    Returns:
        DataFrame with return columns added

    Example:
        >>> df = add_returns(df, periods=[1, 5, 10])
        >>> # Adds: close_return_1, close_return_5, close_return_10
    """
    df = df.copy()

    for period in periods:
        col_name = f"{price_column}{suffix}_{period}"
        df[col_name] = df[price_column].pct_change(periods=period) * 100

    logger.debug(f"Added {len(periods)} return features")
    return df


def add_log_returns(
    df: pd.DataFrame,
    price_column: str = 'close',
    periods: list[int] = [1, 5, 10, 20],
    suffix: str = '_log_return',
) -> pd.DataFrame:
    """
    Calculate logarithmic returns over multiple periods.

    Log returns are more suitable for ML as they are additive and symmetric.

    Args:
        df: Input DataFrame
        price_column: Column containing price data
        periods: List of periods for return calculation
        suffix: Suffix for new column names

    Returns:
        DataFrame with log return columns added
    """
    import numpy as np

    df = df.copy()

    for period in periods:
        col_name = f"{price_column}{suffix}_{period}"
        df[col_name] = np.log(df[price_column] / df[price_column].shift(period)) * 100

    logger.debug(f"Added {len(periods)} log return features")
    return df


def add_price_momentum(
    df: pd.DataFrame,
    price_column: str = 'close',
    windows: list[int] = [5, 10, 20, 50],
) -> pd.DataFrame:
    """
    Add price momentum indicators (price relative to moving averages).

    Args:
        df: Input DataFrame
        price_column: Column containing price data
        windows: Window sizes for moving averages

    Returns:
        DataFrame with momentum features
    """
    df = df.copy()

    for window in windows:
        ma_col = f"{price_column}_ma_{window}"
        momentum_col = f"{price_column}_momentum_{window}"

        df[ma_col] = df[price_column].rolling(window=window).mean()
        df[momentum_col] = (df[price_column] / df[ma_col] - 1) * 100

    logger.debug(f"Added {len(windows)} momentum features")
    return df


def add_volume_features(
    df: pd.DataFrame,
    volume_column: str = 'volume',
    windows: list[int] = [5, 10, 20],
) -> pd.DataFrame:
    """
    Add volume-based features.

    Features:
    - Average volume over windows
    - Relative volume (current vs average)
    - Volume momentum

    Args:
        df: Input DataFrame
        volume_column: Column containing volume data
        windows: Window sizes

    Returns:
        DataFrame with volume features
    """
    df = df.copy()

    for window in windows:
        avg_vol_col = f"{volume_column}_avg_{window}"
        rel_vol_col = f"{volume_column}_relative_{window}"

        df[avg_vol_col] = df[volume_column].rolling(window=window).mean()
        df[rel_vol_col] = df[volume_column] / df[avg_vol_col]

    logger.debug(f"Added {len(windows) * 2} volume features")
    return df


def add_volatility(
    df: pd.DataFrame,
    price_column: str = 'close',
    windows: list[int] = [5, 10, 20],
) -> pd.DataFrame:
    """
    Calculate historical volatility (standard deviation of returns).

    Args:
        df: Input DataFrame
        price_column: Column containing price data
        windows: Window sizes for volatility calculation

    Returns:
        DataFrame with volatility features
    """
    import numpy as np

    df = df.copy()

    # Calculate returns first
    returns = np.log(df[price_column] / df[price_column].shift(1))

    for window in windows:
        vol_col = f"{price_column}_volatility_{window}"
        df[vol_col] = returns.rolling(window=window).std() * 100

    logger.debug(f"Added {len(windows)} volatility features")
    return df


def add_technical_flags(
    df: pd.DataFrame,
    price_column: str = 'close',
    volume_column: str = 'volume',
) -> pd.DataFrame:
    """
    Add binary technical indicator flags.

    Flags:
    - Price above/below 20-day MA
    - Volume above average
    - RSI overbought/oversold (if RSI column exists)
    - MACD bullish/bearish (if MACD columns exist)

    Args:
        df: Input DataFrame
        price_column: Column containing price data
        volume_column: Column containing volume data

    Returns:
        DataFrame with technical flags
    """
    df = df.copy()

    # Price vs MA flags
    if price_column in df.columns:
        ma_20 = df[price_column].rolling(window=20).mean()
        df['price_above_ma20'] = (df[price_column] > ma_20).astype(int)

    # Volume flags
    if volume_column in df.columns:
        avg_vol = df[volume_column].rolling(window=20).mean()
        df['volume_above_avg'] = (df[volume_column] > avg_vol).astype(int)

    # RSI flags (if RSI exists)
    if 'RSI' in df.columns:
        df['rsi_overbought'] = (df['RSI'] > 70).astype(int)
        df['rsi_oversold'] = (df['RSI'] < 30).astype(int)

    # MACD flags (if MACD exists)
    if 'MACD.macd' in df.columns and 'MACD.signal' in df.columns:
        df['macd_bullish'] = (df['MACD.macd'] > df['MACD.signal']).astype(int)

    logger.debug("Added technical indicator flags")
    return df


def normalize_features(
    df: pd.DataFrame,
    columns: list[str] | None = None,
    method: Literal['standard', 'minmax', 'robust'] = 'standard',
    exclude_patterns: list[str] = ['ticker', 'name', 'timestamp', 'target'],
) -> pd.DataFrame:
    """
    Normalize numerical features for ML models.

    Args:
        df: Input DataFrame
        columns: Specific columns to normalize (None = auto-detect numeric)
        method: Normalization method
            - 'standard': Z-score normalization (mean=0, std=1)
            - 'minmax': Scale to [0, 1] range
            - 'robust': Use median and IQR (robust to outliers)
        exclude_patterns: Patterns to exclude from normalization

    Returns:
        DataFrame with normalized features
    """
    df = df.copy()

    # Auto-detect numeric columns if not specified
    if columns is None:
        columns = df.select_dtypes(include=['number']).columns.tolist()

        # Exclude columns matching patterns
        columns = [
            col for col in columns
            if not any(pattern in col.lower() for pattern in exclude_patterns)
        ]

    logger.info(f"Normalizing {len(columns)} features using {method} method")

    if method == 'standard':
        for col in columns:
            mean = df[col].mean()
            std = df[col].std()
            if std > 0:
                df[f"{col}_norm"] = (df[col] - mean) / std

    elif method == 'minmax':
        for col in columns:
            min_val = df[col].min()
            max_val = df[col].max()
            if max_val > min_val:
                df[f"{col}_norm"] = (df[col] - min_val) / (max_val - min_val)

    elif method == 'robust':
        for col in columns:
            median = df[col].median()
            q75 = df[col].quantile(0.75)
            q25 = df[col].quantile(0.25)
            iqr = q75 - q25
            if iqr > 0:
                df[f"{col}_norm"] = (df[col] - median) / iqr

    return df


def create_lagged_features(
    df: pd.DataFrame,
    columns: list[str],
    lags: list[int] = [1, 2, 3, 5],
    group_by: str | None = None,
) -> pd.DataFrame:
    """
    Create lagged features for time-series ML models.

    Args:
        df: Input DataFrame
        columns: Columns to create lags for
        lags: List of lag periods
        group_by: Column to group by (e.g., 'ticker' for panel data)

    Returns:
        DataFrame with lagged features

    Example:
        >>> df = create_lagged_features(
        ...     df,
        ...     columns=['close', 'volume'],
        ...     lags=[1, 5, 10],
        ...     group_by='ticker'
        ... )
    """
    df = df.copy()

    if group_by:
        for col in columns:
            for lag in lags:
                df[f"{col}_lag_{lag}"] = df.groupby(group_by)[col].shift(lag)
    else:
        for col in columns:
            for lag in lags:
                df[f"{col}_lag_{lag}"] = df[col].shift(lag)

    logger.debug(f"Created {len(columns) * len(lags)} lagged features")
    return df


def handle_missing_values(
    df: pd.DataFrame,
    strategy: Literal['drop', 'ffill', 'bfill', 'mean', 'median', 'zero'] = 'median',
    threshold: float = 0.5,
) -> pd.DataFrame:
    """
    Handle missing values in the dataset.

    Args:
        df: Input DataFrame
        strategy: Strategy for handling missing values
            - 'drop': Drop rows with any missing values
            - 'ffill': Forward fill
            - 'bfill': Backward fill
            - 'mean': Fill with column mean
            - 'median': Fill with column median
            - 'zero': Fill with zero
        threshold: Drop columns with missing% > threshold (for 'drop' strategy)

    Returns:
        DataFrame with missing values handled
    """
    df = df.copy()
    initial_rows = len(df)

    if strategy == 'drop':
        # Drop columns with too many missing values
        missing_pct = df.isnull().sum() / len(df)
        cols_to_drop = missing_pct[missing_pct > threshold].index.tolist()
        if cols_to_drop:
            logger.warning(f"Dropping {len(cols_to_drop)} columns with >{threshold*100}% missing")
            df = df.drop(columns=cols_to_drop)

        # Drop remaining rows with any missing values
        df = df.dropna()
        logger.info(f"Dropped {initial_rows - len(df)} rows with missing values")

    elif strategy == 'ffill':
        df = df.fillna(method='ffill')

    elif strategy == 'bfill':
        df = df.fillna(method='bfill')

    elif strategy == 'mean':
        numeric_cols = df.select_dtypes(include=['number']).columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

    elif strategy == 'median':
        numeric_cols = df.select_dtypes(include=['number']).columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())

    elif strategy == 'zero':
        df = df.fillna(0)

    return df


def remove_outliers(
    df: pd.DataFrame,
    columns: list[str] | None = None,
    method: Literal['iqr', 'zscore'] = 'iqr',
    threshold: float = 3.0,
) -> pd.DataFrame:
    """
    Remove outliers from numerical columns.

    Args:
        df: Input DataFrame
        columns: Columns to check for outliers (None = all numeric)
        method: Outlier detection method
            - 'iqr': Interquartile range method (default: 1.5*IQR)
            - 'zscore': Z-score method (default: |z| > 3)
        threshold: Threshold for outlier detection
            - For 'iqr': multiplier for IQR (default: 1.5)
            - For 'zscore': max absolute z-score (default: 3)

    Returns:
        DataFrame with outliers removed
    """
    import numpy as np

    df = df.copy()
    initial_rows = len(df)

    if columns is None:
        columns = df.select_dtypes(include=['number']).columns.tolist()

    mask = pd.Series([True] * len(df))

    if method == 'iqr':
        for col in columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR
            mask &= (df[col] >= lower_bound) & (df[col] <= upper_bound)

    elif method == 'zscore':
        for col in columns:
            z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
            mask &= z_scores <= threshold

    df = df[mask]
    removed = initial_rows - len(df)
    logger.info(f"Removed {removed} outliers ({removed/initial_rows*100:.2f}%)")

    return df


def create_target_variable(
    df: pd.DataFrame,
    price_column: str = 'close',
    target_type: Literal['return', 'direction', 'class'] = 'return',
    periods: int = 1,
    classification_threshold: float = 0.0,
    group_by: str | None = None,
) -> pd.DataFrame:
    """
    Create target variable for ML models.

    Args:
        df: Input DataFrame
        price_column: Column containing price data
        target_type: Type of target variable
            - 'return': Percentage return (regression)
            - 'direction': Binary up/down (classification)
            - 'class': Multi-class based on return magnitude
        periods: Forward periods for target calculation
        classification_threshold: Threshold for direction classification
        group_by: Column to group by (for panel data)

    Returns:
        DataFrame with target variable added

    Example:
        >>> # Binary classification: predict if price goes up
        >>> df = create_target_variable(df, target_type='direction', periods=1)
        >>>
        >>> # Regression: predict 5-day forward return
        >>> df = create_target_variable(df, target_type='return', periods=5)
    """
    import numpy as np

    df = df.copy()

    if group_by:
        future_price = df.groupby(group_by)[price_column].shift(-periods)
    else:
        future_price = df[price_column].shift(-periods)

    if target_type == 'return':
        df['target'] = (future_price / df[price_column] - 1) * 100

    elif target_type == 'direction':
        returns = (future_price / df[price_column] - 1) * 100
        df['target'] = (returns > classification_threshold).astype(int)

    elif target_type == 'class':
        returns = (future_price / df[price_column] - 1) * 100
        df['target'] = np.select(
            [returns < -2, returns > 2],
            [0, 2],  # 0 = down, 1 = neutral, 2 = up
            default=1
        )

    logger.info(f"Created {target_type} target variable with {periods} period(s) forward")
    return df


# Convenience function for common preprocessing pipeline
def preprocess_for_ml(
    df: pd.DataFrame,
    price_column: str = 'close',
    volume_column: str = 'volume',
    target_type: Literal['return', 'direction', 'class'] = 'direction',
    target_periods: int = 1,
    add_technical: bool = True,
    normalize: bool = True,
    handle_missing: Literal['drop', 'median'] = 'median',
    remove_outlier: bool = True,
) -> pd.DataFrame:
    """
    Complete preprocessing pipeline for ML.

    This is a convenience function that applies common preprocessing steps.

    Args:
        df: Input DataFrame
        price_column: Column containing price data
        volume_column: Column containing volume data
        target_type: Type of target variable
        target_periods: Forward periods for target
        add_technical: Add technical features
        normalize: Normalize features
        handle_missing: Strategy for missing values
        remove_outlier: Remove outliers

    Returns:
        Preprocessed DataFrame ready for ML
    """
    logger.info("Starting ML preprocessing pipeline")

    # Add features
    if add_technical:
        df = add_returns(df, price_column)
        df = add_price_momentum(df, price_column)
        df = add_volume_features(df, volume_column)
        df = add_volatility(df, price_column)
        df = add_technical_flags(df, price_column, volume_column)

    # Create target
    df = create_target_variable(df, price_column, target_type, target_periods)

    # Handle missing values
    df = handle_missing_values(df, strategy=handle_missing)

    # Remove outliers
    if remove_outlier:
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        # Don't remove outliers from target
        numeric_cols = [c for c in numeric_cols if c != 'target']
        df = remove_outliers(df, columns=numeric_cols)

    # Normalize
    if normalize:
        df = normalize_features(df, method='robust')

    logger.info(f"Preprocessing complete. Final shape: {df.shape}")
    return df
