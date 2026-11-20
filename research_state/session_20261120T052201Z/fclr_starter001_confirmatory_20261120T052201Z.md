# FCLR-STARTER-001 Confirmatory Evaluation

**Session:** session_20261120T052201Z
**Experiment:** FCLR-STARTER-001-20261120T052201Z
**Verdict:** NOT_SUPPORTED

## Model Performance (Holdout)

| Model | QLIKE | MAE | RMSE | N |
|-------|-------|-----|------|---|
| B1 | 0.358479 | 0.000549 | 0.000828 | 10920 |
| C1 | 0.373696 | 0.000568 | 0.000852 | 10920 |
| C2 | 0.367875 | 0.000568 | 0.000858 | 10920 |

## Paired Comparisons

| Comparison | Role | Base QLIKE | Alt QLIKE | Diff | 95% CI | Rel Imp | p-value | Holm Rejected |
|------------|------|------------|-----------|------|--------|---------|---------|---------------|
| C2 vs B1 | primary | 0.358479 | 0.367875 | 0.009396 | [0.002400, 0.016382] | -2.62% | 0.025 | False |
| C1 vs B1 | secondary | 0.358479 | 0.373696 | 0.015217 | [0.007843, 0.022637] | -4.24% | 0.025 | False |
| C2 vs C1 | secondary | 0.373696 | 0.367875 | -0.005821 | [-0.008170, -0.003344] | 1.56% | 0.025 | False |

## Gate Criteria

- rel_improvement_pct: -2.6209718038328043
- ci_supports_improvement: False
- holm_passes: False
- min_instruments: True
- min_blocks: True

**Final Verdict:** NOT_SUPPORTED
