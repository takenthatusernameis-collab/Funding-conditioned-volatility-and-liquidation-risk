from __future__ import annotations

import math
from typing import Dict, List, Optional, Tuple


class TrainOnlyScaler:
    def __init__(self):
        self.mean_ = None
        self.std_ = None

    def fit(self, values: List[float]):
        vals = [v for v in values if v is not None and not (isinstance(v, float) and (math.isnan(v) or math.isinf(v)))]
        if not vals:
            self.mean_ = 0.0
            self.std_ = 1.0
            return self
        self.mean_ = sum(vals) / len(vals)
        var = sum((v - self.mean_) ** 2 for v in vals) / len(vals)
        self.std_ = math.sqrt(var) if var > 1e-18 else 1.0
        return self

    def transform(self, values: List[float]) -> List[float]:
        out = []
        if self.mean_ is None:
            self.fit(values)
        for v in values:
            if v is None or (isinstance(v, float) and (math.isnan(v) or math.isinf(v))):
                out.append(0.0)
            else:
                out.append((v - self.mean_) / self.std_)
        return out


def trailing_percentile(values: List[float], val: float) -> Optional[float]:
    if not values:
        return None
    cnt = sum(1 for v in values if v <= val + 1e-18)
    return cnt / len(values)


def trailing_zscore(values: List[float], val: float) -> Optional[float]:
    if not values:
        return None
    vals = [v for v in values if v is not None]
    if not vals:
        return None
    m = sum(vals) / len(vals)
    var = sum((v - m) ** 2 for v in vals) / len(vals)
    sd = math.sqrt(var) if var > 1e-18 else 0.0
    if sd < 1e-18:
        return 0.0
    return (val - m) / sd


def rv_ratio(rv_short: Optional[float], rv_long: Optional[float]) -> Optional[float]:
    if rv_short is None or rv_long is None or rv_long <= 0:
        return None
    return rv_short / rv_long


def price_dislocation_ma_deviation(price: float, ma_price: Optional[float]) -> Optional[float]:
    if ma_price is None or ma_price <= 0:
        return None
    return (price - ma_price) / ma_price


def price_dislocation_ema_deviation(price: float, ema_price: Optional[float]) -> Optional[float]:
    if ema_price is None or ema_price <= 0:
        return None
    return (price - ema_price) / ema_price
