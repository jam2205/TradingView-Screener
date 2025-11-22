# 📊 Multi-Asset Multi-Timeframe Scanner Guide

Scan **bonds, commodities, indices, and forex** across **multiple timeframes**!

---

## 🎯 Your Custom Markets

This scanner is configured for your specific markets:

### 🥇 Commodities
- **Gold** (spot & futures)
- **Silver** (spot & futures)

### 📈 Indices
- **NASDAQ** 100
- **S&P 500**
- **YM30** (Dow Jones E-mini futures)

### 💱 Forex Pairs
- **GBP/JPY** - British Pound / Japanese Yen
- **EUR/USD** - Euro / US Dollar
- **AUD/USD** - Australian Dollar / US Dollar
- **USD/JPY** - US Dollar / Japanese Yen

### 🏦 Bonds
- **US Treasuries** (2Y, 5Y, 10Y, 30Y)
- **US Dollar Index**

### ⏰ Timeframes
- **5min** - 5-minute bars
- **15min** - 15-minute bars
- **1hr** - 1-hour bars
- **4hr** - 4-hour bars
- **daily** - Daily bars
- **weekly** - Weekly bars
- **monthly** - Monthly bars

---

## 🚀 Quick Start

### Option 1: Web Dashboard (Easiest!)

```bash
streamlit run multi_asset_dashboard.py
```

Opens at: `http://localhost:8501`

**Features:**
- ✅ Click-to-scan all markets
- ✅ Interactive tables
- ✅ Multi-timeframe tabs
- ✅ Download CSV
- ✅ Cookie upload for real-time data

### Option 2: Python Script

```python
from tradingview_screener.multi_asset_scanner import scan_all_your_markets

# Scan all your markets on daily timeframe
results = scan_all_your_markets(timeframe='daily')

print(results['commodities'])  # Gold, Silver
print(results['indices'])      # NASDAQ, SP500, YM30
print(results['forex'])         # GBP/JPY, EUR/USD, etc.
print(results['bonds'])         # US Treasuries
```

### Option 3: Custom Scanning

```python
from tradingview_screener.multi_asset_scanner import MultiAssetScanner

scanner = MultiAssetScanner()

# Scan specific symbols
df = scanner.scan_symbols(
    ['GOLD', 'SILVER', 'SP500', 'NASDAQ', 'GBPJPY'],
    timeframe='4hr'
)
print(df)
```

---

## 📖 Usage Examples

### Example 1: Quick Market Overview

```python
from tradingview_screener.multi_asset_scanner import (
    scan_gold_silver,
    scan_major_indices,
    scan_major_forex,
    scan_treasuries
)

# Quick scans
gold_silver = scan_gold_silver(timeframe='daily')
indices = scan_major_indices(timeframe='daily')
forex = scan_major_forex(timeframe='daily')
bonds = scan_treasuries(timeframe='daily')

print("Gold & Silver:", gold_silver)
print("Indices:", indices)
print("Forex:", forex)
print("Bonds:", bonds)
```

### Example 2: Multi-Timeframe Analysis

```python
from tradingview_screener.multi_asset_scanner import MultiAssetScanner

scanner = MultiAssetScanner()

# Scan Gold on multiple timeframes
gold_timeframes = scanner.scan_multi_timeframe(
    symbols=['GOLD'],
    timeframes=['1hr', '4hr', 'daily', 'weekly']
)

for tf, df in gold_timeframes.items():
    print(f"\n{tf.upper()} Data:")
    print(df)
```

### Example 3: Scan All Your Markets

```python
from tradingview_screener.multi_asset_scanner import scan_all_your_markets

# Get all markets on 4-hour timeframe
results = scan_all_your_markets(timeframe='4hr')

# Access each market
commodities = results['commodities']  # Gold, Silver
indices = results['indices']          # NASDAQ, SP500, YM30
forex = results['forex']               # GBP/JPY, EUR/USD, AUD/USD, USD/JPY
bonds = results['bonds']               # US Treasuries

# Export to CSV
commodities.to_csv('commodities_4hr.csv', index=False)
forex.to_csv('forex_4hr.csv', index=False)
```

### Example 4: Intraday Trading Setup (5min & 15min)

```python
scanner = MultiAssetScanner()

# Your trading watchlist
watchlist = ['GOLD', 'SILVER', 'GBPJPY', 'EURUSD', 'SP500']

# Scan on intraday timeframes
data_5min = scanner.scan_symbols(watchlist, timeframe='5min')
data_15min = scanner.scan_symbols(watchlist, timeframe='15min')

print("5-Minute Data:")
print(data_5min)

print("\n15-Minute Data:")
print(data_15min)
```

### Example 5: Swing Trading Setup (4hr & Daily)

