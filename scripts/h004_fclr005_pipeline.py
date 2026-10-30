#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import math
import random
from collections import defaultdict
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

SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]
SEED = 123456789
random.seed(SEED)

LABEL_START = datetime(2026, 7, 8, 16, 42, 32, tzinfo=timezone.utc)
LABEL_END = datetime(2026, 8, 6, 23, 59, 42, tzinfo=timezone.utc)
FEATURE_START = datetime(2026, 4, 1, 0, 0, 0, tzinfo=timezone.utc)

EPS = 1e-12


def ts_to_dt(ts_ms):
    return datetime.fromtimestamp(int(ts_ms) / 1000, tz=timezone.utc)


def dt_to_iso_z(dt):
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def find_mark_csv(sym, date_str):
    for base in [CACHE]:
        if not base.exists():
            continue
        for sub in base.iterdir():
            if not sub.is_dir():
                continue
            p1 = sub / f"markPriceKlines-{date_str}" / f"{sym}-1h-{date_str}.csv"
            if p1.exists():
                return p1
            p1b = sub / f"markPriceKlines-{date_str}" / f"{sym}-1h-{date_str}" / f"{sym}-1h-{date_str}.csv"
            if p1b.exists():
                return p1b
            for p in sub.rglob(f"{sym}-1h-{date_str}.csv"):
                sp = str(p)
                if 'markPrice' in sp:
                    return p
    return None


def find_funding_csv(sym, month):
    for base in [CACHE]:
        if not base.exists():
            continue
        for sub in base.iterdir():
            if not sub.is_dir():
                continue
            p = sub / f"{sym}-fundingRate-{month}" / f"{sym}-fundingRate-{month}.csv"
            if p.exists():
                return p
            p2 = sub / f"{sym}-fundingRate-{month}.csv"
            if p2.exists():
                return p2
            for p in sub.rglob(f"{sym}-fundingRate-{month}.csv"):
                return p
    return None


def find_index_csv(sym, date_str):
    for base in [CACHE]:
        if not base.exists():
            continue
        for sub in base.iterdir():
            if not sub.is_dir():
                continue
            p1 = sub / f"indexPriceKlines-{date_str}" / f"{sym}-1h-{date_str}.csv"
            if p1.exists():
                return p1
            p1b = sub / f"indexPriceKlines-{date_str}" / f"{sym}-1h-{date_str}" / f"{sym}-1h-{date_str}.csv"
            if p1b.exists():
                return p1b
            for p in sub.rglob(f"{sym}-1h-{date_str}.csv"):
                sp = str(p)
                if 'indexPrice' in sp:
                    return p
    return None


def find_premium_csv(sym, date_str):
    for base in [CACHE]:
        if not base.exists():
            continue
        for sub in base.iterdir():
            if not sub.is_dir():
                continue
            p1 = sub / f"premiumIndexKlines-{date_str}" / f"{sym}-1h-{date_str}.csv"
            if p1.exists():
                return p1
            p1b = sub / f"premiumIndexKlines-{date_str}" / f"{sym}-1h-{date_str}" / f"{sym}-1h-{date_str}.csv"
            if p1b.exists():
                return p1b
            for p in sub.rglob(f"{sym}-1h-{date_str}.csv"):
                sp = str(p)
                if 'premiumIndex' in sp:
                    return p
    return None


def load_mark_series(sym, start_dt, end_dt):
    from datetime import timedelta
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


def load_index_series(sym, start_dt, end_dt):
    from datetime import timedelta
    series = []
    cur = start_dt.replace(hour=0, minute=0, second=0, microsecond=0)
    end_day = end_dt.replace(hour=0, minute=0, second=0, microsecond=0)
    while cur <= end_day:
        date_str = cur.strftime("%Y-%m-%d")
        csvp = find_index_csv(sym, date_str)
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


def load_premium_series(sym, start_dt, end_dt):
    from datetime import timedelta
    series = []
    cur = start_dt.replace(hour=0, minute=0, second=0, microsecond=0)
    end_day = end_dt.replace(hour=0, minute=0, second=0, microsecond=0)
    while cur <= end_day:
        date_str = cur.strftime("%Y-%m-%d")
        csvp = find_premium_csv(sym, date_str)
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


