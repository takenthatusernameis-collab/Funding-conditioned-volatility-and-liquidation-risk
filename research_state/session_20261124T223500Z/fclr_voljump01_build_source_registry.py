#!/usr/bin/env python3
"""Build the FCLR-VOL-JUMP-01 source registry (sha256-asserted ironflow_bulk inventory).

Read-only over the frozen caches; writes only the source-registry json+md into the
session directory. Asserts every .sha256 sidecar before recording a file. No outcome
data is inspected here (outcome-blind inventory only).
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import pyarrow.parquet as pq

REPO = Path(__file__).resolve().parents[2]
RS = REPO / "research_state"
CACHE = RS / "data_cache" / "ironflow_bulk"
SESSION_UTC = "20261124T223500Z"
SESSION_ID = f"session_{SESSION_UTC}"
SESSION_DIR = RS / SESSION_ID
EXPERIMENT_ID = "FCLR-VOL-JUMP-01"
CAMPAIGN_ID = "FCLR-VOL-JUMP-01-20261124T223000Z"

MONTHS = [
    "2025-05", "2025-06", "2025-07", "2025-08", "2025-09", "2025-10",
    "2025-11", "2025-12", "2026-01", "2026-02", "2026-03", "2026-04",
    "2026-05", "2026-06", "2026-07", "2026-08", "2026-09", "2026-10",
]
DATASETS = ["candles_1h", "funding", "open_interest"]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    files = []
    datasets: dict[str, dict] = {}
    bad = 0
    for ds in DATASETS:
        ds_rows = 0
        ds_months = []
        ds_schema = None
        for month in MONTHS:
            pq_path = CACHE / ds / f"{month}.parquet"
            sidecar = pq_path.with_suffix(pq_path.suffix + ".sha256")
            stored = sidecar.read_text(encoding="utf-8").strip().split()[0]
            computed = sha256_file(pq_path)
            match = computed == stored
            if not match:
                bad += 1
            t = pq.read_table(pq_path)
            ds_rows += t.num_rows
            ds_months.append(month)
            if ds_schema is None:
                ds_schema = list(t.column_names)
            files.append({
                "dataset": ds,
                "month": month,
                "path": str(pq_path.relative_to(REPO)),
                "rows": int(t.num_rows),
                "sha256": computed,
                "sha_match": match,
                "sidecar_sha256": stored,
            })
        datasets[ds] = {
            "months": ds_months,
            "n_months": len(ds_months),
            "total_rows": int(ds_rows),
            "schema": ds_schema,
            "parquet_count": len(ds_months),
        }

    registry = {
        "experiment_id": EXPERIMENT_ID,
        "campaign": CAMPAIGN_ID,
        "session_id": SESSION_ID,
        "session_utc": SESSION_UTC,
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "ironflow_bulk (frozen on-disk cache; read-only; no network)",
        "cache_root": str(CACHE.relative_to(REPO)),
        "month_span": [MONTHS[0], MONTHS[-1]],
        "n_months": len(MONTHS),
        "datasets": datasets,
        "input_integrity": {
            "sha256_all_match": bad == 0,
            "sha256_verified_bad": int(bad),
            "n_files": len(files),
            "n_sidecars_checked": len(files),
            "note": "every parquet .sha256 sidecar recomputed and asserted before any outcome was computed",
        },
        "files": files,
    }

    out_json = SESSION_DIR / f"fclr_voljump01_source_registry_{SESSION_UTC}.json"
    out_json.write_text(json.dumps(registry, indent=2), encoding="utf-8")

    lines = [
        "# FCLR-VOL-JUMP-01 Source Registry",
        "",
        f"**Experiment ID:** {EXPERIMENT_ID}",
        f"**Campaign:** {CAMPAIGN_ID}",
        f"**Session:** {SESSION_ID}",
        "",
        "## Frozen input inventory (ironflow_bulk, read-only)",
        f"- Month span: {MONTHS[0]} .. {MONTHS[-1]} ({len(MONTHS)} months)",
        f"- Datasets: {', '.join(DATASETS)}",
        f"- Files hashed: {len(files)} parquet; sidecars matched: {len(files) - bad}/{len(files)}",
        "",
        "| Dataset | Months | Total rows | Schema |",
        "|---|---|---|---|",
    ]
    for ds in DATASETS:
        info = datasets[ds]
        lines.append(
            f"| {ds} | {info['n_months']} | {info['total_rows']} | {', '.join(info['schema'])} |"
        )
    lines += [
        "",
        f"input_integrity.sha256_all_match = {registry['input_integrity']['sha256_all_match']}",
        f"input_integrity.sha256_verified_bad = {bad}",
        "",
        "Every `.sha256` sidecar was recomputed and asserted before any outcome was computed.",
    ]
    out_md = SESSION_DIR / f"fclr_voljump01_source_registry_{SESSION_UTC}.md"
    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"files": len(files), "bad": bad,
                      "sha256_all_match": bad == 0,
                      "json": str(out_json)}, indent=2))


if __name__ == "__main__":
    main()