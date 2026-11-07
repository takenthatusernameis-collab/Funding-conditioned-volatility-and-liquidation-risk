#!/usr/bin/env python3
"""Debug the funding ablation pipeline: inspect target/feature magnitudes."""
from __future__ import annotations
import numpy as np
import pandas as pd
from pathlib import Path
from src.ingest import loader
from src.features import volatility as vf
from src.features import funding as ff

REPO = Path(__file__).resolve().parents[1]
RAW = REPO / "data" / "raw"
ZIPS_DIR = REPO
symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT"]
start = "2024-01-01"
end = "2024-03-31"
horizon = 24

RAW.mkdir(parents=True, exist_ok=True)
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
    if not klist:
        continue
    kdf = pd.concat(klist).sort_index()
    kdf = kdf.loc[(kdf.index >= pd.Timestamp(start, tz="UTC")) & (kdf.index <= pd.Timestamp(end, tz="UTC") + pd.Timedelta(days=1))]
    kdf = vf.add_rv_features(kdf, short_windows=[6, 24], long_windows=[168])
    kdf["target_rv"] = vf.forward_rv(kdf["close"], horizon=horizon)
    kdf["rv_lag"] = kdf["rv_trail_24"].shift(1)
    kdf = kdf.reset_index().rename(columns={"open_time": "timestamp"})
    kdf["symbol"] = sym
    frames.append(kdf)
panel = pd.concat(frames, ignore_index=True)
panel["timestamp"] = pd.to_datetime(panel["timestamp"], utc=True)
panel = panel.set_index(["symbol", "timestamp"]).sort_index()

print("=== panel shape ===", panel.shape)
print("columns:", list(panel.columns))
print("\n=== target_rv describe ===")
print(panel["target_rv"].describe())
print("target_rv NaN frac:", panel["target_rv"].isna().mean())
print("target_rv > 1:", (panel["target_rv"] > 1).sum(), "of", panel["target_rv"].notna().sum())
print("target_rv max:", panel["target_rv"].max())

print("\n=== rv_trail_24 describe ===")
print(panel["rv_trail_24"].describe())
print("NaN frac:", panel["rv_trail_24"].isna().mean())

# funding
flist = []
for sym in symbols:
    for fp in sorted(RAW.glob(f"{sym}-fundingRate-*.csv")):
        try:
            flist.append(loader.load_funding(fp))
        except Exception:
            continue
fdf = pd.concat(flist).sort_index()
fdf = fdf.loc[(fdf.index >= pd.Timestamp(start, tz="UTC")) & (fdf.index <= pd.Timestamp(end, tz="UTC") + pd.Timedelta(days=1))]
fdf = fdf.reset_index().rename(columns={"calc_time": "timestamp"})
fdf["symbol"] = sym  # careful: sym loop var leaks; redo properly below

# rebuild funding panel properly
frames_f = []
for sym in symbols:
    fl = []
    for fp in sorted(RAW.glob(f"{sym}-fundingRate-*.csv")):
        try:
            fl.append(loader.load_funding(fp))
        except Exception:
            continue
    if not fl:
        continue
    fdf = pd.concat(fl).sort_index()
    fdf = fdf.loc[(fdf.index >= pd.Timestamp(start, tz="UTC")) & (fdf.index <= pd.Timestamp(end, tz="UTC") + pd.Timedelta(days=1))]
    fdf = fdf.reset_index().rename(columns={"calc_time": "timestamp"})
    fdf["symbol"] = sym
    frames_f.append(fdf)
fpanel = pd.concat(frames_f, ignore_index=True)
fpanel["timestamp"] = pd.to_datetime(fpanel["timestamp"], utc=True)
fpanel = fpanel.set_index(["symbol", "timestamp"]).sort_index()
print("\n=== funding panel ===")
print(fpanel["last_funding_rate"].describe())
print("funding NaN:", fpanel["last_funding_rate"].isna().sum(), "of", len(fpanel))

# merge
out = panel.copy()
feat_frames = []
for sym in out.index.get_level_values("symbol").unique():
    kidx = out.xs(sym, level="symbol").index
    try:
        fdf = fpanel.xs(sym, level="symbol")
    except KeyError:
        continue
    ffeat = ff.add_funding_features(kidx, fdf)
    ffeat = ffeat.reset_index()
    ffeat["symbol"] = sym
    ffeat = ffeat.set_index(["symbol", "timestamp"]).sort_index()
    feat_frames.append(ffeat)
feats = pd.concat(feat_frames, axis=0)
feats = feats[~feats.index.duplicated(keep="last")].sort_index()
new_cols = [c for c in feats.columns if c not in out.columns]
merged = out.join(feats[new_cols], how="left")
print("\n=== merged funding feature NaN fracs ===")
for c in ["funding_signed", "funding_abs", "funding_pct_24", "funding_z_24"]:
    if c in merged.columns:
        print(c, "NaN:", merged[c].isna().mean(), "min:", merged[c].min(), "max:", merged[c].max())

print("\n=== training window sample (2024-01-01..2024-02-01) ===")
tr = merged.loc[(merged.index.get_level_values("timestamp") >= pd.Timestamp("2024-01-01", tz="UTC")) & (merged.index.get_level_values("timestamp") < pd.Timestamp("2024-02-01", tz="UTC"))]
print("train rows:", len(tr))
print("target_rv describe (train):")
print(tr["target_rv"].describe())
print("rv_trail_24 describe (train):")
print(tr["rv_trail_24"].describe())
print("funding_signed describe (train):")
print(tr["funding_signed"].describe())
print("funding_abs describe (train):")
print(tr["funding_abs"].describe())

# log target
ytr = np.log(np.clip(tr["target_rv"].to_numpy(dtype=float), 1e-12, None))
print("\nlog(target) train: min", np.nanmin(ytr), "max", np.nanmax(ytr), "mean", np.nanmean(ytr))