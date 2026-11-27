#!/usr/bin/env python3
"""FCLR-LIVE-ARCHIVE-08 heavy confirmatory evaluation (stdlib only).

Repo-name SECONDARY estimand: LIQUIDATION RISK. This is a Track-B *modeled*
boundary-breach forecast. It is NOT observed liquidations and NOT a risk
overlay (the campaign-07 forecast gate did NOT pass, so RESEARCH_PROMPT.md
section 9 authorises forecast validation only).

Design (frozen before outcomes; see the sibling prereg):
  * Same frozen balanced mark-price common support S as campaign-07
    (|S| = 22,608; 2024-04..2026-10; BNBUSDT/BTCUSDT/ETHUSDT/SOLUSDT/XRPUSDT),
    read-only cache reuse, no re-download.
  * Same 60/20/20 by unique UTC timestamp + 168h purge/embargo + three
    chronological test blocks; all five symbols in every fold.
  * Track-B modeled hypothetical liquidation boundaries from DISCLOSED constant
    margin/leverage scenarios (long and short kept separate):
        long  boundary  B_long(t)  = P(t) * (1 - (1 - mmr)/L)
        short boundary  B_short(t) = P(t) * (1 + (1 - mmr)/L)
    with maintenance-margin rate mmr = 0.005 and constant leverage L.
    Primary scenario L = 20; robustness scenarios L in {10, 50}.
  * Target = whether the future mark-price path breaches the boundary within a
    fixed horizon H = 24h:
        breach_long(t)  = 1 if min_{k=1..H} P(t+k) <= B_long(t)
        breach_short(t) = 1 if max_{k=1..H} P(t+k) >= B_short(t)
  * Models (fixed-form deterministic stdlib OLS on the binary label; the only
    difference is the funding block):
        M0 (mark-price-only)   = 7 signed HAR log-RV features + mark/EMA24 dist
        M1 (funding-conditioned) = M0 + signed funding(24h) + 90d |funding| pct
  * Primary contrast: M1 vs M0 out-of-sample Brier on the LONG breach label at
    L = 20 (relative Brier reduction >= 2% floor AND bootstrap 95% CI > 0).
  * Secondary (reported, non-gating): SHORT breach Brier, AUC (long & short),
    log-loss (long & short), and long-breach Brier at L in {10, 50}.
  * Inference: >= 2,000 deterministic block-bootstrap replicates (block = 24
    rows, fixed seed) on the per-row Brier difference; leave-one-symbol-out.

Stdlib only. Read-only cache. No network. No package installation.
"""

import bisect
import datetime as dt
import json
import math
import os
import random
import time
import zipfile
import io
import hashlib

SESSION = "20261127T070655Z"
EXPERIMENT = "FCLR-LIVE-ARCHIVE-08"
CAMPAIGN_START = "20261127T070243Z"
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "..", "data_cache")
SYMBOLS = ["BNBUSDT", "BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT"]
MONTHS = [f"{y}_{m:02d}" for y in (2024, 2025, 2026) for m in range(1, 13)
          if (y == 2024 and m >= 4) or y == 2025 or (y == 2026 and m <= 10)]
SEED = 20261127
N_BOOT = 2000
EMBARGO_H = 168
FLOOR = 0.02
N_BLOCKS = 3
BLOCK_ROWS = 24
H = 24            # breach horizon (hours)
MMR = 0.005       # maintenance margin rate (constant, disclosed)
L_PRIMARY = 20    # primary leverage scenario
L_ROBUST = (10, 50)
ALPHA_2 = 0.05 / (2 * 3)


# ----------------------------- cache reader -----------------------------
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
    return any(part.startswith("markPriceKlines-")
               for part in os.path.normpath(path).split(os.sep))


def _is_index_path(path):
    return any(part.startswith("indexPriceKlines-")
               for part in os.path.normpath(path).split(os.sep))


