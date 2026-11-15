# FCLR-LIQ-XSEC-QLIKE PREREGISTRATION — 20261115T214903Z

**Frozen (UTC):** 2026-11-15T21:49:03Z
**Experiment ID:** `FCLR-LIQ-XSEC-QLIKE-20261115T214903Z`
**Class:** CONFIRMATORY (promotable=False)
**outcome_data_inspected_before_freeze:** `false`

## Estimand

- **Target:** next-day liquidation intensity per coin (daily total notional_usd)
- **Primary metric:** mean daily cross-sectional QLIKE (lower is better)
- **Metrics:** mean daily cross-sectional QLIKE, mean daily Spearman rank-IC, top-3 hit-rate
- **Primary metric for materiality:** mean daily cross-sectional QLIKE
- **Contrast:** C2 vs B1; **Materiality floor:** 2.0% relative improvement (C2 lower QLIKE loss)
- **QLIKE:** qlike(y, yhat) = y/yhat - ln(y/yhat) - 1; paired diff (C2 - B1) < 0 favours C2
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

- **Train:** 2025-03-22..2025-05-21 (panel-origin expanding-window train; block1 train window is empty (panel starts 2025-03-22) so block 1 is train-limited by design)
- **Validation:** 2025-05-22..2025-09-30
- **Embargo:** 7 days
- **Test block 1:** 2025-03-22..2025-04-21 (PRISTINE_METPIE)
- **Test block 2:** 2025-04-21..2025-05-21 (PRISTINE_METPIE)
- **Test block 3:** 2025-10-01..2025-10-31 (IRONFLOW_ESTIMAND_NOVEL)

## Gate

- mean_daily_cross_sectional_qlike_C2_vs_B1 relative improvement >= 2.0% (C2 lower loss)
- block_bootstrap 95% CI hi < 0 for paired diff (C2-B1) on primary QLIKE (excludes zero in favorable direction)
- n_paired_instruments >= 5
- n_test_blocks_with_data >= 3

**Verdict space:** ['PASS', 'NOT_MET']

## Hard constraints

- No outcome peeking or threshold tuning before/after freeze.
- No sealed artifact mutation; no paid/credentialed/manual data; no network for outcomes.
- H2_shek_replication remains EXPLORATORY_ONLY (promotable=false).
- NOT_MET is recorded honestly; next materially different heavy cell installed if NOT_MET.
