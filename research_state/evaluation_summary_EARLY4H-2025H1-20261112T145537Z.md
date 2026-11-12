# Track A / Track C Early 4h Evaluation — TRACKA-HL-EARLY4H-2025H1
**Timestamp (UTC):** 2026-11-12T14:55:37Z
**Prereg:** `tracka_prereg_early2025h1_20261112T134503Z.json` (sha256 fdd96bd116460ffd...)
**Panel:** `tracka_hl_early2025h1_panel_20261112T145529Z.parquet` (sha256 08c608035d179be8...)

## Verdicts
### Target `liq` — `INCONCLUSIVE_NUMERICAL_INSTABILITY`

| Model | Mean QLIKE |
|---|---|
| B0 | 24.160825 |
| B1 | 23.891846 |
| C1 | 1.6772025802700173e+24 |
| C2 | 278989949820.22394 |

| Contrast | Mean diff | 95% CI | Rel reduction % | p | Holm |
|---|---|---|---|---|---|
| C2_vs_B1 | 2.7899e+11 | [-18.9704, 8.12625e+11] | -1.16772e+12 | 0.178371 | False |
| C1_vs_B1 | 1.6772e+24 | [-1.41391, 4.88525e+24] | -7.01998e+24 | 0.178371 | False |
| C2_vs_C1 | -1.6772e+24 | [-4.88525e+24, -2.87189] | 100 | 0.178371 | False |

- Test blocks with data: [0, 1, 2, 3] (required 3)
- Paired instruments: 9 (required 5)
- Per-coin mean diff C2-B1: AVAX=23153.8358, BNB=-2.427, BTC=7.354, DOGE=9072777097.622, ETH=69.6541, LINK=-10.9149, SOL=2242353408252.253, SUI=1.914, XRP=2399.2038
- Per-block mean diff C2-B1: 0=-25.2238, 1=-13.0488, 2=2.124, 3=1067439807950.1693

### Target `rv` — `NOT_MET`

| Model | Mean QLIKE |
|---|---|
| B0 | 1.033781 |
| B1 | 0.829789 |
| C1 | 4.555811 |
| C2 | 1.073262 |

| Contrast | Mean diff | 95% CI | Rel reduction % | p | Holm |
|---|---|---|---|---|---|
| C2_vs_B1 | 0.243473 | [-0.0968074, 0.583405] | -29.3416 | 0.160591 | False |
| C1_vs_B1 | 3.72602 | [-0.087594, 11.3133] | -449.032 | 0.200158 | False |
| C2_vs_C1 | -3.48255 | [-11.3982, 0.65501] | 76.4419 | 0.257385 | False |

- Test blocks with data: [0, 1, 2, 3] (required 3)
- Paired instruments: 9 (required 5)
- Per-coin mean diff C2-B1: AVAX=-0.2174, BNB=0.6204, BTC=0.015, DOGE=0.4165, ETH=0.2894, LINK=0.5592, SOL=0.2223, SUI=0.1643, XRP=0.1215
- Per-block mean diff C2-B1: 0=0.5311, 1=0.6357, 2=0.1132, 3=-0.3061

## Compliance
- no_outcome_inspection_before_freeze: True
- no_threshold_shopping: True
- no_sealed_holdout_reuse: True
- no_binance_2024_conflation: True
- no_modeled_proxy_labels: True
- venue_consistent: Hyperliquid-only
