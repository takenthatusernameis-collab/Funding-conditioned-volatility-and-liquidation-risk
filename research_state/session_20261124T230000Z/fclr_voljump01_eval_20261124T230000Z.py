#!/usr/bin/env python3
"""
FCLR-VOL-JUMP-01 heavy broad-panel jump-forecast evaluation.
Executable research artifact: outcome-bound walk-forward classification of the
next-24h signed-jump / semivariance-asymmetry tail event beyond an RV-only
baseline on the frozen ironflow_bulk panel (2025-05..2026-10).
Stdlib + numpy + pandas + pyarrow only; no network; read-only cache.
"""
from __future__ import annotations

import hashlib
import json
import math
import time
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

REPO = Path(__file__).resolve().parents[2]
CACHE = REPO / "research_state" / "data_cache" / "ironflow_bulk"
SESSION = REPO / "research_state" / "session_20261124T230000Z"
UTC = "20261124T230000Z"
UTC_ISO = "2026-11-24T23:00:00Z"

MONTHS = [
    "2025-05", "2025-06", "2025-07", "2025-08", "2025-09", "2025-10",
    "2025-11", "2025-12", "2026-01", "2026-02", "2026-03", "2026-04",
    "2026-05", "2026-06", "2026-07", "2026-08", "2026-09", "2026-10",
]
HORIZON_H = 24
PURGE_EMBARGO_H = 48
QUANTILE_LEVEL = 0.95
MATERIALITY_FLOOR_REL = 0.02
TRAIN_FRAC = 0.6
N_TEST_BLOCKS = 6
BLOCK_MONTHS = 2
EPS = 1e-12


def load_dataset(name: str, cols: list[str]) -> pd.DataFrame:
    frames = []
    for month in MONTHS:
        t = pq.read_table(CACHE / name / f"{month}.parquet", columns=cols)
        frames.append(t.to_pandas())
    df = pd.concat(frames, ignore_index=True)
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    return df


def rolling_bipower(r: np.ndarray) -> np.ndarray:
    # bipower variation = (pi/2) * sum |r_j| * |r_{j+1}| over pairs in the window
    n = len(r)
    out = np.full(n, np.nan)
    if n < 2:
        return out
    abs_prod = np.abs(r[:-1]) * np.abs(r[1:])  # pair (j, j+1) at index j
    csum = np.concatenate([[0.0], np.nancumsum(abs_prod)])  # length n
    # window ending at index i uses pairs (i-H+1 .. i-1) -> abs_prod[i-H+1 .. i-1]
    # sum abs_prod[a..b] = csum[b+1] - csum[a], a=i-H+1, b=i-1 => csum[i] - csum[i-H+1]
    H = HORIZON_H
    out[H - 1:] = (math.pi / 2.0) * (csum[H - 1:] - csum[: n - H + 1])
    return out


def compute_coin_features(df_coin: pd.DataFrame) -> pd.DataFrame:
    """df_coin indexed by timestamp, sorted. Returns feature+label frame."""
    d = df_coin.sort_index().copy()
    close = d["close"].astype(float).to_numpy()
    n = len(d)
    ret = np.full(n, np.nan)
    ret[1:] = np.log(close[1:] / close[:-1])
    d["ret"] = ret

    H = HORIZON_H
    r2 = ret * ret
    csum_r2 = np.concatenate([[0.0], np.nancumsum(r2)])
    # rv[i] = sum r2 over [i-H+1, i] = csum_r2[i+1] - csum_r2[i-H+1], valid i >= H-1
    rv = np.full(n, np.nan)
    rv[H - 1:] = csum_r2[H:] - csum_r2[: n - H + 1]

    rpos = np.where(ret > 0, r2, 0.0)
    rneg = np.where(ret < 0, r2, 0.0)
    csum_rpos = np.concatenate([[0.0], np.nancumsum(rpos)])
    csum_rneg = np.concatenate([[0.0], np.nancumsum(rneg)])
    rs_plus = np.full(n, np.nan)
    rs_minus = np.full(n, np.nan)
    rs_plus[H - 1:] = csum_rpos[H:] - csum_rpos[: n - H + 1]
    rs_minus[H - 1:] = csum_rneg[H:] - csum_rneg[: n - H + 1]

    bv = rolling_bipower(ret)

    # signed jump over window ending at i: J = sign(RS+ - RS-) * (RV - BV)
    jump = np.full(n, np.nan)
    valid = ~(np.isnan(rv) | np.isnan(bv) | np.isnan(rs_plus) | np.isnan(rs_minus))
    rv_v = rv[valid]
    bv_v = bv[valid]
    sp_v = rs_plus[valid]
    sm_v = rs_minus[valid]
    sign = np.where(sp_v >= sm_v, 1.0, -1.0)
    jump[valid] = sign * (rv_v - bv_v)
    # forward 24h jump at forecast origin t = jump over t+1..t+24 = jump value
    # whose window ends at t+24 -> shift backward by HORIZON_H
    jump_fwd = np.full(n, np.nan)
    jump_fwd[: n - H] = jump[H:]
    d["jump_fwd"] = jump_fwd
    d["rv_fwd"] = jump_fwd  # placeholder column kept for schema compatibility
    d["bv_fwd"] = bv

    # trailing RV24h at t (features use only data <= t): rv at index t
    d["rv_trail"] = rv

    return d


