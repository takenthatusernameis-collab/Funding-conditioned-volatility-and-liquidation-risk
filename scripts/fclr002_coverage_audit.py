#!/usr/bin/env python3
"""Coverage audit for FCLR-002: find the widest 5-instrument mark-price window.

FCLR-001's frozen panel is single-instrument (BTCUSDT only) because the other
four symbols have no mark-price CSVs before 2024-04-01
(research_state/coverage_audit_recheck.md).  FCLR-002 is a pre-registered
follow-up that reuses the FCLR-001 v1.0 feature/target/model definitions but
evaluates on a panel that satisfies the protocol's minimum claim-worthy test:
>=5 instruments and >=3 non-overlapping 30-day evaluation blocks.

This script computes, from the working tree only, the exact set of hourly
timestamps where all five symbols have a mark-price row, and reports the
longest contiguous 5-instrument window.  It is a coverage-only audit: no
outcomes are computed here.

Idempotent and deterministic.  No network access, no credentials.
"""
from __future__ import annotations

import glob
import json
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CACHE = REPO / "research_state" / "data_cache"
SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]
OUT = REPO / "research_state" / "fclr002_coverage_audit.json"


def parse_mark_timestamps(sym: str) -> set[int]:
    # Recursive: extracted CSVs live at
    #   <cache>/<SYM>_<YYYY_MM>/markPriceKlines-<YYYY-MM-DD>/<SYM>-1h-<YYYY-MM-DD>.csv
    # but some months were extracted into a nested zip-stem directory
    #   .../markPriceKlines-<YYYY-MM-DD>/<SYM>-1h-<YYYY-MM-DD>/<SYM>-1h-<YYYY-MM-DD>.csv
    files = glob.glob(
        str(CACHE / f"{sym}_2024_0[789]" / "**" / f"*{sym}-1h-*.csv"),
        recursive=True,
    ) + glob.glob(
        str(CACHE / f"{sym}_2024_0[456]" / "**" / f"*{sym}-1h-*.csv"),
        recursive=True,
    )
    ts: set[int] = set()
    for f in files:
        if "markPrice" not in f:
            continue
        try:
            with open(f) as fh:
                next(fh)  # header
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
    """Return [start_ms, end_ms] of maximal contiguous hourly runs."""
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


def main() -> int:
    per_symbol = {s: parse_mark_timestamps(s) for s in SYMBOLS}
    common = set.intersection(*per_symbol.values()) if per_symbol else set()
    windows = contiguous_windows(common)

    # longest window
    longest = max(windows, key=lambda w: w[1] - w[0]) if windows else (None, None)

    rows = []
    for s in SYMBOLS:
        st = per_symbol[s]
        rows.append({
            "symbol": s,
            "mark_rows": len(st),
            "first": datetime.fromtimestamp(min(st) / 1000, tz=timezone.utc).isoformat() if st else None,
            "last": datetime.fromtimestamp(max(st) / 1000, tz=timezone.utc).isoformat() if st else None,
        })

    doc = {
        "experiment": "FCLR-002",
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "universe": SYMBOLS,
        "per_symbol": rows,
        "common_timestamps": len(common),
        "common_first": datetime.fromtimestamp(min(common) / 1000, tz=timezone.utc).isoformat() if common else None,
        "common_last": datetime.fromtimestamp(max(common) / 1000, tz=timezone.utc).isoformat() if common else None,
        "common_contiguous_windows": [
            {
                "start": datetime.fromtimestamp(a / 1000, tz=timezone.utc).isoformat(),
                "end": datetime.fromtimestamp(b / 1000, tz=timezone.utc).isoformat(),
                "hours": (b - a) / 3600000 + 1,
            }
            for a, b in windows
        ],
        "longest_window": {
            "start": datetime.fromtimestamp(longest[0] / 1000, tz=timezone.utc).isoformat() if longest[0] else None,
            "end": datetime.fromtimestamp(longest[1] / 1000, tz=timezone.utc).isoformat() if longest[1] else None,
            "hours": (longest[1] - longest[0]) / 3600000 + 1 if longest[0] is not None else 0,
        },
    }
    OUT.write_text(json.dumps(doc, indent=2))
    print(json.dumps(doc, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())