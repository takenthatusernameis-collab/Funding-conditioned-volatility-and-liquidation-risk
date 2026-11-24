# FCLR-VOL-STRESS-01 Evaluation (heavy stress-forecast)

**Experiment:** FCLR-VOL-STRESS-01  **Campaign:** FCLR-VOL-STRESS-01-20261124T213000Z  **Session:** session_20261124T213500Z
**Status:** CONFIRMATORY_COMPLETE  **Verdict:** PROMOTED  **Holdout opened:** true
**Stress event:** next-24h realized variance > expanding train-only 0.90 quantile of trailing-24h RV per coin.
**Baseline:** RV-only logistic (rv24, rv168, rv24_lag1). **Candidate:** baseline + funding_rate + abs_funding + premium_mi + ema_dist.

| Metric | Baseline (RV-only) | Candidate (RV+funding+price) |
|---|---:|---:|
| Brier score | 0.228093 | 0.218873 |
| Log loss | 0.649280 | 0.637391 |
| n test origins | 16149 | 16149 |
| n stress events | 1445 | 1445 |

Relative Brier improvement: 4.0422% (frozen floor 2%)
Relative log-loss improvement: 1.8311%
Materiality met: True
Verdict: PROMOTED

Inference: cluster-robust (CR1) by coin, Driscoll-Kraay HAC, Holm step-down over
{baseline_vs_candidate_brier, baseline_vs_candidate_log_loss}.
Purge/embargo 48h; train fraction 0.6; no random split; no overlapping forward targets.
All inputs from the frozen, sha256-asserted ironflow_bulk panel; read-only; no network.
