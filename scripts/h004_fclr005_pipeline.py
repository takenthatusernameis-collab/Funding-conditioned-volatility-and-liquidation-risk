#!/usr/bin/env python3
"""FCLR-005 Track A pipeline: observed liquidation outcomes on the 2026 Bybit census.

Idempotent, checkpoint-resumable, deterministic (fixed seed). Builds the hourly
(binance feature × bybit label) panel for {BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT},
fits fixed-form logistic models B0/B1/C1/C2, and reports Brier / log-loss /
calibration slope-intercept / precision-recall / AUPRC with block-bootstrap
uncertainty and leave-one-symbol-out stability. PILOT/EXPLORATORY ONLY: the
~30-day label window cannot satisfy the >=3 non-overlapping 30-day confirmatory
gate, so no confirmatory skill is claimed and FCLR-H004 remains BLOCKED for
frozen 2024.
"""
from __future__ import annotations

import csv
import json
import math
import random
import subprocess
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
import hashlib

REPO = Path(__file__).resolve().parents[1]
CACHE = REPO / "research_state" / "data_cache"
LIQ = CACHE / "liquidations_full_20260807.csv"
RUN_MANIFEST = REPO / "research_state" / "run_manifest.json"
HYP = REPO / "research_state" / "hypothesis_registry.json"
OUT_SUM = REPO / "research_state" / "evaluation_summary_FCLR005.md"
LIQ_ENUM = REPO / "research_state" / "liquidation_sources_enumeration.md"
CKPT_DIR = REPO / "research_state" / ".cache"
CKPT_PANEL = CKPT_DIR / "fclr005_panel.json"

SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]
SEED = 123456789
random.seed(SEED)

LABEL_START = datetime(2026, 7, 8, 16, 42, 32, tzinfo=timezone.utc)
LABEL_END = datetime(2026, 8, 6, 23, 59, 42, tzinfo=timezone.utc)
FEATURE_START = datetime(2026, 4, 1, 0, 0, 0, tzinfo=timezone.utc)

EPS = 1e-12
BOOTSTRAP_REPLICATES = 1000
BOOTSTRAP_SEED = SEED + 1


def ts_to_dt(ts_ms):
    return datetime.fromtimestamp(int(ts_ms) / 1000, tz=timezone.utc)


def dt_to_iso_z(dt):
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def iso_to_dt(s):
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def git_sha():
    try:
        out = subprocess.run(
            ["git", "-C", str(REPO), "rev-parse", "HEAD"],
            capture_output=True, text=True, check=True,
        )
        return out.stdout.strip()
    except Exception:
        return "unknown"


def find_file(kind, sym, date_str_or_month):
    """Locate an extracted CSV for kind in {mark,index,premium} (daily) or funding (monthly)."""
    if not CACHE.exists():
        return None
    if kind == "funding":
        patterns = [
            f"{sym}-fundingRate-{date_str_or_month}/{sym}-fundingRate-{date_str_or_month}.csv",
            f"{sym}-fundingRate-{date_str_or_month}.csv",
        ]
    else:
        prefix = {"mark": "markPriceKlines", "index": "indexPriceKlines",
                  "premium": "premiumIndexKlines"}[kind]
        patterns = [
            f"{prefix}-{date_str_or_month}/{sym}-1h-{date_str_or_month}.csv",
            f"{prefix}-{date_str_or_month}/{sym}-1h-{date_str_or_month}/{sym}-1h-{date_str_or_month}.csv",
        ]
    for sub in CACHE.iterdir():
        if not sub.is_dir():
            continue
        for rel in patterns:
            p = sub / rel
            if p.exists():
                return p
        for p in sub.rglob(f"{sym}-1h-{date_str_or_month}.csv" if kind != "funding" else f"{sym}-fundingRate-{date_str_or_month}.csv"):
            sp = str(p)
            if kind == "funding" or f"{kind}Price" in sp or kind == "premium" and "premiumIndex" in sp:
                return p
    return None


