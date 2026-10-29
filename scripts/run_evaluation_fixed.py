#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import math
import random
from datetime import datetime, timezone, timedelta
from pathlib import Path

import os

REPO = Path(__file__).resolve().parents[1]
RUN_MANIFEST = REPO / "research_state" / "run_manifest.json"

EXPERIMENT = os.environ.get("FCLR_EXPERIMENT", "FCLR-001")
if EXPERIMENT == "FCLR-002":
    OUT = REPO / "research_state" / f"evaluation_summary_{EXPERIMENT}_FIXED.md"
    DATA_END = "2024-09-30"
    SPLIT_KEY = "split_boundaries"
elif EXPERIMENT == "FCLR-003":
    OUT = REPO / "research_state" / f"evaluation_summary_{EXPERIMENT}_FIXED.md"
    DATA_END = "2024-12-31"
    SPLIT_KEY = "split_boundaries_fclr003"
elif EXPERIMENT == "FCLR-004":
    OUT = REPO / "research_state" / f"evaluation_summary_{EXPERIMENT}.md"
    DATA_END = os.environ.get("FCLR_DATA_END", "2024-12-31")
    SPLIT_KEY = os.environ.get("FCLR_SPLIT_KEY", "split_boundaries_fclr004")
else:
    OUT = REPO / "research_state" / "evaluation_summary_FIXED.md"
    DATA_END = "2024-03-31"
    SPLIT_KEY = "split_boundaries"

SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]
EPS = 1e-12
HORIZON = 24

def ts_to_dt(ts_ms):
    return datetime.fromtimestamp(ts_ms / 1000, tz=timezone.utc)

def parse_iso(s):
    if s.endswith('Z'):
        s2 = s[:-1] + '+00:00'
    else:
        s2 = s
    dt = datetime.fromisoformat(s2)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt

def find_mark_csv(sym, date_str):
    candidates = []
    for p in REPO.rglob(f"{sym}-1h-{date_str}.csv"):
        sp = str(p)
        if 'markPrice' in sp and 'indexPrice' not in sp and 'premiumIndex' not in sp:
            candidates.append(p)
    for base in [REPO/"research_state"/"data_cache"]:
        if base.exists():
            for sub in base.iterdir():
                if not sub.is_dir(): continue
                # try nested
                p = sub / f"markPriceKlines-{date_str}" / f"{sym}-1h-{date_str}" / f"{sym}-1h-{date_str}.csv"
                if p.exists(): candidates.append(p)
                p = sub / f"markPriceKlines-{date_str}" / f"{sym}-1h-{date_str}.csv"
                if p.exists(): candidates.append(p)
    seen = set()
    out = []
    for c in candidates:
        rp = c.resolve()
        if rp in seen: continue
        seen.add(rp)
        out.append(rp)
    return out[0] if out else None

def find_premium_csv(sym, date_str):
    candidates = []
    for p in REPO.rglob(f"{sym}-1h-{date_str}.csv"):
        sp = str(p)
        if 'premiumIndex' in sp:
            candidates.append(p)
    for base in [REPO/"research_state"/"data_cache"]:
        if base.exists():
            for sub in base.iterdir():
                if not sub.is_dir(): continue
                p = sub / f"premiumIndexKlines-{date_str}" / f"{sym}-1h-{date_str}" / f"{sym}-1h-{date_str}.csv"
                if p.exists(): candidates.append(p)
                p = sub / f"premiumIndexKlines-{date_str}" / f"{sym}-1h-{date_str}.csv"
                if p.exists(): candidates.append(p)
    seen = set()
    out = []
    for c in candidates:
        rp = c.resolve()
        if rp in seen: continue
        seen.add(rp)
        out.append(rp)
    return out[0] if out else None

