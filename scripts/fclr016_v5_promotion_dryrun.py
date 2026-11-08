#!/usr/bin/env python3
"""Read-only Gate 4 v5 promotion dry-run harness (NO outcomes, NO network, NO data).

Deterministic dry-run for the 4-artifact admissibility package. It evaluates the real
blocked package and a mandatory refusal/acceptance matrix without loading kline/funding/
outcome data, without network access, and without mutating canonical/input artifacts.

Synthetic GO is permitted ONLY for tmp fixture labeled synthetic_test_fixture=true and
no_real_terms_evidence=true; such fixtures never write/claim real evidence and never
mutate canonicals. Confirmatory outcomes remain prohibited until real human-verified
resolved terms evidence exists in-repo and the real package passes all guards.
"""
from __future__ import annotations

import argparse
import copy
import json
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_funding_ablations as rfa  # noqa: E402

VALIDATOR_NAME = "fclr016_v5_promotion_dryrun"
RESOLVED_TERMS = rfa.RESOLVED_TERMS
PASS_COMPLETENESS = rfa.PASS_COMPLETENESS
REQUIRED_HUMAN_TERMS_FIELDS = [
    "terms_url_reviewed",
    "access_date_utc",
    "terms_version_or_snapshot_id|justified_not_provided_by_source",
    "relevant_clause_summary",
    "reviewer_role(human/legal)",
    "conclusion",
    "conditions_or_restrictions",
    "evidence_artifacts/hashes",
    "fabricated=false",
    "status=RESOLVED_VERIFIED",
    "scope_matches_frozen",
]
FORBIDDEN_VALUES = [
    "fabricated=true",
    "agent-only reviewer",
    "TEMPLATE_NOT_EVIDENCE treated as resolved",
    "EXPLICIT_BLOCKER_UNRESOLVED treated as resolved",
    "draft promoted/frozen/GO claims without guards",
    "provenance GO while terms unresolved",
    "admissibility_refs_sha256/path mismatch or reconciliation failure",
    "completeness verdict/pass inconsistency (verdict!=PASS, admissibility_complete!=true, leak/gap blockers)",
    "confirmatory --expect-go on blocked package treated as pass",
    "real terms evidence fabricated or claimed from synthetic fixture",
]
NO_CONFIRMATORY_OUTCOMES_STATEMENT = (
    "Confirmatory outcomes still prohibited until real human-verified resolved terms "
    "evidence exists in-repo and the real package passes all guards."
)


def _sha(p: Path) -> str:
    return rfa.admissibility_sha256(p)


