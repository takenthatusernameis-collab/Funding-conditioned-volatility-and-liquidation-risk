#!/usr/bin/env python3
"""Extract cached Binance archive zips into CSVs (idempotent).

Scans research_state/data_cache for <SYMBOL>_<YYYY_MM>/*/*.zip files and
extracts each into its own directory next to the zip. Records extraction
status in research_state/data_cache/manifest_extract.json.

No network access, no credentials, no trading.
"""
from __future__ import annotations

import hashlib
import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CACHE = REPO / "research_state" / "data_cache"
MANIFEST_OUT = CACHE / "manifest_extract.json"


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    zips = sorted(CACHE.rglob("*.zip"))
    records = []
    for zp in zips:
        dest = zp.parent / zp.stem
        dest.mkdir(parents=True, exist_ok=True)
        try:
            with zipfile.ZipFile(zp) as z:
                names = z.namelist()
                z.extractall(dest)
            csvs = [p for p in dest.iterdir() if p.suffix == ".csv"]
            records.append({
                "zip": str(zp.relative_to(REPO)),
                "dest": str(dest.relative_to(REPO)),
                "zip_sha256": sha256_file(zp),
                "zip_size_bytes": zp.stat().st_size,
                "members": names,
                "csv_count": len(csvs),
                "status": "extracted",
            })
        except Exception as e:  # noqa: BLE001
            records.append({
                "zip": str(zp.relative_to(REPO)),
                "dest": str(dest.relative_to(REPO)),
                "zip_sha256": sha256_file(zp),
                "zip_size_bytes": zp.stat().st_size,
                "members": [],
                "csv_count": 0,
                "status": f"failed: {e}",
            })
    MANIFEST_OUT.write_text(json.dumps({
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "zip_count": len(zips),
        "records": records,
    }, indent=2))
    ok = sum(1 for r in records if r["status"] == "extracted")
    print(f"Extracted {ok}/{len(zips)} zips -> {MANIFEST_OUT}")
    bad = [r for r in records if r["status"] != "extracted"]
    for b in bad:
        print("FAILED", b["zip"], b["status"])
    return 0 if not bad else 1


if __name__ == "__main__":
    raise SystemExit(main())