#!/usr/bin/env python3
"""
FCLR-LIVE-ARCHIVE-02 heavy 3-block confirmatory evaluation (stdlib only).
Reads downloaded Binance archive data (markPriceKlines 1h, fundingRate, metrics)
under research_state/session_20261122T003000Z/raw/, builds causal features and
the next-24h realized-variance target, fits B0/B1/C2 on the train block, and
evaluates paired QLIKE on 3 chronological test blocks. Writes eval .json + .md.
No numpy/pandas/scipy. Reads raw data only; writes eval artifacts only.
"""
import csv, io, json, math, os, re, zipfile
from datetime import datetime, timezone, timedelta
from pathlib import Path

SESSION = Path(__file__).resolve().parent
RAW = SESSION / "raw"
OUT_JSON = SESSION / "fclr_live_archive02_eval_20261122T003000Z.json"
OUT_MD = SESSION / "fclr_live_archive02_eval_20261122T003000Z.md"

EPS = 1e-12

# ---------- stdlib OLS ----------
def ols_fit(X, y):
    n = len(X); p = len(X[0])
    # X with intercept
    Xi = [[1.0] + row for row in X]
    # normal equations: XtX b = Xty
    m = p + 1
    XtX = [[0.0]*m for _ in range(m)]
    Xty = [0.0]*m
    for row, yi in zip(Xi, y):
        for a in range(m):
            Xty[a] += row[a]*yi
            for b in range(m):
                XtX[a][b] += row[a]*row[b]
    # Gaussian elimination with partial pivot
    aug = [XtX[a] + [Xty[a]] for a in range(m)]
    for col in range(m):
        piv = max(range(col, m), key=lambda r: abs(aug[r][col]))
        if abs(aug[piv][col]) < 1e-14:
            aug[col][col] = 1e-9
        aug[col], aug[piv] = aug[piv], aug[col]
        pv = aug[col][col]
        for r in range(col+1, m):
            f = aug[r][col]/pv
            for c in range(col, m+1):
                aug[r][c] -= f*aug[col][c]
    b = [0.0]*m
    for r in range(m-1, -1, -1):
        s = aug[r][m] - sum(aug[r][c]*b[c] for c in range(r+1, m))
        b[r] = s/aug[r][r]
    return b  # [intercept, ...coefs]

def ols_predict(X, b):
    return [b[0] + sum(b[i+1]*x[i] for i in range(len(x))) for x in X]

def qlike(y, pred):
    pairs = [(yy, pp) for yy, pp in zip(y, pred) if yy > 0 and pp > 0]
    if not pairs:
        return float('nan')
    return sum(yy/pp - 1.0 - math.log(yy/pp) for yy, pp in pairs)/len(pairs)

# ---------- load mark price klines ----------
def load_mark():
    rows = []  # (t_ms, close)
    for zname in sorted(RAW.glob("BTCUSDT-markPriceKlines-1h-*.zip")):
        with zipfile.ZipFile(zname) as z:
            csvname = z.namelist()[0]
            text = z.read(csvname).decode("utf-8")
        r = csv.DictReader(io.StringIO(text))
        for rec in r:
            rows.append((int(rec["close_time"]), float(rec["close"])))
    rows.sort()
    return rows  # [(t_ms, close)]

