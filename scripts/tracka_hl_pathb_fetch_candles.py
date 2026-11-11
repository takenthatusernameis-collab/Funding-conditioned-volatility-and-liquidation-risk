#!/usr/bin/env python3
"""Bounded, first-time Track A path-(b) mark-price candleSnapshot acquisition.

Fetches Hyperliquid 1h mark-price candleSnapshot for the 9 funded symbols,
2026-05..2026-10 (6 months), via unauthenticated POST to
https://api.hyperliquid.xyz/info {"type":"candleSnapshot","req":{...}}.

This is FIRST-TIME acquisition (no cache exists), NOT redundant polling.

Saves raw responses under:
  research_state/data_cache/hyperliquid_candles/<COIN>/<YYYY-MM>.json
plus a sibling <YYYY-MM>.sha256 and <YYYY-MM>.accessed.json per file.

Bounded: per-request retries with exponential backoff, honors 429s,
skips already-valid cached months, stops on persistent errors per coin.
Writes a manifest research_state/data_cache/hyperliquid_candles_manifest_<UTC>.json.
"""
from __future__ import annotations

import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

REPO = Path(__file__).resolve().parents[1]
CACHE = REPO / "research_state" / "data_cache" / "hyperliquid_candles"
MANIFEST_DIR = REPO / "research_state"
INFO = "https://api.hyperliquid.xyz/info"
COINS = ["BTC", "ETH", "BNB", "SOL", "XRP", "AVAX", "DOGE", "LINK", "SUI"]
MONTHS = ["2026-05", "2026-06", "2026-07", "2026-08", "2026-09", "2026-10"]

MAX_RETRIES = 6
BASE_PAUSE = 1.5
REQUEST_PAUSE = 0.6
COIN_PAUSE = 1.0
TIMEOUT = 30


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


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def post_with_retries(payload: dict, coin: str, month: str):
    """POST with bounded retries + backoff. Returns (parsed_or_None, status, error_or_None)."""
    last_error = None
    for attempt in range(MAX_RETRIES):
        try:
            r = requests.post(INFO, json=payload, timeout=TIMEOUT)
            if r.status_code == 200:
                try:
                    return r.json(), 200, None
                except Exception as e:
                    return None, 200, f"JSON parse error: {e}"
            if r.status_code == 429:
                last_error = f"HTTP 429 rate-limited"
                pause = (2 ** attempt) + (attempt * 0.1)
                print(f"  [429] {coin} {month} attempt {attempt+1}/{MAX_RETRIES}, sleeping {pause:.1f}s", flush=True)
                time.sleep(pause)
                continue
            if r.status_code in (500, 502, 503, 504):
                last_error = f"HTTP {r.status_code}"
                pause = (2 ** attempt) + (attempt * 0.1)
                print(f"  [{r.status_code}] {coin} {month} attempt {attempt+1}/{MAX_RETRIES}, sleeping {pause:.1f}s", flush=True)
                time.sleep(pause)
                continue
            last_error = f"HTTP {r.status_code}"
            print(f"  [{r.status_code}] {coin} {month} non-retryable", flush=True)
            return None, r.status_code, last_error
        except Exception as e:
            last_error = f"ERR {e}"
            pause = (2 ** attempt) + (attempt * 0.1)
            print(f"  [{last_error}] {coin} {month} attempt {attempt+1}/{MAX_RETRIES}, sleeping {pause:.1f}s", flush=True)
            time.sleep(pause)
    return None, None, last_error


def already_valid(coin: str, month: str):
    d = CACHE / coin
    jp = d / f"{month}.json"
    sp = d / f"{month}.sha256"
    ap = d / f"{month}.accessed.json"
    if jp.exists() and sp.exists() and ap.exists():
        try:
            expected = sp.read_text().strip()
            actual = sha256_bytes(jp.read_bytes())
            if expected == actual:
                meta = json.loads(ap.read_text())
                return True, meta
        except Exception:
            pass
    return False, None


def main() -> None:
    CACHE.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    manifest = {
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "purpose": "Track A path-(b) first-time mark-price 1h candleSnapshot acquisition 2026-05..2026-10 (9 symbols)",
        "endpoint": INFO,
        "coins": COINS,
        "months": MONTHS,
        "results": {},
        "skipped_cached": [],
        "errors": [],
        "elapsed_s": None,
    }
    t0 = time.time()

    for coin in COINS:
        coin_result = {"months": {}, "status": "ok", "error": None}
        print(f"=== {coin} ===", flush=True)
        for m in MONTHS:
            valid, meta = already_valid(coin, m)
            if valid:
                print(f"  {m}: already valid (cached, sha256={meta.get('sha256')}), skipping", flush=True)
                coin_result["months"][m] = {"status": "skipped_cached", "sha256": meta.get("sha256")}
                manifest["skipped_cached"].append(f"{coin}/{m}")
                continue

            s, e = month_range(m)
            payload = {"type": "candleSnapshot", "req": {"coin": coin, "interval": "1h", "startTime": s, "endTime": e}}
            data, status, err = post_with_retries(payload, coin, m)
            d = CACHE / coin
            d.mkdir(parents=True, exist_ok=True)
            jp = d / f"{m}.json"
            sp = d / f"{m}.sha256"
            ap = d / f"{m}.accessed.json"

            if data is None:
                coin_result["months"][m] = {"status": "failed", "error": err, "http_status": status}
                coin_result["status"] = "partial"
                manifest["errors"].append(f"{coin}/{m}: {err} (status={status})")
                print(f"  {m}: FAILED {err} (status={status})", flush=True)
                time.sleep(REQUEST_PAUSE)
                continue

            raw = json.dumps(data, sort_keys=True).encode("utf-8")
            digest = sha256_bytes(raw)
            jp.write_bytes(raw)
            sp.write_text(digest + "\n")
            accessed = {
                "fetched_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "coin": coin,
                "month": m,
                "endpoint": "candleSnapshot",
                "interval": "1h",
                "start_ms": s,
                "end_ms": e,
                "rows": len(data) if isinstance(data, list) else -1,
                "sha256": digest,
                "http_status": status,
            }
            ap.write_text(json.dumps(accessed, indent=1) + "\n")
            n = len(data) if isinstance(data, list) else 0
            coin_result["months"][m] = {"status": "fetched", "rows": n, "sha256": digest}
            print(f"  {m}: fetched {n} rows, sha256={digest[:12]}...", flush=True)
            time.sleep(REQUEST_PAUSE)

        manifest["results"][coin] = coin_result
        time.sleep(COIN_PAUSE)

    manifest["elapsed_s"] = round(time.time() - t0, 3)
    manifest_path = MANIFEST_DIR / f"data_cache/hyperliquid_candles_manifest_{ts}.json"
    # ensure dir
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=1) + "\n")
    print(json.dumps({
        "manifest": str(manifest_path),
        "elapsed_s": manifest["elapsed_s"],
        "skipped_cached": len(manifest["skipped_cached"]),
        "errors": len(manifest["errors"]),
    }, indent=1))


if __name__ == "__main__":
    main()
