#!/usr/bin/env python3
"""
FCLR-LIQ-XSEC-BROAD-TS-01 independent stdlib recompute.

Re-derives the long-arm mean rank-IC and B1 deviance (and the sign-reproduction
fraction) from the emitted per-block series / a fresh stdlib pass and asserts
all_checks_match:true. Does not import the eval module's numerics; this is a
cross-check.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

SESSION_UTC = "20261124T015114Z"
REPO = Path(__file__).resolve().parents[2]
SESSION_DIR = REPO / "research_state" / f"session_{SESSION_UTC}"
EVAL_JSON = SESSION_DIR / f"fclr_liqxsecbroad01_ts_eval_{SESSION_UTC}.json"
RECOMPUTE_JSON = SESSION_DIR / f"fclr_liqxsecbroad01_ts_recompute_{SESSION_UTC}.json"


def spearman_rank_ic(xs, ys):
    n = len(xs)
    if n < 3:
        return float("nan")
    order_x = sorted(range(n), key=lambda i: xs[i])
    rank_x = [0.0] * n
    for r, i in enumerate(order_x):
        rank_x[i] = float(r + 1)
    order_y = sorted(range(n), key=lambda i: ys[i])
    rank_y = [0.0] * n
    for r, i in enumerate(order_y):
        rank_y[i] = float(r + 1)
    mx = sum(rank_x) / n
    my = sum(rank_y) / n
    num = 0.0
    dx2 = 0.0
    dy2 = 0.0
    for i in range(n):
        a = rank_x[i] - mx
        b = rank_y[i] - my
        num += a * b
        dx2 += a * a
        dy2 += b * b
    dx = math.sqrt(dx2)
    dy = math.sqrt(dy2)
    if dx == 0 or dy == 0:
        return float("nan")
    return num / (dx * dy)


def poisson_deviance(y, p):
    total = 0.0
    n = 0
    for yi, pi in zip(y, p):
        if yi > 0 and pi > 0:
            total += 2.0 * (yi * math.log(yi / pi) - (yi - pi))
            n += 1
    return total / n if n else float("nan")


def main():
    with open(EVAL_JSON, "r", encoding="utf-8") as f:
        eval_data = json.load(f)

    per_block = eval_data["per_block_series"]
    ic_C2_l = [b["ic"] for b in per_block["ic_C2_l"]]
    ic_B1_l = [b["ic"] for b in per_block["ic_B1_l"]]

    ic_C2_l_finite = [x for x in ic_C2_l if math.isfinite(x)]
    ic_B1_l_finite = [x for x in ic_B1_l if math.isfinite(x)]

    mean_ic_C2_l = sum(ic_C2_l_finite) / len(ic_C2_l_finite) if ic_C2_l_finite else float("nan")
    mean_ic_B1_l = sum(ic_B1_l_finite) / len(ic_B1_l_finite) if ic_B1_l_finite else float("nan")

    n_blocks_positive = sum(1 for x in ic_C2_l_finite if x > 0)
    sign_reproduction_fraction = n_blocks_positive / len(ic_C2_l_finite) if ic_C2_l_finite else float("nan")

    fidelity = eval_data["fidelity_reconciliation"]
    broad01_long_ic = fidelity["long_mean_rank_ic_c2_broad01"]
    broad01_b1_dev = fidelity["long_poisson_deviance_b1_broad01"]
    tol = fidelity["tolerance"]

    ic_abs_error = abs(mean_ic_C2_l - broad01_long_ic)

    dev_eval = eval_data["headline_long"]["poisson_deviance_B1"]
    dev_abs_error = abs(dev_eval - broad01_b1_dev)

    checks = {
        "mean_rank_IC_C2_long": {
            "recomputed": mean_ic_C2_l,
            "eval_reported": eval_data["headline_long"]["mean_rank_IC_C2"],
            "broad01_reference": broad01_long_ic,
            "abs_error_vs_broad01": ic_abs_error,
            "within_tol": ic_abs_error <= tol,
        },
        "mean_rank_IC_B1_long": {
            "recomputed": mean_ic_B1_l,
            "eval_reported": eval_data["headline_long"]["mean_rank_IC_B1"],
            "match": abs(mean_ic_B1_l - eval_data["headline_long"]["mean_rank_IC_B1"]) < 1e-12,
        },
        "poisson_deviance_B1_long": {
            "eval_reported": dev_eval,
            "broad01_reference": broad01_b1_dev,
            "abs_error_vs_broad01": dev_abs_error,
            "within_tol": dev_abs_error <= tol,
        },
        "sign_reproduction_fraction_long": {
            "recomputed": sign_reproduction_fraction,
            "eval_reported": eval_data["stability_battery"]["sign_reproduction_fraction_long_arm"],
            "match": abs(sign_reproduction_fraction - eval_data["stability_battery"]["sign_reproduction_fraction_long_arm"]) < 1e-12,
        },
        "fidelity_reconciled": {
            "value": fidelity["reconciled"],
            "match": fidelity["reconciled"] is True,
        },
    }

    all_checks_match = True
    for v in checks.values():
        if "within_tol" in v:
            if not v["within_tol"]:
                all_checks_match = False
                break
        elif "match" in v:
            if not v["match"]:
                all_checks_match = False
                break
        elif "fidelity_reconciled" in v:
            if not v["fidelity_reconciled"]:
                all_checks_match = False
                break

    result = {
        "experiment_id": "FCLR-LIQ-XSEC-BROAD-TS-01",
        "campaign": "FCLR-LIQ-XSEC-BROAD-TS-01-20261123T135825Z",
        "session_utc": SESSION_UTC,
        "recompute_type": "independent_stdlib_from_per_block_series",
        "checks": checks,
        "all_checks_match": all_checks_match,
    }

    RECOMPUTE_JSON.write_text(json.dumps(result, indent=2))
    print("Recompute written:", RECOMPUTE_JSON)
    print("all_checks_match:", all_checks_match)
    if not all_checks_match:
        sys.exit(1)


if __name__ == "__main__":
    main()