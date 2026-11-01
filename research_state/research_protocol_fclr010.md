# Research Protocol: FCLR-010 (CONFIRMATORY TRACK A — OBSERVED LIQUIDATIONS)

Version: 1.0
Timestamp: 2026-11-01T04:52:00Z
Status: PRE-REGISTERED BEFORE OUTCOMES
Experiment ID: FCLR-010
Hypothesis: FCLR-H004 (observed liquidation outcomes, conditional on adequate labels)
Track: A (observed liquidation labels — CROSS-TRACK FIREWALL: Hyperliquid universe, NOT merged with Binance panels FCLR-001/002/003/006/007/008/009)

## Objective
Confirmatory test of whether funding extremes plus realized volatility incrementally forecast OBSERVED liquidation intensity on Hyperliquid perpetual futures, using the newly admissible ironflow liquidation census (research_state/data_source_registry.json#ironflow_hyperliquid_liquidation_events). This is the Track A reopen path: a NEW admissible unauthenticated source passed ALL rubric items (unauthenticated, no_keys, symbols>=5, blocks>=3, completeness_doc, license_ok CC BY 4.0, census_or_defensible).

## Data sources (frozen before outcomes)
- Labels: ironflow_hyperliquid_liquidation_events, events config, data/events/YYYY-MM.parquet, window 2025-11-01..2026-10-31 (12 monthly files = 12 non-overlapping ~30-day blocks), 185 native perpetual markets observed in 2025-11. SHA-256 hashes per month recorded in data_source_registry.json; files cached at research_state/data_cache/ironflow_events/.
- Predictors: Hyperliquid mark prices and funding rates from public unauthenticated API (api.hyperliquid.xyz/info) — coverage audit (depth, cadence, auth requirements) to be completed BEFORE outcome inspection; endpoints and vintages frozen in run_manifest at split freeze.
- No Binance data. No merging with Track C panels.

## Universe
- Native Hyperliquid perpetual markets only (market ends with -PERP and contains no ':'; excludes HIP-3 builder/stock/commodity/index markets unless separately registered).
- >=5 symbols required (185 observed in 2025-11).
- Symbols admitted by first-observed-listing; no survivor substitution.

## Period and blocks
- Window: 2025-11-01T00:00:00Z .. 2026-10-31T23:00:00Z (12 months).
- Blocks: 12 non-overlapping monthly 30-day blocks (>=3 minimum met).
- Unit: one native perpetual contract × one fully closed UTC hourly timestamp.

## Labels (observed, not modeled)
- Per symbol per hour: liquidation count and sum of notional_usd from ironflow events; long and short (position_side) kept separate.
- Binary occurrence label: >=1 liquidation in symbol-hour.
- Intensity label: log(1 + notional_usd) per symbol-hour.
- Missing symbol-hours = no observed liquidation rows; absence not interpreted as zero until coverage audit quantifies reporting gaps.

## Predictors (causal, computed from data ending no later than forecast timestamp t)
- Signed funding rate (latest observation available by t).
- Absolute funding percentile vs trailing 90 calendar days (>=30 observations required).
- Trailing RV24h / RV168h from mark-price log returns.
- Fixed model forms only; no regularization, no model-family search, no hyperparameter tuning.

## Models
- Persistence baseline, RV-only baseline, funding-augmented, combined candidate (RV + funding + price dislocation where available).
- Primary contrast: combined vs RV-only on the primary label (occurrence Brier/intensity MAE on test set).

## Splits (frozen before outcomes)
- Chronological train/validation/test by unique UTC timestamps, 60/20/20 default, 7-calendar-day purge/embargo at all boundaries.
- Boundaries determined from coverage audit of label + predictor overlap; recorded in run_manifest.json#split_boundaries_fclr010 with frozen_before_outcomes=true BEFORE any outcome computation.

## Metrics and inference
- Binary occurrence: Brier score, log loss, calibration; paired test-set comparison vs RV-only baseline.
- Intensity: MAE on log(1+notional_usd), positive-sample subset reported separately.
- Uncertainty: block bootstrap (>=2000 deterministic-seed replicates) resampling UTC time blocks jointly across instruments.
- Multiplicity: Holm correction across registered family (occurrence × intensity × horizons where registered).

## Gate
Forecast gate MET only if combined vs RV-only shows improvement on the primary label with 95% CI excluding zero on the improving side, practical materiality floor met, >=5 instruments and >=3 non-overlapping 30-day blocks in the paired OOS panel, acceptable calibration, and no unresolved leakage/label defect. Otherwise NOT_MET; null preserved; no threshold shopping.

## Mandatory constraints
- THIS PROTOCOL IS PRE-REGISTERED BEFORE ANY OUTCOME INSPECTION. No model may be fitted against liquidation labels, and no label-outcome relationship may be inspected, until this protocol is frozen and splits are recorded with frozen_before_outcomes=true.
- Coverage/schema row counts (already recorded: 214,559 rows in 2025-11; 185 native perps) are coverage-only evidence, not outcomes.
- Do not relax rubric, floor, CI criterion, or block minimum. Do not relabel exploratory as confirmatory.
- No .github/workflows/* changes. Commit nothing merely for activity.
- Seal: once the test window outcomes are inspected, this window cannot be treated as uninspected evidence again.

## Next step after pre-registration
1. Coverage audit of Hyperliquid public funding/mark API (unauthenticated) + label/predictor overlap audit.
2. Freeze splits in run_manifest.json#split_boundaries_fclr010 (frozen_before_outcomes=true).
3. Execute FCLR-010 experiment; write evaluation_summary_FCLR010.md + gate assessment.
4. Update experiment_frontier.json and AGENT_HANDOFF.md.
