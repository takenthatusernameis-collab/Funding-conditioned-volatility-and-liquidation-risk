# FCLR-VOL-JUMP-01 Prereg (outcome-blind, frozen) (20261125T030000Z)

- experiment_id: FCLR-VOL-JUMP-01
- session_id: session_20261125T030000Z
- frozen_before_outcomes: True
- outcome_data_inspected_before_freeze: False
- design.kind: walk_forward_classification_signed_jump_semivariance_asymmetry
- materiality_floor_rel: 0.02
- source_registry_sha256: `046d98225067c3dbdf86c94cd47eb4f3de60e33a8cfec370b758fa636e7c2d75`

## Primary question
Does the funding + price-dislocation feature set improve out-of-sample forecasts of a signed-jump / semivariance-asymmetry TAIL event (next-24h jump component above an expanding, train-only high quantile per coin) beyond a realized-volatility-only baseline on the broad ironflow_bulk panel, clearing a frozen materiality floor?

## Design
- target: jump event y_t = 1 if J_{t+1..t+24} > q_t
- jump_definition: J = sign(RS+ - RS-) * (RV - BV), RV = sum of squared 1h log returns over next 24h, BV = bipower variation, RS+/RS- = realized semivariance of positive/negative returns
- baseline: RV-only (persistence / HAR-style trailing log-RV lags) logistic
- candidate: RV-only + signed funding_rate + abs(funding_rate) + mark/index premium + mark/EMA24 distance
- walk_forward: True purge_embargo_h: 48
- materiality_definition: candidate relative Brier (or log-loss) improvement over the RV-only baseline must exceed 0.02 (2%); verdict is symmetric PROMOTED / NOT_SUPPORTED
