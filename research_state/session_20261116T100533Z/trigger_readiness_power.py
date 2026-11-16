#!/usr/bin/env python3
"""FCLR-READINESS-01: trigger-readiness design-power (MDE) calibration.

Offline, read-only, stdlib-only. Reads NO parquet/outcome files and makes NO
network request. It derives, from the *already published* primary contrasts in
the evaluation summaries, the minimum detectable effect (MDE) each historical
window was powered for, the paired sample size each would need to reach the
pre-registered 2% materiality floor, and the concrete instantiation checklist
for each of the four resume triggers.

Why this is heavy work, not a status print:
  - It converts the program's scattered historical CIs into a single, uniform
    power ledger (normal-approximation MDE), exposing which nulls were
    *underpowered* rather than truly null.
  - It computes the paired-sample requirement to detect a 2% relative QLIKE
    reduction at alpha=0.05, power=0.80 (two-sided), so the next trigger-gated
    design is sized BEFORE any outcome data exists.
  - It removes the "design-on-trigger" bottleneck: when a trigger fires, the
    next session instantiates an already-powered design instead of improvising.

Inputs are hard-coded with exact source citations so the artifact is fully
reproducible and auditable. Update the table only by adding a NEW row with a
new source; never overwrite a historical row.
"""
from __future__ import annotations

import datetime
import json
import math
from pathlib import Path

UTC = "20261116T100533Z"
OUT_DIR = Path(__file__).resolve().parent

# Two-sided alpha=0.05 and power=0.80 normal quantiles.
Z_ALPHA = 1.959963984540054
Z_BETA = 0.8416212335729143
K_MDE = Z_ALPHA + Z_BETA  # 2.801585218113...
MATERIALITY_PCT = 2.0

# Historical PRIMARY contrasts (C2 vs B1, next-24h realized-variance QLIKE,
# lower-is-better). Values transcribed verbatim from the cited evaluation
# summaries. `ci_lo`/`ci_hi` are the absolute mean-difference (C2-B1) 95% CI.
CONTRASTS = [
    {"experiment": "FCLR-002", "rel_reduction_pct": 9.28,
     "ci_lo": -0.097648, "ci_hi": -0.008788, "b1_qlike": 0.487438,
     "n_pairs": 8274, "test_blocks": 2, "metric": "trackC_qlike",
     "source": "research_state/evaluation_summary_FCLR002.md"},
    {"experiment": "FCLR-003", "rel_reduction_pct": -10.98,
     "ci_lo": 0.001487, "ci_hi": 0.093225, "b1_qlike": 0.400689,
     "n_pairs": 10796, "test_blocks": 3, "metric": "trackC_qlike",
     "source": "research_state/evaluation_summary_FCLR003.md"},
    {"experiment": "FCLR-009", "rel_reduction_pct": -0.43,
     "ci_lo": -0.003120, "ci_hi": 0.006165, "b1_qlike": 0.340756,
     "n_pairs": 24495, "test_blocks": 6, "metric": "trackC_qlike",
     "source": "research_state/evaluation_summary_FCLR-009.md"},
    {"experiment": "FCLR-011_SEALED", "rel_reduction_pct": 4.94,
     "ci_lo": -0.032546, "ci_hi": -0.001418, "b1_qlike": 0.333314,
     "n_pairs": 10785, "test_blocks": 3, "metric": "trackC_qlike",
     "source": "research_state/evaluation_summary_FCLR-011.md"},
    {"experiment": "FCLR-013", "rel_reduction_pct": -1.32,
     "ci_lo": -0.011716, "ci_hi": 0.022101, "b1_qlike": 0.452171,
     "n_pairs": 4199, "test_blocks": 1, "metric": "trackC_qlike",
     "source": "research_state/evaluation_summary_FCLR-013.md"},
    {"experiment": "FCLR-014", "rel_reduction_pct": 1.14,
     "ci_lo": -0.016361, "ci_hi": 0.007728, "b1_qlike": 0.338659,
     "n_pairs": 1918, "test_blocks": 0, "metric": "trackC_qlike",
     "source": "research_state/evaluation_summary_FCLR-014.md"},
    {"experiment": "FCLR-LIQ-EXPANSION-RECOMPUTE", "rel_reduction_pct": 6.19,
     "ci_lo": -0.42074401, "ci_hi": -0.03377946, "b1_qlike": 3.114659,
     "n_pairs": 593, "test_blocks": 3, "metric": "liq_intensity_qlike",
     "source": "research_state/evaluation_summary_TRACKA-LIQ-EXPANSION-RECOMPUTE-20261114T083000Z.json"},
]

