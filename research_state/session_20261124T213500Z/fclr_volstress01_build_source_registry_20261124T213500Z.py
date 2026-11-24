#!/usr/bin/env python3
"""
FCLR-VOL-STRESS-01 source registry builder.
Sha256-asserts every ironflow_bulk parquet (.candles_1h, .funding, .open_interest)
against its .sha256 sidecar before inventorying. Read-only; no network; no cache
mutation. Emits fclr_volstress01_source_registry_<UTC>.json.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CACHE = REPO / "research_state" / "data_cache" / "ironflow_bulk"
DATASETS = ("candles_1h", "funding", "open_interest")
SESSION_UTC = "20261124T213500Z"
SESSION_ID = f"session_{SESSION_UTC}"
EXPERIMENT_ID = "FCLR-VOL-STRESS-01"
CAMPAIGN = "FCLR-VOL-STRESS-01-20261124T213000Z"
OUT = REPO / "research_state" / SESSION_ID / f"fclr_volstress01_source_registry_{SESSION_UTC}.json"
MONTHS = ["2025-05","2025-06","2025-07","2025-08","2025-09","2025-10",
          "2025-11","2025-12","2026-01","2026-02","2026-03","2026-04",
          "2026-05","2026-06","2026-07","2026-08","2026-09","2026-10"]
SCHEMAS = {
    "candles_1h": ["timestamp","market","coin","dex","market_class","open","high","low","close","volume","trades"],
    "funding": ["timestamp","market","coin","dex","funding_rate","premium"],
    "open_interest": ["timestamp","market","coin","dex","mark_price","oracle_price","open_interest","open_interest_usd"],
}


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    files = []
    datasets = {}
    n_files = 0
    n_bad = 0
    all_match = True
    for ds in DATASETS:
        d = CACHE / ds
        months = []
        total_rows = 0
        for m in MONTHS:
            p = d / f"{m}.parquet"
            side = d / f"{m}.parquet.sha256"
            assert p.is_file(), f"missing parquet {p}"
            assert side.is_file(), f"missing sidecar {side}"
            actual = sha256_file(p)
            stated = side.read_text(encoding="utf-8").strip().split()[0]
            sha_match = actual == stated
            if not sha_match:
                n_bad += 1
                all_match = False
            import pyarrow.parquet as pq
            rows = pq.read_table(p).num_rows
            total_rows += rows
            n_files += 1
            files.append({
                "dataset": ds,
                "month": m,
                "path": f"research_state/data_cache/ironflow_bulk/{ds}/{m}.parquet",
                "rows": int(rows),
                "sha256": actual,
                "sha_match": bool(sha_match),
                "sidecar_sha256": stated,
            })
            months.append(m)
        datasets[ds] = {
            "months": months,
            "n_months": len(months),
            "total_rows": int(total_rows),
            "schema": SCHEMAS[ds],
            "parquet_count": len(months),
        }
    registry = {
        "experiment_id": EXPERIMENT_ID,
        "campaign": CAMPAIGN,
        "session_id": SESSION_ID,
        "session_utc": SESSION_UTC,
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "ironflow_bulk (frozen on-disk cache; read-only; no network)",
        "cache_root": "research_state/data_cache/ironflow_bulk",
        "month_span": [MONTHS[0], MONTHS[-1]],
        "n_months": len(MONTHS),
        "datasets": datasets,
        "input_integrity": {
            "sha256_all_match": bool(all_match),
            "sha256_verified_bad": int(n_bad),
            "n_files": int(n_files),
            "n_sidecars_checked": int(n_files),
            "note": "every parquet .sha256 sidecar recomputed and asserted before read",
        },
        "files": files,
    }
    OUT.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT}  files={n_files} bad={n_bad} all_match={all_match}")
    assert all_match and n_bad == 0 and n_files >= 54


if __name__ == "__main__":
    main()
