#!/usr/bin/env python3
"""Debug the funding ablation pipeline."""
from __future__ import annotations

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
EPS = 1e-12

symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT"]
start = "2024-01-01"
end = "2024-03-31"
horizon = 24

# ensure extracted
RAW.mkdir(parents=True, exist_ok=True)
for zp in loader.discover_zips(ZIPS_DIR):
    if not any(s in zp.name for s in symbols):
        continue
    try:
        loader.extract_zip(zp, RAW)
    except Exception:
        continue

# load klines
frames = []
for sym in symbols:
    klist = []
    for kf in sorted(RAW.glob(f"{sym}-1h-*.csv")):
        try:
            klist.append(loader.load_klines(kf))
        except Exception:
            continue
    if not klist:
        print("NO KLINE", sym)
        continue
    kdf = pd.concat(klist).sort_index()
    kdf = kdf.loc[(kdf.index >= pd.Timestamp(start, tz="UTC")) & (kdf.index <= pd.Timestamp(end, tz="UTC") + pd.Timedelta(days=1))]
    kdf = vf.add_rv_features(kdf, short_windows=[6, 24], long_windows=[168])
    kdf["target_rv"] = vf.forward_rv(kdf["close"], horizon=horizon)
    kdf["rv_lag"] = kdf["rv_trail_24"].shift(1)
    kdf = kdf.reset_index().rename(columns={"open_time": "timestamp"})
    kdf["symbol"] = sym
    frames.append(kdf)
    print(sym, "rows", len(kdf), "target non-null", kdf["target_rv"].notna().sum(),
          "rv24 non-null", kdf["rv_trail_24"].notna().sum(),
          "target min/max", kdf["target_rv"].min(), kdf["target_rv"].max())
panel = pd.concat(frames, ignore_index=True)
panel["timestamp"] = pd.to_datetime(panel["timestamp"], utc=True)
panel = panel.set_index(["symbol", "timestamp"]).sort_index()
print("panel shape", panel.shape)
print("target describe\n", panel["target_rv"].describe())
print("rv_trail_24 describe\n", panel["rv_trail_24"].describe())

# funding
fframes = []
for sym in symbols:
    flist = []
    for fp in sorted(RAW.glob(f"{sym}-fundingRate-*.csv")):
        try:
            flist.append(loader.load_funding(fp))
        except Exception:
            continue
    if not flist:
        print("NO FUNDING", sym)
        continue
    fdf = pd.concat(flist).sort_index()
    fdf = fdf.loc[(fdf.index >= pd.Timestamp(start, tz="UTC")) & (fdf.index <= pd.Timestamp(end, tz="UTC") + pd.Timedelta(days=1))]
    fdf = fdf.reset_index().rename(columns={"calc_time": "timestamp"})
    fdf["symbol"] = sym
    fframes.append(fdf)
    print(sym, "funding rows", len(fdf), "last_funding_rate non-null", fdf["last_funding_rate"].notna().sum())
fpanel = pd.concat(fframes, ignore_index=True)
fpanel["timestamp"] = pd.to_datetime(fpanel["timestamp"], utc=True)
fpanel = fpanel.set_index(["symbol", "timestamp"]).sort_index()

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
feats = pd.concat(feat_frames, axis=1)
new_cols = [c for c in feats.columns if c not in out.columns]
merged = out.join(feats[new_cols], how="left")
print("merged shape", merged.shape)
print("funding_signed non-null", merged["funding_signed"].notna().sum())
print("funding_abs non-null", merged["funding_abs"].notna().sum())
for c in ["funding_pct_24", "funding_pct_72", "funding_pct_168", "funding_z_24", "funding_z_72", "funding_z_168"]:
    if c in merged.columns:
        print(c, "non-null", merged[c].notna().sum(), "min", merged[c].min(), "max", merged[c].max())

# split
sp = wf.SplitBounds(
    train=("2024-01-01T00:00:00+00:00", "2024-02-01T00:00:00+00:00"),
    validation=("2024-02-09T00:00:00+00:00", "2024-02-15T00:00:00+00:00"),
    test=("2024-02-22T00:00:00+00:00", "2024-03-31T00:00:00+00:00"),
    purge_days=7, embargo_days=7,
)
idx = merged.index.get_level_values("timestamp")
train = merged.loc[wf._in_window(idx, sp.train)]
test = merged.loc[wf._in_window(idx, sp.test)]
print("train rows", len(train), "test rows", len(test))
base = [c for c in ["rv_trail_24", "rv_trail_168", "rv_trail_6"] if c in merged.columns]
print("base cols", base)

# A: rv only
fcols = base[:]
train_n, val_n, test_n, _ = wf.apply_train_only_normalization(train, test, test, fcols)
print("train_n target describe\n", train_n["target_rv"].describe())
print("test_n target describe\n", test_n["target_rv"].describe())

# fit HAR OLS on train
from src.models.baselines import RVOnlyHAR
m = RVOnlyHAR(feature_cols=fcols)
m.fit(train_n[fcols], train_n["target_rv"])
p = m.predict(test_n[fcols])
print("preds sample", p[:5])
print("preds min/max", np.nanmin(p), np.nanmax(p), "n nan", np.isnan(p).sum())
y = test_n["target_rv"].to_numpy(dtype=float)
from src.volatility import eval as veval
print("A qlike", veval.qlike(y.tolist(), p.tolist()))
print("A mae", veval.mae(y.tolist(), p.tolist()))