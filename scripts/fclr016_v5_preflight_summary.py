#!/usr/bin/env python3
"""Read-only Gate 4 v5 preflight summary (no outcomes, no network, no data loading).

Deterministic parity check across validator/package/report logic surfaces:
- runs check_admissibility_package (fail-closed) on the 4 package artifacts;
- emits machine-readable JSON + markdown human action checklist + refusal matrix;
- never claims GO, never permits confirmatory outcomes, never mutates canonicals.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_funding_ablations as rfa  # noqa: E402

REQUIRED_HUMAN_TERMS_FIELDS = [
    {"field": "terms_url_reviewed", "guidance": "Exact URL reviewed by a human/legal reviewer."},
    {"field": "access_date_utc", "guidance": "UTC date/time of the human review."},
    {
        "field": "terms_version_or_snapshot_id",
        "guidance": "Version/snapshot identifier, or justified not_provided_by_source with evidence.",
    },
    {"field": "relevant_clause_summary", "guidance": "Human-written summary of clauses relevant to frozen scope/use."},
    {"field": "reviewer_role", "guidance": "Human/legal/maintainer role (not agent-only)."},
    {"field": "conclusion", "guidance": "Human conclusion (e.g. PERMITTED / PERMITTED_WITH_CONDITIONS / NOT_PERMITTED)."},
    {"field": "conditions_or_restrictions", "guidance": "Any conditions/restrictions; explicit empty list if none."},
    {"field": "evidence_artifacts", "guidance": "Paths/hashes/identifiers for review evidence; no fabricated snapshots."},
    {"field": "fabricated", "guidance": "Must be false with verifiable facts; never true on resolved evidence."},
    {"field": "status", "guidance": "Must become RESOLVED_VERIFIED only after complete human review."},
]

FORBIDDEN_VALUES = [
    {"forbidden": "fabricated!=false on resolved evidence", "reason": "terms/license/reviews must not be fabricated"},
    {"forbidden": "reviewer_role agent-only / automated agent only", "reason": "human/legal review required"},
    {"forbidden": "status=TEMPLATE_NOT_EVIDENCE or EXPLICIT_BLOCKER_UNRESOLVED treated as resolved", "reason": "template/blocker is not evidence"},
    {"forbidden": "renaming template/blocker to RESOLVED without complete verified fields", "reason": "shortcut bypass"},
    {"forbidden": "GO/admissible claims while terms unresolved or prereg draft", "reason": "fail-closed admissibility"},
    {"forbidden": "confirmatory outcome/data loading on refusal or missing refs", "reason": "no confirmatory outcomes until frozen+all GO"},
]

PROMOTION_SEQUENCE = [
    "Human/legal reviewer completes terms fields with verifiable facts only; save research_state/fclr016_local_audit/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json (separate file).",
    "Set fabricated=false and status=RESOLVED_VERIFIED only when facts are verified and scope matches frozen Gate 4 v5 scope.",
    "Reconcile admissibility_refs_sha256/paths across provenance manifest, completeness/leakage audit, resolved terms evidence, and prereg draft.",
    "Promote prereg to frozen/non-draft only after all guards are green; do not set GO/admissible while any gate is blocked.",
    "Run validator with --expect-go, then run_funding_ablations --check-admissibility-package --expect-go; both must return all_go=true/confirmatory_outcomes_permitted=true and exit 0.",
    "Only after frozen+all GO and hashes recorded may confirmatory outcome computation be attempted; confirmatory guard must refuse until GO and must not load data on refusal.",
]


def _sha(p: Path) -> str:
    return rfa.admissibility_sha256(p)


def _load(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _refusal_matrix(pkg: dict, pm: dict, ca: dict, te: dict, pr: dict) -> list[dict]:
    gates = pkg.get("gates", {}) if isinstance(pkg, dict) else {}
    errors = pkg.get("errors", []) if isinstance(pkg, dict) else []
    def row(attempt: str, refused: bool, why: str, evidence: Any) -> dict:
        return {"attempt": attempt, "status": "REFUSED" if refused else "NOT_APPLICABLE", "why": why, "gate_evidence": evidence}
    rows = [
        row(
            "promote draft prereg to frozen/GO while package blocked",
            bool(pr.get("draft") is True) or not gates.get("prereg_frozen_non_draft"),
            "Draft/non-frozen prereg cannot claim GO/admissible; all guards must be green before promotion.",
            {"prereg.draft": pr.get("draft"), "gate.prereg_frozen_non_draft": gates.get("prereg_frozen_non_draft"), "gate.prereg_claim_go": gates.get("prereg_claim_go")},
        ),
        row(
            "mark terms RESOLVED without required human fields",
            not gates.get("terms_resolved_verified"),
            "RESOLVED_VERIFIED requires complete human-verified fields, human/legal reviewer_role, fabricated=false.",
            {"terms.status": te.get("status"), "gate.terms_resolved_verified": gates.get("terms_resolved_verified")},
        ),
        row(
            "claim GO/admissible while terms unresolved",
            te.get("status") != rfa.RESOLVED_TERMS or not gates.get("terms_resolved_verified"),
            "Unresolved/template/blocked terms evidence is an explicit blocker; provenance/package cannot be GO.",
            {"terms.status": te.get("status"), "provenance.confirmatory_provenance_go": pm.get("confirmatory_provenance_go"), "gate.provenance_manifest_go": gates.get("provenance_manifest_go")},
        ),
        row(
            "confirmatory --expect-go or confirmatory run with missing/blocked refs",
            not pkg.get("all_go", False) if isinstance(pkg, dict) else True,
            "--expect-go/package checks must refuse when all_go is false; confirmatory path must not load data on refusal.",
            {"all_go": pkg.get("all_go") if isinstance(pkg, dict) else None, "blockers": pkg.get("blockers") if isinstance(pkg, dict) else None, "errors": errors},
        ),
        row(
            "load confirmatory 2025+ outcome data on refusal",
            True,
            "No kline/funding/outcome loading is permitted on refusal; confirmatory outcomes prohibited until frozen+all GO.",
            {"confirmatory_outcomes_permitted": pkg.get("confirmatory_outcomes_permitted") if isinstance(pkg, dict) else False},
        ),
        row(
            "use fabricated/agent-only/template evidence as resolved evidence",
            te.get("fabricated") is True or te.get("status") == "TEMPLATE_NOT_EVIDENCE" or not gates.get("terms_resolved_verified"),
            "fabricated!=false, agent-only reviewer, and templates are forbidden as resolved evidence.",
            {"terms.fabricated": te.get("fabricated"), "terms.status": te.get("status"), "reviewer_role": te.get("reviewer_role")},
        ),
    ]
    return rows


def build_preflight_summary(pm_p: Path, ca_p: Path, te_p: Path, pr_p: Path) -> dict:
    """Build read-only preflight summary. Never loads outcomes/data/network."""
    pm_p, ca_p, te_p, pr_p = map(Path, (pm_p, ca_p, te_p, pr_p))
    pkg = rfa.check_admissibility_package(str(pm_p), str(ca_p), str(te_p), str(pr_p), expect_go=True)
    pm, ca, te, pr = _load(pm_p), _load(ca_p), _load(te_p), _load(pr_p)
    gates = pkg.get("gates", {}) if isinstance(pkg, dict) else {}
    blockers = [k for k, v in gates.items() if not v] if gates else list(pkg.get("blockers", []) or [])
    errors = list(pkg.get("errors", []) or []) if isinstance(pkg, dict) else []
    pkg_ok = bool(pkg.get("ok", False)) if isinstance(pkg, dict) else False
    all_go = bool(pkg.get("all_go", False)) and pkg_ok and not errors
    confirmatory_outcomes_permitted = bool(pkg.get("confirmatory_outcomes_permitted", False)) and all_go
    summary = {
        "validator": "fclr016_v5_preflight_summary",
        "ok": pkg_ok,
        "all_go": all_go,
        "confirmatory_outcomes_permitted": confirmatory_outcomes_permitted,
        "expect_go_refused": not all_go,
        "gates": gates,
        "blockers": blockers,
        "errors": errors,
        "artifacts": {
            "provenance_license_manifest": {"path": str(pm_p.resolve()), "sha256": _sha(pm_p), "status_fields": {"confirmatory_provenance_go": pm.get("confirmatory_provenance_go"), "admissibility_complete": pm.get("admissibility_complete")}},
            "completeness_leakage_audit": {"path": str(ca_p.resolve()), "sha256": _sha(ca_p), "status_fields": {"verdict": ca.get("verdict"), "admissibility_complete": ca.get("admissibility_complete")}},
            "terms_evidence": {"path": str(te_p.resolve()), "sha256": _sha(te_p), "status_fields": {"status": te.get("status"), "fabricated": te.get("fabricated")}},
            "confirmatory_prereg": {"path": str(pr_p.resolve()), "sha256": _sha(pr_p), "status_fields": {"draft": pr.get("draft"), "confirmatory_claim_go": pr.get("confirmatory_claim_go"), "admissibility_complete": pr.get("admissibility_complete")}},
        },
        "required_human_terms_fields": REQUIRED_HUMAN_TERMS_FIELDS,
        "forbidden_values": FORBIDDEN_VALUES,
        "promotion_sequence": PROMOTION_SEQUENCE,
        "refusal_matrix": _refusal_matrix(pkg if isinstance(pkg, dict) else {}, pm, ca, te, pr),
        "package_parity": {
            "source": "run_funding_ablations.check_admissibility_package(expect_go=True)",
            "all_go": pkg.get("all_go") if isinstance(pkg, dict) else None,
            "confirmatory_outcomes_permitted": pkg.get("confirmatory_outcomes_permitted") if isinstance(pkg, dict) else None,
            "hashes": pkg.get("hashes") if isinstance(pkg, dict) else None,
        },
        "no_confirmatory_outcomes": True,
        "no_network": True,
        "no_data_loading": True,
    }
    return summary


def render_markdown(summary: dict) -> str:
    lines = ["# FCLR-016 v5 Preflight Summary (read-only)", ""]
    lines.append(f"- ok: {summary['ok']}")
    lines.append(f"- all_go: {summary['all_go']}")
    lines.append(f"- confirmatory_outcomes_permitted: {summary['confirmatory_outcomes_permitted']}")
    lines.append(f"- expect_go_refused: {summary['expect_go_refused']}")
    lines.append(f"- blockers: {', '.join(summary['blockers']) if summary['blockers'] else '(none)'}")
    lines.append("")
    lines.append("## Artifact hashes / paths")
    for name, info in summary["artifacts"].items():
        lines.append(f"- {name}: `{info['path']}` sha256={info['sha256']} status={json.dumps(info['status_fields'], sort_keys=True)}")
    lines.append("")
    lines.append("## Gate states")
    for k, v in summary["gates"].items():
        lines.append(f"- {k}: {v}")
    if summary["errors"]:
        lines.append("")
        lines.append("## Errors")
        for e in summary["errors"]:
            lines.append(f"- {e}")
    lines.append("")
    lines.append("## Human action checklist (required terms fields)")
    for item in summary["required_human_terms_fields"]:
        lines.append(f"- `{item['field']}`: {item['guidance']}")
    lines.append("")
    lines.append("## Forbidden values / shortcuts (must refuse)")
    for item in summary["forbidden_values"]:
        lines.append(f"- FORBIDDEN: {item['forbidden']} — {item['reason']}")
    lines.append("")
    lines.append("## Promotion sequence (only after all guards green)")
    for i, step in enumerate(summary["promotion_sequence"], 1):
        lines.append(f"{i}. {step}")
    lines.append("")
    lines.append("## Refusal matrix")
    for row in summary["refusal_matrix"]:
        lines.append(f"- [{row['status']}] {row['attempt']}")
        lines.append(f"  - why: {row['why']}")
        lines.append(f"  - evidence: {json.dumps(row['gate_evidence'], sort_keys=True)}")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Read-only FCLR-016 v5 preflight summary")
    ap.add_argument("provenance_manifest")
    ap.add_argument("completeness_audit")
    ap.add_argument("terms_evidence")
    ap.add_argument("prereg_draft")
    ap.add_argument("terms_evidence_override", nargs="?")
    args = ap.parse_args(argv)
    pm_p = Path(args.provenance_manifest)
    ca_p = Path(args.completeness_audit)
    te_p = Path(args.terms_evidence_override or args.terms_evidence)
    pr_p = Path(args.prereg_draft)
    for p in (pm_p, ca_p, te_p, pr_p):
        if not p.exists():
            print(json.dumps({"ok": False, "all_go": False, "confirmatory_outcomes_permitted": False, "error": f"missing: {p}", "validator": "fclr016_v5_preflight_summary"}, sort_keys=True))
            return 2
    try:
        summary = build_preflight_summary(pm_p, ca_p, te_p, pr_p)
    except Exception as e:
        print(json.dumps({"ok": False, "all_go": False, "confirmatory_outcomes_permitted": False, "error": f"cannot build preflight summary: {e}", "validator": "fclr016_v5_preflight_summary"}, sort_keys=True))
        return 2
    print(json.dumps(summary, indent=2, sort_keys=True))
    print("---MARKDOWN---")
    print(render_markdown(summary), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
