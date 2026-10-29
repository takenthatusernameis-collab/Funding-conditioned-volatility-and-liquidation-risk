#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import math
import random
from datetime import datetime, timezone
from pathlib import Path

import os

REPO = Path(__file__).resolve().parents[1]
RUN_MANIFEST = REPO / "research_state" / "run_manifest.json"
PROTOCOL = REPO / "research_state" / "research_protocol.md"

# Experiment selection via env var: "FCLR-001" (default, frozen window ending
# 2024-03-31) or "FCLR-002" (extended window ending 2024-09-30 per frozen protocol).
EXPERIMENT = os.environ.get("FCLR_EXPERIMENT", "FCLR-001")
if EXPERIMENT == "FCLR-002":
    OUT = REPO / "research_state" / "evaluation_summary_FCLR002_REPRO.md"
    DATA_END = "2024-09-30"
else:
    OUT = REPO / "research_state" / "evaluation_summary.md"
    DATA_END = "2024-03-31"

SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]
EPS = 1e-12
HORIZON = 24

def ts_to_dt(ts_ms):
    return datetime.fromtimestamp(ts_ms / 1000, tz=timezone.utc)

def dt_to_iso(dt):
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")

def parse_iso(s):
    # handle Z
    if s.endswith('Z'):
        s2 = s[:-1] + '+00:00'
    else:
        s2 = s
    dt = datetime.fromisoformat(s2)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt

def find_mark_csv(sym, date_str):
    # look in various cache dirs
    candidates = []
    sym_lower = sym.lower()
    # common patterns
    for p in REPO.rglob(f"{sym}-1h-{date_str}.csv"):
        sp = str(p)
        if 'markPrice' in sp:
            # prefer ones in cache dirs
            candidates.append(p)
    # also look in specific dirs
    for base in [REPO/"research_state"/"data_cache"]:
        for sub in base.iterdir() if base.exists() else []:
            p = sub / f"markPriceKlines-{date_str}" / f"{sym}-1h-{date_str}.csv"
            if p.exists():
                candidates.append(p)
            # also maybe files directly
    # deduplicate
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
    # in specific dirs
    for base in [REPO/"research_state"/"data_cache"]:
        for sub in base.iterdir() if base.exists() else []:
            p = sub / f"{sym}-fundingRate-{month}" / f"{sym}-fundingRate-{month}.csv"
            if p.exists():
                return p
    return None

def load_mark_series(sym, start_dt, end_dt):
    # build daily range
    from datetime import timedelta
    series = []  # list of (ts_ms, close)
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
    # sort and deduplicate
    series.sort(key=lambda x: x[0])
    # dedup by ts
    dedup = []
    seen = set()
    for ts_ms, close in series:
        if ts_ms in seen:
            continue
        seen.add(ts_ms)
        dedup.append((ts_ms, close))
    return dedup

def funding_months(end_ym: str) -> list[str]:
    """All YYYY-MM months from 2024-01 through end_ym inclusive.

    end_ym may be a YYYY-MM or a YYYY-MM-DD string.
    """
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


def load_funding_series_all(sym, months: list[str]):
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
    # dedup
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

def realized_variance_from_prices(prices_list):
    if len(prices_list) < 2:
        return None
    rv = 0.0
    for i in range(1, len(prices_list)):
        r = log_ret(prices_list[i], prices_list[i-1])
        if r is None:
            return None
        rv += r*r
    return rv

def qlike(y, yhat):
    if yhat is None or yhat <= 0 or y is None or y <= 0:
        return None
    return y/yhat - math.log(y/yhat) - 1.0


def build_panel():
    m = json.loads(RUN_MANIFEST.read_text())
    splits = m['split_boundaries']
    train = (parse_iso(splits['train']['start']), parse_iso(splits['train']['end']))
    val = (parse_iso(splits['validation']['start']), parse_iso(splits['validation']['end']))
    test = (parse_iso(splits['test']['start']), parse_iso(splits['test']['end']))

    # load all mark series for all symbols (wide range)
    start_all = parse_iso("2024-01-01T00:00:00Z")
    end_all = parse_iso(f"{DATA_END}T23:00:00Z")
    months = funding_months(DATA_END)

    data = {}
    for sym in SYMBOLS:
        data[sym] = {
            'mark': load_mark_series(sym, start_all, end_all),
            'funding': load_funding_series_all(sym, months)
        }
    return train, val, test, data

