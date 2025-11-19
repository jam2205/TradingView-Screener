#!/bin/bash
# Live Scanner Launcher Script

echo "================================================"
echo "  TradingView Live Scanner"
echo "================================================"
echo ""

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null
then
    echo "❌ Streamlit is not installed"
    echo ""
    echo "Install with:"
    echo "  pip install -r requirements-webapp.txt"
    echo ""
    exit 1
fi

echo "✅ Starting Live Scanner..."
echo ""
echo "The app will open in your browser at:"
echo "  http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Launch streamlit
streamlit run live_scanner_app.py
