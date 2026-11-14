# Evaluation Summary — FCLR-FWD-VOL-2025-DISJOINT-CROSS-20261114T183000Z

Generated: 2026-11-14T19:16:15Z
Verdict: **EXPLORATORY_NULL** (promotable=false, max_status=EXPLORATORY_ONLY)

Window: 2025-04-25T00:00:00Z .. 2025-12-31T23:00:00Z (disjoint 2025 test blocks: 2025-06, 2025-11, 2025-12)
Panel: `tracka_fwd_vol_2025_disjoint_cross_panel_20261114T191615Z.parquet` (sha256 de0ca73e7d092a20...)

## Primary (C2 vs B1, 24h QLIKE, pooled 3 blocks)

- mean diff (C2 - B1): 0.006923 (negative = C2 better)
- 95% CI: [-0.012604, 0.028030]
- relative reduction: -1.96%
- p_boot: 0.5350
- Holm-adjusted p: None
- n: 10800
- days: 90

## Checks

- materiality_ge_2pct: False
- ci_excludes_zero_improving: False
- instruments_ge_5: True
- blocks_ge_3: True
- loio_ge_4_of_5: False
- placebo_pass: True
- holm_pass: False
- leakage_audit_pass: True

## Per-block primary

- block 0: train 2025-04-25T00:00:00Z..2025-05-24T23:00:00Z (2760 rows), test 2025-06-01T00:00:00Z..2025-06-30T23:00:00Z (3600 rows)
- block 1: train 2025-09-25T00:00:00Z..2025-10-24T23:00:00Z (3432 rows), test 2025-11-01T00:00:00Z..2025-11-30T23:00:00Z (3600 rows)
- block 2: train 2025-10-25T00:00:00Z..2025-11-23T23:00:00Z (3552 rows), test 2025-12-01T00:00:00Z..2025-12-31T23:00:00Z (3600 rows)

## LOIO (train on 4, evaluate held-out symbol)

- BTCUSDT: rel -2.0977536690971146, CI [-0.00510070752540765, 0.022703259476102956]
- ETHUSDT: rel -6.2623744001755615, CI [-0.0061509632073842675, 0.05876675735597028]
- BNBUSDT: rel 3.330818093383085, CI [-0.04757750538595601, 0.033320825848289035]
- SOLUSDT: rel -6.673768950160815, CI [-0.005732780515136452, 0.050705587167973305]
- XRPUSDT: rel -1.7281552671827116, CI [-0.016343730714990234, 0.026517199850771278]

## Placebo (funding permutation)

- null p95: -1.97% vs true -1.96% -> pass=True


## Exploratory status

- promotable: false
- max_status: EXPLORATORY_ONLY
- Gate 4 Binance v5 terms: EXTERNAL_BLOCKED (no RESOLVED_VERIFIED trigger)
