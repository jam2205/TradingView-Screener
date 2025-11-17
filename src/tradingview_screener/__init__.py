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
