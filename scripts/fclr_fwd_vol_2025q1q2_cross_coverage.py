#!/usr/bin/env python3
"""Coverage + train-feasibility audit for FCLR-FWD-VOL-2025Q1Q2-CROSS (P1, Track C).

Window: the contiguous, READY, disjoint, funding-backed cached months
2025-11-01 .. 2026-04-30 (Binance public archive). Prior period tests consumed
2024 H2, 2025-02..2025-05, 2025-07..2025-10, 2026-05..2026-08 and 2026-08..2026-10;
2025-11..2026-04 has never been used for a test block.

This audit emits ONLY row counts (model-ready inputs, 24h target) and train-span
arithmetic. It computes NO outcome, NO feature value, NO model fit, NO metric.

Usage:
  python3 scripts/fclr_fwd_vol_2025q1q2_cross_coverage.py
"""
from __future__ import annotations

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

EXPERIMENT_ID = "FCLR-FWD-VOL-2025Q1Q2-CROSS-COVERAGE"
DATA_START = "2025-05-01T00:00:00Z"   # funding history start (train + 90d |funding| pct)
DATA_END = "2026-04-30T23:00:00Z"
TRAIN_START = "2025-05-01T00:00:00Z"
EMBARGO_DAYS = 7
BLOCKS = [
    ("2026-01-01T00:00:00Z", "2026-01-31T23:00:00Z"),
    ("2026-02-01T00:00:00Z", "2026-03-02T23:00:00Z"),
    ("2026-03-03T00:00:00Z", "2026-04-01T23:00:00Z"),
]
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
    out_utc = now_utc()
    start, end = _d(DATA_START), _d(DATA_END)
    train_start = _d(TRAIN_START)

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
    for i, (bs, be) in enumerate(BLOCKS):
        b0, b1 = _d(bs), _d(be)
        m = (panel_valid["ts"] >= b0) & (panel_valid["ts"] <= b1)
        sub = panel_valid[m]
        train_end = b0 - pd.Timedelta(days=EMBARGO_DAYS)
        train_days = float((train_end - train_start) / pd.Timedelta(days=1))
        train_spans.append(train_days)
        block_rows.append({
            "block": i, "test_start": bs, "test_end": be,
            "test_days": float((b1 - b0) / pd.Timedelta(days=1)) + 1.0,
            "train_end": train_end.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "train_days": round(train_days, 3),
            "rows": int(m.sum()),
            "symbols_with_rows": int(sub["symbol"].nunique()),
            "rows_per_symbol": {s: int(n) for s, n in sub["symbol"].value_counts().items()},
        })

    # Non-overlap of test blocks and disjointness from prior tested windows.
    tests = [(_d(b[0]), _d(b[1])) for b in BLOCKS]
    non_overlapping = True
    for i in range(len(tests)):
        for j in range(i + 1, len(tests)):
            if tests[i][0] <= tests[j][1] and tests[j][0] <= tests[i][1]:
                non_overlapping = False
    disjoint_from_prior = True
    overlap_notes = []
    for i, (ts, te) in enumerate(tests):
        for (a, b) in TESTED_WINDOWS:
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
        "train_start": TRAIN_START,
        "embargo_days": EMBARGO_DAYS,
        "blocks": BLOCKS,
        "models": {k: v for k, v in fwd.MODEL_FEATURES.items()},
        "per_symbol": per_symbol,
        "per_block": block_rows,
        "train_days_per_block": [round(t, 3) for t in train_spans],
        "n_symbols": int(panel_valid["symbol"].nunique()),
        "n_model_rows": int(len(panel_valid)),
        "checks": checks,
        "feasible": bool(feasible),
        "no_outcomes_computed": True,
    }
    safe = out_utc.replace(":", "").replace("-", "")
    out = RS / f"coverage_audit_fwd_vol_2025q1q2_cross_{safe}.json"
    out.write_text(json.dumps(payload, indent=1))
    print(json.dumps({"artifact": out.name, "feasible": feasible, "checks": checks,
                      "train_days_per_block": payload["train_days_per_block"],
                      "n_symbols": payload["n_symbols"],
                      "n_model_rows": payload["n_model_rows"],
                      "blocks": [{k: r[k] for k in ("block", "rows", "symbols_with_rows")}
                                 for r in block_rows]}, indent=1))


if __name__ == "__main__":
    main()