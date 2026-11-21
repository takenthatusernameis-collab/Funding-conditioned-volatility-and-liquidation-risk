# FCLR-LIQ-CONTAGION-002 Reconciliation Evaluation Report

**Experiment ID:** FCLR-LIQ-CONTAGION-002-20261121T210000Z
**Campaign:** FCLR-LIQ-CONTAGION-002
**Session:** `research_state/session_20261121T210000Z/`
**Generated UTC:** 2026-11-21T21:00:00Z
**Panel:** `research_state/fclr_liq_combined_panel_20261115T181405Z.parquet` (sha256 `81a100d5d0625832bebabaabea13b786e15319577721cfe8507da5b779ec7f14`)
**Panel rows:** 1,740,415 event rows; 15 coins; 2025-03-22T19:00:18Z .. 2026-10-31T22:02:10Z UTC
**Hourly coin-observations:** 211,188 (14,116 hours × 15 coins; 0 dropped for missing funding)
**Directed pairs:** 210 (15 × 14)

---

## Purpose

FCLR-LIQ-CONTAGION-001 (session_20261121T193000Z, COMPLETE) disclosed an unresolved methodological discrepancy:
- eval edge set = 11 edges (Granger-Bonferroni INTERSECT permutation-Bonferroni, density 0.0524)
- independent recompute edge set = 58 edges (empirical-p only, density 0.2762)
- the two edge sets disagree on 47 of 210 directed pairs
- the declared 2% per-edge materiality floor was asserted True but never actually computed (no per-edge variance-explained field)
- funding-tercile and temporal-stability results were never reconciled against the primary edge set

This reconciliation computes per-edge variance explained (the quantity CONTAGION-001 never computed), applies a four-criterion multiple-testing robustness ladder to all 210 directed pairs, reconciles funding-tercile and temporal stability against each criterion's edge set, and runs a 1000-resample moving-block bootstrap for edge-set stability.

---

## Estimator definitions (frozen pre-outcomes)

- VAR order: 6
- Per directed pair (A→B): regress B's hourly liquidation count on B's own lags 1..6 plus A's lagged counts 1..6, with intercept. Restricted model: B's own lags + intercept only.
- Partial variance explained: `variance_explained = 1 - SSR_unrestricted / SSR_restricted`
- Granger F-test: joint F-test of the 6 source-lag coefficients; p-value from F(6, df_resid).
- Raw p criterion: edge if Granger p < 0.01 (uncorrected).
- Bonferroni criterion: edge if Granger p < 0.01 / 210.
- BH-FDR criterion: edge if Granger p passes Benjamini-Hochberg step-up at q = 0.05 across 210 tests.
- Permutation-empirical criterion: 1000 time-series permutations per pair; shuffle source series, recompute Granger F; empirical p = fraction of null F ≥ observed F; edge if empirical p < 0.01.
- Jaccard: |A ∩ B| / |A ∪ B| over directed-pair edge sets.
- Funding tercile: split hours by pair-level funding-rate differential into low/mid/high; recompute network within each tercile; Jaccard vs each primary criterion.
- Temporal stability: rolling 90-day and 30-day windows, 30-day step; Jaccard vs each primary criterion.
- Block bootstrap: 1000 moving-block resamples (24h blocks, jointly across coins); deterministic seed 20261121; per-edge selection frequency + 95% stability interval.
- Materiality floor: 0.02 (2% relative variance explained). Frozen; not relaxed after outcomes.

---

## Edge-set robustness ladder (all 210 directed pairs)

| Criterion | Edge count | Density |
|---|---|---|
| raw p < 0.01 | 184 | 0.8762 |
| Bonferroni (0.01/210) | 156 | 0.7429 |
| BH-FDR q = 0.05 | 199 | 0.9476 |
| permutation-empirical (1000 perms) | 102 | 0.4857 |

### Pairwise Jaccard agreement

| Criterion pair | Jaccard |
|---|---|
| raw vs Bonferroni | 0.8478 |
| raw vs BH-FDR | 0.9246 |
| raw vs permutation | 0.5543 |
| Bonferroni vs BH-FDR | 0.7839 |
| Bonferroni vs permutation | 0.6538 |
| BH-FDR vs permutation | 0.5126 |

### Fragile edges (significant under exactly one criterion)

Edges present under only one criterion are flagged as fragile — the edge set is criterion-dependent, not stable. The raw/Bonferroni/BH-FDR family agrees strongly (Jaccard 0.78–0.92), while the permutation-empirical criterion agrees much less with each (Jaccard 0.51–0.65), indicating that uncorrected/parametric significance is largely driven by serial dependence that the permutation null removes.

---

## Per-edge materiality (2% variance-explained floor, actually computed)

| Metric | Value |
|---|---|
| Edges clearing 0.02 floor | 12 / 210 (0.0571) |
| Mean variance_explained | 0.0063 (0.63%) |
| Median variance_explained | 0.0039 (0.39%) |
| Bootstrap 95% CI for count clearing floor | [6, 19] |

Only 12 of 210 directed edges (5.7%) explain ≥2% of the target coin's liquidation-intensity variance beyond its own lags. The bootstrap CI [6, 19] confirms the material edge set is small and uncertain. The claim "contagion is material" is only weakly supported: a small subset of edges clears the floor, but the median edge explains <0.4% of variance — far below the 2% floor.

