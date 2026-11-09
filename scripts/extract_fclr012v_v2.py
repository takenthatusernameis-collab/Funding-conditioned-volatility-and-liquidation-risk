#!/usr/bin/env python3
"""Extract already-downloaded 2026-11 Binance zips into the CSV layout run_evaluation.py
expects, and fetch+extract any 2026-11 days still missing from the live archive.

This is the FCLR-012-V v2 trigger execution: the pre-registered forward campaign
(forward_campaign_fclr012_prereg.md) fires when a new unsealed 2026 Binance panel
exists beyond 2026-11-02.  Live probes (research_state/fclr012v_extension_probe2.json)
show mark/index/premium klines available through 2026-11-08; the local cache held
only unextracted zips for 2026-11-01..11-07, which run_evaluation.py cannot read
(it looks for <SYM>-1h-<DAY>.csv).  This script closes that engineering gap.

Idempotent: skips already-extracted CSVs.  Coverage-only: computes no outcomes,
no model fitting, no QLIKE.  Unauthenticated public archive only.
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
MONTHLY = "https://data.binance.vision/data/futures/um/monthly/fundingRate"
SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]
KINDS = ["markPriceKlines", "indexPriceKlines", "premiumIndexKlines"]
START = datetime.date(2026, 11, 1)
END = datetime.date(2026, 11, 8)
DAYS = []
d = START
while d <= END:
    DAYS.append(d)
    d += datetime.timedelta(days=1)


def fetch(url: str, dest: Path) -> str:
    """Download a zip into dest (a .zip file), with retries. Idempotent."""
    if dest.exists() and dest.stat().st_size > 0:
        return "skip"
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    last_err = None
    for attempt in range(1, 5):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "kilo-research/1.0"})
            with urllib.request.urlopen(req, timeout=90) as r, tmp.open("wb") as f:
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
            if attempt < 4:
                time.sleep(2 ** attempt)
    return f"fail:{last_err}"


def extract(zip_path: Path, csv_path: Path) -> str:
    if csv_path.exists() and csv_path.stat().st_size > 0:
        return "skip"
    if not zip_path.exists() or zip_path.stat().st_size == 0:
        return "nozip"
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
    n_total = 0
    # 1) ensure every zip exists (fetch from live archive if missing), then extract.
    for sym in SYMBOLS:
        for day in DAYS:
            ds = day.strftime("%Y-%m-%d")
            ym = f"{day.year:04d}-{day.month:02d}"
            for kind in KINDS:
                fname = f"{sym}-1h-{ds}.zip"
                url = f"{BASE}/{kind}/{sym}/1h/{fname}"
                dest = month_dir(sym, ym) / fname
                n_total += 1
                fr = fetch(url, dest)
                key = f"{sym}/{kind}/{ds}"
                if fr not in ("skip", "ok"):
                    results[key] = fr
                    print(f"  WARN fetch {url} -> {fr}", file=sys.stderr)
    # 2) extract every zip into the CSV layout run_evaluation.py reads.
    for sym in SYMBOLS:
        for day in DAYS:
            ds = day.strftime("%Y-%m-%d")
            ym = f"{day.year:04d}-{day.month:02d}"
            for kind in KINDS:
                fname = f"{sym}-1h-{ds}.zip"
                zip_path = month_dir(sym, ym) / fname
                csv_path = month_dir(sym, ym) / f"{kind}-{ds}" / fname.replace(".zip", ".csv")
                r = extract(zip_path, csv_path)
                key = f"{sym}/{kind}/{ds}"
                if r not in ("skip", "ok"):
                    results.setdefault(key, r)
                    print(f"  WARN extract {key} -> {r}", file=sys.stderr)
    print(f"processed {n_total}")
    bad = {k: v for k, v in results.items() if v not in ("ok", "skip")}
    if bad:
        print("FAILURES:", bad)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())