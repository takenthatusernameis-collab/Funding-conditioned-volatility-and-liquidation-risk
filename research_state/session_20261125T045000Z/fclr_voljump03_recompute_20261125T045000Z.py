#!/usr/bin/env python3
"""
FCLR-VOL-JUMP-03 independent stdlib recompute.

Recomputes, using ONLY the Python standard library (hashlib/json/math) and the
stored on-disk config + sufficient statistics, and asserts they match the
canonical artifacts:
  (1) every parquet .sha256 sidecar in the source registry (54 checks);
  (2) the aggregate baseline/candidate Brier from the stored per-config sums of
      squared errors (2 checks);
  (3) the aggregate baseline/candidate log-loss from the stored per-config
      log-loss sums (2 checks);
  (4) per-config baseline/candidate Brier + log-loss for all four
      (estimator x horizon) configs (16 checks);
  (5) the total event count and event rate (2 checks).

No parquet/outcome data is read here; only the frozen source-registry hashes and
the eval sufficient statistics are re-derived. Writes recompute_<UTC>.json.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SESSION = REPO / "research_state" / "session_20261125T045000Z"
UTC = "20261125T045000Z"
UTC_ISO = "2026-11-25T04:50:00Z"


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def close(a: float, b: float) -> bool:
    return math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-12)


def main() -> dict:
    checks: list[dict] = []

    source = json.loads((SESSION / f"fclr_voljump03_source_registry_{UTC}.json").read_text())
    evaluation = json.loads((SESSION / f"fclr_voljump03_eval_{UTC}.json").read_text())

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

    # (2)+(3) Aggregate Brier / log-loss from aggregate sufficient stats.
    ss = evaluation["sufficient_stats"]
    n = ss["n_forecasts"]
    agg_brier_base = ss["sum_sq_base"] / n
    agg_brier_cand = ss["sum_sq_cand"] / n
    agg_ll_base = ss["sum_ll_base"] / n
    agg_ll_cand = ss["sum_ll_cand"] / n
    checks.append({"check": "agg_brier_baseline",
                   "expected": evaluation["metrics"]["baseline"]["brier"],
                   "actual": agg_brier_base,
                   "match": close(agg_brier_base, evaluation["metrics"]["baseline"]["brier"])})
    checks.append({"check": "agg_brier_candidate",
                   "expected": evaluation["metrics"]["candidate"]["brier"],
                   "actual": agg_brier_cand,
                   "match": close(agg_brier_cand, evaluation["metrics"]["candidate"]["brier"])})
    checks.append({"check": "agg_logloss_baseline",
                   "expected": evaluation["metrics"]["baseline"]["log_loss"],
                   "actual": agg_ll_base,
                   "match": close(agg_ll_base, evaluation["metrics"]["baseline"]["log_loss"])})
    checks.append({"check": "agg_logloss_candidate",
                   "expected": evaluation["metrics"]["candidate"]["log_loss"],
                   "actual": agg_ll_cand,
                   "match": close(agg_ll_cand, evaluation["metrics"]["candidate"]["log_loss"])})

    # (4) Per-config Brier / log-loss reconstruction.
    for cfg in evaluation["configs"]:
        css = cfg["sufficient_stats"]
        cn = css["n_forecasts"]
        tag = f"{cfg['estimator']}_H{cfg['horizon_h']}"
        cb = css["sum_sq_base"] / cn
        cc = css["sum_sq_cand"] / cn
        clb = css["sum_ll_base"] / cn
        clc = css["sum_ll_cand"] / cn
        checks.append({"check": f"brier_base:{tag}", "expected": cfg["metrics"]["baseline"]["brier"],
                       "actual": cb, "match": close(cb, cfg["metrics"]["baseline"]["brier"])})
        checks.append({"check": f"brier_cand:{tag}", "expected": cfg["metrics"]["candidate"]["brier"],
                       "actual": cc, "match": close(cc, cfg["metrics"]["candidate"]["brier"])})
        checks.append({"check": f"logloss_base:{tag}", "expected": cfg["metrics"]["baseline"]["log_loss"],
                       "actual": clb, "match": close(clb, cfg["metrics"]["baseline"]["log_loss"])})
        checks.append({"check": f"logloss_cand:{tag}", "expected": cfg["metrics"]["candidate"]["log_loss"],
                       "actual": clc, "match": close(clc, cfg["metrics"]["candidate"]["log_loss"])})

    # (5) Event count + rate.
    checks.append({"check": "n_events", "expected": evaluation["n_events"],
                   "actual": ss["n_events"], "match": evaluation["n_events"] == ss["n_events"]})
    rate = ss["n_events"] / ss["n_forecasts"]
    checks.append({"check": "event_rate", "expected": evaluation["event_rate"],
                   "actual": rate, "match": close(rate, evaluation["event_rate"])})

    all_match = all(c["match"] for c in checks)
    out = {
        "experiment_id": "FCLR-VOL-JUMP-03",
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
    (SESSION / f"fclr_voljump03_recompute_{UTC}.json").write_text(
        json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(f"recompute: n_checks={len(checks)} all_checks_match={all_match} "
          f"mismatches={out['n_mismatches']}")
    return out


if __name__ == "__main__":
    main()