def irls_logistic(X: np.ndarray, y: np.ndarray, max_iter: int = 100, tol: float = 1e-8):
    """Simple IRLS logistic regression with intercept. Returns beta, converged."""
    n, k = X.shape
    X_int = np.column_stack([np.ones(n), X])
    beta = np.zeros(k + 1)
    for _ in range(max_iter):
        eta = X_int @ beta
        eta = np.clip(eta, -60, 60)
        p = 1.0 / (1.0 + np.exp(-eta))
        w = p * (1.0 - p)
        z = eta + (y - p) / np.maximum(w, 1e-12)
        # XtWX = X_int.T @ diag(w) @ X_int  (avoid forming the n×n diag matrix)
        XtWX = X_int.T @ (w[:, None] * X_int)
        XtWz = X_int.T @ (w * z)
        try:
            beta_new = np.linalg.solve(XtWX + 1e-9 * np.eye(k + 1), XtWz)
        except np.linalg.LinAlgError:
            beta_new = beta
        if np.max(np.abs(beta_new - beta)) < tol:
            beta = beta_new
            break
        beta = beta_new
    return beta


def predict_logistic(X: np.ndarray, beta: np.ndarray) -> np.ndarray:
    X_int = np.column_stack([np.ones(X.shape[0]), X])
    eta = np.clip(X_int @ beta, -60, 60)
    return 1.0 / (1.0 + np.exp(-eta))


def brier_score(y: np.ndarray, p: np.ndarray) -> float:
    mask = ~(np.isnan(y) | np.isnan(p))
    if mask.sum() == 0:
        return float("nan")
    return float(np.mean((y[mask] - p[mask]) ** 2))


def log_loss(y: np.ndarray, p: np.ndarray) -> float:
    mask = ~(np.isnan(y) | np.isnan(p))
    if mask.sum() == 0:
        return float("nan")
    p = np.clip(p[mask], EPS, 1 - EPS)
    y = y[mask]
    return float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))


def ece(y: np.ndarray, p: np.ndarray, n_bins: int = 10) -> float:
    mask = ~(np.isnan(y) | np.isnan(p))
    if mask.sum() == 0:
        return float("nan")
    y = y[mask]
    p = p[mask]
    bins = np.linspace(0, 1, n_bins + 1)
    ece_val = 0.0
    for b in range(n_bins):
        m = (p >= bins[b]) & (p < bins[b + 1]) if b < n_bins - 1 else (p >= bins[b]) & (p <= bins[b + 1])
        if m.sum() == 0:
            continue
        ece_val += (m.sum() / len(y)) * abs(np.mean(y[m]) - np.mean(p[m]))
    return float(ece_val)


