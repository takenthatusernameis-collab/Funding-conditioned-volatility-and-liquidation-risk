#!/usr/bin/env python3
"""FCLR-008 coverage-only audit: 2026-01-01..2026-08-06, all 5 symbols.

COVERAGE-ONLY: computes timestamps, symbol coverage, block counts, data hashes.
NO outcome/QLIKE/model inspection of any kind.
"""
import csv
import hashlib
import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CACHE = REPO / "research_state" / "data_cache"
SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]
START = datetime(2026, 1, 1, tzinfo=timezone.utc)
END = datetime(2026, 8, 6, 23, 0, 0, tzinfo=timezone.utc)


def md5_of(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def month_dirs(sym):
    out = []
    d = START
    while d <= END:
        out.append(CACHE / f"{sym}_{d.year}_{d.month:02d}")
        d += timedelta(days=32)
        d = d.replace(day=1)
    return out


def find_mark_csv(sym, date_str):
    """Locate markPriceKlines CSV for a given UTC date."""
    y, m, _ = date_str.split("-")
    base = CACHE / f"{sym}_{y}_{int(m):02d}"
    if not base.is_dir():
        return None
    cand = base / f"markPriceKlines-{date_str}" / f"{sym}-1h-{date_str}.csv"
    if cand.exists():
        return cand
    for p in REPO.rglob(f"{sym}-1h-{date_str}.csv"):
        if "markPrice" in str(p):
            return p
    return None


def find_funding_csv(sym, month):
    y, m = month.split("-")
    base = CACHE / f"{sym}_{y}_{int(m):02d}"
    cand = base / f"{sym}-fundingRate-{month}" / f"{sym}-fundingRate-{month}.csv"
    if cand.exists():
        return cand
    return None


def load_mark_timestamps(path):
    """Return sorted list of (open_ts_ms, close_price) for a markPriceKlines CSV."""
    rows = []
    with open(path, newline="") as f:
        r = csv.reader(f)
        header = next(r, None)
        for row in r:
            if not row:
                continue
            try:
                ts = int(row[0])
                close = float(row[4])
            except (ValueError, IndexError):
                continue
            rows.append((ts, close))
    return rows


def main():
    report = {
        "experiment": "FCLR-008",
        "audit_type": "COVERAGE_ONLY_NO_OUTCOME_INSPECTION",
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "window": {"start": START.isoformat(), "end": END.isoformat()},
        "symbols": SYMBOLS,
        "per_symbol": {},
        "common_timestamps": None,
        "block_counts": {},
        "hashes": {},
        "gaps": [],
    }

    all_ts = None
    for sym in SYMBOLS:
        ts_set = set()
        n_mark_files = 0
        n_fund_files = 0
        sym_hashes = {}
        d = START.replace(hour=0)
        end_day = END.replace(hour=0)
        missing_days = []
        while d <= end_day:
            date_str = d.strftime("%Y-%m-%d")
            mp = find_mark_csv(sym, date_str)
            if mp is None:
                missing_days.append(date_str)
            else:
                n_mark_files += 1
                rows = load_mark_timestamps(mp)
                ts_set.update(ts for ts, _ in rows)
                sym_hashes[f"mark_{date_str}"] = md5_of(mp)
            d += timedelta(days=1)

        # funding files
        d2 = START.replace(day=1)
        while d2 <= END:
            month = d2.strftime("%Y-%m")
            fp = find_funding_csv(sym, month)
            if fp:
                n_fund_files += 1
                sym_hashes[f"funding_{month}"] = md5_of(fp)
            d2 += timedelta(days=32)
            d2 = d2.replace(day=1)

        report["per_symbol"][sym] = {
            "mark_files": n_mark_files,
            "funding_file_count": n_fund_files,
            "missing_mark_days": missing_days,
            "n_mark_timestamps": len(ts_set),
            "first_ts": min(ts_set) if ts_set else None,
            "last_ts": max(ts_set) if ts_set else None,
        }
        if all_ts is None:
            all_ts = ts_set
        else:
            all_ts &= ts_set

    common = sorted(all_ts)
    report["common_timestamps"] = {
        "count": len(common),
        "first": common[0] if common else None,
        "last": common[-1] if common else None,
    }
    # block counts: non-overlapping 30-day (720h) blocks within common span
    if common:
        first = datetime.fromtimestamp(common[0] / 1000, tz=timezone.utc)
        last = datetime.fromtimestamp(common[-1] / 1000, tz=timezone.utc)
        span_days = (last - first).days + 1
        report["common_span_days"] = span_days
        report["block_counts"]["non_overlapping_30d"] = span_days // 30
        report["block_counts"]["remainder_days"] = span_days % 30
    report["hashes"] = sym_hashes

    out = REPO / "research_state" / "fclr008_coverage_audit.json"
    out.write_text(json.dumps(report, indent=1))
    print(f"Wrote {out}")
    print(f"Common timestamps: {len(common)}")
    print(f"Common span days: {report.get('common_span_days')}")
    print(f"Non-overlapping 30d blocks: {report['block_counts']['non_overlapping_30d']}")
    for sym in SYMBOLS:
        ps = report["per_symbol"][sym]
        print(f"  {sym}: mark_files={ps['mark_files']} "
              f"missing_days={len(ps['missing_mark_days'])} ts={ps['n_mark_timestamps']}")


if __name__ == "__main__":
    main()