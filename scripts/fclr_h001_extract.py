#!/usr/bin/env python3
"""FCLR-H001 data extraction: unzip Binance public-archive daily/monthly zips into data/raw.

Restartable, idempotent, checksum-recorded. No network access required (local zips only).
Writes raw CSVs under data/raw/<kind>/<SYMBOL>/<file>.csv and a manifest of what was extracted.
"""
from __future__ import annotations

import csv
import hashlib
import json
import os
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
RAW = REPO / "data" / "raw"
MANIFEST = REPO / "research_state" / "data_cache" / "fclr_h001_extract_manifest.json"

KIND_PREFIXES = {
    "klines": ("-1h-", "markPriceKlines-1h-", "indexPriceKlines-1h-", "premiumIndexKlines-1h-"),
    "funding": ("fundingRate-",),
}


def classify(path: Path):
    name = path.name
    if name.endswith(".zip"):
        stem = name[:-4]
    else:
        stem = name
    for kind, pats in KIND_PREFIXES.items():
        for p in pats:
            if p in stem:
                return kind
    return None


def symbol_of(name: str) -> str:
    for p in ("-1h-", "markPriceKlines-1h-", "indexPriceKlines-1h-", "premiumIndexKlines-1h-", "fundingRate-"):
        if p in name:
            return name.split(p)[0]
    return name


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def extract_one(zip_path: Path, out_dir: Path, force: bool = False) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    info = {"zip": str(zip_path.relative_to(REPO)), "size": zip_path.stat().st_size,
            "zip_sha256": sha256_file(zip_path), "members": [], "extracted": []}
    with zipfile.ZipFile(zip_path) as z:
        for m in z.namelist():
            if not m.endswith(".csv"):
                continue
            target = out_dir / m
            info["members"].append(m)
            if target.exists() and not force:
                info["extracted"].append({"file": str(target.relative_to(REPO)), "sha256": sha256_file(target)})
                continue
            with z.open(m) as src, open(target, "wb") as dst:
                dst.write(src.read())
            info["extracted"].append({"file": str(target.relative_to(REPO)), "sha256": sha256_file(target)})
    return info


def main():
    root = REPO
    zips = sorted(p for p in root.iterdir() if p.suffix == ".zip")
    manifest = {"generated_utc": None, "counts": {}, "files": []}
    counts = {}
    for zp in zips:
        kind = classify(zp)
        if kind is None:
            continue
        sym = symbol_of(zp.name)
        out_dir = RAW / kind / sym
        info = extract_one(zp, out_dir)
        info["kind"] = kind
        info["symbol"] = sym
        manifest["files"].append(info)
        counts[kind] = counts.get(kind, 0) + 1
    manifest["counts"] = counts
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    with open(MANIFEST, "w") as f:
        json.dump(manifest, f, indent=2, sort_keys=True)
    print(json.dumps({"counts": counts, "n_files": len(manifest["files"]), "manifest": str(MANIFEST.relative_to(REPO))}, indent=2))


if __name__ == "__main__":
    main()