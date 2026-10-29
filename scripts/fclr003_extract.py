#!/usr/bin/env python3
"""Extract downloaded FCLR-003 zips into CSVs.

The existing cache has an inconsistent nesting (some months extracted directly,
some into a subdirectory named after the zip).  scripts/run_evaluation.py finds
markPrice CSVs via rglob, so the exact path does not matter; this script extracts
every zip that is still compressed so the CSVs exist for the evaluation.

Idempotent: skips zips whose CSV is already present.
"""
from __future__ import annotations

import sys
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CACHE = REPO / "research_state" / "data_cache"


def main() -> int:
    # Restrict to the new FCLR-003 month directories only, so the existing
    # 2024-04..2024-09 cache (already extracted, possibly nested) is never
    # touched or duplicated.  run_evaluation.py finds CSVs via rglob regardless
    # of nesting depth.
    new_dirs = [CACHE / f"{s}_2024_1{m}" for s in
                ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]
                for m in ["0", "1", "2"]]
    zips = []
    for d in new_dirs:
        if d.exists():
            zips.extend(sorted(d.rglob("*.zip")))
    extracted = 0
    for zp in zips:
        if "fundingRate" in zp.name:
            continue
        try:
            with zipfile.ZipFile(zp) as z:
                csvs = [n for n in z.namelist() if n.endswith(".csv")]
                if not csvs:
                    continue
                already = any((zp.parent / n).exists() for n in csvs)
                if already:
                    continue
                z.extractall(zp.parent)
                extracted += 1
        except Exception as e:
            print(f"FAILED to extract {zp}: {e}", flush=True)
            return 1
    print(f"Extracted {extracted} zips", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())