# Track A / Track C Early 4h Evaluation — TRACKA-HL-EARLY4H-2025H1
**Timestamp (UTC):** 2026-11-12T13:45:36Z
**Prereg:** `tracka_prereg_early2025h1_20261112T134503Z.json` (sha256 fdd96bd116460ffd...)
**Panel:** `tracka_hl_early2025h1_panel_20261112T134520Z.parquet` (sha256 1d6bf748daf6217f...)

## Verdicts
### Target `liq` — `NOT_MET`

| Model | Mean QLIKE |
|---|---|
| B0 | 0.0 |
| B1 | 0.0 |
| C1 | 0.0 |
| C2 | 0.0 |

| Contrast | Mean diff | 95% CI | Rel reduction % | p | Holm |
|---|---|---|---|---|---|
| C2_vs_B1 | 0 | [0, 0] | n/a | 1 | False |
| C1_vs_B1 | 0 | [0, 0] | n/a | 1 | False |
| C2_vs_C1 | 0 | [0, 0] | n/a | 1 | False |

- Test blocks with data: [0, 1, 2, 3] (required 3)
- Paired instruments: 9 (required 5)
- Per-coin mean diff C2-B1: AVAX=0.0, BNB=0.0, BTC=0.0, DOGE=0.0, ETH=0.0, LINK=0.0, SOL=0.0, SUI=0.0, XRP=0.0
- Per-block mean diff C2-B1: 0=0.0, 1=0.0, 2=0.0, 3=0.0

### Target `rv` — `NOT_MET`

| Model | Mean QLIKE |
|---|---|
| B0 | 2.384346 |
| B1 | 2.384346 |
| C1 | 2.384346 |
| C2 | 2.384346 |

| Contrast | Mean diff | 95% CI | Rel reduction % | p | Holm |
|---|---|---|---|---|---|
| C2_vs_B1 | 7.78861e-15 | [3.95568e-15, 1.07634e-14] | -3.26656e-13 | 7.29997e-06 | True |
| C1_vs_B1 | 9.27757e-15 | [4.44067e-15, 1.29507e-14] | -3.89104e-13 | 1.92429e-05 | True |
| C2_vs_C1 | -1.48897e-15 | [-2.3422e-15, -4.84998e-16] | 6.24476e-14 | 0.00167392 | True |

- Test blocks with data: [0, 1, 2, 3] (required 3)
- Paired instruments: 9 (required 5)
- Per-coin mean diff C2-B1: AVAX=0.0, BNB=0.0, BTC=0.0, DOGE=0.0, ETH=0.0, LINK=0.0, SOL=0.0, SUI=0.0, XRP=0.0
- Per-block mean diff C2-B1: 0=0.0, 1=0.0, 2=0.0, 3=0.0

## Compliance
- no_outcome_inspection_before_freeze: True
- no_threshold_shopping: True
- no_sealed_holdout_reuse: True
- no_binance_2024_conflation: True
- no_modeled_proxy_labels: True
- venue_consistent: Hyperliquid-only
