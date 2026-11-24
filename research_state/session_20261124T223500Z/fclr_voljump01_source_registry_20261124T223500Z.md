# FCLR-VOL-JUMP-01 Source Registry

**Experiment ID:** FCLR-VOL-JUMP-01
**Campaign:** FCLR-VOL-JUMP-01-20261124T223000Z
**Session:** session_20261124T223500Z

## Frozen input inventory (ironflow_bulk, read-only)
- Month span: 2025-05 .. 2026-10 (18 months)
- Datasets: candles_1h, funding, open_interest
- Files hashed: 54 parquet; sidecars matched: 54/54

| Dataset | Months | Total rows | Schema |
|---|---|---|---|
| candles_1h | 18 | 3643742 | timestamp, market, coin, dex, market_class, open, high, low, close, volume, trades |
| funding | 18 | 4104648 | timestamp, market, coin, dex, funding_rate, premium |
| open_interest | 18 | 3977432 | timestamp, market, coin, dex, mark_price, oracle_price, open_interest, open_interest_usd |

input_integrity.sha256_all_match = True
input_integrity.sha256_verified_bad = 0

Every `.sha256` sidecar was recomputed and asserted before any outcome was computed.
