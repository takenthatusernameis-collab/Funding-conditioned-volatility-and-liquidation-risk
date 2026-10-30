#!/usr/bin/env python3
"""Complete the FCLR-H004 / Track A 2026 feature cache.

The 2026 markPriceKlines + fundingRate for the 5-symbol universe were already
downloaded by scripts/h004_download_2026.py.  This script fills the REMAINING
inputs the evaluation consumes:

  - indexPriceKlines 1h  (mark/index premium)
  - premiumIndexKlines 1h (premium vs index cross-check)
  - fundingRate monthly  (signed funding, absolute-funding percentile)

Layout mirrors h004_download_2026.py so scripts/run_evaluation_fixed.py
(find_mark_csv / find_premium_csv / find_index_csv / find_funding_csv) resolves
the same paths.

Idempotent: skips files already present with non-zero size.  Unauthenticated,
from data.binance.vision.  No credentials, no paid services, no trading.
"""
import datetime
import sys
import time
import zipfile
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CACHE = REPO / "research_state" / "data_cache"
BASE = "https://data.binance.vision/data/futures/um/daily"
MONTHLY = "https://data.binance.vision/data/futures/um/monthly/fundingRate"
SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]
KINDS = ["indexPriceKlines", "premiumIndexKlines"]
START = datetime.date(2026, 4, 1)
END = datetime.date(2026, 8, 6)
MAX_ATTEMPTS = 4
TIMEOUT = 90


def fetch(url: str, dest: Path) -> str:
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
    results = {}
    days = []
    d = START
    while d <= END:
        days.append(d)
        d += datetime.timedelta(days=1)

    # daily index/premium klines
    for sym in SYMBOLS:
        for day in days:
            ds = day.strftime("%Y-%m-%d")
            ym = f"{day.year:04d}-{day.month:02d}"
            for kind in KINDS:
                fname = f"{sym}-1h-{ds}.zip"
                url = f"{BASE}/{kind}/{sym}/1h/{fname}"
                # NOTE: the bare filename is identical across kinds, so the zip
                # MUST live under a kind-specific subdir.  Putting it at the
                # month root would collide with the markPriceKlines zips that
                # h004_download_2026.py already placed there and silently skip.
                dest = month_dir(sym, ym) / kind / fname
                r = fetch(url, dest)
                csv_path = month_dir(sym, ym) / f"{kind}-{ds}" / fname.replace(".zip", ".csv")
                if r == "ok":
                    r = extract(dest, csv_path)
                key = f"{sym}/{kind}/{ds}"
                results[key] = r
                if r not in ("skip", "ok"):
                    print(f"  WARN {url} -> {r}", file=sys.stderr)

    # monthly fundingRate
    months = []
    cur = datetime.date(2026, 4, 1)
    while cur <= END:
        months.append(cur.strftime("%Y-%m"))
        cur = datetime.date(cur.year, cur.month + 1, 1) if cur.month < 12 else datetime.date(cur.year + 1, 1, 1)
    for sym in SYMBOLS:
        for month in months:
            fname = f"{sym}-fundingRate-{month}.zip"
            url = f"{MONTHLY}/{sym}/{fname}"
            dest = month_dir(sym, month) / fname
            r = fetch(url, dest)
            csv_path = month_dir(sym, month) / f"{sym}-fundingRate-{month}" / fname.replace(".zip", ".csv")
            if r == "ok":
                r = extract(dest, csv_path)
            results[f"{sym}/fundingRate/{month}"] = r
            if r not in ("skip", "ok"):
                print(f"  WARN funding {sym} {month} -> {r}", file=sys.stderr)

    ok = sum(1 for v in results.values() if v in ("ok", "skip"))
    print(f"done {ok}/{len(results)}")
    bad = {k: v for k, v in results.items() if v not in ("ok", "skip")}
    if bad:
        print("FAILURES:", bad)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())