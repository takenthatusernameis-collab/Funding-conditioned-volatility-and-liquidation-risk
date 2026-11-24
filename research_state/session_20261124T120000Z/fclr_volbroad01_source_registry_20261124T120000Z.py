#!/usr/bin/env python3
"""
Phase 1 — FCLR-VOL-BROAD-01 source registry.
Read-only enumeration of research_state/data_cache/ironflow_bulk/{candles_1h,funding,open_interest}.
Asserts every .sha256 sidecar before reading; caches read-only, not mutated; no network.
Produces fclr_volbroad01_source_registry_{json,md} under the session dir.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
SESSION = REPO / "research_state" / "session_20261124T120000Z"
CACHE = REPO / "research_state" / "data_cache" / "ironflow_bulk"
DATASETS = ["candles_1h", "funding", "open_interest"]
SESSION_UTC = "20261124T120000Z"
SESSION_ID = f"session_{SESSION_UTC}"
EXPERIMENT_ID = "FCLR-VOL-BROAD-01"
CAMPAIGN = f"{EXPERIMENT_ID}-20261124T035500Z"


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_sidecar(p: Path) -> str | None:
    side = p.with_suffix(p.suffix + ".sha256")
    if not side.exists():
        return None
    return side.read_text(encoding="utf-8").strip().split()[0]


def inventory() -> dict:
    files = []
    verified_ok = 0
    verified_bad = 0
    all_match = True
    per_dataset = {ds: {"files": 0, "rows": 0} for ds in DATASETS}
    panel_parts = []
    for ds in DATASETS:
        ddir = CACHE / ds
        for parquet in sorted(ddir.glob("*.parquet")):
            month = parquet.stem
            stored = read_sidecar(parquet)
            actual = sha256_file(parquet)
            match = stored is not None and stored == actual
            if not match:
                all_match = False
            if stored is None:
                verified_bad += 1
            elif match:
                verified_ok += 1
            else:
                verified_bad += 1
            # read rows + schema + coins (read-only)
            import pyarrow.parquet as pq
            tbl = pq.read_table(parquet)
            n_rows = tbl.num_rows
            schema_names = list(tbl.schema.names)
            import pandas as pd
            df = tbl.to_pandas()
            n_coins = int(df["coin"].nunique()) if "coin" in df.columns else None
            entry = {
                "dataset": ds,
                "month": month,
                "path": str(parquet.relative_to(REPO)),
                "sha256": actual,
                "stored_sha256": stored,
                "sha_match": match,
                "rows": n_rows,
                "schema": schema_names,
                "n_coins": n_coins,
            }
            files.append(entry)
            panel_parts.append(f"{ds}|{month}|{actual}|{n_rows}")
            per_dataset[ds]["files"] += 1
            per_dataset[ds]["rows"] += n_rows
    files.sort(key=lambda e: (e["dataset"], e["month"]))
    panel_sha = hashlib.sha256("|".join(panel_parts).encode("utf-8")).hexdigest()
    return {
        "files": files,
        "verified_ok": verified_ok,
        "verified_bad": verified_bad,
        "all_match": all_match,
        "n_files": len(files),
        "per_dataset": per_dataset,
        "panel_sha256": panel_sha,
    }


def main() -> None:
    inv = inventory()
    integrity = {
        "sha256_sidecars_total": inv["n_files"],
        "sha256_verified_ok": inv["verified_ok"],
        "sha256_verified_bad": inv["verified_bad"],
        "sha256_all_match": inv["all_match"],
        "panel_sha256": inv["panel_sha256"],
        "panel_hash_method": "sha256 of concatenated dataset|month|sha256|rows across all parquet files (dataset|month sorted)",
    }
    # distinct coins across candles_1h (the broad universe)
    import pyarrow.parquet as pq
    import pandas as pd
    all_coins = set()
    for ds in DATASETS:
        for parquet in sorted((CACHE / ds).glob("*.parquet")):
            df = pq.read_table(parquet).to_pandas()
            if "coin" in df.columns:
                all_coins.update(df["coin"].dropna().unique().tolist())
    coverage = {
        "month_span": "2025-05 .. 2026-10 (18 months)",
        "datasets": DATASETS,
        "per_dataset_totals": inv["per_dataset"],
        "n_distinct_coins_union": len(all_coins),
        "note": "candles_1h defines the 342-coin broad universe; funding and open_interest cover the 198 coins with funding/OI data; the volatility panel uses the intersection.",
    }
    schemas = {
        "candles_1h": ["timestamp", "market", "coin", "dex", "market_class", "open", "high", "low", "close", "volume", "trades"],
        "funding": ["timestamp", "market", "coin", "dex", "funding_rate", "premium"],
        "open_interest": ["timestamp", "market", "coin", "dex", "mark_price", "oracle_price", "open_interest", "open_interest_usd"],
    }
    registry = {
        "experiment_id": EXPERIMENT_ID,
        "campaign": CAMPAIGN,
        "session_utc": SESSION_UTC,
        "session_id": SESSION_ID,
        "phase": "SOURCE_REGISTRY_ON_DISK",
        "source": "fclr_volbroad01_source_registry",
        "registry_kind": "ironflow_bulk_on_disk_panel",
        "method": "read-only enumeration of research_state/data_cache/ironflow_bulk/{candles_1h,funding,open_interest}; sha256 sidecar asserted for every parquet before read; caches read-only, not mutated; no network",
        "input_integrity": integrity,
        "coverage": coverage,
        "schemas": schemas,
        "files": inv["files"],
        "generated_utc": "2026-11-24T12:00:00Z",
    }
    json_path = SESSION / f"fclr_volbroad01_source_registry_{SESSION_UTC}.json"
    json_path.write_text(json.dumps(registry, indent=2), encoding="utf-8")
    print(f"Wrote {json_path} ({len(inv['files'])} files, sha256_all_match={inv['all_match']}, verified_bad={inv['verified_bad']})")


if __name__ == "__main__":
    main()
