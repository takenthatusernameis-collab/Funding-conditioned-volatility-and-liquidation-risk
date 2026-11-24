#!/usr/bin/env python3
"""FCLR-VOL-STRESS-01 heavy evaluation: broad-panel funding-conditioned
volatility-STRESS (tail-exceedance) forecast.

Outcome-blind design frozen in the prereg (bound to the source-registry sha256):
  - target  : y_t = 1 if forward 24h realized variance RV_{t+1..t+24} > q_t,
              where q_t is an expanding, TRAIN-ONLY per-coin 0.95 quantile of
              trailing 24h realized variance (monthly checkpoints, prior months only).
  - baseline: RV-only (HAR-style trailing log-RV lags) logistic.
  - candidate: RV-only + signed funding_rate + |funding_rate| + premium +
              mark/EMA24 distance.
  - walk-forward expanding train, 6 x 2-month test blocks, 48h purge+embargo.
  - metrics: Brier, log-loss, ECE; relative improvement vs baseline.
  - inference: cluster bootstrap by coin, Driscoll-Kraay HAC (block level),
    Holm step-down over the declared family.
  - frozen materiality floor: 2% relative Brier improvement.

Stdlib + numpy + pandas + pyarrow only. No network. Read-only over the frozen cache.
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
SESSION_UTC = "20261124T222500Z"
SESSION_ID = f"session_{SESSION_UTC}"
SESSION_DIR = RS / SESSION_ID
CAMPAIGN_ID = "FCLR-VOL-STRESS-01-20261124T213000Z"
EXPERIMENT_ID = "FCLR-VOL-STRESS-01"

MONTHS = [
    "2025-05", "2025-06", "2025-07", "2025-08", "2025-09", "2025-10",
    "2025-11", "2025-12", "2026-01", "2026-02", "2026-03", "2026-04",
    "2026-05", "2026-06", "2026-07", "2026-08", "2026-09", "2026-10",
]
QUANTILE_LEVEL = 0.95
MIN_HISTORY = 24 * 30          # 30 days of hourly returns before a threshold is defined
RV_WINDOW = 24                 # hours
FWD_WINDOW = 24                # hours
PURGE_EMBARGO_H = 48
N_TEST_BLOCKS = 6
BLOCK_MONTHS = 2
INITIAL_TRAIN_MONTHS = 6
MATERIALITY_FLOOR_REL = 0.02
N_BOOT = 2000
BOOT_SEED = 20261124
N_LAGS = 3                     # HAR-style trailing RV lags (0,24,48h)
RIDGE = 1e-4


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def assert_sha256(parquet_path: Path) -> bool:
    sidecar = parquet_path.with_suffix(parquet_path.suffix + ".sha256")
    stored = sidecar.read_text(encoding="utf-8").strip().split()[0]
    return sha256_file(parquet_path) == stored


def load_month(dataset: str, month: str) -> pd.DataFrame:
    p = CACHE / dataset / f"{month}.parquet"
    if not assert_sha256(p):
        raise ValueError(f"sha256 mismatch for {p}")
    return pq.read_table(p).to_pandas()


def to_naive_utc(s: pd.Series) -> pd.Series:
    s = pd.to_datetime(s, utc=True)
    return s.dt.tz_convert(None)


def floor_hour(s: pd.Series) -> pd.Series:
    return to_naive_utc(s).dt.floor("h")


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


def sigmoid(z: np.ndarray) -> np.ndarray:
    out = np.empty_like(z, dtype=float)
    pos = z >= 0
    out[pos] = 1.0 / (1.0 + np.exp(-z[pos]))
    ez = np.exp(z[~pos])
    out[~pos] = ez / (1.0 + ez)
    return out


def fit_logistic(X: np.ndarray, y: np.ndarray, ridge: float = RIDGE,
                 n_iter: int = 40, tol: float = 1e-8) -> np.ndarray:
    """IRLS / Newton logistic with L2 (ridge) on non-intercept terms."""
    n, d = X.shape
    beta = np.zeros(d, dtype=float)
    reg = np.eye(d) * ridge
    reg[0, 0] = 0.0  # do not penalize intercept
    for _ in range(n_iter):
        p = sigmoid(X @ beta)
        w = np.clip(p * (1.0 - p), 1e-9, None)
        grad = X.T @ (y - p) - reg @ beta
        H = (X.T * w) @ X + reg
        try:
            step = np.linalg.solve(H, grad)
        except np.linalg.LinAlgError:
            step = np.linalg.lstsq(H, grad, rcond=None)[0]
        beta += step
        if np.max(np.abs(step)) < tol:
            break
    return beta


def brier(y: np.ndarray, p: np.ndarray) -> float:
    return float(np.mean((p - y) ** 2))


def log_loss(y: np.ndarray, p: np.ndarray) -> float:
    p = np.clip(p, 1e-12, 1.0 - 1e-12)
    return float(-np.mean(y * np.log(p) + (1.0 - y) * np.log(1.0 - p)))


def ece(y: np.ndarray, p: np.ndarray, n_bins: int = 10) -> float:
    edges = np.linspace(0.0, 1.0, n_bins + 1)
    total = 0.0
    n = len(y)
    for i in range(n_bins):
        lo, hi = edges[i], edges[i + 1]
        m = (p > lo) & (p <= hi) if i > 0 else (p >= lo) & (p <= hi)
        if m.sum() == 0:
            continue
        total += (m.sum() / n) * abs(y[m].mean() - p[m].mean())
    return float(total)


def driscoll_kraay_t(block_diffs: np.ndarray, lag: int = 2) -> float:
    """Block-level Driscoll-Kraay / Newey-West HAC t-stat for mean=0 test."""
    x = np.asarray(block_diffs, dtype=float)
    n = len(x)
    if n < 3:
        return float("nan")
    xbar = x.mean()
    e = x - xbar
    # HAC variance with Bartlett kernel
    var = float(e @ e) / n
    for l in range(1, min(lag, n - 1) + 1):
        w = 1.0 - l / (lag + 1.0)
        cov = float(e[l:] @ e[:-l]) / n
        var += 2.0 * w * cov
    if var <= 0:
        return float("nan")
    se = math.sqrt(var / n)
    return xbar / se if se > 0 else float("nan")


def run() -> dict:
    # ---- Load frozen inputs (sha256-asserted) ----
    candle_frames = [load_month("candles_1h", m) for m in MONTHS]
    candles = pd.concat(candle_frames, ignore_index=True)
    candles["timestamp"] = floor_hour(candles["timestamp"])
    candles = candles[["coin", "timestamp", "close"]].dropna()
    candles = candles.sort_values(["coin", "timestamp"]).reset_index(drop=True)

    fund_frames = [load_month("funding", m) for m in MONTHS]
    funding = pd.concat(fund_frames, ignore_index=True)
    funding["timestamp"] = floor_hour(funding["timestamp"])
    funding = funding[["coin", "timestamp", "funding_rate", "premium"]].dropna()
    funding = funding.groupby(["coin", "timestamp"], as_index=False).mean()

    oi_frames = [load_month("open_interest", m) for m in MONTHS]
    oi = pd.concat(oi_frames, ignore_index=True)
    oi["timestamp"] = floor_hour(oi["timestamp"])
    oi = oi[["coin", "timestamp", "mark_price"]].dropna()

    # ---- Per-coin hourly RV, forward RV, HAR lags ----
    parts = []
    for coin, g in candles.groupby("coin", sort=False):
        g = g.sort_values("timestamp")
        close = g["close"].to_numpy(dtype=float)
        if len(close) < MIN_HISTORY + FWD_WINDOW + N_LAGS * RV_WINDOW:
            continue
        close = np.where(close > 0, close, np.nan)
        logc = np.log(close)
        ret = np.diff(logc)  # ret[i] is return at index i+1
        sq = ret * ret
        n_ret = len(ret)
        # cumulative sum of squared returns, with leading zero
        C = np.concatenate([[0.0], np.cumsum(sq)])
        # index in return-space: return j (0-based) at row j+1
        # trailing RV at return j: mean sq[j-23..j]
        # forward RV at return j: mean sq[j+1..j+24]
        idx = np.arange(n_ret)
        trail = np.full(n_ret, np.nan)
        fwd = np.full(n_ret, np.nan)
        valid_trail = idx >= (RV_WINDOW - 1)
        trail[valid_trail] = (C[idx[valid_trail] + 1] - C[idx[valid_trail] - (RV_WINDOW - 1)]) / RV_WINDOW
        valid_fwd = idx + FWD_WINDOW < n_ret
        fwd[valid_fwd] = (C[idx[valid_fwd] + 1 + FWD_WINDOW] - C[idx[valid_fwd] + 1]) / FWD_WINDOW
        # map return index j -> row j+1
        rows = idx + 1
        ts = g["timestamp"].to_numpy()[rows]
        df = pd.DataFrame({
            "coin": coin,
            "timestamp": ts,
            "trailing_rv": trail,
            "forward_rv": fwd,
        })
        # HAR lags of trailing RV (shift by 24h rows)
        for lag in range(N_LAGS):
            df[f"rv_lag{lag}"] = df["trailing_rv"].shift(lag * RV_WINDOW)
        parts.append(df)
    panel = pd.concat(parts, ignore_index=True)
    panel = panel.dropna(subset=["trailing_rv", "forward_rv"]).reset_index(drop=True)
    panel["month"] = panel["timestamp"].dt.to_period("M")

    # ---- Merge funding + mark/EMA24 distance features (known at t) ----
    panel = panel.merge(funding, on=["coin", "timestamp"], how="left")
    panel["abs_funding"] = panel["funding_rate"].abs()
    # mark EMA24 distance per coin
    oi = oi.sort_values(["coin", "timestamp"])
    oi["mark_ema24"] = (
        oi.groupby("coin")["mark_price"]
        .transform(lambda s: s.ewm(span=RV_WINDOW, adjust=False).mean())
    )
    oi["mark_dist"] = (oi["mark_price"] - oi["mark_ema24"]) / oi["mark_ema24"]
    panel = panel.merge(oi[["coin", "timestamp", "mark_dist"]], on=["coin", "timestamp"], how="left")
    # forward-fill funding/oi features within coin (hourly grid, small gaps)
    panel = panel.sort_values(["coin", "timestamp"])
    for col in ["funding_rate", "abs_funding", "premium", "mark_dist"]:
        panel[col] = panel.groupby("coin")[col].ffill()
    panel = panel.dropna(subset=["funding_rate", "premium", "mark_dist"]).reset_index(drop=True)

    # ---- Expanding, TRAIN-ONLY per-coin 0.95 quantile (monthly checkpoints) ----
    panel = panel.sort_values(["coin", "timestamp"]).reset_index(drop=True)
    q = np.full(len(panel), np.nan)
    rv = panel["trailing_rv"].to_numpy()
    months = panel["month"].to_numpy()
    for coin, g in panel.groupby("coin", sort=False):
        idxs = g.index.to_numpy()
        rvc = rv[idxs]
        mc = months[idxs]
        change = np.flatnonzero(np.r_[True, mc[1:] != mc[:-1]])
        for k, start in enumerate(change):
            if start < MIN_HISTORY:
                continue
            qq = float(np.quantile(rvc[:start], QUANTILE_LEVEL))
            end = change[k + 1] if k + 1 < len(change) else len(g)
            q[idxs[start:end]] = qq
    panel["q"] = q
    panel["event"] = (panel["forward_rv"] > panel["q"]).astype(int)
    panel = panel[panel["q"].notna()].reset_index(drop=True)

    # ---- Feature matrices ----
    base_cols = [f"rv_lag{lag}" for lag in range(N_LAGS)]
    extra_cols = ["funding_rate", "abs_funding", "premium", "mark_dist"]
    panel = panel.dropna(subset=base_cols + extra_cols).reset_index(drop=True)

    # ---- Walk-forward expanding train, 6 x 2-month test blocks, 48h purge ----
    all_months = sorted(panel["month"].unique())
    test_records = []  # (block, coin, y, b_base, b_cand)
    block_brier = []
    for k in range(N_TEST_BLOCKS):
        tr_end = INITIAL_TRAIN_MONTHS + BLOCK_MONTHS * k
        te_start = tr_end
        te_end = te_start + BLOCK_MONTHS
        if te_end > len(all_months):
            break
        train_months = set(all_months[:tr_end])
        test_months = set(all_months[te_start:te_end])
        train = panel[panel["month"].isin(train_months)].copy()
        test = panel[panel["month"].isin(test_months)].copy()
        # purge/embargo: drop train rows within PURGE_EMBARGO_H before test start
        test_start_ts = test["timestamp"].min()
        cutoff = test_start_ts - pd.Timedelta(hours=PURGE_EMBARGO_H)
        train = train[train["timestamp"] < cutoff]
        if len(train) < 500 or len(test) < 100:
            continue
        # standardize on train
        all_cols = base_cols + extra_cols
        mu = train[all_cols].mean().to_numpy()
        sd = train[all_cols].std().to_numpy()
        sd = np.where(sd < 1e-12, 1.0, sd)
        col_pos = {c: i for i, c in enumerate(all_cols)}

        def design(df: pd.DataFrame, cols: list[str]) -> np.ndarray:
            pos = [col_pos[c] for c in cols]
            Z = (df[cols].to_numpy() - mu[pos]) / sd[pos]
            return np.column_stack([np.ones(len(df)), Z])

        Xb_tr = design(train, base_cols)
        Xb_te = design(test, base_cols)
        Xc_tr = design(train, base_cols + extra_cols)
        Xc_te = design(test, base_cols + extra_cols)
        y_tr = train["event"].to_numpy(dtype=float)
        y_te = test["event"].to_numpy(dtype=float)
        beta_b = fit_logistic(Xb_tr, y_tr)
        beta_c = fit_logistic(Xc_tr, y_tr)
        p_b = sigmoid(Xb_te @ beta_b)
        p_c = sigmoid(Xc_te @ beta_c)
        for cb, yv, pb, pc in zip(test["coin"].to_numpy(), y_te, p_b, p_c):
            test_records.append((k, cb, yv, pb, pc))
        block_brier.append((
            k,
            brier(y_te, p_b),
            brier(y_te, p_c),
            log_loss(y_te, p_b),
            log_loss(y_te, p_c),
        ))

    if not test_records:
        raise RuntimeError("no test records produced")

    rec = pd.DataFrame(test_records, columns=["block", "coin", "y", "p_base", "p_cand"])
    y = rec["y"].to_numpy()
    p_base = rec["p_base"].to_numpy()
    p_cand = rec["p_cand"].to_numpy()

    brier_base = brier(y, p_base)
    brier_cand = brier(y, p_cand)
    ll_base = log_loss(y, p_base)
    ll_cand = log_loss(y, p_cand)
    ece_base = ece(y, p_base)
    ece_cand = ece(y, p_cand)

    rel_brier = (brier_base - brier_cand) / brier_base if brier_base > 0 else float("nan")
    rel_ll = (ll_base - ll_cand) / ll_base if ll_base > 0 else float("nan")

    # ---- Cluster bootstrap by coin on Brier difference ----
    rng = np.random.default_rng(BOOT_SEED)
    coins = rec["coin"].to_numpy()
    unique_coins = np.unique(coins)
    coin_groups = {c: np.flatnonzero(coins == c) for c in unique_coins}
    boot_rel = np.empty(N_BOOT)
    base_sq = (p_base - y) ** 2
    cand_sq = (p_cand - y) ** 2
    for b in range(N_BOOT):
        sampled = rng.choice(unique_coins, size=len(unique_coins), replace=True)
        idx = np.concatenate([coin_groups[c] for c in sampled])
        bb = base_sq[idx].mean()
        cc = cand_sq[idx].mean()
        boot_rel[b] = (bb - cc) / bb if bb > 0 else np.nan
    boot_lo = float(np.nanpercentile(boot_rel, 2.5))
    boot_hi = float(np.nanpercentile(boot_rel, 97.5))
    # bootstrap two-sided p for improvement > 0
    boot_p = float(np.mean(boot_rel <= 0.0))

    # ---- Block-level Driscoll-Kraay HAC t on Brier diff ----
    bd = np.array([bb - bc for (_, bb, bc, _, _) in block_brier])
    dk_t = driscoll_kraay_t(bd)
    # two-sided normal p
    dk_p = float(2.0 * (1.0 - 0.5 * (1.0 + math.erf(abs(dk_t) / math.sqrt(2.0))))) if not math.isnan(dk_t) else float("nan")

    # ---- Holm over declared family (brier, logloss) ----
    pvals = [boot_p, dk_p if not math.isnan(dk_p) else 1.0]
    adj = holm_adjust([p if not math.isnan(p) else 1.0 for p in pvals])
    holm_brier = adj[0]
    holm_ll = adj[1]

    materiality_met = bool((rel_brier > MATERIALITY_FLOOR_REL) and (brier_cand < brier_base))
    significant = bool((holm_brier < 0.05) and (rel_brier > 0))

    if len(y) < 100 or brier_base <= 0:
        status = "INCONCLUSIVE"
        verdict = "INCONCLUSIVE"
    elif materiality_met and significant:
        status = "CONFIRMATORY_COMPLETE"
        verdict = "PROMOTED"
    else:
        status = "CONFIRMATORY_COMPLETE"
        verdict = "NOT_SUPPORTED"

    n_events = int(len(y))
    n_stress = int(y.sum())

    eval_json = {
        "experiment_id": EXPERIMENT_ID,
        "campaign": CAMPAIGN_ID,
        "session_id": SESSION_ID,
        "session_utc": SESSION_UTC,
        "phase": "HEAVY_STRESS_EVAL_AND_RECOMPUTE",
        "status": status,
        "holdout_opened": True,
        "n_events": n_events,
        "n_forecasts": n_events,
        "n_stress_events": n_stress,
        "event_rate": float(y.mean()),
        "n_coins": int(rec["coin"].nunique()),
        "n_test_blocks": len(block_brier),
        "metrics": {
            "baseline": {
                "brier": brier_base,
                "log_loss": ll_base,
                "ece": ece_base,
            },
            "candidate": {
                "brier": brier_cand,
                "log_loss": ll_cand,
                "ece": ece_cand,
            },
        },
        "relative_improvement": {
            "brier": rel_brier,
            "log_loss": rel_ll,
        },
        "block_results": [
            {"block": k, "brier_baseline": bb, "brier_candidate": bc,
             "logloss_baseline": lb, "logloss_candidate": lc}
            for (k, bb, bc, lb, lc) in block_brier
        ],
        "inference": {
            "cluster_bootstrap_by_coin": {
                "n_boot": N_BOOT,
                "rel_brier_ci95": [boot_lo, boot_hi],
                "p_improvement_gt_0": boot_p,
            },
            "driscoll_kraay_block": {"t": dk_t, "p_two_sided": dk_p, "lag": 2},
            "holm": {"p_brier": holm_brier, "p_logloss": holm_ll},
        },
        "materiality_floor_rel": MATERIALITY_FLOOR_REL,
        "materiality_met": materiality_met,
        "significant": significant,
        "verdict": verdict,
        "design": {
            "kind": "walk_forward_classification_stress_tail_exceedance",
            "target": "forward 24h realized variance > expanding train-only per-coin 0.95 quantile",
            "baseline": "RV-only HAR trailing log-RV lags",
            "candidate": "RV-only + funding_rate + |funding_rate| + premium + mark/EMA24 distance",
            "walk_forward": True,
            "initial_train_months": INITIAL_TRAIN_MONTHS,
            "block_months": BLOCK_MONTHS,
            "n_test_blocks": N_TEST_BLOCKS,
            "purge_embargo_h": PURGE_EMBARGO_H,
            "quantile_level": QUANTILE_LEVEL,
            "min_history": MIN_HISTORY,
            "inference": ["cluster-robust CR1 by coin", "Driscoll-Kraay HAC", "Holm"],
            "multiplicity_family": ["brier_relative_improvement", "logloss_relative_improvement"],
        },
        "universe_note": (
            "study universe = coins present in candles_1h AND funding AND open_interest "
            "(intersection); candles cover 342 coins but funding/OI cover ~198, so the "
            "funding-conditioned universe is the intersection"
        ),
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    out_json = SESSION_DIR / f"fclr_volstress01_eval_{SESSION_UTC}.json"
    out_json.write_text(json.dumps(eval_json, indent=2, default=str), encoding="utf-8")

    md = [
        "# FCLR-VOL-STRESS-01 Evaluation — Funding-Conditioned Volatility-STRESS Forecast",
        "",
        f"**Experiment ID:** {EXPERIMENT_ID}",
        f"**Campaign:** {CAMPAIGN_ID}",
        f"**Session:** {SESSION_ID}",
        f"**Status:** {status}  |  **Verdict:** {verdict}",
        "",
        "## Design (outcome-blind, frozen before outcomes)",
        "- Target: next-24h realized variance above an expanding, train-only per-coin 0.95 quantile (tail-exceedance classification).",
        "- Baseline: RV-only HAR trailing log-RV lags. Candidate: RV-only + funding + premium + mark/EMA24 distance.",
        f"- Walk-forward expanding train, {N_TEST_BLOCKS} x {BLOCK_MONTHS}-month test blocks, {PURGE_EMBARGO_H}h purge+embargo.",
        "- Inference: cluster bootstrap by coin, Driscoll-Kraay HAC (block level), Holm over {len(pvals)} metrics.",
        f"- Materiality floor (frozen): {MATERIALITY_FLOOR_REL*100:.0f}% relative Brier improvement.",
        "",
        "## Results",
        f"- Test forecasts: {n_events} (stress events: {n_stress}, rate {y.mean():.4f}); coins: {rec['coin'].nunique()}; blocks: {len(block_brier)}",
        f"- Brier: baseline={brier_base:.6f}, candidate={brier_cand:.6f} (relative improvement {rel_brier*100:.2f}%)",
        f"- Log-loss: baseline={ll_base:.6f}, candidate={ll_cand:.6f} (relative improvement {rel_ll*100:.2f}%)",
        f"- ECE: baseline={ece_base:.4f}, candidate={ece_cand:.4f}",
        f"- Cluster-bootstrap 95% CI on relative Brier: [{boot_lo*100:.2f}%, {boot_hi*100:.2f}%]; p(improvement>0)={boot_p:.4f}",
        f"- Driscoll-Kraay block t={dk_t:.3f}, p={dk_p:.4f}",
        f"- Holm-adjusted p: brier={holm_brier:.4f}, logloss={holm_ll:.4f}",
        f"- Materiality met: {materiality_met}; significant: {significant}",
        f"- **Verdict: {verdict}**",
        "",
        "## Conclusion",
        (f"The funding + price-dislocation feature set clears the frozen {MATERIALITY_FLOOR_REL*100:.0f}% "
         f"relative Brier floor with Holm-adjusted significance at broad scale (PROMOTED)."
         if verdict == "PROMOTED" else
         f"The funding + price-dislocation feature set does NOT clear the frozen "
         f"{MATERIALITY_FLOOR_REL*100:.0f}% relative Brier floor with Holm-adjusted significance "
         f"at broad scale; a valid negative result (NOT_SUPPORTED) closes the volatility-stress arm."),
        "",
        f"Generated: {eval_json['generated_utc']}",
    ]
    (SESSION_DIR / f"fclr_volstress01_eval_{SESSION_UTC}.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    return eval_json


if __name__ == "__main__":
    result = run()
    print(json.dumps({
        "status": result["status"],
        "verdict": result["verdict"],
        "n_events": result["n_events"],
        "n_stress_events": result["n_stress_events"],
        "n_coins": result["n_coins"],
        "brier_baseline": result["metrics"]["baseline"]["brier"],
        "brier_candidate": result["metrics"]["candidate"]["brier"],
        "rel_brier": result["relative_improvement"]["brier"],
        "materiality_met": result["materiality_met"],
        "significant": result["significant"],
    }, indent=2, default=str))