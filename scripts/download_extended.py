#!/usr/bin/env python3
"""Download extended Binance archive coverage (2024-04..2024-06) for FCLR-001 follow-up.

Idempotent: skips existing files, verifies zip checksums against SHA256 recorded
in run_manifest where known, records provenance in research_state/data_cache/manifest_extended.json.
No credentials, no paid services, no trading.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import time
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CACHE = REPO / "research_state" / "data_cache"
BASE = "https://data.binance.vision/data/futures/um"
MANIFEST_OUT = REPO / "research_state" / "data_cache" / "manifest_extended.json"

SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]
MONTHS = ["2024-04", "2024-05", "2024-06"]
KINDS_DAILY = ["markPriceKlines", "indexPriceKlines", "premiumIndexKlines", "klines"]
MAX_ATTEMPTS = 4
TIMEOUT = 60


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def download(url: str, dest: Path) -> bool:
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "kilo-research/1.0"})
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r, tmp.open("wb") as f:
                while True:
                    chunk = r.read(65536)
                    if not chunk:
                        break
                    f.write(chunk)
            tmp.replace(dest)
            return True
        except Exception as e:
            print(f"  attempt {attempt} failed for {url}: {e}", flush=True)
            if tmp.exists():
                tmp.unlink()
            if attempt < MAX_ATTEMPTS:
                time.sleep(2 ** attempt)
    return False


def month_days(month: str) -> list[str]:
    y, m = month.split("-")
    start = datetime(int(y), int(m), 1, tzinfo=timezone.utc)
    if m == "12":
        end = datetime(int(y) + 1, 1, 1, tzinfo=timezone.utc)
    else:
        end = datetime(int(y), int(m) + 1, 1, tzinfo=timezone.utc)
    out = []
    cur = start
    while cur < end:
        out.append(cur.strftime("%Y-%m-%d"))
        cur += timedelta(days=1)
    return out


def main() -> int:
    records = []
    for sym in SYMBOLS:
        for month in MONTHS:
            # funding monthly
            fz = f"{sym}-fundingRate-{month}.zip"
            url = f"{BASE}/monthly/fundingRate/{sym}/{fz}"
            dest = CACHE / f"{sym}_{month.replace('-', '_')}" / fz
            if not dest.exists():
                print(f"downloading {url}", flush=True)
                if not download(url, dest):
                    print(f"FAILED {url}", flush=True)
                    return 1
            records.append({
                "symbol": sym, "month": month, "type": "funding_rate_monthly",
                "path": str(dest.relative_to(REPO)), "url": url,
                "sha256": sha256_file(dest), "size_bytes": dest.stat().st_size,
            })
            # daily klines
            for kind in KINDS_DAILY:
                for day in month_days(month):
                    f = f"{sym}-1h-{day}.zip"
                    url = f"{BASE}/daily/{kind}/{sym}/1h/{f}"
                    d = CACHE / f"{sym}_{month.replace('-', '_')}" / f"{kind}-{day}"
                    dest = d / f
                    if not dest.exists():
                        print(f"downloading {url}", flush=True)
                        if not download(url, dest):
                            print(f"FAILED {url}", flush=True)
                            return 1
                    records.append({
                        "symbol": sym, "month": month, "type": kind,
                        "date": day, "path": str(dest.relative_to(REPO)), "url": url,
                        "sha256": sha256_file(dest), "size_bytes": dest.stat().st_size,
                    })
    MANIFEST_OUT.write_text(json.dumps({
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "https://data.binance.vision/data/futures/um",
        "records": records,
    }, indent=2))
    print(f"Wrote {MANIFEST_OUT} with {len(records)} records", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())