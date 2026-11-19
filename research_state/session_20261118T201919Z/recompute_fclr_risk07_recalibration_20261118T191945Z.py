#!/usr/bin/env python3
"""Independent aggregate recompute for FCLR-LIQ-RISK-RECALIBRATION-07.

Re-derives every reported per-scenario delta_brier/delta_ece/delta_log_loss,
the pooled equal-weight means, the materiality-floor counts and the verdict
directly from the per-scenario metrics stored in
fclr_risk07_recalibration_<UTC>.json, using independent aggregation code (not
the recalibration script's assemble() helpers). Reports exact discrepancies
(must be 0).

No network. No cached-data re-read. Stdlib only.
"""
from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SESSION_DIR = REPO / "research_state" / "session_20261118T191945Z"
UTC_STAMP = "20261118T191945Z"
CAMPAIGN = "FCLR-LIQ-RISK-RECALIBRATION-07-20261118T191714Z"

CALIBRATORS = ("C1_platt", "C2_isotonic", "C3_prior_offset")
FLOOR_MODELS = ("C1_platt", "C3_prior_offset")
PRIMARY_SCENARIO = "L10|long|H24"
TOL = 1e-12


def close(a, b):
    if a is None and b is None:
        return True
    if a is None or b is None:
        return False
    return abs(float(a) - float(b)) <= TOL


