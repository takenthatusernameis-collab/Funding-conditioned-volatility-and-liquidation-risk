#!/usr/bin/env python3
"""Fill the 2025-01..2026-08 mark/index/premium/funding gap in the Binance archive cache.

Discovered 2026-10-30: the Binance public-data archive DOES contain 2025 and 2026
daily markPriceKlines/indexPriceKlines/premiumIndexKlines/klines and monthly
fundingRate files.  Earlier 404 probes in this repo used the wrong path prefix
(`data/um/...` instead of `data/futures/um/...`) and the wrong shape (per-day
`*.csv` instead of per-day `*.zip`), which produced a false "archive ends 2024"
conclusion.  This script re-derives the correct provenanced path and backfills
the gap idempotently.

Correct layout (verified live 2026-10-30, HTTP 200):
  daily   : data/futures/um/daily/{kind}/{SYM}/1h/{SYM}-1h-{YYYY-MM-DD}.zip
  monthly : data/futures/um/monthly/fundingRate/{SYM}/{SYM}-fundingRate-{YYYY-MM}.zip
  kinds   : markPriceKlines, indexPriceKlines, premiumIndexKlines, klines

Coverage-only: no outcomes are computed here.  No credentials, no paid services,
no trading.  Idempotent: existing files are skipped.
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
import urllib.request
import zipfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CACHE = REPO / "research_state" / "data_cache"
BASE = "https://data.binance.vision/data/futures/um"
MANIFEST_OUT = REPO / "research_state" / "data_cache" / "manifest_gapfill.json"

SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]
# Fill every missing month from 2025-01 through 2026-08 inclusive.
MONTHS = []
_cur = datetime(2025, 1, 1, tzinfo=timezone.utc)
_end = datetime(2026, 8, 1, tzinfo=timezone.utc)
while _cur <= _end:
    MONTHS.append(_cur.strftime("%Y-%m"))
    _cur += timedelta(days=31)
    _cur = _cur.replace(day=1)

KINDS_DAILY = ["markPriceKlines", "indexPriceKlines", "premiumIndexKlines", "klines"]
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
        except Exception as e:  # noqa: BLE001
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
    failed = []
    for sym in SYMBOLS:
        for month in MONTHS:
            # monthly funding rate
            fz = f"{sym}-fundingRate-{month}.zip"
            url = f"{BASE}/monthly/fundingRate/{sym}/{fz}"
            dest = CACHE / f"{sym}_{month.replace('-', '_')}" / fz
            if not dest.exists():
                print(f"downloading {url}", flush=True)
                if not download(url, dest):
                    print(f"FAILED {url}", flush=True)
                    failed.append(url)
                    continue
            records.append({
                "symbol": sym, "month": month, "type": "funding_rate_monthly",
                "path": str(dest.relative_to(REPO)), "url": url,
                "sha256": sha256_file(dest), "size_bytes": dest.stat().st_size,
            })
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
                            failed.append(url)
                            continue
                    records.append({
                        "symbol": sym, "month": month, "type": kind,
                        "date": day, "path": str(dest.relative_to(REPO)), "url": url,
                        "sha256": sha256_file(dest), "size_bytes": dest.stat().st_size,
                    })
    MANIFEST_OUT.write_text(json.dumps({
        "experiment": "FCLR-002-gapfill",
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "https://data.binance.vision/data/futures/um",
        "records": records,
        "failed": failed,
    }, indent=2))
    print(f"Wrote {MANIFEST_OUT} with {len(records)} records, {len(failed)} failures", flush=True)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())