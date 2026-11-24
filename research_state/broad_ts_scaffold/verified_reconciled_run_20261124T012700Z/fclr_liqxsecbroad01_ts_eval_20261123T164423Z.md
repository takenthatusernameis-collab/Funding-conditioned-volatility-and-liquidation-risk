# FCLR-LIQ-XSEC-BROAD-TS-01 — Temporal Stability Evaluation

**Experiment ID:** FCLR-LIQ-XSEC-BROAD-TS-01
**Campaign:** FCLR-LIQ-XSEC-BROAD-TS-01-20261123T135825Z
**Session UTC:** 20261123T164423Z

## Question
Is the SUPPORTED broad-universe cross-sectional funding -> next-hour observed liquidation-intensity association (BROAD-01) temporally stable — not dominated by one time block — per RESEARCH_PROMPT.md section 17 condition #4?

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

## BROAD-01 fidelity reconciliation
- Long-arm mean rank-IC: 0.155133343457 (reference 0.155133343457; abs error 0)
- Long-arm Poisson deviance B1: 14895.300476998453 (reference 14895.300476998453; abs error 0)
- Reconciled within 0.001: True

## Headline (long arm, notional target)
- Mean cross-sectional Spearman rank-IC (C2, funding-conditioned): 0.155133
- Mean cross-sectional Spearman rank-IC (B1, RV-only baseline): -0.016519
- Poisson deviance B1: 14895.300477
- Poisson deviance C2: 14929.610988
- Relative improvement: -0.002303 (-0.2303%)
- Materiality floor: 2.0%, met: False

## Stability battery (primary arm: long)
- Sign reproduction fraction (long arm): 1.0000 (30/30 blocks positive), threshold 0.80
- Sign reproduced: True
- Rolling 6-block rank-IC: min=0.118543 median=0.153692 max=0.183882 CI95=[0.109359,0.197771]
- Ordered-block trend: rho=-0.369967 p_two_sided=0.048951 alpha=0.008333 not_reject=True
- First-half vs second-half gap: -0.033455 CI95=[-0.026532,0.026818] excludes_sign_reversal=False
- LOOIC range: 0.005220 [0.152453, 0.157673]
- RV-tercile frac positive: 0.4222
- UTC-bucket frac positive: 1.0000 (3/3)

## Multiplicity (Holm, 6-arm family, alpha_k=0.008333)
- Raw pvals: {"trend_test_long_arm": 0.048951, "first_second_half_gap_long_arm": 0.5085, "loio_range_long_arm": 0.0, "rolling_mean_min_long_arm": 0.0, "per_regime_rv_tercile_long_arm": 0.0, "per_regime_utc_bucket_long_arm": 0.0}
- Holm-adjusted pvals: {"loio_range_long_arm": 0.0, "rolling_mean_min_long_arm": 0.0, "per_regime_rv_tercile_long_arm": 0.0, "per_regime_utc_bucket_long_arm": 0.0, "trend_test_long_arm": 0.097902, "first_second_half_gap_long_arm": 0.5085}
- Primary significant after Holm: False

## Decision
- Sign reproduced: True
- Gap CI excludes sign reversal: False
- Trend not reject stationarity: True
- Verdict: NOT_STABLE
- Null preserved honestly: True

## Conclusion
The temporal stability of the cross-sectional funding -> next-hour observed liquidation intensity association on the broad 799-coin ironflow_bulk universe (2025-05..2026-10) is NOT_STABLE. This is a stability test of a cross-sectional association, NOT a time-series forecast gate pass and NOT an observed-liquidation census (capped feed).
