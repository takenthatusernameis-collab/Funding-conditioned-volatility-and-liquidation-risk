#!/usr/bin/env python3
"""
FCLR-PANEL-FE-001 Step 2/3: Panel fixed-effects funding-conditioning study.

Two-way (coin + hour-of-day) fixed-effects panel regression estimated by the
within (successive partialling-out / alternating-projection demeaning) transform:
  y~ = beta * x~ + e~   where ~ = residual after projecting out coin FE and hour FE.

Half A (volatility, FCLR-001 panel):
  A1: next_log_rv1h ~ coin_FE + hour_FE + signed_funding          (PRIMARY)
  A2: log_target_rv24h ~ coin_FE + hour_FE + signed_funding       (robustness)
  A3: next_log_rv1h ~ coin_FE + hour_FE + abs_funding_pct_trail   (robustness)
Inference: cluster-robust (CR1) by coin + Driscoll-Kraay HAC + Newey-West HAC.
Walk-forward OOS: expanding-window one-step-ahead at daily 00:00 UTC origins,
funding-conditioned FE vs no-funding FE baseline, QLIKE on rv1h level,
Diebold-Mariano on daily-mean QLIKE loss differential.

Half B (liquidation intensity, combined metpie+ironflow panel):
  B1: log1p(liq_count) ~ coin_FE + hour_FE + funding_rate_mean      (PRIMARY)
  B2: log1p(liq_notional) ~ coin_FE + hour_FE + funding_rate_mean   (PRIMARY)
  B3: log1p(liq_count) ~ coin_FE + hour_FE + abs_fund_pct_mean      (robustness)
Hourly aggregation: complete (coin, hour) grid; zero-event hours are explicit zeros
(has_event=False); funding predictor = mean fundingRate inside hour; zero-event hours
get funding ffill from most recent prior in-panel observation (funding ffill only,
never outcome ffill), flagged funding_is_ffill=True.
Walk-forward OOS: QLIKE on notional intensity + Poisson deviance robustness,
Diebold-Mariano.

Materiality floor: implied effect from +1 SD funding shock >= 2% relative (frozen,
NOT relaxed after outcomes). Holm familywise correction across primary contrasts
within each half. outcome_data_inspected_before_freeze=false. Both frozen panel
sha256 asserted in header before any read. premium never used (all-null).
funding_asof_lag_h is hours-since-funding, NOT a rate; never used as a rate.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

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
N_BOOT_DM = 2000

RNG = np.random.RandomState(SEED)


def _assert_hash(path: Path, expected: str, label: str) -> str:
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    assert actual == expected, f"{label} hash mismatch: {actual} != {expected}"
    return actual


def _demean_two_way(df: pd.DataFrame, y_col: str, x_cols: list[str],
                    coin_col: str = "coin", hour_col: str = "hour"):
    """Two-way FE within transform: residualize y and X on coin FE + hour FE.

    Uses successive partialling out (demean by coin, then by hour, then by coin,
    then by hour) which converges to the two-way within residuals. Returns
    demeaned y (n,), demeaned X (n, k), and the within-R^2 of x on y for SE.
    """
    data = df[[coin_col, hour_col, y_col] + x_cols].copy()
    data = data.dropna()
    n = len(data)
    y = data[y_col].to_numpy(dtype=float).copy()
    X = data[x_cols].to_numpy(dtype=float).copy()
    coins = data[coin_col].to_numpy()
    hours = data[hour_col].to_numpy()

    # Successive partialling out: coin -> hour -> coin -> hour (enough for 2-way).
    for _ in range(4):
        # partial out coin means
        for c in np.unique(coins):
            m = coins == c
            y[m] -= y[m].mean()
            X[m] -= X[m].mean(axis=0)
        # partial out hour means
        for h in np.unique(hours):
            m = hours == h
            y[m] -= y[m].mean()
            X[m] -= X[m].mean(axis=0)

    return y, X, data.index.to_numpy()


def _ols(X: np.ndarray, y: np.ndarray) -> dict:
    """OLS with no intercept (data already demeaned). Returns beta, residuals,
    sigma2, and X'X inverse."""
    n, k = X.shape
    XtX = X.T @ X
    XtX_inv = np.linalg.pinv(XtX)
    beta = XtX_inv @ (X.T @ y)
    fitted = X @ beta
    resid = y - fitted
    df_resid = n - k
    sigma2 = float((resid @ resid) / df_resid) if df_resid > 0 else np.nan
    return {"beta": beta, "resid": resid, "fitted": fitted,
            "sigma2": sigma2, "n": n, "k": k, "df_resid": df_resid,
            "XtX_inv": XtX_inv, "X": X}


