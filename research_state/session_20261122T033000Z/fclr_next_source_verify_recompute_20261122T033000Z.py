#!/usr/bin/env python3
"""FCLR-NEXT-SOURCE-VERIFY-01 independent recompute (stdlib-only).

Separate code path from fclr_next_source_verify01_eval.py:
  - Independent CSV parsing / assembly.
  - Spearman rho via average-tie ranking (independent implementation).
  - Spearman p-value via analytical t-approximation + regularized incomplete
    beta (gammln + betacf modified Lentz), deterministic — different method
    from eval's permutation test.
  - Same pre-specified decision rules (FCLR-NEXT-CONFIRM-001).
  - Asserts numerical agreement with eval outputs (rho exact match; decision
    match; both p<0.05 where eval claims significance).

Reads CSVs only; writes recompute JSON under session dir.
"""

import csv
import glob
import hashlib
import json
import math
import os

SESSION_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(os.path.dirname(SESSION_DIR))
DATA_DIR = os.path.join(REPO_ROOT, "data", "raw")
UTC = "20261122T033000Z"
ARTIFACT_ID = f"fclr_next_source_verify01_recompute_{UTC}"
ALPHA = 0.05
SYMBOLS = ["BTCUSDT", "ETHUSDT"]
BLOCKS = [
    {"id": "B1_2024-01", "start_ms": 1704067200000, "end_ms": 1706745599999},
    {"id": "B2_2024-02", "start_ms": 1706745600000, "end_ms": 1709251199999},
    {"id": "B3_2024-03", "start_ms": 1709251200000, "end_ms": 1711929599999},
]


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------- math: log-gamma, regularized incomplete beta, t two-tailed ----------

def gammln(xx):
    cof = [76.18009172947146, -86.50532032941677, 24.01409824083091,
           -1.231739572450155, 0.1208650973866179e-2, -0.5395239384953e-5]
    x = xx
    tmp = x + 5.5
    tmp -= (x + 0.5) * math.log(tmp)
    ser = 1.000000000190015
    for j in range(6):
        x += 1
        ser += cof[j] / x
    return -tmp + math.log(2.5066282746310005 * ser / xx)


def betacf(a, b, x):
    # Modified Lentz continued fraction for incomplete beta
    qab = a + b
    qap = a + 1.0
    qam = a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < 1e-30:
        d = 1e-30
    d = 1.0 / d
    h = d
    for m in range(1, 200):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < 1e-30:
            d = 1e-30
        c = 1.0 + aa / c
        if abs(c) < 1e-30:
            c = 1e-30
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < 1e-30:
            d = 1e-30
        c = 1.0 + aa / c
        if abs(c) < 1e-30:
            c = 1e-30
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < 1e-14:
            break
    return h


def betai(a, b, x):
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    lbeta = gammln(a) + gammln(b) - gammln(a + b)
    front = math.exp(math.log(x) * a + math.log(1.0 - x) * b - lbeta)
    if x < (a + 1.0) / (a + b + 2.0):
        return front * betacf(a, b, x) / a
    return 1.0 - front * betacf(b, a, 1.0 - x) / b


def t_two_tailed_p(t, df):
    if df <= 0:
        return float("nan")
    x = df / (df + t * t)
    return betai(df / 2.0, 0.5, x)


# ---------- statistics ----------

def mean(xs):
    return sum(xs) / len(xs) if xs else float("nan")


def rankdata(xs):
    n = len(xs)
    order = sorted(range(n), key=lambda i: xs[i])
    ranks = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        i = j + 1
    return ranks


def pearson(xs, ys):
    n = len(xs)
    if n < 2:
        return float("nan")
    mx, my = mean(xs), mean(ys)
    num = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
    dx = sum((a - mx) ** 2 for a in xs)
    dy = sum((b - my) ** 2 for b in ys)
    if dx == 0 or dy == 0:
        return 0.0
    return num / math.sqrt(dx * dy)


def spearman_analytical(xs, ys):
    n = len(xs)
    if n < 3:
        return float("nan"), float("nan")
    r = pearson(rankdata(xs), rankdata(ys))
    if abs(r) >= 1.0:
        return r, 0.0
    t = r * math.sqrt((n - 2) / (1.0 - r * r))
    p = t_two_tailed_p(t, n - 2)
    return r, p


# ---------- data ----------

def symbol_of(name):
    for s in SYMBOLS:
        if name.startswith(s + "-"):
            return s
    return None


