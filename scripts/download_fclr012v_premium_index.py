#!/usr/bin/env python3
"""Download premium/index klines for the FCLR-012-V forward panel (all 5 symbols).

scripts/fclr012_download.py fetched premiumIndexKlines and indexPriceKlines only
for BTCUSDT (the coverage audit then reported 6 premium files/symbol because the
other four symbols were never fetched).  The C2 model form needs mark/index
premium, so a complete premium/index set across all five symbols is required for
a claim-worthy forward run.

Idempotent: skips files already present with non-zero size.  Coverage-only: no
outcomes are computed here.  No credentials, no paid services, no trading.
"""
import datetime
import sys
import time
import urllib.request
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CACHE = REPO / "research_state" / "data_cache"
BASE = "https://data.binance.vision/data/futures/um/daily"
SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]
KINDS = ["premiumIndexKlines", "indexPriceKlines"]
START = datetime.date(2026, 8, 7)
END = datetime.date(2026, 11, 2)

DAYS = []
d = START
while d <= END:
    DAYS.append(d)
    d += datetime.timedelta(days=1)

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
        except Exception as e:  # noqa: BLE001
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
    except Exception as e:  # noqa: BLE001
        return f"fail:{e}"


def month_dir(sym: str, month: str) -> Path:
    return CACHE / f"{sym}_{month.replace('-', '_')}"


def main() -> int:
    results = {}
    for sym in SYMBOLS:
        for day in DAYS:
            ds = day.strftime("%Y-%m-%d")
            ym = f"{day.year:04d}-{day.month:02d}"
            for kind in KINDS:
                fname = f"{sym}-1h-{ds}.zip"
                url = f"{BASE}/{kind}/{sym}/1h/{fname}"
                # write the zip INSIDE the KIND-<DAY> subdir so it never collides
                # with the OHLCV klines zips that live at the month-dir root.
                dest = month_dir(sym, ym) / f"{kind}-{ds}" / fname
                r = fetch(url, dest)
                csv_path = month_dir(sym, ym) / f"{kind}-{ds}" / fname.replace(".zip", ".csv")
                if r == "ok":
                    r = extract(dest, csv_path)
                key = f"{sym}/{kind}/{ds}"
                results[key] = r
                if r not in ("skip", "ok"):
                    print(f"  WARN {url} -> {r}", file=sys.stderr)
    ok = sum(1 for v in results.values() if v in ("ok", "skip"))
    print(f"done {ok}/{len(results)}")
    bad = {k: v for k, v in results.items() if v not in ("ok", "skip")}
    if bad:
        print("FAILURES:", bad)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())