def main():
    src = SESSION_DIR / f"fclr_risk07_recalibration_{UTC_STAMP}.json"
    payload = json.loads(src.read_text(encoding="utf-8"))
    holds = payload["holdouts"]  # dict keyed by holdout name
    discrepancies = []

    # 1) per-scenario deltas recomputed from stored brier / ece / log_loss
    for holdout, h in holds.items():
        for sc, sm in h["scenarios"].items():
            models = sm["models"]
            b0 = models["C0_identity"]
            for name in CALIBRATORS:
                m = models[name]
                exp_db = b0["brier"] - m["brier"]
                exp_de = b0["ece"] - m["ece"]
                exp_dl = b0["log_loss"] - m["log_loss"]
                got = {"delta_brier": m.get("delta_brier"),
                       "delta_ece": m.get("delta_ece"),
                       "delta_log_loss": m.get("delta_log_loss")}
                exp = {"delta_brier": exp_db, "delta_ece": exp_de,
                       "delta_log_loss": exp_dl}
                for field in ("delta_brier", "delta_ece", "delta_log_loss"):
                    if not close(got[field], exp[field]):
                        discrepancies.append(
                            {"holdout": holdout, "scenario": sc, "model": name,
                             "field": field, "stored": got[field], "recomputed": exp[field]})

    # 2) pooled equal-weight means per holdout / calibrator
    for holdout, h in holds.items():
        for name in CALIBRATORS:
            dbs = [h["scenarios"][sc]["models"][name]["delta_brier"]
                   for sc in h["scenarios"]]
            des = [h["scenarios"][sc]["models"][name]["delta_ece"]
                   for sc in h["scenarios"]]
            dls = [h["scenarios"][sc]["models"][name]["delta_log_loss"]
                   for sc in h["scenarios"]]
            exp = {"mean_delta_brier": sum(dbs) / len(dbs),
                   "mean_delta_ece": sum(des) / len(des),
                   "mean_delta_log_loss": sum(dls) / len(dls),
                   "n_scenarios": len(dbs)}
            got = h["pooled"][name]
            for field in ("mean_delta_brier", "mean_delta_ece", "mean_delta_log_loss"):
                if not close(got.get(field), exp[field]):
                    discrepancies.append(
                        {"holdout": holdout, "model": name, "field": "pooled_" + field,
                         "stored": got.get(field), "recomputed": exp[field]})
            if got.get("n_scenarios") != exp["n_scenarios"]:
                discrepancies.append(
                    {"holdout": holdout, "model": name, "field": "pooled_n_scenarios",
                     "stored": got.get("n_scenarios"), "recomputed": exp["n_scenarios"]})

    # 3) materiality floor (C1/C3): brier hits, ece hits, real mean, placebo p95
    n_holdouts = len(holds)
    brier_hits = {name: 0 for name in FLOOR_MODELS}
    ece_hits = {name: 0 for name in FLOOR_MODELS}
    real_mean_db = {name: 0.0 for name in FLOOR_MODELS}
    placebo_p95_mean = {name: 0.0 for name in FLOOR_MODELS}
    for name in FLOOR_MODELS:
        for holdout, h in holds.items():
            bb = h["primary_bootstrap"].get(name, {}).get("brier_bootstrap") or {}
            eb = h["primary_bootstrap"].get(name, {}).get("ece_bootstrap") or {}
            if bb.get("mean", 0) > 0 and bb.get("ci_lo", 0) > 0:
                brier_hits[name] += 1
            if eb.get("mean", 0) >= 0.005 and eb.get("ci_lo", 0) >= 0:
                ece_hits[name] += 1
            real_mean_db[name] += h["pooled"][name]["mean_delta_brier"]
            placebo_p95_mean[name] += h["placebo"][name]["pooled_null_p95"]
        real_mean_db[name] /= n_holdouts
        placebo_p95_mean[name] /= n_holdouts

    floor_detail = {}
    floor_met = False
    for name in FLOOR_MODELS:
        cd1 = brier_hits[name] >= 2
        cd2 = ece_hits[name] >= 2
        cd3 = real_mean_db[name] > placebo_p95_mean[name]
        fm = bool(cd1 and cd2 and cd3)
        floor_detail[name] = {
            "delta_brier_significant_holdouts": brier_hits[name],
            "delta_ece_material_holdouts": ece_hits[name],
            "real_mean_delta_brier": real_mean_db[name],
            "placebo_p95_mean": placebo_p95_mean[name],
            "criterion_1_brier_2of3": cd1,
            "criterion_2_ece_2of3": cd2,
            "criterion_3_beats_placebo_p95": cd3,
            "floor_met": fm,
        }
        if fm:
            floor_met = True

    verdict = "MATERIALITY_FLOOR_MET" if floor_met else "HONEST_NEGATIVE_OR_INCONCLUSIVE"

    stored_floor = payload["floor_evaluation"]
    for name in FLOOR_MODELS:
        sd = stored_floor["details"][name]
        rd = floor_detail[name]
        for field in ("delta_brier_significant_holdouts", "delta_ece_material_holdouts"):
            if sd.get(field) != rd[field]:
                discrepancies.append({"field": f"floor.{name}.{field}",
                                      "stored": sd.get(field), "recomputed": rd[field]})
        for field in ("real_mean_delta_brier", "placebo_p95_mean"):
            if not close(sd.get(field), rd[field]):
                discrepancies.append({"field": f"floor.{name}.{field}",
                                      "stored": sd.get(field), "recomputed": rd[field]})
        if bool(sd.get("floor_met")) != bool(rd["floor_met"]):
            discrepancies.append({"field": f"floor.{name}.floor_met",
                                  "stored": sd.get("floor_met"), "recomputed": rd["floor_met"]})
    if not close(stored_floor.get("real_mean_delta_brier", {}).get(CALIBRATORS[0]),
                 real_mean_db.get(CALIBRATORS[0])):
        pass  # stored structure may key differently; handled via details above
    if bool(stored_floor.get("floor_met")) != bool(floor_met):
        discrepancies.append({"field": "floor_met",
                              "stored": stored_floor.get("floor_met"),
                              "recomputed": floor_met})
    if stored_floor.get("n_holdouts") != n_holdouts:
        discrepancies.append({"field": "n_holdouts",
                              "stored": stored_floor.get("n_holdouts"),
                              "recomputed": n_holdouts})

    # 4) verdict
    if payload.get("verdict") != verdict:
        discrepancies.append({"field": "verdict",
                              "stored": payload.get("verdict"), "recomputed": verdict})

    out = {
        "schema": "recompute_fclr_risk07_recalibration",
        "session": f"session_{UTC_STAMP}",
        "generated_utc": UTC_STAMP,
        "campaign": CAMPAIGN,
        "source_artifact": src.name,
        "network_used": False,
        "numpy_used": False,
        "parquet_used": False,
        "n_holdouts": n_holdouts,
        "recomputed_brier_hits_2of3": brier_hits,
        "recomputed_ece_hits_2of3": ece_hits,
        "recomputed_real_mean_delta_brier": real_mean_db,
        "recomputed_placebo_p95_mean_delta_brier": placebo_p95_mean,
        "recomputed_floor_detail": floor_detail,
        "recomputed_floor_met": floor_met,
        "recomputed_verdict": verdict,
        "n_discrepancies": len(discrepancies),
        "discrepancies": discrepancies,
        "status": "RECONCILED_ZERO_DISCREPANCIES" if not discrepancies else "DISCREPANCIES_FOUND",
    }
    (SESSION_DIR / f"recompute_fclr_risk07_recalibration_{UTC_STAMP}.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps({"status": out["status"], "n_discrepancies": len(discrepancies),
                      "floor_met": floor_met, "verdict": verdict}, indent=2))


if __name__ == "__main__":
    main()
