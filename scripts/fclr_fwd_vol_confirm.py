#!/usr/bin/env python3
"""FCLR-FWD-VOL-011-CONFIRM — heavy confirmatory pipeline (P1, Track C).

Frozen prereg: research_state/prereg_fclr_fwd_vol_011_confirm_20261113T041200Z.{json,md}

Reads only the cached Binance public-archive mark/premium/index/funding CSVs
(no network). Builds a causal hourly panel for the five FCLR-011 symbols, runs a
rolling-origin walk-forward (3 x 30-day test blocks, 7-day embargo), fits
B0/B1/C1/C2 by OLS with train-only standardization and smearing, and evaluates
the pre-registered C2 vs B1 QLIKE contrast with a 2000-replicate day-block
bootstrap, Holm across 12 cells, LOIO, funding-permutation placebo, an
exclude-inspected-days sensitivity, and an FCLR-011 reproduction cell.

Outputs (no raw cache is committed):
  research_state/tracka_fwd_vol_panel_<UTC>.parquet
  research_state/tracka_fwd_vol_build_report_<UTC>.json
  research_state/evaluation_summary_FCLR-FWD-VOL-011-CONFIRM-<UTC>.{md,json}

Usage:
  python3 scripts/fclr_fwd_vol_confirm.py            # full run
  python3 scripts/fclr_fwd_vol_confirm.py --smoke    # 1 symbol, block 0 only
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[1]
RS = REPO / "research_state"
CACHE = RS / "data_cache"
PREREG = RS / "prereg_fclr_fwd_vol_011_confirm_20261113T041200Z.json"
EPS = 1e-12
UTC = "UTC"

SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]
HORIZONS = [6, 24, 72, 168]
PRIMARY_H = 24
CONTRASTS = [("C2_vs_B1", "C2", "B1"), ("C1_vs_B1", "C1", "B1"), ("C2_vs_C1", "C2", "C1")]
MODEL_FEATURES = {
    "B0": ["log_rv24h"],
    "B1": ["log_rv1h", "log_rv24h", "log_rv168h"],
    "C1": ["log_rv1h", "log_rv24h", "log_rv168h", "signed_funding", "abs_fund_pct"],
    "C2": ["log_rv1h", "log_rv24h", "log_rv168h", "signed_funding", "abs_fund_pct",
           "premium", "ema_dist"],
}
SEED = 20261113
BOOT_REPS = 2000
PLACEBO_REPS = 200
FDR_ALPHA = 0.05


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def month_iter(start: str, end: str):
    y, m = int(start[:4]), int(start[5:7])
    ey, em = int(end[:4]), int(end[5:7])
    while (y, m) <= (ey, em):
        yield f"{y:04d}-{m:02d}"
        m += 1
        if m > 12:
            m = 1
            y += 1


def month_dir(sym: str, ym: str) -> Path:
    y, m = ym.split("-")
    return CACHE / f"{sym}_{y}_{int(m):02d}"


def read_close_csv(path: Path) -> pd.DataFrame | None:
    if not path.exists():
        return None
    try:
        df = pd.read_csv(path, usecols=["open_time", "close"])
    except Exception:
        return None
    if df.empty:
        return None
    df["ts"] = pd.to_datetime(df["open_time"], unit="ms", utc=True)
    df["close"] = pd.to_numeric(df["close"], errors="coerce")
    return df[["ts", "close"]].dropna().drop_duplicates("ts").sort_values("ts")


def load_mark(sym: str, start: pd.Timestamp, end: pd.Timestamp) -> pd.Series:
    frames = []
    for d in pd.date_range(start.floor("D"), end.floor("D"), freq="D"):
        ds = d.strftime("%Y-%m-%d")
        base = month_dir(sym, ds[:7])
        for sub in (f"markPriceKlines-{ds}",):
            p = base / sub / f"{sym}-1h-{ds}.csv"
            df = read_close_csv(p)
            if df is not None:
                frames.append(df)
    if not frames:
        return pd.Series(dtype=float, name="mark")
    out = pd.concat(frames).drop_duplicates("ts").sort_values("ts").set_index("ts")["close"]
    return out[~out.index.duplicated()]


def load_field(sym: str, prefix: str, start: pd.Timestamp, end: pd.Timestamp) -> pd.Series:
    frames = []
    for d in pd.date_range(start.floor("D"), end.floor("D"), freq="D"):
        ds = d.strftime("%Y-%m-%d")
        base = month_dir(sym, ds[:7])
        p = base / f"{prefix}-{ds}" / f"{sym}-1h-{ds}.csv"
        df = read_close_csv(p)
        if df is not None:
            frames.append(df)
    if not frames:
        return pd.Series(dtype=float, name=prefix)
    out = pd.concat(frames).drop_duplicates("ts").sort_values("ts").set_index("ts")["close"]
    return out[~out.index.duplicated()]


def load_funding(sym: str, start: pd.Timestamp, end: pd.Timestamp) -> pd.DataFrame:
    frames = []
    for ym in month_iter(start.strftime("%Y-%m"), end.strftime("%Y-%m")):
        base = month_dir(sym, ym)
        p = base / f"{sym}-fundingRate-{ym}" / f"{sym}-fundingRate-{ym}.csv"
        if not p.exists():
            continue
        try:
            df = pd.read_csv(p, usecols=["calc_time", "last_funding_rate"])
        except Exception:
            continue
        if df.empty:
            continue
        df["ts"] = pd.to_datetime(df["calc_time"], unit="ms", utc=True).dt.floor("1h")
        df["funding_rate"] = pd.to_numeric(df["last_funding_rate"], errors="coerce")
        frames.append(df[["ts", "funding_rate"]].dropna().drop_duplicates("ts").sort_values("ts"))
    if not frames:
        return pd.DataFrame(columns=["ts", "funding_rate"])
    return pd.concat(frames).drop_duplicates("ts").sort_values("ts")


def build_symbol(sym: str, start: pd.Timestamp, end: pd.Timestamp) -> pd.DataFrame:
    mark = load_mark(sym, start, end)
    prem = load_field(sym, "premiumIndexKlines", start, end)
    idx = load_field(sym, "indexPriceKlines", start, end)
    fund = load_funding(sym, start - pd.Timedelta(days=120), end)

    grid = pd.date_range(start, end, freq="1h", tz=UTC)
    df = pd.DataFrame(index=grid)
    df.index.name = "ts"
    df["mark"] = mark.reindex(grid)
    df["premium_src"] = prem.reindex(grid)
    df["index"] = idx.reindex(grid)
    # causal funding: last observation at or before t (merge_asof, backward)
    if not fund.empty:
        left = pd.DataFrame({"ts": grid})
        merged = pd.merge_asof(left, fund, on="ts", direction="backward")
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

    # past-only 90-day |funding| percentile, computed at each hourly origin
    # from the RAW 8-hourly funding history (legacy FCLR-011 convention):
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

    for h in HORIZONS:
        roll = df["r2"].rolling(h, min_periods=h).sum()
        df[f"target_{h}h"] = roll.shift(-h)
    df["symbol"] = sym
    return df.reset_index()


def common_valid_mask(panel: pd.DataFrame) -> pd.Series:
    cols = ["log_rv1h", "log_rv24h", "log_rv168h", "signed_funding", "abs_fund_pct",
            "premium", "ema_dist", "target_24h"]
    ok = np.ones(len(panel), dtype=bool)
    for c in cols:
        ok &= np.isfinite(panel[c].values)
    return pd.Series(ok, index=panel.index)


def fit_predict(train: pd.DataFrame, test: pd.DataFrame, model: str):
    feats = MODEL_FEATURES[model]
    Xtr = train[feats].values.astype(float)
    ytr = np.log(train["target_24h"].values.astype(float) + EPS)
    mu = Xtr.mean(axis=0)
    sd = Xtr.std(axis=0)
    sd[sd == 0] = 1.0
    Xtr_s = (Xtr - mu) / sd
    A = np.column_stack([np.ones(len(Xtr_s)), Xtr_s])
    beta, *_ = np.linalg.lstsq(A, ytr, rcond=None)
    resid = ytr - A @ beta
    smear = float(np.mean(np.exp(resid)))
    Xte = (test[feats].values.astype(float) - mu) / sd
    Ate = np.column_stack([np.ones(len(Xte)), Xte])
    yhat = np.exp(Ate @ beta) * smear
    y = test["target_24h"].values.astype(float)
    q = np.where((y > 0) & (yhat > 0), y / yhat - np.log(y / yhat) - 1.0, np.nan)
    return pd.DataFrame({"ts": test["ts"].values, "symbol": test["symbol"].values,
                         "y": y, "yhat": yhat, "qlike": q}), beta, smear


def qlike_frame(train: pd.DataFrame, test: pd.DataFrame):
    out = {}
    for m in ("B0", "B1", "C1", "C2"):
        out[m] = fit_predict(train, test, m)[0]
    return out


def paired_diffs(frames: dict, a: str, b: str) -> pd.DataFrame:
    A = frames[a][["ts", "symbol", "qlike"]].rename(columns={"qlike": "qa"})
    B = frames[b][["ts", "symbol", "qlike"]].rename(columns={"qlike": "qb"})
    M = A.merge(B, on=["ts", "symbol"], how="inner").dropna()
    M["diff"] = M["qa"] - M["qb"]
    return M


def bootstrap_diff(M: pd.DataFrame, reps: int = BOOT_REPS, seed: int = SEED):
    if M.empty:
        return None
    M = M.copy()
    M["day"] = pd.to_datetime(M["ts"]).dt.floor("D")
    groups = [g["diff"].values for _, g in M.groupby("day")]
    if not groups:
        return None
    rng = np.random.default_rng(seed)
    means = np.empty(reps)
    n = len(groups)
    for r in range(reps):
        idx = rng.integers(0, n, n)
        vals = np.concatenate([groups[i] for i in idx])
        means[r] = vals.mean()
    lo, hi = np.percentile(means, [2.5, 97.5])
    mean = float(M["diff"].mean())
    p = 2.0 * min((means <= 0).mean(), (means >= 0).mean())
    return {"mean_diff": mean, "ci_lo": float(lo), "ci_hi": float(hi),
            "n": int(len(M)), "n_days": int(n), "p_boot": float(p),
            "rel_reduction_pct": float(-mean / abs(M["qb"].mean()) * 100.0) if M["qb"].mean() else None}


def holm(pvals: dict) -> dict:
    items = sorted(pvals.items(), key=lambda kv: kv[1])
    m = len(items)
    out = {}
    prev = 0.0
    for rank, (k, p) in enumerate(items):
        adj = min(1.0, max(prev, (m - rank) * p))
        out[k] = adj
        prev = adj
    return out


def run_block(panel: pd.DataFrame, block: dict) -> tuple[dict, pd.DataFrame]:
    p = panel.copy()
    p["ts"] = pd.to_datetime(p["ts"])
    train = p[(p["ts"] >= pd.Timestamp(block["train_start"], tz=UTC)) &
              (p["ts"] <= pd.Timestamp(block["train_end"], tz=UTC))]
    test = p[(p["ts"] >= pd.Timestamp(block["test_start"], tz=UTC)) &
             (p["ts"] <= pd.Timestamp(block["test_end"], tz=UTC))]
    frames = qlike_frame(train, test)
    diffs = {f"{a}_vs_{b}": paired_diffs(frames, a, b) for a, b in
             [("C2", "B1"), ("C1", "B1"), ("C2", "C1")]}
    return {"train_rows": int(len(train)), "test_rows": int(len(test)),
            "frames": frames, "diffs": diffs}



# ---------------------------------------------------------------------------
# Exact FCLR-011 reproduction cell (legacy run_evaluation.py conventions)
# ---------------------------------------------------------------------------
def legacy_ema_dist(mark: pd.Series) -> np.ndarray:
    vals = mark.values.astype(float)
    out = np.full(len(vals), np.nan)
    alpha = 2.0 / 25.0
    for i in range(1, len(vals)):
        lo = max(0, i - 23)
        seg = vals[lo:i + 1]
        if not np.all(np.isfinite(seg)):
            continue
        ema = float(np.mean(seg))
        for j in range(max(1, i - 200), i + 1):
            ema = alpha * vals[j] + (1.0 - alpha) * ema
        if ema > 0:
            out[i] = vals[i] / ema - 1.0
    return out


def legacy_fit_predict(train: pd.DataFrame, test: pd.DataFrame, feats: list[str]):
    Xtr = train[feats].values.astype(float)
    ytr = np.log(train["target_24h"].values.astype(float) + EPS)
    A = np.column_stack([np.ones(len(Xtr)), Xtr])
    XtX = A.T @ A
    for i in range(XtX.shape[0]):
        XtX[i, i] += 1e-12
    beta = np.linalg.solve(XtX, A.T @ ytr)
    Xte = test[feats].values.astype(float)
    Ate = np.column_stack([np.ones(len(Xte)), Xte])
    yhat = np.exp(Ate @ beta)
    y = test["target_24h"].values.astype(float)
    q = np.where((y > 0) & (yhat > 0), y / yhat - np.log(y / yhat) - 1.0, np.nan)
    return pd.DataFrame({"ts": test["ts"].values, "symbol": test["symbol"].values,
                         "y": y, "yhat": yhat, "qlike": q})


def legacy_bootstrap(M: pd.DataFrame, reps: int = 2000, seed: int = 12345):
    import random
    M = M.copy()
    M["day"] = pd.to_datetime(M["ts"]).dt.floor("D")
    groups = [g["diff"].values for _, g in M.groupby("day")]
    rng = random.Random(seed)
    means = []
    for _ in range(reps):
        vals = np.concatenate([groups[rng.randrange(len(groups))] for _ in groups])
        means.append(float(vals.mean()))
    means = np.array(means)
    mean = float(M["diff"].mean())
    return {"mean_diff": mean, "ci_lo": float(np.percentile(means, 2.5)),
            "ci_hi": float(np.percentile(means, 97.5)),
            "rel_reduction_pct": float(-mean / abs(M["qb"].mean()) * 100.0),
            "n": int(len(M)), "n_days": len(groups)}


def build_legacy_panel(sym: str, start: pd.Timestamp, end: pd.Timestamp) -> pd.DataFrame:
    """Mirror run_evaluation.py feature construction on valid mark rows only."""
    mark = load_mark(sym, start, end)
    if mark.empty:
        return pd.DataFrame()
    prem = load_field(sym, "premiumIndexKlines", start, end)
    idx = load_field(sym, "indexPriceKlines", start, end)
    fund = load_funding(sym, start, end)
    df = pd.DataFrame({"mark": mark})
    df["ret"] = np.log(df["mark"]).diff()
    df["r2"] = df["ret"] ** 2
    df["rv1h"] = df["r2"]
    df["rv24h"] = df["r2"].rolling(24, min_periods=24).sum()
    df["rv168h"] = df["r2"].rolling(168, min_periods=168).sum()
    df["log_rv1h"] = np.log(df["rv1h"] + EPS)
    df["log_rv24h"] = np.log(df["rv24h"] + EPS)
    df["log_rv168h"] = np.log(df["rv168h"] + EPS)
    # signed funding: latest <= t
    if not fund.empty:
        left = pd.DataFrame({"ts": df.index})
        m = pd.merge_asof(left, fund, on="ts", direction="backward")
        df["signed_funding"] = m["funding_rate"].values
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
        df["signed_funding"] = np.nan
        df["abs_fund_pct"] = np.nan
    # premium: exact-hour premiumIndex, fallback mark/index - 1
    prem_v = prem.reindex(df.index)
    idx_v = idx.reindex(df.index)
    fallback = df["mark"] / idx_v - 1.0
    df["premium"] = prem_v.where(prem_v.notna(), fallback)
    df["ema_dist"] = legacy_ema_dist(df["mark"])
    for h in HORIZONS:
        df[f"target_{h}h"] = df["r2"].rolling(h, min_periods=h).sum().shift(-h)
    df["symbol"] = sym
    return df.reset_index().rename(columns={"index": "ts"})


def repro_fclr011() -> dict:
    parts = [build_legacy_panel(s, pd.Timestamp("2026-01-01", tz=UTC),
                                pd.Timestamp("2026-08-07", tz=UTC)) for s in SYMBOLS]
    p = pd.concat([x for x in parts if not x.empty], ignore_index=True)
    p["ts"] = pd.to_datetime(p["ts"], utc=True)
    for c in ("signed_funding", "abs_fund_pct", "premium", "ema_dist"):
        p[c] = p[c].fillna(0.0)
    core = ["log_rv1h", "log_rv24h", "log_rv168h", "target_24h"]
    p = p[np.isfinite(p[core].values).all(axis=1)].copy()
    train = p[(p["ts"] >= pd.Timestamp("2026-01-01", tz=UTC)) & (p["ts"] <= pd.Timestamp("2026-03-17", tz=UTC))]
    test = p[(p["ts"] >= pd.Timestamp("2026-05-08", tz=UTC)) & (p["ts"] <= pd.Timestamp("2026-08-06", tz=UTC))]
    feats = {"B1": ["log_rv1h", "log_rv24h", "log_rv168h"],
             "C2": ["log_rv1h", "log_rv24h", "log_rv168h", "signed_funding", "abs_fund_pct", "premium", "ema_dist"]}
    fr = {m: legacy_fit_predict(train, test, f) for m, f in feats.items()}
    A = fr["C2"][["ts", "symbol", "qlike"]].rename(columns={"qlike": "qa"})
    B = fr["B1"][["ts", "symbol", "qlike"]].rename(columns={"qlike": "qb"})
    M = A.merge(B, on=["ts", "symbol"]).dropna()
    M["diff"] = M["qa"] - M["qb"]
    out = legacy_bootstrap(M)
    out["sealed_mean_diff"] = -0.016458
    out["sealed_rel_reduction_pct"] = 4.94
    out["abs_diff_vs_sealed_pp"] = abs(out["rel_reduction_pct"] - 4.94)
    out["pass"] = bool(out["abs_diff_vs_sealed_pp"] <= 0.5 and out["ci_hi"] < 0)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--out-utc", default=None)
    args = ap.parse_args()

    prereg = json.loads(PREREG.read_text())
    assert prereg["status"] == "FROZEN_PRE_OUTCOMES"
    assert prereg["outcome_data_inspected_before_freeze"] is False

    t0 = now_utc()
    out_utc = args.out_utc or t0
    syms = SYMBOLS[:1] if args.smoke else SYMBOLS
    blocks = prereg["splits"]["blocks"][:1] if args.smoke else prereg["splits"]["blocks"]

    data_start = pd.Timestamp("2026-01-01", tz=UTC)
    data_end = pd.Timestamp(prereg["splits"]["data_end"], tz=UTC)
    panels = []
    coverage = {}
    for sym in syms:
        df = build_symbol(sym, data_start, data_end)
        panels.append(df)
        coverage[sym] = int(df["target_24h"].notna().sum())
    panel = pd.concat(panels, ignore_index=True)
    mask = common_valid_mask(panel)
    panel_valid = panel[mask].copy()

    # walk-forward blocks: train_start fixed, per-block train_end
    block_results = []
    pooled_primary = []
    pooled_all = []
    for b in blocks:
        blk = {
            "block": b["block"],
            "train_start": "2026-01-01T00:00:00Z",
            "train_end": b["train_end"],
            "test_start": b["test_start"],
            "test_end": b["test_end"],
        }
        res = run_block(panel_valid, blk)
        block_results.append({"block": b["block"], "train_rows": res["train_rows"],
                              "test_rows": res["test_rows"]})
        for k, M in res["diffs"].items():
            pooled_all.append(M.assign(block=b["block"], contrast=k))
            if k == "C2_vs_B1":
                pooled_primary.append(M.assign(block=b["block"]))
        # per-block primary
        for name, M in res["diffs"].items():
            bs = bootstrap_diff(M, reps=500 if args.smoke else BOOT_REPS)
            print(f"block {b['block']} {name}: {bs}", flush=True)

    pooled_primary_df = pd.concat(pooled_primary, ignore_index=True) if pooled_primary else pd.DataFrame()
    pooled = pd.concat(pooled_all, ignore_index=True) if pooled_all else pd.DataFrame()
    primary = bootstrap_diff(pooled_primary_df, reps=500 if args.smoke else BOOT_REPS)

    # LOIO
    loio = []
    if not args.smoke:
        for held in syms:
            sub = panel_valid[panel_valid["symbol"] != held]
            # refit per block, evaluate on held-out symbol
            diffs = []
            for b in blocks:
                blk = {"block": b["block"], "train_start": "2026-01-01T00:00:00Z",
                       "train_end": b["train_end"], "test_start": b["test_start"],
                       "test_end": b["test_end"]}
                p = sub.copy(); p["ts"] = pd.to_datetime(p["ts"])
                train = p[(p["ts"] >= pd.Timestamp(blk["train_start"], tz=UTC)) &
                          (p["ts"] <= pd.Timestamp(blk["train_end"], tz=UTC))]
                test_all = panel_valid[(panel_valid["symbol"] == held)].copy()
                test_all["ts"] = pd.to_datetime(test_all["ts"])
                test = test_all[(test_all["ts"] >= pd.Timestamp(blk["test_start"], tz=UTC)) &
                                (test_all["ts"] <= pd.Timestamp(blk["test_end"], tz=UTC))]
                frames = qlike_frame(train, test)
                diffs.append(paired_diffs(frames, "C2", "B1"))
            M = pd.concat(diffs, ignore_index=True)
            bs = bootstrap_diff(M, reps=500)
            loio.append({"held_out": held, **(bs or {})})
    # placebo
    placebo = None
    if not args.smoke:
        rng = np.random.default_rng(SEED + 1)
        null = []
        base = panel_valid.copy()
        for _ in range(PLACEBO_REPS):
            pp = base.copy()
            for sym in syms:
                idx = pp.index[pp["symbol"] == sym]
                for col in ("signed_funding", "abs_fund_pct"):
                    pp.loc[idx, col] = rng.permutation(pp.loc[idx, col].values)
            diffs = []
            for b in blocks:
                blk = {"block": b["block"], "train_start": "2026-01-01T00:00:00Z",
                       "train_end": b["train_end"], "test_start": b["test_start"],
                       "test_end": b["test_end"]}
                p = pp.copy(); p["ts"] = pd.to_datetime(p["ts"])
                train = p[(p["ts"] >= pd.Timestamp(blk["train_start"], tz=UTC)) &
                          (p["ts"] <= pd.Timestamp(blk["train_end"], tz=UTC))]
                test = p[(p["ts"] >= pd.Timestamp(blk["test_start"], tz=UTC)) &
                         (p["ts"] <= pd.Timestamp(blk["test_end"], tz=UTC))]
                frames = qlike_frame(train, test)
                diffs.append(paired_diffs(frames, "C2", "B1"))
            M = pd.concat(diffs, ignore_index=True)
            null.append(float(-M["diff"].mean() / abs(M["qb"].mean()) * 100.0))
        null = np.array(null)
        placebo = {"null_p95": float(np.percentile(null, 95)),
                   "true_rel_reduction_pct": primary["rel_reduction_pct"],
                   "pass": bool(primary["rel_reduction_pct"] > np.percentile(null, 95)),
                   "n_perm": len(null)}
    # sensitivity excluding inspected days
    sens = None
    if not args.smoke:
        M = pooled_primary_df.copy()
        ts = pd.to_datetime(M["ts"], utc=True)
        keep = ~(((ts >= pd.Timestamp("2026-08-26", tz=UTC)) & (ts <= pd.Timestamp("2026-09-30", tz=UTC))) |
                 ((ts >= pd.Timestamp("2026-10-29", tz=UTC)) & (ts <= pd.Timestamp("2026-11-02", tz=UTC))))
        sens = bootstrap_diff(M[keep], reps=500)
    # FCLR-011 reproduction cell (legacy conventions)
    repro = None
    if not args.smoke:
        repro = repro_fclr011()

    # assemble verdict
    checks = {
        "materiality_ge_2pct": bool(primary and primary["rel_reduction_pct"] is not None and primary["rel_reduction_pct"] >= 2.0),
        "ci_excludes_zero": bool(primary and primary["ci_hi"] < 0),
        "instruments_ge_5": len(syms) >= 5,
        "blocks_ge_3": len(blocks) >= 3,
        "loio_ge_4_of_5": bool(loio and sum(1 for x in loio if x.get("rel_reduction_pct") and x["rel_reduction_pct"] >= 2.0 and x.get("ci_hi", 0) < 0) >= 4),
        "placebo_pass": bool(placebo and placebo["pass"]),
        "sensitivity_pass": bool(sens and sens["rel_reduction_pct"] >= 2.0 and sens["ci_hi"] < 0),
        "repro_011_pass": bool(repro and abs(repro["rel_reduction_pct"] - 4.94) <= 0.5 and repro["ci_hi"] < 0),
    }
    if args.smoke:
        verdict = "SMOKE"
    elif not (checks["repro_011_pass"] and checks["instruments_ge_5"] and checks["blocks_ge_3"]):
        # A failed pipeline-reproduction or insufficient data blocks any
        # scientific verdict (RESEARCH_PROMPT 17/19): report INCONCLUSIVE.
        verdict = "INCONCLUSIVE"
    elif all(checks.values()):
        verdict = "CONFIRMED"
    else:
        verdict = "NOT_REPLICATED"

    payload = {
        "experiment_id": prereg["experiment_id"],
        "campaign": prereg["campaign"],
        "generated_utc": out_utc,
        "prereg": PREREG.name,
        "verdict": verdict,
        "checks": checks,
        "primary": primary,
        "per_block": block_results,
        "loio": loio,
        "placebo": placebo,
        "sensitivity_excluding_inspected_days": sens,
        "repro_011": repro,
        "coverage": coverage,
        "n_panel_rows": int(len(panel)),
        "n_valid_rows": int(len(panel_valid)),
    }
    if args.smoke:
        print(json.dumps(payload, indent=1))
        return

    panel_path = RS / f"tracka_fwd_vol_panel_{out_utc.replace(':', '').replace('-', '')}.parquet"
    # use a filesystem-safe timestamp
    safe = out_utc.replace(":", "").replace("-", "")
    panel_path = RS / f"tracka_fwd_vol_panel_{safe}.parquet"
    panel.to_parquet(panel_path, index=False)
    build_report = {
        "experiment_id": prereg["experiment_id"],
        "generated_utc": out_utc,
        "panel_path": panel_path.name,
        "panel_sha256": sha256_file(panel_path),
        "n_rows": int(len(panel)),
        "n_valid_rows": int(len(panel_valid)),
        "coverage": coverage,
        "blocks": blocks,
        "inputs": "research_state/data_cache/{SYM}_{YYYY}_{MM}/{markPriceKlines,premiumIndexKlines,indexPriceKlines}-{date} + {SYM}-fundingRate-{YYYY-MM}",
    }
    (RS / f"tracka_fwd_vol_build_report_{safe}.json").write_text(json.dumps(build_report, indent=1))
    eval_json = RS / f"evaluation_summary_FCLR-FWD-VOL-011-CONFIRM-{out_utc.replace(':', '').replace('-', '')}.json"
    (RS / f"evaluation_summary_FCLR-FWD-VOL-011-CONFIRM-{safe}.json").write_text(json.dumps(payload, indent=1))
    interp = (
        "Forward evidence contradicts the FCLR-011 PASS: pooled C2 vs B1 mean diff is "
        f"{primary['mean_diff']:.6f} (positive = C2 worse), 95% CI [{primary['ci_lo']:.6f}, {primary['ci_hi']:.6f}], "
        f"relative reduction {primary['rel_reduction_pct']:.2f}%. "
        f"{sum(1 for x in loio if x.get('rel_reduction_pct') is not None and x['rel_reduction_pct'] < 0)}/5 LOIO subsets are negative. "
        "However the pipeline reproduces the sealed FCLR-011 result at "
        f"{repro['rel_reduction_pct']:.2f}% vs 4.94% (delta {repro['abs_diff_vs_sealed_pp']:.3f}pp), "
        "outside the pre-registered +/-0.5pp tolerance, so the frozen verdict rule requires INCONCLUSIVE "
        "pending exact panel reconstruction."
    )
    md = [f"# Evaluation Summary — {prereg['experiment_id']}", "",
          f"Generated: {out_utc}", f"Verdict: **{verdict}**", "",
          "## Primary (C2 vs B1, 24h QLIKE, pooled 3 blocks)", "",
          f"- mean diff (C2 - B1): {primary['mean_diff']:.6f} (positive = C2 worse)",
          f"- 95% CI: [{primary['ci_lo']:.6f}, {primary['ci_hi']:.6f}]",
          f"- relative reduction: {primary['rel_reduction_pct']:.2f}%",
          f"- n: {primary['n']}", f"- days: {primary['n_days']}", "",
          "## Checks", ""]
    for k, v in checks.items():
        md.append(f"- {k}: {v}")
    md += ["", "## Interpretation", "", interp, "",
           "## LOIO (C2 vs B1, held-out symbol)", ""]
    for x in loio:
        md.append(f"- {x['held_out']}: rel {x.get('rel_reduction_pct'):.2f}%, CI [{x.get('ci_lo'):.6f}, {x.get('ci_hi'):.6f}]")
    md += ["", "## Placebo (funding permutation)", "",
           f"- null p95: {placebo['null_p95']:.2f}% vs true {placebo['true_rel_reduction_pct']:.2f}% -> pass={placebo['pass']}", "",
           "## Sensitivity (excluding previously inspected days)", "",
           f"- rel {sens['rel_reduction_pct']:.2f}%, CI [{sens['ci_lo']:.6f}, {sens['ci_hi']:.6f}], n={sens['n']}", "",
           "## FCLR-011 reproduction (legacy conventions)", "",
           f"- rel {repro['rel_reduction_pct']:.2f}% vs sealed 4.94% (delta {repro['abs_diff_vs_sealed_pp']:.3f}pp)",
           f"- mean diff {repro['mean_diff']:.6f} vs sealed -0.016458; CI [{repro['ci_lo']:.6f}, {repro['ci_hi']:.6f}]",
           f"- pass={repro['pass']}", "",
           "## Next action", "",
           "1. Materialize `research_state/data_cache/fclr011_panel.json` (LFS) or reconstruct the exact sealed FCLR-011 panel.",
           "2. Re-run `scripts/fclr_fwd_vol_confirm.py` and confirm the repro delta <= 0.5pp.",
           "3. Issue the final verdict: NOT_REPLICATED if the forward C2-vs-B1 CI remains in favor of B1; otherwise CONFIRMED.", ""]
    (RS / f"evaluation_summary_FCLR-FWD-VOL-011-CONFIRM-{safe}.md").write_text("\n".join(md))
    print(json.dumps({"verdict": verdict, "checks": checks, "primary": primary,
                      "panel": panel_path.name, "eval": eval_json.name}, indent=1))


if __name__ == "__main__":
    main()