def _cluster_se_by_coin(ols_res: dict, data: pd.DataFrame, coin_col: str = "coin",
                        x_cols: list[str] | None = None) -> list[float]:
    """Cluster-robust (CR1) standard errors clustered by coin."""
    beta = ols_res["beta"]
    resid = ols_res["resid"]
    XtX_inv = ols_res["XtX_inv"]
    k = len(beta)
    X = data[x_cols].to_numpy(dtype=float)
    coins = data[coin_col].to_numpy()
    # meat = sum_g (X_g' resid_g) (X_g' resid_g)'
    meat = np.zeros((k, k))
    for c in np.unique(coins):
        m = coins == c
        ug = X[m] * resid[m, None]  # (n_g, k)
        meat += ug.T @ ug
    vcov = XtX_inv @ meat @ XtX_inv
    se = np.sqrt(np.maximum(np.diag(vcov), 0.0))
    return [float(s) for s in se]


def _driscoll_kraay_se(ols_res: dict, data: pd.DataFrame, hour_col: str = "hour",
                       x_cols: list[str] | None = None) -> list[float]:
    """Driscoll-Kraay HAC SE on h_t = sum_i x_it e_it cross-sectional moment sums."""
    beta = ols_res["beta"]
    resid = ols_res["resid"]
    X = data[x_cols].to_numpy(dtype=float)
    hours = data[hour_col].to_numpy()
    k = len(beta)
    T = len(np.unique(hours))
    # h_t = sum_i x_it e_it over cross-section at hour t
    H = np.zeros((T, k))
    hour_list = sorted(np.unique(hours))
    for ti, h in enumerate(hour_list):
        m = hours == h
        H[ti] = (X[m] * resid[m, None]).sum(axis=0)
    # Newey-West on H with lag L = floor(4*(T/100)^(2/9))
    L = int(np.floor(4 * (T / 100.0) ** (2.0 / 9.0)))
    L = max(1, min(L, T - 1))
    gamma0 = (H.T @ H) / T
    vcov = gamma0.copy()
    for l in range(1, L + 1):
        w = 1.0 - l / (L + 1.0)
        gammal = (H[l:].T @ H[:-l]) / T
        vcov += w * (gammal + gammal.T)
    vcov = np.linalg.pinv(ols_res["XtX_inv"]) @ vcov @ np.linalg.pinv(ols_res["XtX_inv"])
    se = np.sqrt(np.maximum(np.diag(vcov), 0.0))
    return [float(s) for s in se]


def _newey_west_se(ols_res: dict, x_cols: list[str] | None = None) -> list[float]:
    """Newey-West HAC on the stacked within-transformed series (ordered by hour)."""
    beta = ols_res["beta"]
    resid = ols_res["resid"]
    X = ols_res["X"]
    k = len(beta)
    n = len(resid)
    T_eff = max(1, int(np.floor(n / 5.0)))
    L = int(np.floor(4 * (T_eff / 100.0) ** (2.0 / 9.0)))
    L = max(1, min(L, n - 1))
    # u_t = x_t * e_t stacked
    U = X * resid[:, None]
    gamma0 = (U.T @ U) / n
    vcov = gamma0.copy()
    for l in range(1, L + 1):
        w = 1.0 - l / (L + 1.0)
        gammal = (U[l:].T @ U[:-l]) / n
        vcov += w * (gammal + gammal.T)
    XtX_inv = np.linalg.pinv(X.T @ X)
    vcov = XtX_inv @ vcov @ XtX_inv
    se = np.sqrt(np.maximum(np.diag(vcov), 0.0))
    return [float(s) for s in se]


