#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import math
import random
from datetime import datetime, timezone, timedelta
from pathlib import Path

import os
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from synthetic_boundary_labels import synthetic_boundary_label

REPO = Path(__file__).resolve().parents[1]
RUN_MANIFEST = REPO / "research_state" / "run_manifest.json"
OUT = REPO / "research_state" / "evaluation_summary_h003.md"

# Experiment selection via env var: "FCLR-001" (default, frozen window ending
# 2024-03-31, BTCUSDT-only 4-day test block) or "FCLR-002" (extended 5-symbol
# panel 2024-04-01..2024-09-30 per frozen protocol). Default preserves the
# existing recorded FCLR-H003 artifact exactly.
EXPERIMENT = os.environ.get("H003_EXPERIMENT", "FCLR-001")
if EXPERIMENT == "FCLR-002":
    DATA_END = "2024-09-30"
    OUT = REPO / "research_state" / "evaluation_summary_h003_FCLR002.md"
else:
    DATA_END = "2024-03-31"

SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]
EPS = 1e-12
HORIZON = 24
MMR = 0.005
LEVERAGES = [3.0, 5.0, 10.0, 20.0]
SIDES = ["long", "short"]

def ts_to_dt(ts_ms):
    return datetime.fromtimestamp(ts_ms / 1000, tz=timezone.utc)

def parse_iso(s):
    if s.endswith('Z'):
        s2 = s[:-1] + '+00:00'
    else:
        s2 = s
    dt = datetime.fromisoformat(s2)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt

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

def funding_months(end_ym: str) -> list[str]:
    """All YYYY-MM months from 2024-01 through end_ym inclusive."""
    y, m = end_ym[:7].split("-")
    out = []
    cur_y, cur_m = 2024, 1
    while (cur_y, cur_m) < (int(y), int(m)):
        out.append(f"{cur_y}-{cur_m:02d}")
        cur_m += 1
        if cur_m > 12:
            cur_m = 1
            cur_y += 1
    out.append(f"{cur_y}-{cur_m:02d}")
    return out

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
    if t_idx < 0:
        ema_dist = None
    else:
        ema = mark_list[0][1]
        alpha = 2.0/(24+1)
        for i in range(1, t_idx+1):
            ema = alpha * mark_list[i][1] + (1-alpha) * ema
        ema_dist = mark_list[t_idx][1] / ema - 1.0 if ema > 0 else None
    return {
        'ts_ms': ts_ms_t,
        'rv1h': rv1h, 'rv24h': rv24h, 'rv168h': rv168h,
        'signed_funding': signed_funding,
        'abs_fund_pct': abs_fund_pct,
        'ema_dist': ema_dist,
        'prem': 0.0
    }

def fit_logistic(X_list, y_list, max_iter=1000, lr=0.01):
    rows = []
    for X,y in zip(X_list, y_list):
        if y is None:
            continue
        rows.append((X, int(y)))
    if len(rows) < 20:
        return None
    n = len(rows)
    p = len(rows[0][0]) + 1
    w = [0.0] * p
    for it in range(max_iter):
        grad = [0.0] * p
        for X,y in rows:
            z = w[0]
            for i in range(len(X)):
                z += w[i+1] * X[i]
            if z > 20: z = 20
            if z < -20: z = -20
            pred = 1.0 / (1.0 + math.exp(-z))
            diff = pred - y
            grad[0] += diff
            for i in range(len(X)):
                grad[i+1] += diff * X[i]
        for i in range(p):
            w[i] -= lr * grad[i] / n
    return w

def predict_logistic(w, X):
    if w is None or X is None:
        return None
    z = w[0]
    for i in range(len(X)):
        z += w[i+1] * X[i]
    if z > 20: z = 20
    if z < -20: z = -20
    pred = 1.0 / (1.0 + math.exp(-z))
    return pred

def brier_score(preds, ys):
    if not preds: return None
    bs = 0.0; n = 0
    for p,y in zip(preds,ys):
        if p is None: continue
        bs += (p-y)**2; n += 1
    return bs/n if n>0 else None

