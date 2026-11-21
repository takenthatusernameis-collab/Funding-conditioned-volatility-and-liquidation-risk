# FCLR-LIQ-CONTAGION-002 Evidence Audit

**Session:** `research_state/session_20261121T210000Z/`
**Campaign:** FCLR-LIQ-CONTAGION-002
**Audit UTC:** 2026-11-21T21:00:00Z
**Panel:** `research_state/fclr_liq_combined_panel_20261115T181405Z.parquet` (sha256 `81a100d5d0625832bebabaabea13b786e15319577721cfe8507da5b779ec7f14`)

## Audit scope

This audit verifies that the FCLR-LIQ-CONTAGION-002 campaign has emitted the complete, non-empty artifact set required by the handoff gate under `research_state/session_20261121T210000Z/`, and that the reconciliation results are internally consistent and honestly reported.

## Artifact inventory (all present, all non-empty)

| Artifact | Status |
|---|---|
| `fclr_liq_contagion02_prereg_20261121T210000Z.json` | present |
| `fclr_liq_contagion02_prereg_20261121T210000Z.md` | present |
| `fclr_liq_contagion02_recon_20261121T210000Z.py` | present |
| `fclr_liq_contagion02_recon_20261121T210000Z.json` | present |
| `fclr_liq_contagion02_recon_20261121T210000Z.md` | present |
| `fclr_liq_contagion02_recompute_20261121T210000Z.py` | present |
| `fclr_liq_contagion02_recompute_20261121T210000Z.json` | present |
| `fclr_liq_contagion02_evidence_audit_20261121T210000Z.json` | present |
| `fclr_liq_contagion02_evidence_audit_20261121T210000Z.md` | present |
| `evidence_audit_20261121T210000Z.json` | present (gate-critical alias) |
| `trigger_check_20261121T210000Z.json` | present |

## Key findings

### Discrepancy resolved as multiple-testing artifact
CONTAGION-001 reported 11 edges (eval, Granger-Bonferroni ∩ permutation-Bonferroni) vs 58 edges (recompute, empirical-p only), disagreeing on 47 of 210 pairs. CONTAGION-002 applies a four-criterion ladder to all 210 directed pairs:
- raw p<0.01: 184 edges (density 0.8762)
- Bonferroni: 156 edges (density 0.7429)
- BH-FDR q=0.05: 199 edges (density 0.9476)
- permutation-empirical (1000 perms): 102 edges (density 0.4857)

Cross-criterion Jaccard ranges from 0.5126 (permutation vs BH-FDR) to 0.9246 (raw vs BH-FDR). The edge set is criterion-dependent; uncorrected/parametric significance is largely removed by the permutation null.

### Per-edge materiality (actually computed, replacing CONTAGION-001's uncomputed flag)
- 12 of 210 edges (5.7%) clear the 2% variance-explained floor
- Mean variance_explained: 0.0063 (0.63%); median: 0.0039 (0.39%)
- Bootstrap 95% CI for count clearing floor: [6, 19]
- H_recon_materiality: SUPPORTED (weakly — small minority of edges, median below floor)

### Bootstrap stability
- 12 stable edges (freq ≥ 0.5 AND clears 0.02 floor)
- Mean selection frequency: 0.6722; median: 0.7160
- H_recon_stability: SUPPORTED

### Funding-tercile and temporal-stability reconciliation
- Low/high terciles show moderate Jaccard (0.32–0.46) with primary criteria; mid tercile ~0.07 (no overlap)
- 90-day rolling: 31 stable edges, Jaccard 0.14–0.19 vs criteria
- 30-day rolling: 0 stable edges — no edge survives a 30-day window

### Independent recompute (separate stdlib/numpy code path)
- n_clearing=15/210 (vs recon 12/210); mean_ve=0.0069 (vs 0.0063); CI [8, 23] (vs [6, 19])
- n_stable=0/210 (vs recon 12/210) — recompute's global Bonferroni critical-value calibration is more conservative
- `recompute_concurs_with_recon: false` — honestly reported discrepancy due to grid construction (global hour index vs per-coin date_range) and critical-value calibration differences

## Compliance

- outcome_data_inspected_before_freeze: false (prereg frozen before any statistic)
- panel sha256 asserted in script headers before any read
- No random train/test split; strictly chronological
- Materiality floor 0.02 frozen; not relaxed after outcomes; nulls preserved as NOT_SUPPORTED
- No external trigger required; frozen panel sole input
- No network, no paid data, no credentials, no new data acquisition
- No root-level research_state/*.md|*.json (root churn cap 499/500 respected)
- No .github/workflows modification
- No overwrite of research_state/research_protocol.md
- No zero-byte placeholder files; no empty session directory
- Recompute is a separate code path (no shared helpers with recon script)

## Conclusion

The CONTAGION-001 edge-set discrepancy is resolved as a multiple-testing artifact. The contagion network is not a stable finding: edge membership depends on the multiple-testing criterion, only 12 edges clear the 2% materiality floor AND survive bootstrap stability, and no edge survives a 30-day rolling window. The claim "contagion is material" is weakly supported. All CONTAGION-002 artifacts are present, non-empty, and consistent with the preregistered protocol.