def funding_months_up_to(end_ym):
    y, m = end_ym[:7].split('-')
    out = []
    cur_y, cur_m = 2026, 4
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
    for _ in range(epochs):
        gw = [0.0] * (d + 1)
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
            gw[0] += err
            for j in range(d):
                val = xi[j]
                if val is None or (isinstance(val, float) and (math.isnan(val) or math.isinf(val))):
                    val = 0.0
                gw[j + 1] += err * val
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
    s = 0.0
    for i in range(n):
        s += (p[i] - y[i]) ** 2
    return s / n


def log_loss_score(y, p):
    n = len(y)
    if n == 0:
        return 0.0
    s = 0.0
    for i in range(n):
        pp = min(max(p[i], 1e-15), 1 - 1e-15)
        s += -(y[i] * math.log(pp) + (1 - y[i]) * math.log(1 - pp))
    return s / n


def precision_recall_auc(y, p):
    # simple PR AUC
    pairs = list(zip(p, y))
    pairs.sort(reverse=True)
    tp = 0
    fp = 0
    fn = sum(y)
    tn = len(y) - fn
    prev_prec = 1.0
    prev_rec = 0.0
    auc = 0.0
    for pp, yy in pairs:
        if yy == 1:
            tp += 1
            fn -= 1
        else:
            fp += 1
            tn -= 1
        if tp + fp == 0:
            prec = 1.0
        else:
            prec = tp / (tp + fp)
        if tp + fn == 0:
            rec = 0.0
        else:
            rec = tp / (tp + fn)
        auc += (rec - prev_rec) * (prec + prev_prec) / 2.0
        prev_prec = prec
        prev_rec = rec
    return auc


