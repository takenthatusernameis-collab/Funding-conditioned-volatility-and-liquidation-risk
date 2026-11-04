#!/usr/bin/env python3
"""Diagnostic: find longest contiguous mark-price run per symbol in cache."""
from pathlib import Path
from datetime import date, timedelta

base = Path("research_state/data_cache")
prefix = "markPriceKlines-"
for sym in ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]:
    days = []
    for mdir in sorted(base.glob(f"{sym}_*")):
        for d in sorted(mdir.glob(f"{prefix}*")):
            day = d.name[len(prefix):]
            csv = d / f"{sym}-1h-{day}.csv"
            if csv.exists() and csv.stat().st_size > 0:
                days.append(day)
    days.sort()
    ds = [date.fromisoformat(x) for x in days]
    best = []
    cur = []
    prev = None
    for d in ds:
        if prev is None or (d - prev).days == 1:
            cur.append(d)
        else:
            if len(cur) > len(best):
                best = cur
            cur = [d]
        prev = d
    if len(cur) > len(best):
        best = cur
    # also check the tail
    tail = ds[-1] if ds else None
    print(f"{sym}: total_mark_days={len(ds)} longest_run={best[0]}..{best[-1]} ({len(best)} days) tail={tail}")