"""
Multi-Timeframe Multi-Asset Scanner

This module provides scanning capabilities across:
- Bonds
- Commodities (Gold, Silver)
- Indices (NASDAQ, S&P 500, Dow Jones)
- Forex pairs (GBP/JPY, EUR/USD, AUD/USD, etc.)

With support for multiple timeframes:
- 5min, 15min, 1hr, 4hr, daily, weekly, monthly
"""
from __future__ import annotations

__all__ = ['MultiAssetScanner', 'MARKETS', 'TIMEFRAMES', 'MAJOR_SYMBOLS']

from typing import TYPE_CHECKING, Optional, Literal
from datetime import datetime
import logging

from tradingview_screener import Query, col

if TYPE_CHECKING:
    import pandas as pd

logger = logging.getLogger(__name__)

# Market definitions
MARKETS = {
    'bonds': 'bond',
    'commodities': 'cfd',  # Gold, Silver via CFDs
    'indices': 'index',
    'forex': 'forex',
    'stocks': 'america',
    'crypto': 'crypto'
}

# Timeframe mappings
TIMEFRAMES = {
    '5min': '5',
    '5m': '5',
    '15min': '15',
    '15m': '15',
    '1hr': '60',
    '1h': '60',
    '4hr': '240',
    '4h': '240',
    'daily': '1D',
    'D': '1D',
    'weekly': '1W',
    'W': '1W',
    'monthly': '1M',
    'M': '1M'
}

# Major symbols for quick access
MAJOR_SYMBOLS = {
    # Indices
    'SP500': 'SP:SPX',           # S&P 500
    'NASDAQ': 'NASDAQ:NDX',      # NASDAQ 100
    'NASDAQ_COMP': 'TVC:IXIC',   # NASDAQ Composite
    'DOW': 'TVC:DJI',            # Dow Jones Industrial Average
    'YM30': 'CBOT_MINI:YM1!',    # E-mini Dow futures
    'ES': 'CME_MINI:ES1!',       # E-mini S&P 500 futures
    'NQ': 'CME_MINI:NQ1!',       # E-mini NASDAQ futures

    # Commodities
    'GOLD': 'TVC:GOLD',          # Gold spot
    'GOLD_FUTURES': 'COMEX:GC1!', # Gold futures
    'SILVER': 'TVC:SILVER',      # Silver spot
    'SILVER_FUTURES': 'COMEX:SI1!', # Silver futures
    'OIL': 'TVC:USOIL',          # Crude Oil
    'NATGAS': 'NYMEX:NG1!',      # Natural Gas

    # Forex Major Pairs
    'EURUSD': 'FX_IDC:EURUSD',   # EUR/USD
    'GBPJPY': 'FX_IDC:GBPJPY',   # GBP/JPY
    'GBPUSD': 'FX_IDC:GBPUSD',   # GBP/USD
    'USDJPY': 'FX_IDC:USDJPY',   # USD/JPY
    'AUDUSD': 'FX_IDC:AUDUSD',   # AUD/USD
    'USDCAD': 'FX_IDC:USDCAD',   # USD/CAD
    'NZDUSD': 'FX_IDC:NZDUSD',   # NZD/USD
    'EURGBP': 'FX_IDC:EURGBP',   # EUR/GBP
    'EURJPY': 'FX_IDC:EURJPY',   # EUR/JPY
    'AUDJPY': 'FX_IDC:AUDJPY',   # AUD/JPY

    # Bonds
    'US10Y': 'TVC:US10Y',        # US 10-Year Treasury
    'US30Y': 'TVC:US30Y',        # US 30-Year Treasury
    'US02Y': 'TVC:US02Y',        # US 2-Year Treasury
    'US05Y': 'TVC:US05Y',        # US 5-Year Treasury
    'DX': 'TVC:DXY',             # US Dollar Index
}


