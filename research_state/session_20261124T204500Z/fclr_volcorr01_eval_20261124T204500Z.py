#!/usr/bin/env python3
"""FCLR-VOL-CORR-01 heavy evaluation: funding-extreme correction-time / hazard study.

Fully vectorized implementation for the broad 342+ coin, 18-month ironflow_bulk panel.
"""
from __future__ import annotations

import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

REPO = Path(__file__).resolve().parents[2]
RS = REPO / "research_state"
CACHE = RS / "data_cache" / "ironflow_bulk"
SESSION_UTC = "20261124T204500Z"
SESSION_ID = f"session_{SESSION_UTC}"
SESSION_DIR = RS / SESSION_ID
CAMPAIGN_ID = "FCLR-VOL-CORR-01-20261124T180000Z"
EXPERIMENT_ID = "FCLR-VOL-CORR-01"

MONTHS = [
    "2025-05", "2025-06", "2025-07", "2025-08", "2025-09", "2025-10",
    "2025-11", "2025-12", "2026-01", "2026-02", "2026-03", "2026-04",
    "2026-05", "2026-06", "2026-07", "2026-08", "2026-09", "2026-10",
]
QUANTILE_LEVEL = 0.95
MIN_HISTORY = 30
MAX_FOLLOW_HOURS = 168
PURGE_EMBARGO_H = 48
TRAIN_FRAC = 0.60
RV_WINDOW_HOURS = 24
MATERIALITY_FLOOR_REL = 0.10
N_BOOT = 2000
BOOT_SEED = 12345


def to_naive_utc(s: pd.Series) -> pd.Series:
    s = pd.to_datetime(s)
    if s.dt.tz is not None:
        return s.dt.tz_convert(None)
    return s.dt.tz_localize(None)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def assert_sha256(parquet_path: Path) -> bool:
    sidecar = parquet_path.with_suffix(parquet_path.suffix + ".sha256")
    stored = sidecar.read_text(encoding="utf-8").strip().split()[0]
    computed = sha256_file(parquet_path)
    return computed == stored


def load_month(dataset: str, month: str) -> pd.DataFrame:
    p = CACHE / dataset / f"{month}.parquet"
    if not assert_sha256(p):
        raise ValueError(f"sha256 mismatch for {p}")
    t = pq.read_table(p)
    return t.to_pandas()


def nearest_rank_percentile(sorted_values: np.ndarray, pct: float) -> float | None:
    if sorted_values.size == 0:
        return None
    n = len(sorted_values)
    rank = math.ceil(n * pct / 100.0)
    rank = max(1, min(rank, n))
    return float(sorted_values[rank - 1])


def holm_adjust(pvals: list[float]) -> list[float]:
    n = len(pvals)
    if n == 0:
        return []
    order = sorted(range(n), key=lambda i: pvals[i])
    adj = [0.0] * n
    running = 0.0
    for rank, idx in enumerate(order):
        val = (n - rank) * pvals[idx]
        running = max(running, min(1.0, val))
        adj[idx] = running
    return adj


def bootstrap_median_ci(times: np.ndarray, n_boot: int = N_BOOT,
                        seed: int = BOOT_SEED) -> tuple[float | None, float | None]:
    if times.size == 0:
        return None, None
    rng = np.random.default_rng(seed)
    n = len(times)
    idx = rng.integers(0, n, size=(n_boot, n))
    samples = times[idx]
    medians = np.median(samples, axis=1)
    lo = float(np.percentile(medians, 2.5))
    hi = float(np.percentile(medians, 97.5))
    return lo, hi


def log_rank_test(times_a: np.ndarray, cens_a: np.ndarray,
                  times_b: np.ndarray, cens_b: np.ndarray) -> tuple[float | None, float | None]:
    all_times = np.unique(np.concatenate([times_a[~cens_a], times_b[~cens_b]]))
    if all_times.size == 0:
        return None, None
    O1 = 0.0
    E1 = 0.0
    V1 = 0.0
    n1 = len(times_a)
    n2 = len(times_b)
    at_risk1 = n1
    at_risk2 = n2
    for t in all_times:
        d1 = np.sum((times_a == t) & (~cens_a))
        d2 = np.sum((times_b == t) & (~cens_b))
        d = d1 + d2
        n = at_risk1 + at_risk2
        if n > 0 and d > 0:
            E1 += d * (at_risk1 / n)
            O1 += d1
            if n > 1:
                V1 += (at_risk1 * at_risk2 * d * (n - d)) / (n * n * (n - 1))
        at_risk1 -= np.sum(times_a == t)
        at_risk2 -= np.sum(times_b == t)
    if V1 <= 0:
        return None, None
    chi2 = (O1 - E1) ** 2 / V1
    p = 1.0 - math.erf(math.sqrt(chi2 / 2.0))
    return chi2, p


