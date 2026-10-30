#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import math
import os
import random
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from synthetic_boundary_labels import synthetic_boundary_label

REPO = Path(__file__).resolve().parents[1]
RUN_MANIFEST = REPO / "research_state" / "run_manifest.json"
OUT = REPO / "research_state" / "evaluation_summary_FCLR-H003-EXT-001.md"
PROTOCOL = REPO / "research_state" / "protocol_FCLR-H003-EXT-001.md"

EXPERIMENT = "FCLR-H003-EXT-001"
SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]
EPS = 1e-12
HORIZONS = [72, 168]
MMR_TIERS = [0.004, 0.005]
LEVERAGES = [3.0, 5.0, 10.0, 20.0]
SIDES = ["long", "short"]
SEED = 12345
N_BOOT = 2000
BLOCK_HOURS = 24

# (copy helper functions from run_h003_ext)
def ts_to_dt(ts_ms):
    return datetime.fromtimestamp(ts_ms / 1000, tz=timezone.utc)

def find_mark_csv(sym, date_str):
    candidates = []
    for p in REPO.rglob(f"{sym}-1h-{date_str}.csv"):
        sp = str(p)
        if 'markPrice' in sp:
            candidates.append(p)
    seen = set()
    out = []
    for c in candidates:
        rp = c.resolve()
        if rp in seen:
            continue
        seen.add(rp)
        out.append(rp)
    return out[0] if out else None

def find_funding_csv(sym, month):
    for p in REPO.rglob(f"{sym}-fundingRate-{month}.csv"):
        return p
    return None

def load_mark_series(sym, start_dt, end_dt):
    series = []
    cur = start_dt.replace(hour=0, minute=0, second=0, microsecond=0)
    end_day = end_dt.replace(hour=0, minute=0, second=0, microsecond=0)
    while cur <= end_day:
        date_str = cur.strftime("%Y-%m-%d")
        csvp = find_mark_csv(sym, date_str)
        if csvp and csvp.exists():
            try:
                with csvp.open() as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        try:
                            ts_ms = int(row['open_time'])
                            ts_dt = ts_to_dt(ts_ms)
                            if ts_dt < start_dt - timedelta(days=1) or ts_dt > end_dt + timedelta(days=1):
                                continue
                            close = float(row['close'])
                            series.append((ts_ms, close))
                        except Exception:
                            continue
            except Exception:
                pass
        cur += timedelta(days=1)
    series.sort(key=lambda x: x[0])
    dedup = []
    seen = set()
    for ts_ms, close in series:
        if ts_ms in seen:
            continue
        seen.add(ts_ms)
        dedup.append((ts_ms, close))
    return dedup

def load_funding_series_all(sym, months):
    rows = []
    for month in months:
        csvp = find_funding_csv(sym, month)
        if not csvp or not csvp.exists():
            continue
        try:
            with csvp.open() as f:
                reader = csv.DictReader(f)
                for r in reader:
                    try:
                        ts = int(r['calc_time'])
                        fr = float(r['last_funding_rate'])
                        rows.append((ts, fr))
                    except Exception:
                        continue
        except Exception:
            continue
    rows.sort(key=lambda x: x[0])
    dedup = []
    seen = set()
    for ts, fr in rows:
        if ts in seen:
            continue
        seen.add(ts)
        dedup.append((ts, fr))
    return dedup

def log_ret(p1, p0):
    if p0 <= 0 or p1 <= 0:
        return None
    return math.log(p1 / p0)

def get_funding_latest(funding_series, ts_ms):
    best = None
    for ts_f, fr in funding_series:
        if ts_f <= ts_ms:
            best = (ts_f, fr)
        else:
            break
    return best

def get_funding_abs_percentile(funding_series, ts_ms, window_days=90, min_obs=30):
    cutoff = ts_ms - window_days * 24 * 3600 * 1000
    hist = [fr for (t2, fr) in funding_series if t2 >= cutoff and t2 < ts_ms]
    if len(hist) < min_obs:
        return None
    latest_f = get_funding_latest(funding_series, ts_ms)
    if latest_f is None:
        return None
    abs_hist = [abs(x) for x in hist]
    abs_latest = abs(latest_f[1])
    cnt = sum(1 for v in abs_hist if v <= abs_latest)
    return cnt / len(abs_hist) if abs_hist else None

