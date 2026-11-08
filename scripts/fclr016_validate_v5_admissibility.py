#!/usr/bin/env python3
"""Deterministic, read-only Gate 4 v5 admissibility validator (NO outcomes, NO network).

Checks provenance/license manifest, completeness/leakage audit, terms evidence, and prereg draft
for internal consistency and fail-closed confirmatory readiness. Exits 0 only when a caller
explicitly requests --expect-go and all gates pass (not the case for current artifacts).
"""
from __future__ import annotations
import argparse, hashlib, json, sys
from pathlib import Path

def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def load(p: Path):
    return json.loads(p.read_text())

def fail(msg):
    print(json.dumps({"validator":"fclr016_v5_admissibility","ok":False,"error":msg}, indent=2))
    return 2

def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--provenance-manifest", required=True)
    ap.add_argument("--completeness-audit", required=True)
    ap.add_argument("--terms-evidence", required=True)
    ap.add_argument("--prereg-draft", required=True)
    ap.add_argument("--expect-go", action="store_true", help="Require full confirmatory GO; otherwise just validate schema/blocker consistency")
    args = ap.parse_args(argv)
    pm_p, ca_p, te_p, pr_p = map(Path, [args.provenance_manifest, args.completeness_audit, args.terms_evidence, args.prereg_draft])
    for p in (pm_p, ca_p, te_p, pr_p):
        if not p.exists():
            return fail(f"missing: {p}")
    pm, ca, te, pr = load(pm_p), load(ca_p), load(te_p), load(pr_p)

    # hard invariants for admissibility artifacts
    for name, d in [("provenance",pm),("completeness",ca),("terms",te),("prereg",pr)]:
        if d.get("no_confirmatory_outcomes") is not True:
            return fail(f"{name}.no_confirmatory_outcomes must be true")
        if d.get("fabricated") is True:
            return fail(f"{name}.fabricated must not be true")
    # scope alignment
    scope = pm.get("frozen_scope") or {}
    for name,d in [("completeness",ca),("prereg",pr)]:
        if (d.get("frozen_scope") or {}).get("window") != scope.get("window"):
            return fail(f"{name} scope window mismatch vs provenance manifest")
    # prereg must remain draft/NO_GO while blockers exist
    if pr.get("draft") is True:
        for k in ("frozen_before_outcomes","promotable_to_frozen","admissibility_complete","license_terms_resolved"):
            if pr.get(k) is True:
                return fail(f"draft prereg cannot set {k}=true")
        if pr.get("confirmatory_claim_go") != "NO_GO":
            return fail("draft prereg must keep confirmatory_claim_go=NO_GO")
    # terms blocker consistency
    if te.get("status") in ("EXPLICIT_BLOCKER_UNRESOLVED",) and (pm.get("confirmatory_provenance_go") is True or pm.get("admissibility_complete") is True):
        return fail("provenance manifest cannot be GO while terms evidence is unresolved")
    # refs integrity (if present)
    refs = (pr.get("admissibility_refs_sha256") or {})
    expected = {
        "provenance_license_manifest": sha256(pm_p),
        "completeness_leakage_audit": sha256(ca_p),
    }
    for k,v in expected.items():
        if refs.get(k) and refs.get(k) != v:
            return fail(f"prereg refs sha256 mismatch for {k}: {refs.get(k)} != {v}")

    all_go = (
        pm.get("confirmatory_provenance_go") is True and pm.get("admissibility_complete") is True and
        ca.get("verdict") == "PASS_COMPLETENESS_LEAKAGE_DETERMINISTIC" and ca.get("admissibility_complete") is True and
        te.get("status") == "RESOLVED_VERIFIED" and te.get("fabricated") is False and
        pr.get("draft") is False and pr.get("frozen_before_outcomes") is True and pr.get("admissibility_complete") is True and
        pr.get("confirmatory_claim_go") == "GO"
    )
    if args.expect_go and not all_go:
        return fail("expect-go set but admissibility package is not fully GO")
    print(json.dumps({
        "validator":"fclr016_v5_admissibility","ok":True,"expect_go":bool(args.expect_go),"all_go":bool(all_go),
        "confirmatory_outcomes_permitted":bool(all_go),
        "blockers": [] if all_go else ["terms unresolved or draft prereg or manifest not GO (by design)"],
        "hashes":{"provenance_manifest":sha256(pm_p),"completeness_audit":sha256(ca_p),"terms_evidence":sha256(te_p),"prereg_draft":sha256(pr_p)}
    }, indent=2, sort_keys=True))
    return 0

if __name__ == "__main__":
    sys.exit(main())
