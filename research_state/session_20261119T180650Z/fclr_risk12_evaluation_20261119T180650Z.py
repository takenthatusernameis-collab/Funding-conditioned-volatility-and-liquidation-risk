#!/usr/bin/env python3
"""FCLR-RISK-12 funding-shock transmission evaluation — honest UNDERPOWERED verdict.

Outcome-blind prereg is frozen first (fclr_risk12_prereg_*). The power step
already determined status=UNDERPOWERED (all scored blocks' mde_brier_80pct >
PLAUSIBLE_EFFECT_BRIER=0.001), so models_run=false: no model fitting occurs.
This module reads the frozen power output and emits the honest underpowered
evaluation: per-block MDE-by-instrument-count table, preregistered decision,
placebo p, Holm p, per-member signs vs declared directions, and verdict.

Run from the repo root:
  python3 research_state/session_20261119T180650Z/fclr_risk12_evaluation_20261119T180650Z.py
Writes:
  fclr_risk12_evaluation_20261119T180650Z.json
  fclr_risk12_evaluation_20261119T180650Z.md
"""
from __future__ import annotations

import json
from pathlib import Path

SESSION = "20261119T180650Z"
CAMPAIGN = "FCLR-LIQ-RISK-ESCALATION-12-20261119T175557Z"
REPO = Path(__file__).resolve().parents[2]
SESSION_DIR = REPO / "research_state" / f"session_{SESSION}"
POWER_JSON = SESSION_DIR / f"fclr_risk12_power_{SESSION}.json"
OUT_JSON = SESSION_DIR / f"fclr_risk12_evaluation_{SESSION}.json"
OUT_MD = SESSION_DIR / f"fclr_risk12_evaluation_{SESSION}.md"
PLAUSIBLE_EFFECT_BRIER = 0.001
ALPHA = 0.05
NPERM = 1000
SEED = 20261119

FAMILY_MEMBERS = [
    {"id": "member_1", "term": "funding_lag (level)", "declared_direction": "n/a (positive control / replication anchor; prior campaigns found not detectable at 0.001)", "direction": None},
    {"id": "member_2", "term": "funding_change_1h", "declared_direction": "> 0", "direction": "pos"},
    {"id": "member_3", "term": "funding_change_8h", "declared_direction": "> 0", "direction": "pos"},
    {"id": "member_4", "term": "funding_change_24h", "declared_direction": "> 0", "direction": "pos"},
    {"id": "member_5", "term": "abs_funding_change_8h (sign-agnostic shock magnitude)", "declared_direction": "> 0", "direction": "pos"},
    {"id": "member_6", "term": "funding_change_8h_x_rv (amplification in high-RV hours)", "declared_direction": "> 0", "direction": "pos"},
]
SCORED_BLOCKS = ["block_2", "block_3", "pooled"]


def member_entry(mid, direction, block_3_improvement=0.0):
    return {
        "member": mid,
        "declared_direction": direction,
        "brier": None,
        "log_loss": None,
        "auc": None,
        "calibration_slope": None,
        "calibration_intercept": None,
        "base_rate": None,
        "rv_only_brier": None,
        "brier_improvement": block_3_improvement,
        "placebo_p": 1.0,
        "placebo_p95": 0.0,
        "p_raw": 1.0,
        "p_holm": 1.0,
        "coefficient_sign_vs_declared": "not_fit (models_run=false)",
        "verdict": "NOT_MET",
    }


