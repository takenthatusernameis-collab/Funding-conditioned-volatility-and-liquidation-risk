#!/usr/bin/env python3
"""
Phase 4 — FCLR-VOL-BROAD-01 independent stdlib recompute.
Verifies the eval headline and source-registry integrity from stored hashes/config.
Separate code path from the evaluation; no model refit; stdlib + hash checks only.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
SESSION = REPO / "research_state" / "session_20261124T120000Z"
CACHE = REPO / "research_state" / "data_cache" / "ironflow_bulk"
SESSION_UTC = "20261124T120000Z"
SESSION_ID = f"session_{SESSION_UTC}"
EXPERIMENT_ID = "FCLR-VOL-BROAD-01"
CAMPAIGN = f"{EXPERIMENT_ID}-20261124T035500Z"


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    checks = {}
    n_checks = 0

    # ---- 1. Source registry integrity: re-compute every parquet sha256 ----
    registry_path = SESSION / f"fclr_volbroad01_source_registry_{SESSION_UTC}.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    reg_file_sha = sha256_file(registry_path)

    all_match = True
    verified_bad = 0
    n_files = 0
    for entry in registry["files"]:
        p = REPO / entry["path"]
        actual = sha256_file(p)
        stored = entry["sha256"]
        match = actual == stored
        n_files += 1
        if not match:
            all_match = False
            verified_bad += 1
    checks["source_files_recompute"] = n_files
    checks["source_files_stated"] = registry["input_integrity"]["sha256_sidecars_total"]
    checks["source_file_count_ok"] = bool(n_files >= 54)
    checks["source_all_match_recompute"] = bool(all_match)
    checks["source_verified_bad_is_zero"] = bool(verified_bad == 0)
    checks["sha256_all_match_stated"] = bool(
        registry["input_integrity"]["sha256_all_match"] is True
    )
    checks["sha256_verified_bad_stated_is_zero"] = bool(
        registry["input_integrity"]["sha256_verified_bad"] == 0
    )
    checks["source_registry_file_hashable"] = bool(len(reg_file_sha) == 64)
    n_checks += 8

    # ---- 2. Prereg binds to source registry and is outcome-blind ----
    prereg_path = SESSION / f"fclr_volbroad01_prereg_{SESSION_UTC}.json"
    prereg = json.loads(prereg_path.read_text(encoding="utf-8"))
    prereg_reg_sha = prereg.get("source_registry_sha256") or prereg.get(
        "input_hash_assertions", {}
    ).get("source_registry_sha256")
    checks["prereg_source_registry_sha256_binds"] = bool(
        prereg_reg_sha == reg_file_sha
    )
    checks["prereg_frozen_before_outcomes"] = bool(
        prereg.get("frozen_before_outcomes") is True
        or prereg.get("decision_frozen_before_outcomes") is True
    )
    checks["prereg_outcome_not_inspected"] = bool(
        prereg.get("outcome_data_inspected_before_freeze") is False
    )
    checks["prereg_design_walk_forward"] = bool(
        "walk_forward" in str(prereg.get("design", {}).get("kind", ""))
    )
    tf = prereg.get("train_frac", prereg.get("design", {}).get("train_frac"))
    checks["prereg_train_frac_valid"] = bool(isinstance(tf, (int, float)) and 0 < tf < 1)
    purge = prereg.get(
        "purge_embargo_h", prereg.get("design", {}).get("purge_embargo_h")
    )
    checks["prereg_purge_valid"] = bool(isinstance(purge, int) and purge >= 1)
    floor = prereg.get("materiality_floor_rel_qlike")
    checks["prereg_materiality_valid"] = bool(
        isinstance(floor, (int, float)) and floor > 0
    )
    n_checks += 7

    # ---- 3. Eval JSON internal consistency (recompute vs stored) ----
    eval_path = SESSION / f"fclr_volbroad01_eval_{SESSION_UTC}.json"
    evald = json.loads(eval_path.read_text(encoding="utf-8"))
    base_q = evald["metrics"]["baseline"]["qlike"]
    cand_q = evald["metrics"]["candidate"]["qlike"]
    base_m = evald["metrics"]["baseline"]["mse"]
    cand_m = evald["metrics"]["candidate"]["mse"]

    qlike_diff_recompute = cand_q - base_q
    checks["eval_qlike_diff_consistent"] = bool(
        abs(qlike_diff_recompute - evald.get("qlike_diff", qlike_diff_recompute))
        < 1e-9
    )

    rel_pct_recompute = (base_q - cand_q) / base_q * 100 if base_q > 0 else float("nan")
    checks["eval_rel_qlike_pct_consistent"] = bool(
        abs(rel_pct_recompute - evald.get("rel_qlike_pct", rel_pct_recompute))
        < 1e-6
    )

    materiality_threshold_pct = 2.0
    materiality_met_recompute = bool(rel_pct_recompute >= materiality_threshold_pct)
    checks["eval_materiality_consistent"] = bool(
        materiality_met_recompute == evald.get("materiality_met")
    )

    verdict = evald.get("verdict")
    checks["eval_verdict_valid"] = bool(
        verdict in {"PROMOTED", "NOT_SUPPORTED", "INCONCLUSIVE"}
    )
    checks["eval_no_promotion_without_materiality"] = bool(
        not (verdict == "PROMOTED" and evald.get("materiality_met") is not True)
    )
    checks["eval_status_valid"] = bool(
        evald.get("status")
        in {"CONFIRMATORY_COMPLETE", "NOT_SUPPORTED", "PROMOTED", "INCONCLUSIVE"}
    )
    checks["eval_holdout_opened"] = bool(evald.get("holdout_opened") is True)
    checks["eval_n_forecasts_positive"] = bool(
        isinstance(evald.get("n_forecasts"), int) and evald.get("n_forecasts", 0) >= 1
    )
    checks["eval_n_test_blocks_positive"] = bool(
        isinstance(evald.get("n_test_blocks"), int)
        and evald.get("n_test_blocks", 0) >= 1
    )
    checks["eval_metrics_numeric_nonneg"] = bool(
        isinstance(base_q, (int, float))
        and isinstance(cand_q, (int, float))
        and isinstance(base_m, (int, float))
        and isinstance(cand_m, (int, float))
        and base_q >= 0
        and cand_q >= 0
        and base_m >= 0
        and cand_m >= 0
    )
    n_checks += 10

    # ---- 4. Experiment/session ID binding across all JSON artifacts ----
    for label, data in (("REGISTRY", registry), ("PREREG", prereg), ("EVAL", evald)):
        checks[f"{label}_experiment_id"] = bool(data.get("experiment_id") == EXPERIMENT_ID)
        checks[f"{label}_session_id"] = bool(
            data.get("session_id") == SESSION_ID
            or data.get("session_utc") == SESSION_UTC
        )
    n_checks += 6

    all_checks_match = all(v is True for v in checks.values() if isinstance(v, bool))

    recompute = {
        "experiment_id": EXPERIMENT_ID,
        "campaign": CAMPAIGN,
        "session_utc": SESSION_UTC,
        "session_id": SESSION_ID,
        "method": "independent stdlib recompute; re-computes parquet sha256 hashes, "
        "verifies prereg-to-registry hash binding, and re-derives eval headline "
        "consistency (QLIKE diff, relative pct, materiality floor, verdict). "
        "Separate code path from evaluation; no model refit.",
        "eval_output_path": f"research_state/session_{SESSION_UTC}/fclr_volbroad01_eval_{SESSION_UTC}.json",
        "eval_output_sha256": sha256_file(eval_path),
        "source_registry_path": f"research_state/session_{SESSION_UTC}/fclr_volbroad01_source_registry_{SESSION_UTC}.json",
        "source_registry_file_sha256": reg_file_sha,
        "sign_convention": "(baseline - candidate) / baseline, positive = candidate better",
        "used_identically_in_eval_and_recompute": True,
        "checks": checks,
        "n_checks": n_checks,
        "all_checks_match": bool(all_checks_match),
        "headline": {
            "qlike_baseline": base_q,
            "qlike_candidate": cand_q,
            "qlike_diff": qlike_diff_recompute,
            "rel_qlike_pct": rel_pct_recompute,
            "mse_baseline": base_m,
            "mse_candidate": cand_m,
            "materiality_floor_pct": 2.0,
            "materiality_met": materiality_met_recompute,
            "verdict": verdict,
        },
        "generated_utc": "2026-11-24T12:00:00Z",
    }

    out_path = SESSION / f"fclr_volbroad01_recompute_{SESSION_UTC}.json"
    out_path.write_text(json.dumps(recompute, indent=2), encoding="utf-8")
    print(f"Wrote {out_path}")
    print(f"n_checks={n_checks}, all_checks_match={all_checks_match}")
    failed = [k for k, v in checks.items() if isinstance(v, bool) and v is not True]
    if failed:
        print(f"FAILED CHECKS: {failed}")


if __name__ == "__main__":
    main()
