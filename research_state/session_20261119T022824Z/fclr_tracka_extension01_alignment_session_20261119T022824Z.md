# Track A extension alignment (observed Hyperliquid liquidations)

- campaign: `FCLR-LIQ-TRACKA-EXTENSION-01-20261119T015256Z`
- session: `session_20261119T022824Z`
- months spec: `2025-11..2026-10` -> 2025-11..2026-10 (12 months); coins: 13 main-dex perps
- panel rows: 113880 -> `research_state/session_20261119T022824Z/fclr_tracka_extension01_panel_session_20261119T022824Z.csv`
- observed liquidation events: 1128446 (USD notional 20970455300)
- events joined to candle hours: 1128446 / 1128446 (yield 1.0000)
- hours with >=1 liquidation: 21557
- funding coverage: 1.000; OI coverage: 0.993
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
