#!/usr/bin/env python3
"""Download Binance UM perp mark/index/premium klines + monthly fundingRate for the
5-symbol universe across 2025-01-01..2026-05-22 (FCLR-007 pristine confirmatory window).

This window is chosen to be ENTIRELY BEFORE the already-inspected FCLR-006 window
(2026-05-23..2026-08-06), so no sealed/inspected holdout is reused as fresh evidence
(RESEARCH_PROMPT.md §13, §17).  It is also entirely AFTER the FCLR-003 window
(2024-10-02..2024-12-31), so it is a genuinely new, unsealed, never-evaluated panel.

Writes *extracted CSVs* into
research_state/data_cache/<SYM>_<YYYY>_<MM>/<KIND>-<DAY>/<SYM>-1h-<DAY>.csv and
<SYM>_<YYYY>_<MM>/<SYM>-fundingRate-<MM>/<SYM>-fundingRate-<MM>.csv — the exact
layout scripts/run_evaluation.py expects (find_mark_csv / find_premium_csv /
find_index_csv / find_funding_csv).

Idempotent: skips files already present with non-zero size.

No credentials, no paid services, no trading.
"""
import os
import sys
import time
import datetime
import zipfile
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CACHE = REPO / "research_state" / "data_cache"
BASE = "https://data.binance.vision/data/futures/um/daily"
MONTHLY = "https://data.binance.vision/data/futures/um/monthly/fundingRate"
SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]
KINDS = ["markPriceKlines", "indexPriceKlines", "premiumIndexKlines"]
START = datetime.date(2025, 1, 1)
END = datetime.date(2026, 5, 22)
DAYS = []
d = START
while d <= END:
    DAYS.append(d)
    d += datetime.timedelta(days=1)

MAX_ATTEMPTS = 4
TIMEOUT = 90

months = []
cur = datetime.date(2025, 1, 1)
while cur <= END:
    months.append(cur.strftime("%Y-%m"))
    cur = (datetime.date(cur.year, cur.month + 1, 1) if cur.month < 12
           else datetime.date(cur.year + 1, 1, 1))


def fetch(url: str, dest: Path) -> str:
    """Download a zip into dest (a .zip file), with retries."""
    if dest.exists() and dest.stat().st_size > 0:
        return "skip"
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    last_err = None
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "kilo-research/1.0"})
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r, tmp.open("wb") as f:
                while True:
                    chunk = r.read(65536)
                    if not chunk:
                        break
                    f.write(chunk)
            if tmp.stat().st_size < 50:
                tmp.unlink()
                return "empty"
            tmp.replace(dest)
            return "ok"
        except Exception as e:
            last_err = e
            if tmp.exists():
                tmp.unlink()
            if attempt < MAX_ATTEMPTS:
                time.sleep(2 ** attempt)
    return f"fail:{last_err}"


def extract(zip_path: Path, csv_path: Path) -> str:
    """Extract the single CSV inside a funding/kline zip to csv_path."""
    if csv_path.exists() and csv_path.stat().st_size > 0:
        return "skip"
    try:
        with zipfile.ZipFile(zip_path) as z:
            names = z.namelist()
            if not names:
                return "emptyzip"
            csv_path.parent.mkdir(parents=True, exist_ok=True)
            csv_path.write_bytes(z.read(names[0]))
        return "ok"
    except Exception as e:
        return f"fail:{e}"


def month_dir(sym: str, month: str) -> Path:
    return CACHE / f"{sym}_{month.replace('-', '_')}"


def main() -> int:
    # Build the full (url, dest, csv_path) task list first, then download in parallel.
    tasks = []
    for sym in SYMBOLS:
        for day in DAYS:
            ds = day.strftime("%Y-%m-%d")
            ym = f"{day.year:04d}-{day.month:02d}"
            for kind in KINDS:
                fname = f"{sym}-1h-{ds}.zip"
                url = f"{BASE}/{kind}/{sym}/1h/{fname}"
                dest = month_dir(sym, ym) / fname
                csv_path = month_dir(sym, ym) / f"{kind}-{ds}" / fname.replace(".zip", ".csv")
                tasks.append((f"{sym}/{kind}/{ds}", url, dest, csv_path))
    for sym in SYMBOLS:
        for month in months:
            fname = f"{sym}-fundingRate-{month}.zip"
            url = f"{MONTHLY}/{sym}/{fname}"
            dest = month_dir(sym, month) / fname
            csv_path = month_dir(sym, month) / f"{sym}-fundingRate-{month}" / fname.replace(".zip", ".csv")
            tasks.append((f"{sym}/fundingRate/{month}", url, dest, csv_path))

    results = {}
    fail = []

    def run(task):
        key, url, dest, csv_path = task
        r = fetch(url, dest)
        if r == "ok":
            r = extract(dest, csv_path)
        return key, r

    with ThreadPoolExecutor(max_workers=16) as ex:
        futs = {ex.submit(run, t): t[0] for t in tasks}
        done = 0
        for fut in as_completed(futs):
            key, r = fut.result()
            results[key] = r
            done += 1
            if r not in ("skip", "ok"):
                fail.append((key, r))
            if done % 500 == 0:
                print(f"  progress {done}/{len(tasks)}", file=sys.stderr, flush=True)

    ok = sum(1 for v in results.values() if v in ("ok", "skip"))
    print(f"done {ok}/{len(results)}")
    if fail:
        print("FAILURES:", fail[:50])
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())