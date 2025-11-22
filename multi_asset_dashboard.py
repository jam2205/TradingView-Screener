"""
Multi-Asset Multi-Timeframe Dashboard

Interactive web dashboard for scanning:
- Bonds (US Treasuries)
- Commodities (Gold, Silver)
- Indices (NASDAQ, SP500, Dow Jones)
- Forex (GBP/JPY, EUR/USD, AUD/USD, etc.)

Across multiple timeframes: 5min, 15min, 1hr, 4hr, daily, weekly, monthly
"""
import streamlit as st
import pandas as pd
from datetime import datetime
import json

from tradingview_screener.multi_asset_scanner import (
    MultiAssetScanner,
    MAJOR_SYMBOLS,
    scan_all_your_markets
)

# Page config
st.set_page_config(
    page_title="Multi-Asset Scanner Dashboard",
    page_icon="📊",
    layout="wide",
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .market-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Session state
if 'cookies' not in st.session_state:
    st.session_state.cookies = None
if 'scan_data' not in st.session_state:
    st.session_state.scan_data = {}

# Header
st.markdown('<div class="main-header">📊 Multi-Asset Market Scanner</div>', unsafe_allow_html=True)
st.caption("Scan Bonds, Commodities, Indices & Forex across multiple timeframes")

# Sidebar - Authentication
with st.sidebar:
    st.header("🔐 Authentication")

    auth_method = st.radio(
        "Authentication:",
        ["Session Cookie", "Cookie File", "No Auth (Delayed)"]
    )

    if auth_method == "Session Cookie":
        session_id = st.text_input("Session ID:", type="password")
        if st.button("Authenticate"):
            if session_id:
                st.session_state.cookies = {'sessionid': session_id}
                st.success("✅ Authenticated!")
            else:
                st.error("Enter session ID")

    elif auth_method == "Cookie File":
        cookie_file = st.file_uploader("Upload JSON:", type=['json'])
        if cookie_file:
            try:
                cookies_data = json.load(cookie_file)
                if 'sessionid' in cookies_data:
                    st.session_state.cookies = cookies_data
                    st.success("✅ Loaded!")
                else:
                    st.error("Missing 'sessionid'")
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.session_state.cookies = None
        st.warning("Using delayed data")

    st.divider()

    # Quick scan settings
    st.header("⚡ Quick Scan")

    timeframe = st.selectbox(
        "Timeframe:",
        ['5min', '15min', '1hr', '4hr', 'daily', 'weekly', 'monthly'],
        index=4  # default: daily
    )

    if st.button("🚀 Scan All Markets", type="primary", use_container_width=True):
        with st.spinner(f"Scanning all markets on {timeframe}..."):
            try:
                results = scan_all_your_markets(
                    timeframe=timeframe,
                    cookies=st.session_state.cookies
                )
                st.session_state.scan_data = results
                st.session_state.scan_timeframe = timeframe
                st.success(f"✅ Scan complete!")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

# Main content
tabs = st.tabs([
    "📊 Dashboard",
    "🥇 Commodities",
    "📈 Indices",
    "💱 Forex",
    "🏦 Bonds",
    "⏰ Multi-Timeframe",
    "⚙️ Custom Scan"
])

# Tab 1: Dashboard
with tabs[0]:
    st.header("Market Overview Dashboard")

    if st.session_state.scan_data:
        tf = st.session_state.get('scan_timeframe', 'daily')
        st.info(f"📅 Showing {tf.upper()} data")

        # Metrics row
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if 'commodities' in st.session_state.scan_data:
                st.metric("Commodities", len(st.session_state.scan_data['commodities']))

        with col2:
            if 'indices' in st.session_state.scan_data:
                st.metric("Indices", len(st.session_state.scan_data['indices']))

        with col3:
            if 'forex' in st.session_state.scan_data:
                st.metric("Forex Pairs", len(st.session_state.scan_data['forex']))

        with col4:
            if 'bonds' in st.session_state.scan_data:
                st.metric("Bonds", len(st.session_state.scan_data['bonds']))

        # Display all markets
        for market_name, df in st.session_state.scan_data.items():
            st.subheader(f"{market_name.title()}")
            if len(df) > 0:
                st.dataframe(df, use_container_width=True)

                # Download button
                csv = df.to_csv(index=False)
                st.download_button(
                    f"📥 Download {market_name}",
                    csv,
                    f"{market_name}_{tf}_{datetime.now().strftime('%Y%m%d')}.csv",
                    "text/csv",
                    key=f"download_{market_name}"
                )
            else:
                st.warning(f"No {market_name} data")
            st.divider()

    else:
        st.info("👈 Click 'Scan All Markets' in the sidebar to start")

        # Show available markets
        st.subheader("📋 Available Markets")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**🥇 Commodities:**")
            st.write("• Gold (spot & futures)")
            st.write("• Silver (spot & futures)")
            st.write("• Crude Oil")
            st.write("• Natural Gas")

            st.markdown("**📈 Indices:**")
            st.write("• S&P 500 (SP500)")
            st.write("• NASDAQ 100")
            st.write("• Dow Jones (YM30 futures)")
            st.write("• E-mini S&P (ES)")
            st.write("• E-mini NASDAQ (NQ)")

        with col2:
            st.markdown("**💱 Forex Pairs:**")
            st.write("• GBP/JPY")
            st.write("• EUR/USD")
            st.write("• AUD/USD")
            st.write("• USD/JPY")
            st.write("• EUR/GBP, EUR/JPY, AUD/JPY")

            st.markdown("**🏦 Bonds:**")
            st.write("• US 2-Year Treasury")
            st.write("• US 5-Year Treasury")
            st.write("• US 10-Year Treasury")
            st.write("• US 30-Year Treasury")

# Tab 2: Commodities
with tabs[1]:
    st.header("🥇 Commodities Scanner")

    scanner = MultiAssetScanner(cookies=st.session_state.cookies)

    commodities = st.multiselect(
        "Select commodities:",
        ['GOLD', 'GOLD_FUTURES', 'SILVER', 'SILVER_FUTURES', 'OIL', 'NATGAS'],
        default=['GOLD', 'SILVER']
    )

    tf_commodities = st.selectbox(
        "Timeframe:",
        ['5min', '15min', '1hr', '4hr', 'daily', 'weekly', 'monthly'],
        key='tf_commodities'
    )

    if st.button("Scan Commodities"):
        with st.spinner("Scanning commodities..."):
            df = scanner.scan_symbols(commodities, timeframe=tf_commodities)
            st.dataframe(df, use_container_width=True)

            csv = df.to_csv(index=False)
            st.download_button(
                "📥 Download",
                csv,
                f"commodities_{tf_commodities}_{datetime.now().strftime('%Y%m%d')}.csv"
            )

# Tab 3: Indices
with tabs[2]:
    st.header("📈 Indices Scanner")

    scanner = MultiAssetScanner(cookies=st.session_state.cookies)

    indices = st.multiselect(
        "Select indices:",
        ['SP500', 'NASDAQ', 'DOW', 'YM30', 'ES', 'NQ'],
        default=['SP500', 'NASDAQ', 'YM30']
    )

    tf_indices = st.selectbox(
        "Timeframe:",
        ['5min', '15min', '1hr', '4hr', 'daily', 'weekly', 'monthly'],
        key='tf_indices'
    )

    if st.button("Scan Indices"):
        with st.spinner("Scanning indices..."):
            df = scanner.scan_symbols(indices, timeframe=tf_indices)
            st.dataframe(df, use_container_width=True)

            csv = df.to_csv(index=False)
            st.download_button(
                "📥 Download",
                csv,
                f"indices_{tf_indices}_{datetime.now().strftime('%Y%m%d')}.csv"
            )

# Tab 4: Forex
with tabs[3]:
    st.header("💱 Forex Scanner")

    scanner = MultiAssetScanner(cookies=st.session_state.cookies)

    forex_pairs = st.multiselect(
        "Select forex pairs:",
        ['EURUSD', 'GBPJPY', 'GBPUSD', 'USDJPY', 'AUDUSD', 'USDCAD', 'EURJPY', 'AUDJPY'],
        default=['GBPJPY', 'EURUSD', 'AUDUSD', 'USDJPY']
    )

    tf_forex = st.selectbox(
        "Timeframe:",
        ['5min', '15min', '1hr', '4hr', 'daily', 'weekly', 'monthly'],
        key='tf_forex'
    )

    if st.button("Scan Forex"):
        with st.spinner("Scanning forex..."):
            df = scanner.scan_symbols(forex_pairs, timeframe=tf_forex)
            st.dataframe(df, use_container_width=True)

            csv = df.to_csv(index=False)
            st.download_button(
                "📥 Download",
                csv,
                f"forex_{tf_forex}_{datetime.now().strftime('%Y%m%d')}.csv"
            )

# Tab 5: Bonds
with tabs[4]:
    st.header("🏦 Bond Market Scanner")

    scanner = MultiAssetScanner(cookies=st.session_state.cookies)

    bonds = st.multiselect(
        "Select bonds:",
        ['US02Y', 'US05Y', 'US10Y', 'US30Y', 'DX'],
        default=['US02Y', 'US10Y', 'US30Y']
    )

    tf_bonds = st.selectbox(
        "Timeframe:",
        ['5min', '15min', '1hr', '4hr', 'daily', 'weekly', 'monthly'],
        key='tf_bonds'
    )

    if st.button("Scan Bonds"):
        with st.spinner("Scanning bonds..."):
            df = scanner.scan_symbols(bonds, timeframe=tf_bonds)
            st.dataframe(df, use_container_width=True)

            csv = df.to_csv(index=False)
            st.download_button(
                "📥 Download",
                csv,
                f"bonds_{tf_bonds}_{datetime.now().strftime('%Y%m%d')}.csv"
            )

# Tab 6: Multi-Timeframe
with tabs[5]:
    st.header("⏰ Multi-Timeframe Analysis")

    scanner = MultiAssetScanner(cookies=st.session_state.cookies)

    symbols_mtf = st.multiselect(
        "Select symbols:",
        list(MAJOR_SYMBOLS.keys()),
        default=['GOLD', 'SILVER', 'SP500', 'NASDAQ', 'GBPJPY']
    )

    timeframes_mtf = st.multiselect(
        "Select timeframes:",
        ['5min', '15min', '1hr', '4hr', 'daily', 'weekly', 'monthly'],
        default=['1hr', '4hr', 'daily']
    )

    if st.button("Run Multi-Timeframe Scan"):
        with st.spinner(f"Scanning {len(symbols_mtf)} symbols across {len(timeframes_mtf)} timeframes..."):
            results = scanner.scan_multi_timeframe(symbols_mtf, timeframes_mtf)

            for tf, df in results.items():
                st.subheader(f"{tf.upper()} Timeframe")
                st.dataframe(df, use_container_width=True)

                csv = df.to_csv(index=False)
                st.download_button(
                    f"📥 Download {tf}",
                    csv,
                    f"multi_tf_{tf}_{datetime.now().strftime('%Y%m%d')}.csv",
                    key=f"download_mtf_{tf}"
                )

# Tab 7: Custom Scan
with tabs[6]:
    st.header("⚙️ Custom Scan")

    st.info("Build your own custom market scan")

    scanner = MultiAssetScanner(cookies=st.session_state.cookies)

    # Symbol input
    custom_symbols = st.text_area(
        "Enter symbols (one per line):",
        value="GOLD\nSILVER\nSP500\nNASDAQ\nGBPJPY\nEURUSD",
        height=150
    )

    symbols_list = [s.strip() for s in custom_symbols.split('\n') if s.strip()]

    tf_custom = st.selectbox(
        "Timeframe:",
        ['5min', '15min', '1hr', '4hr', 'daily', 'weekly', 'monthly'],
        key='tf_custom'
    )

    if st.button("Run Custom Scan"):
        with st.spinner(f"Scanning {len(symbols_list)} symbols..."):
            df = scanner.scan_symbols(symbols_list, timeframe=tf_custom)

            st.success(f"✅ Scanned {len(df)} symbols")
            st.dataframe(df, use_container_width=True)

            csv = df.to_csv(index=False)
            st.download_button(
                "📥 Download Results",
                csv,
                f"custom_scan_{tf_custom}_{datetime.now().strftime('%Y%m%d')}.csv"
            )

# Footer
st.divider()
st.caption("💡 Tip: Authenticate for real-time data. Use sidebar to upload your TradingView cookie.")
