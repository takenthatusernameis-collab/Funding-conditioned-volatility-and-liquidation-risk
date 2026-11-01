#!/usr/bin/env python3
"""Build the FCLR-COUPLED-001 hourly panel from ironflow Hyperliquid liquidation census.

Vectorized pandas construction. Caches to research_state/.cache/fclr_coupled_panel.parquet
so the experiment is restartable without re-reading 2.17M raw rows.

Labels only. Features are computed later from label history (decision-time, causal).
Cross-track firewall: Hyperliquid native perps ONLY. No Binance data.
"""
from __future__ import annotations

import os
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

REPO = Path(__file__).resolve().parents[1]
IRONFLOW = REPO / "research_state" / "data_cache" / "ironflow_events"
CACHE = REPO / "research_state" / ".cache" / "fclr_coupled_panel.parquet"
MANIFEST = REPO / "research_state" / "run_manifest.json"
import json
with open(MANIFEST) as _f:
    _M = json.load(_f)
_S = _M["split_boundaries_fclr010"]
WIN_START = pd.Timestamp(_S["data_window"]["start"])
WIN_END = pd.Timestamp(_S["data_window"]["end"])


def build(force: bool = False) -> pd.DataFrame:
    if CACHE.exists() and not force:
        return pd.read_parquet(CACHE)

    files = sorted(f for f in os.listdir(IRONFLOW) if f.endswith(".parquet"))
    frames = []
    for fname in files:
        t = pq.read_table(
            IRONFLOW / fname,
            columns=["timestamp", "market", "position_side", "notional_usd"],
        )
        df = t.to_pandas()
        # keep native perps only
        m = df["market"].astype(str).str.endswith("-PERP") & ~df["market"].astype(str).str.contains(":")
        df = df.loc[m].copy()
        df["hour"] = df["timestamp"].dt.floor("h")
        df["notional_usd"] = df["notional_usd"].fillna(0.0).astype(np.float64)
        df["is_long"] = (df["position_side"].astype(str) == "long").astype(np.int64)
        df["is_short"] = (df["position_side"].astype(str) == "short").astype(np.int64)
        df["side_count"] = np.ones(len(df), dtype=np.int64)
        frames.append(df[["hour", "market", "side_count", "is_long", "is_short", "notional_usd"]])

    raw = pd.concat(frames, ignore_index=True)
    raw = raw[(raw["hour"] >= WIN_START) & (raw["hour"] <= WIN_END)]

    g = (
        raw.groupby(["market", "hour"], as_index=False)
        .agg(
            cnt=("side_count", "sum"),
            long_cnt=("is_long", "sum"),
            short_cnt=("is_short", "sum"),
            usd=("notional_usd", "sum"),
        )
    )
    # complete hourly grid per symbol so zero-liquidation hours are explicit rows
    symbols = sorted(g["market"].unique().tolist())
    hours = pd.date_range(WIN_START, WIN_END, freq="h", inclusive="left")
    idx = pd.MultiIndex.from_product([symbols, hours], names=["market", "hour"])
    panel = idx.to_frame(index=False)
    panel = panel.merge(g, on=["market", "hour"], how="left")
    for c in ["cnt", "long_cnt", "short_cnt", "usd"]:
        panel[c] = panel[c].fillna(0.0 if c == "usd" else 0).astype(np.int64 if c != "usd" else np.float64)
    panel["y_occ"] = (panel["cnt"] > 0).astype(np.int64)
    panel["y_int"] = np.log1p(panel["usd"])
    panel = panel.sort_values(["market", "hour"]).reset_index(drop=True)
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    panel.to_parquet(CACHE, index=False)
    return panel


if __name__ == "__main__":
    p = build(force=True)
    print(f"Panel: {p.shape}  symbols={p['market'].nunique()}  hours={p['hour'].nunique()}")
    print("occurrence rate:", p['y_occ'].mean().round(6))
    print(p.head())