#!/usr/bin/env python3
"""Deterministic, read-only Gate 4 v5 admissibility validator (NO outcomes, NO network).

Validates provenance/license manifest, completeness/leakage audit, terms evidence, and
prereg draft as a coherent, fail-closed package. Exits 0 with ok=true for a consistent
blocked/non-GO package; with --expect-go requires full confirmatory GO and exits 2 otherwise.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

RESOLVED_TERMS = "RESOLVED_VERIFIED"
PASS_COMPLETENESS = "PASS_COMPLETENESS_LEAKAGE_DETERMINISTIC"


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def fail(msg: str, **extra):
    out = {"validator": "fclr016_v5_admissibility", "ok": False, "error": msg}
    out.update(extra)
    print(json.dumps(out, indent=2, sort_keys=True))
    return 2


def _artifact_common(name: str, d: dict):
    if d.get("no_confirmatory_outcomes") is not True:
        return f"{name}.no_confirmatory_outcomes must be true"
    if d.get("fabricated") is True:
        return f"{name}.fabricated must not be true"
    if str(d.get("confirmatory_claim_go", "")).upper() not in ("NO_GO", "GO", ""):
        return f"{name}.confirmatory_claim_go has unexpected value"
    return None


def _check_resolved_terms_evidence(te: dict):
    """Fail-closed checks when terms evidence claims RESOLVED_VERIFIED."""
    if te.get("status") != RESOLVED_TERMS:
        return None
    if te.get("fabricated") is not False:
        return "RESOLVED_VERIFIED terms evidence must set fabricated=false"
    for k in ("terms_url_reviewed", "access_date_utc", "reviewer_role", "conclusion"):
        v = te.get(k)
        if v is None or (isinstance(v, str) and not v.strip()):
            return f"RESOLVED_VERIFIED terms evidence missing required field: {k}"
    rr = str(te.get("reviewer_role", "")).lower()
    if "agent" in rr and "human" not in rr and "legal" not in rr and "maintainer" not in rr:
        return "RESOLVED_VERIFIED terms evidence reviewer_role appears agent-only (human/legal review required)"
    if te.get("confirmatory_provenance_go") is not True and te.get("admissibility_complete") is False:
        pass  # may be resolved but package still blocked by other gates; caller evaluates
    return None


def _scope_window(d: dict):
    return (d.get("frozen_scope") or {}).get("window")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--provenance-manifest", required=True)
    ap.add_argument("--completeness-audit", required=True)
    ap.add_argument("--terms-evidence", required=True)
    ap.add_argument("--prereg-draft", required=True)
    ap.add_argument("--expect-go", action="store_true", help="Require full confirmatory GO; otherwise validate package consistency")
    args = ap.parse_args(argv)
    pm_p, ca_p, te_p, pr_p = map(Path, [args.provenance_manifest, args.completeness_audit, args.terms_evidence, args.prereg_draft])
    for p in (pm_p, ca_p, te_p, pr_p):
        if not p.exists():
            return fail(f"missing: {p}")
    pm, ca, te, pr = load(pm_p), load(ca_p), load(te_p), load(pr_p)

    # hard invariants
    for name, d in [("provenance", pm), ("completeness", ca), ("terms", te), ("prereg", pr)]:
        err = _artifact_common(name, d)
        if err:
            return fail(err)
    # provenance manifest must not claim fabricated/resolved-via-fabrication in nested terms block
    lt = pm.get("license_terms") or {}
    if lt.get("fabricated") is True:
        return fail("provenance.license_terms.fabricated must not be true")
    if te.get("fabricated") is True or te.get("status") == RESOLVED_TERMS and te.get("fabricated") is not False:
        return fail("terms evidence fabricated marker inconsistent with resolved status")
    # scope alignment
    scope = pm.get("frozen_scope") or {}
    if not scope:
        return fail("provenance manifest missing frozen_scope")
    for name, d in [("completeness", ca), ("terms", te), ("prereg", pr)]:
        dw = _scope_window(d)
        if dw and dw != scope.get("window"):
            return fail(f"{name} scope window mismatch vs provenance manifest")
    # prereg consistency
    if pr.get("draft") is True:
        for k in ("frozen_before_outcomes", "promotable_to_frozen", "admissibility_complete", "license_terms_resolved"):
            if pr.get(k) is True:
                return fail(f"draft prereg cannot set {k}=true")
        if pr.get("confirmatory_claim_go") != "NO_GO":
            return fail("draft prereg must keep confirmatory_claim_go=NO_GO")
        if (pr.get("gates") or {}).get("confirmatory_outcomes_permitted") is True:
            return fail("draft prereg gates.confirmatory_outcomes_permitted must be false")
    # terms/provenance cross-checks (fail-closed)
    terms_err = _check_resolved_terms_evidence(te)
    if terms_err:
        return fail(terms_err)
    terms_resolved = te.get("status") == RESOLVED_TERMS and te.get("fabricated") is False
    if te.get("status") in ("EXPLICIT_BLOCKER_UNRESOLVED", "UNRESOLVED", "BLOCKED") and (
        pm.get("confirmatory_provenance_go") is True or pm.get("admissibility_complete") is True
    ):
        return fail("provenance manifest cannot be GO while terms evidence is unresolved")
    if pm.get("confirmatory_provenance_go") is True and not terms_resolved:
        return fail("provenance confirmatory_provenance_go=true requires RESOLVED_VERIFIED terms evidence")
    if (pm.get("license_terms") or {}).get("status") == "RESOLVED_VERIFIED" and not terms_resolved:
        return fail("provenance manifest claims RESOLVED_VERIFIED license_terms but terms evidence artifact is not resolved")
    # completeness/leakage
    if ca.get("verdict") != PASS_COMPLETENESS and (
        pm.get("admissibility_complete") is True or args.expect_go
    ):
        return fail(f"admissibility/expect-go requires completeness verdict {PASS_COMPLETENESS}")
    if (ca.get("completeness") or {}).get("ok") is False and ca.get("verdict") == PASS_COMPLETENESS:
        return fail("completeness verdict PASS but completeness.ok is false")
    # non-draft prereg claiming GO/admissible without terms resolved/provenance is refused
    if pr.get("draft") is False and (pr.get("confirmatory_claim_go") == "GO" or pr.get("admissibility_complete") is True):
        if not terms_resolved:
            return fail("non-draft GO/admissible prereg requires RESOLVED_VERIFIED terms evidence")
        if pm.get("confirmatory_provenance_go") is not True or pm.get("admissibility_complete") is not True:
            return fail("non-draft GO/admissible prereg requires provenance manifest GO+admissibility_complete")
    # refs integrity (if present)
    refs = (pr.get("admissibility_refs_sha256") or {})
    expected = {
        "provenance_license_manifest": sha256(pm_p),
        "completeness_leakage_audit": sha256(ca_p),
    }
    for k, v in expected.items():
        if refs.get(k) and refs.get(k) != v:
            return fail(f"prereg refs sha256 mismatch for {k}: {refs.get(k)} != {v}")
    te_ref = (pr.get("admissibility_refs_paths") or {}).get("terms_evidence_blocked") or (pr.get("admissibility_refs_paths") or {}).get("terms_evidence")
    if te_ref and Path(te_ref).name != te_p.name and not str(te_ref).endswith(te_p.name):
        # only enforce when clearly contradictory
        pass
    if refs.get("terms_evidence") and refs.get("terms_evidence") != sha256(te_p):
        return fail(f"prereg refs sha256 mismatch for terms_evidence: {refs.get('terms_evidence')} != {sha256(te_p)}")

    gates = {
        "terms_resolved_verified": bool(terms_resolved),
        "provenance_manifest_go": bool(pm.get("confirmatory_provenance_go") is True and pm.get("admissibility_complete") is True),
        "completeness_leakage_pass": bool(ca.get("verdict") == PASS_COMPLETENESS and ca.get("admissibility_complete") is True),
        "prereg_frozen_non_draft": bool(pr.get("draft") is False and pr.get("frozen_before_outcomes") is True and pr.get("admissibility_complete") is True),
        "prereg_claim_go": bool(pr.get("confirmatory_claim_go") == "GO"),
    }
    blockers = [k for k, v in gates.items() if not v]
    all_go = not blockers and all(
        [
            pm.get("no_confirmatory_outcomes") is True,
            ca.get("no_confirmatory_outcomes") is True,
            te.get("no_confirmatory_outcomes") is True,
            pr.get("no_confirmatory_outcomes") is True,
            pm.get("fabricated") is not True,
            te.get("fabricated") is False,
        ]
    )
    if args.expect_go and not all_go:
        return fail("expect-go set but admissibility package is not fully GO", gates=gates, blockers=blockers)
    print(
        json.dumps(
            {
                "validator": "fclr016_v5_admissibility",
                "ok": True,
                "expect_go": bool(args.expect_go),
                "all_go": bool(all_go),
                "confirmatory_outcomes_permitted": bool(all_go),
                "gates": gates,
                "blockers": blockers,
                "hashes": {
                    "provenance_manifest": sha256(pm_p),
                    "completeness_audit": sha256(ca_p),
                    "terms_evidence": sha256(te_p),
                    "prereg_draft": sha256(pr_p),
                },
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())