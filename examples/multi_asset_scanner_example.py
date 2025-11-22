"""
Multi-Asset Multi-Timeframe Scanner Example

Scan bonds, gold, silver, indices, and forex across multiple timeframes.
"""
from tradingview_screener.multi_asset_scanner import (
    MultiAssetScanner,
    scan_all_your_markets,
    MAJOR_SYMBOLS
)
import pandas as pd
from datetime import datetime

print("="*70)
print("Multi-Asset Multi-Timeframe Scanner")
print("="*70)
print()

# Initialize scanner
scanner = MultiAssetScanner()

# Your specified markets
YOUR_SYMBOLS = [
    # Commodities
    'GOLD',
    'SILVER',

    # Indices
    'NASDAQ',
    'SP500',
    'YM30',  # Dow Jones futures

    # Forex
    'GBPJPY',  # GBP/JPY
    'EURUSD',  # EUR/USD
    'USDJPY',  # USD/JPY (for JPY exposure)
    'AUDUSD',  # AUD/USD

    # Bonds
    'US10Y',   # 10-Year Treasury
    'US30Y',   # 30-Year Treasury
]

# Your specified timeframes
YOUR_TIMEFRAMES = ['5min', '15min', '1hr', '4hr', 'daily', 'weekly', 'monthly']

print("📊 Markets to scan:")
for sym in YOUR_SYMBOLS:
    full_name = MAJOR_SYMBOLS.get(sym, sym)
    print(f"  • {sym:15} → {full_name}")
print()

print("⏰ Timeframes:")
for tf in YOUR_TIMEFRAMES:
    print(f"  • {tf}")
print()

# Example 1: Scan all markets on daily timeframe
print("\n" + "="*70)
print("Example 1: Daily Scan of All Your Markets")
print("="*70)

results_daily = scan_all_your_markets(timeframe='daily')

print("\n📈 Daily Results:\n")
for market, df in results_daily.items():
    print(f"{market.upper()}:")
    print(f"  Rows: {len(df)}")
    if len(df) > 0:
        print(f"  Columns: {list(df.columns)[:5]}...")
        print(df.head(3).to_string(index=False))
    print()

# Example 2: Multi-timeframe analysis of Gold and Silver
print("\n" + "="*70)
print("Example 2: Gold & Silver Multi-Timeframe Analysis")
print("="*70)

print("\n🥇 Scanning Gold and Silver across all timeframes...\n")

metals_multi_tf = scanner.scan_multi_timeframe(
    symbols=['GOLD', 'SILVER'],
    timeframes=YOUR_TIMEFRAMES
)

for tf, df in metals_multi_tf.items():
    print(f"{tf.upper()} Timeframe:")
    if 'close' in df.columns or any('close' in col for col in df.columns):
        print(df.to_string(index=False))
    print()

# Example 3: Forex pairs across multiple timeframes
print("\n" + "="*70)
print("Example 3: Forex Multi-Timeframe Scan")
print("="*70)

forex_pairs = ['GBPJPY', 'EURUSD', 'AUDUSD', 'USDJPY']
print(f"\n💱 Scanning {', '.join(forex_pairs)} on 1hr and 4hr...\n")

forex_1hr = scanner.scan_symbols(forex_pairs, timeframe='1hr')
forex_4hr = scanner.scan_symbols(forex_pairs, timeframe='4hr')

print("1-Hour Data:")
print(forex_1hr.to_string(index=False))
print()

print("4-Hour Data:")
print(forex_4hr.to_string(index=False))
print()

# Example 4: Indices comparison
print("\n" + "="*70)
print("Example 4: Major Indices Daily Scan")
print("="*70)

indices = ['NASDAQ', 'SP500', 'YM30']
print(f"\n📊 Scanning {', '.join(indices)}...\n")

indices_df = scanner.scan_indices(indices, timeframe='daily')
print(indices_df.to_string(index=False))
print()

# Example 5: Bond market overview
print("\n" + "="*70)
print("Example 5: US Treasury Bonds")
print("="*70)

print("\n🏦 Scanning US Treasuries...\n")

bonds_df = scanner.scan_bonds(['US02Y', 'US05Y', 'US10Y', 'US30Y'], timeframe='daily')
print(bonds_df.to_string(index=False))
print()

# Example 6: Quick morning scan
print("\n" + "="*70)
print("Example 6: Morning Market Scan (All Assets)")
print("="*70)

print("\n🌅 Complete morning overview across all markets...\n")

all_markets = scanner.scan_all_markets(timeframe='daily')

for market_name, market_df in all_markets.items():
    print(f"\n{market_name.upper()}:")
    print("-" * 70)
    if len(market_df) > 0:
        print(market_df.head().to_string(index=False))
    else:
        print("  No data")

# Example 7: Export data
print("\n" + "="*70)
print("Example 7: Export Data")
print("="*70)

# Save to CSV
output_file = f'market_scan_{datetime.now().strftime("%Y%m%d")}.csv'
all_symbols_df = scanner.scan_symbols(YOUR_SYMBOLS, timeframe='daily')
all_symbols_df.to_csv(output_file, index=False)
print(f"\n✅ Data exported to: {output_file}")

# Save multi-timeframe data
print("\n💾 Saving multi-timeframe data...")
for tf in ['1hr', '4hr', 'daily']:
    filename = f'market_scan_{tf}_{datetime.now().strftime("%Y%m%d")}.csv'
    df = scanner.scan_symbols(YOUR_SYMBOLS, timeframe=tf)
    df.to_csv(filename, index=False)
    print(f"  ✓ Saved {tf}: {filename}")

print("\n" + "="*70)
print("✅ Multi-Asset Scanner Complete!")
print("="*70)
