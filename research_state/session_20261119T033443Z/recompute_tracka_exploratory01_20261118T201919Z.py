#!/usr/bin/env python3
"""Independent stdlib recompute of the Track A exploratory alignment aggregates.

Reads only the emitted panel CSV (no parquet, no pandas) and re-derives the
aggregate counts claimed in
``fclr_tracka_exploratory01_alignment_20261118T201919Z.json``. Any mismatch is a
hard discrepancy and fails closed.
"""
from __future__ import annotations

import csv
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SESSION = REPO / "research_state" / "session_20261118T201919Z"
PANEL = SESSION / "fclr_tracka_exploratory01_panel_20261118T201919Z.csv"
SUMMARY = SESSION / "fclr_tracka_exploratory01_alignment_20261118T201919Z.json"


def main() -> None:
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    months = summary["window_months"]
    expected_hours = {"2025-11": 720, "2025-12": 744, "2026-01": 744,
                      "2026-02": 672, "2026-03": 744, "2026-04": 720}

    rows = 0
    liq_count = 0
    liq_notional = 0.0
    hours_with_liq = 0
    coins = set()
    coin_month_hours = defaultdict(int)
    coin_liq = defaultdict(int)

    with PANEL.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for r in reader:
            rows += 1
            coin = r["coin"]
            month = r["month"]
            coins.add(coin)
            coin_month_hours[(coin, month)] += 1
            c = int(float(r["liq_count"]))
            liq_count += c
            liq_notional += float(r["liq_notional_usd"])
            if c > 0:
                hours_with_liq += 1
                coin_liq[coin] += c

    gap_rates = {
        f"{coin}|{m}": round(1.0 - coin_month_hours[(coin, m)] / expected_hours[m], 6)
        for coin in sorted(coins) for m in months
    }
    max_gap = max(gap_rates.values()) if gap_rates else None

    checks = {
        "panel_rows_match": rows == summary["panel_rows"],
        "liq_count_match": liq_count == summary["liq_count_total"],
        "liq_notional_match": abs(liq_notional - summary["liq_notional_usd_total"]) < 1e-3,
        "hours_with_liq_match": hours_with_liq == summary["hours_with_liq_total"],
        "coins_with_events_match": sorted(c for c, n in coin_liq.items() if n > 0)
                                   == summary["coins_with_events"],
        "max_gap_match": max_gap is not None and abs(max_gap - summary["max_gap_rate"]) < 1e-9,
    }
    payload = {
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "script": "recompute_tracka_exploratory01",
        "reads": [str(PANEL.relative_to(REPO))],
        "recomputed": {
            "panel_rows": rows,
            "liq_count_total": liq_count,
            "liq_notional_usd_total": round(liq_notional, 6),
            "hours_with_liq": hours_with_liq,
            "coins_with_events": sorted(c for c, n in coin_liq.items() if n > 0),
            "max_gap_rate": max_gap,
        },
        "checks": checks,
        "n_discrepancies": sum(1 for v in checks.values() if not v),
        "pass": all(checks.values()),
        "network": False,
    }
    out = SESSION / "recompute_tracka_exploratory01_20261118T201919Z.json"
    out.write_text(json.dumps(payload, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"pass": payload["pass"], "n_discrepancies": payload["n_discrepancies"]}))


if __name__ == "__main__":
    main()
