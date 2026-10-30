#!/usr/bin/env python3
"""Coverage-only audit for FCLR-007 panel (2025-01-01..2026-03-31).

NO outcome computation. Only verifies: markPriceKlines presence, hourly
contiguity, common 5-symbol timestamp intersection, and fundingRate presence.
"""
from __future__ import annotations

import csv
import json
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CACHE = REPO / "research_state" / "data_cache"
SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]
START = datetime(2025, 1, 1, tzinfo=timezone.utc)
END = datetime(2026, 3, 31, 23, 59, 59, tzinfo=timezone.utc)


def month_dir(sym, y, m):
    return CACHE / f"{sym}_{y}_{m:02d}"


def find_mark_csv(sym, date_str):
    y, m, _ = date_str.split("-")
    base = month_dir(sym, int(y), int(m))
    for cand in [
        base / f"markPriceKlines-{date_str}" / f"{sym}-1h-{date_str}.csv",
        base / f"markPriceKlines-{date_str}" / f"{sym}-1h-{date_str}" / f"{sym}-1h-{date_str}.csv",
    ]:
        if cand.exists():
            return cand
    for p in REPO.rglob(f"{sym}-1h-{date_str}.csv"):
        if "markPrice" in str(p):
            return p
    return None


def find_funding_csv(sym, month):
    y, m = month.split("-")
    base = month_dir(sym, int(y), int(m))
    cand = base / f"{sym}-fundingRate-{month}" / f"{sym}-fundingRate-{month}.csv"
    if cand.exists():
        return cand
    for p in REPO.rglob(f"{sym}-fundingRate-{month}.csv"):
        return p
    return None


def main():
    report = {"panel": "2025-01-01..2026-03-31", "symbols": SYMBOLS, "per_symbol": {}}
    all_ts = {s: set() for s in SYMBOLS}
    missing_days = defaultdict(list)
    cur = START.replace(hour=0, minute=0, second=0, microsecond=0)
    end_day = END.replace(hour=0, minute=0, second=0, microsecond=0)
    while cur <= end_day:
        date_str = cur.strftime("%Y-%m-%d")
        for s in SYMBOLS:
            p = find_mark_csv(s, date_str)
            if not p:
                missing_days[date_str].append(s)
                continue
            try:
                with p.open() as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        try:
                            ts = int(row["open_time"])
                            dt = datetime.fromtimestamp(ts / 1000, tz=timezone.utc)
                            if START <= dt <= END:
                                all_ts[s].add(ts)
                        except Exception:
                            pass
            except Exception as e:
                missing_days[date_str].append(f"{s}:ERR{e}")
        cur += timedelta(days=1)

    for s in SYMBOLS:
        ts = sorted(all_ts[s])
        report["per_symbol"][s] = {
            "n_rows": len(ts),
            "first": datetime.fromtimestamp(ts[0] / 1000, tz=timezone.utc).isoformat() if ts else None,
            "last": datetime.fromtimestamp(ts[-1] / 1000, tz=timezone.utc).isoformat() if ts else None,
        }

    common = set.intersection(*[all_ts[s] for s in SYMBOLS]) if all_ts else set()
    common_sorted = sorted(common)
    report["common"] = {
        "n": len(common_sorted),
        "first": datetime.fromtimestamp(common_sorted[0] / 1000, tz=timezone.utc).isoformat() if common_sorted else None,
        "last": datetime.fromtimestamp(common_sorted[-1] / 1000, tz=timezone.utc).isoformat() if common_sorted else None,
    }
    gaps = []
    if len(common_sorted) > 1:
        prev = common_sorted[0]
        for t in common_sorted[1:]:
            if t - prev != 3600_000:
                gaps.append((prev, t))
            prev = t
    report["common_gaps"] = len(gaps)
    report["missing_mark_days"] = dict(missing_days)

    funding = {}
    for s in SYMBOLS:
        months = []
        y, m = 2025, 1
        while (y, m) <= (2026, 3):
            months.append(f"{y}-{m:02d}")
            m += 1
            if m > 12:
                m = 1
                y += 1
        miss = []
        n_rows = 0
        for mo in months:
            p = find_funding_csv(s, mo)
            if not p:
                miss.append(mo)
                continue
            try:
                with p.open() as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        try:
                            n_rows += 1
                        except Exception:
                            pass
            except Exception:
                miss.append(mo)
        funding[s] = {"n_rows": n_rows, "missing_months": miss}
    report["funding"] = funding

    out = REPO / "research_state" / "fclr007_coverage_audit.json"
    out.write_text(json.dumps(report, indent=1))
    print(json.dumps(report, indent=1))


if __name__ == "__main__":
    main()