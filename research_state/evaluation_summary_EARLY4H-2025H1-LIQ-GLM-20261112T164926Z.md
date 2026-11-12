# Track A — Early 4h Liquidation GLM Evaluation — TRACKA-HL-EARLY4H-2025H1-LIQ-GLM
**Timestamp (UTC):** 2026-11-12T16:49:26Z
**Prereg:** `tracka_prereg_early2025h1_liq_glm_20261112T164838Z.json` (sha256 d9ebb279c04793f9...)
**Panel:** `tracka_hl_early2025h1_panel_20261112T145529Z.parquet` (sha256 08c608035d179be8...)
**Estimator:** Poisson/quasi-Poisson GLM, log link, IRLS, no regularization
**Target:** `t1_liq` (positive rows only)

## Verdict — `liq`: `INCONCLUSIVE_NUMERICAL_INSTABILITY`

| Model | Mean QLIKE | Converged | Iters | Max row QLIKE |
|---|---|---|---|---|
| B1 | 4.15034 | True | 7 | 212.773 |
| C1 | 4768.72 | True | 9 | 4.82783e+06 |
| C2 | 3.43491e+06 | True | 10 | 3.48042e+09 |

| Contrast | Mean diff | 95% CI | Rel reduction % | p | Holm |
|---|---|---|---|---|---|
| C2_vs_B1 | 3.4349e+06 | [-1.33168, 1.01058e+07] | -8.27619e+07 | 0.182741 | False |
| C1_vs_B1 | 4764.57 | [-0.190361, 14018] | -114799 | 0.182753 | False |
| C2_vs_C1 | 3.43014e+06 | [-1.13105, 1.00918e+07] | -71929.9 | 0.182741 | False |

- Test blocks with data: [0, 1, 2, 3] (required 3)
- Paired instruments: 9 (required 5)
- Per-coin mean diff C2-B1: AVAX=15.7301, BNB=0.7388, BTC=0.9227, DOGE=82756.2638, ETH=3.0261, LINK=0.6664, SOL=29003515.8699, SUI=0.3468, XRP=8.5195
- Per-block mean diff C2-B1: 0=0.3104, 1=-1.8672, 2=0.2939, 3=13371110.2562

## Gate
- materiality_ge_2pct: False
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
