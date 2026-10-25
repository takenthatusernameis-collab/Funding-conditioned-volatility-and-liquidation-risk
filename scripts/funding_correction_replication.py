#!/usr/bin/env python3
"""Funding-correction survival replication (FCLR-H002).

Reconstruct funding-extreme events and time-to-correction from admissible public
data. Compare high vs low realized-volatility conditions. Report partial if exact
methodology unavailable.

This is a replication attempt based on pre-specified event definition; full
methodology from the paper may not be independently reconstructed.
"""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from datetime import datetime, timedelta, timezone

REPO = Path(__file__).resolve().parents[1]
RUN_MANIFEST = REPO / "research_state" / "run_manifest.json"


def load_funding_series(funding_csv_path):
    """Load funding rate series from CSV. Returns list of (timestamp_ms, funding_rate)."""
    rows = []
    with open(funding_csv_path) as f:
        reader = csv.DictReader(f)
        for r in reader:
            try:
                ts = int(r['calc_time'])
                fr = float(r['last_funding_rate'])
                rows.append((ts, fr))
            except Exception:
                continue
    rows.sort(key=lambda x: x[0])
    return rows


def identify_funding_extremes(funding_series, window_days=90, percentile_threshold=95):
    """
    Identify funding extremes as funding rates in top/bottom percentile
    relative to trailing window. Pre-specified definition.
    Returns list of extreme events with metadata.
    """
    if not funding_series:
        return []
    events = []
    # Build rolling window
    for i, (ts, fr) in enumerate(funding_series):
        # Look back window_days
        cutoff = ts - window_days * 24 * 3600 * 1000
        hist = [r for (t2, r) in funding_series[:i] if t2 >= cutoff]
        if len(hist) < 30:  # need enough history
            continue
        hist_sorted = sorted(hist)
        p_low = hist_sorted[int(len(hist_sorted) * (1 - percentile_threshold/100.0))]
        p_high = hist_sorted[int(len(hist_sorted) * (percentile_threshold/100.0))]
        is_extreme = fr <= p_low or fr >= p_high
        if is_extreme:
            events.append({
                'timestamp_ms': ts,
                'funding_rate': fr,
                'is_extreme': True,
                'side': 'positive' if fr >= p_high else 'negative',
                'threshold_low': p_low,
                'threshold_high': p_high
            })
    return events


def time_to_correction(funding_series, event_ts, event_side, threshold_low, threshold_high, max_hours=168):
    """
    Time until funding rate crosses back to within normalization threshold.
    Returns hours to correction, or None if censored (doesn't cross within max_hours).
    """
    # Look forward from event
    start_idx = None
    for i, (ts, fr) in enumerate(funding_series):
        if ts >= event_ts:
            start_idx = i
            break
    if start_idx is None:
        return None
    # Check subsequent funding rates
    for j in range(start_idx + 1, len(funding_series)):
        ts_j, fr_j = funding_series[j]
        hours_elapsed = (ts_j - event_ts) / (3600 * 1000)
        if hours_elapsed > max_hours:
            return None  # censored
        # Check if corrected (back within threshold)
        if event_side == 'positive':
            # Positive extreme corrected if funding drops below threshold_high
            if fr_j <= threshold_high:  # crossed back
                return hours_elapsed
        elif event_side == 'negative':
            # Negative extreme corrected if funding rises above threshold_low
            if fr_j >= threshold_low:
                return hours_elapsed
    return None  # censored


def compute_realized_volatility_simple(price_series, window_hours=24):
    """Compute simple realized volatility over trailing window."""
    if len(price_series) < window_hours + 1:
        return None
    rets = []
    for i in range(len(price_series) - window_hours, len(price_series)):
        if i == 0:
            continue
        p_prev = price_series[i-1]
        p_curr = price_series[i]
        if p_prev <= 0 or p_curr <= 0:
            continue
        rets.append(math.log(p_curr / p_prev))
    if not rets:
        return None
    rv = math.sqrt(sum(r*r for r in rets))
    return rv


def replicate_funding_correction(symbols=None):
    """
    Replicate funding-correction pattern. Returns results dict.
    Reports partial if methodology details uncertain.
    """
    if symbols is None:
        symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'XRPUSDT']

    all_events = []
    results = {
        'status': 'partial',  # partial replication as methodology may not be fully reconstructible
        'note': 'Replication based on pre-specified event definition; full paper methodology may require additional details not independently available',
        'symbols': symbols,
        'events': []
    }

    for sym in symbols:
        # Try to load funding data
        for month in ['2024-01', '2024-02', '2024-03']:
            fund_dir = REPO / f"{sym}-fundingRate-{month}"
            fund_csv = fund_dir / f"{sym}-fundingRate-{month}.csv"
            if fund_csv.exists():
                try:
                    funding_series = load_funding_series(fund_csv)
                    events = identify_funding_extremes(funding_series)
                    for ev in events:
                        ttc = time_to_correction(funding_series, ev['timestamp_ms'],
                                                ev['side'], ev['threshold_low'],
                                                ev['threshold_high'])
                        ev['symbol'] = sym
                        ev['time_to_correction_hours'] = ttc
                        ev['censored'] = ttc is None
                        all_events.append(ev)
                except Exception as e:
                    results['errors'] = results.get('errors', []) + [f"{sym}-{month}: {str(e)}"]

    results['total_events'] = len(all_events)
    results['events'] = all_events[:100]  # truncate for summary

    # Compute summary statistics
    corrected = [e for e in all_events if not e['censored'] and e['time_to_correction_hours'] is not None]
    if corrected:
        times = [e['time_to_correction_hours'] for e in corrected]
        results['median_correction_hours'] = sorted(times)[len(times)//2]
        results['mean_correction_hours'] = sum(times) / len(times)
        results['corrected_count'] = len(corrected)
        results['censored_count'] = len([e for e in all_events if e['censored']])

    return results


if __name__ == '__main__':
    res = replicate_funding_correction()
    print(json.dumps(res, indent=2))
