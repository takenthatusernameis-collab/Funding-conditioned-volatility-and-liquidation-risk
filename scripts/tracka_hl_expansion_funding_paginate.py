#!/usr/bin/env python3
"""Paginate Hyperliquid fundingHistory (API caps at 500 rows per call) for expansion
candidates until full 2026-05-01..2026-10-31 coverage. Bounded, unauthenticated,
provenanced; skips coins already fully covered.
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
FUNDING = RS / "data_cache" / "hyperliquid_funding"
INFO = "https://api.hyperliquid.xyz/info"
COINS = ["ZEC", "NEAR", "UNI", "AAVE", "CRV", "ADA", "LTC", "BCH"]
END_MS = int(datetime(2026, 10, 31, 23, 59, 59, tzinfo=timezone.utc).timestamp() * 1000) + 999
MAX_CHUNKS = 12  # hard bound per coin


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


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


def main() -> None:
    summary = {"generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "coins": {}, "errors": []}
    for coin in COINS:
        p = FUNDING / f"{coin}.json"
        data = json.loads(p.read_text()) if p.exists() else []
        times = [r.get("time") for r in data if r.get("time") is not None]
        last_ms = max(times) if times else int(datetime(2026, 5, 1, tzinfo=timezone.utc).timestamp() * 1000) - 1
        chunks = 0
        while last_ms < END_MS and chunks < MAX_CHUNKS:
            chunks += 1
            fetched_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            chunk, err = post({"type": "fundingHistory", "coin": coin, "startTime": last_ms + 1, "endTime": END_MS})
            if err is not None or not isinstance(chunk, list):
                summary["coins"][coin] = summary["coins"].get(coin, {})
                summary["coins"][coin][f"chunk_{chunks}"] = {"status": "error", "error": err, "fetched_utc": fetched_utc}
                summary["errors"].append(f"{coin} chunk {chunks}: {err}")
                time.sleep(1.0)
                break
            if not chunk:
                break
            data.extend(chunk)
            new_last = max(r.get("time") for r in chunk if r.get("time") is not None)
            if new_last <= last_ms:
                break  # no progress
            last_ms = new_last
            time.sleep(0.6)
        seen = {}
        for r in data:
            seen.setdefault(r.get("time"), r)
        data = [seen[t] for t in sorted(seen) if t is not None]
        p.write_text(json.dumps(data, separators=(",", ":")))
        raw = json.dumps(data, separators=(",", ":")).encode()
        (FUNDING / f"{coin}.sha256").write_text(sha256_bytes(raw) + "\n")
        prov = {"fetched_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "coin": coin, "endpoint": "fundingHistory", "paginated_chunks": chunks,
                "start_ms": int(datetime(2026, 5, 1, tzinfo=timezone.utc).timestamp() * 1000),
                "end_ms": END_MS, "rows": len(data), "sha256": sha256_bytes(raw),
                "http_status": 200, "api_key_required": False, "requester_pays": False,
                "signature_required": False, "unauthenticated": True,
                "coverage_first_ms": min(r.get("time") for r in data if r.get("time") is not None),
                "coverage_last_ms": last_ms}
        (FUNDING / f"{coin}.accessed.json").write_text(json.dumps(prov, indent=2) + "\n")
        summary["coins"][coin] = {"rows": len(data), "chunks": chunks,
                                  "coverage_first_ms": prov["coverage_first_ms"],
                                  "coverage_last_ms": prov["coverage_last_ms"],
                                  "end_target_ms": END_MS}
        print(f"{coin}: {len(data)} rows, chunks={chunks}, last={last_ms}", flush=True)
        time.sleep(0.5)
    report_path = RS / f"tracka_hl_expansion_funding_paginate_report_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json"
    report_path.write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({"report": str(report_path), "errors": summary["errors"]}, indent=2))


if __name__ == "__main__":
    main()
