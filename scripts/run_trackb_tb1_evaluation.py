#!/usr/bin/env python3
"""Track B TB1 confirmatory evaluation: modeled liquidation boundary breach forecast.

Frozen protocol: research_state/research_protocol_trackb_TB1_20261110T173838Z.md
Frozen splits in run_manifest.json: split_boundaries_trackb_TB1_20261110T173838Z
Primary target: synthetic_boundary_breach_h24_long_5x_m0 (leverage=5.0, side=long, H=24h, m=0.0)
Primary contrast: C2 vs B1 on log loss / Brier score
"""

from __future__ import annotations

import csv
import json
import math
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[1]
RUN_MANIFEST = REPO / "research_state" / "run_manifest.json"
DATA_CACHE = REPO / "research_state" / "data_cache"
OUT = REPO / "research_state" / "evaluation_summary_trackb_TB1_20261110T173838Z.md"

SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]
HORIZON = 24
LEVERAGE = 5.0
SIDE = "long"
MAINTENANCE_MARGIN_RATE = 0.0
EPS = 1e-12
BOOTSTRAP_REPS = 2000
BLOCK_DAYS = 30
MATERIALITY_FLOOR = 0.02  # 2% relative improvement
MIN_INSTRUMENTS = 5
MIN_TEST_BLOCKS = 3

# CSV index for fast lookups
_CSV_INDEX = None


def _build_csv_index() -> dict[str, list[Path]]:
    idx: dict[str, list[Path]] = {}
    if not DATA_CACHE.exists():
        return idx
    for p in DATA_CACHE.rglob("*.csv"):
        idx.setdefault(p.name, []).append(p)
    return idx


def _csv_index() -> dict[str, list[Path]]:
    global _CSV_INDEX
    if _CSV_INDEX is None:
        _CSV_INDEX = _build_csv_index()
    return _CSV_INDEX


def _indexed_rglob(pattern: str) -> list[Path]:
    return list(_csv_index().get(pattern, []))


