# Evaluation Summary — FCLR-011-INDEPENDENT-RECOMPUTE-20261114T042139Z

Generated: 2026-11-16T00:41:50Z
Campaign: `FCLR-FUND-VOL-LIQ-REDTEAM-20261114T042139Z`
Prereg: `research_state/prereg_fclr011_recompute_20261114T042139Z.json` (status FROZEN_PRE_OUTCOMES, frozen before outcomes)

## Verdict: **NOT_REPRODUCED** (VALID_EXPLORATORY)

- Promotable: `False` (audit only, never promotable)
- Sealed FCLR-011 artifacts: unchanged (read-only in this cell)
- Smoke run: `False`

## Panel

- Panel: `research_state/session_20261116T0040Z/fclr011_recompute_panel_20261116T004150Z.parquet`
- Panel SHA-256: `41962f823e59de5989c7d854cb3180cad61a4cbc2f5f230133c41b321342c1f4`
- Rows: 29136
- Instruments: 5 ['BNBUSDT', 'BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'XRPUSDT']
- Test blocks (UTC days): 91
- Test window: ['2026-05-08T00:00:00Z', '2026-08-06T23:00:00Z']

## Coverage (test rows)

- test_rows_total: 10920
- test_rows_core_complete: 10905
- core_coverage: 0.998626

## Paired contrasts (QLIKE, lower is better)

| Contrast | n pairs | B QLIKE | A QLIKE | mean diff | 95% CI | rel reduction | Holm p | material | CI excl 0 |
|---|---|---|---|---|---|---|---|---|---|
| C2_vs_B1 | 10905 | 0.563193 | 2.21902 | 1.65582718 | [1.08325714, 2.31925702] | -294.0072% | 1.0 | False | False |
| C1_vs_B1 | 10905 | 0.563193 | 2.493112 | 1.9299197 | [1.28687695, 2.68084884] | -342.6749% | 1.0 | False | False |
| C2_vs_C1 | 10905 | 2.493112 | 2.21902 | -0.27409252 | [-0.36923154, -0.19176797] | 10.994% | 0.0 | True | True |

## Robustness

- LOIO: 0/5 instruments clear the 2% materiality floor
- Placebo (funding permutation, n=200): null p95 -204.0345%, p≈1.0, pass=False

## Per-symbol (C2 vs B1)

| Symbol | n | B1 QLIKE | C2 QLIKE | rel reduction |
|---|---|---|---|---|
| BNBUSDT | 2182 | 0.524682 | 3.282813 | -525.6767% |
| BTCUSDT | 2184 | 0.66013 | 2.960629 | -348.492% |
| ETHUSDT | 2183 | 0.612899 | 2.171316 | -254.2697% |
| SOLUSDT | 2178 | 0.484804 | 1.272375 | -162.4513% |
| XRPUSDT | 2178 | 0.533138 | 1.404079 | -163.3614% |

## Per-block (C2 vs B1)

| Block (UTC day) | n | rel reduction |
|---|---|---|
| 2026-05-08 | 120 | -264.7456% |
| 2026-05-09 | 120 | -106.7385% |
| 2026-05-10 | 120 | -1768.0671% |
| 2026-05-11 | 120 | -373.2432% |
| 2026-05-12 | 119 | -2084.3493% |
| 2026-05-13 | 120 | -4679.8407% |
| 2026-05-14 | 120 | -2222.6032% |
| 2026-05-15 | 120 | -491.1534% |
| 2026-05-16 | 120 | 32.8962% |
| 2026-05-17 | 120 | -140.843% |
| 2026-05-18 | 120 | -185.9906% |
| 2026-05-19 | 119 | 29.1347% |
| 2026-05-20 | 120 | 7.9118% |
| 2026-05-21 | 120 | -212.7223% |
| 2026-05-22 | 120 | -1025.2689% |
| 2026-05-23 | 120 | -1162.0907% |
| 2026-05-24 | 120 | -274.6062% |
| 2026-05-25 | 119 | -53.2042% |
| 2026-05-26 | 120 | -66.4324% |
| 2026-05-27 | 120 | -3515.7771% |
| 2026-05-28 | 120 | -518.7868% |
| 2026-05-29 | 120 | -307.9514% |
| 2026-05-30 | 120 | -464.9955% |
| 2026-05-31 | 120 | -329.3841% |
| 2026-06-01 | 120 | -3238.3892% |
| 2026-06-02 | 120 | -2346.3338% |
| 2026-06-03 | 120 | -1297.327% |
| 2026-06-04 | 120 | -540.7537% |
| 2026-06-05 | 120 | -104.0368% |
| 2026-06-06 | 119 | -17.4953% |
| 2026-06-07 | 120 | -146.3005% |
| 2026-06-08 | 119 | -29.7437% |
| 2026-06-09 | 120 | 13.6109% |
| 2026-06-10 | 120 | 26.0095% |
| 2026-06-11 | 120 | 28.0908% |
| 2026-06-12 | 120 | 24.0348% |
| 2026-06-13 | 120 | 30.7493% |
| 2026-06-14 | 120 | 3.6171% |
| 2026-06-15 | 120 | -303.4443% |
| 2026-06-16 | 120 | -53.0915% |
| 2026-06-17 | 120 | -867.5578% |
| 2026-06-18 | 120 | -274.4394% |
| 2026-06-19 | 120 | 26.0874% |
| 2026-06-20 | 120 | 48.8357% |
| 2026-06-21 | 120 | 8.9829% |
| 2026-06-22 | 120 | -72.0059% |
| 2026-06-23 | 120 | -14.858% |
| 2026-06-24 | 120 | -129.0743% |
| 2026-06-25 | 120 | -70.0543% |
| 2026-06-26 | 120 | -25.2578% |
| 2026-06-27 | 120 | 43.1822% |
| 2026-06-28 | 120 | 24.4659% |
| 2026-06-29 | 120 | 50.6426% |
| 2026-06-30 | 120 | 43.663% |
| 2026-07-01 | 120 | -294.4962% |
| 2026-07-02 | 120 | 42.8021% |
| 2026-07-03 | 120 | -142.4206% |
| 2026-07-04 | 120 | -643.0502% |
| 2026-07-05 | 120 | -612.8642% |
| 2026-07-06 | 120 | -2740.8724% |
| 2026-07-07 | 120 | -1102.5188% |
| 2026-07-08 | 120 | 18.3054% |
| 2026-07-09 | 120 | -75.4729% |
| 2026-07-10 | 120 | 21.0961% |
| 2026-07-11 | 120 | -69.633% |
| 2026-07-12 | 119 | -564.8075% |
| 2026-07-13 | 120 | -566.3094% |
| 2026-07-14 | 119 | -419.5007% |
| 2026-07-15 | 120 | -878.8301% |
| 2026-07-16 | 120 | -1736.7736% |
| 2026-07-17 | 119 | 20.5904% |
| 2026-07-18 | 120 | 60.5414% |
| 2026-07-19 | 120 | -331.955% |
| 2026-07-20 | 120 | -952.2853% |
| 2026-07-21 | 120 | -361.1924% |
| 2026-07-22 | 119 | -545.124% |
| 2026-07-23 | 119 | -69.4842% |
| 2026-07-24 | 120 | 19.7006% |
| 2026-07-25 | 120 | 56.8229% |
| 2026-07-26 | 119 | -566.484% |
| 2026-07-27 | 120 | -3791.2823% |
| 2026-07-28 | 119 | -983.8155% |
| 2026-07-29 | 120 | -4882.696% |
| 2026-07-30 | 119 | -300.6607% |
| 2026-07-31 | 118 | -53.0987% |
| 2026-08-01 | 120 | -61.5228% |
| 2026-08-02 | 120 | -109.8664% |
| 2026-08-03 | 120 | -603.6413% |
| 2026-08-04 | 120 | -531.8104% |
| 2026-08-05 | 120 | 28.5066% |
| 2026-08-06 | 120 | -3.3009% |

## Leakage audit

- target_not_equal_to_trailing_rv24h: False
- target_uses_strictly_future_bars: True
- funding_asof_backward_only: True
- funding_asof_min_lag_h: 0.0
- zero_fill_used: False
- forward_fill_used: False
- train_only_scaling: True
- splits_respect_embargo_days: True

target_rv24h is a forward sum over t+1..t+24 and never equals trailing rv24h; funding is attached with merge_asof(direction=backward, tolerance=24h) and the resulting lag is reported; no zero/forward fill; scaling fit on train rows only; 7d purge/embargo at both boundaries.


## Comparison to the sealed FCLR-011 result

| Contrast | Sealed rel reduction | Recomputed rel reduction |
|---|---|---|
| C2_vs_B1 | 4.94% | -294.0072 |
| C1_vs_B1 | 1.36% | -342.6749 |
| C2_vs_C1 | 3.63% | 10.994 |

## Notes

- Mark/index premium is NOT computable from the cached 2026 Binance archive (no markPriceKlines/indexPriceKlines/premiumIndexKlines); C2 degrades to C1 + mark/EMA24 distance. This is a limitation of the independent recompute, not a claim about the sealed result.
- No zero-fill, no forward-fill. Funding attached by backward merge_asof (<= 24h tolerance). Target is a strictly forward 24h realized variance.
