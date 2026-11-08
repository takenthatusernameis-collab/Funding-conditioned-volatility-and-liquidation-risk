#!/usr/bin/env python3
"""FCLR-NEXT-142 / FCLR-020: deterministic read-only Gate 4 confirmatory-readiness
action matrix from FCLR-019 evidence bundle index.

Consumes fclr019 latest (and only local refs it cites as needed/readable metadata)
and emits per-window/prerequisite action rows: current state, blocker/missing reason,
action_required, verification_command_or_check (read-only deterministic local checks),
and authorizes_confirmatory_outcomes=false.

Read-only, no network, no model-outcome computation, no freeze/promotion, no sealed
overwrite. Planning/draft evidence only. Never marks satisfied, never infers
satisfaction from absence of a blocker string, never fabricates evidence as present.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DEFAULT_FCLR019 = REPO / "research_state" / "fclr019_local_audit" / "fclr019_gate4_evidence_bundle_index_latest.json"
DEFAULT_OUT = REPO / "research_state" / "fclr020_local_audit"

STATES = ("present_unverified", "present_blocker", "missing")


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(REPO))
    except Exception:
        return str(path)


def read_file_state(path: Path):
    if not path.exists():
        return None, "missing", f"missing:{rel(path)}"
    try:
        txt = path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return None, "read_error", f"read_error:{rel(path)}:{e}"
    if txt.startswith("version https://git-lfs.github.com/spec/v1"):
        return None, "unavailable_pointer", f"lfs_pointer_unavailable:{rel(path)}"
    try:
        return json.loads(txt), "ok", None
    except Exception as e:
        return None, "parse_error", f"parse_error:{rel(path)}:{e}"


def local_evidence_snapshot(path_str):
    """Read-only metadata snapshot for a cited path; never marks evidence satisfied."""
    if not path_str or not isinstance(path_str, str):
        return {"path": path_str, "exists": False, "read_state": "no_path_cited"}
    p = Path(path_str)
    if not p.is_absolute():
        p = REPO / path_str
    if not p.exists():
        return {"path": path_str, "exists": False, "read_state": "missing"}
    try:
        b = p.read_bytes()
    except Exception as e:
        return {"path": path_str, "exists": True, "read_state": "read_error", "error": str(e)}
    if b.startswith(b"version https://git-lfs.github.com/spec/v1"):
        return {"path": path_str, "exists": True, "read_state": "unavailable_pointer"}
    return {"path": path_str, "exists": True, "read_state": "readable", "sha256": sha256_bytes(b), "bytes": len(b)}


def base_row(prerequisite_id, prerequisite_label, node, window_id=None, extra_actions=None, extra_checks=None):
    node = node if isinstance(node, dict) else {}
    state = node.get("state") if node.get("state") in STATES else "missing"
    reason = node.get("blocker_note") or node.get("note") or node.get("verification_note") or f"state={state}"
    evidence_ref = node.get("evidence_ref")
    row = {
        "window_id": window_id,
        "prerequisite_id": prerequisite_id,
        "prerequisite_label": prerequisite_label,
        "current_state": state,
        "read_state": node.get("read_state"),
        "evidence_ref": evidence_ref,
        "evidence_snapshot": local_evidence_snapshot(evidence_ref),
        "blocker_or_missing_reason": reason,
        "action_required": list(extra_actions or []),
        "verification_command_or_check": list(extra_checks or []),
        "authorizes_confirmatory_outcomes": False,
        "satisfied": False,
        "satisfaction_inferred": False,
    }
    return row


def state_actions(state, subject, blocked_actions, missing_actions, unverified_actions):
    if state == "present_blocker":
        return blocked_actions
    if state == "missing":
        return missing_actions
    return unverified_actions


def common_readonly_checks(evidence_ref):
    checks = [
        "python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)",
        "python scripts/check_tracka_scope_registry_drift.py  # read-only drift check",
        "python scripts/tracka_resume_check.py  # read-only resume check (network:false)",
    ]
    if evidence_ref and isinstance(evidence_ref, str) and not evidence_ref.startswith("fclr018."):
        checks.insert(0, f"test -f {evidence_ref} && sha256sum {evidence_ref}  # read-only existence/hash check")
        if evidence_ref.endswith('.json'):
            checks.insert(1, f"python3 -c \"import json; json.load(open('{evidence_ref}')); print('json_ok')\"  # read-only parse check")
    return checks


def rows_for_window(candidate):
    wid = candidate.get("window_id")
    ch = candidate.get("checklist") or {}
    rows = []

    # 1) identity/provenance range
    node = ch.get("identity_provenance_range") or {}
    st = node.get("state") if node.get("state") in STATES else "missing"
    rows.append(base_row(
        "identity_provenance_range", "Identity/provenance range evidence (bounded)", node, wid,
        extra_actions=state_actions(
            st, "provenance",
            blocked_actions=[
                "Provide verifiable bounded provenance/identity-range evidence for the candidate window (human/legal/repository evidence as applicable).",
                "Do not run confirmatory outcomes until provenance is identity-verified for bounded confirmatory ranges and all other guards pass.",
                "If FCLR-015 bounded context is claimed, ensure a readable local FCLR-015 artifact exists and is cited with hash/provenance facts (no fabrication).",
            ],
            missing_actions=[
                "Locate or produce a verifiable local provenance/identity-range evidence artifact for the window; cite exact path/hash.",
                "Do not infer provenance from cache presence, path names, or absence of blockers.",
            ],
            unverified_actions=[
                "Human review required: verify cited provenance artifact is authentic, bounded, and sufficient for the intended confirmatory range.",
                "Confirm 2024-04..09 confirmatory use remains bounded by PROVENANCED_CONFIRMATORY_RANGES + manifest/terms/admissibility guards.",
                "Present-unverified is not satisfied; do not compute confirmatory outcomes on this basis alone.",
            ],
        ),
        extra_checks=common_readonly_checks(node.get("evidence_ref")) + [
            "python scripts/fclr015_gate4_cache_input_manifest.py --help >/dev/null 2>&1 || true  # read-only capability check (no confirmatory outcomes)",
        ],
    ))

    # 2) manifest_terms_evidence summary + children
    mt = ch.get("manifest_terms_evidence") or {}
    mt_node = {"state": mt.get("summary_state") if mt.get("summary_state") in STATES else "missing", "read_state": "from_fclr019_summary", "evidence_ref": None, "note": f"provenance_manifest={((mt.get('provenance_manifest') or {}).get('state'))}, terms_evidence={((mt.get('terms_evidence') or {}).get('state'))}"}
    rows.append(base_row(
        "manifest_terms_evidence", "Manifest/terms evidence package", mt_node, wid,
        extra_actions=[
            "Resolve manifest and terms evidence blockers before any confirmatory use (human/legal review required for terms).",
            "For v5 terms: produce verifiable RESOLVED_VERIFIED evidence only with fabricated=false and frozen scope; reconcile refs/hashes.",
            "Never fabricate terms/license/reviews or mark terms resolved without verifiable facts.",
        ],
        extra_checks=common_readonly_checks(None) + [
            "python scripts/fclr016_v5_admissibility_report.py --bogus --json 2>&1 | head -c 200  # refusal path must be parseable, exit!=0 expected",
            "python scripts/fclr016_v5_promotion_dryrun.py --bogus --json 2>&1 | head -c 200  # refusal path must be parseable, exit!=0 expected",
        ],
    ))
    for child_key, child_label, cls_actions in [
        ("provenance_manifest", "Provenance/license manifest artifact", [
            "Ensure provenance manifest exists, is readable, and states confirmatory_provenance_go/admissibility_complete/license_terms status with verifiable facts.",
            "Reconcile manifest refs/hashes after any legitimate evidence update; do not overwrite sealed artifacts.",
        ]),
        ("terms_evidence", "Terms/license evidence artifact (human/legal)", [
            "Human/legal action required: resolve EXPLICIT_BLOCKER_UNRESOLVED with verifiable evidence (fabricated=false).",
            "Do not create RESOLVED_VERIFIED without frozen scope and reconciled refs/hashes; do not edit .github/workflows.",
        ]),
    ]:
        cn = mt.get(child_key) or {}
        rows.append(base_row(
            f"manifest_terms_evidence.{child_key}", child_label, cn, wid,
            extra_actions=cls_actions + ["No confirmatory outcomes/freeze/promotion while this prerequisite is not concretely satisfied by verifiable evidence."],
            extra_checks=common_readonly_checks(cn.get("evidence_ref")),
        ))

    # 3) admissibility package
    ap = ch.get("admissibility_package_status") or {}
    ap_node = {"state": ap.get("summary_state") if ap.get("summary_state") in STATES else "missing", "read_state": "from_fclr019_summary", "evidence_ref": None, "note": f"completeness={((ap.get('completeness_leakage_audit') or {}).get('state'))}, prereg_draft={((ap.get('confirmatory_prereg_draft') or {}).get('state'))}, v5_window={((ap.get('v5_window_terms_state_from_fclr018') or {}).get('state'))}"}
    rows.append(base_row(
        "admissibility_package_status", "Admissibility package status", ap_node, wid,
        extra_actions=[
            "Resolve completeness/leakage/admissibility blockers with verifiable local artifacts; keep v5 all_go=false handling fail-closed until resolved.",
            "Any confirmatory outcomes require real package all_go=true and fresh frozen prereg before outcomes.",
        ],
        extra_checks=common_readonly_checks(None),
    ))
    for child_key, child_label in [
        ("completeness_leakage_audit", "Completeness/leakage audit artifact"),
        ("confirmatory_prereg_draft_ref", "Confirmatory prereg draft/ref artifact (not fresh frozen prereg)"),
        ("v5_window_terms_state_from_fclr018", "v5 window terms/admissibility state (from FCLR-018)"),
    ]:
        cn = ap.get(child_key) or {}
        extra = ["A DRAFT prereg skeleton/ref is not sufficient for confirmatory outcomes; fresh frozen prereg before outcomes is required."] if child_key == "confirmatory_prereg_draft_ref" else ["Do not compute confirmatory outcomes while v5/window blocker state denies permission."] if child_key.startswith("v5_window") else ["Address listed completeness/leakage blockers with verifiable evidence before confirmatory use."]
        rows.append(base_row(
            f"admissibility_package_status.{child_key}", child_label, cn, wid,
            extra_actions=extra,
            extra_checks=common_readonly_checks(cn.get("evidence_ref")) if isinstance(cn.get("evidence_ref"), str) and not cn.get("evidence_ref","" ).startswith("fclr018.") else common_readonly_checks(None),
        ))

    # 4) fresh frozen prereg
    ff = ch.get("fresh_frozen_prereg_before_outcomes_required") or {}
    ff_st = ff.get("state") if ff.get("state") in STATES else "missing"
    rows.append(base_row(
        "fresh_frozen_prereg_before_outcomes_required", "Fresh frozen prereg before outcomes (required)", ff, wid,
        extra_actions=[
            "Create/freeze a fresh confirmatory preregistration BEFORE any confirmatory outcomes are computed (mandatory).",
            "Record frozen prereg hash/ref and ensure all admissibility/provenance/terms/leakage guards are green before outcomes.",
            "DRAFT prereg skeletons, FCLR-018 matrices, FCLR-019 indices, and FCLR-020 action matrices are NOT sufficient.",
            "Do not run or present v4/exploratory/confounded analyses as confirmatory claims.",
        ],
        extra_checks=common_readonly_checks(ff.get("evidence_ref")) + [
            "test ! -f research_state/NO_SUCH_FRESH_FROZEN_PREREG  # placeholder reminder: a concrete frozen prereg artifact path must be supplied and verified before outcomes",
        ],
    ))

    # 5) leakage/sufficiency gates
    lg = ch.get("leakage_sufficiency_gates") or {}
    rows.append(base_row(
        "leakage_sufficiency_gates", "Leakage controls and data sufficiency gates", lg, wid,
        extra_actions=[
            "Verify chronological leakage controls, purge/embargo as preregistered, and >=3 non-overlapping 30-day blocks / >=5 symbols for claim-worthy Gate 4 runs.",
            "Use only loader-compatible admissible local panel; do not threshold-shop or relax gates post-hoc.",
            "Local coverage/block feasibility is not a substitute for admissibility package GO + fresh frozen prereg.",
        ],
        extra_checks=common_readonly_checks(lg.get("evidence_ref")) + [
            "python scripts/run_funding_ablations.py  # baseline pilot must run clean with honest verdict (no confirmatory claim from this command alone)",
        ],
    ))

    return rows


def build_matrix(fclr019_path: Path):
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    f19, f19_state, f19_note = read_file_state(fclr019_path)
    if f19_state != "ok" or not isinstance(f19, dict):
        report = {
            "artifact": "fclr020_gate4_readiness_action_matrix",
            "version": 1,
            "timestamp_utc": ts,
            "draft_only": True,
            "no_confirmatory_outcomes": True,
            "exploratory_only": True,
            "no_network": True,
            "not_go_for_confirmatory_outcomes": True,
            "confirmatory_ready_now": False,
            "confirmatory_outcomes_go": False,
            "error": f"fclr019_latest_unreadable:{f19_state}:{f19_note}",
            "input_fclr019": {"path": rel(fclr019_path), "read_state": f19_state, "note": f19_note},
            "window_action_matrices": [],
            "global_actions": [],
        }
        report["report_sha256"] = sha256_bytes(json.dumps(report, sort_keys=True).encode())
        return report, ts

    candidates = f19.get("candidate_indices") or f19.get("candidates") or []
    window_matrices = []
    for c in candidates:
        rows = rows_for_window(c)
        # safety: enforce invariants
        for r in rows:
            r["authorizes_confirmatory_outcomes"] = False
            r["satisfied"] = False
            r["satisfaction_inferred"] = False
            if r.get("current_state") not in STATES:
                r["current_state"] = "missing"
        window_matrices.append({
            "window_id": c.get("window_id"),
            "start": c.get("start"), "end": c.get("end"),
            "basis": c.get("basis"),
            "fclr019_index_summary_state": c.get("index_summary_state"),
            "confirmatory_outcomes_go": False,
            "action_rows": rows,
        })

    global_actions = [{
        "scope": "global",
        "action_required": [
            "Keep v5 terms/admissibility fail-closed until verifiable human/legal evidence resolves blockers and package is GO.",
            "Track A/H004 remains blocked; do not re-probe absent Hyperliquid months in a loop.",
            "No .github/workflows edits; no sealed holdout/anchor overwrites; no competing handoff files.",
        ],
        "verification_command_or_check": [
            "python scripts/fclr016_v5_admissibility_report.py --bogus --json 2>&1 | head -c 200",
            "python scripts/tracka_resume_check.py | python3 -c \"import sys,json; d=json.load(sys.stdin); print(d['pass'], d['network'])\"",
        ],
        "authorizes_confirmatory_outcomes": False,
    }]

    report = {
        "artifact": "fclr020_gate4_readiness_action_matrix",
        "version": 1,
        "timestamp_utc": ts,
        "draft_only": True,
        "no_confirmatory_outcomes": True,
        "exploratory_only": True,
        "no_network": True,
        "not_go_for_confirmatory_outcomes": True,
        "confirmatory_ready_now": False,
        "confirmatory_outcomes_go": False,
        "purpose": "deterministic read-only per-window action matrix from FCLR-019; explicit blockers/actions/verifiers only; never authorizes confirmatory outcomes",
        "input_fclr019": {"path": rel(fclr019_path), "read_state": f19_state, "sha256": sha256_bytes(fclr019_path.read_bytes()) if fclr019_path.exists() else None},
        "caveats": {
            "draft_only_not_frozen_not_promoted": True,
            "no_confirmatory_outcomes_computed": True,
            "no_prerequisite_marked_satisfied": True,
            "no_satisfaction_inferred_from_absent_blocker": True,
            "lfs_pointer_treated_as_unavailable": True,
            "states_used": list(STATES),
        },
        "global_actions": global_actions,
        "window_action_matrices": window_matrices,
        "decision": {
            "confirmatory_ready_now": False,
            "confirmatory_outcomes_go": False,
            "reason": "draft_action_matrix_only_from_fclr019_no_confirmatory_authorization",
        },
    }
    report["report_sha256"] = sha256_bytes(json.dumps(report, sort_keys=True).encode())
    return report, ts


def write_md(report: dict, path: Path):
    L = []
    L.append(f"# FCLR-020 Gate 4 readiness/action matrix ({report.get('timestamp_utc')})")
    L.append("")
    L.append("- method: deterministic read-only action mapping from FCLR-019; no network; no model-outcome computation")
    L.append(f"- draft_only: **{report.get('draft_only')}** | no_confirmatory_outcomes: **{report.get('no_confirmatory_outcomes')}** | exploratory_only: **{report.get('exploratory_only')}** | no_network: **{report.get('no_network')}**")
    L.append(f"- not_go_for_confirmatory_outcomes: **{report.get('not_go_for_confirmatory_outcomes')}** | confirmatory_ready_now: **{report.get('confirmatory_ready_now')}** | confirmatory_outcomes_go: **{report.get('confirmatory_outcomes_go')}**")
    L.append("")
    if report.get("error"):
        L.append(f"## Error\n- `{report.get('error')}`")
    L.append("## Caveats")
    for k, v in (report.get("caveats") or {}).items():
        L.append(f"- {k}: `{v}`")
    L.append("")
    L.append("## Global actions")
    for g in report.get("global_actions") or []:
        L.append(f"- authorizes_confirmatory_outcomes=`{g.get('authorizes_confirmatory_outcomes')}`")
        for a in g.get("action_required") or []:
            L.append(f"  - action: {a}")
        for v in g.get("verification_command_or_check") or []:
            L.append(f"  - verify: `{v}`")
    L.append("")
    L.append("## Per-window action matrices")
    for w in report.get("window_action_matrices") or []:
        L.append(f"### {w.get('window_id')} ({w.get('start')}..{w.get('end')})")
        L.append(f"- fclr019_index_summary_state=**{w.get('fclr019_index_summary_state')}** confirmatory_outcomes_go=**{w.get('confirmatory_outcomes_go')}**")
        for r in w.get("action_rows") or []:
            L.append(f"#### {r.get('prerequisite_id')} — {r.get('prerequisite_label')}")
            L.append(f"- current_state=**{r.get('current_state')}** read_state=`{r.get('read_state')}` authorizes_confirmatory_outcomes=`{r.get('authorizes_confirmatory_outcomes')}` satisfied=`{r.get('satisfied')}` satisfaction_inferred=`{r.get('satisfaction_inferred')}`")
            L.append(f"- blocker_or_missing_reason: {r.get('blocker_or_missing_reason')}")
            if r.get("evidence_ref"):
                L.append(f"- evidence_ref: `{r.get('evidence_ref')}` snapshot=`{(r.get('evidence_snapshot') or {}).get('read_state')}`")
            for a in r.get("action_required") or []:
                L.append(f"- action_required: {a}")
            for v in r.get("verification_command_or_check") or []:
                L.append(f"- verification_command_or_check: `{v}`")
            L.append("")
    L.append("Planning/draft action matrix only — not GO for confirmatory outcomes, not frozen/promoted, no prerequisite marked satisfied, no overlay/H001/Track A status change.")
    path.write_text("\n".join(L) + "\n", encoding="utf-8")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--fclr019-json", default=str(DEFAULT_FCLR019))
    ap.add_argument("--out-dir", default=str(DEFAULT_OUT))
    ap.add_argument("--json-name", default=None)
    ap.add_argument("--md-name", default=None)
    args = ap.parse_args(argv)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    report, ts = build_matrix(Path(args.fclr019_json))
    json_name = args.json_name or f"fclr020_gate4_readiness_action_matrix_{ts}.json"
    md_name = args.md_name or f"fclr020_gate4_readiness_action_matrix_{ts}.md"
    jpath = out_dir / json_name
    mpath = out_dir / md_name
    jpath.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_md(report, mpath)
    (out_dir / "fclr020_gate4_readiness_action_matrix_latest.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out_dir / "fclr020_gate4_readiness_action_matrix_latest.md").write_text(mpath.read_text(encoding="utf-8"), encoding="utf-8")
    print(json.dumps({
        "json": rel(jpath), "md": rel(mpath),
        "latest_json": rel(out_dir / "fclr020_gate4_readiness_action_matrix_latest.json"),
        "latest_md": rel(out_dir / "fclr020_gate4_readiness_action_matrix_latest.md"),
        "draft_only": True, "no_confirmatory_outcomes": True, "exploratory_only": True, "no_network": True,
        "not_go_for_confirmatory_outcomes": True, "confirmatory_ready_now": False, "confirmatory_outcomes_go": False,
        "window_count": len(report.get("window_action_matrices") or []),
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
