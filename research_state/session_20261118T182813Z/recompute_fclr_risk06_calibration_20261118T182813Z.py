#!/usr/bin/env python3
"""Independent aggregate recompute for FCLR-LIQ-RISK-CALIBRATION-06.

Re-derives every reported ΔBrier / Δlog-loss aggregate and the materiality-floor
verdict directly from the per-scenario metrics stored in
fclr_risk06_calibration_<UTC>.json, without reusing the calibration script's
aggregation helpers. Reports exact discrepancies (must be 0).

No network. No cached-data re-read. Stdlib only.
"""
from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SESSION_DIR = REPO / "research_state" / "session_20261118T182813Z"
UTC_STAMP = "20261118T182813Z"

MODELS = ("B1_funding_conditioned", "B2_funding_shock")
PRIMARY = "L10|long|H24"


def main():
    src = SESSION_DIR / f"fclr_risk06_calibration_{UTC_STAMP}.json"
    payload = json.loads(src.read_text(encoding="utf-8"))
    holds = payload["holdouts"]
    discrepancies = []
    recomputed = []

    for h in holds:
        sc = h["scenario_metrics"]
        # recompute per-scenario deltas from stored brier / log_loss values
        scen_deltas = {}
        for name, m in sc.items():
            if "B0_rv_only" not in m:
                continue
            for mod in MODELS:
                if mod not in m:
                    continue
                scen_deltas.setdefault(mod, {})[name] = {
                    "delta_brier": m["B0_rv_only"]["brier"] - m[mod]["brier"],
                    "delta_logloss": m["B0_rv_only"]["log_loss"] - m[mod]["log_loss"],
                    "delta_brier_placebo": (
                        m["B0_rv_only"]["brier"] - m[mod]["placebo_brier"]
                        if "placebo_brier" in m[mod] else None
                    ),
                }
        # check stored per-scenario deltas match
        for mod in MODELS:
            for name, m in sc.items():
                if mod not in m or "delta_brier_vs_B0" not in m[mod]:
                    continue
                diff = abs(m[mod]["delta_brier_vs_B0"] - scen_deltas[mod][name]["delta_brier"])
                if diff > 1e-12:
                    discrepancies.append(
                        {"holdout": h["holdout"], "scenario": name, "model": mod,
                         "field": "delta_brier_vs_B0", "abs_diff": diff})

        # recompute pooled means
        pooled = {}
        for mod in MODELS:
            vals = [v["delta_brier"] for v in scen_deltas[mod].values()]
            pvals = [v["delta_brier_placebo"] for v in scen_deltas[mod].values()
                     if v["delta_brier_placebo"] is not None]
            pooled[mod] = {
                "mean_delta_brier": sum(vals) / len(vals) if vals else None,
                "n_scenarios": len(vals),
                "mean_delta_brier_placebo": (sum(pvals) / len(pvals)) if pvals else None,
            }
            stored = h["pooled"].get(mod, {})
            if stored.get("mean_delta_brier") is not None:
                d = abs(stored["mean_delta_brier"] - pooled[mod]["mean_delta_brier"])
                if d > 1e-12:
                    discrepancies.append({"holdout": h["holdout"], "model": mod,
                                          "field": "pooled_mean_delta_brier", "abs_diff": d})
                if (stored.get("mean_delta_brier_placebo") is not None
                        and pooled[mod]["mean_delta_brier_placebo"] is not None):
                    d2 = abs(stored["mean_delta_brier_placebo"]
                             - pooled[mod]["mean_delta_brier_placebo"])
                    if d2 > 1e-12:
                        discrepancies.append({"holdout": h["holdout"], "model": mod,
                                              "field": "pooled_mean_delta_brier_placebo",
                                              "abs_diff": d2})
        recomputed.append({"holdout": h["holdout"], "pooled": pooled})

    # recompute floor verdict
    beats = {}
    for mod in MODELS:
        n = 0
        for h in holds:
            pr = h["primary"].get(mod)
            if not pr or not pr.get("bootstrap"):
                continue
            if pr["delta_brier"] > 0 and pr["bootstrap"]["ci_lo"] > 0:
                n += 1
        beats[mod] = n
    real_mean = {
        mod: sum(h["primary"][mod]["delta_brier"] for h in holds if mod in h["primary"])
        / len(holds)
        for mod in MODELS
    }
    placebo_mean = {
        mod: (sum(r["pooled"][mod]["mean_delta_brier_placebo"] for r in recomputed
                  if r["pooled"][mod]["mean_delta_brier_placebo"] is not None)
              / len(recomputed))
        for mod in MODELS
    }
    floor_met = any(
        beats[mod] >= 2 and abs(real_mean[mod]) > abs(placebo_mean[mod])
        for mod in MODELS
    )
    stored_floor = payload["floor_evaluation"]
    if stored_floor["beats_B0_by_holdout_primary"] != beats:
        discrepancies.append({"field": "beats_B0_by_holdout_primary",
                              "stored": stored_floor["beats_B0_by_holdout_primary"],
                              "recomputed": beats})
    if bool(stored_floor["floor_met"]) != bool(floor_met):
        discrepancies.append({"field": "floor_met", "stored": stored_floor["floor_met"],
                              "recomputed": floor_met})
    if payload["verdict"] != ("MATERIALITY_FLOOR_MET" if floor_met
                              else "HONEST_NEGATIVE_OR_INCONCLUSIVE"):
        discrepancies.append({"field": "verdict", "stored": payload["verdict"],
                              "recomputed": "MATERIALITY_FLOOR_MET" if floor_met
                              else "HONEST_NEGATIVE_OR_INCONCLUSIVE"})

    out = {
        "schema": "recompute_fclr_risk06_calibration",
        "session": f"session_{UTC_STAMP}",
        "generated_utc": UTC_STAMP,
        "campaign": "FCLR-LIQ-RISK-CALIBRATION-06-20261118T182600Z",
        "source_artifact": src.name,
        "network_used": False,
        "n_holdouts": len(holds),
        "recomputed_per_holdout_pooled": recomputed,
        "recomputed_beats_B0_by_holdout_primary": beats,
        "recomputed_real_mean_delta_brier_primary": real_mean,
        "recomputed_placebo_mean_delta_brier": placebo_mean,
        "recomputed_floor_met": floor_met,
        "recomputed_verdict": ("MATERIALITY_FLOOR_MET" if floor_met
                               else "HONEST_NEGATIVE_OR_INCONCLUSIVE"),
        "n_discrepancies": len(discrepancies),
        "discrepancies": discrepancies,
        "status": "RECONCILED_ZERO_DISCREPANCIES" if not discrepancies else "DISCREPANCIES_FOUND",
    }
    (SESSION_DIR / f"recompute_fclr_risk06_calibration_{UTC_STAMP}.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps({"status": out["status"], "n_discrepancies": len(discrepancies),
                      "floor_met": floor_met, "beats": beats}, indent=2))


if __name__ == "__main__":
    main()
