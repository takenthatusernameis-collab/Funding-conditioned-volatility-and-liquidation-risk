"""Price dislocation features (premium, mark-to-index, MA deviation).

Missing basis/spot values are NaN, never zero. All features are computable
strictly at forecast time using only lagged information.
"""
from __future__ import annotations

from typing import Optional

import numpy as np
import pandas as pd


def premium_vs_index(
    mark: pd.Series, index: pd.Series
) -> pd.Series:
    """Perpetual premium = mark / index - 1. NaN where index missing."""
    m = pd.to_numeric(mark, errors="coerce")
    idx = pd.to_numeric(index, errors="coerce")
    return m / idx - 1.0


def mark_to_index(mark: pd.Series, index: pd.Series) -> pd.Series:
    m = pd.to_numeric(mark, errors="coerce")
    idx = pd.to_numeric(index, errors="coerce")
    return (m - idx) / idx.replace(0.0, np.nan)


def ma_deviation(price: pd.Series, window: int) -> pd.Series:
    p = pd.to_numeric(price, errors="coerce")
    ma = p.rolling(window=window, min_periods=window).mean()
    return (p - ma) / ma.replace(0.0, np.nan)


def ema_deviation(price: pd.Series, span: int) -> pd.Series:
    p = pd.to_numeric(price, errors="coerce")
    ema = p.ewm(span=span, adjust=False, min_periods=span).mean()
    return (p - ema) / ema.replace(0.0, np.nan)


def lagged_return(price: pd.Series, lag: int = 1) -> pd.Series:
    p = pd.to_numeric(price, errors="coerce")
    return p.pct_change(lag)


def add_price_features(
    df: pd.DataFrame,
    ma_windows: Optional[list] = None,
    ema_spans: Optional[list] = None,
) -> pd.DataFrame:
    """Add price-dislocation features to a frame that may contain close,
    mark_close, index_close columns."""
    if ma_windows is None:
        ma_windows = [24, 72, 168]
    if ema_spans is None:
        ema_spans = [24, 72]
    out = df.copy()
    if "close" in out.columns:
        for w in ma_windows:
            out[f"ma_dev_{w}"] = ma_deviation(out["close"], w)
        for sp in ema_spans:
            out[f"ema_dev_{sp}"] = ema_deviation(out["close"], sp)
        out["ret_1"] = lagged_return(out["close"], 1)
        out["ret_24"] = lagged_return(out["close"], 24)
    if "mark_close" in out.columns and "index_close" in out.columns:
        out["premium"] = premium_vs_index(out["mark_close"], out["index_close"])
        out["mark_to_index"] = mark_to_index(out["mark_close"], out["index_close"])
    return out