# Evaluation Summary (trackb_TB1_20261110T173838Z)

Experiment: trackb_TB1_20261110T173838Z (Track B modeled boundary breaches)
Campaign: TRACKB-MODELED-BREACH-TB1-20261110T173838Z
Data range: 2025-01-01 .. 2026-10-31
Generated: 2026-11-10T18:05:00Z
Proxy: synthetic boundary proxy ≠ observed liquidations

## Splits (frozen before outcomes)
- Train: 2025-01-01T00:00:00Z .. 2026-02-05T00:00:00Z (60%)
- Val: 2026-02-12T00:00:00Z .. 2026-06-19T00:00:00Z (20%)
- Test: 2026-06-26T00:00:00Z .. 2026-10-31T23:00:00Z (20%) [7d embargo/purge]

## Configuration
- Primary target: synthetic_boundary_breach_h24_long_5x_m0 (leverage=5.0, side=long, maintenance_margin_rate=0.0, horizon=24h)
- Baseline B1: RV features only (log rv1h, log rv24h, log rv168h)
- Model C2: B1 + funding features (signed_funding, abs_fund_pct) + prem + ema_dist
- Primary contrast: C2 vs B1
- Primary metrics: Log Loss, Brier Score (lower is better)
- Materiality floor: >= 2% relative improvement
- Block bootstrap replications: 2000
- Block size: 30 days (720 hours)
- Multiplicity: Holm correction across 2 pre-specified metrics (alpha=0.025 per metric)

## Test set results (modeled proxy)

- BTCUSDT: n_test_obs=3000, synthetic_breach_rate=0.000000
- ETHUSDT: n_test_obs=3000, synthetic_breach_rate=0.000000
- BNBUSDT: n_test_obs=3000, synthetic_breach_rate=0.000000
- SOLUSDT: n_test_obs=3000, synthetic_breach_rate=0.000000
- XRPUSDT: n_test_obs=3000, synthetic_breach_rate=0.000000
- Total: n_instruments=5, n_obs=14977, n_test_blocks=4

## Critical finding: DEGENERATE TEST SET
The frozen test split (2026-06-26 .. 2026-10-31) contains **ZERO synthetic boundary breaches** across all 5 instruments. The label distribution is entirely negative (prevalence = 0.0000%). This makes the binary classification task degenerate — both models trivially predict "no breach" with near-perfect accuracy, rendering comparative metrics meaningless.

Full-window breach rates (for context):
- BTCUSDT: 0/19848 (0.0000%)
- ETHUSDT: 33/19848 (0.1663%)
- BNBUSDT: 2/19848 (0.0101%)
- SOLUSDT: 11/19848 (0.0554%)
- XRPUSDT: 60/19824 (0.3027%)

The test period simply does not contain the extreme 24-hour price moves required to breach a 5x long liquidation boundary (20% adverse move). The synthetic label design with leverage=5.0 and H=24 produces events so rare that a randomly selected 4-month test window can easily have zero events.

## Paired comparisons (block bootstrap, >=2000 replications) — NOT INTERPRETABLE

### C2_vs_B1 (primary)
- Test n: 14977
- B1 Log Loss: 0.000613, C2 Log Loss: 0.000603
- Diff (C2-B1) Log Loss: -0.000010 (95% CI [-0.000030, 0.000006])
- Relative improvement (Log Loss): 1.58% (NOT interpretable — degenerate labels)
- B1 Brier Score: 0.000001, C2 Brier Score: 0.000001
- Diff (C2-B1) Brier: -0.000000
- Relative improvement (Brier): 9.47% (NOT interpretable — degenerate labels)

## Gate assessment (primary contrast C2 vs B1)

- >=5 instruments: PASS (5)
- >=3 non-overlapping 30-day blocks in test: PASS (4)
- >=2% relative improvement (Log Loss): NOT_MET (1.58%) — metric uninterpretable
- >=2% relative improvement (Brier): NOT_MET (metric uninterpretable due to zero events)
- 95% CI excludes null in favorable direction (Log Loss): NOT_MET — CI [-0.000030, 0.000006] crosses zero; also metric uninterpretable
- Holm multiplicity (pre-specified metrics): APPLIED (alpha=0.025 per metric)
- Forecast/gate (all criteria): **NOT_MET** — test set has zero positive labels, making confirmatory evaluation impossible

## Notes
- All results use frozen splits only; no tuning on holdout.
- synthetic_boundary_label uses only prices strictly after t_index (t+1..t+horizon); no leakage.
- Modeled breach proxy only. NOT observed liquidations. No risk overlay until gate passes.
- Provenance verified: provenance_verified=true, unmapped_count==0 (adjacent sha256 sidecars).
- prereg_hash recorded in manifest: 5e075968e5958471530d0618cdba1410f8fb3d5afdb31c3be13f99aa07d27c92
- **Fundamental limitation**: The 5x/24h long synthetic boundary is too conservative for this test window. Zero events in test = no confirmatory evidence possible. This window is INADMISSIBLE for confirmatory Track B with this label definition. Future Track B work must either (a) choose a label definition with adequate event rate in the test window, or (b) select a test window with observed events.