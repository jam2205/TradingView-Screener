"""
Batch Data Collection Example

Collect multiple datasets simultaneously for comprehensive market coverage.
"""
from tradingview_screener import Query, col
from tradingview_screener.ml_collector import MLDataCollector
from tradingview_screener.features import add_returns, add_technical_flags

# Initialize collector
collector = MLDataCollector(
    output_dir='data/batch_collection',
    format='parquet',
)

# Define multiple datasets with different strategies
datasets = {
    # Large cap momentum
    'large_cap_momentum': (
        Query()
        .select('name', 'close', 'volume', 'market_cap_basic', 'RSI', 'MACD.macd', 'MACD.signal')
        .where(
            col('market_cap_basic') > 10_000_000_000,
            col('volume') > 1_000_000,
            col('relative_volume_10d_calc') > 1.2,
        )
        .order_by('volume', ascending=False)
        .limit(500)
    ),

    # Small cap growth
    'small_cap_growth': (
        Query()
        .select('name', 'close', 'volume', 'market_cap_basic', 'Perf.1M', 'Perf.3M', 'price_earnings_ttm')
        .where(
            col('market_cap_basic').between(100_000_000, 2_000_000_000),
            col('volume') > 100_000,
            col('Perf.3M') > 10,
        )
        .order_by('Perf.3M', ascending=False)
        .limit(300)
    ),

    # High RSI (overbought)
    'overbought_stocks': (
        Query()
        .select('name', 'close', 'volume', 'RSI', 'market_cap_basic')
        .where(
            col('RSI') > 70,
            col('volume') > 500_000,
        )
        .order_by('RSI', ascending=False)
        .limit(200)
    ),

    # High dividend yield
    'high_dividend': (
        Query()
        .select('name', 'close', 'dividend_yield_recent', 'market_cap_basic', 'price_earnings_ttm')
        .where(
            col('dividend_yield_recent') > 4,
            col('market_cap_basic') > 1_000_000_000,
        )
        .order_by('dividend_yield_recent', ascending=False)
        .limit(200)
    ),

    # Crypto momentum
    'crypto_momentum': (
        Query()
        .set_markets('crypto')
        .select('name', 'close', 'volume', 'market_cap_calc', 'RSI', 'Perf.W', 'Perf.1M')
        .where(
            col('market_cap_calc') > 100_000_000,
            col('relative_volume_10d_calc') > 1.5,
        )
        .order_by('volume', ascending=False)
        .limit(150)
    ),
}

# Define custom preprocessing for each dataset
callbacks = {
    'large_cap_momentum': [
        lambda df: add_returns(df, periods=[1, 5, 10]),
        lambda df: add_technical_flags(df),
    ],
    'small_cap_growth': [
        lambda df: add_returns(df, periods=[1, 5, 10]),
    ],
    'crypto_momentum': [
        lambda df: add_returns(df, periods=[1, 5]),
    ],
}

# Collect all datasets in batch
print(f"Collecting {len(datasets)} datasets in batch...\n")

results = collector.collect_batch(
    queries=datasets,
    callbacks=callbacks,
)

# Print summary
print("\n" + "="*60)
print("BATCH COLLECTION SUMMARY")
print("="*60)

for dataset_name, df in results.items():
    print(f"\n{dataset_name}:")
    print(f"  Rows: {len(df)}")
    print(f"  Columns: {len(df.columns)}")
    print(f"  Sample: {list(df['name'].head(3))}")

print("\n✓ Batch collection complete!")
print(f"✓ Successfully collected {len(results)}/{len(datasets)} datasets")
print(f"✓ Data saved to: {collector.output_dir}")
