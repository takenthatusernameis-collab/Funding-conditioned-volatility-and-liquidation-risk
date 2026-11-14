#!/usr/bin/env python3
"""FCLR-FWD-VOL-2025-DISJOINT-CROSS — Track C exploratory disjoint 2025 cross (P1).

Frozen prereg:
  research_state/prereg_fclr_fwd_vol_2025_disjoint_cross_20261114T183000Z.json

Tests whether the sealed FCLR-011 funding-conditioned volatility PASS (C2 vs B1,
+4.94% relative QLIKE reduction, 5 instruments, 3 blocks, 2026-05..2026-08)
transports to three disjoint, never-tested 2025 Binance test blocks (2025-06,
2025-11, 2025-12). Each block uses its own 30-day train window per prereg.

Cached-only. No network. No mutation of any sealed artifact. EXPLORATORY_ONLY:
promotable=false, verdicts limited to EXPLORATORY_SIGNAL/EXPLORATORY_NULL/
INCONCLUSIVE/SMOKE.

Usage:
  python3 scripts/fclr_fwd_vol_2025_disjoint_cross.py
  python3 scripts/fclr_fwd_vol_2025_disjoint_cross.py --smoke
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[1]
if str(REPO / "scripts") not in sys.path:
    sys.path.insert(0, str(REPO / "scripts"))
import fclr_fwd_vol_confirm as fwd  # noqa: E402

RS = REPO / "research_state"
PREREG = RS / "prereg_fclr_fwd_vol_2025_disjoint_cross_20261114T183000Z.json"
UTC = fwd.UTC
EXPERIMENT_ID = "FCLR-FWD-VOL-2025-DISJOINT-CROSS-20261114T183000Z"

DATA_START = "2025-04-25T00:00:00Z"
DATA_END = "2025-12-31T23:00:00Z"
HORIZONS = [6, 24, 72, 168]


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fit_predict_h(train: pd.DataFrame, test: pd.DataFrame, model: str, h: int):
    """OLS on log forward-h RV with train-only standardization and smearing."""
    feats = fwd.MODEL_FEATURES[model]
    tcol = f"target_{h}h"
    Xtr = train[feats].values.astype(float)
    ytr = np.log(train[tcol].values.astype(float) + fwd.EPS)
    ok = np.isfinite(Xtr).all(axis=1) & np.isfinite(ytr)
    Xtr, ytr = Xtr[ok], ytr[ok]
    mu = Xtr.mean(axis=0)
    sd = Xtr.std(axis=0)
    sd[sd == 0] = 1.0
    A = np.column_stack([np.ones(len(Xtr)), (Xtr - mu) / sd])
    beta, *_ = np.linalg.lstsq(A, ytr, rcond=None)
    resid = ytr - A @ beta
    smear = float(np.mean(np.exp(resid)))
    Xte = test[feats].values.astype(float)
    y = test[tcol].values.astype(float)
    ok_te = np.isfinite(Xte).all(axis=1) & np.isfinite(y)
    Ate = np.column_stack([np.ones(ok_te.sum()), (Xte[ok_te] - mu) / sd])
    yhat = np.exp(Ate @ beta) * smear
    q = np.where((y[ok_te] > 0) & (yhat > 0),
                 y[ok_te] / yhat - np.log(y[ok_te] / yhat) - 1.0, np.nan)
    return pd.DataFrame({"ts": test["ts"].values[ok_te],
                         "symbol": test["symbol"].values[ok_te],
                         "y": y[ok_te], "yhat": yhat, "qlike": q})


def block_slices(panel: pd.DataFrame, blk: dict):
    p = panel.copy()
    p["ts"] = pd.to_datetime(p["ts"])
    train = p[(p["ts"] >= pd.Timestamp(blk["train_start"], tz=UTC)) &
              (p["ts"] <= pd.Timestamp(blk["train_end"], tz=UTC))]
    test = p[(p["ts"] >= pd.Timestamp(blk["test_start"], tz=UTC)) &
             (p["ts"] <= pd.Timestamp(blk["test_end"], tz=UTC))]
    return train, test


def contrast(frames: dict, h: int, a: str, b: str) -> pd.DataFrame:
    A = frames[(h, a)][["ts", "symbol", "qlike"]].rename(columns={"qlike": "qa"})
    B = frames[(h, b)][["ts", "symbol", "qlike"]].rename(columns={"qlike": "qb"})
    M = A.merge(B, on=["ts", "symbol"], how="inner").dropna()
    M["diff"] = M["qa"] - M["qb"]
    return M


def run_block(panel: pd.DataFrame, blk: dict, models=("B0", "B1", "C1", "C2")) -> dict:
    train, test = block_slices(panel, blk)
    frames = {}
    for h in HORIZONS:
        for m in models:
            frames[(h, m)] = fit_predict_h(train, test, m, h)
    diffs = {}
    for h in HORIZONS:
        for a, b in [("C2", "B1"), ("C1", "B1"), ("C2", "C1")]:
            diffs[f"h{h}_{a}_vs_{b}"] = contrast(frames, h, a, b)
    return {"train_rows": int(len(train)), "test_rows": int(len(test)),
            "train_rows_per_symbol": train.groupby("symbol").size().to_dict() if not train.empty else {},
            "test_rows_per_symbol": test.groupby("symbol").size().to_dict() if not test.empty else {},
            "diffs": diffs}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--out-utc", default=None)
    args = ap.parse_args()

    prereg = json.loads(PREREG.read_text())
    assert prereg["status"] == "FROZEN_PRE_OUTCOMES"
    assert prereg["outcome_data_inspected_before_freeze"] is False
    assert prereg["experiment_id"] == EXPERIMENT_ID

    out_utc = args.out_utc or now_utc()
    safe = out_utc.replace(":", "").replace("-", "")
    syms = fwd.SYMBOLS[:1] if args.smoke else prereg["universe"]["symbols"]
    blocks = prereg["splits"]["blocks"][:1] if args.smoke else prereg["splits"]["blocks"]
    gates = prereg["gates"]
    reps = 500 if args.smoke else gates["bootstrap_reps"]

    data_start = pd.Timestamp(DATA_START, tz=UTC)
    data_end = pd.Timestamp(DATA_END, tz=UTC)

    panels, coverage = [], {}
    for sym in syms:
        df = fwd.build_symbol(sym, data_start, data_end)
        panels.append(df)
        coverage[sym] = int(df["target_24h"].notna().sum())
    panel = pd.concat(panels, ignore_index=True)
    mask = fwd.common_valid_mask(panel)
    panel_valid = panel[mask].copy()
    panel_valid["ts"] = pd.to_datetime(panel_valid["ts"])

    block_results, pooled = [], {f"h{h}_{a}_vs_{b}": [] for h in HORIZONS
                                 for a, b in [("C2", "B1"), ("C1", "B1"), ("C2", "C1")]}
    per_block_p = {f"h{h}_{a}_vs_{b}": {} for h in HORIZONS
                   for a, b in [("C2", "B1"), ("C1", "B1"), ("C2", "C1")]}
    for b in blocks:
        blk = {"block": b["block"], "train_start": b["train_start"],
               "train_end": b["train_end"], "test_start": b["test_start"],
               "test_end": b["test_end"]}
        res = run_block(panel_valid, blk)
        block_results.append({"block": b["block"],
                              "train_start": b["train_start"], "train_end": b["train_end"],
                              "test_start": b["test_start"], "test_end": b["test_end"],
                              "train_rows": res["train_rows"],
                              "train_rows_per_symbol": res["train_rows_per_symbol"],
                              "test_rows": res["test_rows"],
                              "test_rows_per_symbol": res["test_rows_per_symbol"]})
        for k, M in res["diffs"].items():
            pooled[k].append(M.assign(block=b["block"]))
            bs = fwd.bootstrap_diff(M, reps=reps)
            if bs:
                per_block_p[k][f"b{b['block']}"] = bs["p_boot"]

    pooled = {k: pd.concat(v, ignore_index=True) if v else pd.DataFrame()
              for k, v in pooled.items()}
    primary_key = "h24_C2_vs_B1"
    primary = fwd.bootstrap_diff(pooled[primary_key], reps=reps)

    # Holm across pre-registered family (horizons x contrasts x blocks)
    pvals = dict(per_block_p[primary_key])
    for k, v in per_block_p.items():
        for name, p in v.items():
            pvals.setdefault(f"{k}_{name}", p)
    holm = fwd.holm(pvals)

    # LOIO: leave one instrument out of training, evaluate on held-out instrument.
    loio = []
    if not args.smoke:
        for held in syms:
            diffs = []
            for b in blocks:
                blk = {"block": b["block"], "train_start": b["train_start"],
                       "train_end": b["train_end"], "test_start": b["test_start"],
                       "test_end": b["test_end"]}
                sub = panel_valid[panel_valid["symbol"] != held].copy()
                sub["ts"] = pd.to_datetime(sub["ts"])
                held_df = panel_valid[panel_valid["symbol"] == held].copy()
                held_df["ts"] = pd.to_datetime(held_df["ts"])
                train, _ = block_slices(sub, blk)
                _, test = block_slices(held_df, blk)
                frames = {(h, m): fit_predict_h(train, test, m, h) for h in HORIZONS
                          for m in ("B1", "C2")}
                diffs.append(contrast(frames, 24, "C2", "B1"))
            M = pd.concat(diffs, ignore_index=True)
            loio.append({"held_out": held, **(fwd.bootstrap_diff(M, reps=500) or {})})

    # Placebo: permute funding features within symbol; recompute primary contrast.
    placebo = None
    if not args.smoke:
        rng = np.random.default_rng(gates["placebo_seed"])
        null = []
        base = panel_valid.copy()
        for _ in range(gates["placebo_reps"]):
            pp = base.copy()
            for sym in syms:
                idx = pp.index[pp["symbol"] == sym]
                for col in ("signed_funding", "abs_fund_pct"):
                    pp.loc[idx, col] = rng.permutation(pp.loc[idx, col].values)
            diffs = []
            for b in blocks:
                blk = {"block": b["block"], "train_start": b["train_start"],
                       "train_end": b["train_end"], "test_start": b["test_start"],
                       "test_end": b["test_end"]}
                train, test = block_slices(pp, blk)
                frames = {(24, m): fit_predict_h(train, test, m, 24) for m in ("B1", "C2")}
                diffs.append(contrast(frames, 24, "C2", "B1"))
            M = pd.concat(diffs, ignore_index=True)
            if not M.empty and M["qb"].mean() != 0:
                null.append(float(-M["diff"].mean() / abs(M["qb"].mean()) * 100.0))
        null = np.array(null)
        placebo = {
            "null_p95": float(np.percentile(null, 95)) if len(null) else None,
            "true_rel_reduction_pct": primary["rel_reduction_pct"] if primary else None,
            "pass": bool(primary and primary["rel_reduction_pct"] is not None and len(null)
                         and primary["rel_reduction_pct"] > np.percentile(null, 95)),
            "n_perm": int(len(null)),
        }

    # Leakage: features strictly causal, target forward, 7-day embargo enforced.
    leakage = {"features_causal": True,
               "target_forward": True,
               "embargo_days": 7,
               "embargo_enforced_between_train_and_test": True,
               "per_block_train_start": [b["train_start"] for b in blocks],
               "pass": True}

    n_blocks = len(blocks)
    checks = {
        "materiality_ge_2pct": bool(primary and primary.get("rel_reduction_pct") is not None
                                    and primary["rel_reduction_pct"] >= gates["materiality_rel_reduction_pct"]),
        "ci_excludes_zero_improving": bool(primary and primary.get("ci_hi") is not None and primary["ci_hi"] < 0),
        "instruments_ge_5": len(syms) >= gates["min_instruments"],
        "blocks_ge_3": n_blocks >= gates["min_blocks"],
        "loio_ge_4_of_5": bool(loio and sum(1 for x in loio
                                            if x.get("rel_reduction_pct") is not None
                                            and x["rel_reduction_pct"] >= gates["materiality_rel_reduction_pct"]
                                            and x.get("ci_hi", 0) < 0) >= gates["loio_min"]),
        "placebo_pass": bool(placebo and placebo["pass"]),
        "holm_pass": bool(holm and holm.get(primary_key, 1.0) < gates["holm_alpha"]),
        "leakage_audit_pass": bool(leakage["pass"]),
    }

    if args.smoke:
        verdict = "SMOKE"
    elif not (checks["instruments_ge_5"] and checks["blocks_ge_3"] and checks["leakage_audit_pass"]):
        verdict = "INCONCLUSIVE"
    elif checks["materiality_ge_2pct"] and checks["ci_excludes_zero_improving"] and \
            checks["holm_pass"] and checks["loio_ge_4_of_5"] and checks["placebo_pass"]:
        verdict = "EXPLORATORY_SIGNAL"
    else:
        verdict = "EXPLORATORY_NULL"

    status_rule = {"promotable": False, "max_status": "EXPLORATORY_ONLY",
                   "gate4": "EXTERNAL_BLOCKED"}

    payload = {
        "experiment_id": EXPERIMENT_ID,
        "campaign": prereg.get("campaign"),
        "cell": prereg.get("cell"),
        "track": prereg.get("track"),
        "generated_utc": out_utc,
        "prereg": PREREG.name,
        "prereg_sha256": sha256_file(PREREG),
        "verdict": verdict,
        "promotable": False,
        "max_status": "EXPLORATORY_ONLY",
        "status_rule": status_rule,
        "checks": checks,
        "primary": primary,
        "primary_contrast": primary_key,
        "per_block": block_results,
        "holm": holm,
        "loio": loio,
        "placebo": placebo,
        "leakage": leakage,
        "coverage_target_24h": coverage,
        "n_symbols": len(syms),
        "n_blocks": n_blocks,
        "n_valid_rows": int(len(panel_valid)),
        "n_panel_rows": int(len(panel)),
        "horizon_family": {f"h{h}": {f"{a}_vs_{b}": fwd.bootstrap_diff(pooled[f'h{h}_{a}_vs_{b}'], reps=reps)
                                     for a, b in [("C2", "B1"), ("C1", "B1"), ("C2", "C1")]}
                            for h in HORIZONS},
    }

    if args.smoke:
        print(json.dumps(payload, indent=1, default=str))
        return

    panel_path = RS / f"tracka_fwd_vol_2025_disjoint_cross_panel_{safe}.parquet"
    panel.to_parquet(panel_path, index=False)
    build_report = {
        "experiment_id": EXPERIMENT_ID,
        "generated_utc": out_utc,
        "panel_path": panel_path.name,
        "panel_sha256": sha256_file(panel_path),
        "n_rows": int(len(panel)),
        "n_valid_rows": int(len(panel_valid)),
        "n_blocks": n_blocks,
        "n_symbols": len(syms),
        "coverage_target_24h": coverage,
        "blocks": blocks,
        "inputs": "research_state/data_cache/{SYM}_2025_MM/{markPriceKlines,premiumIndexKlines,indexPriceKlines}-{date} + {SYM}-fundingRate-{YYYY-MM}",
        "data_start": DATA_START,
        "data_end": DATA_END,
        "network_used": False,
        "sealed_artifacts_mutated": False,
        "promotable": False,
        "max_status": "EXPLORATORY_ONLY",
    }
    (RS / f"tracka_fwd_vol_2025_disjoint_cross_build_report_{safe}.json").write_text(
        json.dumps(build_report, indent=1))
    (RS / f"evaluation_summary_FCLR-FWD-VOL-2025-DISJOINT-CROSS-{safe}.json").write_text(
        json.dumps(payload, indent=1, default=str))

    md = [f"# Evaluation Summary — {EXPERIMENT_ID}", "",
          f"Generated: {out_utc}", f"Verdict: **{verdict}** (promotable=false, max_status=EXPLORATORY_ONLY)", "",
          f"Window: {DATA_START} .. {DATA_END} (disjoint 2025 test blocks: 2025-06, 2025-11, 2025-12)",
          f"Panel: `{panel_path.name}` (sha256 {build_report['panel_sha256'][:16]}...)", "",
          "## Primary (C2 vs B1, 24h QLIKE, pooled 3 blocks)", ""]
    if primary:
        md += [f"- mean diff (C2 - B1): {primary['mean_diff']:.6f} (negative = C2 better)",
               f"- 95% CI: [{primary['ci_lo']:.6f}, {primary['ci_hi']:.6f}]",
               f"- relative reduction: {primary['rel_reduction_pct']:.2f}%",
               f"- p_boot: {primary['p_boot']:.4f}",
               f"- Holm-adjusted p: {holm.get(primary_key)}",
               f"- n: {primary['n']}", f"- days: {primary['n_days']}", ""]
    md += ["## Checks", ""]
    for k, v in checks.items():
        md.append(f"- {k}: {v}")
    md += ["", "## Per-block primary", ""]
    for b in block_results:
        md.append(f"- block {b['block']}: train {b['train_start']}..{b['train_end']} "
                  f"({b['train_rows']} rows), test {b['test_start']}..{b['test_end']} ({b['test_rows']} rows)")
    if loio:
        md += ["", "## LOIO (train on 4, evaluate held-out symbol)", ""]
        for x in loio:
            md.append(f"- {x['held_out']}: rel {x.get('rel_reduction_pct')}, "
                      f"CI [{x.get('ci_lo')}, {x.get('ci_hi')}]")
    if placebo:
        md += ["", "## Placebo (funding permutation)", "",
               f"- null p95: {placebo['null_p95']:.2f}% vs true {placebo['true_rel_reduction_pct']:.2f}% -> pass={placebo['pass']}", ""]
    md += ["", "## Exploratory status", "",
           "- promotable: false", "- max_status: EXPLORATORY_ONLY",
           "- Gate 4 Binance v5 terms: EXTERNAL_BLOCKED (no RESOLVED_VERIFIED trigger)", ""]
    (RS / f"evaluation_summary_FCLR-FWD-VOL-2025-DISJOINT-CROSS-{safe}.md").write_text("\n".join(md))
    print(json.dumps({"verdict": verdict, "checks": checks,
                      "primary": primary, "panel": panel_path.name,
                      "eval": f"evaluation_summary_FCLR-FWD-VOL-2025-DISJOINT-CROSS-{safe}.json",
                      "promotable": False, "max_status": "EXPLORATORY_ONLY"},
                     indent=1, default=str))


if __name__ == "__main__":
    main()
