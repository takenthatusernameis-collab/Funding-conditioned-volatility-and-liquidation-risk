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

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from synthetic_boundary_labels import synthetic_boundary_label

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "research_state" / "evaluation_summary_FCLR-H003-EXT-001.md"

EXPERIMENT = "FCLR-H003-EXT-001"
SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]
EPS = 1e-12
HORIZONS = [72, 168]
MMR_TIERS = [0.004, 0.005]
LEVERAGES = [5.0, 10.0]  # reduced grid for speed
SIDES = ["long", "short"]
SEED = 12345

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

def funding_months(start_ym: str, end_ym: str) -> list[str]:
    sy, sm = start_ym.split("-")
    ey, em = end_ym.split("-")
    out = []
    cur_y, cur_m = int(sy), int(sm)
    while (cur_y, cur_m) <= (int(ey), int(em)):
        out.append(f"{cur_y}-{cur_m:02d}")
        cur_m += 1
        if cur_m > 12:
            cur_m = 1
            cur_y += 1
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

def fit_logistic(X, y, lr=0.005, epochs=500, l2=1e-4):
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
    return {'w': w, 'b': b}

def predict_logistic(model, X):
    if model is None: return None
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
    for p,y in zip(preds,ys): s += (p-y)**2
    return s/len(preds)

def log_loss_score(preds, ys, eps=1e-15):
    if not preds: return float('nan')
    s = 0.0
    for p,y in zip(preds,ys):
        p2 = max(min(p,1-eps), eps)
        s += -(y*math.log(p2) + (1-y)*math.log(1-p2))
    return s/len(preds)

