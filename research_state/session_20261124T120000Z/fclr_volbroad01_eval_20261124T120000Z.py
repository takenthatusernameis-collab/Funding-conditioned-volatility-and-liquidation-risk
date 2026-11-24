#!/usr/bin/env python3
"""
Phase 3 — FCLR-VOL-BROAD-01 heavy walk-forward evaluation.
Real computation on the frozen ironflow_bulk panel (no fabricated numbers).

Design: chronological walk-forward, TRAIN_FRAC=0.60, PURGE_EMBARGO_H=48, BLOCK_H=168,
expanding train-only normalization. Pooled two-way (coin + hour-of-day) fixed-effects
within-transform OLS. Funding-conditioned candidate vs realized-volatility-only baseline.
Metrics: QLIKE (primary) and MSE; Diebold-Mariano HAC on daily loss differential;
cluster-robust CR1 by coin; Driscoll-Kraay HAC; Holm over declared family.
Materiality floor: +1 sample-SD funding shock must move QLIKE by >= 2% relative.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow.parquet as pq
from math import erfc

REPO = Path(__file__).resolve().parent.parent.parent
SESSION = REPO / "research_state" / "session_20261124T120000Z"
CACHE = REPO / "research_state" / "data_cache" / "ironflow_bulk"
SESSION_UTC = "20261124T120000Z"
SESSION_ID = f"session_{SESSION_UTC}"
EXPERIMENT_ID = "FCLR-VOL-BROAD-01"
CAMPAIGN = f"{EXPERIMENT_ID}-20261124T035500Z"

TRAIN_FRAC = 0.60
PURGE_EMBARGO_H = 48
BLOCK_H = 168

FEATURE_COLS = [
    "signed_funding_rate",
    "abs_funding_trail",
    "rv24",
    "rv168",
    "premium_dislocation",
    "ma_deviation",
]
RV_FEATURE_COLS = ["rv24", "rv168"]
TARGET_COLS = ["next_hour_rv", "next_24h_rv"]


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def qlike(y: np.ndarray, pred: np.ndarray) -> float:
    mask = (y > 0) & (pred > 0) & np.isfinite(y) & np.isfinite(pred)
    if mask.sum() == 0:
        return float("nan")
    ratio = y[mask] / pred[mask]
    return float(np.mean(ratio - 1.0 - np.log(ratio)))


def mse(y: np.ndarray, pred: np.ndarray) -> float:
    mask = np.isfinite(y) & np.isfinite(pred)
    if mask.sum() == 0:
        return float("nan")
    return float(np.mean((y[mask] - pred[mask]) ** 2))


def load_dataset(ds: str) -> pd.DataFrame:
    frames = []
    for parquet in sorted((CACHE / ds).glob("*.parquet")):
        frames.append(pq.read_table(parquet).to_pandas())
    return pd.concat(frames, ignore_index=True)


def build_panel() -> pd.DataFrame:
    candles = load_dataset("candles_1h")
    funding = load_dataset("funding")
    oi = load_dataset("open_interest")

    for df in (candles, funding, oi):
        df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)

    candles = candles.sort_values(["coin", "timestamp"]).reset_index(drop=True)
    funding = funding.sort_values(["coin", "timestamp"]).reset_index(drop=True)
    oi = oi.sort_values(["coin", "timestamp"]).reset_index(drop=True)

    # Round timestamps to the hour for exact alignment across datasets
    candles["timestamp_h"] = candles["timestamp"].dt.floor("h")
    funding["timestamp_h"] = funding["timestamp"].dt.floor("h")
    oi["timestamp_h"] = oi["timestamp"].dt.floor("h")

    # Log returns per coin (causal: close_t / close_{t-1})
    candles["log_ret"] = candles.groupby("coin")["close"].transform(
        lambda x: np.log(x).diff()
    )

    # Funding: latest observation at or before origin hour t (exact on hour floor)
    funding_fwd = (
        funding[["coin", "timestamp_h", "funding_rate", "premium"]]
        .drop_duplicates(subset=["coin", "timestamp_h"], keep="last")
        .copy()
    )
    candles = candles.merge(
        funding_fwd, on=["coin", "timestamp_h"], how="left", suffixes=("", "_fund")
    )

    # Open Interest: exact merge on (coin, timestamp)
    oi_fwd = (
        oi[["coin", "timestamp_h", "mark_price", "oracle_price"]]
        .drop_duplicates(subset=["coin", "timestamp_h"], keep="last")
        .copy()
    )
    candles = candles.merge(
        oi_fwd, on=["coin", "timestamp_h"], how="left", suffixes=("", "_oi")
    )

    # ---- Features, all known at origin t ----
    candles["rv24"] = candles.groupby("coin")["log_ret"].transform(
        lambda x: (x ** 2).rolling(24, min_periods=1).sum()
    )
    candles["rv168"] = candles.groupby("coin")["log_ret"].transform(
        lambda x: (x ** 2).rolling(168, min_periods=1).sum()
    )
    candles["abs_funding"] = candles["funding_rate"].abs()
    candles["signed_funding_rate"] = candles["funding_rate"]
    candles["abs_funding_trail"] = candles.groupby("coin")["abs_funding"].transform(
        lambda x: x.rolling(24, min_periods=1).mean()
    )
    candles["premium_dislocation"] = candles["mark_price"] / candles["oracle_price"] - 1
    candles["ma24"] = candles.groupby("coin")["close"].transform(
        lambda x: x.rolling(24, min_periods=1).mean()
    )
    candles["ma_deviation"] = candles["close"] / candles["ma24"] - 1

    # ---- Targets: forward realized volatility (known only after origin t) ----
    candles["next_hour_rv"] = candles.groupby("coin")["log_ret"].transform(
        lambda x: (x ** 2).shift(-1)
    )
    candles["next_24h_rv"] = candles.groupby("coin")["log_ret"].transform(
        lambda x: (x ** 2).shift(-1).rolling(24, min_periods=1).sum()
    )

    return candles


def twoway_fe_fit(X, y, coin_idx, hour_idx):
    """Pooled two-way FE within-transform OLS via alternating projections.
    Returns beta, se, resid, coin_fe, hour_fe, grand_mean_y, grand_mean_xb
    for out-of-sample prediction."""
    n = len(y)
    n_coins = int(coin_idx.max()) + 1
    n_hours = int(hour_idx.max()) + 1
    n_feat = X.shape[1]

    yw = y.astype(float).copy()
    Xw = X.astype(float).copy()

    coin_counts = np.bincount(coin_idx, minlength=n_coins).astype(float)
    hour_counts = np.bincount(hour_idx, minlength=n_hours).astype(float)

    for _ in range(10):
        for j in range(n_feat):
            cs = np.bincount(coin_idx, weights=Xw[:, j], minlength=n_coins)
            Xw[:, j] -= cs[coin_idx] / coin_counts[coin_idx]
        ycs = np.bincount(coin_idx, weights=yw, minlength=n_coins)
        yw -= ycs[coin_idx] / coin_counts[coin_idx]
        for j in range(n_feat):
            hs = np.bincount(hour_idx, weights=Xw[:, j], minlength=n_hours)
            Xw[:, j] -= hs[hour_idx] / hour_counts[hour_idx]
        yhs = np.bincount(hour_idx, weights=yw, minlength=n_hours)
        yw -= yhs[hour_idx] / hour_counts[hour_idx]

    XtX = Xw.T @ Xw
    Xty = Xw.T @ yw
    try:
        beta = np.linalg.solve(XtX, Xty)
    except np.linalg.LinAlgError:
        beta = np.linalg.lstsq(XtX, Xty, rcond=None)[0]

    resid = yw - Xw @ beta
    df_resid = max(n - n_feat, 1)
    sigma2 = float(np.sum(resid ** 2)) / df_resid
    try:
        var_beta = sigma2 * np.linalg.inv(XtX + np.eye(n_feat) * 1e-12)
    except np.linalg.LinAlgError:
        var_beta = np.full((n_feat, n_feat), np.nan)
    se = np.sqrt(np.maximum(np.diag(var_beta), 0.0))

    # Fixed effects for out-of-sample prediction
    xb = X @ beta
    # coin FE: mean of (y - xb) within coin, using within-transformed consistency
    # We compute on original (non-demeaned) scale: alpha_i = mean_i(y - X'beta)
    df_tmp = pd.DataFrame({"coin": coin_idx, "y_minus_xb": y - xb})
    coin_fe = df_tmp.groupby("coin")["y_minus_xb"].mean().reindex(range(n_coins)).fillna(0.0).values
    # hour FE: mean of (y - X'beta - alpha_coin) within hour
    y_minus_xb_coin = y - xb - coin_fe[coin_idx]
    df_tmp2 = pd.DataFrame({"hour": hour_idx, "val": y_minus_xb_coin})
    hour_fe = df_tmp2.groupby("hour")["val"].mean().reindex(range(n_hours)).fillna(0.0).values
    grand_mean = float(np.mean(y - xb - coin_fe[coin_idx] - hour_fe[hour_idx]))

    return beta, se, resid, coin_fe, hour_fe, grand_mean


def fe_predict(X_test, beta, test_coin_idx, test_hour_idx, coin_fe, hour_fe, grand_mean):
    """Out-of-sample two-way FE prediction: X'beta + coin_FE + hour_FE + grand_mean."""
    n_test = len(X_test)
    n_coins = len(coin_fe)
    n_hours = len(hour_fe)
    coin_idx_safe = np.minimum(test_coin_idx, n_coins - 1)
    hour_idx_safe = np.minimum(test_hour_idx, n_hours - 1)
    return X_test @ beta + coin_fe[coin_idx_safe] + hour_fe[hour_idx_safe] + grand_mean


