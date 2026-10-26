#!/usr/bin/env python3
"""Check whether the FCLR-002 BTCUSDT mark series is continuous across 03-31."""
import os
import sys

os.environ["FCLR_EXPERIMENT"] = "FCLR-002"
import importlib.util

spec = importlib.util.spec_from_file_location("run_evaluation", "scripts/run_evaluation.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

train, val, test, data = m.build_panel()
mark = data["BTCUSDT"]["mark"]
print("BTCUSDT mark series length:", len(mark))
# print timestamps around the 03-30/03-31 boundary (indices 2128..2165)
for i in range(2128, min(2166, len(mark))):
    ts_ms, close = mark[i]
    dt = m.ts_to_dt(ts_ms)
    print(f"i={i} {dt.strftime('%m-%d %H:%M')} close={close:.2f}")