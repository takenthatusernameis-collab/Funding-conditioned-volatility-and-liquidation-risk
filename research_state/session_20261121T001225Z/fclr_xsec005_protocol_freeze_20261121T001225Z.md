# FCLR-XSEC-005 Protocol Freeze — Notional-Weighted Regime-Conditioned Cross-Sectional Funding Effect on Next-Hour Liquidation Intensity

**Experiment ID:** FCLR-XSEC-005-20261121T001225Z
**Session UTC:** 20261121T001225Z
**Protocol Path:** research_state/session_20261121T001225Z/fclr_xsec005_protocol_freeze_20261121T001225Z.md
**Panel:** research_state/fclr_liq_combined_panel_20261115T181405Z.parquet
**Panel SHA256:** 81a100d5d0625832bebabaabea13b786e15319577721cfe8507da5b779ec7f14
**Panel Hash Verified:** true
**Panel Frozen Before Target Generation:** true
**Outcome Data Inspected Before Freeze:** false

## Mechanism

UTC-hour / market-wide-RV conditioning of the funding effect applied to **NEXT-HOUR NOTIONAL-WEIGHTED OBSERVED LIQUIDATION INTENSITY** (sum of notional_usd, not event count) on the frozen combined metpie+ironflow panel; distinct estimand from FCLR-XSEC-004 count-based outcome.

## Estimand

`regime_conditioned_cross_sectional_funding_effect_on_next_hour_notional_weighted_liquidation_intensity`

## Distinct From

- FCLR-STARTER-001 (time-series 24h forward RV forecast, verdict NOT_SUPPORTED)
- FCLR-XSEC-001 (pooled within-hour cross-sectional funding contrast on RV, verdict NOT_SUPPORTED)
- FCLR-XSEC-002 (regime-conditioned funding contrast on next-hour RV, verdict SUPPORTED)
- FCLR-XSEC-003 (thin RV-only holdout, SUPERSEDED, never executed)
- **FCLR-XSEC-004 (regime-conditioned funding contrast on next-hour liquidation intensity, COUNT-BASED, verdict SUPPORTED)**
- FCLR-LIQ-COMBINED-PANEL (time-series 24h liquidation intensity QLIKE C2 vs B1, NOT_MET)
- FCLR-LIQ-XSEC-ORDERING (daily cross-sectional liquidation ordering, NOT_MET)
- FCLR-LIQ-XSEC-QLIKE (daily cross-sectional liquidation QLIKE, NOT_MET)
- TRACKA-HL-LIQ-XSEC (pooled cross-sectional funding IC on ironflow, EXPLORATORY_NULL)

## Panel Specification

- **Coins (15):** AAVE, ADA, AVAX, BNB, BTC, CRV, DOGE, ETH, LINK, LTC, NEAR, SOL, SUI, UNI, XRP
- **Time Span:** 2025-03-22T19:00:00Z .. 2026-10-31T22:00:00Z
- **Total Hours:** 10,052
- **Total Rows:** 1,740,415
- **Zero-Null Features:** true

## Regime Definition

- **Regime Variable:** Market-wide RV at hour t = cross-sectional mean of coin rv24h at t across coins present in hour t
- **Regime Split:** High vs low tercile of market-wide RV (middle tercile excluded)
- **Hour Eligibility:** Hours with fewer than 3 coins present are excluded from regime eligibility

## Predictor

- **Primary:** abs_fund_pct within-(hour, regime) cross-sectional rank
- **Split:** high_funding = top half of coins by rank, low_funding = bottom half within the same (hour, regime)

## Outcome

- **Primary (Notional-Weighted):** Next-hour NOTIONAL-WEIGHTED observed liquidation intensity per coin = sum of notional_usd over all observed liquidation events of that coin in the closed UTC hour t+1 (shift -1 within coin) — **DOLLAR SEVERITY, NOT EVENT COUNT**
- **Secondary (Count-Based, Cross-Reference Only):** Next-hour observed liquidation event count per coin

## Baseline (Specificity Control)

- Within-regime RV persistence: coin's own rv24h at t split high/low within (hour, regime) predicting next-hour notional-weighted liquidation intensity

## Inference

- **Alpha:** 0.05
- **Bootstrap Reps:** 2,000
- **Bootstrap Seed:** 20261121
- **Family Size:** 4
- **Family:** Regimes × {funding contrast, RV persistence baseline} = 2 regimes × 2 contrasts
- **Multiplicity Correction:** Holm
- **Materiality Floor:** 0.02
- **Materiality Definition:** abs(mean_diff_high_minus_low) / mean_abs_outcome over the regime's coin-hours, where mean_abs_outcome is the mean absolute next-hour notional-weighted liquidation intensity across the regime's coin-hours

## Gate Criteria (ALL must pass for SUPPORTED verdict)

1. CI excludes zero (for at least one funding contrast)
2. Holm passes (for that funding contrast)
3. Materiality floor met (for that funding contrast)
4. Minimum instruments represented
5. Adequate hours per regime

## Hard Constraints

- No holdout inspected before freeze
- No sealed protocol overwrite (research_state/research_protocol.md is sealed legacy FCLR-001 2024-01..03)
- No network, no paid/credentialed data
- No root-level artifacts in research_state/ (root md+json count 499/500, one more breaches churn cap)
- Do NOT re-run FCLR-STARTER-001, FCLR-XSEC-001, FCLR-XSEC-002, FCLR-XSEC-003, FCLR-XSEC-004
- Track separation: observed liquidations (Track A / this campaign) are never conflated with modeled boundary breaches (Track B) or with RV forecasts

## Cross-Reference

FCLR-XSEC-004 (count-based) found LOW-RV regime funding contrast SUPPORTED: CI [448605.26, 841155.73], p=0.0, Holm adj_p=0.0, materiality 0.80. HIGH-RV regime was an honest null. This campaign tests whether that finding survives a **notional-weighted (dollar severity)** outcome transform — i.e., does funding predict *how much* capital is liquidated, not just *how many* events fire.