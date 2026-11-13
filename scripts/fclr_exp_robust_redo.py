#!/usr/bin/env python3
"""FCLR-EXP-ROBUST-REDO — Track A expansion robustness redo (P2).

Frozen prereg: research_state/prereg_fclr_exp_robust_redo_20261113T063000Z.{json,md}

Re-runs the pre-registered LOIO / placebo / bootstrap-setting checks on the sealed
expansion panel with a higher-resolution placebo (2000 permutations vs the prior
1000) and a fixed seed. The sealed panel, splits, features, and materiality floor
are unchanged. The prior FRAGILE 19.04% verdict is NOT re-scored; this cell issues
an independent ROBUST / FRAGILE / INCONCLUSIVE verdict.

No network. No mutation of the sealed panel or prior verdict.

Usage:
  python3 scripts/fclr_exp_robust_redo.py
  python3 scripts/fclr_exp_robust_redo.py --smoke
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[1]
RS = REPO / "research_state"
PREREG = RS / "prereg_fclr_exp_robust_redo_20261113T063000Z.json"

# Reuse the verified panel machinery (panel schema, OLS, bootstrap, LOIO).
import sys
if str(REPO / "scripts") not in sys.path:
    sys.path.insert(0, str(REPO / "scripts"))
import run_expansion_robustness as base  # noqa: E402


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def convert(obj):
    if isinstance(obj, (np.bool_, np.integer, np.floating)):
        return obj.item()
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, dict):
        return {k: convert(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [convert(v) for v in obj]
    if isinstance(obj, tuple):
        return tuple(convert(v) for v in obj)
    if isinstance(obj, float) and pd.isna(obj):
        return None
    return obj


def placebo(panel: pd.DataFrame, perms: int, seed: int) -> dict:
    true = base.run_c2_vs_b1_eval(panel, base.N_BOOT, base.SEED_BOOTSTRAP)
    true_rel = true["rel_reduction_pct"]
    rng = np.random.default_rng(seed)
    null = []
    for i in range(perms):
        pp = panel.copy()
        for sym in base.SYMBOLS:
            idx = pp.index[pp["coin"] == sym]
            if not len(idx):
                continue
            for col in ("fundingRate", "abs_fund_pct"):
                pp.loc[idx, col] = rng.permutation(pp.loc[idx, col].values)
        pp = base.build_features(pp)
        res = base.run_c2_vs_b1_eval(pp, base.N_BOOT, seed + i)
        if res["rel_reduction_pct"] is not None:
            null.append(float(res["rel_reduction_pct"]))
    null = np.array(null)
    p95 = float(np.percentile(null, 95)) if len(null) else None
    return {
        "check": "PLACEBO_PERMUTATION",
        "true_rel_reduction_pct": true_rel,
        "n_perm": int(len(null)),
        "null_p95": p95,
        "null_mean": float(null.mean()) if len(null) else None,
        "null_std": float(null.std()) if len(null) else None,
        "p_value_approx": float((null >= true_rel).mean()) if len(null) else None,
        "overall_pass": bool(p95 is not None and true_rel > p95),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--out-utc", default=None)
    args = ap.parse_args()

    prereg = json.loads(PREREG.read_text())
    assert prereg["status"] == "FROZEN_PRE_OUTCOMES"
    assert prereg["outcome_data_inspected_before_freeze"] is False

    out_utc = args.out_utc or now_utc()
    safe = out_utc.replace(":", "").replace("-", "")

    panel_path = RS / "tracka_hl_expansion_panel_20261111T202344Z.parquet"
    actual_sha = sha256_file(panel_path)
    expected_sha = prereg["sealed_reference"]["panel_sha256"]
    assert actual_sha == expected_sha, f"panel sha mismatch: {actual_sha} != {expected_sha}"

    panel = base.load_and_prepare_panel()
    perms = 20 if args.smoke else prereg["gates"]["placebo_permutations"]
    loio = base.run_loio_check(panel)
    plac = placebo(panel, perms, prereg["gates"]["placebo_seed"])
    boot = base.run_bootstrap_settings_check(panel)

    # Full-panel primary contrast (C2 vs B1): materiality + CI-excludes-zero,
    # the two remaining pre-registered gates beyond LOIO / placebo / bootstrap.
    full = base.run_c2_vs_b1_eval(panel, base.N_BOOT, base.SEED_BOOTSTRAP)
    checks = {
        "loio_ge_6_of_8": bool(loio["overall_pass"]),
        "placebo_pass": bool(plac["overall_pass"]),
        "bootstrap_settings_pass": bool(boot["overall_pass"]),
        "materiality_ge_2pct": bool(full["passes_materiality"]),
        "ci_excludes_zero": bool(full["ci_excludes_zero"]),
    }
    if args.smoke:
        verdict = "SMOKE"
    elif not (panel["split"] == "test").any():
        verdict = "INCONCLUSIVE"
    elif all(checks.values()):
        verdict = "ROBUST"
    else:
        verdict = "FRAGILE"

    payload = {
        "experiment_id": prereg["experiment_id"],
        "campaign": prereg["campaign"],
        "cell": prereg["cell"],
        "generated_utc": out_utc,
        "prereg": PREREG.name,
        "verdict": verdict,
        "checks": checks,
        "panel": panel_path.name,
        "panel_sha256": actual_sha,
        "placebo": plac,
        "loio": {
            "pass_count": loio["pass_count"],
            "total": loio["total"],
            "threshold": loio["threshold"],
            "overall_pass": loio["overall_pass"],
            "per_instrument": loio["per_instrument"],
        },
        "bootstrap_settings": boot,
        "full_panel_contrast": full,
        "prior_sealed_verdict": prereg["sealed_reference"]["prior_verdict"],
        "n_rows": int(len(panel)),
    }

    if args.smoke:
        print(json.dumps(convert(payload), indent=1))
        return

    (RS / f"evaluation_summary_FCLR-EXP-ROBUST-REDO-{safe}.json").write_text(
        json.dumps(convert(payload), indent=1))
    md = [
        f"# Evaluation Summary — {prereg['experiment_id']}", "",
        f"Generated: {out_utc}", f"Verdict: **{verdict}**", "",
        f"Panel: {panel_path.name} (sha256 {actual_sha[:16]}...)", "",
        "## Checks", "",
        f"- loio_ge_6_of_8: {checks['loio_ge_6_of_8']} ({loio['pass_count']}/{loio['total']})",
        f"- placebo_pass: {checks['placebo_pass']} (null p95 {plac['null_p95']}, true {plac['true_rel_reduction_pct']})",
        f"- bootstrap_settings_pass: {checks['bootstrap_settings_pass']}", "",
        "## Placebo (funding permutation)", "",
        f"- true rel reduction: {plac['true_rel_reduction_pct']:.2f}%",
        f"- null p95: {plac['null_p95']:.4f}% (n={plac['n_perm']})",
        f"- p-value approx: {plac['p_value_approx']}", "",
        "## LOIO", "",
    ]
    for sym, res in loio["per_instrument"].items():
        md.append(f"- {sym}: rel {res['rel_reduction_pct']:.2f}%, CI [{res['ci_lo']:.6f}, {res['ci_hi']:.6f}], "
                  f"mat={res['passes_materiality']}, ci={res['ci_excludes_zero']}")
    md += ["", "## Note", "",
           "The prior sealed 19.04% PASS (LOIO 4/8, placebo null p95 21.10%) is FRAGILE and is "
           "not re-scored here. This cell only tests whether the pre-registered design changes "
           "the verdict.", ""]
    (RS / f"evaluation_summary_FCLR-EXP-ROBUST-REDO-{safe}.md").write_text("\n".join(md))
    print(json.dumps({"verdict": verdict, "checks": checks,
                      "loio": f"{loio['pass_count']}/{loio['total']}",
                      "placebo_pass": plac["overall_pass"],
                      "eval": f"evaluation_summary_FCLR-EXP-ROBUST-REDO-{safe}.json"}, indent=1))


if __name__ == "__main__":
    main()