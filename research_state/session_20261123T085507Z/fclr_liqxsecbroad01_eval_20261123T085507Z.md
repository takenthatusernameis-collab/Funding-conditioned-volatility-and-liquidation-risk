# FCLR-LIQ-XSEC-BROAD-01 — Broad-Universe Cross-Sectional Evaluation

**Experiment ID:** FCLR-LIQ-XSEC-BROAD-01
**Campaign:** FCLR-LIQ-XSEC-BROAD-01-20261123T080000Z
**Session UTC:** 20261123T085507Z

## Label construct (observed ironflow liquidations, capped-sample feed)
- Per-coin per-hour next-hour observed liquidation intensity (count + notional), long/short separate
- Capped-sample feed: absence != zero; claims restricted to presence/intensity ordering
- Horizon: 1h; Dedup: wallet-level by tx_hash

## Universe
- Test coins: 799 (survivor: 637, exited: 162)
- Test rows: 1715710, Liquidation rows: 2849452
- Test blocks (168h non-overlapping): 30 (valid: 30)

## Input integrity
- SHA-256 sidecars verified: 72/72 (bad=0)

## Headline (long arm, notional target)
- Mean cross-sectional Spearman rank-IC (C2, funding-conditioned): 0.155133
- Mean cross-sectional Spearman rank-IC (B1, RV-only baseline): -0.016519
- Poisson deviance B1: 14895.300477
- Poisson deviance C2: 14929.610988
- Relative improvement (baseline-candidate)/baseline: -0.002303 (-0.2303%)
- Sign convention: (baseline - candidate) / baseline, positive = candidate better
- Materiality floor: 2.0%, met: False

## Headline (short arm, notional target)
- Mean cross-sectional Spearman rank-IC (C2): -0.002054
- Poisson deviance B1: 13423.736369, C2: 13328.791641
- Relative improvement: 0.007073 (0.7073%), materiality met: False

## Uncertainty (per-coin block bootstrap, N=2000)
- Bootstrap valid: 2000
- CI95: [0.142081, 0.168895]
- CI95 excludes null in favorable direction: True

## Placebo / permutation null (N=1000)
- Placebo valid: 1000
- Placebo 95th percentile: 0.001260
- True effect exceeds 95th percentile of null: True

## Leave-one-instrument-out (8 subsets, >=6 pass)
- LOIO valid: 8, sign reproduced: 8, pass: True

## Multiplicity (Holm, 6-family, alpha_k={ALPHA_K:.6f})
- Raw pvals: {"RV_tercile_arm": 0.0, "UTC_bucket_arm": 0.0, "count_target": 0.0, "notional_target": 0.0, "long_side": 0.0, "short_side": 0.0}
- Holm-adjusted pvals: {"RV_tercile_arm": 0.0, "UTC_bucket_arm": 0.0, "count_target": 0.0, "notional_target": 0.0, "long_side": 0.0, "short_side": 0.0}
- Primary significant after Holm: True

## Decision
- Narrow-universe sign reproduced: True
- CI95 excludes null favorable: True
- Primary significant after Holm: True
- Verdict: SUPPORTED_GENERALIZATION
- Null preserved honestly: False
- No threshold shopping: true; No relaxed materiality floor: true; No overlay built: true

## Conclusion
The cross-sectional funding -> next-hour observed liquidation intensity association, tested on the broad 799-coin ironflow_bulk universe (2025-05..2026-10), yields a mean rank-IC of 0.155133 (long arm). Verdict: SUPPORTED_GENERALIZATION. This is a cross-sectional generalization test, NOT a time-series forecast gate pass and NOT an observed-liquidation census (capped feed).
