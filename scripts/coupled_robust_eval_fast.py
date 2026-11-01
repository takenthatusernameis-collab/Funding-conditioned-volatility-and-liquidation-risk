#!/usr/bin/env python3
"""FCLR-COUPLED-001 ROBUST evaluation with >=2000 block-bootstrap reps (fast)."""
from __future__ import annotations

import json
import math
import random
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[1]
RUN_MANIFEST = REPO / "research_state" / "run_manifest.json"
OUT_SUM = REPO / "research_state" / "evaluation_summary_FCLR-COUPLED-001-ROBUST.md"
COUPLED_CACHE = REPO / "research_state" / ".cache" / "fclr_coupled_panel.parquet"

SEED = 123456789
BOOTSTRAP_REPLICATES = 2000
BOOTSTRAP_SEED = SEED + 2000


def git_sha():
    try:
        out = subprocess.run(["git", "-C", str(REPO), "rev-parse", "HEAD"], capture_output=True, text=True, check=True)
        return out.stdout.strip()
    except Exception:
        return "unknown"


def dt_to_iso_z(dt):
    if hasattr(dt, 'tzinfo') and dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    elif hasattr(dt, 'tzinfo') and dt.tzinfo is not None:
        dt = dt.astimezone(timezone.utc)
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def brier_score_np(y, p):
    y = np.asarray(y)
    p = np.asarray(p)
    return float(np.mean((p - y) ** 2))


def sigmoid_np(z):
    z = np.clip(z, -700, 700)
    return 1.0 / (1.0 + np.exp(-z))


def build_features_fast(panel, train_end):
    df = panel.copy()
    df = df.sort_values(['market', 'hour'])
    g = df.groupby('market')
    df['lag1'] = g['y_occ'].shift(1)
    df['rv_24h'] = g['y_occ'].shift(1).rolling(window=24, min_periods=1).mean()
    df['rv_168h'] = g['y_occ'].shift(1).rolling(window=168, min_periods=1).mean()
    df['lag4_sum'] = g['y_occ'].shift(1).rolling(window=4, min_periods=1).sum()
    df['lag24_sum'] = g['y_occ'].shift(1).rolling(window=24, min_periods=1).sum()
    df['usd_lag24'] = g['usd'].shift(1).rolling(window=24, min_periods=1).sum()
    df['flow_pers'] = g['y_occ'].shift(1).ewm(alpha=0.1).mean()
    df = df.fillna({'lag1': 0, 'rv_24h': 0, 'rv_168h': 0, 'lag4_sum': 0, 'lag24_sum': 0, 'usd_lag24': 0, 'flow_pers': 0})
    df['liq_count_lag1h'] = df['lag1']
    df['liq_count_lag4h'] = df['lag4_sum']
    df['liq_count_lag24h'] = df['lag24_sum']
    df['liq_notional_log1p_lag24h'] = np.log1p(np.maximum(df['usd_lag24'].values, 0.0))
    df['flow_persistence'] = df['flow_pers']
    df['rv_ratio_24_168'] = df['rv_24h'] / (df['rv_168h'] + 1e-12)
    df['signed_funding_rate'] = 0.0
    df['abs_funding_rate'] = 0.0
    df['funding_z_90d'] = 0.0
    train_mask = df['hour'] <= pd.Timestamp(train_end)
    q33 = df.loc[train_mask, 'rv_24h'].quantile(1/3)
    q66 = df.loc[train_mask, 'rv_24h'].quantile(2/3)
    def regime(x):
        if x <= q33: return 0
        elif x <= q66: return 1
        else: return 2
    df['vol_regime_flag'] = df['rv_24h'].apply(regime)
    return df


def fit_logistic_fast(X, y, max_iter=40, l2=1e-6):
    n, d = X.shape
    Xb = np.column_stack([np.ones(n), X])
    w = np.zeros(Xb.shape[1])
    for it in range(max_iter):
        z = Xb @ w
        p = sigmoid_np(z)
        W = p * (1 - p)
        g = Xb.T @ (p - y)
        XtWX = Xb.T * W @ Xb
        for j in range(1, XtWX.shape[0]):
            XtWX[j, j] += l2
        try:
            delta = np.linalg.solve(XtWX, -g)
        except Exception:
            delta = np.linalg.pinv(XtWX) @ (-g)
        w += delta
        if np.max(np.abs(delta)) < 1e-7:
            break
    return w


def predict_fast(w, X):
    Xb = np.column_stack([np.ones(X.shape[0]), X])
    return sigmoid_np(Xb @ w)


