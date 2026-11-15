# FCLR-LIQ-XSEC-ORDERING PREREGISTRATION — 20261115T203501Z

**Frozen (UTC):** 2026-11-15T20:35:01Z
**Experiment ID:** `FCLR-LIQ-XSEC-ORDERING-20261115T203501Z`
**Class:** CONFIRMATORY (promotable=False)
**outcome_data_inspected_before_freeze:** `false`

## Estimand

- **Target:** next-day liquidation intensity per coin (daily total notional_usd)
- **Ordering metric:** Spearman rank correlation (predicted vs realized next-day intensity)
- **Metrics:** mean daily Spearman rank-IC, top-3 hit-rate, cross-sectional QLIKE
- **Primary metric for materiality:** mean daily Spearman rank-IC
- **Contrast:** C2 vs B1; **Materiality floor:** 2.0%
- **Min instruments:** 5; **Min test blocks:** 3; **Block bootstrap:** 2000 reps (seed 20261115)
- **Purge/embargo:** 7 days; **Walk-forward:** expanding window

## Universe

- 15 Hyperliquid coins: AAVE, ADA, AVAX, BNB, BTC, CRV, DOGE, ETH, LINK, LTC, NEAR, SOL, SUI, UNI, XRP
- Source: combined metpie (2025-03-22..2025-05-25) + ironflow (2025-05-25..2026-10-31) observed liquidation events

## Features

- **B1:** ['rv24h', 'rv168h']
- **C2:** ['rv24h', 'rv168h', 'fundingRate', 'abs_fund_pct', 'premium', 'ema_dist']
- All features are causal (past-only as-of joins) at the event->daily aggregation grain. Funding features are the last funding timestamp <= event; RV features are 4h-candle rolling std over past bars.

## Splits

- **Train:** 2025-03-22..2025-08-31 (PRISTINE blocks 0-1 + ESTIMAND_OVERLAP blocks 2-4 (estimand-novel for the combined panel))
- **Validation:** 2025-09-01..2025-09-30
- **Embargo:** 7 days
- **Test block 1:** 2025-10-01..2025-10-31 (PRISTINE_ADJACENT_ESTIMAND_NOVEL)
- **Test block 2:** 2026-01-01..2026-01-31 (IRONFLOW_ESTIMAND_NOVEL)
- **Test block 3:** 2026-09-01..2026-09-30 (IRONFLOW_ESTIMAND_NOVEL)

## Gate

- mean_daily_spearman_rank_ic_C2_vs_B1 >= 2.0% (relative improvement)
- block_bootstrap_ci_hi < 0 (excludes zero in favorable direction for primary metric)
- n_paired_instruments >= 5
- n_test_blocks_with_data >= 3

**Verdict space:** ['PASS', 'NOT_MET']

## Hard constraints

- No outcome peeking or threshold tuning before/after freeze.
- No sealed artifact mutation; no paid/credentialed/manual data; no network for outcomes.
- H2_shek_replication remains EXPLORATORY_ONLY (promotable=false).
- NOT_MET is recorded honestly; next materially different heavy cell installed if NOT_MET.
