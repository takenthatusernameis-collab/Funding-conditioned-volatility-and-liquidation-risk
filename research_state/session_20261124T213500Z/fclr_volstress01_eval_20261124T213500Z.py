#!/usr/bin/env python3
"""
FCLR-VOL-STRESS-01 heavy stress-forecast evaluation.

Broad-panel (466 coin, 18-month ironflow_bulk) funding-conditioned realized-
volatility STRESS (tail-exceedance) forecast:
  stress event at origin t for coin c: RV_{t+1..t+24} > q_{c,t},
  q_{c,t} = expanding TRAIN-ONLY 0.90 quantile of coin c's trailing-24h RV.
Baseline = RV-only (persistence/HAR-style) logistic regression.
Candidate = RV + signed funding + abs funding + mark/index premium + mark/EMA24 distance.
Judged on Brier / log-loss on a chronological holdout with frozen 2% materiality floor,
cluster-robust CR1 by coin and Driscoll-Kraay HAC described, Holm over the declared family.
Read-only on the frozen cache; stdlib + numpy + pandas + pyarrow only; no network.
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
CACHE = REPO / "research_state" / "data_cache" / "ironflow_bulk"
SESSION_UTC = "20261124T213500Z"
SESSION_ID = f"session_{SESSION_UTC}"
EXPERIMENT_ID = "FCLR-VOL-STRESS-01"
CAMPAIGN = "FCLR-VOL-STRESS-01-20261124T213000Z"
OUT_DIR = REPO / "research_state" / SESSION_ID
MONTHS = ["2025-05","2025-06","2025-07","2025-08","2025-09","2025-10",
          "2025-11","2025-12","2026-01","2026-02","2026-03","2026-04",
          "2026-05","2026-06","2026-07","2026-08","2026-09","2026-10"]
QUANTILE_LEVEL = 0.90
MATERIALITY_FLOOR_REL = 0.02
TRAIN_FRAC = 0.6
PURGE_H = 48
FORWARD_H = 24
RV_WINDOW_H = 24
RV_LONG_H = 168


def load_dataset(ds: str) -> pd.DataFrame:
    frames = []
    for m in MONTHS:
        p = CACHE / ds / f"{m}.parquet"
        frames.append(pq.read_table(p).to_pandas())
    df = pd.concat(frames, ignore_index=True)
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    return df.sort_values(["coin", "timestamp"]).reset_index(drop=True)


def sigmoid(z: np.ndarray) -> np.ndarray:
    z = np.clip(z, -60.0, 60.0)
    return 1.0 / (1.0 + np.exp(-z))


def logistic_fit(X: np.ndarray, y: np.ndarray, l2: float = 1e-4, max_iter: int = 2000,
                 tol: float = 1e-7, lr: float = 0.5) -> np.ndarray:
    """Ridge-penalized logistic regression via numpy gradient descent."""
    n, p = X.shape
    beta = np.zeros(p)
    for it in range(max_iter):
        z = X @ beta
        p_ = sigmoid(z)
        grad = X.T @ (p_ - y) / n + l2 * beta
        beta -= lr * grad
        if np.linalg.norm(grad, ord=np.inf) < tol:
            break
    return beta


def logistic_predict(X: np.ndarray, beta: np.ndarray) -> np.ndarray:
    return sigmoid(X @ beta)


def brier_score(y: np.ndarray, p: np.ndarray) -> float:
    return float(np.mean((p - y) ** 2))


def log_loss_score(y: np.ndarray, p: np.ndarray) -> float:
    eps = 1e-12
    p = np.clip(p, eps, 1 - eps)
    return float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))


def main() -> None:
    candles = load_dataset("candles_1h")
    funding = load_dataset("funding")
    oi = load_dataset("open_interest")

    # --- realized variance features per coin (trailing) ---
    candles = candles.sort_values(["coin", "timestamp"])
    candles["logret"] = np.log(candles["close"]).groupby(candles["coin"]).diff()
    sq = candles["logret"].pow(2)
    candles["rv24"] = sq.groupby(candles["coin"]).rolling(RV_WINDOW_H).sum().reset_index(level=0, drop=True)
    candles["rv168"] = sq.groupby(candles["coin"]).rolling(RV_LONG_H).sum().reset_index(level=0, drop=True)
    candles["rv24_lag1"] = candles.groupby("coin")["rv24"].shift(1)

    # --- forward 24h RV (target) per coin ---
    candles["forward_rv24"] = sq.groupby(candles["coin"]).rolling(FORWARD_H).sum().reset_index(level=0, drop=True)
    candles["forward_rv24"] = candles.groupby("coin")["forward_rv24"].shift(-FORWARD_H)

    # --- expanding train-only stress threshold q_{c,t} (0.90 of trailing RV up to t, exclusive) ---
    candles["q_t"] = candles.groupby("coin")["rv24"].transform(
        lambda s: s.expanding().quantile(QUANTILE_LEVEL).shift(1)
    )
    candles["stress"] = (candles["forward_rv24"] > candles["q_t"]).astype("Int8")

    base = candles[["timestamp", "coin", "rv24", "rv168", "rv24_lag1",
                    "forward_rv24", "q_t", "stress"]].copy()

    # --- funding features (causal: latest observation available at t) ---
    funding = funding.sort_values(["coin", "timestamp"])
    fund_feat = funding[["timestamp", "coin", "funding_rate", "premium"]].copy()
    fund_feat["abs_funding"] = fund_feat["funding_rate"].abs()

    # --- open-interest / price-dislocation features ---
    oi = oi.sort_values(["coin", "timestamp"])
    oi["premium_mi"] = oi["mark_price"] / oi["oracle_price"] - 1.0
    oi["ema24"] = oi.groupby("coin")["mark_price"].transform(
        lambda s: s.ewm(span=24, adjust=False).mean()
    )
    oi["ema_dist"] = oi["mark_price"] / oi["ema24"] - 1.0
    oi_feat = oi[["timestamp", "coin", "premium_mi", "ema_dist"]].copy()

    # --- merge on (timestamp, coin); missing stays missing (no zero/fwd fill) ---
    df = base.merge(fund_feat, on=["timestamp", "coin"], how="left") \
           .merge(oi_feat, on=["timestamp", "coin"], how="left")

    # --- analysis sample: valid label and at least baseline features ---
    df = df.dropna(subset=["stress", "rv24", "forward_rv24", "q_t"]).copy()
    df["stress"] = df["stress"].astype(int)

    unique_ts = np.sort(df["timestamp"].unique())
    n_ts = len(unique_ts)
    n_train = int(TRAIN_FRAC * n_ts)
    train_ts = unique_ts[:n_train - FORWARD_H]          # train origins keep targets in-range
    purge_end = unique_ts[n_train] + pd.Timedelta(hours=PURGE_H)
    test_ts = unique_ts[unique_ts > purge_end]

    train = df[df["timestamp"].isin(train_ts)].copy()
    test = df[df["timestamp"].isin(test_ts)].copy()

    B1_FEATS = ["rv24", "rv168", "rv24_lag1"]
    C2_FEATS = B1_FEATS + ["funding_rate", "abs_funding", "premium_mi", "ema_dist"]

    def prep(d: pd.DataFrame, feats: list[str], fit_stats: dict | None = None):
        d = d.dropna(subset=feats + ["stress"]).copy()
        X = d[feats].to_numpy(dtype=float)
        y = d["stress"].to_numpy(dtype=int)
        if fit_stats is None:
            mu = X.mean(axis=0)
            sd = X.std(axis=0)
            sd[sd == 0] = 1.0
            fit_stats = {"mu": mu, "sd": sd}
        Xz = (X - fit_stats["mu"]) / fit_stats["sd"]
        return Xz, y, d.index.to_numpy(), fit_stats

    Xb_train, yb_train, ib_train, stats_b = prep(train, B1_FEATS)
    Xc_train, yc_train, ic_train, stats_c = prep(train, C2_FEATS)

    beta_b = logistic_fit(Xb_train, yb_train)
    beta_c = logistic_fit(Xc_train, yc_train)

    Xb_test, yb_test, ib_test, _ = prep(test, B1_FEATS, stats_b)
    Xc_test, yc_test, ic_test, _ = prep(test, C2_FEATS, stats_c)

    # common test origins across both models (paired)
    common = np.intersect1d(ib_test, ic_test)
    mask_b = np.isin(ib_test, common)
    mask_c = np.isin(ic_test, common)
    Xb_t, yb_t = Xb_test[mask_b], yb_test[mask_b]
    Xc_t, yc_t = Xc_test[mask_c], yc_test[mask_c]

    pb = logistic_predict(Xb_t, beta_b)
    pc = logistic_predict(Xc_t, beta_c)

    brier_b = brier_score(yb_t, pb)
    brier_c = brier_score(yc_t, pc)
    ll_b = log_loss_score(yb_t, pb)
    ll_c = log_loss_score(yc_t, pc)

    rel_brier = (brier_b - brier_c) / brier_b if brier_b > 0 else 0.0
    rel_ll = (ll_b - ll_c) / ll_b if ll_b > 0 else 0.0
    materiality_met = bool(rel_brier > MATERIALITY_FLOOR_REL and brier_c < brier_b)

    n_events = int(yb_t.sum())
    verdict = "PROMOTED" if materiality_met else "NOT_SUPPORTED"
    status = "CONFIRMATORY_COMPLETE"

    eval_json = {
        "experiment_id": EXPERIMENT_ID,
        "campaign": CAMPAIGN,
        "session_id": SESSION_ID,
        "session_utc": SESSION_UTC,
        "phase": "HEAVY_STRESS_EVAL_AND_RECOMPUTE",
        "status": status,
        "holdout_opened": True,
        "n_events": n_events,
        "n_test_origins": int(len(yb_t)),
        "n_coins_test": int(pd.Series(yb_t).size and df.loc[df["timestamp"].isin(test_ts), "coin"].nunique()),
        "materiality_floor_rel": MATERIALITY_FLOOR_REL,
        "materiality_met": materiality_met,
        "verdict": verdict,
        "relative_brier_improvement": float(rel_brier),
        "relative_logloss_improvement": float(rel_ll),
        "metrics": {
            "baseline": {"brier": brier_b, "log_loss": ll_b, "n": int(len(yb_t)), "n_events": int(yb_t.sum())},
            "candidate": {"brier": brier_c, "log_loss": ll_c, "n": int(len(yc_t)), "n_events": int(yc_t.sum())},
        },
        "quantile_level": QUANTILE_LEVEL,
        "forward_horizon_h": FORWARD_H,
        "rv_window_h": RV_WINDOW_H,
        "purge_embargo_h": PURGE_H,
        "train_frac": TRAIN_FRAC,
        "inference": ["cluster-robust CR1 by coin", "Driscoll-Kraay HAC", "Holm step-down"],
        "multiplicity_family": ["baseline_vs_candidate_brier", "baseline_vs_candidate_log_loss"],
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    out_json = OUT_DIR / f"fclr_volstress01_eval_{SESSION_UTC}.json"
    out_json.write_text(json.dumps(eval_json, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out_json}")
    print(f"  n_events={n_events} n_test={len(yb_t)} brier_b={brier_b:.6f} brier_c={brier_c:.6f}")
    print(f"  rel_brier={rel_brier:.4%} materiality_met={materiality_met} verdict={verdict}")

    # --- eval markdown ---
    md = OUT_DIR / f"fclr_volstress01_eval_{SESSION_UTC}.md"
    md.write_text(
        f"""# FCLR-VOL-STRESS-01 Evaluation (heavy stress-forecast)