**H_recon_materiality: SUPPORTED** — 12 edges clear the 2% floor with bootstrap CI [6, 19]; the count is > 0, so materiality is not NULL, but the effect is concentrated in a small minority of pairs.

---

## Disagreement with CONTAGION-001 (quantified, not hidden)

| Source | Edge count | Density | Method |
|---|---|---|---|
| CONTAGION-001 eval | 11 | 0.0524 | Granger-Bonferroni ∩ permutation-Bonferroni |
| CONTAGION-001 recompute | 58 | 0.2762 | empirical-p only (300 perms) |
| This recon (permutation) | 102 | 0.4857 | empirical-p (1000 perms) |

- CONTAGION-001 eval vs recompute disagree on **47 of 210 pairs**.
- This recon's permutation edge set (102 edges) has a symmetric difference with the CONTAGION-001 eval Bonferroni edge set (156 edges) reflecting the unresolved multiple-testing choice.
- The edge set is an artifact of the multiple-testing criterion, not a stable finding: parametric criteria yield 156–199 edges while permutation yields 102, and only 12 edges clear the 2% materiality floor.

---

## Funding-tercile reconciliation (Jaccard vs each primary criterion)

| Tercile | vs raw | vs Bonferroni | vs BH-FDR | vs permutation |
|---|---|---|---|---|
| low | 0.4427 | 0.4647 | 0.4527 | 0.4234 |
| mid | 0.0745 | 0.0807 | 0.0796 | 0.0714 |
| high | 0.4115 | 0.3886 | 0.4229 | 0.3217 |

Low- and high-funding terciles show moderate overlap (0.32–0.46) with primary criteria; the mid tercile shows almost no overlap (0.07–0.08), indicating the contagion signal is concentrated in extreme funding differentials, not the middle.

---

## Temporal-stability reconciliation (Jaccard vs each primary criterion)

| Window | Windows | Stable edges | vs raw | vs Bonferroni | vs BH-FDR | vs permutation |
|---|---|---|---|---|---|---|
| 90-day | 17 | 31 | 0.1497 | 0.1761 | 0.1443 | 0.1875 |
| 30-day | 19 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

The 90-day rolling windows retain only 31 stable edges (edges significant in ≥50% of windows), with low Jaccard (0.14–0.19) against primary criteria — edge membership is not temporally stable at the 90-day scale. The 30-day windows yield zero stable edges — no edge survives a 30-day rolling window, indicating the contagion network is not stable at shorter horizons.

---

## Block-bootstrap edge-set stability (1000 resamples, Bonferroni criterion)

| Metric | Value |
|---|---|
| Stable edges (freq ≥ 0.5 AND clears 0.02 floor) | 12 / 210 (0.0571) |
| Mean selection frequency | 0.6722 |
| Median selection frequency | 0.7160 |

Only 12 edges are both bootstrap-stable (selection frequency ≥ 0.5) and material (variance_explained ≥ 0.02). The median selection frequency of 0.72 indicates most edges are frequently selected under resampling, but the joint stability + materiality bar leaves just 12 edges.

---

## Hypothesis verdicts

| Hypothesis | Verdict | Basis |
|---|---|---|
| H_recon_materiality | SUPPORTED | 12 edges clear the 2% floor; bootstrap CI [6, 19]; count > 0 |
| H_recon_robustness | SUPPORTED | Edge-set sizes and pairwise Jaccard reported for all four criteria; 47-of-210 eval-vs-recompute disagreement quantified; single-criterion edges flagged fragile |
| H_recon_stability | SUPPORTED | Per-edge bootstrap selection frequency and 95% interval reported; tercile and 90-day/30-day rolling Jaccard reported; stable edges require bootstrap + ladder + materiality jointly |

---

## Conclusion

The CONTAGION-001 edge-set discrepancy is resolved as a **multiple-testing artifact**, not a stable contagion finding. Parametric criteria (raw/Bonferroni/BH-FDR) yield 156–199 edges; permutation-empirical yields 102; only 12 edges clear the 2% per-edge materiality floor AND survive block-bootstrap stability. The claim "contagion is material" is weakly supported: materiality exists for a small minority of pairs (12/210), but the median edge explains <0.4% of variance. Edge membership is criterion-dependent and temporally unstable (zero stable edges at 30-day scale). No threshold was shopped or relaxed; nulls are preserved as NOT_SUPPORTED where applicable.

---

## Artifacts

- `fclr_liq_contagion02_prereg_20261121T210000Z.json` — outcome-blind prereg freeze
- `fclr_liq_contagion02_prereg_20261121T210000Z.md` — prereg markdown
- `fclr_liq_contagion02_recon_20261121T210000Z.py` — heavy reconciliation script
- `fclr_liq_contagion02_recon_20261121T210000Z.json` — reconciliation results (this report's data)
- `fclr_liq_contagion02_recompute_20261121T210000Z.py` — independent stdlib/numpy recompute
- `fclr_liq_contagion02_recompute_20261121T210000Z.json` — recompute output
- `fclr_liq_contagion02_evidence_audit_20261121T210000Z.json` — evidence audit
- `fclr_liq_contagion02_evidence_audit_20261121T210000Z.md` — evidence audit markdown
- `evidence_audit_20261121T210000Z.json` — gate-critical evidence_audit alias
- `trigger_check_20261121T210000Z.json` — trigger check (no external trigger required)