def _load(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _save(p: Path, obj: Any) -> None:
    p.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _copy_pkg_to_tmp(td: Path, pm: Path, ca: Path, te: Path, pr: Path) -> tuple[Path, Path, Path, Path]:
    td.mkdir(parents=True, exist_ok=True)
    out = (td / "pm.json", td / "ca.json", td / "te.json", td / "pr.json")
    for src, dst in zip((pm, ca, te, pr), out):
        shutil.copy2(src, dst)
    return out


def _eval_pkg(pm: Path, ca: Path, te: Path, pr: Path, expect_go: bool = True) -> dict:
    pkg = rfa.check_admissibility_package(str(pm), str(ca), str(te), str(pr), expect_go=expect_go)
    gates = pkg.get("gates", {}) if isinstance(pkg, dict) else {}
    errors = list(pkg.get("errors", []) or []) if isinstance(pkg, dict) else []
    blockers = list(pkg.get("blockers", []) or []) if isinstance(pkg, dict) else []
    all_go = bool(pkg.get("all_go", False)) and bool(pkg.get("ok", False)) and not errors
    return {
        "ok": bool(pkg.get("ok", False)) if isinstance(pkg, dict) else False,
        "all_go": all_go,
        "confirmatory_outcomes_permitted": bool(pkg.get("confirmatory_outcomes_permitted", False)) and all_go,
        "expect_go": bool(expect_go),
        "expect_go_refused": bool(expect_go) and not all_go,
        "gates": gates,
        "blockers": blockers,
        "errors": errors,
        "hashes": pkg.get("hashes") if isinstance(pkg, dict) else None,
        "raw_expect_go_refused_flag": bool(pkg.get("expect_go_refused", False)) if isinstance(pkg, dict) else False,
    }


def _scenario(sid: str, title: str, result: dict, expected_refused: bool, reason: str,
              synthetic_fixture: bool = False) -> dict:
    refused = not bool(result.get("all_go"))
    status = "PASS_REFUSED" if (expected_refused and refused) else (
        "PASS_GO_SYNTHETIC_FIXTURE_ONLY" if (not expected_refused and not refused and synthetic_fixture)
        else "FAIL"
    )
    return {
        "scenario_id": sid,
        "title": title,
        "status": status,
        "expected_refused": expected_refused,
        "actual_refused": refused,
        "synthetic_test_fixture": bool(synthetic_fixture),
        "no_real_terms_evidence": bool(synthetic_fixture),
        "refusal_reasons": result.get("errors") or result.get("blockers") or [],
        "blockers": result.get("blockers", []),
        "gates": result.get("gates", {}),
        "reason": reason,
        "result_summary": {
            "ok": result.get("ok"),
            "all_go": result.get("all_go"),
            "confirmatory_outcomes_permitted": result.get("confirmatory_outcomes_permitted"),
            "expect_go_refused": result.get("expect_go_refused"),
        },
    }


def _resolved_synthetic_terms(scope: dict) -> dict:
    return {
        "artifact": "fclr016_v5_terms_evidence",
        "schema_version": 5,
        "generated_utc": "2026-11-08T00:00:00Z",
        "git_sha_recorded": "synthetic",
        "confirmatory_claim_go": "GO",
        "confirmatory_provenance_go": True,
        "admissibility_complete": True,
        "no_confirmatory_outcomes": True,
        "fabricated": False,
        "status": RESOLVED_TERMS,
        "synthetic_test_fixture": True,
        "no_real_terms_evidence": True,
        "frozen_scope": scope,
        "terms_url_reviewed": "https://example.invalid/synthetic-terms",
        "access_date_utc": "2026-11-08T00:00:00Z",
        "terms_version_or_snapshot_id": "synthetic-snapshot-1",
        "relevant_clause_summary": "Synthetic fixture only; not legal evidence.",
        "reviewer_role": "human maintainer (synthetic test fixture)",
        "conclusion": "PERMITTED_WITH_CONDITIONS",
        "conditions_or_restrictions": ["synthetic fixture only"],
        "evidence_artifacts": [{"path": "synthetic://fixture", "sha256": "0" * 64}],
    }


def _go_synthetic_package(td: Path, scope: dict) -> tuple[Path, Path, Path, Path]:
    pm = {
        "artifact": "fclr016_v5_provenance_license_manifest",
        "schema_version": 5,
        "generated_utc": "2026-11-08T00:00:00Z",
        "confirmatory_provenance_go": True,
        "admissibility_complete": True,
        "confirmatory_claim_go": "GO",
        "no_confirmatory_outcomes": True,
        "fabricated": False,
        "synthetic_test_fixture": True,
        "no_real_terms_evidence": True,
        "cache_identity_vs_binance_vision": "GO_PARTIAL_BOUNDED_IDENTITY_ONLY",
        "frozen_scope": scope,
        "license_terms": {"status": RESOLVED_TERMS, "fabricated": False, "synthetic_test_fixture": True},
    }
    ca = {
        "artifact": "fclr016_v5_completeness_leakage_audit",
        "schema_version": 5,
        "generated_utc": "2026-11-08T00:00:00Z",
        "confirmatory_claim_go": "GO",
        "admissibility_complete": True,
        "no_confirmatory_outcomes": True,
        "fabricated": False,
        "synthetic_test_fixture": True,
        "no_real_terms_evidence": True,
        "verdict": PASS_COMPLETENESS,
        "frozen_scope": scope,
        "completeness": {"ok": True},
    }
    te = _resolved_synthetic_terms(scope)
    pr = {
        "artifact": "fclr016_v5_confirmatory_prereg",
        "schema_version": 5,
        "draft": False,
        "frozen_before_outcomes": True,
        "promotable_to_frozen": True,
        "confirmatory_claim_go": "GO",
        "admissibility_complete": True,
        "license_terms_resolved": True,
        "no_confirmatory_outcomes": True,
        "fabricated": False,
        "synthetic_test_fixture": True,
        "no_real_terms_evidence": True,
        "generated_utc": "2026-11-08T00:00:00Z",
        "git_sha_recorded": "synthetic",
        "frozen_scope": scope,
        "gates": {"confirmatory_outcomes_permitted": False},
    }
    paths = (td / "pm_go.json", td / "ca_go.json", td / "te_go.json", td / "pr_go.json")
    for p, d in zip(paths, (pm, ca, te, pr)):
        _save(p, d)
    return paths


def run_dryrun(real_pm: Path, real_ca: Path, real_te: Path, real_pr: Path,
               candidate_terms: Path | None = None, candidate_prereg: Path | None = None) -> dict:
    """Execute deterministic promotion dry-run. Read-only on inputs; tmp-only writes."""
    real_pm, real_ca, real_te, real_pr = map(Path, (real_pm, real_ca, real_te, real_pr))
    input_hashes = {"pm": _sha(real_pm), "ca": _sha(real_ca), "te": _sha(real_te), "pr": _sha(real_pr)}
    pm_obj, ca_obj, te_obj, pr_obj = _load(real_pm), _load(real_ca), _load(real_te), _load(real_pr)
    scope = (pm_obj.get("frozen_scope") or ca_obj.get("frozen_scope") or
             {"window": "2025-08-01..2025-10-31"})

    scenarios: list[dict] = []
    with tempfile.TemporaryDirectory(prefix="fclr016_v5_promotion_dryrun_") as td_s:
        td = Path(td_s)

        # (a) Real blocked package
        (td / "a").mkdir()
        rpm, rca, rte, rpr = _copy_pkg_to_tmp(td / "a", real_pm, real_ca, real_te, real_pr)
        res_a = _eval_pkg(rpm, rca, rte, rpr, expect_go=True)
        scenarios.append(_scenario(
            "a_real_blocked_package", "Real blocked package refuses GO",
            res_a, True,
            "The current real package is blocked and must not permit confirmatory outcomes."))

        # (b) Candidate terms missing required human fields -> refused
        (td / "b").mkdir()
        bpm, bca, bte, bpr = _copy_pkg_to_tmp(td / "b", real_pm, real_ca, real_te, real_pr)
        bte_obj = _load(bte)
        bte_obj.update({"status": RESOLVED_TERMS, "fabricated": False, "terms_url_reviewed": "",
                        "access_date_utc": "2026-11-08T00:00:00Z", "reviewer_role": "human legal reviewer",
                        "conclusion": "PERMITTED", "frozen_scope": scope})
        _save(bte, bte_obj)
        scenarios.append(_scenario(
            "b_missing_human_fields", "Resolved terms missing required human fields refused",
            _eval_pkg(bpm, bca, bte, bpr, expect_go=True), True,
            "All required human-verified fields must be present; missing field refuses."))

        # (c) fabricated=true or agent-only reviewer -> refused
        (td / "c1").mkdir()
        cpm, cca, cte, cpr = _copy_pkg_to_tmp(td / "c1", real_pm, real_ca, real_te, real_pr)
        cte_obj = _resolved_synthetic_terms(scope)
        cte_obj["fabricated"] = True
        cte_obj["synthetic_test_fixture"] = False
        _save(cte, cte_obj)
        scenarios.append(_scenario(
            "c_fabricated_true", "fabricated=true refused",
            _eval_pkg(cpm, cca, cte, cpr, expect_go=True), True,
            "Fabricated terms evidence is forbidden."))
        (td / "c2").mkdir()
        cpm2, cca2, cte2, cpr2 = _copy_pkg_to_tmp(td / "c2", real_pm, real_ca, real_te, real_pr)
        cte2_obj = _resolved_synthetic_terms(scope)
        cte2_obj["reviewer_role"] = "automated agent only"
        _save(cte2, cte2_obj)
        scenarios.append(_scenario(
            "c_agent_only_reviewer", "agent-only reviewer refused",
            _eval_pkg(cpm2, cca2, cte2, cpr2, expect_go=True), True,
            "Human/legal reviewer required; agent-only reviewer refuses."))

        # (d) template/blocker treated as resolved -> refused
        for sid, status, label in [
            ("d_template_as_resolved", "TEMPLATE_NOT_EVIDENCE", "TEMPLATE_NOT_EVIDENCE"),
            ("d_blocker_as_resolved", "EXPLICIT_BLOCKER_UNRESOLVED", "EXPLICIT_BLOCKER_UNRESOLVED"),
        ]:
            sub = td / sid
            sub.mkdir()
            dpm, dca, dte, dpr = _copy_pkg_to_tmp(sub, real_pm, real_ca, real_te, real_pr)
            dobj = _load(dte)
            # Keep blocker/template status but try to force GO claims on manifest/prereg side.
            dobj["status"] = status
            dobj["fabricated"] = False
            _save(dte, dobj)
            dpm_obj = _load(dpm)
            dpm_obj["confirmatory_provenance_go"] = True
            dpm_obj["admissibility_complete"] = True
            dpm_obj["license_terms"] = {"status": RESOLVED_TERMS, "fabricated": False}
            _save(dpm, dpm_obj)
            scenarios.append(_scenario(
                sid, f"{label} treated as resolved refused",
                _eval_pkg(dpm, dca, dte, dpr, expect_go=True), True,
                f"{label} is not resolved evidence; GO claims must be refused."))

        # (e) Draft promoted/frozen/GO claims without guards -> refused
        (td / "e").mkdir()
        epm, eca, ete, epr = _copy_pkg_to_tmp(td / "e", real_pm, real_ca, real_te, real_pr)
        epr_obj = _load(epr)
        epr_obj.update({"draft": True, "frozen_before_outcomes": True, "promotable_to_frozen": True,
                        "confirmatory_claim_go": "GO", "admissibility_complete": True})
        _save(epr, epr_obj)
        scenarios.append(_scenario(
            "e_draft_promoted_claims", "Draft promoted/frozen/GO claims without guards refused",
            _eval_pkg(epm, eca, ete, epr, expect_go=True), True,
            "Draft prereg cannot claim frozen/promotable/GO/admissible."))

        # (f) Provenance GO while terms unresolved -> refused
        (td / "f").mkdir()
        fpm, fca, fte, fpr = _copy_pkg_to_tmp(td / "f", real_pm, real_ca, real_te, real_pr)
        fpm_obj = _load(fpm)
        fpm_obj["confirmatory_provenance_go"] = True
        fpm_obj["admissibility_complete"] = True
        _save(fpm, fpm_obj)
        scenarios.append(_scenario(
            "f_provenance_go_terms_unresolved", "Provenance GO while terms unresolved refused",
            _eval_pkg(fpm, fca, fte, fpr, expect_go=True), True,
            "Provenance/manifest cannot be GO while terms are unresolved."))

        # (g) admissibility_refs_sha256/path mismatch or reconciliation failure -> refused
        (td / "g").mkdir()
        gpm, gca, gte, gpr = _copy_pkg_to_tmp(td / "g", real_pm, real_ca, real_te, real_pr)
        gpr_obj = _load(gpr)
        gpr_obj.setdefault("admissibility_refs_sha256", {})["terms_evidence"] = "0" * 64
        _save(gpr, gpr_obj)
        scenarios.append(_scenario(
            "g_refs_sha256_mismatch", "admissibility refs sha256 mismatch refused",
            _eval_pkg(gpm, gca, gte, gpr, expect_go=True), True,
            "Reconciliation/hash mismatch must refuse."))

        # (h) Completeness verdict/pass inconsistency -> refused
        (td / "h1").mkdir()
        hpm, hca, hte, hpr = _copy_pkg_to_tmp(td / "h1", real_pm, real_ca, real_te, real_pr)
        hca_obj = _load(hca)
        hca_obj["verdict"] = "FAIL_INCOMPLETE"
        hca_obj["admissibility_complete"] = False
        _save(hca, hca_obj)
        scenarios.append(_scenario(
            "h_completeness_verdict_not_pass", "Completeness verdict!=PASS refused",
            _eval_pkg(hpm, hca, hte, hpr, expect_go=True), True,
            "Completeness/leakage verdict must pass deterministically."))
        (td / "h2").mkdir()
        hpm2, hca2, hte2, hpr2 = _copy_pkg_to_tmp(td / "h2", real_pm, real_ca, real_te, real_pr)
        hca2_obj = _load(hca2)
        hca2_obj["verdict"] = PASS_COMPLETENESS
        hca2_obj.setdefault("completeness", {})["ok"] = False
        _save(hca2, hca2_obj)
        scenarios.append(_scenario(
            "h_completeness_pass_inconsistent", "Completeness PASS but completeness.ok false refused",
            _eval_pkg(hpm2, hca2, hte2, hpr2, expect_go=True), True,
            "Verdict/pass inconsistency must refuse."))

        # (i) Confirmatory --expect-go contract on blocked package -> refused with stable contract
        scenarios.append(_scenario(
            "i_expect_go_blocked_contract", "Confirmatory --expect-go contract on blocked package refused",
            res_a, True,
            "Blocked package with expect-go must return stable non-GO refusal contract."))

        # (j) Synthetic fully-satisfied GO fixture -> GO only on labeled synthetic tmp fixture
        (td / "j").mkdir()
        jpm, jca, jte, jpr = _go_synthetic_package(td / "j", scope)
        res_j = _eval_pkg(jpm, jca, jte, jpr, expect_go=True)
        scenarios.append(_scenario(
            "j_synthetic_go_fixture_only", "Synthetic fully-satisfied GO fixture accepted only as labeled fixture",
            res_j, False,
            "GO may be reported only for synthetic_test_fixture=true/no_real_terms_evidence=true tmp fixture; never real evidence.",
            synthetic_fixture=True))

        # Optional candidate terms/prereg evaluated read-only in tmp copies
        candidate_eval = None
        if candidate_terms or candidate_prereg:
            (td / "candidate").mkdir()
            cpm_p, cca_p, cte_p, cpr_p = _copy_pkg_to_tmp(td / "candidate", real_pm, real_ca, real_te, real_pr)
            if candidate_terms:
                shutil.copy2(candidate_terms, cte_p)
            if candidate_prereg:
                shutil.copy2(candidate_prereg, cpr_p)
            candidate_eval = _eval_pkg(cpm_p, cca_p, cte_p, cpr_p, expect_go=True)
            candidate_eval["inputs"] = {
                "candidate_terms_evidence": str(Path(candidate_terms).resolve()) if candidate_terms else None,
                "candidate_prereg": str(Path(candidate_prereg).resolve()) if candidate_prereg else None,
            }

    # Verify inputs unchanged after dry-run
    post_hashes = {"pm": _sha(real_pm), "ca": _sha(real_ca), "te": _sha(real_te), "pr": _sha(real_pr)}
    if post_hashes != input_hashes:
        raise RuntimeError("INPUT_ARTIFACTS_MUTATED")

    all_pass = all(s["status"].startswith("PASS") for s in scenarios)
    report = {
        "validator": VALIDATOR_NAME,
        "ok": all_pass,
        "all_go": False,  # dry-run never grants real GO
        "confirmatory_outcomes_permitted": False,
        "no_confirmatory_outcomes_statement": NO_CONFIRMATORY_OUTCOMES_STATEMENT,
        "no_confirmatory_outcomes": True,
        "no_network": True,
        "no_data_loading": True,
        "canonical_mutation": False,
        "input_artifacts_unchanged": True,
        "required_human_terms_fields": REQUIRED_HUMAN_TERMS_FIELDS,
        "forbidden_values_or_shortcuts": FORBIDDEN_VALUES,
        "real_package": {
            "paths": {
                "provenance_license_manifest": str(real_pm.resolve()),
                "completeness_leakage_audit": str(real_ca.resolve()),
                "terms_evidence": str(real_te.resolve()),
                "confirmatory_prereg": str(real_pr.resolve()),
            },
            "sha256": input_hashes,
            "go_refused": True,
            "confirmatory_outcomes_permitted": False,
        },
        "candidate_evaluation": candidate_eval,
        "scenarios": scenarios,
        "summary": {
            "total": len(scenarios),
            "passed": sum(1 for s in scenarios if s["status"].startswith("PASS")),
            "failed": sum(1 for s in scenarios if s["status"] == "FAIL"),
            "synthetic_go_fixture_only": sum(1 for s in scenarios if s["synthetic_test_fixture"] and not s["actual_refused"]),
        },
    }
    return report


def render_markdown(report: dict) -> str:
    lines = ["# FCLR-016 v5 Promotion Dry-Run (read-only)", ""]
    lines.append(f"- ok: {report['ok']}")
    lines.append(f"- all_go (real): {report['all_go']}")
    lines.append(f"- confirmatory_outcomes_permitted: {report['confirmatory_outcomes_permitted']}")
    lines.append(f"- canonical_mutation: {report['canonical_mutation']}")
    lines.append(f"- no_network/no_data_loading: {report['no_network']}/{report['no_data_loading']}")
    lines.append("")
    lines.append("## Statement")
    lines.append(report["no_confirmatory_outcomes_statement"])
    lines.append("")
    lines.append("## Required human terms fields")
    for f in report["required_human_terms_fields"]:
        lines.append(f"- {f}")
    lines.append("")
    lines.append("## Forbidden values / shortcuts")
    for f in report["forbidden_values_or_shortcuts"]:
        lines.append(f"- {f}")
    lines.append("")
    lines.append("## Scenarios")
    for s in report["scenarios"]:
        lines.append(f"- [{s['status']}] {s['scenario_id']}: {s['title']}")
        lines.append(f"  - expected_refused={s['expected_refused']} actual_refused={s['actual_refused']} synthetic={s['synthetic_test_fixture']}")
        lines.append(f"  - reason: {s['reason']}")
        if s["refusal_reasons"]:
            lines.append(f"  - refusal_reasons: {json.dumps(s['refusal_reasons'][:5], sort_keys=True)}")
    if report.get("candidate_evaluation"):
        ce = report["candidate_evaluation"]
        lines.append("")
        lines.append("## Candidate evaluation (read-only tmp copy)")
        lines.append(f"- all_go: {ce.get('all_go')} confirmatory_outcomes_permitted: {ce.get('confirmatory_outcomes_permitted')}")
        lines.append(f"- blockers: {json.dumps(ce.get('blockers'), sort_keys=True)}")
    return "\n".join(lines) + "\n"


def _cli_refusal(error: str) -> dict:
    return {
        "ok": False,
        "all_go": False,
        "confirmatory_outcomes_permitted": False,
        "expect_go_refused": True,
        "error": error,
        "errors": [error],
        "blockers": ["refusal"],
        "validator": VALIDATOR_NAME,
        "no_confirmatory_outcomes": True,
        "no_confirmatory_outcomes_statement": NO_CONFIRMATORY_OUTCOMES_STATEMENT,
        "no_network": True,
        "no_data_loading": True,
        "canonical_mutation": False,
    }


def main(argv: list[str] | None = None) -> int:
    try:
        ap = argparse.ArgumentParser(description="Read-only FCLR-016 v5 promotion dry-run harness")
        ap.add_argument("provenance_manifest")
        ap.add_argument("completeness_audit")
        ap.add_argument("terms_evidence")
        ap.add_argument("prereg_draft")
        ap.add_argument("--candidate-terms-evidence", default=None)
        ap.add_argument("--candidate-prereg", default=None)
        ap.add_argument("--json-only", action="store_true")
        try:
            args = ap.parse_args(argv)
        except SystemExit as e:
            code = e.code if isinstance(e.code, int) else 2
            return code if code != 0 else 0
        paths = [Path(args.provenance_manifest), Path(args.completeness_audit),
                 Path(args.terms_evidence), Path(args.prereg_draft)]
        for p in paths:
            if not p.exists():
                print(json.dumps(_cli_refusal(f"missing: {p}"), sort_keys=True))
                return 2
            if not p.is_file():
                print(json.dumps(_cli_refusal(f"not a file: {p}"), sort_keys=True))
                return 2
        cte = Path(args.candidate_terms_evidence) if args.candidate_terms_evidence else None
        cpr = Path(args.candidate_prereg) if args.candidate_prereg else None
        for p in (cte, cpr):
            if p and not p.exists():
                print(json.dumps(_cli_refusal(f"missing candidate: {p}"), sort_keys=True))
                return 2
            if p and not p.is_file():
                print(json.dumps(_cli_refusal(f"candidate not a file: {p}"), sort_keys=True))
                return 2
        try:
            report = run_dryrun(*paths, candidate_terms=cte, candidate_prereg=cpr)
        except Exception as e:
            print(json.dumps(_cli_refusal(f"cannot build promotion dry-run: {e}"), sort_keys=True))
            return 2
        if not isinstance(report, dict):
            print(json.dumps(_cli_refusal("invalid report payload"), sort_keys=True))
            return 2
        report.setdefault("all_go", False)
        report.setdefault("confirmatory_outcomes_permitted", False)
        report.setdefault("no_confirmatory_outcomes", True)
        report.setdefault("no_network", True)
        report.setdefault("no_data_loading", True)
        print(json.dumps(report, indent=2, sort_keys=True))
        if not args.json_only:
            print("---MARKDOWN---")
            print(render_markdown(report), end="")
        return 0 if report.get("ok") else 2
    except Exception as e:
        print(json.dumps(_cli_refusal(f"internal refusal: {e}"), sort_keys=True))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
