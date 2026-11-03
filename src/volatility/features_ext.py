from __future__ import annotations

import math
from typing import Dict, List, Optional, Tuple


EPS = 1e-18


def log_returns(prices: List[float]) -> List[Optional[float]]:
    out = []
    for i in range(1, len(prices)):
        a, b = prices[i - 1], prices[i]
        if a is None or b is None or a <= 0 or b <= 0:
            out.append(None)
        else:
            out.append(math.log(b / a))
    return out


def realized_variance_from_rets(returns: List[Optional[float]]) -> Optional[float]:
    vals = [r for r in returns if r is not None]
    if not vals:
        return None
    return sum(r * r for r in vals)


def trailing_rv(prices: List[float], idx: int, window: int) -> Optional[float]:
    if idx < 0 or idx - window < 0:
        return None
    seg = prices[idx - window : idx + 1]
    rets = log_returns(seg)
    if any(r is None for r in rets):
        return None
    rv = realized_variance_from_rets(rets)
    if rv is None:
        return None
    return rv


def forward_rv(prices: List[float], idx: int, horizon: int) -> Optional[float]:
    if idx < 0 or idx + horizon >= len(prices):
        return None
    seg = prices[idx : idx + 1 + horizon]
    rets = log_returns(seg)
    if any(r is None for r in rets):
        return None
    rv = realized_variance_from_rets(rets)
    if rv is None:
        return None
    return rv


def rolling_percentile_trailing(values_trailing: List[float], val: float) -> Optional[float]:
    if not values_trailing:
        return None
    # count <= val
    cnt = sum(1 for v in values_trailing if v <= val + 1e-18)
    return cnt / len(values_trailing)


def zscore_trailing(values_trailing: List[float], val: float) -> Optional[float]:
    if not values_trailing:
        return None
    m = sum(values_trailing) / len(values_trailing)
    var = sum((v - m) ** 2 for v in values_trailing) / len(values_trailing)
    sd = math.sqrt(var) if var > 1e-18 else 0.0
    if sd < 1e-18:
        return 0.0
    return (val - m) / sd


def ema(series: List[float], idx: int, span: int) -> Optional[float]:
    if idx < 0 or span <= 0:
        return None
    # simple EMA approximation using trailing window up to idx
    alpha = 2.0 / (span + 1.0)
    # compute from start of available up to idx? better use trailing
    start = max(0, idx - max(500, span * 10))
    ema_val = series[start]
    for i in range(start + 1, idx + 1):
        v = series[i]
        if v is None:
            continue
        ema_val = alpha * v + (1 - alpha) * ema_val
    return ema_val


def ma(series: List[float], idx: int, window: int) -> Optional[float]:
    if idx < window - 1:
        return None
    seg = series[idx - window + 1 : idx + 1]
    vals = [v for v in seg if v is not None]
    if len(vals) != len(seg):
        return None
    return sum(vals) / len(vals)