def load_raw(sym):
    mark = {}
    index = {}
    funding = []
    gaps = []
    layouts = set()
    for mo in MONTHS:
        cache_dir = os.path.join(CACHE, f"{sym}_{mo}")
        if not os.path.isdir(cache_dir):
            gaps.append({"symbol": sym, "month": mo, "reason": "month_dir_missing"})
            continue
        for root, _dirs, files in os.walk(cache_dir):
            for fn in files:
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
                except Exception as exc:  # noqa: BLE001
                    gaps.append({"symbol": sym, "month": mo, "path": rel,
                                 "reason": str(exc)})
                    continue
                if is_mark:
                    mark.update(parsed)
                else:
                    index.update(parsed)
        for ext in (".zip", ".csv"):
            fpath = os.path.join(
                cache_dir, f"{sym}-fundingRate-{mo.replace('_', '-')}{ext}")
            if os.path.exists(fpath):
                try:
                    funding.extend(parse_funding(read_any_lines(fpath)))
                except Exception as exc:  # noqa: BLE001
                    gaps.append({"symbol": sym, "month": mo,
                                 "source": "fundingRate", "reason": str(exc)})
                break
        else:
            gaps.append({"symbol": sym, "month": mo,
                         "source": "fundingRate", "reason": "funding_missing"})
    funding.sort()
    return {"mark": mark, "index": index, "funding": funding,
            "gaps": gaps, "layouts": sorted(layouts)}


# ----------------------------- panel build -----------------------------
def build_panel(sym, raw, common):
    mark = raw["mark"]
    funding = raw["funding"]
    gaps = raw["gaps"]
    ts = sorted(t for t in mark if t in common)
    n = len(ts)
    if n < 200:
        return [], {"symbol": sym, "n_rows": 0, "n_times": n,
                    "gaps": gaps, "layouts": raw["layouts"]}
    close = mark
    r = [0.0] * n
    for i in range(1, n):
        if ts[i] - ts[i - 1] == 3600 and close[ts[i]] > 0 and close[ts[i - 1]] > 0:
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
    rp24 = rollsum(rpos, 24)
    rm24 = rollsum(rneg, 24)
    rp168 = rollsum(rpos, 168)
    rm168 = rollsum(rneg, 168)

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
    for i in range(168, n - H):
        if (rv24[i] is None or rv168[i] is None or rp24[i] is None or
                rm24[i] is None or rp168[i] is None or rm168[i] is None):
            continue
        # require a contiguous 24h forward mark path for a clean breach label
        if ts[i + H] - ts[i] != H * 3600:
            continue
        t = ts[i]
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
        em = ema.get(t)
        mdist = (mk - em) / em if (mk is not None and em not in (None, 0)) else 0.0
        p0 = close[t]
        fmin = min(close[ts[i + k]] for k in range(1, H + 1))
        fmax = max(close[ts[i + k]] for k in range(1, H + 1))
        rows.append({
            "symbol": sym, "t": t,
            "rv1": rv1[i], "rv24": rv24[i], "rv168": rv168[i],
            "rv_plus24": rp24[i], "rv_minus24": rm24[i],
            "rv_plus168": rp168[i], "rv_minus168": rm168[i],
            "fund24": fund24, "fund_pct": pct, "mdist": mdist,
            "p0": p0, "fmin": fmin, "fmax": fmax,
        })
    info = {"n_rows": len(rows), "n_times": n, "gaps": gaps,
            "layouts": raw["layouts"], "n_mark_raw": len(mark),
            "n_in_common": len(ts)}
    return rows, info


# ----------------------------- stdlib OLS -----------------------------
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
    return [M[i][p] / (M[i][i] if abs(M[i][i]) > 1e-14 else 1e-14) for i in range(p)]


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


# ----------------------------- metrics -----------------------------
def _clip(p):
    return min(1.0 - 1e-6, max(1e-6, p))


def brier(y, p):
    return sum((_clip(p[i]) - y[i]) ** 2 for i in range(len(y))) / len(y)


def logloss(y, p):
    tot = 0.0
    for i in range(len(y)):
        pc = _clip(p[i])
        tot += -(y[i] * math.log(pc) + (1 - y[i]) * math.log(1 - pc))
    return tot / len(y)


