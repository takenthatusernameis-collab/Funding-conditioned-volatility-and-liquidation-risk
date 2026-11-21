#!/usr/bin/env python3
"""
Independent stdlib/numpy recomputation of FCLR-LIQ-CONTAGION-001.

Recomputes the contagion headline from the frozen panel using a separate code
path from the eval script (direct pivot + numpy OLS Granger, distinct
aggregation implementation) and reports concurrence with the eval headline.
Read-only. No network. Panel sha256 asserted before any read.
"""

from __future__ import annotations

import hashlib
import json
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
N_PAIRS = N_COINS * (N_COINS - 1)
LAGS = 24
GRANGER_P = 6
ALPHA_BONF = 0.01 / N_PAIRS
MATERIALITY_FLOOR = 0.02
SEED = 20261121
RNG = np.random.default_rng(SEED)

OUT_DIR = RS / SESSION


def _sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _ols_granger_f(y: np.ndarray, x: np.ndarray, p: int):
    """Independent Granger F: unrestricted vs restricted AR(p), numpy lstsq."""
    n = len(y)
    if n <= 2 * p + 5:
        return np.nan, np.nan
    Y = y[p:]
    lagcols = []
    for i in range(1, p + 1):
        lagcols.append(np.column_stack([y[p - i:-i], x[p - i:-i]]))
    X_u = np.column_stack(lagcols)
    X_r = np.column_stack([y[p - i:-i] for i in range(1, p + 1)])
    m = np.all(np.isfinite(X_u), axis=1) & np.all(np.isfinite(X_r), axis=1) & np.isfinite(Y)
    Ym = Y[m]; Xu = X_u[m]; Xr = X_r[m]
    if len(Xu) <= 2 * p + 5:
        return np.nan, np.nan
    def rss(Xmat, Yvec):
        B, *_ = np.linalg.lstsq(np.column_stack([np.ones(len(Xmat)), Xmat]), Yvec, rcond=None)
        return float(np.sum((Yvec - np.column_stack([np.ones(len(Xmat)), Xmat]) @ B) ** 2))
    rss_u = rss(Xu, Ym); rss_r = rss(Xr, Ym)
    df_u = len(Ym) - 2 * p - 1
    if rss_u <= 0 or df_u <= 0:
        return np.nan, np.nan
    f_stat = ((rss_r - rss_u) / p) / (rss_u / df_u)
    return float(f_stat), float(f_stat)  # p handled by permutation below


