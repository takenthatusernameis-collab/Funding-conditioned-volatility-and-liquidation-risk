#!/usr/bin/env python3
"""Download 2026-07-08..2026-08-06 Binance UM perp market data for the 5-symbol universe.

Unauthenticated, from data.binance.vision. Writes raw zips into data_cache/<SYM>_<YYYY>_<MM>/.
Idempotent: skips files already present with non-zero size.
"""
import os
import sys
import time
import datetime
import urllib.request

CACHE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                     "research_state", "data_cache")
SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]
BASE = "https://data.binance.vision/data/futures/um/daily"
DAYS = []
d = datetime.date(2026, 7, 8)
end = datetime.date(2026, 8, 6)
while d <= end:
    DAYS.append(d)
    d += datetime.timedelta(days=1)

def fetch(url, dest):
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        return "skip"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read()
            if len(data) < 50:
                return "empty"
            with open(dest, "wb") as f:
                f.write(data)
            return "ok"
        except Exception as e:
            if attempt == 2:
                return f"fail:{e}"
            time.sleep(2 ** attempt)

def main():
    os.makedirs(CACHE, exist_ok=True)
    results = {}
    for sym in SYMBOLS:
        ym_dir = os.path.join(CACHE, f"{sym}_2026_07")
        os.makedirs(ym_dir, exist_ok=True)
        for day in DAYS:
            ds = day.strftime("%Y-%m-%d")
            for kind in ["markPriceKlines", "indexPriceKlines", "premiumIndexKlines"]:
                fname = f"{sym}-1h-{ds}.zip"
                url = f"{BASE}/{kind}/{sym}/1h/{fname}"
                dest = os.path.join(ym_dir, fname)
                r = fetch(url, dest)
                results[f"{sym}/{kind}/{ds}"] = r
                if r not in ("skip", "ok"):
                    print(f"  WARN {url} -> {r}", file=sys.stderr)
        for mon in ["2026-07", "2026-08"]:
            url = f"https://data.binance.vision/data/futures/um/monthly/fundingRate/{sym}/{sym}-fundingRate-{mon}.zip"
            dest = os.path.join(ym_dir, f"{sym}-fundingRate-{mon}.zip")
            r = fetch(url, dest)
            results[f"{sym}/fundingRate/{mon}"] = r
    ok = sum(1 for v in results.values() if v in ("ok", "skip"))
    print(f"done {ok}/{len(results)}")
    bad = {k: v for k, v in results.items() if v not in ("ok", "skip")}
    if bad:
        print("FAILURES:", bad)

if __name__ == "__main__":
    main()