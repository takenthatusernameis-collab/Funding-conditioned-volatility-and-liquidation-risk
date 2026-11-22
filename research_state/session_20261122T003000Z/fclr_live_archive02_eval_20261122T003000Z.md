# FCLR-LIVE-ARCHIVE-02 Evaluation — 3-Block Confirmatory (stdlib)

**Campaign:** FCLR-LIVE-ARCHIVE-02  |  **Session UTC:** 2026-11-22T00:30:00Z
**Artifact:** `fclr_live_archive02_eval_20261122T003000Z.json` + `fclr_live_archive02_eval_20261122T003000Z.md`
**Decision:** NOT_SUPPORTED

## Design (frozen in prereg, outcome-blind)
- Data source: `data.binance.vision` (unauthenticated) — futures/um/daily/metrics + futures/um/monthly/fundingRate + futures/um/monthly/markPriceKlines/1h, BTCUSDT
- Data window: 2025-06-01 .. 2025-08-18; valid forecast hours: 2017
- Target: next-24-hour realized variance (sum of squared 1h mark-price log returns, t+1..t+24)
- Train: 2025-06-01..2025-06-30 | Embargo: 7 days (2025-07-01..2025-07-07)
- Test blocks: 2025-07-08..07-21 | 2025-07-22..2025-08-04 | 2025-08-05..2025-08-18
- Models: B0 persistence | B1 RV-only HAR (OLS, train-only std, Duan smear) | C2 = B1 + funding + abs funding pct + OI + taker vol ratio
- Materiality floor: >= 2% relative QLIKE reduction (C2 vs B1), frozen in advance
- Liquidation risk: PROXIED (OI + taker imbalance + mark dislocation), never observed liquidations (no liquidationSnapshot dataset)

## Block results (common rows, aligned across B0/B1/C2)
| block | n | QLIKE_B0 | QLIKE_B1 | QLIKE_C2 | diff C2-B1 | rel % |
|-----|---|----------|----------|----------|------------|-------|
| test_block_1 | 335 | 0.733313 | 0.355756 | 0.311464 | -0.044292 | -12.4501% |
| test_block_2 | 335 | 0.302552 | 0.197524 | 0.204824 | +0.007300 | +3.6957% |
| test_block_3 | 335 | 0.462726 | 0.178367 | 0.183920 | +0.005554 | +3.1136% |

## Aggregate
- Mean diff C2-B1: -0.010479
- Mean rel C2-B1: -1.8802%
- Blocks improved (C2<B1): 1/3
- Materiality floor (>=2% reduction): FAIL
- Decision: NOT_SUPPORTED

## Safeguards
- No look-ahead, no survivorship substitution, no forward fill; missing features remain missing.
- mark/index premium not downloaded -> missing, never zero-filled.
- stdlib-only (numpy/pandas/scipy not installed in runner).
