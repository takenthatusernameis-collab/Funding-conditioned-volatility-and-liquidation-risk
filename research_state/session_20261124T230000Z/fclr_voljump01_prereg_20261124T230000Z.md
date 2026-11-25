# FCLR-VOL-JUMP-01 Preregistration (20261124T230000Z)

- experiment_id: FCLR-VOL-JUMP-01
- session_id: session_20261124T230000Z
- campaign: FCLR-VOL-JUMP-01-20261124T223000Z
- generated_utc: 2026-11-24T23:00:00Z
- frozen_before_outcomes: true
- outcome_data_inspected_before_freeze: false
- source_registry_sha256: e8d3bb5eb4ebde9439d3753c3241742f4f9e9239d90c817c2ab809fc519ef01b

## Primary question
Does the funding + price-dislocation feature set improve out-of-sample forecasts of a signed-jump / semivariance-asymmetry TAIL event (next-24h jump component above an expanding, train-only high quantile per coin) beyond a realized-volatility-only baseline on the broad ironflow_bulk panel, clearing a frozen materiality floor?

## Design
- kind: walk_forward_classification_signed_jump_semivariance_asymmetry
- outcome_family: signed_jump_semivariance_asymmetry_classification
- forecast_origin: hourly t (close of hour t)
- target: jump event y_t = 1 if J_{t+1..t+24} > q_t
- jump_definition: J = sign(RS+ - RS-) * (RV - BV); RV = sum of squared 1h log returns over next 24h; BV = bipower variation; RS+/RS- = realized semivariance of positive/negative returns
- quantile_q_t: expanding, train-only per-coin high quantile (0.95) of trailing |J|, shifted by 1 (no future information)
- baseline: RV-only (persistence / HAR-style trailing log-RV lags) logistic
- candidate: RV-only + signed funding_rate + abs(funding_rate) + mark/index premium + mark/EMA24 distance
- feature_standardization: train-only (expanding) z-score
- walk_forward: true
- train_frac: 0.6
- purge_embargo_h: 48
- n_test_blocks: 6
- block_months: 2
- no_random_split: true
- no_overlapping_forward_targets_across_purge: true
- inference: cluster-robust CR1 by coin; Driscoll-Kraay HAC (block-level); Holm step-down over declared family
- multiplicity_family: brier_relative_improvement; logloss_relative_improvement
- metrics: brier; log_loss; calibration_ece

## Materiality
- materiality_floor_rel: 0.02
- materiality_floor: 0.02
- definition: candidate relative Brier (or log-loss) improvement over the RV-only baseline must exceed 0.02 (2%); verdict is symmetric PROMOTED / NOT_SUPPORTED

## Universe
coins present in candles_1h AND funding AND open_interest (intersection), with sufficient trailing history for train-only quantile.

## Frozen inputs
ironflow_bulk 18 monthly parquet per dataset; sha256-asserted; read-only; bounds 2025-05 .. 2026-10. Bound to source_registry sha256 e8d3bb5eb4ebde9439d3753c3241742f4f9e9239d90c817c2ab809fc519ef01b.
