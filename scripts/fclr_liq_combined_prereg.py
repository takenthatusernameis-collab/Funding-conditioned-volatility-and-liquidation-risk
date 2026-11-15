#!/usr/bin/env python3
"""FCLR-LIQ-COMBINED-PANEL step 4: PREREG_FREEZE (pre-outcomes).

Freezes a NEW pre-outcomes prereg for the 24h observed-liquidation-intensity QLIKE
C2-vs-B1 expanding-window walk-forward on the combined metpie+ironflow panel.

This script ONLY writes the prereg JSON+MD with outcome_data_inspected_before_freeze=false.
It does NOT read the panel outcomes, does NOT compute any forecast metric, and does NOT
mutate any sealed artifact. Thresholds below are fixed here and must not be tuned later.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
RS = REPO / "research_state"

TS = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

PREREG = {
    "experiment_id": f"FCLR-LIQ-COMBINED-{TS}",
    "prereg_frozen_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "class": "CONFIRMATORY",
    "promotable": False,
    "outcome_data_inspected_before_freeze": False,
    "estimand": {
        "name": "24h_observed_liquidation_intensity_qlike",
        "target": "daily_total_notional_usd_next_24h",
        "aggregation": "sum of notional_usd over (coin, calendar_day)",
        "target_shift": "next_calendar_day (shift -1 within coin)",
        "loss": "QLIKE",
        "baseline": "B1",
        "challenger": "C2",
        "contrast": "C2_vs_B1",
        "materiality_floor_pct": 2.0,
        "min_instruments": 5,
        "min_test_blocks": 3,
        "block_bootstrap_reps": 2000,
        "block_bootstrap_seed": 20261115,
        "holm_family": ["C2_vs_B1"],
        "purge_embargo_days": 7,
        "walk_forward": "expanding_window",
    },
    "universe": {
        "coins": ["AAVE", "ADA", "AVAX", "BNB", "BTC", "CRV", "DOGE", "ETH",
                  "LINK", "LTC", "NEAR", "SOL", "SUI", "UNI", "XRP"],
        "n_coins": 15,
        "source_family": "combined metpie (2025-03-22..2025-05-25) + ironflow (2025-05-25..2026-10-31) Hyperliquid observed liquidation events",
        "panel_artifact": None,
    },
    "features": {
        "B1": ["rv24h", "rv168h"],
        "C2": ["rv24h", "rv168h", "fundingRate", "abs_fund_pct", "premium", "ema_dist"],
        "note": "All features are causal (past-only as-of joins) at the event->daily aggregation grain. Funding features are the last funding timestamp <= event; RV features are 4h-candle rolling std over past bars.",
    },
    "splits": {
        "train": {"start": "2025-03-22", "end": "2025-08-31",
                  "blocks": "PRISTINE blocks 0-1 + ESTIMAND_OVERLAP blocks 2-4 (estimand-novel for the combined panel)"},
        "validation": {"start": "2025-09-01", "end": "2025-09-30"},
        "embargo_days": 7,
        "test_blocks": [
            {"index": 1, "start": "2025-10-01", "end": "2025-10-31",
             "class": "PRISTINE_ADJACENT_ESTIMAND_NOVEL"},
            {"index": 2, "start": "2026-01-01", "end": "2026-01-31",
             "class": "IRONFLOW_ESTIMAND_NOVEL"},
            {"index": 3, "start": "2026-09-01", "end": "2026-09-30",
             "class": "IRONFLOW_ESTIMAND_NOVEL"},
        ],
        "note": "Test blocks are estimand-novel (new source family + new target). Expanding-window walk-forward: fit on train+val+preceding test blocks, evaluate next test block.",
    },
    "gate": {
        "pass_conditions": [
            "relative_qlike_reduction_C2_vs_B1 >= 2.0%",
            "block_bootstrap_ci_hi < 0 (excludes zero in favorable direction)",
            "n_paired_instruments >= 5",
            "n_test_blocks_with_data >= 3",
        ],
        "verdict_space": ["PASS", "NOT_MET"],
        "null_handling": "Record NOT_MET honestly; do not retune thresholds; install next materially different heavy cell if NOT_MET.",
    },
    "constraints": {
        "no_outcome_peeking_before_freeze": True,
        "no_threshold_tuning_after_freeze": True,
        "no_sealed_artifact_mutation": True,
        "no_paid_or_credentialed_data": True,
        "no_network_for_outcomes": True,
        "H2_shek_replication_remains": "EXPLORATORY_ONLY (promotable=false)",
    },
}

prereg_json = RS / f"prereg_fclr_liq_combined_{TS}.json"
prereg_md = RS / f"prereg_fclr_liq_combined_{TS}.md"

prereg_json.write_text(json.dumps(PREREG, indent=2) + "\n")

md = []
md.append(f"# FCLR-LIQ-COMBINED PREREGISTRATION — {TS}")
md.append("")
md.append(f"**Frozen (UTC):** {PREREG['prereg_frozen_utc']}")
md.append(f"**Experiment ID:** `{PREREG['experiment_id']}`")
md.append(f"**Class:** {PREREG['class']} (promotable={PREREG['promotable']})")
md.append(f"**outcome_data_inspected_before_freeze:** `false`")
md.append("")
md.append("## Estimand")
md.append("")
md.append(f"- **Target:** next-24h observed liquidation intensity (daily total notional_usd)")
md.append(f"- **Loss:** QLIKE; **Contrast:** C2 vs B1; **Materiality floor:** 2.0%")
md.append(f"- **Min instruments:** 5; **Min test blocks:** 3; **Block bootstrap:** 2000 reps (seed 20261115)")
md.append(f"- **Purge/embargo:** 7 days; **Walk-forward:** expanding window")
md.append("")
md.append("## Universe")
md.append("")
md.append(f"- 15 Hyperliquid coins: {', '.join(PREREG['universe']['coins'])}")
md.append(f"- Source: combined metpie (2025-03-22..2025-05-25) + ironflow (2025-05-25..2026-10-31) observed liquidation events")
md.append("")
md.append("## Features")
md.append("")
md.append(f"- **B1:** {PREREG['features']['B1']}")
md.append(f"- **C2:** {PREREG['features']['C2']}")
md.append(f"- {PREREG['features']['note']}")
md.append("")
md.append("## Splits")
md.append("")
md.append(f"- **Train:** {PREREG['splits']['train']['start']}..{PREREG['splits']['train']['end']} ({PREREG['splits']['train']['blocks']})")
md.append(f"- **Validation:** {PREREG['splits']['validation']['start']}..{PREREG['splits']['validation']['end']}")
md.append(f"- **Embargo:** {PREREG['splits']['embargo_days']} days")
for tb in PREREG['splits']['test_blocks']:
    md.append(f"- **Test block {tb['index']}:** {tb['start']}..{tb['end']} ({tb['class']})")
md.append("")
md.append("## Gate")
md.append("")
for c in PREREG['gate']['pass_conditions']:
    md.append(f"- {c}")
md.append("")
md.append(f"**Verdict space:** {PREREG['gate']['verdict_space']}")
md.append("")
md.append("## Hard constraints")
md.append("")
md.append("- No outcome peeking or threshold tuning before/after freeze.")
md.append("- No sealed artifact mutation; no paid/credentialed/manual data; no network for outcomes.")
md.append("- H2_shek_replication remains EXPLORATORY_ONLY (promotable=false).")
md.append("- NOT_MET is recorded honestly; next materially different heavy cell installed if NOT_MET.")
prereg_md.write_text("\n".join(md) + "\n")

print(json.dumps({"prereg_json": str(prereg_json.relative_to(REPO)),
                  "prereg_md": str(prereg_md.relative_to(REPO)),
                  "experiment_id": PREREG["experiment_id"]}, indent=2))