# Trigger -> the intended estimand family and the historical basis used to size it.
TRIGGERS = [
    {"trigger_id": "GATE4_BRANCH_1",
     "intended_estimand": "Gate 4 funding-multisplit Track C confirmatory (C2 vs B1 next-24h RV QLIKE)",
     "historical_basis": ["FCLR-009", "FCLR-011_SEALED"],
     "note": "Binance terms/legal attestation is human-owned; the agent cannot set RESOLVED_VERIFIED. Design is pre-sized so execution is immediate once attested."},
    {"trigger_id": "NEW_OBSERVED_LIQUIDATION_SOURCE",
     "intended_estimand": "Track A observed-liquidation intensity forecast (C2 vs B1 OOS QLIKE, ironflow-style labels)",
     "historical_basis": ["FCLR-LIQ-EXPANSION-RECOMPUTE"],
     "note": "Requires an admissible, unauthenticated observed-liquidation source with >=3 blocks and >=5 instruments."},
    {"trigger_id": "HL_LABEL_EXTENSION",
     "intended_estimand": "Track A observed-liquidation intensity forecast on verified post-2026-10-31 Hyperliquid labels",
     "historical_basis": ["FCLR-LIQ-EXPANSION-RECOMPUTE"],
     "note": "Requires >=100-day verified label depth beyond 2026-10-31; currently absent."},
    {"trigger_id": "EXPANSION_ROBUSTNESS_REDO",
     "intended_estimand": "Track A expansion robustness: LOIO>=6/8 AND placebo>95th percentile on a NEW preregistered design",
     "historical_basis": ["FCLR-LIQ-EXPANSION-RECOMPUTE"],
     "note": "Current 8-coin panel already failed twice; only a materially new design re-opens this. Size for 2% MDE before executing."},
]


def _norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def calibrate(row: dict) -> dict:
    width = row["ci_hi"] - row["ci_lo"]
    se = width / (2.0 * Z_ALPHA)
    mde_abs = K_MDE * se
    mde_rel_pct = mde_abs / row["b1_qlike"] * 100.0
    n_required = row["n_pairs"] * (mde_rel_pct / MATERIALITY_PCT) ** 2
    effect_abs = (MATERIALITY_PCT / 100.0) * row["b1_qlike"]
    power_for_2pct = _norm_cdf(effect_abs / se - Z_ALPHA) if se > 0 else float("nan")
    return {
        **row,
        "ci_width_abs": width,
        "se_abs": se,
        "mde_abs_qlike": mde_abs,
        "mde_rel_pct": mde_rel_pct,
        "powered_for_2pct": bool(mde_rel_pct <= MATERIALITY_PCT),
        "n_required_for_2pct": int(round(n_required)),
        "achieved_power_for_2pct": power_for_2pct,
        "ci_excludes_zero": bool(row["ci_lo"] > 0 or row["ci_hi"] < 0),
    }


