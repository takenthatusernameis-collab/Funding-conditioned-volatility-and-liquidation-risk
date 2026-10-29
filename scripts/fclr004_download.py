#!/usr/bin/env python3
"""Download FCLR-004 forward-extension data (2025-01..2025-12) for the 5-symbol panel.

FCLR-004 is a pre-registered follow-up to FCLR-003.  All three prior frozen
experiments (FCLR-001, FCLR-002, FCLR-003) consumed the 2024-01..2024-12-31
panel and their sealed holdouts cannot be reused.  This script pulls the
calendar year 2025 from the free, unauthenticated Binance public archive so
that a fresh >=3-block test window can be opened on data that no frozen
experiment has inspected.

Downloads ONLY the inputs the evaluation consumes:
  - markPriceKlines 1h  (realized-volatility features, EMA distance)
  - indexPriceKlines 1h (mark/index premium, per protocol)
  - premiumIndexKlines 1h (premium vs index cross-check)
  - fundingRate monthly  (signed funding, absolute-funding percentile)

Idempotent: skips existing files.  Coverage-only: no outcomes computed here.
No credentials, no paid services, no trading.
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CACHE = REPO / "research_state" / "data_cache"
BASE = "https://data.binance.vision/data/futures/um"
MANIFEST_OUT = REPO / "research_state" / "data_cache" / "manifest_fclr004.json"

SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]
MONTHS = ["2025-01", "2025-02", "2025-03", "2025-04", "2025-05", "2025-06",
          "2025-07", "2025-08", "2025-09", "2025-10", "2025-11", "2025-12"]
KINDS_DAILY = ["markPriceKlines", "indexPriceKlines", "premiumIndexKlines"]
MAX_ATTEMPTS = 4
TIMEOUT = 90


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
    failures = []
    for sym in SYMBOLS:
        for month in MONTHS:
            mdir = month.replace("-", "_")
            # fundingRate monthly
            fz = f"{sym}-fundingRate-{month}.zip"
            url = f"{BASE}/monthly/fundingRate/{sym}/{fz}"
            dest = CACHE / f"{sym}_{mdir}" / fz
            if not dest.exists():
                print(f"downloading {url}", flush=True)
                if not download(url, dest):
                    print(f"FAILED {url}", flush=True)
                    failures.append(url)
                    return 1
            records.append({
                "symbol": sym, "month": month, "type": "funding_rate_monthly",
                "path": str(dest.relative_to(REPO)), "url": url,
                "sha256": sha256_file(dest), "size_bytes": dest.stat().st_size,
            })
            # daily klines of each kind
            for kind in KINDS_DAILY:
                for day in month_days(month):
                    f = f"{sym}-1h-{day}.zip"
                    url = f"{BASE}/daily/{kind}/{sym}/1h/{f}"
                    d = CACHE / f"{sym}_{mdir}" / f"{kind}-{day}"
                    dest = d / f
                    if not dest.exists():
                        print(f"downloading {url}", flush=True)
                        if not download(url, dest):
                            print(f"FAILED {url}", flush=True)
                            failures.append(url)
                            return 1
                    records.append({
                        "symbol": sym, "month": month, "type": kind,
                        "date": day, "path": str(dest.relative_to(REPO)), "url": url,
                        "sha256": sha256_file(dest), "size_bytes": dest.stat().st_size,
                    })
    MANIFEST_OUT.write_text(json.dumps({
        "experiment": "FCLR-004",
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": BASE,
        "records": records,
    }, indent=2))
    print(f"Wrote {MANIFEST_OUT} with {len(records)} records", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())