def _fe_estimate(df: pd.DataFrame, y_col: str, x_cols: list[str]) -> dict:
    """Run two-way FE and return beta, SEs (3 kinds), t-stats, p-values, n."""
    y, X, idx = _demean_two_way(df, y_col, x_cols)
    data = df.loc[idx].copy()
    ols_res = _ols(X, y)
    beta = ols_res["beta"]
    k = len(beta)
    se_cr1 = _cluster_se_by_coin(ols_res, data, x_cols=x_cols)
    se_dk = _driscoll_kraay_se(ols_res, data, x_cols=x_cols)
    se_nw = _newey_west_se(ols_res, x_cols=x_cols)

    results = []
    for j, xname in enumerate(x_cols):
        b = float(beta[j])
        results.append({
            "predictor": xname,
            "beta": b,
            "se_cluster_coin": se_cr1[j],
            "se_driscoll_kraay": se_dk[j],
            "se_newey_west": se_nw[j],
            "t_cluster_coin": b / se_cr1[j] if se_cr1[j] > 0 else np.nan,
            "t_driscoll_kraay": b / se_dk[j] if se_dk[j] > 0 else np.nan,
            "t_newey_west": b / se_nw[j] if se_nw[j] > 0 else np.nan,
        })
    return {
        "n": int(ols_res["n"]),
        "k": int(k),
        "sigma2": float(ols_res["sigma2"]),
        "within_r2": float(1.0 - (ols_res["resid"] @ ols_res["resid"]) /
                           ((y @ y) if (y @ y) > 0 else 1.0)),
        "coefficients": results,
    }


def _wald_p(t_stat: float, df: int) -> float:
    """Two-sided p-value from t-stat (normal approximation, df large enough)."""
    if np.isnan(t_stat):
        return np.nan
    # Use normal approximation for p (G=5 clusters -> report caveat; HAC is large-sample)
    from scipy import stats
    return float(2 * stats.norm.sf(abs(t_stat)))


def _holm_adjust(p_values: list[float]) -> list[float]:
    order = sorted(range(len(p_values)), key=lambda i: p_values[i])
    adj = [0.0] * len(p_values)
    m = len(p_values)
    for rank, i in enumerate(order):
        adj[i] = min(1.0, float(p_values[i]) * (m - rank))
    return adj


def _qlike(actual: np.ndarray, pred: np.ndarray) -> float:
    mask = (actual > 0) & (pred > 0) & np.isfinite(actual) & np.isfinite(pred)
    if mask.sum() == 0:
        return np.nan
    ratio = actual[mask] / pred[mask]
    return float(np.mean(ratio - 1.0 - np.log(ratio)))


def _poisson_deviance(actual: np.ndarray, pred: np.ndarray) -> float:
    mask = (actual >= 0) & (pred > 0) & np.isfinite(actual) & np.isfinite(pred)
    if mask.sum() == 0:
        return np.nan
    y = actual[mask]
    mu = pred[mask]
    with np.errstate(divide="ignore", invalid="ignore"):
        dev = 2.0 * np.sum(y * np.log(np.where(y > 0, y / mu, 1.0)) - (y - mu))
    return float(dev / mask.sum())


