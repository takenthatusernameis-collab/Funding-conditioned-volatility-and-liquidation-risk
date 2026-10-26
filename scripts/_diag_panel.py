#!/usr/bin/env python3
"""Diagnostic: panel composition for FCLR-001 vs FCLR-002."""
import os
import sys
from collections import Counter

os.environ.setdefault("FCLR_EXPERIMENT", sys.argv[1] if len(sys.argv) > 1 else "FCLR-001")
import importlib.util

spec = importlib.util.spec_from_file_location(
    "run_evaluation", "scripts/run_evaluation.py"
)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

train, val, test, data = m.build_panel()


def in_split_dt(dt, bounds):
    lo, hi = bounds
    return lo <= dt <= hi


eval_rows = []
for sym in m.SYMBOLS:
    mark_list = data[sym]["mark"]
    fund_list = data[sym]["funding"]
    for i in range(len(mark_list)):
        ts_ms = mark_list[i][0]
        ts_dt = m.ts_to_dt(ts_ms)
        split = None
        if in_split_dt(ts_dt, train):
            split = "train"
        elif in_split_dt(ts_dt, val):
            split = "val"
        elif in_split_dt(ts_dt, test):
            split = "test"
        else:
            continue
        if i < 168:
            continue
        if i + m.HORIZON >= len(mark_list):
            continue
        future_prices = [mark_list[i][1]] + [
            mark_list[i + 1 + j][1] for j in range(m.HORIZON)
        ]
        y = m.realized_variance_from_prices(future_prices)
        if y is None or y <= 0:
            continue
        feats = m.build_features_for_origin(mark_list, fund_list, i)
        if feats is None:
            continue
        eval_rows.append({"sym": sym, "split": split, "ts_ms": ts_ms})

print("EXPERIMENT:", os.environ["FCLR_EXPERIMENT"])
print("total eval rows:", len(eval_rows))
print("per split:", Counter(r["split"] for r in eval_rows))
print("per symbol (all splits):", Counter(r["sym"] for r in eval_rows))
print("per symbol in test:", Counter(r["sym"] for r in eval_rows if r["split"] == "test"))
print("mark series lengths:", {s: len(data[s]["mark"]) for s in m.SYMBOLS})
print("funding series lengths:", {s: len(data[s]["funding"]) for s in m.SYMBOLS})