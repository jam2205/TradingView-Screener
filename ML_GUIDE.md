# Machine Learning Data Collection Guide

Welcome to the **TradingView Screener ML Extension**! This guide will help you leverage this powerful tool for your machine learning pipeline.

## 📋 Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Core Features](#core-features)
- [ML Data Collector](#ml-data-collector)
- [Feature Engineering](#feature-engineering)
- [Configuration](#configuration)
- [Examples](#examples)
- [Best Practices](#best-practices)
- [Common Use Cases](#common-use-cases)

---

## Overview

This extension transforms the TradingView Screener into a complete **machine learning data collection framework**. It provides:

✅ **Automated Data Collection** - Schedule periodic data gathering
✅ **Multiple Storage Formats** - CSV, Parquet, SQLite
✅ **Feature Engineering** - Pre-built technical indicators and transformations
✅ **Data Validation** - Built-in quality checks
✅ **Batch Processing** - Collect multiple datasets simultaneously
✅ **Time-Series Support** - Historical data management
✅ **ML-Ready Output** - Properly formatted for scikit-learn, PyTorch, TensorFlow

---

## Quick Start

### 1. Simple Data Collection

```python
from tradingview_screener import Query, col
from tradingview_screener.ml_collector import MLDataCollector

# Initialize collector
collector = MLDataCollector(
    output_dir='data/market_data',
    format='parquet',  # Efficient for ML
)

# Define your screening criteria
query = (
    Query()
    .select('name', 'close', 'volume', 'market_cap_basic', 'RSI', 'MACD.macd')
    .where(
        col('market_cap_basic') > 10_000_000_000,  # Large cap
        col('volume') > 1_000_000,  # High volume
    )
    .limit(500)
)

# Collect data
df = collector.collect_once(query, dataset_name='large_caps')
print(f"Collected {len(df)} stocks")
```

### 2. Add ML Features

```python
from tradingview_screener.features import preprocess_for_ml

# Complete preprocessing pipeline
df_ml_ready = preprocess_for_ml(
    df,
    target_type='direction',  # Predict price direction
    target_periods=1,  # 1 day ahead
    add_technical=True,
    normalize=True,
)

# Save for training
df_ml_ready.to_parquet('data/training_data.parquet')
```

### 3. Train Your Model

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Prepare features and target
X = df_ml_ready.drop(columns=['target', 'ticker', 'name'])
y = df_ml_ready['target']

# Split and train
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = RandomForestClassifier()
model.fit(X_train, y_train)

print(f"Accuracy: {model.score(X_test, y_test):.2%}")
```

---

## Installation

### Install the package:

```bash
pip install tradingview-screener
```

### Install ML dependencies:

```bash
pip install pandas pyarrow scikit-learn
```

### Optional dependencies:

```bash
# For authentication (real-time data)
pip install rookiepy

# For deep learning
pip install torch tensorflow

# For advanced ML
pip install xgboost lightgbm catboost
```

---

## Core Features

### 1. ML Data Collector

The `MLDataCollector` class is your main interface for data collection.

```python
from tradingview_screener.ml_collector import MLDataCollector

collector = MLDataCollector(
    output_dir='data',              # Where to save data
    format='parquet',                # Storage format
    timestamp_format='%Y%m%d_%H%M%S', # Timestamp format
    add_collection_metadata=True,    # Add collection time
    validate_data=True,              # Data quality checks
    cookies=None,                    # For real-time data
)
```

#### Key Methods:

**`collect_once()`** - Collect data immediately
```python
df = collector.collect_once(
    query=query,
    dataset_name='my_dataset',
    save=True,
    callbacks=[preprocessing_function],
)
```

**`schedule_collection()`** - Automated scheduled collection
```python
collector.schedule_collection(
    query=query,
    dataset_name='hourly_data',
    interval_minutes=60,      # Every hour
    max_collections=24,        # For 24 hours
    on_error='continue',
)
```

**`collect_batch()`** - Multiple datasets at once
```python
results = collector.collect_batch(
    queries={
        'large_caps': large_cap_query,
        'small_caps': small_cap_query,
        'crypto': crypto_query,
    }
)
```

**`load_historical_data()`** - Load previously collected data
```python
historical = collector.load_historical_data(
    dataset_name='hourly_data',
    start_date=datetime(2024, 1, 1),
    end_date=datetime(2024, 12, 31),
    combine=True,
)
```

---

### 2. Feature Engineering

Pre-built feature engineering functions for financial ML.

#### Price-based Features

```python
from tradingview_screener.features import (
    add_returns,
    add_log_returns,
    add_price_momentum,
)

# Percentage returns
df = add_returns(df, price_column='close', periods=[1, 5, 10, 20])

# Log returns (better for ML)
df = add_log_returns(df, price_column='close', periods=[1, 5, 10])

# Momentum (price vs moving averages)
df = add_price_momentum(df, price_column='close', windows=[5, 10, 20, 50])
```

#### Volume Features

```python
from tradingview_screener.features import add_volume_features

df = add_volume_features(
    df,
    volume_column='volume',
    windows=[5, 10, 20],  # Average volume windows
)
# Adds: volume_avg_X, volume_relative_X
```

#### Volatility Features

```python
from tradingview_screener.features import add_volatility

df = add_volatility(
    df,
    price_column='close',
    windows=[5, 10, 20],
)
# Adds: close_volatility_X (rolling standard deviation)
```

#### Technical Flags

```python
from tradingview_screener.features import add_technical_flags

df = add_technical_flags(df)
# Adds binary flags:
# - price_above_ma20
# - volume_above_avg
# - rsi_overbought / rsi_oversold
# - macd_bullish
```

#### Normalization

```python
from tradingview_screener.features import normalize_features

df = normalize_features(
    df,
    method='robust',  # Options: standard, minmax, robust
)
```

#### Target Variable Creation

```python
from tradingview_screener.features import create_target_variable

# Binary classification: predict price direction
df = create_target_variable(
    df,
    target_type='direction',  # up or down
    periods=1,  # predict 1 day ahead
)

# Regression: predict returns
df = create_target_variable(
    df,
    target_type='return',  # actual percentage return
    periods=5,  # predict 5-day return
)

# Multi-class: predict magnitude
df = create_target_variable(
    df,
    target_type='class',  # down, neutral, up
    periods=1,
)
```

#### Complete Preprocessing Pipeline

```python
from tradingview_screener.features import preprocess_for_ml

# One function for complete preprocessing
df_ready = preprocess_for_ml(
    df,
    price_column='close',
    volume_column='volume',
    target_type='direction',
    target_periods=1,
    add_technical=True,      # Add all technical features
    normalize=True,          # Normalize features
    handle_missing='median', # Handle missing values
    remove_outlier=True,     # Remove outliers
)
```

---

### 3. Data Validation

Automatic data quality checks:

- **Empty DataFrame detection**
- **Missing value analysis**
- **Duplicate row detection**
- **Constant column detection**
- **Outlier detection**

All issues are logged automatically.

---

## Configuration

Use YAML configuration files for reproducible experiments.

**Example: `ml_config.yaml`**

```yaml
output:
  directory: "data/market_data"
  format: "parquet"

datasets:
  large_cap_momentum:
    description: "Large cap stocks with high momentum"
    market: "america"
    columns:
      - name
      - close
      - volume
      - RSI
      - MACD.macd
    filters:
      - column: "market_cap_basic"
        operation: "greater"
        value: 10000000000
    limit: 500

schedule:
  enabled: true
  interval_minutes: 60
  max_collections: 24

feature_engineering:
  returns:
    periods: [1, 5, 10]
  normalization:
    enabled: true
    method: "robust"
  target:
    type: "direction"
    periods: 1
```

---

## Examples

### Example 1: Simple Collection

See: `examples/simple_ml_collection.py`

Demonstrates basic data collection and preprocessing.

```bash
python examples/simple_ml_collection.py
```

### Example 2: Scheduled Collection

See: `examples/scheduled_collection.py`

Automated hourly data collection for time-series datasets.

```bash
python examples/scheduled_collection.py
```

### Example 3: Batch Collection

See: `examples/batch_collection.py`

Collect multiple datasets (stocks, crypto, etc.) simultaneously.

```bash
python examples/batch_collection.py
```

### Example 4: Full ML Pipeline

See: `examples/full_ml_pipeline.py`

Complete end-to-end pipeline: collection → features → training → evaluation.

```bash
python examples/full_ml_pipeline.py
```

---

## Best Practices

### 1. Data Collection Strategy

**For Backtesting:**
- Collect once and save
- Use larger datasets (1000+ stocks)
- Include multiple timeframes

**For Live Trading:**
- Schedule regular collection (every hour/day)
- Monitor data quality
- Use real-time data (with authentication)

### 2. Feature Engineering

**Do:**
- ✅ Create domain-specific features (technical indicators)
- ✅ Normalize features for better model performance
- ✅ Handle missing values appropriately
- ✅ Remove outliers carefully

**Don't:**
- ❌ Use future information (data leakage)
- ❌ Over-engineer features (curse of dimensionality)
- ❌ Ignore missing value patterns

### 3. Storage Format

| Format | Best For | Pros | Cons |
|--------|----------|------|------|
| **Parquet** | ML pipelines | Fast, compressed, typed | Requires pyarrow |
| **CSV** | Human readable | Universal, simple | Slower, larger |
| **SQLite** | Querying | SQL support, versioning | More complex |

**Recommendation:** Use **Parquet** for ML workflows.

### 4. Target Variable

**Classification Tasks:**
- Binary: `target_type='direction'` (up/down)
- Multi-class: `target_type='class'` (down/neutral/up)

**Regression Tasks:**
- Returns: `target_type='return'`

**Choosing Prediction Horizon:**
- Short-term (1-5 days): More noise, harder to predict
- Medium-term (5-20 days): Good balance
- Long-term (20+ days): Smoother trends, less frequent signals

### 5. Data Quality

Always validate:
1. **Missing values** - Use `validate_data=True` in collector
2. **Outliers** - Remove or cap extreme values
3. **Duplicates** - Check for duplicate tickers/timestamps
4. **Stale data** - Monitor `update_mode` field

---

## Common Use Cases

### Use Case 1: Price Direction Prediction

**Goal:** Predict if stock price will go up or down tomorrow

```python
query = Query().select('name', 'close', 'volume', 'RSI', 'MACD.macd').limit(500)
df = collector.collect_once(query, 'price_prediction')
df = preprocess_for_ml(df, target_type='direction', target_periods=1)

# Train binary classifier
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier()
# ... train model
```

### Use Case 2: Momentum Trading Signals

**Goal:** Identify stocks with strong momentum for swing trading

```python
query = (
    Query()
    .select('name', 'close', 'volume', 'relative_volume_10d_calc', 'Perf.W', 'Perf.1M')
    .where(
        col('relative_volume_10d_calc') > 1.5,
        col('Perf.W') > 5,
    )
    .limit(100)
)

df = collector.collect_once(query, 'momentum_stocks')
```

### Use Case 3: Value Investing Screener

**Goal:** Find undervalued stocks with good fundamentals

```python
query = (
    Query()
    .select('name', 'close', 'price_earnings_ttm', 'price_book_fq',
            'dividend_yield_recent', 'debt_to_equity')
    .where(
        col('price_earnings_ttm').between(5, 15),
        col('price_book_fq') < 2,
        col('dividend_yield_recent') > 3,
    )
    .limit(200)
)
```

### Use Case 4: Crypto Trading Bot

**Goal:** Build ML model for cryptocurrency trading

```python
query = (
    Query()
    .set_markets('crypto')
    .select('name', 'close', 'volume', 'RSI', 'MACD.macd', 'Perf.W')
    .where(col('market_cap_calc') > 100_000_000)
    .limit(100)
)

# Schedule hourly collection
collector.schedule_collection(
    query=query,
    dataset_name='crypto_hourly',
    interval_minutes=60,
    max_collections=None,  # Run indefinitely
)
```

### Use Case 5: Portfolio Optimization

**Goal:** Collect data for portfolio allocation models

```python
queries = {
    'large_cap': Query().where(col('market_cap_basic') > 10e9).limit(500),
    'mid_cap': Query().where(col('market_cap_basic').between(2e9, 10e9)).limit(300),
    'small_cap': Query().where(col('market_cap_basic').between(300e6, 2e9)).limit(200),
}

# Collect all at once
data = collector.collect_batch(queries)

# Calculate correlations, optimize allocations, etc.
```

---

## Advanced Topics

### Real-Time Data Collection

For real-time data, you need TradingView authentication:

```python
import rookiepy

# Load cookies from browser
cookies = rookiepy.to_cookiejar(rookiepy.chrome(['.tradingview.com']))

collector = MLDataCollector(cookies=cookies)
df = collector.collect_once(query)  # Real-time data!
```

### Custom Callbacks

Apply custom transformations during collection:

```python
def custom_feature_engineering(df):
    # Your custom logic
    df['custom_ratio'] = df['close'] / df['volume']
    return df

df = collector.collect_once(
    query,
    callbacks=[custom_feature_engineering]
)
```

### Panel Data (Multiple Time Points)

For time-series models:

```python
from tradingview_screener.features import create_lagged_features

# Collect multiple snapshots
collector.schedule_collection(query, 'daily_data', interval_minutes=1440)

# Load and create panel
df = collector.load_historical_data('daily_data', combine=True)

# Add lagged features
df = create_lagged_features(
    df,
    columns=['close', 'volume'],
    lags=[1, 2, 3, 5],
    group_by='ticker',  # Important for panel data!
)
```

---

## Troubleshooting

### Issue: Missing values in collected data

**Cause:** Not all stocks have all fields (e.g., small caps may not have analyst ratings)

**Solution:**
```python
from tradingview_screener.features import handle_missing_values
df = handle_missing_values(df, strategy='median')
```

### Issue: API rate limiting

**Cause:** Too many requests in short time

**Solution:**
- Use `interval_minutes` > 5 for scheduled collection
- Limit query results (don't request 10,000 stocks)
- Add delays between batch collections

### Issue: Stale data

**Cause:** Using delayed data without authentication

**Solution:**
- Authenticate with TradingView (see Real-Time Data section)
- Check `update_mode` field
- Consider data freshness in your model

---

## Next Steps

1. **Start Simple** - Run `examples/simple_ml_collection.py`
2. **Customize** - Modify queries for your use case
3. **Automate** - Set up scheduled collection
4. **Experiment** - Try different features and models
5. **Deploy** - Build your trading system!

---

## Resources

- [Main README](README.md) - TradingView Screener documentation
- [API Fields](https://shner-elmo.github.io/TradingView-Screener/fields/stocks.html) - All available fields
- [Examples](examples/) - Complete example scripts
- [GitHub Issues](https://github.com/shner-elmo/TradingView-Screener/issues) - Report bugs or request features

---

## Contributing

Have ideas for ML features? Open an issue or submit a PR!

**Potential improvements:**
- Additional feature engineering functions
- Integration with popular ML frameworks
- Hyperparameter optimization helpers
- Backtesting framework
- Real-time prediction API

---

**Happy Machine Learning! 🚀📈**
