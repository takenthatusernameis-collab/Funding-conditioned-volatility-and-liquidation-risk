#!/usr/bin/env python3
"""FCLR-LIQ-COMBINED-PANEL step 2: BOUNDED_CONTEXT_ACQUISITION.

Bounded first-time unauthenticated Hyperliquid market-context acquisition for the
15 funded coins of the combined metpie+ironflow observed-liquidation panel.

Why: the cached HL context only reaches 2025-11. The combined window starts
2025-03-22. This script fetches, for each funded coin:
  - 1h candleSnapshot for 2025-03..2025-04 (RV24h/rv168h need 1h bars; 1h is
    live-only for old ranges, so this MAY return empty -- recorded honestly, and
    4h is the guaranteed fallback for RV estimation).
  - 4h candleSnapshot for 2025-03..2025-10 (complete historical candles).
  - fundingHistory for 2025-03..2025-10 (signed + premium).

Only the 6 funded coins lacking a 2025-05..2025-10 4h cache are fetched for
2025-05..2025-10; all 15 funded coins are fetched for 2025-03..2025-04.

Idempotent: skips any coin/month with an existing non-empty JSON + .accessed +
.sha256. Provenance-stamped (.accessed.json + .sha256 per coin/month). Bounded
pagination (chunked fundingHistory), exponential backoff with a max retry budget.
No keys, no signature, no requester-pays, no paid/credentialed/manual data.
Never fabricates: empty results are recorded as empty and retried only within
the retry budget; a permanently empty source is documented, not synthesized.
"""
from __future__ import annotations

import hashlib
import json
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests

REPO = Path(__file__).resolve().parents[1]
RS = REPO / "research_state"
CACHE = RS / "data_cache"
CANDLES_1H = CACHE / "hyperliquid_candles_1h_combined"
CANDLES_4H = CACHE / "hyperliquid_candles_4h_early"  # reuse existing early 4h store
FUNDING = CACHE / "hyperliquid_funding_early"        # reuse existing early funding store
for d in (CANDLES_1H, CANDLES_4H, FUNDING):
    d.mkdir(parents=True, exist_ok=True)

INFO = "https://api.hyperliquid.xyz/info"

# 15 funded coins (>=5000 combined observed-liquidation events AND cached HL funding).
FUNDED = ["AAVE", "ADA", "AVAX", "BNB", "BTC", "CRV", "DOGE", "ETH",
          "LINK", "LTC", "NEAR", "SOL", "SUI", "UNI", "XRP"]

# Coins that already have a 2025-05..2025-10 4h cache (fetched for 2025-03..04 only).
EARLY_4H_CACHED = {"AVAX", "BNB", "BTC", "DOGE", "ETH", "LINK", "SOL", "SUI", "XRP"}
# Coins missing 2025-05..2025-10 4h cache (fetched for the full 2025-03..2025-10).
MISSING_4H = [c for c in FUNDED if c not in EARLY_4H_CACHED]

EARLY_MONTHS = ["2025-03", "2025-04"]                      # fetch for ALL 15 funded
LATE_MONTHS = ["2025-05", "2025-06", "2025-07", "2025-08", "2025-09", "2025-10"]
FUND_CHUNK_DAYS = 21
MAX_RETRIES = 8


def iso_ms(s: str) -> int:
    return int(datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp() * 1000)


def month_range(m: str):
    y, mo = m.split("-")
    start = iso_ms(f"{y}-{mo}-01T00:00:00Z")
    if mo == "12":
        ny, nmo = f"{int(y) + 1}", "01"
    else:
        ny, nmo = y, f"{int(mo) + 1:02d}"
    end = iso_ms(f"{ny}-{nmo}-01T00:00:00Z") - 1
    return start, end


def post(payload, retries: int = MAX_RETRIES, pause: float = 2.0):
    last = None
    for attempt in range(retries):
        try:
            r = requests.post(INFO, json=payload, timeout=30)
            if r.status_code == 200:
                try:
                    return r.json(), None
                except Exception as e:
                    last = f"JSON_ERR {e}"
            else:
                last = f"HTTP {r.status_code}"
                if r.status_code == 429:
                    time.sleep(pause * (2 ** attempt) + 1.0)
                    continue
        except Exception as e:
            last = f"ERR {e}"
        time.sleep(pause * (1.5 ** attempt))
    return None, last


def write_json_atomic(p: Path, obj) -> None:
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, separators=(",", ":")) + "\n")
    tmp.replace(p)


def provenance(coin, month, endpoint, interval, start_ms, end_ms, rows, digest):
    return {
        "fetched_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "coin": coin,
        "month": month,
        "endpoint": endpoint,
        "interval": interval,
        "start_ms": start_ms,
        "end_ms": end_ms,
        "rows": rows,
        "sha256": digest,
        "http_status": 200,
        "api_key_required": False,
        "requester_pays": False,
        "signature_required": False,
        "unauthenticated": True,
        "license": "Hyperliquid public API, unauthenticated; no terms restriction on research use identified",
    }


