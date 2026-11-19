# Track A exploratory admissibility verdict

- status: **ADMISSIBLE**
- instruments with observed liquidations: 13 (gate >= 5)
- complete months: 6 (gate >= 3)
- max coin-month candle gap: 0.0000 (gate <= 0.2)
- alignment yield: 1.0000 (gate >= 0.95)
- observed-only labels: True

## Gate detail

- `g1_provenance_hashed`: PASS
- `g2_instruments_ge_5`: PASS
- `g3_complete_months_ge_3`: PASS
- `g4_gap_rate_le_20pct`: PASS
- `g5_observed_labels_only`: PASS
- `g6_alignment_yield_ge_95pct`: PASS

## Consequences

Register FCLR-LIQ-TRACKA-CONFIRMATORY-01 only after extending the candle/funding/OI cache to 2026-05..2026-10 and re-running this audit.

No confirmatory claim is made in this exploratory session.
