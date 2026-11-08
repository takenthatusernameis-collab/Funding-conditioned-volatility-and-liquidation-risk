#!/usr/bin/env python3
"""Read-only Gate 4 v5 scope-coherence / blocker-matrix report (no outcomes, no network, no data).

Extends the admissibility-package view with an explicit per-gate blocker matrix that
includes scope alignment across pm/ca/te/pr, and references verifiable local evidence
for 2024-04..09 (fclr015/fclr017/inventory reconciliation) as present_unverified/bounded
ONLY — never as confirmatory GO and never creating/satisfying evidence.

Deterministic, tmp-testable. Fail-closed: never claims GO or permits confirmatory outcomes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import run_funding_ablations as rfa  # noqa: E402

# Local evidence refs for 2024-04..09 — referenceable as present_unverified/bounded only.
LOCAL_2024_0409_EVIDENCE_REFS = [
    {
        "id": "fclr015_input_manifest_2024_04_09",
        "path": "research_state/fclr015_local_audit/fclr015_input_manifest_2024_04_09_20261107T180626Z.json",
        "claim_class": "present_unverified_bounded_identity_audit",
        "confirmatory_go": False,
        "note": "Bounded Binance Vision identity verification context; not by itself confirmatory GO/package completeness/license resolution.",
    },
    {
        "id": "fclr017_gate4_cache_coverage_audit_latest",
        "path": "research_state/fclr017_local_audit/fclr017_gate4_cache_audit_latest.json",
        "claim_class": "present_unverified_bounded_coverage_audit",
        "confirmatory_go": False,
        "note": "Local cache coverage/lineage audit (exploratory, no outcomes/network); not confirmatory GO or provenance/license/terms resolution.",
    },
]


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _load(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _scope_window(d: dict) -> str | None:
    return (d.get("frozen_scope") or {}).get("window")


def _file_evidence(path_rel: str) -> dict:
    p = REPO / path_rel
    if not p.exists() or not p.is_file():
        return {"path": path_rel, "present": False, "sha256": None, "bytes": None, "read_state": "missing"}
    try:
        b = p.read_bytes()
        return {"path": path_rel, "present": True, "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b), "read_state": "ok"}
    except Exception as e:
        return {"path": path_rel, "present": False, "sha256": None, "bytes": None, "read_state": f"read_error:{type(e).__name__}"}


def _scope_alignment_matrix(pm: dict, ca: dict, te: dict, pr: dict) -> dict:
    windows = {
        "provenance_license_manifest": _scope_window(pm),
        "completeness_leakage_audit": _scope_window(ca),
        "terms_evidence": _scope_window(te),
        "confirmatory_prereg": _scope_window(pr),
    }
    non_null = {k: v for k, v in windows.items() if v}
    aligned = len(set(non_null.values())) <= 1 if non_null else False
    # Identify prereg-vs-pm/ca mismatch explicitly (the known 2024-04..09 draft vs 2025-08..10 manifests case).
    prereg_w = windows["confirmatory_prereg"]
    pm_w = windows["provenance_license_manifest"]
    ca_w = windows["completeness_leakage_audit"]
    prereg_scope_mismatch = bool(
        prereg_w and ((pm_w and prereg_w != pm_w) or (ca_w and prereg_w != ca_w))
    )
    return {
        "scope_windows": windows,
        "all_windows_aligned": aligned,
        "prereg_scope_mismatch_vs_provenance_completeness": prereg_scope_mismatch,
        "required_artifact_classes_for_prereg_window": {
            "prereg_window": prereg_w,
            "required_when_claiming_confirmatory_go": [
                "provenance_license_manifest scoped to prereg window with verifiable provenance/license (not fabricated)",
                "completeness_leakage_audit scoped to prereg window with deterministic PASS verdict",
                "resolved human/legal terms_evidence (RESOLVED_VERIFIED, fabricated=false) scoped/covering prereg window",
                "fresh frozen prereg (draft=false, frozen_before_outcomes=true) with reconciled refs/hashes",
            ],
            "satisfied_by_current_package": False,
            "note": "Matrix is read-only diagnostic; does not create/satisfy evidence and does not claim GO.",
        },
    }


def _local_evidence_refs() -> list[dict]:
    out = []
    for ref in LOCAL_2024_0409_EVIDENCE_REFS:
        ev = _file_evidence(ref["path"])
        out.append({
            **ref,
            "evidence": ev,
            "reference_only": True,
            "present_unverified_bounded": bool(ev.get("present")),
            "usable_as_confirmatory_go": False,
        })
    return out


def build_scope_coherence_report(pm_p, ca_p, te_p, pr_p) -> dict:
    pm_p, ca_p, te_p, pr_p = map(Path, (pm_p, ca_p, te_p, pr_p))
    pkg = rfa.check_admissibility_package(str(pm_p), str(ca_p), str(te_p), str(pr_p), expect_go=True)
    pm, ca, te, pr = _load(pm_p), _load(ca_p), _load(te_p), _load(pr_p)
    gates = pkg.get("gates", {}) if isinstance(pkg, dict) else {}
    errors = list(pkg.get("errors", []) or []) if isinstance(pkg, dict) else []
    blockers = [k for k, v in gates.items() if not v] if gates else list(pkg.get("blockers", []) or [])
    scope_matrix = _scope_alignment_matrix(pm, ca, te, pr)
    local_refs = _local_evidence_refs()
    gate_blocker_matrix = []
    for gate, ok in gates.items():
        reason = "ok" if ok else "blocked"
        gate_blocker_matrix.append({
            "gate": gate,
            "pass": bool(ok),
            "blocker": (not ok),
            "reason_class": "scope_alignment" if (gate in ("provenance_manifest_go", "completeness_leakage_pass") and scope_matrix["prereg_scope_mismatch_vs_provenance_completeness"]) else ("terms_unresolved" if gate == "terms_resolved_verified" else ("prereg_not_frozen_or_claim" if gate.startswith("prereg") else reason)),
        })
    # Add explicit scope-alignment row regardless of gate booleans.
    gate_blocker_matrix.append({
        "gate": "scope_alignment_prereg_vs_provenance_completeness",
        "pass": not scope_matrix["prereg_scope_mismatch_vs_provenance_completeness"],
        "blocker": scope_matrix["prereg_scope_mismatch_vs_provenance_completeness"],
        "reason_class": "scope_alignment",
        "detail": scope_matrix["scope_windows"],
    })
    return {
        "validator": "fclr024_v5_scope_coherence_report",
        "ok": bool(pkg.get("ok", False)),
        "all_go": False,  # never claimed by this diagnostic tool
        "confirmatory_outcomes_permitted": False,
        "package_all_go_raw": bool(pkg.get("all_go", False)),
        "package_confirmatory_outcomes_permitted_raw": bool(pkg.get("confirmatory_outcomes_permitted", False)),
        "gates": gates,
        "blockers": blockers,
        "errors": errors,
        "gate_blocker_matrix": gate_blocker_matrix,
        "scope_coherence": scope_matrix,
        "local_2024_04_09_evidence_refs": local_refs,
        "artifacts": {
            "provenance_license_manifest": {"path": str(pm_p.resolve()), "sha256": _sha(pm_p), "scope_window": _scope_window(pm)},
            "completeness_leakage_audit": {"path": str(ca_p.resolve()), "sha256": _sha(ca_p), "scope_window": _scope_window(ca)},
            "terms_evidence": {"path": str(te_p.resolve()), "sha256": _sha(te_p), "scope_window": _scope_window(te), "status": te.get("status"), "fabricated": te.get("fabricated")},
            "confirmatory_prereg": {"path": str(pr_p.resolve()), "sha256": _sha(pr_p), "scope_window": _scope_window(pr), "draft": pr.get("draft")},
        },
        "no_confirmatory_outcomes": True,
        "no_network": True,
        "no_data_loading": True,
        "creates_or_satisfies_evidence": False,
        "fabricates_provenance_completeness_license": False,
    }


def render_markdown(r: dict) -> str:
    L = ["# FCLR-024 v5 scope-coherence / blocker matrix (read-only)", ""]
    L.append(f"- ok: {r['ok']}")
    L.append(f"- all_go (forced false by diagnostic): {r['all_go']}")
    L.append(f"- confirmatory_outcomes_permitted (forced false): {r['confirmatory_outcomes_permitted']}")
    L.append(f"- package_all_go_raw (from underlying check, informational): {r['package_all_go_raw']}")
    L.append(f"- scope prereg mismatch vs pm/ca: {r['scope_coherence']['prereg_scope_mismatch_vs_provenance_completeness']}")
    L.append("")
    L.append("## Scope windows")
    for k, v in r["scope_coherence"]["scope_windows"].items():
        L.append(f"- {k}: {v}")
    L.append("")
    L.append("## Gate/blocker matrix")
    for row in r["gate_blocker_matrix"]:
        L.append(f"- {row['gate']}: pass={row['pass']} blocker={row['blocker']} reason={row['reason_class']}")
    if r["errors"]:
        L.append("")
        L.append("## Errors")
        for e in r["errors"]:
            L.append(f"- {e}")
    L.append("")
    L.append("## Local 2024-04..09 evidence refs (present_unverified/bounded only; NOT confirmatory GO)")
    for ref in r["local_2024_04_09_evidence_refs"]:
        ev = ref["evidence"]
        L.append(f"- {ref['id']}: present={ev.get('present')} read_state={ev.get('read_state')} confirmatory_go={ref['confirmatory_go']} class={ref['claim_class']}")
    L.append("")
    L.append("## Invariants")
    L.append("- No confirmatory outcomes. No network. No data loading. No evidence created/satisfied. No fabrication.")
    return "\n".join(L) + "\n"


def _refusal(error: str) -> dict:
    return {
        "ok": False, "all_go": False, "confirmatory_outcomes_permitted": False,
        "error": error, "errors": [error], "blockers": ["refusal"], "gates": {},
        "gate_blocker_matrix": [], "scope_coherence": {}, "local_2024_04_09_evidence_refs": [],
        "validator": "fclr024_v5_scope_coherence_report",
        "no_confirmatory_outcomes": True, "no_network": True, "no_data_loading": True,
        "creates_or_satisfies_evidence": False, "fabricates_provenance_completeness_license": False,
    }


def main(argv=None) -> int:
    try:
        ap = argparse.ArgumentParser(description="Read-only FCLR-024 v5 scope-coherence report")
        ap.add_argument("provenance_manifest")
        ap.add_argument("completeness_audit")
        ap.add_argument("terms_evidence")
        ap.add_argument("prereg_draft")
        ap.add_argument("terms_evidence_override", nargs="?")
        ap.add_argument("--json-only", action="store_true")
        try:
            args = ap.parse_args(argv)
        except SystemExit as e:
            code = e.code if isinstance(e.code, int) else 2
            if code == 0:
                return 0
            print(json.dumps(_refusal(f"argparse error: {e}"), sort_keys=True))
            return code
        pm_p = Path(args.provenance_manifest); ca_p = Path(args.completeness_audit)
        te_p = Path(args.terms_evidence_override or args.terms_evidence); pr_p = Path(args.prereg_draft)
        for p in (pm_p, ca_p, te_p, pr_p):
            if not p.exists() or not p.is_file():
                print(json.dumps(_refusal(f"missing/not-file: {p}"), sort_keys=True))
                return 2
        try:
            report = build_scope_coherence_report(pm_p, ca_p, te_p, pr_p)
        except Exception as e:
            print(json.dumps(_refusal(f"cannot build report: {e}"), sort_keys=True))
            return 2
        print(json.dumps(report, indent=2, sort_keys=True))
        if not args.json_only:
            print("---MARKDOWN---")
            print(render_markdown(report), end="")
        return 0
    except Exception as e:
        print(json.dumps(_refusal(f"internal refusal: {e}"), sort_keys=True))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
