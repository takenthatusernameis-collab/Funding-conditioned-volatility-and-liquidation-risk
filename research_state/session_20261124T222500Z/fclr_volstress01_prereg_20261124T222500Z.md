# FCLR-VOL-STRESS-01 Prereg (outcome-blind, frozen before outcomes)

**Experiment ID:** FCLR-VOL-STRESS-01
**Campaign:** FCLR-VOL-STRESS-01-20261124T213000Z
**Session:** session_20261124T222500Z
**Frozen before outcomes:** True
**Outcome data inspected before freeze:** False
**Source registry sha256:** `9446ed189153399fd13793e3978bad1bd348794f3f72b5849ccf8542c7013a53`

## Design
- Kind: walk_forward_classification_stress_tail_exceedance
- Target: stress event y_t = 1 if RV_{t+1..t+24} > q_t
- Threshold: expanding, train-only per-coin high quantile (0.95) of trailing RV, shifted by 1 (no future info)
- Baseline: RV-only (HAR-style trailing log-RV lags) logistic
- Candidate: RV-only + signed funding_rate + abs(funding_rate) + premium + mark/EMA24 distance
- Walk-forward: train_frac=0.6, purge_embargo_h=48, n_test_blocks=6
- Materiality floor (relative Brier improvement): 0.02

## Verdict rule
- PROMOTED: materiality_met is True AND candidate beats baseline on Brier (Holm-adjusted)
- NOT_SUPPORTED: materiality floor not met (valid, publishable negative result)
- INCONCLUSIVE: insufficient events / degenerate metrics