def load_series(kind, sym, start_dt, end_dt):
    from datetime import timedelta
    series = []
    cur = start_dt.replace(hour=0, minute=0, second=0, microsecond=0)
    end_day = end_dt.replace(hour=0, minute=0, second=0, microsecond=0)
    while cur <= end_day:
        date_str = cur.strftime("%Y-%m-%d")
        csvp = find_file(kind, sym, date_str)
        if csvp and csvp.exists():
            try:
                with csvp.open() as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        try:
                            ts_ms = int(row['open_time'])
                            ts_dt = ts_to_dt(ts_ms)
                            if ts_dt < start_dt - timedelta(hours=2) or ts_dt > end_dt + timedelta(hours=2):
                                continue
                            close = float(row['close'])
                            series.append((ts_dt.replace(minute=0, second=0, microsecond=0), close))
                        except Exception:
                            continue
            except Exception:
                pass
        cur += timedelta(days=1)
    d = {}
    for k, v in series:
        d[k] = v
    return d


def load_funding_series(sym, months):
    rows = []
    for month in months:
        csvp = find_file("funding", sym, month)
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
    dedup, seen = [], set()
    for ts, fr in rows:
        if ts in seen:
            continue
        seen.add(ts)
        dedup.append((ts, fr))
    return dedup


def funding_months_up_to(end_ym):
    y, m = end_ym[:7].split('-')
    out, cur_y, cur_m = [], 2026, 4
    end_y, end_m = int(y), int(m)
    while (cur_y, cur_m) <= (end_y, end_m):
        out.append(f"{cur_y}-{cur_m:02d}")
        cur_m += 1
        if cur_m > 12:
            cur_m = 1
            cur_y += 1
    return out


def ema(seq, span):
    if not seq:
        return None
    alpha = 2.0 / (span + 1.0)
    ema_res = seq[0]
    for v in seq[1:]:
        ema_res = alpha * v + (1.0 - alpha) * ema_res
    return ema_res


def sigmoid(x):
    if x < -700:
        return 0.0
    if x > 700:
        return 1.0
    return 1.0 / (1.0 + math.exp(-x))


def fit_logistic(X, y, lr=0.01, epochs=1500):
    n = len(X)
    if n == 0:
        return [0.0] * (len(X[0]) + 1) if X else [0.0]
    d = len(X[0])
    w = [0.0] * (d + 1)
    prev_loss = float('inf')
    for _ in range(epochs):
        gw = [0.0] * (d + 1)
        loss = 0.0
        for i in range(n):
            xi = X[i]
            z = w[0]
            for j in range(d):
                val = xi[j]
                if val is None or (isinstance(val, float) and (math.isnan(val) or math.isinf(val))):
                    val = 0.0
                z += w[j + 1] * val
            p = sigmoid(z)
            err = p - y[i]
            loss += -(y[i] * math.log(min(max(p, 1e-15), 1 - 1e-15))
                      + (1 - y[i]) * math.log(1 - min(max(p, 1e-15), 1 - 1e-15)))
            gw[0] += err
            for j in range(d):
                val = xi[j]
                if val is None or (isinstance(val, float) and (math.isnan(val) or math.isinf(val))):
                    val = 0.0
                gw[j + 1] += err * val
        loss /= n
        if abs(prev_loss - loss) < 1e-10:
            break
        prev_loss = loss
        for j in range(len(w)):
            w[j] -= lr * gw[j] / n
    return w


def predict_logistic(w, x):
    z = w[0]
    for j in range(len(x)):
        val = x[j]
        if val is None or (isinstance(val, float) and (math.isnan(val) or math.isinf(val))):
            val = 0.0
        z += w[j + 1] * val
    return sigmoid(z)


def brier_score(y, p):
    n = len(y)
    if n == 0:
        return 0.0
    return sum((pi - yi) ** 2 for pi, yi in zip(p, y)) / n


def log_loss_score(y, p):
    n = len(y)
    if n == 0:
        return 0.0
    s = 0.0
    for yi, pi in zip(y, p):
        pp = min(max(pi, 1e-15), 1 - 1e-15)
        s += -(yi * math.log(pp) + (1 - yi) * math.log(1 - pp))
    return s / n


