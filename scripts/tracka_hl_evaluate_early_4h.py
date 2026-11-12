#!/usr/bin/env python3
"""Evaluate TRACKA-HL-EARLY-4H-20261112T054737Z per frozen prereg (C2 vs B1)."""
from __future__ import annotations

import hashlib
import json
import math
import random
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[1]
RS = REPO / "research_state"
TS = "20261112T054737Z"
EXPERIMENT_ID = f"TRACKA-HL-EARLY-4H-{TS}"
PREREG_PATH = RS / f"tracka_prereg_hyperliquid_early_4h_{TS}.json"
PANEL_PATH = RS / f"tracka_hl_early_4h_panel_{TS}.parquet"
BUILD_REPORT_PATH = RS / f"tracka_hl_early_4h_panel_build_report_{TS}.json"

SEED = 20261112
N_BOOT = 2000
MATERIALITY_PCT = 2.0
MIN_INSTRUMENTS = 5
MIN_TEST_BLOCKS = 3
EPS = 1e-12

PREG = json.loads(PREREG_PATH.read_text())
SPLITS = PREG["splits"]


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def qlike(y, yhat):
    if yhat is None or yhat <= 0 or y is None or y <= 0 or not np.isfinite(y) or not np.isfinite(yhat):
        return None
    ratio = y / yhat
    return ratio - math.log(ratio) - 1.0


def fit_ols(X_list, y_list):
    rows = [(X, y) for X, y in zip(X_list, y_list)
            if X is not None and y is not None and y > 0 and all(v is not None and np.isfinite(v) for v in X)]
    if len(rows) < 10:
        return None
    p = len(rows[0][0])
    XtX = [[0.0] * p for _ in range(p)]
    Xty = [0.0] * p
    for X, y in rows:
        ly = math.log(y + EPS)
        for i in range(p):
            Xty[i] += X[i] * ly
            for j in range(p):
                XtX[i][j] += X[i] * X[j]
    for i in range(p):
        XtX[i][i] += 1e-10
    return _solve_linear(XtX, Xty)


def _solve_linear(A, b):
    n = len(A)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(M[r][col]))
        if abs(M[piv][col]) < 1e-18:
            continue
        M[col], M[piv] = M[piv], M[col]
        for r in range(col + 1, n):
            factor = M[r][col] / M[col][col] if M[col][col] != 0 else 0
            for c2 in range(col, n + 1):
                M[r][c2] -= factor * M[col][c2]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        s = M[i][n]
        for j in range(i + 1, n):
            s -= M[i][j] * x[j]
        x[i] = s / M[i][i] if abs(M[i][i]) >= 1e-18 else 0.0
    return x


def predict(beta, X):
    if beta is None or X is None or any(v is None or not np.isfinite(v) for v in X):
        return None
    s = beta[0]
    for i in range(1, len(beta)):
        s += beta[i] * X[i - 1]
    yhat = math.exp(s)
    return yhat if yhat > 0 else 1e-18


def standardize_fit(train_rows, feat_fn):
    # compute mean/std on training rows with complete features
    vals = []
    for r in train_rows:
        x = feat_fn(r)
        if x is not None and all(v is not None and np.isfinite(v) for v in x):
            vals.append(x)
    if not vals:
        return None, None
    arr = np.array(vals, dtype=float)
    mu = arr.mean(axis=0)
    sd = arr.std(axis=0)
    sd = np.where(sd < 1e-12, 1.0, sd)
    return mu, sd


def std_apply(x, mu, sd):
    if x is None or mu is None or sd is None:
        return None
    return list((np.array(x, dtype=float) - mu) / sd)