def cluster_bootstrap_ci(y: np.ndarray, p_base: np.ndarray, p_cand: np.ndarray,
                         groups: np.ndarray, n_boot: int = 2000, seed: int = 0):
    """Cluster bootstrap by coin for relative Brier improvement CI."""
    rng = np.random.default_rng(seed)
    mask = ~(np.isnan(y) | np.isnan(p_base) | np.isnan(p_cand))
    y = y[mask]; p_base = p_base[mask]; p_cand = p_cand[mask]; groups = groups[mask]
    uniq = np.unique(groups)
    n = len(y)
    obs_diff = brier_score(y, p_base) - brier_score(y, p_cand)
    boots = []
    for _ in range(n_boot):
        draw = rng.choice(uniq, size=len(uniq), replace=True)
        sel = np.isin(groups, draw)
        if sel.sum() < 10:
            continue
        boots.append(brier_score(y[sel], p_base[sel]) - brier_score(y[sel], p_cand[sel]))
    boots = np.array(boots)
    if len(boots) < 10:
        return [float("nan"), float("nan")], float("nan")
    lo = float(np.percentile(boots, 2.5)); hi = float(np.percentile(boots, 97.5))
    p_gt0 = float(np.mean(boots > 0))
    return [lo, hi], p_gt0


def driscoll_kraay(block_diffs: np.ndarray, lag: int = 2):
    """Driscoll-Kraay HAC t-stat for mean block difference."""
    x = block_diffs[~np.isnan(block_diffs)]
    if len(x) < 3:
        return float("nan"), float("nan"), lag
    mean = float(np.mean(x))
    n = len(x)
    # Newey-West style HAC variance over blocks
    ac0 = float(np.mean((x - mean) ** 2))
    var = ac0
    for l in range(1, min(lag, n - 1) + 1):
        gamma = float(np.mean((x[l:] - mean) * (x[:n - l] - mean)))
        var += 2 * (1 - l / (lag + 1)) * gamma
    var = max(var / n, 1e-18)
    se = math.sqrt(var)
    t = mean / se if se > 0 else float("nan")
    # two-sided p via normal approx: p = 1 - erf(|t|/sqrt(2))
    p = 1.0 - math.erf(abs(t) / math.sqrt(2.0)) if t == t else float("nan")
    return t, p, lag


def holm(pvals: list[float], alpha: float = 0.05):
    pvals = np.array(pvals, dtype=float)
    order = np.argsort(pvals)
    m = len(pvals)
    adjusted = np.full(m, np.nan)
    for rank, idx in enumerate(order):
        adjusted[idx] = pvals[idx] * (m - rank)
    adjusted = np.minimum(adjusted, 1.0)
    # enforce monotonicity
    sorted_idx = np.argsort(pvals)
    adj_sorted = np.maximum.accumulate(pvals[sorted_idx] * (m - np.arange(m)))
    adj_sorted = np.minimum(adj_sorted, 1.0)
    adjusted = np.empty(m)
    adjusted[sorted_idx] = adj_sorted
    rejected = adjusted <= alpha
    return adjusted.tolist(), bool(np.any(rejected))


