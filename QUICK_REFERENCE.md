# 🚀 Quick Reference - Multi-Asset Scanner

One-page reference for your custom market scanner!

---

## ⚡ Quick Start Commands

### Launch Web Dashboard
```bash
streamlit run multi_asset_dashboard.py
```

### Run Example Script
```bash
python examples/multi_asset_scanner_example.py
```

---

## 📊 Your Markets

### Scan ALL Your Markets (One Line!)
```python
from tradingview_screener.multi_asset_scanner import scan_all_your_markets

# Scan everything on 4-hour timeframe
results = scan_all_your_markets(timeframe='4hr')

print(results['commodities'])  # Gold, Silver
print(results['indices'])      # NASDAQ, SP500, YM30
print(results['forex'])         # GBP/JPY, EUR/USD, AUD/USD, USD/JPY
print(results['bonds'])         # US Treasuries
```

---

## 🎯 Individual Market Scans

### Gold & Silver
```python
from tradingview_screener.multi_asset_scanner import scan_gold_silver

df = scan_gold_silver(timeframe='1hr')
print(df)
```

### Indices (NASDAQ, SP500, YM30)
```python
from tradingview_screener.multi_asset_scanner import scan_major_indices

df = scan_major_indices(timeframe='daily')
print(df)
```

### Forex (GBP/JPY, EUR/USD, AUD/USD, USD/JPY)
```python
from tradingview_screener.multi_asset_scanner import scan_major_forex

df = scan_major_forex(timeframe='4hr')
print(df)
```

### US Bonds
```python
from tradingview_screener.multi_asset_scanner import scan_treasuries

df = scan_treasuries(timeframe='daily')
print(df)
```

---

## ⏰ Timeframes Available

| Timeframe | Use For | Example |
|-----------|---------|---------|
| `'5min'` | Scalping | `scan_all_your_markets('5min')` |
| `'15min'` | Day trading | `scan_all_your_markets('15min')` |
| `'1hr'` | Intraday | `scan_all_your_markets('1hr')` |
| `'4hr'` | Swing entries | `scan_all_your_markets('4hr')` |
| `'daily'` | Swing/position | `scan_all_your_markets('daily')` |
| `'weekly'` | Position trading | `scan_all_your_markets('weekly')` |
| `'monthly'` | Long-term | `scan_all_your_markets('monthly')` |

---

## 🔧 Custom Scans

### Scan Specific Symbols
```python
from tradingview_screener.multi_asset_scanner import MultiAssetScanner

scanner = MultiAssetScanner()

# Your custom watchlist
watchlist = ['GOLD', 'SILVER', 'SP500', 'NASDAQ', 'GBPJPY', 'EURUSD']

df = scanner.scan_symbols(watchlist, timeframe='4hr')
print(df)
```

### Multi-Timeframe Analysis
```python
scanner = MultiAssetScanner()

# Scan Gold on multiple timeframes
results = scanner.scan_multi_timeframe(
    symbols=['GOLD'],
    timeframes=['1hr', '4hr', 'daily', 'weekly']
)

for tf, df in results.items():
    print(f"\n{tf} Data:")
    print(df)
```

---

## 📋 Symbol List

### Your Commodities
- `'GOLD'` - Gold Spot
- `'SILVER'` - Silver Spot

### Your Indices
- `'NASDAQ'` - NASDAQ 100
- `'SP500'` - S&P 500
- `'YM30'` - Dow Jones E-mini Futures

### Your Forex Pairs
- `'GBPJPY'` - British Pound / Japanese Yen
- `'EURUSD'` - Euro / US Dollar
- `'AUDUSD'` - Australian Dollar / US Dollar
- `'USDJPY'` - US Dollar / Japanese Yen

### Your Bonds
- `'US10Y'` - US 10-Year Treasury
- `'US30Y'` - US 30-Year Treasury
- `'US02Y'` - US 2-Year Treasury

---

## 💾 Export Data

### Save to CSV
```python
df = scan_all_your_markets(timeframe='daily')

# Save each market
df['commodities'].to_csv('gold_silver_daily.csv', index=False)
df['indices'].to_csv('indices_daily.csv', index=False)
df['forex'].to_csv('forex_daily.csv', index=False)
df['bonds'].to_csv('bonds_daily.csv', index=False)
```

### Save All Timeframes
```python
scanner = MultiAssetScanner()
timeframes = ['5min', '15min', '1hr', '4hr', 'daily']

for tf in timeframes:
    df = scan_all_your_markets(timeframe=tf)
    # Save each market for this timeframe
    for market, data in df.items():
        data.to_csv(f'{market}_{tf}.csv', index=False)
```