def log_loss_score(preds, ys, eps=1e-12):
    if not preds: return None
    ll = 0.0; n = 0
    for p,y in zip(preds,ys):
        if p is None: continue
        p_c = min(max(p, eps), 1-eps)
        ll += -(y*math.log(p_c) + (1-y)*math.log(1-p_c)); n += 1
    return ll/n if n>0 else None

def calibration_bins(preds, ys, n_bins=10):
    bins = [[] for _ in range(n_bins)]
    for p,y in zip(preds,ys):
        if p is None: continue
        b = min(int(p*n_bins), n_bins-1)
        bins[b].append((p,y))
    out = []
    for b in bins:
        if not b:
            out.append(None)
            continue
        mean_p = sum(x[0] for x in b)/len(b)
        mean_y = sum(x[1] for x in b)/len(b)
        out.append((mean_p, mean_y, len(b)))
    return out

def precision_recall(preds, ys, thresholds=None):
    if thresholds is None:
        thresholds = [i/100.0 for i in range(0,101)]
    out = []
    for th in thresholds:
        tp=fp=tn=fn=0
        for p,y in zip(preds,ys):
            if p is None: continue
            pred_label = 1 if p>=th else 0
            if pred_label==1 and y==1: tp+=1
            elif pred_label==1 and y==0: fp+=1
            elif pred_label==0 and y==0: tn+=1
            elif pred_label==0 and y==1: fn+=1
        prec = tp/(tp+fp) if (tp+fp)>0 else 0.0
        rec = tp/(tp+fn) if (tp+fn)>0 else 0.0
        if prec+rec>0:
            f1 = 2*prec*rec/(prec+rec)
        else:
            f1 = 0.0
        out.append((th, prec, rec, f1, tp,fp,tn,fn))
    if out:
        best = max(out, key=lambda x:x[3])
    else:
        best = None
    out_sorted = sorted(out, key=lambda x:x[2])
    auprc = 0.0
    for i in range(1, len(out_sorted)):
        auprc += (out_sorted[i][2]-out_sorted[i-1][2])*(out_sorted[i][1]+out_sorted[i-1][1])/2.0
    return {'best_f1': best, 'auprc': auprc}

