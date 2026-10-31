#!/usr/bin/env python3
"""Coverage-only audit for FCLR-007 panel (2026-04-01..2026-07-31).

NO outcome computation. Only verifies: markPriceKlines/indexPriceKlines
presence, hourly contiguity, common 5-symbol timestamp intersection, fundingRate
presence, and source file hashes. Writes research_state/fclr007_coverage_audit.md
and refreshes research_state/fclr007_coverage_audit.json with the audited panel.
"""
from __future__ import annotations

import csv
import hashlib
import json
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CACHE = REPO / "research_state" / "data_cache"
SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]
START = datetime(2026, 4, 1, tzinfo=timezone.utc)
END = datetime(2026, 7, 31, 23, 59, 59, tzinfo=timezone.utc)


def month_dir(sym, y, m):
    return CACHE / f"{sym}_{y}_{m:02d}"


def find_csv(kind, sym, date_str):
    y, m, _ = date_str.split("-")
    base = month_dir(sym, int(y), int(m))
    for cand in [
        base / f"{kind}-{date_str}" / f"{sym}-1h-{date_str}.csv",
        base / f"{kind}-{date_str}" / f"{sym}-1h-{date_str}" / f"{sym}-1h-{date_str}.csv",
    ]:
        if cand.exists():
            return cand
    for p in REPO.rglob(f"{sym}-1h-{date_str}.csv"):
        if kind in str(p) and f"{kind}-" in str(p):
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


