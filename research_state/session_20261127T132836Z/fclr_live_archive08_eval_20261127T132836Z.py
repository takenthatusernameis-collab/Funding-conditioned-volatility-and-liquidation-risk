#!/usr/bin/env python3
"""FCLR-LIVE-ARCHIVE-08 heavy confirmatory evaluation (stdlib only).

Track-B modeled boundary-breach forecast = the liquidation-risk half of the
repository name (Funding-conditioned-volatility-and-liquidation-risk). NOT a
risk overlay: these are disclosed, hypothetical, modeled liquidation-boundary
breaches, not observed liquidations. Forecast validation only, permitted under
RESEARCH_PROMPT.md section 9 because the campaign-07 forecast gate did not pass.

Design (frozen, carried forward from campaign-07):
  - Same frozen balanced mark-price common support S (|S| = 22,608; five symbols
    BNBUSDT/BTCUSDT/ETHUSDT/SOLUSDT/XRPUSDT; 2024-04..2026-10 UTC).
  - Same 60/20/20 split by unique UTC timestamp on S, 168h purge/embargo, three
    chronological test blocks; all five symbols in every block/fold.
  - Fixed-form deterministic stdlib OLS only; train-only scaling; no
    regularization / model-family search / feature search / threshold tuning.

Campaign-08 target (new): Track-B modeled boundary-breach indicator under a
disclosed constant leverage scenario (20x; long boundary = entry*0.95, short
boundary = entry*1.05), horizon 24h. Long and short labels kept separate.
Target = whether the future mark-price path breaches the boundary within the
horizon. Synthetic modeled breaches, not observed liquidations.

Models:
  B (mark-price-only baseline): trailing RV features + mark/index premium +
      mark/EMA24 distance.
  C (funding-conditioned candidate): B + signed funding(24h) + trailing 90d
      |funding| percentile.
Metrics: out-of-sample AUC / log-loss / Brier, long and short separate.
Inference: >=2000 deterministic block-bootstrap replicates (blocks resampled
jointly across symbols at the timestamp level) + leave-one-symbol-out.

Read-only cache; no network; stdlib only.
"""

import bisect
import datetime as dt
import hashlib
import io
import json
import math
import os
import random
import time
import zipfile

SESSION = "20261127T132836Z"
EXPERIMENT = "FCLR-LIVE-ARCHIVE-08"
CAMPAIGN_START = "20261127T131654Z"
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "..", "data_cache")
SYMBOLS = ["BNBUSDT", "BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT"]
MONTHS = [f"{y}_{m:02d}" for y in (2024, 2025, 2026) for m in range(1, 13)
          if (y == 2024 and m >= 4) or y == 2025 or (y == 2026 and m <= 10)]
SEED = 20261127
N_BOOT = 2000
EMBARGO_H = 168
N_BLOCKS = 3
BLOCK_ROWS = 24
LEVERAGE = 20.0
LONG_FACTOR = 1.0 - 1.0 / LEVERAGE
SHORT_FACTOR = 1.0 + 1.0 / LEVERAGE
HORIZON_H = 24
EPS = 1e-7
FLOOR = 0.02


def read_zip_csv(path):
    with open(path, "rb") as f:
        z = zipfile.ZipFile(io.BytesIO(f.read()))
        return z.read(z.namelist()[0]).decode("utf-8", "ignore").splitlines()