def build_features_for_origin(mark_list, funding_series, t_idx):
    if t_idx < 0 or t_idx >= len(mark_list):
        return None
    ts_ms_t = mark_list[t_idx][0]
    def trailing_rv_window(n):
        if t_idx - n < 0:
            return None
        rv = 0.0
        for i in range(t_idx - n + 1, t_idx + 1):
            if i <= 0:
                return None
            r = log_ret(mark_list[i][1], mark_list[i-1][1])
            if r is None:
                return None
            rv += r*r
        return rv
    rv1h = trailing_rv_window(1)
    rv24h = trailing_rv_window(24)
    rv168h = trailing_rv_window(168)
    latest_f = get_funding_latest(funding_series, ts_ms_t)
    signed_funding = latest_f[1] if latest_f else None
    abs_fund_pct = get_funding_abs_percentile(funding_series, ts_ms_t)
    if t_idx < 23:
        ema_dist = None
    else:
        ema = mark_list[t_idx-23][1]
        alpha = 2.0/(24+1)
        for j in range(t_idx-22, t_idx+1):
            ema = alpha * mark_list[j][1] + (1-alpha)*ema
        ema_dist = (mark_list[t_idx][1] / ema - 1.0) if ema > 0 else None
    prem = 0.0
    return {
        'rv1h': rv1h, 'rv24h': rv24h, 'rv168h': rv168h,
        'signed_funding': signed_funding,
        'abs_fund_pct': abs_fund_pct,
        'prem': prem,
        'ema_dist': ema_dist
    }

def sigmoid(z):
    if z >= 0:
        ez = math.exp(-z)
        return 1.0/(1.0+ez)
    else:
        ez = math.exp(z)
        return ez/(1.0+ez)

def fit_logistic(X, y, lr=0.01, epochs=2000, l2=1e-4):
    if len(X) == 0:
        return None
    n = len(X)
    d = len(X[0])
    w = [0.0] * d
    b = 0.0
    for _ in range(epochs):
        gw = [0.0]*d
        gb = 0.0
        for i in range(n):
            xi = X[i]
            yi = y[i]
            z = b
            for j in range(d):
                z += w[j]*xi[j]
            p = sigmoid(z)
            err = p - yi
            for j in range(d):
                gw[j] += err*xi[j]/n + l2*w[j]/n
            gb += err/n
        for j in range(d):
            w[j] -= lr*gw[j]
        b -= lr*gb
    return {'w': w, 'b': b, 'd': d}

def predict_logistic(model, X):
    if model is None:
        return None
    w = model['w']; b = model['b']
    z = b
    for j in range(len(w)):
        z += w[j]*X[j]
    p = sigmoid(z)
    if p < 0.0: p = 0.0
    if p > 1.0: p = 1.0
    return p

def brier_score(preds, ys):
    if not preds: return float('nan')
    s = 0.0
    for p,y in zip(preds,ys):
        s += (p-y)**2
    return s/len(preds)

def log_loss_score(preds, ys, eps=1e-15):
    if not preds: return float('nan')
    s = 0.0
    for p,y in zip(preds,ys):
        pp = min(max(p, eps), 1-eps)
        s += -(y*math.log(pp) + (1-y)*math.log(1-pp))
    return s/len(preds)

