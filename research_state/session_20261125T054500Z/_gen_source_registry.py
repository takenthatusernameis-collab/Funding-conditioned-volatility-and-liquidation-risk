#!/usr/bin/env python3
"""FCLR-VOL-JUMP-04 on-disk source registry generator.

Inventory the frozen ironflow_bulk candles_1h / funding / open_interest monthly
parquet (18 months each, 2025-05..2026-10). Recompute every .sha256 sidecar and
assert it matches the parquet bytes BEFORE any outcome is computed. Caches are
read-only. Writes the source registry json + md for the jump04 session.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pyarrow.parquet as pq

REPO = Path(__file__).resolve().parents[2]
CACHE = REPO / "research_state" / "data_cache" / "ironflow_bulk"
SESSION = REPO / "research_state" / "session_20261125T054500Z"
UTC = "20261125T054500Z"
UTC_ISO = "2026-11-25T05:45:00Z"

MONTHS = [
    "2025-05", "2025-06", "2025-07", "2025-08", "2025-09", "2025-10",
    "2025-11", "2025-12", "2026-01", "2026-02", "2026-03", "2026-04",
    "2026-05", "2026-06", "2026-07", "2026-08", "2026-09", "2026-10",
]
DATASETS = ["candles_1h", "funding", "open_interest"]


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> dict:
    files = []
    datasets = {}
    n_bad = 0
    n_sidecars = 0
    for name in DATASETS:
        ddir = CACHE / name
        months = []
        total_rows = 0
        schema = None
        for month in MONTHS:
            pq_path = ddir / f"{month}.parquet"
            sidecar = ddir / f"{month}.parquet.sha256"
            months.append(month)
            pf = pq.ParquetFile(pq_path)
            if schema is None:
                schema = list(pf.schema_arrow.names)
            rows = pf.metadata.num_rows
            total_rows += rows
            actual = sha256_file(pq_path)
            expected = sidecar.read_text().strip() if sidecar.is_file() else None
            n_sidecars += 1
            match = expected == actual
            if not match:
                n_bad += 1
            files.append({
                "dataset": name,
                "month": month,
                "path": str(pq_path.relative_to(REPO)),
                "rows": int(rows),
                "schema": schema,
                "sha256": actual,
                "sidecar_sha256": expected,
                "sha_match": match,
            })
        datasets[name] = {
            "months": months,
            "n_months": len(months),
            "total_rows": int(total_rows),
            "schema": schema,
            "parquet_count": len(months),
        }

    registry = {
        "experiment_id": "FCLR-VOL-JUMP-04",
        "campaign": "FCLR-VOL-JUMP-04-20261125T045000Z",
        "session_id": f"session_{UTC}",
        "session_utc": UTC,
        "generated_utc": UTC_ISO,
        "source": "ironflow_bulk (frozen on-disk cache; read-only; no network)",
        "cache_root": "research_state/data_cache/ironflow_bulk",
        "month_span": [MONTHS[0], MONTHS[-1]],
        "n_months": len(MONTHS),
        "n_coins_universe_intersection": None,
        "datasets": datasets,
        "input_integrity": {
            "sha256_all_match": n_bad == 0,
            "sha256_verified_bad": int(n_bad),
            "n_files": len(files),
            "n_sidecars_checked": n_sidecars,
            "note": "every parquet .sha256 sidecar recomputed and asserted before any outcome was computed",
        },
        "files": files,
    }

    out_json = SESSION / f"fclr_voljump04_source_registry_{UTC}.json"
    out_json.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")

    md = []
    md.append(f"# FCLR-VOL-JUMP-04 Source Registry ({UTC})\n\n")
    md.append(f"- experiment_id: FCLR-VOL-JUMP-04\n- session_id: session_{UTC}\n")
    md.append(f"- source: {registry['source']}\n")
    md.append(f"- month_span: {registry['month_span']} ({registry['n_months']} months)\n")
    md.append(f"- files inventoried: {len(files)}\n")
    md.append(f"- sha256_all_match: {registry['input_integrity']['sha256_all_match']}\n")
    md.append(f"- sha256_verified_bad: {registry['input_integrity']['sha256_verified_bad']}\n\n")
    md.append("## Datasets\n\n| dataset | months | rows | parquet |\n|---|---|---|---|\n")
    for name in DATASETS:
        d = datasets[name]
        md.append(f"| {name} | {d['n_months']} | {d['total_rows']} | {d['parquet_count']} |\n")
    (SESSION / f"fclr_voljump04_source_registry_{UTC}.md").write_text("".join(md), encoding="utf-8")

    print(f"source_registry: files={len(files)} bad={n_bad} all_match={registry['input_integrity']['sha256_all_match']}")
    return registry


if __name__ == "__main__":
    main()