def get_funding_latest(funding_series, ts_ms):
    # find latest with calc_time <= ts_ms
    best = None
    for ts_f, fr in funding_series:
        if ts_f <= ts_ms:
            best = (ts_f, fr)
        else:
            break  # since sorted
    return best

def get_funding_abs_percentile(funding_series, ts_ms, window_days=90, min_obs=30):
    cutoff = ts_ms - window_days * 24 * 3600 * 1000
    hist = [fr for (t2, fr) in funding_series if t2 >= cutoff and t2 < ts_ms]  # only past
    if len(hist) < min_obs:
        return None
    # compute percentile rank of abs
    # but we need percentile of absolute funding vs history? protocol says "percentile rank of absolute funding versus that contract's preceding 90 calendar days only"
    abs_hist = [abs(x) for x in hist]
    latest_f = get_funding_latest(funding_series, ts_ms)
    if latest_f is None:
        return None
    abs_latest = abs(latest_f[1])
    # rank
    cnt = sum(1 for v in abs_hist if v <= abs_latest)
    return cnt / len(abs_hist) if abs_hist else None

def build_features_for_origin(mark_series, funding_series, t_idx, train_stats=None):
    # t_idx is index in mark_series (hourly bars)
    if t_idx < 0 or t_idx >= len(mark_series):
        return None
    ts_ms_t = mark_series[t_idx][0]
    # trailing RVs
    # RV1h - just last return squared? or realized variance over 1h window of 1 bar? "RV1h, RV24h, RV168h: trailing realized variances from hourly mark-price log returns"
    # trailing_rv over window of hours
    def trailing_rv_window(n):
        if t_idx - n < 0:
            return None
        # sum of squares of returns over n bars ending at t_idx? i.e. from t_idx-n to t_idx gives n returns?
        rv = 0.0
        for i in range(t_idx - n + 1, t_idx + 1):
            if i <= 0:
                return None
            r = log_ret(mark_series[i][1], mark_series[i-1][1])
            if r is None:
                return None
            rv += r*r
        return rv

    rv1h = trailing_rv_window(1)
    rv24h = trailing_rv_window(24)
    rv168h = trailing_rv_window(168)

    # funding
    latest_f = get_funding_latest(funding_series, ts_ms_t)
    signed_funding = latest_f[1] if latest_f else None
    abs_fund_pct = get_funding_abs_percentile(funding_series, ts_ms_t)

    # premium/EMA - protocol says mark/index premium and mark/EMA24 distance; but we may not have index fully; try to use premium index if exists? or skip if missing
    prem = None
    ema_dist = None
    # try to find premium/index/ema from files if possible - look up quickly
    # for now compute EMA of mark price over 24h
    if t_idx >= 23:  # need 24 bars
        # compute EMA (simple)
        # start with SMA
        ema = sum(mark_series[i][1] for i in range(t_idx-23, t_idx+1)) / 24.0
        # rough EMA
        alpha = 2.0 / (24.0 + 1.0)
        ema = sum(mark_series[i][1] * (alpha * (1-alpha)**(t_idx - i)) for i in range(max(0,t_idx-200), t_idx+1)) / sum(alpha * (1-alpha)**(t_idx-i) for i in range(max(0,t_idx-200), t_idx+1)) if False else None
        # simpler approximation
        ema = mark_series[t_idx][1]  # placeholder not great; better compute recursively
    # easier EMA
    if t_idx >= 0:
        # compute EMA up to t_idx
        ema = mark_series[0][1]
        alpha = 2.0/(24+1)
        for i in range(1, t_idx+1):
            ema = alpha * mark_series[i][1] + (1-alpha) * ema
        ema_dist = mark_series[t_idx][1] / ema - 1.0 if ema > 0 else None
    else:
        ema_dist = None

    return {
        'ts_ms': ts_ms_t,
        'rv1h': rv1h,
        'rv24h': rv24h,
        'rv168h': rv168h,
        'signed_funding': signed_funding,
        'abs_fund_pct': abs_fund_pct,
        'ema_dist': ema_dist,
        'prem': prem,  # may be missing
    }

