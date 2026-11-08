#!/usr/bin/env python3
"""FCLR-002 panel builder from the LOCAL 2024-04..2024-09 Binance cache.

Delivers the exact per-origin row contract that
scripts/run_evaluation.py / scripts/cache_panel.py consume:

    (sym, ts_ms, iso, split, y, rv1h, rv24h, rv168h, signed_funding,
     abs_fund_pct, ema_dist, prem)

No network access. No outcomes beyond target/feature construction. Reads only
the admissible local cache under research_state/data_cache/<SYM>_<YYYY>_<MM>.

Writes research_state/data_cache/fclr002_panel_local.json (LFS-safe, JSON).

Usage:
    python scripts/build_fclr002_panel_local.py [--out PATH] [--sym SYM ...]
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

import run_evaluation as ev  # noqa: E402

EXPERIMENT = "FCLR-002"
SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]
HORIZON = 24
EPS = 1e-12
MIN_HISTORY = 168  # need rv168h trailing window


def parse_iso(s):
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    dt = datetime.fromisoformat(s)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def load_splits():
    m = json.loads((REPO / "research_state" / "run_manifest.json").read_text())
    sp = m["split_boundaries"]
    train = (parse_iso(sp["train"]["start"]), parse_iso(sp["train"]["end"]))
    val = (parse_iso(sp["validation"]["start"]), parse_iso(sp["validation"]["end"]))
    test = (parse_iso(sp["test"]["start"]), parse_iso(sp["test"]["end"]))
    return train, val, test


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(REPO / "research_state" / "data_cache" / "fclr002_panel_local.json"))
    ap.add_argument("--sym", action="append", default=None)
    args = ap.parse_args()

    syms = args.sym or SYMBOLS
    train, val, test = load_splits()
    start_all = parse_iso("2024-01-01T00:00:00Z")
    end_all = parse_iso("2024-09-30T23:00:00Z")
    months = ev.funding_months("2024-09", "2024-01")

    data = {}
    for sym in syms:
        data[sym] = {
            "mark": ev.load_mark_series(sym, start_all, end_all),
            "funding": ev.load_funding_series_all(sym, months),
        }

    def in_split(dt, bounds):
        lo, hi = bounds
        return lo <= dt <= hi

    rows = []
    dropped = {"short_history": 0, "no_future": 0, "bad_y": 0, "no_feats": 0}
    for sym in syms:
        mark_list = data[sym]["mark"]
        fund_list = data[sym]["funding"]
        for i in range(len(mark_list)):
            ts_ms = mark_list[i][0]
            ts_dt = ev.ts_to_dt(ts_ms)
            if in_split(ts_dt, train):
                split = "train"
            elif in_split(ts_dt, val):
                split = "val"
            elif in_split(ts_dt, test):
                split = "test"
            else:
                continue
            if i < MIN_HISTORY:
                dropped["short_history"] += 1
                continue
            if i + HORIZON >= len(mark_list):
                dropped["no_future"] += 1
                continue
            future = [mark_list[i][1]] + [mark_list[i + 1 + j][1] for j in range(HORIZON)]
            y = ev.realized_variance_from_prices(future)
            if y is None or y <= 0:
                dropped["bad_y"] += 1
                continue
            feats = ev.build_features_for_origin(mark_list, fund_list, i, sym=sym)
            if feats is None:
                dropped["no_feats"] += 1
                continue
            rows.append({
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
            })

    payload = {
        "experiment": EXPERIMENT,
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "local cache research_state/data_cache/<SYM>_<YYYY>_<MM> (no network)",
        "splits": {
            "train": [ev.dt_to_iso(train[0]), ev.dt_to_iso(train[1])],
            "val": [ev.dt_to_iso(val[0]), ev.dt_to_iso(val[1])],
            "test": [ev.dt_to_iso(test[0]), ev.dt_to_iso(test[1])],
        },
        "dropped": dropped,
        "n_rows": len(rows),
        "by_split": {s: sum(1 for r in rows if r["split"] == s) for s in ("train", "val", "test")},
        "by_sym": {s: sum(1 for r in rows if r["sym"] == s) for s in syms},
        "rows": rows,
    }
    Path(args.out).write_text(json.dumps(payload))
    print(json.dumps({"out": args.out, "n_rows": len(rows),
                      "by_split": payload["by_split"], "by_sym": payload["by_sym"],
                      "dropped": dropped}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())