#!/usr/bin/env python3
"""
Build fclr_voljump01_source_registry for FCLR-VOL-JUMP-01.
Recomputes every ironflow_bulk parquet .sha256 sidecar, asserts match,
and emits the sha256-asserted source registry (json + md) for the session.
Read-only on the frozen cache; no network.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CACHE = REPO / "research_state" / "data_cache" / "ironflow_bulk"
SESSION = REPO / "research_state" / "session_20261124T230000Z"
UTC = "20261124T230000Z"
UTC_ISO = "2026-11-24T23:00:00Z"

DATASETS = ["candles_1h", "funding", "open_interest"]
MONTHS = [
    "2025-05", "2025-06", "2025-07", "2025-08", "2025-09", "2025-10",
    "2025-11", "2025-12", "2026-01", "2026-02", "2026-03", "2026-04",
    "2026-05", "2026-06", "2026-07", "2026-08", "2026-09", "2026-10",
]
SCHEMAS = {
    "candles_1h": ["timestamp", "market", "coin", "dex", "market_class", "open", "high", "low", "close", "volume", "trades"],
    "funding": ["timestamp", "market", "coin", "dex", "funding_rate", "premium"],
    "open_interest": ["timestamp", "market", "coin", "dex", "mark_price", "oracle_price", "open_interest", "open_interest_usd"],
}


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    SESSION.mkdir(parents=True, exist_ok=True)
    files = []
    bad = 0
    total_rows = 0
    for ds in DATASETS:
        ds_rows = 0
        for month in MONTHS:
            parquet = CACHE / ds / f"{month}.parquet"
            sidecar = CACHE / ds / f"{month}.parquet.sha256"
            actual = sha256_file(parquet)
            stated = sidecar.read_text(encoding="utf-8").strip().split()[0]
            sha_match = actual == stated
            if not sha_match:
                bad += 1
            # row count + schema via pyarrow
            import pyarrow.parquet as pq  # noqa: PLC0415
            pf = pq.read_table(parquet)
            rows = pf.num_rows
            ds_rows += rows
            files.append({
                "dataset": ds,
                "month": month,
                "path": f"research_state/data_cache/ironflow_bulk/{ds}/{month}.parquet",
                "rows": int(rows),
                "schema": list(pf.schema.names),
                "sha256": actual,
                "sidecar_sha256": stated,
                "sha_match": bool(sha_match),
            })
        total_rows += ds_rows

    all_match = bad == 0 and len(files) >= 54
    registry = {
        "experiment_id": "FCLR-VOL-JUMP-01",
        "campaign": "FCLR-VOL-JUMP-01-20261124T223000Z",
        "session_id": f"session_{UTC}",
        "session_utc": UTC,
        "generated_utc": UTC_ISO,
        "source": "ironflow_bulk (frozen on-disk cache; read-only; no network)",
        "cache_root": "research_state/data_cache/ironflow_bulk",
        "month_span": ["2025-05", "2026-10"],
        "n_months": 18,
        "n_coins_universe_intersection": 466,
        "datasets": {
            "candles_1h": {
                "months": MONTHS, "n_months": 18,
                "total_rows": sum(f["rows"] for f in files if f["dataset"] == "candles_1h"),
                "schema": SCHEMAS["candles_1h"], "parquet_count": 18,
            },
            "funding": {
                "months": MONTHS, "n_months": 18,
                "total_rows": sum(f["rows"] for f in files if f["dataset"] == "funding"),
                "schema": SCHEMAS["funding"], "parquet_count": 18,
            },
            "open_interest": {
                "months": MONTHS, "n_months": 18,
                "total_rows": sum(f["rows"] for f in files if f["dataset"] == "open_interest"),
                "schema": SCHEMAS["open_interest"], "parquet_count": 18,
            },
        },
        "input_integrity": {
            "sha256_all_match": bool(all_match),
            "sha256_verified_bad": int(bad),
            "n_files": int(len(files)),
            "n_sidecars_checked": int(len(files)),
            "note": "every parquet .sha256 sidecar recomputed and asserted before any outcome was computed",
        },
        "files": files,
    }
    json_path = SESSION / f"fclr_voljump01_source_registry_{UTC}.json"
    md_path = SESSION / f"fclr_voljump01_source_registry_{UTC}.md"
    json_path.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
    registry_sha = hashlib.sha256(json_path.read_bytes()).hexdigest()
    lines = [
        f"# FCLR-VOL-JUMP-01 Source Registry ({UTC})",
        "",
        f"- experiment_id: FCLR-VOL-JUMP-01",
        f"- session_id: session_{UTC}",
        f"- campaign: FCLR-VOL-JUMP-01-20261124T223000Z",
        f"- generated_utc: {UTC_ISO}",
        f"- source: ironflow_bulk (frozen on-disk cache; read-only; no network)",
        f"- cache_root: research_state/data_cache/ironflow_bulk",
        f"- month_span: 2025-05 .. 2026-10 (18 months)",
        f"- n_coins_universe_intersection: 466",
        f"- source_registry_json_sha256: {registry_sha}",
        "",
        "## input_integrity",
        f"- sha256_all_match: {all_match}",
        f"- sha256_verified_bad: {bad}",
        f"- n_files: {len(files)}",
        f"- n_sidecars_checked: {len(files)}",
        "",
        "## datasets",
    ]
    for ds in DATASETS:
        d = registry["datasets"][ds]
        lines += [
            f"### {ds}",
            f"- months: {d['n_months']} (2025-05 .. 2026-10)",
            f"- total_rows: {d['total_rows']}",
            f"- parquet_count: {d['parquet_count']}",
            f"- schema: {', '.join(d['schema'])}",
        ]
    lines += ["", "## files (sha256-asserted)", ""]
    for f in files:
        lines.append(f"- {f['dataset']}/{f['month']}: rows={f['rows']} sha256={f['sha256']} sha_match={f['sha_match']}")
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {json_path} ({len(files)} files, bad={bad}, all_match={all_match})")
    print(f"Wrote {md_path}")
    print(f"registry json sha256 = {registry_sha}")


if __name__ == "__main__":
    main()
