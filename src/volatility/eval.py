from __future__ import annotations

import math
from typing import Dict, List, Optional, Tuple


def qlike(y: List[float], yhat: List[float]) -> Optional[float]:
    vals = []
    for a, b in zip(y, yhat):
        if a is None or b is None or a <= 0 or b <= 0:
            continue
        vals.append(a / b - math.log(a / b) - 1.0)
    if not vals:
        return None
    return sum(vals) / len(vals)


def mse(y: List[float], yhat: List[float]) -> Optional[float]:
    vals = []
    for a, b in zip(y, yhat):
        if a is None or b is None:
            continue
        d = a - b
        vals.append(d * d)
    if not vals:
        return None
    return sum(vals) / len(vals)


def mae(y: List[float], yhat: List[float]) -> Optional[float]:
    vals = []
    for a, b in zip(y, yhat):
        if a is None or b is None:
            continue
        vals.append(abs(a - b))
    if not vals:
        return None
    return sum(vals) / len(vals)
