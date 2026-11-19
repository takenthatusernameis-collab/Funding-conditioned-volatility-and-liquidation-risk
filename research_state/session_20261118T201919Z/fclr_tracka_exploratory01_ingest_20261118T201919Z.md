# Track A exploratory ingest manifest

- campaign: `FCLR-LIQ-TRACKA-EXPLORATORY-01-20261118T201919Z`
- session: `session_20261118T201919Z`
- generated_utc: 2026-11-19T01:27:30Z
- source: https://huggingface.co/datasets/ironflow/hyperliquid-liquidations (cc-by-4.0, unauthenticated)
- window: 2025-11 .. 2026-04 (6 complete months)
- venue filter: main-dex perps only (`dex == ''`, `market_class == 'perp'`)
- coins: BTC, ETH, BNB, SOL, XRP, AVAX, DOGE, LINK, SUI, ARB, OP, APT, ADA

| month | events(all) | events(13c) | liq_notional_13c | candle_hours | dup_rows |
|---|---|---|---|---|---|
| 2025-11 | 214559 | 143987 | 3615604649 | 720 | 0 |
| 2025-12 | 108154 | 69562 | 1750530754 | 744 | 0 |
| 2026-01 | 154506 | 85666 | 3365475186 | 744 | 0 |
| 2026-02 | 173549 | 121342 | 1984200289 | 672 | 0 |
| 2026-03 | 145298 | 69004 | 1325199042 | 744 | 0 |
| 2026-04 | 108755 | 48268 | 980408379 | 720 | 0 |

Totals: 537829 13-coin liquidation rows, 56472 coin-hours of 1h candles.

Provenance: every source parquet sha256 is recorded in the JSON twin. No cached input was modified; no CSV twin of raw events is written because raw parquet remains the canonical provenance object.
