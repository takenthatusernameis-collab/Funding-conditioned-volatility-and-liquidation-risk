#!/usr/bin/env python3
"""Independent stdlib recompute of the Track A extension panel (item 6).

Recomputes from the panel CSV produced by fclr_tracka_extension01_alignment and
compares against the alignment summary JSON: panel rows, event totals, notional
totals, hours-with-liq, coins-with-events, max coin-month gap rate. Reports
n_discrepancies=0 when all match. Stdlib only (csv/json/calendar/datetime); no
pandas/numpy/statsmodels; no network; read-only.
"""
from __future__ import annotations

import calendar
import csv
import hashlib
import json
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
RS = REPO / "research_state"
SESSION = RS / "session_20261119T022824Z"
STAMP = "session_20261119T022824Z"
PANEL = SESSION / f"fclr_tracka_extension01_panel_{STAMP}.csv"
ALIGNMENT = SESSION / f"fclr_tracka_extension01_alignment_{STAMP}.json"
SESSION_ID = "session_20261119T022824Z"
CAMPAIGN = "FCLR-LIQ-TRACKA-EXTENSION-01-20261119T015256Z"


def month_range(month: str):
    y, m = int(month[:4]), int(month[5:7])
    first = date(y, m, 1)
    if m == 12:
        last = date(y + 1, 1, 1) - timedelta(days=1)
    else:
        last = date(y, m + 1, 1) - timedelta(days=1)
    return first, last


def main() -> None:
    align = json.loads(ALIGNMENT.read_text(encoding="utf-8"))

    # Recompute independently from the panel CSV.
    n_rows = 0
    total_events = 0
    total_notional = 0.0
    hours_with_liq = 0
    coins_with_events = set()
    coin_month_rows = defaultdict(int)

    with PANEL.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            n_rows += 1
            coin = row["coin"]
            month = row["month"]
            liq_count = int(float(row["liq_count"]))
            liq_notional = float(row["liq_notional_usd"])
            total_events += liq_count
            total_notional += liq_notional
            coin_month_rows[(coin, month)] += 1
            if liq_count > 0:
                hours_with_liq += 1
                coins_with_events.add(coin)

    # Max coin-month gap rate: 1 - (rows present / expected hours in month).
    max_gap = 0.0
    for (coin, month), rows in coin_month_rows.items():
        first, last = month_range(month)
        expected = (last - first).days + 1
        expected *= 24
        gap = 1.0 - rows / expected
        if gap > max_gap:
            max_gap = gap

    max_gap = round(max_gap, 6)
    total_notional = round(total_notional, 6)

    # Compare against alignment summary.
    checks = [
        ("panel_rows", n_rows, align["panel_rows"]),
        ("event totals (liq_count)", total_events, align["liq_count_total"]),
        ("notional totals (liq_notional_usd)", total_notional, align["liq_notional_usd_total"]),
        ("hours-with-liq", hours_with_liq, align["hours_with_liq_total"]),
        ("coins-with-events", len(coins_with_events), len(align["coins_with_events"])),
        ("max coin-month gap rate", max_gap, align["max_gap_rate"]),
    ]
    discrepancies = []
    for name, got, expected in checks:
        if isinstance(expected, (int, bool)) and not isinstance(expected, float):
            match = got == expected
        else:
            # Relative tolerance: float summation order can shift the last digits
            # of large totals; this is not a data discrepancy.
            scale = max(1.0, abs(float(expected)))
            match = abs(float(got) - float(expected)) <= 1e-9 * scale
        if not match:
            discrepancies.append({"check": name, "recomputed": got, "alignment": expected})

    result = {
        "generated_utc": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "campaign_id": CAMPAIGN,
        "session_id": SESSION_ID,
        "panel_path": str(PANEL.relative_to(REPO)),
        "panel_sha256": hashlib.sha256(PANEL.read_bytes()).hexdigest(),
        "method": "stdlib-only independent recompute from panel CSV",
        "recomputed": {
            "panel_rows": n_rows,
            "liq_count_total": total_events,
            "liq_notional_usd_total": total_notional,
            "hours_with_liq_total": hours_with_liq,
            "coins_with_events": sorted(coins_with_events),
            "max_gap_rate": max_gap,
        },
        "alignment_reference": {
            "panel_rows": align["panel_rows"],
            "liq_count_total": align["liq_count_total"],
            "liq_notional_usd_total": align["liq_notional_usd_total"],
            "hours_with_liq_total": align["hours_with_liq_total"],
            "coins_with_events": align["coins_with_events"],
            "max_gap_rate": align["max_gap_rate"],
        },
        "n_discrepancies": len(discrepancies),
        "discrepancies": discrepancies,
        "status": "PASS" if len(discrepancies) == 0 else "FAIL",
    }
    out = SESSION / f"recompute_tracka_extension01_{SESSION_ID}.json"
    out.write_text(json.dumps(result, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"n_discrepancies": result["n_discrepancies"], "status": result["status"], "panel_rows": n_rows}, indent=1))


if __name__ == "__main__":
    main()
