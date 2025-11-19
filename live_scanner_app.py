"""
Live TradingView Scanner - Web Interface

A Streamlit web app for real-time market scanning with TradingView data.
Features:
- Cookie authentication for live/real-time data
- Live price scanning and monitoring
- Interactive data tables
- Download collected data
- Multiple preset scanning strategies

Usage:
    streamlit run live_scanner_app.py
"""
import streamlit as st
import pandas as pd
from datetime import datetime
import time
import json
from pathlib import Path

from tradingview_screener import Query, col
from tradingview_screener.ml_collector import MLDataCollector

# Page configuration
st.set_page_config(
    page_title="TradingView Live Scanner",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeeba;
        color: #856404;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'cookies' not in st.session_state:
    st.session_state.cookies = None
if 'is_authenticated' not in st.session_state:
    st.session_state.is_authenticated = False
if 'scan_data' not in st.session_state:
    st.session_state.scan_data = None
if 'scan_history' not in st.session_state:
    st.session_state.scan_history = []
if 'auto_scan_enabled' not in st.session_state:
    st.session_state.auto_scan_enabled = False

# Header
st.markdown('<div class="main-header">📊 TradingView Live Scanner</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Real-time market data collection and analysis</div>', unsafe_allow_html=True)

# Sidebar - Authentication
with st.sidebar:
    st.header("🔐 Authentication")

    auth_method = st.radio(
        "Choose authentication method:",
        ["Session Cookie", "Cookie JSON File", "No Authentication (Delayed Data)"]
    )

    if auth_method == "Session Cookie":
        st.info("📝 How to get your session cookie:\n\n"
                "1. Go to [TradingView.com](https://www.tradingview.com)\n"
                "2. Open Developer Tools (F12)\n"
                "3. Go to Application → Cookies\n"
                "4. Copy the 'sessionid' value")

        session_id = st.text_input(
            "Enter sessionid cookie:",
            type="password",
            placeholder="your_session_id_here"
        )

        if st.button("🔑 Authenticate", type="primary"):
            if session_id:
                st.session_state.cookies = {'sessionid': session_id}
                st.session_state.is_authenticated = True
                st.success("✅ Authenticated successfully!")
                st.rerun()
            else:
                st.error("❌ Please enter a session ID")

    elif auth_method == "Cookie JSON File":
        st.info("Upload a JSON file with your cookies.\n\n"
                "Format: `{\"sessionid\": \"your_value\"}`")

        cookie_file = st.file_uploader(
            "Upload cookie JSON file:",
            type=['json'],
            help="Upload a JSON file containing your TradingView cookies"
        )

        if cookie_file is not None:
            try:
                cookies_data = json.load(cookie_file)
                if 'sessionid' in cookies_data:
                    st.session_state.cookies = cookies_data
                    st.session_state.is_authenticated = True
                    st.success("✅ Cookies loaded successfully!")
                    st.rerun()
                else:
                    st.error("❌ JSON must contain 'sessionid' field")
            except Exception as e:
                st.error(f"❌ Error loading cookie file: {e}")

    else:  # No Authentication
        st.warning("⚠️ Using delayed data (15-minute delay)")
        if st.button("Continue with delayed data"):
            st.session_state.cookies = None
            st.session_state.is_authenticated = True
            st.rerun()

    st.divider()

    # Authentication status
    if st.session_state.is_authenticated:
        st.markdown('<div class="success-box">✅ Ready to scan</div>', unsafe_allow_html=True)
        if st.button("🚪 Logout"):
            st.session_state.cookies = None
            st.session_state.is_authenticated = False
            st.rerun()
    else:
        st.markdown('<div class="warning-box">⚠️ Not authenticated</div>', unsafe_allow_html=True)

# Main content
if not st.session_state.is_authenticated:
    st.info("👈 Please authenticate using the sidebar to start scanning")

    # Show features
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 🔄 Real-time Data")
        st.write("Access live market data with authentication")

    with col2:
        st.markdown("### 📊 Custom Scans")
        st.write("Create custom screening strategies")

    with col3:
        st.markdown("### 💾 Export Data")
        st.write("Download data in multiple formats")

else:
    # Tabs for different features
    tab1, tab2, tab3, tab4 = st.tabs(["🔍 Live Scanner", "📈 Preset Scans", "📊 Data View", "⚙️ Settings"])

    # Tab 1: Live Scanner
    with tab1:
        st.header("Custom Live Scanner")

        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("Build Your Query")

            # Market selection
            markets = st.multiselect(
                "Markets:",
                ['america', 'crypto', 'forex', 'cfd', 'futures', 'bonds'],
                default=['america']
            )

            # Columns selection
            available_columns = [
                'name', 'close', 'open', 'high', 'low', 'volume',
                'market_cap_basic', 'relative_volume_10d_calc',
                'RSI', 'MACD.macd', 'MACD.signal',
                'EMA5', 'EMA20', 'EMA50', 'EMA200',
                'VWAP', 'change', 'Perf.W', 'Perf.1M',
                'price_earnings_ttm', 'dividend_yield_recent',
                'volatility.D'
            ]

            selected_columns = st.multiselect(
                "Columns to display:",
                available_columns,
                default=['name', 'close', 'volume', 'market_cap_basic', 'RSI', 'change']
            )

            # Filters
            st.subheader("Filters")

            col_a, col_b = st.columns(2)

            with col_a:
                min_volume = st.number_input(
                    "Min Volume:",
                    min_value=0,
                    value=1000000,
                    step=100000,
                    format="%d"
                )

                min_market_cap = st.number_input(
                    "Min Market Cap ($):",
                    min_value=0,
                    value=1000000000,
                    step=1000000000,
                    format="%d"
                )

            with col_b:
                min_rel_volume = st.number_input(
                    "Min Relative Volume:",
                    min_value=0.0,
                    value=1.0,
                    step=0.1,
                    format="%.1f"
                )

                result_limit = st.number_input(
                    "Result Limit:",
                    min_value=10,
                    max_value=1000,
                    value=100,
                    step=10
                )

        with col2:
            st.subheader("Scan Controls")

            if st.button("🔍 Run Scan Now", type="primary", use_container_width=True):
                with st.spinner("Scanning markets..."):
                    try:
                        # Build query
                        query = Query()

                        if len(markets) == 1:
                            query.set_markets(markets[0])

                        query.select(*selected_columns)

                        # Apply filters
                        filters = []
                        if min_volume > 0:
                            filters.append(col('volume') > min_volume)
                        if min_market_cap > 0:
                            filters.append(col('market_cap_basic') > min_market_cap)
                        if min_rel_volume > 0:
                            filters.append(col('relative_volume_10d_calc') > min_rel_volume)

                        if filters:
                            query.where(*filters)

                        query.limit(result_limit)

                        # Execute query
                        total_count, df = query.get_scanner_data(cookies=st.session_state.cookies)

                        # Store in session state
                        st.session_state.scan_data = df
                        st.session_state.scan_history.append({
                            'timestamp': datetime.now(),
                            'total_count': total_count,
                            'returned': len(df)
                        })

                        st.success(f"✅ Scan complete! Found {total_count} matches, showing {len(df)}")
                        st.rerun()

                    except Exception as e:
                        st.error(f"❌ Error during scan: {e}")

            st.divider()

            # Auto-refresh
            st.subheader("Auto-Scan")
            auto_scan = st.checkbox("Enable auto-scan", value=st.session_state.auto_scan_enabled)
            st.session_state.auto_scan_enabled = auto_scan

            if auto_scan:
                refresh_interval = st.select_slider(
                    "Refresh interval:",
                    options=[30, 60, 120, 300, 600],
                    value=60,
                    format_func=lambda x: f"{x}s" if x < 60 else f"{x//60}min"
                )
                st.info(f"Auto-scanning every {refresh_interval}s")
                time.sleep(refresh_interval)
                st.rerun()

            st.divider()

            # Scan history
            if st.session_state.scan_history:
                st.subheader("Recent Scans")
                for scan in st.session_state.scan_history[-5:]:
                    st.caption(f"{scan['timestamp'].strftime('%H:%M:%S')} - {scan['returned']} results")

        # Display results
        if st.session_state.scan_data is not None:
            st.divider()
            st.subheader("Scan Results")

            # Metrics
            col1, col2, col3, col4 = st.columns(4)

            df = st.session_state.scan_data

            with col1:
                st.metric("Total Results", len(df))
            with col2:
                if 'close' in df.columns:
                    avg_price = df['close'].mean()
                    st.metric("Avg Price", f"${avg_price:.2f}")
            with col3:
                if 'volume' in df.columns:
                    total_vol = df['volume'].sum()
                    st.metric("Total Volume", f"{total_vol:,.0f}")
            with col4:
                if 'change' in df.columns:
                    avg_change = df['change'].mean()
                    st.metric("Avg Change", f"{avg_change:.2f}%")

            # Data table
            st.dataframe(
                df,
                use_container_width=True,
                height=400
            )

            # Download buttons
            col1, col2, col3 = st.columns(3)

            with col1:
                csv = df.to_csv(index=False)
                st.download_button(
                    "📥 Download CSV",
                    csv,
                    f"scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    "text/csv",
                    use_container_width=True
                )

            with col2:
                # Parquet download
                parquet_path = f"/tmp/scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.parquet"
                df.to_parquet(parquet_path, index=False)
                with open(parquet_path, 'rb') as f:
                    st.download_button(
                        "📥 Download Parquet",
                        f,
                        f"scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.parquet",
                        use_container_width=True
                    )

            with col3:
                json_str = df.to_json(orient='records', indent=2)
                st.download_button(
                    "📥 Download JSON",
                    json_str,
                    f"scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    "application/json",
                    use_container_width=True
                )

    # Tab 2: Preset Scans
    with tab2:
        st.header("Preset Scanning Strategies")

        preset_scans = {
            "🚀 Large Cap Momentum": {
                "description": "Large cap stocks with high volume and momentum",
                "query": lambda: (
                    Query()
                    .select('name', 'close', 'volume', 'market_cap_basic', 'RSI', 'MACD.macd', 'change', 'Perf.W')
                    .where(
                        col('market_cap_basic') > 10_000_000_000,
                        col('volume') > 1_000_000,
                        col('relative_volume_10d_calc') > 1.2
                    )
                    .order_by('volume', ascending=False)
                    .limit(100)
                )
            },
            "💎 Small Cap Growth": {
                "description": "Small cap stocks with growth potential",
                "query": lambda: (
                    Query()
                    .select('name', 'close', 'volume', 'market_cap_basic', 'Perf.1M', 'Perf.3M', 'RSI')
                    .where(
                        col('market_cap_basic').between(100_000_000, 2_000_000_000),
                        col('volume') > 100_000,
                        col('Perf.3M') > 10
                    )
                    .order_by('Perf.3M', ascending=False)
                    .limit(100)
                )
            },
            "📊 High Volume Breakout": {
                "description": "Stocks with unusual volume spikes",
                "query": lambda: (
                    Query()
                    .select('name', 'close', 'volume', 'relative_volume_10d_calc', 'change', 'RSI')
                    .where(
                        col('relative_volume_10d_calc') > 2.0,
                        col('volume') > 500_000
                    )
                    .order_by('relative_volume_10d_calc', ascending=False)
                    .limit(100)
                )
            },
            "🔥 Overbought Stocks": {
                "description": "Stocks in overbought territory (RSI > 70)",
                "query": lambda: (
                    Query()
                    .select('name', 'close', 'volume', 'RSI', 'change', 'market_cap_basic')
                    .where(
                        col('RSI') > 70,
                        col('volume') > 500_000
                    )
                    .order_by('RSI', ascending=False)
                    .limit(100)
                )
            },
            "❄️ Oversold Stocks": {
                "description": "Stocks in oversold territory (RSI < 30)",
                "query": lambda: (
                    Query()
                    .select('name', 'close', 'volume', 'RSI', 'change', 'market_cap_basic')
                    .where(
                        col('RSI') < 30,
                        col('volume') > 500_000
                    )
                    .order_by('RSI', ascending=True)
                    .limit(100)
                )
            },
            "💰 Value Stocks": {
                "description": "Undervalued stocks with good fundamentals",
                "query": lambda: (
                    Query()
                    .select('name', 'close', 'price_earnings_ttm', 'dividend_yield_recent', 'market_cap_basic')
                    .where(
                        col('price_earnings_ttm').between(5, 15),
                        col('dividend_yield_recent') > 3
                    )
                    .order_by('dividend_yield_recent', ascending=False)
                    .limit(100)
                )
            },
            "🪙 Crypto Momentum": {
                "description": "High momentum cryptocurrencies",
                "query": lambda: (
                    Query()
                    .set_markets('crypto')
                    .select('name', 'close', 'volume', 'market_cap_calc', 'RSI', 'Perf.W', 'change')
                    .where(
                        col('market_cap_calc') > 100_000_000,
                        col('relative_volume_10d_calc') > 1.5
                    )
                    .order_by('volume', ascending=False)
                    .limit(100)
                )
            }
        }

        # Display preset scans in grid
        cols = st.columns(2)

        for idx, (name, config) in enumerate(preset_scans.items()):
            with cols[idx % 2]:
                with st.container():
                    st.subheader(name)
                    st.caption(config['description'])

                    if st.button(f"Run {name}", key=f"preset_{idx}", use_container_width=True):
                        with st.spinner(f"Running {name}..."):
                            try:
                                query = config['query']()
                                total_count, df = query.get_scanner_data(cookies=st.session_state.cookies)

                                st.session_state.scan_data = df
                                st.success(f"✅ Found {len(df)} results")

                                # Switch to data view tab
                                st.info("👉 Check the 'Data View' tab to see results")

                            except Exception as e:
                                st.error(f"❌ Error: {e}")

                    st.divider()

    # Tab 3: Data View
    with tab3:
        st.header("Data Viewer & Analysis")

        if st.session_state.scan_data is not None:
            df = st.session_state.scan_data

            # Summary statistics
            st.subheader("Summary Statistics")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Total Rows", len(df))
                st.metric("Total Columns", len(df.columns))

            with col2:
                if 'close' in df.columns:
                    st.metric("Avg Price", f"${df['close'].mean():.2f}")
                    st.metric("Price Range", f"${df['close'].min():.2f} - ${df['close'].max():.2f}")

            with col3:
                if 'volume' in df.columns:
                    st.metric("Total Volume", f"{df['volume'].sum():,.0f}")
                    st.metric("Avg Volume", f"{df['volume'].mean():,.0f}")

            st.divider()

            # Data table with filtering
            st.subheader("Filter & View Data")

            # Column selector
            display_columns = st.multiselect(
                "Select columns to display:",
                df.columns.tolist(),
                default=df.columns.tolist()[:10]
            )

            # Sorting
            col1, col2 = st.columns(2)
            with col1:
                sort_column = st.selectbox("Sort by:", df.columns.tolist())
            with col2:
                sort_order = st.radio("Order:", ["Ascending", "Descending"], horizontal=True)

            # Apply sorting
            sorted_df = df[display_columns].sort_values(
                by=sort_column,
                ascending=(sort_order == "Ascending")
            )

            # Display
            st.dataframe(sorted_df, use_container_width=True, height=500)

            # Statistics
            st.subheader("Column Statistics")
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()

            if numeric_cols:
                selected_stat_col = st.selectbox("Select column for statistics:", numeric_cols)

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric("Mean", f"{df[selected_stat_col].mean():.2f}")
                with col2:
                    st.metric("Median", f"{df[selected_stat_col].median():.2f}")
                with col3:
                    st.metric("Std Dev", f"{df[selected_stat_col].std():.2f}")
                with col4:
                    st.metric("Count", f"{df[selected_stat_col].count()}")

        else:
            st.info("👈 Run a scan first to view data")

    # Tab 4: Settings
    with tab4:
        st.header("Settings & Configuration")

        st.subheader("Data Collection Settings")

        output_format = st.selectbox(
            "Default export format:",
            ['Parquet', 'CSV', 'JSON'],
            index=0
        )

        auto_save = st.checkbox("Auto-save scan results", value=False)

        if auto_save:
            save_dir = st.text_input("Save directory:", value="data/live_scans")
            st.info(f"Results will be saved to: {save_dir}")

        st.divider()

        st.subheader("Display Settings")

        rows_per_page = st.slider("Rows per page:", 10, 100, 50, 10)

        theme = st.selectbox("Color theme:", ['Light', 'Dark'], index=0)

        st.divider()

        st.subheader("Cookie Management")

        if st.session_state.cookies:
            st.success("✅ Cookie is currently loaded")

            if st.button("🔄 Test Connection"):
                with st.spinner("Testing connection..."):
                    try:
                        test_query = Query().select('name').limit(1)
                        _, test_df = test_query.get_scanner_data(cookies=st.session_state.cookies)
                        st.success("✅ Connection successful! Real-time data is available.")
                    except Exception as e:
                        st.error(f"❌ Connection failed: {e}")

            if st.button("📥 Export Cookie"):
                cookie_json = json.dumps(st.session_state.cookies, indent=2)
                st.download_button(
                    "Download cookie JSON",
                    cookie_json,
                    "tradingview_cookie.json",
                    "application/json"
                )
        else:
            st.warning("⚠️ No cookie loaded (using delayed data)")

        st.divider()

        st.subheader("About")
        st.info(
            "**TradingView Live Scanner**\n\n"
            "Version: 1.0.0\n\n"
            "Built with TradingView Screener ML Extension\n\n"
            "For more information, see the documentation."
        )

        if st.button("Clear all data"):
            st.session_state.scan_data = None
            st.session_state.scan_history = []
            st.success("✅ Data cleared")
            st.rerun()

# Footer
st.divider()
st.caption("💡 Tip: Authenticate with your TradingView cookie to access real-time data. Use the sidebar to upload your session cookie.")
