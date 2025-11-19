# 📊 Live TradingView Scanner - Web App Guide

A beautiful web interface for real-time market scanning with cookie authentication!

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements-webapp.txt
```

Or install manually:
```bash
pip install streamlit pandas tradingview-screener
```

### 2. Launch the Web App

```bash
streamlit run live_scanner_app.py
```

The app will open in your browser at `http://localhost:8501`

---

## 🔐 Getting Your TradingView Cookie

To access **real-time/live data**, you need to authenticate with your TradingView session cookie.

### Method 1: Manual Cookie Extraction (Recommended)

1. **Go to [TradingView.com](https://www.tradingview.com)**
2. **Log in** to your account
3. **Open Developer Tools:**
   - Chrome/Edge: Press `F12` or `Ctrl+Shift+I`
   - Firefox: Press `F12` or `Ctrl+Shift+K`
   - Safari: Enable Developer menu first, then press `Cmd+Option+I`

4. **Navigate to Application/Storage tab:**
   - Chrome/Edge: Click "Application" tab
   - Firefox: Click "Storage" tab
   - Safari: Click "Storage" tab

5. **Find Cookies:**
   - Expand "Cookies" in the left sidebar
   - Click on `https://www.tradingview.com`

6. **Copy the sessionid:**
   - Find the row with Name: `sessionid`
   - Copy the **Value** (it's a long string like: `abc123xyz...`)

7. **Paste in the app:**
   - In the sidebar, select "Session Cookie"
   - Paste the sessionid value
   - Click "Authenticate"

### Method 2: Cookie JSON File

1. Create a JSON file with your cookie:

```json
{
  "sessionid": "your_session_id_here"
}
```

2. Save it as `tradingview_cookie.json`

3. In the app:
   - Select "Cookie JSON File"
   - Upload your JSON file

### Method 3: No Authentication (Delayed Data)

If you don't need real-time data, you can use delayed data (15-minute delay):
- Select "No Authentication (Delayed Data)"
- Click "Continue with delayed data"

---

## 🎯 Features

### 🔍 Live Scanner Tab

**Custom scanning with real-time filters:**

- **Market Selection:** Stocks, Crypto, Forex, Futures, Bonds
- **Column Selection:** Choose which data points to display
- **Filters:**
  - Minimum Volume
  - Minimum Market Cap
  - Minimum Relative Volume
  - Result Limit

- **Auto-Scan:** Enable automatic scanning at regular intervals (30s to 10min)
- **Live Updates:** See scan history and latest results

### 📈 Preset Scans Tab

**7 ready-to-use scanning strategies:**

1. 🚀 **Large Cap Momentum** - High-volume large caps
2. 💎 **Small Cap Growth** - Growth potential small caps
3. 📊 **High Volume Breakout** - Unusual volume spikes
4. 🔥 **Overbought Stocks** - RSI > 70
5. ❄️ **Oversold Stocks** - RSI < 30
6. 💰 **Value Stocks** - Good fundamentals
7. 🪙 **Crypto Momentum** - High-momentum cryptocurrencies

**Usage:** Just click "Run" on any preset to execute!

### 📊 Data View Tab

**Interactive data analysis:**

- Summary statistics
- Column filtering
- Custom sorting
- Statistical analysis (mean, median, std dev)
- Full data table view

### ⚙️ Settings Tab

**Configuration options:**

- Export format selection
- Auto-save settings
- Cookie management
- Connection testing
- Data clearing

---

## 💾 Export Data

All scans can be downloaded in multiple formats:

- **CSV** - Universal format
- **Parquet** - Efficient ML format
- **JSON** - Structured data

Click the download buttons below scan results!

---

## 🎨 Interface Overview

### Sidebar
- **Authentication panel** - Upload/enter your cookie
- **Authentication status** - See connection status
- **Logout button** - Clear session

### Main Tabs
1. **Live Scanner** - Custom queries
2. **Preset Scans** - Quick strategies
3. **Data View** - Analyze results
4. **Settings** - Configure app

---

## 📋 Example Workflows

### Workflow 1: Find High-Volume Stocks

1. Authenticate with your cookie
2. Go to "Live Scanner" tab
3. Set filters:
   - Min Volume: 5,000,000
   - Min Market Cap: $1B
   - Min Relative Volume: 1.5
4. Click "Run Scan Now"
5. View results and download CSV

### Workflow 2: Monitor Crypto Markets

1. Authenticate
2. Go to "Preset Scans"
3. Click "Run 🪙 Crypto Momentum"
4. Switch to "Data View" tab
5. Sort by volume or change%
6. Download data

### Workflow 3: Auto-Monitoring

1. Set up your custom scan in "Live Scanner"
2. Enable "Auto-scan" checkbox
3. Select refresh interval (e.g., 60s)
4. Let it run - it will auto-refresh!

---

## 🔧 Troubleshooting

### Issue: "Connection failed"

**Cause:** Invalid or expired cookie

**Solution:**
1. Get a fresh cookie from TradingView
2. Make sure you're logged in
3. Copy the exact sessionid value

### Issue: "No data returned"

**Cause:** Filters are too restrictive

**Solution:**
- Reduce minimum values
- Increase result limit
- Try a preset scan first

### Issue: "App won't start"

**Cause:** Missing dependencies

**Solution:**
```bash
pip install -r requirements-webapp.txt
```

### Issue: "Delayed data only"

**Cause:** Not authenticated

**Solution:**
- Upload your session cookie
- Or accept 15-minute delayed data

---

## 🎯 Pro Tips

### 1. Real-time Data
- **Free accounts** get real-time data for most US exchanges after authentication
- **Pro accounts** get real-time data for more exchanges
- Check the `update_mode` column to see data freshness

### 2. Auto-Scanning
- Use 60s or higher intervals to avoid rate limiting
- Perfect for monitoring specific strategies
- Keep the browser tab open for continuous scanning

### 3. Combining Filters
- Stack multiple filters for precise screening
- Example: High volume + Low RSI = Oversold bounce candidates

### 4. Export & Analyze
- Export to Parquet for ML pipelines
- Export to CSV for Excel analysis
- Export to JSON for web apps

### 5. Cookie Security
- Never share your session cookie
- Cookies expire - get a fresh one if errors occur
- Use JSON file upload for easier re-authentication

---

## 🌐 Accessing Remotely

### Run on a Server

```bash
# Allow external connections
streamlit run live_scanner_app.py --server.address 0.0.0.0
```

### Deploy to Cloud

**Streamlit Cloud (Free):**
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Deploy from your repo

**Other Options:**
- Heroku
- AWS/Google Cloud
- Docker container

---

## 📊 Available Data Fields

### Price & Volume
- `close`, `open`, `high`, `low`
- `volume`, `relative_volume_10d_calc`
- `change` (% change)

### Technical Indicators
- `RSI` - Relative Strength Index
- `MACD.macd`, `MACD.signal`
- `EMA5`, `EMA20`, `EMA50`, `EMA200`
- `VWAP` - Volume Weighted Average Price
- `volatility.D` - Daily volatility

### Fundamentals
- `market_cap_basic` - Market capitalization
- `price_earnings_ttm` - P/E ratio
- `dividend_yield_recent` - Dividend yield
- `earnings_per_share_basic_ttm`

### Performance
- `Perf.W` - 1-week performance
- `Perf.1M` - 1-month performance
- `Perf.3M` - 3-month performance

[See full field list](https://shner-elmo.github.io/TradingView-Screener/fields/stocks.html)

---

## 🔄 Updates & Maintenance

### Keeping Cookies Fresh

Cookies typically last:
- **While logged in:** Active
- **After logout:** Expired
- **Timeout:** ~30 days (varies)

**Best practice:** Re-authenticate if you see errors

### App Updates

Pull latest changes:
```bash
git pull
pip install -r requirements-webapp.txt --upgrade
```

---

## 📚 Integration with ML Pipeline

The web app works seamlessly with the ML extension:

```python
# Export from web app, then:
import pandas as pd
from tradingview_screener.features import preprocess_for_ml

# Load exported data
df = pd.read_parquet('scan_20250117_120000.parquet')

# Preprocess for ML
df_ml = preprocess_for_ml(df, target_type='direction')

# Train model...
```

---

## ❓ FAQ

**Q: Do I need a TradingView account?**
A: No, but you get delayed data without authentication.

**Q: Is my cookie safe?**
A: Your cookie stays local - it's never sent to external servers (only to TradingView API).

**Q: Can I scan multiple markets?**
A: Yes! Select multiple markets in the dropdown.

**Q: How many results can I get?**
A: Up to 1000 per scan (adjust "Result Limit").

**Q: Can I save scan configurations?**
A: Currently manual - future feature planned!

**Q: Does auto-scan work in background?**
A: Only while the browser tab is open and active.

---

## 🎉 Enjoy Your Live Scanner!

You now have a powerful web interface for real-time market scanning!

**Next Steps:**
1. Launch the app: `streamlit run live_scanner_app.py`
2. Upload your cookie
3. Start scanning!

---

**Happy Scanning! 📊🚀**