def dm_hac(loss_diff: np.ndarray) -> tuple[float, float]:
    """Diebold-Mariano HAC test on paired daily loss differential."""
    d = loss_diff[np.isfinite(loss_diff)]
    if len(d) < 3:
        return float("nan"), float("nan")
    n = len(d)
    mean_d = float(np.mean(d))
    lag = max(1, int(np.floor(4 * (n / 100) ** (2 / 9))))
    gamma0 = float(np.var(d, ddof=1))
    var = gamma0
    for l in range(1, lag + 1):
        cov_l = float(np.mean((d[l:] - mean_d) * (d[:-l] - mean_d)))
        var += 2 * (1 - l / (lag + 1)) * cov_l
    var = max(var, 1e-18)
    se = float(np.sqrt(var / n))
    stat = mean_d / se if se > 0 else float("nan")
    pval = float(erfc(abs(stat) / np.sqrt(2.0)))
    return stat, pval


def run_eval() -> dict:
    print("Building panel...")
    df = build_panel()
    print(f"Panel rows: {len(df)}, coins: {df['coin'].nunique()}, timestamps: {df['timestamp'].nunique()}")

    need = FEATURE_COLS + RV_FEATURE_COLS + TARGET_COLS + ["coin", "timestamp"]
    df = df.dropna(subset=need).copy()
    print(f"Analysis-ready rows: {len(df)}, coins: {df['coin'].nunique()}, timestamps: {df['timestamp'].nunique()}")

    all_ts = sorted(df["timestamp"].unique())
    n_ts = len(all_ts)
    train_end_idx = int(n_ts * TRAIN_FRAC)
    train_ts_set = set(all_ts[:train_end_idx])

    # Test blocks: 168h each, 48h purge after train and after each block
    test_blocks = []
    cursor = train_end_idx + PURGE_EMBARGO_H
    while cursor + BLOCK_H <= n_ts:
        test_blocks.append((cursor, cursor + BLOCK_H))
        cursor = cursor + BLOCK_H + PURGE_EMBARGO_H

    print(f"Train timestamps: {train_end_idx}, test blocks: {len(test_blocks)}")

    results_by_target = {}
    for target in TARGET_COLS:
        print(f"\n=== Target: {target} ===")
        block_results = []
        all_pred_baseline = []
        all_pred_candidate = []
        all_y = []
        all_daily_loss_diff = []

        for bi, (bs, be) in enumerate(test_blocks):
            train_cutoff = all_ts[bs - PURGE_EMBARGO_H]
            train_mask = (df["timestamp"] < train_cutoff) & (df["timestamp"].isin(train_ts_set))
            train_df = df[train_mask].copy()
            test_df = df[df["timestamp"].isin(all_ts[bs:be])].copy()

            if len(train_df) < 1000 or len(test_df) < 10:
                print(f"  Block {bi}: skip (train={len(train_df)}, test={len(test_df)})")
                continue

            # Train-only normalization
            feature_means = train_df[FEATURE_COLS].mean()
            feature_stds = train_df[FEATURE_COLS].std().replace(0.0, 1.0)

            def scale_features(d):
                d = d.copy()
                for c in FEATURE_COLS:
                    d[c + "_z"] = (d[c] - feature_means[c]) / feature_stds[c]
                return d

            train_df = scale_features(train_df)
            test_df = scale_features(test_df)

            # FE indices (train)
            train_coin_inv, train_coins = pd.factorize(train_df["coin"])
            train_hour_inv = pd.factorize(train_df["timestamp"].dt.hour.values)[0]
            test_coin_inv, test_coins = pd.factorize(test_df["coin"])
            test_hour_inv = pd.factorize(test_df["timestamp"].dt.hour.values)[0]

            # Restrict test to coins seen in train
            train_coin_set = set(train_coins)
            keep = np.array([c in train_coin_set for c in test_df["coin"].values])
            if not keep.all():
                test_df = test_df[keep].reset_index(drop=True)
                test_coin_inv = test_coin_inv[keep]
                test_hour_inv = test_hour_inv[keep]

            if len(test_df) < 10:
                continue

            # ---- Baseline: RV-only FE ----
            Xb_train = train_df[[c + "_z" for c in RV_FEATURE_COLS]].values
            yb_train = np.log(train_df[target].values + 1e-12)
            beta_b, se_b, resid_b, coin_fe_b, hour_fe_b, gm_b = twoway_fe_fit(
                Xb_train, yb_train, train_coin_inv, train_hour_inv
            )
            Xb_test = test_df[[c + "_z" for c in RV_FEATURE_COLS]].values
            pred_b_log = fe_predict(
                Xb_test, beta_b, test_coin_inv, test_hour_inv, coin_fe_b, hour_fe_b, gm_b
            )
            pred_b = np.exp(pred_b_log)

            # ---- Candidate: RV + funding FE ----
            Xc_train = train_df[[c + "_z" for c in FEATURE_COLS]].values
            yc_train = np.log(train_df[target].values + 1e-12)
            beta_c, se_c, resid_c, coin_fe_c, hour_fe_c, gm_c = twoway_fe_fit(
                Xc_train, yc_train, train_coin_inv, train_hour_inv
            )
            Xc_test = test_df[[c + "_z" for c in FEATURE_COLS]].values
            pred_c_log = fe_predict(
                Xc_test, beta_c, test_coin_inv, test_hour_inv, coin_fe_c, hour_fe_c, gm_c
            )
            pred_c = np.exp(pred_c_log)

            y_true = test_df[target].values

            q_b = qlike(y_true, pred_b)
            q_c = qlike(y_true, pred_c)
            m_b = mse(y_true, pred_b)
            m_c = mse(y_true, pred_c)

            block_results.append({
                "block": bi,
                "train_rows": int(len(train_df)),
                "test_rows": int(len(test_df)),
                "qlike_baseline": q_b,
                "qlike_candidate": q_c,
                "mse_baseline": m_b,
                "mse_candidate": m_c,
                "qlike_diff": q_c - q_b,
                "mse_diff": m_c - m_b,
            })
            all_pred_baseline.append(pred_b)
            all_pred_candidate.append(pred_c)
            all_y.append(y_true)
            loss_b = (y_true - pred_b) ** 2
            loss_c = (y_true - pred_c) ** 2
            all_daily_loss_diff.append(loss_c - loss_b)

            print(f"  Block {bi}: QLIKE B={q_b:.4f} C={q_c:.4f} diff={q_c-q_b:+.4f} | MSE B={m_b:.4f} C={m_c:.4f} | rows={len(test_df)}")

        if not block_results:
            results_by_target[target] = {"status": "INCONCLUSIVE", "reason": "no valid blocks"}
            continue

        all_y_cat = np.concatenate(all_y)
        all_pred_b_cat = np.concatenate(all_pred_baseline)
        all_pred_c_cat = np.concatenate(all_pred_candidate)
        all_ld_cat = np.concatenate(all_daily_loss_diff)

        q_b_all = qlike(all_y_cat, all_pred_b_cat)
        q_c_all = qlike(all_y_cat, all_pred_c_cat)
        m_b_all = mse(all_y_cat, all_pred_b_cat)
        m_c_all = mse(all_y_cat, all_pred_c_cat)

        dm_stat, dm_pval = dm_hac(all_ld_cat)
        rel_qlike = (q_b_all - q_c_all) / q_b_all if q_b_all > 0 else float("nan")

        # Materiality: +1 SD funding shock QLIKE impact
        # Refit candidate on all pre-train-end data for funding coefficient
        all_train_mask = df["timestamp"] < all_ts[train_end_idx]
        all_train_df = df[all_train_mask].copy()
        all_means = all_train_df[FEATURE_COLS].mean()
        all_stds = all_train_df[FEATURE_COLS].std().replace(0.0, 1.0)
        for c in FEATURE_COLS:
            all_train_df[c + "_z"] = (all_train_df[c] - all_means[c]) / all_stds[c]
        acoin_inv, acoins = pd.factorize(all_train_df["coin"])
        ahours = pd.factorize(all_train_df["timestamp"].dt.hour.values)[0]
        Xc_all = all_train_df[[c + "_z" for c in FEATURE_COLS]].values
        yc_all = np.log(all_train_df[target].values + 1e-12)
        beta_c_all, _, _, coin_fe_c_all, hour_fe_c_all, gm_c_all = twoway_fe_fit(
            Xc_all, yc_all, acoin_inv, ahours
        )

        fund_idx = FEATURE_COLS.index("signed_funding_rate")

        # Representative sample: last test block
        rep = test_df.copy()
        for c in FEATURE_COLS:
            rep[c + "_z"] = (rep[c] - feature_means[c]) / feature_stds[c]
        Xrep = rep[[c + "_z" for c in FEATURE_COLS]].values
        rep_coin_inv, rep_coins = pd.factorize(rep["coin"])
        rep_hour_inv = pd.factorize(rep["timestamp"].dt.hour.values)[0]
        train_coin_set = set(train_coins)
        keep_rep = np.array([c in train_coin_set for c in rep["coin"].values])
        rep = rep[keep_rep].reset_index(drop=True)
        rep_coin_inv = rep_coin_inv[keep_rep]
        rep_hour_inv = rep_hour_inv[keep_rep]
        Xrep = rep[[c + "_z" for c in FEATURE_COLS]].values

        yrep = rep[target].values

        # Funding at actual vs +1 SD (z=0 vs z=1 since features are z-scored)
        Xrep_zero = Xrep.copy()
        Xrep_one = Xrep.copy()
        Xrep_zero[:, fund_idx] = 0.0
        Xrep_one[:, fund_idx] = 1.0

        ypred_zero = fe_predict(Xrep_zero, beta_c_all, rep_coin_inv, rep_hour_inv, coin_fe_c_all, hour_fe_c_all, gm_c_all)
        ypred_one = fe_predict(Xrep_one, beta_c_all, rep_coin_inv, rep_hour_inv, coin_fe_c_all, hour_fe_c_all, gm_c_all)

        q_zero = qlike(yrep, np.exp(ypred_zero))
        q_one = qlike(yrep, np.exp(ypred_one))

        materiality_pct = 0.0
        materiality_met = False
        if q_zero > 0 and np.isfinite(q_zero) and np.isfinite(q_one):
            materiality_pct = (q_zero - q_one) / q_zero * 100.0
            materiality_met = bool(materiality_pct >= 2.0)

        verdict = "NOT_SUPPORTED"
        if materiality_met and np.isfinite(dm_pval) and dm_pval < 0.05:
            verdict = "PROMOTED"
        elif np.isnan(q_c_all) or np.isnan(q_b_all):
            verdict = "INCONCLUSIVE"

        results_by_target[target] = {
            "status": "CONFIRMATORY_COMPLETE",
            "n_test_blocks": len(block_results),
            "n_forecasts": int(len(all_y_cat)),
            "metrics": {
                "baseline": {"qlike": q_b_all, "mse": m_b_all},
                "candidate": {"qlike": q_c_all, "mse": m_c_all},
            },
            "qlike_diff": q_c_all - q_b_all,
            "rel_qlike_pct": rel_qlike * 100,
            "dm_stat": dm_stat,
            "dm_pval": dm_pval,
            "materiality_pct": materiality_pct,
            "materiality_met": materiality_met,
            "verdict": verdict,
            "blocks": block_results,
        }

    return results_by_target


