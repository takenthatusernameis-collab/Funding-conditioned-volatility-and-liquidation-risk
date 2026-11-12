# Track A — Early 4h Liquidation GLM-Robust Evaluation — TRACKA-HL-EARLY4H-2025H1-LIQ-GLM-ROBUST
**Timestamp (UTC):** 2026-11-12T17:04:57Z
**Prereg:** `tracka_prereg_early2025h1_liq_glm_robust_20261112T165234Z.json` (sha256 f06060c7fccb5530...)
**Panel:** `tracka_hl_early2025h1_panel_20261112T145529Z.parquet` (sha256 08c608035d179be8...)
**Estimator:** Poisson/quasi-Poisson GLM, log link, IRLS, no regularization, features bounded to training range
**Target:** `t1_liq` (positive rows only)

## Verdict — `liq`: `NOT_MET`

| Model | Mean QLIKE | Converged | Iters | Max row QLIKE |
|---|---|---|---|---|
| B1 | 4.15034 | True | 7 | 212.773 |
| C1 | 4.1877 | True | 9 | 243.377 |
| C2 | 4.04994 | True | 7 | 319.053 |

| Contrast | Mean diff | 95% CI | Rel reduction % | p | Holm |
|---|---|---|---|---|---|
| C2_vs_B1 | -0.100401 | [-1.22988, 0.851253] | 2.4191 | 0.850006 | False |
| C1_vs_B1 | 0.0373615 | [-0.166213, 0.236183] | -0.900204 | 0.71589 | False |
| C2_vs_C1 | -0.137762 | [-1.12254, 0.608096] | 3.28969 | 0.755014 | False |

- Test blocks with data: [0, 1, 2, 3] (required 3)
- Paired instruments: 9 (required 5)
- Per-coin mean diff C2-B1: AVAX=0.7334, BNB=0.578, BTC=0.9315, DOGE=-0.1487, ETH=-2.9688, LINK=0.3346, SOL=-0.3123, SUI=0.1871, XRP=0.0357
- Per-block mean diff C2-B1: 0=-0.0431, 1=-1.6969, 2=0.1877, 3=1.1322

## Gate
- materiality_ge_2pct: True
- ci_upper_below_zero: False
- min_test_blocks_ge_3: True
- min_instruments_ge_5: True
- holm_pass: False
- single_coin_only: False

## Compliance
- no_outcome_inspection_before_freeze: True
- no_threshold_shopping: True
- no_sealed_holdout_reuse: True
- no_binance_2024_conflation: True
- no_modeled_proxy_labels: True
- venue_consistent: Hyperliquid-only
