#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import random
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
RUN_MANIFEST = REPO / "research_state" / "run_manifest.json"

EXPERIMENTS = [
    ('FCLR-002', 'split_boundaries', '2024-09-30'),
    ('FCLR-003', None, '2024-12-31'),  # no split in manifest
]

SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]
EPS = 1e-12
HORIZON = 24

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

def in_split_dt(dt, bounds):
    lo,hi = bounds
    return lo <= dt <= hi

from run_evaluation import (
    load_mark_series,
    funding_months, load_funding_series_all,
    realized_variance_from_prices, qlike, fit_ols, predict,
    build_features_for_origin
)

def block_bootstrap_diff(preds_a, preds_b, n_boot=2000, seed=12345):
    key_b = {(p['sym'], p['ts_ms']): p for p in preds_b}
    pairs = []
    for pa in preds_a:
        k = (pa['sym'], pa['ts_ms'])
        if k in key_b:
            pb = key_b[k]
            d = pa['qlike'] - pb['qlike']
            pairs.append({'d': d, 'sym': pa['sym'], 'ts_ms': pa['ts_ms']})
    if not pairs:
        return None
    from collections import defaultdict
    blocks = defaultdict(list)
    for pr in pairs:
        dt = ts_to_dt(pr['ts_ms'])
        blocks[dt.date().isoformat()].append(pr['d'])
    block_list = list(blocks.values())
    rng = random.Random(seed)
    stats = []
    for _ in range(n_boot):
        samp = []
        for _ in range(len(block_list)):
            b = rng.choice(block_list)
            samp.extend(b)
        if not samp: continue
        stats.append(sum(samp)/len(samp))
    stats.sort()
    lo = stats[int(0.025*len(stats))] if stats else None
    hi = stats[int(0.975*len(stats))] if stats else None
    mean_d = sum(p['d'] for p in pairs)/len(pairs)
    return {'mean': mean_d, 'ci_lo': lo, 'ci_hi': hi, 'n_pairs': len(pairs)}

def get_rv_ratio(f):
    if f.get('rv24h') and f.get('rv168h') and f['rv168h']>0: return f['rv24h']/f['rv168h']
    return None

