# Track A / Track C Early 4h Evaluation — TRACKA-HL-EARLY4H-2025H1
**Timestamp (UTC):** 2026-11-12T13:46:34Z
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
| B0 | 19.267881 |
| B1 | 19.267881 |
| C1 | 19.267881 |
| C2 | 19.267881 |

| Contrast | Mean diff | 95% CI | Rel reduction % | p | Holm |
|---|---|---|---|---|---|
| C2_vs_B1 | 1.25796e-15 | [1.06093e-15, 1.45577e-15] | -6.5288e-15 | 8.59491e-36 | True |
| C1_vs_B1 | 4.63234e-15 | [4.29138e-15, 4.96143e-15] | -2.40418e-14 | 9.82188e-162 | True |
| C2_vs_C1 | -3.37438e-15 | [-3.80325e-15, -3.04061e-15] | 1.7513e-14 | 2.18235e-67 | True |

- Test blocks with data: [0, 1, 2, 3] (required 3)
- Paired instruments: 9 (required 5)
- Per-coin mean diff C2-B1: AVAX=0.0, BNB=-0.0, BTC=0.0, DOGE=0.0, ETH=0.0, LINK=0.0, SOL=0.0, SUI=0.0, XRP=0.0
- Per-block mean diff C2-B1: 0=0.0, 1=0.0, 2=0.0, 3=0.0

## Compliance
- no_outcome_inspection_before_freeze: True
- no_threshold_shopping: True
- no_sealed_holdout_reuse: True
- no_binance_2024_conflation: True
- no_modeled_proxy_labels: True
- venue_consistent: Hyperliquid-only
