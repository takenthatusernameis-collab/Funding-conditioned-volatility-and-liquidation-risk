# Evaluation Summary — FCLR-LIQ-EXPANSION-RECOMPUTE-20261114T073346Z

Generated: 2026-11-14T08:30:00Z
Campaign: `FCLR-FUND-VOL-LIQ-REDTEAM-20261114T042139Z`
Prereg: `research_state/prereg_tracka_liq_expansion_recompute_20261114T073346Z.json` (status FROZEN_PRE_OUTCOMES, frozen before outcomes)

## Verdict: **INCONCLUSIVE** (VALID_EXPLORATORY)

- Promotable: `False` (audit only, never promotable)
- Sealed TRACKA-HL-EXPANSION artifacts: unchanged (read-only in this cell)
- Smoke run: `False`

## Sealed-reference replication statement

- Sealed C2_vs_B1 rel QLIKE reduction: 19.03709721199804% (CI [-5.0881020797243135, -0.4776599249731716], n_pairs=593, n_blocks=3, symbols=['AAVE', 'ADA', 'BCH', 'CRV', 'LTC', 'NEAR', 'UNI', 'ZEC'])
- Recomputed C2_vs_B1 rel QLIKE reduction: 6.1900% (CI [-0.420744, -0.033779], n_pairs=593, n_blocks=3)
- Sealed 19.04% C2-vs-B1 replicates: False (recomputed 6.1900% vs sealed 19.03709721199804%; materially consistent threshold = sealed x 0.5 = 9.52%)
- Sealed LOIO 4/8 replicates: recomputed LOIO 7/8 (sealed 4/8)
- Sealed placebo failure (true 19.04% <= null p95 21.10%) replicates: False (recomputed true 6.1900% vs null p95 7.6603%)

## Panel

- Panel: `research_state/tracka_liq_expansion_recompute_panel_20261114T083000Z.parquet`
- Panel SHA-256: `a4d73c79683550a15e616f3f5fbd93128db1c5498944f9139226f543cfe96715`
- Rows: 0
- Instruments: 8 ['AAVE', 'ADA', 'BCH', 'CRV', 'LTC', 'NEAR', 'UNI', 'ZEC']
- Test blocks with data: [0, 1, 2] (need >= 3)
- Test window: ['2026-07-07T00:00:00Z', '2026-10-17T23:00:00Z']

## Coverage (test rows)

- test_rows_total: 728
- test_rows_core_complete: 725
- test_rows_core_positive: 593
- core_coverage: 0.995879

## Paired contrasts (QLIKE, lower is better)

| Contrast | n pairs | B QLIKE | A QLIKE | mean diff | 95% CI | rel reduction | Holm p | material | CI excl 0 |
|---|---|---|---|---|---|---|---|---|---|
| C2_vs_B1 | 593 | 3.114659 | 2.921861 | -0.19279729 | [-0.42074401, -0.03377946] | 6.19% | 0.036 | True | True |
| C1_vs_B1 | 593 | 3.114659 | 3.01872 | -0.09593918 | [-0.26335287, -0.00308607] | 3.0802% | 0.087 | True | True |
| C2_vs_C1 | 593 | 3.01872 | 2.921861 | -0.09685811 | [-0.15739114, -0.03069339] | 3.2086% | 0.087 | True | True |

## Robustness

- LOIO: 7/8 instruments clear the 2.0% materiality floor
- Placebo (funding permutation, n=200): null p95 7.6603%, p≈0.44, pass=False

## Per-symbol (C2 vs B1)

| Symbol | n | B1 QLIKE | C2 QLIKE | rel reduction |
|---|---|---|---|---|
| AAVE | 79 | 2.462176 | 2.39238 | 2.8347% |
| ADA | 77 | 1.917268 | 1.935114 | -0.9308% |
| BCH | 65 | 3.620224 | 3.583475 | 1.0151% |
| CRV | 67 | 2.845424 | 3.006025 | -5.6442% |
| LTC | 56 | 4.565833 | 4.76715 | -4.4092% |
| NEAR | 80 | 2.695591 | 2.563343 | 4.9061% |
| UNI | 82 | 2.318319 | 2.386314 | -2.9329% |
| ZEC | 87 | 4.798357 | 3.363528 | 29.9025% |

## Per-block (C2 vs B1)

| Block | n | B1 QLIKE | C2 QLIKE | rel reduction |
|---|---|---|---|---|
| block_0 | 175 | 2.634459 | 2.600679 | 1.2822% |
| block_1 | 202 | 3.987869 | 3.567125 | 10.5506% |
| block_2 | 216 | 2.687096 | 2.578637 | 4.0363% |

## Leakage audit

- target_uses_strictly_future_bars: True
- zero_fill_used: False
- forward_fill_used: False
- train_only_scaling: True
- splits_respect_embargo_days: True
- funding_asof_backward_only: True

target_next_intensity is a strictly forward sum over t+1..t+24h (shift -1 day); funding attached by backward merge_asof (<=24h tolerance); RV attached by backward merge_asof (<=168h tolerance); no zero/forward fill; scaling fit on train rows only; 7d purge/embargo at train/val/test boundaries; features causal (data ending <= t).


## Comparison to the sealed Track A expansion result

| Contrast | Sealed rel reduction | Recomputed rel reduction |
|---|---|---|
| C2_vs_B1 | 19.03709721199804% | 6.19 |
| C1_vs_B1 | 9.679438491416526% | 3.0802 |
| C2_vs_C1 | 10.360496618139631% | 3.2086 |

## Notes

- Observed Hyperliquid ironflow liquidation labels only; no Binance/2024 conflation; no modeled/proxy/synthetic labels; no threshold-shopping; no sealed-holdout reuse.
- Premium IS computable here (Hyperliquid funding cache carries the premium field).
- No zero-fill, no forward-fill. Funding/RV attached by backward merge_asof. Target is a strictly forward 24h liquidation intensity.
