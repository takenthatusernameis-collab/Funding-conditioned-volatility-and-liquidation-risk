#!/usr/bin/env python3
"""FCLR-012-V coverage-only audit: 2026-08-07..2026-11-02, all 5 symbols.

COVERAGE-ONLY: computes timestamps, symbol coverage, block counts, data hashes.
NO outcome/QLIKE/model inspection of any kind.  Run BEFORE pre-registration and
BEFORE any outcome computation, per RESEARCH_PROMPT.md §14.
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
START = datetime(2026, 8, 7, tzinfo=timezone.utc)
END = datetime(2026, 11, 2, 23, 0, 0, tzinfo=timezone.utc)


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
        "experiment": "FCLR-012-V",
        "audit_type": "COVERAGE_ONLY_NO_OUTCOME_INSPECTION",
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "window": {"start": START.isoformat(), "end": END.isoformat()},
        "symbols": SYMBOLS,
        "per_symbol": {},
        "common_timestamps": None,
        "block_counts": {},
        "hashes": {},
        "gaps": [],
        "missing_days": {},
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
    if common:
        first = datetime.fromtimestamp(common[0] / 1000, tz=timezone.utc)
        last = datetime.fromtimestamp(common[-1] / 1000, tz=timezone.utc)
        span_days = (last - first).days + 1
        report["common_span_days"] = span_days
        report["block_counts"]["non_overlapping_30d"] = span_days // 30
        report["block_counts"]["remainder_days"] = span_days % 30
        # contiguous-day check
        prev = None
        gaps = []
        for ts in common:
            dt = datetime.fromtimestamp(ts / 1000, tz=timezone.utc)
            if prev is not None and (dt - prev) > timedelta(hours=2):
                gaps.append({"after": prev.isoformat(), "before": dt.isoformat()})
            prev = dt
        report["timestamp_gaps"] = gaps
    report["hashes"] = sym_hashes
    report["missing_days"] = {s: report["per_symbol"][s]["missing_mark_days"] for s in SYMBOLS}

    out = REPO / "research_state" / "fclr012v_coverage_audit.json"
    out.write_text(json.dumps(report, indent=1))
    print(f"Wrote {out}")
    print(f"Common timestamps: {len(common)}")
    print(f"Common span days: {report.get('common_span_days')}")
    print(f"Non-overlapping 30d blocks: {report['block_counts']['non_overlapping_30d']}")
    for sym in SYMBOLS:
        ps = report["per_symbol"][sym]
        print(f"  {sym}: mark_files={ps['mark_files']} "
              f"missing_days={len(ps['missing_mark_days'])} ts={ps['n_mark_timestamps']} "
              f"first={ps['first_ts']} last={ps['last_ts']}")
    print("Missing days:", {s: v for s, v in report["missing_days"].items() if v})


if __name__ == "__main__":
    main()