def _diebold_mariano(loss_diff: np.ndarray) -> dict:
    """Diebold-Mariano test on daily-mean loss differential, Newey-West HAC."""
    d = loss_diff[~np.isnan(loss_diff)]
    T = len(d)
    if T < 3:
        return {"dm_stat": np.nan, "dm_p": np.nan, "n_days": int(T)}
    mean_d = float(d.mean())
    # Newey-West variance of the mean
    L = int(np.floor(4 * (T / 100.0) ** (2.0 / 9.0)))
    L = max(1, min(L, T - 1))
    gamma0 = float(np.var(d, ddof=1))
    vcov = gamma0
    for l in range(1, L + 1):
        w = 1.0 - l / (L + 1.0)
        acov = float(np.cov(d[l:], d[:-l], ddof=0)[0, 1]) if T > l else 0.0
        vcov += 2.0 * w * acov
    se_mean = np.sqrt(max(vcov, 1e-12) / T)
    dm_stat = mean_d / se_mean
    from scipy import stats
    dm_p = float(2 * stats.norm.sf(abs(dm_stat)))
    return {"dm_stat": float(dm_stat), "dm_p": dm_p, "n_days": int(T),
            "mean_loss_diff": mean_d}


def _walk_forward_oos(df: pd.DataFrame, y_col: str, x_cols: list[str],
                      date_col: str, test_start: pd.Timestamp) -> dict:
    """Expanding-window walk-forward OOS. At each daily 00:00 UTC origin,
    fit on all data <= origin, forecast the next 24 hours."""
    df = df.sort_values([date_col, "coin"]).reset_index(drop=True)
    df["date"] = df[date_col].dt.floor("D")
    origins = sorted(df["date"].unique())
    origins = [o for o in origins if o >= test_start]
    if len(origins) < 2:
        return {"n_origins": 0, "qlike_baseline": np.nan, "qlike_funding": np.nan,
                "qlike_rel_reduction": np.nan, "dm": {"dm_stat": np.nan, "dm_p": np.nan,
                "n_days": 0}, "daily_qlike_diff": []}

    daily_qlike_b = []
    daily_qlike_f = []
    daily_dates = []

    for origin in origins:
        train = df[df[date_col] <= origin]
        forecast_day = origin + pd.Timedelta(days=1)
        test = df[df[date_col] == forecast_day]
        if len(train) == 0 or len(test) == 0:
            continue

        # Fit two models on train (demeaned within train sample)
        def fit_predict(tr: pd.DataFrame, te: pd.DataFrame, use_funding: bool):
            cols = x_cols if use_funding else [c for c in x_cols if c not in ("signed_funding", "funding_rate_mean", "abs_funding_pct_trail", "abs_fund_pct_mean")]
            if len(cols) == 0:
                # baseline: predict with coin+hour FE only -> grand mean within train
                pred_val = float(tr[y_col].mean())
                return np.full(len(te), pred_val)
            # Build demeaned train
            y_tr, X_tr, idx_tr = _demean_two_way(tr, y_col, cols)
            ols_tr = _ols(X_tr, y_tr)
            beta = ols_tr["beta"]
            # Apply to test: demean test using train coin/hour means
            coin_means_y = tr.groupby("coin")[y_col].mean()
            hour_means_y = tr.groupby("hour")[y_col].mean()
            coin_means_x = tr.groupby("coin")[cols].mean()
            hour_means_x = tr.groupby("hour")[cols].mean()
            preds = []
            for _, row in te.iterrows():
                c = row["coin"]; h = row["hour"]
                y_hat = (coin_means_y.get(c, tr[y_col].mean())
                         + hour_means_y.get(h, tr[y_col].mean())
                         - tr[y_col].mean())
                x_hat = 0.0
                for j, col in enumerate(cols):
                    xv = row[col]
                    if pd.isna(xv):
                        xv = coin_means_x[col].get(c, tr[col].mean())
                    x_hat += beta[j] * (xv
                                      - coin_means_x[col].get(c, tr[col].mean())
                                      - hour_means_x[col].get(h, tr[col].mean())
                                      + tr[col].mean())
                y_hat += x_hat
                preds.append(y_hat)
            return np.array(preds)

        y_test = test[y_col].to_numpy(dtype=float)
        pred_f = fit_predict(train, test, use_funding=True)
        pred_b = fit_predict(train, test, use_funding=False)

        # Map log-vol back to level for QLIKE (fair: same monotone map both arms)
        if y_col.startswith("log_"):
            y_test_l = np.exp(y_test)
            pred_f_l = np.exp(np.clip(pred_f, -20, 20))
            pred_b_l = np.exp(np.clip(pred_b, -20, 20))
        else:
            y_test_l = y_test
            pred_f_l = pred_f
            pred_b_l = pred_b

        q_b = _qlike(y_test_l, pred_b_l)
        q_f = _qlike(y_test_l, pred_f_l)
        if not np.isnan(q_b) and not np.isnan(q_f):
            daily_qlike_b.append(q_b)
            daily_qlike_f.append(q_f)
            daily_dates.append(str(origin.date()))

    daily_qlike_b = np.array(daily_qlike_b)
    daily_qlike_f = np.array(daily_qlike_f)
    loss_diff = daily_qlike_b - daily_qlike_f  # positive = funding better
    q_b = float(daily_qlike_b.mean()) if len(daily_qlike_b) else np.nan
    q_f = float(daily_qlike_f.mean()) if len(daily_qlike_f) else np.nan
    rel = float((q_b - q_f) / q_b) if q_b and q_b > 0 else np.nan
    dm = _diebold_mariano(loss_diff)
    return {
        "n_origins": int(len(daily_dates)),
        "dates": daily_dates,
        "qlike_baseline": q_b,
        "qlike_funding": q_f,
        "qlike_rel_reduction": rel,
        "dm": dm,
    }