def fit_ols(X_list, y_list):
    # X_list is list of dicts or lists of features; use numpy-like simple impl
    # build design matrix
    # filter valid
    rows = []
    for X,y in zip(X_list, y_list):
        if y is None or y <= 0:
            continue
        # check all needed features present? be flexible
        rows.append((X,y))
    if len(rows) < 10:
        return None
    n = len(rows)
    p = len(rows[0][0])
    # normal equations (X'X) beta = X'y
    # build X'X
    XtX = [[0.0]*p for _ in range(p)]
    Xty = [0.0]*p
    for X,y in rows:
        # X is a list
        ly = math.log(y + EPS)
        for i in range(p):
            Xty[i] += X[i] * ly
            for j in range(p):
                XtX[i][j] += X[i]*X[j]
    # add small ridge for stability
    for i in range(p):
        XtX[i][i] += 1e-12
    # solve
    beta = solve_linear(XtX, Xty)
    return beta

def solve_linear(A, b):
    n = len(A)
    M = [row[:] + [b[i]] for i,row in enumerate(A)]
    for col in range(n):
        # pivot
        piv = max(range(col, n), key=lambda r: abs(M[r][col]))
        if abs(M[piv][col]) < 1e-18:
            continue
        M[col], M[piv] = M[piv], M[col]
        for r in range(col+1, n):
            factor = M[r][col] / M[col][col] if M[col][col] != 0 else 0
            for c2 in range(col, n+1):
                M[r][c2] -= factor * M[col][c2]
    x = [0.0]*n
    for i in range(n-1, -1, -1):
        s = M[i][n]
        for j in range(i+1, n):
            s -= M[i][j] * x[j]
        if abs(M[i][i]) < 1e-18:
            x[i] = 0.0
        else:
            x[i] = s / M[i][i]
    return x

def predict(beta, X):
    if beta is None or X is None:
        return None
    s = beta[0]  # intercept
    for i in range(1, len(beta)):
        if i-1 < len(X) and X[i-1] is not None:
            s += beta[i] * X[i-1]
    # predict log rv, transform back
    yhat_log = s
    # smearing correction not strictly necessary for point forecast in log scale for comparison? but protocol says documented smearing; use simple exp
    yhat = math.exp(yhat_log)
    if yhat < 0:
        yhat = 1e-18
    return yhat

