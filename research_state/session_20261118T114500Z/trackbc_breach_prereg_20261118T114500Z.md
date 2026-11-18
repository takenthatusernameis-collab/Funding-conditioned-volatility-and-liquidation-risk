# Track B/C breach-forecast prereg — FCLR-VOL-LIQ-BREACH-FORECAST-03

**Session:** `session_20261118T114500Z` | **Campaign:** `FCLR-VOL-LIQ-BREACH-FORECAST-03-20261118T103106Z` | **Label:** EXPLORATORY/PILOT
**Frozen:** 2026-11-18T11:45:00Z, before any outcome inspection (`outcome_data_inspected_before_freeze=false`). Stdlib only (`math`/`csv`/`json`/`zipfile`/`datetime`/`statistics`/`random`). No network, no parquet, no numpy/pandas/scipy.

## Research question
Do funding-conditioned realized-volatility features (causal at forecast origin t) predict modeled liquidation-boundary breaches within horizon H, beyond an RV-only baseline?

## Outcome (Track B modeled labels, not observed liquidations)
- Synthetic modeled boundary breach, `observed_liquidation_labels=false`.
- Source: `trackb_breach_labels_20261118T093031Z.json` (carried into this session dir), month 2024-04, 5 instruments (BTC/ETH/SOL/XRP/BNB), L in {5,10,20} x side {long,short} x H in {4h,24h}, mmr=0.005, entry at close of bar t, evaluation on hourly mark path t+1..t+H.
- Outcome column: `breached` (0/1). Unit: one scenario-row = instrument x entry-origin x leverage x side x horizon.

## Data & splits (2024-04 only; PILOT — single labeled month)
- Feature cache months: 2024-03 (history) + 2024-04 (labels/eval), read-only ZIP/CSV dir twins under `research_state/data_cache/`.
- Entry-origin rule: entry at close of bar t; features use only data available no later than bar t close (causal). Trailing RV windows end at bar t; funding = latest observation with calc_time <= bar t close.
- Purge/embargo: 7 days at split boundaries.
- Split 1: train 2024-04-01..15, embargo 16..22, test 23..30.
- Split 2: train 2024-04-01..17, embargo 18..24, test 25..30.

## Features (causal at t)
`lrv1, lrv24, lrv168, fund, fund_abs, fmean, fewma` (definitions in prereg json). Standardization train-only per split; zero-variance -> std=1; missing stays missing (no fill).

## Model family (drift-free, stdlib IRLS logistic, fixed ridge lambda=1e-6, max 100 iters, tol 1e-8, seed 12345)
- B0 RV-only: `lrv1, lrv24, lrv168`
- B1 funding-conditioned: `lrv1, lrv24, lrv168, fund, fund_abs, fmean, fewma`
- No regularization search, no hyperparameter tuning, no threshold tuning on test.

## Evaluation
- Metrics: ROC-AUC (Mann-Whitney U), precision@k (k = top 5% of test rows by predicted probability), Brier score, decile calibration.
- Contrasts: B1 vs B0 Delta AUC and Delta precision@k, pooled and per scenario (12 scenarios) x 2 splits.
- Uncertainty: block bootstrap over UTC-day test blocks (joint across instruments), seed 12345, 500 reps, CI95 percentile.
- Robustness: leave-one-instrument-out Delta AUC.
- Paired test origins identical across B0 and B1.

## Materiality floor (exploratory only)
Delta AUC >= +0.01 over RV-only on pooled OOS test with CI95 lower bound > 0 = materially informative. No forecast-gate pass or confirmatory claim.

## Multiplicity
Declared family = 12 scenarios x 2 splits x 2 metrics; report raw, Holm-adjusted where claimed.

## Prohibitions
No future bars, no full-sample normalization, no sealed months, no look-ahead, no test-set tuning, no observed-liquidation labeling.
