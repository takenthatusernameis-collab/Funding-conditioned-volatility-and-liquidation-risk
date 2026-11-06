#!/usr/bin/env python3
"""Debug: inspect panel + predictions for funding ablation (per-symbol correct)."""
import numpy as np
import pandas as pd
from pathlib import Path

from src.ingest import loader
from src.features import volatility as vf
from src.features import funding as ff
from src.eval import walkforward as wf

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
    lo = pd.Timestamp(start, tz="UTC")
    hi = pd.Timestamp(end, tz="UTC") + pd.Timedelta(days=1)
    kdf = kdf.loc[(kdf.index >= lo) & (kdf.index <= hi)]
    kdf = vf.add_rv_features(kdf, short_windows=[6, 24], long_windows=[168])
    kdf["target_rv"] = vf.forward_rv(kdf["close"], horizon=24)
    kdf["rv_lag"] = kdf["rv_trail_24"].shift(1)
    kdf = kdf.reset_index().rename(columns={"open_time": "timestamp"})
    kdf["symbol"] = sym
    frames.append(kdf)
kpanel = pd.concat(frames, ignore_index=True)
kpanel["timestamp"] = pd.to_datetime(kpanel["timestamp"], utc=True)
kpanel = kpanel.set_index(["symbol", "timestamp"]).sort_index()

# Per-symbol funding panel
fpanel_frames = []
for sym in symbols:
    flist = []
    for fp in sorted(RAW.glob(f"{sym}-fundingRate-*.csv")):
        try:
            flist.append(loader.load_funding(fp))
        except Exception:
            continue
    if not flist:
        continue
    fdf = pd.concat(flist).sort_index()
    lo = pd.Timestamp(start, tz="UTC")
    hi = pd.Timestamp(end, tz="UTC") + pd.Timedelta(days=1)
    fdf = fdf.loc[(fdf.index >= lo) & (fdf.index <= hi)]
    fdf = fdf.reset_index().rename(columns={"calc_time": "timestamp"})
    fdf["symbol"] = sym
    fpanel_frames.append(fdf)
fpanel = pd.concat(fpanel_frames, ignore_index=True)
fpanel["timestamp"] = pd.to_datetime(fpanel["timestamp"], utc=True)
fpanel = fpanel.set_index(["symbol", "timestamp"]).sort_index()

print("=== kpanel target_rv stats ===")
t = kpanel["target_rv"]
print("n:", len(t), "min:", t.min(), "max:", t.max(), "nan:", t.isna().sum(), "inf:", np.isinf(t).sum())
print("target_rv describe:", t.describe().to_dict())

print("\n=== close stats ===")
print(kpanel["close"].describe().to_dict())
print("close zeros:", (kpanel["close"] <= 0).sum())

print("\n=== funding panel ===")
print(fpanel[["last_funding_rate"]].describe().to_dict())
print("funding nan:", fpanel["last_funding_rate"].isna().sum(), "of", len(fpanel))
print("funding dup index:", fpanel.index.duplicated().sum())

sym = "BTCUSDT"
kidx = kpanel.xs(sym, level="symbol").index
ffeat = ff.add_funding_features(kidx, fpanel.xs(sym, level="symbol"))
print("\n=== funding features (BTCUSDT) ===")
print(ffeat.describe().to_dict())
print("funding_signed nan:", ffeat["funding_signed"].isna().sum(), "of", len(ffeat))
print("funding_abs max:", ffeat["funding_abs"].max())
print("funding_pct_24 nan:", ffeat["funding_pct_24"].isna().sum())
print("funding_z_168 nan:", ffeat["funding_z_168"].isna().sum(), "max abs:", ffeat["funding_z_168"].abs().max())

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
print("\n=== split sizes ===", "train:", len(train), "test:", len(test))
train_n, val_n, test_n, _ = wf.apply_train_only_normalization(train, test, test, base)
ytr = train_n["target_rv"].to_numpy(dtype=float)
ytr_log = np.log(np.clip(ytr, EPS, None))
print("ytr_log: min", np.nanmin(ytr_log), "max", np.nanmax(ytr_log), "mean", np.nanmean(ytr_log))
Xtr = train_n[base].to_numpy(dtype=float)
print("Xtr: any inf?", np.isinf(Xtr).any(), "any nan?", np.isnan(Xtr).any())
mask = np.isfinite(ytr_log) & np.all(np.isfinite(Xtr), axis=1)
print("fit rows:", mask.sum(), "of", len(ytr_log))
Xc, yc = Xtr[mask], ytr_log[mask]
print("Xc mean:", Xc.mean(axis=0), "yc mean:", yc.mean())
n, k = Xc.shape
XtX = Xc.T @ Xc
lam = 1e-3
coef = np.linalg.solve(XtX + lam * np.eye(k), Xc.T @ yc)
intercept = float(yc.mean() - coef @ Xc.mean(axis=0))
print("coef:", coef, "intercept:", intercept)
Xte = test_n[base].to_numpy(dtype=float)
p_log = intercept + Xte @ coef
p = np.exp(p_log)
print("pred: min", np.nanmin(p), "max", np.nanmax(p), "mean", np.nanmean(p), "nan", np.isnan(p).sum())
y = test_n["target_rv"].to_numpy(dtype=float)
print("y test: min", np.nanmin(y), "max", np.nanmax(y))
m = np.isfinite(y) & np.isfinite(p) & (y > 0) & (p > 0)
print("valid pairs:", m.sum())
from src.volatility import eval as veval
print("qlike:", veval.qlike(y[m].tolist(), p[m].tolist()))