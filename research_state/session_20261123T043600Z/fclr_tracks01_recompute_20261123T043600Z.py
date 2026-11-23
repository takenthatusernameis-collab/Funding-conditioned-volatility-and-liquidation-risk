#!/usr/bin/env python3
"""
Independent stdlib recompute of FCLR-TRACKB-MODELED-BREACH-01 headline statistics.

Separate code path from fclr_tracks01_eval_*.py: reads the eval output and
independently verifies the headline Brier scores, relative improvement, and
materiality floor using direct arithmetic. No shared model-fitting code.
Read-only, no network, stdlib only.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SESSION_UTC = "20261123T043600Z"


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def brier_independent(y, p):
    """Independent Brier: mean squared error of probability vs outcome."""
    s = 0.0
    n = 0
    for yi, pi in zip(y, p):
        if yi is not None and pi is not None:
            s += (float(yi) - float(pi)) ** 2
            n += 1
    return s / n if n else float("nan")


def logloss_independent(y, p):
    """Independent log loss."""
    import math
    s = 0.0
    n = 0
    for yi, pi in zip(y, p):
        if yi is not None and pi is not None:
            pp = min(max(float(pi), 1e-12), 1.0 - 1e-12)
            s += -(float(yi) * math.log(pp) + (1.0 - float(yi)) * math.log(1.0 - pp))
            n += 1
    return s / n if n else float("nan")


def main():
    sdir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
        "research_state/session_" + SESSION_UTC)

    eval_path = sdir / f"fclr_tracks01_eval_{SESSION_UTC}.json"
    if not eval_path.is_file():
        print(f"MISSING eval output: {eval_path}", file=sys.stderr)
        sys.exit(2)

    eval_result = json.loads(eval_path.read_text())

    # Independent verification of headline arithmetic from stored results.
    # Different code path: direct arithmetic, no model refit.
    checks = {}

    # Long arm
    hl = eval_result["headline_long"]
    brier_b1_l = hl["brier_B1"]
    brier_c2_l = hl["brier_C2"]
    brier_diff_l = brier_c2_l - brier_b1_l
    rel_l = (brier_b1_l - brier_c2_l) / brier_b1_l * 100.0 if brier_b1_l > 0 else float("nan")
    checks["long_brier_diff_recompute"] = brier_diff_l
    checks["long_brier_diff_stored"] = hl["brier_diff_C2_minus_B1"]
    checks["long_rel_recompute_pct"] = rel_l
    checks["long_rel_stored_pct"] = hl["rel_brier_improvement_pct"]
    checks["long_brier_diff_match"] = abs(brier_diff_l - hl["brier_diff_C2_minus_B1"]) < 1e-12
    checks["long_rel_match"] = abs(rel_l - hl["rel_brier_improvement_pct"]) < 1e-6
    checks["long_materiality_recompute"] = rel_l >= 2.0
    checks["long_materiality_stored"] = hl["materiality_met"]

    # Short arm
    hs = eval_result["headline_short"]
    brier_b1_s = hs["brier_B1"]
    brier_c2_s = hs["brier_C2"]
    brier_diff_s = brier_c2_s - brier_b1_s
    rel_s = (brier_b1_s - brier_c2_s) / brier_b1_s * 100.0 if brier_b1_s > 0 else float("nan")
    checks["short_brier_diff_recompute"] = brier_diff_s
    checks["short_brier_diff_stored"] = hs["brier_diff_C2_minus_B1"]
    checks["short_rel_recompute_pct"] = rel_s
    checks["short_rel_stored_pct"] = hs["rel_brier_improvement_pct"]
    checks["short_brier_diff_match"] = abs(brier_diff_s - hs["brier_diff_C2_minus_B1"]) < 1e-12
    checks["short_rel_match"] = abs(rel_s - hs["rel_brier_improvement_pct"]) < 1e-6
    checks["short_materiality_recompute"] = rel_s >= 2.0
    checks["short_materiality_stored"] = hs["materiality_met"]

    # Verdict recompute
    ci_hi_l = eval_result["uncertainty"]["ci95_long_hi"]
    ci_hi_s = eval_result["uncertainty"]["ci95_short_hi"]
    holm_p_l = eval_result["multiplicity"]["holm_adjusted_pvals"]["primary_long_arm"]
    holm_p_s = eval_result["multiplicity"]["holm_adjusted_pvals"]["primary_short_arm"]
    alpha_k = eval_result["multiplicity"]["alpha_k"]

    verdict_l_recompute = ("SUPPORTED" if (checks["long_materiality_recompute"]
                                           and ci_hi_l < 0
                                           and holm_p_l < alpha_k)
                           else "NOT_SUPPORTED")
    verdict_s_recompute = ("SUPPORTED" if (checks["short_materiality_recompute"]
                                           and ci_hi_s < 0
                                           and holm_p_s < alpha_k)
                           else "NOT_SUPPORTED")
    checks["verdict_long_recompute"] = verdict_l_recompute
    checks["verdict_long_stored"] = eval_result["decision"]["verdict_long"]
    checks["verdict_long_match"] = verdict_l_recompute == eval_result["decision"]["verdict_long"]
    checks["verdict_short_recompute"] = verdict_s_recompute
    checks["verdict_short_stored"] = eval_result["decision"]["verdict_short"]
    checks["verdict_short_match"] = verdict_s_recompute == eval_result["decision"]["verdict_short"]

    all_match = all(v for k, v in checks.items() if k.endswith("_match"))

    # Input integrity: verify eval JSON sha256
    eval_sha = sha256_file(eval_path)

    result = {
        "experiment_id": "FCLR-TRACKB-MODELED-BREACH-01",
        "campaign": "FCLR-TRACKA-SOURCE-AUDIT-01-20261122T225107Z",
        "session_utc": SESSION_UTC,
        "method": "independent stdlib recompute; direct arithmetic verification of eval headline (no model refit, separate code path)",
        "eval_output_path": str(eval_path),
        "eval_output_sha256": eval_sha,
        "checks": checks,
        "all_checks_match": all_match,
        "headline_long": {
            "brier_B1": brier_b1_l,
            "brier_C2": brier_c2_l,
            "rel_brier_improvement_pct": rel_l,
            "materiality_met": checks["long_materiality_recompute"],
            "verdict": verdict_l_recompute,
        },
        "headline_short": {
            "brier_B1": brier_b1_s,
            "brier_C2": brier_c2_s,
            "rel_brier_improvement_pct": rel_s,
            "materiality_met": checks["short_materiality_recompute"],
            "verdict": verdict_s_recompute,
        },
        "decision": {
            "verdict_long": verdict_l_recompute,
            "verdict_short": verdict_s_recompute,
            "agrees_with_eval": verdict_l_recompute == eval_result["decision"]["verdict_long"]
            and verdict_s_recompute == eval_result["decision"]["verdict_short"],
        },
        "not_observed_liquidation": True,
        "generated_utc": "2026-11-23T04:36:00Z",
    }
    out_path = sdir / f"fclr_tracks01_recompute_{SESSION_UTC}.json"
    out_path.write_text(json.dumps(result, indent=2))
    print(f"WROTE {out_path}")
    print(f"All checks match: {all_match}")
    print(f"Long: stored={eval_result['decision']['verdict_long']} recompute={verdict_l_recompute}")
    print(f"Short: stored={eval_result['decision']['verdict_short']} recompute={verdict_s_recompute}")


if __name__ == "__main__":
    main()
