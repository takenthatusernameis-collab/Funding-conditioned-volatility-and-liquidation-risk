#!/usr/bin/env python3
"""
FCLR-LIVE-ARCHIVE-08 Phase 2 — Heavy boundary-breach evaluation skeleton.
STDLIB ONLY. No numpy/pandas/pyarrow/requests. No network. Read-only cache.

This is a skeleton that must be completed with the actual heavy computation:
- Rebuild common support S from cache (mark-price only, all three layouts, dedup by open_time, close>0)
- Construct modeled boundary-breach labels (long/short, 24h horizon, constant margin/leverage scenarios)
- 3-block chronological OOS evaluation (60/20/20 + 168h embargo)
- B1 mark-price-only baseline vs C2 funding-conditioned candidate
- Metrics: AUC / log-loss / Brier
- >=2000 block-bootstrap + leave-one-symbol-out
- Write fclr_live_archive08_eval_<UTC>.json with complete results and verdict
"""

from __future__ import annotations

import csv
import datetime as dt
import hashlib
import json
import math
import os
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
RS = REPO / "research_state"
CACHE = RS / "data_cache"
SESSION = RS / "session_20261128T040000Z"

SYMBOLS = ["BNBUSDT", "BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT"]
WINDOW_START_MS = int(dt.datetime(2024, 4, 1, tzinfo=dt.timezone.utc).timestamp() * 1000)
WINDOW_END_MS = int(dt.datetime(2026, 10, 31, 23, 0, 0, tzinfo=dt.timezone.utc).timestamp() * 1000)
EMBARGO_H = 168
BLOCK_ROWS = 24
N_BOOTSTRAP = 2000
SEED = 20261126
MATERIALITY_FLOOR = 0.02


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def read_mark_price_csv(path: Path) -> list[tuple[int, float]]:
    """Read mark price kline CSV; return [(open_time_ms, close)] with close>0."""
    rows: list[tuple[int, float]] = []
    with open(path, newline="", encoding="utf-8", errors="ignore") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        if header is None:
            return rows
        # Find open_time and close column indices
        cols = {name: i for i, name in enumerate(header)}
        ot = cols.get("open_time")
        cl = cols.get("close")
        if ot is None or cl is None:
            return rows
        for r in reader:
            if len(r) <= max(ot, cl):
                continue
            try:
                t = int(r[ot])
                c = float(r[cl])
            except (ValueError, IndexError):
                continue
            if c > 0:
                rows.append((t, c))
    return rows


def build_common_support() -> dict:
    """Build common support S: sorted UTC hourly timestamps where ALL FIVE symbols
    have markPriceKlines close>0 within the 2024-04-01..2026-10-31 window.

    Handles two on-disk layouts:
      Layout 1 (nested, 2024-04..2024-09):
        {SYM}_{YYYY_MM}/markPriceKlines-YYYY-MM-DD/{SYM}-1h-YYYY-MM-DD/{SYM}-1h-YYYY-MM-DD.csv
      Layout 2 (flat, 2024-10..2026-10):
        {SYM}_{YYYY_MM}/markPriceKlines-YYYY-MM-DD/{SYM}-1h-YYYY-MM-DD.csv
    """
    per_symbol: dict[str, dict[int, float]] = {}
    for sym in SYMBOLS:
        sym_map: dict[int, float] = {}
        for d in sorted(CACHE.iterdir()):
            if not d.is_dir():
                continue
            if not d.name.startswith(sym + "_"):
                continue
            for p in sorted(d.iterdir()):
                if not p.is_dir():
                    continue
                if "markpriceklines" not in p.name.lower():
                    continue
                # Layout 1: nested subdirectory per symbol-day
                nested_found = False
                for q in sorted(p.iterdir()):
                    if not q.is_dir():
                        continue
                    nested_found = True
                    for f in sorted(q.iterdir()):
                        name = f.name.lower()
                        if not name.endswith(".csv"):
                            continue
                        _read_csv_into(sym_map, f, WINDOW_START_MS, WINDOW_END_MS)
                # Layout 2: CSV files directly inside the markPriceKlines directory
                if not nested_found:
                    for f in sorted(p.iterdir()):
                        name = f.name.lower()
                        if not name.endswith(".csv"):
                            continue
                        _read_csv_into(sym_map, f, WINDOW_START_MS, WINDOW_END_MS)
        per_symbol[sym] = sym_map

    # Intersect timestamps across all five symbols
    common: set[int] = set(per_symbol[SYMBOLS[0]].keys())
    for sym in SYMBOLS[1:]:
        common &= set(per_symbol[sym].keys())

    S = sorted(common)
    return {
        "S": S,
        "n_common": len(S),
        "per_symbol_counts": {sym: len(per_symbol[sym]) for sym in SYMBOLS},
    }


def _read_csv_into(sym_map: dict, path: Path, ws_ms: int, we_ms: int) -> None:
    """Read one mark-price CSV; add (open_time_ms, close) where close>0 and in window."""
    try:
        with open(path, newline="", encoding="utf-8", errors="ignore") as f:
            reader = csv.reader(f)
            header = next(reader, None)
            if header is None:
                return
            cols = {name: i for i, name in enumerate(header)}
            ot = cols.get("open_time")
            cl = cols.get("close")
            if ot is None or cl is None:
                return
            for r in reader:
                if len(r) <= max(ot, cl):
                    continue
                try:
                    t = int(r[ot])
                    c = float(r[cl])
                except (ValueError, IndexError):
                    continue
                if c > 0 and ws_ms <= t <= we_ms:
                    sym_map[t] = c
    except (OSError, IsADirectoryError):
        return


def main() -> None:
    result = build_common_support()
    print(f"Common support N: {result['n_common']}")
    print(f"Per-symbol counts: {result['per_symbol_counts']}")
    print("Skeleton: heavy boundary-breach evaluation not yet implemented.")


if __name__ == "__main__":
    main()
