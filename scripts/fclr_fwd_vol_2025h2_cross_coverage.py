#!/usr/bin/env python3
"""Coverage-only audit for FCLR-FWD-VOL-2025H2-CROSS (Track C volatility, P1).

Counts finite rows for every model input and the primary 24h target on a frozen
hourly grid, per 30-day block, over the cached Binance 2025-04-01..2025-10-15
window (funding history covers all 12 months of 2025, so a 90-day causal
|funding| percentile is fully populated before block 0).

Emits NO outcome, NO feature values, NO model fit, NO metric. Coverage only.

Usage:
  python3 scripts/fclr_fwd_vol_2025h2_cross_coverage.py
"""
from __future__ import annotations

import hashlib
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

EXPERIMENT_ID = "FCLR-FWD-VOL-2025H2-CROSS"
DATA_START = "2025-04-01T00:00:00Z"
DATA_END = "2025-10-15T23:00:00Z"
BLOCKS = [
    ("2025-07-16T23:00:00Z", "2025-07-23T00:00:00Z", "2025-08-21T23:00:00Z"),
    ("2025-08-13T23:00:00Z", "2025-08-20T00:00:00Z", "2025-09-18T23:00:00Z"),
    ("2025-09-09T23:00:00Z", "2025-09-16T00:00:00Z", "2025-10-15T23:00:00Z"),
]

INPUT_COLS = ["log_rv1h", "log_rv24h", "log_rv168h", "signed_funding",
              "abs_fund_pct", "premium", "ema_dist", "target_24h"]


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


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
            "model_ready_rows": int(len(sub)),
            "target_24h_rows": int(df["target_24h"].notna().sum()),
        }
    panel = pd.concat(panels, ignore_index=True)
    panel_valid = panel[fwd.common_valid_mask(panel)].copy()
    panel_valid["ts"] = pd.to_datetime(panel_valid["ts"])

    block_rows = []
    for i, (train_end, test_start, test_end) in enumerate(BLOCKS):
        b0, b1 = pd.Timestamp(test_start, tz=UTC), pd.Timestamp(test_end, tz=UTC)
        te = pd.Timestamp(train_end, tz=UTC)
        m_test = (panel_valid["ts"] >= b0) & (panel_valid["ts"] <= b1)
        m_train = (panel_valid["ts"] >= start) & (panel_valid["ts"] <= te)
        sub_test = panel_valid[m_test]
        sub_train = panel_valid[m_train]
        block_rows.append({
            "block": i, "train_end": train_end, "test_start": test_start,
            "test_end": test_end,
            "train_rows": int(m_train.sum()),
            "test_rows": int(m_test.sum()),
            "train_symbols": int(sub_train["symbol"].nunique()),
            "test_symbols": int(sub_test["symbol"].nunique()),
            "rows_per_symbol_test": {s: int(n) for s, n in sub_test["symbol"].value_counts().items()},
        })

    checks = {
        "instruments_ge_5": int(panel_valid["symbol"].nunique()) >= 5,
        "blocks_ge_3": len(BLOCKS) >= 3,
        "every_block_symbols_ge_5": all(r["test_symbols"] >= 5 for r in block_rows),
        "every_block_test_rows_ge_100": all(r["test_rows"] >= 100 for r in block_rows),
        "every_block_train_rows_ge_1000": all(r["train_rows"] >= 1000 for r in block_rows),
        "target_present": int(panel_valid["target_24h"].notna().sum()) > 0,
    }

    payload = {
        "experiment_id": "FCLR-FWD-VOL-2025H2-CROSS-20261113T101900Z",
        "kind": "coverage_audit_only",
        "generated_utc": out_utc,
        "data_start": DATA_START,
        "data_end": DATA_END,
        "blocks": [{"train_end": r["train_end"], "test_start": r["test_start"],
                    "test_end": r["test_end"]} for r in block_rows],
        "models": {k: v for k, v in fwd.MODEL_FEATURES.items()},
        "input_columns": INPUT_COLS,
        "per_symbol": per_symbol,
        "per_block": block_rows,
        "n_symbols": int(panel_valid["symbol"].nunique()),
        "n_model_rows": int(len(panel_valid)),
        "n_panel_rows": int(len(panel)),
        "checks": checks,
        "no_outcomes_computed": True,
    }
    safe = out_utc.replace(":", "").replace("-", "")
    out = RS / f"coverage_audit_fwd_vol_2025h2_cross_{safe}.json"
    out.write_text(json.dumps(payload, indent=1))
    print(json.dumps({"artifact": out.name, "checks": checks,
                      "n_symbols": payload["n_symbols"],
                      "n_model_rows": payload["n_model_rows"],
                      "blocks": [{k: r[k] for k in ("block", "train_rows", "test_rows", "train_symbols", "test_symbols")}
                                 for r in block_rows]}, indent=1))


if __name__ == "__main__":
    main()