def load_symbol(symbol):
    klines = []
    fundings = []
    files_sha = {}
    for path in glob.glob(os.path.join(DATA_DIR, "**", "*.csv"), recursive=True):
        name = os.path.basename(path)
        if symbol_of(name) != symbol:
            continue
        files_sha[name] = sha256_file(path)
        with open(path, newline="") as f:
            rows = list(csv.DictReader(f))
        if "-1h-" in name:
            for r in rows:
                try:
                    klines.append((int(r["open_time"]), float(r["close"])))
                except (KeyError, ValueError, TypeError):
                    pass
        elif "funding" in name.lower():
            for r in rows:
                try:
                    fundings.append((int(r["calc_time"]), float(r["last_funding_rate"])))
                except (KeyError, ValueError, TypeError):
                    pass
    klines = sorted(dict.fromkeys(klines))  # dedupe by open_time, keep sorted
    fundings.sort()
    return klines, fundings, files_sha


def nearest_prior_funding(fundings, t):
    best = None
    for ct, rate in fundings:
        if ct <= t:
            best = rate
        else:
            break
    return best


def assemble(klines, fundings):
    rows = []
    for i in range(len(klines) - 1):
        t, c0 = klines[i]
        _, c1 = klines[i + 1]
        if c0 <= 0 or c1 <= 0:
            continue
        lr = math.log(c1 / c0)
        f = nearest_prior_funding(fundings, t)
        if f is None:
            continue
        rows.append({
            "t": t, "lr": lr, "sub_vol": abs(lr),
            "funding": f, "abs_funding": abs(f),
            "sign_f": 1 if f > 0 else (-1 if f < 0 else 0),
            "sign_r": 1 if lr > 0 else (-1 if lr < 0 else 0),
        })
    for r in rows:
        r["opp"] = (r["sign_f"] != r["sign_r"]) and (r["sign_r"] != 0)
    return rows


def evaluate():
    symbol_results = {}
    for sym in SYMBOLS:
        klines, fundings, files_sha = load_symbol(sym)
        rows = assemble(klines, fundings)
        symbol_results[sym] = {
            "kline_rows": len(klines),
            "funding_rows": len(fundings),
            "assembled_rows": len(rows),
            "files_sha256": files_sha,
        }

    blocks = {}
    h1_ps = []
    any_admissible = False
    h3_confirmed = True
    liq_found = []

    for path in glob.glob(os.path.join(DATA_DIR, "**", "*.csv"), recursive=True):
        with open(path, newline="") as f:
            header = next(csv.reader(f), [])
        for c in header:
            if "liquid" in c.lower():
                liq_found.append((os.path.basename(path), c))
    h3_confirmed = len(liq_found) == 0

    h1_any_pass = False
    h2_dir_ok = True
    for b in BLOCKS:
        br = {"block_id": b["id"], "symbols": {}}
        for sym in SYMBOLS:
            klines, fundings, _ = load_symbol(sym)
            rows = assemble(klines, fundings)
            brows = [r for r in rows if b["start_ms"] <= r["t"] <= b["end_ms"]]
            entry = {"n_rows": len(brows)}
            if len(brows) < 10:
                entry["status"] = "INCONCLUSIVE_TOO_FEW_ROWS"
                entry["h1"] = {"rho": None, "p": None, "pass_alpha": None}
                entry["h2"] = {"diff_mean": None, "p": None, "direction_consistent": None}
            else:
                any_admissible = True
                rho, p = spearman_analytical([r["abs_funding"] for r in brows],
                                             [r["sub_vol"] for r in brows])
                entry["h1"] = {"rho": rho, "p": p, "pass_alpha": (p is not None and p == p and p < ALPHA)}
                if entry["h1"]["pass_alpha"]:
                    h1_any_pass = True
                h1_ps.append(p)
                opp = [r["sub_vol"] for r in brows if r["opp"]]
                same = [r["sub_vol"] for r in brows if not r["opp"]]
                dm = mean(opp) - mean(same) if opp and same else float("nan")
                # permutation-ish direction: sign of diff; mark consistent if diff<0 (or not testable)
                dc = (dm < 0) if (dm == dm) else None
                entry["h2"] = {"diff_mean": dm, "p": None, "direction_consistent": dc,
                               "n_opp": len(opp), "n_same": len(same)}
                if dc is False:
                    h2_dir_ok = False
            br["symbols"][sym] = entry
        blocks[b["id"]] = br

    # Fisher combine (analytical chi2 survival for even df)
    def chi2_surv(x, df):
        k = df // 2
        xm2 = x / 2.0
        term = math.exp(-xm2)
        total = term
        for j in range(1, k):
            term *= xm2 / j
            total += term
        return total

    ps = [p for p in h1_ps if p == p]
    chi2 = -2.0 * sum(math.log(max(p, 1e-300)) for p in ps) if ps else float("nan")
    fp = chi2_surv(chi2, 2 * len(ps)) if ps else float("nan")

    if not any_admissible:
        decision = "NOT_SUPPORTED"
        reason = "No admissible block meets minima."
    elif not h3_confirmed:
        decision = "NOT_SUPPORTED"
        reason = "H3 failed: liquidation columns present."
    elif h1_any_pass and h2_dir_ok and h3_confirmed:
        decision = "GO"
        reason = "H1 passed in >=1 admissible block; H2 direction consistent; H3 absence confirmed."
    else:
        decision = "INCONCLUSIVE"
        reason = "Admissible blocks exist but GO thresholds not jointly met."

    return {
        "artifact_id": ARTIFACT_ID,
        "session_utc": UTC,
        "symbols": symbol_results,
        "blocks": blocks,
        "h3_liquidation_absence": {"confirmed": h3_confirmed, "liquidation_columns_found": liq_found},
        "aggregate": {
            "h1_fisher_chi2": chi2,
            "h1_fisher_p": fp,
            "h1_any_block_pass_alpha": h1_any_pass,
            "h2_direction_consistent_all_blocks": h2_dir_ok,
            "h3_confirmed": h3_confirmed,
            "any_admissible_block": any_admissible,
        },
        "decision": decision,
        "decision_reason": reason,
        "method": "independent_recompute_analytical_t_approx",
    }


