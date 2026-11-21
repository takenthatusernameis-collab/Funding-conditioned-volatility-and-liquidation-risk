# FCLR-LIQ-OOS-FORECAST-001 — OOS Liquidation-Risk Forecast Evaluation
**Campaign:** FCLR-LIQ-OOS-FORECAST-001-20261121T055825Z  |  Session: 20261121T055825Z
**Panel:** combined liquidation `fclr_liq_combined_panel_20261115T181405Z.parquet` sha256 `81a100d5d0625832bebabaabea13b786e15319577721cfe8507da5b779ec7f14`
**Verdict:** `NOT_SUPPORTED`  |  All metrics pass: False

## Estimand
Out-of-sample forecast of next-24h observed notional-weighted liquidation intensity, C2 (funding-conditioned) vs B1 (RV-only), observed liquidations only (never modeled boundary breaches).

## Splits (chronological expanding walk-forward)
- Train: 2025-03-22 -> 2025-12-31 | Validation: 2026-01-01 -> 2026-03-31 (diagnostic, no tuning)
- Test blocks: 2026-04-01..2026-05-31 ; 2026-06-01..2026-08-31 ; 2026-09-01..2026-10-31 | purge 1 day

## Per-block summary
| block 0 | 2026-04-01..2026-05-31 | n_train=1764 | n_test=280 | event_rate=0.318 |
  | B1 | QLIKE=6.15245570930545 | Brier=0.21944416034742578 | LogLoss=0.6311406072349599 | n=280 |
  | C2 | QLIKE=6.156741629653714 | Brier=0.19239637936269482 | LogLoss=0.5704418754042392 | n=280 |
| block 1 | 2026-06-01..2026-08-31 | n_train=2044 | n_test=405 | event_rate=0.380 |
  | B1 | QLIKE=13.69104742018202 | Brier=0.23597205185919307 | LogLoss=0.6648455822786362 | n=405 |
  | C2 | QLIKE=14.241221904919994 | Brier=0.20430998489626706 | LogLoss=0.5986493634569006 | n=405 |
| block 2 | 2026-09-01..2026-10-31 | n_train=2449 | n_test=278 | event_rate=0.388 |
  | B1 | QLIKE=12.510070484376834 | Brier=0.23804190325235677 | LogLoss=0.6690670824130499 | n=278 |
  | C2 | QLIKE=13.979061849518674 | Brier=0.21911185087138335 | LogLoss=0.6300989498195516 | n=278 |

## Joint metric family (QLIKE / Brier / LogLoss) — block bootstrap + Holm, 2% floor
| metric | mean_B1 | mean_C2 | mean_diff(C2-B1) | CI_low | CI_high | CI_excl0_C2_better | p_value | Holm_adj_p | Holm_pass | rel_reduction | materiality>=2% | gate_pass |
| QLIKE | 11.15821536701558 | 11.814913522286426 | 0.6566981552708464 | 0.6566981552708464 | 0.6566981552708464 | False | 0.0 | 0.0 | True | -0.058853332156689545 | False | False |
| Brier | 0.23176396158297782 | 0.20511902870902107 | -0.02664493287395671 | -0.0266449328739566 | -0.0266449328739566 | True | 0.0 | 0.0 | True | 0.11496581561675255 | True | True |
| LogLoss | 0.6562642572787792 | 0.5995267137726553 | -0.05673754350612388 | -0.05673754350612374 | -0.05673754350612374 | True | 0.0 | 0.0 | True | 0.08645533087751565 | True | True |

## Verdict: `NOT_SUPPORTED`
SUPPORTED only if ALL three metrics clear every gate; otherwise honest NOT_SUPPORTED. No threshold-shopping or floor relaxation after seeing outcomes.

## Cross-references: FCLR-XSEC-002/004/005/006/007/008; FCLR-LIQ-COMBINED-PANEL; Track B modeled breaches (NOT_MET); Track A combined panel (NOT_MET).