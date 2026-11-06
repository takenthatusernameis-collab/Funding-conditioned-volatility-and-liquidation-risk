from __future__ import annotations

import math
from typing import List, Optional


def _is_finite_pos(x) -> bool:
    try:
        xf = float(x)
    except Exception:
        return False
    return math.isfinite(xf) and xf > 0


def _is_finite(x) -> bool:
    try:
        return math.isfinite(float(x))
    except Exception:
        return False


def qlike(y: List[float], yhat: List[float]) -> Optional[float]:
    vals = []
    for a, b in zip(y, yhat):
        if not (_is_finite_pos(a) and _is_finite_pos(b)):
            continue
        ratio = a / b
        vals.append(ratio - math.log(ratio) - 1.0)
    if not vals:
        return None
    return sum(vals) / len(vals)


def mse(y: List[float], yhat: List[float]) -> Optional[float]:
    vals = []
    for a, b in zip(y, yhat):
        if not (_is_finite(a) and _is_finite(b)):
            continue
        d = a - b
        vals.append(d * d)
    if not vals:
        return None
    return sum(vals) / len(vals)


def mae(y: List[float], yhat: List[float]) -> Optional[float]:
    vals = []
    for a, b in zip(y, yhat):
        if not (_is_finite(a) and _is_finite(b)):
            continue
        vals.append(abs(a - b))
    if not vals:
        return None
    return sum(vals) / len(vals)
