# FCLR-LIVE-ARCHIVE-08 Preregistration — session_20261128T040000Z

**Campaign:** FCLR-LIVE-ARCHIVE-08-20261127T131654Z (Track-B modeled boundary-breach forecast)
**Session:** session_20261128T040000Z
**Generated:** 2026-11-28T04:00:00Z
**Experiment ID:** FCLR-LIVE-ARCHIVE-08

## Freeze flags

- outcome_data_inspected_before_freeze: false
- frozen_before_outcomes: true
- decision_frozen_before_outcomes: true

## Hypothesis

FCLR-H008: funding-conditioned price features improve out-of-sample forecasts of modeled hypothetical long/short liquidation-boundary breaches within a fixed horizon beyond a mark-price-only baseline on the disjoint 2024-04..2026-10 cohort, judged on out-of-sample AUC/log-loss/Brier.

## Window

2024-04-01..2026-10-31 UTC

## Symbols

BNBUSDT, BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT

## Common support

N: 22608 (all five symbols have markPriceKlines close>0 at each UTC hourly timestamp)

## Target

Whether future mark-price path breaches pre-registered hypothetical long/short liquidation boundary within fixed horizon (Track-B modeled boundary-breach proxy, never observed liquidation).
- Horizon: 24 hours
- Boundaries: derived from disclosed constant margin/leverage scenarios (not data-driven)
- Labels: separate long/short breach labels per horizon; modeled proxy only

## Splits

60/20/20 by unique UTC timestamp on S; 168h purge/embargo; test -> 3 chronological blocks
- train_ts: 13550
- val_ts: 4517
- test_ts: 4517
- test_rows_across_5_symbols: 22585

## Models

- B1: mark-price-only baseline (RV1h, RV24h, RV168h features), train-only scaling
- C2: funding-conditioned (signed funding(24h), trailing 90d |funding| pct, mark/index premium, mark/EMA24 distance + mark price), train-only scaling

## Primary contrast

C2 vs B1 on paired test-set out-of-sample AUC / log-loss / Brier

## Inference

>=2000 deterministic block-bootstrap replicates (block=24 rows, seed=20261126); leave-one-symbol-out (5 symbols)

## Materiality floor

0.02

## Alpha spending

Sequential look k=2 under RESEARCH_PROMPT section 17; alpha_2 = 0.05/(2×3) = 0.008333

## Decision rule

FORECAST_GATE_PASSED iff C2 vs B1 improves on primary target AND materiality floor met AND CI supports improvement; else NOT_SUPPORTED / INCONCLUSIVE; symmetric verdict only

## Leakage controls

- Outcome-blind freeze before target generation
- Train-only model fitting and train-only standardization
- 168h purge/embargo between train/val/test
- No outcome inspection before design freeze
- Read-only cache reuse; no re-download; stdlib only; no network

## Status

stdlib_only: true
network: false
read_only_cache: true
not_an_overlay: true

## Note

Outcome-blind prereg frozen before any outcome computation. Track-B modeled boundary-breach forecast (NOT a risk overlay; campaign-07 forecast gate did NOT pass, so per RESEARCH_PROMPT section 9 no risk overlay is authorized).
