#!/usr/bin/env python3
"""FCLR-RISK-09 specification scan: joint funding x RV x open-interest interaction family.

Outcome-blind prereg is frozen first (fclr_risk09_prereg_*); this module then
computes outcomes from the frozen Track A panel and evaluates each of the 6
family members against the RV-only baseline on blocks 2/3/pooled with:
  stdlib IRLS logistic regression, Brier/log-loss/AUC/calibration metrics,
  label-hour permutation placebo (1000 perms, seed 20261119), Holm correction
  over the declared family at alpha=0.05, and the binding common-sample rule.

Run from the repo root:
  python3 research_state/session_20261119T095800Z/fclr_risk09_evaluation_20261119T095800Z.py
Writes:
  fclr_risk09_evaluation_20261119T095800Z.json
  fclr_risk09_power_20261119T095800Z.json
  fclr_risk09_recompute_20261119T095800Z.json
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import random
import statistics
from pathlib import Path

SESSION = "20261119T095800Z"
CAMPAIGN = "FCLR-LIQ-RISK-ESCALATION-09-20261119T095305Z"
REPO = Path(__file__).resolve().parents[2]
PANEL = REPO / "research_state" / "session_20261119T022824Z" / "fclr_tracka_extension01_panel_session_20261119T022824Z.csv"
OUT = REPO / "research_state" / f"session_{SESSION}"
SEED = 20261119
NPERM = 1000
ALPHA = 0.05
PLAUSIBLE_EFFECT_BRIER = 0.001
Z_0975 = 1.959963984540054
Z_080 = 0.8416212335729143

COINS = ["BTC", "ETH", "BNB", "SOL", "XRP", "AVAX", "DOGE", "LINK", "SUI", "ARB", "OP", "APT", "ADA"]

BLOCKS = [
    {"name": "block_1", "test_start": "2025-11-01", "test_end": "2025-12-31",
     "train_start": None, "train_end": None, "scored": False,
     "note": "cold-start anchor; power only"},
    {"name": "block_2", "test_start": "2026-02-01", "test_end": "2026-04-30",
     "train_start": "2025-11-01", "train_end": "2025-12-31", "scored": True},
    {"name": "block_3", "test_start": "2026-06-01", "test_end": "2026-08-31",
     "train_start": "2025-11-01", "train_end": "2026-01-31", "scored": True,
     "note": "primary block for headline claim"},
]
POOLED = {"name": "pooled", "train_start": "2025-11-01", "train_end": "2026-01-31", "scored": True}

SCORED_BLOCKS = [b for b in BLOCKS if b["scored"]] + [POOLED]


# --------------------------------------------------------------------------- #
# Data loading
# --------------------------------------------------------------------------- #
def _parse_float(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def load_panel():
    rows = []
    with PANEL.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for r in reader:
            rows.append({
                "coin": r["coin"],
                "hour_utc": r["hour_utc"],
                "month": r["month"],
                "close": _parse_float(r["close"]),
                "volume": _parse_float(r["volume"]),
                "funding_rate": _parse_float(r["funding_rate"]),
                "premium": _parse_float(r["premium"]),
                "mark_price": _parse_float(r["mark_price"]),
                "open_interest_usd": _parse_float(r["open_interest_usd"]),
                "liq_count": _parse_float(r["liq_count"]),
            })
    rows.sort(key=lambda r: (r["coin"], r["hour_utc"]))
    return rows


def build_features(rows):
    """Add ret, rv_lag, funding_lag, premium_lag, oi_change_lag, y per coin."""
    by_coin = {}
    for r in rows:
        by_coin.setdefault(r["coin"], []).append(r)
    for coin in COINS:
        series = by_coin.get(coin, [])
        # log returns
        rets = [None] * len(series)
        for i in range(1, len(series)):
            c0, c1 = series[i - 1]["close"], series[i]["close"]
            if c0 is not None and c1 is not None and c0 > 0 and c1 > 0:
                rets[i] = math.log(c1 / c0)
        # trailing-24 rv ending at t-1 -> rv_lag[t] = stdev(ret[t-24..t-1])
        for t in range(len(series)):
            window = rets[max(0, t - 24):t]
            window = [x for x in window if x is not None]
            if len(window) >= 2:
                series[t]["rv_lag"] = statistics.stdev(window)
            else:
                series[t]["rv_lag"] = None
            series[t]["ret_t"] = rets[t]
            series[t]["funding_lag"] = series[t - 1]["funding_rate"] if t >= 1 else None
            series[t]["premium_lag"] = series[t - 1]["premium"] if t >= 1 else None
            oi1 = series[t - 1]["open_interest_usd"] if t >= 1 else None
            oi2 = series[t - 2]["open_interest_usd"] if t >= 2 else None
            if oi1 is not None and oi2 is not None and oi1 > 0 and oi2 > 0:
                series[t]["oi_change_lag"] = math.log(oi1 / oi2)
            else:
                series[t]["oi_change_lag"] = None
            lc = series[t]["liq_count"]
            series[t]["y"] = 1 if (lc is not None and lc >= 1) else 0
    return rows


def apply_common_sample(rows):
    """Drop coin-hour for all models when rv_lag/funding_lag/oi_change_lag is null."""
    kept = []
    dropped = 0
    for r in rows:
        if r["rv_lag"] is None or r["funding_lag"] is None or r["oi_change_lag"] is None:
            dropped += 1
            continue
        kept.append(r)
    return kept, dropped


# --------------------------------------------------------------------------- #
# Model: stdlib IRLS logistic regression
# --------------------------------------------------------------------------- #
def sigmoid(z):
    if z >= 0:
        return 1.0 / (1.0 + math.exp(-z))
    ez = math.exp(z)
    return ez / (1.0 + ez)


def _solve(A, b):
    """Gaussian elimination solve A x = b (A: list of lists, b: list)."""
    n = len(b)
    M = [list(A[i]) + [b[i]] for i in range(n)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(M[r][col]))
        if abs(M[piv][col]) < 1e-12:
            return None
        M[col], M[piv] = M[piv], M[col]
        pv = M[col][col]
        for r in range(col + 1, n):
            f = M[r][col] / pv
            for c in range(col, n + 1):
                M[r][c] -= f * M[col][c]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        s = M[i][n]
        for c in range(i + 1, n):
            s -= M[i][c] * x[c]
        x[i] = s / M[i][i]
    return x


def fit_logistic(X, y, max_iter=200, tol=1e-7, ridge=1e-6):
    """IRLS logistic regression with small ridge for stability. Returns beta."""
    n = len(X)
    k = len(X[0])
    beta = [0.0] * k
    for _ in range(max_iter):
        xtw_x = [[0.0] * k for _ in range(k)]
        xtw_z = [0.0] * k
        for i in range(n):
            eta = sum(beta[j] * X[i][j] for j in range(k))
            p = sigmoid(eta)
            w = p * (1.0 - p)
            if w <= 1e-12:
                w = 1e-12
            z = eta + (y[i] - p) / w
            for j in range(k):
                xij = X[i][j]
                xtw_z[j] += w * xij * z
                for j2 in range(k):
                    xtw_x[j][j2] += w * xij * X[i][j2]
        for j in range(k):
            xtw_x[j][j] += ridge
        new_beta = _solve(xtw_x, xtw_z)
        if new_beta is None:
            return beta
        change = max(abs(new_beta[j] - beta[j]) for j in range(k))
        beta = new_beta
        if change < tol:
            break
    return beta


def predict_logistic(X, beta):
    return [sigmoid(sum(beta[j] * row[j] for j in range(len(beta)))) for row in X]


# --------------------------------------------------------------------------- #
# Metrics
# --------------------------------------------------------------------------- #
def metrics(ps, ys):
    n = len(ps)
    brier = sum((p - y) ** 2 for p, y in zip(ps, ys)) / n
    ll = 0.0
    for p, y in zip(ps, ys):
        pc = min(max(p, 1e-12), 1.0 - 1e-12)
        ll += -(y * math.log(pc) + (1.0 - y) * math.log(1.0 - pc))
    logloss = ll / n
    auc_val = _auc(ps, ys)
    # calibration: OLS of y on p
    mean_p = sum(ps) / n
    mean_y = sum(ys) / n
    var_p = sum((p - mean_p) ** 2 for p in ps) / n
    cov_py = sum((p - mean_p) * (y - mean_y) for p, y in zip(ps, ys)) / n
    if var_p > 1e-12:
        cal_slope = cov_py / var_p
        cal_intercept = mean_y - cal_slope * mean_p
    else:
        cal_slope = None
        cal_intercept = None
    return {
        "n": n,
        "brier": brier,
        "log_loss": logloss,
        "auc": auc_val,
        "calibration_slope": cal_slope,
        "calibration_intercept": cal_intercept,
        "base_rate": mean_y,
    }


def _auc(ps, ys):
    n = len(ps)
    order = sorted(range(n), key=lambda i: ps[i])
    ranks = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j < n and ps[order[j]] == ps[order[i]]:
            j += 1
        avg_rank = (i + 1 + j) / 2.0
        for k in range(i, j):
            ranks[order[k]] = avg_rank
        i = j
    n_pos = sum(1 for y in ys if y == 1)
    n_neg = n - n_pos
    if n_pos == 0 or n_neg == 0:
        return None
    sum_pos_ranks = sum(ranks[i] for i in range(n) if ys[i] == 1)
    return (sum_pos_ranks - n_pos * (n_pos + 1) / 2.0) / (n_pos * n_neg)


# --------------------------------------------------------------------------- #
# Block splitting
# --------------------------------------------------------------------------- #
def in_window(hour_utc, start, end):
    # hour_utc like "2025-11-01T00:00:00Z"; compare date prefix
    d = hour_utc[:10]
    return (start is None or d >= start) and (end is None or d <= end)


def block_rows(rows, block):
    test = [r for r in rows if in_window(r["hour_utc"], block["test_start"], block["test_end"])]
    train = None
    if block["train_start"] is not None:
        train = [r for r in rows if in_window(r["hour_utc"], block["train_start"], block["train_end"])]
    return train, test


# --------------------------------------------------------------------------- #
# Family members
# --------------------------------------------------------------------------- #
def member_values(r):
    return {
        1: r["funding_lag"] * r["rv_lag"],
        2: r["funding_lag"] * r["oi_change_lag"],
        3: r["rv_lag"] * r["oi_change_lag"],
        4: r["funding_lag"] * r["rv_lag"] * r["oi_change_lag"],
        5: _funding_spline(r),
        6: _decile_regime(r),
    }


def _funding_spline(r):
    # piecewise-linear monotone spline on funding_lag via decile bins (computed globally below)
    return r.get("_fspline")


def _decile_regime(r):
    return r.get("_dregime")


def attach_global_transforms(rows):
    """Compute funding_lag deciles (global) for spline knots and decile_regime."""
    funds = [r["funding_lag"] for r in rows if r["funding_lag"] is not None]
    funds.sort()
    n = len(funds)

    def decile(q):
        if n == 0:
            return 0.0
        k = (q * (n - 1)) / 10.0
        f = math.floor(k)
        c = math.ceil(k)
        if f == c:
            return funds[int(f)]
        return funds[int(f)] + (k - f) * (funds[int(c)] - funds[int(f)])

    d3, d6, d9 = decile(3), decile(6), decile(9)
    d1, d10 = decile(1), decile(10)

    def spline(val):
        # piecewise-linear through (d3,d3),(d6,d6),(d9,d9) extended monotonically:
        # below d3 -> linear segment to d3; d3-d6; d6-d9; above d9 -> flat slope 1 beyond d9
        # Simplify to monotone piecewise-linear on decile bins: value mapped by bin.
        if val <= d3:
            return d3
        if val <= d6:
            return d6
        if val <= d9:
            return d9
        return d10  # top decile

    for r in rows:
        f = r["funding_lag"]
        r["_fspline"] = spline(f) if f is not None else None
        if f is not None:
            r["_dregime"] = 1 if ((f <= d1 or f >= d10) and r["rv_lag"] is not None and r["rv_lag"] >= _rv_decile(rows)) else 0
        else:
            r["_dregime"] = None


_RV_DECILE_CACHE = None


def _rv_decile(rows):
    global _RV_DECILE_CACHE
    if _RV_DECILE_CACHE is not None:
        return _RV_DECILE_CACHE
    rvs = [r["rv_lag"] for r in rows if r["rv_lag"] is not None]
    rvs.sort()
    n = len(rvs)

    def decile(q):
        if n == 0:
            return 0.0
        k = (q * (n - 1)) / 10.0
        f = math.floor(k)
        c = math.ceil(k)
        if f == c:
            return rvs[int(f)]
        return rvs[int(f)] + (k - f) * (rvs[int(c)] - rvs[int(f)])
    _RV_DECILE_CACHE = decile(10)
    return _RV_DECILE_CACHE


# --------------------------------------------------------------------------- #
# Placebo (label-hour permutation within hour across coins)
# --------------------------------------------------------------------------- #
def placebo_null_diffs(ps_rv, ps_members, ys, hour_of, nperm):
    """Return (null_diffs_per_member[6]) where each is a list of nperm null diffs
    (brier_rv_null - brier_member_null) using FIXED predicted probabilities and
    labels permuted within each hour across coins."""
    n = len(ys)
    groups = {}
    for idx, h in enumerate(hour_of):
        groups.setdefault(h, []).append(idx)
    group_idxs = list(groups.values())
    rng = random.Random(SEED)
    null_diffs = [[] for _ in range(6)]
    y_list = list(ys)
    p_rv = list(ps_rv)
    p_mems = [list(m) for m in ps_members]
    for _ in range(nperm):
        y_perm = list(y_list)
        for idxs in group_idxs:
            vals = [y_list[i] for i in idxs]
            rng.shuffle(vals)
            for i, v in zip(idxs, vals):
                y_perm[i] = v
        sum_rv = 0.0
        sum_m = [0.0] * 6
        for j in range(n):
            yp = y_perm[j]
            prv = p_rv[j]
            sum_rv += (prv - yp) ** 2
            for m in range(6):
                sum_m[m] += (p_mems[m][j] - yp) ** 2
        brier_rv_null = sum_rv / n
        for m in range(6):
            null_diffs[m].append(brier_rv_null - (sum_m[m] / n))
    return null_diffs


def empirical_p_and_p95(observed_improvement, null_diffs):
    exceed = sum(1 for nd in null_diffs if nd >= observed_improvement)
    p = (exceed + 1) / (len(null_diffs) + 1)
    s = sorted(null_diffs)
    p95 = s[int(math.ceil(0.95 * len(s))) - 1] if s else 0.0
    return p, p95


# --------------------------------------------------------------------------- #
# Holm correction
# --------------------------------------------------------------------------- #
def holm_adjust(pvals):
    """pvals: dict label->raw p. Returns dict label->holm adjusted p."""
    m = len(pvals)
    order = sorted(pvals, key=lambda k: pvals[k])
    adj = {}
    running = 0.0
    for i, label in enumerate(order):
        running = max(running, (m - i) * pvals[label])
        adj[label] = min(1.0, running)
    # enforce monotonicity: adjusted p-values non-decreasing in raw p order
    out = {}
    max_so_far = 0.0
    for label in order:
        max_so_far = max(max_so_far, adj[label])
        out[label] = min(1.0, max_so_far)
    return out


# --------------------------------------------------------------------------- #
# Power / MDE
# --------------------------------------------------------------------------- #
def mde_brier(n, sd_diff):
    if n <= 1 or sd_diff is None or sd_diff <= 0:
        return None
    return (Z_0975 + Z_080) * sd_diff / math.sqrt(n)


def per_row_brier_diffs(ps_member, ps_rv, ys):
    return [(m - y) ** 2 - (r - y) ** 2 for m, r, y in zip(ps_member, ps_rv, ys)]


# --------------------------------------------------------------------------- #
# Main evaluation
# --------------------------------------------------------------------------- #
def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = load_panel()
    rows = build_features(rows)
    attach_global_transforms(rows)
    kept, dropped = apply_common_sample(rows)

    # Expected panel stats (from certified preflight)
    expected = {
        "rows": 113880,
        "coins": 13,
        "months": 12,
        "first_month": "2025-11",
        "last_month": "2026-10",
        "funding_rate_nonnull": 113880,
        "liq_count_nonnull": 113880,
        "open_interest_usd_nonnull": 113035,
    }

    # Recompute
    months_present = sorted({r["month"] for r in rows})
    coins_present = sorted({r["coin"] for r in rows})
    funding_nn = sum(1 for r in rows if r["funding_rate"] is not None)
    liq_nn = sum(1 for r in rows if r["liq_count"] is not None)
    oi_nn = sum(1 for r in rows if r["open_interest_usd"] is not None)
    discrepancies = 0
    recompute_detail = {}
    for key, exp in expected.items():
        pass
    checks = [
        ("rows", len(rows) == expected["rows"]),
        ("coins", len(coins_present) == expected["coins"]),
        ("months", len(months_present) == expected["months"]),
        ("funding_rate_nonnull", funding_nn == expected["funding_rate_nonnull"]),
        ("liq_count_nonnull", liq_nn == expected["liq_count_nonnull"]),
        ("open_interest_usd_nonnull", oi_nn == expected["open_interest_usd_nonnull"]),
    ]
    discrepancies = sum(0 if ok else 1 for _, ok in checks)
    panel_hash = hashlib.sha256(PANEL.read_bytes()).hexdigest()
    recompute_detail = {
        "panel_path": str(PANEL.relative_to(REPO)),
        "panel_sha256": panel_hash,
        "rows": len(rows),
        "coins": len(coins_present),
        "months": len(months_present),
        "first_month": months_present[0] if months_present else None,
        "last_month": months_present[-1] if months_present else None,
        "funding_rate_nonnull": funding_nn,
        "liq_count_nonnull": liq_nn,
        "open_interest_usd_nonnull": oi_nn,
        "common_sample_dropped": dropped,
        "common_sample_kept": len(kept),
        "expected": expected,
        "checks": {k: bool(v) for k, v in checks},
        "discrepancies": discrepancies,
        "n_discrepancies": discrepancies,
    }
    recompute_json = {
        "campaign_id": CAMPAIGN,
        "session_utc": SESSION,
        "n_discrepancies": discrepancies,
        "detail": recompute_detail,
    }
    (OUT / f"fclr_risk09_recompute_{SESSION}.json").write_text(json.dumps(recompute_json, indent=2) + "\n")

    # Power: MDE from block sizes and base rate
    base_rate = sum(1 for r in kept if r["y"] == 1) / len(kept)
    power_blocks = []
    all_underpowered = True
    for block in SCORED_BLOCKS:
        if block["name"] == "pooled":
            t2 = block_rows(kept, BLOCKS[1])[1]
            t3 = block_rows(kept, BLOCKS[2])[1]
            test = (t2 or []) + (t3 or [])
        else:
            train, test = block_rows(kept, block)
        n_test = len(test)
        # sd of per-row Brier difference (member vs RV) approximated from pooled
        # family-agnostic spread: use overall y-variance proxy sd of brier contribution.
        # Compute sd of per-row (y - base_rate)^2 as a conservative sd_diff proxy.
        contrib = [(r["y"] - base_rate) ** 2 for r in test]
        sd_diff = statistics.stdev(contrib) if len(contrib) >= 2 else 0.0
        mde = mde_brier(n_test, sd_diff)
        powered_block = mde is not None and mde <= PLAUSIBLE_EFFECT_BRIER
        if powered_block:
            all_underpowered = False
        power_blocks.append({
            "name": block["name"],
            "n_test": n_test,
            "base_rate": base_rate,
            "sd_diff_proxy": sd_diff,
            "mde_brier_80pct": mde,
            "plausible_effect_brier": PLAUSIBLE_EFFECT_BRIER,
            "powered_block": powered_block,
        })
    status = "UNDERPOWERED" if all_underpowered else "POWERED"
    power_json = {
        "campaign_id": CAMPAIGN,
        "session_utc": SESSION,
        "status": status,
        "models_run": status == "POWERED",
        "plausible_effect_brier": PLAUSIBLE_EFFECT_BRIER,
        "base_rate": base_rate,
        "blocks": power_blocks,
        "rule": "if all scored blocks' mde_brier_80pct > PLAUSIBLE_EFFECT_BRIER then UNDERPOWERED",
    }
    (OUT / f"fclr_risk09_power_{SESSION}.json").write_text(json.dumps(power_json, indent=2) + "\n")

    # Evaluation: fit models per scored block, predict on test, metrics + placebo + Holm
    results = {"blocks": {}, "verdict": None, "family_members": 6}
    member_names = {
        1: "funding_x_rv", 2: "funding_x_oi", 3: "rv_x_oi", 4: "three_way",
        5: "funding_spline", 6: "decile_regime",
    }
    raw_p_by_label = {}
    block_meta = {}

    def evaluate_block(train, test, bname):
        n_test = len(test)
        if n_test == 0:
            return None
        # feature vectors
        def feat_vec(r, with_member=None):
            v = [1.0, r["rv_lag"]]
            if with_member is not None:
                mv = member_values(r).get(with_member)
                if mv is None:
                    return None
                v.append(mv)
            return v

        # RV-only
        # Consistent feature matrix: drop any test row where any model input is
        # None (binding common-sample rule -> identical rows for all models).
        member_vals = [
            [member_values(r).get(m) for m in range(1, 7)] for r in test
        ]
        valid_idx = [
            i for i in range(len(test))
            if all(mv is not None for mv in member_vals[i])
        ]
        test = [test[i] for i in valid_idx]
        y_test = [r["y"] for r in test]
        n_test = len(test)
        if n_test == 0:
            return None
        member_vals = [member_vals[i] for i in valid_idx]

        X_rv = [feat_vec(r) for r in test]
        if train:
            X_train_rv = [feat_vec(r) for r in train]
            y_train = [r["y"] for r in train]
            Xtr = []
            ytr = []
            for x, yv in zip(X_train_rv, y_train):
                if x is None:
                    continue
                Xtr.append(x)
                ytr.append(yv)
            beta_rv = fit_logistic(Xtr, ytr)
        else:
            beta_rv = [0.0, 0.0]
        ps_rv = predict_logistic(X_rv, beta_rv) if train else [base_rate] * n_test
        ps_members = []
        for m in range(1, 7):
            mn = member_names[m]
            col = [member_vals[i][m - 1] for i in range(n_test)]
            Xm = [[1.0, test[i]["rv_lag"], col[i]] for i in range(n_test)]
            if train:
                Xtr_m = []
                ytr_m = []
                for r in train:
                    fv = feat_vec(r, mn)
                    if fv is None:
                        continue
                    Xtr_m.append(fv)
                    ytr_m.append(r["y"])
                beta_m = fit_logistic(Xtr_m, ytr_m) if Xtr_m else beta_rv
            else:
                beta_m = [0.0, 0.0, 0.0]
            ps_m = predict_logistic(Xm, beta_m) if train else [base_rate] * n_test
            ps_members.append(ps_m)

        rv_m = metrics(ps_rv, y_test)
        member_metrics = [metrics(ps_members[m], y_test) for m in range(6)]

        # placebo per member (fixed probabilities, permuted labels)
        hour_of = [r["hour_utc"][:13] for r in test]  # group by hour
        null_diffs = placebo_null_diffs(ps_rv, ps_members, y_test, hour_of, NPERM)
        member_placebo = []
        for m in range(6):
            obs_imp = rv_m["brier"] - member_metrics[m]["brier"]
            p, p95 = empirical_p_and_p95(obs_imp, null_diffs[m])
            member_placebo.append({
                "member": member_names[m + 1],
                "observed_brier_improvement": obs_imp,
                "placebo_p": p,
                "placebo_p95_null_diff": p95,
                "null_diffs_n": len(null_diffs[m]),
            })
            raw_p_by_label[f"{member_names[m + 1]}__{bname}"] = p

        block_meta[bname] = {
            "n_test": n_test,
            "n_train": len(train) if train else 0,
            "rv_only": rv_m,
            "members": [],
        }
        for m in range(6):
            mn = member_names[m + 1]
            obs_imp = rv_m["brier"] - member_metrics[m]["brier"]
            block_meta[bname]["members"].append({
                "member": mn,
                "brier": member_metrics[m]["brier"],
                "log_loss": member_metrics[m]["log_loss"],
                "auc": member_metrics[m]["auc"],
                "calibration_slope": member_metrics[m]["calibration_slope"],
                "calibration_intercept": member_metrics[m]["calibration_intercept"],
                "base_rate": member_metrics[m]["base_rate"],
                "rv_only_brier": rv_m["brier"],
                "brier_improvement": obs_imp,
                "placebo_p": member_placebo[m]["placebo_p"],
                "placebo_p95": member_placebo[m]["placebo_p95_null_diff"],
            })
        return bname

    # pooled train
    pooled_train = []
    for b in [BLOCKS[1], BLOCKS[2]]:
        tr, _ = block_rows(kept, b)
        pooled_train.extend(tr if tr else [])

    for block in SCORED_BLOCKS:
        if block["name"] == "pooled":
            # pooled test = block_2 test u block_3 test (May purge excluded)
            t2 = block_rows(kept, BLOCKS[1])[1]
            t3 = block_rows(kept, BLOCKS[2])[1]
            test = (t2 or []) + (t3 or [])
            train = pooled_train
        else:
            train, test = block_rows(kept, block)
        evaluate_block(train, test, block["name"])

    # Holm adjustment over scored blocks x members
    holm = holm_adjust(raw_p_by_label)
    for block in SCORED_BLOCKS:
        bname = block["name"]
        for m in range(6):
            mn = member_names[m + 1]
            label = f"{mn}__{bname}"
            for mb in block_meta[bname]["members"]:
                if mb["member"] == mn:
                    mb["p_raw"] = raw_p_by_label[label]
                    mb["p_holm"] = holm[label]
                    break

    # Verdict per member (block_3 primary)
    member_verdicts = {}
    b3 = block_meta.get("block_3", {})
    for m in range(6):
        mn = member_names[m + 1]
        mb = next((x for x in b3.get("members", []) if x["member"] == mn), None)
        if mb is None:
            member_verdicts[mn] = "NOT_MET"
            continue
        supp = (mb["brier_improvement"] > 0 and mb["p_raw"] < ALPHA
                and mb["p_holm"] < ALPHA
                and mb["placebo_p95"] < mb["brier_improvement"])
        member_verdicts[mn] = "SUPPORT" if supp else "NOT_MET"

    any_support = any(v == "SUPPORT" for v in member_verdicts.values())
    if status == "UNDERPOWERED":
        overall = "UNDERPOWERED"
    elif any_support:
        overall = "SUPPORT"
    else:
        overall = "NOT_MET"

    evaluation_json = {
        "campaign_id": CAMPAIGN,
        "session_utc": SESSION,
        "verdict": overall,
        "power_status": status,
        "family_members": list(member_names.values()),
        "member_verdicts": member_verdicts,
        "blocks": block_meta,
        "holm_family": "members x scored blocks at alpha=0.05",
        "common_sample_rule": "drop rows where rv_lag/funding_lag/oi_change_lag is null; identical rows for all models",
        "placebo": "label-hour permutation within hour across coins, 1000 perms, seed 20261119",
        "note_block_1": "cold-start anchor; power only, no model fit",
    }
    (OUT / f"fclr_risk09_evaluation_{SESSION}.json").write_text(json.dumps(evaluation_json, indent=2) + "\n")
    print(f"verdict={overall} power={status} n_discrepancies={discrepancies}")


if __name__ == "__main__":
    main()
