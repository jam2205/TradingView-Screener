"""
Simple Machine Learning Data Collection Example

This script demonstrates basic data collection for ML pipelines.
"""
from tradingview_screener import Query, col
from tradingview_screener.ml_collector import MLDataCollector
from tradingview_screener.features import preprocess_for_ml

# Initialize the ML data collector
collector = MLDataCollector(
    output_dir='data/ml_data',
    format='parquet',  # Parquet is efficient for ML workflows
    add_collection_metadata=True,
    validate_data=True,
)

# Define your screening query
# Example: Large cap stocks with high volume and momentum
query = (
    Query()
    .select(
        'name',
        'close',
        'open',
        'high',
        'low',
        'volume',
        'market_cap_basic',
        'relative_volume_10d_calc',
        'RSI',
        'MACD.macd',
        'MACD.signal',
        'EMA5',
        'EMA20',
        'EMA50',
        'change',
    )
    .where(
        col('market_cap_basic') > 10_000_000_000,  # Market cap > $10B
        col('volume') > 1_000_000,  # Volume > 1M
        col('relative_volume_10d_calc') > 1.2,  # Above average volume
    )
    .order_by('volume', ascending=False)
    .limit(500)
)

# Collect data once
print("Collecting market data...")
df = collector.collect_once(
    query=query,
    dataset_name='large_cap_momentum',
    save=True,
)

print(f"\nCollected {len(df)} stocks")
print(f"\nFirst few rows:\n{df.head()}")

# Preprocess for machine learning
print("\nPreprocessing data for ML...")
df_processed = preprocess_for_ml(
    df,
    price_column='close',
    volume_column='volume',
    target_type='direction',  # Binary classification: predict if price goes up
    target_periods=1,  # Predict next period
    add_technical=True,
    normalize=True,
    handle_missing='median',
    remove_outlier=True,
)

print(f"\nProcessed data shape: {df_processed.shape}")
print(f"Features: {list(df_processed.columns)}")

# Save processed data
output_path = 'data/ml_data/processed_data.parquet'
df_processed.to_parquet(output_path, index=False)
print(f"\nProcessed data saved to: {output_path}")

print("\n✓ Data collection and preprocessing complete!")
print("\nNext steps:")
print("1. Split data into train/test sets")
print("2. Train your ML model")
print("3. Evaluate and deploy")