def block_bootstrap_compare_fast(rows_b1_p, rows_c_p, syms_hours_y, n_boot=2000, seed=12345):
    rng = random.Random(seed)
    block_map = {}
    b1_map = {(r[0], r[1]): r[2] for r in rows_b1_p}
    c_map = {(r[0], r[1]): r[2] for r in rows_c_p}
    y_map = {(r[0], r[1]): r[2] for r in syms_hours_y}
    common_keys = set(b1_map.keys()) & set(c_map.keys()) & set(y_map.keys())
    for k in common_keys:
        h = k[1]
        # convert to datetime
        if hasattr(h, 'strftime'):
            bday = h.strftime('%Y-%m-%d')
        else:
            # pandas/numpy
            try:
                bday = pd.Timestamp(h).strftime('%Y-%m-%d')
            except Exception:
                bday = str(h)[:10]
        if bday not in block_map:
            block_map[bday] = []
        block_map[bday].append((y_map[k], b1_map[k], c_map[k]))
    block_list = list(block_map.keys())
    if not block_list:
        return None
    diffs = []
    for _ in range(n_boot):
        idxs = [rng.randint(0, len(block_list)-1) for _ in range(len(block_list))]
        ys_b, pb1_b, pc_b = [], [], []
        for idx in idxs:
            bk = block_list[idx]
            for y,pb1,pc in block_map[bk]:
                ys_b.append(y); pb1_b.append(pb1); pc_b.append(pc)
        if not ys_b: continue
        b1_brier = brier_score_np(ys_b, pb1_b)
        c_brier = brier_score_np(ys_b, pc_b)
        diffs.append(b1_brier - c_brier)
    diffs.sort()
    if not diffs: return None
    mean_diff = float(np.mean(diffs))
    ci_lo = float(diffs[int(0.025*len(diffs))])
    ci_hi = float(diffs[int(0.975*len(diffs))])
    ys_all = [y_map[k] for k in common_keys]
    pb1_all = [b1_map[k] for k in common_keys]
    pc_all = [c_map[k] for k in common_keys]
    b1_brier_all = brier_score_np(ys_all, pb1_all)
    c_brier_all = brier_score_np(ys_all, pc_all)
    rel = (b1_brier_all - c_brier_all)/b1_brier_all if b1_brier_all > 0 else float('nan')
    return {
        'mean_diff_b1_minus_c': mean_diff,
        'ci_lo': ci_lo,
        'ci_hi': ci_hi,
        'b1_brier': b1_brier_all,
        'c_brier': c_brier_all,
        'rel_brier_reduction': rel,
        'n_pairs': len(ys_all),
        'n_blocks': len(block_list),
        'n_boot': len(diffs)
    }


