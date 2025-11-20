# 📓 Google Colab Quick Start Guide

Get started with TradingView ML Data Collection in Google Colab!

---

## 🚀 One-Click Launch

**Click here to open in Colab:**

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/jam2205/TradingView-Screener/blob/claude/data-collection-tool-012ct4SD9dgooKzsu9q71uL2/TradingView_ML_Collector.ipynb)

---

## 📋 What's Included

The notebook contains **5 complete examples:**

1. ✅ **Simple Data Collection** - Basic market scanning
2. ✅ **Feature Engineering** - Add technical indicators
3. ✅ **Complete ML Pipeline** - Train a price prediction model
4. ✅ **Preset Scans** - 7 ready-to-use strategies
5. ✅ **Export Data** - Save in CSV/Parquet/JSON

---

## 🎯 Quick Start (3 Steps)

### Step 1: Open the Notebook

Click the "Open in Colab" badge above, or manually:

1. Go to [Google Colab](https://colab.research.google.com)
2. Click **File → Upload notebook**
3. Go to **GitHub** tab
4. Enter: `jam2205/TradingView-Screener`
5. Branch: `claude/data-collection-tool-012ct4SD9dgooKzsu9q71uL2`
6. Select: `TradingView_ML_Collector.ipynb`

### Step 2: Run Setup Cells

Run these cells in order:
1. **Section 1** - Install dependencies (30 seconds)
2. **Section 2** - Clone repository (10 seconds)
3. **Section 3** - Import libraries (5 seconds)

### Step 3: Choose an Example!

Jump to any example and run it:
- **Example 1** - Simple collection
- **Example 2** - Feature engineering
- **Example 3** - Full ML pipeline ⭐ (recommended!)
- **Example 4** - Preset scans
- **Example 5** - Export data

---

## 🔐 Authentication (Optional)

For **real-time data**, add your TradingView cookie:

1. Go to [TradingView.com](https://www.tradingview.com) (logged in)
2. Press **F12** → **Application** → **Cookies**
3. Copy the `sessionid` value
4. In the notebook, go to **Section 4**
5. Paste the sessionid in the `SESSIONID` variable
6. Run the cell

**Without authentication:** You'll get 15-minute delayed data (still works fine!)

---

## 📊 Example Output

### Example 1: Simple Collection
```
✅ Collected 100 stocks
📊 Columns: ['ticker', 'name', 'close', 'volume', 'market_cap_basic', 'RSI', 'MACD.macd', 'change']

📈 Summary Statistics:
Average Price: $152.34
Total Volume: 847,234,567
Average RSI: 52.18
Average Change: 1.23%
```

### Example 3: ML Pipeline
```
🤖 Step 4: Training Random Forest model...
✅ Model trained!

📊 Step 5: Model Evaluation

🎯 Accuracy Scores:
  Training:   72.45%
  Test:       64.23%
  Difference: 8.22%

📋 Classification Report (Test Set):
              precision    recall  f1-score   support
        Down       0.63      0.59      0.61        49
          Up       0.65      0.69      0.67        54
    accuracy                           0.64       103
```

---

## 💾 Downloading Your Data

After running any example, download the results:

```python
# Run this cell to download
from google.colab import files

# Download CSV
files.download('/content/exports/market_data.csv')

# Or download Parquet (better for ML)
files.download('/content/exports/market_data.parquet')
```

Or use the Files panel (left sidebar) → `/content/exports/`

---

## 🎯 Common Workflows

### Workflow 1: Quick Data Collection

1. Run Sections 1-3 (setup)
2. Go to **Example 1**
3. Run the collection cell
4. Download CSV

**Time:** ~2 minutes

### Workflow 2: Train ML Model

1. Run Sections 1-3 (setup)
2. Optional: Add authentication (Section 4)
3. Go to **Example 3**
4. Run all cells in sequence
5. Get trained model!

**Time:** ~5 minutes

### Workflow 3: Multiple Strategies

1. Run Sections 1-3 (setup)
2. Go to **Example 4**
3. Run all preset scans
4. Compare results
5. Download best performers

**Time:** ~3 minutes

---

## 🔧 Customization

### Change the Query

Modify any query to fit your needs:

```python
# Example: Find penny stocks with high volume
query = (
    Query()
    .select('name', 'close', 'volume', 'change')
    .where(
        col('close').between(0.50, 5.00),  # Price $0.50-$5
        col('volume') > 5_000_000,         # High volume
    )
    .limit(50)
)
```

### Add More Features

```python
from tradingview_screener.features import add_returns

# Add custom period returns
df = add_returns(df, periods=[1, 3, 7, 14, 30])
```

### Try Different Models

```python
from sklearn.ensemble import GradientBoostingClassifier
from xgboost import XGBClassifier

# Gradient Boosting
model = GradientBoostingClassifier()

# Or XGBoost (install first: !pip install xgboost)
model = XGBClassifier()
```

---

## 📚 Available Examples

| Example | What It Does | Run Time |
|---------|--------------|----------|
| **Example 1** | Basic data collection | ~30s |
| **Example 2** | Add technical features | ~45s |
| **Example 3** | Complete ML pipeline | ~2min |
| **Example 4** | Preset scans (3 strategies) | ~1min |
| **Example 5** | Export to multiple formats | ~10s |

---

## 💡 Pro Tips

### 1. Save Your Work
```python
# Save to Google Drive
from google.colab import drive
drive.mount('/content/drive')

# Save data to Drive
df.to_parquet('/content/drive/MyDrive/trading_data.parquet')
```

### 2. Schedule Regular Collection
```python
# Collect data every hour (keep notebook running)
import time

for i in range(24):  # 24 hours
    df = collector.collect_once(query, f'hourly_{i}', cookies=cookies)
    print(f"Collection {i+1}/24 complete")
    time.sleep(3600)  # Wait 1 hour
```

### 3. Combine Multiple Scans
```python
# Collect from different strategies
momentum_df = collector.collect_once(momentum_query, 'momentum')
value_df = collector.collect_once(value_query, 'value')
oversold_df = collector.collect_once(oversold_query, 'oversold')

# Combine
all_stocks = pd.concat([momentum_df, value_df, oversold_df])
all_stocks = all_stocks.drop_duplicates(subset=['ticker'])
```

---

## ❓ Troubleshooting

### Issue: "Module not found"
**Solution:** Re-run Section 1 (install dependencies)

### Issue: "Repository not found"
**Solution:** Re-run Section 2 (clone repository)

### Issue: "No data returned"
**Solution:**
- Check your filters (might be too restrictive)
- Try increasing the limit
- Check if markets are open (US markets closed on weekends)

### Issue: "Connection timeout"
**Solution:**
- Restart runtime: Runtime → Restart runtime
- Re-run setup cells
- Try again

### Issue: "Memory error"
**Solution:**
- Reduce the limit in your query
- Use GPU runtime: Runtime → Change runtime type → GPU
- Clear variables: `del df` and restart kernel

---

## 🎯 Next Steps

After running the notebook:

1. **Experiment** - Modify queries and strategies
2. **Download** - Export data for further analysis
3. **Train** - Build and test ML models
4. **Deploy** - Use locally or in production
5. **Automate** - Schedule regular data collection

---

## 📖 Additional Resources

- **Full ML Guide:** [ML_GUIDE.md](ML_GUIDE.md)
- **Quick Start:** [ML_QUICKSTART.md](ML_QUICKSTART.md)
- **Live Scanner:** [LIVE_SCANNER_GUIDE.md](LIVE_SCANNER_GUIDE.md)
- **Examples:** [examples/](examples/)

---

## 🆘 Need Help?

- Check the notebook's built-in documentation
- Read the [ML_GUIDE.md](ML_GUIDE.md)
- Open an issue on [GitHub](https://github.com/jam2205/TradingView-Screener/issues)

---

## 🎉 Ready to Start!

Click the badge at the top to open in Colab!

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/jam2205/TradingView-Screener/blob/claude/data-collection-tool-012ct4SD9dgooKzsu9q71uL2/TradingView_ML_Collector.ipynb)

**Happy Data Collection! 📊🚀**
