"""Funding features for Track C.

All features use only information available at forecast time (strictly lagged).
Missing funding values are NaN, never zero.
"""
from __future__ import annotations

from typing import Optional

import numpy as np
import pandas as pd


def signed_funding(funding_rate: pd.Series) -> pd.Series:
    return pd.to_numeric(funding_rate, errors="coerce")


def abs_funding(funding_rate: pd.Series) -> pd.Series:
    return signed_funding(funding_rate).abs()


def resample_funding_to_hourly(
    funding: pd.DataFrame,
    klines_index: pd.DatetimeIndex,
    col: str = "last_funding_rate",
) -> pd.Series:
    """Map funding observations onto the hourly kline index using the last
    known funding value at or before each kline timestamp (forward-fill).

    Funding is observed 3x/day on Binance perp; this produces a stepwise series
    aligned to the hourly grid. Missing history stays NaN.
    """
    s = pd.to_numeric(funding[col], errors="coerce").dropna()
    if s.empty:
        return pd.Series(np.nan, index=klines_index, name="funding")
    s = s.sort_index()
    aligned = s.reindex(klines_index, method="ffill")
    return aligned


def trailing_funding_pct(
    funding: pd.Series, window: int
) -> pd.Series:
    """Rolling percentile rank of the current funding value within the trailing
    `window` observations (train-only in the evaluator)."""
    s = pd.to_numeric(funding, errors="coerce")
    out = pd.Series(np.nan, index=s.index, dtype=float)
    vals = s.to_numpy()
    for i in range(len(s)):
        if i + 1 < window:
            continue
        hist = vals[i + 1 - window : i + 1]
        hist = hist[~np.isnan(hist)]
        if hist.size == 0 or np.isnan(vals[i]):
            continue
        out.iloc[i] = (hist <= vals[i]).mean()
    return out


def trailing_funding_zscore(funding: pd.Series, window: int) -> pd.Series:
    s = pd.to_numeric(funding, errors="coerce")
    roll = s.rolling(window=window, min_periods=window)
    mean = roll.mean()
    std = roll.std(ddof=0)
    out = (s - mean) / std.replace(0.0, np.nan)
    return out


def add_funding_features(
    klines_index: pd.DatetimeIndex,
    funding: pd.DataFrame,
    windows: Optional[list] = None,
) -> pd.DataFrame:
    if windows is None:
        windows = [24, 72, 168]
    s = resample_funding_to_hourly(funding, klines_index)
    out = pd.DataFrame(index=klines_index)
    out["funding_signed"] = s
    out["funding_abs"] = s.abs()
    for w in windows:
        out[f"funding_pct_{w}"] = trailing_funding_pct(s, w)
        out[f"funding_z_{w}"] = trailing_funding_zscore(s, w)
    return out