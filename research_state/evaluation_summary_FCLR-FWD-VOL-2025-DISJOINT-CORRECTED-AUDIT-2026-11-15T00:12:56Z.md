# Evaluation Summary — FCLR-FWD-VOL-2025-DISJOINT-CORRECTED-AUDIT-2026-11-15T00:12:56Z

Generated: 2026-11-15T00:12:56Z
Prereg: `research_state/prereg_fclr_fwd_vol_2025_disjoint_corrected_audit_2026-11-15T00:12:56Z.json` (status FROZEN_PRE_OUTCOMES, frozen before outcomes)
Campaign: `FCLR-FWD-VOL-2025-DISJOINT-CORRECTED-AUDIT`

## Verdict: **NOT_EXPLAINED_BY_ESTIMATOR**

- Rationale: corrected=-1.963%, sealed_reference=-1.963%, swing=0.000pp, sign_flip=False
- Corrected-estimator robustness audit, EXPLORATORY_ONLY, promotable=false. Does not reopen any sealed verdict.

## Sealed reference (FCLR-FWD-VOL-2025-DISJOINT-CROSS-20261114T183000Z)

- primary contrast: C2_vs_B1 (24h QLIKE)
- mean_diff: 0.006923
- rel_reduction_pct: -1.963%
- 95% CI: [-0.012604, 0.028030]
- n: 10800, days: 90

## Corrected-estimator result (primary C2 vs B1, 24h QLIKE)

- mean_diff: 0.006923
- rel_reduction_pct: -1.963%
- 95% CI: [-0.013104, 0.027938]
- p_boot: 0.5050
- n: 10800, days: 90
- Holm p (primary): 1.0

- Swing vs sealed reference: 0.000 pp
- Sign flip: False

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
- all_pass: True

### Per-block row counts

- block 0: train 3600 rows, test 3600 rows, train/symbol {'BNBUSDT': 720, 'BTCUSDT': 720, 'ETHUSDT': 720, 'SOLUSDT': 720, 'XRPUSDT': 720}, test/symbol {'BNBUSDT': 720, 'BTCUSDT': 720, 'ETHUSDT': 720, 'SOLUSDT': 720, 'XRPUSDT': 720}
- block 1: train 3600 rows, test 3600 rows, train/symbol {'BNBUSDT': 720, 'BTCUSDT': 720, 'ETHUSDT': 720, 'SOLUSDT': 720, 'XRPUSDT': 720}, test/symbol {'BNBUSDT': 720, 'BTCUSDT': 720, 'ETHUSDT': 720, 'SOLUSDT': 720, 'XRPUSDT': 720}
- block 2: train 3600 rows, test 3720 rows, train/symbol {'BNBUSDT': 720, 'BTCUSDT': 720, 'ETHUSDT': 720, 'SOLUSDT': 720, 'XRPUSDT': 720}, test/symbol {'BNBUSDT': 744, 'BTCUSDT': 744, 'ETHUSDT': 744, 'SOLUSDT': 744, 'XRPUSDT': 744}

## Cell details

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
- Placebo: null p95 -2.317912777762358, true -1.9633752428119808, pass=True

  - LOIO BTCUSDT: rel -2.098%, CI [-0.005255330889459642, 0.023973911941966176], material=False
  - LOIO ETHUSDT: rel -6.262%, CI [-0.008383923536976081, 0.05649692607221912], material=False
  - LOIO BNBUSDT: rel 3.331%, CI [-0.04965139358215072, 0.030309834307374963], material=True
  - LOIO SOLUSDT: rel -6.674%, CI [-0.008326062005227888, 0.05151237688026724], material=False
  - LOIO XRPUSDT: rel -1.728%, CI [-0.014728953153011296, 0.027292385718208672], material=False

Per-block primary (C2 vs B1):
- block_0: mean diff 0.044565, rel -12.294%, n=3600
- block_1: mean diff -0.009866, rel 3.519%, n=3600
- block_2: mean diff -0.013929, rel 3.356%, n=3600

## Leakage audit

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

The corrected estimator reproduces the sealed reference (-1.963% vs -1.963%, swing 0.000pp) with no material sign flip. The 2025 EXPLORATORY_NULL is NOT attributable to estimator conventions (train-only standardization + Duan smearing); it should be preserved as a bounded negative result.

---

*All results EXPLORATORY_ONLY, promotable=false. No sealed artifact mutated.*
