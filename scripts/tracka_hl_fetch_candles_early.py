#!/usr/bin/env python3
"""Bounded first-time acquisition of Hyperliquid 1h candleSnapshot for GAP-TRACKA-EARLY-OBSERVED-2025H2_2026Q1.
Saves raw JSON per coin/month under research_state/data_cache/hyperliquid_candles/<COIN>/<YYYY-MM>.json
with .accessed.json provenance and .sha256 checksum. No redundant polling: skips months with existing
valid non-empty JSON list. Retries with backoff on errors/429. Bounded: missing months 2025-11..2026-04 only;
never re-fetches cached 2026-05..2026-10.
"""
from __future__ import annotations

import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

REPO = Path(__file__).resolve().parents[1]
RS = REPO / "research_state"
CACHE = RS / "data_cache" / "hyperliquid_candles"
CACHE.mkdir(parents=True, exist_ok=True)

INFO = "https://api.hyperliquid.xyz/info"
COINS = ["BTC", "ETH", "BNB", "SOL", "XRP", "AVAX", "DOGE", "LINK", "SUI"]
MONTHS = ["2025-11", "2025-12", "2026-01", "2026-02", "2026-03", "2026-04"]


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


def post(payload, retries=6, pause=2.0):
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


def main() -> None:
    summary = {"generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
               "coins": {}, "errors": [], "fetched": [], "cached": []}
    for coin in COINS:
        coin_dir = CACHE / coin
        coin_dir.mkdir(parents=True, exist_ok=True)
        summary["coins"][coin] = {}
        for m in MONTHS:
            out = coin_dir / f"{m}.json"
            accessed = coin_dir / f"{m}.accessed.json"
            sha = coin_dir / f"{m}.sha256"
            if out.exists():
                try:
                    data = json.loads(out.read_text())
                    if isinstance(data, list) and len(data) > 0 and accessed.exists() and sha.exists():
                        summary["coins"][coin][m] = {"status": "cached", "n": len(data)}
                        summary["cached"].append(f"{coin}/{m}")
                        continue
                except Exception:
                    pass
            s, e = month_range(m)
            data, err = post({"type": "candleSnapshot", "req": {"coin": coin, "interval": "1h", "startTime": s, "endTime": e}})
            fetched_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            if err is not None or not isinstance(data, list):
                summary["coins"][coin][m] = {"status": "error", "error": err, "fetched_utc": fetched_utc}
                summary["errors"].append(f"{coin} {m}: {err}")
                time.sleep(1.0)
                continue
            write_json_atomic(out, data)
            digest = hashlib.sha256(out.read_bytes()).hexdigest()
            sha.write_text(digest + "\n")
            provenance = {
                "fetched_utc": fetched_utc,
                "coin": coin,
                "month": m,
                "endpoint": "candleSnapshot",
                "interval": "1h",
                "start_ms": s,
                "end_ms": e,
                "rows": len(data),
                "sha256": digest,
                "http_status": 200,
                "api_key_required": False,
                "requester_pays": False,
                "signature_required": False,
                "unauthenticated": True,
            }
            write_json_atomic(accessed, provenance)
            summary["coins"][coin][m] = {"status": "fetched", "n": len(data), "fetched_utc": fetched_utc}
            summary["fetched"].append(f"{coin}/{m}")
            print(f"{coin} {m}: {len(data)} rows", flush=True)
            time.sleep(0.5)
        time.sleep(0.5)
    report_path = RS / f"tracka_hl_early_candle_fetch_report_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json"
    report_path.write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({"report": str(report_path), "fetched": len(summary["fetched"]), "cached": len(summary["cached"]), "errors": summary["errors"]}, indent=2))


if __name__ == "__main__":
    main()
