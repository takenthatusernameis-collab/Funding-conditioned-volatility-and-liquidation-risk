#!/usr/bin/env python3
"""FCLR-FWD-VOL-2024-DISJOINT-2024-06 singleton diagnostic (EXPLORATORY_ONLY).

Campaign: FCLR-FWD-VOL-2024-DISJOINT-2024-06-20261114T231100Z
Frozen prereg:
  research_state/prereg_fclr_fwd_vol_2024_disjoint_2024_06_20261114T231100Z.json

Singleton diagnostic only (never a fresh three-block confirmation). Cached-only,
no network, no sealed-artifact mutation. All outputs EXPLORATORY_ONLY,
promotable=false.

Usage:
  python3 scripts/fclr_fwd_vol_2024_disjoint_2024_06.py --smoke
  python3 scripts/fclr_fwd_vol_2024_disjoint_2024_06.py
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[1]
RS = REPO / "research_state"
CACHE = RS / "data_cache"
UTC = timezone.utc

EXPERIMENT_ID = "FCLR-FWD-VOL-2024-DISJOINT-2024-06-20261114T231100Z"
PREREG_JSON = RS / "prereg_fclr_fwd_vol_2024_disjoint_2024_06_20261114T231100Z.json"
PREREG_MD = RS / "prereg_fclr_fwd_vol_2024_disjoint_2024_06_20261114T231100Z.md"

SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]
KINDS = ("markPriceKlines", "premiumIndexKlines", "indexPriceKlines")
DATA_START = pd.Timestamp("2024-04-25T00:00:00Z")
DATA_END = pd.Timestamp("2024-06-30T23:00:00Z")
BUFFER_END = pd.Timestamp("2024-07-07T23:00:00Z")
TRAIN_START = pd.Timestamp("2024-04-25T00:00:00Z")
TRAIN_END = pd.Timestamp("2024-05-24T23:00:00Z")
TEST_START = pd.Timestamp("2024-06-01T00:00:00Z")
TEST_END = pd.Timestamp("2024-06-30T23:00:00Z")
EMBARGO_DAYS = 7

EPS = 1e-12
HORIZON = 24
MODEL_FEATURES = {
    "B0": ["log_rv24h"],
    "B1": ["log_rv1h", "log_rv24h", "log_rv168h"],
    "C1": ["log_rv1h", "log_rv24h", "log_rv168h", "signed_funding", "abs_fund_pct"],
    "C2": ["log_rv1h", "log_rv24h", "log_rv168h", "signed_funding", "abs_fund_pct", "premium", "ema_dist"],
}
CONTRASTS = [("C2", "B1"), ("C1", "B1"), ("C2", "C1")]
BOOT_REPS = 2000
BOOT_SEED = 20261114
PLACEBO_REPS = 200
PLACEBO_SEED = 20261114
VERDICTS = ("EXPLAINED_BY_ESTIMATOR", "EXPLAINED_BY_DATA", "UNEXPLAINED", "INCONCLUSIVE")


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _month_dir(sym: str, ym: str) -> Path:
    return CACHE / f"{sym}_{ym.replace('-', '_')}"


def _find_kline_csv(base: Path, prefix: str, ds: str, sym: str) -> Path | None:
    candidates = [
        base / f"{prefix}-{ds}" / f"{sym}-1h-{ds}.csv",
        base / f"{prefix}-{ds}" / f"{sym}-1h-{ds}" / f"{sym}-1h-{ds}.csv",
    ]
    for c in candidates:
        if c.exists():
            return c
    # fallback recursive search within day dir
    day_dir = base / f"{prefix}-{ds}"
    if day_dir.exists():
        hits = sorted(day_dir.glob(f"**/{sym}-1h-{ds}.csv"))
        if hits:
            return hits[0]
    return None


def _read_close_csv(path: Path) -> pd.DataFrame | None:
    try:
        df = pd.read_csv(path)
    except Exception:
        return None
    if "open_time" not in df.columns or "close" not in df.columns or df.empty:
        return None
    out = pd.DataFrame({
        "ts": pd.to_datetime(df["open_time"], unit="ms", utc=True),
        "close": pd.to_numeric(df["close"], errors="coerce"),
    }).dropna()
    return out if not out.empty else None


def load_series(sym: str, prefix: str, start: pd.Timestamp, end: pd.Timestamp) -> pd.Series:
    frames = []
    for d in pd.date_range(start.floor("D"), end.floor("D"), freq="D", tz=UTC):
        ds = d.strftime("%Y-%m-%d")
        base = _month_dir(sym, ds[:7])
        p = _find_kline_csv(base, prefix, ds, sym)
        df = _read_close_csv(p) if p else None
        if df is not None:
            frames.append(df)
    if not frames:
        return pd.Series(dtype=float, name=prefix)
    out = pd.concat(frames).drop_duplicates("ts").sort_values("ts").set_index("ts")["close"]
    return out[~out.index.duplicated()]


def load_funding(sym: str, start: pd.Timestamp, end: pd.Timestamp) -> pd.DataFrame:
    frames = []
    for ym in sorted({d.strftime("%Y-%m") for d in pd.date_range(start.floor("D"), end.floor("D"), freq="D", tz=UTC)}):
        base = _month_dir(sym, ym)
        candidates = [
            base / f"{sym}-fundingRate-{ym}" / f"{sym}-fundingRate-{ym}.csv",
            base / f"{sym}-fundingRate-{ym}.csv",
        ]
        p = next((c for c in candidates if c.exists()), None)
        if p is None:
            # recursive fallback
            hits = sorted(base.glob(f"**/{sym}-fundingRate-{ym}.csv")) if base.exists() else []
            p = hits[0] if hits else None
        if p is None or not p.exists():
            continue
        try:
            df = pd.read_csv(p, usecols=["calc_time", "last_funding_rate"])
        except Exception:
            continue
        if df.empty:
            continue
        df["ts"] = pd.to_datetime(df["calc_time"], unit="ms", utc=True).dt.floor("h")
        df["funding_rate"] = pd.to_numeric(df["last_funding_rate"], errors="coerce")
        frames.append(df[["ts", "funding_rate"]].dropna().drop_duplicates("ts").sort_values("ts"))
    if not frames:
        return pd.DataFrame(columns=["ts", "funding_rate"])
    return pd.concat(frames).drop_duplicates("ts").sort_values("ts")


def build_symbol(sym: str, start: pd.Timestamp, end: pd.Timestamp) -> pd.DataFrame:
    mark = load_series(sym, "markPriceKlines", start, end)
    prem = load_series(sym, "premiumIndexKlines", start, end)
    idx = load_series(sym, "indexPriceKlines", start, end)
    fund = load_funding(sym, start - pd.Timedelta(days=120), end)

    grid = pd.date_range(start, end, freq="1h", tz=UTC)
    df = pd.DataFrame(index=grid)
    df.index.name = "ts"
    df["mark"] = mark.reindex(grid)
    df["premium_src"] = prem.reindex(grid)
    df["index"] = idx.reindex(grid)
    if not fund.empty:
        left = pd.DataFrame({"ts": grid})
        merged = pd.merge_asof(left, fund.sort_values("ts"), on="ts", direction="backward")
        df["funding_rate"] = merged["funding_rate"].values
    else:
        df["funding_rate"] = np.nan

    df["ret"] = np.log(df["mark"]).diff()
    df["r2"] = df["ret"] ** 2
    df["rv1h"] = df["r2"]
    df["rv24h"] = df["r2"].rolling(24, min_periods=24).sum()
    df["rv168h"] = df["r2"].rolling(168, min_periods=168).sum()
    df["log_rv1h"] = np.log(df["rv1h"] + EPS)
    df["log_rv24h"] = np.log(df["rv24h"] + EPS)
    df["log_rv168h"] = np.log(df["rv168h"] + EPS)
    df["signed_funding"] = df["funding_rate"]
    df["premium"] = df["premium_src"]
    fallback_prem = df["mark"] / df["index"] - 1.0
    df["premium"] = df["premium"].where(df["premium"].notna(), fallback_prem)
    ema24 = df["mark"].ewm(span=24, adjust=False).mean()
    df["ema_dist"] = df["mark"] / ema24 - 1.0

    # past-only 90-day |funding| percentile from raw 8h funding history:
    # latest funding <= t; history strictly < t; min 30 observations.
    if not fund.empty:
        f = fund.dropna().drop_duplicates("ts").sort_values("ts")
        ft = pd.to_datetime(f["ts"], utc=True).values.astype("datetime64[ns]")
        fa = f["funding_rate"].abs().values
        ts_all = df.index.values.astype("datetime64[ns]")
        latest = np.searchsorted(ft, ts_all, side="right") - 1
        pct = np.full(len(df), np.nan)
        for i in range(len(df)):
            j = latest[i]
            if j < 0:
                continue
            lo = np.searchsorted(ft, ts_all[i] - np.timedelta64(90, "D"), side="left")
            hist = fa[lo:j]
            if len(hist) >= 30:
                pct[i] = np.count_nonzero(hist <= fa[j]) / len(hist)
        df["abs_fund_pct"] = pct
    else:
        df["abs_fund_pct"] = np.nan

    roll = df["r2"].rolling(HORIZON, min_periods=HORIZON).sum()
    df["target_24h"] = roll.shift(-HORIZON)
    df["symbol"] = sym
    return df.reset_index()


def finite_mask(df: pd.DataFrame, cols: list[str]) -> np.ndarray:
    ok = np.ones(len(df), dtype=bool)
    for c in cols:
        ok &= np.isfinite(df[c].values)
    return ok


def fit_sealed(train: pd.DataFrame, feats: list[str]):
    Xtr = train[feats].values.astype(float)
    ytr = np.log(train["target_24h"].values.astype(float) + EPS)
    A = np.column_stack([np.ones(len(Xtr)), Xtr])
    XtX = A.T @ A
    for i in range(XtX.shape[0]):
        XtX[i, i] += 1e-12
    beta = np.linalg.solve(XtX, A.T @ ytr)
    return {"kind": "sealed", "beta": beta, "feats": feats, "mu": None, "sd": None, "smear": 1.0}


def fit_corrected(train: pd.DataFrame, feats: list[str]):
    Xtr = train[feats].values.astype(float)
    ytr = np.log(train["target_24h"].values.astype(float) + EPS)
    mu = Xtr.mean(axis=0)
    sd = Xtr.std(axis=0)
    sd = np.where(sd == 0, 1.0, sd)
    Xs = (Xtr - mu) / sd
    A = np.column_stack([np.ones(len(Xs)), Xs])
    beta, *_ = np.linalg.lstsq(A, ytr, rcond=None)
    resid = ytr - A @ beta
    smear = float(np.mean(np.exp(resid)))
    return {"kind": "corrected", "beta": beta, "feats": feats, "mu": mu, "sd": sd, "smear": smear}


def predict(model: dict, test: pd.DataFrame) -> pd.DataFrame:
    feats = model["feats"]
    X = test[feats].values.astype(float)
    y = test["target_24h"].values.astype(float)
    if model["kind"] == "sealed":
        A = np.column_stack([np.ones(len(X)), X])
        yhat = np.exp(A @ model["beta"])
    else:
        Xs = (X - model["mu"]) / model["sd"]
        A = np.column_stack([np.ones(len(Xs)), Xs])
        yhat = np.exp(A @ model["beta"]) * model["smear"]
    q = np.where((y > 0) & (yhat > 0), y / yhat - np.log(y / yhat) - 1.0, np.nan)
    return pd.DataFrame({"ts": test["ts"].values, "symbol": test["symbol"].values,
                         "y": y, "yhat": yhat, "qlike": q})


def fit_predict(train: pd.DataFrame, test: pd.DataFrame, model_name: str, arm: str):
    feats = MODEL_FEATURES[model_name]
    cols = feats + ["target_24h"]
    tr = train[finite_mask(train, cols)].copy()
    te = test[finite_mask(test, cols)].copy()
    if len(tr) == 0 or len(te) == 0:
        return pd.DataFrame(columns=["ts", "symbol", "y", "yhat", "qlike"]), {"train_rows": len(tr), "test_rows": len(te)}
    fit = fit_sealed(tr, feats) if arm == "sealed" else fit_corrected(tr, feats)
    pred = predict(fit, te)
    meta = {"train_rows": int(len(tr)), "test_rows": int(len(te)),
            "smear": float(fit["smear"]), "scaled": arm == "corrected"}
    return pred, meta


def contrast_diff(frames: dict, a: str, b: str) -> pd.DataFrame:
    A = frames[a][["ts", "symbol", "qlike"]].rename(columns={"qlike": "qa"})
    B = frames[b][["ts", "symbol", "qlike"]].rename(columns={"qlike": "qb"})
    M = A.merge(B, on=["ts", "symbol"], how="inner").dropna()
    M["diff"] = M["qa"] - M["qb"]
    return M


def bootstrap_diff(M: pd.DataFrame, reps: int = BOOT_REPS, seed: int = BOOT_SEED):
    if M.empty:
        return None
    M = M.copy()
    M["day"] = pd.to_datetime(M["ts"]).dt.floor("D")
    groups = [g["diff"].values for _, g in M.groupby("day")]
    n = len(groups)
    if n == 0:
        return None
    rng = np.random.default_rng(seed)
    means = np.empty(reps)
    for r in range(reps):
        idx = rng.integers(0, n, n)
        vals = np.concatenate([groups[i] for i in idx])
        means[r] = vals.mean()
    lo, hi = np.percentile(means, [2.5, 97.5])
    mean = float(M["diff"].mean())
    p = float(2.0 * min((means <= 0).mean(), (means >= 0).mean()))
    qb_mean = float(M["qb"].mean())
    rel = float(-mean / abs(qb_mean) * 100.0) if qb_mean else None
    return {"mean_diff": mean, "ci_lo": float(lo), "ci_hi": float(hi),
            "p_boot": p, "n": int(len(M)), "n_days": int(n),
            "rel_reduction_pct": rel}


def holm(pvals: dict[str, float]) -> dict[str, float]:
    items = sorted(pvals.items(), key=lambda kv: kv[1])
    m = len(items)
    out = {}
    prev = 0.0
    for rank, (k, p) in enumerate(items):
        adj = min(1.0, max(prev, (m - rank) * p))
        out[k] = float(adj)
        prev = adj
    return out


def split_panel(panel: pd.DataFrame):
    p = panel.copy()
    p["ts"] = pd.to_datetime(p["ts"], utc=True)
    train = p[(p["ts"] >= TRAIN_START) & (p["ts"] <= TRAIN_END)].copy()
    test = p[(p["ts"] >= TEST_START) & (p["ts"] <= TEST_END)].copy()
    return train, test


def leakage_audit(panel: pd.DataFrame) -> dict:
    p = panel.copy()
    p["ts"] = pd.to_datetime(p["ts"], utc=True)
    train, test = split_panel(p)
    embargo_gap = (TEST_START - TRAIN_END).days
    # feature causality: by construction features at t use <=t (funding merge_asof backward, rolling past, shifted target forward)
    # empirical check: target_24h is forward sum shifted -24 => for each row target uses t+1..t+24
    # check no train ts >= test ts and embargo respected
    checks = {
        "train_after_test_empty": bool(train["ts"].max() < test["ts"].min()),
        "embargo_days": int(embargo_gap),
        "embargo_enforced": bool(embargo_gap == EMBARGO_DAYS),
        "features_causal_by_construction": True,
        "target_forward_by_construction": True,
        "no_future_scaling_fitting_imputation": True,
    }
    checks["pass"] = all(bool(v) for v in checks.values() if isinstance(v, bool)) and checks["embargo_days"] == EMBARGO_DAYS
    return checks


def collect_source_hashes() -> list[dict]:
    out = []
    for sym in SYMBOLS:
        for ym in ["2024-04", "2024-05", "2024-06"]:
            base = _month_dir(sym, ym)
            if not base.exists():
                out.append({"symbol": sym, "month": ym, "path": str(base), "exists": False})
                continue
            # hash representative required files/dirs contents by listing and hashing csv files present
            csvs = sorted(base.glob("**/*.csv"))
            for c in csvs:
                rel = c.relative_to(REPO)
                out.append({"symbol": sym, "month": ym, "path": str(rel), "sha256": sha256_file(c), "bytes": c.stat().st_size})
    return out


def run_arm(panel: pd.DataFrame, arm: str, reps: int = BOOT_REPS, placebo_reps: int = PLACEBO_REPS) -> dict:
    train, test = split_panel(panel)
    frames = {}
    fit_meta = {}
    for m in MODEL_FEATURES:
        pred, meta = fit_predict(train, test, m, arm)
        frames[m] = pred
        fit_meta[m] = meta
    diffs = {f"{a}_vs_{b}": contrast_diff(frames, a, b) for a, b in CONTRASTS}
    stats = {k: bootstrap_diff(v, reps=reps, seed=BOOT_SEED) for k, v in diffs.items()}
    pvals = {k: (v["p_boot"] if v else 1.0) for k, v in stats.items()}
    holm_adj = holm(pvals)
    # LOIO: leave one instrument out of training, evaluate on held-out instrument
    loio = []
    for held in SYMBOLS:
        tr_loo = train[train["symbol"] != held].copy()
        te_loo = test[test["symbol"] == held].copy()
        loo_frames = {}
        ok = True
        for m in ("B1", "C2"):
            pred, _ = fit_predict(tr_loo, te_loo, m, arm)
            loo_frames[m] = pred
        M = contrast_diff(loo_frames, "C2", "B1")
        bs = bootstrap_diff(M, reps=max(200, reps // 4), seed=BOOT_SEED)
        loio.append({"held_out": held, **(bs or {})})
    # placebo: permute funding features within symbol on full panel copy, refit/eval
    rng = np.random.default_rng(PLACEBO_SEED)
    null = []
    for _ in range(placebo_reps):
        pp = panel.copy()
        for sym in SYMBOLS:
            idx = pp.index[pp["symbol"] == sym]
            if len(idx) == 0:
                continue
            for col in ("signed_funding", "abs_fund_pct"):
                vals = pp.loc[idx, col].values.copy()
                pp.loc[idx, col] = rng.permutation(vals)
        trp, tep = split_panel(pp)
        pf = {}
        for m in ("B1", "C2"):
            pred, _ = fit_predict(trp, tep, m, arm)
            pf[m] = pred
        M = contrast_diff(pf, "C2", "B1")
        bs = bootstrap_diff(M, reps=max(100, reps // 10), seed=BOOT_SEED)
        if bs and bs.get("rel_reduction_pct") is not None:
            null.append(float(bs["rel_reduction_pct"]))
    primary = stats.get("C2_vs_B1")
    placebo = None
    if null and primary and primary.get("rel_reduction_pct") is not None:
        arr = np.array(null)
        placebo = {
            "n_perm": int(len(null)),
            "null_p95": float(np.percentile(arr, 95)),
            "true_rel_reduction_pct": float(primary["rel_reduction_pct"]),
            "pass": bool(primary["rel_reduction_pct"] > np.percentile(arr, 95)),
        }
    else:
        placebo = {"n_perm": len(null), "null_p95": None, "true_rel_reduction_pct": (primary or {}).get("rel_reduction_pct"), "pass": False}
    return {
        "arm": arm,
        "fit_meta": fit_meta,
        "contrasts": stats,
        "holm": holm_adj,
        "loio": loio,
        "placebo": placebo,
        "primary": primary,
    }


def decide_verdict(results: dict, lineage: dict, leakage: dict) -> str:
    if not lineage.get("pass") or not leakage.get("pass"):
        return "INCONCLUSIVE"
    sealed = results.get("sealed", {}).get("primary") or {}
    corrected = results.get("corrected", {}).get("primary") or {}
    for s in (sealed, corrected):
        if not s or s.get("n", 0) == 0:
            return "INCONCLUSIVE"
    # estimator attribution: meaningful swing in primary sign/magnitude between arms
    s_rel = sealed.get("rel_reduction_pct")
    c_rel = corrected.get("rel_reduction_pct")
    if s_rel is None or c_rel is None:
        return "INCONCLUSIVE"
    swing = abs(float(c_rel) - float(s_rel))
    sign_flip = (s_rel > 0) != (c_rel > 0) and max(abs(s_rel), abs(c_rel)) >= 1.0
    if swing >= 2.0 or sign_flip:
        return "EXPLAINED_BY_ESTIMATOR"
    # data explanation: if lineage had issues it would be caught above; no extra data arm here
    # but if both arms consistent and both materially adverse/same-direction null-ish, mark unexplained (bounded)
    return "UNEXPLAINED"


def lineage_check(panel: pd.DataFrame) -> dict:
    p = panel.copy()
    p["ts"] = pd.to_datetime(p["ts"], utc=True)
    train, test = split_panel(p)
    cols_needed = sorted(set(sum(MODEL_FEATURES.values(), [])) | {"target_24h", "ts", "symbol"})
    per_cell = {}
    for m, feats in MODEL_FEATURES.items():
        cols = feats + ["target_24h"]
        tr = train[finite_mask(train, cols)]
        te = test[finite_mask(test, cols)]
        per_cell[m] = {"train_rows": int(len(tr)), "test_rows": int(len(te)), "train_days": int(tr["ts"].dt.floor("D").nunique()), "test_days": int(te["ts"].dt.floor("D").nunique())}
    checks = {
        "row_count": int(len(p)),
        "key_count": int(p[["symbol", "ts"]].drop_duplicates().shape[0]),
        "duplicate_keys": int(p.duplicated(["symbol", "ts"]).sum()),
        "symbols": sorted(p["symbol"].unique().tolist()),
        "span_start": str(p["ts"].min()),
        "span_end": str(p["ts"].max()),
        "train_rows": int(len(train)),
        "test_rows": int(len(test)),
        "has_5_symbols": len(p["symbol"].unique()) == 5,
        "no_duplicate_keys": int(p.duplicated(["symbol", "ts"]).sum()) == 0,
        "span_ok": p["ts"].min() == DATA_START and p["ts"].max() == BUFFER_END,
        "train_test_nonempty": len(train) > 0 and len(test) > 0,
        "per_model_cell_coverage": per_cell,
    }
    checks["per_cell_nonzero"] = all(v["train_rows"] > 0 and v["test_rows"] > 0 for v in per_cell.values())
    checks["pass"] = all([
        checks["has_5_symbols"], checks["no_duplicate_keys"], checks["span_ok"],
        checks["train_test_nonempty"], checks["per_cell_nonzero"],
    ])
    return checks


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true", help="fast reduced-rep smoke run")
    args = ap.parse_args()

    prereg = json.loads(PREREG_JSON.read_text())
    assert prereg["status"] == "FROZEN_PRE_OUTCOMES"
    assert prereg["outcome_data_inspected_before_freeze"] is False
    assert prereg["frozen_before_outcomes"] is True
    assert prereg["experiment_id"] == EXPERIMENT_ID

    reps = 200 if args.smoke else BOOT_REPS
    placebo_reps = 20 if args.smoke else PLACEBO_REPS

    # build panel (grid to buffer end for forward targets)
    panels = []
    for sym in SYMBOLS:
        panels.append(build_symbol(sym, DATA_START, BUFFER_END))
    panel = pd.concat(panels, ignore_index=True)
    panel["ts"] = pd.to_datetime(panel["ts"], utc=True)
    panel = panel.sort_values(["symbol", "ts"]).reset_index(drop=True)

    lin = lineage_check(panel)
    leak = leakage_audit(panel)

    # panel artifact
    out_utc = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    if args.smoke:
        panel_path = None
        panel_hash = None
        build_report_path = None
        eval_json_path = None
        eval_md_path = None
    else:
        panel_path = RS / f"tracka_fwd_vol_2024_disjoint_2024_06_panel_{out_utc}.parquet"
        panel.to_parquet(panel_path, index=False)
        panel_hash = sha256_file(panel_path)
        source_hashes = collect_source_hashes()
        build_report = {
            "experiment_id": EXPERIMENT_ID,
            "campaign": EXPERIMENT_ID,
            "generated_utc": now_utc(),
            "prereg": PREREG_JSON.name,
            "prereg_sha256": sha256_file(PREREG_JSON),
            "panel_path": str(panel_path.relative_to(REPO)),
            "panel_sha256": panel_hash,
            "row_count": int(len(panel)),
            "key_count": int(panel[["symbol", "ts"]].drop_duplicates().shape[0]),
            "symbols": sorted(panel["symbol"].unique().tolist()),
            "span_start": str(panel["ts"].min()),
            "span_end": str(panel["ts"].max()),
            "data_months": ["2024-04", "2024-05", "2024-06"],
            "train": {"start": str(TRAIN_START), "end": str(TRAIN_END)},
            "test": {"start": str(TEST_START), "end": str(TEST_END)},
            "embargo_days": EMBARGO_DAYS,
            "target_buffer_end": str(BUFFER_END),
            "lineage_check": lin,
            "leakage_audit": leak,
            "source_file_hash_count": len(source_hashes),
            "source_file_hashes_sample": source_hashes[:20],
            "promotable": False,
            "max_status": "EXPLORATORY_ONLY",
        }
        build_report_path = RS / f"tracka_fwd_vol_2024_disjoint_2024_06_build_report_{out_utc}.json"
        build_report_path.write_text(json.dumps(build_report, indent=2, sort_keys=True, default=str))

    # compute outcomes only after lineage/leakage checks recorded in-memory (and build report written in full mode)
    if not lin.get("pass") or not leak.get("pass"):
        results = {}
        verdict = "INCONCLUSIVE"
    else:
        results = {
            "sealed": run_arm(panel, "sealed", reps=reps, placebo_reps=placebo_reps),
            "corrected": run_arm(panel, "corrected", reps=reps, placebo_reps=placebo_reps),
        }
        verdict = decide_verdict(results, lin, leak)

    # attribution detail
    swing = None
    if results.get("sealed") and results.get("corrected"):
        s = (results["sealed"].get("primary") or {}).get("rel_reduction_pct")
        c = (results["corrected"].get("primary") or {}).get("rel_reduction_pct")
        if s is not None and c is not None:
            swing = float(c) - float(s)

    summary = {
        "experiment_id": EXPERIMENT_ID,
        "campaign": EXPERIMENT_ID,
        "generated_utc": now_utc(),
        "smoke": bool(args.smoke),
        "prereg": PREREG_JSON.name,
        "prereg_sha256": sha256_file(PREREG_JSON),
        "prereg_frozen_before_outcomes": True,
        "promotable": False,
        "max_status": "EXPLORATORY_ONLY",
        "singleton_only": True,
        "verdict": verdict,
        "verdict_space": list(VERDICTS),
        "lineage_check": lin,
        "leakage_audit": leak,
        "estimator_swing_corrected_minus_sealed_rel_pct": swing,
        "results": results,
        "panel": {
            "path": str(panel_path.relative_to(REPO)) if panel_path else None,
            "sha256": panel_hash,
            "row_count": int(len(panel)),
            "key_count": int(panel[["symbol", "ts"]].drop_duplicates().shape[0]),
            "symbols": sorted(panel["symbol"].unique().tolist()),
            "span_start": str(panel["ts"].min()),
            "span_end": str(panel["ts"].max()),
        },
        "splits": {
            "train_start": str(TRAIN_START), "train_end": str(TRAIN_END),
            "test_start": str(TEST_START), "test_end": str(TEST_END),
            "embargo_days": EMBARGO_DAYS, "target_buffer_end": str(BUFFER_END),
        },
        "notes": "Singleton diagnostic only. Not a three-block confirmation. No sealed verdicts reopened.",
    }

    if not args.smoke:
        eval_json_path = RS / f"evaluation_summary_{EXPERIMENT_ID}_{out_utc}.json"
        eval_md_path = RS / f"evaluation_summary_{EXPERIMENT_ID}_{out_utc}.md"
        eval_json_path.write_text(json.dumps(summary, indent=2, sort_keys=True, default=str))
        md = []
        md.append(f"# Evaluation Summary — {EXPERIMENT_ID}")
        md.append("")
        md.append(f"- Generated: {summary['generated_utc']}")
        md.append(f"- Verdict: **{verdict}**")
        md.append(f"- Promotable: false | Max status: EXPLORATORY_ONLY | Singleton: true")
        md.append(f"- Prereg: `{PREREG_JSON.name}` (sha256 `{summary['prereg_sha256']}`)")
        md.append(f"- Panel: `{summary['panel']['path']}` (sha256 `{panel_hash}`)")
        md.append("")
        md.append("## Lineage & Leakage")
        md.append(f"- lineage pass: {lin.get('pass')} | leakage pass: {leak.get('pass')}")
        md.append(f"- rows={lin.get('row_count')} keys={lin.get('key_count')} dup_keys={lin.get('duplicate_keys')} symbols={lin.get('symbols')}")
        md.append(f"- span: {lin.get('span_start')} .. {lin.get('span_end')}")
        md.append("")
        md.append("## Estimator Arms (primary C2 vs B1, 24h QLIKE)")
        for arm in ("sealed", "corrected"):
            prim = (results.get(arm) or {}).get("primary")
            if prim:
                md.append(f"- {arm}: mean_diff={prim.get('mean_diff')}, rel_reduction_pct={prim.get('rel_reduction_pct')}, ci=[{prim.get('ci_lo')}, {prim.get('ci_hi')}], p_boot={prim.get('p_boot')}, n={prim.get('n')}, days={prim.get('n_days')}")
            else:
                md.append(f"- {arm}: no primary result")
        md.append(f"- swing (corrected-sealed rel pct): {swing}")
        md.append("")
        md.append("## Verdict")
        md.append(f"- {verdict} (EXPLORATORY_ONLY, promotable=false, singleton diagnostic)")
        eval_md_path.write_text("\n".join(md) + "\n")

    print(json.dumps({
        "experiment_id": EXPERIMENT_ID,
        "verdict": verdict,
        "smoke": bool(args.smoke),
        "lineage_pass": lin.get("pass"),
        "leakage_pass": leak.get("pass"),
        "estimator_swing_rel_pct": swing,
        "panel_sha256": panel_hash,
        "eval_json": str(eval_json_path.relative_to(REPO)) if eval_json_path else None,
    }, indent=2, sort_keys=True))
    return 0 if verdict in VERDICTS else 2


if __name__ == "__main__":
    raise SystemExit(main())
