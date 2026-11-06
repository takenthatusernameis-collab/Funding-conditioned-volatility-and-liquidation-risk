# Research Protocol (FROZEN - Pre-Holdout)

**Frozen:** 2026-11-06T20:36:32Z
**Repo:** Funding-conditioned-volatility-and-liquidation-risk

## Hypothesis
Do funding extremes, realized volatility, and pre-specified price dislocation/smoothing features improve out-of-sample forecasts of future realized volatility/stress and hypothetical liquidation-boundary crossings vs RV-only baseline?

## Universe
Initial: BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT (USD-M perpetuals), 2024-01 to 2024-03. Expand if coverage permits. Use venue-native archival coverage; do not assume surviving symbols represent full history.

## Data Sources (Admissible)
- Binance public archive (local zips): klines (1h), fundingRate, indexPriceKlines, markPriceKlines, premiumIndexKlines. Access: unauthenticated. See data_source_registry.json.

## Features (computed with info at forecast time)
Funding: signed funding rate, |funding|, trailing funding percentile/standardized (rolling train-only), time-to-next-funding if knowable.
RV: trailing RV 6h/24h/168h, RV24/RV168 ratio.
Price: perpetual premium vs index, mark-to-index, mark-to-last, deviation from trailing MA/EMA, lagged returns.

## Targets
1. Forward RV over 6h, 24h, 72h, 7d (primary)
2. Hypothetical long/short liquidation boundary breach within horizon under disclosed assumptions (Track B) - separate from observed liquidations
3. Observed liquidations (Track A) only if admissible high-coverage labels exist

## Baselines
B1: Persistence (lagged RV)
B2: RV-only (HAR-style where feasible)

## Evaluation
- Chronological walk-forward or expanding window. No random split.
- Purge/embargo >= max horizon.
- Train-only normalization for all features/thresholds.
- Sealed final holdout (boundaries set from coverage before evaluation).
- Metrics: QLIKE (primary for RV), MAE/RMSE, block-aware CIs. For binary: Brier/log loss, calibration, precision-recall.
- Multiple comparisons corrected (Holm). Report raw+adjusted.

## Decision Gates
- Gate 1 (Data): Loadable samples with normalized UTC timestamps.
- Gate 2 (Protocol): Frozen before holdout examination.
- Gate 3 (RV-only baseline): OOS RV-only meets sanity checks; results recorded in evaluation_summary.md with run_manifest.json.
- Gate 4 (Incremental): Only after Gate 3, test funding+price ablations vs RV-only.

## Constraints
No trading/paper/live, no credentials/paid data, no workflow changes under .github/workflows, separate Track A/B/C, preserve negatives.
