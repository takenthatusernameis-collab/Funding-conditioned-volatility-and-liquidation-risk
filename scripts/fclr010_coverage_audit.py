#!/usr/bin/env python3
"""FCLR-010 coverage-only audit: Hyperliquid, 2025-11-01..2026-10-31.

COVERAGE-ONLY: computes timestamps, symbol coverage, block counts, data hashes.
NO outcome/QLIKE/model inspection of any kind.
"""
import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
import os

REPO = Path(__file__).resolve().parents[1]
IRONFLOW = REPO / "research_state" / "data_cache" / "ironflow_events"

START = datetime(2025, 11, 1, tzinfo=timezone.utc)
END = datetime(2026, 10, 31, tzinfo=timezone.utc)


def md5_of(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    report = {
        "experiment": "FCLR-010",
        "audit_type": "COVERAGE_ONLY_NO_OUTCOME_INSPECTION",
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "window": {"start": START.isoformat(), "end": END.isoformat()},
        "labels": {
            "source": "ironflow_hyperliquid_liquidation_events",
            "path": str(IRONFLOW),
        },
        "predictors": {
            "source": "hyperliquid_public_api",
            "base_url": "https://api.hyperliquid.xyz/info",
            "notes": "mark/funding coverage to be audited via cached files or API probes; cached dir may exist",
        },
        "native_perps": [],
        "per_symbol": {},
        "label_hours_union": None,
        "block_counts": {},
        "hashes": {},
        "gaps": [],
        "label_summary": {},
    }

    if not IRONFLOW.exists():
        report["gaps"].append("ironflow cache missing")
        out = REPO / "research_state" / "fclr010_coverage_audit.json"
        out.write_text(json.dumps(report, indent=1))
        print(f"Wrote {out}")
        return

    files = sorted([f for f in os.listdir(IRONFLOW) if f.endswith('.parquet')])
    report["label_summary"]["files"] = files
    for f in files:
        report["hashes"][f"ironflow_{f}"] = md5_of(IRONFLOW / f)

    try:
        import pyarrow.parquet as pq
    except Exception as e:
        report["gaps"].append(f"pyarrow_import_error:{e}")
        out = REPO / "research_state" / "fclr010_coverage_audit.json"
        out.write_text(json.dumps(report, indent=1))
        print(f"Wrote {out}")
        return

    all_label_ts_union = set()
    native_set = set()
    for f in files:
        t = pq.read_table(IRONFLOW / f, columns=['timestamp', 'market'])
        markets = t.column('market').to_pylist()
        for m in markets:
            if isinstance(m, str) and m.endswith('-PERP') and ':' not in m:
                native_set.add(m)
        ts_list = t.column('timestamp').to_pylist()
        for x in ts_list:
            if hasattr(x, 'timestamp'):
                ts_s = x.timestamp()
            else:
                continue  # should not happen
            h = datetime.fromtimestamp(ts_s, tz=timezone.utc).replace(minute=0, second=0, microsecond=0)
            all_label_ts_union.add(int(h.timestamp() * 1000))

    native = sorted(list(native_set))
    report["native_perps"] = native
    report["native_perp_count"] = len(native)

    common = sorted(list(all_label_ts_union))
    report["label_hours_union"] = {
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

    out = REPO / "research_state" / "fclr010_coverage_audit.json"
    out.write_text(json.dumps(report, indent=1))
    print(f"Wrote {out}")
    print(f"Native perps: {len(native)}")
    print(f"Label union hours: {len(common)}")
    print(f"Span days: {report.get('common_span_days')}, blocks30: {report['block_counts'].get('non_overlapping_30d')}")


if __name__ == "__main__":
    main()
