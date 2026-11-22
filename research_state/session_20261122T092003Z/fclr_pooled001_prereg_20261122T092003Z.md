# FCLR-POOLED-001 Outcome-Blind Prereg Freeze

Session UTC: 20261122T092003Z
Campaign: FCLR-POOLED-001-20261122T040000Z (rank-0, gate-enforced)
outcome_data_inspected_before_freeze: false
frozen_before_outcomes: true

## Design
Pooled chronological out-of-sample confirmatory design on on-disk ironflow bulk data.
Data: research_state/data_cache/ironflow_bulk/, 18 months 2025-05..2026-10.
Sha256 sidecars asserted before reading; caches not modified.

## Hypotheses
- H1: C2 (RV+funding+premium+OI) beats B1 (RV-only) on 24h forward RV QLIKE OOS
- H2: Funding-conditioned QLIKE differs by funding tercile (train thresholds)
- H3: Funding tercile predicts high forward liquidation intensity (Brier skill vs climatology)

## Targets
- Primary: next-24h forward realized variance of mark-price returns (QLIKE)
- Secondary: 6h, 72h, 168h forward RV horizons
- Liquidation risk: binary forward liq notional > train median per market-hour

## Features
- B1 baseline: RV24h_t
- C2 candidate: RV24h_t + signed funding + mark/index premium + open interest
- Standardization: train-only mean/std; zero-variance columns -> 1.0

## Splits
- Train: first 70% of hours; Purge/embargo: 24h; Test: remaining hours
- Funding tercile thresholds from TRAIN only

## Estimation
OLS on log(fwd_RV24h + 1e-12); Duan smearing factor on train

## Inference
Per-coin day-block bootstrap (N=2000, seed=20261122); Diebold-Mariano with day-block variance

## Decision Gates
- Materiality floor: 2.0% relative QLIKE reduction
- GO rule: rel QLIKE C2-vs-B1 <= -2.0% AND bootstrap CI95 upper bound < 0
- Otherwise: NOT_SUPPORTED; no threshold-shopping after outcomes

## Software
stdlib + pyarrow only; numpy/pandas/scipy not used
