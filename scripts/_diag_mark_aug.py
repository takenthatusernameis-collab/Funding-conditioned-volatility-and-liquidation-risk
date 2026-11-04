#!/usr/bin/env python3
"""Diagnostic: list actual mark-price days in 2026-08..2026-11 per symbol."""
from pathlib import Path
from datetime import date, timedelta

base = Path("research_state/data_cache")
prefix = "markPriceKlines-"
sym = "BTCUSDT"
days = []
for mdir in sorted(base.glob(f"{sym}_2026_*")):
    for d in sorted(mdir.glob(f"{prefix}*")):
        day = d.name[len(prefix):]
        csv = d / f"{sym}-1h-{day}.csv"
        if csv.exists() and csv.stat().st_size > 0:
            days.append(day)
days.sort()
ds = [date.fromisoformat(x) for x in days]
# print all days in Aug 2026 onwards
for d in ds:
    if d >= date(2026, 8, 1):
        print(d.isoformat())
print("count Aug-onwards:", sum(1 for d in ds if d >= date(2026, 8, 1)))