#!/usr/bin/env python3
"""Read-only Gate 4 v5 admissibility package report (no outcomes, no network, no data)."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Import the existing validator logic; no kline/funding/outcome loading occurs here.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_funding_ablations as rfa  # noqa: E402


def _sha(p: Path) -> str:
    return rfa.admissibility_sha256(p)


def build_report(pm_p, ca_p, te_p, pr_p) -> dict:
    """Build read-only admissibility report. Never loads outcomes/data/network."""
    pm_p, ca_p, te_p, pr_p = Path(pm_p), Path(ca_p), Path(te_p), Path(pr_p)
    res = rfa.check_admissibility_package(str(pm_p), str(ca_p), str(te_p), str(pr_p), expect_go=True)
    pm = json.loads(pm_p.read_text(encoding="utf-8"))
    ca = json.loads(ca_p.read_text(encoding="utf-8"))
    te = json.loads(te_p.read_text(encoding="utf-8"))
    pr = json.loads(pr_p.read_text(encoding="utf-8"))
    gates = res.get("gates", {}) if isinstance(res.get("gates"), dict) else {}
    blockers = [k for k, v in gates.items() if not v]
    errors = res.get("errors", []) or []
    pkg_ok = bool(res.get("ok", False))
    all_go = bool(res.get("all_go", False)) and pkg_ok and not errors
    report = {
        "validator": "fclr016_v5_admissibility_report",
        "ok": pkg_ok,
        "all_go": all_go,
        "confirmatory_outcomes_permitted": bool(res.get("confirmatory_outcomes_permitted", False)) and all_go,
        "gates": gates,
        "blockers": blockers,
        "errors": errors,
        "artifacts": {
            "provenance_license_manifest": {"path": str(pm_p), "sha256": _sha(pm_p)},
            "completeness_leakage_audit": {"path": str(ca_p), "sha256": _sha(ca_p)},
            "terms_evidence": {"path": str(te_p), "sha256": _sha(te_p)},
            "confirmatory_prereg": {"path": str(pr_p), "sha256": _sha(pr_p)},
        },
        "artifact_claims_summary": {
            "provenance.confirmatory_provenance_go": pm.get("confirmatory_provenance_go"),
            "provenance.admissibility_complete": pm.get("admissibility_complete"),
            "completeness.verdict": ca.get("verdict"),
            "completeness.admissibility_complete": ca.get("admissibility_complete"),
            "terms.status": te.get("status"),
            "terms.fabricated": te.get("fabricated"),
            "prereg.draft": pr.get("draft"),
            "prereg.confirmatory_claim_go": pr.get("confirmatory_claim_go"),
            "prereg.admissibility_complete": pr.get("admissibility_complete"),
        },
        "required_human_terms_fields": [
            "terms_url_reviewed",
            "access_date_utc",
            "terms_version_or_snapshot_id (or justified not_provided_by_source)",
            "relevant_clause_summary",
            "reviewer_role (human/legal)",
            "conclusion",
            "conditions_or_restrictions",
            "evidence_artifacts (with hashes)",
            "fabricated=false",
            "status=RESOLVED_VERIFIED",
        ],
        "next_materially_different_route": (
            "Human terms review -> create research_state/fclr016_local_audit/"
            "fclr016_v5_terms_evidence_RESOLVED_<UTC>.json -> reconcile "
            "admissibility_refs_sha256/paths -> promote prereg to frozen only after "
            "all guards green -> run package check + confirmatory guard "
            "(must refuse until frozen+all GO; must not load data on refusal)."
        ),
        "no_confirmatory_outcomes": True,
        "no_network": True,
        "no_data_loading": True,
    }
    return report


def render_markdown(report: dict) -> str:
    lines = ["# FCLR-016 v5 Admissibility Report", ""]
    lines.append(f"- all_go: {report['all_go']}")
    lines.append(f"- confirmatory_outcomes_permitted: {report['confirmatory_outcomes_permitted']}")
    lines.append(f"- blockers: {', '.join(report['blockers']) if report['blockers'] else '(none)'}")
    lines.append("")
    lines.append("## Gate states")
    for k, v in report["gates"].items():
        lines.append(f"- {k}: {v}")
    if report["errors"]:
        lines.append("")
        lines.append("## Errors")
        for e in report["errors"]:
            lines.append(f"- {e}")
    lines.append("")
    lines.append("## Required human terms-evidence fields")
    for f in report["required_human_terms_fields"]:
        lines.append(f"- {f}")
    lines.append("")
    lines.append("## Next materially different route")
    lines.append(report["next_materially_different_route"])
    return "\n".join(lines)


def _refusal(error: str) -> dict:
    return {
        "ok": False,
        "all_go": False,
        "confirmatory_outcomes_permitted": False,
        "expect_go_refused": True,
        "gates": {},
        "blockers": ["refusal"],
        "errors": [error],
        "error": error,
        "validator": "fclr016_v5_admissibility_report",
        "no_confirmatory_outcomes": True,
        "no_network": True,
        "no_data_loading": True,
    }


def main(argv=None) -> int:
    try:
        ap = argparse.ArgumentParser(description="Read-only FCLR-016 v5 admissibility report")
        ap.add_argument("provenance_manifest")
        ap.add_argument("completeness_audit")
        ap.add_argument("terms_evidence")
        ap.add_argument("prereg_draft")
        ap.add_argument("terms_evidence_override", nargs="?")
        try:
            args = ap.parse_args(argv)
        except SystemExit as e:
            # argparse already printed usage; keep stable exit code.
            code = e.code if isinstance(e.code, int) else 2
            return code if code != 0 else 0
        pm_p = Path(args.provenance_manifest)
        ca_p = Path(args.completeness_audit)
        te_p = Path(args.terms_evidence_override or args.terms_evidence)
        pr_p = Path(args.prereg_draft)
        for p in (pm_p, ca_p, te_p, pr_p):
            if not p.exists():
                print(json.dumps(_refusal(f"missing: {p}"), sort_keys=True))
                return 2
            if not p.is_file():
                print(json.dumps(_refusal(f"not a file: {p}"), sort_keys=True))
                return 2
        try:
            report = build_report(pm_p, ca_p, te_p, pr_p)
        except Exception as e:
            print(json.dumps(_refusal(f"cannot build admissibility report: {e}"), sort_keys=True))
            return 2
        if not isinstance(report, dict):
            print(json.dumps(_refusal("invalid report payload"), sort_keys=True))
            return 2
        report.setdefault("ok", False)
        report.setdefault("all_go", False)
        report.setdefault("confirmatory_outcomes_permitted", False)
        report.setdefault("no_confirmatory_outcomes", True)
        report.setdefault("no_network", True)
        report.setdefault("no_data_loading", True)
        print(json.dumps(report, indent=2, sort_keys=True))
        print("---MARKDOWN---")
        print(render_markdown(report))
        return 0 if report.get("ok") else 2
    except Exception as e:
        print(json.dumps(_refusal(f"internal refusal: {e}"), sort_keys=True))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())