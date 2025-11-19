"""
Cookie JSON Creator

This script helps you create a cookie JSON file for the Live Scanner app.
"""
import json
from pathlib import Path

print("="*60)
print("TradingView Cookie JSON Creator")
print("="*60)
print()
print("How to get your sessionid:")
print("1. Go to https://www.tradingview.com")
print("2. Open Developer Tools (F12)")
print("3. Go to Application → Cookies → https://www.tradingview.com")
print("4. Copy the 'sessionid' value")
print()

sessionid = input("Paste your sessionid here: ").strip()

if sessionid:
    cookie_data = {
        "sessionid": sessionid
    }

    output_file = Path("tradingview_cookie.json")

    with open(output_file, 'w') as f:
        json.dump(cookie_data, f, indent=2)

    print()
    print(f"✅ Cookie saved to: {output_file.absolute()}")
    print()
    print("You can now upload this file in the Live Scanner app!")
else:
    print("❌ No sessionid provided")