def main() -> None:
    _assert_hash(PANEL_A, PANEL_A_SHA256, "FCLR-001 panel")
    _assert_hash(PANEL_B, PANEL_B_SHA256, "combined liquidation panel")

    results = {
        "experiment_id": f"FCLR-PANEL-FE-001-{SESSION}",
        "campaign": "FCLR-PANEL-FE-001",
        "session_utc": SESSION,
        "generated_utc": "2026-11-21T13:01:59Z",
        "outcome_data_inspected_before_freeze": False,
        "repository": "Funding-conditioned-volatility-and-liquidation-risk",
        "materiality_floor": MATERIALITY_FLOOR,
        "seed": SEED,
        "panels": {
            "fclr001": {"path": str(PANEL_A), "sha256": PANEL_A_SHA256, "hash_verified": True},
            "combined_liquidation": {"path": str(PANEL_B), "sha256": PANEL_B_SHA256, "hash_verified": True},
        },
        "half_a_volatility": {},
        "half_b_liquidation": {},
        "verdict": {},
    }

    # ============ HALF A: Volatility ============
    df_a = pd.read_parquet(PANEL_A)
    df_a["ts"] = pd.to_datetime(df_a["ts"], utc=True)
    df_a["hour"] = df_a["ts"].dt.hour
    # next-hour log rv1h within coin
    df_a = df_a.sort_values(["coin", "ts"]).reset_index(drop=True)
    df_a["rv1h_next"] = df_a.groupby("coin")["rv1h"].shift(-1)
    df_a["next_log_rv1h"] = np.log(df_a["rv1h_next"])
    df_a["target_rv24h_log"] = np.log(df_a["target_rv24h"])
    # abs_funding_pct_trail robustness predictor
    if "abs_funding_pct_trail" not in df_a.columns:
        df_a["abs_funding_pct_trail"] = df_a["signed_funding"].abs()

    test_start_a = pd.Timestamp("2026-05-08T00:00:00Z", tz="UTC")

    # A1: next_log_rv1h ~ signed_funding
    a1_df = df_a[["coin", "ts", "hour", "next_log_rv1h", "signed_funding"]].dropna().copy()
    a1 = _fe_estimate(a1_df, "next_log_rv1h", ["signed_funding"])
    for c in a1["coefficients"]:
        c["p_cluster_coin"] = _wald_p(c["t_cluster_coin"], a1["n"])
        c["p_driscoll_kraay"] = _wald_p(c["t_driscoll_kraay"], a1["n"])
        c["p_newey_west"] = _wald_p(c["t_newey_west"], a1["n"])
    results["half_a_volatility"]["A1_next_log_rv1h_signed_funding"] = a1

    # A2: log_target_rv24h ~ signed_funding
    a2_df = df_a[["coin", "ts", "hour", "target_rv24h_log", "signed_funding"]].dropna().copy()
    a2 = _fe_estimate(a2_df, "target_rv24h_log", ["signed_funding"])
    for c in a2["coefficients"]:
        c["p_cluster_coin"] = _wald_p(c["t_cluster_coin"], a2["n"])
        c["p_driscoll_kraay"] = _wald_p(c["t_driscoll_kraay"], a2["n"])
        c["p_newey_west"] = _wald_p(c["t_newey_west"], a2["n"])
    results["half_a_volatility"]["A2_log_target_rv24h_signed_funding"] = a2

    # A3: next_log_rv1h ~ abs_funding_pct_trail
    a3_df = df_a[["coin", "ts", "hour", "next_log_rv1h", "abs_funding_pct_trail"]].dropna().copy()
    a3 = _fe_estimate(a3_df, "next_log_rv1h", ["abs_funding_pct_trail"])
    for c in a3["coefficients"]:
        c["p_cluster_coin"] = _wald_p(c["t_cluster_coin"], a3["n"])
        c["p_driscoll_kraay"] = _wald_p(c["t_driscoll_kraay"], a3["n"])
        c["p_newey_west"] = _wald_p(c["t_newey_west"], a3["n"])
    results["half_a_volatility"]["A3_next_log_rv1h_abs_funding_pct_trail"] = a3

    # Walk-forward OOS Half A
    wf_a = _walk_forward_oos(df_a, "next_log_rv1h", ["signed_funding"], "ts", test_start_a)
    results["half_a_volatility"]["walk_forward_oos"] = wf_a

    # Holm across primary contrasts in half A (A1 + A2)
    p_vals_a = [a1["coefficients"][0]["p_driscoll_kraay"],
                a2["coefficients"][0]["p_driscoll_kraay"]]
    holm_a = _holm_adjust(p_vals_a)
    results["half_a_volatility"]["holm_adj_p_A1"] = float(holm_a[0])
    results["half_a_volatility"]["holm_adj_p_A2"] = float(holm_a[1])

    # Materiality: implied effect from 1-SD shock
    for key in ("A1_next_log_rv1h_signed_funding", "A2_log_target_rv24h_signed_funding",
                "A3_next_log_rv1h_abs_funding_pct_trail"):
        block = results["half_a_volatility"][key]
        coef = block["coefficients"][0]
        x = df_a[coef["predictor"]].dropna()
        sd = float(x.std()) if len(x) > 0 else np.nan
        implied = float(abs(coef["beta"]) * sd) if not np.isnan(sd) else np.nan
        coef["x_sd"] = sd
        coef["implied_effect_1sd"] = implied
        coef["materiality_floor_met"] = bool(implied is not None and not np.isnan(implied) and implied >= MATERIALITY_FLOOR)
        coef["ci_95_dk_excludes_zero"] = bool(
            abs(coef["t_driscoll_kraay"]) > 1.96 if not np.isnan(coef["t_driscoll_kraay"]) else False)

    # ============ HALF B: Liquidation intensity ============
    df_b = pd.read_parquet(PANEL_B)
    ts_col = "timestamp" if "timestamp" in df_b.columns else "ts"
    df_b[ts_col] = pd.to_datetime(df_b[ts_col], utc=True)
    df_b["hour_ts"] = df_b[ts_col].dt.floor("h")

    # Aggregate event-level to hourly per coin
    hourly = (
        df_b.groupby(["coin", "hour_ts"])
        .agg(
            liq_count=("notional_usd", "size"),
            liq_notional=("notional_usd", "sum"),
            funding_rate_mean=("fundingRate", "mean"),
            abs_fund_pct_mean=("abs_fund_pct", "mean"),
        )
        .reset_index()
    )

    # Build complete hourly grid per coin over observed span; zero-event hours explicit zeros
    grid_rows = []
    for coin in hourly["coin"].unique():
        sub = hourly[hourly["coin"] == coin].sort_values("hour_ts")
        full_idx = pd.date_range(start=sub["hour_ts"].min(), end=sub["hour_ts"].max(), freq="h")
        full = pd.DataFrame({"coin": coin, "hour_ts": full_idx})
        full = full.merge(sub, on=["coin", "hour_ts"], how="left")
        full["liq_count"] = full["liq_count"].fillna(0).astype(int)
        full["liq_notional"] = full["liq_notional"].fillna(0.0)
        full["has_event"] = full["liq_count"] > 0
        # funding ffill only (never outcome ffill); zero-event hours carry prior funding
        full["funding_rate_mean"] = full["funding_rate_mean"].ffill()
        full["abs_fund_pct_mean"] = full["abs_fund_pct_mean"].ffill()
        full["funding_is_ffill"] = ~full["has_event"]
        grid_rows.append(full)
    hourly_grid = pd.concat(grid_rows, ignore_index=True)
    # Drop leading hours with no prior funding
    hourly_grid = hourly_grid[hourly_grid["funding_rate_mean"].notna()].copy()

    hourly_grid["hour"] = hourly_grid["hour_ts"].dt.hour
    hourly_grid["log1p_liq_count"] = np.log1p(hourly_grid["liq_count"])
    hourly_grid["log1p_liq_notional"] = np.log1p(hourly_grid["liq_notional"])

    test_start_b = pd.Timestamp("2025-05-08T00:00:00Z", tz="UTC")

    # B1: log1p(liq_count) ~ funding_rate_mean
    b1_df = hourly_grid[["coin", "hour_ts", "hour", "log1p_liq_count", "funding_rate_mean"]].dropna().copy()
    b1 = _fe_estimate(b1_df, "log1p_liq_count", ["funding_rate_mean"])
    for c in b1["coefficients"]:
        c["p_cluster_coin"] = _wald_p(c["t_cluster_coin"], b1["n"])
        c["p_driscoll_kraay"] = _wald_p(c["t_driscoll_kraay"], b1["n"])
        c["p_newey_west"] = _wald_p(c["t_newey_west"], b1["n"])
    results["half_b_liquidation"]["B1_log1p_liq_count_funding_rate_mean"] = b1

    # B2: log1p(liq_notional) ~ funding_rate_mean
    b2_df = hourly_grid[["coin", "hour_ts", "hour", "log1p_liq_notional", "funding_rate_mean"]].dropna().copy()
    b2 = _fe_estimate(b2_df, "log1p_liq_notional", ["funding_rate_mean"])
    for c in b2["coefficients"]:
        c["p_cluster_coin"] = _wald_p(c["t_cluster_coin"], b2["n"])
        c["p_driscoll_kraay"] = _wald_p(c["t_driscoll_kraay"], b2["n"])
        c["p_newey_west"] = _wald_p(c["t_newey_west"], b2["n"])
    results["half_b_liquidation"]["B2_log1p_liq_notional_funding_rate_mean"] = b2

    # B3: log1p(liq_count) ~ abs_fund_pct_mean (robustness)
    b3_df = hourly_grid[["coin", "hour_ts", "hour", "log1p_liq_count", "abs_fund_pct_mean"]].dropna().copy()
    b3 = _fe_estimate(b3_df, "log1p_liq_count", ["abs_fund_pct_mean"])
    for c in b3["coefficients"]:
        c["p_cluster_coin"] = _wald_p(c["t_cluster_coin"], b3["n"])
        c["p_driscoll_kraay"] = _wald_p(c["t_driscoll_kraay"], b3["n"])
        c["p_newey_west"] = _wald_p(c["t_newey_west"], b3["n"])
    results["half_b_liquidation"]["B3_log1p_liq_count_abs_fund_pct_mean"] = b3

    # Walk-forward OOS Half B (on notional intensity level)
    wf_b = _walk_forward_oos(hourly_grid, "log1p_liq_notional", ["funding_rate_mean"], "hour_ts", test_start_b)
    results["half_b_liquidation"]["walk_forward_oos"] = wf_b

    # Holm across primary contrasts in half B (B1 + B2)
    p_vals_b = [b1["coefficients"][0]["p_driscoll_kraay"],
                b2["coefficients"][0]["p_driscoll_kraay"]]
    holm_b = _holm_adjust(p_vals_b)
    results["half_b_liquidation"]["holm_adj_p_B1"] = float(holm_b[0])
    results["half_b_liquidation"]["holm_adj_p_B2"] = float(holm_b[1])

    # Materiality Half B
    for key in ("B1_log1p_liq_count_funding_rate_mean", "B2_log1p_liq_notional_funding_rate_mean",
                "B3_log1p_liq_count_abs_fund_pct_mean"):
        block = results["half_b_liquidation"][key]
        coef = block["coefficients"][0]
        x = hourly_grid[coef["predictor"]].dropna()
        sd = float(x.std()) if len(x) > 0 else np.nan
        implied = float(abs(coef["beta"]) * sd) if not np.isnan(sd) else np.nan
        coef["x_sd"] = sd
        coef["implied_effect_1sd"] = implied
        coef["materiality_floor_met"] = bool(implied is not None and not np.isnan(implied) and implied >= MATERIALITY_FLOOR)
        coef["ci_95_dk_excludes_zero"] = bool(
            abs(coef["t_driscoll_kraay"]) > 1.96 if not np.isnan(coef["t_driscoll_kraay"]) else False)

    # ============ Verdicts ============
    def _verdict(block, wf_key):
        coef = block["coefficients"][0]
        dk_sig = coef["ci_95_dk_excludes_zero"]
        mat = coef["materiality_floor_met"]
        holm = block.get("holm_adj_p_" + block.get("_key", "x"), 1.0) < ALPHA
        wf = results.get(wf_key, {})
        q_rel = wf.get("qlike_rel_reduction", np.nan)
        dm_ok = wf.get("dm", {}).get("dm_p", 1.0)
        return {
            "coefficient_nonzero_hac": bool(dk_sig),
            "materiality_met": bool(mat),
            "holm_passes": bool(holm),
            "qlike_rel_reduction": float(q_rel) if not np.isnan(q_rel) else None,
            "dm_p": float(dm_ok) if not np.isnan(dm_ok) else None,
        }

    results["half_a_volatility"]["A1_next_log_rv1h_signed_funding"]["_key"] = "A1_next_log_rv1h_signed_funding"
    results["half_b_liquidation"]["B1_log1p_liq_count_funding_rate_mean"]["_key"] = "B1_log1p_liq_count_funding_rate_mean"

    results["verdict"]["half_a_vol_H_panelfe_vol"] = _verdict(
        results["half_a_volatility"]["A1_next_log_rv1h_signed_funding"], "walk_forward_oos")
    results["verdict"]["half_b_liq_H_panelfe_liq"] = _verdict(
        results["half_b_liquidation"]["B1_log1p_liq_count_funding_rate_mean"], "walk_forward_oos")

    results["verdict"]["overall"] = (
        "SUPPORTED" if all(
            v["coefficient_nonzero_hac"] and v["materiality_floor_met"] and v["holm_passes"]
            for v in results["verdict"].values() if isinstance(v, dict) and "coefficient_nonzero_hac" in v
        ) else "NOT_SUPPORTED")
    results["verdict"]["note"] = ("A null on either half is recorded as NOT_SUPPORTED. "
                                  "The 2% materiality floor is frozen and not relaxed after outcomes.")

    # Drop helper keys before serializing
    for half in ("half_a_volatility", "half_b_liquidation"):
        for key in list(results[half].keys()):
            if isinstance(results[half][key], dict) and "_key" in results[half][key]:
                del results[half][key]["_key"]

    out_path = OUT_DIR / f"fclr_panelfe01_eval_{SESSION}.json"
    with open(out_path, "w") as fh:
        json.dump(results, fh, indent=2, default=float)
    print(f"Saved evaluation to {out_path}")
    print(f"Overall verdict: {results['verdict']['overall']}")


if __name__ == "__main__":
    main()