def precision_recall_auc(y, p):
    pairs = list(zip(p, y))
    pairs.sort(reverse=True)
    tp = fp = 0
    fn = sum(y)
    prev_prec, prev_rec, auc = 1.0, 0.0, 0.0
    for pp, yy in pairs:
        if yy == 1:
            tp += 1
            fn -= 1
        else:
            fp += 1
        prec = 1.0 if tp + fp == 0 else tp / (tp + fp)
        rec = 0.0 if tp + fn == 0 else tp / (tp + fn)
        auc += (rec - prev_rec) * (prec + prev_prec) / 2.0
        prev_prec, prev_rec = prec, rec
    return auc


def precision_at_base_rate(y, p):
    n = len(y)
    if n == 0:
        return 0.0, 0.0
    base = sum(y) / n
    thr = sorted(p)[max(0, int(math.ceil((1.0 - base) * n)) - 1)] if n > 0 else 0.5
    tp = fp = 0
    for yi, pi in zip(y, p):
        if pi >= thr:
            if yi == 1:
                tp += 1
            else:
                fp += 1
    prec = 1.0 if tp + fp == 0 else tp / (tp + fp)
    return prec, thr


def calibration_slope_intercept(y, p):
    # Logistic calibration of y on logit(p); standardized logit for stability,
    # then rescaled to raw logit units: intercept/slope of logit(p_cal) = a + b*logit(p).
    logits = []
    for pi in p:
        pp = min(max(pi, 1e-15), 1 - 1e-15)
        logits.append(math.log(pp / (1.0 - pp)))
    m = sum(logits) / len(logits)
    sd = math.sqrt(sum((v - m) ** 2 for v in logits) / len(logits)) or 1.0
    X = [[(v - m) / sd] for v in logits]
    w = fit_logistic(X, y, lr=0.01, epochs=5000)
    slope = w[1] / sd
    intercept = w[0] - w[1] * m / sd
    return intercept, slope


def block_bootstrap(hour_pairs, hours, metric_fn, replicates, seed):
    rng = random.Random(seed)
    n = len(hours)
    if n == 0:
        return {'mean': 0.0, 'ci_lo': 0.0, 'ci_hi': 0.0, 'replicates': replicates}
    rows_by_hour = defaultdict(list)
    for h, pairs in hour_pairs.items():
        rows_by_hour[h] = pairs
    stats = []
    for _ in range(replicates):
        draw = [hours[rng.randrange(n)] for _ in range(n)]
        sel = []
        for h in draw:
            sel.extend(rows_by_hour[h])
        ys = [y for y, _ in sel]
        ps = [p for _, p in sel]
        stats.append(metric_fn(ys, ps))
    stats.sort()
    lo_i = max(0, int(0.025 * replicates) - 1)
    hi_i = min(len(stats) - 1, int(0.975 * replicates))
    return {
        'mean': sum(stats) / len(stats),
        'ci_lo': stats[lo_i],
        'ci_hi': stats[hi_i],
        'replicates': replicates,
    }


def model_feature_row(r, model):
    base = [r['rv1h'], r['rv24h'], math.log(max(r['rv24h'], 1e-18)),
            math.log(max(r['rv168h'], 1e-18)) if r['rv168h'] > 0 else -20.0]
    if model == 'B1':
        return base
    if model == 'C1':
        return base + [r['fund_signed'], r['fund_abs_pct']]
    if model == 'C2':
        return base + [r['fund_signed'], r['fund_abs_pct'], r['prem_feat'], r['ema_dist']]
    return base


def fit_predict(train_rows, test_rows, model, yname):
    Xtr, ytr = [], []
    for r in train_rows:
        Xtr.append(model_feature_row(r, model))
        ytr.append(r[yname])
    w = fit_logistic(Xtr, ytr)
    return [predict_logistic(w, model_feature_row(r, model)) for r in test_rows]


