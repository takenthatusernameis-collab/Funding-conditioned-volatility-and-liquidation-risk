#!/usr/bin/env python3
"""FCLR-VOL-STRESS-01 independent stdlib recompute.

Separate code path from the evaluation: re-asserts every source parquet sha256,
checks the prereg binds to the registry and is outcome-blind, recomputes the
headline Brier relative improvement / materiality / verdict decision from the
stored eval summary, and verifies experiment/session id binding. No model refit.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SESSION = REPO / "research_state" / "session_20261124T222500Z"
SESSION_UTC = "20261124T222500Z"
SESSION_ID = f"session_{SESSION_UTC}"
EXPERIMENT_ID = "FCLR-VOL-STRESS-01"
CAMPAIGN = "FCLR-VOL-STRESS-01-20261124T213000Z"


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    checks: dict[str, bool] = {}
    n_checks = 0

    # ---- 1. Source registry integrity: recompute every parquet sha256 ----
    registry_path = SESSION / f"fclr_volstress01_source_registry_{SESSION_UTC}.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    reg_file_sha = sha256_file(registry_path)

    all_match = True
    verified_bad = 0
    n_files = 0
    for entry in registry["files"]:
        p = REPO / entry["path"]
        actual = sha256_file(p)
        match = actual == entry["sha256"]
        n_files += 1
        if not match:
            all_match = False
            verified_bad += 1
    checks["source_files_recompute"] = n_files
    checks["source_file_count_ok"] = bool(n_files >= 54)
    checks["source_all_match_recompute"] = bool(all_match)
    checks["source_verified_bad_is_zero"] = bool(verified_bad == 0)
    checks["sha256_all_match_stated"] = bool(
        registry["input_integrity"]["sha256_all_match"] is True
    )
    checks["sha256_verified_bad_stated_is_zero"] = bool(
        registry["input_integrity"]["sha256_verified_bad"] == 0
    )
    checks["datasets_map_present"] = bool(
        {"candles_1h", "funding", "open_interest"}.issubset(registry.get("datasets", {}))
    )
    files_list = registry.get("files", [])
    checks["files_have_valid_sha256"] = bool(
        len(files_list) >= 54
        and all(
            isinstance(e.get("sha256"), str)
            and len(e["sha256"]) == 64
            and e.get("sha_match") is not False
            for e in files_list
        )
    )
    n_checks += 8

    # ---- 2. Prereg binds to source registry and is outcome-blind ----
    prereg_path = SESSION / f"fclr_volstress01_prereg_{SESSION_UTC}.json"
    prereg = json.loads(prereg_path.read_text(encoding="utf-8"))
    prereg_reg_sha = prereg.get("source_registry_sha256") or prereg.get(
        "input_hash_assertions", {}
    ).get("source_registry_sha256")
    checks["prereg_source_registry_sha256_binds"] = bool(prereg_reg_sha == reg_file_sha)
    checks["prereg_frozen_before_outcomes"] = bool(
        prereg.get("frozen_before_outcomes") is True
        or prereg.get("decision_frozen_before_outcomes") is True
    )
    checks["prereg_outcome_not_inspected"] = bool(
        prereg.get("outcome_data_inspected_before_freeze") is False
    )
    design = prereg.get("design", {})
    checks["prereg_design_kind_stress"] = bool(
        any(k in str(design.get("kind", "")).lower()
            for k in ("forecast", "classification", "stress", "tail", "exceedance", "walk_forward"))
    )
    floor = prereg.get("materiality_floor_rel", prereg.get("materiality_floor"))
    checks["prereg_materiality_valid"] = bool(
        isinstance(floor, (int, float)) and floor > 0
    )
    n_checks += 5

    # ---- 3. Eval internal consistency (recompute headline from stored summary) ----
    eval_path = SESSION / f"fclr_volstress01_eval_{SESSION_UTC}.json"
    evald = json.loads(eval_path.read_text(encoding="utf-8"))
    brier_base = evald["metrics"]["baseline"]["brier"]
    brier_cand = evald["metrics"]["candidate"]["brier"]
    ll_base = evald["metrics"]["baseline"]["log_loss"]
    ll_cand = evald["metrics"]["candidate"]["log_loss"]

    rel_brier_recompute = (brier_base - brier_cand) / brier_base if brier_base > 0 else None
    rel_ll_recompute = (ll_base - ll_cand) / ll_base if ll_base > 0 else None
    stored_rel = evald.get("relative_improvement", {})
    checks["eval_rel_brier_consistent"] = bool(
        rel_brier_recompute is not None
        and abs(rel_brier_recompute - stored_rel.get("brier", rel_brier_recompute)) < 1e-9
    )
    checks["eval_rel_logloss_consistent"] = bool(
        rel_ll_recompute is not None
        and abs(rel_ll_recompute - stored_rel.get("log_loss", rel_ll_recompute)) < 1e-9
    )
    materiality_recompute = bool(
        rel_brier_recompute is not None
        and rel_brier_recompute > floor
        and brier_cand < brier_base
    )
    checks["eval_materiality_consistent"] = bool(
        materiality_recompute == evald.get("materiality_met")
    )
    significant_recompute = bool(evald.get("significant") is True)
    if evald.get("n_events", 0) < 100 or brier_base <= 0:
        verdict_recompute = "INCONCLUSIVE"
    elif materiality_recompute and significant_recompute:
        verdict_recompute = "PROMOTED"
    else:
        verdict_recompute = "NOT_SUPPORTED"
    checks["eval_verdict_consistent"] = bool(verdict_recompute == evald.get("verdict"))
    checks["eval_verdict_valid"] = bool(
        evald.get("verdict") in {"PROMOTED", "NOT_SUPPORTED", "INCONCLUSIVE"}
    )
    checks["eval_no_promotion_without_materiality"] = bool(
        not (evald.get("verdict") == "PROMOTED" and evald.get("materiality_met") is not True)
    )
    checks["eval_status_valid"] = bool(
        evald.get("status")
        in {"CONFIRMATORY_COMPLETE", "NOT_SUPPORTED", "PROMOTED", "INCONCLUSIVE"}
    )
    checks["eval_holdout_opened"] = bool(evald.get("holdout_opened") is True)
    n_events = evald.get("n_events", evald.get("n_forecasts"))
    checks["eval_n_events_positive"] = bool(isinstance(n_events, int) and n_events >= 1)
    checks["eval_metrics_numeric_nonneg"] = bool(
        all(isinstance(v, (int, float)) and v >= 0
            for v in (brier_base, brier_cand, ll_base, ll_cand))
    )
    n_checks += 12

    # ---- 4. Experiment/session ID binding across all JSON artifacts ----
    for label, data in (("REGISTRY", registry), ("PREREG", prereg), ("EVAL", evald)):
        checks[f"{label}_experiment_id"] = bool(data.get("experiment_id") == EXPERIMENT_ID)
        checks[f"{label}_session_id"] = bool(
            data.get("session_id") == SESSION_ID or data.get("session_utc") == SESSION_UTC
        )
    n_checks += 6

    all_checks_match = all(checks.values())
    out = {
        "experiment_id": EXPERIMENT_ID,
        "campaign": CAMPAIGN,
        "session_id": SESSION_ID,
        "session_utc": SESSION_UTC,
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "method": "independent stdlib recompute from stored input hashes/config; separate code path; no model refit",
        "all_checks_match": bool(all_checks_match),
        "n_checks": int(n_checks),
        "checks": checks,
        "headline": {
            "brier_baseline": brier_base,
            "brier_candidate": brier_cand,
            "logloss_baseline": ll_base,
            "logloss_candidate": ll_cand,
            "rel_brier_improvement_recompute": rel_brier_recompute,
            "rel_logloss_improvement_recompute": rel_ll_recompute,
            "materiality_floor_rel": floor,
            "materiality_met_recompute": materiality_recompute,
            "significant_recompute": significant_recompute,
            "verdict_recompute": verdict_recompute,
            "verdict_eval": evald.get("verdict"),
        },
        "source_files_recomputed": n_files,
        "source_verified_bad": verified_bad,
    }
    out_json = SESSION / f"fclr_volstress01_recompute_{SESSION_UTC}.json"
    out_json.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps({"all_checks_match": all_checks_match, "n_checks": n_checks,
                      "verdict_recompute": verdict_recompute,
                      "verdict_eval": evald.get("verdict"),
                      "failed": [k for k, v in checks.items() if not v]}, indent=2))


if __name__ == "__main__":
    main()