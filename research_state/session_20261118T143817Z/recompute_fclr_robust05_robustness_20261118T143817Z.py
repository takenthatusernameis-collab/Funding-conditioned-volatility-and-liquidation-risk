#!/usr/bin/env python3
"""Independent recompute of the ROBUST-05 aggregates from the stored raw arrays.

This script does NOT re-estimate the models. It re-derives every reported
aggregate (per-model mean QLIKE/MAE/RMSE, per-split and pooled deltas, the
UTC-day block bootstrap CI95 for each candidate model, and the pre-registered
materiality verdict) directly from the stored per-origin loss arrays, using an
independent implementation of the frozen bootstrap specification.

stdlib only (json/math/random). Read-only w.r.t. the robustness artifact.
"""
from __future__ import annotations

import json
import math
import random
from pathlib import Path

SESSION = Path(__file__).resolve().parent
ROBUST = SESSION / "fclr_robust05_robustness_20261118T143817Z.json"
OUT = SESSION / "recompute_fclr_robust05_robustness_20261118T143817Z.json"

MODELS = ["A_rv_only", "B_rv_signed", "C_rv_abs", "D_rv_signed_abs", "E_rv_funding_trails"]
SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "BNBUSDT"]
BOOT_REPS = 2000
SEED = 12345
MEAN_TOL = 1e-12
CI_TOL = 1e-9


def _mean(xs):
    return sum(xs) / len(xs) if xs else None


def _split_means(split):
    out = {}
    a = split["models"]["A_rv_only"]["per_instrument"]
    for m in MODELS:
        q, mae, rmse = [], [], []
        for s in SYMBOLS:
            pi = split["models"][m]["per_instrument"].get(s, {})
            q.extend(pi.get("qlike", []))
            mae.extend(pi.get("mae", []))
            rmse.extend(pi.get("rmse_sq", []))
        out[m] = {
            "n": len(q),
            "mean_qlike": _mean(q),
            "mean_mae": _mean(mae),
            "mean_rmse": (math.sqrt(_mean(rmse)) if rmse else None),
            "mean_delta_qlike_vs_A": 0.0,
        }
        if m != "A_rv_only":
            aq = []
            for s in SYMBOLS:
                aq.extend(a.get(s, {}).get("qlike", []))
            out[m]["mean_delta_qlike_vs_A"] = _mean(aq) - _mean(q) if len(aq) == len(q) else None
    return out


def _bootstrap_split(split, seed=SEED, reps=BOOT_REPS):
    """Independent implementation of the frozen UTC-day block bootstrap."""
    rng = random.Random(seed)
    boot = {}
    for m in MODELS:
        if m == "A_rv_only":
            continue
        by_day_model, by_day_a = {}, {}
        for s in SYMBOLS:
            pm = split["models"][m]["per_instrument"].get(s, {})
            pa = split["models"]["A_rv_only"]["per_instrument"].get(s, {})
            for q, d in zip(pm.get("qlike", []), pm.get("days", [])):
                by_day_model.setdefault(d, []).append(q)
            for q, d in zip(pa.get("qlike", []), pa.get("days", [])):
                by_day_a.setdefault(d, []).append(q)
        common = sorted(set(by_day_model) & set(by_day_a))
        data = []
        for d in common:
            mm, aa = by_day_model[d], by_day_a[d]
            for k in range(min(len(mm), len(aa))):
                data.append((d, aa[k] - mm[k]))
        days = sorted({d for d, _ in data})
        means = []
        if data and days:
            for _ in range(reps):
                sampled = [rng.choice(days) for _ in days]
                vals = [dv for (d, dv) in data if d in sampled]
                if vals:
                    means.append(sum(vals) / len(vals))
        if means:
            means.sort()
            boot[m] = {
                "mean_improvement": sum(means) / len(means),
                "ci_2_5": means[int(0.025 * len(means))],
                "ci_97_5": means[int(0.975 * len(means))],
                "n_reps": len(means),
            }
        else:
            boot[m] = {"mean_improvement": None, "ci_2_5": None, "ci_97_5": None, "n_reps": 0}
    return boot


