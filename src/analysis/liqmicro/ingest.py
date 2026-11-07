#!/usr/bin/env python3
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[3]
IRONFLOW = REPO / "research_state" / "data_cache" / "ironflow_events"

# 113 src audit: top-level `import pyarrow.parquet as pq` removed. No parquet/outcome/data
# read happens at module import.
# 114 src guard: lazy pd.read_parquet()/open() reads in load_all() now require an explicit
# guarded contract (guarded=True). Without it, GuardedReadRefused is raised before any disk
# read, so no implicit outcome/data load executes on blocked or misconfigured branches.
# Callers (run_liqmicro.py, run_liqmicro_v2.py) route load_all(guarded=True) through
# scripts.fclr010_guarded_entry.guarded_execute and only pass guarded=True after
# READY_FROZEN.

class GuardedReadRefused(RuntimeError):
    """Raised when a src/ method-level data read is attempted without passing the guarded contract."""

    pass


class IronflowIngestor:
    def __init__(self, data_dir: Path = IRONFLOW):
        self.data_dir = data_dir
        self.files = sorted([f for f in os.listdir(data_dir) if f.endswith('.parquet')]) if data_dir.exists() else []

    def load_all(self, *, guarded: bool = False) -> pd.DataFrame:
        if not guarded:
            raise GuardedReadRefused(
                "IronflowIngestor.load_all: parquet read refused; guarded contract not satisfied "
                "(pass guarded=True only after guarded_execute returns READY_FROZEN)."
            )
        dfs = []
        for fname in self.files:
            try:
                df = pd.read_parquet(self.data_dir / fname)
                dfs.append(df)
            except Exception as e:
                print(f"Error loading {fname}: {e}")
        if not dfs:
            return pd.DataFrame()
        return pd.concat(dfs, ignore_index=True)

    def aggregate_hourly(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return pd.DataFrame()
        # Ensure timestamp is datetime
        if 'timestamp' in df.columns:
            df = df.copy()
            df['ts'] = pd.to_datetime(df['timestamp'], utc=True)
        else:
            return pd.DataFrame()

        # Determine side column
        side_col = None
        for c in ['position_side', 'side', 'liquidation_side']:
            if c in df.columns:
                side_col = c
                break

        # Determine market/symbol
        sym_col = 'market' if 'market' in df.columns else ('symbol' if 'symbol' in df.columns else None)
        if sym_col is None:
            return pd.DataFrame()

        # Filter to native perps only if possible
        df = df[df[sym_col].astype(str).apply(lambda x: isinstance(x,str) and x.endswith('-PERP') and ':' not in x)]

        # Create hour bucket
        df['hour'] = df['ts'].dt.floor('h')

        agg_dict = {}
        if 'notional_usd' in df.columns:
            agg_dict['notional_usd'] = 'sum'
        if 'size' in df.columns:
            agg_dict['size'] = 'sum'
        agg_dict[sym_col] = 'count'  # count of events

        grouped = df.groupby(['hour', sym_col]).agg(agg_dict).rename(columns={sym_col: 'liq_count'}).reset_index()
        grouped.rename(columns={sym_col: 'symbol'}, inplace=True)

        # Add long/short split if available
        if side_col is not None:
            for side_val in df[side_col].dropna().unique():
                side_df = df[df[side_col] == side_val]
                side_agg = side_df.groupby(['hour', sym_col]).size().reset_index(name=f'liq_count_{side_val}')
                side_agg.rename(columns={sym_col: 'symbol'}, inplace=True)
                grouped = grouped.merge(side_agg, on=['hour', 'symbol'], how='left')

        grouped = grouped.fillna(0)
        return grouped


class HyperliquidFundingIngestor:
    def __init__(self, data_dir: Path = None):
        if data_dir is None:
            data_dir = REPO / "research_state" / "data_cache" / "hyperliquid_funding"
        self.data_dir = data_dir
        self.files = sorted([f for f in os.listdir(data_dir) if f.endswith('.json')]) if data_dir.exists() else []

    def load_all(self, *, guarded: bool = False) -> pd.DataFrame:
        if not guarded:
            raise GuardedReadRefused(
                "HyperliquidFundingIngestor.load_all: json/open read refused; guarded contract not satisfied "
                "(pass guarded=True only after guarded_execute returns READY_FROZEN)."
            )
        import json
        dfs = []
        for fname in self.files:
            try:
                fname_str = str(fname)
                coin = fname_str.replace('.json', '')
                with open(self.data_dir / fname_str) as f:
                    data = json.load(f)
                rows = []
                for rec in data:
                    try:
                        t = rec.get('time') or rec.get('timestamp')
                        fr = rec.get('fundingRate')
                        if t is None or fr is None:
                            continue
                        ts = pd.to_datetime(int(t), unit='ms', utc=True)
                        rows.append({
                            'coin': coin,
                            'symbol_hl': f'{coin}-PERP',
                            'timestamp': ts,
                            'funding_rate': float(fr),
                            'hour': ts.floor('h')
                        })
                    except Exception:
                        continue
                if rows:
                    dfs.append(pd.DataFrame(rows))
            except Exception as e:
                print(f"Error loading {fname}: {e}")
        if not dfs:
            return pd.DataFrame()
        df = pd.concat(dfs, ignore_index=True)
        return df