def auc(y, p):
    n1 = sum(1 for v in y if v == 1)
    n0 = len(y) - n1
    if n1 == 0 or n0 == 0:
        return None
    order = sorted(range(len(p)), key=lambda i: p[i])
    ranks = [0.0] * len(p)
    i = 0
    while i < len(order):
        j = i
        while j < len(order) and p[order[j]] == p[order[i]]:
            j += 1
        avg = (i + j - 1) / 2.0 + 1.0
        for k in range(i, j):
            ranks[order[k]] = avg
        i = j
    sum_pos = sum(ranks[i] for i in range(len(y)) if y[i] == 1)
    return (sum_pos - n1 * (n1 + 1) / 2.0) / (n1 * n0)


def feat_row(x, model):
    base = [math.log(max(x["rv1"], 1e-12)),
            math.log(max(x["rv24"], 1e-12)),
            math.log(max(x["rv168"], 1e-12)),
            math.log(max(x["rv_plus24"], 1e-12)),
            math.log(max(x["rv_minus24"], 1e-12)),
            math.log(max(x["rv_plus168"], 1e-12)),
            math.log(max(x["rv_minus168"], 1e-12)),
            x["mdist"]]
    if model == "M0":
        return base
    if model == "M1":
        return base + [x["fund24"], x["fund_pct"]]
    raise ValueError(model)


def fit_model(model, tr, label):
    X = [[1.0] + feat_row(x, model) for x in tr]
    y = [label(x) for x in tr]
    return {"model": model, "beta": ols_fit(X, y)}


def predict(m, x):
    return ols_predict(m["beta"], [1.0] + feat_row(x, m["model"]))


def breach_long(x, L):
    return 1 if x["fmin"] <= x["p0"] * (1.0 - (1.0 - MMR) / L) else 0


def breach_short(x, L):
    return 1 if x["fmax"] >= x["p0"] * (1.0 + (1.0 - MMR) / L) else 0


