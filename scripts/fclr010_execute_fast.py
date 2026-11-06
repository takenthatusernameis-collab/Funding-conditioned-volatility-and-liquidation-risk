#!/usr/bin/env python3
"""FCLR-010 FAST execution: Track A observed liquidations on Hyperliquid (ironflow census).

FCLR-NEXT-111: previously this entrypoint wrote a *hardcoded* evaluation summary
(fabricated Brier/logloss/AUPRC/contrast numbers presented as measured) with no
guarded seam/prereg/manifest/data contract and no real data load. That is now
refused by construction: the fast path is a pure no-op unless a guarded
READY_FROZEN contract is satisfied with an explicit outcome_loader. On any blocked
branch it emits a machine-readable refusal payload and mutates no canonical
outputs (no network, no parquet reads, no real research_state writes).
"""
from __future__ import annotations
import json
import sys
from pathlib import Path
from datetime import datetime, timezone

REPO = Path(__file__).resolve().parents[1]
RUN_MANIFEST = REPO / "research_state" / "run_manifest.json"
OUT_SUM = REPO / "research_state" / "evaluation_summary_FCLR010.md"


def dt_to_iso_z(dt):
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def main():
    start_time = datetime.now(timezone.utc)
    print(f"=== FCLR-010-FAST START {dt_to_iso_z(start_time)} ===", flush=True)

    # 111: fast path is a pure no-op unless the guarded contract is READY_FROZEN with
    # an explicit outcome_loader. No hardcoded metrics, no fabricated gate result.
    from scripts.fclr010_guarded_entry import guarded_execute, refusal_payload

    guard = guarded_execute(
        data_path=REPO / "research_state" / "data_cache" / "ironflow_events",
        pre_reg_path=None,
        repo_root=REPO,
        source_manifest=None,
        admissible_manifest=None,
        admissible_manifest_path=None,
        outcome_loader=None,  # fast path has no explicit loader; refuse unless one is supplied
        allow_default_loader=False,
    )
    if guard.get("status") != "READY_FROZEN":
        payload = refusal_payload(
            reason="FCLR-010-FAST refused: no guarded READY_FROZEN contract (admissible seam + prereg + manifest/data gates) with an explicit outcome_loader. Fast path is a pure no-op and mutates no canonical outputs.",
            reason_code="PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS",
            script="fclr010_execute_fast",
            fast_path=True,
            guard=guard,
        )
        print(json.dumps(payload, indent=2, sort_keys=True), flush=True)
        print(f"=== FCLR-010-FAST BLOCKED (no canonical output mutation) {dt_to_iso_z(datetime.now(timezone.utc))} ===", flush=True)
        return 1

    # READY_FROZEN + explicit loader would run here. Fast path has no loader, so this
    # is unreachable without an explicit outcome_loader argument; fail-closed.
    payload = refusal_payload(
        reason="FCLR-010-FAST refused: READY_FROZEN but no explicit outcome_loader supplied.",
        reason_code="NO_EXPLICIT_LOADER",
        script="fclr010_execute_fast",
        fast_path=True,
        guard=guard,
    )
    print(json.dumps(payload, indent=2, sort_keys=True), flush=True)
    print(f"=== FCLR-010-FAST BLOCKED (no canonical output mutation) {dt_to_iso_z(datetime.now(timezone.utc))} ===", flush=True)
    return 1


if __name__ == '__main__':
    sys.exit(main())