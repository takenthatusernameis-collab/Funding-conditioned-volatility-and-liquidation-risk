# Evaluation Summary — FCLR-FWD-VOL-2025H2-CROSS-20261113T102139Z

Generated: 2026-11-13T10:22:40Z
Verdict: **NOT_REPLICATED**

Window: 2025-04-01T00:00:00Z .. 2025-10-15T23:00:00Z (never previously tested; disjoint from FCLR-011, 2025-CROSS, 2024Q4-CROSS, and forward cells)
Panel: `tracka_fwd_vol_2025h2_cross_panel_20261113T102240Z.parquet` (sha256 61cef0e6cac22084...)

## Primary (C2 vs B1, 24h QLIKE, pooled 3 blocks)

- mean diff (C2 - B1): 0.027446 (negative = C2 better)
- 95% CI: [0.002173, 0.071397]
- relative reduction: -8.97%
- p_boot: 0.0090
- Holm-adjusted p: None
- n: 10680
- days: 84

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

- block 0: train 12000, test 3600
- block 1: train 15360, test 3600
- block 2: train 18600, test 3480

## LOIO (train on 4, evaluate held-out symbol)

- BTCUSDT: rel -4.083178053795394, CI [0.0030857425227737373, 0.022200455338575096]
- ETHUSDT: rel -1.2171983569534013, CI [-0.0026239120101443367, 0.011924199884347042]
- BNBUSDT: rel -0.8814915749183864, CI [-0.024914457633755858, 0.02593855785408064]
- SOLUSDT: rel -108.46846947488042, CI [0.011397647075984512, 0.6949391491322396]
- XRPUSDT: rel -0.37731267220226267, CI [-0.005367484609375148, 0.007640052833048791]

## Placebo (funding permutation)

- null p95: -1.15% vs true -8.97% -> pass=False
