#!/usr/bin/env python3
"""FCLR-013 coverage audit: widest 5-instrument mark-price window across ALL cached years.

FCLR-002's audit script (scripts/fclr002_coverage_audit.py) hard-globbed the
2024_0[456789] subdirectories, so the widest-window computation silently
returned only 2024-04-01..2024-09-30 even though real mark-price data also
exists for 2024-10..2024-12, all of 2025, and 2026-01..2026-10 in
research_state/data_cache.  This script re-runs the same computation over the
full cache tree so the widest defensible 5-instrument window is known before
any outcomes are inspected.

Coverage-only: no outcomes, no splits, no model evaluation.  Deterministic,
idempotent, no network access, no credentials.
"""
from __future__ import annotations

import argparse
import glob
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CACHE = REPO / "research_state" / "data_cache"
SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]
OUT = REPO / "research_state" / "fclr013_coverage_audit.json"


def parse_mark_timestamps(sym: str) -> set[int]:
    files = glob.glob(
        str(CACHE / f"{sym}_*" / "**" / f"*{sym}-1h-*.csv"),
        recursive=True,
    )
    ts: set[int] = set()
    for f in files:
        if "markPrice" not in f:
            continue
        try:
            with open(f) as fh:
                next(fh)
                for line in fh:
                    p = line.split(",")
                    try:
                        ts.add(int(p[0]))
                    except (ValueError, IndexError):
                        continue
        except OSError:
            continue
    return ts


def contiguous_windows(ts_set: set[int]) -> list[tuple[int, int]]:
    if not ts_set:
        return []
    sorted_ts = sorted(ts_set)
    windows = []
    start = prev = sorted_ts[0]
    HOUR_MS = 3600 * 1000
    for t in sorted_ts[1:]:
        if t - prev == HOUR_MS:
            prev = t
        else:
            windows.append((start, prev))
            start = prev = t
    windows.append((start, prev))
    return windows


def fmt(ms: int) -> str:
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).isoformat()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=None)
    args = parser.parse_args(argv)
    out_path = Path(args.out) if args.out else OUT

    per_symbol = {s: parse_mark_timestamps(s) for s in SYMBOLS}
    common = set.intersection(*per_symbol.values()) if per_symbol else set()
    windows = contiguous_windows(common)
    longest = max(windows, key=lambda w: w[1] - w[0]) if windows else (None, None)

    rows = []
    for s in SYMBOLS:
        st = per_symbol[s]
        rows.append({
            "symbol": s,
            "mark_rows": len(st),
            "first": fmt(min(st)) if st else None,
            "last": fmt(max(st)) if st else None,
        })

    doc = {
        "experiment": "FCLR-013",
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "universe": SYMBOLS,
        "per_symbol": rows,
        "common_timestamps": len(common),
        "common_first": fmt(min(common)) if common else None,
        "common_last": fmt(max(common)) if common else None,
        "common_contiguous_windows": [
            {
                "start": fmt(a),
                "end": fmt(b),
                "hours": (b - a) / 3600000 + 1,
                "non_overlapping_30d_blocks": int((b - a) / 3600000 + 1) // (30 * 24),
            }
            for a, b in windows
        ],
        "longest_window": {
            "start": fmt(longest[0]) if longest[0] is not None else None,
            "end": fmt(longest[1]) if longest[1] is not None else None,
            "hours": (longest[1] - longest[0]) / 3600000 + 1 if longest[0] is not None else 0,
            "non_overlapping_30d_blocks": int(((longest[1] - longest[0]) / 3600000 + 1) // (30 * 24)) if longest[0] is not None else 0,
        },
    }
    out_path.write_text(json.dumps(doc, indent=2))
    print(json.dumps(doc, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())