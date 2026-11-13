#!/usr/bin/env python3
"""Coverage-only audit for FCLR-FWD-VOL-2024-CROSS (P2, Track C volatility).

Counts finite rows for every model input and the primary 24h target on a frozen
hourly grid, per 30-day block, over the cached Binance 2024-07-01..2024-09-30
window (funding history begins 2024-04, so a 90-day causal |funding| percentile
is fully populated before block 0).

Emits NO outcome, NO feature values, NO model fit, NO metric. Coverage only.

Usage:
  python3 scripts/fclr_fwd_vol_2024_cross_coverage.py
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

EXPERIMENT_ID = "FCLR-FWD-VOL-2024-CROSS-20261113T091500Z"
DATA_START = "2024-07-01T00:00:00Z"
DATA_END = "2024-09-30T23:00:00Z"
BLOCKS = [
    ("2024-07-01T00:00:00Z", "2024-07-30T23:00:00Z"),
    ("2024-07-31T00:00:00Z", "2024-08-29T23:00:00Z"),
    ("2024-08-30T00:00:00Z", "2024-09-28T23:00:00Z"),
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
    for i, (bs, be) in enumerate(BLOCKS):
        b0, b1 = pd.Timestamp(bs, tz=UTC), pd.Timestamp(be, tz=UTC)
        m = (panel_valid["ts"] >= b0) & (panel_valid["ts"] <= b1)
        sub = panel_valid[m]
        block_rows.append({
            "block": i, "start": bs, "end": be,
            "rows": int(m.sum()),
            "symbols_with_rows": int(sub["symbol"].nunique()),
            "rows_per_symbol": {s: int(n) for s, n in sub["symbol"].value_counts().items()},
        })

    checks = {
        "instruments_ge_5": int(panel_valid["symbol"].nunique()) >= 5,
        "blocks_ge_3": len(BLOCKS) >= 3,
        "every_block_symbols_ge_5": all(r["symbols_with_rows"] >= 5 for r in block_rows),
        "every_block_rows_ge_100": all(r["rows"] >= 100 for r in block_rows),
        "target_present": int(panel_valid["target_24h"].notna().sum()) > 0,
    }

    payload = {
        "experiment_id": EXPERIMENT_ID,
        "kind": "coverage_audit_only",
        "generated_utc": out_utc,
        "prereg": "prereg_fclr_fwd_vol_2024_cross_20261113T091500Z.json",
        "data_start": DATA_START,
        "data_end": DATA_END,
        "blocks": BLOCKS,
        "models": {k: v for k, v in fwd.MODEL_FEATURES.items()},
        "input_columns": INPUT_COLS,
        "per_symbol": per_symbol,
        "per_block": block_rows,
        "n_symbols": int(panel_valid["symbol"].nunique()),
        "n_model_rows": int(len(panel_valid)),
        "checks": checks,
        "no_outcomes_computed": True,
    }
    safe = out_utc.replace(":", "").replace("-", "")
    out = RS / f"coverage_audit_fwd_vol_2024_cross_{safe}.json"
    out.write_text(json.dumps(payload, indent=1))
    print(json.dumps({"artifact": out.name, "checks": checks,
                      "n_symbols": payload["n_symbols"],
                      "n_model_rows": payload["n_model_rows"],
                      "blocks": [{k: r[k] for k in ("block", "rows", "symbols_with_rows")}
                                 for r in block_rows]}, indent=1))


if __name__ == "__main__":
    main()