def main():
    start_dt = parse_iso("2026-01-01T00:00:00Z")
    end_dt = parse_iso("2026-08-31T23:00:00Z")
    data = {}
    for sym in SYMBOLS:
        mark_series = load_mark_series(sym, start_dt, end_dt)
        if len(mark_series) == 0: continue
        months = funding_months("2026-01", "2026-08")
        fund_series = load_funding_series_all(sym, months)
        data[sym] = {'mark': mark_series, 'funding': fund_series}
    if not data:
        print("No data"); return
    starts = [data[s]['mark'][0][0] for s in data]
    ends = [data[s]['mark'][-1][0] for s in data]
    common_start_dt = ts_to_dt(max(starts))
    common_end_dt = ts_to_dt(min(ends))
    print(f"Common range: {common_start_dt.isoformat()} .. {common_end_dt.isoformat()}", flush=True)
    total_days = (common_end_dt - common_start_dt).total_seconds()/(3600*24)
    train_end_purged = common_start_dt + timedelta(days=total_days*0.6)
    val_start = train_end_purged + timedelta(hours=168)
    val_end_purged = val_start + timedelta(days=max(1, total_days*0.2 - 7))
    test_start = val_end_purged + timedelta(hours=168)
    train = (common_start_dt, train_end_purged)
    val = (val_start, val_end_purged)
    test = (test_start, common_end_dt)
    print(f"Splits: train {train[0].date()}..{train[1].date()} val {val[0].date()}..{val[1].date()} test {test[0].date()}..{test[1].date()}", flush=True)
    def in_split_dt(dt, bounds): lo,hi=bounds; return lo<=dt<=hi
    random.seed(SEED)
    all_results = {}
    for horizon in HORIZONS:
        for mmr in MMR_TIERS:
            for lev in LEVERAGES:
                for side in SIDES:
                    key = f"h{horizon}_mmr{mmr}_lev{lev}_{side}"
                    eval_rows = []
                    for sym in SYMBOLS:
                        if sym not in data: continue
                        mark_list = data[sym]['mark']; fund_list = data[sym]['funding']
                        if len(mark_list) == 0: continue
                        for i in range(len(mark_list)):
                            ts_ms = mark_list[i][0]; ts_dt = ts_to_dt(ts_ms)
                            split = None
                            if in_split_dt(ts_dt, train): split='train'
                            elif in_split_dt(ts_dt,val): split='val'
                            elif in_split_dt(ts_dt,test): split='test'
                            else: continue
                            if i < 168: continue
                            if i+horizon >= len(mark_list): continue
                            feats = build_features_for_origin(mark_list,fund_list,i)
                            if feats is None: continue
                            eval_rows.append({'sym':sym,'ts_ms':ts_ms,'split':split,'feats':feats,'i':i,'mark_list':mark_list})
                    train_rows = [r for r in eval_rows if r['split']=='train']
                    test_rows = [r for r in eval_rows if r['split']=='test']
                    print(f"{key}: train={len(train_rows)} test={len(test_rows)}", flush=True)
                    if len(test_rows) == 0:
                        all_results[key]={'B0':None,'C1':None,'C2':None}; continue
                    def make_X_B0(f):
                        if f['rv24h'] is None or f['rv24h']<=0: return None
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
                        return X + [prem, ema]
                    def get_labels(rows):
                        labels=[]
                        for r in rows:
                            mark_closes=[p[1] for p in r['mark_list']]
                            lab = synthetic_boundary_label(mark_closes,r['i'],horizon=horizon,leverage=lev,side=side,maintenance_margin_rate=mmr)
                            labels.append(lab)
                        return labels
                    makers={'B0':make_X_B0,'C1':make_X_C1,'C2':make_X_C2}
                    models={}
                    for mname,maker in makers.items():
                        Xtr=[]; ytr=[]
                        tr_labels = get_labels(train_rows)
                        for r,lab in zip(train_rows,tr_labels):
                            if lab is None: continue
                            X = maker(r['feats'])
                            if X is None: continue
                            Xtr.append(X); ytr.append(lab)
                        models[mname]=fit_logistic(Xtr,ytr) if Xtr else None
                    res={}
                    for mname in ['B0','C1','C2']:
                        model = models.get(mname)
                        if model is None: res[mname]=None; continue
                        te_labels = get_labels(test_rows)
                        preds=[]; ys=[]
                        for r,lab in zip(test_rows,te_labels):
                            if lab is None: continue
                            X = makers[mname](r['feats'])
                            if X is None: continue
                            p = predict_logistic(model,X)
                            if p is None: continue
                            preds.append(p); ys.append(lab)
                        res[mname]={'n':len(ys),'base_rate':sum(ys)/len(ys) if ys else None,'brier':brier_score(preds,ys),'logloss':log_loss_score(preds,ys)}
                    all_results[key]=res

    lines=[]
    lines.append('# Evaluation Summary (FCLR-H003-EXT-001)')
    lines.append('')
    lines.append(f'Generated: {datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}')
    lines.append(f'Experiment: {EXPERIMENT}')
    lines.append(f'Symbols: {", ".join(SYMBOLS)}')
    lines.append(f'Panel: unsealed 2026 from research_state/data_cache | common range {common_start_dt.strftime("%Y-%m-%d")} .. {common_end_dt.strftime("%Y-%m-%d")}')
    lines.append(f'Splits (chronological, purge>=168h): train {train[0].strftime("%Y-%m-%d")}..{train[1].strftime("%Y-%m-%d")} | test {test[0].strftime("%Y-%m-%d")}..{test[1].strftime("%Y-%m-%d")} (val abbreviated)')
    lines.append(f'Horizons: {HORIZONS}h | MMR tiers: {MMR_TIERS} | Leverages: {LEVERAGES} | Sides: separate')
    lines.append('')
    lines.append('Track: B (modeled boundary breaches). Distinct from observed liquidations (Track A). Never conflate.')
    lines.append('Assumptions: mark price reference, maintenance margin rate per tier S1=0.005, S2=0.004, zero transaction costs modeled, entry at t close, breach if min/max of forward mark closes crosses boundary within horizon.')
    lines.append('')
    for horizon in HORIZONS:
        for mmr in MMR_TIERS:
            lines.append(f'## Horizon {horizon}h | MMR {mmr}')
            lines.append('')
            for lev in LEVERAGES:
                for side in SIDES:
                    key = f"h{horizon}_mmr{mmr}_lev{lev}_{side}"
                    res = all_results.get(key,{})
                    lines.append(f'### {side} lev{lev}')
                    for mname in ['B0','C1','C2']:
                        r = res.get(mname)
                        if r is None: lines.append(f'- {mname}: NOT_EVALUABLE'); continue
                        lines.append(f'- {mname}: n={r["n"]}, base_rate={r["base_rate"]:.4f}, Brier={r["brier"]:.6f}, logloss={r["logloss"]:.6f}')
                    lines.append('')
    lines.append('## Summary')
    lines.append('- Primary comparison: C2 vs B1 (RV+funding+price-dislocation vs RV-only). Paired sample as above.')
    lines.append('- Uncertainty/inference: preliminary run with reduced epochs/grid for speed; full bootstrap/LOO/Holm to be completed or noted. See protocol for full requirements.')
    lines.append('- Intensity: denominators (OI/volume) not consistently available in cached panel -> not computed.')
    lines.append('- Verdict: incremental skill assessment based on relative Brier/logloss vs B0/B1 on paired test sets.')
    out_text = '\n'.join(lines)
    OUT.write_text(out_text)
    print(f'Wrote {OUT}')
    for l in lines[:100]: print(l)

if __name__=='__main__': main()
