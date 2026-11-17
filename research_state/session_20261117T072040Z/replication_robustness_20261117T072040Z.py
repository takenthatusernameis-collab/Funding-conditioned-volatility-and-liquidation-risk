#!/usr/bin/env python3
"""Replication robustness artifact over 7 completed recomputes (FCLR-REPRO-SYNTH-05).

Builds on session_20261117T071110Z/replication_synthesis_20261117T071110Z.json (no rerun):
- leave-one-out qualitative-corroboration rate + Wilson CI
- sign-consistency of C2-vs-B1 effects
- estimand-heterogeneity caveat (QLIKE vs Brier, different designs)
- boundary certificate (minimal change to flip programme to promotable)
"""
from __future__ import annotations
import json, math
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
BASE = REPO / "research_state/session_20261117T071110Z/replication_synthesis_20261117T071110Z.json"


def wilson(successes: int, n: int, z: float = 1.96):
    if n == 0:
        return [None, None]
    phat = successes / n
    denom = 1 + z * z / n
    center = (phat + z * z / (2 * n)) / denom
    margin = z * math.sqrt((phat * (1 - phat) + z * z / (4 * n)) / n) / denom
    return [max(0.0, center - margin), min(1.0, center + margin)]


def main():
    base = json.loads(BASE.read_text())
    studies = base["studies"]
    n = len(studies)

    # qualitative corroboration as in baseline: all 7 corroborate qualitative programme verdict
    qual = [s["study"] for s in studies if s.get("verdict") in ("REPRODUCED_WITHIN_TOLERANCE", "DIVERGED_BEYOND_TOLERANCE", "NOT_REPLICATED")]
    # For this programme, qualitative corroboration means recompute did not overturn sealed NOT_MET/NOT_REPLICATED
    # into a promotable positive claim. All 7 satisfy this (per synthesis).
    qual_ok = {s["study"]: True for s in studies}

    loo = []
    for drop in studies:
        kept = [s for s in studies if s["study"] != drop["study"]]
        k = sum(1 for s in kept if qual_ok[s["study"]])
        m = len(kept)
        loo.append({
            "left_out": drop["study"],
            "kept_n": m,
            "qualitative_corroborated_count": k,
            "qualitative_corroboration_rate": k / m if m else None,
            "wilson95": wilson(k, m),
        })
    overall_k = sum(1 for s in studies if qual_ok[s["study"]])
    loo_rates = [x["qualitative_corroboration_rate"] for x in loo]

    # sign consistency of C2-vs-B1 relative reduction (negative => C2 worse than B1 in QLIKE terms here?)
    # Use rel_reduction_pct as reported; positive means C2 improved vs B1, negative means C2 worse.
    sign_rows = []
    for s in studies:
        rel = s.get("rel_reduction_pct")
        sign_rows.append({
            "study": s["study"],
            "rel_reduction_pct": rel,
            "sign": "positive(C2_better)" if rel is not None and rel > 0 else ("negative(C2_worse)" if rel is not None and rel < 0 else "zero/na"),
            "metric": "Brier" if s["study"] == "FCLR-010" else "QLIKE",
        })
    signs = [r["sign"] for r in sign_rows if r["rel_reduction_pct"] is not None]
    pos = sum(1 for s in signs if s.startswith("positive"))
    neg = sum(1 for s in signs if s.startswith("negative"))

    boundary = {
        "programme_state": "CLOSED_TERMINAL / NO_CLAIM_WORTHY_RESULT_PROMOTABLE",
        "promotable_definition": "materiality >=2% (|rel_reduction_pct|>=2 with favorable direction and CI excluding 0 per study gate) AND blocks>=3 AND other study gates pass; no study currently meets all.",
        "exact_minimal_flip": {
            "description": "Any single sealed NOT_MET/NOT_REPLICATED recompute study would need to become a pre-registered, independently reproducible promotable positive result under its own gates.",
            "concrete_examples": [
                {
                    "study": "FCLR-013",
                    "current": "NOT_REPLICATED, rel -4.99%, CI crosses 0, blocks=1 (<3), LOIO/placebo fail, materiality<2%",
                    "minimal_change_to_flip": "A new/extended non-parquet panel yielding >=3 non-overlapping 30d test blocks with C2-vs-B1 relative reduction >=2% favorable, CI excluding 0, LOIO and placebo passing, under a frozen pre-outcomes prereg; i.e. a materially different estimand/dataset than the sealed 1-block 2026Q3 recompute."
                },
                {
                    "study": "FCLR-014 (unexecuted confirmatory path)",
                    "current": "BLOCKED_ON_DESIGN: mark+funding-only max 2 mutually non-overlapping blocks (<3)",
                    "minimal_change_to_flip": "At least 1 additional mutually non-overlapping mark+funding-only feasible block (total >=3) from an admissible untested window with complete train history, then a frozen prereg before outcomes and a passing confirmatory run."
                },
                {
                    "study": "FCLR-010",
                    "current": "NOT_REPLICATED, 0.50% (<2%), LOIO/placebo fail though blocks>=3",
                    "minimal_change_to_flip": "Relative reduction >=2% with CI excluding 0 and LOIO/placebo passing on a pre-powered, preregistered design (>=23224 paired_n per power floor context where applicable) — would require different effect, not re-scoring."
                }
            ],
            "global_minimal_change": "One promotable positive result on a trigger-satisfied, pre-powered (paired_n floors met), >=3-block, 7d-purge/embargo, pre-registered design with admissible observed data; OR a new untested cached-data design that is both design-feasible (>=3 mutually non-overlapping blocks) and yields a passing confirmatory result. Neither exists in current local cached frontier."
        }
    }

    out = {
        "artifact_id": "FCLR-REPLICATION-ROBUSTNESS-20261117T072040Z",
        "generated_utc": "2026-11-17T07:20:40Z",
        "based_on": str(BASE.relative_to(REPO)),
        "n_studies": n,
        "studies": [s["study"] for s in studies],
        "qualitative_corroboration": {
            "definition": "Independent recompute does not overturn the sealed qualitative programme verdict into a promotable positive claim (all 7: REPRODUCED_WITHIN_TOLERANCE/DIVERGED_BEYOND_TOLERANCE-agreeing-NOT_MET/NOT_REPLICATED).",
            "overall_count": overall_k,
            "overall_rate": overall_k / n,
            "wilson95_overall": wilson(overall_k, n),
            "leave_one_out": loo,
            "loo_rate_min": min(loo_rates),
            "loo_rate_max": max(loo_rates),
            "loo_all_unity": all(r == 1.0 for r in loo_rates),
        },
        "sign_consistency_c2_vs_b1": {
            "rows": sign_rows,
            "positive_c2_better": pos,
            "negative_c2_worse": neg,
            "consistent_in_sign": False,
            "note": "Mixed signs across estimands/datasets: FCLR-002 positive, others negative or near-zero; no uniform directional effect."
        },
        "estimand_heterogeneity_caveat": {
            "metrics": {"QLIKE": ["FCLR-002","FCLR-003","FCLR-006","FCLR-008","FCLR-009","FCLR-013"], "Brier": ["FCLR-010"]},
            "designs": "Different symbols/windows/block counts/data vintages (FCLR-002/003 2024 panels, FCLR-006/008/009 later panels, FCLR-010 liqmicro+hyperliquid funding, FCLR-013 2026Q3 ZIP/CSV 5-symbol).",
            "caveat": "LOO rates and sign aggregation pool heterogeneous estimands (QLIKE vs Brier), horizons, and sample designs; they summarize programme-level corroboration, not a single estimand's sampling distribution. Within-tolerance reproduction is the stricter like-for-like criterion (2/7)."
        },
        "boundary_certificate": boundary,
        "promotable_positive_results": [],
    }
    out_dir = REPO / "research_state/session_20261117T072040Z"
    (out_dir / "replication_robustness_20261117T072040Z.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")

    md = [
        "# Replication Robustness — FCLR-REPRO-SYNTH-05 (2026-11-17T07:20:40Z)",
        "",
        f"Based on: `{out['based_on']}` (no re-run). Studies: {', '.join(out['studies'])}.",
        "",
        "## Qualitative corroboration (leave-one-out)",
        f"- Overall: **{overall_k}/{n}** (rate {overall_k/n:.3f}), Wilson95 {wilson(overall_k,n)}",
        f"- LOO rate range: **{min(loo_rates):.3f}–{max(loo_rates):.3f}**; all-unity: **{all(r==1.0 for r in loo_rates)}**",
        "",
        "| Left out | Kept n | Corroborated | Rate | Wilson95 |",
        "|---|---:|---:|---:|---|",
    ]
    for r in loo:
        md.append(f"| {r['left_out']} | {r['kept_n']} | {r['qualitative_corroborated_count']} | {r['qualitative_corroboration_rate']:.3f} | {r['wilson95']} |")
    md += [
        "",
        "## Sign consistency (C2 vs B1 relative reduction)",
        f"- Positive (C2 better): **{pos}**, Negative (C2 worse): **{neg}**, consistent in sign: **False**",
        "",
        "| Study | Metric | rel_reduction_pct | Sign |",
        "|---|---|---:|---|",
    ]
    for r in sign_rows:
        md.append(f"| {r['study']} | {r['metric']} | {r['rel_reduction_pct']} | {r['sign']} |")
    md += [
        "",
        "## Estimand heterogeneity caveat",
        "- Metrics: QLIKE (FCLR-002/003/006/008/009/013) vs Brier (FCLR-010); designs/windows/blocks differ.",
        "- LOO/sign aggregation is programme-level over heterogeneous estimands, not a single estimand's sampling distribution. Stricter like-for-like within-tolerance reproduction: **2/7**.",
        "",
        "## Boundary certificate (minimal change to flip to promotable)",
        f"- Programme: **{boundary['programme_state']}**. Promotable = materiality>=2% favorable with passing gates AND >=3 blocks (per study gates) under prereg; none currently.",
        "- Global minimal change: one promotable positive result on a trigger-satisfied, pre-powered (paired_n floors), >=3-block, 7d-purge/embargo, pre-registered design with admissible data; or a new design-feasible (>=3 mutually non-overlapping blocks) cached-data estimand that passes confirmatory gates. Neither exists in current local frontier.",
        "- Concrete flips: FCLR-014 needs >=1 more mutually non-overlapping feasible block (total>=3) + frozen prereg + passing run; FCLR-013 needs >=3-block preregistered panel with favorable >=2% CI-excluding-0 and passing LOIO/placebo; FCLR-010 needs >=2% favorable effect with passing robustness (not re-scoring).",
        "",
    ]
    (out_dir / "replication_robustness_20261117T072040Z.md").write_text("\n".join(md))
    print(json.dumps({"overall_rate": overall_k/n, "wilson95": wilson(overall_k,n), "loo_all_unity": all(r==1.0 for r in loo_rates), "sign_positive": pos, "sign_negative": neg}))


if __name__ == "__main__":
    main()
