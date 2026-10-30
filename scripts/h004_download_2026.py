#!/usr/bin/env python3
"""Download Binance UM perp mark/index/premium klines + monthly fundingRate for the
5-symbol universe across 2026-04-01..2026-08-06 (Track A / FCLR-H004 feature history).

Unauthenticated, from data.binance.vision.  Writes *extracted CSVs* into
research_state/data_cache/<SYM>_<YYYY>_<MM>/<KIND>-<DAY>/<SYM>-1h-<DAY>.csv and
<SYM>_<YYYY>_<MM>/<SYM>-fundingRate-<MM>/<SYM>-fundingRate-<MM>.csv — the exact
layout scripts/run_evaluation.py expects (find_mark_csv / find_premium_csv /
find_index_csv / find_funding_csv).

Idempotent: skips files already present with non-zero size.  Never touches the
existing OHLCV klines zips (those sit at the month-dir root, not under a KIND-
subdirectory).

No credentials, no paid services, no trading.
"""
import os
import sys
import time
import datetime
import zipfile
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CACHE = REPO / "research_state" / "data_cache"
BASE = "https://data.binance.vision/data/futures/um/daily"
MONTHLY = "https://data.binance.vision/data/futures/um/monthly/fundingRate"
SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]
KINDS = ["markPriceKlines", "indexPriceKlines", "premiumIndexKlines"]
# feature history: 2026-04-01 .. 2026-08-06 (liquidation window 07-08..08-06 needs
# >=90d funding history and >=168h RV history before its first forecast origin)
START = datetime.date(2026, 4, 1)
END = datetime.date(2026, 8, 6)
DAYS = []
d = START
while d <= END:
    DAYS.append(d)
    d += datetime.timedelta(days=1)

MAX_ATTEMPTS = 4
TIMEOUT = 90


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
    results = {}
    # daily mark/index/premium klines
    for sym in SYMBOLS:
        for day in DAYS:
            ds = day.strftime("%Y-%m-%d")
            ym = f"{day.year:04d}-{day.month:02d}"
            for kind in KINDS:
                fname = f"{sym}-1h-{ds}.zip"
                url = f"{BASE}/{kind}/{sym}/1h/{fname}"
                dest = month_dir(sym, ym) / fname
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