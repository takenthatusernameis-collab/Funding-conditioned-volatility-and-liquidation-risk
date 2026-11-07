#!/usr/bin/env python3
"""Quick check of duplicate columns in merged panel."""
from __future__ import annotations

import numpy as np
import pandas as pd
from pathlib import Path

from src.ingest import loader
from src.features import volatility as vf
from src.features import funding as ff

REPO = Path(__file__).resolve().parents[1]
RAW = REPO / "data" / "raw"
symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT"]
start = "2024-01-01"
end = "2024-03-31"

frames = []
for sym in symbols:
    klist = []
    for kf in sorted(RAW.glob(f"{sym}-1h-*.csv")):
        try:
            klist.append(loader.load_klines(kf))
        except Exception:
            continue
    kdf = pd.concat(klist).sort_index()
    kdf = kdf.loc[(kdf.index >= pd.Timestamp(start, tz="UTC")) & (kdf.index <= pd.Timestamp(end, tz="UTC") + pd.Timedelta(days=1))]
    kdf = vf.add_rv_features(kdf, short_windows=[6, 24], long_windows=[168])
    kdf = kdf.reset_index().rename(columns={"open_time": "timestamp"})
    kdf["symbol"] = sym
    frames.append(kdf)
panel = pd.concat(frames, ignore_index=True)
panel["timestamp"] = pd.to_datetime(panel["timestamp"], utc=True)
panel = panel.set_index(["symbol", "timestamp"]).sort_index()

fframes = []
for sym in symbols:
    flist = []
    for fp in sorted(RAW.glob(f"{sym}-fundingRate-*.csv")):
        try:
            flist.append(loader.load_funding(fp))
        except Exception:
            continue
    fdf = pd.concat(flist).sort_index()
    fdf = fdf.loc[(fdf.index >= pd.Timestamp(start, tz="UTC")) & (fdf.index <= pd.Timestamp(end, tz="UTC") + pd.Timedelta(days=1))]
    fdf = fdf.reset_index().rename(columns={"calc_time": "timestamp"})
    fdf["symbol"] = sym
    fframes.append(fdf)
fpanel = pd.concat(fframes, ignore_index=True)
fpanel["timestamp"] = pd.to_datetime(fpanel["timestamp"], utc=True)
fpanel = fpanel.set_index(["symbol", "timestamp"]).sort_index()

out = panel.copy()
feat_frames = []
for sym in out.index.get_level_values("symbol").unique():
    kidx = out.xs(sym, level="symbol").index
    fdf = fpanel.xs(sym, level="symbol")
    ffeat = ff.add_funding_features(kidx, fdf)
    ffeat = ffeat.reset_index()
    ffeat["symbol"] = sym
    ffeat = ffeat.set_index(["symbol", "timestamp"]).sort_index()
    feat_frames.append(ffeat)

feats_ax1 = pd.concat(feat_frames, axis=1)
print("axis=1 concat columns:", feats_ax1.columns.tolist())
print("axis=1 dup counts:", feats_ax1.columns.duplicated().sum())

feats_ax0 = pd.concat(feat_frames, axis=0)
print("axis=0 concat shape:", feats_ax0.shape, "cols:", feats_ax0.columns.tolist())
print("axis=0 dup index:", feats_ax0.index.duplicated().sum())
