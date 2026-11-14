# Evaluation Summary — FCLR-LIQ-EXPANSION-RECONCILIATION-20261114T083642Z

Generated: 2026-11-14T11:32:26Z
Campaign: `FCLR-LIQ-EXPANSION-RECONCILIATION-20261114T083642Z`
Prereg: `research_state/prereg_tracka_liq_expansion_reconciliation_20261114T083642Z.json` (status FROZEN_PRE_OUTCOMES, frozen before outcomes)

## Overall Verdict: **EXPLAINED_BY_ESTIMATOR**

- Rationale: Estimator difference on sealed panel accounts for >50% of gap (sealed_estimator=19.04%, recompute_estimator=6.19%, diff=12.85%, gap=12.85%)

## 2×2 Reconciliation Matrix (C2_vs_B1 relative QLIKE reduction %)

| | Sealed Estimator | Recompute Estimator |
|---|---|---|
| Sealed panel | 19.0371% | 6.19% |
| Recompute panel | 19.0371% | 6.19% |

Sealed reference (TRACKA-HL-EXPANSION): 19.04%
Recompute reference (FCLR-LIQ-EXPANSION-RECOMPUTE): 6.19%
Gap: 12.85 percentage points

## Cell Details

### Sealed panel + Sealed estimator

| Contrast | n pairs | B QLIKE | A QLIKE | mean diff | 95% CI | rel reduction | Holm p | material | CI excl 0 |
|---|---|---|---|---|---|---|---|---|---|
| C2_vs_B1 | 593 | 14.234009 | 11.524267 | -2.70974212 | [-5.08810208, -0.47765992] | 19.0371% | 0.075 | True | True |
| C1_vs_B1 | 593 | 14.234009 | 12.856237 | -1.37777214 | [-3.17486072, -0.20487391] | 9.6794% | 0.075 | True | True |
| C2_vs_C1 | 593 | 12.856237 | 11.524267 | -1.33196998 | [-1.91324136, -0.27278602] | 10.3605% | 0.075 | True | True |

- LOIO: 8/8 instruments clear the 2.0% materiality floor
- Placebo (funding permutation, n=200): null p95 None%, p≈None, pass=False

### Sealed panel + Recompute estimator

| Contrast | n pairs | B QLIKE | A QLIKE | mean diff | 95% CI | rel reduction | Holm p | material | CI excl 0 |
|---|---|---|---|---|---|---|---|---|---|
| C2_vs_B1 | 593 | 3.114659 | 2.921861 | -0.19279729 | [-0.42074401, -0.03377946] | 6.19% | 0.036 | True | True |
| C1_vs_B1 | 593 | 3.114659 | 3.01872 | -0.09593918 | [-0.26335287, -0.00308607] | 3.0802% | 0.087 | True | True |
| C2_vs_C1 | 593 | 3.01872 | 2.921861 | -0.09685811 | [-0.15739114, -0.03069339] | 3.2086% | 0.087 | True | True |

- LOIO: 7/8 instruments clear the 2.0% materiality floor
- Placebo (funding permutation, n=200): null p95 7.6603%, p≈0.44, pass=False

### Recompute panel + Sealed estimator

| Contrast | n pairs | B QLIKE | A QLIKE | mean diff | 95% CI | rel reduction | Holm p | material | CI excl 0 |
|---|---|---|---|---|---|---|---|---|---|
| C2_vs_B1 | 593 | 14.234009 | 11.524267 | -2.70974212 | [-5.08810208, -0.47765992] | 19.0371% | 0.075 | True | True |
| C1_vs_B1 | 593 | 14.234009 | 12.856237 | -1.37777214 | [-3.17486072, -0.20487391] | 9.6794% | 0.075 | True | True |
| C2_vs_C1 | 593 | 12.856237 | 11.524267 | -1.33196998 | [-1.91324136, -0.27278602] | 10.3605% | 0.075 | True | True |

- LOIO: 8/8 instruments clear the 2.0% materiality floor
- Placebo (funding permutation, n=200): null p95 None%, p≈None, pass=False

### Recompute panel + Recompute estimator