class MultiAssetScanner:
    """
    Multi-asset, multi-timeframe market scanner.

    Supports scanning across:
    - Bonds (US Treasuries, etc.)
    - Commodities (Gold, Silver, Oil, etc.)
    - Indices (S&P 500, NASDAQ, Dow Jones)
    - Forex (major and minor pairs)
    - Stocks
    - Crypto

    With multiple timeframes:
    - 5min, 15min, 1hr, 4hr, daily, weekly, monthly

    Example:
        >>> scanner = MultiAssetScanner()
        >>>
        >>> # Scan specific symbols
        >>> df = scanner.scan_symbols(
        ...     ['GOLD', 'SILVER', 'SP500', 'NASDAQ', 'GBPJPY'],
        ...     timeframe='1hr'
        ... )
        >>>
        >>> # Scan all forex pairs
        >>> df = scanner.scan_forex(timeframe='4hr')
        >>>
        >>> # Scan all major indices
        >>> df = scanner.scan_indices(timeframe='daily')
    """

    def __init__(self, cookies: dict | None = None):
        """
        Initialize the multi-asset scanner.

        Args:
            cookies: TradingView session cookies for real-time data
        """
        self.cookies = cookies

    def scan_symbols(
        self,
        symbols: list[str],
        timeframe: str = 'daily',
        columns: list[str] | None = None,
    ) -> pd.DataFrame:
        """
        Scan specific symbols across any timeframe.

        Args:
            symbols: List of symbols (use short names like 'GOLD', 'SP500', 'GBPJPY')
            timeframe: Timeframe (5min, 15min, 1hr, 4hr, daily, weekly, monthly)
            columns: Columns to retrieve (None = default set)

        Returns:
            DataFrame with symbol data

        Example:
            >>> scanner = MultiAssetScanner()
            >>> df = scanner.scan_symbols(['GOLD', 'SILVER', 'SP500'], timeframe='1hr')
        """
        # Convert short names to full symbols
        full_symbols = []
        for sym in symbols:
            if sym in MAJOR_SYMBOLS:
                full_symbols.append(MAJOR_SYMBOLS[sym])
            else:
                full_symbols.append(sym)

        # Default columns with timeframe-specific fields
        if columns is None:
            tf = self._normalize_timeframe(timeframe)
            columns = [
                'name',
                'description',
                f'close|{tf}',
                f'open|{tf}',
                f'high|{tf}',
                f'low|{tf}',
                f'volume|{tf}',
                f'change|{tf}',
                f'RSI|{tf}',
                f'MACD.macd|{tf}',
                f'MACD.signal|{tf}',
                f'EMA5|{tf}',
                f'EMA20|{tf}',
                f'EMA50|{tf}',
                f'EMA200|{tf}',
            ]

        # Create query
        query = Query().set_tickers(*full_symbols).select(*columns)

        # Execute
        logger.info(f"Scanning {len(full_symbols)} symbols on {timeframe}")
        total_count, df = query.get_scanner_data(cookies=self.cookies)

        return df

    def scan_forex(
        self,
        pairs: list[str] | None = None,
        timeframe: str = 'daily',
        min_volume: float | None = None,
    ) -> pd.DataFrame:
        """
        Scan forex pairs.

        Args:
            pairs: Specific pairs to scan (None = all major pairs)
            timeframe: Timeframe to analyze
            min_volume: Minimum volume filter

        Returns:
            DataFrame with forex data

        Example:
            >>> scanner = MultiAssetScanner()
            >>> df = scanner.scan_forex(['GBPJPY', 'EURUSD', 'AUDUSD'], timeframe='4hr')
        """
        if pairs is None:
            # Default major pairs
            pairs = [
                'EURUSD', 'GBPUSD', 'USDJPY', 'GBPJPY',
                'AUDUSD', 'USDCAD', 'EURJPY', 'AUDJPY'
            ]

        return self.scan_symbols(pairs, timeframe=timeframe)

    def scan_indices(
        self,
        indices: list[str] | None = None,
        timeframe: str = 'daily',
    ) -> pd.DataFrame:
        """
        Scan major market indices.

        Args:
            indices: Specific indices (None = all major)
            timeframe: Timeframe to analyze

        Returns:
            DataFrame with index data

        Example:
            >>> scanner = MultiAssetScanner()
            >>> df = scanner.scan_indices(['SP500', 'NASDAQ', 'DOW'], timeframe='1hr')
        """
        if indices is None:
            indices = ['SP500', 'NASDAQ', 'DOW', 'YM30', 'ES', 'NQ']

        return self.scan_symbols(indices, timeframe=timeframe)

    def scan_commodities(
        self,
        commodities: list[str] | None = None,
        timeframe: str = 'daily',
    ) -> pd.DataFrame:
        """
        Scan commodities (metals, energy).

        Args:
            commodities: Specific commodities (None = major commodities)
            timeframe: Timeframe to analyze

        Returns:
            DataFrame with commodity data

        Example:
            >>> scanner = MultiAssetScanner()
            >>> df = scanner.scan_commodities(['GOLD', 'SILVER', 'OIL'], timeframe='4hr')
        """
        if commodities is None:
            commodities = [
                'GOLD', 'GOLD_FUTURES',
                'SILVER', 'SILVER_FUTURES',
                'OIL', 'NATGAS'
            ]

        return self.scan_symbols(commodities, timeframe=timeframe)

    def scan_bonds(
        self,
        bonds: list[str] | None = None,
        timeframe: str = 'daily',
    ) -> pd.DataFrame:
        """
        Scan bond markets (US Treasuries).

        Args:
            bonds: Specific bonds (None = major treasuries)
            timeframe: Timeframe to analyze

        Returns:
            DataFrame with bond data

        Example:
            >>> scanner = MultiAssetScanner()
            >>> df = scanner.scan_bonds(['US10Y', 'US30Y', 'US02Y'], timeframe='daily')
        """
        if bonds is None:
            bonds = ['US02Y', 'US05Y', 'US10Y', 'US30Y', 'DX']

        return self.scan_symbols(bonds, timeframe=timeframe)

    def scan_multi_timeframe(
        self,
        symbols: list[str],
        timeframes: list[str] | None = None,
    ) -> dict[str, pd.DataFrame]:
        """
        Scan symbols across multiple timeframes.

        Args:
            symbols: Symbols to scan
            timeframes: List of timeframes (None = all standard timeframes)

        Returns:
            Dictionary mapping timeframe -> DataFrame

        Example:
            >>> scanner = MultiAssetScanner()
            >>> results = scanner.scan_multi_timeframe(
            ...     ['GOLD', 'SP500', 'GBPJPY'],
            ...     timeframes=['1hr', '4hr', 'daily']
            ... )
            >>> print(results['1hr'])  # 1-hour data
            >>> print(results['daily'])  # Daily data
        """
        if timeframes is None:
            timeframes = ['5min', '15min', '1hr', '4hr', 'daily', 'weekly', 'monthly']

        results = {}
        for tf in timeframes:
            logger.info(f"Scanning {tf} timeframe...")
            results[tf] = self.scan_symbols(symbols, timeframe=tf)

        return results

    def scan_all_markets(
        self,
        timeframe: str = 'daily',
        include_stocks: bool = False,
        include_crypto: bool = False,
    ) -> dict[str, pd.DataFrame]:
        """
        Scan all major markets.

        Args:
            timeframe: Timeframe to analyze
            include_stocks: Include stock indices
            include_crypto: Include cryptocurrencies

        Returns:
            Dictionary with results for each market

        Example:
            >>> scanner = MultiAssetScanner()
            >>> results = scanner.scan_all_markets(timeframe='4hr')
            >>> print(results['forex'])
            >>> print(results['commodities'])
            >>> print(results['bonds'])
        """
        results = {}

        # Forex
        logger.info("Scanning forex markets...")
        results['forex'] = self.scan_forex(timeframe=timeframe)

        # Commodities
        logger.info("Scanning commodities...")
        results['commodities'] = self.scan_commodities(timeframe=timeframe)

        # Indices
        logger.info("Scanning indices...")
        results['indices'] = self.scan_indices(timeframe=timeframe)

        # Bonds
        logger.info("Scanning bonds...")
        results['bonds'] = self.scan_bonds(timeframe=timeframe)

        return results

    def _normalize_timeframe(self, timeframe: str) -> str:
        """Convert user-friendly timeframe to TradingView format."""
        return TIMEFRAMES.get(timeframe.lower(), timeframe)