---

## 🔐 Real-Time Data (Optional)

### Add Your TradingView Cookie
```python
# Get your sessionid from TradingView.com
cookies = {'sessionid': 'your_session_id_here'}

# Use with any scan
results = scan_all_your_markets(timeframe='5min', cookies=cookies)
```

**Without cookie:** 15-minute delayed data
**With cookie:** Real-time data!

---

## 📊 Common Workflows

### Morning Market Scan
```python
from tradingview_screener.multi_asset_scanner import scan_all_your_markets

# Get daily overview
results = scan_all_your_markets(timeframe='daily')

print("📊 MARKET OVERVIEW")
print("\nCommodities:", results['commodities'][['name', 'close', 'change']])
print("\nIndices:", results['indices'][['name', 'close', 'change']])
print("\nForex:", results['forex'][['name', 'close', 'change']])
print("\nBonds:", results['bonds'][['name', 'close', 'change']])
```

### Intraday Setup
```python
scanner = MultiAssetScanner()

# 5-min for entries, 1-hr for trend
data_5min = scanner.scan_symbols(['GOLD', 'GBPJPY'], timeframe='5min')
data_1hr = scanner.scan_symbols(['GOLD', 'GBPJPY'], timeframe='1hr')

print("Entry (5-min):", data_5min)
print("Trend (1-hr):", data_1hr)
```

### Weekly Review
```python
scanner = MultiAssetScanner()

# Compare weekly vs monthly
weekly = scanner.scan_symbols(['GOLD', 'SP500', 'US10Y'], timeframe='weekly')
monthly = scanner.scan_symbols(['GOLD', 'SP500', 'US10Y'], timeframe='monthly')

print("Weekly:", weekly)
print("Monthly:", monthly)
```

---

## 🌐 Web Dashboard Quick Reference

### Launch Dashboard
```bash
streamlit run multi_asset_dashboard.py
```

### Tabs Available
1. **📊 Dashboard** - Overview of all markets
2. **🥇 Commodities** - Gold, silver, oil
3. **📈 Indices** - NASDAQ, SP500, YM30
4. **💱 Forex** - GBP/JPY, EUR/USD, etc.
5. **🏦 Bonds** - US Treasuries
6. **⏰ Multi-Timeframe** - Compare timeframes
7. **⚙️ Custom Scan** - Build your own

### Quick Actions
- Upload cookie in sidebar
- Select timeframe
- Click "Scan All Markets"
- Download CSV for any market

---

## 🎯 Pro Tips

### 1. Multi-Market Correlation
```python
# Scan related markets together
scanner = MultiAssetScanner()
df = scanner.scan_symbols(
    ['GOLD', 'DX', 'US10Y'],  # Gold, Dollar Index, Bonds
    timeframe='daily'
)
# Gold typically inverse to Dollar & Yields
```

### 2. Multi-Timeframe Confirmation
```python
# Check alignment across timeframes
scanner = MultiAssetScanner()
results = scanner.scan_multi_timeframe(
    ['GBPJPY'],
    timeframes=['1hr', '4hr', 'daily']
)
# Daily = trend, 4hr = setup, 1hr = entry
```

### 3. Risk-On / Risk-Off
```python
scanner = MultiAssetScanner()

# Risk-on assets
risk_on = scanner.scan_symbols(['SP500', 'AUDUSD'], 'daily')

# Risk-off assets
risk_off = scanner.scan_symbols(['GOLD', 'USDJPY'], 'daily')
```

---

## 📚 Full Documentation

- **Complete Guide:** [MULTI_ASSET_GUIDE.md](MULTI_ASSET_GUIDE.md)
- **Example Script:** [examples/multi_asset_scanner_example.py](examples/multi_asset_scanner_example.py)
- **ML Guide:** [ML_GUIDE.md](ML_GUIDE.md)
- **Colab Notebook:** [TradingView_ML_Collector.ipynb](TradingView_ML_Collector.ipynb)

---

## ⚡ One-Liners for Common Tasks

```python
# Scan all markets on 4-hour
scan_all_your_markets('4hr')

# Just gold and silver daily
scan_gold_silver('daily')

# Forex on 1-hour
scan_major_forex('1hr')

# Indices daily
scan_major_indices('daily')

# Bonds daily
scan_treasuries('daily')

# Custom watchlist
MultiAssetScanner().scan_symbols(['GOLD', 'SP500', 'GBPJPY'], '4hr')

# Multi-timeframe gold
MultiAssetScanner().scan_multi_timeframe(['GOLD'], ['1hr', '4hr', 'daily'])
```

---

**Print this page for quick reference! 📄**
