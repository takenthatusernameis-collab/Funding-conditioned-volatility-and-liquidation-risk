import json, sys, time
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm

# --- config from FCLR-011 recompute ---
IN_PANEL = Path("research_state/session_20261116T0040Z/fclr011_recompute_panel_20261116T004150Z.parquet")
OUT_DIR = Path("research_state/session_20261116T035833Z")
UTC = "20261116T035833Z"
N_BOOT = 2000
RNG_SEED = 42
PURGE_DAYS = 7
EMBARGO_DAYS = 7
# recompute window from prior artifacts
TRAIN_START = "2026-03-09"
TRAIN_END = "2026-05-07"
TEST_START = "2026-05-08"
TEST_END = "2026-08-06"

BASE_COLS = ["logret_24h_lag1", "rv_24h_lag1", "funding_abs_lag1", "funding_z_lag1"]
FUND_COLS = ["funding_ema24_lag1"]
EMA_COLS = ["ema24_change_lag1"]
TARGET = "log_rv_forward_24h"
Y_COL = "rv_forward_24h"

MODELS = {
    "B1": BASE_COLS,
    "B1_plus_funding": BASE_COLS + FUND_COLS,
    "B1_plus_ema24": BASE_COLS + EMA_COLS,
    "B1_plus_funding_plus_ema24": BASE_COLS + FUND_COLS + EMA_COLS,
}

def qlike(y, yhat):
    y = np.asarray(y, dtype=float)
    yhat = np.asarray(yhat, dtype=float)
    eps = 1e-12
    yhat = np.maximum(yhat, eps)
    y = np.maximum(y, eps)
    return np.mean(y / yhat - np.log(y / yhat) - 1.0)

def duan_smear(resid):
    return float(np.mean(np.exp(resid)))

def fit_predict(train, test, cols):
    Xtr = train[cols].to_numpy(float)
    ytr = train[TARGET].to_numpy(float)
    Xte = test[cols].to_numpy(float)
    Xtr_c = sm.add_constant(Xtr, has_constant='add')
    Xte_c = sm.add_constant(Xte, has_constant='add')
    model = sm.OLS(ytr, Xtr_c).fit()
    pred_log = model.predict(Xte_c)
    smear = duan_smear(model.resid)
    pred_rv = np.exp(pred_log) * smear
    pred_rv = np.maximum(pred_rv, 1e-12)
    return pred_rv, {"smear": smear, "params": {k: float(v) for k,v in zip(["const"]+cols, model.params)}, "rsquared": float(model.rsquared), "nobs": int(model.nobs)}

def block_bootstrap_qlike_diff(y, a, b, block_hours=24, n_boot=2000, seed=42):
    # paired diff in QLIKE (a-b) over blocks
    rng = np.random.default_rng(seed)
    n = len(y)
    block_ids = np.arange(n) // block_hours
    uniq = np.unique(block_ids)
    # precompute per-block contributions? easier: sample block indices
    diffs = []
    idx_by_block = {u: np.where(block_ids==u)[0] for u in uniq}
    blocks = list(uniq)
    B = len(blocks)
    for _ in range(n_boot):
        draw = rng.choice(B, size=B, replace=True)
        sel = np.concatenate([idx_by_block[blocks[i]] for i in draw])
        qa = qlike(y[sel], a[sel])
        qb = qlike(y[sel], b[sel])
        diffs.append(qa - qb)
    diffs = np.array(diffs)
    return diffs

def ci_pct(diffs, base_qlike_b):
    # improvement of a over b: (QLIKE_b - QLIKE_a)/QLIKE_b = -diff/base
    pct = (-diffs / base_qlike_b) * 100.0
    lo, hi = np.percentile(pct, [2.5, 97.5])
    return float(np.mean(pct)), float(lo), float(hi)

