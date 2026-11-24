#!/usr/bin/env python3
"""FCLR-VOL-CORR-01 independent stdlib recompute.

Separate code path from the evaluation: re-asserts every source parquet sha256,
checks the prereg binds to the registry and is outcome-blind, recomputes the
headline correction-time contrast / materiality / verdict decision from the stored
eval summary, and verifies experiment/session id binding. No model refit.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SESSION = REPO / "research_state" / "session_20261124T204500Z"
SESSION_UTC = "20261124T204500Z"
SESSION_ID = f"session_{SESSION_UTC}"
EXPERIMENT_ID = "FCLR-VOL-CORR-01"
CAMPAIGN = "FCLR-VOL-CORR-01-20261124T180000Z"


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
    registry_path = SESSION / f"fclr_volcorr01_source_registry_{SESSION_UTC}.json"
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
    n_checks += 7

    # ---- 2. Prereg binds to source registry and is outcome-blind ----
    prereg_path = SESSION / f"fclr_volcorr01_prereg_{SESSION_UTC}.json"
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
    checks["prereg_design_kind_correction"] = bool(
        any(k in str(design.get("kind", "")).lower()
            for k in ("event_study", "survival", "hazard", "correction"))
    )
    floor = design.get("materiality_floor_rel", prereg.get("materiality_floor_rel"))
    checks["prereg_materiality_valid"] = bool(
        isinstance(floor, (int, float)) and floor > 0
    )
    n_checks += 5

    # ---- 3. Eval internal consistency (recompute headline from stored summary) ----
    eval_path = SESSION / f"fclr_volcorr01_eval_{SESSION_UTC}.json"
    evald = json.loads(eval_path.read_text(encoding="utf-8"))
    base_med = evald["metrics"]["baseline"]["median_correction_h"]
    cand_med = evald["metrics"]["candidate"]["median_correction_h"]

    contrast_recompute = (cand_med - base_med) / base_med if base_med > 0 else None
    checks["eval_contrast_consistent"] = bool(
        contrast_recompute is not None
        and abs(contrast_recompute - evald.get("median_contrast_rel", contrast_recompute)) < 1e-6
    )
    floor = design.get("materiality_floor_rel", 0.10)
    materiality_recompute = bool(contrast_recompute is not None and abs(contrast_recompute) >= floor)
    checks["eval_materiality_consistent"] = bool(
        materiality_recompute == evald.get("materiality_met")
    )
    direction_recompute = bool(cand_med > base_med)
    checks["eval_direction_consistent"] = bool(
        direction_recompute == evald.get("direction_slower_correction_high_rv")
    )
    if base_med is None or cand_med is None:
        verdict_recompute = "INCONCLUSIVE"
    elif materiality_recompute and direction_recompute:
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
    checks["eval_n_events_positive"] = bool(
        isinstance(evald.get("n_events"), int) and evald.get("n_events", 0) >= 1
    )
    checks["eval_metrics_numeric_nonneg"] = bool(
        isinstance(base_med, (int, float)) and isinstance(cand_med, (int, float))
        and base_med >= 0 and cand_med >= 0
    )
    n_checks += 11

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
            "baseline_median_correction_h": base_med,
            "candidate_median_correction_h": cand_med,
            "median_contrast_rel_recompute": contrast_recompute,
            "materiality_floor_rel": floor,
            "materiality_met_recompute": materiality_recompute,
            "direction_slower_recompute": direction_recompute,
            "verdict_recompute": verdict_recompute,
            "verdict_eval": evald.get("verdict"),
        },
        "source_files_recomputed": n_files,
        "source_verified_bad": verified_bad,
    }
    out_json = SESSION / f"fclr_volcorr01_recompute_{SESSION_UTC}.json"
    out_json.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps({"all_checks_match": all_checks_match, "n_checks": n_checks,
                      "verdict_recompute": verdict_recompute,
                      "verdict_eval": evald.get("verdict")}, indent=2))


if __name__ == "__main__":
    main()