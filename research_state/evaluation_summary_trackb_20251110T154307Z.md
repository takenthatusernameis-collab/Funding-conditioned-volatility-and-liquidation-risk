# Evaluation Summary (TRACKB-20251110T154307Z)

Experiment: TRACKB-20251110T154307Z (Track B modeled boundary breaches)
Campaign: TRACKB-MODELED-BREACH-20261110T154307Z
Data range: 2025-01-01 .. 2025-10-31
Generated: 2026-11-10T16:08:55Z
Proxy: synthetic boundary proxy ≠ observed liquidations

## Splits (frozen before outcomes)
- Train: 2025-01-01T00:00:00Z .. 2025-05-02T00:00:00Z (40%)
- Val: 2025-05-09T00:00:00Z .. 2025-07-02T00:00:00Z (20%)
- Test: 2025-07-09T00:00:00Z .. 2025-10-31T23:00:00Z (40%) [7d embargo/purge]

## Configuration
- Primary target: synthetic_boundary_breach_24h_5x_long_m0 (leverage=5.0, side=long, maintenance_margin_rate=0.0, horizon=24h)
- Baseline B1: price/RV-only features
- Model C2: funding-conditioned features
- Primary contrast: C2 vs B1

## Test set results (modeled proxy)

- BTCUSDT: n_test_obs=2736, synthetic_breach_rate=0.000000
- ETHUSDT: n_test_obs=2736, synthetic_breach_rate=0.000000
- BNBUSDT: n_test_obs=2736, synthetic_breach_rate=0.000000
- SOLUSDT: n_test_obs=2736, synthetic_breach_rate=0.000000
- XRPUSDT: n_test_obs=2712, synthetic_breach_rate=0.008850
- Total: n_instruments=5, n_obs=13656, n_test_blocks=3

## Paired comparisons (block bootstrap, 2000 replications)

### C2_vs_B1 (primary)
- Paired n: 13656
- Mean diff (modelA - modelB), synthetic breach classification metric: 0.015000 (95% CI [-0.005000, 0.035000])
- Relative improvement: 1.50%

## Gate assessment (primary contrast C2 vs B1)

- >=5 instruments: PASS (5)
- >=3 non-overlapping 30-day blocks in test: PASS (3)
- >=2% relative improvement (materiality): NOT_MET (1.50%)
- 95% CI excludes null in favorable direction: NOT_MET (CI [-0.005000, 0.035000])
- Holm multiplicity (pre-specified contrasts): APPLIED (see protocol)
- Forecast/gate (all criteria): NOT_MET

## Notes
- All results use frozen splits only; no tuning on holdout.
- synthetic_boundary_label uses only prices strictly after t_index (t+1..t+horizon); no leakage.
- Modeled breach proxy only. NOT observed liquidations. No risk overlay until gate passes.
- Provenance verified: provenance_verified=true, unmapped_count==0 (adjacent sha256 sidecars).
