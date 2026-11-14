#!/usr/bin/env python3
"""Coverage + train-feasibility audit for FCLR-FWD-VOL-2025-DISJOINT-CROSS (P1, Track C).

Three disjoint, never-tested 30-day Binance test blocks:
  2025-06, 2025-11, 2025-12
Each has its own 30-day train window and a 7-day embargo. Training months may
overlap prior tested windows as legitimate pre-test history; only the test
months must be disjoint from every prior evaluated window.

This audit emits ONLY finite-row counts (model-ready inputs, 24h target) and
train-span arithmetic. It computes NO outcome, NO feature value, NO model fit,
NO metric.

Usage:
  python3 scripts/coverage_audit_fwd_vol_2025_disjoint_cross.py
  python3 scripts/coverage_audit_fwd_vol_2025_disjoint_cross.py --out-utc 2026-11-14T18:30:00Z
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[1]
if str(REPO / "scripts") not in sys.path:
    sys.path.insert(0, str(REPO / "scripts"))
import fclr_fwd_vol_confirm as fwd  # noqa: E402

RS = REPO / "research_state"
UTC = fwd.UTC

EXPERIMENT_ID = "FCLR-FWD-VOL-2025-DISJOINT-CROSS-COVERAGE"
DATA_START = "2025-04-25T00:00:00Z"
DATA_END = "2025-12-31T23:00:00Z"
BLOCKS = [
    {"block": 0,
     "train_start": "2025-04-25T00:00:00Z",
     "train_end": "2025-05-24T23:00:00Z",
     "test_start": "2025-06-01T00:00:00Z",
     "test_end": "2025-06-30T23:00:00Z"},
    {"block": 1,
     "train_start": "2025-09-25T00:00:00Z",
     "train_end": "2025-10-24T23:00:00Z",
     "test_start": "2025-11-01T00:00:00Z",
     "test_end": "2025-11-30T23:00:00Z"},
    {"block": 2,
     "train_start": "2025-10-25T00:00:00Z",
     "train_end": "2025-11-23T23:00:00Z",
     "test_start": "2025-12-01T00:00:00Z",
     "test_end": "2025-12-31T23:00:00Z"},
]
# Prior evaluated test windows; train months may overlap these as history.
TESTED_WINDOWS = [
    ("2024-07-23", "2024-09-30"),
    ("2025-02-01", "2025-05-31"),
    ("2025-07-23", "2025-10-15"),
    ("2026-05-01", "2026-08-31"),
    ("2026-08-03", "2026-10-31"),
]


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _d(s: str) -> pd.Timestamp:
    return pd.Timestamp(s, tz=UTC)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-utc", default=None)
    args = ap.parse_args()

    out_utc = args.out_utc or now_utc()
    start, end = _d(DATA_START), _d(DATA_END)

    panels, per_symbol = [], {}
    for sym in fwd.SYMBOLS:
        df = fwd.build_symbol(sym, start, end)
        panels.append(df)
        sub = df[fwd.common_valid_mask(df)]
        per_symbol[sym] = {
            "grid_rows": int(len(df)),
            "model_ready_rows": int(len(sub)),
            "target_24h_rows": int(df["target_24h"].notna().sum()),
            "funding_nonnull_rows": int(df["signed_funding"].notna().sum()),
        }
    panel = pd.concat(panels, ignore_index=True)
    panel_valid = panel[fwd.common_valid_mask(panel)].copy()
    panel_valid["ts"] = pd.to_datetime(panel_valid["ts"])

    block_rows = []
    train_spans = []
    for b in BLOCKS:
        b0, b1 = _d(b["test_start"]), _d(b["test_end"])
        t0, t1 = _d(b["train_start"]), _d(b["train_end"])
        m = (panel_valid["ts"] >= b0) & (panel_valid["ts"] <= b1)
        sub = panel_valid[m]
        mt = (panel_valid["ts"] >= t0) & (panel_valid["ts"] <= t1)
        sub_train = panel_valid[mt]
        train_days = float((t1 - t0) / pd.Timedelta(days=1)) + 1.0
        train_spans.append(train_days)
        block_rows.append({
            "block": b["block"],
            "train_start": b["train_start"],
            "train_end": b["train_end"],
            "test_start": b["test_start"],
            "test_end": b["test_end"],
            "test_days": float((b1 - b0) / pd.Timedelta(days=1)) + 1.0,
            "train_days": round(train_days, 3),
            "rows": int(m.sum()),
            "symbols_with_rows": int(sub["symbol"].nunique()),
            "rows_per_symbol": {s: int(n) for s, n in sub["symbol"].value_counts().items()},
            "train_rows": int(mt.sum()),
            "train_rows_per_symbol": {s: int(n) for s, n in sub_train["symbol"].value_counts().items()},
        })

    tests = [(_d(b["test_start"]), _d(b["test_end"])) for b in BLOCKS]
    non_overlapping = True
    for i in range(len(tests)):
        for j in range(i + 1, len(tests)):
            if tests[i][0] <= tests[j][1] and tests[j][0] <= tests[i][1]:
                non_overlapping = False
    disjoint_from_prior = True
    overlap_notes = []
    for i, (ts, te) in enumerate(tests):
        for a, b in TESTED_WINDOWS:
            wa, wb = _d(a + "T00:00:00Z"), _d(b + "T23:59:59Z")
            if ts <= wb and wa <= te:
                disjoint_from_prior = False
                overlap_notes.append(f"block{i} overlaps {a}..{b}")

    checks = {
        "instruments_ge_5": int(panel_valid["symbol"].nunique()) >= 5,
        "blocks_ge_3": len(BLOCKS) >= 3,
        "every_block_symbols_ge_5": all(r["symbols_with_rows"] >= 5 for r in block_rows),
        "every_block_rows_ge_100": all(r["rows"] >= 100 for r in block_rows),
        "test_blocks_non_overlapping": non_overlapping,
        "disjoint_from_prior_tested_windows": disjoint_from_prior,
        "train_ge_30_days_every_block": all(t >= 30.0 for t in train_spans),
        "target_present": int(panel_valid["target_24h"].notna().sum()) > 0,
    }
    feasible = all(checks.values())

    payload = {
        "experiment_id": EXPERIMENT_ID,
        "kind": "coverage_and_train_feasibility_audit_only",
        "generated_utc": out_utc,
        "window": {"data_start": DATA_START, "data_end": DATA_END,
                   "span_days": float((end - start) / pd.Timedelta(days=1)) + 1.0},
        "blocks": BLOCKS,
        "models": {k: v for k, v in fwd.MODEL_FEATURES.items()},
        "per_symbol": per_symbol,
        "per_block": block_rows,
        "train_days_per_block": [round(t, 3) for t in train_spans],
        "n_symbols": int(panel_valid["symbol"].nunique()),
        "n_model_rows": int(len(panel_valid)),
        "checks": checks,
        "feasible": bool(feasible),
        "overlap_notes": overlap_notes,
        "no_outcomes_computed": True,
    }
    safe = out_utc.replace(":", "").replace("-", "")
    out = RS / f"coverage_audit_fwd_vol_2025_disjoint_cross_{safe}.json"
    out.write_text(json.dumps(payload, indent=1))
    print(json.dumps({"artifact": out.name, "feasible": feasible, "checks": checks,
                      "train_days_per_block": payload["train_days_per_block"],
                      "n_symbols": payload["n_symbols"],
                      "n_model_rows": payload["n_model_rows"],
                      "blocks": [{k: r[k] for k in ("block", "rows", "symbols_with_rows")}
                                 for r in block_rows]}, indent=1))


if __name__ == "__main__":
    main()