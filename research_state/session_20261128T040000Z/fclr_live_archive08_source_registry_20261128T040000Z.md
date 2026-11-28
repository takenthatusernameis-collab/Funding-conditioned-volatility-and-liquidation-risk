# FCLR-LIVE-ARCHIVE-08 Source Registry — session_20261128T040000Z

**Campaign:** FCLR-LIVE-ARCHIVE-08-20261127T131654Z (Track-B modeled boundary-breach forecast)
**Session:** session_20261128T040000Z
**Generated:** 2026-11-28T04:00:00Z
**Experiment ID:** FCLR-LIVE-ARCHIVE-08

## Source

- **ID:** binance_public_archive
- **Type:** market_data_archive
- **Venue:** binance
- **Access:** unauthenticated (no API key, no signed request, no account)
- **Payment required:** false
- **Signup required:** false

## Datasets

1. `futures_um_daily_markPriceKlines_1h` — mark price; dedup by open_time; close>0; track: target + RV features + EMA distance
   - Layouts: nested_csv_2024_04_2024_09, flat_csv_2024_10_2024_12, csv_or_zip_2025_01_2026_10
2. `futures_um_daily_indexPriceKlines_1h` — index price; mark/index premium only
3. `futures_um_monthly_fundingRate` — signed funding + trailing 90d |funding| pct

## Cohort

- Symbols: BNBUSDT, BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT
- Months: 2024-04..2026-10 (31 months)
- Selection: coverage-only, outcome-blind (frozen, disjoint from 2021-2024 cohort)
- Common support N: 22608

## Cache

- Root: research_state/data_cache/<SYM>_<YYYY_MM>/
- Access: read-only reuse; no re-download
- Symbol-month dirs: 155 (5 symbols x 31 months)
- Gaps: 0

## Hash registry

- research_state/cached_inputs_hashes.json (20,694 entries)

## Sidecar verification

- Per-file .sha256 sidecars present; gaps disclosed in eval output
- XRPUSDT 2025-10-19 mark-price day has 24 negative closes; dropped by close>0; NOT zero-filled

## Admissibility

- Unauthenticated: true
- No credentials: true
- No payment: true
- Historical depth: 31 months, multi-regime
- Schema verified: true
- Admissible for research: true
- Admissible for Track A observed liquidations: false

## Design family

- Modeled boundary-breach forecast (Track-B)
- Estimand: out-of-sample AUC / log-loss / Brier
- NOT a risk overlay (campaign-07 forecast gate did NOT pass; RESEARCH_PROMPT section 9 forbids overlay)

## Note

Outcome-blind source registry for campaign-08. Mark-price-only common support S, |S|=22608, frozen before any outcome computation.
