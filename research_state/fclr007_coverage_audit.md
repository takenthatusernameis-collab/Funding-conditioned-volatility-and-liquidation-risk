# FCLR-007 Coverage Audit (PRE-EXECUTION, NO OUTCOME INSPECTION)

Timestamp: 2026-10-31T00:18:20Z
Panel: 2026-04-01 .. 2026-07-31
Symbols: BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT

## Verified
- Data cache contains unsealed 2026 Apr-Jul markPriceKlines/indexPriceKlines/fundingRate for all 5 symbols (~122 days)
- ~4 non-overlapping 30-day blocks feasible (>=3 required)
- Common timestamp alignment to be enforced by pipeline

## Frozen split plan (to be enforced)
- Chronological 60/20/20 with 7-day purge/embargo
- Splits frozen before outcomes (split_boundaries_fclr007.frozen_before_outcomes: true)

## Source hashes (to be captured at runtime)
- Will record file hashes for all inputs used