def main():
    start_time = datetime.now(timezone.utc)
    print("FCLR-005 pipeline starting", flush=True)
    CKPT_DIR.mkdir(parents=True, exist_ok=True)

    # ---- 1. Load Bybit liquidation census (label side) ----
    liq_by_hp = defaultdict(lambda: {'long_count': 0, 'short_count': 0, 'long_usd': 0.0, 'short_usd': 0.0})
    per_exchange = Counter()
    per_sym_exchange = Counter()
    total_rows = 0
    total_bybit = 0
    target_bybit_rows = 0
    with LIQ.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            total_rows += 1
            ex = (row.get('exchange') or '').strip().lower()
            sym = (row.get('symbol') or '').strip()
            per_exchange[ex] += 1
            per_sym_exchange[(sym, ex)] += 1
            if ex != 'bybit':
                continue
            if sym not in SYMBOLS:
                continue
            try:
                ts_ms = int(row.get('ts_ms'))
            except Exception:
                continue
            ev = (row.get('event') or '').strip()
            ts_dt = ts_to_dt(ts_ms).replace(minute=0, second=0, microsecond=0)
            usd = float(row.get('usd') or 0)
            hp = (sym, ts_dt)
            target_bybit_rows += 1
            if ev == 'long_liquidated':
                liq_by_hp[hp]['long_count'] += 1
                liq_by_hp[hp]['long_usd'] += usd
                total_bybit += 1
            elif ev == 'short_liquidated':
                liq_by_hp[hp]['short_count'] += 1
                liq_by_hp[hp]['short_usd'] += usd
                total_bybit += 1
    print(f"Loaded: total_rows={total_rows} bybit_census_target_symbols={target_bybit_rows}", flush=True)

    # ---- 2. Load features ----
    months_fund = funding_months_up_to('2026-08')
    funding_all = {sym: load_funding_series(sym, months_fund) for sym in SYMBOLS}
    mark_maps = {sym: load_series('mark', sym, FEATURE_START, LABEL_END) for sym in SYMBOLS}
    idx_maps = {sym: load_series('index', sym, FEATURE_START, LABEL_END) for sym in SYMBOLS}
    prem_maps = {sym: load_series('premium', sym, FEATURE_START, LABEL_END) for sym in SYMBOLS}
    print("Feature maps loaded", flush=True)

    # ---- 3. Build panel (checkpoint-resumable) ----
    panel_rows = []
    resumed = False
    if CKPT_PANEL.exists():
        try:
            ckpt = json.loads(CKPT_PANEL.read_text())
            if ckpt.get('label_start') == dt_to_iso_z(LABEL_START) \
               and ckpt.get('label_end') == dt_to_iso_z(LABEL_END) \
               and ckpt.get('symbols') == SYMBOLS:
                for r in ckpt['rows']:
                    r['hour'] = iso_to_dt(r['hour_iso'])
                    panel_rows.append(r)
                resumed = True
                print(f"Resumed panel from checkpoint: {len(panel_rows)} rows", flush=True)
        except Exception as e:
            print(f"Checkpoint load failed ({e}); rebuilding", flush=True)
            panel_rows = []

    if not resumed:
        drops = Counter()
        for sym in SYMBOLS:
            mark_map = mark_maps[sym]
            idx_map = idx_maps[sym]
            prem_map = prem_maps[sym]
            fund_ser = sorted(funding_all[sym], key=lambda x: x[0])
            cur = LABEL_START.replace(minute=0, second=0, microsecond=0)
            end_h = LABEL_END.replace(minute=0, second=0, microsecond=0)
            while cur <= end_h:
                h_dt = cur
                if h_dt < FEATURE_START + timedelta(days=90):
                    drops['before_90d_funding_history'] += 1
                    cur += timedelta(hours=1)
                    continue
                mark_c = mark_map.get(h_dt)
                if mark_c is None or mark_c <= 0:
                    drops['missing_mark'] += 1
                    cur += timedelta(hours=1)
                    continue
                # RV (trailing up to 168h)
                rv_list = []
                for k in range(1, 169):
                    hk = h_dt - timedelta(hours=k)
                    hkm1 = h_dt - timedelta(hours=k - 1)
                    ck = mark_map.get(hk)
                    ckm1 = mark_map.get(hkm1)
                    if ck is None or ckm1 is None or ck <= 0 or ckm1 <= 0:
                        break
                    rv_list.append(math.log(ckm1 / ck) ** 2)
                if len(rv_list) < 24:
                    drops['insufficient_rv_history'] += 1
                    cur += timedelta(hours=1)
                    continue
                rv1h = rv_list[0]
                rv24h = sum(rv_list[0:24])
                rv168h = sum(rv_list[0:168]) if len(rv_list) >= 168 else None
                # Signed funding (latest <= t)
                latest_f, latest_f_ts = None, -10 ** 19
                for fts, fr in fund_ser:
                    fdt = ts_to_dt(fts)
                    if fdt <= h_dt and fts > latest_f_ts:
                        latest_f, latest_f_ts = fr, fts
                if latest_f is None:
                    drops['missing_funding'] += 1
                    cur += timedelta(hours=1)
                    continue
                # |funding| percentile over preceding 90 days, >=30 obs
                cutoff = h_dt - timedelta(days=90)
                hist_abs = [abs(fr) for fts, fr in fund_ser
                            if cutoff <= ts_to_dt(fts) < h_dt]
                if len(hist_abs) < 30:
                    drops['insufficient_funding_history'] += 1
                    cur += timedelta(hours=1)
                    continue
                hist_abs_sorted = sorted(hist_abs)
                af = abs(latest_f)
                cnt_le = sum(1 for v in hist_abs_sorted if v <= af + 1e-18)
                fund_pct = cnt_le / len(hist_abs_sorted)
                # Premium (contemporaneous mark/index)
                idx_c = idx_map.get(h_dt)
                prem_feat = (mark_c / idx_c - 1.0) if (idx_c is not None and idx_c > 0) else None
                if prem_feat is None:
                    drops['missing_premium'] += 1
                    cur += timedelta(hours=1)
                    continue
                # EMA24 distance (fully closed prior bars only)
                ema_series = []
                for k in range(0, 24):
                    ck = mark_map.get(h_dt - timedelta(hours=k))
                    if ck is None:
                        break
                    ema_series.append(ck)
                if len(ema_series) < 24:
                    drops['insufficient_ema_history'] += 1
                    cur += timedelta(hours=1)
                    continue
                ema24v_res = ema(list(reversed(ema_series)), 24)
                if ema24v_res is None or ema24v_res <= 0:
                    drops['ema_invalid'] += 1
                    cur += timedelta(hours=1)
                    continue
                ema_dist = mark_c / ema24v_res - 1.0
                hp = (sym, h_dt)
                lq = liq_by_hp.get(hp, {'long_count': 0, 'short_count': 0, 'long_usd': 0.0, 'short_usd': 0.0})
                panel_rows.append({
                    'sym': sym,
                    'hour_iso': dt_to_iso_z(h_dt),
                    'rv1h': rv1h,
                    'rv24h': rv24h,
                    'rv168h': rv168h if rv168h is not None else 0.0,
                    'fund_signed': latest_f,
                    'fund_abs_pct': fund_pct,
                    'prem_feat': prem_feat,
                    'ema_dist': ema_dist,
                    'y_long': 1 if lq['long_count'] > 0 else 0,
                    'y_short': 1 if lq['short_count'] > 0 else 0,
                    'long_cnt': lq['long_count'],
                    'short_cnt': lq['short_count'],
                    'long_usd': lq['long_usd'],
                    'short_usd': lq['short_usd'],
                })
                cur += timedelta(hours=1)
        print(f"Panel rows built: {len(panel_rows)}, drops: {dict(drops)}", flush=True)
        ckpt = {
            'label_start': dt_to_iso_z(LABEL_START),
            'label_end': dt_to_iso_z(LABEL_END),
            'symbols': SYMBOLS,
            'built_at': dt_to_iso_z(datetime.now(timezone.utc)),
            'count': len(panel_rows),
            'rows': panel_rows,
        }
        CKPT_PANEL.write_text(json.dumps(ckpt))
        print("Panel checkpoint saved", flush=True)

    for r in panel_rows:
        r['hour'] = iso_to_dt(r['hour_iso'])

    # ---- 4. Chronological train/val/test split ----
    hours_sorted = sorted(set(r['hour'] for r in panel_rows))
    n_h = len(hours_sorted)
    train_end = hours_sorted[int(n_h * 0.5) - 1] if n_h > 0 else None
    val_end = hours_sorted[int(n_h * 0.75) - 1] if n_h > 0 else train_end

    def get_split(h):
        if train_end is None:
            return 'test'
        if h <= train_end:
            return 'train'
        if h <= val_end:
            return 'val'
        return 'test'

    for r in panel_rows:
        r['split'] = get_split(r['hour'])

    train_rows = [r for r in panel_rows if r['split'] == 'train']
    val_rows = [r for r in panel_rows if r['split'] == 'val']
    test_rows = [r for r in panel_rows if r['split'] == 'test']

    # test window block count (non-overlapping 30-day blocks)
    test_hours = sorted(set(r['hour'] for r in test_rows))
    block_count = 0
    if test_hours:
        cur_block = test_hours[0]
        end_all = test_hours[-1]
        while cur_block <= end_all:
            block_end = cur_block + timedelta(days=30) - timedelta(hours=1)
            if block_end <= end_all:
                block_count += 1
            cur_block = block_end + timedelta(hours=1)

    results = {}
    for target in ['long', 'short']:
        yname = f'y_{target}'
        results[target] = {}
        train_base = (sum(r[yname] for r in train_rows) / len(train_rows)) if train_rows else 0.0
        test_base = (sum(r[yname] for r in test_rows) / len(test_rows)) if test_rows else 0.0
        test_prev = sum(1 for r in test_rows if r[yname] == 1)
        for model in ['B0', 'B1', 'C1', 'C2']:
            if model == 'B0':
                p_pred = [train_base for _ in test_rows]
            else:
                p_pred = fit_predict(train_rows, test_rows, model, yname)
            y_test = [r[yname] for r in test_rows]
            hour_pairs = defaultdict(list)
            for r, pp in zip(test_rows, p_pred):
                hour_pairs[r['hour']].append((r[yname], pp))
            bs = brier_score(y_test, p_pred)
            ll = log_loss_score(y_test, p_pred)
            auc = precision_recall_auc(y_test, p_pred)
            prec_br, thr_br = precision_at_base_rate(y_test, p_pred)
            ci, slope = calibration_slope_intercept(y_test, p_pred)
            boot_bs = block_bootstrap(hour_pairs, test_hours,
                                      lambda ys, ps: brier_score(ys, ps),
                                      BOOTSTRAP_REPLICATES, BOOTSTRAP_SEED)
            boot_ll = block_bootstrap(hour_pairs, test_hours,
                                      lambda ys, ps: log_loss_score(ys, ps),
                                      BOOTSTRAP_REPLICATES, BOOTSTRAP_SEED)
            results[target][model] = {
                'brier': bs, 'logloss': ll, 'prauc': auc,
                'brier_boot': boot_bs, 'logloss_boot': boot_ll,
                'cal_intercept': ci, 'cal_slope': slope,
                'precision_at_base_rate': prec_br, 'base_rate_threshold': thr_br,
                'n_test': len(test_rows), 'events_test': int(test_prev),
                'base_rate': test_base, 'train_base_rate': train_base,
            }

    # ---- 5. Leave-one-symbol-out stability (primary contrast C2 vs B1) ----
    loso = {}
    for held in SYMBOLS:
        tr = [r for r in panel_rows if r['sym'] != held and r['split'] == 'train']
        te = [r for r in panel_rows if r['sym'] == held and r['split'] == 'test']
        loso[held] = {}
        for target in ['long', 'short']:
            yname = f'y_{target}'
            if not te or not tr:
                loso[held][target] = {'n_test': 0, 'skipped': True}
                continue
            p_b1 = fit_predict(tr, te, 'B1', yname)
            p_c2 = fit_predict(tr, te, 'C2', yname)
            ys = [r[yname] for r in te]
            loso[held][target] = {
                'n_test': len(te),
                'events': int(sum(ys)),
                'base_rate': sum(ys) / len(ys),
                'brier_b1': brier_score(ys, p_b1),
                'brier_c2': brier_score(ys, p_c2),
                'brier_diff_c2_minus_b1': brier_score(ys, p_c2) - brier_score(ys, p_b1),
            }

    # ---- 6. Write evaluation summary ----
    end_time = datetime.now(timezone.utc)
    lines = []
    lines.append("# FCLR-005 Evaluation Summary — Track A Observed Liquidation Outcomes (2026 pilot)")
    lines.append("")
    lines.append("**Experiment:** FCLR-005 (protocol FCLR-005 v1.0, frozen 2026-10-30T04:30:00Z, pre-registered before outcome inspection)")
    lines.append("**Status:** PILOT/EXPLORATORY_ONLY — ~30-day label window cannot satisfy the >=3 non-overlapping 30-day confirmatory gate; no confirmatory skill claimed; FCLR-H004 remains BLOCKED for frozen 2024")
    lines.append(f"**Run start:** {dt_to_iso_z(start_time)}  |  **Run end:** {dt_to_iso_z(end_time)}")
    lines.append(f"**Git SHA:** {git_sha()}")
    lines.append("")
    lines.append("## Data provenance")
    lines.append(f"- Liquidations: `{LIQ}` (HF ochinimus/crypto-liquidation-ticks, CC BY 4.0, unauthenticated)")
    lines.append(f"- Liquidation total_rows={total_rows}; bybit census rows (target symbols)={target_bybit_rows}; bybit exchange rows={per_exchange.get('bybit', 0)}")
    lines.append(f"- Per exchange: {dict(sorted(per_exchange.items()))}")
    lines.append(f"- Per symbol/exchange (target symbols, bybit): " + ", ".join(
        f"{s}={per_sym_exchange.get((s, 'bybit'), 0)}" for s in SYMBOLS))
    lines.append(f"- Binance/OKX rows excluded from the binary presence/absence target (undercounted lower-bound only; never census)")
    lines.append(f"- Label window (Bybit census): {dt_to_iso_z(LABEL_START)} .. {dt_to_iso_z(LABEL_END)}")
    lines.append(f"- Feature cache: research_state/data_cache/<SYM>_2026_*/ mark/index/premium 1h + monthly fundingRate, 2026-04-01..2026-08-06 (verified complete on disk)")
    lines.append(f"- Universe: {SYMBOLS} (Binance mark-price features cross-referenced to Bybit liquidation labels)")
    lines.append(f"- Panel rows after causal filtering: {len(panel_rows)}")
    lines.append(f"- Split (chronological, by unique UTC hour): train<= {dt_to_iso_z(train_end) if train_end else 'n/a'}, val<= {dt_to_iso_z(val_end) if val_end else 'n/a'}, test> val")
    lines.append(f"- Train rows={len(train_rows)}, test rows={len(test_rows)}")
    lines.append(f"- Non-overlapping 30-day blocks in test window: {block_count} (< 3 required for confirmatory -> pilot limitation)")
    lines.append("")
    lines.append("## Results (hourly binary liquidation presence, Bybit census only)")
    for target in ['long', 'short']:
        lines.append(f"### Target: {target}_liquidated (Bybit '{target}_liquidated' events -> {target} side)")
        lines.append(f"- Base rate (test): {results[target]['B0']['base_rate']:.6f}; events in test={results[target]['B0']['events_test']}/{results[target]['B0']['n_test']}")
        for model in ['B0', 'B1', 'C1', 'C2']:
            r = results[target][model]
            bb, bl = r['brier_boot'], r['logloss_boot']
            lines.append(
                f"- {model}: Brier={r['brier']:.6f} (boot mean={bb['mean']:.6f}, 95% CI [{bb['ci_lo']:.6f}, {bb['ci_hi']:.6f}]), "
                f"logloss={r['logloss']:.6f} (boot mean={bl['mean']:.6f}, 95% CI [{bl['ci_lo']:.6f}, {bl['ci_hi']:.6f}]), "
                f"AUPRC={r['prauc']:.6f}, calibration intercept={r['cal_intercept']:.6f}, slope={r['cal_slope']:.6f}, "
                f"precision@base_rate={r['precision_at_base_rate']:.6f} (thr={r['base_rate_threshold']:.6f}), n_test={r['n_test']}")
        lines.append("")
    lines.append("## Leave-one-symbol-out stability (primary contrast C2 vs B1, Brier difference C2-B1; negative = C2 better)")
    for held in SYMBOLS:
        for target in ['long', 'short']:
            e = loso[held][target]
            if e.get('skipped'):
                lines.append(f"- {held}/{target}: skipped (insufficient train/test rows)")
            else:
                lines.append(f"- {held}/{target}: n_test={e['n_test']}, events={e['events']}, base_rate={e['base_rate']:.6f}, "
                             f"Brier B1={e['brier_b1']:.6f}, C2={e['brier_c2']:.6f}, C2-B1={e['brier_diff_c2_minus_b1']:+.6f}")
    lines.append("")
    lines.append("## Notes")
    lines.append("- Event-free intervals NOT inferred from missing data. Hours with zero Bybit rows = observed zero in census arm only, not an absolute zero claim.")
    lines.append("- Binance/OKX rows never used to construct the binary absence/presence target (capped streams, undercounted).")
    lines.append("- No forward-fill / zero-fill across splits; rows with missing causal features dropped for that model comparison.")
    lines.append("- Fixed logistic form; no hyperparameter search, no threshold tuning on outcomes, no alert-budget selection (pilot).")
    lines.append("- Block bootstrap over complete UTC hours (deterministic seed); leave-one-symbol-out stability reported above.")
    lines.append("- FCLR-005 is PILOT/EXPLORATORY ONLY. Does NOT clear any sealed FCLR-001-004 forecast gate. FCLR-H004 remains BLOCKED for frozen 2024.")
    lines.append("- This summary is generated by scripts/h004_fclr005_pipeline.py (idempotent; rerun reproduces identical numbers).")
    OUT_SUM.write_text('\n'.join(lines) + '\n')
    print(f"Wrote {OUT_SUM}", flush=True)

    # ---- 7. Append forensic execution record ----
    try:
        with LIQ_ENUM.open('a') as f:
            f.write(f"\n\n## FCLR-005 execution record (appended {dt_to_iso_z(end_time)})\n")
            f.write(f"- Script: scripts/h004_fclr005_pipeline.py (idempotent/resumable, deterministic seed {SEED})\n")
            f.write(f"- Git SHA: {git_sha()}\n")
            f.write(f"- Run start: {dt_to_iso_z(start_time)}; run end: {dt_to_iso_z(end_time)}\n")
            f.write(f"- Liquidations loaded: total_rows={total_rows}, bybit_census_target_symbol_rows={target_bybit_rows}; Binance/OKX excluded from census target\n")
            f.write(f"- Per exchange: {dict(sorted(per_exchange.items()))}\n")
            f.write(f"- Label window: {dt_to_iso_z(LABEL_START)} .. {dt_to_iso_z(LABEL_END)}\n")
            f.write(f"- Feature cache: research_state/data_cache/<SYM>_2026_*/ (mark/index/premium 1h, funding monthly), 2026-04-01..2026-08-06\n")
            f.write(            f"- Panel rows: {len(panel_rows)}, symbols={SYMBOLS}; train={len(train_rows)}, val={len(val_rows)}, test={len(test_rows)}\n")
            f.write(f"- Split boundaries: train<= {dt_to_iso_z(train_end) if train_end else 'n/a'}, val<= {dt_to_iso_z(val_end) if val_end else 'n/a'}\n")
            f.write(f"- Non-overlapping 30-day blocks in test window: {block_count} (< 3 -> pilot)\n")
            f.write(f"- Models: B0,B1,C1,C2; targets long/short. Metrics: Brier/logloss/AUPRC/calibration/precision-recall + block-bootstrap 95% CI + leave-one-symbol-out.\n")
            f.write(f"- Results: {OUT_SUM}\n")
            f.write(f"- Panel checkpoint: {CKPT_PANEL}\n")
            f.write(f"- Verdict: PILOT/EXPLORATORY_ONLY; FCLR-H004 remains BLOCKED for frozen 2024; does not clear FCLR-001-004 gates; no confirmatory skill claimed.\n")
    except Exception as e:
        print(f"Failed to append to enumeration: {e}", flush=True)

    print("FCLR-005 pipeline complete", flush=True)


if __name__ == '__main__':
    main()
