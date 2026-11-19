#!/usr/bin/env python3
"""FCLR-RISK-11 independent recompute: verify frozen panel integrity (n_discrepancies=0).

Mirrors the RISK-10 recompute: re-reads the frozen Track A panel, rebuilds
features, applies the common-sample rule, and checks panel stats against the
certified preflight expectations. Emits n_discrepancies.

Run from the repo root:
  python3 research_state/session_20261119T130817Z/fclr_risk11_recompute_20261119T130817Z.py
Writes:
  fclr_risk11_recompute_20261119T130817Z.json
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

COINS = ["BTC", "ETH", "BNB", "SOL", "XRP", "AVAX", "DOGE", "LINK", "SUI", "ARB", "OP", "APT", "ADA"]


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


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = load_panel()
    rows = build_features(rows)
    kept, dropped = apply_common_sample(rows)

    expected = {
        "rows": 113880,
        "coins": 13,
        "months": 12,
        "first_month": "2025-11",
        "last_month": "2026-10",
        "funding_rate_nonnull": 113880,
        "liq_count_nonnull": 113880,
        "open_interest_usd_nonnull": 113035,
    }

    months_present = sorted({r["month"] for r in rows})
    coins_present = sorted({r["coin"] for r in rows})
    funding_nn = sum(1 for r in rows if r["funding_rate"] is not None)
    liq_nn = sum(1 for r in rows if r["liq_count"] is not None)
    oi_nn = sum(1 for r in rows if r["open_interest_usd"] is not None)

    checks = [
        ("rows", len(rows) == expected["rows"]),
        ("coins", len(coins_present) == expected["coins"]),
        ("months", len(months_present) == expected["months"]),
        ("funding_rate_nonnull", funding_nn == expected["funding_rate_nonnull"]),
        ("liq_count_nonnull", liq_nn == expected["liq_count_nonnull"]),
        ("open_interest_usd_nonnull", oi_nn == expected["open_interest_usd_nonnull"]),
    ]
    discrepancies = sum(0 if ok else 1 for _, ok in checks)
    panel_hash = hashlib.sha256(PANEL.read_bytes()).hexdigest()

    recompute_detail = {
        "panel_path": str(PANEL.relative_to(REPO)),
        "panel_sha256": panel_hash,
        "rows": len(rows),
        "coins": len(coins_present),
        "months": len(months_present),
        "first_month": months_present[0] if months_present else None,
        "last_month": months_present[-1] if months_present else None,
        "funding_rate_nonnull": funding_nn,
        "liq_count_nonnull": liq_nn,
        "open_interest_usd_nonnull": oi_nn,
        "common_sample_dropped": dropped,
        "common_sample_kept": len(kept),
        "expected": expected,
        "checks": {k: bool(v) for k, v in checks},
        "discrepancies": discrepancies,
        "n_discrepancies": discrepancies,
    }
    recompute_json = {
        "campaign_id": CAMPAIGN,
        "session_utc": SESSION,
        "n_discrepancies": discrepancies,
        "detail": recompute_detail,
    }
    (OUT / f"fclr_risk11_recompute_{SESSION}.json").write_text(json.dumps(recompute_json, indent=2) + "\n")
    print(f"n_discrepancies={discrepancies} rows={len(rows)} kept={len(kept)}")


if __name__ == "__main__":
    main()
