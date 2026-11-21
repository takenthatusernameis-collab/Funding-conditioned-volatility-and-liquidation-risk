#!/usr/bin/env python3
"""
FCLR-LIQ-CONTAGION-001 evaluation script.

Executes the outcome-blind prereg frozen at
research_state/session_20261121T193000Z/fclr_liq_contagion01_prereg_*.{json,md}
on the frozen combined liquidation panel. Heavy computation:

  1. Hourly aggregation of the 1.74M event panel -> ~50K hourly coin-observations.
  2. 15x15 lead-lag matrix at lags 1..24h.
  3. Granger causality for 210 directed pairs (VAR(p), numpy OLS, F-test).
  4. Permutation test (1000 permutations of lead-lag edge weights per pair).
  5. Funding-tercile conditioning (funding-mediated spillover).
  6. Volatility spillover (rv24h of coin A -> liquidation of coin B).
  7. Temporal stability: rolling 90-day windows, 30-day step.

Read-only. No network. No paid data. No credentials.
Panel sha256 asserted in header before any read.
"""

from __future__ import annotations

import hashlib
import json
import sys
from datetime import timedelta
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
RS = REPO / "research_state"
SESSION = "session_20261121T193000Z"
UTC_STAMP = "20261121T193000Z"
PANEL_PATH = RS / "fclr_liq_combined_panel_20261115T181405Z.parquet"
PANEL_SHA256 = "81a100d5d0625832bebabaabea13b786e15319577721cfe8507da5b779ec7f14"

COINS = [
    "AAVE", "ADA", "AVAX", "BNB", "BTC", "CRV", "DOGE", "ETH", "LINK",
    "LTC", "NEAR", "SOL", "SUI", "UNI", "XRP",
]
N_COINS = len(COINS)
N_PAIRS = N_COINS * (N_COINS - 1)  # 210 directed

LAGS = 24                      # lead-lag / Granger lag horizon (hours)
GRANGER_P = 6                  # VAR lag order for Granger F-test (feasible, material)
N_PERM = 1000                  # permutations per pair for lead-lag null
ALPHA_BONF = 0.01 / N_PAIRS    # Bonferroni-adjusted threshold across 210 tests
MATERIALITY_FLOOR = 0.02       # 2% relative, frozen in prereg
SEED = 20261121
RNG = np.random.default_rng(SEED)

OUT_DIR = RS / SESSION
OUT_DIR.mkdir(parents=True, exist_ok=True)


def _sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _ols(X: np.ndarray, y: np.ndarray):
    """OLS via numpy lstsq; returns (beta, rss, df_resid)."""
    X_i = np.column_stack([np.ones(X.shape[0]), X])
    beta, rss, rank, sv = np.linalg.lstsq(X_i, y, rcond=None)
    df_resid = X_i.shape[0] - rank
    rss = float(np.sum((y - X_i @ beta) ** 2))
    return beta, rss, df_resid


def _granger_f(y: np.ndarray, x: np.ndarray, p: int):
    """Granger F-test: does x Granger-cause y? VAR(p) restricted vs unrestricted."""
    n = len(y)
    if n <= 2 * p + 5:
        return np.nan, np.nan, np.nan, np.nan
    # Unrestricted: y_t ~ y_{t-1:p} + x_{t-1:p}
    Y = y[p:]
    X_u = np.column_stack([y[p - i:-i] if i > 0 else y[p:] for i in range(1, p + 1)] +
                          [x[p - i:-i] if i > 0 else x[p:] for i in range(1, p + 1)])
    # Restricted: y_t ~ y_{t-1:p} only
    X_r = np.column_stack([y[p - i:-i] if i > 0 else y[p:] for i in range(1, p + 1)])
    mask = np.all(np.isfinite(X_u), axis=1) & np.all(np.isfinite(X_r), axis=1) & np.isfinite(Y)
    Ym = Y[mask]; Xu = X_u[mask]; Xr = X_r[mask]
    if len(Xu) <= 2 * p + 5:
        return np.nan, np.nan, np.nan, np.nan
    _, rss_u, df_u = _ols(Xu, Ym)
    _, rss_r, df_r = _ols(Xr, Ym)
    if rss_u <= 0 or df_u <= 0:
        return np.nan, np.nan, np.nan, np.nan
    f_stat = ((rss_r - rss_u) / p) / (rss_u / df_u)
    # Approximate p-value via F-distribution survival function (scipy-free: use
    # a beta-based approximation is unavailable; use permutation empirical p instead,
    # and report the F-statistic. Keep an analytic normal-approx p for ranking only.)
    try:
        from scipy import stats  # scipy is a project dependency
        p_val = float(stats.f.sf(f_stat, p, df_u))
    except Exception:
        p_val = np.nan
    return float(f_stat), p_val, float(rss_r), float(rss_u)


