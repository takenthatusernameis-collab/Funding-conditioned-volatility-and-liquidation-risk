#!/usr/bin/env python3
"""Independent numpy-only recomputation of the FCLR-011 terminal headline.

Re-derives the feature-attribution contrasts (B1, B1+funding, B1+ema24,
B1+funding+ema24) on the stored recompute panel using ONLY numpy
(OLS via normal equations solved by np.linalg.lstsq, train-only z-scaling,
Duan smearing). Compares to the carried-forward sealed RCA011
feature-attribution artifact and asserts agreement within a declared
tolerance. No statsmodels, no network, read-only.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parent.parent.parent
PANEL = REPO / "research_state/session_20261116T0040Z/fclr011_recompute_panel_20261116T004150Z.parquet"
SEALED = REPO / "research_state/session_20261116T100533Z/rca011_feature_attribution_20261116T035833Z.json"
OUT_DIR = REPO / "research_state/session_20261116T115028Z"

TRAIN_START = pd.Timestamp("2026-01-01T00:00:00Z")
TRAIN_END = pd.Timestamp("2026-03-17T23:00:00Z")
TEST_START = pd.Timestamp("2026-05-08T00:00:00Z")
TEST_END = pd.Timestamp("2026-08-06T23:00:00Z")
PURGE_DAYS = 7
EPS = 1e-12

B1_FEATS = ["log_rv1h", "log_rv24h", "log_rv168h"]
FUNDING_FEATS = ["funding_z", "abs_fund_pct_z"]
EMA24_FEATS = ["ema24_dist_z"]
TARGET = "target_rv24h"


def ols_fit(X: np.ndarray, y: np.ndarray) -> np.ndarray:
    X_int = np.column_stack([np.ones(X.shape[0]), X])
    beta, *_ = np.linalg.lstsq(X_int, y, rcond=None)
    return beta


def ols_predict(X: np.ndarray, beta: np.ndarray) -> np.ndarray:
    X_int = np.column_stack([np.ones(X.shape[0]), X])
    return X_int @ beta


def duan_smear(y_log: np.ndarray, pred_log: np.ndarray) -> float:
    return float(np.mean(np.exp(y_log - pred_log)))


def qlike(y: np.ndarray, pred: np.ndarray) -> float:
    mask = (y > 0) & (pred > 0)
    ratio = y[mask] / pred[mask]
    return float(np.mean(ratio - 1.0 - np.log(ratio)))


def clean_xy(df: pd.DataFrame, feats: list[str], target: str):
    cols = feats + [target]
    mask = df[cols].notna().all(axis=1)
    X = df.loc[mask, feats].to_numpy(dtype=float)
    y = df.loc[mask, target].to_numpy(dtype=float)
    return X, y


def main() -> int:
    df = pd.read_parquet(PANEL)
    df["ts"] = pd.to_datetime(df["ts"], utc=True)

    train_mask = (df["ts"] >= TRAIN_START) & (df["ts"] <= TRAIN_END)
    test_raw = df[(df["ts"] >= TEST_START) & (df["ts"] <= TEST_END)].copy()
    train_df = df[train_mask].copy()

    purge_before = TRAIN_END + pd.Timedelta(days=PURGE_DAYS)
    assert TEST_START >= purge_before, f"purge violated: test {TEST_START} < {purge_before}"

    # Train-only z-scaling for funding / ema24 source columns
    scale_src = ["signed_funding", "abs_funding_pct_trail", "ema24_dist"]
    scalers = {}
    for feat in scale_src:
        vals = train_df[feat].to_numpy(dtype=float)
        valid = ~np.isnan(vals)
        mean = float(vals[valid].mean()) if valid.any() else 0.0
        std = float(vals[valid].std(ddof=0)) if valid.any() else 1.0
        if std == 0:
            std = 1.0
        scalers[feat] = (mean, std)
        for d in (train_df, test_raw):
            d[feat + "_z"] = (d[feat] - mean) / std

    # Map to expected feature names used by sealed attribution
    train_df["funding_z"] = train_df["signed_funding_z"]
    train_df["abs_fund_pct_z"] = train_df["abs_funding_pct_trail_z"]
    train_df["ema24_dist_z"] = train_df["ema24_dist_z"]
    test_raw["funding_z"] = test_raw["signed_funding_z"]
    test_raw["abs_fund_pct_z"] = test_raw["abs_funding_pct_trail_z"]
    test_raw["ema24_dist_z"] = test_raw["ema24_dist_z"]

    models = {
        "B1": B1_FEATS,
        "B1_plus_funding": B1_FEATS + FUNDING_FEATS,
        "B1_plus_ema24": B1_FEATS + EMA24_FEATS,
        "B1_plus_funding_plus_ema24": B1_FEATS + FUNDING_FEATS + EMA24_FEATS,
    }

    fits = {}
    for name, feats in models.items():
        Xtr, ytr_raw = clean_xy(train_df, feats, TARGET)
        ytr_fit = np.log(ytr_raw + EPS)
        beta = ols_fit(Xtr, ytr_fit)
        pred_log = ols_predict(Xtr, beta)
        smear = duan_smear(ytr_fit, pred_log)
        fits[name] = {"beta": beta, "smear": smear, "n_train": int(Xtr.shape[0]), "feats": feats}

        Xte, yte_raw = clean_xy(test_raw, feats, TARGET)
        pred_log_te = ols_predict(Xte, beta)
        pred_te = np.exp(pred_log_te) * smear
        pos = yte_raw > 0
        q = qlike(yte_raw[pos], pred_te[pos])
        fits[name]["qlike_test"] = q
        fits[name]["n_test"] = int(pos.sum())

    contrasts_def = {
        "B1_plus_funding_vs_B1": ("B1_plus_funding", "B1"),
        "B1_plus_ema24_vs_B1": ("B1_plus_ema24", "B1"),
        "B1_plus_funding_plus_ema24_vs_B1": ("B1_plus_funding_plus_ema24", "B1"),
        "B1_plus_funding_plus_ema24_vs_B1_plus_funding": ("B1_plus_funding_plus_ema24", "B1_plus_funding"),
        "B1_plus_funding_plus_ema24_vs_B1_plus_ema24": ("B1_plus_funding_plus_ema24", "B1_plus_ema24"),
    }

    recomputed = {}
    for cid, (a, b) in contrasts_def.items():
        qa = fits[a]["qlike_test"]
        qb = fits[b]["qlike_test"]
        rel = (qb - qa) / qb * 100.0  # relative reduction of model A vs baseline B (positive = A better/lower QLIKE)
        recomputed[cid] = {"qlike_a": qa, "qlike_b": qb, "rel_pct": float(rel)}

    sealed = json.loads(SEALED.read_text())
    sealed_contrasts = sealed["contrasts"]

    tol_qlike = 1e-6
    tol_rel = 1e-3  # percent-points
    comparisons = {}
    all_pass = True
    for cid in contrasts_def:
        s = sealed_contrasts[cid]
        r = recomputed[cid]
        d_qlike_a = abs(r["qlike_a"] - s["qlike_a"])
        d_qlike_b = abs(r["qlike_b"] - s["qlike_b"])
        d_rel = abs(r["rel_pct"] - s["rel_reduction_pct"])
        ok = (d_qlike_a <= tol_qlike) and (d_qlike_b <= tol_qlike) and (d_rel <= tol_rel)
        all_pass = all_pass and ok
        comparisons[cid] = {
            "sealed_qlike_a": s["qlike_a"], "recomputed_qlike_a": r["qlike_a"], "abs_diff_qlike_a": d_qlike_a,
            "sealed_qlike_b": s["qlike_b"], "recomputed_qlike_b": r["qlike_b"], "abs_diff_qlike_b": d_qlike_b,
            "sealed_rel_pct": s["rel_reduction_pct"], "recomputed_rel_pct": r["rel_pct"], "abs_diff_rel_pct": d_rel,
            "within_tolerance": ok,
        }

    result = {
        "session_utc": "2026-11-16T11:50:28Z",
        "method": "numpy-only OLS (np.linalg.lstsq) + train-only z-scaling (ddof=0) + Duan smearing; no statsmodels; read-only",
        "panel_path": str(PANEL.relative_to(REPO)),
        "panel_sha256": hashlib.sha256(PANEL.read_bytes()).hexdigest(),
        "sealed_reference": str(SEALED.relative_to(REPO)),
        "train_window": [str(TRAIN_START), str(TRAIN_END)],
        "test_window": [str(TEST_START), str(TEST_END)],
        "purge_days": PURGE_DAYS,
        "target": TARGET,
        "models": {k: {"qlike_test": v["qlike_test"], "n_train": v["n_train"], "n_test": v["n_test"], "smear": v["smear"]} for k, v in fits.items()},
        "contrasts_recomputed": recomputed,
        "comparison": comparisons,
        "tolerances": {"qlike_abs": tol_qlike, "rel_pct_points": tol_rel},
        "all_within_tolerance": bool(all_pass),
        "conclusion": (
            "Independent numpy-only recomputation reproduces the sealed RCA011 "
            "feature-attribution QLIKE values and contrasts within declared tolerance; "
            "the terminal FCLR-011 NOT_REPRODUCED / fragile finding is confirmed by a "
            "third independent implementation path."
            if all_pass else
            "Independent recomputation diverged from sealed RCA011 beyond tolerance; "
            "investigate panel/schema drift."
        ),
    }

    out_json = OUT_DIR / "independent_recompute_fclr011_20261116T115028Z.json"
    out_json.write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))
    print(f"\nWROTE {out_json}")
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())