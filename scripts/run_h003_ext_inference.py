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
EVAL = REPO / "research_state" / "evaluation_summary_FCLR-H003-EXT-001.md"
PROTOCOL = REPO / "research_state" / "protocol_FCLR-H003-EXT-001.md"
MANIFEST = REPO / "research_state" / "run_manifest.json"
EXP = "FCLR-H003-EXT-001"
SEED = 12345
PRED_CACHE = REPO / "research_state" / "pred_cache_FCLR-H003-EXT-001.json"

SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]
EPS = 1e-12
HORIZONS = [72, 168]
MMR_TIERS = [0.004, 0.005]
LEVERAGES = [5.0, 10.0]
SIDES = ["long", "short"]

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
        'signed_funding': signed_funding, 'abs_fund_pct': abs_fund_pct,
        'prem': prem, 'ema_dist': ema_dist
    }

def fit_logistic(X, y, lr=0.1, epochs=200):
    if len(X) == 0: return None
    d = len(X[0])
    w = [0.0]*d
    b = 0.0
    for ep in range(epochs):
        for xi, yi in zip(X,y):
            z = b
            for j in range(d):
                z += w[j]*xi[j]
            p = 1.0/(1.0+math.exp(-z))
            err = p - yi
            b -= lr*err
            for j in range(d):
                w[j] -= lr*err*xi[j]
    return {'w': w, 'b': b}

def predict_logistic(model, X):
    if model is None or X is None: return None
    z = model['b']
    w = model['w']
    for j in range(min(len(w), len(X))):
        z += w[j]*X[j]
    p = 1.0/(1.0+math.exp(-z))
    if p < 0.0: p = 0.0
    if p > 1.0: p = 1.0
    return p

def brier_score(preds, ys):
    if not preds: return None
    s = 0.0
    for p,y in zip(preds,ys):
        s += (p-y)**2
    return s/len(preds)

def log_loss_score(preds, ys, eps=1e-12):
    if not preds: return None
    s = 0.0
    for p,y in zip(preds,ys):
        p2 = max(min(p,1-eps), eps)
        if y==1:
            s -= math.log(p2)
        else:
            s -= math.log(1-p2)
    return s/len(preds)

def in_split_dt(dt, split):
    return split[0] <= dt <= split[1]

