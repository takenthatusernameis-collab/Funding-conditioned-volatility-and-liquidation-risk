#!/usr/bin/env python3
"""FCLR-NEXT-141 / FCLR-019: deterministic read-only Gate 4 evidence-bundle index.

Consumes fclr018 latest + available local provenance/admissibility evidence refs
and emits a machine-readable evidence bundle index per candidate window, mapping
each confirmatory prerequisite to present_unverified / present_blocker / missing.

Read-only, no network, no model-outcome computation, no freeze/promotion, no
sealed artifact overwrite. Planning/draft evidence only. Never marks any
prerequisite satisfied unless a concrete local evidence artifact states it
(this tool emits only present_unverified/present_blocker/missing states).
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DEFAULT_FCLR018 = REPO / "research_state" / "fclr018_local_audit" / "fclr018_gate4_prereg_readiness_latest.json"
DEFAULT_OUT = REPO / "research_state" / "fclr019_local_audit"
DEFAULT_FCLR015_DIR = REPO / "research_state" / "fclr015_local_audit"
DEFAULT_FCLR016_DIR = REPO / "research_state" / "fclr016_local_audit"

# Default v5 package refs (best-known local paths; status derived from content only)
V5_DEFAULTS = {
    "terms_evidence": "research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json",
    "provenance_manifest": "research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json",
    "completeness_leakage_audit": "research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json",
    "confirmatory_prereg_draft": "research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json",
}

STATES = ("present_unverified", "present_blocker", "missing")


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(REPO))
    except Exception:
        return str(path)


def read_file_state(path: Path):
    """Return (data_or_None, read_state, note). read_state is one of:
    missing, unavailable_pointer (LFS), read_error, parse_error, ok.
    """
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


def prereq(read_state: str, data, blocker_fn, note=None, evidence_ref=None):
    """Map read state + content to allowed output states only."""
    base = {"evidence_ref": evidence_ref, "read_state": read_state, "note": note}
    if read_state == "missing":
        return {"state": "missing", **base}
    if read_state in ("unavailable_pointer", "read_error", "parse_error"):
        # file ref exists or was targeted but not usable as concrete readable evidence
        label = "unavailable_pointer" if read_state == "unavailable_pointer" else read_state
        return {"state": "missing", **base, "note": note or label}
    # read_state ok
    blocked, bnote = blocker_fn(data) if blocker_fn else (False, None)
    if blocked:
        return {"state": "present_blocker", **base, "blocker_note": bnote}
    return {"state": "present_unverified", **base, "verification_note": bnote or "readable local artifact present; not treated as satisfied by this index"}


def terms_blocker(doc):
    if not isinstance(doc, dict):
        return True, "terms_evidence_not_object"
    status = str(doc.get("status") or "").upper()
    fabricated = bool(doc.get("fabricated"))
    if fabricated:
        return True, "terms_evidence_fabricated_true"
    if status in ("EXPLICIT_BLOCKER_UNRESOLVED", "BLOCKED", "NO_GO", "UNRESOLVED", ""):
        return True, f"terms_status={status or 'EMPTY'}"
    if status in ("RESOLVED_VERIFIED", "RESOLVED"):
        # still not "satisfied" in this index; return unverified with note
        return False, f"terms_status={status}_readable_but_not_confirmed_satisfied_by_index"
    return True, f"terms_status_unrecognized={status}"


def manifest_blocker(doc):
    if not isinstance(doc, dict):
        return True, "provenance_manifest_not_object"
    if doc.get("fabricated"):
        return True, "manifest_fabricated_true"
    if not doc.get("confirmatory_provenance_go"):
        return True, "confirmatory_provenance_go_false_or_missing"
    if not doc.get("admissibility_complete"):
        return True, "admissibility_complete_false_or_missing"
    lt = (doc.get("license_terms") or {}) if isinstance(doc.get("license_terms"), dict) else {}
    lts = str(lt.get("status") or "").upper()
    if "RESOLVED" not in lts or "UNRESOLVED" in lts or "BLOCK" in lts:
        return True, f"license_terms_status={lts or 'MISSING'}"
    return False, "manifest_fields_present_but_not_confirmed_satisfied_by_index"


def completeness_blocker(doc):
    if not isinstance(doc, dict):
        return True, "completeness_audit_not_object"
    blockers = doc.get("blockers_remaining")
    if isinstance(blockers, list) and blockers:
        return True, f"blockers_remaining_count={len(blockers)}"
    comp = doc.get("completeness") if isinstance(doc.get("completeness"), dict) else {}
    leakage = doc.get("leakage_window_checks") if isinstance(doc.get("leakage_window_checks"), dict) else {}
    if comp.get("ok") is False:
        return True, "completeness_ok_false"
    if leakage.get("ok") is False:
        return True, "leakage_window_ok_false"
    if comp.get("ok") is True and leakage.get("ok") is True and not blockers:
        return False, "deterministic_audit_ok_fields_present_but_not_confirmed_satisfied_by_index"
    return True, "completeness_leakage_status_unresolved"


def frozen_prereg_blocker(doc):
    if not isinstance(doc, dict):
        return True, "prereg_not_object"
    # Fresh frozen prereg before outcomes is required; DRAFT is never sufficient.
    if doc.get("draft") is True or not doc.get("frozen_before_outcomes"):
        return True, "prereg_draft_or_not_frozen_before_outcomes"
    if not doc.get("confirmatory_claim_go") or str(doc.get("confirmatory_claim_go")).upper() in ("NO_GO", "NO-GO", "BLOCKED"):
        return True, "prereg_claim_go_not_confirmed"
    return False, "prereg_appears_frozen_but_not_confirmed_satisfied_by_index"


def window_provenance_prereq(window):
    prov = window.get("provenance_status")
    reasons = window.get("confirmatory_ineligibility_reasons") or []
    if prov == "IDENTITY_VERIFIED_BOUNDED_FCLR015":
        # bounded identity evidence context exists per fclr018; still not "satisfied" overall
        return {"state": "present_unverified", "read_state": "from_fclr018", "evidence_ref": "fclr018.window.provenance_status", "verification_note": "IDENTITY_VERIFIED_BOUNDED_FCLR015 for window per fclr018; confirmatory still bounded by ranges/manifest/terms/fresh-frozen-prereg", "blocker_note": None}
    return {"state": "present_blocker", "read_state": "from_fclr018", "evidence_ref": "fclr018.window.provenance_status", "blocker_note": f"provenance_status={prov}; reasons={reasons}"}


def window_coverage_leakage_sufficiency_prereq(window):
    cov_ok = bool(window.get("calendar_coverage_all_symbols_complete"))
    block_ok = bool(window.get("block_count_gate_ge_3"))
    reasons = []
    if not cov_ok:
        reasons.append("calendar_coverage_incomplete_or_unverified")
    if not block_ok:
        reasons.append("block_count_gate_lt_3")
    # leakage controls are design requirements; local coverage/block feasibility only here
    if reasons:
        return {"state": "present_blocker", "read_state": "from_fclr018", "evidence_ref": "fclr018.window.coverage/block_fields", "blocker_note": ";".join(reasons)}
    return {"state": "present_unverified", "read_state": "from_fclr018", "evidence_ref": "fclr018.window.coverage/block_fields", "verification_note": "local coverage/block-count feasibility fields present; leakage audit for any confirmatory run still requires fresh frozen prereg + admissibility package"}


def v5_terms_package_prereq(window):
    v5 = window.get("v5_terms_blocker_state") or {}
    terms = str(v5.get("terms_status") or "").upper()
    all_go = bool(v5.get("all_go"))
    cop = bool(v5.get("confirmatory_outcomes_permitted"))
    if terms in ("EXPLICIT_BLOCKER_UNRESOLVED", "UNRESOLVED", "BLOCKED", "") or not all_go or cop:
        return {"state": "present_blocker", "read_state": "from_fclr018", "evidence_ref": "fclr018.window.v5_terms_blocker_state", "blocker_note": f"terms_status={terms or 'EMPTY'} all_go={all_go} confirmatory_outcomes_permitted={cop}"}
    return {"state": "present_unverified", "read_state": "from_fclr018", "evidence_ref": "fclr018.window.v5_terms_blocker_state", "verification_note": "v5 state not marked blocker by fclr018 fields, but not confirmed satisfied by index"}


def find_fclr015_evidence(fclr015_dir: Path):
    if not fclr015_dir.exists():
        return None, "missing"
    # any probe artifact mentioning 2024_04_09 as present local evidence reference
    cands = sorted(set(list(fclr015_dir.glob("*2024_04_09*probe*.json")) + list(fclr015_dir.glob("*probe*2024_04_09*.json")) + list(fclr015_dir.glob("*2024_04_09*.json"))))
    cands = [c for c in cands if c.is_file()]
    if cands:
        return cands[-1], "ok"
    return None, "missing"


def build_index(fclr018_path: Path, out_dir: Path, fclr015_dir: Path, fclr016_dir: Path, v5_refs: dict):
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    f18, f18_state, f18_note = read_file_state(fclr018_path)
    if f18_state != "ok" or not isinstance(f18, dict):
        report = {
            "artifact": "fclr019_gate4_evidence_bundle_index",
            "version": 1,
            "timestamp_utc": ts,
            "draft_only": True,
            "no_confirmatory_outcomes": True,
            "exploratory_only": True,
            "no_network": True,
            "not_go_for_confirmatory_outcomes": True,
            "error": f"fclr018_latest_unreadable:{f18_state}:{f18_note}",
            "input_fclr018": {"path": rel(fclr018_path), "read_state": f18_state, "note": f18_note},
            "candidate_indices": [],
        }
        report["report_sha256"] = sha256_bytes(json.dumps(report, sort_keys=True).encode())
        return report, ts

    # v5 evidence artifacts (global package refs)
    v5 = {}
    for key, default_rel in v5_refs.items():
        p = REPO / default_rel
        data, rs, note = read_file_state(p)
        if key == "terms_evidence":
            pr = prereq(rs, data, terms_blocker, note=note, evidence_ref=rel(p))
        elif key == "provenance_manifest":
            pr = prereq(rs, data, manifest_blocker, note=note, evidence_ref=rel(p))
        elif key == "completeness_leakage_audit":
            pr = prereq(rs, data, completeness_blocker, note=note, evidence_ref=rel(p))
        elif key == "confirmatory_prereg_draft":
            # draft/frozen prereq file itself is not fresh frozen prereg; always blocked unless real frozen
            pr = prereq(rs, data, frozen_prereg_blocker, note=note, evidence_ref=rel(p))
        else:
            pr = prereq(rs, data, lambda d: (True, "unknown_ref_type"), note=note, evidence_ref=rel(p))
        v5[key] = pr

    # fresh frozen prereg before outcomes is explicitly required and absent unless a concrete frozen artifact states it.
    fresh_frozen = {"state": "missing", "read_state": "policy_check", "evidence_ref": None,
                    "note": "fresh frozen prereg before outcomes required = missing/not frozen (no concrete local frozen prereg artifact confirmed by this index)"}
    # if a v5 confirmatory prereg artifact is readable and actually frozen, still keep present_unverified only through v5 prereq; this separate field remains missing unless explicitly distinct frozen artifact logic is added with concrete evidence.
    f15_path, f15_state = find_fclr015_evidence(fclr015_dir)
    f15 = {"path": rel(f15_path) if f15_path else None, "read_state": f15_state}

    candidates = f18.get("candidate_windows") or []
    indices = []
    for w in candidates:
        wid = w.get("window_id")
        prov_pr = window_provenance_prereq(w)
        # augment evidenced bounded with fclr015 artifact presence (unverified, never satisfied)
        if prov_pr["state"] == "present_unverified" and w.get("provenance_status") == "IDENTITY_VERIFIED_BOUNDED_FCLR015":
            if f15_state == "ok":
                prov_pr = {**prov_pr, "fclr015_evidence_artifact": f15, "blocker_note": None}
            else:
                prov_pr = {"state": "present_blocker", "read_state": "from_fclr018+fclr015_scan", "evidence_ref": "fclr018.window.provenance_status;fclr015_dir_scan", "blocker_note": f"bounded_provenance_claim_without_readable_fclr015_artifact_in_scan:{f15_state}", "fclr015_evidence_artifact": f15}
        cov_pr = window_coverage_leakage_sufficiency_prereq(w)
        v5pkg_pr = v5_terms_package_prereq(w)
        checklist = {
            "identity_provenance_range": prov_pr,
            "manifest_terms_evidence": {
                "provenance_manifest": v5["provenance_manifest"],
                "terms_evidence": v5["terms_evidence"],
                "summary_state": "present_blocker" if any(x["state"] == "present_blocker" for x in [v5["provenance_manifest"], v5["terms_evidence"]]) else ("missing" if any(x["state"] == "missing" for x in [v5["provenance_manifest"], v5["terms_evidence"]]) else "present_unverified"),
            },
            "admissibility_package_status": {
                "completeness_leakage_audit": v5["completeness_leakage_audit"],
                "confirmatory_prereg_draft_ref": v5["confirmatory_prereg_draft"],
                "v5_window_terms_state_from_fclr018": v5pkg_pr,
                "summary_state": "present_blocker" if any(x["state"] == "present_blocker" for x in [v5["completeness_leakage_audit"], v5["confirmatory_prereg_draft"], v5pkg_pr]) else ("missing" if any(x["state"] == "missing" for x in [v5["completeness_leakage_audit"], v5["confirmatory_prereg_draft"], v5pkg_pr]) else "present_unverified"),
            },
            "fresh_frozen_prereg_before_outcomes_required": fresh_frozen,
            "leakage_sufficiency_gates": cov_pr,
        }
        states = []
        def collect(obj):
            if isinstance(obj, dict):
                if obj.get("state") in STATES:
                    states.append(obj["state"])
                for v in obj.values():
                    collect(v)
        collect(checklist)
        any_blocker = "present_blocker" in states
        any_missing = "missing" in states
        indices.append({
            "window_id": wid,
            "start": w.get("start"), "end": w.get("end"),
            "basis": w.get("basis"),
            "fclr018_provenance_status": w.get("provenance_status"),
            "fclr018_confirmatory_eligibility": w.get("confirmatory_eligibility"),
            "confirmatory_outcomes_go": False,
            "index_summary_state": "present_blocker" if any_blocker else ("missing" if any_missing else "present_unverified"),
            "checklist": checklist,
        })

    report = {
        "artifact": "fclr019_gate4_evidence_bundle_index",
        "version": 1,
        "timestamp_utc": ts,
        "draft_only": True,
        "no_confirmatory_outcomes": True,
        "exploratory_only": True,
        "no_network": True,
        "not_go_for_confirmatory_outcomes": True,
        "purpose": "deterministic read-only evidence-bundle index per candidate window; maps confirmatory prerequisites to present_unverified/present_blocker/missing from local files/fields only",
        "inputs": {
            "fclr018_latest": {"path": rel(fclr018_path), "read_state": f18_state, "sha256": sha256_bytes((REPO / rel(fclr018_path)).read_bytes()) if f18_state == "ok" and fclr018_path.exists() else None},
            "fclr015_dir": rel(fclr015_dir),
            "fclr016_dir": rel(fclr016_dir),
            "fclr015_evidence_scan": f15,
            "v5_refs": v5_refs,
        },
        "global_v5_evidence": v5,
        "fresh_frozen_prereg_before_outcomes_required": fresh_frozen,
        "caveats": {
            "draft_only_not_frozen_not_promoted": True,
            "no_confirmatory_outcomes_computed": True,
            "no_prerequisite_marked_satisfied": True,
            "states_used": list(STATES),
            "lfs_pointer_treated_as_unavailable_pointer_missing_state": True,
            "v5_all_go_false_terms_explicit_blocker_unresolved_expected": True,
        },
        "candidate_indices": indices,
        "decision": {
            "confirmatory_ready_now": False,
            "confirmatory_outcomes_go": False,
            "reason": "draft_evidence_index_only_v5_terms_blocker_and_fresh_frozen_prereg_missing",
        },
    }
    report["report_sha256"] = sha256_bytes(json.dumps(report, sort_keys=True).encode())
    return report, ts


def write_md(report: dict, path: Path):
    L = []
    L.append(f"# FCLR-019 Gate 4 evidence-bundle index ({report.get('timestamp_utc')})")
    L.append("")
    L.append("- method: deterministic local evidence read; read-only; no network; no model-outcome computation")
    L.append(f"- draft_only: **{report.get('draft_only')}** | no_confirmatory_outcomes: **{report.get('no_confirmatory_outcomes')}** | exploratory_only: **{report.get('exploratory_only')}** | no_network: **{report.get('no_network')}**")
    L.append(f"- not_go_for_confirmatory_outcomes: **{report.get('not_go_for_confirmatory_outcomes')}**")
    L.append(f"- confirmatory_ready_now: **{report.get('decision',{}).get('confirmatory_ready_now')}** | confirmatory_outcomes_go: **{report.get('decision',{}).get('confirmatory_outcomes_go')}**")
    L.append("")
    L.append("## Caveats")
    for k, v in (report.get("caveats") or {}).items():
        L.append(f"- {k}: `{v}`")
    L.append("")
    L.append("## Global v5 evidence refs")
    for k, v in (report.get("global_v5_evidence") or {}).items():
        L.append(f"- {k}: state=**{v.get('state')}** ref=`{v.get('evidence_ref')}` read_state=`{v.get('read_state')}` note=`{v.get('note') or v.get('blocker_note') or v.get('verification_note')}`")
    L.append(f"- fresh_frozen_prereg_before_outcomes_required: state=**{report.get('fresh_frozen_prereg_before_outcomes_required',{}).get('state')}**")
    L.append("")
    L.append("## Candidate window indices")
    for c in report.get("candidate_indices") or []:
        L.append(f"### {c.get('window_id')} ({c.get('start')}..{c.get('end')})")
        L.append(f"- fclr018_provenance_status=`{c.get('fclr018_provenance_status')}` fclr018_confirmatory_eligibility=`{c.get('fclr018_confirmatory_eligibility')}` index_summary_state=**{c.get('index_summary_state')}** confirmatory_outcomes_go=**{c.get('confirmatory_outcomes_go')}**")
        ch = c.get("checklist") or {}
        L.append(f"- identity_provenance_range: **{(ch.get('identity_provenance_range') or {}).get('state')}** `{(ch.get('identity_provenance_range') or {}).get('blocker_note') or (ch.get('identity_provenance_range') or {}).get('verification_note')}`")
        mt = ch.get("manifest_terms_evidence") or {}
        L.append(f"- manifest_terms_evidence.summary: **{mt.get('summary_state')}** (provenance_manifest={((mt.get('provenance_manifest') or {}).get('state'))}, terms_evidence={((mt.get('terms_evidence') or {}).get('state'))})")
        ap = ch.get("admissibility_package_status") or {}
        L.append(f"- admissibility_package_status.summary: **{ap.get('summary_state')}** (completeness={((ap.get('completeness_leakage_audit') or {}).get('state'))}, v5_window_terms={((ap.get('v5_window_terms_state_from_fclr018') or {}).get('state'))})")
        L.append(f"- fresh_frozen_prereg_before_outcomes_required: **{((ch.get('fresh_frozen_prereg_before_outcomes_required') or {}).get('state'))}**")
        L.append(f"- leakage_sufficiency_gates: **{((ch.get('leakage_sufficiency_gates') or {}).get('state'))}** `{((ch.get('leakage_sufficiency_gates') or {}).get('blocker_note') or (ch.get('leakage_sufficiency_gates') or {}).get('verification_note'))}`")
        L.append("")
    L.append("Planning/draft evidence only — not GO for confirmatory outcomes, not frozen/promoted, no prerequisite marked satisfied, no overlay/H001/Track A status change.")
    path.write_text("\n".join(L) + "\n", encoding="utf-8")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--fclr018-json", default=str(DEFAULT_FCLR018))
    ap.add_argument("--fclr015-dir", default=str(DEFAULT_FCLR015_DIR))
    ap.add_argument("--fclr016-dir", default=str(DEFAULT_FCLR016_DIR))
    ap.add_argument("--terms-evidence", default=V5_DEFAULTS["terms_evidence"])
    ap.add_argument("--provenance-manifest", default=V5_DEFAULTS["provenance_manifest"])
    ap.add_argument("--completeness-leakage-audit", default=V5_DEFAULTS["completeness_leakage_audit"])
    ap.add_argument("--confirmatory-prereg-draft", default=V5_DEFAULTS["confirmatory_prereg_draft"])
    ap.add_argument("--out-dir", default=str(DEFAULT_OUT))
    ap.add_argument("--json-name", default=None)
    ap.add_argument("--md-name", default=None)
    args = ap.parse_args(argv)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    v5_refs = {
        "terms_evidence": args.terms_evidence,
        "provenance_manifest": args.provenance_manifest,
        "completeness_leakage_audit": args.completeness_leakage_audit,
        "confirmatory_prereg_draft": args.confirmatory_prereg_draft,
    }
    report, ts = build_index(Path(args.fclr018_json), out_dir, Path(args.fclr015_dir), Path(args.fclr016_dir), v5_refs)
    json_name = args.json_name or f"fclr019_gate4_evidence_bundle_index_{ts}.json"
    md_name = args.md_name or f"fclr019_gate4_evidence_bundle_index_{ts}.md"
    jpath = out_dir / json_name
    mpath = out_dir / md_name
    jpath.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_md(report, mpath)
    (out_dir / "fclr019_gate4_evidence_bundle_index_latest.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out_dir / "fclr019_gate4_evidence_bundle_index_latest.md").write_text(mpath.read_text(encoding="utf-8"), encoding="utf-8")
    print(json.dumps({
        "json": rel(jpath), "md": rel(mpath),
        "latest_json": rel(out_dir / "fclr019_gate4_evidence_bundle_index_latest.json"),
        "latest_md": rel(out_dir / "fclr019_gate4_evidence_bundle_index_latest.md"),
        "draft_only": True, "no_confirmatory_outcomes": True, "exploratory_only": True, "no_network": True,
        "not_go_for_confirmatory_outcomes": True, "confirmatory_ready_now": False,
        "candidate_count": len(report.get("candidate_indices") or []),
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
