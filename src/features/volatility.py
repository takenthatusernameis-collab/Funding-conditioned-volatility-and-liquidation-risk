"""Realized-volatility features for Track C (volatility outcomes).

All features are computed with information available strictly at forecast time.
Forward RV is the target; trailing RVs are predictors. Missing basis/spot is NaN,
never zero.
"""
from __future__ import annotations

from typing import Dict, List, Optional

import numpy as np
import pandas as pd

EPS = 1e-18


def log_returns(close: pd.Series) -> pd.Series:
    r = np.log(close / close.shift(1))
    return r


def realized_variance(returns: pd.Series, window: int) -> pd.Series:
    """Rolling realized variance over `window` non-overlapping-ish bars.

    Uses a rolling sum of squared log returns (inclusive of current bar's prior
    return). Result is NaN where insufficient history exists.
    """
    sq = returns ** 2
    rv = sq.rolling(window=window, min_periods=window).sum()
    return rv


def realized_vol(rv_var: pd.Series) -> pd.Series:
    return np.sqrt(rv_var.clip(lower=0.0))


def add_rv_features(
    df: pd.DataFrame,
    short_windows: Optional[List[int]] = None,
    long_windows: Optional[List[int]] = None,
) -> pd.DataFrame:
    """Add trailing RV features to a UTC-indexed klines frame.

    Expects columns: close. Adds rv_trail_{w} (variance) and rv_ratio_{short}_{long}.
    """
    if short_windows is None:
        short_windows = [6, 24]
    if long_windows is None:
        long_windows = [168]
    out = df.copy()
    rets = log_returns(out["close"])
    for w in short_windows + long_windows:
        out[f"rv_trail_{w}"] = realized_variance(rets, w)
    # ratios
    for sw in short_windows:
        for lw in long_windows:
            short = out[f"rv_trail_{sw}"]
            long = out[f"rv_trail_{lw}"]
            out[f"rv_ratio_{sw}_{lw}"] = short / long.replace(0.0, np.nan)
    return out


def forward_rv(
    close: pd.Series,
    horizon: int,
    annualize: bool = False,
    bars_per_year: int = 24 * 365,
) -> pd.Series:
    """Forward realized variance over the next `horizon` bars.

    Returns a Series aligned to the forecast-origin index. The value at origin t
    is the sum of squared log returns over the forward window [t+1 .. t+horizon].
    Values are NaN where the forward window is not fully observed (no leakage:
    future bars are required). The sum is of *squared* returns, so the result is
    non-negative; a prior signed-return variant produced negative targets and
    invalid log-target regressions and has been removed.
    """
    rets = log_returns(close)
    sq = rets ** 2
    # rolling sum over the window ending at t+horizon-1 covers rets[t+1..t+horizon];
    # shift it back by (horizon-1) so the value lands on the origin t.
    fwd = sq.rolling(window=horizon, min_periods=horizon).sum().shift(-(horizon - 1))
    if annualize:
        fwd = fwd * (bars_per_year / horizon)
    return fwd


def forward_rv_vol(close: pd.Series, horizon: int, **kwargs) -> pd.Series:
    return np.sqrt(forward_rv(close, horizon, **kwargs).clip(lower=0.0))