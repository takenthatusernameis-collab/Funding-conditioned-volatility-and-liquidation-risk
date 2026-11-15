#!/usr/bin/env python3
"""FCLR-NEXT-002: design-power and MDE calibration for concluded nulls.

Deterministic, offline, read-only over persisted design quantities. No model
re-fit, no sealed-contrast recomputation, no network, no mutation of sealed
artifacts.

Reads frozen prereg/evaluation artifacts for the 2025 disjoint volatility
forward cross and the 2026Q1Q2 observed-liquidation cross-section and derives
analytic standard errors, MDE_80, and achieved power at pre-specified floors.

Outputs (EXPLORATORY_ONLY, promotable=false):
  research_state/evaluation_summary_FCLR-POWER-CALIBRATION-<UTC>.json
  research_state/evaluation_summary_FCLR-POWER-CALIBRATION-<UTC>.md
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

REPO = Path(__file__).resolve().parents[1]
RS = REPO / "research_state"
DEFAULT_UTC = "2026-11-15T01:34:12Z"
PREREG_NAME = f"prereg_fclr_power_calibration_{DEFAULT_UTC}.json"

Z_975 = 1.959963984540054
Z_80 = 0.8416212335729143
Z_95 = 1.6448536269514722
MDE80_FACTOR = Z_975 + Z_80  # 2.8015852181129683

VOL_EVAL = RS / "evaluation_summary_FCLR-FWD-VOL-2025-DISJOINT-CORRECTED-AUDIT-2026-11-15T00:12:56Z.json"
VOL_PREREG = RS / "prereg_fclr_fwd_vol_2025_disjoint_cross_20261114T183000Z.json"
VOL_PANEL = RS / "tracka_fwd_vol_2025_disjoint_cross_panel_20261114T191615Z.parquet"
LIQ_EVAL = RS / "evaluation_summary_TRACKA-LIQ-XSEC-FORWARD-2026-11-13T22:31:55Z.json"
LIQ_PREREG = RS / "prereg_tracka_liq_xsec_forward_2026q1q2_20261113T222859Z.json"
LIQ_PANEL = RS / "tracka_liq_xsec_forward_panel_2026-11-13T22:31:55Z.parquet"

SEALED_EVALS = {
    RS / "evaluation_summary_FCLR-FWD-VOL-2025-DISJOINT-CROSS-20261114T191615Z.json",
    RS / "evaluation_summary_FCLR-FWD-VOL-2025-DISJOINT-RECONCILE-20261114T193000Z.json",
    RS / "evaluation_summary_FCLR-FWD-VOL-2024-DISJOINT-2024-06-20261114T231100Z_20261114T231545Z.json",
    VOL_EVAL,
    LIQ_EVAL,
}
SEALED_PREREGS = {VOL_PREREG, LIQ_PREREG}


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_json(p: Path) -> dict:
    return json.loads(p.read_text())


def phi(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def power_two_sided(delta_abs: float, se: float, alpha: float = 0.05) -> float:
    if se <= 0 or not math.isfinite(se):
        return float("nan")
    z = Z_975 if abs(alpha - 0.05) < 1e-12 else 1.959963984540054
    lam = abs(delta_abs) / se
    return phi(lam - z) + phi(-lam - z)


def analytic_se_from_ci(ci_lo: float, ci_hi: float, z: float = Z_975) -> float:
    return (ci_hi - ci_lo) / (2.0 * z)


def verdict_from_power(power: Optional[float]) -> str:
    if power is None or not math.isfinite(power):
        return "INCONCLUSIVE"
    return "NULL_INFORMATIVE" if power >= 0.80 else "NULL_UNDERPOWERED"


def vol_floor_abs(mean_diff: float, rel_reduction_pct: float, floor_rel: float = 0.02) -> Optional[float]:
    # improvement is negative QLIKE change; floor is 2% of implied baseline
    if not math.isfinite(mean_diff) or not math.isfinite(rel_reduction_pct):
        return None
    if abs(rel_reduction_pct) < 1e-12:
        return None
    baseline = abs(mean_diff) / (abs(rel_reduction_pct) / 100.0)
    if not math.isfinite(baseline) or baseline <= 0:
        return None
    return floor_rel * baseline


def analyze_vol(eval_json: dict) -> dict:
    contrasts = eval_json["cell"]["contrasts"]
    rows = {}
    for key, c in contrasts.items():
        se = analytic_se_from_ci(float(c["ci_lo"]), float(c["ci_hi"]))
        mde80 = MDE80_FACTOR * se
        floor_abs = vol_floor_abs(float(c["mean_diff"]), float(c["rel_reduction_pct"]), 0.02)
        power = power_two_sided(floor_abs, se) if floor_abs is not None else float("nan")
        rows[key] = {
            "n": c.get("n"),
            "n_days": c.get("n_days"),
            "mean_diff": c["mean_diff"],
            "ci_lo": c["ci_lo"],
            "ci_hi": c["ci_hi"],
            "rel_reduction_pct": c["rel_reduction_pct"],
            "se_analytic": se,
            "mde80_abs_qlike": mde80,
            "floor_rel_pct": 2.0,
            "floor_abs_qlike": floor_abs,
            "achieved_power_at_floor": power,
            "verdict": verdict_from_power(power),
        }
    primary = rows["h24_C2_vs_B1"]
    # per-horizon summary for primary contrast family C2_vs_B1
    per_horizon = {h: rows[f"{h}_C2_vs_B1"] for h in ("h6", "h24", "h72", "h168")}
    pooled_primary_verdict = primary["verdict"]
    return {
        "track": "volatility_forward_2025_disjoint",
        "primary_key": "h24_C2_vs_B1",
        "primary": primary,
        "per_horizon_C2_vs_B1": per_horizon,
        "all_contrasts": rows,
        "track_verdict": pooled_primary_verdict,
        "track_verdict_rule": "based on primary h24 C2_vs_B1 achieved power at 2% implied-baseline QLIKE floor",
    }


def analyze_liq(eval_json: dict) -> dict:
    primary = eval_json["primary"]
    q5 = float(primary["null_5th"])
    q95 = float(primary["null_95th"])
    width = q95 - q5
    mid = (q5 + q95) / 2.0
    symmetry_abs_frac = abs(mid) / width if width else float("inf")
    symmetry_pass = symmetry_abs_frac <= 0.01
    se_pooled = width / (2.0 * Z_95)
    floor_ic = float(eval_json.get("materiality", {}).get("floor_ic", 0.05))
    mde80 = MDE80_FACTOR * se_pooled
    power_pooled = power_two_sided(floor_ic, se_pooled)
    pooled_n = int(primary["pooled_n"])
    per_block_out = {}
    per_block_ics = []
    for blk, info in primary["per_block"].items():
        n = int(info["n"])
        se_blk = se_pooled * math.sqrt(pooled_n / n) if n > 0 else float("nan")
        per_block_out[blk] = {
            "ic": info["ic"],
            "n": n,
            "n_pairs": info.get("n_pairs"),
            "se_analytic_pooled_null_scaled": se_blk,
            "se_method": "approximation: pooled-null SE scaled by sqrt(pooled_n/block_n); per-block null quantiles not persisted",
            "mde80_abs_ic": MDE80_FACTOR * se_blk if math.isfinite(se_blk) else None,
            "achieved_power_at_floor": power_two_sided(floor_ic, se_blk) if math.isfinite(se_blk) else None,
            "verdict": verdict_from_power(power_two_sided(floor_ic, se_blk) if math.isfinite(se_blk) else None),
        }
        per_block_ics.append(float(info["ic"]))
    neg_blocks = sum(1 for ic in per_block_ics if ic < 0)
    pos_blocks = sum(1 for ic in per_block_ics if ic > 0)
    sign_consistent_count = max(neg_blocks, pos_blocks)
    sign_consistent = sign_consistent_count >= 2
    verdict = "INCONCLUSIVE" if not symmetry_pass else verdict_from_power(power_pooled)
    return {
        "track": "observed_liquidation_xsec_forward",
        "pooled": {
            "pooled_ic": primary["pooled_ic"],
            "mean_ic": primary.get("mean_ic"),
            "pooled_n": pooled_n,
            "null_5th": q5,
            "null_95th": q95,
            "null_width": width,
            "null_mid": mid,
            "symmetry_abs_frac": symmetry_abs_frac,
            "symmetry_pass_1pct": symmetry_pass,
            "se_analytic": se_pooled,
            "mde80_abs_ic": mde80,
            "floor_abs_ic": floor_ic,
            "achieved_power_at_floor": power_pooled,
            "verdict": verdict,
        },
        "per_block": per_block_out,
        "sign_consistency": {
            "n_blocks": len(per_block_ics),
            "negative_blocks": neg_blocks,
            "positive_blocks": pos_blocks,
            "same_sign_count": sign_consistent_count,
            "requirement_ge_2_of_3": True,
            "met": sign_consistent,
            "observed_ics": per_block_ics,
        },
        "track_verdict": verdict,
        "track_verdict_rule": "pooled achieved power at |IC|>=0.05 floor with null symmetry validation; per-block power is n-scaled approximation",
    }


def known_answer_self_test() -> dict:
    # Toy deterministic fixture (NOT market evidence): known effect recovery via CI-derived SE/MDE math.
    # If true delta=0.30 and SE=0.10, 95% CI half-width 0.196 => SE recovers 0.10 and power at 0.30 is high.
    se_true = 0.10
    delta_true = 0.30
    ci_lo = delta_true - Z_975 * se_true
    ci_hi = delta_true + Z_975 * se_true
    se_est = analytic_se_from_ci(ci_lo, ci_hi)
    mde80 = MDE80_FACTOR * se_est
    power = power_two_sided(delta_true, se_est)
    recovered = abs(se_est - se_true) < 1e-12 and power > 0.80 and mde80 < delta_true
    return {
        "description": "deterministic toy fixture (NOT market evidence): known SE/delta arithmetic recovery",
        "delta_true": delta_true,
        "se_true": se_true,
        "ci_lo": ci_lo,
        "ci_hi": ci_hi,
        "se_recovered": se_est,
        "mde80": mde80,
        "power_at_true_delta": power,
        "recovered_within_tolerance": recovered,
        "tolerance": 1e-12,
    }


def snapshot_hashes(paths) -> Dict[str, str]:
    return {str(p): sha256_file(p) for p in paths if p.exists()}


def build_md(out: dict) -> str:
    v = out["volatility"]
    l = out["observed_liquidation"]
    lines = []
    lines.append(f"# FCLR Power/MDE Calibration — {out['experiment_id']}")
    lines.append("")
    lines.append(f"- generated_utc: `{out['generated_utc']}`")
    lines.append(f"- status: `{out['status']}`  verdict: `{out['verdict']}`  max_status: `{out['max_status']}`  promotable: `{out['promotable']}`")
    lines.append(f"- prereg: `{out['prereg']}`")
    lines.append("- No model re-fit, no sealed-contrast recomputation, no sealed verdict changed.")
    lines.append("")
    lines.append("## Volatility forward (2025 disjoint)")
    lines.append(f"- track verdict (primary h24 C2_vs_B1): **{v['track_verdict']}**")
    p = v["primary"]
    lines.append(f"- primary h24 C2_vs_B1: SE={p['se_analytic']:.9f}, MDE80={p['mde80_abs_qlike']:.9f} QLIKE, floor={p['floor_abs_qlike']}, power={p['achieved_power_at_floor']:.6f}")
    lines.append("- per-horizon C2_vs_B1:")
    for h, r in v["per_horizon_C2_vs_B1"].items():
        lines.append(f"  - {h}: n={r['n']} days={r['n_days']} SE={r['se_analytic']:.9f} MDE80={r['mde80_abs_qlike']:.9f} floor={r['floor_abs_qlike']} power={r['achieved_power_at_floor']:.6f} verdict={r['verdict']}")
    lines.append("")
    lines.append("## Observed liquidation cross-section (forward)")
    lines.append(f"- track verdict (pooled): **{l['track_verdict']}**")
    lp = l["pooled"]
    lines.append(f"- pooled: SE={lp['se_analytic']:.9f}, MDE80={lp['mde80_abs_ic']:.9f} IC, floor={lp['floor_abs_ic']}, power={lp['achieved_power_at_floor']:.6f}, symmetry_pass={lp['symmetry_pass_1pct']} (mid={lp['null_mid']:.6g}, frac={lp['symmetry_abs_frac']:.6g})")
    lines.append(f"- sign consistency: {l['sign_consistency']['same_sign_count']}/{l['sign_consistency']['n_blocks']} same sign (met={l['sign_consistency']['met']}), ICs={l['sign_consistency']['observed_ics']}")
    lines.append("- per-block (SE is pooled-null n-scaled approximation, flagged):")
    for b, r in l["per_block"].items():
        lines.append(f"  - {b}: n={r['n']} ic={r['ic']:.6g} SE~{r['se_analytic_pooled_null_scaled']:.9f} MDE80~{r['mde80_abs_ic']:.9f} power~{r['achieved_power_at_floor']:.6f} verdict={r['verdict']}")
    lines.append("")
    lines.append("## Known-answer self-test")
    ka = out["known_answer_self_test"]
    lines.append(f"- recovered={ka['recovered_within_tolerance']} (SE {ka['se_recovered']} vs {ka['se_true']}, power {ka['power_at_true_delta']:.6f}) — NOT market evidence")
    lines.append("")
    lines.append("## Interpretation guardrails")
    lines.append("- EXPLORATORY_ONLY, promotable=false; does not reopen sealed verdicts or claim a market effect.")
    return "\n".join(lines) + "\n"


def run(out_utc: str = DEFAULT_UTC, write: bool = True) -> dict:
    prereg_path = RS / f"prereg_fclr_power_calibration_{out_utc}.json"
    prereg = read_json(prereg_path)
    # verify input hashes match prereg
    input_paths = {
        "vol_eval_sha256": VOL_EVAL,
        "vol_prereg_sha256": VOL_PREREG,
        "vol_panel_sha256": VOL_PANEL,
        "liq_eval_sha256": LIQ_EVAL,
        "liq_prereg_sha256": LIQ_PREREG,
        "liq_panel_sha256": LIQ_PANEL,
    }
    for k, p in input_paths.items():
        actual = sha256_file(p)
        expected = prereg["inputs"][k]
        if actual != expected:
            raise SystemExit(f"input hash mismatch for {p.name}: expected {expected} got {actual}")

    sealed_before = snapshot_hashes(sorted(SEALED_EVALS | SEALED_PREREGS, key=str))
    vol_eval = read_json(VOL_EVAL)
    liq_eval = read_json(LIQ_EVAL)
    vol = analyze_vol(vol_eval)
    liq = analyze_liq(liq_eval)
    ka = known_answer_self_test()
    if not ka["recovered_within_tolerance"]:
        raise SystemExit("known-answer self-test failed")

    overall = "INCONCLUSIVE" if "INCONCLUSIVE" in (vol["track_verdict"], liq["track_verdict"]) else "COMPLETE"
    out = {
        "experiment_id": f"FCLR-POWER-CALIBRATION-{out_utc}",
        "campaign": "FCLR-POWER-CALIBRATION",
        "generated_utc": out_utc,
        "status": "VALID_EXPLORATORY",
        "verdict": overall,
        "max_status": "EXPLORATORY_ONLY",
        "promotable": False,
        "audit_only": True,
        "does_not_reopen_sealed_verdict": True,
        "prereg": str(prereg_path.relative_to(REPO)),
        "prereg_sha256": sha256_file(prereg_path),
        "inputs": {k: {"path": str(p.relative_to(REPO)), "sha256": sha256_file(p)} for k, p in [
            ("vol_eval", VOL_EVAL), ("vol_prereg", VOL_PREREG), ("vol_panel", VOL_PANEL),
            ("liq_eval", LIQ_EVAL), ("liq_prereg", LIQ_PREREG), ("liq_panel", LIQ_PANEL),
        ]},
        "method": {
            "alpha": 0.05,
            "power_target": 0.80,
            "z_975": Z_975,
            "z_80": Z_80,
            "z_95": Z_95,
            "mde80_factor": MDE80_FACTOR,
            "vol_se": "SE = (ci_hi - ci_lo) / (2*z_975) from persisted 95% CI",
            "liq_pooled_se": "SE = (null_95th - null_5th) / (2*z_95) with 1% symmetry check",
            "liq_per_block_se": "SE_block = SE_pooled * sqrt(pooled_n/block_n) (approximation; per-block null quantiles not persisted)",
            "power": "Phi(|delta|/SE - z_975) + Phi(-|delta|/SE - z_975)",
        },
        "volatility": vol,
        "observed_liquidation": liq,
        "known_answer_self_test": ka,
        "sealed_hashes_before": sealed_before,
    }

    # verify no sealed mutation
    sealed_after = snapshot_hashes(sorted(SEALED_EVALS | SEALED_PREREGS, key=str))
    if sealed_after != sealed_before:
        raise SystemExit(f"sealed artifact mutation detected: before!=after")
    out["sealed_hashes_after"] = sealed_after
    out["sealed_artifacts_mutated"] = False

    if write:
        eval_json_path = RS / f"evaluation_summary_FCLR-POWER-CALIBRATION-{out_utc}.json"
        eval_md_path = RS / f"evaluation_summary_FCLR-POWER-CALIBRATION-{out_utc}.md"
        eval_json_path.write_text(json.dumps(out, indent=2, sort_keys=False) + "\n")
        eval_md_path.write_text(build_md(out))
        out["output_json"] = str(eval_json_path.relative_to(REPO))
        out["output_md"] = str(eval_md_path.relative_to(REPO))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-utc", default=DEFAULT_UTC)
    ap.add_argument("--no-write", action="store_true")
    args = ap.parse_args()
    out = run(out_utc=args.out_utc, write=not args.no_write)
    print(json.dumps({
        "experiment_id": out["experiment_id"],
        "verdict": out["verdict"],
        "vol_track": out["volatility"]["track_verdict"],
        "liq_track": out["observed_liquidation"]["track_verdict"],
        "sealed_artifacts_mutated": out["sealed_artifacts_mutated"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
