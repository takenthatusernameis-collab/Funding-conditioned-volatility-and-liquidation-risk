#!/usr/bin/env python3
"""Build the FCLR-VOL-STRESS-01 outcome-blind prereg, frozen before outcomes.

Binds the frozen design to the source-registry sha256. No outcome data is read.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
RS = REPO / "research_state"
SESSION_UTC = "20261124T222500Z"
SESSION_ID = f"session_{SESSION_UTC}"
SESSION_DIR = RS / SESSION_ID
EXPERIMENT_ID = "FCLR-VOL-STRESS-01"
CAMPAIGN_ID = "FCLR-VOL-STRESS-01-20261124T213000Z"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    registry_path = SESSION_DIR / f"fclr_volstress01_source_registry_{SESSION_UTC}.json"
    registry_sha = sha256_file(registry_path)

    prereg = {
        "experiment_id": EXPERIMENT_ID,
        "campaign": CAMPAIGN_ID,
        "session_id": SESSION_ID,
        "session_utc": SESSION_UTC,
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "frozen_before_outcomes": True,
        "decision_frozen_before_outcomes": True,
        "outcome_data_inspected_before_freeze": False,
        "source_registry_sha256": registry_sha,
        "input_hash_assertions": {"source_registry_sha256": registry_sha},
        "primary_question": (
            "Does the funding + price-dislocation feature set improve out-of-sample "
            "forecasts of a realized-volatility STRESS event (next-24h realized variance "
            "exceeding an expanding, train-only high quantile per coin) beyond a "
            "realized-volatility-only baseline on the broad ironflow_bulk panel?"
        ),
        "design": {
            "kind": "walk_forward_classification_stress_tail_exceedance",
            "outcome_family": "tail_exceedance_classification",
            "forecast_origin": "hourly t (close of hour t)",
            "target": "stress event y_t = 1 if RV_{t+1..t+24} > q_t",
            "rv_definition": "trailing 24h realized variance from hourly close-to-close log returns",
            "threshold_q_t": "expanding, train-only per-coin high quantile (0.95) of trailing RV, shifted by 1 (no future info)",
            "baseline": "RV-only (HAR-style trailing log-RV lags) logistic",
            "candidate": "RV-only + signed funding_rate + abs(funding_rate) + premium + mark/EMA24 distance",
            "feature_standardization": "train-only (expanding) z-score",
            "walk_forward": True,
            "train_frac": 0.60,
            "purge_embargo_h": 48,
            "n_test_blocks": 6,
            "block_months": 2,
            "no_random_split": True,
            "no_overlapping_forward_targets_across_purge": True,
            "inference": [
                "cluster-robust CR1 by coin",
                "Driscoll-Kraay HAC (block-level)",
                "Holm step-down over declared family",
            ],
            "multiplicity_family": ["brier_relative_improvement", "logloss_relative_improvement"],
            "metrics": ["brier", "log_loss", "calibration_ece"],
        },
        "materiality_floor_rel": 0.02,
        "materiality_floor": 0.02,
        "materiality_definition": (
            "candidate relative Brier improvement over the RV-only baseline must exceed "
            "0.02 (2%); verdict is symmetric PROMOTED / NOT_SUPPORTED"
        ),
        "verdict_rule": {
            "PROMOTED": "materiality_met is True AND candidate beats baseline on Brier (Holm-adjusted)",
            "NOT_SUPPORTED": "materiality floor not met (valid, publishable negative result)",
            "INCONCLUSIVE": "insufficient events / degenerate metrics",
        },
        "universe": "coins present in candles_1h AND funding AND open_interest (intersection)",
        "frozen_inputs_note": "ironflow_bulk 18 monthly parquet per dataset; sha256-asserted; read-only",
    }

    out_json = SESSION_DIR / f"fclr_volstress01_prereg_{SESSION_UTC}.json"
    out_json.write_text(json.dumps(prereg, indent=2), encoding="utf-8")

    lines = [
        "# FCLR-VOL-STRESS-01 Prereg (outcome-blind, frozen before outcomes)",
        "",
        f"**Experiment ID:** {EXPERIMENT_ID}",
        f"**Campaign:** {CAMPAIGN_ID}",
        f"**Session:** {SESSION_ID}",
        f"**Frozen before outcomes:** {prereg['frozen_before_outcomes']}",
        f"**Outcome data inspected before freeze:** {prereg['outcome_data_inspected_before_freeze']}",
        f"**Source registry sha256:** `{registry_sha}`",
        "",
        "## Design",
        f"- Kind: {prereg['design']['kind']}",
        f"- Target: {prereg['design']['target']}",
        f"- Threshold: {prereg['design']['threshold_q_t']}",
        f"- Baseline: {prereg['design']['baseline']}",
        f"- Candidate: {prereg['design']['candidate']}",
        f"- Walk-forward: train_frac={prereg['design']['train_frac']}, purge_embargo_h={prereg['design']['purge_embargo_h']}, n_test_blocks={prereg['design']['n_test_blocks']}",
        f"- Materiality floor (relative Brier improvement): {prereg['materiality_floor_rel']}",
        "",
        "## Verdict rule",
        f"- PROMOTED: {prereg['verdict_rule']['PROMOTED']}",
        f"- NOT_SUPPORTED: {prereg['verdict_rule']['NOT_SUPPORTED']}",
        f"- INCONCLUSIVE: {prereg['verdict_rule']['INCONCLUSIVE']}",
    ]
    out_md = SESSION_DIR / f"fclr_volstress01_prereg_{SESSION_UTC}.md"
    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"source_registry_sha256": registry_sha,
                      "json": str(out_json)}, indent=2))


if __name__ == "__main__":
    main()