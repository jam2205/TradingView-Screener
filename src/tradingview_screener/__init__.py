"""
.. include:: ../../README.md
"""

from __future__ import annotations

from tradingview_screener.column import Column, col
from tradingview_screener.query import Query, And, Or

# ML Extension Modules (optional imports)
try:
    from tradingview_screener.ml_collector import MLDataCollector
    from tradingview_screener import features
    __ml_available__ = True
except ImportError:
    __ml_available__ = False

# Multi-Asset Scanner (optional imports)
try:
    from tradingview_screener.multi_asset_scanner import (
        MultiAssetScanner,
        scan_all_your_markets,
        scan_gold_silver,
        scan_major_indices,
        scan_major_forex,
        scan_treasuries,
        MAJOR_SYMBOLS,
        MARKETS,
        TIMEFRAMES
    )
    __multi_asset_available__ = True
except ImportError:
    __multi_asset_available__ = False
