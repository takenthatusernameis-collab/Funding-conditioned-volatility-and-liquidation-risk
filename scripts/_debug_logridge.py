#!/usr/bin/env python3
"""Debug the log-ridge HAR predictions vs OLS HAR."""
import numpy as np
import pandas as pd
from pathlib import Path

from src.ingest import loader
from src.features import volatility as vf
from src.features import funding as ff
from src.eval import walkforward as wf
from src.models.baselines import RVOnlyHAR

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

base = ["rv_trail_24", "rv_trail_168", "rv_trail_6"]
sp = wf.SplitBounds(
    train=("2024-01-01T00:00:00+00:00", "2024-02-01T00:00:00+00:00"),
    validation=("2024-02-09T00:00:00+00:00", "2024-02-15T00:00:00+00:00"),
    test=("2024-02-22T00:00:00+00:00", "2024-03-31T00:00:00+00:00"),
    purge_days=7, embargo_days=7,
)
idx = kpanel.index.get_level_values("timestamp")
train = kpanel.loc[wf._in_window(idx, sp.train)]
test = kpanel.loc[wf._in_window(idx, sp.test)]
train_n, val_n, test_n, _ = wf.apply_train_only_normalization(train, test, test, base)

# OLS HAR (raw target) - the baseline approach
preds_ols = np.full(len(test_n), np.nan)
for sym, grp in test_n.groupby(level="symbol", sort=False):
    tr = train_n.loc[train_n.index.get_level_values("symbol") == sym]
    m = RVOnlyHAR(feature_cols=base)
    m.fit(tr[base], tr["target_rv"])
    preds_ols[test_n.index.get_indexer(grp.index)] = m.predict(grp[base])
y = test_n["target_rv"].to_numpy(dtype=float)
from src.volatility import eval as veval
m_ols = np.isfinite(y) & np.isfinite(preds_ols) & (y > 0) & (preds_ols > 0)
print("=== OLS HAR (raw target) ===")
print("pred min/max/mean:", np.nanmin(preds_ols), np.nanmax(preds_ols), np.nanmean(preds_ols))
print("y min/max/mean:", np.nanmin(y), np.nanmax(y), np.nanmean(y))
print("qlike:", veval.qlike(y[m_ols].tolist(), preds_ols[m_ols].tolist()), "valid:", m_ols.sum())

# log-ridge HAR
def ridge_fit(X, y, lam):
    mask = np.isfinite(y) & np.all(np.isfinite(X), axis=1)
    Xc, yc = X[mask], y[mask]
    if len(yc) < 2:
        return np.zeros(X.shape[1]), float(np.nanmean(yc)) if np.isfinite(yc).any() else 0.0
    n, k = Xc.shape
    XtX = Xc.T @ Xc
    try:
        coef = np.linalg.solve(XtX + lam * np.eye(k), Xc.T @ yc)
    except np.linalg.LinAlgError:
        coef = np.zeros(k)
    intercept = float(yc.mean() - coef @ Xc.mean(axis=0))
    return coef, intercept

preds_log = np.full(len(test_n), np.nan)
for sym, grp in test_n.groupby(level="symbol", sort=False):
    tr = train_n.loc[train_n.index.get_level_values("symbol") == sym]
    ytr = tr["target_rv"].to_numpy(dtype=float)
    ytr_log = np.log(np.clip(ytr, EPS, None))
    Xtr = tr[base].to_numpy(dtype=float)
    coef, intercept = ridge_fit(Xtr, ytr_log, 1e-3)
    print(f"sym={sym}: coef={coef}, intercept={intercept}, ytr_log mean={np.nanmean(ytr_log):.3f}, std={np.nanstd(ytr_log):.3f}")
    print(f"  Xtr mean={Xtr.mean(axis=0)}, std={Xtr.std(axis=0)}")
    mask = np.isfinite(ytr_log) & np.all(np.isfinite(Xtr), axis=1)
    Xc, yc = Xtr[mask], ytr_log[mask]
    XtX = Xc.T @ Xc
    print(f"  XtX diag={np.diag(XtX)}, cond={np.linalg.cond(XtX):.2e}")
    Xte = grp[base].to_numpy(dtype=float)
    p_log = intercept + Xte @ coef
    preds_log[test_n.index.get_indexer(grp.index)] = np.exp(p_log)
m_log = np.isfinite(y) & np.isfinite(preds_log) & (y > 0) & (preds_log > 0)
print("\n=== log-ridge HAR (lam=1e-3) ===")
print("pred min/max/mean:", np.nanmin(preds_log), np.nanmax(preds_log), np.nanmean(preds_log))
print("qlike:", veval.qlike(y[m_log].tolist(), preds_log[m_log].tolist()), "valid:", m_log.sum())

# Try log-ridge with stronger regularization
for lam in [1e-1, 1e0, 1e1, 1e2]:
    preds_l = np.full(len(test_n), np.nan)
    for sym, grp in test_n.groupby(level="symbol", sort=False):
        tr = train_n.loc[train_n.index.get_level_values("symbol") == sym]
        ytr = tr["target_rv"].to_numpy(dtype=float)
        ytr_log = np.log(np.clip(ytr, EPS, None))
        Xtr = tr[base].to_numpy(dtype=float)
        coef, intercept = ridge_fit(Xtr, ytr_log, lam)
        Xte = grp[base].to_numpy(dtype=float)
        p_log = intercept + Xte @ coef
        preds_l[test_n.index.get_indexer(grp.index)] = np.exp(p_log)
    mm = np.isfinite(y) & np.isfinite(preds_l) & (y > 0) & (preds_l > 0)
    print(f"lam={lam}: pred mean={np.nanmean(preds_l):.6f} qlike={veval.qlike(y[mm].tolist(), preds_l[mm].tolist())}")