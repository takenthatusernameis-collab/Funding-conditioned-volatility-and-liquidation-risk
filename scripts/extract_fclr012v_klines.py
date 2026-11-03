#!/usr/bin/env python3
"""Extract premium/index kline CSVs for the FCLR-012-V forward panel.

scripts/fclr012_download.py downloaded the premiumIndexKlines-<DAY> and
indexPriceKlines-<DAY> zips for 2026-08-07..2026-11-02 but only extracted the
*mark* CSVs.  The C2 model form needs mark/index premium, so the premium and
index CSVs must be on disk in the layout scripts/run_evaluation.py expects:

    <SYM>_<YYYY>_<MM>/<KIND>-<DAY>/<SYM>-1h-<DAY>.csv

This script is idempotent (skips already-extracted, non-empty CSVs) and never
touches the OHLCV klines zips at the month-dir root.

Coverage-only: no outcomes are computed here.
"""
import sys
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CACHE = REPO / "research_state" / "data_cache"
SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]
KINDS = ["premiumIndexKlines", "indexPriceKlines"]


def extract_one(zip_path: Path) -> str:
    csv_path = zip_path.with_suffix(".csv")
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


def main() -> int:
    results = {}
    n_ok = n_skip = 0
    for sym in SYMBOLS:
        for month_dir in sorted(CACHE.glob(f"{sym}_2026_*")):
            for kind in KINDS:
                for zp in sorted(month_dir.glob(f"{kind}-*/*.zip")):
                    r = extract_one(zp)
                    key = f"{sym}/{zp.parent.name}/{zp.name}"
                    results[key] = r
                    if r in ("ok", "skip"):
                        n_ok += 1
                    else:
                        print(f"WARN {key} -> {r}", file=sys.stderr)
    bad = {k: v for k, v in results.items() if v not in ("ok", "skip")}
    print(f"processed {len(results)} zips; ok/skip={n_ok}; failures={len(bad)}")
    if bad:
        for k, v in list(bad.items())[:20]:
            print(f"  {k}: {v}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())