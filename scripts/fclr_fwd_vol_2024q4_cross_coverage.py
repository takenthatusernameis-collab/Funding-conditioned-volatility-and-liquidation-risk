#!/usr/bin/env python3
"""Coverage-only audit for FCLR-FWD-VOL-2024Q4-CROSS (P1, Track C volatility).

Counts finite rows for every model input and the primary 24h target on a frozen
hourly grid, per rolling-origin block, over a window that sits entirely inside the
cached Binance mark-price coverage (mark/premium/index klines exist for
2024-07-01..2024-09-30; funding history exists from 2024-04-01).

Emits NO outcome, NO feature values, NO model fit, NO metric. Coverage only.

Usage:
  python3 scripts/fclr_fwd_vol_2024q4_cross_coverage.py
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

import sys

REPO = Path(__file__).resolve().parents[1]
if str(REPO / "scripts") not in sys.path:
    sys.path.insert(0, str(REPO / "scripts"))
import fclr_fwd_vol_confirm as fwd  # noqa: E402

RS = REPO / "research_state"
UTC = fwd.UTC

EXPERIMENT_ID = "FCLR-FWD-VOL-2024Q4-CROSS-20261113T091500Z"
DATA_START = "2024-07-01T00:00:00Z"
DATA_END = "2024-09-30T23:00:00Z"
BLOCKS = [
    ("2024-07-16T23:00:00Z", "2024-07-23T00:00:00Z", "2024-08-21T23:00:00Z"),
    ("2024-08-13T23:00:00Z", "2024-08-20T00:00:00Z", "2024-09-18T23:00:00Z"),
    ("2024-09-09T23:00:00Z", "2024-09-16T00:00:00Z", "2024-09-30T23:00:00Z"),
]


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def main() -> None:
    out_utc = now_utc()
    start = pd.Timestamp(DATA_START, tz=UTC)
    end = pd.Timestamp(DATA_END, tz=UTC)

    panels, per_symbol = [], {}
    for sym in fwd.SYMBOLS:
        df = fwd.build_symbol(sym, start, end)
        panels.append(df)
        sub = df[fwd.common_valid_mask(df)]
        per_symbol[sym] = {
            "grid_rows": int(len(df)),
            "mark_rows": int(df["mark"].notna().sum()),
            "model_ready_rows": int(len(sub)),
            "target_24h_rows": int(df["target_24h"].notna().sum()),
        }
    panel = pd.concat(panels, ignore_index=True)
    panel_valid = panel[fwd.common_valid_mask(panel)].copy()
    panel_valid["ts"] = pd.to_datetime(panel_valid["ts"])

    block_rows = []
    for i, (te, ts, te2) in enumerate(BLOCKS):
        tr = panel_valid[panel_valid["ts"] <= pd.Timestamp(te, tz=UTC)]
        te_s = panel_valid[(panel_valid["ts"] >= pd.Timestamp(ts, tz=UTC)) &
                           (panel_valid["ts"] <= pd.Timestamp(te2, tz=UTC))]
        block_rows.append({
            "block": i, "train_end": te, "test_start": ts, "test_end": te2,
            "train_rows": int(len(tr)), "test_rows": int(len(te_s)),
            "train_symbols": int(tr["symbol"].nunique()),
            "test_symbols": int(te_s["symbol"].nunique()),
        })

    checks = {
        "instruments_ge_5": int(panel_valid["symbol"].nunique()) >= 5,
        "blocks_ge_3": len(BLOCKS) >= 3,
        "every_block_train_rows_ge_1000": all(r["train_rows"] >= 1000 for r in block_rows),
        "every_block_test_rows_ge_100": all(r["test_rows"] >= 100 for r in block_rows),
        "every_block_train_symbols_ge_5": all(r["train_symbols"] >= 5 for r in block_rows),
        "every_block_test_symbols_ge_5": all(r["test_symbols"] >= 5 for r in block_rows),
        "mark_price_present_all_months": all(v["mark_rows"] > 0 for v in per_symbol.values()),
    }

    payload = {
        "experiment_id": EXPERIMENT_ID,
        "kind": "coverage_audit_only",
        "generated_utc": out_utc,
        "data_start": DATA_START,
        "data_end": DATA_END,
        "blocks": BLOCKS,
        "input_columns": list(fwd.MODEL_FEATURES["C2"]) + ["target_24h"],
        "per_symbol": per_symbol,
        "per_block": block_rows,
        "n_symbols": int(panel_valid["symbol"].nunique()),
        "n_model_rows": int(len(panel_valid)),
        "checks": checks,
        "no_outcomes_computed": True,
    }
    safe = out_utc.replace(":", "").replace("-", "")
    out = RS / f"coverage_audit_fwd_vol_2024q4_cross_{safe}.json"
    out.write_text(json.dumps(payload, indent=1))
    print(json.dumps({"artifact": out.name, "checks": checks,
                      "n_symbols": payload["n_symbols"],
                      "n_model_rows": payload["n_model_rows"],
                      "blocks": [{k: r[k] for k in ("block", "train_rows", "test_rows")}
                                 for r in block_rows]}, indent=1))


if __name__ == "__main__":
    main()