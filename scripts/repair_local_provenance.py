#!/usr/bin/env python3
"""Local-only provenance repair: generate sha256 sidecars + JSON manifests for local Track C data.

Dep-light, stdlib-only, NO NETWORK, NO OUTCOMES/TARGETS/FEATURES/MODELS.
Walks research_state/data_cache and data/raw, emits adjacent <file>.sha256 sidecars
for every data file, and rewrites manifest_extended.json / manifest_extract.json
as real JSON record lists (path + sha256) consumable by trackc_provenance_lineage.py.
Replaces Git LFS pointer stubs with actual content-hash manifests.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CACHE = REPO_ROOT / "research_state" / "data_cache"
RAW = REPO_ROOT / "data" / "raw"

EXTENSIONS = {".csv", ".zip"}
MANIFEST_EXTENDED = CACHE / "manifest_extended.json"
MANIFEST_EXTRACT = CACHE / "manifest_extract.json"


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_sidecar(p: Path) -> str:
    digest = sha256_file(p)
    sc = Path(str(p) + ".sha256")
    sc.write_text(digest + "\n")
    return digest


def collect_files(roots: list[Path]) -> list[Path]:
    found: list[Path] = []
    for root in roots:
        if not root.exists():
            continue
        for p in root.rglob("*"):
            if p.is_file() and p.suffix.lower() in EXTENSIONS:
                sp = str(p)
                if "/.git/" in sp:
                    continue
                found.append(p)
    return sorted(found)


def build_manifest_records(files: list[Path]) -> list[dict]:
    records = []
    for p in files:
        try:
            rp = p.resolve()
        except Exception:
            rp = p
        rel = rp.relative_to(REPO_ROOT.resolve()) if rp.is_relative_to(REPO_ROOT.resolve()) else str(rp)
        digest = sha256_file(rp)
        records.append({"path": str(rel), "sha256": digest, "size": rp.stat().st_size})
    return records


def main() -> int:
    files = collect_files([CACHE, RAW])
    print(f"files_considered={len(files)}")
    # 1) write adjacent sha256 sidecars
    sidecar_count = 0
    for p in files:
        write_sidecar(p)
        sidecar_count += 1
    print(f"sidecars_written={sidecar_count}")
    # 2) rewrite manifests as real JSON record lists
    ext_records = build_manifest_records([p for p in files if p.suffix.lower() == ".zip"])
    exr_records = build_manifest_records([p for p in files if p.suffix.lower() == ".csv"])
    for path, records in ((MANIFEST_EXTENDED, ext_records), (MANIFEST_EXTRACT, exr_records)):
        doc = {
            "version": 1,
            "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "source": "local_only_provenance_repair",
            "network_used": False,
            "records": records,
        }
        path.write_text(json.dumps(doc, indent=2, sort_keys=True) + "\n")
        print(f"manifest_written={path} records={len(records)}")
    print("next_action: run trackc_provenance_lineage.py + trackc_funding_schema_audit.py to confirm machine-verifiable provenance")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
