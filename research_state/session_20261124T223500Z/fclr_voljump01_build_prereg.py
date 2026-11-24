#!/usr/bin/env python3
"""Build the FCLR-VOL-JUMP-01 outcome-blind prereg, frozen before outcomes.

Binds the frozen signed-jump / semivariance-asymmetry design to the source-registry
sha256. No outcome data is read. The design kind is a DISTINCT outcome family
(jump / asymmetry / bipower / semivariance), not the closed mean-QLIKE,
correction-time, or total-variance tail-exceedance endpoints.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
RS = REPO / "research_state"
SESSION_UTC = "20261124T223500Z"
SESSION_ID = f"session_{SESSION_UTC}"
SESSION_DIR = RS / SESSION_ID
EXPERIMENT_ID = "FCLR-VOL-JUMP-01"
CAMPAIGN_ID = "FCLR-VOL-JUMP-01-20261124T223000Z"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    registry_path = SESSION_DIR / f"fclr_voljump01_source_registry_{SESSION_UTC}.json"
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
            "forecasts of a SIGNED-JUMP / SEMIVARIANCE-ASYMMETRY event (next-24h jump "
            "component -- realized variance minus bipower variation, signed by the sign "
            "of the realized semivariance difference RS+ - RS- -- exceeding an expanding, "
            "train-only high quantile per coin) beyond a realized-volatility-only "
            "baseline on the broad ironflow_bulk panel?"
        ),
        "design": {
            "kind": "walk_forward_classification_signed_jump_semivariance_asymmetry",
            "outcome_family": "jump_asymmetry_classification",
            "forecast_origin": "hourly t (close of hour t)",
            "target": (
                "jump event y_t = 1 if |signed_jump|_{t+1..t+24} > q_t, where the "
                "signed-jump magnitude is the next-24h jump component "
                "J = max(RV - BV, 0) (realized variance minus bipower variation) signed "
                "by sign(RS+ - RS-), and q_t is an EXPANDING, TRAIN-ONLY per-coin high "
                "quantile (0.95) of trailing signed-jump magnitude"
            ),
            "rv_definition": "trailing 24h realized variance from hourly close-to-close log returns",
            "bipower_definition": "trailing 24h bipower variation (pi/2)*mean(|r_i||r_{i-1}|) (continuous-variation estimator)",
            "jump_definition": "J = max(RV - BV, 0) (discontinuous / jump component)",
            "semivariance_definition": "RS+ = sum r^2 for r>0; RS- = sum r^2 for r<0; signed by sign(RS+ - RS-)",
            "threshold_q_t": "expanding, train-only per-coin 0.95 quantile of trailing signed-jump magnitude, monthly checkpoints, prior months only (no future info)",
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
            "distinct_from_closed_arms": (
                "NOT mean log-RV QLIKE (FCLR-VOL-BROAD-01, closed), NOT correction-time / "
                "hazard (FCLR-VOL-CORR-01, closed), NOT total-variance tail exceedance "
                "(FCLR-VOL-STRESS-01, closed). This is the jump / semivariance-asymmetry "
                "classification estimand."
            ),
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

    out_json = SESSION_DIR / f"fclr_voljump01_prereg_{SESSION_UTC}.json"
    out_json.write_text(json.dumps(prereg, indent=2), encoding="utf-8")

    lines = [
        "# FCLR-VOL-JUMP-01 Prereg (outcome-blind, frozen before outcomes)",
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
        f"- Jump component: {prereg['design']['jump_definition']}",
        f"- Semivariance sign: {prereg['design']['semivariance_definition']}",
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
    out_md = SESSION_DIR / f"fclr_voljump01_prereg_{SESSION_UTC}.md"
    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"source_registry_sha256": registry_sha,
                      "json": str(out_json)}, indent=2))


if __name__ == "__main__":
    main()