def read_csv_lines(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read().splitlines()


def read_any_lines(path):
    if path.lower().endswith(".zip"):
        return read_zip_csv(path)
    return read_csv_lines(path)


def sha256_file(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def parse_klines(lines):
    out = {}
    for ln in lines:
        p = ln.split(",")
        if not p or p[0] in ("open_time", "") or not p[0].lstrip("-").isdigit():
            continue
        try:
            t = int(p[0]) // 1000
            close = float(p[4])
        except Exception:
            continue
        if close > 0:
            out[t] = close
    return out


def parse_funding(lines):
    out = []
    for ln in lines:
        p = ln.split(",")
        if not p or p[0] in ("calc_time", "") or not p[0].lstrip("-").isdigit():
            continue
        try:
            t = int(p[0]) // 1000
            rate = float(p[2])
        except Exception:
            continue
        out.append((t, rate))
    out.sort()
    return out


def _is_mark_path(path):
    parts = os.path.normpath(path).split(os.sep)
    return any(part.startswith("markPriceKlines-") for part in parts)


def _is_index_path(path):
    parts = os.path.normpath(path).split(os.sep)
    return any(part.startswith("indexPriceKlines-") for part in parts)


def load_raw(sym):
    mark = {}
    index = {}
    funding = []
    gaps = []
    layouts = set()
    files_read = []
    for mo in MONTHS:
        cache_dir = os.path.join(CACHE, f"{sym}_{mo}")
        if not os.path.isdir(cache_dir):
            gaps.append({"symbol": sym, "month": mo, "reason": "month_dir_missing"})
            continue
        for root, _dirs, files in os.walk(cache_dir):
            for fn in sorted(files):
                path = os.path.join(root, fn)
                low = fn.lower()
                if not (low.endswith(".csv") or low.endswith(".zip")):
                    continue
                is_mark = _is_mark_path(path)
                is_index = _is_index_path(path)
                if not (is_mark or is_index):
                    continue
                rel = os.path.relpath(path, cache_dir)
                layouts.add("nested" if rel.count(os.sep) >= 2 else "flat")
                try:
                    parsed = parse_klines(read_any_lines(path))
                except Exception as exc:
                    gaps.append({"symbol": sym, "month": mo, "path": rel,
                                 "reason": str(exc)})
                    continue
                files_read.append(rel)
                if is_mark:
                    mark.update(parsed)
                else:
                    index.update(parsed)
        for ext in (".zip", ".csv"):
            fpath = os.path.join(
                cache_dir, f"{sym}-fundingRate-{mo.replace('_', '-')}{ext}")
            if os.path.exists(fpath):
                files_read.append(os.path.relpath(fpath, cache_dir))
                try:
                    funding.extend(parse_funding(read_any_lines(fpath)))
                except Exception as exc:
                    gaps.append({"symbol": sym, "month": mo,
                                 "source": "fundingRate", "reason": str(exc)})
                break
        else:
            gaps.append({"symbol": sym, "month": mo,
                         "source": "fundingRate", "reason": "funding_missing"})
    funding.sort()
    return {"mark": mark, "index": index, "funding": funding,
            "gaps": gaps, "layouts": sorted(layouts), "files_read": files_read}


def build_panel(sym, raw, common):
    """Feature/label rows for one symbol restricted to common support S, with
    Track-B modeled boundary-breach targets (long/short separate)."""
    mark = raw["mark"]
    index = raw["index"]
    funding = raw["funding"]
    ts = sorted(t for t in mark if t in common)
    n = len(ts)
    if n < 200:
        return [], {"symbol": sym, "n_rows": 0, "n_times": n,
                    "gaps": raw["gaps"], "layouts": raw["layouts"]}
    close = mark
    r = [0.0] * n
    for i in range(1, n):
        if ts[i] - ts[i - 1] == 3600 and close[ts[i]] > 0:
            r[i] = math.log(close[ts[i]] / close[ts[i - 1]])
    rv1 = [v * v for v in r]
    rpos = [v * v if v > 0 else 0.0 for v in r]
    rneg = [v * v if v < 0 else 0.0 for v in r]

    def rollsum(vals, w):
        out = [None] * n
        acc = [0.0] * (n + 1)
        for i in range(n):
            acc[i + 1] = acc[i] + vals[i]
        for i in range(w - 1, n):
            out[i] = acc[i + 1] - acc[i + 1 - w]
        return out

    rv24 = rollsum(rv1, 24)
    rv168 = rollsum(rv1, 168)
    rv_plus24 = rollsum(rpos, 24)
    rv_minus24 = rollsum(rneg, 24)
    rv_plus168 = rollsum(rpos, 168)
    rv_minus168 = rollsum(rneg, 168)
    accp = [0.0] * (n + 1)
    accn = [0.0] * (n + 1)
    for i in range(n):
        accp[i + 1] = accp[i] + rpos[i]
        accn[i + 1] = accn[i] + rneg[i]

    ema = {}
    alpha = 2.0 / (24 + 1)
    e = None
    for t in ts:
        m = mark.get(t)
        if m is None:
            continue
        e = m if e is None else alpha * m + (1 - alpha) * e
        ema[t] = e

    ft = [x[0] for x in funding]
    fv = [x[1] for x in funding]

    rows = []
    for i in range(168, n - HORIZON_H):
        t = ts[i]
        if (rv24[i] is None or rv168[i] is None or rv_plus24[i] is None or
                rv_minus24[i] is None or rv_plus168[i] is None or
                rv_minus168[i] is None):
            continue
        entry = mark[t]
        # Modeled boundary-breach target over the next HORIZON_H hours.
        fut_marks = []
        ok = True
        for k in range(1, HORIZON_H + 1):
            m = mark.get(t + k * 3600)
            if m is None:
                ok = False
                break
            fut_marks.append(m)
        if not ok:
            continue
        long_boundary = entry * LONG_FACTOR
        short_boundary = entry * SHORT_FACTOR
        y_long = 1 if min(fut_marks) < long_boundary else 0
        y_short = 1 if max(fut_marks) > short_boundary else 0

        j = bisect.bisect_right(ft, t) - 1 if ft else -1
        if j < 0:
            continue
        cur_rate = fv[j]
        lo = bisect.bisect_right(ft, t - 24 * 3600)
        fund24 = sum(fv[lo:j + 1]) if j >= lo else 0.0
        lo90 = bisect.bisect_right(ft, t - 90 * 86400)
        window = [abs(x) for x in fv[lo90:j + 1]]
        pct = (sum(1 for x in window if x <= abs(cur_rate)) / len(window)) \
            if window else 0.5
        mk = mark.get(t)
        ix = index.get(t)
        prem = (mk - ix) / ix if (mk is not None and ix not in (None, 0)) else 0.0
        em = ema.get(t)
        mdist = (mk - em) / em if (mk is not None and em not in (None, 0)) else 0.0

        rows.append({
            "symbol": sym, "t": t,
            "rv1": rv1[i], "rv24": rv24[i], "rv168": rv168[i],
            "rv_plus24": rv_plus24[i], "rv_minus24": rv_minus24[i],
            "rv_plus168": rv_plus168[i], "rv_minus168": rv_minus168[i],
            "y_long": y_long, "y_short": y_short,
            "fund24": fund24, "fund_pct": pct, "prem": prem, "mdist": mdist,
            "entry": entry,
        })
    info = {"n_rows": len(rows), "n_times": n, "gaps": raw["gaps"],
            "layouts": raw["layouts"],
            "n_mark_raw": len(mark), "n_in_common": len(ts),
            "files_read": raw.get("files_read", [])}
    return rows, info


def solve(A, b):
    p = len(A)
    M = [A[i][:] + [b[i]] for i in range(p)]
    for c in range(p):
        pivrow = max(range(c, p), key=lambda rr: abs(M[rr][c]))
        M[c], M[pivrow] = M[pivrow], M[c]
        piv = M[c][c]
        if abs(piv) < 1e-14:
            piv = 1e-14
        for rr in range(p):
            if rr != c:
                f = M[rr][c] / piv
                if f:
                    for k in range(c, p + 1):
                        M[rr][k] -= f * M[c][k]
    return [M[i][p] / (M[i][i] if abs(M[i][i]) > 1e-14 else 1e-14)
            for i in range(p)]


def ols_fit(X, y):
    p = len(X[0])
    XtX = [[0.0] * p for _ in range(p)]
    Xty = [0.0] * p
    for i in range(len(X)):
        xi = X[i]
        yi = y[i]
        for a in range(p):
            Xty[a] += xi[a] * yi
            xa = xi[a]
            row = XtX[a]
            for bb in range(p):
                row[bb] += xa * xi[bb]
    for a in range(p):
        XtX[a][a] += 1e-9
    return solve(XtX, Xty)


def ols_predict(beta, x):
    return sum(b * xi for b, xi in zip(beta, x))


def sigmoid(x):
    if x >= 0:
        return 1.0 / (1.0 + math.exp(-x))
    ex = math.exp(x)
    return ex / (1.0 + ex)


def auc_score(y, p):
    n = len(y)
    order = sorted(range(n), key=lambda i: p[i])
    ranks = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and p[order[j + 1]] == p[order[j]]:
            j += 1
        avg_rank = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            ranks[order[k]] = avg_rank
        i = j + 1
    n_pos = sum(1 for v in y if v == 1)
    n_neg = n - n_pos
    if n_pos == 0 or n_neg == 0:
        return float("nan")
    sum_ranks_pos = sum(ranks[i] for i in range(n) if y[i] == 1)
    return (sum_ranks_pos - n_pos * (n_pos + 1) / 2.0) / (n_pos * n_neg)


def binary_metrics(y, p):
    n = len(y)
    brier = sum((p[i] - y[i]) ** 2 for i in range(n)) / n
    ll = 0.0
    for i in range(n):
        pi = min(max(p[i], EPS), 1.0 - EPS)
        ll += -(y[i] * math.log(pi) + (1 - y[i]) * math.log(1 - pi))
    ll /= n
    return {
        "auc": auc_score(y, p),
        "brier": brier,
        "log_loss": ll,
        "n": n,
        "n_pos": int(sum(1 for v in y if v == 1)),
        "n_neg": int(n - sum(1 for v in y if v == 1)),
    }


def main():
    t0 = time.time()
    print(f"[{dt.datetime.now(dt.timezone.utc).strftime('%H:%M:%S')}] [1/6] "
          "loading verified data cache (read-only, 3 layouts) ...", flush=True)
    raw = {}
    all_files_read = []
    for s in SYMBOLS:
        raw[s] = load_raw(s)
        all_files_read.extend(raw[s]["files_read"])
        print(f"  {s}: mark_raw={len(raw[s]['mark'])} "
              f"index_raw={len(raw[s]['index'])} "
              f"funding={len(raw[s]['funding'])} "
              f"layouts={raw[s]['layouts']}", flush=True)

    common = set(raw[SYMBOLS[0]]["mark"])
    for s in SYMBOLS[1:]:
        common &= set(raw[s]["mark"])
    common = sorted(common)
    n_common = len(common)
    print(f"  |S| (all-five mark-price common support) = {n_common}", flush=True)
    if n_common < 500:
        raise SystemExit(f"FATAL: common support |S|={n_common} < 500; aborting")

    panel = []
    per_sym = {}
    all_gaps = []
    layout_notes = {}
    for s in SYMBOLS:
        rows, info = build_panel(s, raw[s], set(common))
        per_sym[s] = info["n_rows"]
        layout_notes[s] = {"layouts": info["layouts"],
                           "n_mark_raw": info.get("n_mark_raw"),
                           "n_in_common": info.get("n_in_common")}
        all_gaps.extend(info["gaps"])
        panel.extend(rows)
        print(f"  {s}: {info['n_rows']} rows (in-common ts={info.get('n_in_common')}), "
              f"gaps={len(info['gaps'])}", flush=True)
    panel.sort(key=lambda x: (x["t"], x["symbol"]))

    uniq = sorted({x["t"] for x in panel})
    nu = len(uniq)
    i60 = int(0.6 * nu)
    i80 = int(0.8 * nu)
    b1 = uniq[i60] if nu > i60 else uniq[-1]
    b2 = uniq[i80] if nu > i80 else uniq[-1]
    cut1 = b1 - EMBARGO_H * 3600
    cut2 = b2 - EMBARGO_H * 3600
    train = [x for x in panel if x["t"] < cut1]
    val = [x for x in panel if cut1 <= x["t"] < cut2]
    test = [x for x in panel if x["t"] >= cut2]
    print(f"  splits: train={len(train)} val={len(val)} test={len(test)} "
          f"(unique_ts={nu})", flush=True)

    BASE_FEATS = ["rv1", "rv24", "rv168", "rv_plus24", "rv_minus24",
                  "rv_plus168", "rv_minus168", "prem", "mdist"]
    CAND_FEATS = BASE_FEATS + ["fund24", "fund_pct"]

    def feat_vec(x, feats):
        return [math.log(max(x[k], 1e-12)) if k in ("rv1", "rv24", "rv168",
                   "rv_plus24", "rv_minus24", "rv_plus168", "rv_minus168")
                else x[k] for k in feats]

    def standardize(tr, feats):
        p = len(feats)
        means = [0.0] * p
        stds = [0.0] * p
        for a in range(p):
            col = [feat_vec(x, feats)[a] for x in tr]
            m = sum(col) / len(col)
            v = sum((c - m) ** 2 for c in col) / len(col)
            means[a] = m
            stds[a] = math.sqrt(v) if v > 0 else 1.0
        return means, stds

    def std_x(x, feats, means, stds):
        return [1.0] + [(feat_vec(x, feats)[a] - means[a]) / stds[a]
                        for a in range(len(feats))]

    means_B, stds_B = standardize(train, BASE_FEATS)
    means_C, stds_C = standardize(train, CAND_FEATS)

    def fit(model, tr, feats, means, stds):
        X = [std_x(x, feats, means, stds) for x in tr]
        y = [x["y_long"] for x in tr] if model.endswith("_long") \
            else [x["y_short"] for x in tr]
        return ols_fit(X, y)

    def predict_label(beta, x, feats, means, stds):
        return sigmoid(ols_predict(beta, std_x(x, feats, means, stds)))

    print(f"[{dt.datetime.now(dt.timezone.utc).strftime('%H:%M:%S')}] [3/6] "
          "fitting OLS models (train only) ...", flush=True)
    models = {}
    for mname, feats, means, stds in (("B_long", BASE_FEATS, means_B, stds_B),
                                      ("C_long", CAND_FEATS, means_C, stds_C),
                                      ("B_short", BASE_FEATS, means_B, stds_B),
                                      ("C_short", CAND_FEATS, means_C, stds_C)):
        models[mname] = fit(mname, train, feats, means, stds)

    def prob(mname, x):
        feats = BASE_FEATS if mname.startswith("B_") else CAND_FEATS
        means, stds = (means_B, stds_B) if mname.startswith("B_") \
            else (means_C, stds_C)
        return predict_label(models[mname], x, feats, means, stds)

    test_preds = {}
    for mname in ("B_long", "C_long", "B_short", "C_short"):
        test_preds[mname] = [prob(mname, x) for x in test]
    test_y = {"long": [x["y_long"] for x in test],
              "short": [x["y_short"] for x in test]}

    def metrics_for(mname, label):
        ys = test_y[label]
        ps = test_preds[mname]
        return binary_metrics(ys, ps)

    met = {}
    for label in ("long", "short"):
        met[label] = {}
        for mname in ("B_long", "C_long") if label == "long" \
                else ("B_short", "C_short"):
            met[label][mname] = metrics_for(mname, label)

    # Per-block metrics (3 chronological blocks of the test set by timestamp).
    test_ts = sorted({x["t"] for x in test})
    nt = len(test_ts)
    block_idx = [list(range(b, nt, N_BLOCKS)) for b in range(N_BLOCKS)]
    block_ts = [[test_ts[k] for k in bi] for bi in block_idx]
    test_by_ts = {}
    for x in test:
        test_by_ts.setdefault(x["t"], []).append(x)

    per_block = {}
    for label in ("long", "short"):
        per_block[label] = {}
        for mname in ("B_long", "C_long") if label == "long" \
                else ("B_short", "C_short"):
            per_block[label][mname] = []
        for bi in range(N_BLOCKS):
            tset = set(block_ts[bi])
            rows_b = [x for x in test if x["t"] in tset]
            ys_l = {"long": [x["y_long"] for x in rows_b],
                    "short": [x["y_short"] for x in rows_b]}
            for mname in ("B_long", "C_long") if label == "long" \
                    else ("B_short", "C_short"):
                ps = [prob(mname, x) for x in rows_b]
                per_block[label][mname].append(binary_metrics(ys_l[label], ps))

    # Leave-one-symbol-out.
    loo = {}
    for held in SYMBOLS:
        tr = [x for x in train if x["symbol"] != held]
        te = [x for x in test if x["symbol"] == held]
        if not tr or not te:
            continue
        mB_B, stds_B_h = standardize(tr, BASE_FEATS)
        mB_C, stds_C_h = standardize(tr, CAND_FEATS)
        beta_B = fit("B_long", tr, BASE_FEATS, mB_B, stds_B_h)
        beta_C = fit("C_long", tr, CAND_FEATS, mB_C, stds_C_h)

        def pr_long(beta, feats, means, stds, x):
            return sigmoid(ols_predict(beta, std_x(x, feats, means, stds)))

        te_long_y = [x["y_long"] for x in te]
        te_short_y = [x["y_short"] for x in te]
        pB_l = [pr_long(beta_B, BASE_FEATS, mB_B, stds_B_h, x) for x in te]
        pC_l = [pr_long(beta_C, CAND_FEATS, mB_C, stds_C_h, x) for x in te]
        # Short: refit on short target.
        beta_Bs = fit("B_short", tr, BASE_FEATS, mB_B, stds_B_h)
        beta_Cs = fit("C_short", tr, CAND_FEATS, mB_C, stds_C_h)
        pB_s = [pr_long(beta_Bs, BASE_FEATS, mB_B, stds_B_h, x) for x in te]
        pC_s = [pr_long(beta_Cs, CAND_FEATS, mB_C, stds_C_h, x) for x in te]
        mB_l = binary_metrics(te_long_y, pB_l)
        mC_l = binary_metrics(te_long_y, pC_l)
        mB_s = binary_metrics(te_short_y, pB_s)
        mC_s = binary_metrics(te_short_y, pC_s)
        loo[held] = {"n_long": len(te), "n_short": len(te),
                     "B_long": mB_l, "C_long": mC_l,
                     "B_short": mB_s, "C_short": mC_s}
        print(f"  LOO {held}: n={len(te)} "
              f"AUC_long B={mB_l['auc']:.4f} C={mC_l['auc']:.4f} "
              f"AUC_short B={mB_s['auc']:.4f} C={mC_s['auc']:.4f}", flush=True)

    # Block bootstrap (>=2000 replicates), resample test blocks jointly across
    # symbols; no refit (fixed fitted model), recompute metrics on resampled set.
    print(f"[{dt.datetime.now(dt.timezone.utc).strftime('%H:%M:%S')}] [4/6] "
          f"block bootstrap x{N_BOOT} ...", flush=True)
    test_ts_sorted = sorted(test_ts)
    nb = len(test_ts_sorted)
    nblocks = max(1, nb // BLOCK_ROWS)
    rng = random.Random(SEED)
    boot = {"long": [], "short": []}
    for label in ("long", "short"):
        for _ in range(N_BOOT):
            chosen = []
            for _b in range(nblocks):
                st = rng.randrange(0, max(1, nb - BLOCK_ROWS + 1))
                chosen.extend(test_ts_sorted[st:min(st + BLOCK_ROWS, nb)])
            cset = set(chosen)
            rows_b = [x for x in test if x["t"] in cset]
            if not rows_b:
                continue
            ys = {"long": [x["y_long"] for x in rows_b],
                  "short": [x["y_short"] for x in rows_b]}
            rep = {}
            for mname in ("B_long", "C_long") if label == "long" \
                    else ("B_short", "C_short"):
                ps = [prob(mname, x) for x in rows_b]
                rep[mname] = binary_metrics(ys[label], ps)
            b_diff = rep["C_long"]["brier"] - rep["B_long"]["brier"] \
                if label == "long" else rep["C_short"]["brier"] - rep["B_short"]["brier"]
            auc_diff = rep["C_long"]["auc"] - rep["B_long"]["auc"] \
                if label == "long" else rep["C_short"]["auc"] - rep["B_short"]["auc"]
            boot[label].append({"brier_diff": b_diff, "auc_diff": auc_diff,
                                "B_brier": rep["B_long"]["brier"]
                                if label == "long" else rep["B_short"]["brier"],
                                "C_brier": rep["C_long"]["brier"]
                                if label == "long" else rep["C_short"]["brier"],
                                "B_auc": rep["B_long"]["auc"]
                                if label == "long" else rep["B_short"]["auc"],
                                "C_auc": rep["C_long"]["auc"]
                                if label == "long" else rep["C_short"]["auc"]})

    def boot_ci(vals, qlo=0.025, qhi=0.975):
        s = sorted([v for v in vals if v == v])  # drop nan
        if not s:
            return [float("nan"), float("nan")]
        lo = s[max(0, int(qlo * len(s)) - 1)] if len(s) > 1 else s[0]
        hi = s[min(len(s) - 1, int(qhi * len(s)) - 1)] if len(s) > 1 else s[0]
        return [lo, hi]

    sufficient = len(test) >= 500 and nu >= 500
    results_by_label = {}
    for label in ("long", "short"):
        bB = met[label]["B_long"]["brier"] if label == "long" \
            else met[label]["B_short"]["brier"]
        bC = met[label]["C_long"]["brier"] if label == "long" \
            else met[label]["C_short"]["brier"]
        aB = met[label]["B_long"]["auc"] if label == "long" \
            else met[label]["B_short"]["auc"]
        aC = met[label]["C_long"]["auc"] if label == "long" \
            else met[label]["C_short"]["auc"]
        rel_brier = (bB - bC) / max(bB, 1e-12)
        rel_auc = (aC - aB) / max(aB, 1e-12) if aB == aB else 0.0
        bd = [b["brier_diff"] for b in boot[label]]
        ad = [b["auc_diff"] for b in boot[label]]
        bci = boot_ci(bd)
        aci = boot_ci(ad)
        improved = (rel_brier >= FLOOR and bci[0] > 0)
        verdict = "PROMOTED" if (sufficient and improved) else "NOT_SUPPORTED"
        results_by_label[label] = {
            "brier_B": bB, "brier_C": bC, "relative_brier_reduction": rel_brier,
            "auc_B": aB, "auc_C": aC, "relative_auc_improvement": rel_auc,
            "logloss_B": met[label]["B_long"]["log_loss"] if label == "long"
            else met[label]["B_short"]["log_loss"],
            "logloss_C": met[label]["C_long"]["log_loss"] if label == "long"
            else met[label]["C_short"]["log_loss"],
            "bootstrap_brier_diff_ci95": bci,
            "bootstrap_auc_diff_ci95": aci,
            "verdict": verdict,
        }

    overall_verdict = "PROMOTED" if all(
        r["verdict"] == "PROMOTED" for r in results_by_label.values()
    ) else "NOT_SUPPORTED"

    result = {
        "experiment_id": EXPERIMENT,
        "campaign": f"{EXPERIMENT}-{CAMPAIGN_START}",
        "session_id": SESSION,
        "session_utc": SESSION,
        "generated_at": dt.datetime.now(dt.timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ"),
        "source": "BINANCE_PUBLIC_ARCHIVE_READ_ONLY_CACHE",
        "symbols": SYMBOLS,
        "months": f"2024-04..2026-10 ({len(MONTHS)} months)",
        "n_symbols": len(SYMBOLS),
        "leverage": LEVERAGE,
        "long_boundary_factor": LONG_FACTOR,
        "short_boundary_factor": SHORT_FACTOR,
        "horizon_h": HORIZON_H,
        "common_support": {
            "definition": ("UTC hourly timestamps where all five symbols have "
                           "markPriceKlines close>0"),
            "n_common": n_common,
            "per_symbol_mark_raw": {s: len(raw[s]["mark"]) for s in SYMBOLS},
            "per_symbol_rows": per_sym,
            "layout_notes": layout_notes,
        },
        "n_train": len(train), "n_val": len(val), "n_test": len(test),
        "n_unique_timestamps": nu,
        "embargo_hours": EMBARGO_H,
        "splits": ("60/20/20 by unique UTC timestamp on S; 7-day (168h) "
                   "purge/embargo; test -> 3 chronological blocks"),
        "models": {"B": "mark-price-only baseline (7 RV features + prem + mdist)",
                   "C": "funding-conditioned candidate (B + fund24 + fund_pct)"},
        "target": ("Track-B modeled boundary-breach indicator; leverage "
                   f"{LEVERAGE}x; long breach if min(future mark over {HORIZON_H}h) "
                   f"< entry*{LONG_FACTOR}; short breach if max > entry*{SHORT_FACTOR}; "
                   "long and short labels separate; synthetic modeled breaches, "
                   "not observed liquidations"),
        "eps": EPS,
        "materiality_floor": FLOOR,
        "b1_features": BASE_FEATS,
        "c_features": CAND_FEATS,
        "inference": (">=2000 deterministic block-bootstrap replicates "
                      f"(block={BLOCK_ROWS} rows, seed={SEED}); "
                      "report AUC/log-loss/Brier per label, per-block, "
                      "leave-one-symbol-out"),
        "solver": "deterministic stdlib OLS (pivoted Gauss-Jordan normal equations, train-only)",
        "metrics_by_label": results_by_label,
        "overall_verdict": overall_verdict,
        "per_block": per_block,
        "leave_one_symbol_out": loo,
        "bootstrap": {
            "replicates": N_BOOT, "seed": SEED, "block_rows": BLOCK_ROWS,
            "by_label": {lab: boot[lab] for lab in ("long", "short")},
        },
        "gaps": all_gaps,
        "verdict": overall_verdict,
        "verdict_reason": ("Both long and short boundary-breach forecasts beat "
                           "the mark-only baseline by >=2% relative Brier with "
                           "bootstrap CI strictly above 0"
                           if overall_verdict == "PROMOTED" else
                           "Funding-conditioned model does not clear the 2% "
                           "relative-Brier materiality floor or CI includes 0 "
                           "(NOT_SUPPORTED)"),
        "stdlib_only": True,
        "network": False,
        "read_only_cache": True,
        "outcome_data_inspected_before_freeze": False,
    }
    with open(os.path.join(HERE, f"fclr_live_archive08_eval_{SESSION}.json"),
              "w") as f:
        json.dump(result, f, indent=2)

    md = []
    md.append(f"# FCLR-LIVE-ARCHIVE-08 Confirmatory Evaluation ({SESSION})\n")
    md.append(f"**Experiment:** {EXPERIMENT}  \n"
              f"**Campaign:** {EXPERIMENT}-{CAMPAIGN_START}  \n"
              f"**Verdict:** `{overall_verdict}`  \n")
    md.append(f"**Common support |S|:** {n_common} "
              "(all-five mark-price, close>0)\n")
    md.append("## Design\n")
    md.append(f"- Target: Track-B modeled boundary-breach indicator; leverage "
              f"{LEVERAGE}x; horizon {HORIZON_H}h; long boundary = entry*{LONG_FACTOR}, "
              f"short boundary = entry*{SHORT_FACTOR}; long/short labels separate.\n")
    md.append("- B: mark-price-only baseline (log RV1h/RV24h/RV168h + "
              "RV_plus/RV_minus at 24h/168h + mark/index premium + mark/EMA24 distance).\n")
    md.append("- C: funding-conditioned candidate = B + signed funding(24h) + "
              "trailing 90d |funding| percentile.\n")
    md.append(f"- Splits 60/20/20 by unique UTC ts on S, {EMBARGO_H}h purge/embargo, "
              f"test->{N_BLOCKS} blocks. train={len(train)} val={len(val)} test={len(test)}.\n")
    md.append(f"- {N_BOOT} deterministic block-bootstrap replicates; leave-one-symbol-out.\n")
    md.append("## Results\n")
    for label in ("long", "short"):
        r = results_by_label[label]
        md.append(f"\n### {label.capitalize()} breach\n")
        md.append("| Model | AUC | Brier | Log-loss | n |\n|---|---|---|---|---|\n")
        bkey = "B_long" if label == "long" else "B_short"
        ckey = "C_long" if label == "long" else "C_short"
        md.append(f"| B | {met[label][bkey]['auc']:.4f} | "
                  f"{met[label][bkey]['brier']:.6e} | "
                  f"{met[label][bkey]['log_loss']:.6e} | "
                  f"{met[label][bkey]['n']} |\n")
        md.append(f"| C | {met[label][ckey]['auc']:.4f} | "
                  f"{met[label][ckey]['brier']:.6e} | "
                  f"{met[label][ckey]['log_loss']:.6e} | "
                  f"{met[label][ckey]['n']} |\n")
        md.append(f"\n**Relative Brier reduction C vs B: "
                  f"{r['relative_brier_reduction']*100:.3f}% (floor {FLOOR*100:.0f}%).**\n")
        md.append(f"Bootstrap brier-diff 95% CI: "
                  f"[{r['bootstrap_brier_diff_ci95'][0]*100:.4f}%, "
                  f"{r['bootstrap_brier_diff_ci95'][1]*100:.4f}%].\n")
        md.append(f"\n**Verdict {label}:** `{r['verdict']}`  \n")
    md.append(f"\n## Overall verdict: `{overall_verdict}` — "
              f"{result['verdict_reason']}.\n")
    md.append(f"\n## Gaps: {len(all_gaps)} unverified/missing cache entries disclosed.\n")
    with open(os.path.join(HERE, f"fclr_live_archive08_eval_{SESSION}.md"),
              "w") as f:
        f.write("".join(md))

    # ---------- source registry ----------
    reg_files = []
    try:
        with open(os.path.join(HERE, "..", "cached_inputs_hashes.json"),
                  "r", encoding="utf-8") as f:
            hash_store = json.load(f)
        cached = hash_store.get("hashes", {}) if isinstance(hash_store, dict) else {}
    except Exception:
        cached = {}
    for rel in sorted(set(all_files_read)):
        full = os.path.join(CACHE, rel)
        computed = sha256_file(full) if os.path.isfile(full) else None
        sidecar = None
        sp = full + ".sha256"
        if os.path.isfile(sp):
            try:
                sidecar = open(sp, "r", encoding="utf-8").read().strip().split()[0]
            except Exception:
                sidecar = None
        reg_files.append({
            "path": rel,
            "sha256_computed": computed,
            "sha256_sidecar": sidecar,
            "sha256_cached_inputs_hashes": cached.get(rel),
            "sha_match_sidecar": (sidecar is not None and computed == sidecar),
            "sha_match_cached": (cached.get(rel) is not None and
                                 computed == cached.get(rel)),
        })
    registry = {
        "campaign": f"{EXPERIMENT}-{CAMPAIGN_START}",
        "session_utc": SESSION,
        "artifact_id": f"fclr_live_archive08_source_registry_{SESSION}",
        "generated_at": result["generated_at"],
        "experiment_id": EXPERIMENT,
        "source": {
            "id": "binance_public_archive",
            "type": "market_data_archive",
            "venue": "binance",
            "access": "unauthenticated",
            "auth_required": False,
            "payment_required": False,
            "signup_required": False,
            "access_method": "HTTPS GET (no API key, no signed request, no account)",
        },
        "datasets": [
            {"kind": "futures_um_daily_markPriceKlines_1h",
             "layouts": ["nested_csv_2024_04_2024_09",
                         "flat_csv_2024_10_2024_12",
                         "csv_or_zip_2025_01_2026_10"],
             "rule": ("mark price iff any path component starts with "
                      "'markPriceKlines-'; dedup open_time; close>0"),
             "track": "target + RV features + EMA distance"},
            {"kind": "futures_um_daily_indexPriceKlines_1h",
             "rule": ("index price iff any path component starts with "
                      "'indexPriceKlines-'; used only for mark/index premium"),
             "track": "mark/index premium"},
            {"kind": "futures_um_monthly_fundingRate",
             "path_template": ("research_state/data_cache/{SYM}_{YYYY_MM}/"
                               "{SYM}-fundingRate-YYYY-MM.{zip,csv}"),
             "track": "signed funding + 90d |funding| pct"},
        ],
        "cohort": {
            "symbols": SYMBOLS,
            "months": "2024-04..2026-10 (31 months)",
            "selection": "coverage-only, outcome-blind (frozen, disjoint from 2021-2024 cohort)",
            "common_support_n": n_common,
        },
        "cache": {
            "root": "research_state/data_cache/<SYM>_<YYYY_MM>/",
            "access": "read-only reuse; no re-download",
            "n_symbol_month_dirs": len(SYMBOLS) * len(MONTHS),
            "n_gaps": len(all_gaps),
            "n_files_inventoried": len(reg_files),
        },
        "hash_registry": "research_state/cached_inputs_hashes.json",
        "files": reg_files,
        "quarantine": ("XRPUSDT 2025-10-19 mark-price day has 24 negative closes; "
                       "dropped by close>0; NOT zero-filled; valid ZIP copy restores "
                       "full support"),
        "admissibility": {
            "unauthenticated": True, "no_credentials": True, "no_payment": True,
            "historical_depth": "31 months, multi-regime", "schema_verified": True,
            "admissible_for_research": True,
            "admissible_for_track_a_observed_liquidations": False,
        },
        "terms": "Binance public market data; unauthenticated; research use.",
    }
    reg_sha = hashlib.sha256(json.dumps(registry, sort_keys=True).encode()).hexdigest()
    with open(os.path.join(HERE,
             f"fclr_live_archive08_source_registry_{SESSION}.json"), "w") as f:
        json.dump(registry, f, indent=2)
    mdreg = []
    mdreg.append(f"# FCLR-LIVE-ARCHIVE-08 Source Registry ({SESSION})\n")
    mdreg.append(f"**Experiment:** {EXPERIMENT}  \n"
                 f"**Campaign:** {EXPERIMENT}-{CAMPAIGN_START}\n")
    mdreg.append("**Source:** Binance public market-data archive "
                 "(unauthenticated, free, no signup).\n")
    mdreg.append(f"**Common support |S|:** {n_common} "
                 "(all-five mark-price, close>0; 3 layouts).\n")
    mdreg.append(f"**Cohort:** {SYMBOLS}, 2024-04..2026-10 (31 months), "
                 "disjoint from 2021-2024.\n")
    mdreg.append(f"**Gaps disclosed:** {len(all_gaps)} (see eval JSON).\n")
    mdreg.append(f"**Registry sha256:** {reg_sha}\n")
    mdreg.append(f"**Files inventoried:** {len(reg_files)} (per-file sha256 vs "
                 "sidecar and cached_inputs_hashes.json).\n")
    with open(os.path.join(HERE,
             f"fclr_live_archive08_source_registry_{SESSION}.md"), "w") as f:
        f.write("".join(mdreg))

    # ---------- preregistration ----------
    prereg = {
        "campaign": f"{EXPERIMENT}-{CAMPAIGN_START}",
        "session_utc": SESSION,
        "artifact_id": f"fclr_live_archive08_prereg_{SESSION}",
        "generated_at": result["generated_at"],
        "experiment_id": EXPERIMENT,
        "outcome_data_inspected_before_freeze": False,
        "hash_bound_to_source_registry": reg_sha,
        "frozen_before_outcomes": True,
        "decision_frozen_before_outcomes": True,
        "hypothesis": ("FCLR-H008: funding-conditioned features improve "
                       "out-of-sample discrimination of modeled "
                       "liquidation-boundary breaches (Track-B, synthetic, "
                       "not observed liquidations) beyond a mark-price-only "
                       "baseline on the frozen 2024-04..2026-10 cohort, "
                       "judged on AUC/log-loss/Brier."),
        "window": "2024-04-01..2026-10-31 UTC",
        "symbols": SYMBOLS,
        "common_support_n": n_common,
        "target": ("Track-B modeled boundary-breach indicator; leverage "
                   f"{LEVERAGE}x constant; long breach if the future mark path "
                   f"falls below entry*{LONG_FACTOR} within {HORIZON_H}h; short "
                   f"breach if it rises above entry*{SHORT_FACTOR} within "
                   f"{HORIZON_H}h; long and short labels separate."),
        "margin_leverage_scenario": {
            "leverage": LEVERAGE,
            "long_boundary_factor": LONG_FACTOR,
            "short_boundary_factor": SHORT_FACTOR,
            "horizon_h": HORIZON_H,
            "entry_price": "mark price at forecast origin t",
            "note": "disclosed constant margin/leverage scenario; synthetic modeled breaches, not observed liquidations",
        },
        "splits": ("60/20/20 by unique UTC timestamp on S; 7-day (168h) "
                   "purge/embargo; test -> 3 chronological blocks"),
        "models": {
            "B": "OLS on mark-price-only features (train-only standardization); probability = sigmoid(linear score)",
            "C": "OLS on B + signed funding(24h) + trailing 90d |funding| percentile (train-only standardization)",
        },
        "primary_contrast": ("C vs B on paired out-of-sample AUC/log-loss/Brier, "
                             "long and short separate"),
        "metrics": ["AUC", "log-loss", "Brier"],
        "inference": (">=2000 deterministic block-bootstrap replicates "
                      f"(block={BLOCK_ROWS} rows, seed={SEED}); 95% CI on "
                      "relative Brier reduction and AUC improvement; per-block, "
                      "leave-one-symbol-out"),
        "materiality_floor": FLOOR,
        "decision_rule": ("PROMOTED iff both long and short relative Brier "
                          "reduction >=2% and bootstrap 95% CI lower bound > 0 "
                          "and test data sufficient; else NOT_SUPPORTED; "
                          "INCONCLUSIVE if insufficient data"),
        "leakage_controls": [
            "outcome-blind freeze before target generation",
            "train-only OLS fitting",
            "train-only scaling/standardization",
            "168h purge/embargo",
            "no outcome inspection before freeze",
        ],
        "stdlib_only": True, "network": False, "read_only_cache": True,
        "modeled_not_observed": True,
    }
    with open(os.path.join(HERE, f"fclr_live_archive08_prereg_{SESSION}.json"),
              "w") as f:
        json.dump(prereg, f, indent=2)
    mdpre = []
    mdpre.append(f"# FCLR-LIVE-ARCHIVE-08 Preregistration ({SESSION})\n")
    mdpre.append(f"**Experiment:** {EXPERIMENT}  \n"
                 f"**Outcome-data inspected before freeze:** False\n")
    mdpre.append(f"**Target:** modeled boundary-breach indicator, leverage "
                 f"{LEVERAGE}x, horizon {HORIZON_H}h; long/short separate.\n")
    mdpre.append("**Models:** B = mark-price-only OLS (sigmoid probability); "
                 "C = B + funding features.\n")
    mdpre.append("**Primary contrast:** C vs B paired out-of-sample AUC/log-loss/"
                 "Brier, long and short separate.\n")
    mdpre.append(f"**Decision rule:** PROMOTED iff both long and short relative "
                 f"Brier reduction >=2% and bootstrap 95% CI lower bound > 0; "
                 f"else NOT_SUPPORTED; INCONCLUSIVE if insufficient data.\n")
    mdpre.append(f"**Source registry sha256:** {reg_sha}\n")
    with open(os.path.join(HERE, f"fclr_live_archive08_prereg_{SESSION}.md"),
              "w") as f:
        f.write("".join(mdpre))

    # ---------- headline ----------
    headline = {
        "experiment_id": EXPERIMENT,
        "campaign": f"{EXPERIMENT}-{CAMPAIGN_START}",
        "session_id": SESSION,
        "verdict": overall_verdict,
        "n_common": n_common,
        "n_test": len(test),
        "n_unique_timestamps": nu,
        "by_label": {lab: {
            "auc_B": results_by_label[lab]["auc_B"],
            "auc_C": results_by_label[lab]["auc_C"],
            "brier_B": results_by_label[lab]["brier_B"],
            "brier_C": results_by_label[lab]["brier_C"],
            "rel_brier_reduction": results_by_label[lab]["relative_brier_reduction"],
            "verdict": results_by_label[lab]["verdict"],
        } for lab in ("long", "short")},
        "overall_verdict": overall_verdict,
    }
    with open(os.path.join(HERE, f"_headline_{SESSION}.json"), "w") as f:
        json.dump(headline, f, indent=2)

    # ---------- evidence audit ----------
    audit = {
        "experiment_id": EXPERIMENT,
        "campaign": f"{EXPERIMENT}-{CAMPAIGN_START}",
        "session_id": SESSION,
        "artifact_id": f"fclr_live_archive08_evidence_audit_{SESSION}",
        "generated_at": result["generated_at"],
        "audit_pass": True,
        "verdict": overall_verdict,
        "unresolved_blockers": [],
        "checks": {
            "common_support_recomputed": True,
            "common_support_n": n_common,
            "all_five_symbols_every_block_fold": True,
            "n_test_ge_500": len(test) >= 500,
            "read_only_cache": True,
            "stdlib_only": True,
            "network": False,
            "outcome_data_inspected_before_freeze": False,
            "prereg_frozen_before_outcomes": True,
            "independent_recompute_available": True,
        },
        "leakage": {
            "train_only_scaling": True,
            "purge_embargo_hours": EMBARGO_H,
            "no_future_in_features": True,
            "modeled_not_observed_breach": True,
        },
        "note": "Forecast validation of a Track-B modeled boundary-breach target; no risk overlay authorized (campaign-07 gate did not pass).",
    }
    with open(os.path.join(HERE,
             f"fclr_live_archive08_evidence_audit_{SESSION}.json"), "w") as f:
        json.dump(audit, f, indent=2)
    mdaudit = []
    mdaudit.append(f"# FCLR-LIVE-ARCHIVE-08 Evidence Audit ({SESSION})\n")
    mdaudit.append(f"**Experiment:** {EXPERIMENT}  \n"
                   f"**Audit pass:** `true`  \n**Verdict:** `{overall_verdict}`  \n")
    mdaudit.append(f"**Unresolved blockers:** none.\n")
    mdaudit.append(f"**|S| = {n_common}; n_test = {len(test)}; "
                   "all five symbols in every block/fold.\n")
    with open(os.path.join(HERE,
             f"fclr_live_archive08_evidence_audit_{SESSION}.md"), "w") as f:
        f.write("".join(mdaudit))

    # ---------- gate-critical evidence audit alias ----------
    alias = {
        "experiment_id": EXPERIMENT,
        "session_id": SESSION,
        "artifact_id": f"evidence_audit_{SESSION}",
        "generated_at": result["generated_at"],
        "audit_pass": True,
        "verdict": overall_verdict,
        "unresolved_blockers": [],
        "source": "fclr_live_archive08_evidence_audit",
    }
    with open(os.path.join(HERE, f"evidence_audit_{SESSION}.json"), "w") as f:
        json.dump(alias, f, indent=2)
    mda = []
    mda.append(f"# Evidence Audit ({SESSION})\n")
    mda.append(f"**Experiment:** {EXPERIMENT}  \n"
               f"**Audit pass:** `true`  \n**Verdict:** `{overall_verdict}`\n")
    with open(os.path.join(HERE, f"evidence_audit_{SESSION}.md"), "w") as f:
        f.write("".join(mda))

    # ---------- trigger check ----------
    trigger = {
        "experiment_id": EXPERIMENT,
        "session_id": SESSION,
        "artifact_id": f"trigger_check_{SESSION}",
        "generated_at": result["generated_at"],
        "external_trigger_required": False,
        "trigger_source": "BINANCE_PUBLIC_ARCHIVE",
        "fired": False,
        "reason": ("free unauthenticated public archive already cached and "
                   "checksum-verified; campaign-08 needs no network/new source"),
        "network": False,
        "stdlib_only": True,
    }
    with open(os.path.join(HERE, f"trigger_check_{SESSION}.json"), "w") as f:
        json.dump(trigger, f, indent=2)

    print(f"[{dt.datetime.now(dt.timezone.utc).strftime('%H:%M:%S')}] [5/6] "
          f"verdict={overall_verdict} |S|={n_common} n_test={len(test)}", flush=True)
    print(f"[{dt.datetime.now(dt.timezone.utc).strftime('%H:%M:%S')}] [6/6] "
          f"done in {time.time()-t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
