#!/usr/bin/env python3
"""Debug funding ablation nulls using script functions directly."""
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
panel = pd.concat(frames, ignore_index=True)
panel["timestamp"] = pd.to_datetime(panel["timestamp"], utc=True)
panel = panel.set_index(["symbol", "timestamp"]).sort_index()
print("panel shape", panel.shape)

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
trail = [c for c in merged.columns if c.startswith(("funding_pct_", "funding_z_"))]
ablations = {
    "A_rv_only": base[:],
    "B_rv_signed": base + ["funding_signed"],
    "C_rv_abs": base + ["funding_abs"],
    "D_rv_signed_abs": base + ["funding_signed", "funding_abs"],
    "E_rv_funding_trails": base + ["funding_signed", "funding_abs"] + trail,
}

for ab_name, fcols in ablations.items():
    fcols = [c for c in fcols if c in merged.columns]
    print(f"\n=== {ab_name} cols={fcols}")
    try:
        train_n, val_n, test_n, _ = wf.apply_train_only_normalization(train, test, test, fcols)
    except Exception as e:
        print("  norm ERR", e)
        continue
    for c in fcols:
        nn = test_n[c].isna().sum()
        if nn > 0:
            print(f"  test_n[{c}] NaN {nn}/{len(test_n)}")
    from src.models.baselines import RVOnlyHAR
    m = RVOnlyHAR(feature_cols=fcols)
    try:
        m.fit(train_n[fcols], train_n["target_rv"])
    except Exception as e:
        print("  fit ERR", e)
        continue
    p = m.predict(test_n[fcols])
    y = test_n["target_rv"].to_numpy(dtype=float)
    from src.volatility import eval as veval
    print("  coef", m.coef_, "intercept", m.intercept_)
    print("  pred nan", np.isnan(p).sum(), "min", np.nanmin(p), "max", np.nanmax(p))
    print("  qlike", veval.qlike(y.tolist(), p.tolist()), "mae", veval.mae(y.tolist(), p.tolist()))