#!/usr/bin/env python3
"""Inspect the 24 rows that FCLR-002 adds relative to FCLR-001 in the test window."""
import os
import sys
from collections import Counter

os.environ["FCLR_EXPERIMENT"] = "FCLR-002"
import importlib.util

spec = importlib.util.spec_from_file_location("run_evaluation", "scripts/run_evaluation.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

train, val, test, data = m.build_panel()
mark = data["BTCUSDT"]["mark"]
fund = data["BTCUSDT"]["funding"]

# Recompute eval rows for test split only, with per-origin diagnostics.
rows = []
for i in range(len(mark)):
    ts_ms = mark[i][0]
    ts_dt = m.ts_to_dt(ts_ms)
    if not (test[0] <= ts_dt <= test[1]):
        continue
    if i < 168 or i + m.HORIZON >= len(mark):
        continue
    future_prices = [mark[i][1]] + [mark[i + 1 + j][1] for j in range(m.HORIZON)]
    y = m.realized_variance_from_prices(future_prices)
    if y is None or y <= 0:
        continue
    feats = m.build_features_for_origin(mark, fund, i)
    if feats is None:
        continue
    rows.append((ts_ms, ts_dt, i, y, feats))

print("test eval rows:", len(rows))
for ts_ms, ts_dt, i, y, f in rows:
    print(
        f"{ts_dt.strftime('%m-%d %H:%M')} i={i} y={y:.2e} "
        f"rv24h={f['rv24h']:.2e} signed_fund={f['signed_funding']} "
        f"abs_fund_pct={f['abs_fund_pct']} ema_dist={f['ema_dist']:.4f}"
    )