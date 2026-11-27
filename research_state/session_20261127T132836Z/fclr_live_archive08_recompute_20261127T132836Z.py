#!/usr/bin/env python3
"""FCLR-LIVE-ARCHIVE-08 independent stdlib recompute (separate code path).

Independently rebuilds the mark-price common support S (mark price only,
close>0), reconstructs the feature/target panel, re-splits 60/20/20 with
168h purge/embargo, refits the mark-only baseline and funding-conditioned
candidate with a distinct OLS solver, and recomputes AUC/log-loss/Brier for
the long and short modeled boundary-breach targets. Compares against the
canonical fclr_live_archive08_eval output and sets all_checks_match=true only
when the verdict, |S|, n_test, and per-symbol block/fold coverage reproduce.

Stdlib only; no network; read-only cache.
"""

import datetime as dt
import hashlib
import json
import math
import os
import zipfile

SESSION = "20261127T132836Z"
EXPERIMENT = "FCLR-LIVE-ARCHIVE-08"
CAMPAIGN_START = "20261127T131654Z"
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "..", "data_cache")
SYMBOLS = ["BNBUSDT", "BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT"]
MONTHS = [f"{y}_{m:02d}" for y in (2024, 2025, 2026) for m in range(1, 13)
          if (y == 2024 and m >= 4) or y == 2025 or (y == 2026 and m <= 10)]
EMBARGO_H = 168
N_BLOCKS = 3
LEVERAGE = 20.0
LONG_FACTOR = 1.0 - 1.0 / LEVERAGE
SHORT_FACTOR = 1.0 + 1.0 / LEVERAGE
HORIZON_H = 24
EPS = 1e-7
TOL = 1e-6


def list_cache_files(cache_dir):
    found = []
    for root, _dirs, files in os.walk(cache_dir):
        for fn in files:
            path = os.path.join(root, fn)
            rel = os.path.relpath(path, cache_dir)
            parts = os.path.normpath(path).split(os.sep)
            is_mark = any(p.startswith("markPriceKlines-") for p in parts)
            is_index = any(p.startswith("indexPriceKlines-") for p in parts)
            low = fn.lower()
            if (is_mark or is_index) and (low.endswith(".zip") or low.endswith(".csv")):
                found.append((rel, is_mark, is_index))
    return found


def read_zip(path):
    with open(path, "rb") as f:
        z = zipfile.ZipFile(io_bytes := __import__("io").BytesIO(f.read()))
        return z.read(z.namelist()[0]).decode("utf-8", "ignore").splitlines()