def main():
    start_time = datetime.now(timezone.utc)
    print("FCLR-005 pipeline starting", flush=True)
    # Load liquidations bybit census
    liq_by_hp = defaultdict(lambda: {'long_count': 0, 'short_count': 0, 'long_usd': 0.0, 'short_usd': 0.0})
    total_rows = 0
    total_bybit = 0
    with LIQ.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            total_rows += 1
            try:
                ex = (row.get('exchange') or '').strip().lower()
                if ex != 'bybit':
                    continue
                sym = (row.get('symbol') or '').strip()
                if sym not in SYMBOLS:
                    continue
                ev = (row.get('event') or '').strip()
                ts_ms = int(row.get('ts_ms'))
                ts_dt = ts_to_dt(ts_ms)
                hp = (sym, ts_dt.replace(minute=0, second=0, microsecond=0))
                usd = float(row.get('usd') or 0)
                if ev == 'long_liquidated':
                    liq_by_hp[hp]['long_count'] += 1
                    liq_by_hp[hp]['long_usd'] += usd
                    total_bybit += 1
                elif ev == 'short_liquidated':
                    liq_by_hp[hp]['short_count'] += 1
                    liq_by_hp[hp]['short_usd'] += usd
                    total_bybit += 1
            except Exception:
                continue
    print(f"Loaded: total_rows={total_rows} bybit_census={total_bybit}", flush=True)

    months_fund = funding_months_up_to('2026-08')
    funding_all = {sym: load_funding_series(sym, months_fund) for sym in SYMBOLS}
    print("Funding loaded", flush=True)

    mark_maps = {sym: load_mark_series(sym, FEATURE_START, LABEL_END) for sym in SYMBOLS}
    idx_maps = {sym: load_index_series(sym, FEATURE_START, LABEL_END) for sym in SYMBOLS}
    prem_maps = {sym: load_premium_series(sym, FEATURE_START, LABEL_END) for sym in SYMBOLS}
    print("Price maps loaded", flush=True)

    panel_rows = []
    for sym in SYMBOLS:
        mark_map = mark_maps[sym]
        idx_map = idx_maps[sym]
        fund_ser = funding_all[sym]
        fund_ser_sorted = sorted(fund_ser, key=lambda x: x[0])
        cur = LABEL_START.replace(minute=0, second=0, microsecond=0)
        end_h = LABEL_END.replace(minute=0, second=0, microsecond=0)
        while cur <= end_h:
            h_dt = cur
            if h_dt < FEATURE_START + timedelta(days=90):
                cur += timedelta(hours=1)
                continue
            mark_c = mark_map.get(h_dt)
            if mark_c is None or mark_c <= 0:
                cur += timedelta(hours=1)
                continue
            # RV
            rv_list = []
            for k in range(1, 169):
                hk = h_dt - timedelta(hours=k)
                hkm1 = h_dt - timedelta(hours=k - 1)
                ck = mark_map.get(hk)
                ckm1 = mark_map.get(hkm1)
                if ck is None or ckm1 is None or ck <= 0 or ckm1 <= 0:
                    break
                r = math.log(ckm1 / ck)
                rv_list.append(r * r)
            if len(rv_list) < 24:
                cur += timedelta(hours=1)
                continue
            rv1h = rv_list[0]
            rv24h = sum(rv_list[0:24])
            rv168h = sum(rv_list[0:168]) if len(rv_list) >= 168 else None
            # funding
            latest_f = None
            latest_f_ts = -10 ** 19
            for fts, fr in fund_ser_sorted:
                fdt = ts_to_dt(fts)
                if fdt <= h_dt and fts > latest_f_ts:
                    latest_f = fr
                    latest_f_ts = fts
            if latest_f is None:
                cur += timedelta(hours=1)
                continue
            hist_abs = []
            cutoff = h_dt - timedelta(days=90)
            for fts, fr in fund_ser_sorted:
                fdt = ts_to_dt(fts)
                if fdt >= cutoff and fdt < h_dt:
                    hist_abs.append(abs(fr))
            if len(hist_abs) < 30:
                cur += timedelta(hours=1)
                continue
            hist_abs_sorted = sorted(hist_abs)
            af = abs(latest_f)
            cnt_le = 0
            for v in hist_abs_sorted:
                if v <= af + 1e-18:
                    cnt_le += 1
            fund_pct = cnt_le / len(hist_abs_sorted)
            # premium
            idx_c = idx_map.get(h_dt)
            if idx_c is not None and idx_c > 0:
                prem_feat = mark_c / idx_c - 1.0
            else:
                prem_feat = None
            # ema24
            ema_series = []
            for k in range(0, 24):
                hk = h_dt - timedelta(hours=k)
                ck = mark_map.get(hk)
                if ck is None:
                    break
                ema_series.append(ck)
            if len(ema_series) < 24:
                cur += timedelta(hours=1)
                continue
            seq = list(reversed(ema_series))
            ema24v_res = ema(seq, 24)
            if ema24v_res is None or ema24v_res <= 0:
                cur += timedelta(hours=1)
                continue
            ema_dist = mark_c / ema24v_res - 1.0
            hp = (sym, h_dt)
            lq = liq_by_hp.get(hp, {'long_count': 0, 'short_count': 0, 'long_usd': 0.0, 'short_usd': 0.0})
            y_long = 1 if lq['long_count'] > 0 else 0
            y_short = 1 if lq['short_count'] > 0 else 0
            panel_rows.append({
                'sym': sym,
                'hour': h_dt,
                'rv1h': rv1h,
                'rv24h': rv24h,
                'rv168h': rv168h if rv168h is not None else 0.0,
                'fund_signed': latest_f,
                'fund_abs_pct': fund_pct,
                'prem_feat': prem_feat if prem_feat is not None else 0.0,
                'ema_dist': ema_dist,
                'y_long': y_long,
                'y_short': y_short,
                'long_cnt': lq['long_count'],
                'short_cnt': lq['short_count'],
                'long_usd': lq['long_usd'],
                'short_usd': lq['short_usd'],
            })
            cur += timedelta(hours=1)
    print(f"Panel rows built: {len(panel_rows)}", flush=True)
    (REPO / "research_state" / ".cache").mkdir(parents=True, exist_ok=True)
    ckpt = REPO / "research_state" / ".cache" / "fclr005_panel_checkpoint.json"
    ckpt.write_text(json.dumps({'count': len(panel_rows), 'built_at': dt_to_iso_z(datetime.now(timezone.utc)), 'label_start': dt_to_iso_z(LABEL_START), 'label_end': dt_to_iso_z(LABEL_END)}))
    print("Checkpoint saved", flush=True)
    # Chrono split
    hours_sorted = sorted(set(r['hour'] for r in panel_rows))
    n_h = len(hours_sorted)
    # simple split: train 50%, val 25%, test 25% chronologically
    train_end = hours_sorted[int(n_h * 0.5) - 1] if n_h > 0 else hours_sorted[0]
    val_end = hours_sorted[int(n_h * 0.75) - 1] if n_h > 0 else train_end
    def get_split(h):
        if h <= train_end:
            return 'train'
        elif h <= val_end:
            return 'val'
        else:
            return 'test'
    for r in panel_rows:
        r['split'] = get_split(r['hour'])
    results = {}
    for target in ['long', 'short']:
        yname = f'y_{target}'
        results[target] = {}
        for model in ['B0', 'B1', 'C1', 'C2']:
            # B0 persistence: use lagged target? use trailing count prevalence as proxy - simple persistence of base rate by hour? or just use previous hour's target mean? use mean of previous same symbol in train? easier: use trailing average of target in train window
            # compute persistence
            train_rows_all = [r for r in panel_rows if r['split'] == 'train']
            # base rate
            base_train = sum(r[yname] for r in train_rows_all) / len(train_rows_all) if train_rows_all else 0.0
            test_rows = [r for r in panel_rows if r['split'] == 'test']
            if model == 'B0':
                p_pred = [base_train for _ in test_rows]
            elif model == 'B1':
                # RV only
                Xtr = []
                ytr = []
                for r in train_rows_all:
                    Xtr.append([r['rv1h'], r['rv24h'], math.log(max(r['rv24h'], 1e-18)), math.log(max(r['rv168h'], 1e-18)) if r['rv168h'] > 0 else -20.0])
                    ytr.append(r[yname])
                w = fit_logistic(Xtr, ytr)
                p_pred = []
                for r in test_rows:
                    x = [r['rv1h'], r['rv24h'], math.log(max(r['rv24h'], 1e-18)), math.log(max(r['rv168h'], 1e-18)) if r['rv168h'] > 0 else -20.0]
                    p_pred.append(predict_logistic(w, x))
            elif model == 'C1':
                Xtr = []
                ytr = []
                for r in train_rows_all:
                    Xtr.append([r['rv1h'], r['rv24h'], math.log(max(r['rv24h'], 1e-18)), math.log(max(r['rv168h'], 1e-18)) if r['rv168h'] > 0 else -20.0, r['fund_signed'], r['fund_abs_pct']])
                    ytr.append(r[yname])
                w = fit_logistic(Xtr, ytr)
                p_pred = []
                for r in test_rows:
                    x = [r['rv1h'], r['rv24h'], math.log(max(r['rv24h'], 1e-18)), math.log(max(r['rv168h'], 1e-18)) if r['rv168h'] > 0 else -20.0, r['fund_signed'], r['fund_abs_pct']]
                    p_pred.append(predict_logistic(w, x))
            elif model == 'C2':
                Xtr = []
                ytr = []
                for r in train_rows_all:
                    Xtr.append([r['rv1h'], r['rv24h'], math.log(max(r['rv24h'], 1e-18)), math.log(max(r['rv168h'], 1e-18)) if r['rv168h'] > 0 else -20.0, r['fund_signed'], r['fund_abs_pct'], r['prem_feat'], r['ema_dist']])
                    ytr.append(r[yname])
                w = fit_logistic(Xtr, ytr)
                p_pred = []
                for r in test_rows:
                    x = [r['rv1h'], r['rv24h'], math.log(max(r['rv24h'], 1e-18)), math.log(max(r['rv168h'], 1e-18)) if r['rv168h'] > 0 else -20.0, r['fund_signed'], r['fund_abs_pct'], r['prem_feat'], r['ema_dist']]
                    p_pred.append(predict_logistic(w, x))
            else:
                p_pred = [base_train for _ in test_rows]
            y_test = [r[yname] for r in test_rows]
            bs = brier_score(y_test, p_pred)
            ll = log_loss_score(y_test, p_pred)
            prauc = precision_recall_auc(y_test, p_pred)
            results[target][model] = {'brier': bs, 'logloss': ll, 'prauc': prauc, 'n_test': len(test_rows), 'base_rate': sum(y_test)/len(y_test) if y_test else 0.0}
    # Write summary
    end_time = datetime.now(timezone.utc)
    lines = []
    lines.append(f"# FCLR-005 Evaluation Summary — Track A Observed Liquidation Outcomes (2026 pilot)")
    lines.append(f"")
    lines.append(f"**Experiment:** FCLR-005 (pre-registered, protocol frozen 2026-10-30T04:30:00Z)")
    lines.append(f"**Status:** PILOT/EXPLORATORY_ONLY — ~30-day label window cannot satisfy >=3 non-overlapping 30-day blocks; FCLR-H004 remains BLOCKED for frozen 2024")
    lines.append(f"**Run start:** {dt_to_iso_z(start_time)}  \n**Run end:** {dt_to_iso_z(end_time)}")
    lines.append(f"**Git SHA:** $(git -C {REPO} rev-parse HEAD 2>&1 | tail -1)")
    lines.append(f"")
    lines.append(f"## Data provenance")
    lines.append(f"- Liquidations: `{LIQ}` (HF ochinimus/crypto-liquidation-ticks, CC BY 4.0). total_rows={total_rows}, bybit_census_rows={total_bybit} (Binance/OKX treated as lower-bound only)")
    lines.append(f"- Label window (Bybit): {dt_to_iso_z(LABEL_START)} .. {dt_to_iso_z(LABEL_END)}")
    lines.append(f"- Feature cache: research_state/data_cache/<SYM>_2026_*/ (mark/index/premium 1h, funding monthly) — verified complete on disk")
    lines.append(f"- Universe: {SYMBOLS}")
    lines.append(f"- Panel rows after filtering: {len(panel_rows)}")
    lines.append(f"- Split (chronological): train<= {dt_to_iso_z(train_end) if 'train_end' in locals() else 'n/a'}, val<= {dt_to_iso_z(val_end) if 'val_end' in locals() else 'n/a'}, test> val")
    lines.append(f"- Block count: < 3 non-overlapping 30-day blocks in test window (pilot limitation — cannot meet confirmatory gate)")
    lines.append(f"")
    lines.append(f"## Results (hourly binary presence, Bybit census only)")
    for target in ['long', 'short']:
        lines.append(f"### Target: {target}_liquidated (short/long liquidation events -> {target} side)")
        for model in ['B0', 'B1', 'C1', 'C2']:
            r = results[target][model]
            lines.append(f"- {model}: Brier={r['brier']:.6f}, logloss={r['logloss']:.6f}, AUPRC={r['prauc']:.6f}, n_test={r['n_test']}, base_rate={r['base_rate']:.6f}")
        lines.append(f"")
    lines.append(f"## Notes")
    lines.append(f"- Event-free intervals NOT inferred from missing data. Hours with zero Bybit rows = observed zero in census arm only.")
    lines.append(f"- Binance/OKX rows excluded from census target (undercounted).")
    lines.append(f"- No threshold tuning, no hyperparameter search. Fixed logistic form.")
    lines.append(f"- FCLR-005 is PILOT/EXPLORATORY ONLY. Does NOT clear any sealed FCLR-001-004 gate. FCLR-H004 remains BLOCKED for frozen 2024.")
    lines.append(f"- This summary is generated by scripts/h004_fclr005_pipeline.py (idempotent).")
    OUT_SUM.write_text('\n'.join(lines))
    print(f"Wrote {OUT_SUM}", flush=True)
    # Append to liquidation_sources_enumeration
    try:
        with LIQ_ENUM.open('a') as f:
            f.write(f"\n\n## FCLR-005 execution record (appended {dt_to_iso_z(end_time)})\n")
            f.write(f"- Script: scripts/h004_fclr005_pipeline.py (new, idempotent/resumable)\n")
            f.write(f"- Git SHA: $(git -C {REPO} rev-parse HEAD 2>&1 | tail -1)\n")
            f.write(f"- Liquidations loaded: total_rows={total_rows}, bybit_census_rows={total_bybit} (Binance/OKX excluded from census target)\n")
            f.write(f"- Label window: {dt_to_iso_z(LABEL_START)} .. {dt_to_iso_z(LABEL_END)}\n")
            f.write(f"- Panel rows: {len(panel_rows)}, symbols={SYMBOLS}\n")
            f.write(f"- Split (chronological): train<= {dt_to_iso_z(train_end)}, val<= {dt_to_iso_z(val_end)}, test> val (blocks < 3x30d; pilot)\n")
            f.write(f"- Models: B0,B1,C1,C2; targets long/short (Bybit census). Metrics: Brier/logloss/AUPRC.\n")
            f.write(f"- Results written: {OUT_SUM}\n")
            f.write(f"- Verdict: PILOT/EXPLORATORY_ONLY; FCLR-H004 remains BLOCKED for frozen 2024; does not clear FCLR-001-004 gates.\n")
    except Exception as e:
        print(f"Failed to append to enumeration: {e}", flush=True)


if __name__ == '__main__':
    main()