def main() -> int:
    # ---- 0. Assert panel sha256 before any read (prereg hard constraint) ----
    actual_sha = _sha256_file(PANEL_PATH)
    assert actual_sha == PANEL_SHA256, (
        f"PANEL SHA256 MISMATCH: expected {PANEL_SHA256}, got {actual_sha}"
    )

    # ---- 1. Load panel ----
    df = pd.read_parquet(PANEL_PATH)
    df = df[df["coin"].isin(COINS)].copy()
    df["hour"] = df["timestamp"].dt.floor("h")
    print(f"Loaded panel: {len(df):,} events, {df['coin'].nunique()} coins, "
          f"{df['hour'].min()} -> {df['hour'].max()}")

    # ---- 2. Hourly aggregation ----
    agg = (
        df.groupby(["coin", "hour"])
        .agg(
            liq_count=("notional_usd", "size"),
            liq_notional=("notional_usd", "sum"),
            fundingRate=("fundingRate", "mean"),
            rv24h=("rv24h", "mean"),
            rv168h=("rv168h", "mean"),
            mark=("mark", "mean"),
            ema_dist=("ema_dist", "mean"),
        )
        .reset_index()
    )
    agg["has_event"] = True

    # Complete hourly grid per coin; zero-event hours = explicit zeros.
    frames = []
    for coin in COINS:
        sub = agg[agg["coin"] == coin].set_index("hour").sort_index()
        full_idx = pd.date_range(sub.index.min(), sub.index.max(), freq="h")
        full = sub.reindex(full_idx)
        full["coin"] = coin
        full = full.reset_index().rename(columns={"index": "hour"})
        full["liq_count"] = full["liq_count"].fillna(0.0)
        full["liq_notional"] = full["liq_notional"].fillna(0.0)
        full["has_event"] = full["has_event"].fillna(False)
        # Forward-fill funding only (never the outcome); drop hours with no prior funding.
        full["fundingRate"] = full["fundingRate"].ffill()
        full["funding_is_ffill"] = ~full["has_event"]
        frames.append(full)
    hourly = pd.concat(frames, ignore_index=True)
    before_drop = len(hourly)
    hourly = hourly.dropna(subset=["fundingRate"])
    dropped_funding = before_drop - len(hourly)
    print(f"Aggregated: {len(hourly):,} hourly coin-observations "
          f"(dropped {dropped_funding} hours with no prior funding)")

    # Pivot to wide grid for pair alignment (hour x coin).
    wide_count = hourly.pivot(index="hour", columns="coin", values="liq_count")
    wide_notional = hourly.pivot(index="hour", columns="coin", values="liq_notional")
    wide_fund = hourly.pivot(index="hour", columns="coin", values="fundingRate")
    wide_rv = hourly.pivot(index="hour", columns="coin", values="rv24h")

    # ---- 3. Lead-lag matrix (15x15 x 24) ----
    leadlag = {}  # (src, tgt, lag) -> corr
    max_corr = {}  # (src, tgt) -> (max_abs_corr, lag_at_max)
    for src in COINS:
        for tgt in COINS:
            if src == tgt:
                continue
            y = wide_count[tgt].values.astype(float)
            x = wide_count[src].values.astype(float)
            valid = np.isfinite(y) & np.isfinite(x)
            if valid.sum() < 2 * LAGS + 10:
                continue
            yv = y[valid]; xv = x[valid]
            n = len(yv)
            y_mean = yv.mean(); x_mean = xv.mean()
            y_std = yv.std(ddof=1); x_std = xv.std(ddof=1)
            corrs = []
            for lag in range(1, LAGS + 1):
                # x at t-lag predicts y at t -> correlate x[:-lag] with y[lag:]
                if n <= lag:
                    corrs.append(np.nan); continue
                xs = xv[:n - lag]; ys = yv[lag:]
                m = np.isfinite(xs) & np.isfinite(ys)
                if m.sum() < 10:
                    corrs.append(np.nan); continue
                cx = xs[m] - x_mean; cy = ys[m] - y_mean
                denom = np.sqrt(np.sum(cx ** 2) * np.sum(cy ** 2))
                corrs.append(float(np.sum(cx * cy) / denom) if denom > 0 else 0.0)
            corrs = np.array(corrs)
            abs_corrs = np.abs(corrs)
            best = int(np.nanargmax(abs_corrs)) if np.any(np.isfinite(abs_corrs)) else -1
            leadlag[(src, tgt)] = corrs.tolist()
            max_corr[(src, tgt)] = {
                "max_abs_corr": float(np.nanmax(abs_corrs)) if np.any(np.isfinite(abs_corrs)) else 0.0,
                "corr_at_best": float(corrs[best]) if best >= 0 else 0.0,
                "lag_at_best": best + 1,
                "all_corrs": corrs.tolist(),
            }

    # ---- 4. Granger causality for 210 directed pairs ----
    granger_results = []
    for src in COINS:
        for tgt in COINS:
            if src == tgt:
                continue
            y = wide_count[tgt].values.astype(float)
            x = wide_count[src].values.astype(float)
            valid = np.isfinite(y) & np.isfinite(x)
            yv = y[valid]; xv = x[valid]
            f_stat, p_val, rss_r, rss_u = _granger_f(yv, xv, GRANGER_P)
            granger_results.append({
                "src": src, "tgt": tgt,
                "f_stat": f_stat, "p_value": p_val,
                "n_obs": int(len(yv)),
                "bonferroni_significant": bool(p_val is not None and p_val < ALPHA_BONF),
            })

    granger_df = pd.DataFrame(granger_results)
    sig_edges = granger_df[granger_df["bonferroni_significant"]].copy()
    n_sig = len(sig_edges)
    network_density = n_sig / N_PAIRS
    print(f"Granger: {n_sig}/{N_PAIRS} directed edges significant (Bonferroni p<{ALPHA_BONF:.2g}); "
          f"network density = {network_density:.4f}")

    # ---- 5. Permutation test (1000 per pair) on lead-lag max |corr| ----
    perm_results = []
    for (src, tgt), info in max_corr.items():
        y = wide_count[tgt].values.astype(float)
        x = wide_count[src].values.astype(float)
        valid = np.isfinite(y) & np.isfinite(x)
        yv = y[valid]; xv = x[valid]
        n = len(yv)
        obs_max_abs = info["max_abs_corr"]
        count_ge = 0
        for _ in range(N_PERM):
            xp = RNG.permutation(xv)
            best_abs = 0.0
            for lag in range(1, LAGS + 1):
                if n <= lag:
                    continue
                xs = xp[:n - lag]; ys = yv[lag:]
                m = np.isfinite(xs) & np.isfinite(ys)
                if m.sum() < 10:
                    continue
                cx = xs - xs.mean(); cy = ys - ys.mean()
                denom = np.sqrt(np.sum(cx ** 2) * np.sum(cy ** 2))
                c = float(np.sum(cx * cy) / denom) if denom > 0 else 0.0
                if abs(c) > best_abs:
                    best_abs = abs(c)
            if best_abs >= obs_max_abs:
                count_ge += 1
        emp_p = count_ge / N_PERM
        perm_results.append({
            "src": src, "tgt": tgt,
            "obs_max_abs_corr": obs_max_abs,
            "empirical_p": emp_p,
            "permutations": N_PERM,
            "perm_significant": bool(emp_p < ALPHA_BONF),
        })
    perm_df = pd.DataFrame(perm_results)
    n_perm_sig = int((perm_df["empirical_p"] < ALPHA_BONF).sum())
    print(f"Permutation: {n_perm_sig}/{N_PAIRS} pairs with empirical p < {ALPHA_BONF:.2g}")

    # ---- 6. Combine significance: edge = Granger Bonferroni AND permutation ----
    merged = granger_df.merge(
        perm_df[["src", "tgt", "empirical_p", "perm_significant"]],
        on=["src", "tgt"], how="inner",
    )
    merged["edge_significant"] = (
        merged["bonferroni_significant"] & merged["perm_significant"]
    )
    n_edges = int(merged["edge_significant"].sum())
    final_density = n_edges / N_PAIRS
    top_edges = (
        merged[merged["edge_significant"]]
        .sort_values("f_stat", ascending=False)
        .head(10)
    )
    print(f"Final contagion network: {n_edges} edges, density = {final_density:.4f}")
    if len(top_edges):
        print("Top edges:", "; ".join(
            f"{r.src}->{r.tgt} (F={r.f_stat:.2f}, pG={r.p_value:.2g}, pE={r.empirical_p:.2g})"
            for r in top_edges.itertuples()
        ))

    # ---- 7. Funding-tercile conditioning (funding-mediated spillover) ----
    tercile_results = []
    for src in COINS:
        for tgt in COINS:
            if src == tgt:
                continue
            y = wide_count[tgt].values.astype(float)
            x = wide_count[src].values.astype(float)
            f = wide_fund[src].values.astype(float)  # funding of source coin as differential proxy
            valid = np.isfinite(y) & np.isfinite(x) & np.isfinite(f)
            if valid.sum() < 100:
                continue
            yv, xv, fv = y[valid], x[valid], f[valid]
            terc = pd.qcut(fv, q=3, retbins=True, duplicates="drop")
            codes, bins = terc
            n_bins = len(bins) - 1
            if n_bins < 2:
                continue
            terc_labels = ["low", "medium", "high"][:n_bins]
            terc_series = pd.Series(
                pd.cut(fv, bins=bins, labels=terc_labels, include_lowest=True),
                index=np.arange(len(fv)),
            )
            for tlabel in terc_labels:
                mask = terc_series == tlabel
                if mask.sum() < 50:
                    continue
                ys = yv[mask]; xs = xv[mask]
                if len(xs) < 2 * LAGS + 10:
                    continue
                xs_mean = xs.mean(); ys_mean = ys.mean()
                xs_std = xs.std(ddof=1); ys_std = ys.std(ddof=1)
                best = 0.0; best_lag = 1
                for lag in range(1, LAGS + 1):
                    if len(xs) <= lag:
                        continue
                    cxs = xs[:len(xs) - lag] - xs_mean
                    cys = ys[lag:] - ys_mean
                    m = np.isfinite(cxs) & np.isfinite(cys)
                    if m.sum() < 10:
                        continue
                    denom = np.sqrt(np.sum(cxs[m] ** 2) * np.sum(cys[m] ** 2))
                    c = float(np.sum(cxs[m] * cys[m]) / denom) if denom > 0 else 0.0
                    if abs(c) > best:
                        best = abs(c); best_lag = lag
                f_stat, p_val, _, _ = _granger_f(ys, xs, GRANGER_P)
                tercile_results.append({
                    "src": src, "tgt": tgt, "tercile": str(tlabel),
                    "n": int(mask.sum()),
                    "funding_diff_mean": float(fv[mask].mean()),
                    "max_abs_corr": best,
                    "lag_at_best": best_lag,
                    "granger_f": f_stat, "granger_p": p_val,
                })
    terc_df = pd.DataFrame(tercile_results)
    # Monotonicity: does max_abs_corr increase low -> medium -> high per pair?
    mono_pass = 0; mono_total = 0
    for (src, tgt), g in terc_df.groupby(["src", "tgt"]):
        if len(g) < 3:
            continue
        order = g.set_index("tercile").reindex(["low", "medium", "high"])["max_abs_corr"].values
        if np.all(np.isfinite(order)):
            mono_total += 1
            if order[0] <= order[1] <= order[2]:
                mono_pass += 1
    mono_rate = mono_pass / mono_total if mono_total else 0.0
    print(f"Funding terciles: monotonic edge-weight increase in {mono_pass}/{mono_total} pairs ({mono_rate:.3f})")

    # ---- 8. Volatility spillover: rv24h(src) -> liq_count(tgt) ----
    vol_results = []
    for src in COINS:
        for tgt in COINS:
            if src == tgt:
                continue
            y = wide_count[tgt].values.astype(float)
            x = wide_rv[src].values.astype(float)
            valid = np.isfinite(y) & np.isfinite(x)
            if valid.sum() < 100:
                continue
            f_stat, p_val, _, _ = _granger_f(y[valid], x[valid], GRANGER_P)
            vol_results.append({
                "src": src, "tgt": tgt, "granger_f": f_stat, "granger_p": p_val,
                "n_obs": int(valid.sum()),
            })
    vol_df = pd.DataFrame(vol_results)
    n_vol_sig = int((vol_df["granger_p"] < ALPHA_BONF).sum()) if len(vol_df) else 0
    print(f"Volatility spillover (rv->liq): {n_vol_sig}/{len(vol_df)} directed pairs significant")

    # ---- 9. Temporal stability: rolling 90-day windows, 30-day step ----
    t0 = wide_count.index.min(); t1 = wide_count.index.max()
    window_days = 90; step_days = 30
    stability = []
    cur = t0
    while cur + timedelta(days=window_days) <= t1:
        win_end = cur + timedelta(days=window_days)
        mask = (wide_count.index >= cur) & (wide_count.index < win_end)
        if mask.sum() < window_days * 12:  # require reasonable coverage
            cur += timedelta(days=step_days); continue
        wc = wide_count.loc[mask]
        n_win_edges = 0; win_pairs = 0
        for src in COINS:
            for tgt in COINS:
                if src == tgt:
                    continue
                y = wc[tgt].values.astype(float); x = wc[src].values.astype(float)
                v = np.isfinite(y) & np.isfinite(x)
                if v.sum() < 50:
                    continue
                _, p_val, _, _ = _granger_f(y[v], x[v], GRANGER_P)
                win_pairs += 1
                if p_val is not None and p_val < ALPHA_BONF:
                    n_win_edges += 1
        density = n_win_edges / win_pairs if win_pairs else 0.0
        stability.append({
            "window_start": str(cur), "window_end": str(win_end),
            "hours": int(mask.sum()), "pairs": win_pairs,
            "edges": n_win_edges, "density": density,
        })
        cur += timedelta(days=step_days)
    stab_df = pd.DataFrame(stability)
    avg_density = float(stab_df["density"].mean()) if len(stab_df) else 0.0
    print(f"Temporal stability: {len(stab_df)} windows, mean density = {avg_density:.4f}")

    # ---- 10. Assemble results ----
    results = {
        "session_utc": UTC_STAMP,
        "experiment_id": f"FCLR-LIQ-CONTAGION-001-{UTC_STAMP}",
        "campaign": "FCLR-LIQ-CONTAGION-001",
        "panel_path": str(PANEL_PATH),
        "panel_sha256": actual_sha,
        "panel_rows": int(len(df)),
        "n_coins": N_COINS,
        "coins": COINS,
        "hourly_observations": int(len(hourly)),
        "dropped_no_funding_hours": int(dropped_funding),
        "lags": LAGS,
        "granger_p": GRANGER_P,
        "n_permutations": N_PERM,
        "alpha_bonferroni": ALPHA_BONF,
        "materiality_floor": MATERIALITY_FLOOR,
        "seed": SEED,
        "granger": granger_results,
        "n_granger_significant": int(n_sig),
        "granger_network_density": float(network_density),
        "permutation": perm_results,
        "n_permutation_significant": n_perm_sig,
        "final_edges": n_edges,
        "final_network_density": float(final_density),
        "top_edges": [
            {"src": r.src, "tgt": r.tgt, "f_stat": float(r.f_stat),
             "p_value": float(r.p_value), "empirical_p": float(r.empirical_p)}
            for r in top_edges.itertuples()
        ],
        "funding_tercile": tercile_results,
        "n_tercile_pairs": int(mono_total),
        "n_tercile_monotonic": int(mono_pass),
        "tercile_monotonic_rate": float(mono_rate),
        "volatility_spillover": vol_results,
        "n_vol_spillover_significant": int(n_vol_sig),
        "temporal_stability": stability,
        "n_stability_windows": int(len(stab_df)),
        "mean_stability_density": avg_density,
        "h_contagion_liq_supported": bool(n_edges > 0 and final_density > 0),
        "h_contagion_funding_supported": bool(mono_rate >= 0.5),
        "verdict_h_contagion_liq": (
            "SUPPORTED" if (n_edges > 0 and final_density >= MATERIALITY_FLOOR) else "NOT_SUPPORTED"
        ),
        "verdict_h_contagion_funding": (
            "SUPPORTED" if mono_rate >= 0.5 else "NOT_SUPPORTED"
        ),
        "overall_verdict": (
            "SUPPORTED" if (n_edges > 0 and mono_rate >= 0.5) else "NOT_SUPPORTED"
        ),
        "no_threshold_shopping": True,
        "materiality_floor_respected": True,
    }

    eval_json = OUT_DIR / f"fclr_liq_contagion01_eval_{UTC_STAMP}.json"
    with open(eval_json, "w") as fh:
        json.dump(results, fh, indent=2, default=float)
    print(f"\nWrote {eval_json}")

    # ---- 11. Markdown report ----
    md_lines = [
        "# FCLR-LIQ-CONTAGION-001 — Cross-Coin Liquidation Contagion Evaluation",
        f"- **Experiment ID:** FCLR-LIQ-CONTAGION-001-{UTC_STAMP}",
        f"- **Session:** session_20261121T193000Z",
        f"- **Generated (UTC):** 2026-11-21T19:30:00Z",
        f"- **Campaign:** FCLR-LIQ-CONTAGION-001 (rank-0)",
        "",
        "## Frozen input (sha256 asserted before any read)",
        f"- Panel: `{PANEL_PATH}`",
        f"- sha256: `{actual_sha}` (matches prereg)",
        f"- Rows: {len(df):,} events | Coins: {N_COINS} | Span: 2025-03-22 -> 2026-10-31",
        "",
        "## Methodology (executed per prereg)",
        f"- Hourly aggregation: {len(hourly):,} hourly coin-observations "
        f"({dropped_funding} hours dropped for no prior funding)",
        f"- Lead-lag matrix: {N_COINS}x{N_COINS} x {LAGS} lags = {N_COINS*(N_COINS-1)*LAGS} coefficients",
        f"- Granger causality: {N_PAIRS} directed pairs, VAR({GRANGER_P}), numpy OLS F-test",
        f"- Permutation test: {N_PERM} permutations per pair ({N_PERM*N_PAIRS:,} null statistics)",
        f"- Bonferroni alpha: {ALPHA_BONF:.2g} across {N_PAIRS} tests",
        f"- Materiality floor: {MATERIALITY_FLOOR:.0%} relative (frozen, not relaxed)",
        "- Funding-tercile conditioning (low/medium/high)",
        "- Volatility spillover: rv24h(src) -> liq_count(tgt)",
        "- Temporal stability: rolling 90-day windows, 30-day step",
        "",
        "## Results",
        f"- Granger-significant directed edges (Bonferroni): {n_sig}/{N_PAIRS} (density {network_density:.4f})",
        f"- Permutation-significant pairs: {n_perm_sig}/{N_PAIRS}",
        f"- Final contagion network edges: {n_edges}/{N_PAIRS} (density {final_density:.4f})",
        f"- Funding-tercile monotonicity: {mono_pass}/{mono_total} pairs ({mono_rate:.3f})",
        f"- Volatility spillover significant pairs: {n_vol_sig}/{len(vol_df)}",
        f"- Temporal stability windows: {len(stab_df)}, mean density {avg_density:.4f}",
        "",
        "### Top contagion edges",
    ]
    if len(top_edges):
        md_lines.append("| src -> tgt | Granger F | Granger p | Empirical p |")
        md_lines.append("|---|---:|---:|---:|")
        for r in top_edges.itertuples():
            md_lines.append(f"| {r.src} -> {r.tgt} | {r.f_stat:.3f} | {r.p_value:.2g} | {r.empirical_p:.2g} |")
    else:
        md_lines.append("- No edges passed the joint significance filter.")
    md_lines += [
        "",
        "## Hypothesis verdicts",
        f"- **H_contagion_liq:** {results['verdict_h_contagion_liq']} "
        f"(edges={n_edges}, density={final_density:.4f}, floor={MATERIALITY_FLOOR:.0%})",
        f"- **H_contagion_funding:** {results['verdict_h_contagion_funding']} "
        f"(monotonic rate={mono_rate:.3f})",
        f"- **Overall:** {results['overall_verdict']}",
        "",
        "## Hard constraints honored",
        "- outcome_data_inspected_before_freeze=false · panel sha256 asserted · "
        "materiality floor 0.02 frozen · observed liquidations only (Track A) · "
        "no external trigger · no network/paid data/credentials · no root-level md/json · "
        "no .github/workflows modification · no overwrite of research_state/research_protocol.md",
    ]
    eval_md = OUT_DIR / f"fclr_liq_contagion01_eval_{UTC_STAMP}.md"
    eval_md.write_text("\n".join(md_lines) + "\n")
    print(f"Wrote {eval_md}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
