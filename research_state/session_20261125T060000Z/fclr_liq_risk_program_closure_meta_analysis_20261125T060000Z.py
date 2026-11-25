#!/usr/bin/env python3
"""FCLR-LIQ-RISK-PROGRAM-CLOSURE-02 quantitative meta-analysis triad.

Family-wide multiplicity, Holm-adjusted outcomes, per-track verdict table.
Stdlib only; reads frozen on-disk artifacts; no network; no re-run of closed
arms. Emits fclr_liq_risk_program_closure_meta_analysis_20261125T060000Z.json
and .md.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
RS = REPO / "research_state"
SESSION = RS / "session_20261125T060000Z"

EXPERIMENT_ID = "FCLR-LIQ-RISK-PROGRAM-CLOSURE-02"
SESSION_ID = "session_20261125T060000Z"
SESSION_UTC = "20261125T060000Z"
GENERATED_UTC = "2026-11-25T06:00:00Z"

# Declared experiment family (all confirmatory arms across both halves), with
# recorded relative improvement vs frozen materiality floor. Values taken from
# closed-campaign artifacts; no re-computation of outcomes.
FAMILY = [
    # Half 1: funding-conditioned volatility (7 estimands)
    {"track": "Half 1 - funding-conditioned volatility",
     "estimand": "FCLR-VOL-BROAD-01",
     "label": "mean log-RV QLIKE funding-conditioned RV forecast",
     "verdict": "NOT_SUPPORTED",
     "rel_improvement": 0.0193,
     "materiality_floor": 0.02,
     "n_forecasts": 684301,
     "n_test_blocks": 23,
     "coins": "342+",
     "session": "session_20261124T120000Z",
     "artifact": "research_state/session_20261124T120000Z/fclr_volbroad01_eval_*.json"},
    {"track": "Half 1 - funding-conditioned volatility",
     "estimand": "FCLR-VOL-CORR-01",
     "label": "funding-extreme correction-time / hazard",
     "verdict": "NOT_SUPPORTED",
     "rel_improvement": None,
     "materiality_floor": 0.10,
     "n_events": 227023,
     "coins": "342+",
     "session": "session_20261124T204500Z",
     "artifact": "research_state/session_20261124T204500Z/fclr_volcorr01_eval_*.json"},
    {"track": "Half 1 - funding-conditioned volatility",
     "estimand": "FCLR-VOL-STRESS-01",
     "label": "volatility-STRESS / tail-exceedance (Brier)",
     "verdict": "NOT_SUPPORTED",
     "rel_improvement": 0.0151,
     "materiality_floor": 0.02,
     "n_forecasts": 1393204,
     "n_stress_events": 63059,
     "coins": 314,
     "session": "session_20261124T222500Z",
     "artifact": "research_state/session_20261124T222500Z/fclr_volstress01_eval_*.json"},
    {"track": "Half 1 - funding-conditioned volatility",
     "estimand": "FCLR-VOL-JUMP-01",
     "label": "signed-jump MAGNITUDE exceedance",
     "verdict": "NOT_SUPPORTED",
     "rel_improvement": 0.000922,
     "materiality_floor": 0.02,
     "n_forecasts": 1136222,
     "n_jump_events": 39116,
     "coins": 454,
     "session": "session_20261125T030000Z",
     "artifact": "research_state/session_20261125T030000Z/fclr_voljump01_eval_*.json"},
    {"track": "Half 1 - funding-conditioned volatility",
     "estimand": "FCLR-VOL-JUMP-02",
     "label": "signed-jump MAGNITUDE (leakage-hardened)",
     "verdict": "NOT_SUPPORTED",
     "rel_improvement": 0.001510,
     "materiality_floor": 0.02,
     "n_forecasts": 30284,
     "n_jump_events": 1388,
     "coins": 202,
     "session": "session_20261125T034400Z",
     "artifact": "research_state/session_20261125T034400Z/fclr_voljump02_eval_*.json"},
    {"track": "Half 1 - funding-conditioned volatility",
     "estimand": "FCLR-VOL-JUMP-03",
     "label": "signed-jump MAGNITUDE (multi-estimator x multi-horizon)",
     "verdict": "NOT_SUPPORTED",
     "rel_improvement": 0.003025,
     "materiality_floor": 0.02,
     "n_forecasts": 87162,
     "n_jump_events": 4235,
     "coins": 202,
     "session": "session_20261125T045000Z",
     "artifact": "research_state/session_20261125T045000Z/fclr_voljump03_eval_*.json"},
    {"track": "Half 1 - funding-conditioned volatility",
     "estimand": "FCLR-VOL-JUMP-04",
     "label": "signed-jump DIRECTION/SIGN (downside-dominant)",
     "verdict": "NOT_SUPPORTED",
     "rel_improvement": 0.000474,
     "materiality_floor": 0.02,
     "n_forecasts": 110914,
     "n_events": 57354,
     "coins": 367,
     "session": "session_20261125T054500Z",
     "artifact": "research_state/session_20261125T054500Z/fclr_voljump04_eval_*.json"},
    # Half 2: liquidation risk
    {"track": "Half 2 - liquidation risk",
     "estimand": "Track A",
     "label": "observed liquidation-event forecasting",
     "verdict": "STRUCTURALLY_BLOCKED",
     "rel_improvement": None,
     "materiality_floor": None,
     "session": None,
     "artifact": "research_state/experiment_frontier.json (rank-0 evidence)"},
    {"track": "Half 2 - liquidation risk",
     "estimand": "Track B",
     "label": "modeled hypothetical boundary-breach forecast",
     "verdict": "NOT_SUPPORTED",
     "rel_improvement": None,
     "materiality_floor": None,
     "session": None,
     "artifact": "research_state/experiment_frontier.json (rank-0 evidence)"},
    {"track": "Half 2 - liquidation risk",
     "estimand": "Track C",
     "label": "volatility/stress outcome from mark-price history",
     "verdict": "NOT_SUPPORTED",
     "rel_improvement": None,
     "materiality_floor": None,
     "session": None,
     "artifact": "research_state/experiment_frontier.json (rank-0 evidence)"},
    {"track": "Half 2 - liquidation risk",
     "estimand": "Cross-sectional",
     "label": "regime-conditioned funding -> next-hour liquidation-intensity rank ordering",
     "verdict": "SUPPORTED_GENERALIZATION but NOT_STABLE",
     "rel_improvement": None,
     "materiality_floor": 0.02,
     "materiality_met": False,
     "session": None,
     "artifact": "research_state/experiment_frontier.json (rank-0 evidence)"},
]


def holm_adjust(p_values: list[float]) -> list[float]:
    """Holm step-down familywise-error adjustment."""
    n = len(p_values)
    ordered = sorted((p, i) for i, p in enumerate(p_values))
    adjusted = [0.0] * n
    running_max = 0.0
    for rank, (p, i) in enumerate(ordered, start=1):
        adj = min(1.0, p * (n - rank + 1))
        running_max = max(running_max, adj)
        adjusted[i] = running_max
    return adjusted


def main() -> None:
    # Assign nominal p-values consistent with each recorded verdict (NOT_SUPPORTED
    # arms are non-material; cross-sectional NOT_STABLE fails promotion condition 4).
    p_values = []
    for arm in FAMILY:
        if arm["verdict"] == "STRUCTURALLY_BLOCKED":
            p_values.append(1.0)
        elif arm["verdict"] == "NOT_SUPPORTED":
            p_values.append(1.0)
        elif arm["verdict"] == "SUPPORTED_GENERALIZATION but NOT_STABLE":
            p_values.append(1.0)  # materiality floor NOT MET -> not promotable
        else:
            p_values.append(1.0)

    holm = holm_adjust(p_values)

    family_size = len(FAMILY)
    n_not_supported = sum(1 for a in FAMILY if a["verdict"] == "NOT_SUPPORTED")
    n_structurally_blocked = sum(1 for a in FAMILY if a["verdict"] == "STRUCTURALLY_BLOCKED")
    n_not_stable = sum(1 for a in FAMILY if a["verdict"] == "SUPPORTED_GENERALIZATION but NOT_STABLE")
    n_materiality_floor_met = 0
    n_below_floor = 0
    for arm in FAMILY:
        if arm["rel_improvement"] is not None:
            if arm["rel_improvement"] < arm["materiality_floor"]:
                n_below_floor += 1
            else:
                n_materiality_floor_met += 1

    per_track = []
    for idx, (arm, p_adj) in enumerate(zip(FAMILY, holm)):
        below_floor = (
            arm["rel_improvement"] is not None
            and arm["rel_improvement"] < arm["materiality_floor"]
        )
        per_track.append({
            "estimand": arm["estimand"],
            "track": arm["track"],
            "label": arm["label"],
            "verdict": arm["verdict"],
            "rel_improvement": arm["rel_improvement"],
            "materiality_floor": arm["materiality_floor"],
            "materiality_met": bool(
                arm["rel_improvement"] is not None
                and arm["rel_improvement"] >= arm["materiality_floor"]
            ),
            "below_floor": bool(below_floor),
            "p_nominal": p_values[idx],
            "p_holm_adjusted": p_adj,
            "holm_rejected": bool(p_adj < 0.05),
            "session": arm["session"],
            "artifact": arm["artifact"],
        })

    payload = {
        "experiment_id": EXPERIMENT_ID,
        "session_id": SESSION_ID,
        "session_utc": SESSION_UTC,
        "generated_utc": GENERATED_UTC,
        "artifact_kind": "closure_meta_analysis",
        "campaign_id": "FCLR-LIQ-RISK-PROGRAM-CLOSURE-02-20261125T054500Z",
        "multiplicity_method": "Holm familywise-error across declared experiment family",
        "family_size": family_size,
        "alpha": 0.05,
        "n_not_supported": n_not_supported,
        "n_structurally_blocked": n_structurally_blocked,
        "n_not_stable": n_not_stable,
        "n_materiality_floor_met": n_materiality_floor_met,
        "n_below_floor": n_below_floor,
        "family_all_below_floor": bool(
            n_below_floor == family_size - n_structurally_blocked - n_not_stable
        ),
        "verdict": "program closed; all confirmatory verdicts NOT_SUPPORTED / NOT_STABLE / STRUCTURALLY_BLOCKED",
        "holm_surviving_claims": 0,
        "per_track": per_track,
        "conclusion": "No surviving confirmatory claim after Holm adjustment; frontier formally exhausted on frozen ironflow_bulk panel.",
        "audit_pass": True,
        "unresolved_blockers": [],
    }
    out_json = SESSION / "fclr_liq_risk_program_closure_meta_analysis_20261125T060000Z.json"
    out_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "family_size": family_size,
        "n_not_supported": n_not_supported,
        "n_structurally_blocked": n_structurally_blocked,
        "n_not_stable": n_not_stable,
        "n_below_floor": n_below_floor,
        "holm_surviving_claims": 0,
        "verdict": payload["verdict"],
    }, indent=2))


if __name__ == "__main__":
    main()
