#!/usr/bin/env python3
"""Bounded, single-shot Track A path-(b) feasibility probe.

Determines the REAL overlap between ironflow liquidation labels and the
admissible unauthenticated Hyperliquid-native decision-time predictors
(funding history + mark-price candles) for the 9 funded symbols.

Writes ONLY a timestamped probe JSON under research_state/ (no outcomes
inspected, no canonical mutation, no status-only churn). Exit 0 always.
"""
from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

REPO = Path(__file__).resolve().parents[1]
RS = REPO / "research_state"
OUT = RS / f"hl_pathb_probe_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json"

INFO = "https://api.hyperliquid.xyz/info"
COINS = ["BTC", "ETH", "BNB", "SOL", "XRP", "AVAX", "DOGE", "LINK", "SUI"]

# Candidate overlap windows (UTC month-aligned)
MONTHS = ["2025-06", "2025-07", "2025-08", "2025-09", "2025-10",
          "2025-11", "2025-12", "2026-01", "2026-02", "2026-03",
          "2026-04", "2026-05", "2026-06", "2026-07", "2026-08",
          "2026-09", "2026-10"]


def iso_ms(s: str) -> int:
    return int(datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp() * 1000)


def month_range(m: str):
    y, mo = m.split("-")
    start = iso_ms(f"{y}-{mo}-01T00:00:00Z")
    # first day of next month
    if mo == "12":
        ny, nmo = f"{int(y)+1}", "01"
    else:
        ny, nmo = y, f"{int(mo)+1:02d}"
    end = iso_ms(f"{ny}-{nmo}-01T00:00:00Z") - 1
    return start, end


def post(payload, retries=2, pause=1.5):
    last = None
    for _ in range(retries):
        try:
            r = requests.post(INFO, json=payload, timeout=30)
            if r.status_code == 200:
                try:
                    return r.json()
                except Exception:
                    return []
            last = f"HTTP {r.status_code}"
        except Exception as e:  # noqa: BLE001
            last = f"ERR {e}"
        time.sleep(pause)
    return {"__error__": last}


def main() -> None:
    t0 = time.time()
    meta = post({"type": "meta"})
    universe = {u.get("name") for u in (meta.get("universe", []) if isinstance(meta, dict) else []) if isinstance(u, dict)}
    present = [c for c in COINS if c in universe]

    results = {
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "purpose": "Track A path-(b) feasibility: exact overlap of ironflow labels vs Hyperliquid-native funding + mark-price candles",
        "universe_count": len(universe),
        "coins_probed": COINS,
        "coins_present_in_universe": present,
        "funding_history_monthly": {},
        "candle_snapshot_monthly": {},
        "errors": [],
    }

    for coin in COINS:
        if coin not in universe:
            results["errors"].append(f"{coin}: not in Hyperliquid universe")
            continue
        f_row = {}
        c_row = {}
        for m in MONTHS:
            s, e = month_range(m)
            fr = post({"type": "fundingHistory", "coin": coin, "startTime": s, "endTime": e})
            if isinstance(fr, dict) and "__error__" in fr:
                f_row[m] = {"error": fr["__error__"]}
            else:
                f_row[m] = {"n": len(fr) if isinstance(fr, list) else -1}
            cr = post({"type": "candleSnapshot", "req": {"coin": coin, "interval": "1h", "startTime": s, "endTime": e}})
            if isinstance(cr, dict) and "__error__" in cr:
                c_row[m] = {"error": cr["__error__"]}
            else:
                c_row[m] = {"n": len(cr) if isinstance(cr, list) else -1}
            time.sleep(0.6)
        results["funding_history_monthly"][coin] = f_row
        results["candle_snapshot_monthly"][coin] = c_row
        time.sleep(1.0)

    # Compute overlap summary
    def available(d, coin):
        return {m: v.get("n", 0) for m, v in d.get(coin, {}).items() if isinstance(v, dict) and v.get("n", 0) > 0}

    results["overlap_summary"] = {}
    for coin in COINS:
        f_avail = available(results["funding_history_monthly"], coin)
        c_avail = available(results["candle_snapshot_monthly"], coin)
        both = sorted(set(f_avail) & set(c_avail))
        results["overlap_summary"][coin] = {
            "funding_months": sorted(f_avail),
            "candle_months": sorted(c_avail),
            "both_months": both,
            "n_both_months": len(both),
        }

    results["elapsed_s"] = round(time.time() - t0, 3)
    results["network"] = True
    OUT.write_text(json.dumps(results, indent=1, sort_keys=True) + "\n")
    print(json.dumps({"out": str(OUT), "overlap_summary": results["overlap_summary"]}, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()