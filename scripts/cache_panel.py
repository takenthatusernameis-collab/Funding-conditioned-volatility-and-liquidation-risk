#!/usr/bin/env python3
"""Cache the FCLR-002 evaluation panel to JSON for fast re-analysis.

Writes research_state/data_cache/fclr002_panel.json with per-row
(sym, ts_ms, y, rv1h, rv24h, rv168h, signed_funding, abs_fund_pct, ema_dist, prem).
Reuses the exact data discovery of scripts/run_evaluation.py so the cached
panel is identical to what the pre-registered evaluation consumes.
"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

# build_panel() reads the module-level DATA_END, which is derived from the
# FCLR_EXPERIMENT env var at import time.  Set it BEFORE importing so the
# extended 2024-04..2024-09 window is loaded.
os.environ.setdefault("FCLR_EXPERIMENT", "FCLR-002")

import run_evaluation as ev  # noqa: E402

EXPERIMENT = os.environ.get("FCLR_EXPERIMENT", "FCLR-002")
OUT = REPO / "research_state" / "data_cache" / "fclr002_panel.json"
EPS = ev.EPS
HORIZON = ev.HORIZON
SYMBOLS = ev.SYMBOLS


def in_split_dt(dt, bounds):
    lo, hi = bounds
    return lo <= dt <= hi


def main() -> None:
    train, val, test, data = ev.build_panel()

    mark_lists = {sym: data[sym]["mark"] for sym in SYMBOLS}
    rows = []
    for sym in SYMBOLS:
        mark_list = mark_lists[sym]
        fund_list = data[sym]["funding"]
        for i in range(len(mark_list)):
            ts_ms = mark_list[i][0]
            ts_dt = ev.ts_to_dt(ts_ms)
            split = None
            if in_split_dt(ts_dt, train):
                split = "train"
            elif in_split_dt(ts_dt, val):
                split = "val"
            elif in_split_dt(ts_dt, test):
                split = "test"
            else:
                continue
            if i < 168 or i + HORIZON >= len(mark_list):
                continue
            future_prices = [mark_list[i][1]] + [
                mark_list[i + 1 + j][1] for j in range(HORIZON)
            ]
            y = ev.realized_variance_from_prices(future_prices)
            if y is None or y <= 0:
                continue
            feats = ev.build_features_for_origin(mark_list, fund_list, i)
            if feats is None:
                continue
            rows.append(
                {
                    "sym": sym,
                    "ts_ms": ts_ms,
                    "iso": ev.dt_to_iso(ts_dt),
                    "split": split,
                    "y": y,
                    "rv1h": feats["rv1h"],
                    "rv24h": feats["rv24h"],
                    "rv168h": feats["rv168h"],
                    "signed_funding": feats["signed_funding"],
                    "abs_fund_pct": feats["abs_fund_pct"],
                    "ema_dist": feats["ema_dist"],
                    "prem": feats["prem"],
                }
            )

    payload = {
        "experiment": EXPERIMENT,
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "splits": {
            "train": [ev.dt_to_iso(train[0]), ev.dt_to_iso(train[1])],
            "val": [ev.dt_to_iso(val[0]), ev.dt_to_iso(val[1])],
            "test": [ev.dt_to_iso(test[0]), ev.dt_to_iso(test[1])],
        },
        "n_rows": len(rows),
        "by_split": {
            s: sum(1 for r in rows if r["split"] == s)
            for s in ("train", "val", "test")
        },
        "by_sym": {
            sym: sum(1 for r in rows if r["sym"] == sym) for sym in SYMBOLS
        },
        "rows": rows,
    }
    OUT.write_text(json.dumps(payload))
    print(f"Wrote {OUT} n={len(rows)} by_split={payload['by_split']}")


if __name__ == "__main__":
    main()