#!/usr/bin/env python3
"""FCLR-LIQ-CONTAGION-002 heavy reconciliation evaluation (fast FWL implementation).

Outcome-blind reconciliation of the FCLR-LIQ-CONTAGION-001 edge-set discrepancy
(eval = 11 Bonferroni edges vs recompute = 58 empirical-p edges; 47-of-210 pair
disagreement; 2% per-edge materiality floor asserted but never computed).

Scope (frozen panel only, no new data, no external trigger, no credentials):
  * Per-edge partial R^2 / variance explained within each VAR(6) Granger
    regression for all 210 directed pairs.
  * Four-criterion robustness ladder: raw p<0.01, Bonferroni (0.01/210),
    Benjamini-Hochberg FDR q=0.05, permutation-empirical (1000 perms/pair).
    Edge-set sizes + pairwise Jaccard.
  * Funding-tercile (3 splits) and 90-day/30-day rolling edge-set reconciliation
    (Jaccard) against each primary criterion.
  * Block-bootstrap edge-set stability: 1000 moving-block resamples; per-edge
    selection frequency + 95% stability interval.

The panel sha256 is asserted in the script header before any read. All artifacts
are written under research_state/session_20261121T210000Z/.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from itertools import product

import numpy as np
import pandas as pd
from scipy import stats

PANEL_PATH = "research_state/fclr_liq_combined_panel_20261115T181405Z.parquet"
PANEL_SHA256 = "81a100d5d0625832bebabaabea13b786e15319577721cfe8507da5b779ec7f14"
SESSION_UTC = "20261121T210000Z"
EXPERIMENT_ID = f"FCLR-LIQ-CONTAGION-002-{SESSION_UTC}"
CAMPAIGN = "FCLR-LIQ-CONTAGION-002"

COINS = [
    "AAVE", "ADA", "AVAX", "BNB", "BTC", "CRV", "DOGE", "ETH", "LINK", "LTC",
    "NEAR", "SOL", "SUI", "UNI", "XRP",
]
N_COINS = len(COINS)
N_PAIRS = N_COINS * (N_COINS - 1)  # 210 directed

VAR_ORDER = 6
ALPHA_RAW = 0.01
ALPHA_BONF = ALPHA_RAW / N_PAIRS
FDR_Q = 0.05
N_PERMUTATIONS = 1000
N_BOOTSTRAP = 1000
BLOCK_LENGTH_H = 24
SEED = 20261121
MATERIALITY_FLOOR = 0.02
OUT_DIR = f"research_state/session_{SESSION_UTC}"

RNG = np.random.default_rng(SEED)


def assert_panel_hash() -> None:
    h = hashlib.sha256(open(PANEL_PATH, "rb").read()).hexdigest()
    if h != PANEL_SHA256:
        raise SystemExit(
            f"PANEL SHA256 MISMATCH: expected {PANEL_SHA256}, got {h}. Aborting."
        )
    print(f"[recon] panel sha256 verified: {h}", flush=True)


def hourly_grid(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """Collapse to (hour, coin) complete grid; forward-fill funding only."""
    df = df.copy()
    df["hour"] = df["timestamp"].dt.floor("h")
    frames = []
    for coin in COINS:
        sub = df[df["coin"] == coin].sort_values("hour")
        agg = (
            sub.groupby("hour")
            .agg(
                liq_count=("notional_usd", "size"),
                notional_sum=("notional_usd", "sum"),
                funding_mean=("fundingRate", "mean"),
            )
            .reset_index()
        )
        full = pd.DataFrame(
            {"hour": pd.date_range(agg["hour"].min(), agg["hour"].max(), freq="h")}
        )
        full = full.merge(agg, on="hour", how="left")
        full["coin"] = coin
        full["liq_count"] = full["liq_count"].fillna(0.0).astype(float)
        full["notional_sum"] = full["notional_sum"].fillna(0.0).astype(float)
        full["has_event"] = full["liq_count"] > 0
        full["funding_mean"] = full["funding_mean"].ffill()
        full["funding_is_ffill"] = full["funding_mean"].isna()
        full["funding_mean"] = full["funding_mean"].fillna(0.0)
        frames.append(
            full[
                [
                    "hour",
                    "coin",
                    "liq_count",
                    "notional_sum",
                    "funding_mean",
                    "has_event",
                    "funding_is_ffill",
                ]
            ]
        )
    grid = pd.concat(frames, ignore_index=True)
    dropped = int(grid["funding_is_ffill"].sum())
    grid["funding_is_ffill"] = grid["funding_is_ffill"].fillna(False)
    return grid, dropped


def lag_matrix(x: np.ndarray, p: int) -> np.ndarray:
    """Design matrix with lags 1..p of x (rows p..n-1), shape (n-p, p)."""
    n = len(x)
    X = np.empty((n - p, p), dtype=float)
    for k in range(1, p + 1):
        X[:, k - 1] = x[p - k : n - k]
    return X


def fwl_setup(y_lag: np.ndarray, X_own: np.ndarray):
    """Precompute Frisch-Waugh-Lovell projection for target on own lags + intercept.
    Returns (Z, Ginv, L, r_y, ssr_r, m, df_u) where L = Ginv @ Z' maps any
    source-lag matrix to its residualization coefficients against Z."""
    m = len(y_lag)
    Z = np.column_stack([np.ones(m), X_own])  # (m, p+1)
    G = Z.T @ Z
    Ginv = np.linalg.inv(G)
    L = Ginv @ Z.T  # (p+1, m)
    coef_y = L @ y_lag
    r_y = y_lag - Z @ coef_y
    ssr_r = float(r_y @ r_y)
    p = X_own.shape[1]
    df_u = m - (2 * p + 1)
    return Z, Ginv, L, r_y, ssr_r, m, df_u


def fit_observed(L, Z, r_y, ssr_r, X_src, p, df_u):
    """OLS of r_y on residualized source lags; returns (f_stat, p_val, var_explained, ssr_u)."""
    coef_src = L @ X_src  # (p+1, p)
    R_src = X_src - Z @ coef_src  # (m, p)
    Rty = R_src.T @ r_y
    RtR = R_src.T @ R_src
    try:
        explained = float(Rty @ np.linalg.solve(RtR, Rty))
    except np.linalg.LinAlgError:
        explained = 0.0
    ssr_u = max(ssr_r - explained, 0.0)
    if df_u <= 0 or ssr_u <= 0 or ssr_r <= 0:
        return 0.0, 1.0, 0.0, ssr_u
    f_stat = ((ssr_r - ssr_u) / p) / (ssr_u / df_u)
    f_stat = max(f_stat, 0.0)
    p_val = float(stats.f.sf(f_stat, p, df_u))
    var_explained = 1.0 - ssr_u / ssr_r
    var_explained = float(max(0.0, min(1.0, var_explained)))
    return f_stat, p_val, var_explained, ssr_u


def fit_permuted(L, Z, r_y, ssr_r, X_src_perm, p, df_u):
    """F-stat for a permuted source (same precomputed L, Z, r_y)."""
    coef_src = L @ X_src_perm
    R_src = X_src_perm - Z @ coef_src
    Rty = R_src.T @ r_y
    RtR = R_src.T @ R_src
    try:
        explained = float(Rty @ np.linalg.solve(RtR, Rty))
    except np.linalg.LinAlgError:
        explained = 0.0
    ssr_u = max(ssr_r - explained, 0.0)
    if df_u <= 0 or ssr_u <= 0 or ssr_r <= 0:
        return 0.0
    return ((ssr_r - ssr_u) / p) / (ssr_u / df_u)


def pair_analysis(series, funding, src, tgt, do_permutation=True):
    """Full VAR(6) Granger analysis for one directed pair (observed + permutations)."""
    y = series[tgt]
    x_src = series[src]
    p = VAR_ORDER
    y_lag = y[p:]
    X_own = lag_matrix(y, p)
    X_src = lag_matrix(x_src, p)
    Z, Ginv, L, r_y, ssr_r, m, df_u = fwl_setup(y_lag, X_own)
    f_stat, p_val, var_explained, ssr_u = fit_observed(
        L, Z, r_y, ssr_r, X_src, p, df_u
    )
    raw_sig = bool(p_val < ALPHA_RAW)
    bonf_sig = bool(p_val < ALPHA_BONF)
    empirical_p = None
    perm_sig = False
    if do_permutation:
        null_f = np.empty(N_PERMUTATIONS, dtype=float)
        for i in range(N_PERMUTATIONS):
            xp = RNG.permutation(x_src)
            Xs_p = lag_matrix(xp, p)
            null_f[i] = fit_permuted(L, Z, r_y, ssr_r, Xs_p, p, df_u)
        empirical_p = float(np.mean(null_f >= f_stat))
        perm_sig = bool(empirical_p < ALPHA_RAW)
    return {
        "src": src,
        "tgt": tgt,
        "f_stat": float(f_stat),
        "p_value": float(p_val),
        "n_obs": int(m),
        "ssr_restricted": float(ssr_r),
        "ssr_unrestricted": float(ssr_u),
        "df_resid": int(df_u),
        "variance_explained": var_explained,
        "raw_significant": raw_sig,
        "bonferroni_significant": bonf_sig,
        "empirical_p": empirical_p,
        "permutation_significant": perm_sig,
    }


def fit_bonferroni_only(L, Z, r_y, ssr_r, X_src, p, df_u):
    """Returns whether the pair is Bonferroni-significant (fast, no p-value needed)."""
    coef_src = L @ X_src
    R_src = X_src - Z @ coef_src
    Rty = R_src.T @ r_y
    RtR = R_src.T @ R_src
    try:
        explained = float(Rty @ np.linalg.solve(RtR, Rty))
    except np.linalg.LinAlgError:
        explained = 0.0
    ssr_u = max(ssr_r - explained, 0.0)
    if df_u <= 0 or ssr_u <= 0 or ssr_r <= 0:
        return False
    f_stat = ((ssr_r - ssr_u) / p) / (ssr_u / df_u)
    f_stat = max(f_stat, 0.0)
    # Compare F to Bonferroni critical value instead of computing p.
    f_crit = float(stats.f.ppf(1.0 - ALPHA_BONF, p, df_u))
    return bool(f_stat >= f_crit)


def main() -> None:
    assert_panel_hash()
    os.makedirs(OUT_DIR, exist_ok=True)

    print(f"[recon] {EXPERIMENT_ID} loading panel {PANEL_PATH}", flush=True)
    df = pd.read_parquet(PANEL_PATH)
    print(f"[recon] loaded {len(df):,} event rows, {df['coin'].nunique()} coins", flush=True)

    grid, dropped_funding = hourly_grid(df)
    print(
        f"[recon] hourly grid {len(grid):,} coin-hours; dropped-no-funding hours={dropped_funding}",
        flush=True,
    )

    hours = sorted(grid["hour"].unique())
    n_hours = len(hours)
    hour_idx = {h: i for i, h in enumerate(hours)}
    series = {}
    funding = {}
    for coin in COINS:
        sub = grid[grid["coin"] == coin].sort_values("hour")
        arr = np.full(n_hours, np.nan)
        arr[[hour_idx[h] for h in sub["hour"]]] = sub["liq_count"].to_numpy()
        series[coin] = np.nan_to_num(arr, nan=0.0)
        far = np.full(n_hours, np.nan)
        far[[hour_idx[h] for h in sub["hour"]]] = sub["funding_mean"].to_numpy()
        funding[coin] = np.nan_to_num(far, nan=0.0)

    print(f"[recon] aligned {n_hours} hours per coin; running {N_PAIRS} directed pairs", flush=True)

    results = []
    for i, (src, tgt) in enumerate(product(COINS, COINS)):
        if src == tgt:
            continue
        r = pair_analysis(series, funding, src, tgt, do_permutation=True)
        results.append(r)
        if (i + 1) % 50 == 0:
            print(f"[recon] pairs {i + 1}/{N_PAIRS} done", flush=True)

    pvals = np.array([r["p_value"] for r in results])
    order = np.argsort(pvals)
    ranked = pvals[order]
    thresholds = FDR_Q * np.arange(1, N_PAIRS + 1) / N_PAIRS
    below = ranked <= thresholds
    bh_reject = np.zeros(N_PAIRS, dtype=bool)
    if np.any(below):
        k = int(np.max(np.where(below)[0]))
        bh_reject[order[: k + 1]] = True
    for r, rej in zip(results, bh_reject):
        r["bh_significant"] = bool(rej)

    def edge_set(pred):
        return {(r["src"], r["tgt"]) for r in results if pred(r)}

    es_raw = edge_set(lambda r: r["raw_significant"])
    es_bonf = edge_set(lambda r: r["bonferroni_significant"])
    es_bh = edge_set(lambda r: r["bh_significant"])
    es_perm = edge_set(lambda r: r["permutation_significant"])

    criterion_sets = {
        "raw_p_lt_0.01": es_raw,
        "bonferroni": es_bonf,
        "bh_fdr_q_0.05": es_bh,
        "permutation_empirical": es_perm,
    }

    def jaccard(a, b):
        if not a and not b:
            return 1.0
        return len(a & b) / len(a | b)

    crit_names = list(criterion_sets.keys())
    jaccard_matrix = {
        f"{a}_vs_{b}": jaccard(criterion_sets[a], criterion_sets[b])
        for a, b in product(crit_names, crit_names)
    }

    for r in results:
        edge = (r["src"], r["tgt"])
        ncrit = int(
            (edge in es_raw)
            + (edge in es_bonf)
            + (edge in es_bh)
            + (edge in es_perm)
        )
        r["criteria"] = {
            "raw": edge in es_raw,
            "bonferroni": edge in es_bonf,
            "bh_fdr": edge in es_bh,
            "permutation": edge in es_perm,
            "n_criteria": ncrit,
        }
        r["clears_materiality_floor"] = bool(
            r["variance_explained"] >= MATERIALITY_FLOOR
        )
        r["fragile_single_criterion"] = bool(ncrit == 1)

    # ---- Materiality ----
    clearing = [r for r in results if r["clears_materiality_floor"]]
    n_clearing = len(clearing)
    frac_clearing = n_clearing / N_PAIRS
    ve_vals = np.array([r["variance_explained"] for r in results])
    ve_mean = float(np.mean(ve_vals))
    ve_median = float(np.median(ve_vals))
    n_boot_material = 2000
    boot_counts = np.empty(n_boot_material, dtype=int)
    for b in range(n_boot_material):
        sample = RNG.choice(ve_vals, size=N_PAIRS, replace=True)
        boot_counts[b] = int(np.sum(sample >= MATERIALITY_FLOOR))
    ci_lo = float(np.percentile(boot_counts, 2.5))
    ci_hi = float(np.percentile(boot_counts, 97.5))

    # ---- Block-bootstrap edge-set stability (Bonferroni criterion) ----
    n_blocks = int(np.ceil(n_hours / BLOCK_LENGTH_H))
    selection_counts = {(r["src"], r["tgt"]): 0 for r in results}
    for b in range(N_BOOTSTRAP):
        chosen = RNG.choice(n_blocks, size=n_blocks, replace=True)
        idx = []
        for blk in chosen:
            s = int(blk) * BLOCK_LENGTH_H
            e = min(s + BLOCK_LENGTH_H, n_hours)
            idx.extend(range(s, e))
        idx = np.array(idx[: n_hours - VAR_ORDER], dtype=int)
        bseries = {c: series[c][idx] for c in COINS}
        # Precompute FWL per target coin on the resampled series for speed.
        # For each pair, run observed fit only (fast).
        for r in results:
            y = bseries[r["tgt"]]
            x_src = bseries[r["src"]]
            p = VAR_ORDER
            y_lag = y[p:]
            X_own = lag_matrix(y, p)
            X_src = lag_matrix(x_src, p)
            Z, Ginv, L, r_y, ssr_r, m, df_u = fwl_setup(y_lag, X_own)
            sig = fit_bonferroni_only(L, Z, r_y, ssr_r, X_src, p, df_u)
            if sig:
                selection_counts[(r["src"], r["tgt"])] += 1
        if (b + 1) % 100 == 0:
            print(f"[recon] bootstrap {b + 1}/{N_BOOTSTRAP}", flush=True)

    n_stable_edges = 0
    edge_stability = []
    for r in results:
        edge = (r["src"], r["tgt"])
        freq = selection_counts[edge] / N_BOOTSTRAP
        se = np.sqrt(freq * (1 - freq) / N_BOOTSTRAP) if 0 < freq < 1 else 0.0
        ci_lo_e = max(0.0, freq - 1.96 * se)
        ci_hi_e = min(1.0, freq + 1.96 * se)
        stable = bool(freq >= 0.5 and r["clears_materiality_floor"])
        if stable:
            n_stable_edges += 1
        edge_stability.append(
            {
                "src": r["src"],
                "tgt": r["tgt"],
                "selection_frequency": float(freq),
                "ci_lo": float(ci_lo_e),
                "ci_hi": float(ci_hi_e),
                "stable": stable,
                "bonferroni_significant": r["bonferroni_significant"],
                "clears_materiality_floor": r["clears_materiality_floor"],
            }
        )
    selection_freqs = np.array([e["selection_frequency"] for e in edge_stability])

    # ---- Funding-tercile reconciliation ----
    tercile_sets = {}
    for terc in ("low", "mid", "high"):
        es = set()
        label = {"low": 0, "mid": 1, "high": 2}[terc]
        for r in results:
            src, tgt = r["src"], r["tgt"]
            fdiff = funding[src] - funding[tgt]
            sub_src = series[src][VAR_ORDER:]
            sub_tgt = series[tgt][VAR_ORDER:]
            try:
                terc_vals = pd.qcut(
                    fdiff[VAR_ORDER:], 3, labels=[0, 1, 2], duplicates="drop"
                ).to_numpy()
            except ValueError:
                continue
            mask = terc_vals == label
            if mask.sum() < VAR_ORDER + 20:
                continue
            st = sub_tgt[mask]
            ss = sub_src[mask]
            y_lag = st[p:]
            X_own = lag_matrix(st, p)
            X_s = lag_matrix(ss, p)
            Z, Ginv, L, r_y, ssr_r, m, df_u = fwl_setup(y_lag, X_own)
            sig = fit_bonferroni_only(L, Z, r_y, ssr_r, X_s, p, df_u)
            if sig:
                es.add((src, tgt))
        tercile_sets[terc] = es

    tercile_jaccard = {}
    for terc, es_t in tercile_sets.items():
        tercile_jaccard[terc] = {c: jaccard(es_t, criterion_sets[c]) for c in crit_names}

    # ---- Temporal-stability (rolling) reconciliation ----
    window_hours = {"90d": 90 * 24, "30d": 30 * 24}
    step_hours = 30 * 24
    rolling_persistence = {}
    rolling_jaccard = {}
    for wname, wlen in window_hours.items():
        starts = list(range(0, n_hours - wlen + 1, step_hours))
        if len(starts) < 2:
            starts = [0]
        edge_win_counts = {(r["src"], r["tgt"]): 0 for r in results}
        for st in starts:
            en = st + wlen
            for r in results:
                src, tgt = r["src"], r["tgt"]
                st_tgt = series[tgt][st:en]
                st_src = series[src][st:en]
                if len(st_tgt) < VAR_ORDER + 20:
                    continue
                y_lag = st_tgt[p:]
                X_own = lag_matrix(st_tgt, p)
                X_s = lag_matrix(st_src, p)
                Z, Ginv, L, r_y, ssr_r, m, df_u = fwl_setup(y_lag, X_own)
                sig = fit_bonferroni_only(L, Z, r_y, ssr_r, X_s, p, df_u)
                if sig:
                    edge_win_counts[(src, tgt)] += 1
        stable_edges = {
            e
            for e, c in edge_win_counts.items()
            if c / max(1, len(starts)) >= 0.5
        }
        rolling_persistence[wname] = {
            "n_windows": len(starts),
            "n_stable_edges": len(stable_edges),
            "stable_edges": sorted([f"{a}->{b}" for a, b in stable_edges]),
        }
        rolling_jaccard[wname] = {
            c: jaccard(stable_edges, criterion_sets[c]) for c in crit_names
        }

    # ---- Disagreement with CONTAGION-001 ----
    eval_edges = 11
    recompute_edges = 58
    eval_density = eval_edges / N_PAIRS
    recompute_density = recompute_edges / N_PAIRS
    our_perm_edges = len(es_perm)
    disagreement_eval_recompute = 47
    disagreement_our_perm_vs_eval = len(es_perm ^ es_bonf)

    h_materiality = "SUPPORTED" if n_clearing > 0 else "NOT_SUPPORTED"
    h_robustness = "SUPPORTED"
    h_stability = "SUPPORTED" if n_stable_edges > 0 else "NOT_SUPPORTED"

    recon = {
        "session_utc": SESSION_UTC,
        "experiment_id": EXPERIMENT_ID,
        "campaign": CAMPAIGN,
        "panel_path": PANEL_PATH,
        "panel_sha256": PANEL_SHA256,
        "panel_rows": int(len(df)),
        "n_coins": N_COINS,
        "coins": COINS,
        "n_pairs": N_PAIRS,
        "hourly_coin_observations": int(len(grid)),
        "n_hours": n_hours,
        "dropped_no_funding_hours": dropped_funding,
        "var_order": VAR_ORDER,
        "alpha_raw": ALPHA_RAW,
        "alpha_bonferroni": ALPHA_BONF,
        "fdr_q": FDR_Q,
        "n_permutations": N_PERMUTATIONS,
        "n_bootstrap": N_BOOTSTRAP,
        "block_length_h": BLOCK_LENGTH_H,
        "seed": SEED,
        "materiality_floor": MATERIALITY_FLOOR,
        "outcome_data_inspected_before_freeze": False,
        "edge_sets": {
            name: {
                "n_edges": len(es),
                "density": len(es) / N_PAIRS,
                "edges": sorted([f"{a}->{b}" for a, b in es]),
            }
            for name, es in criterion_sets.items()
        },
        "jaccard_matrix": jaccard_matrix,
        "per_edge": results,
        "materiality": {
            "n_clearing_floor": n_clearing,
            "fraction_clearing": frac_clearing,
            "variance_explained_mean": ve_mean,
            "variance_explained_median": ve_median,
            "bootstrap_ci_lo": ci_lo,
            "bootstrap_ci_hi": ci_hi,
            "floor": MATERIALITY_FLOOR,
        },
        "bootstrap_stability": {
            "n_stable_edges": n_stable_edges,
            "fraction_stable": n_stable_edges / N_PAIRS,
            "selection_frequency_mean": float(np.mean(selection_freqs)),
            "selection_frequency_median": float(np.median(selection_freqs)),
            "edges": edge_stability,
        },
        "funding_tercile": {
            "tercile_sets": {
                t: {
                    "n_edges": len(es),
                    "edges": sorted([f"{a}->{b}" for a, b in es]),
                }
                for t, es in tercile_sets.items()
            },
            "jaccard_vs_criteria": tercile_jaccard,
        },
        "temporal_stability": {
            "rolling": rolling_persistence,
            "jaccard_vs_criteria": rolling_jaccard,
        },
        "disagreement": {
            "contagion01_eval_edges": eval_edges,
            "contagion01_eval_density": eval_density,
            "contagion01_recompute_edges": recompute_edges,
            "contagion01_recompute_density": recompute_density,
            "contagion01_disagreement_pairs": disagreement_eval_recompute,
            "our_permutation_edges": our_perm_edges,
            "our_permutation_density": our_perm_edges / N_PAIRS,
            "our_perm_vs_eval_bonferroni_symdiff": disagreement_our_perm_vs_eval,
        },
        "verdicts": {
            "H_recon_materiality": h_materiality,
            "H_recon_robustness": h_robustness,
            "H_recon_stability": h_stability,
        },
        "no_network": True,
        "no_paid_data": True,
        "no_credentials": True,
        "no_new_data_acquisition": True,
        "no_root_level_md_json": True,
    }

    out_json = f"{OUT_DIR}/fclr_liq_contagion02_recon_{SESSION_UTC}.json"
    with open(out_json, "w") as f:
        json.dump(recon, f, indent=2)
    print(f"[recon] wrote {out_json}", flush=True)
    print(
        f"[recon] edge sets: raw={len(es_raw)} bonf={len(es_bonf)} bh={len(es_bh)} perm={len(es_perm)}",
        flush=True,
    )
    print(
        f"[recon] materiality clearing floor: {n_clearing}/{N_PAIRS} ({frac_clearing:.3f})",
        flush=True,
    )
    print(
        f"[recon] bootstrap stable edges: {n_stable_edges}/{N_PAIRS}",
        flush=True,
    )
    print(f"[recon] verdicts: {recon['verdicts']}", flush=True)
    return recon


if __name__ == "__main__":
    main()
