# H002 Methodology Dossier — Shek Funding-Extreme Correction-Time Replication

Updated: 2026-10-30T12:04:00Z
Status: PARTIAL_REPLICATION (SEALED_PARTIAL)
Blocker: Shek (SSRN, posted 29 Sep 2026) full methodology not publicly retrievable (HTTP 403).

## What IS reconstructed (evidenced)
From `scripts/funding_correction_replication.py`, `tests/test_funding_correction_replication.py`, `research_state/h002_replication_report.md`:

- Event identification: funding extremes on Binance USDT-margined perpetuals (5 symbols: BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT)
- Panel: Jan-Mar 2024 (cached fundingRate monthly zips)
- Results: 88 funding-extreme events total; 84 corrected, 4 censored
- Median correction time 8.0h, mean 12.6h
- Per-symbol: BTCUSDT n=22 c=20 x=2 med=8.0h; ETHUSDT n=20 c=18 x=2 med=16.0h; BNBUSDT n=14 c=14 x=0 med=16.0h; SOLUSDT n=21 c=21 x=0 med=8.0h; XRPUSDT n=11 c=11 x=0 med=16.0h
- Censoring handled explicitly (4 censored events)

## What is MISSING (cannot reconstruct without paper)
- Exact definition of "funding extreme" (threshold rule, rolling window, absolute/relative)
- Precise "correction" event definition (price move threshold, time window, which price series)
- Censoring rules (max observation window, other censoring conditions)
- RV-regime split methodology (how low/high RV defined, thresholds, lookback)
- Contract set / universe details beyond 5 symbols tested
- Exact sample construction filters

## RV-regime contrast feasibility
**IMPOSSIBLE with current data.** Mark-price cache starts 2024-04; Jan-Mar 2024 mark prices not available. Paper claims (1,696 events/18 contracts; median 27h high-RV vs 3h low-RV; lower hazard with higher RV) cannot be tested. No downloads permitted per constraints.

## Conclusion
H002 remains PARTIAL_REPLICATION. Event/censoring stats are independently reconstructed and tested. RV-regime contrast is untestable without Jan-Mar 2024 mark prices and full methodology. Do not promote to confirmatory/forecast/liquidation evidence.
