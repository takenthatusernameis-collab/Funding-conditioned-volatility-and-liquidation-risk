from __future__ import annotations

import math
from typing import List, Optional, Tuple

EPS = 1e-18


def log_returns(prices: List[float]) -> List[Optional[float]]:
    out = []
    for i in range(1, len(prices)):
        a, b = prices[i-1], prices[i]
        if a is None or b is None or a <= 0 or b <= 0:
            out.append(None)
        else:
            out.append(math.log(b / a))
    return out


def realized_variance(returns: List[Optional[float]]) -> Optional[float]:
    vals = [r for r in returns if r is not None]
    if not vals:
        return None
    return sum(r*r for r in vals)


def trailing_rv(prices: List[float], idx: int, window: int) -> Optional[float]:
    if idx - window < 0:
        return None
    seg = prices[idx - window : idx + 1]
    rets = log_returns(seg)
    if any(r is None for r in rets):
        return None
    return realized_variance(rets)


def forward_rv(prices: List[float], idx: int, horizon: int) -> Optional[float]:
    if idx + horizon >= len(prices):
        return None
    seg = prices[idx : idx + 1 + horizon]  # include current
    rets = log_returns(seg)
    if any(r is None for r in rets):
        return None
    return realized_variance(rets)
