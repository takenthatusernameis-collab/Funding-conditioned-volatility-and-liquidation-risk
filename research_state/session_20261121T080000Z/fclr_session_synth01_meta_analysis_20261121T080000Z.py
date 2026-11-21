#!/usr/bin/env python3
"""FCLR-SESSION-SYNTHESIS-01 quantitative meta-analysis (pre-registered, outcome-blind).

This script reads the two frozen FCLR panels (asserting their sha256 in the header),
loads the exact terminal-campaign test statistics from the already-complete
research_state/session_* evaluation JSON artifacts, and performs a pre-registered
inverse-variance weighted fixed-effect meta-analysis (+ DerSimonian-Laird random-effects
sensitivity, Cochran's Q, I^2) over the terminal funding-conditioning contrasts.

It generates NO new outcomes. It is a consolidation / meta-analysis over terminal
artifacts. The verdict is DESCRIPTIVE/CONSOLIDATORY only and never promotes a
terminal hypothesis.

Panel hashes (asserted before any computation):
  FCLR-001:             41962f823e59de5989c7d854cb3180cad61a4cbc2f5f230133c41b321342c1f4
  combined liquidation: 81a100d5d0625832bebabaabea13b786e15319577721cfe8507da5b779ec7f14
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
RS = REPO / "research_state"
OUT = Path(__file__).resolve().parent

FCLR001_PANEL = RS / "fclr011_recompute_panel_20261115T234700Z.parquet"
FCLR001_SHA = "41962f823e59de5989c7d854cb3180cad61a4cbc2f5f230133c41b321342c1f4"
LIQ_PANEL = RS / "fclr_liq_combined_panel_20261115T181405Z.parquet"
LIQ_SHA = "81a100d5d0625832bebabaabea13b786e15319577721cfe8507da5b779ec7f14"


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()


def assert_panels() -> dict:
    a = sha256(FCLR001_PANEL)
    b = sha256(LIQ_PANEL)
    assert a == FCLR001_SHA, f"FCLR001 panel hash mismatch: {a}"
    assert b == LIQ_SHA, f"LIQ panel hash mismatch: {b}"
    return {"fclr001_sha256": a, "liquidation_sha256": b}


def _load_terminal_tests() -> dict:
    """Load exact terminal test statistics from completed session JSONs.

    Each entry: {campaign, outcome, regime, effect_size (mean_diff/mean_abs),
                 mean_diff, mean_abs, ci_low, ci_high, p_value, holm_passes,
                 materiality_met, verdict, n}
    """
    tests = []

    # FCLR-XSEC-002: funding -> next-hour RV, RV tercile regime (FCLR-001 panel)
    p = RS / "session_20261120T210000Z/fclr_xsec002_evaluation_20261120T210000Z.json"
    d = json.loads(p.read_text())
    for name, t in d["tests"].items():
        if "funding_contrast" not in name:
            continue
        ma = t.get("mean_abs_target", t.get("mean_abs_outcome", 0.0)) or 0.0
        tests.append({
            "campaign": "FCLR-XSEC-002",
            "outcome": "rv_next_hour",
            "regime": name.replace("_funding_contrast", ""),
            "effect_size": t["mean_diff_high_minus_low"] / ma if ma else 0.0,
            "mean_diff": t["mean_diff_high_minus_low"],
            "mean_abs": ma,
            "ci_low": t.get("ci_low"), "ci_high": t.get("ci_high"),
            "p_value": t.get("p_value"), "holm_passes": t.get("holm_passes"),
            "materiality_met": t.get("materiality_floor_met"),
            "verdict": d["verdict"], "n": t.get("n_hours"),
        })

    # FCLR-XSEC-004: funding -> next-hour liquidation intensity (count-based)
    p = RS / "session_20261120T230000Z/fclr_xsec004_evaluation_20261120T230000Z.json"
    d = json.loads(p.read_text())
    for name, t in d["tests"].items():
        if "funding_contrast" not in name:
            continue
        ma = t.get("mean_abs_outcome", t.get("mean_abs_target", 0.0)) or 0.0
        tests.append({
            "campaign": "FCLR-XSEC-004",
            "outcome": "liq_count_next_hour",
            "regime": name.replace("_funding_contrast", ""),
            "effect_size": t["mean_diff_high_minus_low"] / ma if ma else 0.0,
            "mean_diff": t["mean_diff_high_minus_low"],
            "mean_abs": ma,
            "ci_low": t.get("ci_low"), "ci_high": t.get("ci_high"),
            "p_value": t.get("p_value"), "holm_passes": t.get("holm_passes"),
            "materiality_met": t.get("materiality_floor_met"),
            "verdict": d["verdict"], "n": t.get("n_hours"),
        })

    # FCLR-XSEC-005: funding -> next-hour liquidation intensity (notional-weighted)
    p = RS / "session_20261121T001225Z/fclr_xsec005_evaluation_20261121T001225Z.json"
    d = json.loads(p.read_text())
    for name, t in d["tests"].items():
        if "funding_contrast" not in name:
            continue
        ma = t.get("mean_abs_outcome", t.get("mean_abs_target", 0.0)) or 0.0
        tests.append({
            "campaign": "FCLR-XSEC-005",
            "outcome": "liq_notional_next_hour",
            "regime": name.replace("_funding_contrast_notional_weighted", "")
                          .replace("_funding_contrast", ""),
            "effect_size": t["mean_diff_high_minus_low"] / ma if ma else 0.0,
            "mean_diff": t["mean_diff_high_minus_low"],
            "mean_abs": ma,
            "ci_low": t.get("ci_low"), "ci_high": t.get("ci_high"),
            "p_value": t.get("p_value"), "holm_passes": t.get("holm_passes"),
            "materiality_met": t.get("materiality_floor_met"),
            "verdict": d["verdict"], "n": t.get("n_hours"),
        })

    # FCLR-XSEC-006: funding -> next-hour notional liq, UTC session bucket
    p = RS / "session_20261121T010934Z/fclr_xsec006_evaluation_20261121T010934Z.json"
    d = json.loads(p.read_text())
    for name, t in d.get("tests", {}).items():
        if not isinstance(t, dict) or "mean_diff_high_minus_low" not in t:
            continue
        ma = t.get("mean_abs_outcome", t.get("mean_abs", 0.0)) or 0.0
        tests.append({
            "campaign": "FCLR-XSEC-006",
            "outcome": "liq_notional_next_hour_utc_bucket",
            "regime": name.replace("_funding_contrast_notional_weighted", "")
                          .replace("_funding_contrast", ""),
            "effect_size": t["mean_diff_high_minus_low"] / ma if ma else 0.0,
            "mean_diff": t["mean_diff_high_minus_low"],
            "mean_abs": ma,
            "ci_low": t.get("ci_low"), "ci_high": t.get("ci_high"),
            "p_value": t.get("p_value"),
            "holm_passes": t.get("holm_passes"),
            "materiality_met": t.get("materiality_floor_met"),
            "verdict": d.get("verdict", "SUPPORTED"), "n": t.get("n_hours"),
        })

    return tests


def _meta_analysis(entries: list[dict], label: str) -> dict:
    """Inverse-variance fixed-effect + DerSimonian-Laird random-effects meta-analysis.

    Effect size per entry: standardized mean difference d = mean_diff / mean_abs.
    Approximate variance of d via the CI half-width: var = ((ci_high - ci_low) / (2*1.96))^2 / mean_abs^2
    (CI is on the raw mean_diff scale; convert to the standardized scale).
    """
    ds = []
    vs = []
    for e in entries:
        d = e["effect_size"]
        if e["ci_low"] is None or e["ci_high"] is None or e["mean_abs"] in (None, 0):
            continue
        half = (e["ci_high"] - e["ci_low"]) / 2.0
        se_raw = half / 1.96
        se_std = se_raw / abs(e["mean_abs"])
        var = se_std ** 2
        if not math.isfinite(var) or var <= 0:
            continue
        ds.append(d)
        vs.append(var)

    if not ds:
        return {"label": label, "k": 0, "verdict": "INSUFFICIENT_EVIDENCE"}

    ds = np.array(ds)
    vs = np.array(vs)
    w = 1.0 / vs
    fe = float(np.sum(w * ds) / np.sum(w))
    fe_var = float(1.0 / np.sum(w))
    fe_se = math.sqrt(fe_var)
    fe_ci = (fe - 1.96 * fe_se, fe + 1.96 * fe_se)

    # Cochran's Q
    q = float(np.sum(w * (ds - fe) ** 2))
    df = len(ds) - 1
    # I^2
    if q > df and df > 0:
        i2 = max(0.0, (q - df) / q) * 100.0
    else:
        i2 = 0.0
    # DerSimonian-Laird tau^2
    c = float(np.sum(w) - np.sum(w ** 2) / np.sum(w))
    tau2 = max(0.0, (q - df) / c) if c > 0 and df > 0 else 0.0
    w_re = 1.0 / (vs + tau2)
    re = float(np.sum(w_re * ds) / np.sum(w_re))
    re_se = math.sqrt(1.0 / np.sum(w_re))
    re_ci = (re - 1.96 * re_se, re + 1.96 * re_se)

    return {
        "label": label,
        "k": len(ds),
        "fixed_effect": {
            "pooled_d": fe, "se": fe_se, "ci95": [fe_ci[0], fe_ci[1]],
            "ci_excludes_zero": bool(fe_ci[0] > 0 or fe_ci[1] < 0),
        },
        "random_effects_dl": {
            "pooled_d": re, "se": re_se, "ci95": [re_ci[0], re_ci[1]],
            "tau2": tau2, "ci_excludes_zero": bool(re_ci[0] > 0 or re_ci[1] < 0),
        },
        "heterogeneity": {"cochran_q": q, "df": df, "i2_percent": i2},
    }


def main() -> dict:
    panel_hashes = assert_panels()

    # Panel structural audit: load and summarize both frozen panels (no outcome computation).
    fclr = pd.read_parquet(FCLR001_PANEL)
    liq = pd.read_parquet(LIQ_PANEL)
    panel_summary = {
        "fclr001": {
            "path": str(FCLR001_PANEL.relative_to(REPO)),
            "sha256": panel_hashes["fclr001_sha256"],
            "rows": int(len(fclr)), "cols": int(fclr.shape[1]),
            "columns": list(map(str, fclr.columns)),
        },
        "liquidation": {
            "path": str(LIQ_PANEL.relative_to(REPO)),
            "sha256": panel_hashes["liquidation_sha256"],
            "rows": int(len(liq)), "cols": int(liq.shape[1]),
            "columns": list(map(str, liq.columns)),
        },
    }

    tests = _load_terminal_tests()
    assert tests, "no terminal tests loaded — expected the completed session artifacts"

    # Stratify by outcome pillar.
    rv_entries = [t for t in tests if t["outcome"].startswith("rv")]
    liq_entries = [t for t in tests if t["outcome"].startswith("liq")]

    rv_meta = _meta_analysis(rv_entries, "rv_pillar")
    liq_meta = _meta_analysis(liq_entries, "liquidation_pillar")
    joint_meta = _meta_analysis(tests, "joint_cross_pillar")

    # Count significant positive / negative contrasts.
    sig_pos = [t for t in tests if t["holm_passes"] and t["effect_size"] > 0
               and (t["ci_low"] is not None and t["ci_low"] > 0)]
    sig_neg = [t for t in tests if t["holm_passes"] and t["effect_size"] < 0
               and (t["ci_high"] is not None and t["ci_high"] < 0)]

    # Terminal campaign verdict tally.
    campaigns = sorted({t["campaign"] for t in tests})
    verdict_by_campaign = {}
    for c in campaigns:
        vs = {t["verdict"] for t in tests if t["campaign"] == c}
        verdict_by_campaign[c] = sorted(vs)

    out = {
        "experiment_id": "FCLR-SESSION-SYNTHESIS-01-20261121T080000Z",
        "session_utc": "20261121T080000Z",
        "design": "outcome_blind_inverse_variance_fixed_effect_plus_dl_random_effects_meta_analysis",
        "outcome_data_inspected_before_freeze": False,
        "generates_no_new_outcomes": True,
        "panel_hashes": panel_hashes,
        "panel_hash_verified": True,
        "panel_summary": panel_summary,
        "n_terminal_tests": len(tests),
        "terminal_tests": tests,
        "meta_analysis": {
            "rv_pillar": rv_meta,
            "liquidation_pillar": liq_meta,
            "joint_cross_pillar": joint_meta,
        },
        "significance_tally": {
            "holm_significant_positive": len(sig_pos),
            "holm_significant_negative": len(sig_neg),
            "positive_campaigns": sorted({t["campaign"] for t in sig_pos}),
        },
        "verdict_by_campaign": verdict_by_campaign,
        "synthesis_verdict": "CONSOLIDATORY_ONLY",
        "synthesis_verdict_note": (
            "Descriptive consolidation of terminal verdicts. Does NOT promote any "
            "terminal hypothesis. RV-pillar OOS confirmations all failed; "
            "liquidation-pillar cross-sectional contrasts are significant but the "
            "OOS forecast gate failed on QLIKE. Joint evidence is directionally "
            "incoherent for a promotable funding-conditioning forecast skill."
        ),
        "cross_reference": [
            "FCLR-STARTER-001", "FCLR-XSEC-001", "FCLR-XSEC-002", "FCLR-XSEC-003",
            "FCLR-XSEC-004", "FCLR-XSEC-005", "FCLR-XSEC-006", "FCLR-XSEC-007",
            "FCLR-XSEC-008", "FCLR-LIQ-OOS-FORECAST-001",
            "FCLR-LIQ-COMBINED-PANEL", "Track A", "Track B",
        ],
        "reopen_requires": ["NEW_OBSERVED_LIQUIDATION_SOURCE"],
    }
    return out


if __name__ == "__main__":
    res = main()
    outpath = OUT / "fclr_session_synth01_meta_analysis_20261121T080000Z.json"
    outpath.write_text(json.dumps(res, indent=2, sort_keys=True))
    print(json.dumps({
        "experiment_id": res["experiment_id"],
        "n_terminal_tests": res["n_terminal_tests"],
        "rv_pooled_d": res["meta_analysis"]["rv_pillar"].get("fixed_effect", {}).get("pooled_d"),
        "liq_pooled_d": res["meta_analysis"]["liquidation_pillar"].get("fixed_effect", {}).get("pooled_d"),
        "joint_pooled_d": res["meta_analysis"]["joint_cross_pillar"].get("fixed_effect", {}).get("pooled_d"),
        "synthesis_verdict": res["synthesis_verdict"],
    }, indent=2))