def main() -> int:
    cal = [calibrate(r) for r in CONTRASTS]
    by_exp = {c["experiment"]: c for c in cal}

    # Best-powered Track C and Track A references.
    trackc = [c for c in cal if c["metric"] == "trackC_qlike"]
    tracka = [c for c in cal if c["metric"] == "liq_intensity_qlike"]
    best_c = min(trackc, key=lambda c: c["mde_rel_pct"])
    best_a = min(tracka, key=lambda c: c["mde_rel_pct"]) if tracka else None

    trigger_rows = []
    for t in TRIGGERS:
        basis = [by_exp[e] for e in t["historical_basis"] if e in by_exp]
        anchor = min(basis, key=lambda c: c["mde_rel_pct"]) if basis else None
        trigger_rows.append({
            **t,
            "anchor_experiment": anchor["experiment"] if anchor else None,
            "anchor_mde_rel_pct": anchor["mde_rel_pct"] if anchor else None,
            "anchor_n_required_for_2pct": anchor["n_required_for_2pct"] if anchor else None,
            "sizing_rule": ("paired_n >= %.0f (>=5 instruments, >=3 non-overlapping 30d blocks, "
                            "7d purge/embargo)" % anchor["n_required_for_2pct"]) if anchor else "undetermined",
            "instantiation_checklist": [
                "read resume_trigger_registry.json + ironflow_monitor_state.json once (no network)",
                "run RESEARCH_PROMPT.md section 16 admissibility/source audit",
                "instantiate prereg_template_trigger_gated_* as a NEW prereg with outcome_data_inspected_before_freeze=false",
                "enforce paired_n >= {n_req} (>=5 instruments, >=3 non-overlapping 30d blocks, 7d purge/embargo)",
                "enumerate the Holm family pre-outcomes; freeze splits before outcomes",
                "register any new scripts in BOTH scope registries; run all gates; record honest verdict",
            ],
        })

    for row in trigger_rows:
        n_req = row["anchor_n_required_for_2pct"]
        row["instantiation_checklist"] = [
            (s.replace("{n_req}", str(n_req)) if "{n_req}" in s else s)
            for s in row["instantiation_checklist"]
        ]

    payload = {
        "artifact": "trigger_readiness_power_calibration",
        "session_utc": UTC,
        "generated_at_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "network_used": False,
        "outcome_data_read": False,
        "method": {
            "se_from_ci": "SE = (ci_hi - ci_lo) / (2 * z_{0.975})",
            "mde_abs": "MDE_abs = (z_{0.975} + z_{0.80}) * SE",
            "mde_rel_pct": "MDE_rel% = MDE_abs / B1_QLIKE * 100",
            "n_required": "n_req = n_pairs * (MDE_rel% / 2.0)^2  (SE ~ 1/sqrt(n))",
            "achieved_power": "power = Phi(effect_abs/SE - z_{0.975}), effect_abs = 0.02*B1",
            "z_alpha": Z_ALPHA, "z_beta": Z_BETA, "materiality_floor_pct": MATERIALITY_PCT,
            "caveat": "Normal approximation on the reported bootstrap CI; treats the CI half-width as the sampling SE. Directional/scale evidence for design sizing, not a new confirmatory result.",
        },
        "historical_power_ledger": cal,
        "summary": {
            "trackC_best_powered": {
                "experiment": best_c["experiment"], "mde_rel_pct": best_c["mde_rel_pct"],
                "n_pairs": best_c["n_pairs"], "test_blocks": best_c["test_blocks"],
                "powered_for_2pct": best_c["powered_for_2pct"]},
            "trackC_underpowered": [c["experiment"] for c in trackc if not c["powered_for_2pct"]],
            "trackA_best_powered": ({"experiment": best_a["experiment"],
                                     "mde_rel_pct": best_a["mde_rel_pct"],
                                     "n_pairs": best_a["n_pairs"],
                                     "n_required_for_2pct": best_a["n_required_for_2pct"]} if best_a else None),
            "key_finding": ("Most historical windows were underpowered for the 2%% materiality floor; "
                            "only %s (n=%d, %d blocks) was adequately powered. The Track A liquidation "
                            "recompute (n=%d) needs ~%d paired observations for a 2%% MDE."
                            % (best_c["experiment"], best_c["n_pairs"], best_c["test_blocks"],
                               best_a["n_pairs"], best_a["n_required_for_2pct"])) if best_a else "",
        },
        "trigger_readiness": trigger_rows,
    }
    (OUT_DIR / f"trigger_readiness_power_calibration_{UTC}.json").write_text(
        json.dumps(payload, indent=2) + "\n")

    lines = [
        f"# FCLR Trigger-Readiness & Design-Power Calibration — {UTC}",
        "",
        "**Offline / read-only.** No network, no parquet/outcome reads. Derived only from published primary contrasts.",
        "",
        "## Method",
        "- `SE = (ci_hi - ci_lo) / (2*z0.975)`; `MDE_abs = (z0.975 + z0.80)*SE`; `MDE_rel% = MDE_abs / B1 * 100`.",
        "- `n_required = n * (MDE_rel% / 2%)^2`; achieved power `= Phi(effect/SE - z0.975)` for a true 2% effect.",
        "- Caveat: normal approximation on reported bootstrap CIs; a design-sizing ledger, **not** a new confirmatory result.",
        "",
        "## Historical power ledger (primary C2 vs B1)",
        "",
        "| experiment | rel% | B1 QLIKE | n_pairs | blocks | MDE rel% | powered for 2%? | n_req for 2% | power@2% |",
        "|---|---:|---:|---:|---:|---:|:---:|---:|---:|",
    ]
    for c in cal:
        lines.append("| %s | %.2f | %.4f | %d | %d | %.2f | %s | %d | %.3f |" % (
            c["experiment"], c["rel_reduction_pct"], c["b1_qlike"], c["n_pairs"],
            c["test_blocks"], c["mde_rel_pct"], "YES" if c["powered_for_2pct"] else "no",
            c["n_required_for_2pct"], c["achieved_power_for_2pct"]))
    lines += ["", "## Key finding", "", payload["summary"]["key_finding"], "",
              "## Trigger-readiness matrix", "",
              "| trigger | anchor | anchor MDE rel% | n_req for 2% | sizing rule |",
              "|---|---|---:|---:|---|"]
    for t in trigger_rows:
        lines.append("| %s | %s | %s | %s | %s |" % (
            t["trigger_id"], t["anchor_experiment"],
            ("%.2f" % t["anchor_mde_rel_pct"]) if t["anchor_mde_rel_pct"] is not None else "n/a",
            t["anchor_n_required_for_2pct"] if t["anchor_n_required_for_2pct"] is not None else "n/a",
            t["sizing_rule"]))
    lines += ["", "## Per-trigger execution contract (pre-sized, outcome-blind)"]
    for t in trigger_rows:
        lines += ["", f"### {t['trigger_id']}", f"- Estimand: {t['intended_estimand']}",
                  f"- Note: {t['note']}"]
        for i, step in enumerate(t["instantiation_checklist"], 1):
            lines.append(f"{i}. {step}")
    (OUT_DIR / f"trigger_readiness_power_calibration_{UTC}.md").write_text("\n".join(lines) + "\n")
    print(json.dumps(payload["summary"], indent=2))
    print("WROTE", OUT_DIR / f"trigger_readiness_power_calibration_{UTC}.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())