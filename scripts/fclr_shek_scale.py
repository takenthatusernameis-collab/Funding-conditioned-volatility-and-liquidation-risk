#!/usr/bin/env python3
"""FCLR-SHEK-SCALE: scaled funding-conditioned correction-hazard study (EXPLORATORY_ONLY).

Heavy, network-free, cache-only execution of the pre-registered campaign
`FCLR-SHEK-SCALE-20261115T040843Z`. Two arms:

  * Arm A (primary, independent): Binance USDⓈ-M funding, 5 symbols x
    2024-04..2026-10 (EXCLUDING the already-reported 2024-01..2024-03).
  * Arm B (secondary, never promotable): ironflow cross-coin funding+candles,
    160 qualifying coins, observed months 2025-05..2025-12.

Frozen event definition is imported from `funding_correction_replication`
(trailing 90d, nearest-rank 5th/95th, >=30 obs, same-side dedupe, first later
re-entry, censor 168h, trailing-24h mark-price RV). The frozen prereg is
`research_state/prereg_fclr_shek_scale_20261115T063600Z.json`.

This module never promotes H2 out of EXPLORATORY_ONLY and never relabels the
correction-time outcome as forecast skill, boundary-breach, or observed-liq.

CLI:
  python3 scripts/fclr_shek_scale.py                       # full run, writes artifacts
  python3 scripts/fclr_shek_scale.py --out <dir>            # alternate artifact dir
  python3 scripts/fclr_shek_scale.py --arm a|b               # single arm
  python3 scripts/fclr_shek_scale.py --no-write              # print JSON summary only
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).resolve().parent))

import funding_correction_replication as fcr

REPO = Path(__file__).resolve().parents[1]
DATA_CACHE = REPO / "research_state" / "data_cache"
PREREG = REPO / "research_state" / "prereg_fclr_shek_scale_20261115T063600Z.json"

DEFAULT_SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]
ARM_A_MONTHS = (
    [f"2024-{m:02d}" for m in range(4, 13)]
    + [f"2025-{m:02d}" for m in range(1, 13)]
    + [f"2026-{m:02d}" for m in range(1, 11)]
)

# Frozen Arm B coin universe (160 coins; recorded in the frozen prereg).
ARM_B_COINS = [
    "AAVE", "ACE", "ADA", "AIXBT", "ALGO", "ALT", "ANIME", "APE", "APT", "AR",
    "ARB", "ARK", "ATOM", "AVAX", "BABY", "BANANA", "BCH", "BERA", "BIGTIME",
    "BIO", "BLAST", "BLUR", "BNB", "BOME", "BRETT", "BSV", "BTC", "CAKE", "CELO",
    "CFX", "CHILLGUY", "COMP", "CRV", "DOGE", "DOOD", "DOT", "DYDX", "DYM",
    "EIGEN", "ENA", "ENS", "ETC", "ETH", "ETHFI", "FARTCOIN", "FET", "FIL",
    "FTT", "FXS", "GALA", "GAS", "GMT", "GMX", "GOAT", "GRASS", "GRIFFAIN",
    "HBAR", "HMSTR", "HYPE", "HYPER", "IMX", "INIT", "INJ", "IO", "IOTA", "IP",
    "JTO", "JUP", "KAITO", "KAS", "LAYER", "LDO", "LINK", "LTC", "MANTA", "MAV",
    "MAVIA", "ME", "MELANIA", "MEME", "MERL", "MEW", "MINA", "MNT", "MOODENG",
    "MORPHO", "MOVE", "NEAR", "NEO", "NIL", "NOT", "NXPC", "OM", "ONDO", "OP",
    "ORDI", "PAXG", "PENDLE", "PENGU", "PEOPLE", "PNUT", "POL", "POLYX",
    "POPCAT", "PROMPT", "PURR", "PYTH", "RENDER", "REZ", "RSR", "RUNE", "S",
    "SAGA", "SAND", "SCR", "SEI", "SNX", "SOL", "SOPH", "SPX", "STRK", "STX",
    "SUI", "SUPER", "SUSHI", "TAO", "TIA", "TNSR", "TON", "TRB", "TRUMP", "TRX",
    "TST", "TURBO", "UMA", "UNI", "USTC", "USUAL", "VINE", "VIRTUAL", "W",
    "WCT", "WIF", "WLD", "XAI", "XLM", "XRP", "YGG", "ZEN", "ZEREBRO", "ZETA",
    "ZK", "ZORA", "ZRO", "kBONK", "kFLOKI", "kLUNC", "kNEIRO", "kPEPE", "kSHIB",
]

BOOT_N = 2000
SEED = 20261115


# --------------------------------------------------------------------------- #
# Arm A: Binance (reuse frozen event-definition functions from fcr)
# --------------------------------------------------------------------------- #
def _resolve_funding_csv(sym: str, month: str):
    md = DATA_CACHE / f"{sym}_{month.replace('-', '_')}"
    if not md.is_dir():
        return None
    nested = md / f"{sym}-fundingRate-{month}" / f"{sym}-fundingRate-{month}.csv"
    if nested.exists():
        return nested
    flat = md / "fundingRate" / f"{sym}-fundingRate-{month}.csv"
    if flat.exists():
        return flat
    matches = sorted(md.rglob(f"{sym}-fundingRate-{month}.csv"))
    if matches:
        return matches[0]
    return None


def _load_arm_a_data(months=None, symbols=None):
    """Pre-load Arm A funding series and mark-price maps once (cache-only, no network)."""
    months = list(months or ARM_A_MONTHS)
    symbols = list(symbols or DEFAULT_SYMBOLS)
    sym_series = {}
    price_maps = {}
    per_symbol_month = {}
    load_errors = []

    for sym in symbols:
        series = []
        per_symbol_month[sym] = {}
        for month in months:
            csv_path = _resolve_funding_csv(sym, month)
            if csv_path is None:
                per_symbol_month[sym][month] = 0
                continue
            rows = fcr.load_funding_series(csv_path)
            per_symbol_month[sym][month] = len(rows)
            if not rows:
                load_errors.append(f"{sym}-{month}: 0 funding rows")
                continue
            series += rows
        series.sort(key=lambda x: x[0])
        seen = set()
        uniq = []
        for ts, fr in series:
            if ts in seen:
                continue
            seen.add(ts)
            uniq.append((ts, fr))
        sym_series[sym] = uniq
        price_maps[sym] = fcr.load_mark_prices(sym, months)

    return sym_series, price_maps, per_symbol_month, load_errors


def _build_regime_edges(events, rv_split):
    """Build per-symbol RV regime edges (tercile or median split). Returns dict symbol->edges."""
    by_symbol = {}
    for ev in events:
        by_symbol.setdefault(ev["symbol"], []).append(ev)
    edges = {}
    for sym, evs in by_symbol.items():
        rvs = sorted(e["rv_24h"] for e in evs if e["rv_24h"] is not None)
        if len(rvs) >= 2:
            if rv_split == "tercile":
                edges[sym] = {
                    "n_rv_valid": len(rvs),
                    "low_edge": fcr._nearest_rank_percentile(rvs, 33.33),
                    "high_edge": fcr._nearest_rank_percentile(rvs, 66.67),
                    "split": "tercile",
                }
            else:  # median
                med = fcr._nearest_rank_percentile(rvs, 50.0)
                edges[sym] = {
                    "n_rv_valid": len(rvs),
                    "low_edge": med,
                    "high_edge": med,
                    "split": "median",
                }
    return edges


def _assign_rv_regimes(events, edges, rv_split):
    """Assign rv_regime to each event in-place from precomputed edges."""
    for ev in events:
        if ev["rv_24h"] is None:
            ev["rv_regime"] = "missing"
            continue
        e = edges.get(ev["symbol"])
        if not e:
            ev["rv_regime"] = "missing"
        elif e["split"] == "tercile":
            if ev["rv_24h"] <= e["low_edge"]:
                ev["rv_regime"] = "low"
            elif ev["rv_24h"] >= e["high_edge"]:
                ev["rv_regime"] = "high"
            else:
                ev["rv_regime"] = "middle"
        else:  # median
            if ev["rv_24h"] <= e["low_edge"]:
                ev["rv_regime"] = "low"
            else:
                ev["rv_regime"] = "high"


def _run_arm_a_impl(sym_series, price_maps, per_symbol_month, load_errors,
                    p_low=5.0, p_high=95.0, censor_hours=168, rv_split="tercile",
                    months=None, symbols=None):
    """Arm A event reconstruction with parameterized percentiles/censor/rv_split.

    percentile_threshold=p_high drives identify_funding_extremes; p_low is
    derived as 100 - p_high (symmetric grid: [1,99],[5,95],[10,90]).
    Censor applied via max_hours in time_to_correction.
    """
    symbols = list(symbols or DEFAULT_SYMBOLS)
    all_events = []

    for sym in symbols:
        uniq = sym_series[sym]
        events = fcr.identify_funding_extremes(uniq, percentile_threshold=p_high)
        for ev in events:
            ttc, censored = fcr.time_to_correction(
                uniq, ev["timestamp_ms"], ev["side"],
                ev["threshold_low"], ev["threshold_high"],
                max_hours=censor_hours)
            ev["symbol"] = sym
            ev["time_to_correction_hours"] = ttc
            ev["censored"] = censored
            rv, n_ret = fcr.compute_rv_at_event(price_maps[sym], ev["timestamp_ms"])
            ev["rv_24h"] = rv
            ev["rv_n_returns"] = n_ret
            all_events.append(ev)

    edges = _build_regime_edges(all_events, rv_split)
    _assign_rv_regimes(all_events, edges, rv_split)

    return {
        "arm": "A_binance_independent",
        "symbols": symbols,
        "months": months,
        "load_errors": load_errors,
        "per_symbol_month_funding_obs": per_symbol_month,
        "regime_edges": edges,
        "events": all_events,
        "cluster_key": "symbol",
        "rv_split": rv_split,
        "rv_edges": edges,
        "percentiles": [p_low, p_high],
        "censor_hours": censor_hours,
    }


def run_arm_a(months=None):
    """Frozen headline Arm A: [5,95] percentiles, 168h censor, per-symbol tercile."""
    sym_series, price_maps, per_symbol_month, load_errors = _load_arm_a_data(months)
    return _run_arm_a_impl(sym_series, price_maps, per_symbol_month, load_errors,
                           5.0, 95.0, 168, "tercile", months)


# --------------------------------------------------------------------------- #
# Arm B: ironflow cross-coin (pandas/pyarrow; coins frozen in prereg)
# --------------------------------------------------------------------------- #
def _ironflow_months():
    fdir = DATA_CACHE / "ironflow_bulk" / "funding"
    return sorted(p.stem for p in fdir.glob("*.parquet"))


def _load_arm_b_data(coins=None):
    """Pre-load Arm B ironflow funding+candles once (cache-only, no network)."""
    import pyarrow.parquet as pq
    import pyarrow as pa

    coins = list(coins or ARM_B_COINS)
    fdir = DATA_CACHE / "ironflow_bulk" / "funding"
    cdir = DATA_CACHE / "ironflow_bulk" / "candles_1h"
    fpaths = sorted(fdir.glob("*.parquet"))
    cpaths = sorted(cdir.glob("*.parquet"))
    if not fpaths or not cpaths:
        raise RuntimeError("ironflow bulk funding/candles parquet missing")

    fdf = pa.concat_tables([pq.read_table(p) for p in fpaths]).to_pandas()
    cdf = pa.concat_tables([pq.read_table(p) for p in cpaths]).to_pandas()

    # normalise timestamps to epoch ms
    fdf["ts_ms"] = (fdf["timestamp"].astype("int64") // 1_000)
    cdf["ts_ms"] = (cdf["timestamp"].astype("int64") // 1_000)

    return fdf, cdf, coins


def _build_regime_edges_pooled(rvs, rv_split):
    """Build pooled RV regime edges (tercile or median split)."""
    if len(rvs) < 2:
        return {}
    if rv_split == "tercile":
        return {
            "n_rv_valid": len(rvs),
            "low_edge": fcr._nearest_rank_percentile(rvs, 33.33),
            "high_edge": fcr._nearest_rank_percentile(rvs, 66.67),
            "split": "tercile",
        }
    med = fcr._nearest_rank_percentile(rvs, 50.0)
    return {
        "n_rv_valid": len(rvs),
        "low_edge": med,
        "high_edge": med,
        "split": "median",
    }


def _assign_rv_regimes_pooled(events, edges, rv_split):
    """Assign rv_regime to each event in-place from pooled edges."""
    if not edges:
        for ev in events:
            ev["rv_regime"] = "missing"
        return
    for ev in events:
        if ev["rv_24h"] is None:
            ev["rv_regime"] = "missing"
            continue
        if edges["split"] == "tercile":
            if ev["rv_24h"] <= edges["low_edge"]:
                ev["rv_regime"] = "low"
            elif ev["rv_24h"] >= edges["high_edge"]:
                ev["rv_regime"] = "high"
            else:
                ev["rv_regime"] = "middle"
        else:  # median
            if ev["rv_24h"] <= edges["low_edge"]:
                ev["rv_regime"] = "low"
            else:
                ev["rv_regime"] = "high"


def _run_arm_b_impl(fdf, cdf, coins,
                    p_low=5.0, p_high=95.0, censor_hours=168, rv_split="tercile"):
    """Arm B event reconstruction with parameterized percentiles/censor/rv_split.

    percentile_threshold=p_high drives identify_funding_extremes; p_low is
    derived as 100 - p_high (symmetric grid: [1,99],[5,95],[10,90]).
    Pooled cross-coin RV split.
    """
    all_events = []
    per_coin = {}
    load_errors = []

    # Pre-compute price maps per coin
    price_maps = {}
    for coin in coins:
        csub = cdf[cdf["coin"] == coin].sort_values("ts_ms")
        price_maps[coin] = dict(zip(csub["ts_ms"].tolist(), csub["close"].astype(float).tolist()))

    for coin in coins:
        sub = fdf[fdf["coin"] == coin].sort_values("ts_ms")
        if sub.empty:
            load_errors.append(f"{coin}: no funding rows")
            continue
        series = list(zip(sub["ts_ms"].tolist(), sub["funding_rate"].astype(float).tolist()))
        # dedupe timestamps
        seen = set()
        uniq = []
        for ts, fr in series:
            if ts in seen:
                continue
            seen.add(ts)
            uniq.append((ts, fr))

        events = fcr.identify_funding_extremes(uniq, percentile_threshold=p_high)
        per_coin[coin] = {"funding_obs": len(uniq), "events": len(events)}

        price_map = price_maps[coin]

        for ev in events:
            ttc, censored = fcr.time_to_correction(
                uniq, ev["timestamp_ms"], ev["side"],
                ev["threshold_low"], ev["threshold_high"],
                max_hours=censor_hours)
            ev["symbol"] = coin
            ev["time_to_correction_hours"] = ttc
            ev["censored"] = censored
            rv, n_ret = fcr.compute_rv_at_event(price_map, ev["timestamp_ms"])
            ev["rv_24h"] = rv
            ev["rv_n_returns"] = n_ret
            all_events.append(ev)

    # pooled cross-coin RV split
    rvs = sorted(e["rv_24h"] for e in all_events if e["rv_24h"] is not None)
    edges = _build_regime_edges_pooled(rvs, rv_split)
    _assign_rv_regimes_pooled(all_events, edges, rv_split)

    return {
        "arm": "B_ironflow_crosscoin_secondary",
        "coins": coins,
        "months": _ironflow_months(),
        "load_errors": load_errors,
        "per_coin": per_coin,
        "events": all_events,
        "cluster_key": "coin",
        "rv_split": rv_split,
        "rv_edges": edges,
        "percentiles": [p_low, p_high],
        "censor_hours": censor_hours,
    }


def run_arm_b(coins=None):
    """Frozen headline Arm B: [5,95] percentiles, 168h censor, pooled tercile."""
    fdf, cdf, coins = _load_arm_b_data(coins)
    return _run_arm_b_impl(fdf, cdf, coins, 5.0, 95.0, 168, "tercile")


# --------------------------------------------------------------------------- #
# Survival contrast (KM median, log-rank, cluster+block bootstrap, Holm)
# --------------------------------------------------------------------------- #
def _survival_records(events):
    recs = []
    for e in events:
        t = e["time_to_correction_hours"]
        c = bool(e["censored"])
        recs.append({
            "symbol": e["symbol"],
            "regime": e["rv_regime"],
            "side": e["side"],
            "t": t,
            "censored": c,
            "event_ts": e["timestamp_ms"],
        })
    return recs


def _month_of(ts_ms):
    dt = datetime.fromtimestamp(ts_ms / 1000.0, tz=timezone.utc)
    return dt.strftime("%Y-%m")


def _km_median(records):
    """Kaplan-Meier median for a list of (t, censored). Returns hours or None.

    None means the KM survival curve never drops to/below 0.5 within the
    observed (right-censored) follow-up — i.e. the median is not reached.
    """
    times = sorted(set(r["t"] for r in records if r["t"] is not None))
    n_total = len(records)
    if not times or n_total == 0:
        return None
    surv = 1.0
    at_risk = n_total
    for t in times:
        d = sum(1 for r in records if r["t"] == t and not r["censored"])
        c = sum(1 for r in records if r["t"] == t and r["censored"])
        if at_risk > 0:
            surv *= (1.0 - d / at_risk)
        if surv <= 0.5:
            return t
        at_risk -= (d + c)
        if at_risk <= 0:
            break
    return None


def _median(records):
    times = sorted(r["t"] for r in records if r["t"] is not None and not r["censored"])
    if not times:
        return None
    return times[len(times) // 2]


def _cluster_block_median_diff_ci(recs_high, recs_low, cluster_key="symbol",
                                  n_boot=BOOT_N, seed=SEED):
    """Cluster (per symbol/coin) + per-month block bootstrap 95% CI for
    median(high corrected) - median(low corrected)."""
    import random
    rng = random.Random(seed)
    if not recs_high or not recs_low:
        return None, None
    # Precompute clusters
    def clusters(recs):
        d = {}
        for r in recs:
            d.setdefault((r["symbol"], _month_of(r["event_ts"])), []).append(r)
        return list(d.values())

    # For cluster bootstrap: resample symbols (or coins) with replacement, then
    # resample months within each symbol with replacement.
    sym_recs_high = {}
    sym_recs_low = {}
    for r in recs_high:
        sym_recs_high.setdefault(r["symbol"], []).append(r)
    for r in recs_low:
        sym_recs_low.setdefault(r["symbol"], []).append(r)
    syms = sorted(set(sym_recs_high) | set(sym_recs_low))
    if len(syms) < 2:
        return None, None

    diffs = []
    for _ in range(n_boot):
        boot_syms = [rng.choice(syms) for _ in range(len(syms))]
        high_t = []
        low_t = []
        for s in boot_syms:
            for recs_map, out in ((sym_recs_high, high_t), (sym_recs_low, low_t)):
                base = recs_map.get(s, [])
                if not base:
                    continue
                months = {}
                for r in base:
                    months.setdefault(_month_of(r["event_ts"]), []).append(r)
                mkeys = list(months)
                if not mkeys:
                    continue
                chosen_months = [rng.choice(mkeys) for _ in mkeys]
                for m in chosen_months:
                    for r in months[m]:
                        if not r["censored"] and r["t"] is not None:
                            out.append(r["t"])
        high_t.sort(); low_t.sort()
        if not high_t or not low_t:
            continue
        diffs.append(high_t[len(high_t)//2] - low_t[len(low_t)//2])
    if len(diffs) < 10:
        return None, None
    diffs.sort()
    return diffs[int(0.025 * len(diffs))], diffs[int(0.975 * len(diffs))]


def _mean(records):
    times = [r["t"] for r in records if r["t"] is not None and not r["censored"]]
    return (sum(times) / len(times)) if times else None


def _primary_family(arm_events, cluster_key):
    """Pre-registered primary comparison family: pooled, positive, negative,
    per-symbol high-vs-low. Returns list of dicts with log-rank p."""
    recs = _survival_records(arm_events)
    families = []

    def compare(high, low, label):
        if not high or not low:
            return None
        high_pairs = [(r["t"], r["censored"]) for r in high if r["t"] is not None]
        low_pairs = [(r["t"], r["censored"]) for r in low if r["t"] is not None]
        if not high_pairs or not low_pairs:
            return None
        chi2, p = fcr.log_rank_test(high_pairs, low_pairs)
        km_hi = _km_median(high)
        km_lo = _km_median(low)
        med_hi = _median(high)
        med_lo = _median(low)
        mean_hi = _mean(high)
        mean_lo = _mean(low)
        ci_lo, ci_hi = _cluster_block_median_diff_ci(high, low, cluster_key)
        # Materiality anchor: KM median if reached, else corrected median.
        base_hi = km_hi if km_hi is not None else med_hi
        base_lo = km_lo if km_lo is not None else med_lo
        med_diff = (base_hi - base_lo) if (base_hi is not None and base_lo is not None) else None
        material = (
            med_diff is not None and base_hi is not None and base_lo is not None
            and abs(med_diff) >= 0.5 * min(base_hi, base_lo)
        )
        return {
            "label": label,
            "high_n": len(high_pairs),
            "low_n": len(low_pairs),
            "chi2": chi2,
            "p_two_sided": p,
            "km_median_high": km_hi,
            "km_median_low": km_lo,
            "median_high": med_hi,
            "median_low": med_lo,
            "mean_high": mean_hi,
            "mean_low": mean_lo,
            "materiality_base_high": base_hi,
            "materiality_base_low": base_lo,
            "median_diff": med_diff,
            "materiality_threshold": (0.5 * min(base_hi, base_lo)) if (base_hi is not None and base_lo is not None) else None,
            "material": material,
            "median_diff_ci": {"lo": ci_lo, "hi": ci_hi},
            "direction_lower_hazard_high_rv": (
                base_hi > base_lo) if (base_hi is not None and base_lo is not None) else None,
        }

    # pooled high vs low
    pooled = compare([r for r in recs if r["regime"] == "high"],
                     [r for r in recs if r["regime"] == "low"],
                     "pooled_high_vs_low")
    if pooled:
        families.append(pooled)
    # positive side high vs low
    pos = compare([r for r in recs if r["regime"] == "high" and r["side"] == "positive"],
                  [r for r in recs if r["regime"] == "low" and r["side"] == "positive"],
                  "positive_high_vs_low")
    if pos:
        families.append(pos)
    # negative side high vs low
    neg = compare([r for r in recs if r["regime"] == "high" and r["side"] == "negative"],
                  [r for r in recs if r["regime"] == "low" and r["side"] == "negative"],
                  "negative_high_vs_low")
    if neg:
        families.append(neg)
    # per-symbol high vs low
    symbols = sorted(set(r["symbol"] for r in recs))
    for s in symbols:
        sym = compare([r for r in recs if r["regime"] == "high" and r["symbol"] == s],
                      [r for r in recs if r["regime"] == "low" and r["symbol"] == s],
                      f"symbol_{s}_high_vs_low")
        if sym:
            families.append(sym)

    # Holm over the family (ignore comparisons with undefined p)
    valid = [f for f in families if f.get("p_two_sided") is not None]
    if valid:
        pvals = [f["p_two_sided"] for f in valid]
        adj = fcr.holm_bonferroni(pvals)
        for f, a in zip(valid, adj):
            f["p_adj_holm"] = a
    for f in families:
        f.setdefault("p_adj_holm", None)
    return families


def _sensitivity_grid():
    """Full frozen pre-registered sensitivity grid for both arms.

    Grid: percentiles [1,99],[5,95],[10,90] x censor [168,336]h x rv_split [tercile,median]
    = 12 cells per arm, 24 total. Headline [5,95]/168h/tercile is recomputed for
    reference but never used to select the headline. Reported only; no outcome
    peeking, no threshold tuning, no headline change.

    Data is loaded once per arm and reused across all 12 cells to avoid
    redundant I/O and parquet concatenation.
    """
    grid = []
    percentile_pairs = [(1.0, 99.0), (5.0, 95.0), (10.0, 90.0)]
    censor_hours_list = [168, 336]
    rv_splits = ["tercile", "median"]

    # Load Arm A data once (series + mark prices reused across all cells).
    aa_sym_series, aa_price_maps, aa_per_sym_month, aa_load_errors = _load_arm_a_data()
    # Load Arm B data once (parquet concat reused across all cells).
    ab_fdf, ab_cdf, ab_coins = _load_arm_b_data()

    for p_low, p_high in percentile_pairs:
        for censor_hours in censor_hours_list:
            for rv_split in rv_splits:
                cell = {
                    "percentiles": [p_low, p_high],
                    "censor_max_follow_hours": censor_hours,
                    "rv_split": rv_split,
                    "is_headline": (p_low == 5.0 and p_high == 95.0
                                    and censor_hours == 168 and rv_split == "tercile"),
                }
                # --- Arm A cell ---
                arm_a_cell = _run_arm_a_impl(aa_sym_series, aa_price_maps,
                                             aa_per_sym_month, aa_load_errors,
                                             p_low, p_high, censor_hours, rv_split)
                arm_a_families = _primary_family(arm_a_cell["events"],
                                                 arm_a_cell["cluster_key"])
                arm_a_pooled = next((f for f in arm_a_families
                                     if f["label"] == "pooled_high_vs_low"), None)
                cell["arm_a"] = {
                    "n_events": len(arm_a_cell["events"]),
                    "n_corrected": sum(1 for e in arm_a_cell["events"]
                                       if not e["censored"]),
                    "n_censored": sum(1 for e in arm_a_cell["events"]
                                      if e["censored"]),
                    "load_errors": arm_a_cell["load_errors"],
                    "primary_family": arm_a_families,
                    "pooled": arm_a_pooled,
                    "verdict": _verdict(arm_a_families, arm_a_pooled),
                    "regime_counts": _regime_counts(arm_a_cell["events"]),
                }
                # --- Arm B cell ---
                arm_b_cell = _run_arm_b_impl(ab_fdf, ab_cdf, ab_coins,
                                             p_low, p_high, censor_hours, rv_split)
                arm_b_families = _primary_family(arm_b_cell["events"],
                                                 arm_b_cell["cluster_key"])
                arm_b_pooled = next((f for f in arm_b_families
                                     if f["label"] == "pooled_high_vs_low"), None)
                cell["arm_b"] = {
                    "n_coins": len(arm_b_cell["coins"]),
                    "n_events": len(arm_b_cell["events"]),
                    "n_corrected": sum(1 for e in arm_b_cell["events"]
                                       if not e["censored"]),
                    "n_censored": sum(1 for e in arm_b_cell["events"]
                                      if e["censored"]),
                    "load_errors": arm_b_cell["load_errors"],
                    "primary_family": arm_b_families,
                    "pooled": arm_b_pooled,
                    "verdict": _verdict(arm_b_families, arm_b_pooled),
                    "regime_counts": _regime_counts(arm_b_cell["events"]),
                }
                grid.append(cell)

    return grid


# --------------------------------------------------------------------------- #
# Verdict
# --------------------------------------------------------------------------- #
def _verdict(families, pooled):
    if not pooled:
        return "INCONCLUSIVE"
    base_hi = pooled.get("materiality_base_high")
    base_lo = pooled.get("materiality_base_low")
    if base_hi is None or base_lo is None:
        return "UNDERPOWERED"
    ci = pooled.get("median_diff_ci") or {}
    p_adj = pooled.get("p_adj_holm")
    direction = base_hi > base_lo
    material = pooled.get("material", False)
    if direction and material and p_adj is not None and p_adj < 0.05:
        return "REPLICATES_DIRECTION"
    if direction and (p_adj is not None and p_adj < 0.05) and not material:
        return "TAIL_SHAPE_EFFECT"
    if p_adj is not None and p_adj >= 0.05:
        if ci.get("lo") is not None and ci.get("hi") is not None and ci["lo"] < 0 < ci["hi"]:
            return "UNDERPOWERED"
        return "NULL"
    return "INCONCLUSIVE"


# --------------------------------------------------------------------------- #
# Orchestration
# --------------------------------------------------------------------------- #
def execute(prereg_path=PREREG):
    prereg = json.loads(Path(prereg_path).read_text())
    out = {"prereg_id": prereg["prereg_id"], "frozen_at_utc": prereg["frozen_at_utc"]}

    arm_a = run_arm_a()
    out["arm_a"] = {
        "n_events": len(arm_a["events"]),
        "n_corrected": sum(1 for e in arm_a["events"] if not e["censored"]),
        "n_censored": sum(1 for e in arm_a["events"] if e["censored"]),
        "load_errors": arm_a["load_errors"],
        "per_symbol_month_funding_obs_summary": {
            s: {
                "months_with_data": sum(1 for v in m.values() if v > 0),
                "min_obs": min(m.values()) if m else 0,
                "max_obs": max(m.values()) if m else 0,
                "total": sum(m.values()),
            }
            for s, m in arm_a["per_symbol_month_funding_obs"].items()
        },
    }
    arm_a_families = _primary_family(arm_a["events"], arm_a["cluster_key"])
    out["arm_a"]["primary_family"] = arm_a_families
    pooled_a = next((f for f in arm_a_families if f["label"] == "pooled_high_vs_low"), None)
    out["arm_a"]["pooled"] = pooled_a
    out["arm_a"]["verdict"] = _verdict(arm_a_families, pooled_a)
    out["arm_a"]["regime_counts"] = _regime_counts(arm_a["events"])

    arm_b = run_arm_b()
    out["arm_b"] = {
        "n_coins": len(arm_b["coins"]),
        "n_events": len(arm_b["events"]),
        "n_corrected": sum(1 for e in arm_b["events"] if not e["censored"]),
        "n_censored": sum(1 for e in arm_b["events"] if e["censored"]),
        "load_errors": arm_b["load_errors"],
        "per_coin_summary_top": dict(sorted(
            arm_b["per_coin"].items(), key=lambda kv: kv[1]["events"], reverse=True)[:20]),
    }
    arm_b_families = _primary_family(arm_b["events"], arm_b["cluster_key"])
    out["arm_b"]["primary_family"] = arm_b_families
    pooled_b = next((f for f in arm_b_families if f["label"] == "pooled_high_vs_low"), None)
    out["arm_b"]["pooled"] = pooled_b
    out["arm_b"]["verdict"] = _verdict(arm_b_families, pooled_b)
    out["arm_b"]["regime_counts"] = _regime_counts(arm_b["events"])

    # Frozen pre-registered sensitivity grid (reported only; never used to
    # select the headline). No outcome peeking, no threshold tuning.
    out["sensitivity_grid"] = _sensitivity_grid()

    out["overall"] = {
        "arm_a_verdict": out["arm_a"]["verdict"],
        "arm_b_verdict": out["arm_b"]["verdict"],
        "class": "EXPLORATORY_ONLY",
        "promotable": False,
        "sealed_artifacts_mutated": False,
        "network_used": False,
    }
    return out, arm_a, arm_b


def _regime_counts(events):
    d = {}
    for e in events:
        rg = e["rv_regime"]
        x = d.setdefault(rg, {"n": 0, "corrected": 0, "censored": 0, "times": []})
        x["n"] += 1
        if e["censored"]:
            x["censored"] += 1
        else:
            x["corrected"] += 1
            x["times"].append(e["time_to_correction_hours"])
    for rg, x in d.items():
        recs = [{"t": t, "censored": False} for t in x["times"]]
        km = _km_median(recs)
        x["km_median_correction_hours"] = km
        ts = sorted(x.pop("times"))
        x["median_correction_hours"] = ts[len(ts)//2] if ts else None
        x["mean_correction_hours"] = (sum(ts)/len(ts)) if ts else None
    return d


def _write_md(result, arm_a, arm_b, out_dir):
    ts = datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines = []
    lines.append(f"# FCLR-SHEK-SCALE Evaluation Summary — {ts}\n")
    lines.append(f"**Prereg:** `{result['prereg_id']}` (frozen `{result['frozen_at_utc']}`)  ")
    lines.append(f"**Class:** EXPLORATORY_ONLY · promotable=false · sealed_mutated=false · network=false\n")
    lines.append("## Arm A — Binance (primary, independent of 2024-Q1)\n")
    a = result["arm_a"]
    lines.append(f"- Events: {a['n_events']} (corrected {a['n_corrected']}, censored {a['n_censored']})")
    lines.append(f"- Verdict: **{a['verdict']}**")
    p = a["pooled"] or {}
    lines.append(f"- Pooled high vs low: KM median {p.get('km_median_high')}h vs {p.get('km_median_low')}h; "
                 f"corrected median {p.get('median_high')}h vs {p.get('median_low')}h; "
                 f"mean {p.get('mean_high')}h vs {p.get('mean_low')}h")
    lines.append(f"- log-rank chi2={p.get('chi2')}, p={p.get('p_two_sided')}, Holm p={p.get('p_adj_holm')}")
    lines.append(f"- median diff (KM-anchored) = {p.get('median_diff')}h; materiality threshold = {p.get('materiality_threshold')}h; material = {p.get('material')}")
    ci = (p.get("median_diff_ci") or {})
    lines.append(f"- Median diff (high-low) 95% cluster+block CI: [{ci.get('lo')}, {ci.get('hi')}]\n")
    lines.append("### Regime counts\n")
    lines.append("| Regime | N | Corrected | Censored | KM median (h) | Corrected median (h) | Mean (h) |")
    lines.append("|---|---|---|---|---|---|---|")
    for rg, v in a["regime_counts"].items():
        lines.append(f"| {rg} | {v['n']} | {v['corrected']} | {v['censored']} | "
                     f"{v.get('km_median_correction_hours')} | {v.get('median_correction_hours')} | {v.get('mean_correction_hours')} |")
    lines.append("\n### Primary comparison family (Holm-adjusted)\n")
    lines.append("| Comparison | High N | Low N | KM hi | KM lo | Mean hi | Mean lo | p | Holm p | Material |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|")
    for f in a["primary_family"]:
        lines.append(f"| {f['label']} | {f['high_n']} | {f['low_n']} | {f['km_median_high']} | {f['km_median_low']} | "
                     f"{f.get('mean_high')} | {f.get('mean_low')} | {f['p_two_sided']} | {f['p_adj_holm']} | {f.get('material')} |")
    lines.append("\n## Arm B — ironflow cross-coin (secondary, never promotable)\n")
    b = result["arm_b"]
    lines.append(f"- Coins: {b['n_coins']}; events: {b['n_events']} (corrected {b['n_corrected']}, censored {b['n_censored']})")
    lines.append(f"- Verdict: **{b['verdict']}**")
    pb = b["pooled"] or {}
    lines.append(f"- Pooled high vs low: KM median {pb.get('km_median_high')}h vs {pb.get('km_median_low')}h; "
                 f"corrected median {pb.get('median_high')}h vs {pb.get('median_low')}h; mean {pb.get('mean_high')}h vs {pb.get('mean_low')}h")
    lines.append(f"- log-rank chi2={pb.get('chi2')}, p={pb.get('p_two_sided')}, Holm p={pb.get('p_adj_holm')}")
    lines.append(f"- median diff (KM-anchored) = {pb.get('median_diff')}h; material = {pb.get('material')}\n")
    lines.append("\n## Overall\n")
    lines.append(f"- Arm A verdict: **{result['overall']['arm_a_verdict']}**; Arm B verdict: **{result['overall']['arm_b_verdict']}**")
    lines.append("- This is an EXPLORATORY_ONLY partial replication; it never promotes H2, and correction time is not forecast skill or observed-liquidation prediction.\n")
    return "\n".join(lines)


def _cell_summary_line(arm_result, cell, side):
    p = (arm_result.get("pooled") or {})
    ci = (p.get("median_diff_ci") or {})
    return (f"  [{cell['percentiles'][0]},{cell['percentiles'][1]}]/"
            f"{cell['censor_max_follow_hours']}h/{cell['rv_split']}: "
            f"events={arm_result['n_events']} "
            f"(corrected={arm_result['n_corrected']}, censored={arm_result['n_censored']}) "
            f"KM med high={p.get('km_median_high')}h low={p.get('km_median_low')}h "
            f"chi2={p.get('chi2')} p={p.get('p_two_sided')} Holm p={p.get('p_adj_holm')} "
            f"med_diff={p.get('median_diff')}h material={p.get('material')} "
            f"verdict={arm_result['verdict']}")


def _write_sens_md(result, grid, out_dir):
    ts = datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines = []
    lines.append(f"# FCLR-SHEK-SCALE Sensitivity Grid — {ts}\n")
    lines.append(f"**Prereg:** `{result['prereg_id']}` (frozen `{result['frozen_at_utc']}`)  ")
    lines.append(f"**Class:** EXPLORATORY_ONLY · promotable=false · sealed_mutated=false · network=false\n")
    lines.append(f"**Grid:** percentiles [1,99],[5,95],[10,90] x censor [168,336]h x rv_split [tercile,median] = 12 cells x 2 arms = 24 cells\n")
    lines.append(f"**Headline cell:** [5,95]/168h/tercile (recomputed for reference, never used to select headline)\n")
    lines.append("---\n")
    lines.append("## Grid cells — Arm A (Binance, primary)\n")
    for cell in grid:
        a = cell["arm_a"]
        lines.append(_cell_summary_line(a, cell, "A"))
        lines.append(f"  CI: [{a['pooled']['median_diff_ci']['lo'] if a['pooled'] and a['pooled'].get('median_diff_ci') else None}, "
                     f"{a['pooled']['median_diff_ci']['hi'] if a['pooled'] and a['pooled'].get('median_diff_ci') else None}]\n")
    lines.append("\n## Grid cells — Arm B (ironflow, secondary, never promotable)\n")
    for cell in grid:
        b = cell["arm_b"]
        lines.append(_cell_summary_line(b, cell, "B"))
        lines.append(f"  CI: [{b['pooled']['median_diff_ci']['lo'] if b['pooled'] and b['pooled'].get('median_diff_ci') else None}, "
                     f"{b['pooled']['median_diff_ci']['hi'] if b['pooled'] and b['pooled'].get('median_diff_ci') else None}]\n")
    lines.append("## Consistency vs headline\n")
    headline = [c for c in grid if c["is_headline"]]
    if headline:
        h = headline[0]
        lines.append(f"- Arm A headline verdict: **{h['arm_a']['verdict']}** (sealed: TAIL_SHAPE_EFFECT)")
        lines.append(f"- Arm B headline verdict: **{h['arm_b']['verdict']}** (sealed: REPLICATES_DIRECTION)")
    lines.append("\nAll cells reported only; none used to select or tune the headline. EXPLORATORY_ONLY, promotable=false.\n")
    return "\n".join(lines)


GRID_CACHE = REPO / "research_state" / "fclr_shek_scale_grid_cache.pkl"


def _save_grid_cache(result, grid, ts):
    """Persist the heavy grid computation so a re-run can skip ~90 min of compute.

    The grid is the expensive part (24 cells x cluster+block bootstraps); if the
    markdown renderer crashes after compute, the work is not lost.
    """
    import pickle
    GRID_CACHE.parent.mkdir(parents=True, exist_ok=True)
    GRID_CACHE.write_bytes(pickle.dumps({"ts": ts, "result": result, "grid": grid}))


def _load_grid_cache():
    import pickle
    if not GRID_CACHE.exists():
        return None
    try:
        return pickle.loads(GRID_CACHE.read_bytes())
    except Exception:
        return None


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=None)
    ap.add_argument("--arm", choices=["a", "b", "both"], default="both")
    ap.add_argument("--no-write", action="store_true")
    ap.add_argument("--use-cache", action="store_true",
                    help="skip heavy grid compute and reuse research_state/fclr_shek_scale_grid_cache.pkl")
    args = ap.parse_args(argv)

    out_dir = Path(args.out) if args.out else REPO / "research_state"
    out_dir.mkdir(parents=True, exist_ok=True)

    prereg = json.loads(PREREG.read_text())
    ts = datetime.now(tz=timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    if args.use_cache:
        cached = _load_grid_cache()
        if not cached:
            raise SystemExit("grid cache missing; run without --use-cache first")
        result, grid = cached["result"], cached["grid"]
        arm_a, arm_b = None, None
        print(f"using grid cache ts={cached.get('ts')} n_cells={len(grid)}")
    else:
        result, arm_a, arm_b = execute()
        grid = result.get("sensitivity_grid", [])
        # Persist the durable JSON artifact FIRST, before any markdown rendering,
        # so a renderer crash cannot lose the heavy computation.
        sens_payload = json.dumps({
            "prereg_id": result["prereg_id"],
            "frozen_at_utc": result["frozen_at_utc"],
            "headline_cell": {"percentiles": [5.0, 95.0], "censor_max_follow_hours": 168, "rv_split": "tercile"},
            "grid_dimensions": {
                "percentiles": [[1.0, 99.0], [5.0, 95.0], [10.0, 90.0]],
                "censor_max_follow_hours": [168, 336],
                "rv_split": ["tercile", "median"],
            },
            "n_cells": len(grid),
            "grid": grid,
        }, indent=2, default=str)
        sens_json_path = out_dir / f"evaluation_summary_FCLR-SHEK-SCALE-SENS-{ts}.json"
        sens_json_path.write_text(sens_payload)
        print(f"wrote {sens_json_path}")
        _save_grid_cache(result, grid, ts)

    payload = json.dumps(result, indent=2, default=str)
    md = _write_md(result, arm_a, arm_b, out_dir)
    sens_payload = json.dumps({
        "prereg_id": result["prereg_id"],
        "frozen_at_utc": result["frozen_at_utc"],
        "headline_cell": {"percentiles": [5.0, 95.0], "censor_max_follow_hours": 168, "rv_split": "tercile"},
        "grid_dimensions": {
            "percentiles": [[1.0, 99.0], [5.0, 95.0], [10.0, 90.0]],
            "censor_max_follow_hours": [168, 336],
            "rv_split": ["tercile", "median"],
        },
        "n_cells": len(grid),
        "grid": grid,
    }, indent=2, default=str)
    sens_md = _write_sens_md(result, grid, out_dir)

    if args.no_write:
        print(payload)
        print("---SENS---")
        print(json.dumps({"n_cells": len(grid), "cells": [{"percentiles": c["percentiles"], "censor": c["censor_max_follow_hours"], "rv_split": c["rv_split"], "arm_a_verdict": c["arm_a"]["verdict"], "arm_b_verdict": c["arm_b"]["verdict"]} for c in grid]}, indent=2))
        return 0

    json_path = out_dir / f"evaluation_summary_FCLR-SHEK-SCALE-{ts}.json"
    md_path = out_dir / f"evaluation_summary_FCLR-SHEK-SCALE-{ts}.md"
    json_path.write_text(payload)
    md_path.write_text(md)

    sens_md_path = out_dir / f"evaluation_summary_FCLR-SHEK-SCALE-SENS-{ts}.md"
    sens_md_path.write_text(sens_md)
    print(f"wrote {json_path}")
    print(f"wrote {md_path}")
    print(f"wrote {sens_json_path}")
    print(f"wrote {sens_md_path}")
    print(f"arm_a verdict={result['arm_a']['verdict']}  arm_b verdict={result['arm_b']['verdict']}")
    print(f"sensitivity grid: {len(grid)} cells written")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())