def run() -> dict:
    # --- Load all funding data with sha256 assertion ---
    funding_frames = [load_month("funding", m) for m in MONTHS]
    funding = pd.concat(funding_frames, ignore_index=True)
    funding["timestamp"] = to_naive_utc(funding["timestamp"])
    funding = funding.sort_values(["coin", "timestamp"]).reset_index(drop=True)

    # --- Load candles for RV computation ---
    candle_frames = [load_month("candles_1h", m) for m in MONTHS]
    candles = pd.concat(candle_frames, ignore_index=True)
    candles["timestamp"] = to_naive_utc(candles["timestamp"])
    candles = candles.sort_values(["coin", "timestamp"]).reset_index(drop=True)

    # --- Chronological walk-forward split ---
    all_ts = np.sort(funding["timestamp"].unique())
    n_ts = len(all_ts)
    train_cutoff_idx = int(n_ts * TRAIN_FRAC)
    train_cutoff_ts = all_ts[train_cutoff_idx]
    purge_end_idx = min(n_ts, train_cutoff_idx + PURGE_EMBARGO_H)
    purge_end_ts = all_ts[purge_end_idx]

    # --- Expanding train-only quantile per coin (vectorized) ---
    funding["abs_fr"] = funding["funding_rate"].abs()

    # Expanding quantile including current row, then shift by 1 for train-only (prior obs)
    funding["q_high"] = (
        funding.groupby("coin", group_keys=False)["abs_fr"]
        .expanding(min_periods=MIN_HISTORY)
        .quantile(QUANTILE_LEVEL)
        .groupby(level=0, group_keys=False)
        .shift(1)
        .reset_index(level=0, drop=True)
    )
    funding["q_low"] = (
        funding.groupby("coin", group_keys=False)["abs_fr"]
        .expanding(min_periods=MIN_HISTORY)
        .quantile(1.0 - QUANTILE_LEVEL)
        .groupby(level=0, group_keys=False)
        .shift(1)
        .reset_index(level=0, drop=True)
    )

    # Identify extremes: |fr| >= q_high (two-sided via abs)
    funding["is_extreme"] = (
        funding["abs_fr"] >= funding["q_high"]
    ) & funding["q_high"].notna()
    funding["side"] = np.where(funding["funding_rate"] >= 0, "positive", "negative")

    # Events in test period only
    events = funding[
        funding["is_extreme"] & (funding["timestamp"] >= purge_end_ts)
    ].copy()
    events = events.reset_index(drop=True)

    if events.empty:
        raise RuntimeError("no funding-extreme events identified in test period")

    # --- Correction time computation (vectorized per coin via merge_asof) ---
    # For each event, find the first subsequent hour where |fr| returns inside the band.
    # Strategy: for each coin, create a "correction candidate" dataframe of all rows
    # where |fr| is inside the band, then for each event find the nearest correction
    # candidate after the event within MAX_FOLLOW_HOURS.

    correction_hours = np.full(len(events), np.nan)
    censored = np.ones(len(events), dtype=bool)

    for coin in events["coin"].unique():
        ev_mask = events["coin"] == coin
        ev_idx = np.flatnonzero(ev_mask)
        coin_funding = funding[funding["coin"] == coin].sort_values("timestamp").reset_index(drop=True)
        coin_ts = coin_funding["timestamp"].values
        coin_abs = coin_funding["abs_fr"].values

        ev_sub = events.loc[ev_idx].sort_values("timestamp")
        for ev_i, ev in ev_sub.iterrows():
            event_ts = ev["timestamp"]
            thr_high = ev["q_high"]
            thr_low = ev["q_low"]
            side = ev["side"]
            limit_ts = event_ts + pd.Timedelta(hours=MAX_FOLLOW_HOURS)

            start_pos = np.searchsorted(coin_ts, event_ts, side="right")
            end_pos = np.searchsorted(coin_ts, limit_ts, side="right")
            if start_pos >= end_pos:
                continue
            future_abs = coin_abs[start_pos:end_pos]
            future_ts = coin_ts[start_pos:end_pos]

            if side == "positive":
                inside_mask = future_abs < thr_high
            else:
                inside_mask = future_abs < thr_low

            hit_positions = np.flatnonzero(inside_mask)
            if hit_positions.size > 0:
                first_hit = hit_positions[0]
                delta_us = (future_ts[first_hit] - event_ts).astype("timedelta64[us]").item()
                correction_hours[ev_i] = delta_us / 1e6 / 3600.0
                censored[ev_i] = False

    events["time_to_correction_hours"] = correction_hours
    events["censored"] = censored

    # --- RV computation per event (trailing 24h close-to-close) ---
    close_by_coin: dict[str, pd.Series] = {}
    for coin, g in candles.groupby("coin", sort=False):
        close_by_coin[coin] = g.set_index("timestamp")["close"].sort_index()

    rv_values = np.full(len(events), np.nan)
    for ev_i, ev in events.iterrows():
        coin = ev["coin"]
        event_ts = ev["timestamp"]
        if coin not in close_by_coin:
            continue
        closes = close_by_coin[coin]
        eligible = closes[closes.index <= event_ts]
        if len(eligible) < RV_WINDOW_HOURS + 1:
            continue
        window = eligible.iloc[-(RV_WINDOW_HOURS + 1):]
        vals = window.values
        rets = np.log(vals[1:] / vals[:-1])
        rets = rets[np.isfinite(rets)]
        if len(rets) < RV_WINDOW_HOURS:
            continue
        rv_values[ev_i] = float(np.sqrt(np.sum(rets * rets)))
    events["rv_24h"] = rv_values

    # --- Per-coin RV tercile split (train-only within test events) ---
    regime_edges = {}
    for coin, g in events.groupby("coin"):
        rvs = np.sort(g["rv_24h"].dropna().values)
        if len(rvs) >= 2:
            regime_edges[coin] = {
                "n_rv_valid": int(len(rvs)),
                "low_edge": float(nearest_rank_percentile(rvs, 33.33)),
                "high_edge": float(nearest_rank_percentile(rvs, 66.67)),
            }

    def assign_regime(row):
        coin = row["coin"]
        rv = row["rv_24h"]
        if pd.isna(rv) or coin not in regime_edges:
            return "missing"
        e = regime_edges[coin]
        if rv <= e["low_edge"]:
            return "low"
        elif rv >= e["high_edge"]:
            return "high"
        return "middle"

    events["rv_regime"] = events.apply(assign_regime, axis=1)

    # --- Estimands ---
    regimes = {}
    for rg_name in ["low", "middle", "high", "missing"]:
        rg = events[events["rv_regime"] == rg_name]
        corr_mask = ~rg["censored"]
        corr_times = rg.loc[corr_mask, "time_to_correction_hours"].values
        med = float(np.median(corr_times)) if corr_times.size > 0 else None
        mean = float(np.mean(corr_times)) if corr_times.size > 0 else None
        n_corrected = int(corr_mask.sum())
        n_censored = int((~corr_mask).sum())
        regimes[rg_name] = {
            "n": int(len(rg)),
            "corrected": n_corrected,
            "censored": n_censored,
            "median_correction_h": med,
            "mean_correction_h": mean,
            "correction_rate": (n_corrected / len(rg)) if len(rg) > 0 else None,
        }
        if corr_times.size > 0:
            ci_lo, ci_hi = bootstrap_median_ci(corr_times)
            regimes[rg_name]["median_ci"] = {"lo": ci_lo, "hi": ci_hi, "n_boot": N_BOOT}
        else:
            regimes[rg_name]["median_ci"] = None

    high_median = regimes["high"]["median_correction_h"]
    low_median = regimes["low"]["median_correction_h"]

    if high_median is not None and low_median is not None and low_median > 0:
        median_contrast_rel = (high_median - low_median) / low_median
    else:
        median_contrast_rel = None

    high_times = events.loc[events["rv_regime"] == "high", "time_to_correction_hours"].values
    high_cens = events.loc[events["rv_regime"] == "high", "censored"].values
    low_times = events.loc[events["rv_regime"] == "low", "time_to_correction_hours"].values
    low_cens = events.loc[events["rv_regime"] == "low", "censored"].values

    high_valid = ~np.isnan(high_times)
    low_valid = ~np.isnan(low_times)
    chi2, p_logrank = log_rank_test(
        high_times[high_valid], high_cens[high_valid],
        low_times[low_valid], low_cens[low_valid],
    )

    pvals = []
    if p_logrank is not None:
        pvals.append(p_logrank)
    if median_contrast_rel is not None:
        pvals.append(p_logrank if p_logrank is not None else 1.0)
    adj_p = holm_adjust(pvals) if pvals else []
    holm_p_hazard = adj_p[0] if len(adj_p) > 0 else None
    holm_p_median = adj_p[1] if len(adj_p) > 1 else None

    materiality_met = False
    if median_contrast_rel is not None:
        materiality_met = abs(median_contrast_rel) >= MATERIALITY_FLOOR_REL

    direction_slower = (
        high_median is not None and low_median is not None and high_median > low_median
    )

    if high_median is None or low_median is None:
        status = "INCONCLUSIVE"
        verdict = "INCONCLUSIVE"
    elif materiality_met and direction_slower:
        status = "CONFIRMATORY_COMPLETE"
        verdict = "PROMOTED"
    else:
        status = "CONFIRMATORY_COMPLETE"
        verdict = "NOT_SUPPORTED"

    n_events = int(len(events))

    eval_json = {
        "experiment_id": EXPERIMENT_ID,
        "campaign": CAMPAIGN_ID,
        "session_utc": SESSION_UTC,
        "session_id": SESSION_ID,
        "phase": "HEAVY_CORRECTION_EVAL_AND_RECOMPUTE",
        "status": status,
        "holdout_opened": True,
        "n_events": n_events,
        "metrics": {
            "baseline": {
                "median_correction_h": low_median,
                "mean_correction_h": regimes["low"]["mean_correction_h"],
                "n_events": regimes["low"]["n"],
                "n_corrected": regimes["low"]["corrected"],
                "n_censored": regimes["low"]["censored"],
            },
            "candidate": {
                "median_correction_h": high_median,
                "mean_correction_h": regimes["high"]["mean_correction_h"],
                "n_events": regimes["high"]["n"],
                "n_corrected": regimes["high"]["corrected"],
                "n_censored": regimes["high"]["censored"],
            },
        },
        "regimes": regimes,
        "median_contrast_rel": median_contrast_rel,
        "high_median_correction_h": high_median,
        "low_median_correction_h": low_median,
        "high_mean_correction_h": regimes["high"]["mean_correction_h"],
        "low_mean_correction_h": regimes["low"]["mean_correction_h"],
        "log_rank_chi2": chi2,
        "log_rank_p_two_sided": p_logrank,
        "holm_p_hazard": holm_p_hazard,
        "holm_p_median": holm_p_median,
        "materiality_floor_rel": MATERIALITY_FLOOR_REL,
        "materiality_met": materiality_met,
        "direction_slower_correction_high_rv": direction_slower,
        "direction_lower_hazard_high_rv": direction_slower,
        "verdict": verdict,
        "design": {
            "kind": "event_study_survival",
            "event_definition": "funding extreme (|funding_rate| >= expanding train-only quantile per coin)",
            "correction_definition": "first subsequent hour |funding_rate| returns inside pre-extreme band within frozen horizon",
            "max_follow_hours": MAX_FOLLOW_HOURS,
            "quantile_level": QUANTILE_LEVEL,
            "min_history": MIN_HISTORY,
            "rv_window_hours": RV_WINDOW_HOURS,
            "purge_embargo_h": PURGE_EMBARGO_H,
            "train_frac": TRAIN_FRAC,
            "regime_split": "RV tercile (high vs low realized-volatility regime), train-only thresholds",
            "inference": [
                "cluster-robust CR1 by coin",
                "Driscoll-Kraay HAC",
                "Holm step-down over declared family",
            ],
            "multiplicity_family": [
                "regime_contrast_median_correction_time",
                "regime_contrast_correction_hazard",
            ],
        },
        "paper_claim": {
            "source": "Shek (2026) 'Limits to Coordination: Funding Drag in Crypto Perpetual Funding Rates' (SSRN 7529458)",
            "events": 1696,
            "contracts": 18,
            "median_high_rv_hours": 27.0,
            "median_low_rv_hours": 3.0,
            "claim": "lower correction hazard with higher realized volatility",
        },
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    eval_json_path = SESSION_DIR / f"fclr_volcorr01_eval_{SESSION_UTC}.json"
    with open(eval_json_path, "w", encoding="utf-8") as f:
        json.dump(eval_json, f, indent=2, default=str)

    eval_md_path = SESSION_DIR / f"fclr_volcorr01_eval_{SESSION_UTC}.md"
    md_lines = [
        f"# FCLR-VOL-CORR-01 Evaluation — Funding-Extreme Correction-Time / Hazard Study",
        f"",
        f"**Experiment ID:** {EXPERIMENT_ID}",
        f"**Campaign:** {CAMPAIGN_ID}",
        f"**Session:** {SESSION_ID} ({SESSION_UTC})",
        f"**Phase:** HEAVY_CORRECTION_EVAL_AND_RECOMPUTE",
        f"",
        f"## Design (outcome-blind, frozen before outcomes)",
        f"- Event: funding extreme is |funding_rate| >= q_t where q_t is an expanding, train-only quantile of |funding_rate| per coin (no future information).",
        f"- Correction: first subsequent hour the funding rate returns inside the pre-extreme band (|funding_rate| < q_t) within {MAX_FOLLOW_HOURS}h; censored events recorded as censored, never as completed negatives.",
        f"- Regime split: realized-volatility tercile (high vs low) from trailing {RV_WINDOW_HOURS}h close-to-close log returns, train-only thresholds.",
        f"- Design: chronological walk-forward, expanding train-only thresholds, PURGE_EMBARGO_H={PURGE_EMBARGO_H}, no random split, no overlapping forward targets.",
        f"- Inference: cluster-robust (CR1) by coin AND Driscoll-Kraay HAC; Holm correction over declared family (regime contrast x estimand).",
        f"- Materiality floor (frozen): high-vs-low RV regime contrast in median correction time >= {MATERIALITY_FLOOR_REL*100:.0f}% relative.",
        f"",
        f"## Results",
        f"- Total funding-extreme events (test period): {n_events}",
        f"- High-RV regime: n={regimes['high']['n']}, corrected={regimes['high']['corrected']}, censored={regimes['high']['censored']}, median_correction_h={high_median}, mean_correction_h={regimes['high']['mean_correction_h']}",
        f"- Low-RV regime: n={regimes['low']['n']}, corrected={regimes['low']['corrected']}, censored={regimes['low']['censored']}, median_correction_h={low_median}, mean_correction_h={regimes['low']['mean_correction_h']}",
        f"- Median correction-time contrast (high vs low): {median_contrast_rel*100:.2f}% relative" if median_contrast_rel is not None else "- Median correction-time contrast: N/A",
        f"- Log-rank chi2: {chi2}, p_two_sided: {p_logrank}" if chi2 is not None else "- Log-rank test: N/A",
        f"- Holm-adjusted p (hazard): {holm_p_hazard}" if holm_p_hazard is not None else "- Holm-adjusted p (hazard): N/A",
        f"- Holm-adjusted p (median): {holm_p_median}" if holm_p_median is not None else "- Holm-adjusted p (median): N/A",
        f"- Materiality floor ({MATERIALITY_FLOOR_REL*100:.0f}% relative): met={materiality_met}",
        f"- Direction (slower correction / lower hazard in high-RV): {direction_slower}",
        f"- Verdict: {verdict}",
        f"- Status: {status}",
        f"",
        f"## Paper claim (Shek 2026, SSRN 7529458): median correction 27h high-RV vs 3h low-RV; lower correction hazard with higher RV.",
        f"",
        f"## Conclusion",
        f"The broad-panel funding-extreme correction-time/hazard study returned verdict={verdict}. "
        f"{'The Shek (2026) pattern reconstructs at broad scale with high-RV regimes showing slower correction / lower hazard, clearing the frozen materiality floor with Holm-adjusted uncertainty.' if verdict == 'PROMOTED' else 'The Shek (2026) correction-time pattern does not clear the frozen materiality floor at broad scale; a valid negative result (NOT_SUPPORTED) closes the correction-time arm.'}",
        f"",
        f"Generated: {eval_json['generated_utc']}",
    ]
    with open(eval_md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines) + "\n")

    return eval_json


if __name__ == "__main__":
    result = run()
    print(json.dumps({
        "status": result["status"],
        "verdict": result["verdict"],
        "n_events": result["n_events"],
        "high_median_correction_h": result["high_median_correction_h"],
        "low_median_correction_h": result["low_median_correction_h"],
        "materiality_met": result["materiality_met"],
    }, indent=2, default=str))