| Contrast | n pairs | B QLIKE | A QLIKE | mean diff | 95% CI | rel reduction | Holm p | material | CI excl 0 |
|---|---|---|---|---|---|---|---|---|---|
| C2_vs_B1 | 593 | 3.114659 | 2.921861 | -0.19279729 | [-0.42074401, -0.03377946] | 6.19% | 0.036 | True | True |
| C1_vs_B1 | 593 | 3.114659 | 3.01872 | -0.09593918 | [-0.26335287, -0.00308607] | 3.0802% | 0.087 | True | True |
| C2_vs_C1 | 593 | 3.01872 | 2.921861 | -0.09685811 | [-0.15739114, -0.03069339] | 3.2086% | 0.087 | True | True |

- LOIO: 7/8 instruments clear the 2.0% materiality floor
- Placebo (funding permutation, n=200): null p95 7.6603%, p≈0.44, pass=False

## Leakage Audit (per cell)

### Sealed panel + Sealed estimator
- target_uses_strictly_future_bars: True
- zero_fill_used: True
- forward_fill_used: False
- train_only_scaling: False
- splits_respect_embargo_days: True
- notes: Panel: sealed, Estimator: sealed. target_next_intensity is a strictly forward sum over t+1..t+24h (shift -1 day); features attached by backward merge_asof (<=24h tolerance); RV attached by backward merge_asof (<=168h tolerance); zero-fill for missing features (sealed estimator); 7d purge/embargo at train/val/test boundaries; features causal (data ending <= t).

### Sealed panel + Recompute estimator
- target_uses_strictly_future_bars: True
- zero_fill_used: False
- forward_fill_used: False
- train_only_scaling: True
- splits_respect_embargo_days: True
- notes: Panel: sealed, Estimator: recompute. target_next_intensity is a strictly forward sum over t+1..t+24h (shift -1 day); features attached by backward merge_asof (<=24h tolerance); RV attached by backward merge_asof (<=168h tolerance); no zero/forward fill; scaling fit on train rows only (recompute estimator); 7d purge/embargo at train/val/test boundaries; features causal (data ending <= t).

### Recompute panel + Sealed estimator
- target_uses_strictly_future_bars: True
- zero_fill_used: True
- forward_fill_used: False
- train_only_scaling: False
- splits_respect_embargo_days: True
- notes: Panel: recompute, Estimator: sealed. target_next_intensity is a strictly forward sum over t+1..t+24h (shift -1 day); features attached by backward merge_asof (<=24h tolerance); RV attached by backward merge_asof (<=168h tolerance); zero-fill for missing features (sealed estimator); 7d purge/embargo at train/val/test boundaries; features causal (data ending <= t).

### Recompute panel + Recompute estimator
- target_uses_strictly_future_bars: True
- zero_fill_used: False
- forward_fill_used: False
- train_only_scaling: True
- splits_respect_embargo_days: True
- notes: Panel: recompute, Estimator: recompute. target_next_intensity is a strictly forward sum over t+1..t+24h (shift -1 day); features attached by backward merge_asof (<=24h tolerance); RV attached by backward merge_asof (<=168h tolerance); no zero/forward fill; scaling fit on train rows only (recompute estimator); 7d purge/embargo at train/val/test boundaries; features causal (data ending <= t).

## Comparison to Reference Results

| Cell | C2_vs_B1 rel reduction | vs Sealed Ref (19.04%) | vs Recompute Ref (6.19%) |
|---|---|---|---|
| sealed+sealed | 19.04% | +0.00pp | +12.85pp |
| sealed+recompute | 6.19% | -12.85pp | +0.00pp |
| recompute+sealed | 19.04% | +0.00pp | +12.85pp |
| recompute+recompute | 6.19% | -12.85pp | +0.00pp |

## Sealed artifacts unchanged

- Sealed panel SHA-256: `39916a72dfc37d15b6cc886d4e43ed878e0b8e1c2f22936fc4ebf8edd366f699` (verified unchanged)
- Recompute panel SHA-256: `a4d73c79683550a15e616f3f5fbd93128db1c5498944f9139226f543cfe96715` (verified unchanged)

---

*All results EXPLORATORY_ONLY, promotable=false. Does not reopen sealed verdict.*