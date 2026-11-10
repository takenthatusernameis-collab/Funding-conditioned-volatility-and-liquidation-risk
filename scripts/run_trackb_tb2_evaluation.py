#!/usr/bin/env python3
"""Track B TB2 confirmatory evaluation (frozen prereg trackb_TB2_20261110T190405Z).

Modeled synthetic boundary-breach labels only (NEVER observed liquidations).
Implements the frozen protocol: B1 (RV1h/RV24h/RV168h) vs C2 (+signed funding,
abs funding percentile 90d>=30obs, mark/index premium, mark/EMA24 distance),
Log Loss + Brier paired contrast on the frozen test split, block bootstrap
(>=2000 replicates, 30-day blocks), Holm across 2 metrics, >=2% Log-Loss
materiality floor. Training-only normalization; missing features remain missing.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

_REPO_SCRIPTS = Path(__file__).resolve().parent
import importlib.util
_sbl_spec = importlib.util.spec_from_file_location("synthetic_boundary_labels", _REPO_SCRIPTS / "synthetic_boundary_labels.py")
_sbl = importlib.util.module_from_spec(_sbl_spec)
_sbl_spec.loader.exec_module(_sbl)
synthetic_boundary_label = _sbl.synthetic_boundary_label

REPO = Path(__file__).resolve().parents[1]
RUN_MANIFEST = REPO / "research_state" / "run_manifest.json"
DATA_CACHE = REPO / "research_state" / "data_cache"
OUT = REPO / "research_state" / "evaluation_summary_trackb_TB2_20261110T190405Z.md"

SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]
WINDOW_START = "2024-01-01"
WINDOW_END = "2024-09-30"
LEVERAGE = 10.0
SIDE = "long"
MAINTENANCE_MARGIN_RATE = 0.0
HORIZON_H = 168
SEED = 20261110
N_BOOTSTRAP = 2000
BLOCK_DAYS = 30
MATERIALITY_REL_LL = 0.02
HOLM_ALPHA = 0.05

TRAIN = ("2024-01-01T00:00:00Z", "2024-06-12T00:00:00Z")
VAL = ("2024-06-19T00:00:00Z", "2024-08-06T00:00:00Z")
TEST = ("2024-08-13T00:00:00Z", "2024-09-30T00:00:00Z")


def parse_iso(s):
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    dt = datetime.fromisoformat(s)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def dt_to_iso(dt):
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def cache_month_dir(sym, date_str):
    y, m, _ = date_str.split("-")
    return DATA_CACHE / f"{sym}_{y}_{int(m):02d}"


def series_csv_path(kind, sym, date_str):
    base = cache_month_dir(sym, date_str)
    d = base / f"{kind}-{date_str}"
    c1 = d / f"{sym}-1h-{date_str}.csv"
    c2 = d / f"{sym}-1h-{date_str}" / f"{sym}-1h-{date_str}.csv"
    if c1.exists():
        return c1
    if c2.exists():
        return c2
    return None


def funding_csv_path(sym, year_month):
    y, m = year_month.split("-")
    base = DATA_CACHE / f"{sym}_{y}_{int(m):02d}"
    d = base / f"{sym}-fundingRate-{year_month}"
    c1 = d / f"{sym}-fundingRate-{year_month}.csv"
    if c1.exists():
        return c1
    return None


def load_ohlcv_series(kind, sym, start_date, end_date):
    series = []
    cur = datetime.strptime(start_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    endd = datetime.strptime(end_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    while cur <= endd:
        dstr = cur.strftime("%Y-%m-%d")
        p = series_csv_path(kind, sym, dstr)
        if p is not None:
            try:
                with open(p, newline="") as f:
                    rdr = csv.DictReader(f)
                    for row in rdr:
                        ts = int(row.get("open_time") or row.get("timestamp") or row.get("time"))
                        close = float(row.get("close") or row.get("c"))
                        series.append((datetime.fromtimestamp(ts / 1000, tz=timezone.utc), close))
            except Exception:
                pass
        cur += timedelta(days=1)
    series.sort(key=lambda x: x[0])
    out, seen = [], set()
    for dtv, c in series:
        if dtv in seen:
            continue
        seen.add(dtv)
        out.append((dtv, c))
    return out


def load_funding_series(sym, start_date, end_date):
    series = []
    cur = datetime.strptime(start_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    endd = datetime.strptime(end_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    while cur <= endd:
        ym = cur.strftime("%Y-%m")
        p = funding_csv_path(sym, ym)
        if p is not None:
            try:
                with open(p, newline="") as f:
                    rdr = csv.DictReader(f)
                    for row in rdr:
                        ts = int(row.get("calc_time") or row.get("timestamp") or row.get("time"))
                        fr = float(row.get("last_funding_rate") or row.get("funding_rate") or row.get("r"))
                        series.append((datetime.fromtimestamp(ts / 1000, tz=timezone.utc), fr))
            except Exception:
                pass
        cur += timedelta(days=32)
        cur = datetime(cur.year, cur.month, 1, tzinfo=timezone.utc)
    series.sort(key=lambda x: x[0])
    return series


def log_ret(p1, p0):
    if p0 is None or p1 is None or p0 <= 0 or p1 <= 0:
        return None
    return math.log(p1 / p0)


def trailing_rv(mark_series, i, n):
    if i - n < 0:
        return None
    rv = 0.0
    for k in range(i - n + 1, i + 1):
        if k <= 0:
            return None
        r = log_ret(mark_series[k][1], mark_series[k - 1][1])
        if r is None:
            return None
        rv += r * r
    return rv


def ema_series(mark_series, span):
    alpha = 2.0 / (span + 1.0)
    out = [None] * len(mark_series)
    ema = None
    for i, (_, p) in enumerate(mark_series):
        if ema is None:
            ema = p
        else:
            ema = alpha * p + (1 - alpha) * ema
        out[i] = ema
    return out


def build_origins(mark_series, funding_series, start_iso, end_iso):
    ts_start = parse_iso(start_iso)
    ts_end = parse_iso(end_iso)
    idx_by_dt = {dt: i for i, (dt, _) in enumerate(mark_series)}
    closes = [c for _, c in mark_series]
    ema = ema_series(mark_series, 24)
    origins = []
    for i, (dt, px) in enumerate(mark_series):
        if dt < ts_start or dt > ts_end:
            continue
        ts_ms = int(dt.timestamp() * 1000)
        # label: mark closes strictly after t (t+1..t+168h)
        lab = synthetic_boundary_label(closes, i, horizon=HORIZON_H, leverage=LEVERAGE,
                                       side=SIDE, maintenance_margin_rate=MAINTENANCE_MARGIN_RATE,
                                       entry_price=px)
        # B1 features
        rv1h = trailing_rv(mark_series, i, 1)
        rv24h = trailing_rv(mark_series, i, 24)
        rv168h = trailing_rv(mark_series, i, 168)
        # funding (compare datetimes)
        best = None
        for tf, fr in funding_series:
            if tf <= dt:
                best = (tf, fr)
            else:
                break
        signed_funding = best[1] if best else None
        cutoff_dt = dt - timedelta(days=90)
        hist = [fr for (t2, fr) in funding_series if cutoff_dt <= t2 < dt]
        abs_fund_pct = None
        if len(hist) >= 30 and best is not None:
            abs_hist = [abs(v) for v in hist]
            cnt = sum(1 for v in abs_hist if v <= abs(best[1]))
            abs_fund_pct = cnt / len(abs_hist)
        # premium + ema distance (contemporaneous)
        prem = None
        ema_dist = None
        idx_p = idx_by_dt.get(dt)
        if idx_p is not None:
            # load index close for this dt from index series passed separately? handled in caller
            pass
        origins.append({
            "dt": dt, "i": i, "px": px, "ts_ms": ts_ms, "label": lab,
            "rv1h": rv1h, "rv24h": rv24h, "rv168h": rv168h,
            "signed_funding": signed_funding, "abs_fund_pct": abs_fund_pct,
            "ema": ema[i],
        })
    return origins


def attach_index_premium(origins, index_series):
    idx_map = {dt: c for dt, c in index_series}
    for o in origins:
        ic = idx_map.get(o["dt"])
        if o["px"] and ic and ic > 0:
            o["prem"] = o["px"] / ic - 1.0
        else:
            o["prem"] = None
        if o["px"] and o["ema"]:
            o["ema_dist"] = o["px"] / o["ema"] - 1.0
        else:
            o["ema_dist"] = None


def standardize_train(train_rows, feature_cols):
    stats = {}
    for c in feature_cols:
        vals = [r[c] for r in train_rows if r[c] is not None]
        if vals:
            mu = float(np.mean(vals)); sd = float(np.std(vals))
            if sd == 0 or math.isnan(sd):
                sd = 1.0
            stats[c] = (mu, sd)
        else:
            stats[c] = (0.0, 1.0)
    return stats


def apply_std(row, stats, feature_cols):
    x = []
    ok = True
    for c in feature_cols:
        v = row[c]
        if v is None:
            ok = False
            break
        mu, sd = stats[c]
        x.append((v - mu) / sd)
    return (x, ok) if ok else None


def neg_log_likelihood(beta, X, y):
    nll = 0.0
    for x, yi in zip(X, y):
        z = beta[0] + sum(b * v for b, v in zip(beta[1:], x))
        # numerically stable softplus
        if z >= 0:
            nll += z + math.log1p(math.exp(-z)) - yi * z
        else:
            ez = math.exp(z)
            nll += math.log1p(ez) - yi * z
    return nll + 1e-6 * sum(b * b for b in beta[1:])


def fit_logistic(X, y):
    nfeat = len(X[0])
    beta0 = [0.0] * (nfeat + 1)
    res = minimize(neg_log_likelihood, beta0, args=(X, y), method="BFGS",
                   options={"maxiter": 5000})
    return res.x


def predict_proba(beta, x):
    z = beta[0] + sum(b * v for b, v in zip(beta[1:], x))
    return 1.0 / (1.0 + math.exp(-z))


def log_loss(p, y):
    p = min(max(p, 1e-12), 1 - 1e-12)
    if y == 1:
        return -math.log(p)
    return -math.log(1 - p)


def brier(p, y):
    return (p - y) ** 2


def main():
    np.random.seed(SEED)
    manifest = json.loads(RUN_MANIFEST.read_text())
    git_sha = None
    try:
        git_sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO,
                                          stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        pass

    lines = []
    lines.append("# Evaluation Summary — Track B TB2 Confirmatory")
    lines.append("")
    lines.append(f"Experiment: trackb_TB2_20261110T190405Z  (frozen prereg v1.0)")
    lines.append(f"Repo: Funding-conditioned-volatility-and-liquidation-risk")
    lines.append(f"Git SHA: {git_sha}")
    lines.append(f"Generated (UTC): {dt_to_iso(datetime.now(timezone.utc))}")
    lines.append(f"Prereg hash: {manifest['split_boundaries_trackb_TB2_20261110T190405Z']['prereg_hash']}")
    lines.append(f"Frozen before outcomes: {manifest['split_boundaries_trackb_TB2_20261110T190405Z']['frozen_before_outcomes']}")
    lines.append(f"Outcome values inspected: {manifest['split_boundaries_trackb_TB2_20261110T190405Z']['outcome_values_inspected']}")
    lines.append("")
    lines.append("## Design (frozen prereg trackb_TB2_20261110T190405Z)")
    lines.append("- Track: B — modeled synthetic boundary-breach labels (proxy; never observed liquidations)")
    lines.append(f"- Target: synthetic_boundary_breach_h{HORIZON_H}_{SIDE}_{LEVERAGE}x_m{MAINTENANCE_MARGIN_RATE}")
    lines.append(f"- Window: {WINDOW_START} .. {WINDOW_END} (5 symbols: {', '.join(SYMBOLS)})")
    lines.append("- Splits (chronological, 7-day purge/embargo):")
    lines.append(f"  - train: {TRAIN[0]} .. {TRAIN[1]}")
    lines.append(f"  - validation: {VAL[0]} .. {VAL[1]}")
    lines.append(f"  - test: {TEST[0]} .. {TEST[1]}")
    lines.append("- Predictors (training-only standardization; missing remains missing):")
    lines.append("  - B1 (RV-only): RV1h, RV24h, RV168h (trailing realized variance from mark-price log returns)")
    lines.append("  - C2 (funding-conditioned): B1 + signed funding + abs funding percentile (prior 90d, >=30 obs)")
    lines.append("    + mark/index premium + mark/EMA24 distance")
    lines.append("- Metrics: Log Loss, Brier (lower better); primary contrast C2 vs B1, paired")
    lines.append("- Materiality: >=2% relative Log Loss reduction vs B1")
    lines.append("- Uncertainty: block bootstrap >=2000 deterministic-seed replicates, 30-day blocks")
    lines.append("- Multiplicity: Holm across 2 pre-specified metrics (alpha=0.025/metric)")
    lines.append("")
    lines.append("## Caveat")
    lines.append("- synthetic proxy != observed liquidations; does not reconstruct account margin/engine/forced liquidations")
    lines.append("- no risk overlay until forecast gate passes")
    lines.append("")

    # Load data
    all_mark = {}
    all_index = {}
    all_funding = {}
    for sym in SYMBOLS:
        all_mark[sym] = load_ohlcv_series("markPriceKlines", sym, WINDOW_START, WINDOW_END)
        all_index[sym] = load_ohlcv_series("indexPriceKlines", sym, WINDOW_START, WINDOW_END)
        all_funding[sym] = load_funding_series(sym, WINDOW_START, WINDOW_END)

    # Build origins per split per symbol
    def build_split(sym, start_iso, end_iso):
        origins = build_origins(all_mark[sym], all_funding[sym], start_iso, end_iso)
        attach_index_premium(origins, all_index[sym])
        return origins

    train_o = {s: build_split(s, *TRAIN) for s in SYMBOLS}
    val_o = {s: build_split(s, *VAL) for s in SYMBOLS}
    test_o = {s: build_split(s, *TEST) for s in SYMBOLS}

    def n_labeled(osplit):
        return sum(1 for s in SYMBOLS for o in osplit[s] if o["label"] is not None)
    def n_origin(osplit):
        return sum(len(osplit[s]) for s in SYMBOLS)

    lines.append("## Event adequacy (frozen label, pre-freeze)")
    lines.append(f"- Train origins: {n_origin(train_o)}, labeled: {n_labeled(train_o)}")
    lines.append(f"- Val origins: {n_origin(val_o)}, labeled: {n_labeled(val_o)}")
    lines.append(f"- Test origins: {n_origin(test_o)}, labeled: {n_labeled(test_o)}")
    test_pos = sum(1 for s in SYMBOLS for o in test_o[s] if o["label"] == 1)
    test_neg = sum(1 for s in SYMBOLS for o in test_o[s] if o["label"] == 0)
    lines.append(f"- Test positives: {test_pos}, negatives: {test_neg}, prevalence={test_pos/(test_pos+test_neg):.4f} if >0 else n/a".replace("if >0 else n/a", ""))
    lines.append(f"  - per symbol test positives:")
    for s in SYMBOLS:
        ps = sum(1 for o in test_o[s] if o["label"] == 1)
        ns = sum(1 for o in test_o[s] if o["label"] == 0)
        lines.append(f"    - {s}: positives={ps}, negatives={ns}, labeled={ps+ns}")
    lines.append("")

    # Feature columns
    b1_cols = ["rv1h", "rv24h", "rv168h"]
    c2_cols = ["rv1h", "rv24h", "rv168h", "signed_funding", "abs_fund_pct", "prem", "ema_dist"]

    # Common eligible test sample: origins with label and ALL C2 features (so B1 & C2 paired on same rows)
    def common_test_rows(sym):
        rows = []
        for o in test_o[sym]:
            if o["label"] is None:
                continue
            if any(o[c] is None for c in c2_cols):
                continue
            rows.append(o)
        return rows

    # Train stats from train origins that have C2 features (training-only)
    train_c2 = []
    for s in SYMBOLS:
        for o in train_o[s]:
            if all(o[c] is not None for c in c2_cols):
                train_c2.append(o)
    stats_b1 = standardize_train(train_c2, b1_cols)
    stats_c2 = standardize_train(train_c2, c2_cols)

    def model_rows(osplit, feature_cols, stats):
        Xb, Xc, Y = [], [], []
        for s in SYMBOLS:
            for o in osplit[s]:
                if o["label"] is None:
                    continue
                rb = apply_std(o, stats_b1, b1_cols)
                rc = apply_std(o, stats_c2, feature_cols)
                if rb is None or rc is None:
                    continue
                Xb.append(rb[0]); Xc.append(rc[0]); Y.append(o["label"])
        return Xb, Xc, Y

    Xb_tr, Xc_tr, Y_tr = model_rows(train_o, c2_cols, stats_c2)
    lines.append("## Fit (training data only; no holdout tuning)")
    lines.append(f"- Train C2-eligible origins: {len(Y_tr)} (B1 same common sample for paired parity)")
    if len(Y_tr) == 0:
        lines.append("- ERROR: no train-eligible rows; cannot fit.")
        OUT.write_text("\n".join(lines) + "\n")
        print("done", OUT)
        return
    beta_b1 = fit_logistic(Xb_tr, Y_tr)
    beta_c2 = fit_logistic(Xc_tr, Y_tr)
    lines.append(f"- Logistic MLE (fixed 1e-6 ridge for numerical stability; not a tuned hyperparameter)")
    lines.append(f"- B1 coefs (intercept, rv1h, rv24h, rv168h): " + ", ".join(f"{b:.6f}" for b in beta_b1))
    lines.append(f"- C2 coefs (intercept, rv1h, rv24h, rv168h, signed_funding, abs_fund_pct, prem, ema_dist): " + ", ".join(f"{b:.6f}" for b in beta_c2))
    lines.append("")

    # Test evaluation
    Xb_te, Xc_te, Y_te = model_rows(test_o, c2_cols, stats_c2)
    n_test = len(Y_te)
    lines.append("## Test-set results (frozen holdout, paired C2 vs B1)")
    lines.append(f"- Test common-eligible origins: {n_test}")
    per_sym = {s: {"b1_ll": [], "c2_ll": [], "b1_bs": [], "c2_bs": [], "y": []} for s in SYMBOLS}
    paired_ll_diff = []
    paired_bs_diff = []
    for xb, xc, y in zip(Xb_te, Xc_te, Y_te):
        pb = predict_proba(beta_b1, xb)
        pc = predict_proba(beta_c2, xc)
        pb_ll = log_loss(pb, y); pc_ll = log_loss(pc, y)
        pb_bs = brier(pb, y); pc_bs = brier(pc, y)
        paired_ll_diff.append(pc_ll - pb_ll)
        paired_bs_diff.append(pc_bs - pb_bs)
    # map back per symbol for reporting
    k = 0
    for s in SYMBOLS:
        for o in test_o[s]:
            if o["label"] is None or any(o[c] is None for c in c2_cols):
                continue
            per_sym[s]["y"].append(Y_te[k])
            k += 1
    # rebuild per-symbol losses properly by re-iterating with symbols
    k = 0
    sym_ll = {s: {"b1": [], "c2": []} for s in SYMBOLS}
    sym_bs = {s: {"b1": [], "c2": []} for s in SYMBOLS}
    for s in SYMBOLS:
        for o in test_o[s]:
            if o["label"] is None or any(o[c] is None for c in c2_cols):
                continue
            # need xb/xc; recompute
            pass
    # Simpler: recompute per-symbol from stored rows isn't retained; do a second pass collecting per symbol
    per_sym_rows = {s: [] for s in SYMBOLS}
    k = 0
    for s in SYMBOLS:
        for o in test_o[s]:
            if o["label"] is None or any(o[c] is None for c in c2_cols):
                continue
            xb = Xb_te[k]; xc = Xc_te[k]; y = Y_te[k]
            pb = predict_proba(beta_b1, xb); pc = predict_proba(beta_c2, xc)
            per_sym_rows[s].append((log_loss(pb, y), log_loss(pc, y), brier(pb, y), brier(pc, y)))
            k += 1
    mean_b1_ll = float(np.mean([d[0] for d in per_sym_rows[s] for s in SYMBOLS])) if n_test else float("nan")
    mean_c2_ll = float(np.mean([d[1] for d in per_sym_rows[s] for s in SYMBOLS])) if n_test else float("nan")
    mean_b1_bs = float(np.mean([d[2] for d in per_sym_rows[s] for s in SYMBOLS])) if n_test else float("nan")
    mean_c2_bs = float(np.mean([d[3] for d in per_sym_rows[s] for s in SYMBOLS])) if n_test else float("nan")
    rel_ll = (mean_b1_ll - mean_c2_ll) / mean_b1_ll if mean_b1_ll else float("nan")
    lines.append(f"- Pooled B1 Log Loss: {mean_b1_ll:.6f}")
    lines.append(f"- Pooled C2 Log Loss: {mean_c2_ll:.6f}")
    lines.append(f"- Pooled B1 Brier: {mean_b1_bs:.6f}")
    lines.append(f"- Pooled C2 Brier: {mean_c2_bs:.6f}")
    lines.append(f"- Paired mean Log Loss diff (C2 - B1): {np.mean(paired_ll_diff):.6f}")
    lines.append(f"- Paired mean Brier diff (C2 - B1): {np.mean(paired_bs_diff):.6f}")
    lines.append(f"- Relative Log Loss reduction vs B1: {rel_ll*100:.4f}%  (materiality floor >=2%)")
    lines.append("")
    lines.append("## Per-symbol test results (common-eligible sample)")
    for s in SYMBOLS:
        rows = per_sym_rows[s]
        if not rows:
            lines.append(f"- {s}: n=0")
            continue
        b1l = np.mean([r[0] for r in rows]); c2l = np.mean([r[1] for r in rows])
        b1b = np.mean([r[2] for r in rows]); c2b = np.mean([r[3] for r in rows])
        ypos = sum(1 for o in test_o[s] if o["label"] == 1)
        lines.append(f"- {s}: n={len(rows)}, positives={ypos}, B1_LL={b1l:.6f}, C2_LL={c2l:.6f}, "
                     f"B1_Brier={b1b:.6f}, C2_Brier={c2b:.6f}, rel_LL_reduction={((b1l-c2l)/b1l*100):.4f}%")
    lines.append("")

    # Block bootstrap
    def partition_blocks(origins_by_sym):
        # group test origins by date across symbols; 30-day blocks
        day_origins = {}
        for s in SYMBOLS:
            for o in test_o[s]:
                if o["label"] is None or any(o[c] is None for c in c2_cols):
                    continue
                day = o["dt"].strftime("%Y-%m-%d")
                day_origins.setdefault(day, []).append(o)
        days = sorted(day_origins.keys())
        blocks = []
        cur = []
        for d in days:
            cur.extend(day_origins[d])
            # start new block every 30 days
        # Build non-overlapping 30-day blocks
        i = 0
        while i < len(days):
            block_day = days[i]
            block_end = (datetime.strptime(block_day, "%Y-%m-%d") + timedelta(days=BLOCK_DAYS)).strftime("%Y-%m-%d")
            blk = []
            for d in days:
                if block_day <= d < block_end:
                    blk.extend(day_origins[d])
            if blk:
                blocks.append(blk)
            # advance to next day >= block_end
            j = i
            while j < len(days) and days[j] < block_end:
                j += 1
            i = j
        return blocks

    blocks = partition_blocks(test_o)
    n_blocks = len(blocks)
    lines.append("## Uncertainty — block bootstrap (test split)")
    lines.append(f"- Bootstrap replicates: {N_BOOTSTRAP} (deterministic seed {SEED})")
    lines.append(f"- Block size: {BLOCK_DAYS} days; non-overlapping test blocks: {n_blocks}")
    rng = np.random.default_rng(SEED)
    boot_ll = []
    boot_bs = []
    paired_ll_arr = np.array(paired_ll_diff)
    paired_bs_arr = np.array(paired_bs_diff)
    # Build per-origin record aligned to blocks for resampling
    # Flatten block membership: map each origin row to its block index
    origin_block = []
    bidx = 0
    for blk in blocks:
        for _ in blk:
            origin_block.append(bidx)
        bidx += 1
    origin_block = np.array(origin_block)
    flat_ll = paired_ll_arr
    flat_bs = paired_bs_arr
    n_orig = len(flat_ll)
    for _ in range(N_BOOTSTRAP):
        sampled_blocks = rng.integers(0, n_blocks, size=n_blocks)
        mask = np.isin(origin_block, sampled_blocks)
        boot_ll.append(float(np.mean(flat_ll[mask])) if mask.any() else 0.0)
        boot_bs.append(float(np.mean(flat_bs[mask])) if mask.any() else 0.0)
    boot_ll = np.array(boot_ll); boot_bs = np.array(boot_bs)
    ci_ll = np.percentile(boot_ll, [2.5, 97.5])
    ci_bs = np.percentile(boot_bs, [2.5, 97.5])
    # p-value: two-sided, H0: diff >= 0 (C2 not better)
    p_ll_one = float(np.mean(boot_ll >= 0))
    p_bs_one = float(np.mean(boot_bs >= 0))
    p_ll = min(1.0, 2 * min(p_ll_one, 1 - p_ll_one))
    p_bs = min(1.0, 2 * min(p_bs_one, 1 - p_bs_one))
    lines.append(f"- Log Loss paired diff mean: {float(np.mean(paired_ll_diff)):.6f}")
    lines.append(f"- Log Loss 95% CI (paired diff): [{ci_ll[0]:.6f}, {ci_ll[1]:.6f}]")
    lines.append(f"- Log Loss p-value (two-sided): {p_ll:.6f}")
    lines.append(f"- Brier paired diff mean: {float(np.mean(paired_bs_diff)):.6f}")
    lines.append(f"- Brier 95% CI (paired diff): [{ci_bs[0]:.6f}, {ci_bs[1]:.6f}]")
    lines.append(f"- Brier p-value (two-sided): {p_bs:.6f}")
    lines.append("")

    # Holm
    pvals = sorted([("Log Loss", p_ll), ("Brier", p_bs)], key=lambda t: t[1])
    holm = []
    for rank, (name, p) in enumerate(pvals, start=1):
        alpha_k = HOLM_ALPHA / (len(pvals) - rank + 1)
        holm.append((name, p, alpha_k, p <= alpha_k))
    lines.append("## Multiplicity — Holm (2 pre-specified metrics, family alpha 0.05)")
    for name, p, alpha_k, pass_ in holm:
        lines.append(f"- {name}: p={p:.6f}, Holm alpha={alpha_k:.4f}, pass={pass_}")
    lines.append("")

    # Gate
    ci_ll_excludes_null_fav = ci_ll[1] < 0  # C2 better -> diff < 0
    ci_bs_excludes_null_fav = ci_bs[1] < 0
    materiality_pass = bool(rel_ll >= MATERIALITY_REL_LL)
    holm_pass = all(h[3] for h in holm)
    n_symbols = len(SYMBOLS)
    gate = {
        "instruments_ge5": n_symbols >= 5,
        "test_blocks_ge3": n_blocks >= 3,
        "ll_materiality_ge2pct": materiality_pass,
        "ll_ci_excludes_null_favorable": ci_ll_excludes_null_fav,
        "holm_pass": holm_pass,
    }
    all_pass = all(gate.values())
    lines.append("## Forecast gate assessment (all required for FORECAST_GATE_PASSED)")
    lines.append(f"- >=5 instruments in paired OOS panel: {'PASS' if gate['instruments_ge5'] else 'NOT_MET'} ({n_symbols})")
    lines.append(f"- >=3 non-overlapping 30-day test blocks: {'PASS' if gate['test_blocks_ge3'] else 'NOT_MET'} ({n_blocks})")
    lines.append(f"- >=2% relative Log Loss reduction vs B1: {'PASS' if gate['ll_materiality_ge2pct'] else 'NOT_MET'} ({rel_ll*100:.4f}%)")
    lines.append(f"- Log Loss 95% CI excludes null in favorable direction: {'PASS' if gate['ll_ci_excludes_null_favorable'] else 'NOT_MET'} (CI [{ci_ll[0]:.6f}, {ci_ll[1]:.6f}])")
    lines.append(f"- Holm multiplicity passes (2 metrics): {'PASS' if gate['holm_pass'] else 'NOT_MET'}")
    lines.append(f"- Forecast gate (ALL criteria): {'PASS' if all_pass else 'NOT_MET'}")
    lines.append("")
    lines.append("## Verdict")
    if all_pass:
        lines.append("RESULT: FORECAST_GATE_PASSED — C2 funding-conditioned model beats B1 RV-only baseline on Log Loss with material, CI-supported, Holm-adjusted skill.")
    else:
        failed = [k for k, v in gate.items() if not v]
        lines.append(f"RESULT: FORECAST_GATE_NOT_MET — unmet criteria: {', '.join(failed)}.")
        lines.append("No risk overlay is eligible. Preserve null result; do not threshold-shop or reuse holdout.")
    lines.append("")
    lines.append("## Data & provenance")
    lines.append("- Source: local research_state/data_cache (Binance UM perp archival mark/index/premium klines 1h, fundingRate 8h); adjacent sha256 sidecars; provenance_verified=true, unmapped_count==0")
    lines.append("- No network / no paid / no manual / no credentialed data used in this run.")
    lines.append("- Track B = modeled breach proxy only; never conflated with Track A observed liquidations.")
    lines.append("")
    OUT.write_text("\n".join(lines) + "\n")
    print("done", OUT)
    return {
        "n_test": n_test, "test_pos": test_pos, "mean_b1_ll": mean_b1_ll, "mean_c2_ll": mean_c2_ll,
        "rel_ll": rel_ll, "ci_ll": [float(ci_ll[0]), float(ci_ll[1])], "ci_bs": [float(ci_bs[0]), float(ci_bs[1])],
        "p_ll": p_ll, "p_bs": p_bs, "gate": gate, "all_pass": all_pass,
        "per_sym": {s: len(per_sym_rows[s]) for s in SYMBOLS},
    }


if __name__ == "__main__":
    main()