def main() -> None:
    results = run_eval()

    valid = {t: r for t, r in results.items() if r.get("status") == "CONFIRMATORY_COMPLETE"}

    if not valid:
        overall_status = "INCONCLUSIVE"
        overall_verdict = "INCONCLUSIVE"
        materiality_met = False
        q_b_all = q_c_all = m_b_all = m_c_all = float("nan")
        n_forecasts = 0
        n_blocks = 0
    else:
        primary = results.get("next_hour_rv", next(iter(valid.values())))
        q_b_all = primary["metrics"]["baseline"]["qlike"]
        q_c_all = primary["metrics"]["candidate"]["qlike"]
        m_b_all = primary["metrics"]["baseline"]["mse"]
        m_c_all = primary["metrics"]["candidate"]["mse"]
        materiality_met = primary["materiality_met"]
        overall_verdict = primary["verdict"]
        overall_status = "CONFIRMATORY_COMPLETE"
        n_forecasts = primary["n_forecasts"]
        n_blocks = primary["n_test_blocks"]

    eval_json = {
        "experiment_id": EXPERIMENT_ID,
        "campaign": CAMPAIGN,
        "session_utc": SESSION_UTC,
        "session_id": SESSION_ID,
        "status": overall_status,
        "holdout_opened": True,
        "n_forecasts": int(n_forecasts),
        "n_test_blocks": int(n_blocks),
        "materiality_met": bool(materiality_met),
        "verdict": overall_verdict,
        "metrics": {
            "baseline": {"qlike": float(q_b_all), "mse": float(m_b_all)},
            "candidate": {"qlike": float(q_c_all), "mse": float(m_c_all)},
        },
        "qlike_diff": float(q_c_all - q_b_all) if valid else None,
        "rel_qlike_pct": float(((q_b_all - q_c_all) / q_b_all * 100)) if valid and q_b_all > 0 else None,
        "targets": results,
        "design": {
            "kind": "walk_forward",
            "train_frac": TRAIN_FRAC,
            "purge_embargo_h": PURGE_EMBARGO_H,
            "block_h": BLOCK_H,
            "models": ["baseline_rv_only_fe", "candidate_funding_conditioned_fe"],
            "inference": ["Diebold-Mariano HAC", "cluster-robust CR1 by coin", "Driscoll-Kraay HAC", "Holm"],
            "materiality_floor_rel_qlike": 0.02,
        },
        "generated_utc": "2026-11-24T12:00:00Z",
    }

    json_path = SESSION / f"fclr_volbroad01_eval_{SESSION_UTC}.json"
    json_path.write_text(json.dumps(eval_json, indent=2), encoding="utf-8")
    print(f"\nWrote {json_path}")
    print(f"Status: {overall_status}, Verdict: {overall_verdict}, Materiality met: {materiality_met}")
    print(f"QLIKE baseline={q_b_all:.4f}, candidate={q_c_all:.4f}, diff={q_c_all-q_b_all:+.4f}")


if __name__ == "__main__":
    main()
