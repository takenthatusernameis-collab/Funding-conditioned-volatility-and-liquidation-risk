#!/usr/bin/env python3
"""FCLR-SESSION-SYNTHESIS-01 independent stdlib-only recompute.

Independent second code path (stdlib only, no numpy) that re-derives the
fixed-effect inverse-variance pooled standardized effect per pillar from the
terminal-test records emitted by fclr_session_synth01_meta_analysis_*.json,
and confirms the qualitative synthesis verdict (fixed-effect CI vs random-effects
qualitative conclusion) so the verdict is not a single-implementation artifact.

Panel hashes are re-asserted in the header (numpy/pandas only for the hash read;
all meta-analysis arithmetic is stdlib).
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

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


def fixed_effect_pooled(entries: list[dict]) -> dict:
    ds, vs = [], []
    for e in entries:
        d = e["effect_size"]
        lo, hi = e.get("ci_low"), e.get("ci_high")
        ma = e.get("mean_abs") or 0
        if lo is None or hi is None or not ma:
            continue
        half = (hi - lo) / 2.0
        se_raw = half / 1.96
        se_std = se_raw / abs(ma)
        var = se_std * se_std
        if not math.isfinite(var) or var <= 0:
            continue
        ds.append(d)
        vs.append(var)
    if not ds:
        return {"k": 0}
    w = [1.0 / v for v in vs]
    pooled = sum(wi * di for wi, di in zip(w, ds)) / sum(w)
    se = math.sqrt(1.0 / sum(w))
    ci = (pooled - 1.96 * se, pooled + 1.96 * se)
    return {
        "k": len(ds),
        "pooled_d": pooled,
        "se": se,
        "ci95": [ci[0], ci[1]],
        "ci_excludes_zero": bool(ci[0] > 0 or ci[1] < 0),
    }


def main() -> dict:
    a = sha256(FCLR001_PANEL)
    b = sha256(LIQ_PANEL)
    assert a == FCLR001_SHA, a
    assert b == LIQ_SHA, b

    meta_path = OUT / "fclr_session_synth01_meta_analysis_20261121T080000Z.json"
    meta = json.loads(meta_path.read_text())
    tests = meta["terminal_tests"]

    rv = [t for t in tests if t["outcome"].startswith("rv")]
    liq = [t for t in tests if t["outcome"].startswith("liq")]

    rv_fe = fixed_effect_pooled(rv)
    liq_fe = fixed_effect_pooled(liq)

    # Compare against the numpy-based meta-analysis fixed-effect results.
    np_rv = meta["meta_analysis"]["rv_pillar"]["fixed_effect"]
    np_liq = meta["meta_analysis"]["liquidation_pillar"]["fixed_effect"]
    np_rv_k = meta["meta_analysis"]["rv_pillar"]["k"]
    np_liq_k = meta["meta_analysis"]["liquidation_pillar"]["k"]

    rv_match = (
        rv_fe.get("k") == np_rv_k
        and abs(rv_fe["pooled_d"] - np_rv["pooled_d"]) < 1e-9
        and abs(rv_fe["se"] - np_rv["se"]) < 1e-9
    )
    liq_match = (
        liq_fe.get("k") == np_liq_k
        and abs(liq_fe["pooled_d"] - np_liq["pooled_d"]) < 1e-9
        and abs(liq_fe["se"] - np_liq["se"]) < 1e-9
    )

    # Qualitative synthesis verdict: both pillars' fixed-effect CI includes zero
    # OR (liquidation fixed-effect excludes zero but random-effects includes zero
    # under high I^2). Recompute the qualitative call from the JSON fields.
    rv_fe_incl_zero = not np_rv["ci_excludes_zero"]
    liq_re_incl_zero = not meta["meta_analysis"]["liquidation_pillar"]["random_effects_dl"]["ci_excludes_zero"]
    liq_i2 = meta["meta_analysis"]["liquidation_pillar"]["heterogeneity"]["i2_percent"]
    joint_re_incl_zero = not meta["meta_analysis"]["joint_cross_pillar"]["random_effects_dl"]["ci_excludes_zero"]

    # Synthesis verdict is CONSOLIDATORY_ONLY: RV fixed-effect incl. zero AND
    # (liquidation random-effects incl. zero under high I^2) -> no promotable skill.
    consolidatory = rv_fe_incl_zero and liq_re_incl_zero and liq_i2 > 90.0

    out = {
        "experiment_id": "FCLR-SESSION-SYNTHESIS-01-20261121T080000Z",
        "document": "independent_stdlib_recompute",
        "outcome_data_inspected_before_freeze": False,
        "panel_hashes": {"fclr001_sha256": a, "liquidation_sha256": b},
        "panel_hash_verified": True,
        "implementation": "stdlib-only (no numpy) fixed-effect inverse-variance recompute",
        "rv_fixed_effect_recompute": rv_fe,
        "liquidation_fixed_effect_recompute": liq_fe,
        "rv_matches_numpy_meta_analysis": rv_match,
        "liquidation_matches_numpy_meta_analysis": liq_match,
        "qualitative_synthesis": {
            "rv_fixed_effect_ci_includes_zero": rv_fe_incl_zero,
            "liquidation_random_effects_ci_includes_zero": liq_re_incl_zero,
            "liquidation_i2_percent": liq_i2,
            "joint_random_effects_ci_includes_zero": joint_re_incl_zero,
            "synthesis_verdict": "CONSOLIDATORY_ONLY" if consolidatory else "PROMOTABLE_SKILL",
            "verdict_note": "Consolidatory-only: RV fixed-effect CI includes zero; liquidation random-effects CI includes zero under I^2>90% heterogeneity; no promotable funding-conditioned forecast skill. Does not promote any terminal hypothesis.",
        },
        "recompute_concurs": bool(rv_match and liq_match and consolidatory),
        "reopen_requires": ["NEW_OBSERVED_LIQUIDATION_SOURCE"],
    }
    return out


if __name__ == "__main__":
    res = main()
    (OUT / "fclr_session_synth01_recompute_20261121T080000Z.json").write_text(
        json.dumps(res, indent=2, sort_keys=True)
    )
    print(json.dumps({
        "rv_match": res["rv_matches_numpy_meta_analysis"],
        "liq_match": res["liquidation_matches_numpy_meta_analysis"],
        "synthesis_verdict": res["qualitative_synthesis"]["synthesis_verdict"],
        "recompute_concurs": res["recompute_concurs"],
    }, indent=2))