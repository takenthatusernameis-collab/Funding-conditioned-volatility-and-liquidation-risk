#!/usr/bin/env python3
import json
import os
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests

REPO = Path(__file__).resolve().parents[1]
CACHE_DIR = REPO / "research_state" / "data_cache" / "hyperliquid_funding"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
RESEARCH_STATE = REPO / "research_state"

API_URL = "https://api.hyperliquid.xyz/info"

# Ironflow overlap - check symbols
IRONFLOW = REPO / "research_state" / "data_cache" / "ironflow_events"
DEFAULT_COINS = ["BTC", "ETH", "SOL", "BNB", "XRP", "AVAX", "DOGE", "LINK", "SUI", "ARB", "OP", "MATIC", "APT"]

def fetch_funding(coin, start_ms, end_ms):
    payload = {"type": "fundingHistory", "coin": coin, "startTime": start_ms, "endTime": end_ms}
    headers = {"Content-Type": "application/json"}
    max_retries = 8
    for attempt in range(max_retries):
        try:
            resp = requests.post(API_URL, json=payload, headers=headers, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                if isinstance(data, list):
                    return data
                return []
            elif resp.status_code in (429, 500, 502, 503, 504):
                time.sleep((2 ** attempt) + (attempt * 0.1))
                continue
            else:
                time.sleep((2 ** attempt))
                continue
        except Exception as e:
            time.sleep((2 ** attempt))
            continue
    return []

def main():
    start = datetime(2025, 11, 1, 0, 0, 0, tzinfo=timezone.utc)
    end = datetime(2026, 10, 30, 23, 59, 59, tzinfo=timezone.utc)

    coins_to_fetch = DEFAULT_COINS
    results = {}

    for coin in coins_to_fetch:
        all_records = []
        # Paginate in ~21 day chunks
        chunk_days = 21
        cur = start
        while cur < end:
            chunk_end = min(cur + timedelta(days=chunk_days), end)
            start_ms = int(cur.timestamp() * 1000)
            end_ms = int(chunk_end.timestamp() * 1000)
            records = fetch_funding(coin, start_ms, end_ms)
            if records:
                all_records.extend(records)
            cur = chunk_end
            time.sleep(0.1)  # rate limit courtesy

        if all_records:
            # Save as parquet-like structure - but we need pandas/pyarrow? Let us write as json first then convert
            out_path = CACHE_DIR / f"{coin}.json"
            with open(out_path, 'w') as f:
                json.dump(all_records, f)
            results[coin] = len(all_records)
            print(f"Fetched {coin}: {len(all_records)} records")
        else:
            print(f"Fetched {coin}: 0 records")
            results[coin] = 0

    # Write audit
    audit_path = RESEARCH_STATE / "liqmicro_funding_audit_002.md"
    lines = []
    lines.append("# LIQMICRO FUNDING AUDIT 002 (Hyperliquid fundingHistory)")
    lines.append(f"**TIMESTAMP (UTC):** {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}")
    lines.append(f"**API:** https://api.hyperliquid.xyz/info (unauthenticated, type=fundingHistory)")
    lines.append(f"**Range:** {start.isoformat()} to {end.isoformat()}")
    lines.append("")
    lines.append("## Coins fetched")
    for coin, cnt in results.items():
        lines.append(f"- {coin}: {cnt} records")
    lines.append("")
    audit_path.write_text("\n".join(lines))
    print(f"Wrote audit to {audit_path}")

if __name__ == '__main__':
    main()
