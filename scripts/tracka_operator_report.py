#!/usr/bin/env python3
"""Operator CLI entrypoint for the Track A compose/report (FCLR-NEXT-105).

Bounded, read-only, no-network, fail-closed. Emits stable machine-readable JSON on
stdout and exits 0 on PASS, 1 on BLOCKED/fail-closed. No real research_state writes.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.tracka_resume_check import compose_operator_report


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="tracka_operator_report",
        description="Track A operator compose/report: drift preflight + gate decision + probe invariant state.",
    )
    p.add_argument("--repo-root", default=str(ROOT))
    p.add_argument("--research-state-dir", default=None)
    p.add_argument("--harness-repo-root", default=None)
    p.add_argument("--data-path", default="/nonexistent_tracka_resume")
    p.add_argument("--pre-reg", default=None)
    p.add_argument("--admissible-manifest", default=None,
                   help="Optional admissible Track A candidate manifest path (GO/NO-GO seam passthrough).")
    p.add_argument("--json", action="store_true", help="Emit compact JSON only (default pretty JSON).")
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    rs = Path(args.research_state_dir) if args.research_state_dir else None
    hrr = Path(args.harness_repo_root) if args.harness_repo_root else None
    try:
        report = compose_operator_report(
            repo_root=Path(args.repo_root),
            research_state_dir=rs,
            data_path=args.data_path,
            prereg=args.pre_reg,
            harness_repo_root=hrr,
            admissible_candidate_path=getattr(args, "admissible_manifest", None),
        )
    except Exception as e:  # G2/131: unexpected operator errors must refuse as JSON, never traceback-as-contract
        report = {
            "script": "tracka_operator_report",
            "status": "BLOCKED",
            "reason": f"operator report failed (fail-closed, no outcomes): {e!r}",
            "reason_code": "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS",
            "fail_closed_order": "drift_preflight->gate_decision->probe_invariant_state",
            "outcomes_inspected": False,
            "network": False,
            "writes_real_research_state": False,
            "canonical_outputs_mutated": False,
            "reads_parquet": False,
            "reads_outcomes": False,
        }
    # G2/129: normalize stable seam-wired fields for CLI parity.
    seam = report.get("admissible_seam_wired")
    if isinstance(seam, dict):
        seam.setdefault("failures", [])
        seam.setdefault("month", None)
    payload = json.dumps(report, indent=None if args.json else 2, sort_keys=True)
    print(payload)
    gate = report.get("gate_decision") or {}
    seam = report.get("admissible_seam_wired") or {}
    blocked = gate.get("status") == "BLOCKED"
    seam_nogo = seam.get("status") == "NO-GO"
    return 0 if (report.get("pass") is True and not blocked and not seam_nogo) else 1


if __name__ == "__main__":
    sys.exit(main())