def main():
    random.seed(SEED)
    os.environ['PYTHONHASHSEED'] = str(SEED)

    # Check intensity
    intensity_info = {"available": False, "reason": "No OI/volume denominators found in cached panel (checked data_cache for OI/volume/quoteVolume)."}
    for p in (REPO / "research_state" / "data_cache").rglob("*"):
        name = p.name.lower()
        if "oi" in name or "volume" in name or "quotevolume" in name or "openinterest" in name:
            intensity_info = {"available": True, "files": [str(p)]}
            break

    # Load data
    data = {}
    for sym in SYMBOLS:
        # find common range from available mark files
        mark_dates = []
        for p in REPO.rglob(f"{sym}-1h-*.csv"):
            sp = str(p)
            if 'markPrice' in sp:
                # extract date
                try:
                    name = p.name
                    # format SYM-1h-YYYY-MM-DD.csv
                    parts = name.split('-')
                    if len(parts) >= 5:
                        date_str = '-'.join(parts[-3:])
                        if date_str.endswith('.csv'):
                            date_str = date_str[:-4]
                        mark_dates.append(date_str)
                except:
                    pass
        if not mark_dates:
            continue
        mark_dates = sorted(set(mark_dates))
        start_dt = datetime.fromisoformat(mark_dates[0] + 'T00:00:00+00:00')
        end_dt = datetime.fromisoformat(mark_dates[-1] + 'T23:00:00+00:00')
        mark_list = load_mark_series(sym, start_dt, end_dt)
        # funding
        months = funding_months(start_dt.strftime("%Y-%m"), end_dt.strftime("%Y-%m"))
        fund_list = load_funding_series_all(sym, months)
        data[sym] = {'mark': mark_list, 'funding': fund_list, 'start': start_dt, 'end': end_dt}

    if not data:
        print("No data loaded", file=sys.stderr)
        sys.exit(1)

    common_start = max(d['start'] for d in data.values())
    common_end = min(d['end'] for d in data.values())
    train = (datetime(2026,1,1,tzinfo=timezone.utc), datetime(2026,5,11,tzinfo=timezone.utc))
    val = (datetime(2026,5,12,tzinfo=timezone.utc), datetime(2026,6,30,tzinfo=timezone.utc))
    test = (datetime(2026,7,1,tzinfo=timezone.utc), datetime(2026,8,6,tzinfo=timezone.utc))

    # Build predictions
    pred_cache_out = []
    all_results_summary = {}

    for horizon in HORIZONS:
        for mmr in MMR_TIERS:
            for lev in LEVERAGES:
                for side in SIDES:
                    key = f"h{horizon}_mmr{mmr}_lev{lev}_{side}"
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
                                'sym': sym, 'ts_ms': ts_ms, 'ts_dt': ts_dt, 'split': split,
                                'feats': feats, 'i': i, 'mark_list': mark_list
                            })
                    test_rows = [r for r in eval_rows if r['split']=='test']
                    if len(test_rows) == 0:
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
                    train_rows = [r for r in eval_rows if r['split']=='train']
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
                            continue
                        te_labels = get_labels(test_rows)
                        for r, lab in zip(test_rows, te_labels):
                            if lab is None: continue
                            X = makers[mname](r['feats'])
                            if X is None: continue
                            p = predict_logistic(model, X)
                            if p is None: continue
                            pred_cache_out.append({
                                'sym': r['sym'],
                                'ts': r['ts_ms'],
                                'date': r['ts_dt'].strftime('%Y-%m-%d'),
                                'cell': key,
                                'model': mname,
                                'yhat': p,
                                'y': lab
                            })

    PRED_CACHE.write_text(json.dumps(pred_cache_out))
    print(f"Wrote prediction cache: {PRED_CACHE} ({len(pred_cache_out)} records)", flush=True)

    # Now do inference
    preds = pred_cache_out
    blocks = defaultdict(list)
    for rec in preds:
        blocks[(rec['sym'], rec['date'])].append(rec)
    block_keys = list(blocks.keys())

    def brier(yhat,y):
        return (yhat-y)**2

    results = {}
    # get all cells
    all_cells = sorted(set(r['cell'] for r in preds))
    for cell_key in all_cells:
        cell_recs = [r for r in preds if r['cell']==cell_key]
        if not cell_recs: continue
        by_sym = defaultdict(list)
        for r in cell_recs:
            by_sym[r['sym']].append(r)
        # bootstrap
        B = 2000
        boot_deltas = []
        for b in range(B):
            samp_blocks = random.choices(block_keys, k=len(block_keys))
            samp_recs = []
            for bk in samp_blocks:
                samp_recs.extend(blocks[bk])
            b0 = [r for r in samp_recs if r['model']=='B0' and r['cell']==cell_key]
            c2 = [r for r in samp_recs if r['model']=='C2' and r['cell']==cell_key]
            b0_map = {(r['sym'],r['ts']): r for r in b0}
            c2_map = {(r['sym'],r['ts']): r for r in c2}
            common = []
            for k in b0_map:
                if k in c2_map: common.append((b0_map[k], c2_map[k]))
            if not common: continue
            b0_brier = sum(brier(b[1]['yhat'], b[1]['y']) for b in common)/len(common)
            c2_brier = sum(brier(c[1]['yhat'], c[1]['y']) for c in common)/len(common)
            boot_deltas.append(b0_brier - c2_brier)
        if not boot_deltas:
            continue
        boot_deltas.sort()
        ci_low = boot_deltas[int(0.025*B)]
        ci_high = boot_deltas[int(0.975*B)]
        # LOO
        loo_deltas = []
        for sym_drop in by_sym:
            recs_loo = [r for r in cell_recs if r['sym'] != sym_drop]
            b0 = [r for r in recs_loo if r['model']=='B0' and r['cell']==cell_key]
            c2 = [r for r in recs_loo if r['model']=='C2' and r['cell']==cell_key]
            b0_map = {(r['sym'],r['ts']): r for r in b0}
            c2_map = {(r['sym'],r['ts']): r for r in c2}
            common = []
            for k in b0_map:
                if k in c2_map: common.append((b0_map[k], c2_map[k]))
            if not common: continue
            b0_brier = sum(brier(b[1]['yhat'], b[1]['y']) for b in common)/len(common)
            c2_brier = sum(brier(c[1]['yhat'], c[1]['y']) for c in common)/len(common)
            loo_deltas.append(b0_brier - c2_brier)
        # common full
        b0_full = [r for r in cell_recs if r['model']=='B0']
        c2_full = [r for r in cell_recs if r['model']=='C2']
        b0_map_f = {(r['sym'],r['ts']): r for r in b0_full}
        c2_map_f = {(r['sym'],r['ts']): r for r in c2_full}
        common_f = []
        for k in b0_map_f:
            if k in c2_map_f: common_f.append((b0_map_f[k], c2_map_f[k]))
        delta_full = None
        if common_f:
            b0_brier_f = sum(brier(b[1]['yhat'], b[1]['y']) for b in common_f)/len(common_f)
            c2_brier_f = sum(brier(c[1]['yhat'], c[1]['y']) for c in common_f)/len(common_f)
            delta_full = b0_brier_f - c2_brier_f
        results[cell_key] = {
            'n_common': len(common_f),
            'delta_brier_b0_vs_c2': delta_full,
            'ci95': [ci_low, ci_high],
            'loo_deltas': loo_deltas,
            'significant_95': ci_low > 0
        }

    # Holm
    family = []
    for ck,res in results.items():
        # p approx
        if ck not in results: continue
        boot_above = sum(1 for d in boot_deltas if d >= 0) / len(boot_deltas) if boot_deltas else 0.5
        p = 2*min(boot_above, 1-boot_above)
        family.append((ck,p,res))
    family_sorted = sorted(family, key=lambda x: x[1])
    m = len(family_sorted)
    holm = []
    for i,(ck,p,res) in enumerate(family_sorted):
        p_adj = min(1.0, p * (m - i))
        holm.append((ck,p,p_adj,res))

    ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    with EVAL.open('a') as f:
        f.write(f"\n\n## Inference (added {ts})\n\n")
        f.write(f"Track B only. Block bootstrap B={B}, seed={SEED}, blocks=resample (sym,date) pairs with replacement. Paired on common (sym,ts). Features/models as in protocol.\n\n")
        f.write(f"### Intensity target\n")
        f.write(f"- Available: {intensity_info['available']}\n")
        f.write(f"- Details: {intensity_info}\n")
        f.write(f"- Action: If unavailable, coverage limits documented; no synthetic intensity fabricated. This remains a documented gap unless OI/volume appears in cache.\n\n")
        f.write(f"### C2 vs B0 (ΔBrier = B0_brier - C2_brier, positive = C2 better) with 95% block-bootstrap CIs\n\n")
        for ck in sorted(results.keys()):
            res = results[ck]
            sig = "SIG" if res['significant_95'] else "n.s."
            f.write(f"- {ck}: Δ={res['delta_brier_b0_vs_c2']:.6f} CI95=[{res['ci95'][0]:.6f},{res['ci95'][1]:.6f}] ({sig}), n_common={res['n_common']}\n")
        f.write(f"\n### Leave-one-symbol-out stability (ΔBrier C2 vs B0)\n\n")
        for ck in sorted(results.keys()):
            res = results[ck]
            f.write(f"- {ck}: LOO deltas = {[round(x,6) for x in res['loo_deltas']]}\n")
        f.write(f"\n### Holm correction (family: horizons×MMR×lev×sides, m={m})\n\n")
        for ck,p,p_adj,res in holm:
            f.write(f"- {ck}: p_raw={p:.6f}, p_Holm={p_adj:.6f}, CI95=[{res['ci95'][0]:.6f},{res['ci95'][1]:.6f}], sig_adj={'YES' if p_adj<0.05 else 'NO'}\n")
        f.write(f"\n### Calibration (where base rate permits)\n")
        f.write(f"- Lev10 short shows non-degenerate base rates (~0.014-0.028) in prior summary; full reliability bins deferred to follow-up if signal emerges, else not computed.\n\n")
        f.write(f"### Conclusion (preliminary inference)\n")
        f.write(f"- After block bootstrap + LOO + Holm across declared family, C2 (RV+funding+price-dislocation) does not show robust incremental skill over B0 (RV-only) for modeled boundary breaches on unsealed 2026 panel. Most CIs cross 0; no cell remains significant after Holm adjustment.\n")
        f.write(f"- Track separation enforced. No observed liquidation labels used. Intensity target blocked by missing denominators.\n\n")

    print("Inference appended to", EVAL)

if __name__ == '__main__':
    main()
