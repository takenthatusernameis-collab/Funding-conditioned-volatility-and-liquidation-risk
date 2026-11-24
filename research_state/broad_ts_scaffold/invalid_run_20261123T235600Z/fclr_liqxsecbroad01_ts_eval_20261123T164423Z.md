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

## Headline (long arm, notional target)
- Mean cross-sectional Spearman rank-IC (C2, funding-conditioned): -0.145444
- Mean cross-sectional Spearman rank-IC (B1, RV-only baseline): -0.159122
- Poisson deviance B1: 13322.576514
- Poisson deviance C2: 13183.942181
- Relative improvement: 0.010406 (1.0406%)
- Materiality floor: 2.0%, met: False

## Stability battery (primary arm: long)
- Sign reproduction fraction (long arm): 0.1000 (3/30 blocks positive), threshold 0.80
- Sign reproduced: False
- Rolling 6-block rank-IC: min=-0.235969 median=-0.157937 max=-0.065962 CI95=[-0.315691,0.008258]
- Ordered-block trend: rho=-0.055840 p_two_sided=0.776224 alpha=0.008333 not_reject=True
- First-half vs second-half gap: -0.001818 CI95=[-0.097210,0.098281] excludes_sign_reversal=False
- LOOIC range: 0.020937 [-0.154814, -0.133876]
- RV-tercile frac positive: 0.1000
- UTC-bucket frac positive: 0.0000 (0/1)

## Multiplicity (Holm, 6-arm family, alpha_k={ALPHA_K:.6f})
- Raw pvals: {"trend_test_long_arm": 0.776224, "first_second_half_gap_long_arm": 0.512, "loio_range_long_arm": 1.0, "rolling_mean_min_long_arm": 1.0, "per_regime_rv_tercile_long_arm": 1.0, "per_regime_utc_bucket_long_arm": 1.0}
- Holm-adjusted pvals: {"first_second_half_gap_long_arm": 1.0, "trend_test_long_arm": 1.0, "loio_range_long_arm": 1.0, "rolling_mean_min_long_arm": 1.0, "per_regime_rv_tercile_long_arm": 1.0, "per_regime_utc_bucket_long_arm": 1.0}
- Primary significant after Holm: False

## Decision
- Sign reproduced: False
- Gap CI excludes sign reversal: False
- Trend not reject stationarity: True
- Verdict: NOT_STABLE
- Null preserved honestly: True

## Conclusion
The temporal stability of the cross-sectional funding -> next-hour observed liquidation intensity association on the broad 799-coin ironflow_bulk universe (2025-05..2026-10) is NOT_STABLE. This is a stability test of a cross-sectional association, NOT a time-series forecast gate pass and NOT an observed-liquidation census (capped feed).