# Convenience functions
def scan_gold_silver(timeframe: str = 'daily', cookies: dict | None = None) -> pd.DataFrame:
    """Quick scan of gold and silver."""
    scanner = MultiAssetScanner(cookies=cookies)
    return scanner.scan_symbols(['GOLD', 'SILVER'], timeframe=timeframe)


def scan_major_indices(timeframe: str = 'daily', cookies: dict | None = None) -> pd.DataFrame:
    """Quick scan of major indices (SP500, NASDAQ, DOW)."""
    scanner = MultiAssetScanner(cookies=cookies)
    return scanner.scan_indices(['SP500', 'NASDAQ', 'DOW', 'YM30'], timeframe=timeframe)


def scan_major_forex(timeframe: str = 'daily', cookies: dict | None = None) -> pd.DataFrame:
    """Quick scan of major forex pairs."""
    scanner = MultiAssetScanner(cookies=cookies)
    return scanner.scan_forex(['GBPJPY', 'EURUSD', 'AUDUSD', 'USDJPY'], timeframe=timeframe)


def scan_treasuries(timeframe: str = 'daily', cookies: dict | None = None) -> pd.DataFrame:
    """Quick scan of US Treasury bonds."""
    scanner = MultiAssetScanner(cookies=cookies)
    return scanner.scan_bonds(timeframe=timeframe)


def scan_all_your_markets(
    timeframe: str = 'daily',
    cookies: dict | None = None
) -> dict[str, pd.DataFrame]:
    """
    Scan all markets you specified:
    - Gold, Silver
    - NASDAQ, SP500, YM30 (Dow futures)
    - GBP/JPY, EUR/USD, AUD/USD, USD/JPY
    - US Bonds

    Returns dictionary with all results.
    """
    scanner = MultiAssetScanner(cookies=cookies)

    results = {
        'commodities': scanner.scan_symbols(['GOLD', 'SILVER'], timeframe),
        'indices': scanner.scan_symbols(['NASDAQ', 'SP500', 'YM30'], timeframe),
        'forex': scanner.scan_symbols(['GBPJPY', 'EURUSD', 'AUDUSD', 'USDJPY'], timeframe),
        'bonds': scanner.scan_bonds(timeframe=timeframe),
    }

    return results