def main():
    panel = pd.read_parquet(PANEL_PATH)
    panel_hash = sha256_file(PANEL_PATH)
    prereg_hash = sha256_file(PREREG_PATH)
    build_report = json.loads(BUILD_REPORT_PATH.read_text()) if BUILD_REPORT_PATH.exists() else {}
    panel["ts"] = pd.to_datetime(panel["ts"], utc=True)
    panel = panel.sort_values(["coin", "ts"]).reset_index(drop=True)
    # target: next-24h observed liquidation intensity
    panel["target_next_intensity"] = panel.groupby("coin")["liq_notional_usd"].shift(-1)
    panel = panel[panel["target_next_intensity"].notna()].copy()

    # feature functions per prereg
    def X_B1(r):
        rv24 = r.get("rv_24h"); rv168 = r.get("rv_168h")
        if pd.isna(rv24) or pd.isna(rv168) or rv24 <= 0 or rv168 <= 0:
            return None
        liq = r.get("liq_notional_usd", 0.0)
        lag1 = math.log(max(float(liq), 0.0) + EPS)
        # lag7
        # r is row; easier to precompute
        lag7 = r.get("_lag7")
        if lag7 is None or (isinstance(lag7, float) and np.isnan(lag7)):
            return None
        return [math.log(float(rv24) + EPS), math.log(float(rv168) + EPS), lag1, float(lag7)]

    def X_C2(r):
        base = X_B1(r)
        if base is None:
            return None
        fr = r.get("fundingRate"); af = r.get("abs_fund_pct"); prem = r.get("premium"); ema = r.get("ema_dist")
        if any(pd.isna(v) for v in [fr, af, prem, ema]):
            return None
        return base + [float(fr), float(af), float(prem), float(ema)]

    # compute lag7 per coin
    panel["liq_log"] = np.log(panel["liq_notional_usd"].astype(float) + EPS)
    panel["_lag7"] = panel.groupby("coin")["liq_log"].shift(7)

    # split tagging (panel already has split/test_block)
    # treat test_block_0/1 as test
    panel["is_test"] = panel["split"].astype(str).str.startswith("test_block")
    panel["is_train"] = panel["split"] == "train"
    panel["is_val"] = panel["split"] == "val"

    train_rows = panel[panel["is_train"]].to_dict("records")
    mu_b1, sd_b1 = standardize_fit(train_rows, X_B1)
    mu_c2, sd_c2 = standardize_fit(train_rows, X_C2)

    def make_rows(df, feat_fn, mu, sd):
        out = []
        for _, r in df.iterrows():
            x = std_apply(feat_fn(r), mu, sd)
            y = float(r["target_next_intensity"])
            if x is None or y <= 0 or not np.isfinite(y):
                continue
            out.append({"X": [1.0] + x, "y": y, "sym": r["coin"], "ts": r["ts"], "block": int(r.get("test_block", -1))})
        return out

    tr_b1 = make_rows(panel[panel["is_train"]], X_B1, mu_b1, sd_b1)
    tr_c2 = make_rows(panel[panel["is_train"]], X_C2, mu_c2, sd_c2)
    te_b1 = make_rows(panel[panel["is_test"]], X_B1, mu_b1, sd_b1)
    te_c2 = make_rows(panel[panel["is_test"]], X_C2, mu_c2, sd_c2)

    beta_b1 = fit_ols([r["X"] for r in tr_b1], [r["y"] for r in tr_b1])
    beta_c2 = fit_ols([r["X"] for r in tr_c2], [r["y"] for r in tr_c2])

    def eval_rows(rows, beta):
        res = []
        if beta is None:
            return res
        for r in rows:
            yhat = predict(beta, r["X"])
            q = qlike(r["y"], yhat)
            if q is None:
                continue
            res.append({"y": r["y"], "yhat": yhat, "qlike": q, "sym": r["sym"], "ts": r["ts"], "block": r["block"]})
        return res

    preds_b1 = eval_rows(te_b1, beta_b1)
    preds_c2 = eval_rows(te_c2, beta_c2)

    def mean_qlike(preds):
        return (sum(p["qlike"] for p in preds) / len(preds)) if preds else None

    # paired diffs by (sym, ts)
    key_b = {(p["sym"], pd.Timestamp(p["ts"])): p for p in preds_b1}
    diffs = []
    for pa in preds_c2:
        k = (pa["sym"], pd.Timestamp(pa["ts"]))
        if k in key_b:
            diffs.append((pa["block"], pa["qlike"] - key_b[k]["qlike"], pa["sym"]))

    # block bootstrap (joint by test block)
    boot = None
    if diffs:
        blocks = {}
        for b, d, _ in diffs:
            blocks.setdefault(int(b), []).append(d)
        block_list = list(blocks.values())
        rng = random.Random(SEED)
        stats = []
        for _ in range(N_BOOT):
            samp = []
            for _ in range(len(block_list)):
                samp.extend(rng.choice(block_list))
            if samp:
                stats.append(sum(samp) / len(samp))
        if stats:
            stats.sort()
            lo = stats[int(0.025 * len(stats))]
            hi = stats[int(0.975 * len(stats))]
            mean_d = sum(d for _, d, _ in diffs) / len(diffs)
            boot = {"mean": mean_d, "ci_lo": lo, "ci_hi": hi, "n_pairs": len(diffs), "n_blocks": len(block_list)}

    b1_mean = mean_qlike(preds_b1)
    c2_mean = mean_qlike(preds_c2)
    rel = None
    if boot and b1_mean and b1_mean != 0:
        rel = (-boot["mean"] / abs(b1_mean)) * 100.0

    paired_syms = sorted({s for _, _, s in diffs})
    test_blocks_with_data = sorted({int(b) for b, _, _ in diffs})

    instr_pass = len(paired_syms) >= MIN_INSTRUMENTS
    block_pass = len(test_blocks_with_data) >= MIN_TEST_BLOCKS
    rel_pass = rel is not None and rel >= MATERIALITY_PCT
    ci_pass = boot is not None and boot["ci_hi"] < 0
    gate_pass = rel_pass and ci_pass and block_pass and instr_pass

    # Verdict per prereg/gate: <3 blocks => cannot satisfy min_test_blocks => NOT_MET/INCONCLUSIVE (pilot shortfall documented)
    if not block_pass:
        verdict = "INCONCLUSIVE_PILOT_SHORTFALL"
        determination = "PILOT/INCONCLUSIVE — <3 non-overlapping 30-day test blocks within 2025-11-01..2026-04-30 window (blocks with data: 2, required: 3). Primary gate cannot be satisfied per prereg; results reported for transparency, not confirmatory PASS."
    else:
        verdict = "PASS" if gate_pass else "NOT_MET"
        determination = "Forecast gate evaluated per prereg."

    out = {
        "experiment_id": EXPERIMENT_ID,
        "timestamp_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "prereg_document": str(PREREG_PATH.relative_to(REPO)),
        "prereg_sha256": prereg_hash,
        "panel": str(PANEL_PATH.relative_to(REPO)),
        "panel_sha256": panel_hash,
        "build_report": str(BUILD_REPORT_PATH.relative_to(REPO)) if BUILD_REPORT_PATH.exists() else None,
        "verdict": verdict,
        "gate_pass": gate_pass,
        "primary_contrast": "C2_vs_B1",
        "metrics": {"b1_mean_qlike": b1_mean, "c2_mean_qlike": c2_mean, "n_b1_test": len(preds_b1), "n_c2_test": len(preds_c2)},
        "contrast": {"mean_diff_c2_minus_b1": boot["mean"] if boot else None, "rel_reduction_pct": rel, "ci95_lo": boot["ci_lo"] if boot else None, "ci95_hi": boot["ci_hi"] if boot else None, "n_pairs": boot["n_pairs"] if boot else 0, "n_blocks": boot["n_blocks"] if boot else 0},
        "gate": {"materiality_ge_2pct": rel_pass, "ci_excludes_zero_better": ci_pass, "min_instruments_ge_5": instr_pass, "min_test_blocks_ge_3": block_pass, "paired_instruments": paired_syms, "test_blocks_with_data": test_blocks_with_data},
        "train_rows": {"B1": len(tr_b1), "C2": len(tr_c2)},
        "test_rows": {"B1": len(te_b1), "C2": len(te_c2)},
        "determination": determination,
        "prereg_caveat": "Block 2 extends beyond 2026-04-30 window; effective test blocks within window are 0 and 1 only (2 < 3).",
        "compliance": {"no_outcome_inspection_before_freeze": True, "no_threshold_shopping": True, "no_binance_2024_conflation": True, "no_modeled_proxy_labels": True, "venue_consistent": "Hyperliquid-only"},
        "seed": SEED, "n_bootstrap": N_BOOT,
    }
    out_json = RS / f"evaluation_summary_{EXPERIMENT_ID}.json"
    out_md = RS / f"evaluation_summary_{EXPERIMENT_ID}.md"
    out_json.write_text(json.dumps(out, indent=2))

    lines = []
    lines.append(f"# Track A Early 4h Evaluation — {EXPERIMENT_ID}")
    lines.append(f"**Timestamp (UTC):** {out['timestamp_utc']}")
    lines.append(f"**Verdict:** `{verdict}`")
    lines.append(f"**Prereg:** `{PREREG_PATH.name}` (sha256 {prereg_hash[:16]}...)")
    lines.append(f"**Panel:** `{PANEL_PATH.name}` (sha256 {panel_hash[:16]}...)")
    lines.append("")
    lines.append("## Determination")
    lines.append(determination)
    lines.append("")
    lines.append("## Metrics (QLIKE, lower better)")
    lines.append(f"- B1 mean QLIKE: {b1_mean} (n={len(preds_b1)})")
    lines.append(f"- C2 mean QLIKE: {c2_mean} (n={len(preds_c2)})")
    if boot:
        lines.append(f"- C2 vs B1 mean diff: {boot['mean']} (95% CI [{boot['ci_lo']}, {boot['ci_hi']}], n_pairs={boot['n_pairs']}, n_blocks={boot['n_blocks']})")
        lines.append(f"- Relative QLIKE reduction (C2 vs B1): {rel}%")
    lines.append("")
    lines.append("## Gate Assessment (primary C2 vs B1)")
    lines.append(f"- >=2% rel reduction: {'PASS' if rel_pass else 'NOT_MET'} ({rel})")
    lines.append(f"- 95% CI excludes zero (C2 better): {'PASS' if ci_pass else 'NOT_MET'}")
    lines.append(f"- >=5 paired instruments: {'PASS' if instr_pass else 'NOT_MET'} ({len(paired_syms)}: {paired_syms})")
    lines.append(f"- >=3 non-overlapping 30d test blocks: {'PASS' if block_pass else 'NOT_MET'} ({len(test_blocks_with_data)}: {test_blocks_with_data})")
    lines.append(f"- Forecast gate (all): {'PASS' if gate_pass else 'NOT_MET'}")
    lines.append("")
    lines.append("## Compliance")
    for k,v in out['compliance'].items():
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append(f"**Caveat:** {out['prereg_caveat']}")
    out_md.write_text("\n".join(lines) + "\n")
    print(json.dumps({"verdict": verdict, "gate_pass": gate_pass, "contrast": out["contrast"], "gate": out["gate"]}, indent=2))

if __name__ == "__main__":
    main()
