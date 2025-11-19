# 🚀 Start Live Scanner - Quick Guide

## Step 1: Install Dependencies

```bash
pip install streamlit pandas tradingview-screener
```

Or use the requirements file:
```bash
pip install -r requirements-webapp.txt
```

## Step 2: Get Your TradingView Cookie

### Option A: Use the Helper Script
```bash
python examples/create_cookie_json.py
```
Follow the prompts to create a `tradingview_cookie.json` file.

### Option B: Manual Copy
1. Go to https://www.tradingview.com (logged in)
2. Press F12 (Developer Tools)
3. Go to Application → Cookies → https://www.tradingview.com
4. Copy the `sessionid` value

## Step 3: Launch the App

```bash
streamlit run live_scanner_app.py
```

The app will open at: `http://localhost:8501`

## Step 4: Authenticate

In the sidebar:
- Select "Session Cookie" or "Cookie JSON File"
- Enter/upload your cookie
- Click "Authenticate"

## Step 5: Start Scanning!

Choose from:
- **Custom scans** in "Live Scanner" tab
- **Preset strategies** in "Preset Scans" tab
- Enable **auto-scan** for continuous monitoring

---

## 🎯 Quick Test

Once authenticated, try this:
1. Go to "Preset Scans" tab
2. Click "Run 🚀 Large Cap Momentum"
3. Check results in "Data View" tab
4. Download as CSV/Parquet

---

## 📖 Full Documentation

See [LIVE_SCANNER_GUIDE.md](LIVE_SCANNER_GUIDE.md) for complete instructions.

---

**Need help?** Check the troubleshooting section in the guide!
