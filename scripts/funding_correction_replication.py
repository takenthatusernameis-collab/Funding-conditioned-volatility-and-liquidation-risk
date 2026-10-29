#!/usr/bin/env python3
"""Funding-correction survival replication (FCLR-H002).

Reconstruct funding-extreme events and time-to-correction from admissible public
data. Compare high vs low realized-volatility conditions. Report partial if exact
methodology unavailable.

This is a replication attempt based on a pre-specified event definition
(research_state/h002_pre_registration.md); the full paper methodology may not be
independently reconstructed. Correction time is a separate outcome from volatility
forecast skill and from observed liquidation; do not conflate them.
"""
from __future__ import annotations

import csv
import json
import math
import os
from pathlib import Path
from datetime import datetime, timezone

REPO = Path(__file__).resolve().parents[1]
DATA_CACHE = REPO / "research_state" / "data_cache"

DEFAULT_SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]
WINDOW_DAYS = 90
MIN_HISTORY = 30
PERCENTILE_LOW = 5.0
PERCENTILE_HIGH = 95.0
MAX_FOLLOW_HOURS = 168
RV_WINDOW_HOURS = 24
MIN_RV_RETURNS = 23


def load_funding_series(funding_csv_path):
    """Load funding rate series from CSV. Returns list of (timestamp_ms, funding_rate)."""
    rows = []
    with open(funding_csv_path) as f:
        reader = csv.DictReader(f)
        for r in reader:
            try:
                ts = int(r["calc_time"])
                fr = float(r["last_funding_rate"])
                if not math.isfinite(fr):
                    continue
                rows.append((ts, fr))
            except Exception:
                continue
    rows.sort(key=lambda x: x[0])
    # dedupe identical timestamps, keep first
    seen = set()
    deduped = []
    for ts, fr in rows:
        if ts in seen:
            continue
        seen.add(ts)
        deduped.append((ts, fr))
    return deduped


def _nearest_rank_percentile(sorted_values, pct):
    if not sorted_values:
        return None
    n = len(sorted_values)
    rank = math.ceil(n * pct / 100.0)
    if rank < 1:
        rank = 1
    if rank > n:
        rank = n
    return sorted_values[rank - 1]


def identify_funding_extremes(funding_series, window_days=WINDOW_DAYS,
                              percentile_threshold=95.0, min_history=MIN_HISTORY):
    """Identify funding extremes relative to trailing 90-day window.

    Two-sided: bottom/top percentiles; positive and negative sides tracked
    separately. Consecutive same-side extremes are deduped: after an extreme on
    a side, subsequent same-side observations are skipped until funding crosses
    back inside [p_low, p_high].
    Returns list of extreme event dicts.
    """
    if not funding_series:
        return []
    events = []
    last_side = None  # 'positive' | 'negative' | None
    ms_per_day = 24 * 3600 * 1000
    for i, (ts, fr) in enumerate(funding_series):
        cutoff = ts - window_days * ms_per_day
        hist = [r for (t2, r) in funding_series[:i] if t2 >= cutoff]
        if len(hist) < min_history:
            last_side = None
            continue
        hist_sorted = sorted(hist)
        p_low = _nearest_rank_percentile(hist_sorted, 100.0 - percentile_threshold)
        p_high = _nearest_rank_percentile(hist_sorted, percentile_threshold)
        inside = p_low <= fr <= p_high
        if inside:
            last_side = None
            continue
        side = "positive" if fr >= p_high else "negative"
        if last_side == side:
            continue  # same-side cluster: keep first extreme only
        last_side = side
        events.append({
            "timestamp_ms": ts,
            "funding_rate": fr,
            "side": side,
            "threshold_low": p_low,
            "threshold_high": p_high,
            "history_count": len(hist),
        })
    return events


