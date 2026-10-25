#!/usr/bin/env python3
"""Synthetic hypothetical mark-price boundary labels (Track B proxy).

These are modeled breach proxies only. They do not represent observed
liquidations, account-specific margin, or exchange liquidation execution.
"""
from __future__ import annotations

import math


def liquidation_boundary_price(entry_price, leverage, side="long", maintenance_margin_rate=0.0):
    if entry_price is None or entry_price <= 0 or leverage is None or leverage <= 0:
        return None
    if side == "long":
        return entry_price * (1.0 - 1.0 / leverage + maintenance_margin_rate)
    if side == "short":
        return entry_price * (1.0 + 1.0 / leverage - maintenance_margin_rate)
    raise ValueError("side must be 'long' or 'short'")


def boundary_crossed_future(mark_closes, t_index, boundary, side, horizon=24):
    # Uses only prices strictly after t_index (t+1..t+horizon); no leakage.
    if boundary is None:
        return None
    seg = mark_closes[t_index + 1 : t_index + 1 + horizon]
    if len(seg) < horizon:
        return None
    if any(p is None or (isinstance(p, float) and math.isnan(p)) for p in seg):
        return None
    if side == "long":
        return min(seg) <= boundary
    if side == "short":
        return max(seg) >= boundary
    raise ValueError("side must be 'long' or 'short'")


def synthetic_boundary_label(mark_closes, t_index, horizon=24, leverage=5.0,
                            side="long", maintenance_margin_rate=0.0,
                            entry_price=None):
    if entry_price is None:
        if t_index < 0 or t_index >= len(mark_closes):
            return None
        entry_price = mark_closes[t_index]
    boundary = liquidation_boundary_price(entry_price, leverage, side, maintenance_margin_rate)
    crossed = boundary_crossed_future(mark_closes, t_index, boundary, side, horizon)
    if crossed is None:
        return None
    return int(bool(crossed))


def attach_labels(mark_closes, horizon=24, leverage=5.0, side="long",
                  maintenance_margin_rate=0.0):
    out = []
    n = len(mark_closes)
    for i in range(n):
        out.append(synthetic_boundary_label(
            mark_closes, i, horizon=horizon, leverage=leverage, side=side,
            maintenance_margin_rate=maintenance_margin_rate))
    return out