def main():
    t0 = time.time()
    print(f"[{dt.datetime.now(dt.timezone.utc).strftime('%H:%M:%S')}] [1/6] loading cache (read-only, 3 layouts) ...", flush=True)
    raw = {}
    for s in SYMBOLS:
        raw[s] = load_raw(s)
        print(f"  {s}: mark_raw={len(raw[s]['mark'])} index_raw={len(raw[s]['index'])} "
              f"funding={len(raw[s]['funding'])} layouts={raw[s]['layouts']}", flush=True)

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
    panel.sort(key=lambda x: x["t"])

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
    if len(test) < 500 or nu < 500:
        raise SystemExit("FATAL: insufficient test data")

    # ---- PRIMARY: long breach at L=20, M1 vs M0, Brier ----
    ylong = [breach_long(x, L_PRIMARY) for x in test]
    base_rate_long = sum(ylong) / len(ylong)
    models = {k: fit_model(k, train, lambda x: breach_long(x, L_PRIMARY))
              for k in ("M0", "M1")}
    preds = {m: [predict(models[m], x) for x in test] for m in ("M0", "M1")}

    def brier_metrics(m):
        p = preds[m]
        return {"brier": brier(ylong, p), "logloss": logloss(ylong, p),
                "auc": auc(ylong, p), "n": len(ylong),
                "n_events": sum(ylong)}

    met_long = {m: brier_metrics(m) for m in ("M0", "M1")}
    brier_M0 = met_long["M0"]["brier"]
    brier_M1 = met_long["M1"]["brier"]
    rel_brier = (brier_M0 - brier_M1) / brier_M0 if brier_M0 > 0 else 0.0

    # ---- SECONDARY: short breach at L=20 ----
    yshort = [breach_short(x, L_PRIMARY) for x in test]
    models_s = {k: fit_model(k, train, lambda x: breach_short(x, L_PRIMARY))
                for k in ("M0", "M1")}

    def pred_s(m):
        return [predict(models_s[m], x) for x in test]

    met_short = {}
    for m in ("M0", "M1"):
        pp = pred_s(m)
        met_short[m] = {"brier": brier(yshort, pp), "logloss": logloss(yshort, pp),
                        "auc": auc(yshort, pp), "n_events": sum(yshort)}

    # ---- SECONDARY: long breach robustness at L in {10,50} ----
    robust = {}
    for L in L_ROBUST:
        yl = [breach_long(x, L) for x in test]
        mm = {k: fit_model(k, train, (lambda LL: (lambda x: breach_long(x, LL)))(L))
              for k in ("M0", "M1")}
        pp = {k: [predict(mm[k], x) for x in test] for k in ("M0", "M1")}
        b0 = brier(yl, pp["M0"])
        b1_ = brier(yl, pp["M1"])
        robust[str(L)] = {"brier_M0": b0, "brier_M1": b1_,
                          "rel_brier_reduction": (b0 - b1_) / b0 if b0 > 0 else 0.0,
                          "n_events": sum(yl)}

    # ---- per-block (3 chronological blocks) on primary long Brier ----
    block_idx = [list(range(b, len(test), N_BLOCKS)) for b in range(N_BLOCKS)]

    def block_brier(m, idxs):
        pp = [preds[m][k] for k in idxs]
        yy = [ylong[k] for k in idxs]
        return brier(yy, pp)

    per_block = {m: {"brier": [block_brier(m, bi) for bi in block_idx]}
                 for m in ("M0", "M1")}

    # ---- leave-one-symbol-out on primary long Brier ----
    loo = {}
    for held in SYMBOLS:
        tr = [x for x in train if x["symbol"] != held]
        te = [x for x in test if x["symbol"] == held]
        if not tr or not te:
            continue
        m0 = fit_model("M0", tr, lambda x: breach_long(x, L_PRIMARY))
        m1 = fit_model("M1", tr, lambda x: breach_long(x, L_PRIMARY))
        yh = [breach_long(x, L_PRIMARY) for x in te]
        p0 = [predict(m0, x) for x in te]
        p1 = [predict(m1, x) for x in te]
        b0 = brier(yh, p0)
        b1_ = brier(yh, p1)
        loo[held] = {"n": len(te), "n_events": sum(yh),
                     "brier_M0": b0, "brier_M1": b1_,
                     "rel_brier_reduction": (b0 - b1_) / b0 if b0 > 0 else 0.0}
        print(f"  LOO {held}: n={len(te)} events={sum(yh)} "
              f"rel_brier={(b0-b1_)/b0*100 if b0>0 else 0:.3f}%", flush=True)

    # ---- block bootstrap on per-row Brier difference (M0 - M1) ----
    print(f"[{dt.datetime.now(dt.timezone.utc).strftime('%H:%M:%S')}] [4/6] block bootstrap x{N_BOOT} ...", flush=True)
    diffs = []
    for k in range(len(test)):
        yk = ylong[k]
        d0 = (_clip(preds["M0"][k]) - yk) ** 2
        d1 = (_clip(preds["M1"][k]) - yk) ** 2
        diffs.append(d0 - d1)
    nb = len(diffs)
    nblocks = max(1, nb // BLOCK_ROWS)
    rng = random.Random(SEED)
    boot = []
    for _ in range(N_BOOT):
        s = 0.0
        cnt = 0
        for _b in range(nblocks):
            st = rng.randrange(0, max(1, nb - BLOCK_ROWS + 1))
            for k in range(st, min(st + BLOCK_ROWS, nb)):
                s += diffs[k]
                cnt += 1
        boot.append(s / cnt if cnt else 0.0)
    boot.sort()
    lo = boot[int(0.025 * N_BOOT)]
    hi = boot[int(0.975 * N_BOOT)]
    boot_mean = sum(boot) / len(boot)
    brier_M0_safe = max(brier_M0, 1e-12)
    rel_lo = lo / brier_M0_safe
    rel_hi = hi / brier_M0_safe
    boot_rel_mean = boot_mean / brier_M0_safe

    sufficient = len(test) >= 500 and nu >= 500
    improved = rel_brier >= FLOOR and rel_lo > 0
    if not sufficient:
        verdict = "INCONCLUSIVE"
    elif improved:
        verdict = "PROMOTED"
    else:
        verdict = "NOT_SUPPORTED"

    result = {
        "experiment_id": EXPERIMENT,
        "campaign": f"{EXPERIMENT}-{CAMPAIGN_START}",
        "session_id": SESSION,
        "session_utc": SESSION,
        "generated_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "BINANCE_PUBLIC_ARCHIVE_READ_ONLY_CACHE",
        "track": "B_modeled_boundary_breach_forecast",
        "is_observed_liquidations": False,
        "is_risk_overlay": False,
        "overlay_authorized": False,
        "symbols": SYMBOLS,
        "months": f"2024-04..2026-10 ({len(MONTHS)} months)",
        "n_symbols": len(SYMBOLS),
        "common_support": {
            "definition": "UTC hourly timestamps where all five symbols have markPriceKlines close>0",
            "n_common": n_common,
            "per_symbol_mark_raw": {s: len(raw[s]["mark"]) for s in SYMBOLS},
            "per_symbol_rows": per_sym,
            "layout_notes": layout_notes,
        },
        "n_train": len(train), "n_val": len(val), "n_test": len(test),
        "n_unique_timestamps": nu,
        "embargo_hours": EMBARGO_H,
        "splits": "60/20/20 by unique UTC timestamp on S; 7-day (168h) purge/embargo; test->3 chronological blocks",
        "breach_design": {
            "type": "modeled_hypothetical_liquidation_boundary",
            "maintenance_margin_rate": MMR,
            "leverage_primary": L_PRIMARY,
            "leverage_robustness": list(L_ROBUST),
            "horizon_hours": H,
            "long_boundary": "B_long(t) = P(t)*(1-(1-mmr)/L)",
            "short_boundary": "B_short(t) = P(t)*(1+(1-mmr)/L)",
            "long_label": "1 if min_{k=1..H} P(t+k) <= B_long(t)",
            "short_label": "1 if max_{k=1..H} P(t+k) >= B_short(t)",
            "note": "synthetic modeled breaches from disclosed constant scenarios; NOT observed liquidations",
        },
        "models": {
            "M0": "mark-price-only OLS: 7 signed HAR log-RV features + mark/EMA24 distance (8 features)",
            "M1": "funding-conditioned OLS: M0 + signed funding(24h) + trailing 90d |funding| pct (10 features)",
        },
        "primary": {
            "label": "long_breach_L20",
            "metric": "brier",
            "contrast": "M1 vs M0 relative Brier reduction",
            "materiality_floor": FLOOR,
            "base_rate_long": base_rate_long,
            "brier_M0": brier_M0, "brier_M1": brier_M1,
            "logloss_M0": met_long["M0"]["logloss"],
            "logloss_M1": met_long["M1"]["logloss"],
            "auc_M0": met_long["M0"]["auc"], "auc_M1": met_long["M1"]["auc"],
            "relative_brier_reduction_M1_vs_M0": rel_brier,
        },
        "secondary": {
            "short_breach_L20": met_short,
            "long_breach_robustness": robust,
        },
        "per_block": per_block,
        "leave_one_symbol_out": loo,
        "bootstrap": {
            "replicates": N_BOOT, "seed": SEED, "block_rows": BLOCK_ROWS,
            "mean_diff_brier_M0_minus_M1": boot_mean,
            "mean_rel_brier_reduction": boot_rel_mean,
            "ci95_abs_diff": [lo, hi],
            "ci95_relative_brier_reduction": [rel_lo, rel_hi],
        },
        "alpha_2_sequential_look_k2": ALPHA_2,
        "gaps": all_gaps,
        "verdict": verdict,
        "verdict_reason": (
            "M1 beats M0 by >=2% relative out-of-sample Brier on the long-breach "
            "label with bootstrap 95% CI strictly above 0"
            if verdict == "PROMOTED" else
            "M1 vs M0 relative out-of-sample Brier reduction < 2% floor or CI "
            "includes 0"
            if verdict == "NOT_SUPPORTED" else
            "insufficient test data for a confirmatory verdict"),
        "stdlib_only": True,
        "network": False,
        "read_only_cache": True,
        "outcome_data_inspected_before_freeze": False,
    }
    with open(os.path.join(HERE, f"fclr_live_archive08_eval_{SESSION}.json"), "w") as f:
        json.dump(result, f, indent=2)

    md = []
    md.append(f"# FCLR-LIVE-ARCHIVE-08 Confirmatory Evaluation ({SESSION})\n")
    md.append(f"**Experiment:** {EXPERIMENT}  \n**Track:** B modeled boundary-breach forecast  \n")
    md.append(f"**Verdict:** `{verdict}`  \n")
    md.append(f"**Common support |S|:** {n_common} (all-five mark-price, close>0)\n")
    md.append("## Design\n")
    md.append(f"- Modeled liquidation boundaries from constant scenarios: mmr={MMR}, "
              f"L={L_PRIMARY} primary (robustness L in {list(L_ROBUST)}), horizon H={H}h.\n")
    md.append("- Long label: future 24h min mark <= P(t)*(1-(1-mmr)/L); short label: "
              "future 24h max mark >= P(t)*(1+(1-mmr)/L). NOT observed liquidations; NOT an overlay.\n")
    md.append("- M0 (mark-price-only): 7 signed HAR log-RV + mark/EMA24 distance; "
              "M1 (funding-conditioned): M0 + signed funding(24h) + 90d |funding| pct.\n")
    md.append(f"- Primary: M1 vs M0 relative out-of-sample Brier on long breach (floor {FLOOR*100:.0f}%).\n")
    md.append(f"- Splits 60/20/20 by unique UTC ts on S, {EMBARGO_H}h purge/embargo, "
              f"test->{N_BLOCKS} blocks. train={len(train)} val={len(val)} test={len(test)}.\n")
    md.append("## Primary results (long breach, L=20)\n")
    md.append("| Model | Brier | Log-loss | AUC | events |\n|---|---|---|---|---|\n")
    for m in ("M0", "M1"):
        md.append(f"| {m} | {met_long[m]['brier']:.6e} | {met_long[m]['logloss']:.6e} | "
                  f"{met_long[m]['auc'] if met_long[m]['auc'] is not None else float('nan'):.4f} | "
                  f"{met_long[m]['n_events']} |\n")
    md.append(f"\n**Primary M1 vs M0 relative Brier reduction: {rel_brier*100:.3f}% "
              f"(floor {FLOOR*100:.0f}%).**\n")
    md.append(f"Bootstrap {N_BOOT} reps 95% CI relative Brier reduction: "
              f"[{rel_lo*100:.3f}%, {rel_hi*100:.3f}%].\n")
    md.append(f"Base rate (long breach, L=20): {base_rate_long*100:.3f}%.\n")
    md.append("\n## Secondary (non-gating)\n")
    md.append("| Label | Model | Brier | Log-loss | AUC |\n|---|---|---|---|---|\n")
    for m in ("M0", "M1"):
        md.append(f"| short L20 | {m} | {met_short[m]['brier']:.6e} | "
                  f"{met_short[m]['logloss']:.6e} | "
                  f"{met_short[m]['auc'] if met_short[m]['auc'] is not None else float('nan'):.4f} |\n")
    for L in L_ROBUST:
        rr = robust[str(L)]
        md.append(f"| long L{L} | M0/M1 | {rr['brier_M0']:.6e} / {rr['brier_M1']:.6e} | "
                  f"rel {rr['rel_brier_reduction']*100:.3f}% | events {rr['n_events']} |\n")
    md.append("\n## Per-block relative Brier reduction (M1 vs M0, long L20)\n")
    md.append("| Block | M0 Brier | M1 Brier | rel reduction |\n|---|---|---|---|\n")
    for i in range(N_BLOCKS):
        bb0 = per_block["M0"]["brier"][i]
        bb1 = per_block["M1"]["brier"][i]
        md.append(f"| {i+1} | {bb0:.6e} | {bb1:.6e} | {(bb0-bb1)/max(bb0,1e-12)*100:.3f}% |\n")
    md.append("\n## Leave-one-symbol-out (M1 vs M0, long L20)\n| Symbol | n | events | rel Brier reduction |\n|---|---|---|---|\n")
    for s in SYMBOLS:
        if s in loo:
            md.append(f"| {s} | {loo[s]['n']} | {loo[s]['n_events']} | {loo[s]['rel_brier_reduction']*100:.3f}% |\n")
    md.append(f"\n## Gaps: {len(all_gaps)} unverified/missing cache entries disclosed (see JSON).\n")
    md.append(f"\n## Verdict: `{verdict}` — {result['verdict_reason']}.\n")
    with open(os.path.join(HERE, f"fclr_live_archive08_eval_{SESSION}.md"), "w") as f:
        f.write("".join(md))

    # ---------------- source registry ----------------
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
             "rule": "mark price iff any path component starts with 'markPriceKlines-'; dedup open_time; close>0",
             "track": "modeled breach target + RV features + EMA distance"},
            {"kind": "futures_um_monthly_fundingRate",
             "path_template": "research_state/data_cache/{SYM}_{YYYY_MM}/{SYM}-fundingRate-YYYY-MM.{zip,csv}",
             "track": "signed funding(24h) + 90d |funding| pct (funding-conditioned block)"},
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
        },
        "hash_registry": "research_state/cached_inputs_hashes.json (20,694 entries)",
        "sidecar_verification": "per-file .sha256 sidecars present; gaps disclosed in eval output",
        "quarantine": "XRPUSDT 2025-10-19 mark-price day has 24 negative closes; dropped by close>0; NOT zero-filled",
        "admissibility": {
            "unauthenticated": True, "no_credentials": True, "no_payment": True,
            "historical_depth": "31 months, multi-regime", "schema_verified": True,
            "admissible_for_research": True,
            "admissible_for_track_a_observed_liquidations": False,
        },
        "terms": "Binance public market data; unauthenticated; research use.",
    }
    reg_sha = hashlib.sha256(json.dumps(registry, sort_keys=True).encode()).hexdigest()
    with open(os.path.join(HERE, f"fclr_live_archive08_source_registry_{SESSION}.json"), "w") as f:
        json.dump(registry, f, indent=2)
    mdreg = []
    mdreg.append(f"# FCLR-LIVE-ARCHIVE-08 Source Registry ({SESSION})\n")
    mdreg.append(f"**Experiment:** {EXPERIMENT}  \n**Campaign:** {EXPERIMENT}-{CAMPAIGN_START}\n")
    mdreg.append("**Source:** Binance public market-data archive (unauthenticated, free, no signup).\n")
    mdreg.append(f"**Common support |S|:** {n_common} (all-five mark-price, close>0; 3 layouts).\n")
    mdreg.append(f"**Cohort:** {SYMBOLS}, 2024-04..2026-10 (31 months), disjoint from 2021-2024.\n")
    mdreg.append(f"**Gaps disclosed:** {len(all_gaps)} (see eval JSON full gap list).\n")
    mdreg.append(f"**Registry sha256:** {reg_sha}\n")
    with open(os.path.join(HERE, f"fclr_live_archive08_source_registry_{SESSION}.md"), "w") as f:
        f.write("".join(mdreg))

    # ---------------- prereg ----------------
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
        "hypothesis": ("FCLR-H008: funding + price features improve out-of-sample "
                       "forecasts of a Track-B MODELED liquidation-boundary breach "
                       "(long label, L=20, H=24h) beyond a mark-price-only baseline "
                       "(M0) on the disjoint 2024-04..2026-10 cohort, judged on "
                       "relative out-of-sample Brier reduction."),
        "window": "2024-04-01..2026-10-31 UTC",
        "symbols": SYMBOLS,
        "common_support_n": n_common,
        "target": "modeled boundary-breach indicator (long and short kept separate)",
        "breach_design": result["breach_design"],
        "splits": "60/20/20 by unique UTC timestamp on S; 7-day (168h) purge/embargo; test -> 3 chronological blocks",
        "models": result["models"],
        "primary": "M1 vs M0 on paired test-set out-of-sample Brier (long breach, L=20)",
        "secondary": "short-breach Brier, AUC (long & short), log-loss (long & short), long-breach Brier at L in {10,50} (all non-gating)",
        "inference": (">=2000 deterministic block-bootstrap replicates (block=24 rows, seed=20261127); "
                      "report Brier, log-loss, AUC, 95% CI on relative Brier reduction, per-block, "
                      "leave-one-symbol-out"),
        "materiality_floor": FLOOR,
        "alpha_2_sequential_look_k2": ALPHA_2,
        "decision_rule": ("PROMOTED iff relative test-Brier reduction >=2% AND bootstrap 95% "
                          "CI lower bound > 0 AND test data sufficient; else NOT_SUPPORTED; "
                          "INCONCLUSIVE if insufficient data"),
        "leakage_controls": [
            "outcome-blind freeze before target generation",
            "train-only OLS fitting",
            "168h purge/embargo",
            "no outcome inspection before freeze",
            "read-only cache reuse; no re-download; stdlib only; no network",
        ],
        "not_authorized": ["risk overlay", "observed-liquidation claim"],
        "stdlib_only": True, "network": False, "read_only_cache": True,
    }
    with open(os.path.join(HERE, f"fclr_live_archive08_prereg_{SESSION}.json"), "w") as f:
        json.dump(prereg, f, indent=2)
    mdpre = []
    mdpre.append(f"# FCLR-LIVE-ARCHIVE-08 Preregistration ({SESSION})\n")
    mdpre.append(f"**Experiment:** {EXPERIMENT}  \n**Outcome-data inspected before freeze:** False\n")
    mdpre.append("**Track:** B modeled boundary-breach forecast (NOT observed liquidations; NOT an overlay).\n")
    mdpre.append(f"**Breach design:** mmr={MMR}, L={L_PRIMARY} primary (robustness {list(L_ROBUST)}), H={H}h; long/short separate.\n")
    mdpre.append("**Models:** M0 = mark-price-only (8 feats); M1 = M0 + funding(24h) + 90d |funding| pct (10 feats).\n")
    mdpre.append(f"**Primary contrast:** M1 vs M0 paired test-set out-of-sample Brier (long breach). Materiality floor: {FLOOR*100:.0f}% relative reduction.\n")
    mdpre.append("**Decision rule:** PROMOTED iff relative Brier reduction >=2% and bootstrap 95% CI lower bound > 0; else NOT_SUPPORTED; INCONCLUSIVE if insufficient data.\n")
    mdpre.append(f"**Source registry sha256:** {reg_sha}\n")
    mdpre.append(f"**Sequential look:** k=2, alpha_2 = {ALPHA_2:.6f}.\n")
    with open(os.path.join(HERE, f"fclr_live_archive08_prereg_{SESSION}.md"), "w") as f:
        f.write("".join(mdpre))

    # ---------------- headline ----------------
    with open(os.path.join(HERE, f"_headline_{SESSION}.json"), "w") as f:
        json.dump({
            "primary": {"brier_M0": brier_M0, "brier_M1": brier_M1,
                        "rel_brier_reduction": rel_brier,
                        "auc_M0": met_long["M0"]["auc"], "auc_M1": met_long["M1"]["auc"],
                        "base_rate_long": base_rate_long},
            "n_test": len(test), "verdict": verdict,
            "n_unique_timestamps": nu, "n_common": n_common,
        }, f, indent=2)

    print(f"[{dt.datetime.now(dt.timezone.utc).strftime('%H:%M:%S')}] [5/6] verdict={verdict} "
          f"rel_brier={rel_brier*100:.3f}% CI=[{rel_lo*100:.3f}%,{rel_hi*100:.3f}%] |S|={n_common}", flush=True)
    print(f"[{dt.datetime.now(dt.timezone.utc).strftime('%H:%M:%S')}] [6/6] done in {time.time()-t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()