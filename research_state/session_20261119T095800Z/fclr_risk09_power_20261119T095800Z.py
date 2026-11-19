#!/usr/bin/env python3
"""FCLR-RISK-09 power / MDE audit (standalone, runnable).

Recomputes the minimum detectable Brier effect from frozen block sizes and the
panel base rate; PLAUSIBLE_EFFECT_BRIER = 0.001 stays frozen. Writes
fclr_risk09_power_20261119T095800Z.json with explicit status in {POWERED,
UNDERPOWERED}.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location(
    "fclr_risk09_eval_core", HERE / "fclr_risk09_evaluation_20261119T095800Z.py"
)
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)

SESSION = MOD.SESSION
CAMPAIGN = MOD.CAMPAIGN
OUT = MOD.OUT
SCORED_BLOCKS = MOD.SCORED_BLOCKS
block_rows = MOD.block_rows
mde_brier = MOD.mde_brier
PLAUSIBLE_EFFECT_BRIER = MOD.PLAUSIBLE_EFFECT_BRIER


def main():
    rows = MOD.load_panel()
    rows = MOD.build_features(rows)
    kept, _dropped = MOD.apply_common_sample(rows)
    base_rate = sum(1 for r in kept if r["y"] == 1) / len(kept)
    blocks = []
    all_underpowered = True
    for block in SCORED_BLOCKS:
        train, test = block_rows(kept, block)
        n_test = len(test)
        contrib = [(r["y"] - base_rate) ** 2 for r in test]
        sd_diff = statistics_stdev(contrib) if len(contrib) >= 2 else 0.0
        mde = mde_brier(n_test, sd_diff)
        powered_block = mde is not None and mde <= PLAUSIBLE_EFFECT_BRIER
        if powered_block:
            all_underpowered = False
        blocks.append({
            "name": block["name"],
            "n_test": n_test,
            "base_rate": base_rate,
            "sd_diff_proxy": sd_diff,
            "mde_brier_80pct": mde,
            "plausible_effect_brier": PLAUSIBLE_EFFECT_BRIER,
            "powered_block": powered_block,
        })
    status = "UNDERPOWERED" if all_underpowered else "POWERED"
    payload = {
        "campaign_id": CAMPAIGN,
        "session_utc": SESSION,
        "status": status,
        "models_run": status == "POWERED",
        "plausible_effect_brier": PLAUSIBLE_EFFECT_BRIER,
        "base_rate": base_rate,
        "blocks": blocks,
        "rule": "if all scored blocks' mde_brier_80pct > PLAUSIBLE_EFFECT_BRIER then UNDERPOWERED",
    }
    (OUT / f"fclr_risk09_power_{SESSION}.json").write_text(json.dumps(payload, indent=2) + "\n")
    print(f"power status={status}")


def statistics_stdev(xs):
    import statistics
    return statistics.stdev(xs)


if __name__ == "__main__":
    main()