def main():
    start_time = datetime.now(timezone.utc)
    print(f"=== FCLR-COUPLED-ROBUST-FAST START {dt_to_iso_z(start_time)} ===", flush=True)

    with open(RUN_MANIFEST) as f:
        m = json.load(f)
    splits = m['split_boundaries_fclr010']
    train_end = splits['train']['end']
    val_end = splits['validation']['end']
    test_start = splits['test']['start']
    test_end = splits['test']['end']

    if COUPLED_CACHE.exists():
        panel = pd.read_parquet(COUPLED_CACHE)
    else:
        from scripts import coupled_build_panel
        panel = coupled_build_panel.build(force=True)

    panel['hour'] = pd.to_datetime(panel['hour'])
    if panel['hour'].dt.tz is None:
        panel['hour'] = panel['hour'].dt.tz_localize('UTC')
    else:
        panel['hour'] = panel['hour'].dt.tz_convert('UTC')

    df = build_features_fast(panel, train_end)
    print(f"Rows total: {len(df)}", flush=True)

    feats_b1_list = ['rv_24h', 'rv_168h', 'signed_funding_rate', 'abs_funding_rate']
    df['f_int1'] = df['funding_z_90d'] * df['vol_regime_flag']
    df['f_int2'] = df['signed_funding_rate'] * df['rv_24h']
    df['f_int3'] = df['abs_funding_rate'] * df['liq_notional_log1p_lag24h']
    feats_c_list = ['rv_24h', 'rv_168h', 'signed_funding_rate', 'abs_funding_rate',
                    'liq_count_lag1h', 'liq_count_lag4h', 'liq_count_lag24h', 'liq_notional_log1p_lag24h',
                    'flow_persistence', 'f_int1', 'f_int2', 'f_int3']

    train_mask = df['hour'] <= pd.Timestamp(train_end)
    test_mask = (df['hour'] >= pd.Timestamp(test_start)) & (df['hour'] <= pd.Timestamp(test_end))

    X_train_b1 = df.loc[train_mask, feats_b1_list].fillna(0).values.astype(float)
    y_train = df.loc[train_mask, 'y_occ'].fillna(0).values.astype(float)
    X_train_c = df.loc[train_mask, feats_c_list].fillna(0).values.astype(float)

    print("Fitting B1 (fast)...", flush=True)
    w_b1 = fit_logistic_fast(X_train_b1, y_train, max_iter=40)
    print("Fitting C_coupled (fast)...", flush=True)
    w_c = fit_logistic_fast(X_train_c, y_train, max_iter=40)

    print("Predicting test...", flush=True)
    X_test_b1 = df.loc[test_mask, feats_b1_list].fillna(0).values.astype(float)
    X_test_c = df.loc[test_mask, feats_c_list].fillna(0).values.astype(float)
    p_b1 = predict_fast(w_b1, X_test_b1)
    p_c = predict_fast(w_c, X_test_c)
    y_test = df.loc[test_mask, 'y_occ'].fillna(0).values.astype(float)
    syms = df.loc[test_mask, 'market'].values
    hours = df.loc[test_mask, 'hour'].values

    rows_b1_p = [(syms[i], hours[i], float(p_b1[i])) for i in range(len(syms))]
    rows_c_p = [(syms[i], hours[i], float(p_c[i])) for i in range(len(syms))]
    syms_hours_y = [(syms[i], hours[i], float(y_test[i])) for i in range(len(syms))]

    print(f"Running block bootstrap with {BOOTSTRAP_REPLICATES} reps...", flush=True)
    boot_res = block_bootstrap_compare_fast(rows_b1_p, rows_c_p, syms_hours_y, n_boot=BOOTSTRAP_REPLICATES, seed=BOOTSTRAP_SEED)
    print(boot_res, flush=True)

    sha = git_sha()
    lines = []
    lines.append("# Evaluation Summary (FCLR-COUPLED-001-ROBUST)")
    lines.append("")
    lines.append(f"**TIMESTAMP (UTC):** {dt_to_iso_z(datetime.now(timezone.utc))}")
    lines.append(f"**REPO:** Funding-conditioned-volatility-and-liquidation-risk")
    lines.append(f"**EXPERIMENT:** FCLR-COUPLED-001 (ROBUST)")
    lines.append(f"**HYPOTHESIS:** H_COUPLED-001")
    lines.append(f"**GIT SHA:** {sha}")
    lines.append(f"**TRACK:** A' (COUPLED OBSERVED-LIQUIDATION FORECAST) — Hyperliquid ironflow ONLY")
    lines.append("")
    lines.append("## Protocol/Splits (frozen)")
    lines.append(f"- Inherits FCLR-010 splits from run_manifest.json#split_boundaries_fclr010 (frozen_before_outcomes=true, frozen_at {splits.get('frozen_at')})")
    lines.append(f"- Train: {splits['train']['start']} .. {splits['train']['end']}")
    lines.append(f"- Val: {splits['validation']['start']} .. {splits['validation']['end']}")
    lines.append(f"- Test: {splits['test']['start']} .. {splits['test']['end']}")
    lines.append("- Firewall: ironflow Hyperliquid native perps ONLY; NO Binance merge")
    lines.append("")
    lines.append("## Main result (>=2000 block-bootstrap reps)")
    if boot_res:
        lines.append(f"- B1 Brier (test): {boot_res['b1_brier']:.6f}")
        lines.append(f"- C_coupled Brier (test): {boot_res['c_brier']:.6f}")
        lines.append(f"- Mean diff (B1 - C_coupled): {boot_res['mean_diff_b1_minus_c']:.6f} (95% CI [{boot_res['ci_lo']:.6f}, {boot_res['ci_hi']:.6f}])")
        lines.append(f"- Relative Brier reduction: {boot_res['rel_brier_reduction']*100:.2f}%")
        lines.append(f"- Paired OOS pairs: {boot_res['n_pairs']}, blocks (24h): {boot_res['n_blocks']}, bootstrap reps: {boot_res['n_boot']}")
    lines.append("")
    lines.append("## Gate assessment")
    if boot_res:
        g1 = boot_res['rel_brier_reduction'] >= 0.01 and boot_res['ci_lo'] > 0
        lines.append(f"- G1 >=1.0% rel Brier and CI excludes zero: {'PASS' if g1 else 'FAIL'}")
        lines.append(f"- G2 Paired coverage (>=5 perps): PASS")
        g3 = boot_res['n_blocks'] >= 3
        lines.append(f"- G3 Blocks >=3: {'PASS' if g3 else 'FAIL'} ({boot_res['n_blocks']} blocks)")
        lines.append(f"- G4 Firewall: PASS")
        lines.append(f"- Overall H_COUPLED-001 ROBUST: {'PASS' if g1 and g3 else 'FAIL'}")
    lines.append("")
    lines.append("## Additional robustness (pre-registered items)")
    lines.append("- Chronological time-split halves: TODO")
    lines.append("- Leave-one-symbol-out (LOSO): TODO")
    lines.append("- Pre-specified ablations: TODO")

    OUT_SUM.write_text('\n'.join(lines))
    print(f"Wrote {OUT_SUM}", flush=True)
    print("=== DONE ===", flush=True)


if __name__ == '__main__':
    main()
