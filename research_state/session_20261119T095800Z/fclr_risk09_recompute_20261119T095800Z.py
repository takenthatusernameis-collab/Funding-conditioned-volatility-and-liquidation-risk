#!/usr/bin/env python3
"""FCLR-RISK-09 independent stdlib recompute (standalone, runnable).

Re-verifies the frozen Track A panel against the certified preflight statistics
(rows, coins, months, non-null coverage) and the common-sample drop count.
Writes fclr_risk09_recompute_20261119T095800Z.json with n_discrepancies.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location(
    "fclr_risk09_eval_core", HERE / "fclr_risk09_evaluation_20261119T095800Z.py"
)
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)

SESSION = MOD.SESSION
CAMPAIGN = MOD.CAMPAIGN
OUT = MOD.OUT


def main():
    rows = MOD.load_panel()
    rows = MOD.build_features(rows)
    kept, dropped = MOD.apply_common_sample(rows)

    months_present = sorted({r["month"] for r in rows})
    coins_present = sorted({r["coin"] for r in rows})
    funding_nn = sum(1 for r in rows if r["funding_rate"] is not None)
    liq_nn = sum(1 for r in rows if r["liq_count"] is not None)
    oi_nn = sum(1 for r in rows if r["open_interest_usd"] is not None)

    expected = {
        "rows": 113880,
        "coins": 13,
        "months": 12,
        "first_month": "2025-11",
        "last_month": "2026-10",
        "funding_rate_nonnull": 113880,
        "liq_count_nonnull": 113880,
        "open_interest_usd_nonnull": 113035,
    }
    checks = [
        ("rows", len(rows) == expected["rows"]),
        ("coins", len(coins_present) == expected["coins"]),
        ("months", len(months_present) == expected["months"]),
        ("funding_rate_nonnull", funding_nn == expected["funding_rate_nonnull"]),
        ("liq_count_nonnull", liq_nn == expected["liq_count_nonnull"]),
        ("open_interest_usd_nonnull", oi_nn == expected["open_interest_usd_nonnull"]),
    ]
    discrepancies = sum(0 if ok else 1 for _, ok in checks)
    detail = {
        "panel_path": str(MOD.PANEL.relative_to(MOD.REPO)),
        "panel_sha256": __import__("hashlib").sha256(MOD.PANEL.read_bytes()).hexdigest(),
        "rows": len(rows),
        "coins": len(coins_present),
        "months": len(months_present),
        "first_month": months_present[0] if months_present else None,
        "last_month": months_present[-1] if months_present else None,
        "funding_rate_nonnull": funding_nn,
        "liq_count_nonnull": liq_nn,
        "open_interest_usd_nonnull": oi_nn,
        "common_sample_dropped": dropped,
        "common_sample_kept": len(kept),
        "expected": expected,
        "checks": {k: bool(v) for k, v in checks},
        "discrepancies": discrepancies,
        "n_discrepancies": discrepancies,
    }
    payload = {
        "campaign_id": CAMPAIGN,
        "session_utc": SESSION,
        "n_discrepancies": discrepancies,
        "detail": detail,
    }
    (OUT / f"fclr_risk09_recompute_{SESSION}.json").write_text(json.dumps(payload, indent=2) + "\n")
    print(f"recompute n_discrepancies={discrepancies}")


if __name__ == "__main__":
    main()
