#!/usr/bin/env python3
"""FCLR-NEXT-143 / FCLR-021: deterministic read-only Gate 4 blocker-resolution
checklist validator consuming the FCLR-020 readiness action matrix.

Consumes fclr020 latest (and only local refs it cites) and, per window and per
prerequisite/checklist item, validates that action_required /
verification_command_or_check cover the required gate set:
  (a) terms/legal evidence resolution,
  (b) provenance/manifest evidence,
  (c) admissibility/completeness/leakage evidence,
  (d) fresh frozen prereg before outcomes,
  (e) leakage/sufficiency.
Emits a machine-checkable coverage matrix row
(window, prerequisite, current_state, coverage_ok, missing_action_class,
 missing_markers, verification_command_or_check) plus missing-action warnings.

Read-only, no network, no model-outcome computation, no freeze/promotion, no
sealed overwrite. Planning/draft evidence only. Never marks satisfied, never
infers satisfaction from absence of a blocker string, never fabricates
evidence as present. coverage_ok means the action/check TEXT references the
required gate class — it is NOT evidence that the prerequisite is resolved.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DEFAULT_FCLR020 = REPO / "research_state" / "fclr020_local_audit" / "fclr020_gate4_readiness_action_matrix_latest.json"
DEFAULT_OUT = REPO / "research_state" / "fclr021_local_audit"

STATES = ("present_unverified", "present_blocker", "missing")

# Gate classes the action/check text must cover per prerequisite.
GATE_CLASSES = (
    "terms_legal_evidence_resolution",
    "provenance_manifest_evidence",
    "admissibility_completeness_leakage_evidence",
    "fresh_frozen_prereg_before_outcomes",
    "leakage_sufficiency_gates",
)

# prerequisite_id -> gate class it must be covered against.
PREREQ_TO_GATE_CLASS = {
    "identity_provenance_range": "provenance_manifest_evidence",
    "manifest_terms_evidence": "terms_legal_evidence_resolution",
    "manifest_terms_evidence.provenance_manifest": "provenance_manifest_evidence",
    "manifest_terms_evidence.terms_evidence": "terms_legal_evidence_resolution",
    "admissibility_package_status": "admissibility_completeness_leakage_evidence",
    "admissibility_package_status.completeness_leakage_audit": "admissibility_completeness_leakage_evidence",
    "admissibility_package_status.confirmatory_prereg_draft_ref": "fresh_frozen_prereg_before_outcomes",
    "admissibility_package_status.v5_window_terms_state_from_fclr018": "terms_legal_evidence_resolution",
    "fresh_frozen_prereg_before_outcomes_required": "fresh_frozen_prereg_before_outcomes",
    "leakage_sufficiency_gates": "leakage_sufficiency_gates",
}

# Required substring markers (case-insensitive) that the joined action /
# verification text must reference for the gate class to count as covered.
GATE_CLASS_MARKERS = {
    "terms_legal_evidence_resolution": {
        "action": ["terms", "human/legal", "fabricated=false", "verifiable evidence"],
        "check": ["fclr016_v5_admissibility_report", "fclr016_v5_promotion_dryrun"],
    },
    "provenance_manifest_evidence": {
        "action": ["provenance", "manifest", "hash", "identity-verified", "bounded"],
        "check": ["sha256sum", "test -f", "json_ok", "fclr015"],
    },
    "admissibility_completeness_leakage_evidence": {
        "action": ["completeness", "leakage", "admissibility", "blockers"],
        "check": ["unittest discover", "check_tracka_scope_registry_drift", "tracka_resume_check"],
    },
    "fresh_frozen_prereg_before_outcomes": {
        "action": ["fresh confirmatory preregistration", "before any confirmatory outcomes", "not sufficient", "draft"],
        "check": ["run_funding_ablations", "unittest discover"],
    },
    "leakage_sufficiency_gates": {
        "action": ["leakage", "purge/embargo", "30-day", "5 symbols", "sufficiency"],
        "check": ["run_funding_ablations", "unittest discover"],
    },
}


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


def gate_class_for(prerequisite_id):
    return PREREQ_TO_GATE_CLASS.get(prerequisite_id)


def coverage_for_row(row):
    """Deterministic text-coverage check of the row's action/check text.

    Returns (coverage_ok, missing_action_class, missing_markers).
    coverage_ok is about text referencing the gate class, NOT about the
    prerequisite being resolved; never inferred from absence of a blocker.
    """
    pid = row.get("prerequisite_id")
    action_text = " ".join(row.get("action_required") or []).lower()
    check_text = " ".join(row.get("verification_command_or_check") or []).lower()
    cls = gate_class_for(pid)
    if cls is None:
        return False, "unmapped_prerequisite", ["no gate class mapped for prerequisite_id:" + str(pid)]
    markers = GATE_CLASS_MARKERS.get(cls, {"action": [], "check": []})
    missing = []
    for m in markers.get("action", []):
        if m.lower() not in action_text:
            missing.append("action:" + m)
    for m in markers.get("check", []):
        if m.lower() not in check_text:
            missing.append("check:" + m)
    coverage_ok = len(missing) == 0
    missing_action_class = None if coverage_ok else cls
    return coverage_ok, missing_action_class, missing


def base_row(window_id, row):
    node = row if isinstance(row, dict) else {}
    state = node.get("current_state") if node.get("current_state") in STATES else "missing"
    coverage_ok, missing_action_class, missing_markers = coverage_for_row(node)
    return {
        "window_id": window_id,
        "prerequisite_id": node.get("prerequisite_id"),
        "prerequisite_label": node.get("prerequisite_label"),
        "current_state": state,
        "read_state": node.get("read_state"),
        "evidence_ref": node.get("evidence_ref"),
        "evidence_snapshot": local_evidence_snapshot(node.get("evidence_ref")),
        "blocker_or_missing_reason": node.get("blocker_or_missing_reason") or f"state={state}",
        "gate_class": PREREQ_TO_GATE_CLASS.get(node.get("prerequisite_id")),
        "coverage_ok": coverage_ok,
        "missing_action_class": missing_action_class,
        "missing_markers": missing_markers,
        "verification_command_or_check": list(node.get("verification_command_or_check") or []),
        "authorizes_confirmatory_outcomes": False,
        "satisfied": False,
        "satisfaction_inferred": False,
    }


def common_readonly_checks(evidence_ref):
    checks = [
        "python -m unittest discover tests -q  # baseline regression (no confirmatory outcomes)",
        "python scripts/check_tracka_scope_registry_drift.py  # read-only drift check",
        "python scripts/tracka_resume_check.py  # read-only resume check (network:false)",
    ]
    if evidence_ref and isinstance(evidence_ref, str) and not evidence_ref.startswith("fclr020."):
        checks.insert(0, f"test -f {evidence_ref} && sha256sum {evidence_ref}  # read-only existence/hash check")
        if evidence_ref.endswith('.json'):
            checks.insert(1, f"python3 -c \"import json; json.load(open('{evidence_ref}')); print('json_ok')\"  # read-only parse check")
    return checks


def rows_for_window(window):
    wid = window.get("window_id")
    rows = []
    for r in window.get("action_rows") or []:
        row = base_row(wid, r)
        row["verification_command_or_check"] = common_readonly_checks(r.get("evidence_ref")) + list(r.get("verification_command_or_check") or [])
        rows.append(row)
    return rows


def build_matrix(fclr020_path: Path):
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    f20, f20_state, f20_note = read_file_state(fclr020_path)
    if f20_state != "ok" or not isinstance(f20, dict):
        report = {
            "artifact": "fclr021_gate4_blocker_resolution_checklist_validator",
            "version": 1,
            "timestamp_utc": ts,
            "draft_only": True,
            "no_confirmatory_outcomes": True,
            "exploratory_only": True,
            "no_network": True,
            "not_go_for_confirmatory_outcomes": True,
            "confirmatory_ready_now": False,
            "confirmatory_outcomes_go": False,
            "authorizes_confirmatory_outcomes": False,
            "error": f"fclr020_latest_unreadable:{f20_state}:{f20_note}",
            "input_fclr020": {"path": rel(fclr020_path), "read_state": f20_state, "note": f20_note},
            "coverage_matrix": [],
            "missing_action_warnings": [],
            "global_actions": [],
        }
        report["report_sha256"] = sha256_bytes(json.dumps(report, sort_keys=True).encode())
        return report, ts

    windows = f20.get("window_action_matrices") or []
    coverage_matrix = []
    missing_action_warnings = []
    for w in windows:
        for row in rows_for_window(w):
            coverage_matrix.append(row)
            if not row["coverage_ok"]:
                missing_action_warnings.append({
                    "window": row["window_id"],
                    "prerequisite": row["prerequisite_id"],
                    "current_state": row["current_state"],
                    "gate_class": row["gate_class"],
                    "missing_action_class": row["missing_action_class"],
                    "missing_markers": row["missing_markers"],
                    "warning": f"coverage gap: {row['window_id']}/{row['prerequisite_id']} gate_class={row['gate_class']} missing={row['missing_markers']}",
                })

    global_actions = [{
        "scope": "global",
        "action_required": [
            "Keep v5 terms/admissibility fail-closed until verifiable human/legal evidence resolves blockers and package is GO.",
            "Track A/H004 remains blocked; do not re-probe absent Hyperliquid months in a loop.",
            "No .github/workflows edits; no sealed holdout/anchor overwrites; no competing handoff files.",
            "coverage_ok references action/check text only; it does not resolve a blocker or mark a prerequisite satisfied.",
        ],
        "verification_command_or_check": [
            "python scripts/fclr016_v5_admissibility_report.py --bogus --json 2>&1 | head -c 200",
            "python scripts/tracka_resume_check.py | python3 -c \"import sys,json; d=json.load(sys.stdin); print(d['pass'], d['network'])\"",
        ],
        "authorizes_confirmatory_outcomes": False,
    }]

    total = len(coverage_matrix)
    covered = sum(1 for r in coverage_matrix if r["coverage_ok"])
    report = {
        "artifact": "fclr021_gate4_blocker_resolution_checklist_validator",
        "version": 1,
        "timestamp_utc": ts,
        "draft_only": True,
        "no_confirmatory_outcomes": True,
        "exploratory_only": True,
        "no_network": True,
        "not_go_for_confirmatory_outcomes": True,
        "confirmatory_ready_now": False,
        "confirmatory_outcomes_go": False,
        "authorizes_confirmatory_outcomes": False,
        "purpose": "deterministic read-only coverage validation of FCLR-020 action/check text against the Gate 4 prerequisite gate set; no outcome computation, no satisfaction inference",
        "input_fclr020": {"path": rel(fclr020_path), "read_state": f20_state, "sha256": sha256_bytes(fclr020_path.read_bytes()) if fclr020_path.exists() else None},
        "gate_classes": list(GATE_CLASSES),
        "coverage_summary": {"total_rows": total, "covered_rows": covered, "gap_rows": total - covered},
        "caveats": {
            "draft_only_not_frozen_not_promoted": True,
            "no_confirmatory_outcomes_computed": True,
            "no_prerequisite_marked_satisfied": True,
            "no_satisfaction_inferred_from_absent_blocker": True,
            "coverage_ok_is_text_coverage_not_resolution": True,
            "lfs_pointer_treated_as_unavailable": True,
            "states_used": list(STATES),
        },
        "global_actions": global_actions,
        "coverage_matrix": coverage_matrix,
        "missing_action_warnings": missing_action_warnings,
        "decision": {
            "confirmatory_ready_now": False,
            "confirmatory_outcomes_go": False,
            "reason": "draft_coverage_validator_only_from_fclr020_no_confirmatory_authorization",
        },
    }
    report["report_sha256"] = sha256_bytes(json.dumps(report, sort_keys=True).encode())
    return report, ts


def write_md(report: dict, path: Path):
    L = []
    L.append(f"# FCLR-021 Gate 4 blocker-resolution checklist validator ({report.get('timestamp_utc')})")
    L.append("")
    L.append("- method: deterministic read-only coverage check of FCLR-020 action/check text vs Gate 4 prerequisite gate set; no network; no model-outcome computation")
    L.append(f"- draft_only: **{report.get('draft_only')}** | no_confirmatory_outcomes: **{report.get('no_confirmatory_outcomes')}** | exploratory_only: **{report.get('exploratory_only')}** | no_network: **{report.get('no_network')}**")
    L.append(f"- not_go_for_confirmatory_outcomes: **{report.get('not_go_for_confirmatory_outcomes')}** | confirmatory_ready_now: **{report.get('confirmatory_ready_now')}** | confirmatory_outcomes_go: **{report.get('confirmatory_outcomes_go')}**")
    L.append("")
    if report.get("error"):
        L.append(f"## Error\n- `{report.get('error')}`")
    L.append("## Caveats")
    for k, v in (report.get("caveats") or {}).items():
        L.append(f"- {k}: `{v}`")
    L.append("")
    cs = report.get("coverage_summary") or {}
    L.append("## Coverage summary")
    L.append(f"- total_rows=**{cs.get('total_rows')}** covered_rows=**{cs.get('covered_rows')}** gap_rows=**{cs.get('gap_rows')}**")
    L.append("")
    L.append("## Global actions")
    for g in report.get("global_actions") or []:
        L.append(f"- authorizes_confirmatory_outcomes=`{g.get('authorizes_confirmatory_outcomes')}`")
        for a in g.get("action_required") or []:
            L.append(f"  - action: {a}")
        for v in g.get("verification_command_or_check") or []:
            L.append(f"  - verify: `{v}`")
    L.append("")
    L.append("## Missing-action warnings (coverage gaps)")
    for w in report.get("missing_action_warnings") or []:
        L.append(f"- window=`{w.get('window')}` prerequisite=`{w.get('prerequisite')}` current_state=`{w.get('current_state')}` gate_class=`{w.get('gate_class')}` missing_action_class=`{w.get('missing_action_class')}` missing_markers=`{w.get('missing_markers')}`")
        L.append(f"  - warning: {w.get('warning')}")
    L.append("")
    L.append("## Coverage matrix (per window / prerequisite)")
    for r in report.get("coverage_matrix") or []:
        L.append(f"### {r.get('window_id')} — {r.get('prerequisite_id')} ({r.get('prerequisite_label')})")
        L.append(f"- current_state=**{r.get('current_state')}** gate_class=`{r.get('gate_class')}` coverage_ok=`{r.get('coverage_ok')}` missing_action_class=`{r.get('missing_action_class')}` missing_markers=`{r.get('missing_markers')}`")
        L.append(f"- blocker_or_missing_reason: {r.get('blocker_or_missing_reason')}")
        if r.get("evidence_ref"):
            L.append(f"- evidence_ref: `{r.get('evidence_ref')}` snapshot=`{(r.get('evidence_snapshot') or {}).get('read_state')}`")
        for v in r.get("verification_command_or_check") or []:
            L.append(f"- verification_command_or_check: `{v}`")
        L.append("")
    L.append("Planning/draft coverage validation only — not GO for confirmatory outcomes, not frozen/promoted, no prerequisite marked satisfied, no overlay/H001/Track A status change.")
    path.write_text("\n".join(L) + "\n", encoding="utf-8")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--fclr020-json", default=str(DEFAULT_FCLR020))
    ap.add_argument("--out-dir", default=str(DEFAULT_OUT))
    ap.add_argument("--json-name", default=None)
    ap.add_argument("--md-name", default=None)
    args = ap.parse_args(argv)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    report, ts = build_matrix(Path(args.fclr020_json))
    json_name = args.json_name or f"fclr021_gate4_blocker_resolution_checklist_validator_{ts}.json"
    md_name = args.md_name or f"fclr021_gate4_blocker_resolution_checklist_validator_{ts}.md"
    jpath = out_dir / json_name
    mpath = out_dir / md_name
    jpath.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_md(report, mpath)
    (out_dir / "fclr021_gate4_blocker_resolution_checklist_validator_latest.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out_dir / "fclr021_gate4_blocker_resolution_checklist_validator_latest.md").write_text(mpath.read_text(encoding="utf-8"), encoding="utf-8")
    print(json.dumps({
        "json": rel(jpath), "md": rel(mpath),
        "latest_json": rel(out_dir / "fclr021_gate4_blocker_resolution_checklist_validator_latest.json"),
        "latest_md": rel(out_dir / "fclr021_gate4_blocker_resolution_checklist_validator_latest.md"),
        "draft_only": True, "no_confirmatory_outcomes": True, "exploratory_only": True, "no_network": True,
        "not_go_for_confirmatory_outcomes": True, "confirmatory_ready_now": False, "confirmatory_outcomes_go": False,
        "authorizes_confirmatory_outcomes": False,
        "total_rows": (report.get("coverage_summary") or {}).get("total_rows"),
        "covered_rows": (report.get("coverage_summary") or {}).get("covered_rows"),
        "gap_rows": (report.get("coverage_summary") or {}).get("gap_rows"),
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
