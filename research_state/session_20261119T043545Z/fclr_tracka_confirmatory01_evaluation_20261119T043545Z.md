# Track A confirmatory three-block evaluation

Campaign: `FCLR-LIQ-TRACKA-CONFIRMATORY-01-20261119T034500Z`
Session: `session_20261119T043545Z`
Verdict: **NOT_MET** (models_run=True)
Headline metric: Brier score
Family size: 4 (Holm correction, alpha=0.05)
Placebo: label-hour permutation null (200 permutations, seed 20261119)

## Block summaries
- block_1: n_train=0, n_test=18395, n_test_events=None, test_base_rate=nan
- block_2: n_train=18395, n_test=26845, n_test_events=5023, test_base_rate=0.187111
- block_3: n_train=28067, n_test=27755, n_test_events=4761, test_base_rate=0.171537

## Family (raw and Holm-adjusted p-values)
- block_3:funding-only_vs_RV_only: brier_model=0.142935, brier_baseline=0.142915, diff=+0.000020, p_raw=0.004975, p_holm=1.000000, reject=False
- block_3:funding_x_RV_vs_RV_only: brier_model=0.142393, brier_baseline=0.142915, diff=-0.000522, p_raw=0.004975, p_holm=1.000000, reject=False
- block_2:funding_x_RV_vs_RV_only: brier_model=0.152743, brier_baseline=0.152615, diff=+0.000129, p_raw=0.174129, p_holm=1.000000, reject=False
- block_2:funding-only_vs_RV_only: brier_model=0.153703, brier_baseline=0.152615, diff=+0.001089, p_raw=1.000000, p_holm=1.000000, reject=False

Headline contrast: {'contrast': 'block_3:funding_x_RV_vs_RV_only', 'block': 'block_3', 'model': 'funding_x_RV', 'baseline': 'RV-only', 'metric': 'Brier', 'brier_model': 0.14239308085125885, 'brier_baseline': 0.14291512194329245, 'brier_diff': -0.0005220410920336038, 'p_raw': 0.004975124378109453, 'p_holm': 1.0, 'reject_holm_005': False, 'model_metrics': {'brier': 0.14239308085125885, 'log_loss': 0.4591518184261665, 'auc': 0.5589843104372662, 'calibration_intercept': 0.4734582933536949, 'calibration_slope': 0.22316729670347749}, 'baseline_metrics': {'brier': 0.14291512194329245, 'log_loss': 0.4609392118632371, 'auc': 0.5654900942442872, 'calibration_intercept': 1.6108937227653888, 'calibration_slope': 1.0648576828550513}}
Verdict: NOT_MET
Absence from the feed is not evidence of no liquidation (missing, not zero). No sealed Binance month read.