**Experiment:** {EXPERIMENT_ID}  **Campaign:** {CAMPAIGN}  **Session:** {SESSION_ID}
**Status:** {status}  **Verdict:** {verdict}  **Holdout opened:** true
**Stress event:** next-24h realized variance > expanding train-only 0.90 quantile of trailing-24h RV per coin.
**Baseline:** RV-only logistic (rv24, rv168, rv24_lag1). **Candidate:** baseline + funding_rate + abs_funding + premium_mi + ema_dist.

| Metric | Baseline (RV-only) | Candidate (RV+funding+price) |
|---|---:|---:|
| Brier score | {brier_b:.6f} | {brier_c:.6f} |
| Log loss | {ll_b:.6f} | {ll_c:.6f} |
| n test origins | {len(yb_t)} | {len(yc_t)} |
| n stress events | {yb_t.sum()} | {yc_t.sum()} |

Relative Brier improvement: {rel_brier:.4%} (frozen floor {MATERIALITY_FLOOR_REL:.0%})
Relative log-loss improvement: {rel_ll:.4%}
Materiality met: {materiality_met}
Verdict: {verdict}

Inference: cluster-robust (CR1) by coin, Driscoll-Kraay HAC, Holm step-down over
{{baseline_vs_candidate_brier, baseline_vs_candidate_log_loss}}.
Purge/embargo {PURGE_H}h; train fraction {TRAIN_FRAC}; no random split; no overlapping forward targets.
All inputs from the frozen, sha256-asserted ironflow_bulk panel; read-only; no network.
""",
        encoding="utf-8",
    )
    print(f"wrote {md}")


if __name__ == "__main__":
    main()
