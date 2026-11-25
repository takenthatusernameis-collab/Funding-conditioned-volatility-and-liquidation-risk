#!/usr/bin/env python3
"""
FCLR-VOL-JUMP-02 independent stdlib recompute.

Recomputes, using ONLY the Python standard library (hashlib/json/math) and the
stored on-disk config + sufficient statistics, and asserts they match the
canonical artifacts:
  (1) every parquet .sha256 sidecar in the source registry (54 checks);
  (2) the aggregate baseline/candidate Brier from the stored per-block sums of
      squared errors (2 checks);
  (3) the aggregate baseline/candidate log-loss from the stored per-block
      log-loss sums (2 checks);
  (4) the total event count and event rate (2 checks).

No parquet/outcome data is read here; only the frozen source-registry hashes and
the eval sufficient statistics are re-derived. Writes recompute_<UTC>.json.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SESSION = REPO / "research_state" / "session_20261125T034400Z"
UTC = "20261125T034400Z"
UTC_ISO = "2026-11-25T03:44:00Z"
EPS = 1e-12


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> dict:
    checks: list[dict] = []

    source = json.loads((SESSION / f"fclr_voljump02_source_registry_{UTC}.json").read_text())
    evaluation = json.loads((SESSION / f"fclr_voljump02_eval_{UTC}.json").read_text())

    # (1) Recompute every parquet sha256 and compare to the registry entry.
    for entry in source.get("files", []):
        rel = entry["path"]
        p = REPO / rel
        actual = sha256_file(p) if p.is_file() else None
        expected = entry["sha256"]
        checks.append({
            "check": f"sha256:{rel}",
            "expected": expected,
            "actual": actual,
            "match": actual == expected,
        })

    # (2)+(3) Reconstruct aggregate Brier / log-loss from sufficient stats.
    ss = evaluation["sufficient_stats"]
    n = ss["n_forecasts"]
    brier_base = ss["sum_sq_base"] / n
    brier_cand = ss["sum_sq_cand"] / n
    ll_base = ss["sum_ll_base"] / n
    ll_cand = ss["sum_ll_cand"] / n

    checks.append({
        "check": "brier_baseline",
        "expected": evaluation["metrics"]["baseline"]["brier"],
        "actual": brier_base,
        "match": math.isclose(brier_base, evaluation["metrics"]["baseline"]["brier"], rel_tol=1e-9, abs_tol=1e-12),
    })
    checks.append({
        "check": "brier_candidate",
        "expected": evaluation["metrics"]["candidate"]["brier"],
        "actual": brier_cand,
        "match": math.isclose(brier_cand, evaluation["metrics"]["candidate"]["brier"], rel_tol=1e-9, abs_tol=1e-12),
    })
    checks.append({
        "check": "logloss_baseline",
        "expected": evaluation["metrics"]["baseline"]["log_loss"],
        "actual": ll_base,
        "match": math.isclose(ll_base, evaluation["metrics"]["baseline"]["log_loss"], rel_tol=1e-9, abs_tol=1e-12),
    })
    checks.append({
        "check": "logloss_candidate",
        "expected": evaluation["metrics"]["candidate"]["log_loss"],
        "actual": ll_cand,
        "match": math.isclose(ll_cand, evaluation["metrics"]["candidate"]["log_loss"], rel_tol=1e-9, abs_tol=1e-12),
    })

    # (4) Event count + rate.
    checks.append({
        "check": "n_events",
        "expected": evaluation["n_events"],
        "actual": ss["n_events"],
        "match": evaluation["n_events"] == ss["n_events"],
    })
    rate = ss["n_events"] / ss["n_forecasts"]
    checks.append({
        "check": "event_rate",
        "expected": evaluation["event_rate"],
        "actual": rate,
        "match": math.isclose(rate, evaluation["event_rate"], rel_tol=1e-9, abs_tol=1e-12),
    })

    all_match = all(c["match"] for c in checks)
    out = {
        "experiment_id": "FCLR-VOL-JUMP-02",
        "session_id": f"session_{UTC}",
        "session_utc": UTC,
        "generated_utc": UTC_ISO,
        "recompute_kind": "independent_stdlib_hash_and_sufficient_stat_recompute",
        "n_checks": len(checks),
        "n_sha256_checks": sum(1 for c in checks if c["check"].startswith("sha256:")),
        "all_checks_match": all_match,
        "n_mismatches": sum(1 for c in checks if not c["match"]),
        "checks": checks,
    }
    (SESSION / f"fclr_voljump02_recompute_{UTC}.json").write_text(
        json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(f"recompute: n_checks={len(checks)} all_checks_match={all_match} "
          f"mismatches={out['n_mismatches']}")
    return out


if __name__ == "__main__":
    main()