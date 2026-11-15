#!/usr/bin/env python3
"""FCLR-DESIGN-FEASIBILITY: invert power calibration to assess decidability on cache.

Deterministic, offline, read-only over persisted design quantities. No model
re-fit, no sealed-contrast recomputation, no SE re-derivation from raw data,
no network, no mutation of sealed artifacts.

Reads persisted SEs/design quantities from the power-calibration eval and the
two cached panels (for maximum available n only). Inverts the two-sided power
equation to compute required n for 80% power at pre-specified floors and
assigns per-track decidability: DECIDABLE_ON_CACHE / UNDECIDABLE_ON_CACHE /
INCONCLUSIVE.

Outputs (EXPLORATORY_ONLY, promotable=false):
  research_state/evaluation_summary_FCLR-DESIGN-FEASIBILITY-<UTC>.json
  research_state/evaluation_summary_FCLR-DESIGN-FEASIBILITY-<UTC>.md
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

REPO = Path(__file__).resolve().parents[1]
RS = REPO / "research_state"
DEFAULT_UTC = "2026-11-15T02:35:00Z"
PREREG_NAME = f"prereg_fclr_design_feasibility_{DEFAULT_UTC}.json"

Z_975 = 1.959963984540054
Z_80 = 0.8416212335729143
Z_95 = 1.6448536269514722
MDE80_FACTOR = Z_975 + Z_80  # 2.8015852181129683

POWER_EVAL = RS / "evaluation_summary_FCLR-POWER-CALIBRATION-2026-11-15T01:34:12Z.json"
POWER_PREREG = RS / "prereg_fclr_power_calibration_2026-11-15T01:34:12Z.json"
VOL_PANEL = RS / "tracka_fwd_vol_2025_disjoint_cross_panel_20261114T191615Z.parquet"
LIQ_PANEL = RS / "tracka_liq_xsec_forward_panel_2026-11-13T22:31:55Z.parquet"

# Sealed artifacts that must not be mutated by this analysis.
SEALED = {
    RS / "evaluation_summary_FCLR-FWD-VOL-2025-DISJOINT-CROSS-20261114T191615Z.json",
    RS / "evaluation_summary_FCLR-FWD-VOL-2025-DISJOINT-RECONCILE-20261114T193000Z.json",
    RS / "evaluation_summary_FCLR-FWD-VOL-2024-DISJOINT-2024-06-20261114T231100Z_20261114T231545Z.json",
    RS / "evaluation_summary_FCLR-FWD-VOL-2025-DISJOINT-CORRECTED-AUDIT-2026-11-15T00:12:56Z.json",
    RS / "evaluation_summary_TRACKA-LIQ-XSEC-FORWARD-2026-11-13T22:31:55Z.json",
    POWER_EVAL,
    POWER_PREREG,
    RS / "prereg_fclr_fwd_vol_2025_disjoint_cross_20261114T183000Z.json",
    RS / "prereg_tracka_liq_xsec_forward_2026q1q2_20261113T222859Z.json",
}


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


def power_two_sided(delta_abs: float, se: float) -> float:
    if se <= 0 or not math.isfinite(se) or not math.isfinite(delta_abs):
        return float("nan")
    lam = abs(delta_abs) / se
    return phi(lam - Z_975) + phi(-lam - Z_975)


def se_required_for_floor(floor_abs: float) -> float:
    """SE that yields 80% power at floor: SE_req = |floor| / (z_975 + z_80)."""
    if not math.isfinite(floor_abs) or floor_abs <= 0:
        return float("nan")
    return abs(floor_abs) / MDE80_FACTOR


def required_n(se_obs: float, se_req: float, n_obs: float) -> float:
    """n_req = n_obs * (SE_obs / SE_req)^2 under 1/sqrt(n) scaling."""
    if se_req <= 0 or not math.isfinite(se_req) or not math.isfinite(se_obs) or n_obs <= 0:
        return float("nan")
    return n_obs * (se_obs / se_req) ** 2


def decidability(n_req: float, n_available: float) -> str:
    if not math.isfinite(n_req) or not math.isfinite(n_available) or n_available <= 0:
        return "INCONCLUSIVE"
    return "DECIDABLE_ON_CACHE" if n_req <= n_available else "UNDECIDABLE_ON_CACHE"


def panel_row_count(p: Path) -> int:
    try:
        import pandas as pd  # type: ignore
        return int(len(pd.read_parquet(p, columns=[])))
    except Exception:
        # Fallback: read full parquet metadata-less via pandas if available; else count via pyarrow.
        try:
            import pyarrow.parquet as pq  # type: ignore
            return int(pq.ParquetFile(p).metadata.num_rows)
        except Exception:
            return -1


def analyze_vol(power_eval: dict, vol_panel_rows: int) -> dict:
    vol = power_eval["volatility"]
    contrasts = vol.get("all_contrasts", {})
    horizons = vol.get("per_horizon_C2_vs_B1", {})
    rows: Dict[str, Any] = {}

    # Per-horizon C2_vs_B1 table (primary family view)
    per_horizon = {}
    for hkey, h in horizons.items():
        se_obs = float(h["se_analytic"])
        floor = float(h["floor_abs_qlike"])
        n_obs = float(h["n"])
        se_req = se_required_for_floor(floor)
        n_req = required_n(se_obs, se_req, n_obs)
        n_avail = n_obs  # contrast-level cached
        per_horizon[hkey] = {
            "contrast": f"{hkey}_C2_vs_B1",
            "n_obs_contrast": h.get("n"),
            "n_days": h.get("n_days"),
            "se_obs": se_obs,
            "floor_abs_qlike": floor,
            "se_req_for_80pct": se_req,
            "n_req_contrast": n_req,
            "n_available_contrast": n_avail,
            "power_at_floor_persisted": h.get("achieved_power_at_floor"),
            "verdict": decidability(n_req, n_avail),
            "scaling_factor_se": (se_obs / se_req) if (math.isfinite(se_req) and se_req > 0) else None,
        }

    # All contrasts
    all_contrasts_out = {}
    for key, c in contrasts.items():
        se_obs = float(c["se_analytic"])
        floor = float(c["floor_abs_qlike"])
        n_obs = float(c["n"])
        se_req = se_required_for_floor(floor)
        n_req = required_n(se_obs, se_req, n_obs)
        n_avail = n_obs
        all_contrasts_out[key] = {
            "n_obs_contrast": c.get("n"),
            "n_days": c.get("n_days"),
            "se_obs": se_obs,
            "floor_abs_qlike": floor,
            "se_req_for_80pct": se_req,
            "n_req_contrast": n_req,
            "n_available_contrast": n_avail,
            "power_at_floor_persisted": c.get("achieved_power_at_floor"),
            "verdict": decidability(n_req, n_avail),
        }

    primary = per_horizon.get("h24", {})
    track_verdict = primary.get("verdict", "INCONCLUSIVE")
    return {
        "track": "volatility_forward_2025_disjoint",
        "primary_contrast": "h24_C2_vs_B1",
        "n_obs_panel_rows": vol_panel_rows,
        "n_available_contrast_cached_primary": 10800,
        "panel_structure": "5 symbols x 90 test days x 3 blocks x 24h = 10800 contrast obs (primary h24); panel rows 30120",
        "se_scaling": "1/sqrt(n) on contrast-level n",
        "primary": primary,
        "per_horizon_C2_vs_B1": per_horizon,
        "all_contrasts": all_contrasts_out,
        "track_verdict": track_verdict,
        "track_verdict_rule": "primary h24 C2_vs_B1 contrast-level decidability at 2% implied-baseline QLIKE floor",
    }


def analyze_liq(power_eval: dict, liq_panel_rows: int) -> dict:
    liq = power_eval["observed_liquidation"]
    pooled = liq["pooled"]
    per_block_in = liq.get("per_block", {})
    sign = liq.get("sign_consistency", {})

    n_obs = float(pooled["pooled_n"])
    floor = float(pooled["floor_abs_ic"])
    se_obs = float(pooled["se_analytic"])
    se_req = se_required_for_floor(floor)
    n_req = required_n(se_obs, se_req, n_obs)
    n_avail = n_obs
    analytic_verdict = decidability(n_req, n_avail)

    # Symmetry-robust SE: max(|q5|, |q95|) / z_95
    q5 = float(pooled["null_5th"])
    q95 = float(pooled["null_95th"])
    se_robust = max(abs(q5), abs(q95)) / Z_95
    n_req_robust = required_n(se_robust, se_req, n_obs)
    robust_verdict = decidability(n_req_robust, n_avail)
    verdict_flips = analytic_verdict != robust_verdict

    per_block_out = {}
    for bk, b in per_block_in.items():
        bn = float(b["n"])
        b_se = float(b.get("se_analytic_pooled_null_scaled", float("nan")))
        b_se_req = se_req  # same IC floor
        b_n_req = required_n(b_se, b_se_req, bn)
        per_block_out[bk] = {
            "n_obs": b.get("n"),
            "ic": b.get("ic"),
            "se_obs_approx": b_se,
            "se_method": b.get("se_method"),
            "se_req_for_80pct": b_se_req,
            "n_req_at_block_scale": b_n_req,
            "n_available_block": bn,
            "power_at_floor_persisted": b.get("achieved_power_at_floor"),
            "verdict_approx": decidability(b_n_req, bn),
        }

    # Decidability is based on analytic SE but instability is surfaced; overall track
    # cannot be cleaner than analytic/robust agreement on decidability and must flag instability.
    if "INCONCLUSIVE" in (analytic_verdict, robust_verdict):
        track_verdict = "INCONCLUSIVE"
    else:
        # If they agree, decidability is that value (instability noted separately).
        # If they disagree, treat as INCONCLUSIVE for safety.
        track_verdict = analytic_verdict if not verdict_flips else "INCONCLUSIVE"

    symmetry = {
        "symmetry_pass_1pct_persisted": pooled.get("symmetry_pass_1pct"),
        "null_mid_persisted": pooled.get("null_mid"),
        "symmetry_abs_frac_persisted": pooled.get("symmetry_abs_frac"),
        "se_analytic_pooled": se_obs,
        "se_robust_max_halfwidth_over_z95": se_robust,
        "analytic_verdict": analytic_verdict,
        "robust_verdict": robust_verdict,
        "verdict_flips_due_to_instability": verdict_flips,
        "note": "Analytic SE used null quantile half-width; symmetry failed (abs_frac>1%). Robust SE uses max(|q5|,|q95|)/z_95."
    }

    return {
        "track": "observed_liquidation_xsec_forward",
        "n_obs_panel_rows": liq_panel_rows,
        "n_available_pooled_cached": int(n_obs),
        "panel_structure": "107 coins x 3 blocks; pooled n=6634 (2996/1605/2033)",
        "se_scaling": "1/sqrt(n) on pooled n",
        "pooled": {
            "n_obs_pooled": pooled.get("pooled_n"),
            "pooled_ic": pooled.get("pooled_ic"),
            "se_obs_analytic": se_obs,
            "floor_abs_ic": floor,
            "se_req_for_80pct": se_req,
            "n_req_pooled": n_req,
            "n_available_pooled": n_avail,
            "power_at_floor_persisted": pooled.get("achieved_power_at_floor"),
            "analytic_decidability": analytic_verdict,
            "se_robust": se_robust,
            "n_req_pooled_robust": n_req_robust,
            "robust_decidability": robust_verdict,
        },
        "per_block": per_block_out,
        "sign_consistency": sign,
        "symmetry_robustness": symmetry,
        "track_verdict": track_verdict,
        "track_verdict_rule": "Decidability from analytic pooled SE vs cached pooled n, with symmetry-robust check; verdict flip => INCONCLUSIVE. Instability is flagged regardless."
    }


def known_answer_self_test() -> dict:
    """Toy fixture (NOT market evidence): verify inversion recovers 80% power."""
    delta = 0.3
    se_true = 0.1
    n_obs = 1000.0
    se_req = se_required_for_floor(delta)
    n_req = required_n(se_true, se_req, n_obs)
    # At n_req, SE becomes se_req => power 0.80 at delta
    se_at_nreq = se_true * math.sqrt(n_obs / n_req)
    power_at_nreq = power_two_sided(delta, se_at_nreq)
    recovered = abs(power_at_nreq - 0.80) < 1e-6
    return {
        "description": "deterministic toy fixture (NOT market evidence): required-n inversion recovery",
        "delta": delta,
        "se_true": se_true,
        "n_obs": n_obs,
        "se_req": se_req,
        "n_req": n_req,
        "se_at_nreq": se_at_nreq,
        "power_at_nreq": power_at_nreq,
        "recovered_80pct_within_tolerance": recovered,
        "tolerance": 1e-6,
    }


def overall_verdict(vol: dict, liq: dict) -> str:
    # Campaign-level: report both; overall is the more conservative informative combination.
    vv = vol.get("track_verdict")
    lv = liq.get("track_verdict")
    if "INCONCLUSIVE" in (vv, lv):
        return "INCONCLUSIVE"
    if vv == "UNDECIDABLE_ON_CACHE" or lv == "UNDECIDABLE_ON_CACHE":
        # if either structurally undecidable on cache, highlight undecidability as the binding constraint
        # but report both explicitly; overall marked UNDECIDABLE_ON_CACHE when vol is (dominant constraint).
        return "UNDECIDABLE_ON_CACHE" if vv == "UNDECIDABLE_ON_CACHE" else "DECIDABLE_ON_CACHE"
    return "DECIDABLE_ON_CACHE"


def render_md(out: dict) -> str:
    v = out["volatility"]
    l = out["observed_liquidation"]
    ka = out["known_answer_self_test"]
    lines = []
    lines.append(f"# FCLR Design Feasibility — {out['experiment_id']}")
    lines.append("")
    lines.append(f"- Generated (UTC): {out['generated_utc']}")
    lines.append(f"- Status: {out['status']} (EXPLORATORY_ONLY, promotable=false, audit_only=true)")
    lines.append(f"- Overall verdict: **{out['verdict']}**")
    lines.append(f"- Prereg: `{out['prereg']}`")
    lines.append("")
    lines.append("## Method")
    lines.append("")
    m = out["method"]
    lines.append(f"- alpha={m['alpha']}, power_target={m['power_target']}, z_975={m['z_975']}, z_80={m['z_80']}, z_95={m['z_95']}, mde80_factor={m['mde80_factor']}")
    lines.append(f"- SE_req = |floor| / mde80_factor; n_req = n_obs * (SE_obs / SE_req)^2 (1/sqrt(n) scaling).")
    lines.append(f"- Verdict rule: {m['decidability_rule']}")
    lines.append("")
    lines.append("## Volatility track (forward 2025 disjoint, C2_vs_B1)")
    lines.append("")
    lines.append(f"- Track verdict: **{v['track_verdict']}** (primary {v['primary_contrast']})")
    lines.append(f"- Panel rows (max available): {v['n_obs_panel_rows']}; primary contrast n_available={v['n_available_contrast_cached_primary']}")
    p = v["primary"]
    lines.append(f"- Primary h24: n_obs={p['n_obs_contrast']}, SE_obs={p['se_obs']:.6g}, floor={p['floor_abs_qlike']:.6g}, SE_req={p['se_req_for_80pct']:.6g}, n_req={p['n_req_contrast']:.1f}, n_available={p['n_available_contrast']} => **{p['verdict']}**")
    lines.append("")
    lines.append("| horizon | n_obs | SE_obs | floor | SE_req | n_req | n_avail | verdict |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---|")
    for hk, h in v["per_horizon_C2_vs_B1"].items():
        lines.append(f"| {hk} | {h['n_obs_contrast']} | {h['se_obs']:.6g} | {h['floor_abs_qlike']:.6g} | {h['se_req_for_80pct']:.6g} | {h['n_req_contrast']:.1f} | {h['n_available_contrast']} | {h['verdict']} |")
    lines.append("")
    lines.append("## Observed-liquidation track (xsec forward)")
    lines.append("")
    lines.append(f"- Track verdict: **{l['track_verdict']}** (analytic vs symmetry-robust reported)")
    lines.append(f"- Panel rows / pooled n_available: {l['n_obs_panel_rows']} / {l['n_available_pooled_cached']}")
    lp = l["pooled"]
    lines.append(f"- Pooled analytic: n_obs={lp['n_obs_pooled']}, SE_obs={lp['se_obs_analytic']:.6g}, floor={lp['floor_abs_ic']}, SE_req={lp['se_req_for_80pct']:.6g}, n_req={lp['n_req_pooled']:.1f}, n_available={lp['n_available_pooled']} => **{lp['analytic_decidability']}**")
    lines.append(f"- Pooled symmetry-robust: SE_robust={lp['se_robust']:.6g}, n_req={lp['n_req_pooled_robust']:.1f}, n_available={lp['n_available_pooled']} => **{lp['robust_decidability']}**")
    sym = l["symmetry_robustness"]
    lines.append(f"- Symmetry instability: pass_1pct_persisted={sym['symmetry_pass_1pct_persisted']}, abs_frac={sym['symmetry_abs_frac_persisted']}, verdict_flips={sym['verdict_flips_due_to_instability']}")
    lines.append("")
    lines.append("### Per-block (approximate, pooled-null SE scaled)")
    lines.append("")
    lines.append("| block | n_obs | IC | SE_obs_approx | n_req | n_avail | verdict_approx |")
    lines.append("|---|---:|---:|---:|---:|---:|---|")
    for bk, b in l["per_block"].items():
        lines.append(f"| {bk} | {b['n_obs']} | {b['ic']:.6g} | {b['se_obs_approx']:.6g} | {b['n_req_at_block_scale']:.1f} | {b['n_available_block']} | {b['verdict_approx']} |")
    lines.append("")
    lines.append("## Known-answer self-test (NOT market evidence)")
    lines.append("")
    lines.append(f"- recovered_80pct_within_tolerance={ka['recovered_80pct_within_tolerance']} (power_at_nreq={ka['power_at_nreq']:.12f}, n_req={ka['n_req']:.6f})")
    lines.append("")
    lines.append("## Inputs (sha256)")
    lines.append("")
    for k, v in out["inputs"].items():
        lines.append(f"- {k}: `{v['path']}` sha256={v['sha256']}")
    lines.append("")
    lines.append("## Sealed-artifact integrity")
    lines.append("")
    lines.append(f"- sealed_artifacts_mutated: {out['sealed_artifacts_mutated']}")
    return "\n".join(lines) + "\n"


def run(out_utc: Optional[str] = None, write: bool = True) -> dict:
    out_utc = out_utc or DEFAULT_UTC
    prereg_path = RS / PREREG_NAME
    prereg = read_json(prereg_path)
    assert prereg.get("status") == "FROZEN_PRE_OUTCOMES"
    assert prereg.get("frozen_before_outcomes") is True
    assert prereg.get("promotable") is False

    # Record sealed hashes before
    sealed_before = {str(p): sha256_file(p) for p in sorted(SEALED) if p.exists()}

    power_eval = read_json(POWER_EVAL)
    # Basic method consistency
    meth = power_eval.get("method", {})
    assert abs(float(meth.get("z_975", Z_975)) - Z_975) < 1e-12
    assert abs(float(meth.get("z_80", Z_80)) - Z_80) < 1e-12
    assert abs(float(meth.get("mde80_factor", MDE80_FACTOR)) - MDE80_FACTOR) < 1e-12
    assert abs(float(meth.get("z_95", Z_95)) - Z_95) < 1e-12

    vol_rows = panel_row_count(VOL_PANEL)
    liq_rows = panel_row_count(LIQ_PANEL)

    vol = analyze_vol(power_eval, vol_rows)
    liq = analyze_liq(power_eval, liq_rows)
    ka = known_answer_self_test()
    verdict = overall_verdict(vol, liq)

    # Record sealed hashes after (must be identical)
    sealed_after = {str(p): sha256_file(p) for p in sorted(SEALED) if p.exists()}
    sealed_mutated = sealed_before != sealed_after

    inputs = {
        "power_calibration_eval": {"path": str(POWER_EVAL.relative_to(REPO)), "sha256": sha256_file(POWER_EVAL)},
        "power_calibration_prereg": {"path": str(POWER_PREREG.relative_to(REPO)), "sha256": sha256_file(POWER_PREREG)},
        "vol_panel": {"path": str(VOL_PANEL.relative_to(REPO)), "sha256": sha256_file(VOL_PANEL)},
        "liq_panel": {"path": str(LIQ_PANEL.relative_to(REPO)), "sha256": sha256_file(LIQ_PANEL)},
    }

    out = {
        "experiment_id": "FCLR-DESIGN-FEASIBILITY-20261115T021249Z",
        "campaign": "FCLR-DESIGN-FEASIBILITY",
        "generated_utc": out_utc,
        "status": "VALID_EXPLORATORY",
        "verdict": verdict,
        "max_status": "EXPLORATORY_ONLY",
        "promotable": False,
        "audit_only": True,
        "does_not_reopen_sealed_verdict": True,
        "prereg": str(prereg_path.relative_to(REPO)),
        "prereg_sha256": sha256_file(prereg_path),
        "inputs": inputs,
        "method": {
            "alpha": 0.05,
            "power_target": 0.8,
            "z_975": Z_975,
            "z_80": Z_80,
            "z_95": Z_95,
            "mde80_factor": MDE80_FACTOR,
            "se_req_formula": "|floor| / (z_975 + z_80)",
            "n_req_formula": "n_obs * (SE_obs / SE_req)^2 (1/sqrt(n) scaling)",
            "decidability_rule": {
                "DECIDABLE_ON_CACHE": "n_req <= n_available",
                "UNDECIDABLE_ON_CACHE": "n_req > n_available",
                "INCONCLUSIVE": "unstable/missing/non-finite inputs",
            },
        },
        "volatility": vol,
        "observed_liquidation": liq,
        "known_answer_self_test": ka,
        "sealed_hashes_before": sealed_before,
        "sealed_hashes_after": sealed_after,
        "sealed_artifacts_mutated": sealed_mutated,
    }

    if write:
        ej = RS / f"evaluation_summary_FCLR-DESIGN-FEASIBILITY-{out_utc}.json"
        em = RS / f"evaluation_summary_FCLR-DESIGN-FEASIBILITY-{out_utc}.md"
        ej.write_text(json.dumps(out, indent=2, sort_keys=False) + "\n")
        em.write_text(render_md(out))
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-utc", default=DEFAULT_UTC)
    ap.add_argument("--no-write", action="store_true")
    args = ap.parse_args()
    out = run(out_utc=args.out_utc, write=not args.no_write)
    print(json.dumps({"verdict": out["verdict"], "vol": out["volatility"]["track_verdict"], "liq": out["observed_liquidation"]["track_verdict"], "sealed_artifacts_mutated": out["sealed_artifacts_mutated"]}, indent=2))


if __name__ == "__main__":
    main()