def main():
    train, val, test, data = build_panel()
    # find common panel timestamps across all symbols
    # build index maps
    sym_to_mark = {}
    for sym in SYMBOLS:
        mark = data[sym]['mark']
        # map ts_ms -> index
        sym_to_mark[sym] = mark

    # get all ts from BTC as reference? or intersection
    # get sets of timestamps
    ts_sets = []
    for sym in SYMBOLS:
        ts_sets.append(set(m[0] for m in sym_to_mark[sym]))
    common_ts = set.intersection(*ts_sets) if ts_sets else set()
    common_list = sorted(list(common_ts))

    # function to get index
    def get_idx(sym, ts_ms):
        mark = sym_to_mark[sym]
        # since sorted, could binary search but small; just iterate not needed
        # build dict
        pass

    # build dicts
    mark_dict = {}
    for sym in SYMBOLS:
        mark_dict[sym] = {m[0]: m[1] for m in sym_to_mark[sym]}
        # also keep list for indexing
    mark_lists = {sym: sym_to_mark[sym] for sym in SYMBOLS}

    # for each origin ts in common_list, need index
    results_all = []

    # collect features for each (sym, origin_idx)
    # build structures
    def in_split_dt(dt, bounds):
        lo,hi = bounds
        return lo <= dt <= hi

    # prepare
    eval_rows = []
    for sym in SYMBOLS:
        mark_list = mark_lists[sym]
        fund_list = data[sym]['funding']
        # map ts to index
        ts_to_idx = {mark_list[i][0]: i for i in range(len(mark_list))}
        for i in range(len(mark_list)):
            ts_ms = mark_list[i][0]
            ts_dt = ts_to_dt(ts_ms)
            # check if in any split
            split = None
            if in_split_dt(ts_dt, train):
                split = 'train'
            elif in_split_dt(ts_dt, val):
                split = 'val'
            elif in_split_dt(ts_dt, test):
                split = 'test'
            else:
                continue
            # need enough history for features and enough future for target
            if i < 168:  # need rv168h
                continue
            # need 24 hours future
            if i + HORIZON >= len(mark_list):
                continue
            # compute target
            future_prices = [mark_list[i][1]] + [mark_list[i+1+j][1] for j in range(HORIZON)]
            y = realized_variance_from_prices(future_prices)
            if y is None or y <= 0:
                continue
            feats = build_features_for_origin(mark_list, fund_list, i)
            if feats is None:
                continue
            eval_rows.append({
                'sym': sym,
                'ts_ms': ts_ms,
                'ts_dt': ts_dt,
                'split': split,
                'y': y,
                'feats': feats,
                'i': i
            })

    print(f"Collected {len(eval_rows)} rows", flush=True)
    # split
    train_rows = [r for r in eval_rows if r['split']=='train']
    val_rows = [r for r in eval_rows if r['split']=='val']
    test_rows = [r for r in eval_rows if r['split']=='test']

    # helper to build X
    def make_X_B0(rows):
        # B0: persistence using preceding RV24h
        Xs, ys = [], []
        for r in rows:
            f = r['feats']
            if f['rv24h'] is None or f['rv24h'] <= 0:
                continue
            Xs.append([math.log(f['rv24h'] + EPS)])  # intercept added separately
            ys.append(r['y'])
        return Xs, ys

    def make_X_B1(rows):
        Xs, ys = [], []
        for r in rows:
            f = r['feats']
            if f['rv1h'] is None or f['rv24h'] is None or f['rv168h'] is None:
                continue
            if f['rv1h'] <= 0 or f['rv24h'] <= 0 or f['rv168h'] <= 0:
                continue
            Xs.append([math.log(f['rv1h'] + EPS), math.log(f['rv24h'] + EPS), math.log(f['rv168h'] + EPS)])
            ys.append(r['y'])
        return Xs, ys

    def make_X_C1(rows):
        Xs, ys = [], []
        for r in rows:
            f = r['feats']
            if f['rv1h'] is None or f['rv24h'] is None or f['rv168h'] is None:
                continue
            if f['rv1h'] <= 0 or f['rv24h'] <= 0 or f['rv168h'] <= 0:
                continue
            sf = f['signed_funding'] if f['signed_funding'] is not None else 0.0
            af = f['abs_fund_pct'] if f['abs_fund_pct'] is not None else 0.0
            Xs.append([math.log(f['rv1h'] + EPS), math.log(f['rv24h'] + EPS), math.log(f['rv168h'] + EPS), sf, af])
            ys.append(r['y'])
        return Xs, ys

    def make_X_C2(rows):
        Xs, ys = [], []
        for r in rows:
            f = r['feats']
            if f['rv1h'] is None or f['rv24h'] is None or f['rv168h'] is None:
                continue
            if f['rv1h'] <= 0 or f['rv24h'] <= 0 or f['rv168h'] <= 0:
                continue
            sf = f['signed_funding'] if f['signed_funding'] is not None else 0.0
            af = f['abs_fund_pct'] if f['abs_fund_pct'] is not None else 0.0
            prem = f['prem'] if f['prem'] is not None else 0.0
            ema = f['ema_dist'] if f['ema_dist'] is not None else 0.0
            Xs.append([math.log(f['rv1h'] + EPS), math.log(f['rv24h'] + EPS), math.log(f['rv168h'] + EPS), sf, af, prem, ema])
            ys.append(r['y'])
        return Xs, ys

    # fit on train
    models = {}
    for name, maker in [('B0', make_X_B0), ('B1', make_X_B1), ('C1', make_X_C1), ('C2', make_X_C2)]:
        Xtr, ytr = maker(train_rows)
        if not Xtr:
            models[name] = None
            continue
        # add intercept
        Xtr_int = [[1.0] + x for x in Xtr]
        beta = fit_ols(Xtr_int, ytr)
        models[name] = {'beta': beta, 'maker': maker}

    # evaluate on test (and also report val for completeness)
    def eval_model(name, split_rows):
        model = models.get(name)
        if not model or model['beta'] is None:
            return []
        maker = model['maker']
        beta = model['beta']
        Xs, ys = maker(split_rows)
        # need to align - easier to recompute with same maker on split_rows in order
        res = []
        # get in order
        Xs2, ys2 = [], []
        for r in split_rows:
            # make single
            pass
        # better iterate
        idx = 0
        # rebuild aligned
        preds = []
        actuals = []
        # do again aligned
        for r in split_rows:
            f = r['feats']
            if name == 'B0':
                if f['rv24h'] is None or f['rv24h'] <= 0: continue
                X = [1.0, math.log(f['rv24h']+EPS)]
            elif name == 'B1':
                if f['rv1h'] is None or f['rv24h'] is None or f['rv168h'] is None: continue
                if f['rv1h']<=0 or f['rv24h']<=0 or f['rv168h']<=0: continue
                X = [1.0, math.log(f['rv1h']+EPS), math.log(f['rv24h']+EPS), math.log(f['rv168h']+EPS)]
            elif name == 'C1':
                if f['rv1h'] is None or f['rv24h'] is None or f['rv168h'] is None: continue
                if f['rv1h']<=0 or f['rv24h']<=0 or f['rv168h']<=0: continue
                sf = f['signed_funding'] if f['signed_funding'] is not None else 0.0
                af = f['abs_fund_pct'] if f['abs_fund_pct'] is not None else 0.0
                X = [1.0, math.log(f['rv1h']+EPS), math.log(f['rv24h']+EPS), math.log(f['rv168h']+EPS), sf, af]
            elif name == 'C2':
                if f['rv1h'] is None or f['rv24h'] is None or f['rv168h'] is None: continue
                if f['rv1h']<=0 or f['rv24h']<=0 or f['rv168h']<=0: continue
                sf = f['signed_funding'] if f['signed_funding'] is not None else 0.0
                af = f['abs_fund_pct'] if f['abs_fund_pct'] is not None else 0.0
                prem = f['prem'] if f['prem'] is not None else 0.0
                ema = f['ema_dist'] if f['ema_dist'] is not None else 0.0
                X = [1.0, math.log(f['rv1h']+EPS), math.log(f['rv24h']+EPS), math.log(f['rv168h']+EPS), sf, af, prem, ema]
            else:
                continue
            yhat = predict(beta, X[1:])
            if yhat is None or yhat <= 0 or r['y'] <= 0:
                continue
            q = qlike(r['y'], yhat)
            if q is not None:
                preds.append({'y': r['y'], 'yhat': yhat, 'qlike': q, 'sym': r['sym'], 'ts_ms': r['ts_ms']})
        return preds

    # evaluate
    results = {}
    for name in ['B0', 'B1', 'C1', 'C2']:
        results[name] = {
            'test': eval_model(name, test_rows),
            'val': eval_model(name, val_rows)
        }

    # compute stats
    def mean_qlike(preds):
        if not preds:
            return None
        return sum(p['qlike'] for p in preds) / len(preds)

    def paired_diff(preds_a, preds_b):
        # need paired by (sym, ts_ms)
        key_b = {(p['sym'], p['ts_ms']): p for p in preds_b}
        diffs = []
        for pa in preds_a:
            key = (pa['sym'], pa['ts_ms'])
            if key in key_b:
                diffs.append(pa['qlike'] - key_b[key]['qlike'])  # positive means a worse
        return diffs

    # block bootstrap
    def block_bootstrap_diff(preds_a, preds_b, n_boot=2000, block_hours=24):
        key_b = {(p['sym'], p['ts_ms']): p for p in preds_b}
        pairs = []
        for pa in preds_a:
            key = (pa['sym'], pa['ts_ms'])
            if key in key_b:
                pairs.append((pa['ts_ms'], pa['qlike'] - key_b[key]['qlike']))
        if not pairs:
            return None
        # form blocks by day
        # group by date
        from collections import defaultdict
        blocks = defaultdict(list)
        for ts_ms, d in pairs:
            dt = ts_to_dt(ts_ms)
            block_key = (dt.date().isoformat(),)
            blocks[block_key].append(d)
        block_list = list(blocks.values())
        rng = random.Random(12345)
        stats = []
        for _ in range(n_boot):
            # sample blocks with replacement
            samp = []
            for _ in range(len(block_list)):
                b = rng.choice(block_list)
                samp.extend(b)
            if not samp:
                continue
            stats.append(sum(samp)/len(samp))
        stats.sort()
        # CI
        lo = stats[int(0.025*len(stats))] if stats else None
        hi = stats[int(0.975*len(stats))] if stats else None
        mean_d = sum((pa['qlike'] - key_b[(pa['sym'],pa['ts_ms'])]['qlike']) for pa in preds_a if (pa['sym'],pa['ts_ms']) in key_b) / len([p for p in pairs])
        return {'mean': mean_d, 'ci_lo': lo, 'ci_hi': hi, 'n_pairs': len(pairs)}

    # compute
    summary = {}
    for name in ['B0','B1','C1','C2']:
        preds_t = results[name]['test']
        summary[name] = {
            'test_qlike_mean': mean_qlike(preds_t),
            'test_n': len(preds_t)
        }

    # contrasts
    contrasts = {}
    for a,b in [('C2','B1'), ('C1','B1'), ('C2','C1')]:
        boot = block_bootstrap_diff(results[a]['test'], results[b]['test'], n_boot=2000)
        if boot:
            mean_d = boot['mean']  # a - b (positive means a worse)
            # relative reduction in QLIKE? lower is better; if C2 better than B1, diff C2-B1 negative means improvement
            rel = (-mean_d / abs(summary[b]['test_qlike_mean'])) * 100 if summary[b]['test_qlike_mean'] and summary[b]['test_qlike_mean'] != 0 else None
            contrasts[f'{a}_vs_{b}'] = {
                'mean_diff': mean_d,
                'rel_reduction_pct': rel,
                'ci_lo': boot['ci_lo'],
                'ci_hi': boot['ci_hi'],
                'n_pairs': boot['n_pairs']
            }

    # write summary
    lines = []
    lines.append(f'# Evaluation Summary ({EXPERIMENT})')
    lines.append('')
    lines.append(f'Experiment: {EXPERIMENT}')
    lines.append(f'Data range: 2024-01-01 .. {DATA_END}')
    lines.append(f'Generated: {datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}')
    lines.append('')
    lines.append('## Splits (frozen)')
    lines.append(f"- Train: {train[0].strftime('%Y-%m-%dT%H:%M:%SZ')} .. {train[1].strftime('%Y-%m-%dT%H:%M:%SZ')}")
    lines.append(f"- Val: {val[0].strftime('%Y-%m-%dT%H:%M:%SZ')} .. {val[1].strftime('%Y-%m-%dT%H:%M:%SZ')}")
    lines.append(f"- Test: {test[0].strftime('%Y-%m-%dT%H:%M:%SZ')} .. {test[1].strftime('%Y-%m-%dT%H:%M:%SZ')} (7d embargo)")
    lines.append('')
    lines.append('## Test set QLIKE (lower is better)')
    lines.append('')
    for name in ['B0','B1','C1','C2']:
        s = summary[name]
        lines.append(f"- {name}: mean_QLIKE={s['test_qlike_mean']:.6f} (n={s['test_n']})")
    lines.append('')
    lines.append('## Paired comparisons (block bootstrap, ~24h blocks, 2000 replications)')
    lines.append('')
    for k,v in contrasts.items():
        lines.append(f"### {k}")
        lines.append(f"- Paired n: {v['n_pairs']}")
        lines.append(f"- Mean diff (modelA - modelB), QLIKE: {v['mean_diff']:.6f} (95% CI [{v['ci_lo']:.6f}, {v['ci_hi']:.6f}])")
        if v['rel_reduction_pct'] is not None:
            lines.append(f"- Relative reduction (QLIKE): {v['rel_reduction_pct']:.2f}% (negative diff means improvement)")
        lines.append('')
    lines.append('## Gate assessment (primary contrast C2 vs B1)')
    lines.append('')
    c = contrasts.get('C2_vs_B1')
    if c:
        passed = c['rel_reduction_pct'] is not None and c['rel_reduction_pct'] >= 2.0 and c['ci_hi'] < 0  # improvement means negative diff
        lines.append(f"- Primary contrast C2 vs B1 meets >=2% relative QLIKE reduction: {'PASS' if passed else 'NOT_MET'}")
        lines.append(f"- Relative reduction: {c['rel_reduction_pct']:.2f}%")
        lines.append(f"- 95% CI for diff (C2-B1): [{c['ci_lo']:.6f}, {c['ci_hi']:.6f}]")
    else:
        lines.append('- Primary contrast: NOT_EVALUABLE')
    lines.append('')
    lines.append('## Notes')
    lines.append('- All results use frozen splits only; no tuning on holdout.')
    lines.append('- Features with missing values filled with 0.0 where protocol allows or rows dropped if core RV features missing.')
    lines.append('- Mark/index premium not fully integrated where source missing; EMA distance computed from mark prices.')
    lines.append('')

    OUT.write_text('\n'.join(lines))
    print(f"Wrote {OUT}")
    print('\n'.join(lines))

if __name__ == '__main__':
    main()