def find_index_csv(sym, date_str):
    candidates = []
    for p in REPO.rglob(f"{sym}-1h-{date_str}.csv"):
        sp = str(p)
        if 'indexPrice' in sp and 'premium' not in sp:
            candidates.append(p)
    for base in [REPO/"research_state"/"data_cache"]:
        if base.exists():
            for sub in base.iterdir():
                if not sub.is_dir(): continue
                p = sub / f"indexPriceKlines-{date_str}" / f"{sym}-1h-{date_str}" / f"{sym}-1h-{date_str}.csv"
                if p.exists(): candidates.append(p)
                p = sub / f"indexPriceKlines-{date_str}" / f"{sym}-1h-{date_str}.csv"
                if p.exists(): candidates.append(p)
    seen = set()
    out = []
    for c in candidates:
        rp = c.resolve()
        if rp in seen: continue
        seen.add(rp)
        out.append(rp)
    return out[0] if out else None

def find_funding_csv(sym, month):
    for p in REPO.rglob(f"{sym}-fundingRate-{month}.csv"):
        return p
    for base in [REPO/"research_state"/"data_cache"]:
        if base.exists():
            for sub in base.iterdir():
                if not sub.is_dir(): continue
                p = sub / f"{sym}-fundingRate-{month}" / f"{sym}-fundingRate-{month}.csv"
                if p.exists(): return p
    return None

def load_mark_series(sym, start_dt, end_dt):
    series = []
    cur = start_dt.replace(hour=0, minute=0, second=0, microsecond=0)
    end_day = end_dt.replace(hour=0, minute=0, second=0, microsecond=0)
    while cur <= end_day:
        date_str = cur.strftime("%Y-%m-%d")
        csvp = find_mark_csv(sym, date_str)
        if csvp and csvp.exists():
            try:
                with csvp.open() as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        try:
                            ts_ms = int(row['open_time'])
                            ts_dt = ts_to_dt(ts_ms)
                            if ts_dt < start_dt - timedelta(days=2) or ts_dt > end_dt + timedelta(days=2):
                                continue
                            close = float(row['close'])
                            series.append((ts_ms, close))
                        except Exception:
                            continue
            except Exception:
                pass
        cur += timedelta(days=1)
    series.sort(key=lambda x: x[0])
    dedup = []
    seen = set()
    for ts_ms, close in series:
        if ts_ms in seen: continue
        seen.add(ts_ms)
        dedup.append((ts_ms, close))
    return dedup

def load_premium_series(sym, start_dt, end_dt):
    series = []
    cur = start_dt.replace(hour=0, minute=0, second=0, microsecond=0)
    end_day = end_dt.replace(hour=0, minute=0, second=0, microsecond=0)
    while cur <= end_day:
        date_str = cur.strftime("%Y-%m-%d")
        csvp = find_premium_csv(sym, date_str)
        if csvp and csvp.exists():
            try:
                with csvp.open() as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        try:
                            ts_ms = int(row['open_time'])
                            close = float(row['close'])
                            series.append((ts_ms, close))
                        except Exception:
                            continue
            except Exception:
                pass
        cur += timedelta(days=1)
    series.sort(key=lambda x: x[0])
    dedup = []
    seen = set()
    for ts_ms, val in series:
        if ts_ms in seen: continue
        seen.add(ts_ms)
        dedup.append((ts_ms, val))
    return dedup

def load_index_series(sym, start_dt, end_dt):
    series = []
    cur = start_dt.replace(hour=0, minute=0, second=0, microsecond=0)
    end_day = end_dt.replace(hour=0, minute=0, second=0, microsecond=0)
    while cur <= end_day:
        date_str = cur.strftime("%Y-%m-%d")
        csvp = find_index_csv(sym, date_str)
        if csvp and csvp.exists():
            try:
                with csvp.open() as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        try:
                            ts_ms = int(row['open_time'])
                            close = float(row['close'])
                            series.append((ts_ms, close))
                        except Exception:
                            continue
            except Exception:
                pass
        cur += timedelta(days=1)
    series.sort(key=lambda x: x[0])
    dedup = []
    seen = set()
    for ts_ms, val in series:
        if ts_ms in seen: continue
        seen.add(ts_ms)
        dedup.append((ts_ms, val))
    return dedup