def main():
    doc = json.loads(ROBUST.read_text())
    per_split = {}
    boot = {}
    mismatches = []
    for split in doc["splits"]:
        name = split["name"]
        sm = _split_means(split)
        per_split[name] = sm
        boot[name] = _bootstrap_split(split)
        for m in MODELS:
            rep = split["summary"][m]
            for key in ("n", "mean_qlike", "mean_mae", "mean_rmse", "mean_delta_qlike_vs_A"):
                got, want = sm[m][key], rep.get(key)
                if got is None or want is None:
                    continue
                if abs(got - want) > MEAN_TOL:
                    mismatches.append({"split": name, "model": m, "field": key,
                                       "reported": want, "recomputed": got})
            if m == "A_rv_only":
                continue
            rep_b = split["bootstrap"][m]
            got_b, want_b = boot[name][m], rep_b
            for key in ("mean_improvement", "ci_2_5", "ci_97_5"):
                if abs(got_b[key] - want_b[key]) > CI_TOL:
                    mismatches.append({"split": name, "model": m, "field": "bootstrap." + key,
                                       "reported": want_b[key], "recomputed": got_b[key]})

    # Pooled recompute: weight split means by n (equal n across splits here).
    pooled = {}
    w_all = [per_split[n]["A_rv_only"]["n"] for n in per_split]
    a_pool = (
        sum(per_split[n]["A_rv_only"]["mean_qlike"] * wi for n, wi in zip(per_split, w_all))
        / sum(w_all)
    )
    for m in MODELS:
        vals = [per_split[n][m]["mean_qlike"] for n in per_split]
        w = [per_split[n][m]["n"] for n in per_split]
        pooled[m] = {
            "n": sum(w),
            "mean_qlike": sum(v * wi for v, wi in zip(vals, w)) / sum(w),
            "mean_delta_qlike_vs_A": (
                0.0 if m == "A_rv_only" else a_pool - sum(v * wi for v, wi in zip(vals, w)) / sum(w)
            ),
        }
    for m in MODELS:
        want = doc["pooled_summary"][m]
        gotq = pooled[m]["mean_qlike"]
        if abs(gotq - want["mean_qlike"]) > 1e-9:
            mismatches.append({"split": "pooled", "model": m, "field": "mean_qlike",
                               "reported": want["mean_qlike"], "recomputed": gotq})
        if m != "A_rv_only" and abs(pooled[m]["mean_delta_qlike_vs_A"] - want["mean_delta_qlike_vs_A"]) > 1e-9:
            mismatches.append({"split": "pooled", "model": m, "field": "mean_delta_qlike_vs_A",
                               "reported": want["mean_delta_qlike_vs_A"],
                               "recomputed": pooled[m]["mean_delta_qlike_vs_A"]})

    # Pre-registered materiality verdict re-derived from recomputed values.
    e_per_split = {n: per_split[n]["E_rv_funding_trails"]["mean_delta_qlike_vs_A"] for n in per_split}
    beats = {n: bool(e_per_split[n] > 0 and boot[n]["E_rv_funding_trails"]["ci_2_5"] > 0)
             for n in per_split}
    real_abs = abs(pooled["E_rv_funding_trails"]["mean_delta_qlike_vs_A"])
    placebo_abs = abs(doc["materiality"]["placebo_abs_delta"])
    verdict = {
        "per_split_delta_E": e_per_split,
        "per_split_beats_A": beats,
        "n_holdouts_E_beats_A": sum(beats.values()),
        "real_abs_delta": real_abs,
        "placebo_abs_delta": placebo_abs,
        "real_exceeds_placebo_abs": real_abs > placebo_abs,
        "materiality_floor_met": (sum(beats.values()) >= 3) and (real_abs > placebo_abs),
        "better_model_by_pooled_mean_qlike": min(pooled, key=lambda m: pooled[m]["mean_qlike"]),
    }
    reported_verdict = doc["materiality"]
    verdict_match = (
        verdict["materiality_floor_met"] == reported_verdict["materiality_floor_met"]
        and verdict["n_holdouts_E_beats_A"] == reported_verdict["n_holdouts_E_beats_A"]
        and verdict["better_model_by_pooled_mean_qlike"] == reported_verdict["better_model_by_pooled_mean_qlike"]
    )

    out = {
        "schema": "recompute_fclr_robust05_robustness",
        "session_utc": "2026-11-18T14:38:17Z",
        "generated_utc": "20261118T143817Z",
        "campaign": doc["campaign"],
        "network_used": False,
        "parquet_used": False,
        "numpy_used": False,
        "method": "re-derivation of all reported aggregates and the frozen UTC-day "
                  "block bootstrap (seed 12345, 2000 reps) from the stored per-origin "
                  "loss arrays; no model re-estimation, no outcome re-inspection",
        "source_artifact": ROBUST.name,
        "models": MODELS,
        "per_split_recomputed": per_split,
        "bootstrap_recomputed": boot,
        "pooled_recomputed": pooled,
        "materiality_recomputed": verdict,
        "materiality_matches_reported": verdict_match,
        "max_discrepancies": mismatches,
        "n_discrepancies": len(mismatches),
        "recompute_agrees": (len(mismatches) == 0 and verdict_match),
        "honest_status": "EXPLORATORY/PILOT. Independent aggregate + bootstrap recompute of "
                         "the ROBUST-05 artifact. A negative result is a valid completion.",
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(f"wrote {OUT.name}: discrepancies={len(mismatches)} verdict_match={verdict_match}")
    print(f"materiality_floor_met={verdict['materiality_floor_met']} "
          f"better={verdict['better_model_by_pooled_mean_qlike']}")


if __name__ == "__main__":
    main()
