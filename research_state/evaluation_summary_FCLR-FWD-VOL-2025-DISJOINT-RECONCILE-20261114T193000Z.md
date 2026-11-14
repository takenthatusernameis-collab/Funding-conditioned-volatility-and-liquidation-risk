# Evaluation Summary — FCLR-FWD-VOL-2025-DISJOINT-RECONCILE-20261114T193000Z

Generated: 2026-11-14T20:40:00Z
Prereg: `research_state/prereg_fclr_fwd_vol_2025_disjoint_reconcile_20261114T193000Z.json` (status FROZEN_PRE_OUTCOMES, frozen before outcomes)
Campaign: `FCLR-FWD-VOL-2025-DISJOINT-RECONCILE-20261114T193000Z`

## Verdict: **UNEXPLAINED**

- Rationale: existing+sealed=-3.165%, existing+corrected=-1.963%, cleaned+sealed=-5.396%, cleaned+corrected=-3.269%; max estimator swing=2.127pp, max data swing=2.231pp
- Audit-only, EXPLORATORY_ONLY, promotable=false. Does not reopen any sealed verdict.

## Attribution matrix (C2 vs B1, 24h relative QLIKE reduction %)

| | Sealed estimator | Corrected estimator |
|---|---|---|
| Existing panel | -3.165% | -1.963% |
| Cleaned panel | -5.396% | -3.269% |

Sealed reference (FCLR-FWD-VOL-2025-DISJOINT-CROSS): -1.963% (mean diff 0.006923, CI [-0.012604, 0.028030])

## Lineage audit (existing panel)