def main():
    out_lines = []
    out_lines.append('# Funding-conditioned interaction analysis')
    out_lines.append(f'Generated: {datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}')
    out_lines.append('')
    m = json.loads(RUN_MANIFEST.read_text())
    for EXPERIMENT, SPLIT_KEY, DATA_END in EXPERIMENTS:
        out_lines.append(f'## {EXPERIMENT}')
        if EXPERIMENT == 'FCLR-002':
            splits = m[SPLIT_KEY]
            train = (parse_iso(splits['train']['start']), parse_iso(splits['train']['end']))
            val = (parse_iso(splits['validation']['start']), parse_iso(splits['validation']['end']))
            test = (parse_iso(splits['test']['start']), parse_iso(splits['test']['end']))
        elif EXPERIMENT == 'FCLR-003':
            # from evaluation summary
            train = (parse_iso('2024-04-01T00:00:00Z'), parse_iso('2024-07-23T23:00:00Z'))
            val = (parse_iso('2024-07-31T00:00:00Z'), parse_iso('2024-09-24T23:00:00Z'))
            test = (parse_iso('2024-10-02T00:00:00Z'), parse_iso('2024-12-31T23:00:00Z'))
        else:
            continue
        months = funding_months(DATA_END)
        data = {}
        start = parse_iso('2024-01-01T00:00:00Z')
        end = parse_iso(f'{DATA_END}T23:59:59Z')
        for sym in SYMBOLS:
            data[sym] = {
                'mark': load_mark_series(sym, start, end),
                'funding': load_funding_series_all(sym, months)
            }
        eval_rows = []
        for sym in SYMBOLS:
            mark_list = data[sym]['mark']
            fund_list = data[sym]['funding']
            for i in range(len(mark_list)):
                ts_ms = mark_list[i][0]
                ts_dt = ts_to_dt(ts_ms)
                split = None
                if in_split_dt(ts_dt, train): split = 'train'
                elif in_split_dt(ts_dt, val): split = 'val'
                elif in_split_dt(ts_dt, test): split = 'test'
                else: continue
                if i < 168: continue
                if i + HORIZON >= len(mark_list): continue
                future_prices = [mark_list[i][1]] + [mark_list[i+1+j][1] for j in range(HORIZON)]
                y = realized_variance_from_prices(future_prices)
                if y is None or y <= 0: continue
                feats = build_features_for_origin(mark_list, fund_list, i, sym=sym)
                if feats is None: continue
                eval_rows.append({'sym':sym,'ts_ms':ts_ms,'ts_dt':ts_dt,'split':split,'y':y,'feats':feats})
        train_rows = [r for r in eval_rows if r['split']=='train']
        test_rows = [r for r in eval_rows if r['split']=='test']
        def make_X_B1(rows):
            Xs,ys=[],[]
            for r in rows:
                f=r['feats']
                if f['rv1h'] is None or f['rv24h'] is None or f['rv168h'] is None: continue
                if f['rv1h']<=0 or f['rv24h']<=0 or f['rv168h']<=0: continue
                Xs.append([math.log(f['rv1h']+EPS), math.log(f['rv24h']+EPS), math.log(f['rv168h']+EPS)])
                ys.append(r['y'])
            return Xs,ys
        def make_X_I1(rows):
            Xs,ys=[],[]
            for r in rows:
                f=r['feats']
                if f['rv1h'] is None or f['rv24h'] is None or f['rv168h'] is None: continue
                if f['rv1h']<=0 or f['rv24h']<=0 or f['rv168h']<=0: continue
                sf = f['signed_funding'] if f['signed_funding'] is not None else 0.0
                Xs.append([math.log(f['rv1h']+EPS), math.log(f['rv24h']+EPS), math.log(f['rv168h']+EPS), sf*math.log(f['rv24h']+EPS)])
                ys.append(r['y'])
            return Xs,ys
        def make_X_I2(rows):
            Xs,ys=[],[]
            for r in rows:
                f=r['feats']
                if f['rv1h'] is None or f['rv24h'] is None or f['rv168h'] is None: continue
                if f['rv1h']<=0 or f['rv24h']<=0 or f['rv168h']<=0: continue
                af = f['abs_fund_pct'] if f['abs_fund_pct'] is not None else 0.0
                rr = get_rv_ratio(f) or 1.0
                Xs.append([math.log(f['rv1h']+EPS), math.log(f['rv24h']+EPS), math.log(f['rv168h']+EPS), af*rr])
                ys.append(r['y'])
            return Xs,ys
        def make_X_I3(rows):
            Xs,ys=[],[]
            for r in rows:
                f=r['feats']
                if f['rv1h'] is None or f['rv24h'] is None or f['rv168h'] is None: continue
                if f['rv1h']<=0 or f['rv24h']<=0 or f['rv168h']<=0: continue
                sf = f['signed_funding'] if f['signed_funding'] is not None else 0.0
                rr = get_rv_ratio(f) or 1.0
                Xs.append([math.log(f['rv1h']+EPS), math.log(f['rv24h']+EPS), math.log(f['rv168h']+EPS), sf*(rr-1.0)])
                ys.append(r['y'])
            return Xs,ys
        makers = {'B1':make_X_B1,'I1':make_X_I1,'I2':make_X_I2,'I3':make_X_I3}
        models = {}
        for name,maker in makers.items():
            Xtr,ytr = maker(train_rows)
            if not Xtr:
                models[name]=None; continue
            Xtr_int = [[1.0]+x for x in Xtr]
            beta = fit_ols(Xtr_int,ytr)
            models[name]={'beta':beta}
        def eval_model(name, split_rows):
            model = models.get(name)
            if not model or model['beta'] is None: return []
            beta = model['beta']
            preds=[]
            for r in split_rows:
                f=r['feats']
                if f['rv1h'] is None or f['rv24h'] is None or f['rv168h'] is None: continue
                if f['rv1h']<=0 or f['rv24h']<=0 or f['rv168h']<=0: continue
                if name=='B1':
                    X=[1.0,math.log(f['rv1h']+EPS),math.log(f['rv24h']+EPS),math.log(f['rv168h']+EPS)]
                elif name=='I1':
                    sf = f['signed_funding'] if f['signed_funding'] is not None else 0.0
                    X=[1.0,math.log(f['rv1h']+EPS),math.log(f['rv24h']+EPS),math.log(f['rv168h']+EPS),sf*math.log(f['rv24h']+EPS)]
                elif name=='I2':
                    af = f['abs_fund_pct'] if f['abs_fund_pct'] is not None else 0.0
                    rr = get_rv_ratio(f) or 1.0
                    X=[1.0,math.log(f['rv1h']+EPS),math.log(f['rv24h']+EPS),math.log(f['rv168h']+EPS),af*rr]
                elif name=='I3':
                    sf = f['signed_funding'] if f['signed_funding'] is not None else 0.0
                    rr = get_rv_ratio(f) or 1.0
                    X=[1.0,math.log(f['rv1h']+EPS),math.log(f['rv24h']+EPS),math.log(f['rv168h']+EPS),sf*(rr-1.0)]
                else: continue
                yhat = predict(beta, X[1:])
                if yhat is None or yhat <= 0 or r['y'] <= 0: continue
                q = qlike(r['y'],yhat)
                if q is not None:
                    preds.append({'y':r['y'],'yhat':yhat,'qlike':q,'sym':r['sym'],'ts_ms':r['ts_ms']})
            return preds
        res={}
        for name in ['B1','I1','I2','I3']:
            res[name]=eval_model(name,test_rows)
        def meanql(p):
            if not p: return None
            return sum(x['qlike'] for x in p)/len(p)
        out_lines.append(f'- Test rows (B1): {len(res["B1"])}')
        for name in ['B1','I1','I2','I3']:
            mq = meanql(res[name])
            out_lines.append(f'  - {name}: mean_QLIKE={mq:.6f if mq is not None else "NA"} (n={len(res[name])})')
        for name in ['I1','I2','I3']:
            boot = block_bootstrap_diff(res[name], res['B1'], n_boot=2000)
            if boot and meanql(res['B1']):
                rel = (-boot['mean']/abs(meanql(res['B1']))) * 100
                out_lines.append(f'  - {name}_vs_B1: mean_diff={boot["mean"]:.6f} 95%CI=[{boot["ci_lo"]:.6f},{boot["ci_hi"]:.6f}] rel={rel:.2f}% n={boot["n_pairs"]}')
            else:
                out_lines.append(f'  - {name}_vs_B1: NOT_EVALUABLE')
        out_lines.append('')
    OUT = REPO / "research_state" / "funding_interaction_analysis.md"
    OUT.write_text('\n'.join(out_lines))
    print(f'Wrote {OUT}')

if __name__ == '__main__':
    main()