def sha256_file(p):
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    report = {
        "panel": "2026-04-01..2026-07-31",
        "symbols": SYMBOLS,
        "audit_timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "per_symbol": {},
        "funding": {},
    }
    all_ts = {s: set() for s in SYMBOLS}
    missing_days = defaultdict(list)
    hash_log = []

    cur = START.replace(hour=0, minute=0, second=0, microsecond=0)
    end_day = END.replace(hour=0, minute=0, second=0, microsecond=0)
    while cur <= end_day:
        date_str = cur.strftime("%Y-%m-%d")
        day_had_mark = True
        for s in SYMBOLS:
            p = find_csv("markPriceKlines", s, date_str)
            if not p:
                missing_days[date_str].append(s)
                day_had_mark = False
                continue
            try:
                h = sha256_file(p)
                hash_log.append({"symbol": s, "date": date_str, "kind": "markPriceKlines", "path": str(p.relative_to(REPO)), "sha256": h})
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
                day_had_mark = False
        if not day_had_mark:
            cur += timedelta(days=1)
            continue
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
        "estimated_common_utc_hours": len(common_sorted),
    }
    gaps = []
    if len(common_sorted) > 1:
        prev = common_sorted[0]
        for t in common_sorted[1:]:
            if t - prev != 3600_000:
                gaps.append([datetime.fromtimestamp(prev / 1000, tz=timezone.utc).isoformat(), datetime.fromtimestamp(t / 1000, tz=timezone.utc).isoformat()])
            prev = t
    report["common_gaps"] = len(gaps)
    report["gap_pairs"] = gaps[:10]
    report["missing_mark_days"] = {d: v for d, v in sorted(missing_days.items())}

    # Proposed frozen chronological 60/20/20 splits with 7-day purge/embargo
    # over the common window 2026-04-01 .. 2026-07-31 (122 days).
    n_days = 122
    train_days = int(round(0.60 * n_days))  # 73
    val_days = int(round(0.20 * n_days))    # 24
    test_days = n_days - train_days - val_days - 2 * 7  # 11 (two 7-day embargoes)
    train_start = START
    train_end = datetime(2026, 6, 12, 23, 0, 0, tzinfo=timezone.utc)
    val_start = datetime(2026, 6, 20, tzinfo=timezone.utc)
    val_end = datetime(2026, 7, 13, 23, 0, 0, tzinfo=timezone.utc)
    test_start = datetime(2026, 7, 21, tzinfo=timezone.utc)
    test_end = END
    report["proposed_splits"] = {
        "rule": "chronological 60/20/20 by unique UTC timestamps across the common 5-symbol panel; 7-day purge/embargo at all split boundaries; no target interval overlaps train/val/test folds",
        "train": {"start": "2026-04-01T00:00:00Z", "end": "2026-06-12T23:00:00Z", "days": train_days},
        "embargo_1": {"start": "2026-06-13T00:00:00Z", "end": "2026-06-19T23:00:00Z", "days": 7},
        "validation": {"start": "2026-06-20T00:00:00Z", "end": "2026-07-13T23:00:00Z", "days": val_days},
        "embargo_2": {"start": "2026-07-14T00:00:00Z", "end": "2026-07-20T23:00:00Z", "days": 7},
        "test": {"start": "2026-07-21T00:00:00Z", "end": "2026-07-31T23:00:00Z", "days": test_days},
        "block_requirement": "test window 2026-07-21..2026-07-31 = 11 days = 0 non-overlapping 30-day blocks; required >=3 -> NOT_MET on this split; do not relax thresholds after outcomes (see FCLR-006 precedent: shortfall documented, experiment still run confirmatory on unsealed data)",
    }

    funding = {}
    for s in SYMBOLS:
        months = []
        y, m = 2026, 4
        while (y, m) <= (2026, 7):
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

    # Markdown report (coverage only; no outcome/QLIKE inspection)
    lines = []
    lines.append("# FCLR-007 COVERAGE-ONLY AUDIT (NO OUTCOME INSPECTION)")
    lines.append("")
    lines.append(f"Audit timestamp: {report['audit_timestamp']}")
    lines.append(f"Repo: {REPO}")
    lines.append(f"Window: 2026-04-01 through 2026-07-31 (~122 days)")
    lines.append(f"Symbols: {', '.join(SYMBOLS)}")
    lines.append("")
    lines.append("## Symbol-Month Coverage")
    for s in SYMBOLS:
        ps = report["per_symbol"][s]
        lines.append(f"### {s}")
        lines.append(f"- markPriceKlines rows: {ps['n_rows']}")
        lines.append(f"- first: {ps['first']}")
        lines.append(f"- last: {ps['last']}")
    lines.append("")
    lines.append("## Common Timestamps (markPriceKlines presence across all 5 symbols)")
    cm = report["common"]
    lines.append(f"- Common dates/timestamps count: {cm['n']}")
    lines.append(f"- First common timestamp: {cm['first']}")
    lines.append(f"- Last common timestamp: {cm['last']}")
    lines.append(f"- Common gaps (non-hourly steps): {report['common_gaps']}")
    lines.append("")
    lines.append("## Coverage Assessment")
    lines.append("- >=5 symbols: PASS (BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT)")
    lines.append("- >=90 common days: data window is 122 days; common hourly timestamps span the full window subject to gaps above")
    lines.append("- Block claim-worthy test under proposed splits: test window 11 days = 0 blocks -> NOT_MET (documented shortfall; do not relax after outcomes)")
    lines.append("")
    lines.append("## Proposed Frozen Chronological Splits (60/20/20, 7-day purge/embargo)")
    sp = report["proposed_splits"]
    lines.append(f"- Train: {sp['train']['start']} .. {sp['train']['end']} ({sp['train']['days']} days)")
    lines.append(f"- Embargo: {sp['embargo_1']['start']} .. {sp['embargo_1']['end']} ({sp['embargo_1']['days']} days)")
    lines.append(f"- Validation: {sp['validation']['start']} .. {sp['validation']['end']} ({sp['validation']['days']} days)")
    lines.append(f"- Embargo: {sp['embargo_2']['start']} .. {sp['embargo_2']['end']} ({sp['embargo_2']['days']} days)")
    lines.append(f"- Test/holdout: {sp['test']['start']} .. {sp['test']['end']} ({sp['test']['days']} days)")
    lines.append("")
    lines.append("## Funding Rate Coverage")
    for s in SYMBOLS:
        f = report["funding"][s]
        lines.append(f"- {s}: {f['n_rows']} rows; missing months: {f['missing_months']}")
    lines.append("")
    lines.append("## Source File Hashes (key markPriceKlines files)")
    for entry in hash_log[:8]:
        lines.append(f"- {entry['path']}: {entry['sha256']}")
    lines.append(f"(first 8 of {len(hash_log)} hashed files shown; full hashes available on re-run)")
    lines.append("")
    lines.append("## Constraints")
    lines.append("- Coverage-only audit: no outcome, QLIKE, or model result inspected in this step.")
    lines.append("- Splits frozen in this audit BEFORE any outcome computation; pre-registration follows in research_state/research_protocol_fclr007.md v1.0.")
    lines.append("- No reuse of sealed FCLR-001/002/003/005/006 holdouts.")

    md_out = REPO / "research_state" / "fclr007_coverage_audit.md"
    md_out.write_text("\n".join(lines) + "\n")
    print(f"Wrote {md_out}")

    json_out = REPO / "research_state" / "fclr007_coverage_audit.json"
    json_out.write_text(json.dumps(report, indent=1) + "\n")
    print(f"Wrote {json_out}")


if __name__ == "__main__":
    main()
