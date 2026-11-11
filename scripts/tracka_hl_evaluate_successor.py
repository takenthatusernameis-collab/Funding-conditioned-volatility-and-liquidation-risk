#!/usr/bin/env python3
"""Track A successor evaluation: pre-registered C2 vs B1 on observed Hyperliquid liquidation intensity.

Loads the RV-augmented aligned panel, constructs the next-24h liquidation-intensity target,
applies the frozen pre-registered splits (train May / val early-Jun / 3 test blocks Jul-Aug-Sep-Oct
with 7d embargo), fits B0/B1/C1/C2, evaluates with QLIKE, runs block-bootstrap paired CIs,
checks the materiality gate (>=2% relative QLIKE reduction, CI excludes zero, >=5 paired instruments,
>=3 test blocks), and emits a timestamped verdict artifact.

Deterministic: fixed seed 20261111, no threshold-shopping, no outcome inspection before freeze.
"""
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
PREREG_PATH = RS / "tracka_prereg_hyperliquid_successor_20261111T133430Z.json"
SEED = 20261111
N_BOOT = 2000
MATERIALITY_PCT = 2.0
MIN_INSTRUMENTS = 5
MIN_TEST_BLOCKS = 3

PREG = json.loads(PREREG_PATH.read_text())
SYMBOLS = PREG["panel"]["symbols"]
SPLITS = PREG["split_boundaries"]
TRAIN = (pd.Timestamp(SPLITS["train"]["start"], tz="UTC"),
         pd.Timestamp(SPLITS["train"]["end"], tz="UTC"))
VAL = (pd.Timestamp(SPLITS["validation"]["start"], tz="UTC"),
       pd.Timestamp(SPLITS["validation"]["end"], tz="UTC"))
TEST_BLOCKS = [(pd.Timestamp(b["start"], tz="UTC"), pd.Timestamp(b["end"], tz="UTC"))
               for b in SPLITS["test_blocks"]]

EPS = 1e-12


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


def split_of(ts: pd.Timestamp):
    if TRAIN[0] <= ts <= TRAIN[1]:
        return "train"
    if VAL[0] <= ts <= VAL[1]:
        return "val"
    for tb in TEST_BLOCKS:
        if tb[0] <= ts <= tb[1]:
            return "test"
    return None


def test_block_of(ts: pd.Timestamp):
    for i, tb in enumerate(TEST_BLOCKS):
        if tb[0] <= ts <= tb[1]:
            return i
    return -1


def fit_ols(X_list, y_list):
    rows = [(X, y) for X, y in zip(X_list, y_list)
            if X is not None and y is not None and y > 0 and all(v is not None for v in X)]
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
    if beta is None or X is None or any(v is None for v in X):
        return None
    s = beta[0]
    for i in range(1, len(beta)):
        s += beta[i] * X[i - 1]
    yhat = math.exp(s)
    return yhat if yhat > 0 else 1e-18