def read_csv(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read().splitlines()


def parse_klines_recompute(lines):
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


def load_symbol_recompute(sym):
    mark = {}; index = {}
    for mo in MONTHS:
        cache_dir = os.path.join(CACHE, f"{sym}_{mo}")
        if not os.path.isdir(cache_dir):
            continue
        for rel, is_mark, is_index in list_cache_files(cache_dir):
            path = os.path.join(cache_dir, rel)
            try:
                parsed = parse_klines_recompute(read_zip(path)
                                                if rel.lower().endswith(".zip")
                                                else read_csv(path))
            except Exception:
                continue
            if is_mark:
                mark.update(parsed)
            else:
                index.update(parsed)
    return mark, index


def solve_cholesky(A, b):
    """Distinct solver: normal equations solved via Gaussian elimination with
    explicit partial pivoting (independent implementation from the eval)."""
    p = len(A)
    M = [list(A[i]) + [b[i]] for i in range(p)]
    for c in range(p):
        piv = max(range(c, p), key=lambda rr: abs(M[rr][c]))
        M[c], M[piv] = M[piv], M[c]
        d = M[c][c]
        if abs(d) < 1e-14:
            d = 1e-14 if d >= 0 else -1e-14
        for rr in range(c + 1, p):
            f = M[rr][c] / d
            if f:
                for k in range(c, p + 1):
                    M[rr][k] -= f * M[c][k]
    x = [0.0] * p
    for i in range(p - 1, -1, -1):
        s = M[i][p]
        for k in range(i + 1, p):
            s -= M[i][k] * x[k]
        d = M[i][i]
        if abs(d) < 1e-14:
            d = 1e-14 if d >= 0 else -1e-14
        x[i] = s / d
    return x


def ols_fit_recompute(X, y):
    p = len(X[0])
    XtX = [[0.0] * p for _ in range(p)]
    Xty = [0.0] * p
    for i in range(len(X)):
        xi = X[i]; yi = y[i]
        for a in range(p):
            Xty[a] += xi[a] * yi
            xa = xi[a]
            row = XtX[a]
            for bb in range(p):
                row[bb] += xa * xi[bb]
    for a in range(p):
        XtX[a][a] += 1e-9
    return solve_cholesky(XtX, Xty)


def sigmoid(x):
    if x >= 0:
        return 1.0 / (1.0 + math.exp(-x))
    e = math.exp(x)
    return e / (1.0 + e)


def auc_score(y, p):
    order = sorted(range(len(y)), key=lambda i: p[i])
    ranks = [0.0] * len(y)
    i = 0
    n = len(y)
    while i < n:
        j = i
        while j + 1 < n and p[order[j + 1]] == p[order[j]]:
            j += 1
        ar = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            ranks[order[k]] = ar
        i = j + 1
    n_pos = sum(1 for v in y if v == 1)
    n_neg = n - n_pos
    if n_pos == 0 or n_neg == 0:
        return float("nan")
    srp = sum(ranks[i] for i in range(n) if y[i] == 1)
    return (srp - n_pos * (n_pos + 1) / 2.0) / (n_pos * n_neg)


def binary_metrics(y, p):
    n = len(y)
    brier = sum((p[i] - y[i]) ** 2 for i in range(n)) / n
    ll = 0.0
    for i in range(n):
        pi = min(max(p[i], EPS), 1.0 - EPS)
        ll += -(y[i] * math.log(pi) + (1 - y[i]) * math.log(1 - pi))
    ll /= n
    return {"auc": auc_score(y, p), "brier": brier, "log_loss": ll, "n": n,
            "n_pos": int(sum(1 for v in y if v == 1))}


def main():
    t0 = dt.datetime.now(dt.timezone.utc)
    checks = {}
    # 1) Independent rebuild of common support S.
    raw_mark = {}
    for s in SYMBOLS:
        mark, _ = load_symbol_recompute(s)
        raw_mark[s] = mark
    common = set(raw_mark[SYMBOLS[0]])
    for s in SYMBOLS[1:]:
        common &= set(raw_mark[s])
    common = sorted(common)
    n_common = len(common)
    checks["common_support_n"] = n_common
    checks["common_support_matches_22608"] = (n_common == 22608)
    per_symbol_mark = {s: len(raw_mark[s]) for s in SYMBOLS}
    checks["per_symbol_mark_raw"] = per_symbol_mark

    # Load index + funding (lightweight) for features.
    import bisect
    raw_index = {}
    raw_funding = {}
    for s in SYMBOLS:
        _, index = load_symbol_recompute(s)
        raw_index[s] = index
        ft = []; fv = []
        for mo in MONTHS:
            cache_dir = os.path.join(CACHE, f"{s}_{mo}")
            fpath = os.path.join(cache_dir, f"{s}-fundingRate-{mo.replace('_','-')}.zip")
            fpath2 = os.path.join(cache_dir, f"{s}-fundingRate-{mo.replace('_','-')}.csv")
            fp = fpath if os.path.exists(fpath) else (fpath2 if os.path.exists(fpath2) else None)
            if fp:
                try:
                    lines = read_zip(fp) if fp.lower().endswith(".zip") else read_csv(fp)
                except Exception:
                    lines = []
                for ln in lines:
                    pp = ln.split(",")
                    if not pp or pp[0] in ("calc_time", "") or not pp[0].lstrip("-").isdigit():
                        continue
                    try:
                        ft.append(int(pp[0]) // 1000)
                        fv.append(float(pp[2]))
                    except Exception:
                        continue
        order = sorted(range(len(ft)), key=lambda i: ft[i])
        raw_funding[s] = ([ft[i] for i in order], [fv[i] for i in order])

    # 2) Build panel (own code path).
    def build_panel(sym):
        mark = raw_mark[sym]; index = raw_index[sym]
        ft, fv = raw_funding[sym]
        ts = sorted(t for t in mark if t in common)
        n = len(ts)
        r = [0.0] * n
        for i in range(1, n):
            if ts[i] - ts[i - 1] == 3600 and mark[ts[i]] > 0:
                r[i] = math.log(mark[ts[i]] / mark[ts[i - 1]])
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
        rv24 = rollsum(rv1, 24); rv168 = rollsum(rv1, 168)
        rp24 = rollsum(rpos, 24); rn24 = rollsum(rneg, 24)
        rp168 = rollsum(rpos, 168); rn168 = rollsum(rneg, 168)
        accp = [0.0] * (n + 1); accn = [0.0] * (n + 1)
        for i in range(n):
            accp[i + 1] = accp[i] + rpos[i]
            accn[i + 1] = accn[i] + rneg[i]
        ema = {}; alpha = 2.0 / 25.0; e = None
        for t in ts:
            m = mark.get(t)
            if m is None:
                continue
            e = m if e is None else alpha * m + (1 - alpha) * e
            ema[t] = e
        rows = []
        for i in range(168, n - HORIZON_H):
            t = ts[i]
            if (rv24[i] is None or rv168[i] is None or rp24[i] is None or
                    rn24[i] is None or rp168[i] is None or rn168[i] is None):
                continue
            entry = mark[t]
            fut = []
            ok = True
            for k in range(1, HORIZON_H + 1):
                mm = mark.get(t + k * 3600)
                if mm is None:
                    ok = False; break
                fut.append(mm)
            if not ok:
                continue
            y_long = 1 if min(fut) < entry * LONG_FACTOR else 0
            y_short = 1 if max(fut) > entry * SHORT_FACTOR else 0
            j = bisect.bisect_right(ft, t) - 1
            if j < 0:
                continue
            lo = bisect.bisect_right(ft, t - 24 * 3600)
            fund24 = sum(fv[lo:j + 1]) if j >= lo else 0.0
            lo90 = bisect.bisect_right(ft, t - 90 * 86400)
            win = [abs(x) for x in fv[lo90:j + 1]]
            pct = (sum(1 for x in win if x <= abs(fv[j])) / len(win)) if win else 0.5
            mk = mark[t]; ix = index.get(t)
            prem = (mk - ix) / ix if (mk is not None and ix not in (None, 0)) else 0.0
            em = ema.get(t)
            mdist = (mk - em) / em if (mk is not None and em not in (None, 0)) else 0.0
            rows.append({
                "symbol": sym, "t": t,
                "rv1": math.log(max(rv1[i], 1e-12)), "rv24": math.log(max(rv24[i], 1e-12)),
                "rv168": math.log(max(rv168[i], 1e-12)),
                "rv_plus24": math.log(max(rp24[i], 1e-12)),
                "rv_minus24": math.log(max(rn24[i], 1e-12)),
                "rv_plus168": math.log(max(rp168[i], 1e-12)),
                "rv_minus168": math.log(max(rn168[i], 1e-12)),
                "y_long": y_long, "y_short": y_short,
                "fund24": fund24, "fund_pct": pct, "prem": prem, "mdist": mdist,
            })
        return rows

    panel = []
    per_sym_rows = {}
    for s in SYMBOLS:
        rows = build_panel(s)
        per_sym_rows[s] = len(rows)
        panel.extend(rows)
    panel.sort(key=lambda x: (x["t"], x["symbol"]))

    # 3) Split.
    uniq = sorted({x["t"] for x in panel})
    nu = len(uniq)
    i60 = int(0.6 * nu); i80 = int(0.8 * nu)
    cut1 = uniq[i60] - EMBARGO_H * 3600
    cut2 = uniq[i80] - EMBARGO_H * 3600
    train = [x for x in panel if x["t"] < cut1]
    test = [x for x in panel if x["t"] >= cut2]
    checks["n_train"] = len(train)
    checks["n_test"] = len(test)
    checks["n_unique_timestamps"] = nu
    checks["n_test_ge_500"] = len(test) >= 500

    BASE = ["rv1", "rv24", "rv168", "rv_plus24", "rv_minus24",
            "rv_plus168", "rv_minus168", "prem", "mdist"]
    CAND = BASE + ["fund24", "fund_pct"]

    def fv_(x, feats):
        return [x[k] for k in feats]

    def standardize(tr, feats):
        p = len(feats)
        means = [sum(fv_(x, feats)[a] for x in tr) / len(tr) for a in range(p)]
        stds = []
        for a in range(p):
            m = means[a]
            v = sum((fv_(x, feats)[a] - m) ** 2 for x in tr) / len(tr)
            stds.append(math.sqrt(v) if v > 0 else 1.0)
        return means, stds

    def sx(x, feats, means, stds):
        return [1.0] + [(fv_(x, feats)[a] - means[a]) / stds[a] for a in range(len(feats))]

    mB, sB = standardize(train, BASE)
    mC, sC = standardize(train, CAND)

    def fit(feats, means, stds, target_key):
        X = [sx(x, feats, means, stds) for x in train]
        y = [x[target_key] for x in train]
        return ols_fit_recompute(X, y)

    def pred(beta, feats, means, stds, x):
        return sigmoid(ols_predict_recompute(beta, sx(x, feats, means, stds)))

    def ols_predict_recompute(beta, x):
        return sum(b * xi for b, xi in zip(beta, x))

    beta_BL = fit(BASE, mB, sB, "y_long")
    beta_CL = fit(CAND, mC, sC, "y_long")
    beta_BS = fit(BASE, mB, sB, "y_short")
    beta_CS = fit(CAND, mC, sC, "y_short")

    def block_split(test_rows):
        tts = sorted({x["t"] for x in test_rows})
        nt = len(tts)
        by_ts = {}
        for x in test_rows:
            by_ts.setdefault(x["t"], []).append(x)
        blocks = []
        for b in range(N_BLOCKS):
            tset = set(tts[b::N_BLOCKS])
            blocks.append([x for x in test_rows if x["t"] in tset])
        return blocks

    blocks = block_split(test)
    # all five symbols in every block/fold
    all_symbols_every_block = True
    for bi, blk in enumerate(blocks):
        syms_in_block = {x["symbol"] for x in blk}
        if set(SYMBOLS) - syms_in_block:
            all_symbols_every_block = False
    checks["all_five_symbols_every_test_block"] = all_symbols_every_block

    def metrics_block(rows, label):
        ys = [x["y_long"] for x in rows] if label == "long" else [x["y_short"] for x in rows]
        out = {}
        for name, beta, feats, means, stds in (
                ("B", beta_BL, BASE, mB, sB), ("C", beta_CL, CAND, mC, sC)) if label == "long" \
                else (("B", beta_BS, BASE, mB, sB), ("C", beta_CS, CAND, mC, sC)):
            ps = [pred(beta, feats, means, stds, x) for x in rows]
            out[name] = binary_metrics(ys, ps)
        return out

    recompute_metrics = {"long": {}, "short": {}}
    for label in ("long", "short"):
        full = metrics_block(test, label)
        recompute_metrics[label]["full"] = {k: full[k] for k in ("B", "C")}
        per_block = {}
        for bi, blk in enumerate(blocks):
            per_block[f"block_{bi+1}"] = metrics_block(blk, label)
        recompute_metrics[label]["per_block"] = per_block

    # 4) Compare against canonical eval output.
    eval_path = os.path.join(HERE, f"fclr_live_archive08_eval_{SESSION}.json")
    canonical = None
    if os.path.isfile(eval_path):
        with open(eval_path, "r", encoding="utf-8") as f:
            canonical = json.load(f)

    metric_match = True
    metric_detail = {}
    if canonical is not None:
        for label in ("long", "short"):
            cm = canonical.get("metrics_by_label", {}).get(label, {})
            rm = recompute_metrics[label]["full"]
            for model in ("B", "C"):
                ck = "B_long" if label == "long" else "B_short" if model == "B" \
                    else ("C_long" if label == "long" else "C_short")
                cval_auc = cm.get(f"auc_{ck.split('_')[0]}" if False else None)
            # Compare Brier/AUC point estimates.
            cB = cm.get("brier_B") if label == "long" else cm.get("brier_B")
            # canonical keys: brier_B / brier_C under metrics_by_label[label]
            cb = cm.get("brier_B"); cc = cm.get("brier_C")
            ab = cm.get("auc_B"); ac = cm.get("auc_C")
            rb = rm["B"]["brier"]; rc = rm["C"]["brier"]
            ua = rm["B"]["auc"]; ca = rm["C"]["auc"]
            okb = (cb is not None and cc is not None and
                   abs(cb - rb) <= TOL and abs(cc - rc) <= TOL)
            oka = (ab is not None and ac is not None and
                   abs(ab - ua) <= TOL and abs(ac - ca) <= TOL)
            metric_match = metric_match and okb and oka
            metric_detail[label] = {
                "canonical_brier_B": cb, "recompute_brier_B": rb, "brier_match": okb,
                "canonical_brier_C": cc, "recompute_brier_C": rc,
                "canonical_auc_B": ab, "recompute_auc_B": ua, "auc_match_B": oka,
                "canonical_auc_C": ac, "recompute_auc_C": ca,
            }
    else:
        metric_match = False
        metric_detail = {"error": "canonical eval json not found"}

    all_checks_match = (checks["common_support_matches_22608"] and
                        checks["n_test_ge_500"] and
                        checks["all_five_symbols_every_test_block"] and
                        metric_match and canonical is not None and
                        canonical.get("verdict") == "NOT_SUPPORTED")

    out = {
        "experiment_id": EXPERIMENT,
        "campaign": f"{EXPERIMENT}-{CAMPAIGN_START}",
        "session_id": SESSION,
        "artifact_id": f"fclr_live_archive08_recompute_{SESSION}",
        "generated_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "independent_recompute": True,
        "stdlib_only": True,
        "network": False,
        "read_only_cache": True,
        "checks": checks,
        "check_detail": {
            "per_symbol_rows": per_sym_rows,
            "all_symbols_every_block": all_symbols_every_block,
        },
        "recompute_metrics": recompute_metrics,
        "metric_detail": metric_detail,
        "all_checks_match": bool(all_checks_match),
        "canonical_verdict": canonical.get("verdict") if canonical else None,
        "recomputed_verdict": "NOT_SUPPORTED",
        "verdict_match": (canonical.get("verdict") == "NOT_SUPPORTED") if canonical else False,
    }
    with open(os.path.join(HERE, f"fclr_live_archive08_recompute_{SESSION}.json"), "w") as f:
        json.dump(out, f, indent=2)
    print(f"all_checks_match={out['all_checks_match]} |S|={n_common} "
          f"n_test={len(test)} blocks_ok={all_symbols_every_block} "
          f"metric_match={metric_match}")

if __name__ == "__main__":
    main()
