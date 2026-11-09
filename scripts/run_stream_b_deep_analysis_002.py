#!/usr/bin/env python3
"""STREAM_B_DEEP_ANALYSIS-002: Regime-stratified QLIKE by funding quartile per symbol on frozen FCLR-002 test splits.

Computes funding |.| quartiles from TRAIN period only (no look-ahead), stratifies TEST rows
per symbol per quartile (Q1 most negative .. Q4 most positive signed funding), and reports
per-symbol per-regime QLIKE for B1 vs C2_all with block-bootstrap CIs (2000 reps, deterministic seed).
Also reports interaction/ablation per regime: funding-feature incremental vs price-dislocation/EMA incremental.
Leakage-resistant: train-only thresholds/normalization, trailing-only features, chronological splits.
"""
from __future__ import annotations

import json
import math
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PANEL = REPO / "research_state" / "data_cache" / "fclr002_panel.json"
OUT = REPO / "research_state" / f"evaluation_summary_STREAM_B_DEEP_ANALYSIS-002_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.md"

from src.volatility import eval as veval
from src.volatility import feature_engineering as fe
from src.volatility import block_bootstrap as bb


def qlike_wrap(y, yhat):
    v = veval.qlike(y, yhat)
    return v if v is not None else float('nan')


def get_vals(rows, key):
    vals = []
    for r in rows:
        v = r.get(key)
        if v is not None and isinstance(v, (int, float)) and not (isinstance(v, float) and (math.isnan(v) or math.isinf(v))):
            vals.append(float(v))
    return vals


def build_all(rows, scalers):
    scaler_rv24, scaler_fund, scaler_fund_abs, scaler_fund_pct, scaler_fund_z, scaler_rv_ratio1, scaler_rv_ratio2, scaler_px = scalers
    res = defaultdict(lambda: ([], []))
    for r in rows:
        y = r.get("y")
        if y is None or y <= 0 or not isinstance(y, (int, float)):
            continue
        rv24 = r.get("rv24h")
        if rv24 is None or rv24 <= 0:
            continue
        rv24_n = scaler_rv24.transform([rv24])[0]
        fund_n = scaler_fund.transform([r.get("signed_funding") if r.get("signed_funding") is not None else 0.0])[0]
        fund_pct_n = scaler_fund_pct.transform([r.get("fund_pct_trail") if r.get("fund_pct_trail") is not None else 0.5])[0]
        fund_z_n = scaler_fund_z.transform([r.get("fund_z_trail") if r.get("fund_z_trail") is not None else 0.0])[0]
        rr1_n = scaler_rv_ratio1.transform([r.get("rv_ratio_24h_168h") if r.get("rv_ratio_24h_168h") is not None else 1.0])[0]
        rr2_n = scaler_rv_ratio2.transform([r.get("rv_ratio_6h_168h") if r.get("rv_ratio_6h_168h") is not None else 1.0])[0]
        px_n = scaler_px.transform([r.get("ema_dist") if r.get("ema_dist") is not None else 0.0])[0]
        px_e = r.get("prem")
        px_e_n = scaler_px.transform([px_e])[0] if isinstance(px_e, (int, float)) else px_n
        yf = float(y)
        rv24f = float(rv24)
        res['B1'][0].append(yf); res['B1'][1].append(rv24f)
        res['C1'][0].append(yf); res['C1'][1].append(rv24f * (1.0 + 0.05 * abs(fund_n)))
        res['A1_fundpctz'][0].append(yf); res['A1_fundpctz'][1].append(rv24f * (1.0 + 0.05 * abs(fund_n) + 0.03 * abs(fund_pct_n) + 0.02 * abs(fund_z_n)))
        res['A2_rvratios'][0].append(yf); res['A2_rvratios'][1].append(rv24f * (1.0 + 0.02 * (rr1_n - rr2_n)))
        res['A3_pricedisloc'][0].append(yf); res['A3_pricedisloc'][1].append(rv24f * (1.0 + 0.03 * abs(px_n) + 0.02 * abs(px_e_n)))
        res['A4_fund_rvrat'][0].append(yf); res['A4_fund_rvrat'][1].append(rv24f * (1.0 + 0.05 * abs(fund_n) + 0.02 * (rr1_n - rr2_n)))
        res['C2_all'][0].append(yf); res['C2_all'][1].append(rv24f * (1.0 + 0.05 * abs(fund_n) + 0.03 * abs(fund_pct_n) + 0.02 * abs(fund_z_n) + 0.02 * (rr1_n - rr2_n) + 0.03 * abs(px_n) + 0.02 * abs(px_e_n)))
        res['I1_fund_x_rvregime'][0].append(yf); res['I1_fund_x_rvregime'][1].append(rv24f * (1.0 + 0.05 * abs(fund_n) + 0.03 * abs(fund_pct_n) + 0.02 * abs(fund_z_n) + 0.01 * abs(fund_n) * max(0.0, rr1_n)))
        res['I2_fund_x_disloc'][0].append(yf); res['I2_fund_x_disloc'][1].append(rv24f * (1.0 + 0.05 * abs(fund_n) + 0.03 * abs(fund_pct_n) + 0.02 * abs(fund_z_n) + 0.02 * abs(fund_n) * abs(px_n)))
        res['I3_rv_x_disloc'][0].append(yf); res['I3_rv_x_disloc'][1].append(rv24f * (1.0 + 0.05 * abs(fund_n) + 0.03 * abs(fund_pct_n) + 0.02 * abs(fund_z_n) + 0.015 * (rr1_n - rr2_n) * abs(px_n)))
    return res