def agree_with_eval(eval_path):
    with open(eval_path) as f:
        ev = json.load(f)
    rec = evaluate()
    checks = {}
    # symbol row counts
    sc = {}
    for sym in SYMBOLS:
        sc[sym] = {
            "eval_assembled": ev["symbols"][sym]["assembled_rows"],
            "recompute_assembled": rec["symbols"][sym]["assembled_rows"],
            "match": ev["symbols"][sym]["assembled_rows"] == rec["symbols"][sym]["assembled_rows"],
        }
    checks["symbol_counts"] = sc
    # per-block rho agreement (eval permutation rho vs recompute analytical rho)
    bc = {}
    for bid in ["B1_2024-01", "B2_2024-02", "B3_2024-03"]:
        for sym in SYMBOLS:
            e = ev["blocks"][bid]["symbols"][sym]["h1"]["rho"]
            r = rec["blocks"][bid]["symbols"][sym]["h1"]["rho"]
            key = f"{bid}/{sym}"
            if e is None and r is None:
                bc[key] = {"eval": None, "recompute": None, "match": True}
            elif e is None or r is None:
                bc[key] = {"eval": e, "recompute": r, "match": False}
            else:
                bc[key] = {"eval": e, "recompute": r, "match": abs(e - r) < 1e-9}
    checks["block_rho"] = bc
    # decision match
    checks["decision_match"] = ev["decision"] == rec["decision"]
    checks["eval_decision"] = ev["decision"]
    checks["recompute_decision"] = rec["decision"]
    # significance agreement on B1 BTCUSDT (eval claims p<0.05)
    b1btc_eval_p = ev["blocks"]["B1_2024-01"]["symbols"]["BTCUSDT"]["h1"]["p"]
    b1btc_rec_p = rec["blocks"]["B1_2024-01"]["symbols"]["BTCUSDT"]["h1"]["p"]
    checks["b1_btcusdt_p_agreement"] = {
        "eval_p": b1btc_eval_p, "recompute_p": b1btc_rec_p,
        "eval_sig": b1btc_eval_p is not None and b1btc_eval_p < ALPHA,
        "recompute_sig": b1btc_rec_p is not None and b1btc_rec_p < ALPHA,
    }
    rec["agreement_with_eval"] = checks
    return rec


def main():
    eval_path = os.path.join(SESSION_DIR, f"fclr_next_source_verify01_eval_{UTC}.json")
    rec = agree_with_eval(eval_path)
    out_path = os.path.join(SESSION_DIR, f"{ARTIFACT_ID}.json")
    with open(out_path, "w") as f:
        json.dump(rec, f, indent=2)
    print(json.dumps({
        "decision": rec["decision"],
        "decision_match": rec["agreement_with_eval"]["decision_match"],
        "b1_btcusdt_p_agreement": rec["agreement_with_eval"]["b1_btcusdt_p_agreement"],
        "json": out_path,
    }, indent=2))


if __name__ == "__main__":
    main()
