#!/usr/bin/env python3
"""Download Binance UM perp mark/index/premium klines for 2024-01-01..2024-03-31.

Unblocks FCLR-H002 (funding-extreme correction-time replication). The pre-registered
replication computes a trailing 24h realized-volatility regime split at each funding
extreme; that split was previously uncomputable because no Jan-Mar 2024 mark prices
were cached (research_state/h002_replication_report.md §4, research_state/
h002_replication_blocker.md). This campaign fills that gap with the canonical
data.binance.vision daily archive, writing into the same nested layout that
scripts/h004_download_2026.py and scripts/run_evaluation.py expect:

    research_state/data_cache/<SYM>_<YYYY>_<MM>/<KIND>-<DAY>/<SYM>-1h-<DAY>.csv

Idempotent: skips files already present with non-zero size.  Never touches the
repo-root markPriceKlines-1h-* directories (those contain OHLCV klines, not mark
prices — see research_state/h002_replication_report.md traceability note).

No credentials, no paid services, no trading.
"""
from __future__ import annotations

import datetime
import io
import sys
import time
import urllib.request
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CACHE = REPO / "research_state" / "data_cache"
BASE = "https://data.binance.vision/data/futures/um/daily"
KINDS = ["markPriceKlines", "indexPriceKlines", "premiumIndexKlines"]
SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]
START = datetime.date(2024, 1, 1)
END = datetime.date(2024, 3, 31)

MAX_ATTEMPTS = 4
TIMEOUT = 90
WORKERS = 8


def day_list():
    days = []
    d = START
    while d <= END:
        days.append(d)
        d += datetime.timedelta(days=1)
    return days


def month_dir(sym: str, day: datetime.date) -> Path:
    return CACHE / f"{sym}_{day.year:04d}_{day.month:02d}"


def fetch_one(task):
    """Download one daily zip; return (key, status)."""
    sym, day, kind = task
    ds = day.strftime("%Y-%m-%d")
    fname = f"{sym}-1h-{ds}.zip"
    url = f"{BASE}/{kind}/{sym}/1h/{fname}"
    dest = month_dir(sym, day) / fname
    csv_path = month_dir(sym, day) / f"{kind}-{ds}" / fname.replace(".zip", ".csv")
    key = f"{sym}/{kind}/{ds}"
    if csv_path.exists() and csv_path.stat().st_size > 0:
        return key, "skip"
    if dest.exists() and dest.stat().st_size > 0:
        # zip present but not yet extracted
        try:
            with zipfile.ZipFile(dest) as z:
                names = z.namelist()
                if not names:
                    return key, "emptyzip"
                csv_path.parent.mkdir(parents=True, exist_ok=True)
                csv_path.write_bytes(z.read(names[0]))
            return key, "ok"
        except Exception as e:
            return key, f"fail:{e}"
    dest.parent.mkdir(parents=True, exist_ok=True)
    last_err = None
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "kilo-research/1.0"})
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r, dest.with_suffix(dest.suffix + ".part").open("wb") as f:
                while True:
                    chunk = r.read(65536)
                    if not chunk:
                        break
                    f.write(chunk)
            tmp = dest.with_suffix(dest.suffix + ".part")
            if tmp.stat().st_size < 50:
                tmp.unlink()
                return key, "empty"
            tmp.replace(dest)
            with zipfile.ZipFile(dest) as z:
                names = z.namelist()
                if not names:
                    return key, "emptyzip"
                csv_path.parent.mkdir(parents=True, exist_ok=True)
                csv_path.write_bytes(z.read(names[0]))
            return key, "ok"
        except Exception as e:
            last_err = e
            tmp = dest.with_suffix(dest.suffix + ".part")
            if tmp.exists():
                tmp.unlink()
            if attempt < MAX_ATTEMPTS:
                time.sleep(2 ** attempt)
    return key, f"fail:{last_err}"


def main() -> int:
    tasks = [(sym, day, kind) for sym in SYMBOLS for day in day_list() for kind in KINDS]
    results = {}
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futs = {ex.submit(fetch_one, t): t for t in tasks}
        for i, fut in enumerate(as_completed(futs), start=1):
            key, status = fut.result()
            results[key] = status
            if status not in ("skip", "ok"):
                print(f"  WARN {key} -> {status}", file=sys.stderr)
            if i % 200 == 0:
                print(f"  progress {i}/{len(tasks)}", file=sys.stderr)
    ok = sum(1 for v in results.values() if v in ("ok", "skip"))
    print(f"done {ok}/{len(results)}")
    bad = {k: v for k, v in results.items() if v not in ("ok", "skip")}
    if bad:
        print("FAILURES:", bad)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())