def main():
    t0 = time.time()
    df = pd.read_parquet(IN_PANEL)
    # ensure datetime
    if 'timestamp' in df.columns:
        ts = pd.to_datetime(df['timestamp'], utc=True)
    elif 'ts' in df.columns:
        ts = pd.to_datetime(df['ts'], utc=True)
    else:
        # try index
        ts = pd.to_datetime(df.index, utc=True)
    df = df.copy()
    df['_ts'] = ts
    df = df.sort_values('_ts')
    # purge/embargo: drop train rows within purge_days before test_start and test rows within embargo logic handled by fixed windows
    train = df[(df['_ts'] >= pd.Timestamp(TRAIN_START, tz='UTC')) & (df['_ts'] <= pd.Timestamp(TRAIN_END, tz='UTC') + pd.Timedelta(hours=23))].copy()
    test = df[(df['_ts'] >= pd.Timestamp(TEST_START, tz='UTC')) & (df['_ts'] <= pd.Timestamp(TEST_END, tz='UTC') + pd.Timedelta(hours=23))].copy()
    # apply purge: remove last PURGE_DAYS days from train end relative to test start
    purge_cut = pd.Timestamp(TEST_START, tz='UTC') - pd.Timedelta(days=PURGE_DAYS)
    train = train[train['_ts'] < purge_cut]
    # dropna on needed cols
    needed = set([TARGET, Y_COL] + BASE_COLS + FUND_COLS + EMA_COLS)
    for c in needed:
        if c not in df.columns:
            raise SystemExit(f"missing col {c}")
    train = train.dropna(subset=list(needed))
    test = test.dropna(subset=list(needed))
    results = {"meta": {"train_rows": len(train), "test_rows": len(test), "n_boot": N_BOOT, "seed": RNG_SEED, "purge_days": PURGE_DAYS}, "models": {}, "contrasts": {}}
    preds = {}
    for name, cols in MODELS.items():
        pred, info = fit_predict(train, test, cols)
        preds[name] = pred
        q = qlike(test[Y_COL].to_numpy(float), pred)
        results["models"][name] = {"qlike": float(q), **info}
        print(name, q, flush=True)
    y = test[Y_COL].to_numpy(float)
    contrasts = [
        ("B1_plus_funding","B1"),
        ("B1_plus_ema24","B1"),
        ("B1_plus_funding_plus_ema24","B1"),
        ("B1_plus_funding_plus_ema24","B1_plus_funding"),
        ("B1_plus_funding_plus_ema24","B1_plus_ema24"),
    ]
    for a,b in contrasts:
        diffs = block_bootstrap_qlike_diff(y, preds[a], preds[b], 24, N_BOOT, RNG_SEED)
        mean_pct, lo, hi = ci_pct(diffs, results["models"][b]["qlike"])
        results["contrasts"][f"{a}_vs_{b}"] = {
            "qlike_a": results["models"][a]["qlike"],
            "qlike_b": results["models"][b]["qlike"],
            "delta_qlike_a_minus_b": results["models"][a]["qlike"] - results["models"][b]["qlike"],
            "improvement_pct_mean": mean_pct,
            "ci95_pct_lo": lo,
            "ci95_pct_hi": hi,
            "ci_crosses_zero": bool(lo <= 0 <= hi),
        }
        print(a,"vs",b,mean_pct,lo,hi, flush=True)
    results["elapsed_s"] = time.time()-t0
    outj = OUT_DIR / f"rca011_feature_attribution_{UTC}.json"
    outj.write_text(json.dumps(results, indent=2))
    # md
    lines = [f"# RCA011 Feature Attribution {UTC}", "", f"train_rows={len(train)} test_rows={len(test)} n_boot={N_BOOT}", "", "## Models", "|model|QLIKE|smear|R2|", "|---|---:|---:|---:|"]
    for n,m in results["models"].items():
        lines.append(f"|{n}|{m['qlike']:.6f}|{m['smear']:.6f}|{m['rsquared']:.6f}|")
    lines += ["", "## Contrasts", "|contrast|dQLIKE(a-b)|impr% mean|CI95 lo|CI95 hi|cross0|", "|---|---:|---:|---:|---:|:---:|"]
    for n,c in results["contrasts"].items():
        lines.append(f"|{n}|{c['delta_qlike_a_minus_b']:.6f}|{c['improvement_pct_mean']:.4f}|{c['ci95_pct_lo']:.4f}|{c['ci95_pct_hi']:.4f}|{c['ci_crosses_zero']}|")
    (OUT_DIR / f"rca011_feature_attribution_{UTC}.md").write_text("\n".join(lines)+"\n")
    print("WROTE", outj, flush=True)

if __name__=='__main__':
    main()
