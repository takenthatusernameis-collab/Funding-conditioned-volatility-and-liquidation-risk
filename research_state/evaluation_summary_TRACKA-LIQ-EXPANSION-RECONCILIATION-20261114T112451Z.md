# Evaluation Summary — FCLR-LIQ-EXPANSION-RECONCILIATION-20261114T083642Z

Generated: 2026-11-14T11:24:51Z
Campaign: `FCLR-LIQ-EXPANSION-RECONCILIATION-20261114T083642Z`
Prereg: `research_state/prereg_tracka_liq_expansion_reconciliation_20261114T083642Z.json` (status FROZEN_PRE_OUTCOMES, frozen before outcomes)

## Overall Verdict: **INCONCLUSIVE**

- Rationale: One or more cells failed to produce a valid result

## 2×2 Reconciliation Matrix (C2_vs_B1 relative QLIKE reduction %)

| | Sealed Estimator | Recompute Estimator |
|---|---|---|
| Sealed panel | 6.19% | 6.19% |
| Recompute panel | 6.19% | 6.19% |

Sealed reference (TRACKA-HL-EXPANSION): 19.04%
Recompute reference (FCLR-LIQ-EXPANSION-RECOMPUTE): 6.19%
Gap: 12.85 percentage points

## Cell Details

### Sealed panel + Sealed estimator

| Contrast | n pairs | B QLIKE | A QLIKE | mean diff | 95% CI | rel reduction | Holm p | material | CI excl 0 |
|---|---|---|---|---|---|---|---|---|---|
| C2_vs_B1 | 593 | 3.114659 | 2.921861 | -0.19279729 | [-0.42074401, -0.03377946] | 6.19% | 0.036 | True | True |
| C1_vs_B1 | 593 | 3.114659 | 3.01872 | -0.09593918 | [-0.26335287, -0.00308607] | 3.0802% | 0.087 | True | True |
| C2_vs_C1 | 593 | 3.01872 | 2.921861 | -0.09685811 | [-0.15739114, -0.03069339] | 3.2086% | 0.087 | True | True |

- LOIO: 7/8 instruments clear the 2.0% materiality floor
- Placebo (funding permutation, n=200): null p95 7.6603%, p≈0.44, pass=False

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
| C2_vs_B1 | 593 | 3.114659 | 2.921861 | -0.19279729 | [-0.42074401, -0.03377946] | 6.19% | 0.036 | True | True |
| C1_vs_B1 | 593 | 3.114659 | 3.01872 | -0.09593918 | [-0.26335287, -0.00308607] | 3.0802% | 0.087 | True | True |
| C2_vs_C1 | 593 | 3.01872 | 2.921861 | -0.09685811 | [-0.15739114, -0.03069339] | 3.2086% | 0.087 | True | True |

- LOIO: 7/8 instruments clear the 2.0% materiality floor
- Placebo (funding permutation, n=200): null p95 7.6603%, p≈0.44, pass=False

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
- zero_fill_used: False
- forward_fill_used: False
- train_only_scaling: True
- splits_respect_embargo_days: True
- notes: Panel: sealed, Estimator: sealed. target_next_intensity is a strictly forward sum over t+1..t+24h (shift -1 day); funding attached by backward merge_asof (<=24h tolerance); RV attached by backward merge_asof (<=168h tolerance); no zero/forward fill; scaling fit on train rows only; 7d purge/embargo at train/val/test boundaries; features causal (data ending <= t).

### Sealed panel + Recompute estimator
- target_uses_strictly_future_bars: True
- zero_fill_used: False
- forward_fill_used: False
- train_only_scaling: True
- splits_respect_embargo_days: True
- notes: Panel: sealed, Estimator: recompute. target_next_intensity is a strictly forward sum over t+1..t+24h (shift -1 day); funding attached by backward merge_asof (<=24h tolerance); RV attached by backward merge_asof (<=168h tolerance); no zero/forward fill; scaling fit on train rows only; 7d purge/embargo at train/val/test boundaries; features causal (data ending <= t).

### Recompute panel + Sealed estimator
- target_uses_strictly_future_bars: True
- zero_fill_used: False
- forward_fill_used: False
- train_only_scaling: True
- splits_respect_embargo_days: True
- notes: Panel: recompute, Estimator: sealed. target_next_intensity is a strictly forward sum over t+1..t+24h (shift -1 day); funding attached by backward merge_asof (<=24h tolerance); RV attached by backward merge_asof (<=168h tolerance); no zero/forward fill; scaling fit on train rows only; 7d purge/embargo at train/val/test boundaries; features causal (data ending <= t).

### Recompute panel + Recompute estimator
- target_uses_strictly_future_bars: True
- zero_fill_used: False
- forward_fill_used: False
- train_only_scaling: True
- splits_respect_embargo_days: True
- notes: Panel: recompute, Estimator: recompute. target_next_intensity is a strictly forward sum over t+1..t+24h (shift -1 day); funding attached by backward merge_asof (<=24h tolerance); RV attached by backward merge_asof (<=168h tolerance); no zero/forward fill; scaling fit on train rows only; 7d purge/embargo at train/val/test boundaries; features causal (data ending <= t).

## Comparison to Reference Results

| Cell | C2_vs_B1 rel reduction | vs Sealed Ref (19.04%) | vs Recompute Ref (6.19%) |
|---|---|---|---|
| sealed+sealed | 6.19% | -12.85pp | +0.00pp |
| sealed+recompute | 6.19% | -12.85pp | +0.00pp |
| recompute+sealed | 6.19% | -12.85pp | +0.00pp |
| recompute+recompute | 6.19% | -12.85pp | +0.00pp |

## Sealed artifacts unchanged

- Sealed panel SHA-256: `39916a72dfc37d15b6cc886d4e43ed878e0b8e1c2f22936fc4ebf8edd366f699` (verified unchanged)
- Recompute panel SHA-256: `a4d73c79683550a15e616f3f5fbd93128db1c5498944f9139226f543cfe96715` (verified unchanged)

---

*All results EXPLORATORY_ONLY, promotable=false. Does not reopen sealed verdict.*