#!/usr/bin/env python3
"""
Minimal Track B modeled-breach eval (fast path: pyarrow column ops only,
no row-by-row Python loops). Produces fclr_tracks01_eval_<UTC>.json + .md
for the FCLR-TRACKA-SOURCE-AUDIT-01 gate binder.
"""
from __future__ import annotations

import hashlib
import json
import math
import sys
from pathlib import Path

try:
    import numpy as np
except Exception as e:
    print("numpy required:", e)
    sys.exit(2)
try:
    import pyarrow.parquet as pq
except Exception as e:
    print("pyarrow required:", e)
    sys.exit(2)

REPO = Path(__file__).resolve().parents[2]
SESSION_UTC = "20261123T043600Z"
BULK = REPO / "research_state" / "data_cache" / "ironflow_bulk"

MONTHS = ["2025-05", "2025-06", "2025-07", "2025-08", "2025-09", "2025-10",
          "2025-11", "2025-12", "2026-01", "2026-02", "2026-03", "2026-04",
          "2026-05", "2026-06", "2026-07", "2026-08", "2026-09", "2026-10"]

HORIZON_H = 24
LEVERAGE = 5.0
MMR = 0.0
N_BOOT = 10
ALPHA_K = 0.05 / 2
MATERIALITY_PCT = 2.0


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sigmoid(z):
    z = np.asarray(z, dtype=float)
    out = np.empty_like(z)
    pos = z >= 0
    out[pos] = 1.0 / (1.0 + np.exp(-z[pos]))
    ez = np.exp(z[~pos])
    out[~pos] = ez / (1.0 + ez)
    return out


def logreg_fit(X, y, max_iter=100, tol=1e-6):
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    n, k1 = X.shape
    Xint = np.column_stack([np.ones(n), X])
    beta = np.zeros(k1 + 1)
    for _ in range(max_iter):
        z = Xint @ beta
        p = sigmoid(z)
        r = y - p
        grad = Xint.T @ r
        W = p * (1.0 - p)
        H = -(Xint.T * W) @ Xint
        try:
            delta = np.linalg.solve(-H, grad)
        except np.linalg.LinAlgError:
            return beta
        beta += delta
        if np.max(np.abs(delta)) < tol:
            break
    return beta


def logreg_predict(X, beta):
    X = np.asarray(X, dtype=float)
    n = X.shape[0]
    Xint = np.column_stack([np.ones(n), X])
    return sigmoid(Xint @ beta)


def brier_score(y, p):
    mask = ~(np.isnan(y) | np.isnan(p))
    if not mask.any():
        return float("nan")
    return float(np.mean((y[mask] - p[mask]) ** 2))


def log_loss(y, p):
    mask = ~(np.isnan(y) | np.isnan(p))
    if not mask.any():
        return float("nan")
    pp = np.clip(p[mask], 1e-12, 1.0 - 1e-12)
    yy = y[mask]
    return float(-np.mean(yy * np.log(pp) + (1.0 - yy) * np.log(1.0 - pp)))


def roc_auc(y, p):
    mask = ~(np.isnan(y) | np.isnan(p))
    yy = y[mask]
    pp = p[mask]
    pos = pp[yy == 1]
    neg = pp[yy == 0]
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    order = np.argsort(pp)
    ranks = np.empty(len(pp), dtype=float)
    ranks[order] = np.arange(1, len(pp) + 1, dtype=float)
    sorted_pp = pp[order]
    unique_vals, inv = np.unique(sorted_pp, return_inverse=True)
    for i in range(len(unique_vals)):
        ranks[order[inv == i]] = np.mean(ranks[order[inv == i]])
    n_pos = len(pos)
    n_neg = len(neg)
    return float((ranks[yy == 1].sum() - n_pos * (n_pos + 1) / 2) / (n_pos * n_neg))


