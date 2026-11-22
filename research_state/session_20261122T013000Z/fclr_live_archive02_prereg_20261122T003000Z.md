# FCLR-LIVE-ARCHIVE-02 Preregistration (outcome-blind, frozen before outcomes)

**Campaign:** FCLR-LIVE-ARCHIVE-02 (rank-0, gate-enforced)
**Session UTC:** 2026-11-22T00:30:00Z
**Artifact:** `fclr_live_archive02_prereg_20261122T003000Z.{json,md}`
**Status:** FROZEN_PRE_OUTCOMES
**outcome_data_inspected_before_freeze:** false

## Freeze assertion

This preregistration (hypotheses, targets, features, 3 chronological blocks, baselines, materiality floor, decision gates, source hashes, config hash) was frozen BEFORE any outcome on the downloaded archive data was computed. No holdout outcome, coefficient, or QLIKE value influenced any cutoff, feature, or threshold below.

## Research question

Do funding extremes + open-interest/taker-flow imbalance improve out-of-sample forecasts of next-24-hour realized variance over a realized-volatility-only baseline, on the previously unexploited Binance public archive (`data.binance.vision` metrics/fundingRate/markPriceKlines domain)?

## Primary hypothesis (H1)

Candidate C2 (RV + funding + OI + taker imbalance) achieves a >= 2% relative QLIKE reduction vs baseline B1 (RV-only HAR) on next-24-hour realized variance, averaged across 3 chronological test blocks, with uncertainty supporting improvement.

## Source domain (asserted hashes)

- metrics sample: `BTCUSDT-metrics-2025-06-15.zip` sha256=`8f6627d563531aa27c801d0085722f438865211052afa32d9b89752ddc7bd7e5`
- funding sample: `BTCUSDT-fundingRate-2025-06.zip` sha256_prefix=`d611a863`
- mark sample: `BTCUSDT-1h-2025-06.zip` sha256_prefix=`af4ef458`
- registry: `fclr_live_archive02_source_registry_20261122T003000Z.json`
- Source is unauthenticated, no credentials/payment/signup, deep history (2020 onward). `api.binance.com` REST returns HTTP 451 (not used).

## Universe / unit / forecast timestamp

- Universe: BTCUSDT (single contract; deep archive coverage)
- Unit: one eligible linear perpetual contract × one fully closed UTC hourly forecast timestamp t
- Forecast timestamp t is immediately after all data for closed hour t are available; every input available by t; outcomes begin with next hourly interval (t+1..t+24); no same-bar or future data enters a predictor

## Target (primary)

- next-24-hour realized variance = sum of squared 1-hour mark-price log returns from t+1 through t+24
- Secondary horizons (registered, not promoted): 6h, 72h, 168h

## Features (all causal, computed at t, data ending no later than t)

- RV1h, RV24h, RV168h: trailing realized variances from hourly mark-price log returns
- signed funding: latest funding observation available by t (sign retained)
- abs funding extremeness: percentile rank of |funding| vs preceding 90 calendar days only; require >= 30 valid historical funding observations before emitting
- sum_open_interest: latest daily value available by t
- sum_taker_long_short_vol_ratio: latest daily value available by t
- mark/index premium: NOT available in this download (indexPriceKlines not fetched); recorded as missing, never zero-filled

## Missing-data rule

Missing features remain missing; never zero-filled or forward-filled to make models comparable. Common eligible rows across compared models.

## Chronological blocks (frozen)

| Block | Start (UTC) | End (UTC) | Purpose |
|-------|-------------|-----------|---------|
| train | 2025-06-01T00:00:00Z | 2025-06-30T23:00:00Z | fit B0/B1/C2 parameters (train-only scaling) |
| embargo | 2025-07-01T00:00:00Z | 2025-07-07T23:00:00Z | 7-day purge/embargo at train/test boundary |
| test block 1 | 2025-07-08T00:00:00Z | 2025-07-21T23:00:00Z | out-of-sample evaluation block 1 (14 days) |
| test block 2 | 2025-07-22T00:00:00Z | 2025-08-04T23:00:00Z | out-of-sample evaluation block 2 (14 days) |
| test block 3 | 2025-08-05T00:00:00Z | 2025-08-18T23:00:00Z | out-of-sample evaluation block 3 (14 days) |

Embargo: 7 calendar days at the train/test boundary; no target interval overlaps training/validation/test folds.

## Models

- B0 persistence baseline: forecast next-24h RV = preceding RV24h
- B1 realized-volatility-only HAR: OLS log(RV+1e-12) ~ log RV1h + log RV24h + log RV168h; train-only standardization; Duan smearing back-transform; eps=1e-12 fixed in advance
- C2 funding+OI+taker candidate: B1 + signed funding + abs funding percentile + sum_open_interest + sum_taker_long_short_vol_ratio; same fitting procedure

## Metric

- Primary: QLIKE = mean(ratio - 1 - log(ratio)), ratio = y / pred, y>0, pred>0
- Secondary: MAE, RMSE on stated target

## Materiality floor (frozen in advance)

>= 2% relative QLIKE reduction (C2 vs B1) required to pass the practical-improvement condition; not relaxed after outcomes.

## Multiplicity

Primary contrast C2 vs B1. Secondary contrasts C1 vs B1 and C2 vs C1 declared in the same family; raw and adjusted results disclosed.

## Decision gate

CONFIRMED requires: (a) paired QLIKE difference supports C2 improvement, (b) relative reduction >= 2% materiality floor, (c) uncertainty interval supports improvement across blocks, (d) no unresolved leakage/source/label/timestamp defect. Otherwise NOT_SUPPORTED or INCONCLUSIVE; null results preserved.

## Liquidation-label rule

No observed liquidation labels exist on this source (no liquidationSnapshot dataset). Any liquidation-risk statement is a modeled proxy (OI + taker imbalance + mark dislocation), labeled LIQUIDATION_RISK_PROXY, never an observed liquidation. Track A (observed liquidation labels) is NOT_SUPPORTED on this source.

## Safeguards

No look-ahead; no survivorship substitution; no forward fill; stdlib-only computation (numpy/pandas/scipy not installed in runner).
