# LIQMICRO Data Audit (FCLR-LIQMICRO-001)
**TIMESTAMP (UTC):** 2026-11-01T22:20:10Z
**Source (admissible):** ironflow Hyperliquid liquidation events ONLY
**Path:** /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk/research_state/data_cache/ironflow_events

**Files found:** 12

## Per-file inventory

| File | Size (MB) | Rows | Markets | Date range (UTC) | Long/Short present |
|------|-----------|------|---------|-------------------|--------------------|
| 2025-11.parquet | 7.61 | 214559 | 199 | 2025-11-01 to 2025-11-30 | yes |
| 2025-12.parquet | 4.24 | 108154 | 222 | 2025-12-01 to 2025-12-31 | yes |
| 2026-01.parquet | 5.83 | 154506 | 281 | 2026-01-01 to 2026-01-31 | yes |
| 2026-02.parquet | 6.35 | 173549 | 298 | 2026-02-01 to 2026-02-28 | yes |
| 2026-03.parquet | 5.72 | 145298 | 307 | 2026-03-01 to 2026-03-31 | yes |
| 2026-04.parquet | 4.77 | 108755 | 325 | 2026-04-01 to 2026-04-30 | yes |
| 2026-05.parquet | 5.73 | 128292 | 340 | 2026-05-01 to 2026-05-31 | yes |
| 2026-06.parquet | 9.99 | 254377 | 353 | 2026-06-01 to 2026-06-30 | yes |
| 2026-07.parquet | 8.45 | 218529 | 286 | 2026-07-01 to 2026-07-31 | yes |
| 2026-08.parquet | 8.29 | 215835 | 319 | 2026-08-01 to 2026-08-31 | yes |
| 2026-09.parquet | 7.87 | 195244 | 329 | 2026-09-01 to 2026-09-30 | yes |
| 2026-10.parquet | 9.81 | 250725 | 349 | 2026-10-01 to 2026-10-30 | yes |

## Aggregate
- **Total events:** 2,167,823
- **Unique markets:** 460
- **Date range:** 2025-11-01 to 2026-10-30 (364 unique days)
- **Native perp markets (end with -PERP, no colon):** 199
- **Long/short separation available:** True

## Funding data availability
- **Funding-related files found:** 488
  - BNBUSDT-fundingRate-2024-02.zip
  - ETHUSDT-fundingRate-2024-02.zip
  - XRPUSDT-fundingRate-2024-01.zip
  - BTCUSDT-fundingRate-2024-02.zip
  - ETHUSDT-fundingRate-2024-01.zip
  - XRPUSDT-fundingRate-2024-02.zip
  - SOLUSDT-fundingRate-2024-01.zip
  - SOLUSDT-fundingRate-2024-03.zip
  - BTCUSDT-fundingRate-2024-03.zip
  - XRPUSDT-fundingRate-2024-03.zip
  - BNBUSDT-fundingRate-2024-01.zip
  - BNBUSDT-fundingRate-2024-03.zip
  - ETHUSDT-fundingRate-2024-03.zip
  - BTCUSDT-fundingRate-2024-01.zip
  - SOLUSDT-fundingRate-2024-02.zip
  - ... and 473 more

## Coverage assessment
- **Approx hours span:** ~8736
- **Events per hour (avg):** ~248.1
  - **OK:** 2,167,823 >= 10^4 events total
  - **OK:** 460 >= 5 markets

## Notes
- Using ONLY ironflow Hyperliquid data (admissible per Track A firewall)
- No Binance data will be merged
- Data cached at `research_state/data_cache/ironflow_events/`