def main() -> None:
    t0 = time.time()
    SESSION.mkdir(parents=True, exist_ok=True)

    print("Loading candles...", flush=True)
    candles = load_dataset("candles_1h", ["timestamp", "coin", "close"])
    print("Loading funding...", flush=True)
    funding = load_dataset("funding", ["timestamp", "coin", "funding_rate", "premium"])
    print("Loading open_interest...", flush=True)
    oi = load_dataset("open_interest", ["timestamp", "coin", "mark_price", "oracle_price"])

    # Universe: intersection of coins
    coins = sorted(set(candles["coin"]) & set(funding["coin"]) & set(oi["coin"]))
    print(f"Universe intersection coins: {len(coins)}", flush=True)

    # Align funding to candle hour: latest funding obs at or before each hour
    funding_h = funding.copy()
    funding_h["hour"] = funding_h["timestamp"].dt.floor("h")
    funding_h = funding_h.sort_values("hour")
    funding_last = funding_h.groupby(["coin", "hour"], as_index=False).tail(1)[
        ["coin", "hour", "funding_rate", "premium"]
    ].rename(columns={"hour": "timestamp"})

    oi_h = oi.copy()
    oi_h["timestamp"] = oi_h["timestamp"].dt.floor("h")
    oi_h = oi_h.groupby(["coin", "timestamp"], as_index=False).tail(1)[
        ["timestamp", "coin", "mark_price", "oracle_price"]
    ]
    # forward-fill prices within coin so merge_asof backward finds last valid quote
    oi_h = oi_h.sort_values(["coin", "timestamp"])
    oi_h["mark_price"] = oi_h.groupby("coin")["mark_price"].ffill()
    oi_h["oracle_price"] = oi_h.groupby("coin")["oracle_price"].ffill()

    candles = candles.sort_values(["coin", "timestamp"])
    frames = []
    for coin in coins:
        cc = candles[candles["coin"] == coin].set_index("timestamp").sort_index()
        if len(cc) < HORIZON_H + 200:
            continue
        cc = compute_coin_features(cc)
        ff = funding_last[funding_last["coin"] == coin].set_index("timestamp").sort_index()
        oo = oi_h[oi_h["coin"] == coin].set_index("timestamp").sort_index()
        # merge asof: latest funding/OI at or before candle hour
        m = pd.merge_asof(cc.reset_index(), ff.reset_index(), on="timestamp", direction="backward")
        m = pd.merge_asof(m, oo.reset_index(), on="timestamp", direction="backward")
        m = m.set_index("timestamp")
        m["coin"] = coin
        frames.append(m[["coin", "close", "ret", "rv_trail", "rv_fwd", "bv_fwd",
                         "jump_fwd", "funding_rate", "premium", "mark_price", "oracle_price"]])
    print(f"Coins with features: {len(frames)}", flush=True)
    panel = pd.concat(frames, ignore_index=False)
    panel = panel.sort_index()

    # Forward realized variance for reference and drop rows without forward jump
    panel["rv_fwd"] = panel["rv_fwd"].astype(float)
    panel["jump_fwd"] = panel["jump_fwd"].astype(float)
    has_jump = panel["jump_fwd"].notna()
    panel = panel[has_jump].copy()
    print(f"Panel rows with forward jump: {len(panel)}", flush=True)

    # Train period boundary (60% of unique timestamps, chronological)
    all_ts = sorted(panel.index.unique())
    n_ts = len(all_ts)
    cut_idx = int(TRAIN_FRAC * n_ts)
    train_cut = all_ts[cut_idx]
    train_mask = panel.index <= train_cut
    print(f"Train cut: {train_cut} (train rows {int(train_mask.sum())} / {len(panel)})", flush=True)

    # Expanding train-only quantile q_t per coin: 0.95 quantile of trailing jump over train period
    train_panel = panel[train_mask]
    q_series = train_panel.groupby("coin")["jump_fwd"].quantile(QUANTILE_LEVEL)
    q_map = q_series.to_dict()
    panel["q_t"] = panel["coin"].map(q_map)
    panel["y"] = (panel["jump_fwd"] > panel["q_t"]).astype(int)
    print(f"Event rate overall: {panel['y'].mean():.6f}", flush=True)

    # Features
    panel["abs_funding"] = panel["funding_rate"].abs()
    panel["premium"] = panel["premium"].astype(float)
    # mark/EMA24 distance per coin
    panel["ema24"] = panel.groupby("coin")["mark_price"].transform(
        lambda s: s.ewm(span=24, adjust=False).mean())
    panel["ema_dist"] = panel["mark_price"] / panel["ema24"] - 1.0

    base_feats = ["rv_trail"]
    cand_feats = ["rv_trail", "funding_rate", "abs_funding", "premium", "ema_dist"]

    # Walk-forward test blocks: chronological blocks after train, each BLOCK_MONTHS, purge 48h
    test_ts = [t for t in all_ts if t > train_cut]
    # split test_ts into contiguous monthly-ish blocks
    blocks = []
    cur = test_ts[0]
    for i in range(N_TEST_BLOCKS):
        block_start = cur
        block_end = block_start + pd.DateOffset(months=BLOCK_MONTHS) - pd.Timedelta(hours=1)
        blocks.append((block_start, block_end))
        cur = block_end + pd.Timedelta(hours=PURGE_EMBARGO_H)

    results = {
        "experiment_id": "FCLR-VOL-JUMP-01",
        "campaign": "FCLR-VOL-JUMP-01-20261124T223000Z",
        "session_id": f"session_{UTC}",
        "session_utc": UTC,
        "generated_utc": UTC_ISO,
        "phase": "HEAVY_JUMP_EVAL_AND_RECOMPUTE",
        "design": {
            "kind": "walk_forward_classification_signed_jump_semivariance_asymmetry",
            "target": "next-24h signed-jump / semivariance-asymmetry tail exceedance (train-only high quantile)",
            "baseline": "RV-only (trailing RV24h) logistic",
            "candidate": "RV + signed funding_rate + abs(funding_rate) + premium + mark/EMA24 distance",
            "horizon_h": HORIZON_H,
            "purge_embargo_h": PURGE_EMBARGO_H,
            "quantile_level": QUANTILE_LEVEL,
            "train_frac": TRAIN_FRAC,
            "n_test_blocks": N_TEST_BLOCKS,
            "materiality_floor_rel": MATERIALITY_FLOOR_REL,
        },
        "universe": {"n_coins": len(coins), "n_panel_rows": int(len(panel))},
    }

    block_results = []
    all_y, all_p_base, all_p_cand, all_groups = [], [], [], []
    for bi, (bs, be) in enumerate(blocks):
        # train = expanding, all data up to purge-gap before block_start (train-only)
        tr = panel[panel.index <= (bs - pd.Timedelta(hours=PURGE_EMBARGO_H))]
        te = panel[(panel.index >= bs) & (panel.index <= be)].copy()
        if len(tr) < 1000 or len(te) < 10:
            print(f"Block {bi}: skip (train {len(tr)}, test {len(te)})", flush=True)
            continue
        # feature matrices, train-only standardization
        def prep(d):
            Xb = d[base_feats].to_numpy(dtype=float)
            Xc = d[cand_feats].to_numpy(dtype=float)
            y = d["y"].to_numpy(dtype=float)
            return Xb, Xc, y
        Xb_tr, Xc_tr, y_tr = prep(tr)
        Xb_te, Xc_te, y_te = prep(te)
        valid_tr = ~(np.isnan(Xb_tr).any(axis=1) | np.isnan(Xc_tr).any(axis=1) | np.isnan(y_tr))
        valid_te = ~(np.isnan(Xb_te).any(axis=1) | np.isnan(Xc_te).any(axis=1) | np.isnan(y_te))
        # standardize features train-only
        means = Xb_tr[valid_tr].mean(axis=0)
        stds = Xb_tr[valid_tr].std(axis=0); stds[stds == 0] = 1.0
        Xb_tr_s = (Xb_tr - means) / stds
        Xb_te_s = (Xb_te - means) / stds
        means_c = Xc_tr[valid_tr].mean(axis=0)
        stds_c = Xc_tr[valid_tr].std(axis=0); stds_c[stds_c == 0] = 1.0
        Xc_tr_s = (Xc_tr - means_c) / stds_c
        Xc_te_s = (Xc_te - means_c) / stds_c

        beta_b = irls_logistic(Xb_tr_s[valid_tr], y_tr[valid_tr])
        beta_c = irls_logistic(Xc_tr_s[valid_tr], y_tr[valid_tr])
        p_b = predict_logistic(Xb_te_s[valid_te], beta_b)
        p_c = predict_logistic(Xc_te_s[valid_te], beta_c)
        y_v = y_te[valid_te]
        groups_v = te["coin"].to_numpy()[valid_te]

        brier_b = brier_score(y_v, p_b)
        brier_c = brier_score(y_v, p_c)
        ll_b = log_loss(y_v, p_b)
        ll_c = log_loss(y_v, p_c)
        rel_b = (brier_b - brier_c) / brier_b if brier_b > 0 else float("nan")
        rel_ll = (ll_b - ll_c) / ll_b if ll_b > 0 else float("nan")

        block_results.append({
            "block": bi,
            "block_start": str(bs), "block_end": str(be),
            "n_test": int(valid_te.sum()),
            "n_events": int(y_v.sum()),
            "brier_baseline": brier_b, "brier_candidate": brier_c,
            "logloss_baseline": ll_b, "logloss_candidate": ll_c,
            "rel_brier_improvement": rel_b, "rel_logloss_improvement": rel_ll,
            "ece_baseline": ece(y_v, p_b), "ece_candidate": ece(y_v, p_c),
        })
        all_y.append(y_v); all_p_base.append(p_b); all_p_cand.append(p_c); all_groups.append(groups_v)
        print(f"Block {bi}: n={int(valid_te.sum())} events={int(y_v.sum())} "
              f"Brier B={brier_b:.6f} C={brier_c:.6f} rel={rel_b:.6f}", flush=True)

    y_all = np.concatenate(all_y)
    p_base_all = np.concatenate(all_p_base)
    p_cand_all = np.concatenate(all_p_cand)
    groups_all = np.concatenate([np.asarray(g) for g in all_groups])

    brier_b = brier_score(y_all, p_base_all)
    brier_c = brier_score(y_all, p_cand_all)
    ll_b = log_loss(y_all, p_base_all)
    ll_c = log_loss(y_all, p_cand_all)
    rel_b = (brier_b - brier_c) / brier_b if brier_b > 0 else float("nan")
    rel_ll = (ll_b - ll_c) / ll_b if ll_b > 0 else float("nan")

    ci, p_gt0 = cluster_bootstrap_ci(y_all, p_base_all, p_cand_all, groups_all, n_boot=2000)

    # per-block differences for Driscoll-Kraay
    block_diffs = np.array([br["rel_brier_improvement"] for br in block_results])
    t_dk, p_dk, lag_dk = driscoll_kraay(block_diffs, lag=2)

    holm_adj, holm_rej = holm([p_gt0, p_dk])

    materiality_met = bool(rel_b > MATERIALITY_FLOOR_REL)
    significant = bool(holm_rej)
    verdict = "NOT_SUPPORTED"
    if materiality_met and significant:
        verdict = "PROMOTED"
    elif not materiality_met and not significant:
        verdict = "NOT_SUPPORTED"
    else:
        verdict = "INCONCLUSIVE"

    results.update({
        "status": "CONFIRMATORY_COMPLETE",
        "holdout_opened": True,
        "n_events": int(y_all.sum()),
        "n_forecasts": int(len(y_all)),
        "n_coins": int(panel["coin"].nunique()),
        "n_test_blocks": len(block_results),
        "event_rate": float(y_all.mean()),
        "metrics": {
            "baseline": {"brier": brier_b, "log_loss": ll_b, "ece": ece(y_all, p_base_all)},
            "candidate": {"brier": brier_c, "log_loss": ll_c, "ece": ece(y_all, p_cand_all)},
        },
        "relative_improvement": {"brier": rel_b, "log_loss": rel_ll},
        "block_results": block_results,
        "inference": {
            "cluster_bootstrap_by_coin": {
                "n_boot": 2000,
                "rel_brier_ci95": ci,
                "p_improvement_gt_0": p_gt0,
            },
            "driscoll_kraay_block": {"t": t_dk, "p_two_sided": p_dk, "lag": lag_dk},
            "holm": {"p_brier": p_gt0, "p_logloss": p_dk, "adjusted": holm_adj, "rejected": holm_rej},
        },
        "materiality_floor_rel": MATERIALITY_FLOOR_REL,
        "materiality_met": materiality_met,
        "significant": significant,
        "verdict": verdict,
        "generated_utc": UTC_ISO,
        "elapsed_seconds": round(time.time() - t0, 2),
    })

    out_json = SESSION / f"fclr_voljump01_eval_{UTC}.json"
    out_json.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(f"\n=== RESULT ===", flush=True)
    print(f"status={results['status']} verdict={verdict} materiality_met={materiality_met}", flush=True)
    print(f"Brier baseline={brier_b:.6f} candidate={brier_c:.6f} rel_improvement={rel_b:.6f}", flush=True)
    print(f"n_events={int(y_all.sum())} n_forecasts={int(len(y_all))} n_coins={int(panel['coin'].nunique())}", flush=True)
    print(f"Wrote {out_json}", flush=True)
    return results


if __name__ == "__main__":
    main()