def time_to_correction(funding_series, event_ts, event_side, threshold_low,
                       threshold_high, max_hours=MAX_FOLLOW_HOURS):
    """Hours until funding crosses back inside [threshold_low, threshold_high].

    Returns (hours, censored_flag). Censored if no correction within max_hours
    or series ends first.
    """
    start_idx = None
    for i, (ts, fr) in enumerate(funding_series):
        if ts > event_ts:
            start_idx = i
            break
    if start_idx is None:
        return None, True
    limit_ms = event_ts + max_hours * 3600 * 1000
    for j in range(start_idx, len(funding_series)):
        ts_j, fr_j = funding_series[j]
        if ts_j > limit_ms:
            return None, True
        hours_elapsed = (ts_j - event_ts) / (3600.0 * 1000.0)
        if event_side == "positive" and fr_j <= threshold_high:
            return hours_elapsed, False
        if event_side == "negative" and fr_j >= threshold_low:
            return hours_elapsed, False
    return None, True


def load_mark_prices(symbol, year_months):
    """Load cached hourly mark-price closes for a symbol. Returns dict ts_ms->price."""
    prices = {}
    for month in year_months:
        d = DATA_CACHE / f"{symbol}_{month}"
        kl = d / f"{symbol}-markPriceKlines-1h"
        # folder layout: indexPriceKlines-1h-YYYY-MM-DD / per-day files
        if not d.exists():
            continue
        for day_dir in sorted(d.iterdir()):
            if not day_dir.is_dir():
                continue
            if not day_dir.name.startswith("markPriceKlines-1h-"):
                continue
            for csv_file in sorted(day_dir.glob("*.csv")):
                try:
                    with open(csv_file) as f:
                        reader = csv.DictReader(f)
                        for r in reader:
                            try:
                                ts = int(r.get("t", r.get("open_time", "")))
                                c = r.get("c", r.get("close", ""))
                                if ts == 0 or c == "":
                                    continue
                                prices[ts] = float(c)
                            except Exception:
                                continue
                except Exception:
                    continue
    return prices


def compute_rv_at_event(price_map, event_ts, window_hours=RV_WINDOW_HOURS):
    """Trailing realized vol (sqrt of summed squared log returns) ending at event.

    Uses hourly closes at or before event_ts; sorted timestamps.
    Returns (rv, n_returns) or (None, 0).
    """
    ts_sorted = sorted(price_map.keys())
    eligible = [t for t in ts_sorted if t <= event_ts]
    if len(eligible) < window_hours + 1:
        return None, 0
    window = eligible[-(window_hours + 1):]
    rets = []
    for a, b in zip(window, window[1:]):
        pa, pb = price_map[a], price_map[b]
        if pa <= 0 or pb <= 0:
            continue
        rets.append(math.log(pb / pa))
    if len(rets) < MIN_RV_RETURNS:
        return None, len(rets)
    rv = math.sqrt(sum(r * r for r in rets))
    return rv, len(rets)


