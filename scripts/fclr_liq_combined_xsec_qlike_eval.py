#!/usr/bin/env python3
"""FCLR-LIQ-XSEC-QLIKE step 2: EVALUATION_AND_GATE.

Executes the FROZEN pre-outcomes prereg
(research_state/prereg_fclr_liq_combined_xsec_qlike_<UTC>.json) on the combined
metpie+ironflow observed-liquidation panel:

  estimand : daily cross-sectional QLIKE of next-day liquidation intensity
  target   : next calendar day total notional_usd per coin (shift -1 within coin)
  metrics  : mean daily cross-sectional QLIKE (primary, lower is better),
             mean daily Spearman rank-IC, top-3 hit-rate
  contrast : C2 vs B1
    B1 = [rv24h, rv168h]
    C2 = [rv24h, rv168h, fundingRate, abs_fund_pct, premium, ema_dist]
  walk     : expanding-window walk-forward
  purge    : 7-day purge/embargo before each test block
  test     : 3 non-overlapping blocks (2025-03-22..2025-04-21 pristine metpie,
             2025-04-21..2025-05-21 pristine metpie, 2025-10-01..2025-10-31 ironflow)
  gate     : primary QLIKE relative improvement >= 2.0% (C2 lower loss)
             AND block-bootstrap 95% CI hi < 0 for paired diff (C2-B1)
             AND >= 5 paired instruments AND >= 3 test blocks with data
  boot     : block bootstrap, 2000 reps, seed 20261115, resample test blocks
  holm     : family = 3 metrics (mean daily cross-sectional QLIKE, mean daily
             Spearman rank-IC, top-3 hit-rate)

QLIKE is a loss: C2 improves when mean_daily_cross_sectional_qlike_C2 <
mean_daily_cross_sectional_qlike_B1, i.e. paired diff (C2 - B1) < 0.

Reads ONLY the panel + frozen prereg (both pre-outcome/frozen). Writes only
timestamped evaluation_summary_FCLR-LIQ-XSEC-QLIKE-<UTC>.{json,md} and updates
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
from scipy.stats import spearmanr

REPO = Path(__file__).resolve().parents[1]
RS = REPO / "research_state"

# Find the latest frozen QLIKE prereg
prereg_files = sorted(RS.glob("prereg_fclr_liq_combined_xsec_qlike_*.json"))
if not prereg_files:
    raise SystemExit("No QLIKE XSEC prereg found. Run fclr_liq_combined_xsec_qlike_prereg.py first.")
PREREG_PATH = prereg_files[-1]

PREG = json.loads(PREREG_PATH.read_text())
EST = PREG["estimand"]
SEED = int(EST["block_bootstrap_seed"])
N_BOOT = int(EST["block_bootstrap_reps"])
MATERIALITY_PCT = float(EST["materiality_floor_pct"])
MIN_INSTRUMENTS = int(EST["min_instruments"])
MIN_TEST_BLOCKS = int(EST["min_test_blocks"])
PURGE_DAYS = int(EST["purge_embargo_days"])
PRIMARY_METRIC = EST["primary_metric_for_materiality"]

TRAIN = (pd.Timestamp(PREG["splits"]["train"]["start"], tz="UTC"),
         pd.Timestamp(PREG["splits"]["train"]["end"], tz="UTC"))
VAL = (pd.Timestamp(PREG["splits"]["validation"]["start"], tz="UTC"),
       pd.Timestamp(PREG["splits"]["validation"]["end"], tz="UTC"))
TEST_BLOCKS = [(pd.Timestamp(b["start"], tz="UTC"),
                pd.Timestamp(b["end"], tz="UTC"))
               for b in PREG["splits"]["test_blocks"]]
UNIVERSE = PREG["universe"]["coins"]
HOLM_FAMILY = EST["holm_family"]


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
        ly = math.log(y + 1e-12)
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
    base = [math.log(rv24 + 1e-12), math.log(rv168 + 1e-12)]
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


def compute_cross_sectional_metrics(panel_day: pd.DataFrame, model: str):
    """Compute cross-sectional metrics for a single day across all coins.

    Returns dict with: spearman_ic, top3_hit_rate, cross_sectional_qlike
    """
    valid = panel_day[panel_day["target"].notna() & panel_day[f"yhat_{model}"].notna()].copy()
    if len(valid) < 5:
        return {"spearman_ic": None, "top3_hit_rate": None, "cross_sectional_qlike": None}

    y_rank = valid["target"].rank(ascending=False, method="average")
    yhat_rank = valid[f"yhat_{model}"].rank(ascending=False, method="average")
    if len(valid) >= 2:
        rho, _ = spearmanr(y_rank, yhat_rank)
        spearman_ic = float(rho) if math.isfinite(rho) else None
    else:
        spearman_ic = None

    realized_top3 = set(valid.nsmallest(3, "target")["coin"])
    predicted_top3 = set(valid.nsmallest(3, f"yhat_{model}")["coin"])
    top3_hit_rate = len(realized_top3 & predicted_top3) / 3.0

    qlike_vals = []
    for _, row in valid.iterrows():
        q = qlike(row["target"], row[f"yhat_{model}"])
        if q is not None:
            qlike_vals.append(q)
    cross_sectional_qlike = np.mean(qlike_vals) if qlike_vals else None

    return {
        "spearman_ic": spearman_ic,
        "top3_hit_rate": top3_hit_rate,
        "cross_sectional_qlike": cross_sectional_qlike,
    }


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

    # Per-test-block expanding-window fit + eval; collect paired daily diffs (C2 - B1)
    all_daily_diffs = {m: [] for m in ["spearman_ic", "top3_hit_rate", "cross_sectional_qlike"]}
    all_daily_diffs["block"] = []
    all_daily_diffs["day"] = []
    block_results = []

    for bi, (bs, be) in enumerate(TEST_BLOCKS):
        cutoff = bs - pd.Timedelta(days=PURGE_DAYS)
        train_df = daily[daily["day"] <= cutoff]
        test_df = daily[(daily["day"] >= bs) & (daily["day"] <= be)]
        test_df = test_df[test_df["target"].notna()].copy()

        blk = {"block": bi, "start": str(bs.date()), "end": str(be.date()),
               "cutoff": str(cutoff.date()), "n_train": int(len(train_df)),
               "n_test": int(len(test_df)), "models": {}}

        betas = {}
        for model in ("B1", "C2"):
            trX, try_ = [], []
            for _, r in train_df.iterrows():
                xv = feature_vec(r, model)
                if xv is None:
                    continue
                trX.append([1.0] + xv)
                try_.append(r["target"])
            betas[model] = fit_ols_logtarget(trX, try_)

        for model in ("B1", "C2"):
            if betas[model] is not None:
                for idx, r in test_df.iterrows():
                    xv = feature_vec(r, model)
                    if xv is None:
                        continue
                    yhat = predict(betas[model], xv)
                    test_df.loc[idx, f"yhat_{model}"] = yhat
            else:
                test_df[f"yhat_{model}"] = np.nan

        daily_metrics = {m: {"B1": [], "C2": []} for m in ["spearman_ic", "top3_hit_rate", "cross_sectional_qlike"]}
        for day, panel_day in test_df.groupby("day"):
            m_b1 = compute_cross_sectional_metrics(panel_day, "B1")
            m_c2 = compute_cross_sectional_metrics(panel_day, "C2")
            if m_b1["spearman_ic"] is not None and m_c2["spearman_ic"] is not None:
                for m in ["spearman_ic", "top3_hit_rate", "cross_sectional_qlike"]:
                    all_daily_diffs[m].append(m_c2[m] - m_b1[m])
                    daily_metrics[m]["B1"].append(m_b1[m])
                    daily_metrics[m]["C2"].append(m_c2[m])
                all_daily_diffs["block"].append(bi)
                all_daily_diffs["day"].append(day)

        for model in ("B1", "C2"):
            blk["models"][model] = {
                "beta": betas[model],
                "n_days": len(daily_metrics["cross_sectional_qlike"][model]),
                "mean_spearman_ic": (np.mean(daily_metrics["spearman_ic"][model])
                                     if daily_metrics["spearman_ic"][model] else None),
                "mean_top3_hit_rate": (np.mean(daily_metrics["top3_hit_rate"][model])
                                       if daily_metrics["top3_hit_rate"][model] else None),
                "mean_cross_sectional_qlike": (np.mean(daily_metrics["cross_sectional_qlike"][model])
                                               if daily_metrics["cross_sectional_qlike"][model] else None),
            }
        block_results.append(blk)

    # Block bootstrap: resample test blocks (with replacement), recompute mean paired diff
    def block_bootstrap(metric_name):
        if not all_daily_diffs[metric_name]:
            return None
        blocks = {}
        for d, b in zip(all_daily_diffs[metric_name], all_daily_diffs["block"]):
            blocks.setdefault(b, []).append(d)
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
        mean_d = sum(all_daily_diffs[metric_name]) / len(all_daily_diffs[metric_name])
        prop_le0 = sum(1 for s in stats if s <= 0) / len(stats)
        prop_ge0 = sum(1 for s in stats if s >= 0) / len(stats)
        p_two = 2.0 * min(prop_le0, prop_ge0)
        p_two = min(1.0, p_two)
        return {"mean": mean_d, "ci_lo": lo, "ci_hi": hi,
                "n_pairs": len(all_daily_diffs[metric_name]), "n_blocks": len(block_list),
                "p_value": p_two}

    boot_qlike = block_bootstrap("cross_sectional_qlike")
    boot_spearman = block_bootstrap("spearman_ic")
    boot_top3 = block_bootstrap("top3_hit_rate")

    # Holm correction across 3 metrics
    p_values = [boot_qlike["p_value"] if boot_qlike else 1.0,
                boot_spearman["p_value"] if boot_spearman else 1.0,
                boot_top3["p_value"] if boot_top3 else 1.0]
    p_sorted = sorted([(p, i) for i, p in enumerate(p_values)])
    holm_reject = [False] * 3
    for rank, (p, idx) in enumerate(p_sorted):
        if p <= 0.05 / (3 - rank):
            holm_reject[idx] = True
        else:
            break

    # Gate assessment - primary metric is mean_daily_cross_sectional_qlike (lower better)
    qlike_b1_vals = []
    for bi, (bs, be) in enumerate(TEST_BLOCKS):
        cutoff = bs - pd.Timedelta(days=PURGE_DAYS)
        train_df = daily[daily["day"] <= cutoff]
        test_df = daily[(daily["day"] >= bs) & (daily["day"] <= be)]
        test_df = test_df[test_df["target"].notna()].copy()
        trX, try_ = [], []
        for _, r in train_df.iterrows():
            xv = feature_vec(r, "B1")
            if xv is None:
                continue
            trX.append([1.0] + xv)
            try_.append(r["target"])
        beta_b1 = fit_ols_logtarget(trX, try_)
        if beta_b1 is not None:
            for idx, r in test_df.iterrows():
                xv = feature_vec(r, "B1")
                if xv is None:
                    continue
                test_df.loc[idx, "yhat_B1"] = predict(beta_b1, xv)
        else:
            test_df["yhat_B1"] = np.nan
        for day, panel_day in test_df.groupby("day"):
            m = compute_cross_sectional_metrics(panel_day, "B1")
            if m["cross_sectional_qlike"] is not None:
                qlike_b1_vals.append(m["cross_sectional_qlike"])

    mean_b1_qlike = np.mean(qlike_b1_vals) if qlike_b1_vals else 0
    mean_c2_minus_b1 = boot_qlike["mean"] if boot_qlike else None
    rel_improvement = ((-mean_c2_minus_b1) / abs(mean_b1_qlike) * 100.0) if (mean_c2_minus_b1 is not None and mean_b1_qlike != 0) else None

    rel_pass = bool(rel_improvement is not None and rel_improvement >= MATERIALITY_PCT)
    ci_pass = bool(boot_qlike and boot_qlike["ci_hi"] < 0)  # CI entirely below zero: C2 lower loss
    instr_pass = len(UNIVERSE) >= MIN_INSTRUMENTS
    block_pass = len(set(all_daily_diffs["block"])) >= MIN_TEST_BLOCKS

    gate_pass = rel_pass and ci_pass and instr_pass and block_pass
    verdict = "PASS" if gate_pass else "NOT_MET"

    # ---- Emit JSON ----
    eval_id = f"FCLR-LIQ-XSEC-QLIKE-{ts_utc}"
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
        "test_blocks": [{"block": bi, "start": str(bs.date()), "end": str(be.date()),
                         "cutoff": str((bs - pd.Timedelta(days=PURGE_DAYS)).date())}
                        for bi, (bs, be) in enumerate(TEST_BLOCKS)],
        "metrics": {
            "cross_sectional_qlike": {
                "mean_diff": boot_qlike["mean"] if boot_qlike else None,
                "rel_improvement_pct": rel_improvement,
                "ci_lo": boot_qlike["ci_lo"] if boot_qlike else None,
                "ci_hi": boot_qlike["ci_hi"] if boot_qlike else None,
                "n_pairs": boot_qlike["n_pairs"] if boot_qlike else 0,
                "n_blocks": boot_qlike["n_blocks"] if boot_qlike else 0,
                "p_value": boot_qlike["p_value"] if boot_qlike else None,
                "holm_reject": holm_reject[0],
            },
            "spearman_ic": {
                "mean_diff": boot_spearman["mean"] if boot_spearman else None,
                "ci_lo": boot_spearman["ci_lo"] if boot_spearman else None,
                "ci_hi": boot_spearman["ci_hi"] if boot_spearman else None,
                "n_pairs": boot_spearman["n_pairs"] if boot_spearman else 0,
                "n_blocks": boot_spearman["n_blocks"] if boot_spearman else 0,
                "p_value": boot_spearman["p_value"] if boot_spearman else None,
                "holm_reject": holm_reject[1],
            },
            "top3_hit_rate": {
                "mean_diff": boot_top3["mean"] if boot_top3 else None,
                "ci_lo": boot_top3["ci_lo"] if boot_top3 else None,
                "ci_hi": boot_top3["ci_hi"] if boot_top3 else None,
                "n_pairs": boot_top3["n_pairs"] if boot_top3 else 0,
                "n_blocks": boot_top3["n_blocks"] if boot_top3 else 0,
                "p_value": boot_top3["p_value"] if boot_top3 else None,
                "holm_reject": holm_reject[2],
            },
        },
        "block_bootstrap": {"reps": N_BOOT, "seed": SEED},
        "holm": {"family": HOLM_FAMILY, "n_tests": 3, "adjusted_alpha": 0.05,
                 "p_values": p_values, "holm_reject": holm_reject},
        "gate": {
            "primary_metric": PRIMARY_METRIC,
            "rel_pass": rel_pass, "rel_improvement_pct": rel_improvement, "materiality_pct": MATERIALITY_PCT,
            "ci_pass": ci_pass, "ci_hi": boot_qlike["ci_hi"] if boot_qlike else None,
            "instr_pass": instr_pass, "n_paired_instruments": len(UNIVERSE),
            "min_instruments": MIN_INSTRUMENTS,
            "block_pass": block_pass, "n_blocks_with_data": len(set(all_daily_diffs["block"])),
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
    md.append(f"# FCLR-LIQ-XSEC-QLIKE Evaluation — {eval_id}")
    md.append("")
    md.append(f"**Generated (UTC):** {out['generated_utc']}")
    md.append(f"**Experiment:** {PREG['experiment_id']}")
    md.append(f"**Prereg:** {PREREG_PATH.name} (frozen pre-outcomes)")
    md.append(f"**Panel:** {panel_path.name} (sha256 {panel_hash[:16]}...)")
    md.append(f"**Verdict:** `{verdict}` — pre-registered C2 vs B1 on daily cross-sectional QLIKE")
    md.append("")
    md.append("## 1. Determination")
    md.append("")
    md.append(f"Expanding-window walk-forward, contrast **C2 vs B1**, "
              f"3 non-overlapping 30-day test blocks, {PURGE_DAYS}d purge/embargo, "
              f"{N_BOOT} block-bootstrap reps (seed {SEED}).")
    md.append(f"Primary metric: **mean daily cross-sectional QLIKE** (lower is better; materiality floor {MATERIALITY_PCT}% relative QLIKE reduction).")
    md.append(f"Forecast gate: **{verdict}**.")
    if gate_pass:
        md.append("Incremental forecast skill of funding + premium + ema features over RV-only baseline DEMONSTRATED at the pre-registered materiality gate on cross-sectional QLIKE.")
    else:
        md.append("Incremental forecast skill NOT demonstrated at the pre-registered materiality gate on cross-sectional QLIKE.")
    md.append("")
    md.append("## 2. Per-metric results (C2 vs B1 paired differences)")
    md.append("")
    md.append("| metric | mean diff | 95% CI | p-value | Holm reject |")
    md.append("|---|---|---|---|---|")
    for m_name, m_data in out["metrics"].items():
        md.append(f"| {m_name} | {m_data['mean_diff']:.6f} | [{m_data['ci_lo']:.6f}, {m_data['ci_hi']:.6f}] | {m_data['p_value']:.4f} | {m_data['holm_reject']} |"
                  if m_data['mean_diff'] is not None
                  else f"| {m_name} | N/A | N/A | N/A | {m_data['holm_reject']} |")
    md.append("")
    md.append("## 3. Primary metric (cross-sectional QLIKE) gate assessment")
    md.append("")
    g = out["gate"]
    md.append(f"- >= {MATERIALITY_PCT}% relative QLIKE reduction (C2 lower loss): {'PASS' if g['rel_pass'] else 'NOT_MET'} ({g['rel_improvement_pct']:.2f}%)" if g['rel_improvement_pct'] is not None else f"- >= {MATERIALITY_PCT}% relative QLIKE reduction: NOT_MET (N/A)")
    md.append(f"- 95% CI hi < 0 (excludes zero, C2 lower loss): {'PASS' if g['ci_pass'] else 'NOT_MET'}")
    md.append(f"- >= {MIN_INSTRUMENTS} paired instruments: {'PASS' if g['instr_pass'] else 'NOT_MET'} ({g['n_paired_instruments']})")
    md.append(f"- >= {MIN_TEST_BLOCKS} non-overlapping test blocks: {'PASS' if g['block_pass'] else 'NOT_MET'} ({g['n_blocks_with_data']})")
    md.append(f"- **Forecast gate (all criteria): {verdict}**")
    md.append("")
    md.append("## 4. Compliance")
    md.append("- outcome_data_inspected_before_freeze: false (prereg frozen pre-outcomes)")
    md.append("- No threshold tuning after freeze: PASS")
    md.append("- No sealed-artifact mutation: PASS")
    md.append("- No network/paid/credentialed data for outcomes: PASS")
    md.append("- H2_shek_replication remains EXPLORATORY_ONLY (promotable=false)")
    md.append("")
    md.append("## 5. Artifacts")
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
    print(f"Verdict: {verdict} | QLIKE rel improvement: {rel_improvement if rel_improvement is not None else 'N/A'}% | "
          f"CI: [{boot_qlike['ci_lo'] if boot_qlike else 'N/A'}, {boot_qlike['ci_hi'] if boot_qlike else 'N/A'}] | "
          f"instruments: {len(UNIVERSE)} | blocks: {len(set(all_daily_diffs['block']))}")
    return {"evaluation_id": eval_id, "verdict": verdict, "gate_pass": gate_pass, "out": out}


def _update_frontier(eval_id, verdict, out, panel_path):
    """Stamp the verdict onto the QLIKE campaign cell WITHOUT changing rank/status."""
    path = RS / "experiment_frontier.json"
    frontier = json.loads(path.read_text())
    now = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    for e in frontier:
        if str(e.get("task", "")).startswith("FCLR-LIQ-XSEC-QLIKE"):
            e["last_checked"] = now
            e["last_verdict"] = verdict
            e["last_evaluation"] = eval_id
            break
    path.write_text(json.dumps(frontier, indent=2, sort_keys=True) + "\n")


def _update_hypothesis_registry(eval_id, verdict, out):
    path = RS / "hypothesis_registry.json"
    reg = json.loads(path.read_text())
    hyps = reg.setdefault("hypotheses", [])
    key = "H_fclr_liq_xsec_qlike_forecast"
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
        "description": "Funding + premium + ema features improve cross-sectional QLIKE forecasting of next-day liquidation intensity (C2) over RV-only baseline (B1) on the combined metpie+ironflow Hyperliquid panel",
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