def fetch_candles(coin: str, interval: str, months: list[str], store: Path,
                  summary: dict, fetched: list, cached: list, empty: list) -> None:
    cdir = store / coin
    cdir.mkdir(parents=True, exist_ok=True)
    for m in months:
        out = cdir / f"{m}.json"
        acc = cdir / f"{m}.accessed.json"
        sha = cdir / f"{m}.sha256"
        if out.exists():
            try:
                data = json.loads(out.read_text())
                if isinstance(data, list) and len(data) > 0 and acc.exists() and sha.exists():
                    cached.append(f"{coin}/{m}")
                    continue
            except Exception:
                pass
        s, e = month_range(m)
        data, err = post({"type": "candleSnapshot",
                          "req": {"coin": coin, "interval": interval,
                                  "startTime": s, "endTime": e}})
        if err is not None or not isinstance(data, list):
            summary["errors"].append(f"{coin}/{m} {interval}: {err}")
            empty.append(f"{coin}/{m}/{interval}")
            time.sleep(1.0)
            continue
        write_json_atomic(out, data)
        digest = hashlib.sha256(out.read_bytes()).hexdigest()
        sha.write_text(digest + "\n")
        write_json_atomic(acc, provenance(coin, m, "candleSnapshot", interval, s, e, len(data), digest))
        if len(data) == 0:
            empty.append(f"{coin}/{m}/{interval}")
        else:
            fetched.append(f"{coin}/{m}/{interval}")
        time.sleep(0.4)


def fetch_funding(coin: str, summary: dict, fetched: list) -> None:
    out = FUNDING / f"{coin}.json"
    acc = FUNDING / f"{coin}.accessed.json"
    sha = FUNDING / f"{coin}.sha256"
    # Merge mode: existing early funding file (2025-05..2025-10) + new early-2025
    # fetch. We fetch 2025-03-01..2025-10-31 as a single bounded paginated pass and
    # merge with any existing records, deduped on time.
    existing = []
    if out.exists():
        try:
            existing = json.loads(out.read_text())
        except Exception:
            existing = []
    by_time = {int(r["time"]): r for r in existing if isinstance(r, dict) and "time" in r}
    start = iso_ms("2025-03-01T00:00:00Z")
    end = iso_ms("2025-10-31T23:59:59Z")
    cur = datetime.fromtimestamp(start / 1000, tz=timezone.utc)
    end_dt = datetime.fromtimestamp(end / 1000, tz=timezone.utc)
    new = 0
    while cur < end_dt:
        chunk_end = min(cur + timedelta(days=FUND_CHUNK_DAYS), end_dt)
        data, err = post({"type": "fundingHistory", "coin": coin,
                          "startTime": int(cur.timestamp() * 1000),
                          "endTime": int(chunk_end.timestamp() * 1000)})
        if err is None and isinstance(data, list):
            for r in data:
                if isinstance(r, dict) and "time" in r:
                    by_time[int(r["time"])] = r
                    new += 1
        else:
            summary["errors"].append(f"funding {coin} {cur.date()}: {err}")
        cur = chunk_end
        time.sleep(0.15)
    merged = [by_time[k] for k in sorted(by_time)]
    write_json_atomic(out, merged)
    digest = hashlib.sha256(out.read_bytes()).hexdigest()
    sha.write_text(digest + "\n")
    write_json_atomic(acc, provenance(coin, "2025-03..2025-10", "fundingHistory", "1h",
                                      start, end, len(merged), digest))
    fetched.append(f"funding/{coin}")
    print(f"funding {coin}: merged={len(merged)} new={new}", flush=True)


def main() -> int:
    summary = {
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "experiment_id": "FCLR-LIQ-COMBINED-PANEL-20261115T170000Z",
        "phase": "BOUNDED_CONTEXT_ACQUISITION",
        "funded_coins": FUNDED,
        "missing_4h_coins_full_early": MISSING_4H,
        "notes": "1h candleSnapshot is live-only for old ranges (may return []); 4h is complete. Empty recorded honestly, not synthesized.",
        "errors": [], "fetched": [], "cached": [], "empty": [],
    }
    fetched, cached, empty = [], [], []
    # 1h candles: 2025-03..2025-04 for all 15 funded (RV24h/168h inputs)
    for coin in FUNDED:
        fetch_candles(coin, "1h", EARLY_MONTHS, CANDLES_1H, summary, fetched, cached, empty)
        time.sleep(0.3)
    # 4h candles: 2025-03..04 all 15; 2025-05..10 only the 6 missing
    for coin in FUNDED:
        months = EARLY_MONTHS + (LATE_MONTHS if coin in MISSING_4H else [])
        fetch_candles(coin, "4h", months, CANDLES_4H, summary, fetched, cached, empty)
        time.sleep(0.3)
    # funding: bounded paginated merge 2025-03..2025-10 for all 15 funded
    for coin in FUNDED:
        fetch_funding(coin, summary, fetched)
        time.sleep(0.2)
    summary["fetched"] = fetched
    summary["cached"] = cached
    summary["empty"] = sorted(set(empty))
    report_path = RS / f"fclr_liq_combined_context_fetch_report_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json"
    report_path.write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({"report": str(report_path),
                      "fetched": len(fetched), "cached": len(cached),
                      "empty": len(summary["empty"]),
                      "errors": summary["errors"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())