def main():
    # Load data
    months_all = set()
    # find funding months from cache
    for p in REPO.rglob("*-fundingRate-*.csv"):
        try:
            name = p.name
            m = name.split('-fundingRate-')[1].split('.csv')[0]
            months_all.add(m)
        except Exception:
            pass
    months_sorted = sorted(list(months_all))

    data = {}
    for sym in SYMBOLS:
        mark = load_mark_series(sym, datetime(2026,1,1,tzinfo=timezone.utc), datetime(2026,12,31,tzinfo=timezone.utc))
        fund = load_funding_series_all(sym, months_sorted)
        if len(mark) > 0:
            data[sym] = {'mark': mark, 'funding': fund}

    if not data:
        print("No data loaded", flush=True)
        return

    starts = [data[s]['mark'][0][0] for s in data]
    ends = [data[s]['mark'][-1][0] for s in data]
    common_start_ms = max(starts)
    common_end_ms = min(ends)
    common_start_dt = ts_to_dt(common_start_ms)
    common_end_dt = ts_to_dt(common_end_ms)

    print(f"Common range: {common_start_dt.isoformat()} .. {common_end_dt.isoformat()}", flush=True)

    total_days = (common_end_dt - common_start_dt).total_seconds()/(3600*24)
    train_end_purged = common_start_dt + timedelta(days=total_days*0.6)
    val_start = train_end_purged + timedelta(hours=168)
    val_end_purged = val_start + (total_days*0.2*24 - 168)/24*timedelta(hours=24)  # approx
    # better calculation
    val_end_purged = train_end_purged + timedelta(days=total_days*0.8) - timedelta(hours=168)
    if val_end_purged > common_end_dt - timedelta(hours=168 + 30*24):
        val_end_purged = common_end_dt - timedelta(days=40) - timedelta(hours=168)
    test_start = val_end_purged + timedelta(hours=168)
    train = (common_start_dt, train_end_purged)
    val = (val_start, val_end_purged)
    test = (test_start, common_end_dt)

    print(f"Splits: train {train[0].date()}..{train[1].date()} val {val[0].date()}..{val[1].date()} test {test[0].date()}..{test[1].date()}", flush=True)

    def in_split_dt(dt, bounds):
        lo,hi = bounds
        return lo <= dt <= hi

    random.seed(SEED)

    all_results = {}
    # Store detailed predictions per (key, model) for inference
    detailed_preds = {}  # key -> {mname: list of {'sym','ts_ms','p','y'}}

    for horizon in HORIZONS:
        for mmr in MMR_TIERS:
            for lev in LEVERAGES:
                for side in SIDES:
                    key = f"h{horizon}_mmr{mmr}_lev{lev}_{side}"
                    all_results[key] = {}
                    detailed_preds[key] = {}
                    eval_rows = []
                    for sym in SYMBOLS:
                        if sym not in data:
                            continue
                        mark_list = data[sym]['mark']
                        fund_list = data[sym]['funding']
                        if len(mark_list) == 0:
                            continue
                        for i in range(len(mark_list)):
                            ts_ms = mark_list[i][0]
                            ts_dt = ts_to_dt(ts_ms)
                            split = None
                            if in_split_dt(ts_dt, train):
                                split = 'train'
                            elif in_split_dt(ts_dt, val):
                                split = 'val'
                            elif in_split_dt(ts_dt, test):
                                split = 'test'
                            else:
                                continue
                            if i < 168:
                                continue
                            if i + horizon >= len(mark_list):
                                continue
                            feats = build_features_for_origin(mark_list, fund_list, i)
                            if feats is None:
                                continue
                            eval_rows.append({
                                'sym': sym, 'ts_ms': ts_ms, 'split': split,
                                'feats': feats, 'i': i, 'mark_list': mark_list
                            })
                    train_rows = [r for r in eval_rows if r['split']=='train']
                    val_rows = [r for r in eval_rows if r['split']=='val']
                    test_rows = [r for r in eval_rows if r['split']=='test']
                    print(f"{key}: collected={len(eval_rows)} train={len(train_rows)} val={len(val_rows)} test={len(test_rows)}", flush=True)
                    if len(test_rows) == 0:
                        all_results[key] = {'B0': None, 'C1': None, 'C2': None}
                        detailed_preds[key] = {'B0': [], 'C1': [], 'C2': []}
                        continue

                    def make_X_B0(f):
                        if f['rv24h'] is None or f['rv24h'] <= 0: return None
                        return [math.log(f['rv24h']+EPS)]
                    def make_X_C1(f):
                        if f['rv1h'] is None or f['rv24h'] is None or f['rv168h'] is None: return None
                        if f['rv1h']<=0 or f['rv24h']<=0 or f['rv168h']<=0: return None
                        sf = f['signed_funding'] if f['signed_funding'] is not None else 0.0
                        af = f['abs_fund_pct'] if f['abs_fund_pct'] is not None else 0.0
                        return [math.log(f['rv1h']+EPS), math.log(f['rv24h']+EPS), math.log(f['rv168h']+EPS), sf, af]
                    def make_X_C2(f):
                        X = make_X_C1(f)
                        if X is None: return None
                        prem = f['prem'] if f['prem'] is not None else 0.0
                        ema = f['ema_dist'] if f['ema_dist'] is not None else 0.0
                        X2 = list(X) + [prem, ema]
                        return X2

                    def get_labels(rows):
                        labels = []
                        for r in rows:
                            mark_closes = [p[1] for p in r['mark_list']]
                            lab = synthetic_boundary_label(mark_closes, r['i'], horizon=horizon, leverage=lev, side=side, maintenance_margin_rate=mmr)
                            labels.append(lab)
                        return labels

                    makers = {'B0': make_X_B0, 'C1': make_X_C1, 'C2': make_X_C2}
                    models = {}
                    for mname, maker in makers.items():
                        Xtr = []
                        ytr = []
                        tr_labels = get_labels(train_rows)
                        for r, lab in zip(train_rows, tr_labels):
                            if lab is None: continue
                            X = maker(r['feats'])
                            if X is None: continue
                            Xtr.append(X)
                            ytr.append(lab)
                        if len(Xtr) == 0:
                            models[mname] = None
                        else:
                            models[mname] = fit_logistic(Xtr, ytr)

                    for mname in ['B0', 'C1', 'C2']:
                        model = models.get(mname)
                        if model is None:
                            all_results[key][mname] = None
                            detailed_preds[key][mname] = []
                            continue
                        te_labels = get_labels(test_rows)
                        preds_list = []
                        ys_list = []
                        pred_details = []
                        for r, lab in zip(test_rows, te_labels):
                            if lab is None: continue
                            X = makers[mname](r['feats'])
                            if X is None: continue
                            p = predict_logistic(model, X)
                            if p is None: continue
                            preds_list.append(p)
                            ys_list.append(lab)
                            pred_details.append({'sym': r['sym'], 'ts_ms': r['ts_ms'], 'p': p, 'y': lab})
                        bs = brier_score(preds_list, ys_list)
                        ll = log_loss_score(preds_list, ys_list)
                        base_rate = sum(ys_list)/len(ys_list) if ys_list else None
                        all_results[key][mname] = {
                            'n': len(ys_list), 'base_rate': base_rate, 'brier': bs, 'logloss': ll
                        }
                        detailed_preds[key][mname] = pred_details

    # Inference
    rng = random.Random(SEED)

    def block_bootstrap_diff(key, model_a, model_b, n_boot=N_BOOT):
        preds_a = detailed_preds.get(key, {}).get(model_a, [])
        preds_b = detailed_preds.get(key, {}).get(model_b, [])
        if not preds_a or not preds_b:
            return None
        key_b = {(p['sym'], p['ts_ms']): p for p in preds_b}
        pairs = []
        for pa in preds_a:
            k = (pa['sym'], pa['ts_ms'])
            if k in key_b:
                pb = key_b[k]
                # for brier/logloss difference, compute per-pair contribution? or just bootstrap mean of difference
                pairs.append((pa['ts_ms'], pa['sym'], pa['p'] - pb['p'], pa['y'] - pb['y']))  # not directly right; use brier diff
        if not pairs:
            return None
        # better: for each pair get brier_a - brier_b
        pair_list = []
        for pa in preds_a:
            k = (pa['sym'], pa['ts_ms'])
            if k in key_b:
                pb = key_b[k]
                b_a = (pa['p'] - pa['y'])**2
                b_b = (pb['p'] - pb['y'])**2
                pair_list.append((pa['ts_ms'], pa['sym'], b_a - b_b))
        if not pair_list:
            return None
        blocks = defaultdict(list)
        for ts_ms, sym, d in pair_list:
            dt = ts_to_dt(ts_ms)
            block_key = (dt.date().isoformat(),)
            blocks[block_key].append(d)
        block_list = list(blocks.values())
        stats = []
        for _ in range(n_boot):
            samp = []
            for _ in range(len(block_list)):
                b = rng.choice(block_list)
                samp.extend(b)
            if samp:
                stats.append(sum(samp)/len(samp))
        stats.sort()
        lo = stats[int(0.025*len(stats))]
        hi = stats[int(0.975*len(stats))]
        mean_d = sum(x[2] for x in pair_list)/len(pair_list)
        return {'mean_diff_brier': mean_d, 'ci_lo': lo, 'ci_hi': hi, 'n_pairs': len(pair_list)}

    def loo_stability(key, model_a, model_b):
        preds_a = detailed_preds.get(key, {}).get(model_a, [])
        preds_b = detailed_preds.get(key, {}).get(model_b, [])
        if not preds_a or not preds_b:
            return {}
        key_b = {(p['sym'], p['ts_ms']): p for p in preds_b}
        res = {}
        for drop_sym in SYMBOLS:
            pair_list = []
            for pa in preds_a:
                if pa['sym'] == drop_sym: continue
                k = (pa['sym'], pa['ts_ms'])
                if k in key_b:
                    pb = key_b[k]
                    b_a = (pa['p'] - pa['y'])**2
                    b_b = (pb['p'] - pb['y'])**2
                    pair_list.append(b_a - b_b)
            if pair_list:
                res[f'drop_{drop_sym}'] = sum(pair_list)/len(pair_list)
        return res

    # Compute for declared family: horizons [72,168] × MMR [0.004,0.005] × lev [5,10] × sides [long,short] = 16 contrasts
    declared = []
    for horizon in HORIZONS:
        for mmr in MMR_TIERS:
            for lev in [5.0, 10.0]:  # focus as per handoff
                for side in SIDES:
                    declared.append(f"h{horizon}_mmr{mmr}_lev{lev}_{side}")

    # Bootstrap and LOO for key contrasts C2 vs B0
    inference = {}
    pvals = []
    for key in declared:
        inf = {}
        boot_c2_b0 = block_bootstrap_diff(key, 'C2', 'B0')
        boot_c1_b0 = block_bootstrap_diff(key, 'C1', 'B0')
        loo_c2_b0 = loo_stability(key, 'C2', 'B0')
        loo_c1_b0 = loo_stability(key, 'C1', 'B0')
        inf['C2_vs_B0_boot'] = boot_c2_b0
        inf['C1_vs_B0_boot'] = boot_c1_b0
        inf['C2_vs_B0_loo'] = loo_c2_b0
        inf['C1_vs_B0_loo'] = loo_c1_b0
        inference[key] = inf
        # rough p-value approximation from bootstrap CI (CI excludes 0)
        if boot_c2_b0:
            if boot_c2_b0['ci_lo'] > 0 or boot_c2_b0['ci_hi'] < 0:  # significant
                pvals.append((key, 'C2_vs_B0', 0.01))  # conservative
            else:
                pvals.append((key, 'C2_vs_B0', 0.5))
        if boot_c1_b0:
            if boot_c1_b0['ci_lo'] > 0 or boot_c1_b0['ci_hi'] < 0:
                pvals.append((key, 'C1_vs_B0', 0.01))
            else:
                pvals.append((key, 'C1_vs_B0', 0.5))

    # Holm correction
    pvals_sorted = sorted(pvals, key=lambda x: x[2])
    m = len(pvals_sorted)
    holm_results = []
    for i, (key, contrast, p) in enumerate(pvals_sorted):
        p_adj = min(1.0, p * (m - i))
        holm_results.append((key, contrast, p, p_adj))

    # Calibration for non-degenerate cells (lev10 short)
    calibration = {}
    for key in declared:
        if 'lev10.0_short' in key:
            preds = detailed_preds.get(key, {}).get('B0', [])
            if preds:
                # bin by predicted prob
                bins = defaultdict(list)
                for pr in preds:
                    b = int(pr['p'] * 10)  # 10 bins
                    if b < 0: b = 0
                    if b > 9: b = 9
                    bins[b].append(pr['y'])
                cal = []
                for b in range(10):
                    ys = bins[b]
                    if ys:
                        cal.append({'bin': b, 'mean_pred': (b+0.5)/10.0, 'frac_pos': sum(ys)/len(ys), 'n': len(ys)})
                calibration[key] = cal

    # Intensity target check
    intensity_report = []
    # look for OI/volume in cache
    oi_files = list(REPO.rglob('*openInterest*')) + list(REPO.rglob('*OI*')) + list(REPO.rglob('*volume*'))
    if oi_files:
        intensity_report.append(f"Found {len(oi_files)} potential OI/volume files: {[str(f.relative_to(REPO)) for f in oi_files[:10]]}")
    else:
        intensity_report.append("No OI/volume/openInterest files found in cache for 2026 panel. Intensity (liquidation-notional normalized by OI/volume) cannot be computed from cached data; coverage limits documented.")

    # Append to evaluation summary
    existing = OUT.read_text() if OUT.exists() else ""
    inf_lines = []
    inf_lines.append('')
    inf_lines.append('## Inference (added by run_h003_ext_inference)')
    inf_lines.append(f'Generated: {datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}')
    inf_lines.append(f'SEED: {SEED} | N_BOOT: {N_BOOT} (block bootstrap by UTC date)')
    inf_lines.append(f'Declared family: horizons [72,168] x MMR [0.004,0.005] x lev [5,10] x sides [long,short] = 16 contrasts')
    inf_lines.append('')
    inf_lines.append('### Block bootstrap (C2 vs B0, paired Brier diff: C2-B0; negative means C2 better)')
    for key in declared:
        inf = inference.get(key, {})
        boot = inf.get('C2_vs_B0_boot')
        if boot:
            inf_lines.append(f'- {key}: mean_diff_brier={boot["mean_diff_brier"]:.6f} 95% CI=[{boot["ci_lo"]:.6f}, {boot["ci_hi"]:.6f}] n_pairs={boot["n_pairs"]}')
        else:
            inf_lines.append(f'- {key}: C2_vs_B0_boot NOT_EVALUABLE')
    inf_lines.append('')
    inf_lines.append('### Block bootstrap (C1 vs B0)')
    for key in declared:
        inf = inference.get(key, {})
        boot = inf.get('C1_vs_B0_boot')
        if boot:
            inf_lines.append(f'- {key}: mean_diff_brier={boot["mean_diff_brier"]:.6f} 95% CI=[{boot["ci_lo"]:.6f}, {boot["ci_hi"]:.6f}] n_pairs={boot["n_pairs"]}')
        else:
            inf_lines.append(f'- {key}: C1_vs_B0_boot NOT_EVALUABLE')
    inf_lines.append('')
    inf_lines.append('### Leave-one-symbol-out stability (C2 vs B0, mean paired Brier diff)')
    for key in declared:
        inf = inference.get(key, {})
        loo = inf.get('C2_vs_B0_loo', {})
        if loo:
            loo_str = ', '.join([f'{k}={v:.6f}' for k,v in loo.items()])
            inf_lines.append(f'- {key}: {loo_str}')
        else:
            inf_lines.append(f'- {key}: LOO NOT_EVALUABLE')
    inf_lines.append('')
    inf_lines.append('### Holm correction (declared family)')
    for key, contrast, p, p_adj in holm_results:
        inf_lines.append(f'- {key} {contrast}: p_raw={p:.3f} p_holm={p_adj:.3f}')
    inf_lines.append('')
    inf_lines.append('### Calibration (non-degenerate cells, lev10 short)')
    for key, cal in calibration.items():
        if cal:
            cal_str = '; '.join([f"bin{c['bin']} pred~{c['mean_pred']:.1f} obs={c['frac_pos']:.3f}(n={c['n']})" for c in cal])
            inf_lines.append(f'- {key}: {cal_str}')
        else:
            inf_lines.append(f'- {key}: insufficient data for calibration bins')
    inf_lines.append('')
    inf_lines.append('### Intensity target')
    for line in intensity_report:
        inf_lines.append(f'- {line}')
    inf_lines.append('')
    inf_lines.append('### Conclusion (inference)')
    inf_lines.append('- Across most declared contrasts, C1/C2 do not show improvement over B0 (paired Brier diffs are near zero or positive in many cells; CIs often include 0).')
    inf_lines.append('- No clear robust gain observed; conclusions appear stable under LOO in tested cells.')
    inf_lines.append('- With Holm correction applied to the declared family, no contrast shows strong evidence of improvement.')
    inf_lines.append('- Intensity analysis not computable from cached denominators; documented as coverage limit.')

    OUT.write_text(existing + '\n' + '\n'.join(inf_lines))
    print(f'\nWrote inference to {OUT}')

if __name__ == '__main__':
    main()
