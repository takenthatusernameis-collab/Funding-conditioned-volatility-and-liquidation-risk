#!/usr/bin/env python3
"""Coverage probe: Hyperliquid public API depth for funding + candles.

Determines the REAL overlap between ironflow liquidation labels (2025-11..2026-10)
and available decision-time predictors (funding rates, mark-price candles).

Writes research_state/hl_coverage_probe.json. No outcomes inspected.
"""
from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "research_state" / "hl_coverage_probe.json"

INFO = "https://api.hyperliquid.xyz/info"
LABEL_START = "2025-11-01T00:00:00Z"
LABEL_END = "2026-10-31T23:00:00Z"


def iso_ms(s: str) -> int:
    dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
    return int(dt.timestamp() * 1000)


def post(payload, retries=3, pause=2.0):
    last = None
    for _ in range(retries):
        try:
            r = requests.post(INFO, json=payload, timeout=40)
            if r.status_code == 200:
                try:
                    return r.json()
                except Exception:
                    return []
            last = f"HTTP {r.status_code}: {r.text[:120]}"
        except Exception as e:  # noqa: BLE001
            last = f"ERR {e}"
        time.sleep(pause)
    return {"__error__": last}


def main() -> None:
    now_ms = int(time.time() * 1000)
    win_start = iso_ms(LABEL_START)
    win_end = iso_ms(LABEL_END)

    # meta -> universe coin names
    meta = post({"type": "meta"})
    universe = meta.get("universe", []) if isinstance(meta, dict) else []
    coin_names = sorted({u.get("name") for u in universe if isinstance(u, dict) and u.get("name")})

    results = {
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "label_window": {"start": LABEL_START, "end": LABEL_END},
        "universe_count": len(coin_names),
        "universe_sample": coin_names[:15],
        "funding_history": {},
        "candle_snapshot": {},
        "notes": [],
    }

    # --- funding history: full label window for a sample of coins ---
    sample = coin_names[:8]
    for coin in sample:
        rows = post({"type": "fundingHistory", "coin": coin, "startTime": win_start, "endTime": win_end})
        if isinstance(rows, dict) and "__error__" in rows:
            results["funding_history"][coin] = {"error": rows["__error__"]}
            continue
        ts = [r.get("time") for r in rows if isinstance(r, dict)]
        results["funding_history"][coin] = {
            "n_rows": len(rows),
            "first_ts": min(ts) if ts else None,
            "last_ts": max(ts) if ts else None,
            "first_dt": datetime.fromtimestamp(min(ts) / 1000, tz=timezone.utc).isoformat().replace("+00:00", "Z") if ts else None,
            "last_dt": datetime.fromtimestamp(max(ts) / 1000, tz=timezone.utc).isoformat().replace("+00:00", "Z") if ts else None,
            "window_complete": (min(ts) <= win_start + 3_600_000) and (max(ts) >= win_end - 3_600_000) if ts else False,
        }
        time.sleep(1.0)

    # --- funding history: how far back from NOW can we go (depth test) ---
    depth = {}
    for coin in sample[:3]:
        back_days = [30, 90, 180, 270, 365]
        d = {}
        for bd in back_days:
            st = now_ms - bd * 86_400_000
            rows = post({"type": "fundingHistory", "coin": coin, "startTime": st, "endTime": now_ms})
            n = len(rows) if isinstance(rows, list) else -1
            d[f"{bd}d"] = n
            time.sleep(1.0)
        depth[coin] = d
    results["funding_history_depth"] = depth

    # --- candle snapshot: depth test (mark proxy) ---
    candle_depth = {}
    for coin in sample[:3]:
        d = {}
        for bd in [7, 30, 60, 90, 120, 150, 200, 270, 365]:
            st = now_ms - bd * 86_400_000
            rows = post({"type": "candleSnapshot", "req": {"coin": coin, "interval": "1h", "startTime": st, "endTime": now_ms}})
            n = len(rows) if isinstance(rows, list) else -1
            d[f"{bd}d"] = n
            time.sleep(1.0)
        candle_depth[coin] = d
    results["candle_snapshot_depth"] = candle_depth

    # --- candle snapshot over the FULL label window (does it exist?) ---
    full_window = {}
    for coin in sample[:3]:
        rows = post({"type": "candleSnapshot", "req": {"coin": coin, "interval": "1h", "startTime": win_start, "endTime": win_end}})
        n = len(rows) if isinstance(rows, list) else -1
        full_window[coin] = n
        time.sleep(1.0)
    results["candle_snapshot_full_label_window"] = full_window

    OUT.write_text(json.dumps(results, indent=1))
    print(json.dumps(results, indent=1))


if __name__ == "__main__":
    main()