def replicate_funding_correction(symbols=None, months=None):
    """Replicate funding-correction pattern with RV-regime hazard contrast."""
    if symbols is None:
        symbols = DEFAULT_SYMBOLS
    if months is None:
        months = ["2024-01", "2024-02", "2024-03"]

    all_events = []
    load_errors = []
    price_maps = {}

    for sym in symbols:
        series = []
        for month in months:
            fund_dir = REPO / f"{sym}-fundingRate-{month}"
            fund_csv = fund_dir / f"{sym}-fundingRate-{month}.csv"
            if fund_csv.exists():
                try:
                    series += load_funding_series(fund_csv)
                except Exception as e:
                    load_errors.append(f"{sym}-{month}: {e}")
        series.sort(key=lambda x: x[0])
        # dedupe across months
        seen = set()
        uniq = []
        for ts, fr in series:
            if ts in seen:
                continue
            seen.add(ts)
            uniq.append((ts, fr))
        events = identify_funding_extremes(uniq)
        price_maps[sym] = load_mark_prices(sym, months)
        for ev in events:
            ttc, censored = time_to_correction(
                uniq, ev["timestamp_ms"], ev["side"],
                ev["threshold_low"], ev["threshold_high"])
            ev["symbol"] = sym
            ev["time_to_correction_hours"] = ttc
            ev["censored"] = censored
            rv, n_ret = compute_rv_at_event(price_maps[sym], ev["timestamp_ms"])
            ev["rv_24h"] = rv
            ev["rv_n_returns"] = n_ret
            all_events.append(ev)

    # RV regime split: terciles per symbol over events with valid RV
    by_symbol = {}
    for ev in all_events:
        by_symbol.setdefault(ev["symbol"], []).append(ev)
    regime_edges = {}
    for sym, evs in by_symbol.items():
        rvs = sorted(e["rv_24h"] for e in evs if e["rv_24h"] is not None)
        if len(rvs) >= 2:
            regime_edges[sym] = {
                "n_rv_valid": len(rvs),
                "low_edge": _nearest_rank_percentile(rvs, 33.33),
                "high_edge": _nearest_rank_percentile(rvs, 66.67),
            }
        for ev in evs:
            if ev["rv_24h"] is None:
                ev["rv_regime"] = "missing"
            else:
                e = regime_edges.get(sym)
                if not e:
                    ev["rv_regime"] = "missing"
                elif ev["rv_24h"] <= e["low_edge"]:
                    ev["rv_regime"] = "low"
                elif ev["rv_24h"] >= e["high_edge"]:
                    ev["rv_regime"] = "high"
                else:
                    ev["rv_regime"] = "middle"

    results = {
        "status": "partial",
        "note": "Partial replication; full Shek methodology (SSRN 7529458) not independently reconstructible (SSRN 403 in this environment). Correction time is separate from volatility-forecast and liquidation outcomes.",
        "paper_claim": {
            "events": 1696,
            "contracts": 18,
            "median_high_rv_hours": 27.0,
            "median_low_rv_hours": 3.0,
            "claim": "lower correction hazard with higher realized volatility",
        },
        "definition": {
            "window_days": WINDOW_DAYS,
            "min_history": MIN_HISTORY,
            "percentiles": [PERCENTILE_LOW, PERCENTILE_HIGH],
            "max_follow_hours": MAX_FOLLOW_HOURS,
            "rv_window_hours": RV_WINDOW_HOURS,
            "min_rv_returns": MIN_RV_RETURNS,
        },
        "symbols": symbols,
        "months": months,
        "regime_edges": regime_edges,
        "load_errors": load_errors,
        "events": [],
    }

    total = len(all_events)
    corrected = [e for e in all_events if not e["censored"]]
    censored = [e for e in all_events if e["censored"]]

    def med(times):
        if not times:
            return None
        s = sorted(times)
        return s[len(s) // 2]

    results["total_events"] = total
    results["corrected_count"] = len(corrected)
    results["censored_count"] = len(censored)
    results["median_correction_hours_all"] = med([e["time_to_correction_hours"]
                                                  for e in corrected])

    # Hazard-by-RV-regime table with censoring
    regimes = {}
    for ev in all_events:
        rg = regimes.setdefault(ev["rv_regime"], {
            "n": 0, "corrected": 0, "censored": 0,
            "correction_times": [], "by_symbol": {}})
        rg["n"] += 1
        if ev["censored"]:
            rg["censored"] += 1
        else:
            rg["corrected"] += 1
            rg["correction_times"].append(ev["time_to_correction_hours"])
        bsym = rg["by_symbol"].setdefault(ev["symbol"], {
            "n": 0, "corrected": 0, "censored": 0,
            "correction_times": []})
        bsym["n"] += 1
        if ev["censored"]:
            bsym["censored"] += 1
        else:
            bsym["corrected"] += 1
            bsym["correction_times"].append(ev["time_to_correction_hours"])
    for rg in regimes.values():
        rg["median_correction_hours"] = med(rg["correction_times"])
        rg["correction_rate"] = (rg["corrected"] / rg["n"]) if rg["n"] else None
        for bsym in rg["by_symbol"].values():
            bsym["median_correction_hours"] = med(bsym["correction_times"])
            bsym["correction_rate"] = (bsym["corrected"] / bsym["n"]) if bsym["n"] else None
    results["hazard_by_rv_regime"] = regimes

    results["events"] = all_events[:200]
    return results


if __name__ == "__main__":
    res = replicate_funding_correction()
    print(json.dumps(res, indent=2))
