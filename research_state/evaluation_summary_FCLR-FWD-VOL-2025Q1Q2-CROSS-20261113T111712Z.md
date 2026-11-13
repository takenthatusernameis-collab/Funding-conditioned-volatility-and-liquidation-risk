# Evaluation Summary — FCLR-FWD-VOL-2025Q1Q2-CROSS-20261113T111601Z

Generated: 2026-11-13T11:17:12Z
Verdict: **NOT_REPLICATED**

Window: 2025-05-01T00:00:00Z .. 2026-04-01T23:00:00Z (never previously tested; test blocks disjoint from FCLR-011, 2025-CROSS, 2024Q4-CROSS, 2025H2-CROSS, and forward cells)
Panel: `tracka_fwd_vol_2025q1q2_cross_panel_20261113T111712Z.parquet` (sha256 6d930a6a41869b82...)

## Primary (C2 vs B1, 24h QLIKE, pooled 3 blocks)

- mean diff (C2 - B1): -0.000737 (negative = C2 better)
- 95% CI: [-0.005287, 0.002960]
- relative reduction: 0.23%
- p_boot: 0.7700
- Holm-adjusted p: None
- n: 10800
- days: 90

## Checks

- materiality_ge_2pct: False
- ci_excludes_zero_improving: False
- instruments_ge_5: True
- blocks_ge_3: True
- loio_ge_4_of_5: False
- placebo_pass: False
- holm_pass: False
- leakage_audit_pass: True

## Per-block primary

- block 0: train 27509, test 3720
- block 1: train 31229, test 3600
- block 2: train 34829, test 3480

## LOIO (train on 4, evaluate held-out symbol)

- BTCUSDT: rel 0.5035431851235425, CI [-0.0037968917748020825, 0.0005328742912491465]
- ETHUSDT: rel 0.9953923253187916, CI [-0.008111703226810837, 0.0015087609475913015]
- BNBUSDT: rel -2.8524315006785006, CI [-0.009823718859350624, 0.02449438330735103]
- SOLUSDT: rel -3.2317634368745316, CI [-0.0016598364602497808, 0.025334653636523916]
- XRPUSDT: rel -0.639082190864802, CI [-0.009315706988503203, 0.013175200822802139]

## Placebo (funding permutation)

- null p95: 0.33% vs true 0.23% -> pass=False
