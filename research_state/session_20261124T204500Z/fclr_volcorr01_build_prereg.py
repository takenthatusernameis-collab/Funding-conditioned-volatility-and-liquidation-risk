#!/usr/bin/env python3
"""Freeze the FCLR-VOL-CORR-01 outcome-blind prereg.

Binds to the source-registry sha256 and freezes the correction-study design
BEFORE any outcome is computed. Writes prereg json+md only.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
RS = REPO / "research_state"
SESSION_UTC = "20261124T204500Z"
SESSION_ID = f"session_{SESSION_UTC}"
SESSION_DIR = RS / SESSION_ID
EXPERIMENT_ID = "FCLR-VOL-CORR-01"
CAMPAIGN_ID = "FCLR-VOL-CORR-01-20261124T180000Z"
REGISTRY_JSON = SESSION_DIR / f"fclr_volcorr01_source_registry_{SESSION_UTC}.json"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    registry_sha = sha256_file(REGISTRY_JSON)
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
        "input_hash_assertions": {
            "source_registry_sha256": registry_sha,
            "cache": "research_state/data_cache/ironflow_bulk/ (read-only, sha256-asserted)",
        },
        "question": (
            "On the full frozen ironflow_bulk panel (18 monthly parquet, 2025-05..2026-10), "
            "does the Shek (2026) funding-extreme correction pattern reconstruct: is the "
            "median/mean time for an extreme funding observation to correct back to its "
            "pre-extreme band LONGER in a high realized-volatility regime than in a low "
            "regime, and is the correction hazard LOWER when realized volatility is higher, "
            "clearing a frozen materiality floor with Holm-adjusted uncertainty?"
        ),
        "design": {
            "kind": "event_study_survival",
            "event_definition": (
                "funding extreme: |funding_rate| >= q_t where q_t is an EXPANDING, "
                "TRAIN-ONLY quantile of |funding_rate| per coin (no future information)"
            ),
            "quantile_level": 0.95,
            "min_history": 30,
            "correction_definition": (
                "first subsequent hour the funding rate returns inside the pre-extreme "
                "band (|funding_rate| < q_t) within a frozen maximum horizon; censored "
                "events recorded as censored, never as completed negatives"
            ),
            "max_follow_hours": 168,
            "regime_split": (
                "realized-volatility tercile (high vs low) from trailing 24h close-to-close "
                "log returns, train-only thresholds"
            ),
            "rv_window_hours": 24,
            "walk_forward": {
                "train_frac": 0.60,
                "purge_embargo_h": 48,
                "random_split": False,
                "note": "chronological expanding train-only thresholds; no overlapping forward targets across the purge boundary",
            },
            "estimands": [
                "median correction time by regime",
                "mean correction time by regime",
                "correction hazard (survival) contrast high-RV vs low-RV",
            ],
            "inference": [
                "cluster-robust (CR1) by coin",
                "Driscoll-Kraay HAC",
                "Holm step-down over the declared family",
            ],
            "multiplicity_family": [
                "regime_contrast_median_correction_time",
                "regime_contrast_correction_hazard",
            ],
            "materiality_floor_rel": 0.10,
            "materiality_rule": (
                "the high-vs-low RV regime contrast in median correction time must exceed "
                ">= 10% relative in the slower-correction direction"
            ),
            "verdict_rule": "symmetric: PROMOTED if materiality_met and direction slower; else NOT_SUPPORTED; INCONCLUSIVE if a regime median is undefined",
            "bootstrap": {"n_boot": 2000, "seed": 12345, "method": "percentile bootstrap of the median correction time"},
        },
        "paper_claim": {
            "source": "Shek (2026) 'Limits to Coordination: Funding Drag in Crypto Perpetual Funding Rates' (SSRN 7529458)",
            "events": 1696,
            "contracts": 18,
            "median_high_rv_hours": 27.0,
            "median_low_rv_hours": 3.0,
            "claim": "lower correction hazard with higher realized volatility",
            "treatment": "working-paper claim to reconstruct, not established truth",
        },
        "do_not": [
            "re-run the broad RV-forecast (FCLR-VOL-BROAD-01, closed NOT_SUPPORTED)",
            "build a risk overlay (forecast gate not passed)",
            "threshold-shop or relax the frozen floor after outcomes",
            "relabel exploratory as confirmatory",
        ],
    }
    out_json = SESSION_DIR / f"fclr_volcorr01_prereg_{SESSION_UTC}.json"
    out_json.write_text(json.dumps(prereg, indent=2), encoding="utf-8")

    lines = [
        "# FCLR-VOL-CORR-01 Prereg (outcome-blind, frozen before outcomes)",
        "",
        f"**Experiment ID:** {EXPERIMENT_ID}",
        f"**Campaign:** {CAMPAIGN_ID}",
        f"**Session:** {SESSION_ID}",
        f"**Frozen before outcomes:** {prereg['frozen_before_outcomes']}",
        f"**Outcome data inspected before freeze:** {prereg['outcome_data_inspected_before_freeze']}",
        f"**Source registry sha256:** `{registry_sha}`",
        "",
        "## Question",
        prereg["question"],
        "",
        "## Design",
        f"- Kind: {prereg['design']['kind']}",
        f"- Event: {prereg['design']['event_definition']}",
        f"- Correction: {prereg['design']['correction_definition']}",
        f"- Regime split: {prereg['design']['regime_split']}",
        f"- Walk-forward: train_frac={prereg['design']['walk_forward']['train_frac']}, purge/embargo={prereg['design']['walk_forward']['purge_embargo_h']}h, random_split=False",
        f"- Estimands: {', '.join(prereg['design']['estimands'])}",
        f"- Inference: {', '.join(prereg['design']['inference'])}; Holm over {prereg['design']['multiplicity_family']}",
        f"- Materiality floor (relative): {prereg['design']['materiality_floor_rel']}",
        f"- Verdict rule: {prereg['design']['verdict_rule']}",
        "",
        "## Paper claim (Shek 2026, SSRN 7529458)",
        "Median correction 27h high-RV vs 3h low-RV; lower correction hazard with higher RV. Treated as a working-paper claim to reconstruct.",
    ]
    out_md = SESSION_DIR / f"fclr_volcorr01_prereg_{SESSION_UTC}.md"
    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"registry_sha256": registry_sha, "json": str(out_json)}, indent=2))


if __name__ == "__main__":
    main()