def main():
    m = json.loads(RUN_MANIFEST.read_text())
    splits = m['split_boundaries']
    train = (parse_iso(splits['train']['start']), parse_iso(splits['train']['end']))
    val = (parse_iso(splits['validation']['start']), parse_iso(splits['validation']['end']))
    test = (parse_iso(splits['test']['start']), parse_iso(splits['test']['end']))

    months = funding_months(DATA_END)
    data = {}
    for sym in SYMBOLS:
        data[sym] = {
            'mark': load_mark_series(sym, parse_iso("2024-01-01T00:00:00Z"), parse_iso(f"{DATA_END}T23:00:00Z")),
            'funding': load_funding_series_all(sym, months)
        }

    def in_split_dt(dt, bounds):
        lo,hi = bounds
        return lo <= dt <= hi

    eval_rows = []
    for sym in SYMBOLS:
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
            if i + HORIZON >= len(mark_list):
                continue
            feats = build_features_for_origin(mark_list, fund_list, i)
            if feats is None:
                continue
            eval_rows.append({
                'sym': sym,
                'ts_ms': ts_ms,
                'split': split,
                'feats': feats,
                'i': i,
                'mark_list': mark_list
            })

    print(f"Collected {len(eval_rows)} rows", flush=True)
    train_rows = [r for r in eval_rows if r['split']=='train']
    val_rows = [r for r in eval_rows if r['split']=='val']
    test_rows = [r for r in eval_rows if r['split']=='test']
    print(f"Splits: train={len(train_rows)} val={len(val_rows)} test={len(test_rows)}", flush=True)

    def make_X_B0(f):
        if f['rv24h'] is None or f['rv24h'] <= 0: return None
        return [math.log(f['rv24h']+EPS)]
    def make_X_C2(f):
        if f['rv1h'] is None or f['rv24h'] is None or f['rv168h'] is None: return None
        if f['rv1h']<=0 or f['rv24h']<=0 or f['rv168h']<=0: return None
        sf = f['signed_funding'] if f['signed_funding'] is not None else 0.0
        af = f['abs_fund_pct'] if f['abs_fund_pct'] is not None else 0.0
        prem = f['prem'] if f['prem'] is not None else 0.0
        ema = f['ema_dist'] if f['ema_dist'] is not None else 0.0
        return [math.log(f['rv1h']+EPS), math.log(f['rv24h']+EPS), math.log(f['rv168h']+EPS), sf, af, prem, ema]

    all_results = {}
    for lev in LEVERAGES:
        for side in SIDES:
            key = f"lev{lev}_{side}"
            all_results[key] = {}
            def get_labels(rows, levl=lev, sidl=side):
                labels = []
                for r in rows:
                    mark_list = r['mark_list']
                    mark_closes = [p[1] for p in mark_list]
                    lab = synthetic_boundary_label(mark_closes, r['i'], horizon=HORIZON, leverage=levl, side=sidl, maintenance_margin_rate=MMR)
                    labels.append(lab)
                return labels
            models = {}
            for mname, maker in [('B0', make_X_B0), ('C2', make_X_C2)]:
                Xtr = []
                ytr = []
                tr_labels = get_labels(train_rows)
                for r, lab in zip(train_rows, tr_labels):
                    if lab is None: continue
                    X = maker(r['feats'])
                    if X is None: continue
                    Xtr.append(X)
                    ytr.append(lab)
                w = fit_logistic(Xtr, ytr)
                models[mname] = {'w': w, 'maker': maker}
            for mname in ['B0', 'C2']:
                model = models[mname]
                w = model['w']
                if w is None:
                    all_results[key][mname] = None
                    continue
                te_labels = get_labels(test_rows)
                preds = []
                ys = []
                for r, lab in zip(test_rows, te_labels):
                    if lab is None: continue
                    X = model['maker'](r['feats'])
                    if X is None: continue
                    p = predict_logistic(w, X)
                    if p is None: continue
                    preds.append(p)
                    ys.append(lab)
                bs = brier_score(preds, ys)
                ll = log_loss_score(preds, ys)
                cal = calibration_bins(preds, ys)
                pr = precision_recall(preds, ys)
                base_rate = sum(ys)/len(ys) if ys else None
                all_results[key][mname] = {
                    'n': len(ys),
                    'base_rate': base_rate,
                    'brier': bs,
                    'logloss': ll,
                    'calibration': cal,
                    'pr': pr
                }

    lines = []
    lines.append('# Evaluation Summary (FCLR-H003)')
    lines.append('')
    lines.append(f'Generated: {datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}')
    lines.append(f'Experiment: {EXPERIMENT}')
    lines.append(f'Horizon: {HORIZON}h | MMR: {MMR} | Leverages: {LEVERAGES} | Sides: {SIDES} (separate)')
    lines.append(f'Panel: {EXPERIMENT} test block {test[0].strftime("%Y-%m-%dT%H:%M:%SZ")} .. {test[1].strftime("%Y-%m-%dT%H:%M:%SZ")}')
    lines.append('')
    lines.append('Notes: Labels are synthetic modeled boundary breaches (not observed liquidations). Long/short evaluated separately. Assumptions: maintenance margin rate 0.005, zero-cost boundary, mark close at decision time as entry, horizon 24h forward mark closes.')
    lines.append('')
    for lev in LEVERAGES:
        for side in SIDES:
            key = f"lev{lev}_{side}"
            lines.append(f'## {key}')
            lines.append('')
            for mname in ['B0', 'C2']:
                res = all_results[key].get(mname)
                if res is None:
                    lines.append(f'- {mname}: NOT_EVALUABLE')
                    continue
                lines.append(f'- {mname}: n={res["n"]}, base_rate={res["base_rate"]:.4f}, Brier={res["brier"]:.6f}, log-loss={res["logloss"]:.6f}, AUPRC={res["pr"]["auprc"]:.6f}')
                if res["pr"]["best_f1"]:
                    bf = res["pr"]["best_f1"]
                    lines.append(f'  best F1 @ thresh {bf[0]:.2f}: prec={bf[1]:.3f} rec={bf[2]:.3f} (TP={bf[4]} FP={bf[5]} TN={bf[6]} FN={bf[7]})')
            lines.append('')
    OUT.write_text('\n'.join(lines))
    print(f'Wrote {OUT}')
    for l in lines[:60]:
        print(l)

if __name__ == '__main__':
    main()
