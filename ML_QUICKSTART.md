# 🚀 ML Quick Start Guide

Get started with machine learning data collection in **5 minutes**!

## 📦 Installation

```bash
# Install with ML dependencies
pip install tradingview-screener[ml]

# Or install separately
pip install tradingview-screener
pip install pandas pyarrow scikit-learn numpy
```

## ⚡ Quick Example

### 1. Collect Market Data

```python
from tradingview_screener import Query, col
from tradingview_screener.ml_collector import MLDataCollector

# Initialize collector
collector = MLDataCollector(output_dir='data', format='parquet')

# Define screening criteria
query = (
    Query()
    .select('name', 'close', 'volume', 'market_cap_basic', 'RSI')
    .where(
        col('market_cap_basic') > 10_000_000_000,
        col('volume') > 1_000_000,
    )
    .limit(500)
)

# Collect data
df = collector.collect_once(query, dataset_name='stocks')
```

**Output:**
```
✓ Collected 500 stocks
✓ Data saved to: data/stocks_20250117_120000.parquet
```

### 2. Add ML Features

```python
from tradingview_screener.features import preprocess_for_ml

# Complete preprocessing
df_ml = preprocess_for_ml(
    df,
    target_type='direction',  # Predict up/down
    add_technical=True,       # Add indicators
    normalize=True,           # Normalize features
)
```

**Output:**
```
✓ Added 45 features
✓ Created target variable
✓ Final shape: (485, 52)
```

### 3. Train ML Model

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Prepare data
X = df_ml.drop(columns=['target', 'ticker', 'name'])
y = df_ml['target']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train model
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# Evaluate
accuracy = model.score(X_test, y_test)
print(f"Accuracy: {accuracy:.2%}")
```

**Output:**
```
Accuracy: 62.45%
```

## 🔄 Automated Collection

Schedule data collection every hour:

```python
collector.schedule_collection(
    query=query,
    dataset_name='hourly_data',
    interval_minutes=60,
    max_collections=24,  # Run for 24 hours
)
```

## 📚 Available Features

### Data Collection
- `MLDataCollector.collect_once()` - Single collection
- `MLDataCollector.schedule_collection()` - Scheduled collection
- `MLDataCollector.collect_batch()` - Multiple datasets
- `MLDataCollector.load_historical_data()` - Load past data

### Feature Engineering
- `add_returns()` - Price returns
- `add_price_momentum()` - Momentum indicators
- `add_volume_features()` - Volume analysis
- `add_volatility()` - Historical volatility
- `add_technical_flags()` - Binary indicators
- `create_target_variable()` - ML targets
- `preprocess_for_ml()` - Complete pipeline

### Storage Formats
- **Parquet** (recommended) - Fast, compressed
- **CSV** - Human readable
- **SQLite** - Database queries

## 📖 Next Steps

1. **Explore Examples:**
   ```bash
   python examples/simple_ml_collection.py
   python examples/full_ml_pipeline.py
   ```

2. **Read Full Guide:** See [ML_GUIDE.md](ML_GUIDE.md)

3. **Customize Queries:** Check [available fields](https://shner-elmo.github.io/TradingView-Screener/fields/stocks.html)

4. **Join Community:** [GitHub Discussions](https://github.com/shner-elmo/TradingView-Screener/discussions)

## 🎯 Common Use Cases

### Stock Price Prediction
```python
query = Query().select('close', 'volume', 'RSI', 'MACD.macd').limit(500)
df = preprocess_for_ml(df, target_type='direction')
```

### Crypto Trading Bot
```python
query = Query().set_markets('crypto').select('close', 'volume', 'RSI').limit(100)
collector.schedule_collection(query, 'crypto', interval_minutes=15)
```

### Value Investing Screener
```python
query = Query().select('price_earnings_ttm', 'dividend_yield_recent').where(
    col('price_earnings_ttm').between(5, 15),
    col('dividend_yield_recent') > 3
)
```

## ❓ Need Help?

- **Documentation:** [ML_GUIDE.md](ML_GUIDE.md)
- **Issues:** [GitHub Issues](https://github.com/shner-elmo/TradingView-Screener/issues)
- **Examples:** See `examples/` directory

---

**Happy Trading! 📈🤖**
