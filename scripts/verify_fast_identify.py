#!/usr/bin/env python3
"""Exhaustive equivalence check: fast sliding-window funding-extreme identifier
vs. the canonical O(n^2) implementation in funding_correction_replication.

Reads ONLY cached data (no network). Exits non-zero if any real series differs.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import funding_correction_replication as fcr
import fclr_shek_scale as shek


def fast_identify(funding_series, window_days=90, percentile_threshold=95.0,
                  min_history=30):
    """Semantically identical to fcr.identify_funding_extremes but O(n) window."""
    from collections import deque
    if not funding_series:
        return []
    events = []
    last_side = None
    ms_per_day = 24 * 3600 * 1000
    window = deque()  # (t2, r) with t2 in (ts_i - 90d, ts_i)
    for i, (ts, fr) in enumerate(funding_series):
        cutoff = ts - window_days * ms_per_day
        while window and window[0][0] < cutoff:
            window.popleft()
        hist = [r for (_, r) in window]
        if len(hist) < min_history:
            last_side = None
            window.append((ts, fr))
            continue
        hist_sorted = sorted(hist)
        p_low = fcr._nearest_rank_percentile(hist_sorted, 100.0 - percentile_threshold)
        p_high = fcr._nearest_rank_percentile(hist_sorted, percentile_threshold)
        inside = p_low <= fr <= p_high
        if inside:
            last_side = None
            window.append((ts, fr))
            continue
        side = "positive" if fr >= p_high else "negative"
        if last_side == side:
            window.append((ts, fr))
            continue
        last_side = side
        events.append({
            "timestamp_ms": ts,
            "funding_rate": fr,
            "side": side,
            "threshold_low": p_low,
            "threshold_high": p_high,
            "history_count": len(hist),
        })
        window.append((ts, fr))
    return events


def _arm_a_series():
    out = []
    for sym in shek.DEFAULT_SYMBOLS:
        for month in shek.ARM_A_MONTHS:
            p = shek._resolve_funding_csv(sym, month)
            if p:
                out.append((f"{sym}-{month}", fcr.load_funding_series(p)))
    return out


def _arm_b_series():
    import pyarrow.parquet as pq
    import pyarrow as pa
    fdir = shek.DATA_CACHE / "ironflow_bulk" / "funding"
    fdf = pa.concat_tables([pq.read_table(p) for p in sorted(fdir.glob("*.parquet"))]).to_pandas()
    fdf["ts_ms"] = (fdf["timestamp"].astype("int64") // 1000)
    out = []
    for coin in shek.ARM_B_COINS:
        sub = fdf[fdf["coin"] == coin].sort_values("ts_ms")
        if sub.empty:
            continue
        series = list(zip(sub["ts_ms"].tolist(), sub["funding_rate"].astype(float).tolist()))
        seen, uniq = set(), []
        for ts, fr in series:
            if ts in seen:
                continue
            seen.add(ts)
            uniq.append((ts, fr))
        out.append((coin, uniq))
    return out


def main():
    failures = 0
    checked = 0
    for label, series in _arm_a_series() + _arm_b_series():
        if not series:
            continue
        checked += 1
        canon = fcr.identify_funding_extremes(series)
        fast = fast_identify(series)
        if canon != fast:
            failures += 1
            print(f"MISMATCH {label}: canon={len(canon)} fast={len(fast)}")
            for i, (a, b) in enumerate(zip(canon, fast)):
                if a != b:
                    print(f"  first diff at idx {i}: canon={a} fast={b}")
                    break
    print(f"checked={checked} failures={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())