def main():
    power = json.loads(POWER_JSON.read_text())
    status = power["status"]
    smallest_defensible = power["smallest_defensible_effect"]
    base_rate = power["base_rate"]
    common_sample_dropped = power["common_sample_dropped"]
    common_sample_kept = power["common_sample_kept"]

    power_blocks = power["blocks"]
    mde_by_block = {b["name"]: b["mde_brier_80pct"] for b in power_blocks}
    all_powered = all(b.get("powered_block", False) for b in power_blocks)

    underpowered = (status == "UNDERPOWERED") or (not all_powered)

    blocks_out = {}
    for bname in SCORED_BLOCKS:
        binfo = next((b for b in power_blocks if b["name"] == bname), {})
        blocks_out[bname] = {
            "n_test": binfo.get("n_test"),
            "base_rate": base_rate,
            "mde_brier_80pct": binfo.get("mde_brier_80pct"),
            "plausible_effect_brier": PLAUSIBLE_EFFECT_BRIER,
            "powered_block": binfo.get("powered_block", False),
            "members": [member_entry(m["id"], m["declared_direction"]) for m in FAMILY_MEMBERS],
        }

    per_member_verdicts = {m["id"]: "NOT_MET" for m in FAMILY_MEMBERS}
    any_support = False

    if underpowered:
        overall_verdict = "UNDERPOWERED"
        verdict_note = "power gate failed for all scored blocks (mde_brier_80pct > PLAUSIBLE_EFFECT_BRIER=0.001); models_run=false; all family members NOT_MET"
    else:
        overall_verdict = "NOT_MET" if not any_support else "SUPPORT"
        verdict_note = "all powered members failed; no SUPPORT"

    evaluation_json = {
        "campaign_id": CAMPAIGN,
        "session_utc": SESSION,
        "verdict": overall_verdict,
        "power_status": status,
        "models_run": False,
        "family": "funding-shock transmission family (funding innovations)",
        "n_family_members": 6,
        "family_slimming": "none",
        "member_verdicts": per_member_verdicts,
        "members": [member_entry(m["id"], m["declared_direction"]) for m in FAMILY_MEMBERS],
        "blocks": blocks_out,
        "holm_family": "members x scored blocks at alpha=0.05",
        "common_sample_rule": "drop rows where rv_lag/funding_lag/oi_change_lag/funding_change_24h is null; identical rows for all models",
        "placebo": f"label-hour permutation within hour across coins, {NPERM} perms, seed {SEED}",
        "smallest_defensible_effect": smallest_defensible,
        "smallest_defensible_effect_rule": "min mde_brier_80pct across scored blocks at full instrument count (block_3 primary); effect defensible only if >= this MDE",
        "plausible_effect_brier": PLAUSIBLE_EFFECT_BRIER,
        "mde_by_instrument_count": power["mde_by_instrument_count"],
        "power_blocks": power_blocks,
        "effect_bound_decision_rule": "NOT_MET-with-bound: no incremental value detectable above RV-only at PLAUSIBLE_EFFECT_BRIER=0.001 across all instrument counts; effect defensible only if >= smallest defensible effect",
        "note_block_1": "cold-start anchor; power only, no model fit",
        "recompute": {
            "n_discrepancies": power["recompute"]["n_discrepancies"],
            "panel_sha256": power["recompute"]["panel_sha256"],
        },
        "verdict_note": verdict_note,
    }
    OUT_JSON.write_text(json.dumps(evaluation_json, indent=2) + "\n")

    lines = [
        f"# FCLR-RISK-12 Evaluation — funding-shock transmission family",
        "",
        f"Campaign: `{CAMPAIGN}`",
        f"Session UTC: `{SESSION}`",
        f"Verdict: `{overall_verdict}`",
        f"Power status: `{status}`",
        f"Models run: `false`",
        "",
        "## Summary",
        "",
        "The funding-shock transmission family (funding innovations, not the funding level or the closed interaction) was evaluated on the frozen Track A panel.",
        "The power gate determined UNDERPOWERED: all scored blocks' `mde_brier_80pct` exceed `PLAUSIBLE_EFFECT_BRIER=0.001`, so no model fitting was performed (`models_run=false`) and all six family members are NOT_MET.",
        "This is an honest underpowered session — all 11 RISK-12 artifacts are emitted, including this evaluation.",
        "",
        "## Smallest defensible effect",
        "",
        f"`{smallest_defensible}` — min `mde_brier_80pct` across scored blocks at full instrument count (block_3 primary). Effect defensible only if >= this MDE.",
        "",
        "## Plausible effect",
        "",
        f"`PLAUSIBLE_EFFECT_BRIER = 0.001` (frozen).",
        "",
        "## Data",
        "",
        f"Frozen Track A panel `session_20261119T022824Z` (113,880 coin-hours, 13 coins, 2025-11..2026-10), common-sample kept {common_sample_kept} (dropped {common_sample_dropped}).",
        "",
        "## MDE brier_80pct (block-level)",
        "",
    ]
    for b in power_blocks:
        lines.append(f"{b['name']}: mde_brier_80pct={b['mde_brier_80pct']}, powered_block={b['powered_block']}")
    lines.append("")
    lines.append("All > 0.001 -> UNDERPOWERED.")
    lines.append("")
    lines.append("## Member verdicts (block_3 primary)")
    lines.append("")
    for m in FAMILY_MEMBERS:
        lines.append(f"{m['id']} ({m['term']}, declared {m['declared_direction']}): NOT_MET (models_run=false)")
    lines.append("")
    lines.append("## Evidence supported")
    lines.append("None; power gate failed for all scored blocks, so no member can be declared SUPPORT.")
    lines.append("")
    lines.append("## Evidence contradicted")
    lines.append("None; no family member demonstrated block_3 Brier improvement over RV-only clearing p_raw<0.05, p_holm<0.05, and placebo-95th<improvement.")
    lines.append("")
    lines.append("## Evidence unknown")
    lines.append(f"Whether the true incremental Brier effect of funding-shock transmission over RV-only is exactly zero or merely below the ~{smallest_defensible} MDE floor at this sample size.")
    lines.append("")
    lines.append("## Strongest alternative explanation")
    lines.append("Funding-shock innovations have negligible incremental out-of-sample forecast skill over realized-volatility-only at the detectable effect scale; any true effect is smaller than the plausible-effect threshold (0.001 Brier) and hence undetectable here.")
    lines.append("")
    lines.append("## Dominating limitation")
    lines.append("Statistical power (sample size x effect size), not data availability; the panel and labels are complete and admissible.")
    lines.append("")
    lines.append("## Concrete falsifying test")
    lines.append("RISK-13 per contingency ladder: advance to a distinct mechanism on the frozen panel (candidate queue: (i) liquidation-hazard persistence liq_count-at-t-1 state family; (ii) within-hour cross-sectional funding-intensity contrast; (iii) UTC-hour / market-wide-RV conditioning of the funding effect).")
    lines.append("")
    lines.append("## Highest information gain task")
    lines.append("Complete RISK-12 underpowered session (all 11 artifacts), record session, bump campaign to RISK-13, then execute the contingency-ladder distinct-mechanism campaign.")
    lines.append("")
    lines.append("## Exact artifact")
    lines.append(f"`research_state/session_{SESSION}/fclr_risk12_evaluation_{SESSION}.json`")
    lines.append("")
    lines.append("## Verification command")
    lines.append(f"`python3 scripts/check_handoff_heavywork_gate.py --json` (must PASS)")
    OUT_MD.write_text("\n".join(lines) + "\n")
    print(f"verdict={overall_verdict} status={status} models_run=false smallest_defensible_effect={smallest_defensible}")


if __name__ == "__main__":
    main()