```python
scanner = MultiAssetScanner()

# Swing trading symbols
symbols = ['GOLD', 'SILVER', 'NASDAQ', 'SP500', 'GBPJPY']

# 4-hour for entries
data_4hr = scanner.scan_symbols(symbols, timeframe='4hr')

# Daily for trend
data_daily = scanner.scan_symbols(symbols, timeframe='daily')

print("4-Hour (Entry):")
print(data_4hr[['name', 'close', 'RSI', 'MACD.macd']])

print("\nDaily (Trend):")
print(data_daily[['name', 'close', 'EMA20', 'EMA50']])
```

### Example 6: Position Trading (Weekly & Monthly)

```python
scanner = MultiAssetScanner()

# Long-term view
symbols = ['GOLD', 'SP500', 'US10Y', 'US30Y']

weekly = scanner.scan_symbols(symbols, timeframe='weekly')
monthly = scanner.scan_symbols(symbols, timeframe='monthly')

print("Weekly:")
print(weekly)

print("\nMonthly:")
print(monthly)
```

---

## 🎯 Complete Example Script

See: `examples/multi_asset_scanner_example.py`

```bash
python examples/multi_asset_scanner_example.py
```

This runs all examples and shows:
- Daily scan of all markets
- Multi-timeframe analysis
- Forex comparison
- Indices overview
- Bond market data
- Export to CSV

---

## 🌐 Web Dashboard Features

Launch the dashboard:
```bash
streamlit run multi_asset_dashboard.py
```

### Tabs Available:

**1. 📊 Dashboard Tab**
- One-click scan all markets
- Overview metrics
- All data in one view

**2. 🥇 Commodities Tab**
- Select specific commodities
- Choose timeframe
- Instant scan

**3. 📈 Indices Tab**
- Major indices
- Futures contracts
- Timeframe selection

**4. 💱 Forex Tab**
- All major pairs
- Your custom pairs highlighted
- Multi-timeframe

**5. 🏦 Bonds Tab**
- US Treasuries (2Y, 5Y, 10Y, 30Y)
- Dollar index
- Yield curve analysis

**6. ⏰ Multi-Timeframe Tab**
- Scan across multiple timeframes
- Compare timeframe data
- Export each timeframe

**7. ⚙️ Custom Scan Tab**
- Build custom watchlists
- Any symbols
- Any timeframe

---

## 📊 Available Data Fields

When scanning, you get:

### Price Data (per timeframe)
- `close` - Closing price
- `open` - Opening price
- `high` - High price
- `low` - Low price
- `change` - Percentage change

### Volume
- `volume` - Trading volume

### Technical Indicators (per timeframe)
- `RSI` - Relative Strength Index
- `MACD.macd` - MACD line
- `MACD.signal` - Signal line
- `EMA5` - 5-period EMA
- `EMA20` - 20-period EMA
- `EMA50` - 50-period EMA
- `EMA200` - 200-period EMA

---

## 🔧 Symbol Reference

### Commodities

| Short Name | Full Symbol | Description |
|------------|-------------|-------------|
| GOLD | TVC:GOLD | Gold Spot |
| GOLD_FUTURES | COMEX:GC1! | Gold Futures |
| SILVER | TVC:SILVER | Silver Spot |
| SILVER_FUTURES | COMEX:SI1! | Silver Futures |
| OIL | TVC:USOIL | Crude Oil |
| NATGAS | NYMEX:NG1! | Natural Gas |

### Indices

| Short Name | Full Symbol | Description |
|------------|-------------|-------------|
| SP500 | SP:SPX | S&P 500 Index |
| NASDAQ | NASDAQ:NDX | NASDAQ 100 |
| DOW | TVC:DJI | Dow Jones |
| YM30 | CBOT_MINI:YM1! | E-mini Dow Futures |
| ES | CME_MINI:ES1! | E-mini S&P 500 |
| NQ | CME_MINI:NQ1! | E-mini NASDAQ |

### Forex

| Short Name | Full Symbol | Description |
|------------|-------------|-------------|
| EURUSD | FX_IDC:EURUSD | Euro / US Dollar |
| GBPJPY | FX_IDC:GBPJPY | British Pound / Yen |
| GBPUSD | FX_IDC:GBPUSD | British Pound / Dollar |
| USDJPY | FX_IDC:USDJPY | US Dollar / Yen |
| AUDUSD | FX_IDC:AUDUSD | Aussie Dollar / USD |
| EURJPY | FX_IDC:EURJPY | Euro / Yen |
| AUDJPY | FX_IDC:AUDJPY | Aussie Dollar / Yen |

### Bonds

| Short Name | Full Symbol | Description |
|------------|-------------|-------------|
| US02Y | TVC:US02Y | 2-Year Treasury |
| US05Y | TVC:US05Y | 5-Year Treasury |
| US10Y | TVC:US10Y | 10-Year Treasury |
| US30Y | TVC:US30Y | 30-Year Treasury |
| DX | TVC:DXY | US Dollar Index |