def main() -> int:
    actual_sha = _sha256_file(PANEL_PATH)
    assert actual_sha == PANEL_SHA256, f"SHA256 mismatch: {actual_sha} != {PANEL_SHA256}"

    df = pd.read_parquet(PANEL_PATH)
    df = df[df["coin"].isin(COINS)].copy()
    df["hour"] = df["timestamp"].dt.floor("h")

    # Independent hourly aggregation: count + sum notional per (coin, hour).
    agg = (
        df.groupby(["coin", "hour"])
        .agg(n=("notional_usd", "size"), notional=("notional_usd", "sum"))
        .reset_index()
    )

    # Complete hourly grid per coin; zeros for missing hours.
    grids = {}
    for coin in COINS:
        sub = agg[agg["coin"] == coin].set_index("hour").sort_index()
        full = pd.date_range(sub.index.min(), sub.index.max(), freq="h")
        g = sub.reindex(full)
        g["n"] = g["n"].fillna(0.0)
        grids[coin] = g["n"].values.astype(float)
    index = grids[COINS[0]].__len__()  # placeholder
    hours = pd.date_range(
        min(agg["hour"]), max(agg["hour"]), freq="h"
    )
    wide = pd.DataFrame(index=hours, columns=COINS, dtype=float)
    for coin in COINS:
        sub = agg[agg["coin"] == coin].set_index("hour")[["n"]]
        wide[coin] = sub.reindex(hours)["n"].fillna(0.0)
    wide = wide.astype(float)

    # Lead-lag max |corr| and Granger per directed pair (independent loop).
    pair_rows = []
    for src in COINS:
        xs = wide[src].values
        for tgt in COINS:
            if src == tgt:
                continue
            ys = wide[tgt].values
            m = np.isfinite(xs) & np.isfinite(ys)
            if m.sum() < 2 * LAGS + 10:
                continue
            xv = xs[m]; yv = ys[m]
            n = len(xv)
            best_abs = 0.0
            for lag in range(1, LAGS + 1):
                a = xv[:n - lag]; b = yv[lag:]
                mm = np.isfinite(a) & np.isfinite(b)
                if mm.sum() < 10:
                    continue
                ca = a[mm] - a[mm].mean(); cb = b[mm] - b[mm].mean()
                den = np.sqrt(np.sum(ca * ca) * np.sum(cb * cb))
                c = float(np.sum(ca * cb) / den) if den > 0 else 0.0
                if abs(c) > best_abs:
                    best_abs = abs(c)
            f_stat, _ = _ols_granger_f(yv, xv, GRANGER_P)
            pair_rows.append({
                "src": src, "tgt": tgt,
                "max_abs_corr": best_abs,
                "granger_f": f_stat,
                "n_obs": int(n),
            })

    pair_df = pd.DataFrame(pair_rows)
    # Bonferroni + a bounded permutation on max |corr| for the headline.
    n_perm = 300
    perm_hits = {}
    for _, r in pair_df.iterrows():
        src = r["src"]; tgt = r["tgt"]
        xs = wide[src].values; ys = wide[tgt].values
        m = np.isfinite(xs) & np.isfinite(ys)
        xv = xs[m]; yv = ys[m]
        n = len(xv)
        obs = r["max_abs_corr"]
        hits = 0
        for _ in range(n_perm):
            xp = RNG.permutation(xv)
            ba = 0.0
            for lag in range(1, LAGS + 1):
                if n <= lag:
                    continue
                a = xp[:n - lag]; b = yv[lag:]
                mm = np.isfinite(a) & np.isfinite(b)
                if mm.sum() < 10:
                    continue
                ca = a[mm] - a[mm].mean(); cb = b[mm] - b[mm].mean()
                den = np.sqrt(np.sum(ca * ca) * np.sum(cb * cb))
                c = float(np.sum(ca * cb) / den) if den > 0 else 0.0
                if abs(c) > ba:
                    ba = abs(c)
            if ba >= obs:
                hits += 1
        perm_hits[(src, tgt)] = hits / n_perm
    pair_df["empirical_p"] = pair_df.apply(
        lambda r: perm_hits[(r["src"], r["tgt"])], axis=1
    )
    pair_df["edge_significant"] = (
        pair_df["granger_f"].notna() & (pair_df["empirical_p"] < ALPHA_BONF)
    )

    n_edges = int(pair_df["edge_significant"].sum())
    density = n_edges / N_PAIRS
    top = pair_df[pair_df["edge_significant"]].sort_values("granger_f", ascending=False).head(10)

    # Concurrence vs eval headline: eval found 11 edges, density 0.0524.
    eval_path = OUT_DIR / f"fclr_liq_contagion01_eval_{UTC_STAMP}.json"
    eval_concurs = False
    eval_edges = None; eval_density = None
    if eval_path.exists():
        ev = json.loads(eval_path.read_text())
        eval_edges = ev.get("final_edges")
        eval_density = ev.get("final_network_density")
        eval_concurs = bool(
            eval_edges == n_edges
            and abs(eval_density - density) < 1e-9
        )

    results = {
        "session_utc": UTC_STAMP,
        "experiment_id": f"FCLR-LIQ-CONTAGION-001-{UTC_STAMP}",
        "campaign": "FCLR-LIQ-CONTAGION-001",
        "method": "independent stdlib/numpy recompute (separate code path from eval)",
        "panel_path": str(PANEL_PATH),
        "panel_sha256": actual_sha,
        "panel_rows": int(len(df)),
        "n_coins": N_COINS,
        "n_pairs": N_PAIRS,
        "lags": LAGS,
        "granger_p": GRANGER_P,
        "n_permutations": int(n_perm),
        "alpha_bonferroni": ALPHA_BONF,
        "materiality_floor": MATERIALITY_FLOOR,
        "seed": SEED,
        "hourly_observations": int(wide.notna().sum().sum()),
        "n_edges": n_edges,
        "network_density": float(density),
        "eval_edges": eval_edges,
        "eval_density": eval_density,
        "recompute_concurs_with_eval": bool(eval_concurs),
        "top_edges": [
            {"src": r.src, "tgt": r.tgt, "granger_f": float(r.granger_f),
             "empirical_p": float(r.empirical_p)}
            for r in top.itertuples()
        ],
        "verdict": "CONCURS" if eval_concurs else "DISCREPANCY",
        "no_network": True,
        "no_paid_data": True,
        "no_credentials": True,
    }
    out = OUT_DIR / f"fclr_liq_contagion01_recompute_{UTC_STAMP}.json"
    with open(out, "w") as fh:
        json.dump(results, fh, indent=2, default=float)
    print(f"Wrote {out}")
    print(f"Recompute: {n_edges}/{N_PAIRS} edges, density={density:.4f}, "
          f"eval_edges={eval_edges}, eval_density={eval_density}, concurs={eval_concurs}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
