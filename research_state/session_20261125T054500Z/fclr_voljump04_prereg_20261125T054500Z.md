# FCLR-VOL-JUMP-04 Directional / Sign Jump-Forecast Prereg (frozen before outcomes)

- experiment_id: FCLR-VOL-JUMP-04
- session_id: session_20261125T054500Z
- campaign: FCLR-VOL-JUMP-04-20261125T045000Z
- frozen_before_outcomes: true
- outcome_data_inspected_before_freeze: false
- source_registry_sha256: d2d8b4549e1c185ec8fe09e3aadc705f40f48cfabd44aaa983452ff5da86f422

## Primary question
Does the funding + price-dislocation feature set improve out-of-sample forecasts of the
DIRECTION / SIGN of a signed-jump / semivariance-asymmetry event (next-H signed jump
`J^{(H)} < 0`, downside-dominant: RS- > RS+) beyond an RV-only baseline on the broad
`ironflow_bulk` panel, clearing a frozen 2% materiality floor with Holm-adjusted
uncertainty, when the jump ESTIMATOR (bipower vs threshold-bipower) AND the forecast
HORIZON ({24h, 48h}) are varied and ALL FCLR-POOLED-AUDIT-001 leakage remediations are
applied simultaneously?

## Design (frozen)
- kind: directional signed-jump / semivariance-asymmetry SIGN classification,
  multi-estimator x multi-horizon, non-overlapping, leakage-hardened.
- estimators: bipower, threshold_bipower; horizons_h: 24, 48.
- target: `y_t = 1` iff `J^{(H)}_{t+1..t+H} < 0` (downside-dominant). Binary sign target;
  no train-only quantile threshold; base rate estimated train-only.
- jump: `J^{(H)} = sign(RS+ - RS-) * (RV_H - BV_H)`.
- baseline: RV-only (trailing log-RV_H) logistic.
- candidate: RV + signed funding_rate + abs(funding_rate) + premium + mark/EMA24 distance.
- walk-forward expanding train-only fit; train_frac 0.6; purge_embargo_h 48;
  NON-overlapping forward-outcome windows (origin spacing >= H); mark/index tolerance 0.01;
  delisting-aware per-coin identity; per-coin cluster bootstrap; Holm across the declared
  (estimator x horizon x metric) family; no random split.
- materiality_floor_rel: 0.02 (frozen, not relaxed after outcomes).

## Verdict rule (symmetric)
- PROMOTED: materiality_met True AND candidate beats baseline on Brier with Holm-adjusted significance.
- NOT_SUPPORTED: materiality floor not met in any config (valid, publishable negative result).
- INCONCLUSIVE: insufficient events / degenerate metrics.

## Distinct from prior
Materially different DIRECTIONAL / SIGN design, not the MAGNITUDE-exceedance endpoint closed
by FCLR-VOL-JUMP-01/02/03. Not a relabel of mean-QLIKE, correction-time, or total-variance
tail-exceedance endpoints.