- row_count: 30120
- expected_row_count: 30120
- row_count_match: True
- duplicate_keys: 0
- no_duplicate_keys: True
- symbols: ['BNBUSDT', 'BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'XRPUSDT']
- symbols_match: True
- expected_span: ['2025-04-25T00:00:00Z', '2025-12-31T23:00:00Z']
- observed_span: ['2025-04-25T00:00:00Z', '2025-12-31T23:00:00Z']
- span_match: True
- embargo_days: 7
- embargo_enforced: True
- test_blocks_non_overlapping: True
- corrupt_day_rows: 24
- corrupt_day_expected_rows: 24
- corrupt_day_all_nonpositive: True
- corrupt_source_file: research_state/data_cache/XRPUSDT_2025_10/markPriceKlines-2025-10-19/XRPUSDT-1h-2025-10-19.csv
- source_file_exists: True
- all_pass: True

### Per-block row counts

- block 0: train 3600 rows, test 3600 rows, train/symbol {'BNBUSDT': 720, 'BTCUSDT': 720, 'ETHUSDT': 720, 'SOLUSDT': 720, 'XRPUSDT': 720}, test/symbol {'BNBUSDT': 720, 'BTCUSDT': 720, 'ETHUSDT': 720, 'SOLUSDT': 720, 'XRPUSDT': 720}
- block 1: train 3600 rows, test 3600 rows, train/symbol {'BNBUSDT': 720, 'BTCUSDT': 720, 'ETHUSDT': 720, 'SOLUSDT': 720, 'XRPUSDT': 720}, test/symbol {'BNBUSDT': 720, 'BTCUSDT': 720, 'ETHUSDT': 720, 'SOLUSDT': 720, 'XRPUSDT': 720}
- block 2: train 3600 rows, test 3720 rows, train/symbol {'BNBUSDT': 720, 'BTCUSDT': 720, 'ETHUSDT': 720, 'SOLUSDT': 720, 'XRPUSDT': 720}, test/symbol {'BNBUSDT': 744, 'BTCUSDT': 744, 'ETHUSDT': 744, 'SOLUSDT': 744, 'XRPUSDT': 744}

## Cleaned panel build report

- source_panel: research_state/tracka_fwd_vol_2025_disjoint_cross_panel_20261114T191615Z.parquet
- source_sha256: de0ca73e7d092a205e5f8c1163d56437384d1b15d65b4a27bc54a57e21738cba
- removed_rows: 24
- removed_symbol: XRPUSDT
- removed_day: 2025-10-19
- removed_reason: cached mark close column holds premium-index values (nonpositive prices)
- recomputed_symbols: ['XRPUSDT']
- rows_after: 30096
- row_count_delta: 24
- imputation_used: False
- forward_fill_used: False
- target_rows_removed: 24
- coverage_note: only XRP rolling RV and forward targets change; all other symbols and columns are copied unchanged
- all_pass: True
- panel_path: research_state/fclr_fwd_vol_2025_disjoint_reconcile_panel_20261114T204000Z.parquet
- panel_sha256: 7a9a831747b0edc21c5af5164a6b3bc5603f57a8e4f3981513c0a5858f3752e2
- row_count: 30096
- key_count: 30096
- generated_utc: 2026-11-14T20:40:00Z

### Cleaned panel checks

- removed_row_count_expected_24: True
- no_duplicate_keys: True
- symbols_unchanged: True
- other_symbols_unchanged: True
- no_nonpositive_marks: True
- row_order_preserved: True

## Cell details

### existing panel + sealed estimator

- status: VALID_EXPLORATORY, valid rows: 28944, instruments: 5, blocks: [0, 1, 2]

| Contrast | n | mean diff | 95% CI | rel reduction | Holm p | material | CI excl 0 |
|---|---|---|---|---|---|---|---|
| h6_C2_vs_B1 | 10800 | 0.021130 | [-0.014958, 0.062513] | -2.589% | 1.0000 | False | False |
| h6_C1_vs_B1 | 10800 | 0.011496 | [0.002234, 0.022220] | -1.408% | 0.1600 | False | False |
| h6_C2_vs_C1 | 10800 | 0.009635 | [-0.023929, 0.046078] | -1.164% | 1.0000 | False | False |
| h24_C2_vs_B1 | 10800 | 0.011788 | [-0.011441, 0.038022] | -3.165% | 1.0000 | False | False |
| h24_C1_vs_B1 | 10800 | 0.002608 | [-0.002967, 0.008711] | -0.700% | 1.0000 | False | False |
| h24_C2_vs_C1 | 10800 | 0.009180 | [-0.011992, 0.033595] | -2.447% | 1.0000 | False | False |
| h72_C2_vs_B1 | 10560 | -0.000158 | [-0.007684, 0.006976] | 0.081% | 1.0000 | False | False |
| h72_C1_vs_B1 | 10560 | -0.000127 | [-0.003330, 0.002861] | 0.065% | 1.0000 | False | False |
| h72_C2_vs_C1 | 10560 | -0.000031 | [-0.006982, 0.006785] | 0.016% | 1.0000 | False | False |
| h168_C2_vs_B1 | 10080 | 0.007480 | [0.002281, 0.013808] | -5.981% | 0.0120 | False | False |
| h168_C1_vs_B1 | 10080 | 0.001147 | [-0.000726, 0.003107] | -0.917% | 1.0000 | False | False |
| h168_C2_vs_C1 | 10080 | 0.006333 | [0.001786, 0.011818] | -5.018% | 0.0550 | False | False |

- LOIO: 0/5 instruments clear the 2.0% floor
- Placebo: null p95 -3.55988724992923, true -3.1648455064014294, pass=True

  - LOIO BTCUSDT: rel -2.353%, CI [-0.006455584860056525, 0.02497963153677862], material=False
  - LOIO ETHUSDT: rel -7.928%, CI [-0.0036092873085629457, 0.07807275579090293], material=False
  - LOIO BNBUSDT: rel -2.932%, CI [-0.03516904947236626, 0.06621260214299765], material=False
  - LOIO SOLUSDT: rel -10.588%, CI [0.002779899283682122, 0.08197690303808619], material=False
  - LOIO XRPUSDT: rel -2.915%, CI [-0.012706955102222311, 0.03659373969142674], material=False

Per-block primary (C2 vs B1):
- block_0: mean diff 0.061612, rel -16.725%, n=3600
- block_1: mean diff -0.014003, rel 3.952%, n=3600
- block_2: mean diff -0.012246, rel 3.103%, n=3600

### existing panel + corrected estimator

- status: VALID_EXPLORATORY, valid rows: 28944, instruments: 5, blocks: [0, 1, 2]

| Contrast | n | mean diff | 95% CI | rel reduction | Holm p | material | CI excl 0 |
|---|---|---|---|---|---|---|---|
| h6_C2_vs_B1 | 10800 | 0.012498 | [-0.008885, 0.037061] | -1.849% | 1.0000 | False | False |
| h6_C1_vs_B1 | 10800 | 0.001800 | [-0.004430, 0.008417] | -0.266% | 1.0000 | False | False |
| h6_C2_vs_C1 | 10800 | 0.010698 | [-0.007915, 0.032006] | -1.579% | 1.0000 | False | False |
| h24_C2_vs_B1 | 10800 | 0.006923 | [-0.013104, 0.027938] | -1.963% | 1.0000 | False | False |
| h24_C1_vs_B1 | 10800 | 0.000014 | [-0.004946, 0.004638] | -0.004% | 1.0000 | False | False |
| h24_C2_vs_C1 | 10800 | 0.006909 | [-0.010602, 0.025683] | -1.959% | 1.0000 | False | False |
| h72_C2_vs_B1 | 10560 | -0.000138 | [-0.007144, 0.006661] | 0.071% | 1.0000 | False | False |
| h72_C1_vs_B1 | 10560 | -0.000768 | [-0.003332, 0.001542] | 0.395% | 1.0000 | False | False |
| h72_C2_vs_C1 | 10560 | 0.000630 | [-0.006002, 0.007047] | -0.325% | 1.0000 | False | False |
| h168_C2_vs_B1 | 10080 | 0.006439 | [0.001034, 0.013371] | -4.436% | 0.2040 | False | False |
| h168_C1_vs_B1 | 10080 | 0.001791 | [-0.000073, 0.003924] | -1.234% | 0.6930 | False | False |
| h168_C2_vs_C1 | 10080 | 0.004649 | [-0.000318, 0.010402] | -3.164% | 0.6930 | False | False |

- LOIO: 1/5 instruments clear the 2.0% floor
- Placebo: null p95 -2.3179127777623587, true -1.9633752428119804, pass=True

  - LOIO BTCUSDT: rel -2.098%, CI [-0.005255330889459619, 0.023973911941966138], material=False
  - LOIO ETHUSDT: rel -6.262%, CI [-0.00838392353697605, 0.05649692607221906], material=False
  - LOIO BNBUSDT: rel 3.331%, CI [-0.04965139358215079, 0.030309834307375078], material=True
  - LOIO SOLUSDT: rel -6.674%, CI [-0.00832606200522786, 0.05151237688026703], material=False
  - LOIO XRPUSDT: rel -1.728%, CI [-0.014728953153011353, 0.027292385718208634], material=False

Per-block primary (C2 vs B1):
- block_0: mean diff 0.044565, rel -12.294%, n=3600
- block_1: mean diff -0.009866, rel 3.519%, n=3600
- block_2: mean diff -0.013929, rel 3.356%, n=3600

### cleaned panel + sealed estimator

- status: VALID_EXPLORATORY, valid rows: 29136, instruments: 5, blocks: [0, 1, 2]

| Contrast | n | mean diff | 95% CI | rel reduction | Holm p | material | CI excl 0 |
|---|---|---|---|---|---|---|---|
| h6_C2_vs_B1 | 10800 | 0.035577 | [0.003045, 0.075217] | -4.347% | 0.2340 | False | False |
| h6_C1_vs_B1 | 10800 | 0.011021 | [0.001909, 0.021735] | -1.347% | 0.1800 | False | False |
| h6_C2_vs_C1 | 10800 | 0.024556 | [-0.004477, 0.056929] | -2.961% | 0.6960 | False | False |
| h24_C2_vs_B1 | 10800 | 0.020151 | [-0.002431, 0.045346] | -5.396% | 0.6080 | False | False |
| h24_C1_vs_B1 | 10800 | 0.002196 | [-0.003246, 0.008238] | -0.588% | 1.0000 | False | False |
| h24_C2_vs_C1 | 10800 | 0.017955 | [-0.001726, 0.040674] | -4.780% | 0.6090 | False | False |
| h72_C2_vs_B1 | 10560 | 0.003784 | [-0.003406, 0.010620] | -1.923% | 0.9880 | False | False |
| h72_C1_vs_B1 | 10560 | -0.000513 | [-0.003586, 0.002401] | 0.261% | 1.0000 | False | False |
| h72_C2_vs_C1 | 10560 | 0.004297 | [-0.001994, 0.010674] | -2.190% | 0.8300 | False | False |
| h168_C2_vs_B1 | 10080 | 0.007878 | [0.002558, 0.014277] | -6.235% | 0.0120 | False | False |
| h168_C1_vs_B1 | 10080 | 0.000980 | [-0.001102, 0.003062] | -0.775% | 1.0000 | False | False |
| h168_C2_vs_C1 | 10080 | 0.006898 | [0.002360, 0.012375] | -5.417% | 0.0220 | False | False |

- LOIO: 0/5 instruments clear the 2.0% floor
- Placebo: null p95 -5.820476724036456, true -5.396112193339789, pass=True

  - LOIO BTCUSDT: rel -3.606%, CI [-0.0001730220938773345, 0.028831890840213585], material=False
  - LOIO ETHUSDT: rel -9.568%, CI [0.003502244395193064, 0.0860870018094132], material=False
  - LOIO BNBUSDT: rel -9.063%, CI [-0.011185934763406931, 0.0851572802903876], material=False
  - LOIO SOLUSDT: rel -12.719%, CI [0.009819390873139232, 0.09279481723331204], material=False
  - LOIO XRPUSDT: rel -2.915%, CI [-0.012706955102195756, 0.03659373969147132], material=False

Per-block primary (C2 vs B1):
- block_0: mean diff 0.061612, rel -16.725%, n=3600
- block_1: mean diff 0.011030, rel -3.086%, n=3600
- block_2: mean diff -0.012189, rel 3.089%, n=3600

### cleaned panel + corrected estimator

- status: VALID_EXPLORATORY, valid rows: 29136, instruments: 5, blocks: [0, 1, 2]

| Contrast | n | mean diff | 95% CI | rel reduction | Holm p | material | CI excl 0 |
|---|---|---|---|---|---|---|---|
| h6_C2_vs_B1 | 10800 | 0.017691 | [-0.002635, 0.041231] | -2.620% | 0.7680 | False | False |
| h6_C1_vs_B1 | 10800 | 0.001669 | [-0.004490, 0.008142] | -0.247% | 1.0000 | False | False |
| h6_C2_vs_C1 | 10800 | 0.016021 | [-0.001431, 0.035949] | -2.367% | 0.7200 | False | False |
| h24_C2_vs_B1 | 10800 | 0.011503 | [-0.008375, 0.031940] | -3.269% | 1.0000 | False | False |
| h24_C1_vs_B1 | 10800 | -0.000112 | [-0.004975, 0.004468] | 0.032% | 1.0000 | False | False |
| h24_C2_vs_C1 | 10800 | 0.011615 | [-0.005531, 0.029897] | -3.302% | 1.0000 | False | False |
| h72_C2_vs_B1 | 10560 | 0.002092 | [-0.004770, 0.008579] | -1.081% | 1.0000 | False | False |
| h72_C1_vs_B1 | 10560 | -0.000990 | [-0.003502, 0.001206] | 0.511% | 1.0000 | False | False |
| h72_C2_vs_C1 | 10560 | 0.003082 | [-0.003471, 0.009480] | -1.600% | 1.0000 | False | False |
| h168_C2_vs_B1 | 10080 | 0.007249 | [0.002084, 0.014147] | -5.057% | 0.0600 | False | False |
| h168_C1_vs_B1 | 10080 | 0.001998 | [0.000122, 0.004146] | -1.394% | 0.3960 | False | False |
| h168_C2_vs_C1 | 10080 | 0.005251 | [0.000368, 0.010973] | -3.613% | 0.3960 | False | False |

- LOIO: 0/5 instruments clear the 2.0% floor
- Placebo: null p95 -3.649988529303665, true -3.2693624978152895, pass=True

  - LOIO BTCUSDT: rel -2.452%, CI [-0.0034601990549401255, 0.024691357554687283], material=False
  - LOIO ETHUSDT: rel -7.291%, CI [-0.003643935837183127, 0.06160782732204339], material=False
  - LOIO BNBUSDT: rel 0.176%, CI [-0.03826837624265093, 0.04398046999769058], material=False
  - LOIO SOLUSDT: rel -8.305%, CI [-0.0022567025266987516, 0.05683219468374048], material=False
  - LOIO XRPUSDT: rel -1.728%, CI [-0.014728953153011292, 0.027292385718208714], material=False

Per-block primary (C2 vs B1):
- block_0: mean diff 0.044565, rel -12.294%, n=3600
- block_1: mean diff 0.003269, rel -1.170%, n=3600
- block_2: mean diff -0.013324, rel 3.222%, n=3600

## Leakage audit (per cell)

### existing + sealed
- panel: existing
- estimator: sealed
- target_forward_only: True
- features_causal_at_t: True
- embargo_days: 7
- embargo_enforced_between_train_and_test: True
- train_only_scaling: False
- train_only_smearing: False
- zero_fill_used: False
- forward_fill_used: False
- notes: target_h is the forward sum of squared returns over t+1..t+h; every feature is computed from bars ending at or before t; no fill is applied to any missing feature or target; scaling and smearing (corrected arm) are fitted on train rows only.

### existing + corrected
- panel: existing
- estimator: corrected
- target_forward_only: True
- features_causal_at_t: True
- embargo_days: 7
- embargo_enforced_between_train_and_test: True
- train_only_scaling: True
- train_only_smearing: True
- zero_fill_used: False
- forward_fill_used: False
- notes: target_h is the forward sum of squared returns over t+1..t+h; every feature is computed from bars ending at or before t; no fill is applied to any missing feature or target; scaling and smearing (corrected arm) are fitted on train rows only.

### cleaned + sealed
- panel: cleaned
- estimator: sealed
- target_forward_only: True
- features_causal_at_t: True
- embargo_days: 7
- embargo_enforced_between_train_and_test: True
- train_only_scaling: False
- train_only_smearing: False
- zero_fill_used: False
- forward_fill_used: False
- notes: target_h is the forward sum of squared returns over t+1..t+h; every feature is computed from bars ending at or before t; no fill is applied to any missing feature or target; scaling and smearing (corrected arm) are fitted on train rows only.

### cleaned + corrected
- panel: cleaned
- estimator: corrected
- target_forward_only: True
- features_causal_at_t: True
- embargo_days: 7
- embargo_enforced_between_train_and_test: True
- train_only_scaling: True
- train_only_smearing: True
- zero_fill_used: False
- forward_fill_used: False
- notes: target_h is the forward sum of squared returns over t+1..t+h; every feature is computed from bars ending at or before t; no fill is applied to any missing feature or target; scaling and smearing (corrected arm) are fitted on train rows only.

## Interpretation

Neither estimator conventions nor the cleaned data copy produce a material, dominant swing (sealed -3.165% vs -1.963%; existing -3.165% vs -5.396% on sealed estimator). The EXPLORATORY_NULL is not attributable to either candidate mechanism and should be preserved as a bounded negative result.

---

*All results EXPLORATORY_ONLY, promotable=false. No sealed artifact mutated.*