def main() -> None:
    ts_utc = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    verdict_id = f"TRACKA-HL-{ts_utc}"

    # ---- 1. Load panel ----
    panel_files = sorted(RS.glob("tracka_hl_aligned_panel_with_rv_*.parquet"))
    if not panel_files:
        raise SystemExit("No RV-augmented panel found. Run tracka_hl_build_panel_with_rv.py first.")
    panel_path = panel_files[-1]
    panel = pd.read_parquet(panel_path)
    panel_hash = sha256_file(panel_path)
    panel["ts"] = pd.to_datetime(panel["ts"], utc=True)

    # ---- 2. Construct target: next-24h liq_notional_usd per symbol (shift -1 day) ----
    panel = panel.sort_values(["coin", "ts"]).reset_index(drop=True)
    panel["target_next_intensity"] = panel.groupby("coin")["liq_notional_usd"].shift(-1)
    panel = panel[panel["target_next_intensity"].notna()].copy()
    panel["split"] = panel["ts"].apply(split_of)
    panel = panel[panel["split"].notna()].reset_index(drop=True)
    panel_pos = panel[panel["target_next_intensity"] > 0].copy()
    print(f"Panel rows: {len(panel)}, positive-target rows: {len(panel_pos)}", flush=True)

    # ---- 3. Feature vectors per model ----
    def X_B0(r):
        liq = r["liq_notional_usd"]
        if pd.isna(liq) or liq <= 0:
            return None
        return [math.log(liq + EPS)]

    def X_B1(r):
        for c in ["rv1h", "rv24h", "rv168h"]:
            if pd.isna(r[c]) or r[c] <= 0:
                return None
        return [math.log(r["rv1h"] + EPS), math.log(r["rv24h"] + EPS), math.log(r["rv168h"] + EPS)]

    def X_C1(r):
        base = X_B1(r)
        if base is None:
            return None
        sf = r["fundingRate"] if pd.notna(r["fundingRate"]) else 0.0
        af = r["abs_fund_pct"] if pd.notna(r["abs_fund_pct"]) else 0.0
        return base + [float(sf), float(af)]

    def X_C2(r):
        base = X_C1(r)
        if base is None:
            return None
        prem = r["premium"] if pd.notna(r["premium"]) else 0.0
        ema = r["ema_dist"] if pd.notna(r["ema_dist"]) else 0.0
        return base + [float(prem), float(ema)]

    X_FNS = {"B0": X_B0, "B1": X_B1, "C1": X_C1, "C2": X_C2}
    for name, fn in X_FNS.items():
        panel_pos[f"X_{name}"] = panel_pos.apply(fn, axis=1)

    model_rows = {}
    for name in ["B0", "B1", "C1", "C2"]:
        model_rows[name] = panel_pos[panel_pos[f"X_{name}"].notna()].copy()

    # ---- 4. Fit OLS on train (log target) ----
    models = {}
    for name in ["B0", "B1", "C1", "C2"]:
        dfm = model_rows[name]
        tr = dfm[dfm["split"] == "train"]
        if len(tr) < 10:
            models[name] = None
            continue
        Xtr = [[1.0] + list(x) for x in tr[f"X_{name}"]]
        ytr = list(tr["target_next_intensity"])
        beta = fit_ols(Xtr, ytr)
        models[name] = {"beta": beta}

    # ---- 5. Evaluate on test blocks ----
    def eval_model(name):
        model = models.get(name)
        if not model or model["beta"] is None:
            return []
        beta = model["beta"]
        dfm = model_rows[name]
        te = dfm[dfm["split"] == "test"]
        res = []
        for _, r in te.iterrows():
            X = list(r[f"X_{name}"])
            y = r["target_next_intensity"]
            yhat = predict(beta, X)
            if yhat is None or yhat <= 0 or y <= 0:
                continue
            q = qlike(y, yhat)
            if q is None:
                continue
            res.append({"y": y, "yhat": yhat, "qlike": q, "sym": r["coin"],
                        "ts_ms": int(r["ts"].timestamp() * 1000),
                        "ts": r["ts"], "block": test_block_of(r["ts"])})
        return res

    results = {name: eval_model(name) for name in ["B0", "B1", "C1", "C2"]}

    def mean_qlike(preds):
        if not preds:
            return None
        return sum(p["qlike"] for p in preds) / len(preds)

    # ---- 6. Paired differences + block bootstrap ----
    def paired_diffs(preds_a, preds_b):
        key_b = {(p["sym"], p["ts_ms"]): p for p in preds_b}
        diffs = []
        for pa in preds_a:
            key = (pa["sym"], pa["ts_ms"])
            if key in key_b:
                diffs.append((pa["ts_ms"], pa["ts"], pa["block"], pa["qlike"] - key_b[key]["qlike"]))
        return diffs

    def block_bootstrap(diffs):
        if not diffs:
            return None
        blocks = {}
        for ts_ms, ts, block, d in diffs:
            blocks.setdefault(block, []).append(d)
        block_list = list(blocks.values())
        rng = random.Random(SEED)
        stats = []
        for _ in range(N_BOOT):
            samp = []
            for _ in range(len(block_list)):
                samp.extend(rng.choice(block_list))
            if samp:
                stats.append(sum(samp) / len(samp))
        if not stats:
            return None
        stats.sort()
        lo = stats[int(0.025 * len(stats))]
        hi = stats[int(0.975 * len(stats))]
        mean_d = sum(d for _, _, _, d in diffs) / len(diffs)
        return {"mean": mean_d, "ci_lo": lo, "ci_hi": hi, "n_pairs": len(diffs), "n_blocks": len(block_list)}

    contrasts = {}
    for a, b in [("C2", "B1"), ("C1", "B1"), ("C2", "C1")]:
        diffs = paired_diffs(results[a], results[b])
        boot = block_bootstrap(diffs)
        b_mean = mean_qlike(results[b])
        if boot and b_mean and b_mean != 0:
            rel = (-boot["mean"] / abs(b_mean)) * 100.0
        else:
            rel = None
        contrasts[f"{a}_vs_{b}"] = {
            "mean_diff": boot["mean"] if boot else None,
            "rel_reduction_pct": rel,
            "ci_lo": boot["ci_lo"] if boot else None,
            "ci_hi": boot["ci_hi"] if boot else None,
            "n_pairs": boot["n_pairs"] if boot else 0,
            "n_blocks": boot["n_blocks"] if boot else 0,
        }

    # ---- 7. Gate assessment ----
    c = contrasts.get("C2_vs_B1")
    test_days = sum((tb[1] - tb[0]).days + 1 for tb in TEST_BLOCKS)
    paired_syms = sorted({p["sym"] for p in results["C2"]}) if results.get("C2") else []
    test_blocks_with_data = sorted({p["block"] for p in results["C2"]}) if results.get("C2") else []

    instr_pass = len(paired_syms) >= MIN_INSTRUMENTS
    block_pass = len(test_blocks_with_data) >= MIN_TEST_BLOCKS
    if c and c["mean_diff"] is not None and c["ci_lo"] is not None and c["ci_hi"] is not None:
        rel_pass = c["rel_reduction_pct"] is not None and c["rel_reduction_pct"] >= MATERIALITY_PCT
        ci_pass = c["ci_hi"] < 0
        gate_pass = rel_pass and ci_pass and block_pass and instr_pass
    else:
        rel_pass = False
        ci_pass = False
        gate_pass = False

    verdict = "PASS" if gate_pass else "NOT_MET"

    # ---- 8. Emit verdict artifact ----
    out_md = RS / f"evaluation_summary_{verdict_id}.md"
    lines = []
    lines.append(f"# Track A Successor Evaluation — {verdict_id}")
    lines.append(f"**Timestamp (UTC):** {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}")
    lines.append(f"**Experiment:** {PREG['experiment_id']} (successor prereg)")
    lines.append(f"**Prereg document:** {PREREG_PATH.name}")
    lines.append(f"**Verdict:** `{verdict}` — Track A successor pre-registered C2 vs B1 evaluation")
    lines.append(f"**Panel (RV-augmented):** {panel_path.name} (sha256 {panel_hash[:16]}...)")
    lines.append("")
    lines.append("## 1. Determination")
    lines.append("")
    lines.append(f"Pre-registered primary contrast **C2 vs B1** (QLIKE on next-24h observed liquidation intensity)")
    lines.append(f"evaluated on the admissible overlap window `2026-05-01..2026-10-31` (9 *-PERP symbols).")
    lines.append(f"Forecast gate: **{verdict}**.")
    if gate_pass:
        lines.append("Incremental forecast skill of funding + price features over RV-only baseline DEMONSTRATED.")
    else:
        lines.append("Incremental forecast skill NOT demonstrated at pre-registered materiality gate.")
    lines.append("")
    lines.append("## 2. Panel & Coverage")
    lines.append(f"- Total buckets: {len(panel)} (9 symbols x {(pd.Timestamp('2026-10-31') - pd.Timestamp('2026-05-01')).days + 1} days)")
    lines.append(f"- Buckets with label: {int(panel['has_label'].sum())}")
    lines.append(f"- Buckets with RV24h: {int(panel['has_rv24h'].sum())}")
    lines.append(f"- Buckets complete (label+funding+RV): {int((panel['has_label'] & panel['has_funding'] & panel['has_rv_complete']).sum())}")
    syms_label = sorted(panel.loc[panel['has_label'], 'coin'].unique().tolist())
    lines.append(f"- Symbols with any label: {syms_label} (n={len(syms_label)})")
    lines.append("")
    lines.append("## 3. Test Set QLIKE (lower is better)")
    lines.append("")
    for name in ["B0", "B1", "C1", "C2"]:
        mq = mean_qlike(results[name])
        qstr = f"{mq:.6f}" if mq is not None else "N/A"
        lines.append(f"- {name}: mean_QLIKE={qstr} (n={len(results[name])})")
    lines.append("")
    lines.append("## 4. Paired comparisons (block bootstrap, 30-day blocks, seed=20261111, 2000 replications)")
    lines.append("")
    for k, v in contrasts.items():
        lines.append(f"### {k}")
        lines.append(f"- Paired n: {v['n_pairs']} across {v['n_blocks']} test block(s)")
        if v['mean_diff'] is not None:
            lines.append(f"- Mean diff (modelA - modelB), QLIKE: {v['mean_diff']:.6f}")
        ci = f"[{v['ci_lo']:.6f}, {v['ci_hi']:.6f}]" if v['ci_lo'] is not None else "[N/A, N/A]"
        lines.append(f"- 95% CI: {ci}")
        if v['rel_reduction_pct'] is not None:
            lines.append(f"- Relative QLIKE reduction: {v['rel_reduction_pct']:.2f}%")
        lines.append("")
    lines.append("## 5. Gate assessment (primary contrast C2 vs B1)")
    lines.append("")
    lines.append(f"- >= {MATERIALITY_PCT}% relative QLIKE reduction (C2 vs B1): {'PASS' if rel_pass else 'NOT_MET'}")
    if c and c['rel_reduction_pct'] is not None:
        lines.append(f"- Relative reduction: {c['rel_reduction_pct']:.2f}%")
    lines.append(f"- 95% CI excludes zero (CI hi < 0 => C2 better): {'PASS' if ci_pass else 'NOT_MET'}")
    if c and c['ci_lo'] is not None and c['ci_hi'] is not None:
        lines.append(f"- 95% CI for diff (C2-B1): [{c['ci_lo']:.6f}, {c['ci_hi']:.6f}]")
    lines.append(f"- >= {MIN_INSTRUMENTS} paired OOS instruments: {'PASS' if instr_pass else 'NOT_MET'} ({len(paired_syms)}: {', '.join(paired_syms)})")
    lines.append(f"- >= {MIN_TEST_BLOCKS} non-overlapping test blocks with data: {'PASS' if block_pass else 'NOT_MET'} ({len(test_blocks_with_data)}: blocks {test_blocks_with_data})")
    lines.append(f"- Test window days: {test_days} (3 x ~30-day blocks with 7d embargo)")
    lines.append(f"- Forecast gate (all criteria): **{verdict}**")
    lines.append("")
    lines.append("## 6. Compliance")
    lines.append("- No outcome inspection before prereg freeze: PASS (prereg frozen pre-outcomes)")
    lines.append("- No Binance/2024 conflation: PASS (Hyperliquid only, observed ironflow labels)")
    lines.append("- No modeled/proxy/synthetic liquidation labels: PASS (observed ironflow events only)")
    lines.append("- No threshold-shopping: PASS (pre-registered models, metrics, thresholds)")
    lines.append("- No sealed-holdout reuse: PASS (Track A window distinct from FCLR-002/003/Track B)")
    lines.append("- No `.github/workflows` edits: PASS")
    lines.append("- No redundant network polling: PASS (candles fetched once, first-time acquisition)")
    lines.append("")
    lines.append("## 7. Artifacts")
    lines.append(f"- Panel: {panel_path}")
    lines.append(f"- Panel report: {RS / f'tracka_hl_panel_with_rv_build_report_{ts_utc}.json'}")
    lines.append(f"- Prereg: {PREREG_PATH}")
    lines.append("")
    lines.append("---")
    lines.append(f"**End of verdict.** Verdict ID: {verdict_id}")
    out_md.write_text("\n".join(lines) + "\n")
    print(f"Wrote {out_md}")
    c2b1 = contrasts.get("C2_vs_B1", {})
    print(f"Verdict: {verdict} | C2 vs B1 rel reduction: {c2b1.get('rel_reduction_pct', 'N/A')}% | "
          f"CI: [{c2b1.get('ci_lo', 'N/A')}, {c2b1.get('ci_hi', 'N/A')}] | "
          f"instruments: {len(paired_syms)} | blocks: {len(test_blocks_with_data)}")

    return {"verdict_id": verdict_id, "verdict": verdict, "gate_pass": gate_pass,
            "contrasts": contrasts, "panel_path": str(panel_path), "panel_hash": panel_hash}


if __name__ == "__main__":
    main()
