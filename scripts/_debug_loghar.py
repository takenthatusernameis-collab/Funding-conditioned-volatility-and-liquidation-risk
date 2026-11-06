#!/usr/bin/env python3
"""Test log-HAR: log target on log RV features vs raw OLS."""
import numpy as np
import pandas as pd
from pathlib import Path

from src.ingest import loader
from src.features import volatility as vf
from src.eval import walkforward as wf
from src.volatility import eval as veval

REPO = Path(__file__).resolve().parents[1]
RAW = REPO / "data" / "raw"
ZIPS_DIR = REPO
symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT"]
start, end = "2024-01-01", "2024-03-31"
EPS = 1e-12

for zp in loader.discover_zips(ZIPS_DIR):
    if not any(s in zp.name for s in symbols):
        continue
    try:
        loader.extract_zip(zp, RAW)
    except Exception:
        continue

frames = []
for sym in symbols:
    klist = []
    for kf in sorted(RAW.glob(f"{sym}-1h-*.csv")):
        try:
            klist.append(loader.load_klines(kf))
        except Exception:
            continue
    kdf = pd.concat(klist).sort_index()
    hi = pd.Timestamp(end, tz="UTC") + pd.Timedelta(days=1)
    kdf = kdf.loc[(kdf.index >= pd.Timestamp(start, tz="UTC")) & (kdf.index <= hi)]
    kdf = vf.add_rv_features(kdf, short_windows=[6, 24], long_windows=[168])
    kdf["target_rv"] = vf.forward_rv(kdf["close"], horizon=24)
    kdf["rv_lag"] = kdf["rv_trail_24"].shift(1)
    kdf = kdf.reset_index().rename(columns={"open_time": "timestamp"})
    kdf["symbol"] = sym
    frames.append(kdf)
kpanel = pd.concat(frames, ignore_index=True)
kpanel["timestamp"] = pd.to_datetime(kpanel["timestamp"], utc=True)
kpanel = kpanel.set_index(["symbol", "timestamp"]).sort_index()

# log-HAR features
for c in ["rv_trail_6", "rv_trail_24", "rv_trail_168"]:
    kpanel[f"log_{c}"] = np.log(kpanel[c].clip(lower=EPS))
kpanel["log_target"] = np.log(kpanel["target_rv"].clip(lower=EPS))

log_base = ["log_rv_trail_24", "log_rv_trail_168", "log_rv_trail_6"]
raw_base = ["rv_trail_24", "rv_trail_168", "rv_trail_6"]

sp = wf.SplitBounds(
    train=("2024-01-01T00:00:00+00:00", "2024-02-01T00:00:00+00:00"),
    validation=("2024-02-09T00:00:00+00:00", "2024-02-15T00:00:00+00:00"),
    test=("2024-02-22T00:00:00+00:00", "2024-03-31T00:00:00+00:00"),
    purge_days=7, embargo_days=7,
)
idx = kpanel.index.get_level_values("timestamp")
train = kpanel.loc[wf._in_window(idx, sp.train)]
test = kpanel.loc[wf._in_window(idx, sp.test)]

def ols_fit(X, y):
    mask = np.isfinite(y) & np.all(np.isfinite(X), axis=1)
    Xc, yc = X[mask], y[mask]
    n, k = Xc.shape
    XtX = Xc.T @ Xc
    coef = np.linalg.solve(XtX + 1e-10*np.eye(k), Xc.T @ yc)
    intercept = float(yc.mean() - coef @ Xc.mean(axis=0))
    return coef, intercept

def run(name, fcols, log_target):
    train_n, val_n, test_n, _ = wf.apply_train_only_normalization(train, test, test, fcols)
    preds = np.full(len(test_n), np.nan)
    for sym, grp in test_n.groupby(level="symbol", sort=False):
        tr = train_n.loc[train_n.index.get_level_values("symbol") == sym]
        if log_target:
            ytr = tr["log_target"].to_numpy(dtype=float)
        else:
            ytr = tr["target_rv"].to_numpy(dtype=float)
        Xtr = tr[fcols].to_numpy(dtype=float)
        coef, intercept = ols_fit(Xtr, ytr)
        Xte = grp[fcols].to_numpy(dtype=float)
        p = intercept + Xte @ coef
        if log_target:
            p = np.exp(p)
        preds[test_n.index.get_indexer(grp.index)] = p
    y = test_n["target_rv"].to_numpy(dtype=float)
    m = np.isfinite(y) & np.isfinite(preds) & (y > 0) & (preds > 0)
    q = veval.qlike(y[m].tolist(), preds[m].tolist())
    print(f"{name}: qlike={q:.4f} valid={m.sum()} pred_mean={np.nanmean(preds):.6f} pred_max={np.nanmax(preds):.4f}")

run("raw OLS HAR (baseline)", raw_base, False)
run("log-HAR (log feats, log target)", log_base, True)
run("log-HAR raw feats, log target (BAD)", raw_base, True)