---

## 🎯 Trading Strategies

### Strategy 1: Multi-Market Correlation

```python
scanner = MultiAssetScanner()

# Scan related markets
gold = scanner.scan_symbols(['GOLD'], timeframe='daily')
dollar = scanner.scan_symbols(['DX'], timeframe='daily')
bonds = scanner.scan_symbols(['US10Y'], timeframe='daily')

# Analyze correlation
# Gold typically inversely correlated with Dollar & Yields
```

### Strategy 2: Multi-Timeframe Confirmation

```python
scanner = MultiAssetScanner()

symbol = 'GBPJPY'

# Get multiple timeframes
data_1hr = scanner.scan_symbols([symbol], timeframe='1hr')
data_4hr = scanner.scan_symbols([symbol], timeframe='4hr')
data_daily = scanner.scan_symbols([symbol], timeframe='daily')

# Look for alignment
# - Daily: trend direction
# - 4hr: entry setup
# - 1hr: precise entry
```

### Strategy 3: Risk-On / Risk-Off Monitor

```python
scanner = MultiAssetScanner()

# Risk-On assets
risk_on = scanner.scan_symbols(['SP500', 'NASDAQ', 'AUDUSD'], timeframe='daily')

# Risk-Off assets
risk_off = scanner.scan_symbols(['GOLD', 'US10Y', 'USDJPY'], timeframe='daily')

# Compare performance
```

---

## 💾 Export & Automation

### Export to CSV

```python
scanner = MultiAssetScanner()
df = scanner.scan_symbols(['GOLD', 'SILVER'], timeframe='daily')

# Export
df.to_csv('gold_silver_daily.csv', index=False)
```

### Scheduled Scanning

```python
import time
from datetime import datetime

scanner = MultiAssetScanner()
symbols = ['GOLD', 'SILVER', 'GBPJPY', 'SP500']

# Scan every hour
while True:
    print(f"Scanning at {datetime.now()}")

    df = scanner.scan_symbols(symbols, timeframe='1hr')

    # Save with timestamp
    filename = f'scan_{datetime.now().strftime("%Y%m%d_%H%M")}.csv'
    df.to_csv(filename, index=False)

    print(f"Saved to {filename}")

    time.sleep(3600)  # Wait 1 hour
```

### Batch Export All Timeframes

```python
scanner = MultiAssetScanner()
symbols = ['GOLD', 'SILVER', 'SP500', 'GBPJPY']
timeframes = ['1hr', '4hr', 'daily', 'weekly']

for tf in timeframes:
    df = scanner.scan_symbols(symbols, timeframe=tf)
    df.to_csv(f'markets_{tf}.csv', index=False)
    print(f"✓ Exported {tf}")
```

---

## 🔐 Authentication (For Real-Time Data)

**Without authentication:** 15-minute delayed data
**With authentication:** Real-time data

### Add Your Cookie:

```python
# Method 1: Direct in code
cookies = {'sessionid': 'your_session_id_here'}
scanner = MultiAssetScanner(cookies=cookies)

# Method 2: Use convenience functions
results = scan_all_your_markets(timeframe='1hr', cookies=cookies)
```

### Get Your Session ID:

1. Go to TradingView.com (logged in)
2. Press F12 → Application → Cookies
3. Copy `sessionid` value
4. Use in scanner

---

## 📚 Full API Reference

### MultiAssetScanner Class

```python
scanner = MultiAssetScanner(cookies=None)
```

**Methods:**

- `scan_symbols(symbols, timeframe)` - Scan specific symbols
- `scan_forex(pairs, timeframe)` - Scan forex pairs
- `scan_indices(indices, timeframe)` - Scan indices
- `scan_commodities(commodities, timeframe)` - Scan commodities
- `scan_bonds(bonds, timeframe)` - Scan bonds
- `scan_multi_timeframe(symbols, timeframes)` - Multi-TF scan
- `scan_all_markets(timeframe)` - Scan everything

### Convenience Functions

```python
# Quick scans
scan_gold_silver(timeframe, cookies)
scan_major_indices(timeframe, cookies)
scan_major_forex(timeframe, cookies)
scan_treasuries(timeframe, cookies)
scan_all_your_markets(timeframe, cookies)
```

---

## 🎉 You're Ready!

Start scanning your markets:

**Easiest:** Launch the dashboard
```bash
streamlit run multi_asset_dashboard.py
```

**Quick scan:** Run the example
```bash
python examples/multi_asset_scanner_example.py
```

**Custom:** Use the Python API
```python
from tradingview_screener.multi_asset_scanner import scan_all_your_markets
results = scan_all_your_markets(timeframe='4hr')
```

---

**Happy Trading! 📊💰🚀**