def bootstrap_ci(y, yh_base, yh_alt, block_size=24, reps=2000, seed=12345):
    d, cilo, cihi = bb.block_bootstrap_ci(y, yh_base, yh_alt, veval.qlike, block_size=block_size, num_reps=reps, seed=seed)
    return d, cilo, cihi


def main():
    if not PANEL.exists():
        raise SystemExit(f"Missing panel: {PANEL}")
    d = json.loads(PANEL.read_text())
    rows = d["rows"]
    splits = d["splits"]

    by_sym = defaultdict(list)
    for r in rows:
        by_sym[r["sym"]].append(r)
    for sym in by_sym:
        by_sym[sym] = sorted(by_sym[sym], key=lambda x: x["ts_ms"])

    # Build extended features (train-only trailing percentiles/z-scores)
    extended = []
    for sym, srows in by_sym.items():
        fund_hist = []
        rv1h_hist = []
        rv24h_hist = []
        rv168h_hist = []
        for i, r in enumerate(srows):
            rv1h = r.get("rv1h"); rv24h = r.get("rv24h"); rv168h = r.get("rv168h")
            fund = r.get("signed_funding")
            if fund is not None: fund_hist.append(fund)
            if rv1h is not None: rv1h_hist.append(rv1h)
            if rv24h is not None: rv24h_hist.append(rv24h)
            if rv168h is not None: rv168h_hist.append(rv168h)
            fext = dict(r)
            if fund is not None and fund_hist:
                fext["fund_pct_trail"] = fe.trailing_percentile(fund_hist[:-1] if len(fund_hist) > 1 else fund_hist, fund)
                fext["fund_z_trail"] = fe.trailing_zscore(fund_hist[:-1] if len(fund_hist) > 1 else fund_hist, fund)
            else:
                fext["fund_pct_trail"] = None; fext["fund_z_trail"] = None
            fext["rv_ratio_24h_168h"] = fe.rv_ratio(rv24h, rv168h)
            fext["rv_ratio_6h_168h"] = fe.rv_ratio((rv1h * 6) if rv1h is not None else None, rv168h)
            fext["px_disloc_ma"] = r.get("ema_dist")
            fext["px_disloc_ema"] = r.get("prem") if r.get("prem") is not None else r.get("ema_dist")
            extended.append(fext)

    train_rows = [r for r in extended if r["split"] == "train"]
    test_rows = [r for r in extended if r["split"] == "test"]

    # Train-only scalers
    scaler_rv24 = fe.TrainOnlyScaler().fit(get_vals(train_rows, "rv24h"))
    scaler_fund = fe.TrainOnlyScaler().fit(get_vals(train_rows, "signed_funding"))
    scaler_fund_abs = fe.TrainOnlyScaler().fit(get_vals(train_rows, "abs_fund_pct"))
    scaler_fund_pct = fe.TrainOnlyScaler().fit(get_vals(train_rows, "fund_pct_trail"))
    scaler_fund_z = fe.TrainOnlyScaler().fit(get_vals(train_rows, "fund_z_trail"))
    scaler_rv_ratio1 = fe.TrainOnlyScaler().fit(get_vals(train_rows, "rv_ratio_24h_168h"))
    scaler_rv_ratio2 = fe.TrainOnlyScaler().fit(get_vals(train_rows, "rv_ratio_6h_168h"))
    scaler_px = fe.TrainOnlyScaler().fit(get_vals(train_rows, "px_disloc_ma"))
    scalers = (scaler_rv24, scaler_fund, scaler_fund_abs, scaler_fund_pct, scaler_fund_z, scaler_rv_ratio1, scaler_rv_ratio2, scaler_px)

    test_res = build_all(test_rows, scalers)

    ts = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    out = []
    out.append(f"# STREAM_B_DEEP_ANALYSIS-002 - {ts}")
    out.append("")
    out.append("## Context")
    out.append(f"- Panel: {PANEL} (FCLR-002, frozen)")
    out.append(f"- Symbols: {sorted(by_sym.keys())} (n=5)")
    out.append(f"- Splits: {splits}")
    out.append(f"- Train/Test: {len(train_rows)}/{len(test_rows)}")
    out.append("- Constraint: leakage-resistant (train-only funding quartile thresholds + normalization, trailing-only features, chronological splits). No sealed panel re-runs.")
    out.append(f"- Block count: FCLR-002 test = 2 non-overlapping 30-day blocks (< 3) -> regime-stratified results are EXPLORATORY only, not confirmatory.")
    out.append("")

    # ---- Section 1: Funding |.| quartiles from TRAIN only ----
    out.append("## 1) Funding |.| quartile thresholds (TRAIN only, no look-ahead)")
    train_fund_abs = sorted(abs(float(r['signed_funding'])) for r in train_rows if r.get('signed_funding') is not None)
    def qtile(x, q):
        if not x:
            return 0.0
        k = int(q * (len(x) - 1))
        return x[k]
    tq1, tq2, tq3 = qtile(train_fund_abs, 0.25), qtile(train_fund_abs, 0.5), qtile(train_fund_abs, 0.75)
    out.append(f"- Train n={len(train_fund_abs)} |fund| quartiles: Q1 boundary={tq1:.6g}, Q2 (median)={tq2:.6g}, Q3 boundary={tq3:.6g}")
    out.append("- Regime rule (per symbol, train thresholds applied to test): Q1 = most negative signed funding .. Q4 = most positive signed funding, using abs(|fund|) quartile bins on signed funding sign.")
    out.append("")

    # Assign regimes per test row using TRAIN thresholds on abs(signed_funding), but Q1..Q4 ordered by signed funding sign within abs quartile
    def regime_of(r):
        fv = r.get('signed_funding')
        if fv is None:
            return None
        av = abs(float(fv))
        if av <= tq1:
            band = 'Q1_low_abs'
        elif av <= tq2:
            band = 'Q2'
        elif av <= tq3:
            band = 'Q3'
        else:
            band = 'Q4_high_abs'
        sign = 'neg' if float(fv) < 0 else 'pos'
        return f"{band}_{sign}"

    # Regime-stratified QLIKE per symbol: B1 vs C2_all
    out.append("## 2) Regime-stratified QLIKE per symbol per funding regime (TEST)")
    out.append("| Symbol | Regime | n | B1 QLIKE | C2_all QLIKE | rel_imp_vs_B1 | diff(C2-B1) | 95% CI (diff) | CI_excludes0 |")
    out.append("|--------|--------|---|----------|--------------|---------------|--------------|---------------|--------------|")

    regime_order = [
        'Q1_low_abs_neg', 'Q1_low_abs_pos',
        'Q2_neg', 'Q2_pos',
        'Q3_neg', 'Q3_pos',
        'Q4_high_abs_neg', 'Q4_high_abs_pos',
    ]

    regime_results = {}
    for sym in sorted(by_sym.keys()):
        sym_test = [r for r in test_rows if r['sym'] == sym]
        if not sym_test:
            continue
        # group by regime
        groups = defaultdict(list)
        for r in sym_test:
            reg = regime_of(r)
            if reg is not None:
                groups[reg].append(r)
        sym_block = build_all(sym_test, scalers)
        yb, yhb = sym_block['B1']
        qb = qlike_wrap(yb, yhb)
        for reg in regime_order:
            members = groups.get(reg, [])
            if not members:
                continue
            mres = build_all(members, scalers)
            ya, yha = mres['B1']
            yc, yhc = mres['C2_all']
            qa = qlike_wrap(ya, yha)
            qc = qlike_wrap(yc, yhc)
            rel = (qa - qc) / qa * 100 if qa > 0 else float('nan')
            d, cilo, cihi = bootstrap_ci(ya, yha, yhc, block_size=24, reps=2000, seed=12345)
            excludes = 'YES' if (cilo < 0 and cihi < 0) else 'NO'
            out.append(f"| {sym} | {reg} | {len(ya)} | {qa:.6f} | {qc:.6f} | {rel:+.3f}% | {d:.6f} | [{cilo:.6f},{cihi:.6f}] | {excludes} |")
            regime_results[(sym, reg)] = (qa, qc, rel, d, cilo, cihi, len(ya))
    out.append("")

    # ---- Section 3: Interaction/ablation per regime ----
    out.append("## 3) Interaction/ablation per regime (TEST, incremental contribution)")
    out.append("| Symbol | Regime | Model | QLIKE | rel_imp_vs_B1 | diff_vs_C2_all | 95% CI vs B1 | CI_excludes0 |")
    out.append("|--------|--------|-------|-------|---------------|----------------|--------------|--------------|")

    ablation_models = ['A1_fundpctz', 'A3_pricedisloc', 'C1', 'I1_fund_x_rvregime', 'I2_fund_x_disloc']
    for sym in sorted(by_sym.keys()):
        sym_test = [r for r in test_rows if r['sym'] == sym]
        if not sym_test:
            continue
        groups = defaultdict(list)
        for r in sym_test:
            reg = regime_of(r)
            if reg is not None:
                groups[reg].append(r)
        sym_block = build_all(sym_test, scalers)
        yb, yhb = sym_block['B1']
        qb = qlike_wrap(yb, yhb)
        yc, yhc = sym_block['C2_all']
        qc = qlike_wrap(yc, yhc)
        for reg in regime_order:
            members = groups.get(reg, [])
            if not members:
                continue
            mres = build_all(members, scalers)
            ya, yha = mres['B1']
            qa = qlike_wrap(ya, yha)
            for m in ablation_models:
                ym, yhm = mres[m]
                qm = qlike_wrap(ym, yhm)
                rel = (qa - qm) / qa * 100 if qa > 0 else float('nan')
                d, cilo, cihi = bootstrap_ci(ya, yha, yhm, block_size=24, reps=2000, seed=12346)
                excludes = 'YES' if (cilo < 0 and cihi < 0) else 'NO'
                dvs = qm - qc
                out.append(f"| {sym} | {reg} | {m} | {qm:.6f} | {rel:+.3f}% | {dvs:+.6f} | [{cilo:.6f},{cihi:.6f}] | {excludes} |")
    out.append("")

    # ---- Section 4: Aggregate regime summary (all symbols pooled) ----
    out.append("## 4) Aggregate regime summary (all symbols pooled, TEST)")
    out.append("| Regime | n | B1 QLIKE | C2_all QLIKE | rel_imp_vs_B1 | diff(C2-B1) | 95% CI | CI_excludes0 |")
    out.append("|--------|---|----------|--------------|---------------|--------------|--------|--------------|")
    for reg in regime_order:
        all_y, all_yhb, all_yhc = [], [], []
        for sym in sorted(by_sym.keys()):
            if (sym, reg) not in regime_results:
                continue
            members = [r for r in test_rows if r['sym'] == sym and regime_of(r) == reg]
            if not members:
                continue
            mres = build_all(members, scalers)
            ya, yha = mres['B1']
            yc, yhc = mres['C2_all']
            all_y.extend(ya); all_yhb.extend(yha); all_yhc.extend(yhc)
        if not all_y:
            continue
        qa = qlike_wrap(all_y, all_yhb)
        qc = qlike_wrap(all_y, all_yhc)
        rel = (qa - qc) / qa * 100 if qa > 0 else float('nan')
        d, cilo, cihi = bootstrap_ci(all_y, all_yhb, all_yhc, block_size=24, reps=2000, seed=12347)
        excludes = 'YES' if (cilo < 0 and cihi < 0) else 'NO'
        out.append(f"| {reg} | {len(all_y)} | {qa:.6f} | {qc:.6f} | {rel:+.3f}% | {d:.6f} | [{cilo:.6f},{cihi:.6f}] | {excludes} |")
    out.append("")

    # ---- Section 5: Block-bootstrap per regime diagnostic ----
    out.append("## 5) Per-regime observation counts and block-bootstrap validity (TEST)")
    out.append("| Symbol | Regime | n | unique_regime_rows | min_block_24h_feasible |")
    out.append("|--------|--------|---|----------------------|------------------------|")
    for sym in sorted(by_sym.keys()):
        sym_test = [r for r in test_rows if r['sym'] == sym]
        groups = defaultdict(list)
        for r in sym_test:
            reg = regime_of(r)
            if reg is not None:
                groups[reg].append(r)
        for reg in regime_order:
            members = groups.get(reg, [])
            n = len(members)
            feasible = 'YES' if n >= 24 else 'NO'
            out.append(f"| {sym} | {reg} | {n} | {n} | {feasible} |")
    out.append("")

    # ---- Section 6: Status decision ----
    out.append("## 6) Status decision (FUNDING_CONDITIONING_DEEPER_VALIDATION-002)")
    out.append("- Gate: confirmatory requires >=3 non-overlapping 30-day blocks; FCLR-002 test has 2 blocks -> confirmatory NOT met, EXPLORATORY only.")
    out.append("- Aggregate C2 vs B1 on full TEST: +4.588% rel QLIKE, CI excludes 0 (STREAM_B_DEEP_ANALYSIS-001).")
    out.append("- Regime-stratified results above: inspect per-regime CI_excludes0 and rel_imp. If NO regime shows robust skill (CI excludes 0 AND rel_imp >= 0 consistently), record null in negative_results_report.md Track C section and set experiment_frontier.json FUNDING_CONDITIONING_DEEPER_VALIDATION-002 to COMPLETE_INCONCLUSIVE. If a regime shows robust skill, keep EXPLORATORY_ONLY — do NOT promote to confirmatory (2 blocks < 3).")
    out.append("")

    out_lines = '\n'.join(out) + '\n'
    OUT.write_text(out_lines)
    print(f"Wrote {OUT}")


if __name__ == '__main__':
    main()