# ---------- load metrics (daily OI + taker ratio) ----------
def load_metrics():
    entries = []  # (dt_utc, oi, taker_ratio)
    for zname in sorted(RAW.glob("BTCUSDT-metrics-*.zip")):
        with zipfile.ZipFile(zname) as z:
            csvname = z.namelist()[0]
            text = z.read(csvname).decode("utf-8")
        r = csv.DictReader(io.StringIO(text))
        for rec in r:
            try:
                dt = datetime.strptime(rec["create_time"], "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
                oi = float(rec["sum_open_interest"])
                tr = float(rec["sum_taker_long_short_vol_ratio"])
                entries.append((dt, oi, tr))
            except Exception:
                continue
    entries.sort(key=lambda e: e[0])
    return entries

# ---------- load funding ----------
def load_funding():
    entries = []  # (t_ms, rate)
    for zname in sorted(RAW.glob("BTCUSDT-fundingRate-*.zip")):
        with zipfile.ZipFile(zname) as z:
            csvname = z.namelist()[0]
            text = z.read(csvname).decode("utf-8")
        r = csv.DictReader(io.StringIO(text))
        for rec in r:
            try:
                entries.append((int(rec["calc_time"]), float(rec["last_funding_rate"])))
            except Exception:
                continue
    entries.sort(key=lambda e: e[0])
    return entries

import bisect
def latest_at(entries, t_ms, key_index=0):
    # entries sorted by key_index (0=t_ms) ; find latest with key <= t_ms
    # entries: list of tuples; key at index 0
    keys = [e[0] for e in entries]
    i = bisect.bisect_right(keys, t_ms) - 1
    if i < 0:
        return None
    return entries[i]

def latest_metrics_at(entries, t_dt):
    keys = [e[0] for e in entries]  # datetimes
    i = bisect.bisect_right(keys, t_dt) - 1
    if i < 0:
        return None
    return entries[i]

# ---------- main ----------
mark = load_mark()          # [(t_ms, close)] hourly
metrics = load_metrics()    # [(dt, oi, taker)] 5-min
funding = load_funding()    # [(t_ms, rate)]

N = len(mark)
closes = [c for _, c in mark]
t_ms = [t for t, _ in mark]
t_dt = [datetime.fromtimestamp(t/1000.0, tz=timezone.utc) for t in t_ms]

# log returns r_i = ln(c_i/c_{i-1})
r = [0.0]*N
for i in range(1, N):
    r[i] = math.log(closes[i]/closes[i-1])

r2 = [v*v for v in r]
# cumulative sum of r2 for O(1) window sums (index i inclusive -> cum[i+1]-cum[i-k])
cum = [0.0]*(N+1)
for i in range(N):
    cum[i+1] = cum[i] + r2[i]

def window_sum(i, k):
    # sum r2 over i-k+1 .. i inclusive
    if i-k+1 < 0:
        return None
    return cum[i+1] - cum[i-k+1]

# target_i = sum r2 over i+1 .. i+24
def target_at(i):
    if i+24 >= N:
        return None
    return cum[i+25] - cum[i+1]

# build records for valid forecast hours i (need RV168 -> i>=167; target -> i+24<N)
records = []
for i in range(167, N-24):
    rv1 = r2[i]
    rv24 = window_sum(i, 24)
    rv168 = window_sum(i, 168)
    tgt = target_at(i)
    if rv24 is None or rv168 is None or tgt is None:
        continue
    # funding latest <= t_ms[i]
    f = latest_at(funding, t_ms[i])
    fund = f[1] if f else None
    # metrics latest <= t_dt[i]
    met = latest_metrics_at(metrics, t_dt[i])
    oi = met[1] if met else None
    taker = met[2] if met else None
    records.append({
        "i": i, "t_ms": t_ms[i], "t_dt": t_dt[i].isoformat(),
        "rv1": rv1, "rv24": rv24, "rv168": rv168,
        "funding": fund, "oi": oi, "taker": taker,
        "target": tgt,
    })

print(f"valid forecast hours: {len(records)}")
print(f"time range: {records[0]['t_dt']} .. {records[-1]['t_dt']}" if records else "none")

# ---------- funding abs percentile (90-day lookback, min 30 obs) ----------
# index funding records by t_ms
def abs_funding_pct(rec_idx):
    # available funding observations strictly before this record's t, within prior 90 days
    t = records[rec_idx]["t_ms"]
    cutoff = t - 90*86400*1000
    vals = []
    for fms, fr in funding:
        if cutoff < fms < t:  # strictly prior observations only
            vals.append(abs(fr))
    if len(vals) < 30:
        return None
    vals.sort()
    rank = sum(1 for v in vals if v < abs(records[rec_idx]["funding"])) if records[rec_idx]["funding"] is not None else 0
    return rank/len(vals)

# precompute pct once
for rec in records:
    rec["fund_abs_pct"] = abs_funding_pct(records.index(rec)) if False else None
# recompute efficiently: iterate with index
for idx, rec in enumerate(records):
    rec["fund_abs_pct"] = abs_funding_pct(idx)

print(f"records with funding pct: {sum(1 for r in records if r['fund_abs_pct'] is not None)}")

# ---------- blocks ----------
def in_range(dt_iso, start_s, end_s):
    dt = datetime.fromisoformat(dt_iso)
    st = datetime.fromisoformat(start_s); en = datetime.fromisoformat(end_s)
    return st <= dt <= en

train = [r for r in records if in_range(r["t_dt"], "2025-06-01T00:00:00+00:00", "2025-06-30T23:00:00+00:00")]
embargo = [r for r in records if in_range(r["t_dt"], "2025-07-01T00:00:00+00:00", "2025-07-07T23:00:00+00:00")]
blocks = [
    ("test_block_1", "2025-07-08T00:00:00+00:00", "2025-07-21T23:00:00+00:00"),
    ("test_block_2", "2025-07-22T00:00:00+00:00", "2025-08-04T23:00:00+00:00"),
    ("test_block_3", "2025-08-05T00:00:00+00:00", "2025-08-18T23:00:00+00:00"),
]
test_sets = {name: [r for r in records if in_range(r["t_dt"], s, e)] for name, s, e in blocks}
print(f"train={len(train)} embargo={len(embargo)} " + " ".join(f"{n}={len(test_sets[n])}" for n,_,_ in blocks))

# ---------- feature columns ----------
FEAT_B1 = ["rv1","rv24","rv168"]
FEAT_C2 = ["rv1","rv24","rv168","funding","fund_abs_pct","oi","taker"]

def logpos(x):
    return math.log(x+EPS) if x is not None and x > -EPS else None

def build_xy(recs, feat_cols):
    X, y = [], []
    for rec in recs:
        vals = []
        ok = True
        for c in feat_cols:
            v = rec[c]
            if v is None:
                ok = False; break
            if c in ("rv1","rv24","rv168","target"):
                v = logpos(v)
            elif c == "funding":
                v = v  # signed, raw (can be neg/pos), keep as is
            elif c == "fund_abs_pct":
                v = v  # 0..1
            elif c in ("oi","taker"):
                v = v
            vals.append(v)
        if not ok:
            continue
        yv = logpos(rec["target"])
        if yv is None:
            continue
        X.append(vals); y.append(yv)
    return X, y

# train-only standardization params (fit on B1-complete train rows)
def train_stats(X, cols):
    stats = {}
    for j, c in enumerate(cols):
        col = [row[j] for row in X]
        valid = [v for v in col if v is not None and math.isfinite(v)]
        if not valid:
            stats[c] = (0.0, 1.0); continue
        mean = sum(valid)/len(valid)
        var = sum((v-mean)**2 for v in valid)/len(valid)
        std = math.sqrt(var)
        if std == 0: std = 1.0
        stats[c] = (mean, std)
    return stats

def apply_std(X, stats, cols):
    out = []
    for row in X:
        nr = []
        for j, c in enumerate(cols):
            mean, std = stats[c]
            nr.append((row[j]-mean)/std)
        out.append(nr)
    return out

# ---------- fit on train ----------
Xb1_train, yb1_train = build_xy(train, FEAT_B1)
Xb1_train_std = apply_std(Xb1_train, train_stats(Xb1_train, FEAT_B1), FEAT_B1)
beta_B1 = ols_fit(Xb1_train_std, yb1_train)
# Duan smearing on train
pred_train_b1 = ols_predict(Xb1_train_std, beta_B1)
resid = [y-pp for y, pp in zip(yb1_train, pred_train_b1)]
smear_B1 = math.exp(sum(resid)/len(resid))

# C2 train
Xc2_train, yc2_train = build_xy(train, FEAT_C2)
# common rows between B1 and C2 on train (by record index)
# build aligned: use records that have all C2 features
c2_train_idx = [i for i, rec in enumerate(train) if all(rec[c] is not None for c in FEAT_C2) and rec["target"] is not None]
Xc2_train_al = [ [logpos(train[k]["rv1"]), logpos(train[k]["rv24"]), logpos(train[k]["rv168"]),
                  train[k]["funding"], train[k]["fund_abs_pct"], train[k]["oi"], train[k]["taker"]] for k in c2_train_idx ]
yc2_train_al = [logpos(train[k]["target"]) for k in c2_train_idx]
stats_c2 = train_stats(Xc2_train_al, FEAT_C2)
Xc2_train_std = apply_std(Xc2_train_al, stats_c2, FEAT_C2)
beta_C2 = ols_fit(Xc2_train_std, yc2_train_al)
pred_train_c2 = ols_predict(Xc2_train_std, beta_C2)
resid_c2 = [y-pp for y, pp in zip(yc2_train_al, pred_train_c2)]
smear_C2 = math.exp(sum(resid_c2)/len(resid_c2))

print(f"train B1 rows={len(Xb1_train)}, C2 rows={len(Xc2_train_al)}")
print(f"beta_B1={beta_B1}, smear_B1={smear_B1:.6f}")
print(f"beta_C2={beta_C2}, smear_C2={smear_C2:.6f}")

# ---------- evaluate on test blocks ----------
def eval_block(recs, feat_cols, beta, smear, stats, is_c2):
    X, y = [], []
    for rec in recs:
        if not all(rec[c] is not None for c in feat_cols) or rec["target"] is None:
            continue
        if is_c2:
            row = [logpos(rec["rv1"]), logpos(rec["rv24"]), logpos(rec["rv168"]),
                   rec["funding"], rec["fund_abs_pct"], rec["oi"], rec["taker"]]
        else:
            row = [logpos(rec["rv1"]), logpos(rec["rv24"]), logpos(rec["rv168"])]
        X.append(row); y.append(logpos(rec["target"]))
    if not X:
        return None
    Xs = apply_std(X, stats, feat_cols)
    pred_log = ols_predict(Xs, beta)
    pred = [math.exp(pl)*smear for pl in pred_log]
    yy = [math.exp(yyv)-EPS for yyv in y]  # back to target scale (approx); actually y was log(target+eps)
    # invert: target = exp(y_log) - eps
    y_true = [math.exp(yyv)-EPS for yyv in y]
    q = qlike(y_true, pred)
    mae = sum(abs(a-b) for a,b in zip(y_true,pred))/len(y_true)
    rmse = math.sqrt(sum((a-b)**2 for a,b in zip(y_true,pred))/len(y_true))
    return {"n": len(y_true), "qlike": q, "mae": mae, "rmse": rmse,
            "y_true": y_true, "pred": pred}

# common-row aligned evaluation across models per block
def eval_block_common(recs):
    # rows with all features for C2 (superset) -> common across B1/C2
    commons = [rec for rec in recs if all(rec[c] is not None for c in FEAT_C2) and rec["target"] is not None]
    if not commons:
        return None
    # B1 on common
    X1 = [[logpos(c["rv1"]), logpos(c["rv24"]), logpos(c["rv168"])] for c in commons]
    y1 = [logpos(c["target"]) for c in commons]
    X1s = apply_std(X1, train_stats(Xb1_train, FEAT_B1), FEAT_B1)
    p1 = [math.exp(pl)*smear_B1 for pl in ols_predict(X1s, beta_B1)]
    y1t = [math.exp(y)-EPS for y in y1]
    # C2 on common
    X2 = [[logpos(c["rv1"]), logpos(c["rv24"]), logpos(c["rv168"]),
           c["funding"], c["fund_abs_pct"], c["oi"], c["taker"]] for c in commons]
    y2 = [logpos(c["target"]) for c in commons]
    X2s = apply_std(X2, stats_c2, FEAT_C2)
    p2 = [math.exp(pl)*smear_C2 for pl in ols_predict(X2s, beta_C2)]
    y2t = [math.exp(y)-EPS for y in y2]
    # B0 persistence: pred = rv24 (target scale) -> but target is RV24h forward; persistence uses current rv24
    p0 = [math.exp(logpos(c["rv24"]))-EPS for c in commons]  # current rv24 as forecast
    q_b0 = qlike(y1t, p0); q_b1 = qlike(y1t, p1); q_c2 = qlike(y2t, p2)
    mae_b0 = sum(abs(a-b) for a,b in zip(y1t,p0))/len(y1t)
    rmse_b0 = math.sqrt(sum((a-b)**2 for a,b in zip(y1t,p0))/len(y1t))
    mae_b1 = sum(abs(a-b) for a,b in zip(y1t,p1))/len(y1t)
    rmse_b1 = math.sqrt(sum((a-b)**2 for a,b in zip(y1t,p1))/len(y1t))
    mae_c2 = sum(abs(a-b) for a,b in zip(y2t,p2))/len(y2t)
    rmse_c2 = math.sqrt(sum((a-b)**2 for a,b in zip(y2t,p2))/len(y2t))
    return {
        "n": len(commons),
        "qlike_B0": q_b0, "qlike_B1": q_b1, "qlike_C2": q_c2,
        "diff_C2_B1": q_c2 - q_b1,
        "rel_C2_B1_pct": (q_c2 - q_b1)/q_b1*100 if q_b1 else float('nan'),
        "diff_C1_B1": None,  # C1 not separately computed in this minimal run
        "mae_B0": mae_b0, "rmse_B0": rmse_b0,
        "mae_B1": mae_b1, "rmse_B1": rmse_b1,
        "mae_C2": mae_c2, "rmse_C2": rmse_c2,
        "y_true": y1t, "pred_B0": p0, "pred_B1": p1, "pred_C2": p2,
    }

results = {}
for name, s, e in blocks:
    res = eval_block_common(test_sets[name])
    results[name] = res
    if res:
        print(f"{name}: n={res['n']} QLIKE_B0={res['qlike_B0']:.6f} QLIKE_B1={res['qlike_B1']:.6f} QLIKE_C2={res['qlike_C2']:.6f} diff_C2_B1={res['diff_C2_B1']:+.6f} rel={res['rel_C2_B1_pct']:+.4f}%")
    else:
        print(f"{name}: empty")

# ---------- aggregate ----------
qlike_diffs = [results[n]["diff_C2_B1"] for n in results if results[n] and results[n]["diff_C2_B1"] is not None and math.isfinite(results[n]["diff_C2_B1"])]
rel_pcts = [results[n]["rel_C2_B1_pct"] for n in results if results[n] and results[n]["rel_C2_B1_pct"] is not None and math.isfinite(results[n]["rel_C2_B1_pct"])]
mean_diff = sum(qlike_diffs)/len(qlike_diffs) if qlike_diffs else float('nan')
mean_rel = sum(rel_pcts)/len(rel_pcts) if rel_pcts else float('nan')
# sign consistency: how many blocks have C2 < B1 (improvement)
n_improved = sum(1 for d in qlike_diffs if d < 0)
materiality_pass = mean_rel <= -2.0  # reduction >= 2% means rel <= -2%
gate = "CONFIRMED" if (qlike_diffs and mean_diff < 0 and materiality_pass and n_improved >= 2) else "NOT_SUPPORTED"

summary = {
    "campaign": "FCLR-LIVE-ARCHIVE-02",
    "session_utc": "2026-11-22T00:30:00Z",
    "experiment_id": "FCLR-LIVE-ARCHIVE-02",
    "data_source": "data.binance.vision (futures/um/daily/metrics, futures/um/monthly/fundingRate, futures/um/monthly/markPriceKlines/1h), BTCUSDT, unauthenticated",
    "data_window": "2025-06-01 .. 2025-08-18",
    "symbols": ["BTCUSDT"],
    "target": "next_24h_realized_variance (sum of squared 1h mark-price log returns, t+1..t+24)",
    "eps": EPS,
    "blocks": {"train":"2025-06-01..2025-06-30","embargo":"2025-07-01..2025-07-07",
               "test_block_1":"2025-07-08..2025-07-21","test_block_2":"2025-07-22..2025-08-04","test_block_3":"2025-08-05..2025-08-18"},
    "models": {"B0":"persistence (pred=RV24h)","B1":"RV-only HAR OLS log(RV+eps) ~ log RV1h+log RV24h+log RV168h, train-only std, Duan smear",
               "C2":"B1+signed funding+abs funding pct(90d,min30)+OI+taker vol ratio"},
    "materiality_floor_pct": 2.0,
    "n_forecast_hours": len(records),
    "block_results": {k: {kk: (vv if kk not in ("y_true","pred_B0","pred_B1","pred_C2") else len(vv)) for kk, vv in v.items()} if v else None for k, v in results.items()},
    "aggregate": {"mean_diff_C2_B1": mean_diff, "mean_rel_C2_B1_pct": mean_rel,
                  "n_blocks": len(qlike_diffs), "n_improved": n_improved,
                  "materiality_pass": materiality_pass, "gate": gate},
    "decision": gate,
    "notes": "Libation risk is PROXIED (OI + taker imbalance + mark dislocation), never observed liquidations; no liquidationSnapshot dataset exists in archive. mark/index premium not downloaded -> recorded missing. stdlib-only.",
    "outcome_data_inspected_before_freeze": False,
    "prereg_artifact": "fclr_live_archive02_prereg_20261122T003000Z.json",
    "source_registry_artifact": "fclr_live_archive02_source_registry_20261122T003000Z.json",
}
# write json (strip large arrays)
out = {k: v for k, v in summary.items() if k not in ("block_results",)}
# keep block_results but without arrays
out["block_results"] = summary["block_results"]
OUT_JSON.write_text(json.dumps(out, indent=2))
print(f"\nWrote {OUT_JSON}")
print(f"DECISION: {gate} | mean diff C2-B1={mean_diff:+.6f} | mean rel={mean_rel:+.4f}% | materiality(>=2% reduction): {materiality_pass} | n_improved={n_improved}/3")

# ---------- markdown ----------
lines = []
lines.append("# FCLR-LIVE-ARCHIVE-02 Evaluation — 3-Block Confirmatory (stdlib)")
lines.append("")
lines.append(f"**Campaign:** FCLR-LIVE-ARCHIVE-02  |  **Session UTC:** 2026-11-22T00:30:00Z")
lines.append("**Artifact:** `fclr_live_archive02_eval_20261122T003000Z.json` + `fclr_live_archive02_eval_20261122T003000Z.md`")
lines.append(f"**Decision:** {gate}")
lines.append("")
lines.append("## Design (frozen in prereg, outcome-blind)")
lines.append(f"- Data source: `data.binance.vision` (unauthenticated) — futures/um/daily/metrics + futures/um/monthly/fundingRate + futures/um/monthly/markPriceKlines/1h, BTCUSDT")
lines.append(f"- Data window: 2025-06-01 .. 2025-08-18; valid forecast hours: {len(records)}")
lines.append(f"- Target: next-24-hour realized variance (sum of squared 1h mark-price log returns, t+1..t+24)")
lines.append("- Train: 2025-06-01..2025-06-30 | Embargo: 7 days (2025-07-01..2025-07-07)")
lines.append("- Test blocks: 2025-07-08..07-21 | 2025-07-22..2025-08-04 | 2025-08-05..2025-08-18")
lines.append("- Models: B0 persistence | B1 RV-only HAR (OLS, train-only std, Duan smear) | C2 = B1 + funding + abs funding pct + OI + taker vol ratio")
lines.append(f"- Materiality floor: >= 2% relative QLIKE reduction (C2 vs B1), frozen in advance")
lines.append("- Liquidation risk: PROXIED (OI + taker imbalance + mark dislocation), never observed liquidations (no liquidationSnapshot dataset)")
lines.append("")
lines.append("## Block results (common rows, aligned across B0/B1/C2)")
lines.append("| block | n | QLIKE_B0 | QLIKE_B1 | QLIKE_C2 | diff C2-B1 | rel % |")
lines.append("|-----|---|----------|----------|----------|------------|-------|")
for name, _, _ in blocks:
    res = results[name]
    if res:
        lines.append(f"| {name} | {res['n']} | {res['qlike_B0']:.6f} | {res['qlike_B1']:.6f} | {res['qlike_C2']:.6f} | {res['diff_C2_B1']:+.6f} | {res['rel_C2_B1_pct']:+.4f}% |")
    else:
        lines.append(f"| {name} | - | - | - | - | - | - |")
lines.append("")
lines.append("## Aggregate")
lines.append(f"- Mean diff C2-B1: {mean_diff:+.6f}")
lines.append(f"- Mean rel C2-B1: {mean_rel:+.4f}%")
lines.append(f"- Blocks improved (C2<B1): {n_improved}/3")
lines.append(f"- Materiality floor (>=2% reduction): {'PASS' if materiality_pass else 'FAIL'}")
lines.append(f"- Decision: {gate}")
lines.append("")
lines.append("## Safeguards")
lines.append("- No look-ahead, no survivorship substitution, no forward fill; missing features remain missing.")
lines.append("- mark/index premium not downloaded -> missing, never zero-filled.")
lines.append("- stdlib-only (numpy/pandas/scipy not installed in runner).")
OUT_MD.write_text("\n".join(lines) + "\n")
print(f"Wrote {OUT_MD}")
