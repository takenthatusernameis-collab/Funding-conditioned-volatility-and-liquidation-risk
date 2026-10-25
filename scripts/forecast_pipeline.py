#!/usr/bin/env python3
"""Forecast pipeline skeleton for FCLR-001 (no OOS results)."""
from __future__ import annotations

import json
import math
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
RUN_MANIFEST = REPO / "research_state" / "run_manifest.json"

EPS = 1e-12


def log_returns(prices):
    out = []
    for i in range(1, len(prices)):
        a, b = prices[i - 1], prices[i]
        if a is None or b is None or a <= 0 or b <= 0:
            out.append(None)
        else:
            out.append(math.log(b / a))
    return out


def realized_variance_from_returns(returns):
    vals = [r for r in returns if r is not None]
    if not vals:
        return None
    return sum(r * r for r in vals)


def next_realized_variance(mark_closes, t_index, horizon=24):
    # outcome uses t+1..t+horizon
    seg = mark_closes[t_index + 1 : t_index + 1 + horizon]
    if len(seg) < horizon:
        return None
    rets = log_returns([mark_closes[t_index]] + seg)
    if any(r is None for r in rets):
        return None
    return sum(r * r for r in rets)


def trailing_rv(mark_closes, t_index, window):
    if t_index - window < 0:
        return None
    seg = mark_closes[t_index - window : t_index + 1]
    rets = log_returns(seg)
    if any(r is None for r in rets):
        return None
    return sum(r * r for r in rets)


def standardize_train_only(values):
    valid = [v for v in values if v is not None]
    if not valid:
        return None, None
    m = sum(valid) / len(valid)
    var = sum((v - m) ** 2 for v in valid) / len(valid)
    sd = math.sqrt(var) if var > 0 else 0.0
    return m, sd


def apply_standardization(values, mean, sd):
    out = []
    for v in values:
        if v is None or sd in (0, None):
            out.append(None)
        else:
            out.append((v - mean) / sd)
    return out


def load_splits():
    m = json.loads(RUN_MANIFEST.read_text())
    # default frozen boundaries from protocol/manifest if present
    splits = m.get("splits", {})
    if not splits:
        splits = {
            "train": ("2024-01-02T00:00:00Z", "2024-02-24T08:00:00Z"),
            "val": ("2024-03-02T08:00:00Z", "2024-03-20T02:00:00Z"),
            "test": ("2024-03-27T02:00:00Z", "2024-03-30T23:00:00Z"),
        }
    return splits


def in_split(ts, bounds):
    lo, hi = bounds
    return lo <= ts <= hi


def common_panel_timestamps(series_by_symbol):
    if not series_by_symbol:
        return []
    sets = [set(v) for v in series_by_symbol.values()]
    inter = sets[0]
    for s in sets[1:]:
        inter = inter & s
    return sorted(inter)


if __name__ == "__main__":
    print(json.dumps(load_splits(), indent=2))
