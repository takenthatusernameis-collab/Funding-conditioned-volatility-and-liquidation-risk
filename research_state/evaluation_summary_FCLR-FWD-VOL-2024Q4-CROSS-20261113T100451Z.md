# Evaluation Summary — FCLR-FWD-VOL-2024Q4-CROSS-20261113T091500Z

Generated: 2026-11-13T10:04:51Z
Verdict: **NOT_REPLICATED**

Window: 2024-04-01T00:00:00Z .. 2024-09-30T23:00:00Z (never previously tested; disjoint from FCLR-011, 2025-CROSS, and forward cells)
Panel: `tracka_fwd_vol_2024q4_cross_panel_20261113T100451Z.parquet` (sha256 5349fc345eb47936...)

## Primary (C2 vs B1, 24h QLIKE, pooled 3 blocks)

- mean diff (C2 - B1): 0.091136 (negative = C2 better)
- 95% CI: [-0.012223, 0.256785]
- relative reduction: -20.77%
- p_boot: 0.1850
- Holm-adjusted p: None
- n: 8880
- days: 69

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

- block 0: train 1080, test 3600
- block 1: train 4440, test 3600
- block 2: train 7680, test 1680

## LOIO (train on 4, evaluate held-out symbol)

- BTCUSDT: rel -8.313329591322592, CI [-0.009502325554305448, 0.11292008600368039]
- ETHUSDT: rel -24.817412056448436, CI [-0.008444502404114786, 0.32072669512476865]
- BNBUSDT: rel -11.21267175260545, CI [-0.006584263802630157, 0.12770980812664964]
- SOLUSDT: rel -80.36344079238637, CI [0.03144980820097814, 0.9008033210830774]
- XRPUSDT: rel 7.562738550803065, CI [-0.13277647036092216, 0.002769706890326449]

## Placebo (funding permutation)

- null p95: -19.72% vs true -20.77% -> pass=False
