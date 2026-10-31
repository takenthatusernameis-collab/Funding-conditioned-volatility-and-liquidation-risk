#!/usr/bin/env python3
"""Rigorous block-count audit for FCLR-003 / FCLR-006 / FCLR-007 test windows.

Counts non-overlapping 30-day blocks inside each frozen test window under
three defensible definitions, so the gate criterion (>=3 blocks) can be
evaluated without ambiguity. Writes a machine-readable report to
research_state/fclr006_block_audit.json and prints a summary.

NO recomputation of model outcomes. Only split-boundary arithmetic on
pre-registered test windows recorded in run_manifest.json.
"""
import json
import datetime as dt
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
MANIFEST = REPO / "research_state" / "run_manifest.json"
OUT_JSON = REPO / "research_state" / "fclr006_block_audit.json"

# Frozen test windows taken verbatim from run_manifest.json split_boundaries_*
WINDOWS = {
    "FCLR-003": {"test_start": "2024-10-02T00:00:00Z", "test_end": "2024-12-31T23:00:00Z"},
    "FCLR-006": {"test_start": "2026-05-23T00:00:00Z", "test_end": "2026-08-06T23:00:00Z"},
    "FCLR-007": {"test_start": "2026-07-21T00:00:00Z", "test_end": "2026-07-31T23:00:00Z"},
}


def parse(s):
    return dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)


def count_blocks(start, end, block_days=30, require_full=True):
    """Count non-overlapping blocks of block_days inside [start, end].

    require_full=True  -> only blocks spanning a FULL block_days count.
    require_full=False -> count every block including a shorter final block.
    """
    cursor = start
    full_blocks = 0
    total_blocks = 0
    block_ranges = []
    while cursor < end:
        nxt = cursor + dt.timedelta(days=block_days)
        if nxt <= end:
            full_blocks += 1
            total_blocks += 1
            block_ranges.append((cursor, nxt))
            cursor = nxt
        else:
            # remainder block
            if not require_full:
                total_blocks += 1
                block_ranges.append((cursor, end))
            cursor = end  # advance to terminate
    return total_blocks, full_blocks, block_ranges


def main():
    manifest = json.loads(MANIFEST.read_text())
    results = {}
    for name, w in WINDOWS.items():
        s = parse(w["test_start"])
        e = parse(w["test_end"])
        span_days = (e - s).total_seconds() / 86400.0
        total_strict, full_strict, _ = count_blocks(s, e, require_full=True)
        total_loose, full_loose, ranges = count_blocks(s, e, require_full=False)
        results[name] = {
            "test_start": w["test_start"],
            "test_end": w["test_end"],
            "span_days": round(span_days, 2),
            "blocks_strict_full_only": total_strict,
            "blocks_loose_including_partial": total_loose,
            "gate_3_blocks_strict": total_strict >= 3,
            "gate_3_blocks_loose": total_loose >= 3,
            "block_ranges_loose": [
                {"start": a.strftime("%Y-%m-%dT%H:%M:%SZ"),
                 "end": b.strftime("%Y-%m-%dT%H:%M:%SZ"),
                 "days": round((b - a).total_seconds() / 86400.0, 2)}
                for a, b in ranges
            ],
        }

    report = {
        "generated": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "head": None,
        "purpose": "Rigorous non-overlapping 30-day block count for FCLR-003/006/007 test windows",
        "definitions": {
            "strict": "only full 30-day blocks count (partial trailing block discarded)",
            "loose": "every non-overlapping block counts, including a shorter final block",
        },
        "windows": results,
        "manifest_split_boundaries_fclr006": manifest.get("split_boundaries_fclr006", {}).get(
            "block_requirement"
        ),
    }
    OUT_JSON.write_text(json.dumps(report, indent=2) + "\n")

    for name, r in results.items():
        print(f"{name}: span={r['span_days']}d  strict_blocks={r['blocks_strict_full_only']} "
              f"(gate>=3: {r['gate_3_blocks_strict']})  loose_blocks={r['blocks_loose_including_partial']} "
              f"(gate>=3: {r['gate_3_blocks_loose']})")
    print(f"\nWrote {OUT_JSON}")


if __name__ == "__main__":
    main()