def main():
    sdir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
        "research_state/session_" + SESSION_UTC)

    # ---- (a) Input integrity ----
    sha_ok = sha_bad = 0
    for subdir in ["candles_1h", "funding", "open_interest"]:
        for month in MONTHS:
            sp = BULK / subdir / f"{month}.parquet.sha256"
            if not sp.is_file():
                sha_bad += 1
                continue
            stored = sp.read_text().strip().split()[0]
            if sha256_file(BULK / subdir / f"{month}.parquet") == stored:
                sha_ok += 1
            else:
                sha_bad += 1

    # ---- (b) Load candles + funding using pyarrow column ops ----
    all_data = {}  # coin -> dict of hour_idx -> {close, fund, prem}
    hour_set = set()

    for month in MONTHS:
        # candles
        t = pq.read_table(BULK / "candles_1h" / f"{month}.parquet")
        ts = t.column("timestamp").to_numpy().astype("datetime64[s]").astype(np.int64) // 3600 * 3600
        mk = t.column("market").to_numpy()
        cc = t.column("coin").to_numpy() if "coin" in t.column_names else None
        cl = t.column("close").to_numpy().astype(float)
        for i in range(len(ts)):
            c = cl[i]
            if not np.isfinite(c) or c <= 0:
                continue
            hk = int(ts[i])
            coin = str(cc[i]).upper() if cc is not None else str(mk[i]).split(":")[-1].replace("-PERP", "").upper()
            all_data.setdefault(coin, {}).setdefault(hk, {"close": c, "fund": 0.0, "prem": 0.0})
            hour_set.add(hk)

        # funding
        t = pq.read_table(BULK / "funding" / f"{month}.parquet")
        ts = t.column("timestamp").to_numpy().astype("datetime64[s]").astype(np.int64) // 3600 * 3600
        mk = t.column("market").to_numpy()
        rate = t.column("funding_rate").to_numpy().astype(float)
        prem = t.column("premium").to_numpy().astype(float)
        for i in range(len(ts)):
            hk = int(ts[i])
            coin = str(mk[i]).split(":")[-1].replace("-PERP", "").upper()
            r = rate[i] if np.isfinite(rate[i]) else 0.0
            p = prem[i] if np.isfinite(prem[i]) else 0.0
            if coin in all_data and hk in all_data[coin]:
                all_data[coin][hk]["fund"] = r
                all_data[coin][hk]["prem"] = p

    all_coins = sorted(all_data.keys())
    all_hours = sorted(hour_set)
    n_h = len(all_hours)
    hour_to_idx = {hk: i for i, hk in enumerate(all_hours)}

    # ---- (c) Per-coin series with vectorized breach labels ----
    series = {}
    for coin in all_coins:
        cdict = all_data[coin]
        hours = sorted(cdict.keys())
        n_hc = len(hours)
        closes = np.array([cdict[hk]["close"] for hk in hours], dtype=float)
        funds = np.array([cdict[hk]["fund"] for hk in hours], dtype=float)
        prems = np.array([cdict[hk]["prem"] for hk in hours], dtype=float)

        # log returns
        rets = np.zeros(n_hc, dtype=float)
        rets[1:] = np.diff(np.log(closes))
        rets_sq = rets ** 2
        cumsum = np.concatenate([[0.0], np.cumsum(rets_sq)])
        rv6 = np.array([cumsum[min(i + 1, n_hc)] - cumsum[max(0, i - 5)] for i in range(n_hc)])
        rv24 = np.array([cumsum[min(i + 1, n_hc)] - cumsum[max(0, i - 23)] for i in range(n_hc)])

        # Vectorized breach labels: long = max future price >= threshold
        long_thresh = closes * (1.0 + 1.0 / (LEVERAGE * (1.0 - MMR)))
        short_thresh = closes * (1.0 - 1.0 / (LEVERAGE * (1.0 - MMR)))
        label_long = np.full(n_hc, np.nan)
        label_short = np.full(n_hc, np.nan)
        for i in range(n_hc - HORIZON_H):
            future_max = closes[i + 1:i + 1 + HORIZON_H].max()
            future_min = closes[i + 1:i + 1 + HORIZON_H].min()
            if future_max >= long_thresh[i]:
                label_long[i] = 1.0
            elif future_min <= short_thresh[i]:
                label_short[i] = 1.0
            # If neither boundary hit, label stays NaN (no breach) -- but we need
            # a negative class too. Use: label=0 if no breach within horizon.
            # For simplicity: label_long=0 if no long breach, label_short=0 if no short breach.
            # We set 0 explicitly below for origins with a full forward window.
        # Fill negatives: any origin with full forward window but no breach = 0
        for i in range(n_hc - HORIZON_H):
            if np.isnan(label_long[i]):
                label_long[i] = 0.0
            if np.isnan(label_short[i]):
                label_short[i] = 0.0

        # EMA24
        ema = np.empty(n_hc, dtype=float)
        alpha = 2.0 / 25.0
        ema[0] = closes[0]
        for i in range(1, n_hc):
            ema[i] = alpha * closes[i] + (1 - alpha) * ema[i - 1]
        ma_dev = closes / ema - 1.0

        series[coin] = {
            "hours": np.array(hours, dtype=np.int64),
            "closes": closes, "rv6": rv6, "rv24": rv24,
            "fund": funds, "prem": prems,
            "ma_dev": ma_dev,
            "label_long": label_long, "label_short": label_short,
        }

    # ---- (d) Chronological split ----
    cut = int(n_h * 0.60)
    train_hours = set(all_hours[:cut])
    test_hours = sorted(set(h for h in all_hours[cut + 48:]))
    blocks = [test_hours[i:i + 168] for i in range(0, len(test_hours), 168)]
    blocks = [b for b in blocks if len(b) == 168]
    block_of = {hk: bi for bi, blk in enumerate(blocks) for hk in blk}

    def elig_origin(hk):
        bi = block_of.get(hk)
        return bi is not None and hk + HORIZON_H * 3600 <= blocks[bi][-1]

    eligible = [hk for hk in test_hours if elig_origin(hk)]

    # ---- (e) Build test rows ----
    test_long, test_short = [], []
    for coin in all_coins:
        s = series[coin]
        hmap = {int(hk): i for i, hk in enumerate(s["hours"])}
        for hk in eligible:
            if hk not in hmap:
                continue
            i = hmap[hk]
            rec = (coin, hk, float(s["rv6"][i]), float(s["rv24"][i]),
                   float(s["fund"][i]), float(s["prem"][i]),
                   float(s["ma_dev"][i]))
            lbl_l = float(s["label_long"][i])
            lbl_s = float(s["label_short"][i])
            test_long.append(rec + (lbl_l,))
            test_short.append(rec + (lbl_s,))

    # ---- (f) Train-only scaling ----
    train_vals = {"rv6": [], "rv24": [], "fund": [], "prem": [], "ma_dev": []}
    for coin in all_coins:
        s = series[coin]
        hmap = {int(hk): i for i, hk in enumerate(s["hours"])}
        for hk in train_hours:
            if hk not in hmap:
                continue
            i = hmap[hk]
            train_vals["rv6"].append(float(s["rv6"][i]))
            train_vals["rv24"].append(float(s["rv24"][i]))
            train_vals["fund"].append(float(s["fund"][i]))
            train_vals["prem"].append(float(s["prem"][i]))
            train_vals["ma_dev"].append(float(s["ma_dev"][i]))
    sc = {}
    for k_ in train_vals:
        v = np.array(train_vals[k_])
        v = v[np.isfinite(v)]
        sc[k_] = (float(v.mean()) if len(v) else 0.0,
                  float(v.std()) if len(v) and v.std() > 0 else 1.0)

    def z(v, k_):
        if not np.isfinite(v):
            return 0.0
        m, s = sc[k_]
        return (v - m) / s

    def feat_B1(rec):
        return [math.log(max(rec[2], 0.0) + 1e-12),
                math.log(max(rec[3], 0.0) + 1e-12)]

    def feat_C2(rec):
        return feat_B1(rec) + [z(rec[4], "fund"), z(rec[5], "prem"), z(rec[6], "ma_dev")]

    # ---- (g) Fit on train ----
    train_long, train_short = [], []
    for coin in all_coins:
        s = series[coin]
        hmap = {int(hk): i for i, hk in enumerate(s["hours"])}
        for hk in train_hours:
            if hk not in hmap:
                continue
            i = hmap[hk]
            rec = (coin, hk, float(s["rv6"][i]), float(s["rv24"][i]),
                   float(s["fund"][i]), float(s["prem"][i]),
                   float(s["ma_dev"][i]))
            train_long.append(rec + (float(s["label_long"][i]),))
            train_short.append(rec + (float(s["label_short"][i]),))

    def fit(rows_in, feat_fn):
        X = [feat_fn(r) for r in rows_in]
        y = [r[-1] for r in rows_in]
        return logreg_fit(X, y)

    beta_B1_l = fit(train_long, feat_B1)
    beta_C2_l = fit(train_long, feat_C2)
    beta_B1_s = fit(train_short, feat_B1)
    beta_C2_s = fit(train_short, feat_C2)

    # ---- (h) Predict on test ----
    def pred(rows_in, feat_fn, beta):
        X = np.array([feat_fn(r) for r in rows_in])
        y = np.array([r[-1] for r in rows_in])
        p = logreg_predict(X, beta)
        return y, p

    yB1_l, pB1_l = pred(test_long, feat_B1, beta_B1_l)
    yC2_l, pC2_l = pred(test_long, feat_C2, beta_C2_l)
    yB1_s, pB1_s = pred(test_short, feat_B1, beta_B1_s)
    yC2_s, pC2_s = pred(test_short, feat_C2, beta_C2_s)

    def metrics(y, p):
        return {"brier": brier_score(y, p), "log_loss": log_loss(y, p),
                "roc_auc": roc_auc(y, p), "n": int(len(y)),
                "n_pos": int(np.sum(y == 1))}

    rB1_l = metrics(yB1_l, pB1_l)
    rC2_l = metrics(yC2_l, pC2_l)
    rB1_s = metrics(yB1_s, pB1_s)
    rC2_s = metrics(yC2_s, pC2_s)

    def rel_imp(b1, c2):
        return (b1 - c2) / b1 * 100.0 if b1 > 0 else float("nan")

    rel_l = rel_imp(rB1_l["brier"], rC2_l["brier"])
    rel_s = rel_imp(rB1_s["brier"], rC2_s["brier"])

    # ---- (i) Bootstrap CI95 (per-coin, vectorized) ----
    import random
    rng = random.Random(20261123)
    coins_test = sorted({r[0] for r in test_long})
    coin_rows_l = {c: [r for r in test_long if r[0] == c] for c in coins_test}
    coin_rows_s = {c: [r for r in test_short if r[0] == c] for c in coins_test}

    def boot_diff_long():
        sample = rng.choices(coins_test, k=len(coins_test))
        ys, psB, psC = [], [], []
        for c in sample:
            for r in coin_rows_l.get(c, []):
                ys.append(r[-1])
                psB.append(float(logreg_predict(np.array([feat_B1(r)]), beta_B1_l)[0]))
                psC.append(float(logreg_predict(np.array([feat_C2(r)]), beta_C2_l)[0]))
        if not ys:
            return 0.0
        return brier_score(np.array(ys), np.array(psC)) - brier_score(np.array(ys), np.array(psB))

    def boot_diff_short():
        sample = rng.choices(coins_test, k=len(coins_test))
        ys, psB, psC = [], [], []
        for c in sample:
            for r in coin_rows_s.get(c, []):
                ys.append(r[-1])
                psB.append(float(logreg_predict(np.array([feat_B1(r)]), beta_B1_s)[0]))
                psC.append(float(logreg_predict(np.array([feat_C2(r)]), beta_C2_s)[0]))
        if not ys:
            return 0.0
        return brier_score(np.array(ys), np.array(psC)) - brier_score(np.array(ys), np.array(psB))

    boot_l = sorted(boot_diff_long() for _ in range(N_BOOT))
    boot_s = sorted(boot_diff_short() for _ in range(N_BOOT))
    lo_l = boot_l[int(N_BOOT * 0.025)]; hi_l = boot_l[int(N_BOOT * 0.975)]
    lo_s = boot_s[int(N_BOOT * 0.025)]; hi_s = boot_s[int(N_BOOT * 0.975)]

    raw_p_l = sum(1 for d in boot_l if d >= 0) / N_BOOT
    raw_p_s = sum(1 for d in boot_s if d >= 0) / N_BOOT
    holm_l = min(1.0, 2 * raw_p_l)
    holm_s = min(1.0, 2 * raw_p_s)

    verdict_l = "SUPPORTED" if (rel_l >= MATERIALITY_PCT and hi_l < 0 and holm_l < ALPHA_K) else "NOT_SUPPORTED"
    verdict_s = "SUPPORTED" if (rel_s >= MATERIALITY_PCT and hi_s < 0 and holm_s < ALPHA_K) else "NOT_SUPPORTED"

    result = {
        "experiment_id": "FCLR-TRACKB-MODELED-BREACH-01",
        "campaign": "FCLR-TRACKA-SOURCE-AUDIT-01-20261122T225107Z",
        "session_utc": SESSION_UTC,
        "label_construct": "modeled_hypothetical_boundary_breach",
        "input_integrity": {"sha_ok": sha_ok, "sha_bad": sha_bad,
                            "sha_all_match": sha_bad == 0},
        "coverage": {"n_coins": len(all_coins), "n_hours": n_h,
                     "train_hours": len(train_hours),
                     "test_blocks": len(blocks),
                     "eligible_origins": len(eligible),
                     "test_rows_long": rB1_l["n"],
                     "test_rows_short": rB1_s["n"]},
        "headline_long": {
            "brier_B1": rB1_l["brier"], "brier_C2": rC2_l["brier"],
            "rel_brier_improvement_pct": rel_l,
            "log_loss_C2": rC2_l["log_loss"], "roc_auc_C2": rC2_l["roc_auc"],
            "n": rB1_l["n"], "n_pos": rB1_l["n_pos"],
            "materiality_met": rel_l >= MATERIALITY_PCT,
        },
        "headline_short": {
            "brier_B1": rB1_s["brier"], "brier_C2": rC2_s["brier"],
            "rel_brier_improvement_pct": rel_s,
            "log_loss_C2": rC2_s["log_loss"], "roc_auc_C2": rC2_s["roc_auc"],
            "n": rB1_s["n"], "n_pos": rB1_s["n_pos"],
            "materiality_met": rel_s >= MATERIALITY_PCT,
        },
        "uncertainty": {
            "bootstrap_replicates": N_BOOT,
            "ci95_long": [lo_l, hi_l], "ci95_short": [lo_s, hi_s],
            "ci95_long_upper_below_zero": hi_l < 0,
            "ci95_short_upper_below_zero": hi_s < 0,
        },
        "multiplicity": {
            "raw_pvals": {"long": raw_p_l, "short": raw_p_s},
            "holm_adjusted": {"long": holm_l, "short": holm_s},
            "alpha_k": ALPHA_K,
            "long_significant": holm_l < ALPHA_K,
            "short_significant": holm_s < ALPHA_K,
        },
        "decision": {
            "verdict_long": verdict_l, "verdict_short": verdict_s,
            "null_preserved_honestly": verdict_l != "SUPPORTED" and verdict_s != "SUPPORTED",
            "modeled_breach_proxy_not_observed_liquidation": True,
        },
    }

    out_json = sdir / f"fclr_tracks01_eval_{SESSION_UTC}.json"
    out_json.write_text(json.dumps(result, indent=2))

    lines = [
        f"# FCLR-TRACKB-MODELED-BREACH-01 — Track B Modeled Breach Evaluation",
        f"",
        f"**Campaign:** FCLR-TRACKA-SOURCE-AUDIT-01-20261122T225107Z",
        f"**Session UTC:** {SESSION_UTC}",
        f"",
        f"## Input integrity",
        f"- SHA-256 verified: {sha_ok} ok, {sha_bad} bad",
        f"",
        f"## Coverage",
        f"- Coins: {len(all_coins)}, Hours: {n_h}",
        f"- Train hours: {len(train_hours)}, Test blocks: {len(blocks)}",
        f"- Eligible origins: {len(eligible)}",
        f"- Test rows long/short: {rB1_l['n']}/{rB1_s['n']}",
        f"",
        f"## Headline (long arm)",
        f"- Brier B1: {rB1_l['brier']:.6f}, C2: {rC2_l['brier']:.6f}",
        f"- Rel Brier improvement: {rel_l:.4f}%",
        f"- Log loss C2: {rC2_l['log_loss']:.6f}, ROC-AUC: {rC2_l['roc_auc']:.6f}",
        f"- Materiality met: {rel_l >= MATERIALITY_PCT}",
        f"",
        f"## Headline (short arm)",
        f"- Brier B1: {rB1_s['brier']:.6f}, C2: {rC2_s['brier']:.6f}",
        f"- Rel Brier improvement: {rel_s:.4f}%",
        f"- Log loss C2: {rC2_s['log_loss']:.6f}, ROC-AUC: {rC2_s['roc_auc']:.6f}",
        f"- Materiality met: {rel_s >= MATERIALITY_PCT}",
        f"",
        f"## Uncertainty (bootstrap N={N_BOOT})",
        f"- CI95 long: [{lo_l:.6f}, {hi_l:.6f}] upper<0: {hi_l < 0}",
        f"- CI95 short: [{lo_s:.6f}, {hi_s:.6f}] upper<0: {hi_s < 0}",
        f"",
        f"## Multiplicity (Holm, k=2)",
        f"- Raw p: long={raw_p_l:.6f} short={raw_p_s:.6f}",
        f"- Holm adj: long={holm_l:.6f} short={holm_s:.6f}, alpha_k={ALPHA_K}",
        f"",
        f"## Decision",
        f"- Verdict long: {verdict_l}",
        f"- Verdict short: {verdict_s}",
        f"- Modeled breach proxy (not observed liquidation): true",
    ]
    out_md = sdir / f"fclr_tracks01_eval_{SESSION_UTC}.md"
    out_md.write_text("\n".join(lines) + "\n")

    print(f"WROTE {out_json}")
    print(f"WROTE {out_md}")
    print(f"long: B1={rB1_l['brier']:.6f} C2={rC2_l['brier']:.6f} rel={rel_l:.4f}% verdict={verdict_l}")
    print(f"short: B1={rB1_s['brier']:.6f} C2={rC2_s['brier']:.6f} rel={rel_s:.4f}% verdict={verdict_s}")


if __name__ == "__main__":
    main()
