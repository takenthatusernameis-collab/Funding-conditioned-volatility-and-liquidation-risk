#!/usr/bin/env python3
"""FCLR-RISK-11 power restoration design: block MDE audit + MDE-by-instrument-count table.

Outcome-blind prereg is frozen first (fclr_risk11_prereg_*). This module then
computes MDE from frozen block sizes and panel base rate only (no model-comparison
outcomes), per block and per instrument count, and records the preregistered
smallest-defensible-effect decision.

Run from the repo root:
  python3 research_state/session_20261119T130817Z/fclr_risk11_power_20261119T130817Z.py
Writes:
  fclr_risk11_power_20261119T130817Z.json
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import statistics
from pathlib import Path

SESSION = "20261119T130817Z"
CAMPAIGN = "FCLR-LIQ-RISK-ESCALATION-11-20261119T120000Z"
REPO = Path(__file__).resolve().parents[2]
PANEL = REPO / "research_state" / "session_20261119T022824Z" / "fclr_tracka_extension01_panel_session_20261119T022824Z.csv"
OUT = REPO / "research_state" / f"session_{SESSION}"
PLAUSIBLE_EFFECT_BRIER = 0.001
Z_0975 = 1.959963984540054
Z_080 = 0.8416212335729143

COINS = ["BTC", "ETH", "BNB", "SOL", "XRP", "AVAX", "DOGE", "LINK", "SUI", "ARB", "OP", "APT", "ADA"]

BLOCKS = [
    {"name": "block_1", "test_start": "2025-11-01", "test_end": "2025-12-31",
     "train_start": None, "train_end": None, "scored": False},
    {"name": "block_2", "test_start": "2026-02-01", "test_end": "2026-04-30",
     "train_start": "2025-11-01", "train_end": "2025-12-31", "scored": True},
    {"name": "block_3", "test_start": "2026-06-01", "test_end": "2026-08-31",
     "train_start": "2025-11-01", "train_end": "2026-01-31", "scored": True},
]
SCORED_BLOCK_NAMES = ["block_2", "block_3", "pooled"]


def _parse_float(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def load_panel():
    rows = []
    with PANEL.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for r in reader:
            rows.append({
                "coin": r["coin"],
                "hour_utc": r["hour_utc"],
                "month": r["month"],
                "close": _parse_float(r["close"]),
                "volume": _parse_float(r["volume"]),
                "funding_rate": _parse_float(r["funding_rate"]),
                "premium": _parse_float(r["premium"]),
                "mark_price": _parse_float(r["mark_price"]),
                "open_interest_usd": _parse_float(r["open_interest_usd"]),
                "liq_count": _parse_float(r["liq_count"]),
            })
    rows.sort(key=lambda r: (r["coin"], r["hour_utc"]))
    return rows


def build_features(rows):
    by_coin = {}
    for r in rows:
        by_coin.setdefault(r["coin"], []).append(r)
    for coin in COINS:
        series = by_coin.get(coin, [])
        rets = [None] * len(series)
        for i in range(1, len(series)):
            c0, c1 = series[i - 1]["close"], series[i]["close"]
            if c0 is not None and c1 is not None and c0 > 0 and c1 > 0:
                rets[i] = math.log(c1 / c0)
        for t in range(len(series)):
            window = [x for x in rets[max(0, t - 24):t] if x is not None]
            series[t]["rv_lag"] = statistics.stdev(window) if len(window) >= 2 else None
            series[t]["ret_t"] = rets[t]
            series[t]["funding_lag"] = series[t - 1]["funding_rate"] if t >= 1 else None
            series[t]["premium_lag"] = series[t - 1]["premium"] if t >= 1 else None
            oi1 = series[t - 1]["open_interest_usd"] if t >= 1 else None
            oi2 = series[t - 2]["open_interest_usd"] if t >= 2 else None
            if oi1 is not None and oi2 is not None and oi1 > 0 and oi2 > 0:
                series[t]["oi_change_lag"] = math.log(oi1 / oi2)
            else:
                series[t]["oi_change_lag"] = None
            lc = series[t]["liq_count"]
            series[t]["y"] = 1 if (lc is not None and lc >= 1) else 0
    return rows


def apply_common_sample(rows):
    kept = []
    dropped = 0
    for r in rows:
        if r["rv_lag"] is None or r["funding_lag"] is None or r["oi_change_lag"] is None:
            dropped += 1
            continue
        kept.append(r)
    return kept, dropped


def in_window(hour_utc, start, end):
    d = hour_utc[:10]
    return (start is None or d >= start) and (end is None or d <= end)


def block_test_rows(kept, block):
    return [r for r in kept if in_window(r["hour_utc"], block["test_start"], block["test_end"])]


def mde_brier(n, sd_diff):
    if n <= 1 or sd_diff is None or sd_diff <= 0:
        return None
    return (Z_0975 + Z_080) * sd_diff / math.sqrt(n)


def block_mde(test, base_rate):
    n_test = len(test)
    if n_test == 0:
        return {"n_test": 0, "base_rate": base_rate, "sd_diff_proxy": None, "mde_brier_80pct": None}
    contrib = [(r["y"] - base_rate) ** 2 for r in test]
    sd_diff = statistics.stdev(contrib) if len(contrib) >= 2 else 0.0
    return {
        "n_test": n_test,
        "base_rate": base_rate,
        "sd_diff_proxy": sd_diff,
        "mde_brier_80pct": mde_brier(n_test, sd_diff),
    }


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = load_panel()
    rows = build_features(rows)
    kept, dropped = apply_common_sample(rows)

    base_rate = sum(1 for r in kept if r["y"] == 1) / len(kept)

    # Full-panel block MDE
    blocks = []
    all_underpowered = True
    for name in SCORED_BLOCK_NAMES:
        if name == "pooled":
            test = block_test_rows(kept, BLOCKS[1]) + block_test_rows(kept, BLOCKS[2])
        else:
            blk = next(b for b in BLOCKS if b["name"] == name)
            test = block_test_rows(kept, blk)
        mde_info = block_mde(test, base_rate)
        powered = mde_info["mde_brier_80pct"] is not None and mde_info["mde_brier_80pct"] <= PLAUSIBLE_EFFECT_BRIER
        if powered:
            all_underpowered = False
        blocks.append({"name": name, **mde_info, "plausible_effect_brier": PLAUSIBLE_EFFECT_BRIER, "powered_block": powered})

    # MDE by instrument count (fixed alphabetical coin order; outcome-blind)
    instrument_count_rows = []
    prefix_coins = []
    for k in range(1, len(COINS) + 1):
        prefix_coins.append(COINS[k - 1])
        coin_set = set(prefix_coins)
        subset = [r for r in kept if r["coin"] in coin_set]
        sub_base = sum(1 for r in subset if r["y"] == 1) / len(subset) if subset else 0.0
        entry = {"coin_count": k, "coins": list(prefix_coins), "base_rate": sub_base, "blocks": []}
        for name in SCORED_BLOCK_NAMES:
            if name == "pooled":
                test = block_test_rows(subset, BLOCKS[1]) + block_test_rows(subset, BLOCKS[2])
            else:
                blk = next(b for b in BLOCKS if b["name"] == name)
                test = block_test_rows(subset, blk)
            entry["blocks"].append({"name": name, **block_mde(test, sub_base), "plausible_effect_brier": PLAUSIBLE_EFFECT_BRIER})
        instrument_count_rows.append(entry)

    status = "UNDERPOWERED" if all_underpowered else "POWERED"

    # Smallest defensible effect: min mde_brier_80pct across scored blocks at full instrument count (block_3 primary)
    full = instrument_count_rows[-1]
    block_mdes = {e["name"]: e["mde_brier_80pct"] for e in full["blocks"]}
    valid_mdes = [v for v in block_mdes.values() if v is not None]
    smallest_defensible = min(valid_mdes) if valid_mdes else None

    power_json = {
        "campaign_id": CAMPAIGN,
        "session_utc": SESSION,
        "status": status,
        "models_run": status == "POWERED",
        "plausible_effect_brier": PLAUSIBLE_EFFECT_BRIER,
        "base_rate": base_rate,
        "common_sample_dropped": dropped,
        "common_sample_kept": len(kept),
        "blocks": blocks,
        "mde_by_instrument_count": instrument_count_rows,
        "smallest_defensible_effect": smallest_defensible,
        "smallest_defensible_effect_rule": "min mde_brier_80pct across scored blocks at full instrument count (block_3 primary); effect defensible only if >= this MDE",
        "rule": "if all scored blocks' mde_brier_80pct > PLAUSIBLE_EFFECT_BRIER then UNDERPOWERED",
    }
    (OUT / f"fclr_risk11_power_{SESSION}.json").write_text(json.dumps(power_json, indent=2) + "\n")
    print(f"status={status} base_rate={base_rate:.6f} smallest_defensible_effect={smallest_defensible}")
    for b in blocks:
        print(f"  {b['name']}: n_test={b['n_test']} mde_brier_80pct={b['mde_brier_80pct']} powered={b['powered_block']}")


if __name__ == "__main__":
    main()
