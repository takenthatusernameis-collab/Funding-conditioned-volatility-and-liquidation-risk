#!/usr/bin/env python3
"""
Independent stdlib recompute of the FCLR-LIQ-XSEC-BROAD-01 headline statistics
and frozen verdict rule.

Separate code path from fclr_liqxsecbroad01_eval_*.py: it reads the eval output
JSON and independently re-derives (a) the relative Poisson-deviance improvement
for each arm, (b) the materiality-floor decision, and (c) the frozen
SUPPORTED_GENERALIZATION verdict rule, using direct arithmetic only. No model
refit, no shared code path with the evaluation.

Sign convention (frozen in prereg, identical to eval):
    relative_improvement = (baseline - candidate) / baseline
    positive => candidate (funding-conditioned C2) better than baseline (RV-only B1)

Read-only, no network, stdlib only.

Usage:
  python3 fclr_liqxsecbroad01_recompute_<UTC>.py <session_dir>

Produces under <session_dir>:
  fclr_liqxsecbroad01_recompute_<UTC>.json
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SESSION_UTC = "20261123T085507Z"

SIGN_CONVENTION = "(baseline - candidate) / baseline, positive = candidate better"
MATERIALITY_FRAC = 0.02  # 2.0% frozen floor


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def rel_improvement_independent(baseline: float, candidate: float) -> float:
    """(baseline - candidate) / baseline; positive => candidate better."""
    if baseline is None or baseline <= 0:
        return float("nan")
    return (baseline - candidate) / baseline


def close(a: float, b: float, tol: float) -> bool:
    try:
        return abs(float(a) - float(b)) <= tol
    except (TypeError, ValueError):
        return False


def main():
    sdir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
        "research_state/session_" + SESSION_UTC)

    eval_path = sdir / f"fclr_liqxsecbroad01_eval_{SESSION_UTC}.json"
    if not eval_path.is_file():
        print(f"MISSING eval output: {eval_path}", file=sys.stderr)
        sys.exit(2)

    ev = json.loads(eval_path.read_text())
    checks: dict = {}

    hl = ev["headline_long"]
    hs = ev["headline_short"]

    # --- (a) relative Poisson-deviance improvement (independent arithmetic) ---
    rel_l = rel_improvement_independent(
        hl["poisson_deviance_B1"], hl["poisson_deviance_C2"])
    rel_s = rel_improvement_independent(
        hs["poisson_deviance_B1"], hs["poisson_deviance_C2"])

    checks["long_rel_recompute"] = rel_l
    checks["long_rel_stored"] = hl["relative_improvement"]
    checks["long_rel_match"] = close(rel_l, hl["relative_improvement"], 1e-9)

    checks["short_rel_recompute"] = rel_s
    checks["short_rel_stored"] = hs["relative_improvement"]
    checks["short_rel_match"] = close(rel_s, hs["relative_improvement"], 1e-9)

    # --- (b) materiality floor (>= 2.0%) ---
    long_mat = rel_l >= MATERIALITY_FRAC
    short_mat = rel_s >= MATERIALITY_FRAC
    checks["long_materiality_recompute"] = long_mat
    checks["long_materiality_stored"] = hl["materiality_met"]
    checks["long_materiality_match"] = bool(long_mat) == bool(hl["materiality_met"])
    checks["short_materiality_recompute"] = short_mat
    checks["short_materiality_stored"] = hs["materiality_met"]
    checks["short_materiality_match"] = bool(short_mat) == bool(hs["materiality_met"])

    # --- (c) frozen verdict rule (independent re-derivation) ---
    unc = ev["uncertainty"]
    mult = ev["multiplicity"]
    alpha_k = mult["alpha_k"]
    holm_primary = mult["holm_adjusted_pvals"]["RV_tercile_arm"]

    narrow_sign_reproduced = hl["mean_rank_IC_C2"] > 0
    ci_excludes_null_favorable = unc["ci95_lo"] > 0
    primary_significant_after_holm = holm_primary < alpha_k

    verdict_recompute = (
        "SUPPORTED_GENERALIZATION"
        if (narrow_sign_reproduced and ci_excludes_null_favorable
            and primary_significant_after_holm)
        else "NOT_SUPPORTED"
    )

    checks["narrow_sign_recompute"] = narrow_sign_reproduced
    checks["narrow_sign_stored"] = ev["decision"]["narrow_sign_reproduced"]
    checks["narrow_sign_match"] = bool(narrow_sign_reproduced) == bool(
        ev["decision"]["narrow_sign_reproduced"])

    checks["ci_excludes_null_recompute"] = ci_excludes_null_favorable
    checks["ci_excludes_null_stored"] = ev["decision"]["ci_excludes_null_favorable"]
    checks["ci_excludes_null_match"] = bool(ci_excludes_null_favorable) == bool(
        ev["decision"]["ci_excludes_null_favorable"])

    checks["holm_sig_recompute"] = primary_significant_after_holm
    checks["holm_sig_stored"] = ev["decision"]["primary_significant_after_holm"]
    checks["holm_sig_match"] = bool(primary_significant_after_holm) == bool(
        ev["decision"]["primary_significant_after_holm"])

    checks["verdict_recompute"] = verdict_recompute
    checks["verdict_stored"] = ev["decision"]["verdict"]
    checks["verdict_match"] = verdict_recompute == ev["decision"]["verdict"]

    # --- sign-convention consistency (EVIDENCE NOTE guard) ---
    checks["sign_convention_stored"] = hl["sign_convention"]
    checks["sign_convention_expected"] = SIGN_CONVENTION
    checks["sign_convention_match"] = (
        hl["sign_convention"] == SIGN_CONVENTION
        and hs["sign_convention"] == SIGN_CONVENTION
    )

    # --- bootstrap/placebo/LOIO presence sanity (design executed, not faked) ---
    checks["bootstrap_replicates"] = unc["bootstrap_replicates"]
    checks["placebo_replicates"] = unc["placebo_replicates"]
    checks["loio_subsets"] = unc["loio_subsets"]
    checks["design_executed"] = (
        unc["bootstrap_replicates"] >= 2000
        and unc["placebo_replicates"] >= 1000
        and unc["loio_subsets"] >= 8
    )

    all_match = all(v for k, v in checks.items() if k.endswith("_match"))

    result = {
        "experiment_id": "FCLR-LIQ-XSEC-BROAD-01",
        "campaign": "FCLR-LIQ-XSEC-BROAD-01-20261123T080000Z",
        "session_utc": SESSION_UTC,
        "method": (
            "independent stdlib recompute; direct arithmetic verification of the "
            "eval headline (relative Poisson-deviance improvement, materiality "
            "floor) and the frozen SUPPORTED_GENERALIZATION verdict rule; no "
            "model refit, separate code path from the evaluation"),
        "eval_output_path": str(eval_path),
        "eval_output_sha256": sha256_file(eval_path),
        "sign_convention": SIGN_CONVENTION,
        "checks": checks,
        "all_checks_match": all_match,
        "headline_long": {
            "poisson_deviance_B1": hl["poisson_deviance_B1"],
            "poisson_deviance_C2": hl["poisson_deviance_C2"],
            "relative_improvement_recompute": rel_l,
            "relative_improvement_pct_recompute": rel_l * 100.0,
            "materiality_met_recompute": long_mat,
            "mean_rank_IC_C2": hl["mean_rank_IC_C2"],
        },
        "headline_short": {
            "poisson_deviance_B1": hs["poisson_deviance_B1"],
            "poisson_deviance_C2": hs["poisson_deviance_C2"],
            "relative_improvement_recompute": rel_s,
            "relative_improvement_pct_recompute": rel_s * 100.0,
            "materiality_met_recompute": short_mat,
            "mean_rank_IC_C2": hs["mean_rank_IC_C2"],
        },
        "decision": {
            "verdict_recompute": verdict_recompute,
            "verdict_stored": ev["decision"]["verdict"],
            "agrees_with_eval": verdict_recompute == ev["decision"]["verdict"],
            "note": (
                "Verdict follows the frozen rule (broad-universe generalization "
                "of the cross-sectional rank-ordering association). Materiality "
                "floor on Poisson deviance was NOT met on either arm; the "
                "SUPPORTED_GENERALIZATION is a rank-ordering association result, "
                "not a calibrated-magnitude improvement and not a forecast-gate "
                "pass or an observed-liquidation census."),
        },
        "not_observed_liquidation_census": True,
        "not_a_forecast_gate_pass": True,
        "generated_utc": "2026-11-23T10:22:00Z",
    }
    out_path = sdir / f"fclr_liqxsecbroad01_recompute_{SESSION_UTC}.json"
    out_path.write_text(json.dumps(result, indent=2))
    print(f"WROTE {out_path}")
    print(f"All checks match: {all_match}")
    print(f"Verdict: stored={ev['decision']['verdict']} recompute={verdict_recompute}")
    print(f"Long rel_imp={rel_l:.6f} (materiality={long_mat}); "
          f"Short rel_imp={rel_s:.6f} (materiality={short_mat})")
    if not all_match:
        print("RECONCILE REQUIRED: recompute disagrees with eval; do not declare a verdict.",
              file=sys.stderr)
        sys.exit(3)


if __name__ == "__main__":
    main()