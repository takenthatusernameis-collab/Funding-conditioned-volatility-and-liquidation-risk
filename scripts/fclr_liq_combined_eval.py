#!/usr/bin/env python3
"""FCLR-LIQ-COMBINED-PANEL step 5: EVALUATION_AND_GATE.

Executes the FROZEN pre-outcomes prereg
(research_state/prereg_fclr_liq_combined_20261115T181449Z.json) on the combined
metpie+ironflow observed-liquidation panel:

  estimand : 24h observed-liquidation intensity = daily total notional_usd
  target   : next calendar day total (shift -1 within coin)
  loss     : QLIKE
  contrast : C2 vs B1
    B1 = [rv24h, rv168h]
    C2 = [rv24h, rv168h, fundingRate, abs_fund_pct, premium, ema_dist]
  walk     : expanding-window walk-forward
  purge    : 7-day purge/embargo before each test block
  test     : 3 non-overlapping blocks (2025-10, 2026-01, 2026-09)
  gate     : relative QLIKE reduction >= 2.0% AND block-bootstrap 95% CI hi < 0
             AND >= 5 paired instruments AND >= 3 test blocks with data
  boot     : block bootstrap, 2000 reps, seed 20261115, resample test blocks
  holm     : family = [C2_vs_B1] (single primary; Holm trivial)

Reads ONLY the panel + frozen prereg (both pre-outcome/frozen). Writes only
timestamped evaluation_summary_FCLR-LIQ-COMBINED-<UTC>.{json,md} and updates
experiment_frontier.json + hypothesis_registry.json (non-sealed research state).
Never mutates sealed artifacts or .github/workflows. No network.
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

PREREG_PATH = RS / "prereg_fclr_liq_combined_20261115T181449Z.json"
SEED = 20261115
N_BOOT = 2000
EPS = 1e-12

PREG = json.loads(PREREG_PATH.read_text())
EST = PREG["estimand"]
MATERIALITY_PCT = float(EST["materiality_floor_pct"])
MIN_INSTRUMENTS = int(EST["min_instruments"])
MIN_TEST_BLOCKS = int(EST["min_test_blocks"])
PURGE_DAYS = int(EST["purge_embargo_days"])

TRAIN = (pd.Timestamp(PREG["splits"]["train"]["start"], tz="UTC"),
         pd.Timestamp(PREG["splits"]["train"]["end"], tz="UTC"))
VAL = (pd.Timestamp(PREG["splits"]["validation"]["start"], tz="UTC"),
       pd.Timestamp(PREG["splits"]["validation"]["end"], tz="UTC"))
TEST_BLOCKS = [(pd.Timestamp(b["start"], tz="UTC"),
                pd.Timestamp(b["end"], tz="UTC"))
               for b in PREG["splits"]["test_blocks"]]
UNIVERSE = PREG["universe"]["coins"]


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def qlike(y: float, yhat: float):
    if yhat is None or yhat <= 0 or y is None or y <= 0:
        return None
    if not (math.isfinite(y) and math.isfinite(yhat)):
        return None
    ratio = y / yhat
    return ratio - math.log(ratio) - 1.0


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


def fit_ols_logtarget(X_list, y_list):
    """OLS of log(y) on X (X already includes intercept column)."""
    rows = [(X, y) for X, y in zip(X_list, y_list)
            if X is not None and y is not None and y > 0
            and all(v is not None and math.isfinite(v) for v in X)]
    if len(rows) < 30:
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
        XtX[i][i] += 1e-8
    return _solve_linear(XtX, Xty)


def predict(beta, X):
    if beta is None or X is None or any(v is None or not math.isfinite(v) for v in X):
        return None
    s = beta[0]
    for i in range(1, len(beta)):
        s += beta[i] * X[i - 1]
    if s > 700:
        return None
    yhat = math.exp(s)
    return yhat if yhat > 0 else None


def feature_vec(row, model):
    """Causal feature vector at the daily grain. Returns None if incomplete."""
    rv24 = row["rv24h"]
    rv168 = row["rv168h"]
    if pd.isna(rv24) or pd.isna(rv168) or rv24 <= 0 or rv168 <= 0:
        return None
    base = [math.log(rv24 + EPS), math.log(rv168 + EPS)]
    if model == "B1":
        return base
    vals = {"fundingRate": row["fundingRate"], "abs_fund_pct": row["abs_fund_pct"],
            "premium": row["premium"], "ema_dist": row["ema_dist"]}
    for v in vals.values():
        if v is None or pd.isna(v) or not math.isfinite(v):
            return None
    return base + [float(vals["fundingRate"]), float(vals["abs_fund_pct"]),
                   float(vals["premium"]), float(vals["ema_dist"])]


def build_daily(panel_path: Path) -> pd.DataFrame:
    df = pd.read_parquet(panel_path)
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    df = df[df["coin"].isin(UNIVERSE)].copy()
    df["day"] = df["timestamp"].dt.floor("D")
    daily = (df.groupby(["coin", "day"], as_index=False)
               .agg(y=("notional_usd", "sum"),
                    rv24h=("rv24h", "last"),
                    rv168h=("rv168h", "last"),
                    fundingRate=("fundingRate", "last"),
                    abs_fund_pct=("abs_fund_pct", "last"),
                    premium=("premium", "last"),
                    ema_dist=("ema_dist", "last")))
    daily = daily.sort_values(["coin", "day"]).reset_index(drop=True)
    daily["target"] = daily.groupby("coin")["y"].shift(-1)
    daily["target_day"] = daily.groupby("coin")["day"].shift(-1)
    return daily


def test_block_index(day: pd.Timestamp) -> int:
    for i, (s, e) in enumerate(TEST_BLOCKS):
        if s <= day <= e:
            return i
    return -1


def main() -> dict:
    ts_utc = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    panel_files = sorted(RS.glob("fclr_liq_combined_panel_*.parquet"))
    if not panel_files:
        raise SystemExit("No combined panel found. Run fclr_build_liq_combined_panel.py first.")
    panel_path = panel_files[-1]
    panel_hash = sha256_file(panel_path)

    daily = build_daily(panel_path)
    daily = daily[daily["target"].notna()].reset_index(drop=True)
    print(f"Daily rows with target: {len(daily)}", flush=True)

    # Per-test-block expanding-window fit + eval
    block_results = []  # list of dicts per test block
    pooled = {"B1": [], "C2": []}

    for bi, (bs, be) in enumerate(TEST_BLOCKS):
        cutoff = bs - pd.Timedelta(days=PURGE_DAYS)  # purge/embargo
        train_df = daily[daily["day"] <= cutoff]
        test_df = daily[(daily["day"] >= bs) & (daily["day"] <= be)]
        # test_df must have a target (next day exists)
        test_df = test_df[test_df["target"].notna()]

        blk = {"block": bi, "start": str(bs.date()), "end": str(be.date()),
               "cutoff": str(cutoff.date()), "n_train": int(len(train_df)),
               "n_test": int(len(test_df)), "models": {}}
        for model in ("B1", "C2"):
            trX, try_ = [], []
            for _, r in train_df.iterrows():
                xv = feature_vec(r, model)
                if xv is None:
                    continue
                trX.append([1.0] + xv)
                try_.append(r["target"])
            beta = fit_ols_logtarget(trX, try_)
            preds = []
            if beta is not None:
                for _, r in test_df.iterrows():
                    xv = feature_vec(r, model)
                    if xv is None:
                        continue
                    yhat = predict(beta, xv)
                    y = r["target"]
                    q = qlike(y, yhat)
                    if q is None:
                        continue
                    preds.append({"sym": r["coin"], "ts_ms": int(r["day"].timestamp() * 1000),
                                  "qlike": q, "y": float(y), "yhat": float(yhat)})
            blk["models"][model] = {"beta": beta, "preds": preds,
                                    "mean_qlike": (sum(p["qlike"] for p in preds) / len(preds)) if preds else None,
                                    "n": len(preds)}
            pooled[model].extend(preds)
        block_results.append(blk)

    # Pooled paired diffs C2 - B1
    b1_by_key = {(p["sym"], p["ts_ms"]): p["qlike"] for p in pooled["B1"]}
    diffs = []  # (ts_ms, block, diff)
    for p in pooled["C2"]:
        k = (p["sym"], p["ts_ms"])
        if k in b1_by_key:
            # find block
            bidx = -1
            ts = pd.Timestamp(p["ts_ms"], unit="ms", tz="UTC")
            bidx = test_block_index(ts)
            diffs.append((p["ts_ms"], bidx, p["qlike"] - b1_by_key[k]))

    def block_bootstrap(diffs):
        if not diffs:
            return None
        blocks = {}
        for ts_ms, bidx, d in diffs:
            blocks.setdefault(bidx, []).append(d)
        block_list = list(blocks.values())
        rng = random.Random(SEED)
        stats = []
        for _ in range(N_BOOT):
            samp = []
            for _ in range(len(block_list)):
                samp.extend(rng.choice(block_list))
            if samp:
                stats.append(sum(samp) / len(samp))
        stats.sort()
        lo = stats[int(0.025 * len(stats))]
        hi = stats[int(0.975 * len(stats))]
        mean_d = sum(d for _, _, d in diffs) / len(diffs)
        # bootstrap two-sided p-value for mean diff < 0 (favorable = C2 better)
        prop_le0 = sum(1 for s in stats if s <= 0) / len(stats)
        prop_ge0 = sum(1 for s in stats if s >= 0) / len(stats)
        p_two = 2.0 * min(prop_le0, prop_ge0)
        p_two = min(1.0, p_two)
        return {"mean": mean_d, "ci_lo": lo, "ci_hi": hi,
                "n_pairs": len(diffs), "n_blocks": len(block_list),
                "p_value": p_two}

    boot = block_bootstrap(diffs)
    b1_mean = (sum(p["qlike"] for p in pooled["B1"]) / len(pooled["B1"])) if pooled["B1"] else None
    rel = (-boot["mean"] / abs(b1_mean) * 100.0) if (boot and b1_mean) else None

    # Holm (single-member family)
    holm = {"family": EST["holm_family"], "n_tests": 1, "adjusted_alpha": 0.05,
            "p_value": boot["p_value"] if boot else None,
            "holm_reject": bool(boot and boot["p_value"] is not None and boot["p_value"] <= 0.05)}

    # Gate
    paired_syms = sorted({p["sym"] for p in pooled["C2"] if (p["sym"], p["ts_ms"]) in b1_by_key})
    blocks_with_data = sorted({b for _, b, _ in diffs if b >= 0})
    instr_pass = len(paired_syms) >= MIN_INSTRUMENTS
    block_pass = len(blocks_with_data) >= MIN_TEST_BLOCKS
    rel_pass = bool(rel is not None and rel >= MATERIALITY_PCT)
    ci_pass = bool(boot and boot["ci_hi"] < 0)
    gate_pass = rel_pass and ci_pass and instr_pass and block_pass
    verdict = "PASS" if gate_pass else "NOT_MET"

    # ---- Emit JSON ----
    eval_id = f"FCLR-LIQ-COMBINED-{ts_utc}"
    out = {
        "evaluation_id": eval_id,
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "experiment_id": PREG["experiment_id"],
        "prereg": PREREG_PATH.name,
        "prereg_sha256": sha256_file(PREREG_PATH),
        "panel": panel_path.name,
        "panel_sha256": panel_hash,
        "n_daily_rows": int(len(daily)),
        "n_universe": len(UNIVERSE),
        "contrast": "C2_vs_B1",
        "models": {"B1": PREG["features"]["B1"], "C2": PREG["features"]["C2"]},
        "test_blocks": [{"block": b["block"], "start": b["start"], "end": b["end"],
                         "cutoff": b["cutoff"], "n_train": b["n_train"], "n_test": b["n_test"],
                         "B1_mean_qlike": b["models"]["B1"]["mean_qlike"],
                         "B1_n": b["models"]["B1"]["n"],
                         "C2_mean_qlike": b["models"]["C2"]["mean_qlike"],
                         "C2_n": b["models"]["C2"]["n"]} for b in block_results],
        "pooled": {
            "B1_mean_qlike": b1_mean,
            "C2_mean_qlike": (sum(p["qlike"] for p in pooled["C2"]) / len(pooled["C2"])) if pooled["C2"] else None,
            "B1_n": len(pooled["B1"]),
            "C2_n": len(pooled["C2"]),
        },
        "contrast_C2_vs_B1": {
            "mean_diff": boot["mean"] if boot else None,
            "rel_reduction_pct": rel,
            "ci_lo": boot["ci_lo"] if boot else None,
            "ci_hi": boot["ci_hi"] if boot else None,
            "n_pairs": boot["n_pairs"] if boot else 0,
            "n_blocks": boot["n_blocks"] if boot else 0,
            "p_value": boot["p_value"] if boot else None,
            "block_bootstrap_reps": N_BOOT,
            "seed": SEED,
        },
        "holm": holm,
        "gate": {
            "rel_pass": rel_pass, "rel_reduction_pct": rel, "materiality_pct": MATERIALITY_PCT,
            "ci_pass": ci_pass, "ci_hi": boot["ci_hi"] if boot else None,
            "instr_pass": instr_pass, "n_paired_instruments": len(paired_syms),
            "min_instruments": MIN_INSTRUMENTS,
            "block_pass": block_pass, "n_blocks_with_data": len(blocks_with_data),
            "min_blocks": MIN_TEST_BLOCKS,
            "verdict": verdict,
        },
        "compliance": {
            "outcome_data_inspected_before_freeze": False,
            "no_threshold_tuning": True,
            "no_sealed_artifact_mutation": True,
            "no_network_for_outcomes": True,
            "no_paid_or_credentialed_data": True,
            "purge_embargo_days": PURGE_DAYS,
        },
    }
    out_json = RS / f"evaluation_summary_{eval_id}.json"
    out_json.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")

    # ---- Emit MD ----
    md = []
    md.append(f"# FCLR-LIQ-COMBINED Evaluation — {eval_id}")
    md.append("")
    md.append(f"**Generated (UTC):** {out['generated_utc']}")
    md.append(f"**Experiment:** {PREG['experiment_id']}")
    md.append(f"**Prereg:** {PREREG_PATH.name} (frozen pre-outcomes)")
    md.append(f"**Panel:** {panel_path.name} (sha256 {panel_hash[:16]}...)")
    md.append(f"**Verdict:** `{verdict}` — pre-registered C2 vs B1 on 24h observed liquidation intensity")
    md.append("")
    md.append("## 1. Determination")
    md.append("")
    md.append(f"Expanding-window walk-forward QLIKE, contrast **C2 vs B1**, "
              f"3 non-overlapping 30-day test blocks, {PURGE_DAYS}d purge/embargo, "
              f"{N_BOOT} block-bootstrap reps (seed {SEED}).")
    md.append(f"Forecast gate: **{verdict}**.")
    if gate_pass:
        md.append("Incremental forecast skill of funding + premium + ema features over RV-only baseline DEMONSTRATED at the pre-registered materiality gate.")
    else:
        md.append("Incremental forecast skill NOT demonstrated at the pre-registered materiality gate.")
    md.append("")
    md.append("## 2. Per-block QLIKE (lower is better)")
    md.append("")
    md.append("| block | window | n_train | n_test | B1 mean QLIKE | C2 mean QLIKE |")
    md.append("|---|---|---|---|---|---|")
    for b in block_results:
        b1m = b["models"]["B1"]["mean_qlike"]
        c2m = b["models"]["C2"]["mean_qlike"]
        md.append(f"| {b['block']} | {b['start']}..{b['end']} | {b['n_train']} | {b['n_test']} | "
                  f"{b1m:.6f} | {c2m:.6f} |" if b1m is not None and c2m is not None
                  else f"| {b['block']} | {b['start']}..{b['end']} | {b['n_train']} | {b['n_test']} | N/A | N/A |")
    md.append("")
    md.append("## 3. Pooled test-set QLIKE")
    md.append("")
    md.append(f"- B1 mean QLIKE: {out['pooled']['B1_mean_qlike']:.6f} (n={out['pooled']['B1_n']})" if out['pooled']['B1_mean_qlike'] is not None else "- B1: N/A")
    md.append(f"- C2 mean QLIKE: {out['pooled']['C2_mean_qlike']:.6f} (n={out['pooled']['C2_n']})" if out['pooled']['C2_mean_qlike'] is not None else "- C2: N/A")
    md.append("")
    md.append("## 4. Primary contrast C2 vs B1 (block bootstrap)")
    md.append("")
    c = out["contrast_C2_vs_B1"]
    md.append(f"- Paired n: {c['n_pairs']} across {c['n_blocks']} test block(s)")
    md.append(f"- Mean diff (C2 - B1) QLIKE: {c['mean_diff']:.6f}" if c['mean_diff'] is not None else "- Mean diff: N/A")
    if c['ci_lo'] is not None:
        md.append(f"- 95% CI: [{c['ci_lo']:.6f}, {c['ci_hi']:.6f}]")
    if c['rel_reduction_pct'] is not None:
        md.append(f"- Relative QLIKE reduction: {c['rel_reduction_pct']:.2f}%")
    if c['p_value'] is not None:
        md.append(f"- Bootstrap two-sided p: {c['p_value']:.4f} (Holm-adjusted, single-member family)")
    md.append("")
    md.append("## 5. Gate assessment")
    md.append("")
    g = out["gate"]
    md.append(f"- >= {MATERIALITY_PCT}% relative QLIKE reduction: {'PASS' if g['rel_pass'] else 'NOT_MET'} ({g['rel_reduction_pct']:.2f}%)" if g['rel_reduction_pct'] is not None else f"- >= {MATERIALITY_PCT}% relative QLIKE reduction: NOT_MET (N/A)")
    md.append(f"- 95% CI hi < 0 (excludes zero, C2 better): {'PASS' if g['ci_pass'] else 'NOT_MET'}")
    md.append(f"- >= {MIN_INSTRUMENTS} paired instruments: {'PASS' if g['instr_pass'] else 'NOT_MET'} ({g['n_paired_instruments']})")
    md.append(f"- >= {MIN_TEST_BLOCKS} non-overlapping test blocks: {'PASS' if g['block_pass'] else 'NOT_MET'} ({g['n_blocks_with_data']})")
    md.append(f"- **Forecast gate (all criteria): {verdict}**")
    md.append("")
    md.append("## 6. Compliance")
    md.append("- outcome_data_inspected_before_freeze: false (prereg frozen pre-outcomes)")
    md.append("- No threshold tuning after freeze: PASS")
    md.append("- No sealed-artifact mutation: PASS")
    md.append("- No network/paid/credentialed data for outcomes: PASS")
    md.append("- H2_shek_replication remains EXPLORATORY_ONLY (promotable=false)")
    md.append("")
    md.append("## 7. Artifacts")
    md.append(f"- Panel: {panel_path}")
    md.append(f"- Prereg: {PREREG_PATH}")
    md.append(f"- Eval JSON: {out_json}")
    md.append("")
    md.append("---")
    md.append(f"**End of verdict.** Evaluation ID: {eval_id}")
    out_md = RS / f"evaluation_summary_{eval_id}.md"
    out_md.write_text("\n".join(md) + "\n")

    # ---- Update frontier + hypothesis registry (non-sealed research state) ----
    _update_frontier(eval_id, verdict, out, panel_path)
    _update_hypothesis_registry(eval_id, verdict, out)

    print(f"Wrote {out_json}")
    print(f"Wrote {out_md}")
    print(f"Verdict: {verdict} | C2 vs B1 rel reduction: {rel if rel is not None else 'N/A'}% | "
          f"CI: [{c['ci_lo']}, {c['ci_hi']}] | instruments: {len(paired_syms)} | blocks: {len(blocks_with_data)}")
    return {"evaluation_id": eval_id, "verdict": verdict, "gate_pass": gate_pass, "out": out}


def _update_frontier(eval_id, verdict, out, panel_path):
    """Stamp the verdict onto the matching campaign cell WITHOUT changing rank/status.

    Rank/status transitions (demotion + installation of the next heavy cell) are a
    campaign-management concern handled by the durable handoff, not by the eval, so
    this never leaves rank-0 in a non-active state on its own.
    """
    path = RS / "experiment_frontier.json"
    frontier = json.loads(path.read_text())
    now = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    for e in frontier:
        if str(e.get("task", "")).startswith("FCLR-LIQ-COMBINED-PANEL"):
            e["last_checked"] = now
            e["last_verdict"] = verdict
            e["last_evaluation"] = eval_id
            break
    path.write_text(json.dumps(frontier, indent=2, sort_keys=True) + "\n")


def _update_hypothesis_registry(eval_id, verdict, out):
    path = RS / "hypothesis_registry.json"
    reg = json.loads(path.read_text())
    hyps = reg.setdefault("hypotheses", [])
    key = "H_fclr_liq_combined_panel_forecast"
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    entry = None
    if isinstance(hyps, list):
        for e in hyps:
            if isinstance(e, dict) and e.get("id") == key:
                entry = e
                break
    if entry is None:
        entry = {"id": key}
        if isinstance(hyps, list):
            hyps.append(entry)
        else:
            reg["hypotheses"] = [entry]
    entry.update({
        "id": key,
        "type": "confirmatory",
        "description": "Funding + premium + ema features improve OOS forecast of next-24h observed liquidation intensity (C2) over RV-only baseline (B1) on the combined metpie+ironflow Hyperliquid panel",
        "status": verdict,
        "class": "CONFIRMATORY",
        "promotable": False,
        "terminal": True,
        "terminal_class": verdict,
        "reopen_requires": ["NEW_OBSERVED_LIQUIDATION_SOURCE", "HL_LABEL_EXTENSION"],
        "last_verdict": verdict,
        "last_evaluation": eval_id,
        "last_tested": now,
        "estimand": EST["name"],
        "contrast": "C2_vs_B1",
        "experiment_id": PREG["experiment_id"],
        "updated_utc": now,
    })
    reg["updated_utc"] = now
    path.write_text(json.dumps(reg, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()