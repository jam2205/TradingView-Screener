"""
Scheduled Data Collection Example

This script demonstrates automated, scheduled data collection for ML pipelines.
Perfect for building time-series datasets.
"""
from tradingview_screener import Query, col
from tradingview_screener.ml_collector import MLDataCollector
from tradingview_screener.features import (
    add_returns,
    add_volume_features,
    add_technical_flags,
)

# Initialize collector
collector = MLDataCollector(
    output_dir='data/hourly_data',
    format='parquet',
    add_collection_metadata=True,
)

# Define query for high-volume stocks
query = (
    Query()
    .select(
        'name',
        'close',
        'volume',
        'market_cap_basic',
        'relative_volume_10d_calc',
        'RSI',
        'MACD.macd',
        'MACD.signal',
        'change',
    )
    .where(
        col('market_cap_basic') > 5_000_000_000,
        col('volume') > 500_000,
    )
    .order_by('volume', ascending=False)
    .limit(300)
)


# Define custom preprocessing callback
def add_features(df):
    """Add custom features during collection"""
    df = add_returns(df, price_column='close', periods=[1, 5])
    df = add_volume_features(df, volume_column='volume', windows=[5, 10])
    df = add_technical_flags(df, price_column='close', volume_column='volume')
    return df


# Schedule collection every hour for 24 hours
print("Starting scheduled data collection...")
print("Collecting data every 60 minutes for 24 hours")
print("Press Ctrl+C to stop early\n")

collected_data = collector.schedule_collection(
    query=query,
    dataset_name='hourly_market_data',
    interval_minutes=60,  # Every hour
    max_collections=24,  # 24 hours of data
    callbacks=[add_features],  # Apply feature engineering during collection
    on_error='continue',  # Continue on errors
    max_retries=3,
)

print(f"\n✓ Collection complete! Collected {len(collected_data)} snapshots")

# Load and combine all historical data
print("\nLoading historical data...")
historical_df = collector.load_historical_data(
    dataset_name='hourly_market_data',
    combine=True,
)

print(f"Total historical records: {len(historical_df)}")
print(f"Time range: {historical_df['collection_timestamp'].min()} to {historical_df['collection_timestamp'].max()}")

# Save combined dataset
combined_path = 'data/hourly_data/combined_historical.parquet'
historical_df.to_parquet(combined_path, index=False)
print(f"\n✓ Combined historical data saved to: {combined_path}")
