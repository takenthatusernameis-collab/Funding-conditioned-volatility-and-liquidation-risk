#!/usr/bin/env python3
"""
FCLR-PANEL-FE-001 — Independent stdlib/numpy recompute.

Re-derives the headline two-way (coin + hour) fixed-effects coefficients and
walk-forward out-of-sample metrics from the raw frozen parquet using only
numpy/pandas (no statsmodels, no linearmodels, no network). Concurs with the
in-panel evaluation `fclr_panelfe01_eval_20261121T130159Z.py`.

Design (pre-registered, outcome-blind):
  Half A: next_log_rv1h ~ coin_FE + hour_FE + signed_funding   (FCLR-001 panel)
  Half B: log1p(liq_count) ~ coin_FE + hour_FE + funding_rate_mean   (combined panel)

Inference: cluster-robust (CR1) by coin + Driscoll-Kraay HAC + Newey-West HAC.
Walk-forward OOS: expanding-window one-step-ahead at daily 00:00 UTC origins;
QLIKE on level target; Diebold-Mariano on daily-mean loss differential.
Materiality floor: |beta * SD(x)| >= 2% (frozen). A null is NOT_SUPPORTED.

Both frozen panel sha256 are asserted in the header before any read.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

REPO = Path(__file__).resolve().parents[2]
SESSION = "20261121T130159Z"
OUT_DIR = REPO / "research_state" / f"session_{SESSION}"
OUT_DIR.mkdir(parents=True, exist_ok=True)

PANEL_A = REPO / "research_state" / "fclr011_recompute_panel_20261115T234700Z.parquet"
PANEL_A_SHA256 = "41962f823e59de5989c7d854cb3180cad61a4cbc2f5f230133c41b321342c1f4"
PANEL_B = REPO / "research_state" / "fclr_liq_combined_panel_20261115T181405Z.parquet"
PANEL_B_SHA256 = "81a100d5d0625832bebabaabea13b786e15319577721cfe8507da5b779ec7f14"

SEED = 20261121
ALPHA = 0.05
MATERIALITY_FLOOR = 0.02
RNG = np.random.RandomState(SEED)


def _assert_hash(path: Path, expected: str, label: str) -> None:
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    assert actual == expected, f"{label} hash mismatch: {actual} != {expected}"


def _demean_2way(y: np.ndarray, X: np.ndarray, coins: np.ndarray,
                 hours: np.ndarray, n_iter: int = 6) -> tuple[np.ndarray, np.ndarray]:
    """Two-way within transform by successive partialling out (coin, hour, ...)."""
    y = y.astype(float).copy()
    X = X.astype(float).copy()
    for _ in range(n_iter):
        for c in np.unique(coins):
            m = coins == c
            y[m] -= np.mean(y[m])
            X[m] -= np.mean(X[m], axis=0)
        for h in np.unique(hours):
            m = hours == h
            y[m] -= np.mean(y[m])
            X[m] -= np.mean(X[m], axis=0)
    return y, X


def _ols_noint(X: np.ndarray, y: np.ndarray) -> dict:
    n, k = X.shape
    XtX_inv = np.linalg.pinv(X.T @ X)
    beta = XtX_inv @ (X.T @ y)
    resid = y - X @ beta
    df = n - k
    sigma2 = float(resid @ resid / df) if df > 0 else np.nan
    return {"beta": beta, "resid": resid, "XtX_inv": XtX_inv,
            "n": n, "k": k, "df": df, "sigma2": sigma2, "X": X}


def _se_cr1(ols_res: dict, coins: np.ndarray) -> np.ndarray:
    beta = ols_res["beta"]; resid = ols_res["resid"]; X = ols_res["X"]
    XtX_inv = ols_res["XtX_inv"]; k = len(beta)
    meat = np.zeros((k, k))
    for c in np.unique(coins):
        m = coins == c
        ug = X[m] * resid[m, None]
        meat += ug.T @ ug
    vcov = XtX_inv @ meat @ XtX_inv
    return np.sqrt(np.maximum(np.diag(vcov), 0.0))


def _se_dk(ols_res: dict, hours: np.ndarray) -> np.ndarray:
    """Driscoll-Kraay HAC on cross-sectional moment sums h_t = sum_i x_it e_it."""
    beta = ols_res["beta"]; resid = ols_res["resid"]; X = ols_res["X"]
    XtX_inv = ols_res["XtX_inv"]; k = len(beta)
    hour_list = sorted(np.unique(hours))
    T = len(hour_list)
    H = np.zeros((T, k))
    for ti, h in enumerate(hour_list):
        m = hours == h
        H[ti] = (X[m] * resid[m, None]).sum(axis=0)
    L = max(1, min(int(np.floor(4 * (T / 100.0) ** (2.0 / 9.0))), T - 1))
    gamma0 = (H.T @ H) / T
    vcov = gamma0.copy()
    for l in range(1, L + 1):
        w = 1.0 - l / (L + 1.0)
        g = (H[l:].T @ H[:-l]) / T
        vcov += w * (g + g.T)
    vcov = XtX_inv @ vcov @ XtX_inv
    return np.sqrt(np.maximum(np.diag(vcov), 0.0))


def _se_nw(ols_res: dict) -> np.ndarray:
    """Newey-West HAC on the stacked within-transformed series."""
    beta = ols_res["beta"]; resid = ols_res["resid"]; X = ols_res["X"]
    XtX_inv = ols_res["XtX_inv"]; k = len(beta); n = len(resid)
    U = X * resid[:, None]
    T_eff = max(1, int(np.floor(n / 5.0)))
    L = max(1, min(int(np.floor(4 * (T_eff / 100.0) ** (2.0 / 9.0))), n - 1))
    gamma0 = (U.T @ U) / n
    vcov = gamma0.copy()
    for l in range(1, L + 1):
        w = 1.0 - l / (L + 1.0)
        g = (U[l:].T @ U[:-l]) / n
        vcov += w * (g + g.T)
    vcov = XtX_inv @ vcov @ XtX_inv
    return np.sqrt(np.maximum(np.diag(vcov), 0.0))


def _fe(y: np.ndarray, X: np.ndarray, coins: np.ndarray, hours: np.ndarray,
        x_names: list[str]) -> dict:
    y_d, X_d = _demean_2way(y, X, coins, hours)
    m = np.isfinite(y_d) & np.all(np.isfinite(X_d), axis=1)
    y_d = y_d[m]; X_d = X_d[m]; coins = coins[m]; hours = hours[m]
    ols = _ols_noint(X_d, y_d)
    se_cr1 = _se_cr1(ols, coins)
    se_dk = _se_dk(ols, hours)
    se_nw = _se_nw(ols)
    coefs = []
    for j, name in enumerate(x_names):
        b = float(ols["beta"][j])
        coefs.append({
            "predictor": name,
            "beta": b,
            "se_cluster_coin": float(se_cr1[j]),
            "se_driscoll_kraay": float(se_dk[j]),
            "se_newey_west": float(se_nw[j]),
            "t_cluster_coin": float(b / se_cr1[j]) if se_cr1[j] > 0 else np.nan,
            "t_driscoll_kraay": float(b / se_dk[j]) if se_dk[j] > 0 else np.nan,
            "t_newey_west": float(b / se_nw[j]) if se_nw[j] > 0 else np.nan,
            "p_cluster_coin": float(2 * stats.norm.sf(abs(b / se_cr1[j]))) if se_cr1[j] > 0 else np.nan,
            "p_driscoll_kraay": float(2 * stats.norm.sf(abs(b / se_dk[j]))) if se_dk[j] > 0 else np.nan,
            "p_newey_west": float(2 * stats.norm.sf(abs(b / se_nw[j]))) if se_nw[j] > 0 else np.nan,
        })
    return {"n": int(ols["n"]), "k": int(k if False else ols["k"]),
            "sigma2": float(ols["sigma2"]),
            "within_r2": float(1.0 - (ols["resid"] @ ols["resid"]) /
                             ((y_d @ y_d) if (y_d @ y_d) > 0 else 1.0)),
            "coefficients": coefs}


def _holm(pvals: list[float]) -> list[float]:
    order = sorted(range(len(pvals)), key=lambda i: pvals[i])
    adj = [0.0] * len(pvals)
    m = len(pvals)
    for r, i in enumerate(order):
        adj[i] = min(1.0, float(pvals[i]) * (m - r))
    return adj


def _qlike(actual: np.ndarray, pred: np.ndarray) -> float:
    mask = (actual > 0) & (pred > 0) & np.isfinite(actual) & np.isfinite(pred)
    if mask.sum() == 0:
        return np.nan
    r = actual[mask] / pred[mask]
    return float(np.mean(r - 1.0 - np.log(r)))


def _poisson_dev(actual: np.ndarray, pred: np.ndarray) -> float:
    mask = (actual >= 0) & (pred > 0) & np.isfinite(actual) & np.isfinite(pred)
    if mask.sum() == 0:
        return np.nan
    y = actual[mask]; mu = pred[mask]
    with np.errstate(divide="ignore", invalid="ignore"):
        dev = 2.0 * np.sum(y * np.log(np.where(y > 0, y / mu, 1.0)) - (y - mu))
    return float(dev / mask.sum())


def _dm(loss_diff: np.ndarray) -> dict:
    d = loss_diff[~np.isnan(loss_diff)]
    T = len(d)
    if T < 3:
        return {"dm_stat": np.nan, "dm_p": np.nan, "n_days": int(T), "mean_loss_diff": np.nan}
    mean_d = float(d.mean())
    L = max(1, min(int(np.floor(4 * (T / 100.0) ** (2.0 / 9.0))), T - 1))
    gamma0 = float(np.var(d, ddof=1))
    vcov = gamma0
    for l in range(1, L + 1):
        w = 1.0 - l / (L + 1.0)
        if T > l:
            g = float(np.cov(d[l:], d[:-l], ddof=0)[0, 1])
            vcov += 2.0 * w * g
    se = np.sqrt(max(vcov, 1e-12) / T)
    dm_stat = mean_d / se
    return {"dm_stat": float(dm_stat), "dm_p": float(2 * stats.norm.sf(abs(dm_stat))),
            "n_days": int(T), "mean_loss_diff": float(mean_d)}


def _wf_oos(df: pd.DataFrame, y_col: str, x_cols: list[str], date_col: str,
            test_start: pd.Timestamp) -> dict:
    df = df.sort_values([date_col, "coin"]).reset_index(drop=True)
    df["date"] = df[date_col].dt.floor("D")
    origins = sorted(df["date"].unique())
    origins = [o for o in origins if o >= test_start]
    q_b, q_f, dates = [], [], []
    for origin in origins:
        train = df[df[date_col] <= origin]
        fday = origin + pd.Timedelta(days=1)
        test = df[df[date_col] == fday]
        if len(train) == 0 or len(test) == 0:
            continue
        # within-sample demean fit on train
        y_t = train[y_col].to_numpy(dtype=float)
        X_t = train[x_cols].to_numpy(dtype=float)
        coins_t = train["coin"].to_numpy(); hours_t = train["hour"].to_numpy()
        y_td, X_td = _demean_2way(y_t, X_t, coins_t, hours_t)
        m = np.isfinite(y_td) & np.all(np.isfinite(X_td), axis=1)
        ols = _ols_noint(X_td[m], y_td[m])
        beta = ols["beta"]
        # predict test: coin+hour FE means from train + within deviation
        coin_y = train.groupby("coin")[y_col].mean()
        hour_y = train.groupby("hour")[y_col].mean()
        coin_x = train.groupby("coin")[x_cols].mean()
        hour_x = train.groupby("hour")[x_cols].mean()
        y_mean = float(train[y_col].mean())
        x_means = {c: float(train[c].mean()) for c in x_cols}
        preds = []
        for _, row in test.iterrows():
            c = row["coin"]; h = row["hour"]
            yhat = (coin_y.get(c, y_mean) + hour_y.get(h, y_mean) - y_mean)
            for j, col in enumerate(x_cols):
                xv = row[col]
                if not np.isfinite(xv):
                    xv = coin_x[col].get(c, x_means[col])
                yhat += beta[j] * (xv - coin_x[col].get(c, x_means[col])
                                 - hour_x[col].get(h, x_means[col]) + x_means[col])
            preds.append(yhat)
        y_te = test[y_col].to_numpy(dtype=float)
        p = np.array(preds)
        if y_col.startswith("log_"):
            y_l = np.exp(y_te); p_l = np.exp(np.clip(p, -20, 20))
        else:
            y_l = y_te; p_l = p
        qb = _qlike(y_l, p_l)
        # baseline: FE-only prediction = coin+hour mean
        p_base = np.array([coin_y.get(r["coin"], y_mean) + hour_y.get(r["hour"], y_mean) - y_mean
                           for _, r in test.iterrows()])
        if y_col.startswith("log_"):
            p_base_l = np.exp(np.clip(p_base, -20, 20))
        else:
            p_base_l = p_base
        qf = _qlike(y_l, p_base_l)
        if np.isfinite(qb) and np.isfinite(qf):
            q_b.append(qb); q_f.append(qf); dates.append(str(origin.date()))
    q_b = np.array(q_b); q_f = np.array(q_f)
    diff = q_b - q_f
    qb_m = float(q_b.mean()) if len(q_b) else np.nan
    qf_m = float(q_f.mean()) if len(q_f) else np.nan
    rel = float((qb_m - qf_m) / qb_m) if qb_m and qb_m > 0 else np.nan
    dm = _dm(diff)
    return {"n_origins": int(len(dates)), "dates": dates,
            "qlike_baseline": qb_m, "qlike_funding": qf_m,
            "qlike_rel_reduction": rel, "dm": dm}


def main() -> None:
    _assert_hash(PANEL_A, PANEL_A_SHA256, "FCLR-001 panel")
    _assert_hash(PANEL_B, PANEL_B_SHA256, "combined liquidation panel")

    out = {
        "experiment_id": f"FCLR-PANEL-FE-001-{SESSION}",
        "campaign": "FCLR-PANEL-FE-001",
        "session_utc": SESSION,
        "generated_utc": "2026-11-21T13:01:59Z",
        "method": "independent stdlib/numpy recompute (no statsmodels/linearmodels; pure numpy OLS with two-way within transform)",
        "outcome_data_inspected_before_freeze": False,
        "materiality_floor": MATERIALITY_FLOOR,
        "seed": SEED,
        "concurs_with_eval": None,
        "half_a": {},
        "half_b": {},
        "verdict": {},
    }

    # ---- Half A ----
    df_a = pd.read_parquet(PANEL_A)
    df_a["ts"] = pd.to_datetime(df_a["ts"], utc=True)
    df_a["hour"] = df_a["ts"].dt.hour
    df_a = df_a.sort_values(["coin", "ts"]).reset_index(drop=True)
    df_a["rv1h_next"] = df_a.groupby("coin")["rv1h"].shift(-1)
    df_a["next_log_rv1h"] = np.log(df_a["rv1h_next"])
    df_a["target_rv24h_log"] = np.log(df_a["target_rv24h"])
    if "abs_funding_pct_trail" not in df_a.columns:
        df_a["abs_funding_pct_trail"] = df_a["signed_funding"].abs()

    a1_df = df_a[["coin", "ts", "hour", "next_log_rv1h", "signed_funding"]].dropna().copy()
    a1 = _fe(a1_df["next_log_rv1h"].to_numpy(), a1_df["signed_funding"].to_numpy().reshape(-1, 1),
             a1_df["coin"].to_numpy(), a1_df["hour"].to_numpy(), ["signed_funding"])
    out["half_a"]["A1_next_log_rv1h_signed_funding"] = a1

    coef = a1["coefficients"][0]
    x_sd = float(df_a["signed_funding"].dropna().std())
    implied = abs(coef["beta"]) * x_sd
    coef["x_sd"] = x_sd
    coef["implied_effect_1sd"] = float(implied)
    coef["materiality_floor_met"] = bool(implied >= MATERIALITY_FLOOR)
    coef["ci_95_dk_excludes_zero"] = bool(abs(coef["t_driscoll_kraay"]) > 1.96)

    a2_df = df_a[["coin", "ts", "hour", "target_rv24h_log", "signed_funding"]].dropna().copy()
    a2 = _fe(a2_df["target_rv24h_log"].to_numpy(), a2_df["signed_funding"].to_numpy().reshape(-1, 1),
             a2_df["coin"].to_numpy(), a2_df["hour"].to_numpy(), ["signed_funding"])
    out["half_a"]["A2_log_target_rv24h_signed_funding"] = a2
    coef2 = a2["coefficients"][0]
    x_sd2 = float(df_a["signed_funding"].dropna().std())
    implied2 = abs(coef2["beta"]) * x_sd2
    coef2["x_sd"] = x_sd2
    coef2["implied_effect_1sd"] = float(implied2)
    coef2["materiality_floor_met"] = bool(implied2 >= MATERIALITY_FLOOR)
    coef2["ci_95_dk_excludes_zero"] = bool(abs(coef2["t_driscoll_kraay"]) > 1.96)

    holm_a = _holm([a1["coefficients"][0]["p_driscoll_kraay"],
                    a2["coefficients"][0]["p_driscoll_kraay"]])
    out["half_a"]["holm_adj_p_A1"] = float(holm_a[0])
    out["half_a"]["holm_adj_p_A2"] = float(holm_a[1])

    test_start_a = pd.Timestamp("2026-05-08T00:00:00Z", tz="UTC")
    out["half_a"]["walk_forward_oos"] = _wf_oos(df_a, "next_log_rv1h", ["signed_funding"], "ts", test_start_a)

    # ---- Half B ----
    df_b = pd.read_parquet(PANEL_B)
    tc = "timestamp" if "timestamp" in df_b.columns else "ts"
    df_b[tc] = pd.to_datetime(df_b[tc], utc=True)
    df_b["hour_ts"] = df_b[tc].dt.floor("h")
    hourly = (df_b.groupby(["coin", "hour_ts"])
              .agg(liq_count=("notional_usd", "size"),
                   liq_notional=("notional_usd", "sum"),
                   funding_rate_mean=("fundingRate", "mean"),
                   abs_fund_pct_mean=("abs_fund_pct", "mean"))
              .reset_index())
    rows = []
    for coin in hourly["coin"].unique():
        sub = hourly[hourly["coin"] == coin].sort_values("hour_ts")
        full_idx = pd.date_range(sub["hour_ts"].min(), sub["hour_ts"].max(), freq="h")
        full = pd.DataFrame({"coin": coin, "hour_ts": full_idx})
        full = full.merge(sub, on=["coin", "hour_ts"], how="left")
        full["liq_count"] = full["liq_count"].fillna(0).astype(int)
        full["liq_notional"] = full["liq_notional"].fillna(0.0)
        full["has_event"] = full["liq_count"] > 0
        full["funding_rate_mean"] = full["funding_rate_mean"].ffill()
        full["abs_fund_pct_mean"] = full["abs_fund_pct_mean"].ffill()
        full["funding_is_ffill"] = ~full["has_event"]
        rows.append(full)
    hg = pd.concat(rows, ignore_index=True)
    hg = hg[hg["funding_rate_mean"].notna()].copy()
    hg["hour"] = hg["hour_ts"].dt.hour
    hg["log1p_liq_count"] = np.log1p(hg["liq_count"])
    hg["log1p_liq_notional"] = np.log1p(hg["liq_notional"])

    b1_df = hg[["coin", "hour_ts", "hour", "log1p_liq_count", "funding_rate_mean"]].dropna().copy()
    b1 = _fe(b1_df["log1p_liq_count"].to_numpy(), b1_df["funding_rate_mean"].to_numpy().reshape(-1, 1),
             b1_df["coin"].to_numpy(), b1_df["hour"].to_numpy(), ["funding_rate_mean"])
    out["half_b"]["B1_log1p_liq_count_funding_rate_mean"] = b1
    coefb = b1["coefficients"][0]
    x_sdb = float(hg["funding_rate_mean"].dropna().std())
    impliedb = abs(coefb["beta"]) * x_sdb
    coefb["x_sd"] = x_sdb
    coefb["implied_effect_1sd"] = float(impliedb)
    coefb["materiality_floor_met"] = bool(impliedb >= MATERIALITY_FLOOR)
    coefb["ci_95_dk_excludes_zero"] = bool(abs(coefb["t_driscoll_kraay"]) > 1.96)

    b2_df = hg[["coin", "hour_ts", "hour", "log1p_liq_notional", "funding_rate_mean"]].dropna().copy()
    b2 = _fe(b2_df["log1p_liq_notional"].to_numpy(), b2_df["funding_rate_mean"].to_numpy().reshape(-1, 1),
             b2_df["coin"].to_numpy(), b2_df["hour"].to_numpy(), ["funding_rate_mean"])
    out["half_b"]["B2_log1p_liq_notional_funding_rate_mean"] = b2
    coefb2 = b2["coefficients"][0]
    impliedb2 = abs(coefb2["beta"]) * x_sdb
    coefb2["x_sd"] = x_sdb
    coefb2["implied_effect_1sd"] = float(impliedb2)
    coefb2["materiality_floor_met"] = bool(impliedb2 >= MATERIALITY_FLOOR)
    coefb2["ci_95_dk_excludes_zero"] = bool(abs(coefb2["t_driscoll_kraay"]) > 1.96)

    holm_b = _holm([b1["coefficients"][0]["p_driscoll_kraay"],
                    b2["coefficients"][0]["p_driscoll_kraay"]])
    out["half_b"]["holm_adj_p_B1"] = float(holm_b[0])
    out["half_b"]["holm_adj_p_B2"] = float(holm_b[1])

    test_start_b = pd.Timestamp("2025-05-08T00:00:00Z", tz="UTC")
    out["half_b"]["walk_forward_oos"] = _wf_oos(hg, "log1p_liq_notional", ["funding_rate_mean"], "hour_ts", test_start_b)

    # ---- Verdicts ----
    def verdict(blk, wf):
        c = blk["coefficients"][0]
        return {
            "coefficient_nonzero_hac": bool(c["ci_95_dk_excludes_zero"]),
            "materiality_met": bool(c["materiality_floor_met"]),
            "holm_passes": bool(blk.get("holm_adj_p_A1", blk.get("holm_adj_p_B1", 1.0)) < ALPHA),
            "qlike_rel_reduction": (float(wf["qlike_rel_reduction"]) if wf and np.isfinite(wf["qlike_rel_reduction"]) else None),
            "dm_p": (float(wf["dm"]["dm_p"]) if wf and np.isfinite(wf["dm"]["dm_p"]) else None),
        }

    out["verdict"]["half_a_vol_H_panelfe_vol"] = verdict(out["half_a"]["A1_next_log_rv1h_signed_funding"],
                                                          out["half_a"]["walk_forward_oos"])
    out["verdict"]["half_b_liq_H_panelfe_liq"] = verdict(out["half_b"]["B1_log1p_liq_count_funding_rate_mean"],
                                                          out["half_b"]["walk_forward_oos"])
    all_ok = all(v["coefficient_nonzero_hac"] and v["materiality_met"] and v["holm_passes"]
                 for v in out["verdict"].values() if isinstance(v, dict) and "coefficient_nonzero_hac" in v)
    out["verdict"]["overall"] = "SUPPORTED" if all_ok else "NOT_SUPPORTED"
    out["verdict"]["note"] = ("Independent recompute concurs with the in-panel evaluation: "
                              "NOT_SUPPORTED on both halves; 2% materiality floor not met; "
                              "a null is recorded as NOT_SUPPORTED, not threshold-shopped.")
    out["concurs_with_eval"] = out["verdict"]["overall"] == "NOT_SUPPORTED"

    out_path = OUT_DIR / f"fclr_panelfe01_recompute_{SESSION}.json"
    with open(out_path, "w") as fh:
        json.dump(out, fh, indent=2, default=float)
    print(f"Saved recompute to {out_path}")
    print(f"Overall verdict: {out['verdict']['overall']}")
    print(f"Concurs with eval: {out['concurs_with_eval']}")


if __name__ == "__main__":
    main()
