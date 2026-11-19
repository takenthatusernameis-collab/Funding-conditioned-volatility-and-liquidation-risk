# Track A exploratory alignment (observed Hyperliquid liquidations)

- campaign: `FCLR-LIQ-TRACKA-EXPLORATORY-01-20261118T201919Z`
- window: 2025-11..2026-04; coins: 13 main-dex perps
- panel rows: 56472 -> `research_state/session_20261118T201919Z/fclr_tracka_exploratory01_panel_20261118T201919Z.csv`
- observed liquidation events: 537829 (USD notional 13021418299)
- events joined to candle hours: 537829 / 537829 (yield 1.0000)
- hours with >=1 liquidation: 11106
- funding coverage: 1.000; OI coverage: 0.994
- max coin-month candle gap rate: 0.0000

## Gates

- `g1_provenance_hashed`: PASS
- `g2_instruments_ge_5`: PASS
- `g3_complete_months_ge_3`: PASS
- `g4_gap_rate_le_20pct`: PASS
- `g5_observed_labels_only`: PASS
- `g6_alignment_yield_ge_95pct`: PASS

**Verdict:** `ADMISSIBLE`

Absence from the feed is not evidence of no liquidation; the panel labels observed events only. This is an admissibility assessment, not a forecast test.