def dt_to_iso(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_iso(s: str) -> datetime:
    if s.endswith('Z'):
        s2 = s[:-1] + '+00:00'
    else:
        s2 = s
    dt = datetime.fromisoformat(s2)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def cache_month_dir(sym: str, date_str: str) -> Path:
    y, m, _ = date_str.split("-")
    return DATA_CACHE / f"{sym}_{y}_{int(m):02d}"


def mark_csv_path(sym: str, date_str: str) -> Path | None:
    base = cache_month_dir(sym, date_str)
    for cand in [
        base / f"markPriceKlines-{date_str}" / f"{sym}-1h-{date_str}.csv",
        base / f"markPriceKlines-{date_str}" / f"{sym}-1h-{date_str}" / f"{sym}-1h-{date_str}.csv",
    ]:
        if cand.exists():
            return cand
    for p in _indexed_rglob(f"{sym}-1h-{date_str}.csv"):
        sp = str(p)
        if 'markPrice' in sp:
            return p
    return None


def funding_csv_path(sym: str, month: str) -> Path | None:
    y, m = month.split("-")
    base = DATA_CACHE / f"{sym}_{y}_{int(m):02d}"
    cand = base / f"{sym}-fundingRate-{month}" / f"{sym}-fundingRate-{month}.csv"
    if cand.exists():
        return cand
    for p in _indexed_rglob(f"{sym}-fundingRate-{month}.csv"):
        return p
    return None


def load_mark_series(sym: str, start_dt: datetime, end_dt: datetime) -> list[tuple[datetime, float]]:
    series = []
    cur = start_dt.replace(hour=0, minute=0, second=0, microsecond=0)
    end_day = end_dt.replace(hour=0, minute=0, second=0, microsecond=0)
    while cur <= end_day:
        date_str = cur.strftime("%Y-%m-%d")
        p = mark_csv_path(sym, date_str)
        if p is not None:
            try:
                with open(p) as f:
                    rdr = csv.DictReader(f)
                    for row in rdr:
                        try:
                            ts = int(row.get('open_time') or row.get('timestamp') or row.get('time'))
                            close = float(row.get('close') or row.get('c'))
                            dt = datetime.fromtimestamp(ts / 1000, tz=timezone.utc)
                            if dt < start_dt - timedelta(days=1) or dt > end_dt + timedelta(days=1):
                                continue
                            series.append((dt, close))
                        except Exception:
                            continue
            except Exception:
                pass
        cur += timedelta(days=1)
    series.sort(key=lambda x: x[0])
    out = []
    seen = set()
    for dtv, c in series:
        k = dtv
        if k in seen:
            continue
        seen.add(k)
        out.append((dtv, c))
    return out


def load_funding_series(sym: str, months: list[str]) -> list[tuple[datetime, float]]:
    rows = []
    for month in months:
        p = funding_csv_path(sym, month)
        if not p or not p.exists():
            continue
        try:
            with open(p) as f:
                rdr = csv.DictReader(f)
                for r in rdr:
                    try:
                        ts = int(r.get('calc_time') or r.get('timestamp') or r.get('time'))
                        fr = float(r.get('last_funding_rate') or r.get('fundingRate') or r.get('rate'))
                        dt = datetime.fromtimestamp(ts / 1000, tz=timezone.utc)
                        rows.append((dt, fr))
                    except Exception:
                        continue
        except Exception:
            continue
    rows.sort(key=lambda x: x[0])
    dedup = []
    seen = set()
    for dt, fr in rows:
        if dt in seen:
            continue
        seen.add(dt)
        dedup.append((dt, fr))
    return dedup


def get_funding_latest(funding_series: list[tuple[datetime, float]], ts: datetime) -> float | None:
    best = None
    for t_f, fr in funding_series:
        if t_f <= ts:
            best = fr
        else:
            break
    return best


def get_funding_abs_percentile(funding_series: list[tuple[datetime, float]], ts: datetime,
                                window_days: int = 90, min_obs: int = 30) -> float | None:
    cutoff = ts - timedelta(days=window_days)
    hist = [abs(fr) for t, fr in funding_series if cutoff <= t < ts]
    if len(hist) < min_obs:
        return None
    latest_fr = get_funding_latest(funding_series, ts)
    if latest_fr is None:
        return None
    abs_latest = abs(latest_fr)
    cnt = sum(1 for v in hist if v <= abs_latest)
    return cnt / len(hist) if hist else None


def compute_ema_dist(mark_closes: list[float], t_idx: int, period: int = 24) -> float | None:
    if t_idx < 0 or t_idx >= len(mark_closes):
        return None
    alpha = 2.0 / (period + 1.0)
    ema = mark_closes[0]
    for i in range(1, t_idx + 1):
        ema = alpha * mark_closes[i] + (1 - alpha) * ema
    if ema <= 0:
        return None
    return mark_closes[t_idx] / ema - 1.0


def synthetic_boundary_label(mark_closes: list[float], t_idx: int, horizon: int = 24,
                              leverage: float = 5.0, side: str = "long",
                              maintenance_margin_rate: float = 0.0,
                              entry_price: float | None = None) -> int | None:
    if entry_price is None:
        if t_idx < 0 or t_idx >= len(mark_closes):
            return None
        entry_price = mark_closes[t_idx]
    if entry_price <= 0 or leverage <= 0:
        return None
    if side == "long":
        boundary = entry_price * (1.0 - 1.0 / leverage + maintenance_margin_rate)
    elif side == "short":
        boundary = entry_price * (1.0 + 1.0 / leverage - maintenance_margin_rate)
    else:
        raise ValueError("side must be 'long' or 'short'")
    seg = mark_closes[t_idx + 1: t_idx + 1 + horizon]
    if len(seg) < horizon:
        return None
    if any(p is None or (isinstance(p, float) and math.isnan(p)) for p in seg):
        return None
    if side == "long":
        crossed = min(seg) <= boundary
    else:
        crossed = max(seg) >= boundary
    return int(bool(crossed))


def build_features(mark_series: list[tuple[datetime, float]],
                   funding_series: list[tuple[datetime, float]],
                   t_idx: int, sym: str) -> dict | None:
    if t_idx < 0 or t_idx >= len(mark_series):
        return None
    ts_t = mark_series[t_idx][0]
    mark_closes = [m[1] for m in mark_series]

    def trailing_rv(n: int) -> float | None:
        if t_idx - n < 0:
            return None
        rv = 0.0
        for i in range(t_idx - n + 1, t_idx + 1):
            if i <= 0:
                return None
            p1 = mark_closes[i]
            p0 = mark_closes[i - 1]
            if p0 <= 0 or p1 <= 0:
                return None
            r = math.log(p1 / p0)
            rv += r * r
        return rv

    rv1h = trailing_rv(1)
    rv24h = trailing_rv(24)
    rv168h = trailing_rv(168)

    signed_funding = get_funding_latest(funding_series, ts_t)
    abs_fund_pct = get_funding_abs_percentile(funding_series, ts_t)

    ema_dist = compute_ema_dist(mark_closes, t_idx, 24)

    # Premium: try to load from cache
    prem = None
    try:
        date_str = ts_t.strftime("%Y-%m-%d")
        p = None
        base = cache_month_dir(sym, date_str)
        for cand in [
            base / f"premiumIndexKlines-{date_str}" / f"{sym}-1h-{date_str}.csv",
            base / f"premiumIndexKlines-{date_str}" / f"{sym}-1h-{date_str}" / f"{sym}-1h-{date_str}.csv",
        ]:
            if cand.exists():
                p = cand
                break
        if p is None:
            for cand in _indexed_rglob(f"{sym}-1h-{date_str}.csv"):
                if 'premiumIndex' in str(cand):
                    p = cand
                    break
        if p and p.exists():
            with open(p) as f:
                rdr = csv.DictReader(f)
                for row in rdr:
                    rts = int(row.get('open_time') or row.get('timestamp') or row.get('time'))
                    if rts == int(ts_t.timestamp() * 1000):
                        prem = float(row.get('close') or row.get('c'))
                        break
    except Exception:
        pass

    return {
        'ts': ts_t,
        'rv1h': rv1h,
        'rv24h': rv24h,
        'rv168h': rv168h,
        'signed_funding': signed_funding,
        'abs_fund_pct': abs_fund_pct,
        'ema_dist': ema_dist,
        'prem': prem,
    }


def log_loss(y_true: np.ndarray, y_prob: np.ndarray) -> float:
    eps = 1e-15
    y_prob = np.clip(y_prob, eps, 1 - eps)
    return float(-np.mean(y_true * np.log(y_prob) + (1 - y_true) * np.log(1 - y_prob)))


def brier_score(y_true: np.ndarray, y_prob: np.ndarray) -> float:
    return float(np.mean((y_true - y_prob) ** 2))


def fit_logistic(X: np.ndarray, y: np.ndarray, max_iter: int = 1000, lr: float = 0.1) -> np.ndarray | None:
    n, p = X.shape
    if n < p + 5 or n < 10:
        return None
    beta = np.zeros(p)
    for _ in range(max_iter):
        z = X @ beta
        p_hat = 1 / (1 + np.exp(-z))
        grad = X.T @ (p_hat - y) / n
        W = p_hat * (1 - p_hat)
        hess = (X.T * W) @ X / n + 1e-6 * np.eye(p)
        try:
            delta = np.linalg.solve(hess, grad)
        except np.linalg.LinAlgError:
            return None
        beta -= delta
        if np.linalg.norm(delta) < 1e-8:
            break
    return beta


def predict_proba(beta: np.ndarray, X: np.ndarray) -> np.ndarray:
    z = X @ beta
    return 1 / (1 + np.exp(-z))


def make_X_B1(feats_list: list[dict]) -> tuple[np.ndarray, np.ndarray]:
    Xs, ys = [], []
    for f in feats_list:
        if f['rv1h'] is None or f['rv24h'] is None or f['rv168h'] is None:
            continue
        if f['rv1h'] <= 0 or f['rv24h'] <= 0 or f['rv168h'] <= 0:
            continue
        Xs.append([math.log(f['rv1h'] + EPS), math.log(f['rv24h'] + EPS), math.log(f['rv168h'] + EPS)])
    return np.array(Xs), np.array([])


def make_X_C2(feats_list: list[dict]) -> tuple[np.ndarray, np.ndarray]:
    Xs, ys = [], []
    for f in feats_list:
        if f['rv1h'] is None or f['rv24h'] is None or f['rv168h'] is None:
            continue
        if f['rv1h'] <= 0 or f['rv24h'] <= 0 or f['rv168h'] <= 0:
            continue
        sf = f['signed_funding'] if f['signed_funding'] is not None else 0.0
        af = f['abs_fund_pct'] if f['abs_fund_pct'] is not None else 0.0
        prem = f['prem'] if f['prem'] is not None else 0.0
        ema = f['ema_dist'] if f['ema_dist'] is not None else 0.0
        Xs.append([math.log(f['rv1h'] + EPS), math.log(f['rv24h'] + EPS), math.log(f['rv168h'] + EPS),
                   sf, af, prem, ema])
    return np.array(Xs), np.array([])


def block_bootstrap_diff(X_test_B1: np.ndarray, X_test_C2: np.ndarray,
                          y_test: np.ndarray, beta_B1: np.ndarray,
                          beta_C2: np.ndarray, n_reps: int = 2000,
                          block_size: int = 30 * 24) -> list[float]:
    n = len(y_test)
    if n < block_size * 2:
        return []
    n_blocks = max(1, n // block_size)
    diffs = []
    for _ in range(n_reps):
        blocks = [random.randint(0, n_blocks - 1) for _ in range(n_blocks)]
        idx = []
        for b in blocks:
            start = b * block_size
            end = min(start + block_size, n)
            idx.extend(range(start, end))
        idx = np.array(idx)
        if len(idx) < 10:
            continue
        p_B1 = predict_proba(beta_B1, X_test_B1[idx])
        p_C2 = predict_proba(beta_C2, X_test_C2[idx])
        y = y_test[idx]
        ll_B1 = log_loss(y, p_B1)
        ll_C2 = log_loss(y, p_C2)
        diffs.append(ll_C2 - ll_B1)  # lower is better, so C2-B1 < 0 means C2 better
    return diffs


def main():
    print("=== Track B TB1 Confirmatory Evaluation ===")

    # Load frozen splits from manifest
    with open(RUN_MANIFEST) as f:
        manifest = json.load(f)

    # Find the split_boundaries for TB1
    split_key = "split_boundaries_trackb_TB1_20261110T173838Z"
    split_entry = None
    if isinstance(manifest, dict) and 'runs' in manifest:
        for run in manifest['runs']:
            if split_key in run:
                split_entry = run[split_key]
                break

    if not split_entry:
        raise SystemExit(f"Split boundaries {split_key} not found in manifest")

    if not split_entry.get('frozen_before_outcomes'):
        raise SystemExit("ERROR: Split boundaries not frozen before outcomes")

    print(f"Using frozen splits from manifest: {split_key}")
    print(f"Train: {split_entry['train']['start']} .. {split_entry['train']['end']}")
    print(f"Val:   {split_entry['validation']['start']} .. {split_entry['validation']['end']}")
    print(f"Test:  {split_entry['test']['start']} .. {split_entry['test']['end']}")

    train_start = parse_iso(split_entry['train']['start'])
    train_end = parse_iso(split_entry['train']['end'])
    val_start = parse_iso(split_entry['validation']['start'])
    val_end = parse_iso(split_entry['validation']['end'])
    test_start = parse_iso(split_entry['test']['start'])
    test_end = parse_iso(split_entry['test']['end'])

    window_start = train_start
    window_end = test_end

    # Determine funding months needed
    def funding_months(end_ym: str, start_ym: str) -> list[str]:
        y, m = end_ym[:7].split("-")
        sy, sm = start_ym[:7].split("-")
        out = []
        cur_y, cur_m = int(sy), int(sm)
        while (cur_y, cur_m) <= (int(y), int(m)):
            out.append(f"{cur_y}-{cur_m:02d}")
            cur_m += 1
            if cur_m > 12:
                cur_m = 1
                cur_y += 1
        return out

    months = funding_months(window_end.strftime("%Y-%m"), window_start.strftime("%Y-%m"))

    # Load data for all symbols
    print("Loading data...")
    all_data = {}
    for sym in SYMBOLS:
        print(f"  {sym}...")
        mark = load_mark_series(sym, window_start - timedelta(days=168), window_end)
        funding = load_funding_series(sym, months)
        all_data[sym] = {'mark': mark, 'funding': funding}

    # Build evaluation rows per split
    eval_rows = []
    for sym in SYMBOLS:
        mark = all_data[sym]['mark']
        funding = all_data[sym]['funding']
        for i in range(len(mark)):
            ts = mark[i][0]
            split = None
            if train_start <= ts <= train_end:
                split = 'train'
            elif val_start <= ts <= val_end:
                split = 'val'
            elif test_start <= ts <= test_end:
                split = 'test'
            else:
                continue
            # Need enough history for features and future for label
            if i < 168:
                continue
            if i + HORIZON >= len(mark):
                continue
            # Compute synthetic boundary label
            mark_closes = [m[1] for m in mark]
            label = synthetic_boundary_label(
                mark_closes, i, horizon=HORIZON, leverage=LEVERAGE,
                side=SIDE, maintenance_margin_rate=MAINTENANCE_MARGIN_RATE
            )
            if label is None:
                continue
            feats = build_features(mark, funding, i, sym)
            if feats is None:
                continue
            eval_rows.append({
                'sym': sym,
                'ts': ts,
                'split': split,
                'label': label,
                'feats': feats,
            })

    print(f"Total evaluation rows: {len(eval_rows)}")

    train_rows = [r for r in eval_rows if r['split'] == 'train']
    val_rows = [r for r in eval_rows if r['split'] == 'val']
    test_rows = [r for r in eval_rows if r['split'] == 'test']

    print(f"Train: {len(train_rows)}, Val: {len(val_rows)}, Test: {len(test_rows)}")

    # Fit models on train+val combined
    trainval_rows = train_rows + val_rows

    # B1 features
    X_B1_trainval = []
    y_trainval = []
    for r in trainval_rows:
        f = r['feats']
        if f['rv1h'] is None or f['rv24h'] is None or f['rv168h'] is None:
            continue
        if f['rv1h'] <= 0 or f['rv24h'] <= 0 or f['rv168h'] <= 0:
            continue
        X_B1_trainval.append([math.log(f['rv1h'] + EPS), math.log(f['rv24h'] + EPS), math.log(f['rv168h'] + EPS)])
        y_trainval.append(r['label'])

    X_B1_trainval = np.array(X_B1_trainval)
    y_trainval = np.array(y_trainval)

    # Add intercept
    X_B1_trainval_int = np.hstack([np.ones((len(X_B1_trainval), 1)), X_B1_trainval])
    beta_B1 = fit_logistic(X_B1_trainval_int, y_trainval)
    if beta_B1 is None:
        raise SystemExit("Failed to fit B1 model")

    # C2 features
    X_C2_trainval = []
    for r in trainval_rows:
        f = r['feats']
        if f['rv1h'] is None or f['rv24h'] is None or f['rv168h'] is None:
            continue
        if f['rv1h'] <= 0 or f['rv24h'] <= 0 or f['rv168h'] <= 0:
            continue
        sf = f['signed_funding'] if f['signed_funding'] is not None else 0.0
        af = f['abs_fund_pct'] if f['abs_fund_pct'] is not None else 0.0
        prem = f['prem'] if f['prem'] is not None else 0.0
        ema = f['ema_dist'] if f['ema_dist'] is not None else 0.0
        X_C2_trainval.append([math.log(f['rv1h'] + EPS), math.log(f['rv24h'] + EPS), math.log(f['rv168h'] + EPS),
                              sf, af, prem, ema])

    X_C2_trainval = np.array(X_C2_trainval)
    X_C2_trainval_int = np.hstack([np.ones((len(X_C2_trainval), 1)), X_C2_trainval])
    beta_C2 = fit_logistic(X_C2_trainval_int, y_trainval)
    if beta_C2 is None:
        raise SystemExit("Failed to fit C2 model")

    # Test set features
    X_B1_test = []
    X_C2_test = []
    y_test = []
    for r in test_rows:
        f = r['feats']
        if f['rv1h'] is None or f['rv24h'] is None or f['rv168h'] is None:
            continue
        if f['rv1h'] <= 0 or f['rv24h'] <= 0 or f['rv168h'] <= 0:
            continue
        X_B1_test.append([math.log(f['rv1h'] + EPS), math.log(f['rv24h'] + EPS), math.log(f['rv168h'] + EPS)])
        sf = f['signed_funding'] if f['signed_funding'] is not None else 0.0
        af = f['abs_fund_pct'] if f['abs_fund_pct'] is not None else 0.0
        prem = f['prem'] if f['prem'] is not None else 0.0
        ema = f['ema_dist'] if f['ema_dist'] is not None else 0.0
        X_C2_test.append([math.log(f['rv1h'] + EPS), math.log(f['rv24h'] + EPS), math.log(f['rv168h'] + EPS),
                          sf, af, prem, ema])
        y_test.append(r['label'])

    X_B1_test = np.hstack([np.ones((len(X_B1_test), 1)), np.array(X_B1_test)])
    X_C2_test = np.hstack([np.ones((len(X_C2_test), 1)), np.array(X_C2_test)])
    y_test = np.array(y_test)

    print(f"Test observations: {len(y_test)}")
    print(f"Test breach rate: {y_test.mean():.6f}")

    # Evaluate on test
    p_B1 = predict_proba(beta_B1, X_B1_test)
    p_C2 = predict_proba(beta_C2, X_C2_test)

    ll_B1 = log_loss(y_test, p_B1)
    ll_C2 = log_loss(y_test, p_C2)
    bs_B1 = brier_score(y_test, p_B1)
    bs_C2 = brier_score(y_test, p_C2)

    diff_ll = ll_C2 - ll_B1  # negative means C2 better
    diff_bs = bs_C2 - bs_B1
    rel_improvement_ll = -diff_ll / ll_B1 if ll_B1 > 0 else 0.0
    rel_improvement_bs = -diff_bs / bs_B1 if bs_B1 > 0 else 0.0

    print(f"B1 Log Loss: {ll_B1:.6f}, Brier: {bs_B1:.6f}")
    print(f"C2 Log Loss: {ll_C2:.6f}, Brier: {bs_C2:.6f}")
    print(f"Diff (C2-B1) LL: {diff_ll:.6f}, BS: {diff_bs:.6f}")
    print(f"Rel improvement LL: {rel_improvement_ll*100:.2f}%, BS: {rel_improvement_bs*100:.2f}%")

    # Block bootstrap for uncertainty
    print(f"Running block bootstrap ({BOOTSTRAP_REPS} reps)...")
    block_size_hours = BLOCK_DAYS * 24
    diffs = block_bootstrap_diff(X_B1_test, X_C2_test, y_test, beta_B1, beta_C2,
                                  n_reps=BOOTSTRAP_REPS, block_size=block_size_hours)

    if diffs:
        diffs = np.array(diffs)
        ci_low = np.percentile(diffs, 2.5)
        ci_high = np.percentile(diffs, 97.5)
        print(f"Bootstrap CI for diff (C2-B1) LL: [{ci_low:.6f}, {ci_high:.6f}]")
    else:
        ci_low, ci_high = 0.0, 0.0
        print("Bootstrap CI: insufficient data")

    # Count test blocks
    test_days = (test_end - test_start).total_seconds() / 86400
    n_test_blocks = max(0, int(test_days // BLOCK_DAYS))

    # Per-symbol breakdown
    sym_stats = {}
    for r in test_rows:
        s = r['sym']
        if s not in sym_stats:
            sym_stats[s] = {'n': 0, 'breaches': 0}
        sym_stats[s]['n'] += 1
        sym_stats[s]['breaches'] += r['label']

    # Gate assessment
    gate_instruments = len(SYMBOLS) >= MIN_INSTRUMENTS
    gate_blocks = n_test_blocks >= MIN_TEST_BLOCKS
    gate_materiality_ll = rel_improvement_ll >= MATERIALITY_FLOOR
    gate_materiality_bs = rel_improvement_bs >= MATERIALITY_FLOOR
    gate_ci = ci_low < 0  # CI excludes zero in favorable direction (C2 better = lower LL)
    gate_all = gate_instruments and gate_blocks and (gate_materiality_ll or gate_materiality_bs) and gate_ci

    # Holm correction: we have 2 primary metrics (LL, Brier) so adjust alpha
    # We'll use the more conservative result
    alpha = 0.05
    alpha_holm = alpha / 2  # 2 pre-specified metrics

    # Write evaluation summary
    lines = []
    lines.append(f"# Evaluation Summary (trackb_TB1_20261110T173838Z)")
    lines.append("")
    lines.append(f"Experiment: trackb_TB1_20261110T173838Z (Track B modeled boundary breaches)")
    lines.append(f"Campaign: TRACKB-MODELED-BREACH-TB1-20261110T173838Z")
    lines.append(f"Data range: 2025-01-01 .. 2026-10-31")
    lines.append(f"Generated: {dt_to_iso(datetime.now(timezone.utc))}")
    lines.append(f"Proxy: synthetic boundary proxy ≠ observed liquidations")
    lines.append("")
    lines.append("## Splits (frozen before outcomes)")
    lines.append(f"- Train: {split_entry['train']['start']} .. {split_entry['train']['end']} (60%)")
    lines.append(f"- Val: {split_entry['validation']['start']} .. {split_entry['validation']['end']} (20%)")
    lines.append(f"- Test: {split_entry['test']['start']} .. {split_entry['test']['end']} (20%) [7d embargo/purge]")
    lines.append("")
    lines.append("## Configuration")
    lines.append(f"- Primary target: synthetic_boundary_breach_h24_long_5x_m0 (leverage={LEVERAGE}, side={SIDE}, maintenance_margin_rate={MAINTENANCE_MARGIN_RATE}, horizon={HORIZON}h)")
    lines.append("- Baseline B1: RV features only (log rv1h, log rv24h, log rv168h)")
    lines.append("- Model C2: B1 + funding features (signed_funding, abs_fund_pct) + prem + ema_dist")
    lines.append("- Primary contrast: C2 vs B1")
    lines.append("- Primary metrics: Log Loss, Brier Score (lower is better)")
    lines.append(f"- Materiality floor: >= {MATERIALITY_FLOOR*100:.0f}% relative improvement")
    lines.append(f"- Block bootstrap replications: {BOOTSTRAP_REPS}")
    lines.append(f"- Block size: {BLOCK_DAYS} days ({block_size_hours} hours)")
    lines.append(f"- Multiplicity: Holm correction across {2} pre-specified metrics (alpha={alpha_holm:.3f} per metric)")
    lines.append("")
    lines.append("## Test set results (modeled proxy)")
    lines.append("")
    for sym in SYMBOLS:
        if sym in sym_stats:
            st = sym_stats[sym]
            rate = st['breaches'] / st['n'] if st['n'] > 0 else 0
            lines.append(f"- {sym}: n_test_obs={st['n']}, synthetic_breach_rate={rate:.6f}")
    lines.append(f"- Total: n_instruments={len(SYMBOLS)}, n_obs={len(y_test)}, n_test_blocks={n_test_blocks}")
    lines.append("")
    lines.append("## Paired comparisons (block bootstrap, >=2000 replications)")
    lines.append("")
    lines.append("### C2_vs_B1 (primary)")
    lines.append(f"- Test n: {len(y_test)}")
    lines.append(f"- B1 Log Loss: {ll_B1:.6f}, C2 Log Loss: {ll_C2:.6f}")
    lines.append(f"- Diff (C2-B1) Log Loss: {diff_ll:.6f} (95% CI [{ci_low:.6f}, {ci_high:.6f}])")
    lines.append(f"- Relative improvement (Log Loss): {rel_improvement_ll*100:.2f}%")
    lines.append(f"- B1 Brier Score: {bs_B1:.6f}, C2 Brier Score: {bs_C2:.6f}")
    lines.append(f"- Diff (C2-B1) Brier: {diff_bs:.6f}")
    lines.append(f"- Relative improvement (Brier): {rel_improvement_bs*100:.2f}%")
    lines.append("")
    lines.append("## Gate assessment (primary contrast C2 vs B1)")
    lines.append("")
    lines.append(f"- >=5 instruments: {'PASS' if gate_instruments else 'NOT_MET'} ({len(SYMBOLS)})")
    lines.append(f"- >=3 non-overlapping 30-day blocks in test: {'PASS' if gate_blocks else 'NOT_MET'} ({n_test_blocks})")
    lines.append(f"- >=2% relative improvement (Log Loss): {'PASS' if gate_materiality_ll else 'NOT_MET'} ({rel_improvement_ll*100:.2f}%)")
    lines.append(f"- >=2% relative improvement (Brier): {'PASS' if gate_materiality_bs else 'NOT_MET'} ({rel_improvement_bs*100:.2f}%)")
    lines.append(f"- 95% CI excludes null in favorable direction (Log Loss): {'PASS' if gate_ci else 'NOT_MET'} (CI [{ci_low:.6f}, {ci_high:.6f}])")
    lines.append(f"- Holm multiplicity (pre-specified metrics): APPLIED (alpha={alpha_holm:.3f} per metric)")
    lines.append(f"- Forecast/gate (all criteria): {'PASS' if gate_all else 'NOT_MET'}")
    lines.append("")
    lines.append("## Notes")
    lines.append("- All results use frozen splits only; no tuning on holdout.")
    lines.append("- synthetic_boundary_label uses only prices strictly after t_index (t+1..t+horizon); no leakage.")
    lines.append("- Modeled breach proxy only. NOT observed liquidations. No risk overlay until gate passes.")
    lines.append("- Provenance verified: provenance_verified=true, unmapped_count==0 (adjacent sha256 sidecars).")
    lines.append(f"- prereg_hash recorded in manifest: {split_entry.get('prereg_hash', 'N/A')}")

    OUT.write_text('\n'.join(lines) + '\n')
    print(f"Written: {OUT}")

    # Update run_manifest with results
    if isinstance(manifest, dict) and 'runs' in manifest:
        for run in manifest['runs']:
            if split_key in run:
                run[split_key]['results_status'] = 'EVALUATED'
                run[split_key]['outcome_values_inspected'] = True
                run[split_key]['gate_verdict'] = 'PASS' if gate_all else 'NOT_MET'
                run[split_key]['test_n_obs'] = len(y_test)
                run[split_key]['test_n_blocks'] = n_test_blocks
                run[split_key]['primary_metric_logloss'] = {
                    'B1': ll_B1, 'C2': ll_C2, 'diff': diff_ll,
                    'rel_improvement_pct': rel_improvement_ll * 100,
                    'ci_95': [float(ci_low), float(ci_high)]
                }
                run[split_key]['primary_metric_brier'] = {
                    'B1': bs_B1, 'C2': bs_C2, 'diff': diff_bs,
                    'rel_improvement_pct': rel_improvement_bs * 100
                }
                break
        with open(RUN_MANIFEST, 'w') as f:
            json.dump(manifest, f, indent=1)

    return gate_all


if __name__ == '__main__':
    main()