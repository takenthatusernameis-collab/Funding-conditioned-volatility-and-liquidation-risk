# Track A confirmatory preregistration (registration only — frozen, no evaluation)

- campaign: `FCLR-LIQ-TRACKA-EXTENSION-01-20261119T015256Z`
- session: `session_20261119T022824Z`
- artifact: `fclr_tracka_confirmatory01_prereg_20261119T022824Z`
- parent verdict: Track A extension admissibility ADMISSIBLE (g1..g7 PASS over 2025-11..2026-10)
- frozen_before_outcomes: true
- outcome_target_inspected_before_freeze: false
- registration_only: true
- confirmatory_evaluation_run: false

## Source (unchanged)
- ironflow/hyperliquid-liquidations (CC BY 4.0, unauthenticated), hyperliquid_perpetuals main dex
- dex == "" AND market_class == "perp"
- 13 coins: BTC, ETH, BNB, SOL, XRP, AVAX, DOGE, LINK, SUI, ARB, OP, APT, ADA
- Window: 2025-11 .. 2026-10

## Splits (frozen month boundaries, non-overlapping, chronological)
- block_1 test: 2025-11-01 .. 2025-12-31 (61 days); purge_1: 2026-01-01 .. 2026-01-31 (31 days)
- block_2 test: 2026-02-01 .. 2026-04-30 (89 days); purge_2: 2026-05-01 .. 2026-05-31 (31 days)
- block_3 test: 2026-06-01 .. 2026-08-31 (92 days)
- reserve: 2026-09-01 .. 2026-10-31 (held out, not part of the three confirmatory test blocks)
- Each block >= 60 days; purges >= 20 days; no reshuffling; each block carries pre-test training history from earlier time only.

## Label
- Observed liquidation incidence per (coin, hour_utc): liq_count, liq_notional_usd (+ long/short split)
- OI-normalized variant by contemporaneous open_interest_usd
- Absence from feed is not evidence of no liquidation (missing/unknown, not zero)
- Forecast origin t = closed hour t; outcomes begin t+1; predictors lagged >= 1h

## Features (lagged >= 1h, no look-ahead)
- funding_rate, funding_sign, funding_level, premium, mark-price realized volatility, OI change

## Models & baselines
- intercept-only, funding-only, RV-only, funding x RV interaction
- Simple calibrated logistic baseline for event labels; no booster, no NN

## Metrics
- Brier score (headline, frozen), log-loss, AUC, calibration slope/intercept
- Placebo: label-hour permutation null
- Holm correction over declared family

## Power
- MDE derived from block sizes (61d / 89d / 92d)
- If MDE exceeds plausible effect -> UNDERPOWERED, do not run

## Gate
- Pre-defined support vs honest-negative result; no post-hoc metric addition

## Prohibitions
- No confirmatory evaluation in this campaign (registration only).
- No sealed Binance months for outcomes.
- No re-run of RISK-05/06/07, ROBUST-05, Track C QLIKE.
- No post-hoc metric addition; no statsmodels/numpy in core path.
