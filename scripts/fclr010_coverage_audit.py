#!/usr/bin/env python3
"""FCLR-010 coverage-only audit: Hyperliquid, 2025-11-01..2026-10-31.

COVERAGE-ONLY: computes timestamps, symbol coverage, block counts, data hashes.
NO outcome/QLIKE/model inspection of any kind.

FCLR-NEXT-112: routed through guarded_execute contract. Direct parquet reads are
an explicit outcome_loader invoked ONLY after guarded_execute returns READY_FROZEN.
Blocked branches refuse before any parquet read.
"""
import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Dict, Optional

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


def _load_coverage_outcomes(data_path: Path, context: Optional[Dict] = None) -> Dict:
    """Explicit outcome/parquet loader for coverage audit.

    Invoked ONLY after guarded_execute returns READY_FROZEN. Reads parquet to
    compute coverage statistics (no outcome/QLIKE/model inspection).
    """
    import pyarrow.parquet as pq

    files = sorted([f for f in os.listdir(data_path) if f.endswith('.parquet')]) if data_path.exists() else []
    native_set = set()
    all_label_ts_union = set()
    hashes = {}
    for f in files:
        fpath = data_path / f
        hashes[f"ironflow_{f}"] = md5_of(fpath)
        t = pq.read_table(fpath, columns=['timestamp', 'market'])
        markets = t.column('market').to_pylist()
        for m in markets:
            if isinstance(m, str) and m.endswith('-PERP') and ':' not in m:
                native_set.add(m)
        ts_list = t.column('timestamp').to_pylist()
        for x in ts_list:
            if hasattr(x, 'timestamp'):
                ts_s = x.timestamp()
            else:
                continue
            h = datetime.fromtimestamp(ts_s, tz=timezone.utc).replace(minute=0, second=0, microsecond=0)
            all_label_ts_union.add(int(h.timestamp() * 1000))

    native = sorted(list(native_set))
    common = sorted(list(all_label_ts_union))
    block_counts = {}
    if common:
        first = datetime.fromtimestamp(common[0] / 1000, tz=timezone.utc)
        last = datetime.fromtimestamp(common[-1] / 1000, tz=timezone.utc)
        span_days = (last - first).days + 1
        block_counts["non_overlapping_30d"] = span_days // 30
        block_counts["remainder_days"] = span_days % 30
    return {
        "files": files,
        "hashes": hashes,
        "native_perps": native,
        "native_perp_count": len(native),
        "label_hours_union": {
            "count": len(common),
            "first": common[0] if common else None,
            "last": common[-1] if common else None,
        },
        "block_counts": block_counts,
    }


def main():
    from scripts.fclr010_guarded_entry import guarded_execute, refusal_payload

    guard = guarded_execute(
        data_path=IRONFLOW,
        pre_reg_path=None,
        repo_root=REPO,
        source_manifest=None,
        admissible_manifest=None,
        admissible_manifest_path=None,
        outcome_loader=_load_coverage_outcomes,
        loader_context=None,
        allow_default_loader=False,
    )
    if guard.get("status") != "READY_FROZEN":
        payload = refusal_payload(
            reason="fclr010_coverage_audit refused: no guarded READY_FROZEN contract (admissible seam + prereg + manifest/data gates). Direct parquet reads bypassed.",
            reason_code="PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS",
            script="fclr010_coverage_audit",
            guard=guard,
        )
        print(json.dumps(payload, indent=2, sort_keys=True))
        print(f"=== FCLR-010-COVERAGE-AUDIT BLOCKED {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')} ===", flush=True)
        return 1

    loaded = guard.get("outcomes_loaded")
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
        "native_perps": loaded["native_perps"],
        "native_perp_count": loaded["native_perp_count"],
        "label_summary": {"files": loaded["files"], "hashes": loaded["hashes"]},
        "label_hours_union": loaded["label_hours_union"],
        "block_counts": loaded["block_counts"],
        "gaps": [],
    }
    if loaded["block_counts"]:
        span = loaded["label_hours_union"]["count"] // 24 + 1
        report["common_span_days"] = span
        report["block_counts"] = loaded["block_counts"]

    out = REPO / "research_state" / "fclr010_coverage_audit.json"
    out.write_text(json.dumps(report, indent=1))
    print(f"Wrote {out}")
    print(f"Native perps: {len(loaded['native_perps'])}")
    print(f"Label union hours: {loaded['label_hours_union']['count']}")
    print(f"Span days: {report.get('common_span_days')}, blocks30: {loaded['block_counts'].get('non_overlapping_30d')}")
    return 0


if __name__ == "__main__":
    import os
    import sys
    sys.exit(main())
