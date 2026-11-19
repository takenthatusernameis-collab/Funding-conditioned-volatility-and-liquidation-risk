# Track A exploratory preregistration — Ironflow Hyperliquid observed liquidations

- campaign: `FCLR-LIQ-TRACKA-EXPLORATORY-01-20261118T201919Z`
- session: `session_20261118T201919Z`
- materialized: 2026-11-19T01:35:44Z
- authority: `AGENT_HANDOFF.md` (2026-11-19T00:27:17Z initial task message)

## Source
- dataset: `ironflow/hyperliquid-liquidations` — https://huggingface.co/datasets/ironflow/hyperliquid-liquidations
- license: CC BY 4.0; unauthenticated; no API key; no requester-pays
- HF probe 2026-11-19: last modified `2026-11-13T07:20:34Z`, 38 siblings, events and fills for 18 months `2025-05 .. 2026-10`

## Scope (frozen)
- months: `2025-11 .. 2026-04` (6 complete months fully present in the local bulk cache)
- coins (13): BTC, ETH, BNB, SOL, XRP, AVAX, DOGE, LINK, SUI, ARB, OP, APT, ADA
- venue filter: main-dex perpetuals only (`dex == ""`, `market_class == "perp"`, `market == "<COIN>-PERP"`)
- the earlier window `2025-05 .. 2025-10` is not read for outcomes; the later window
  `2026-05 .. 2026-10` is not yet cached and is explicitly out of this session

## Label definition
- label = **observed** Hyperliquid forced-liquidation event row (not a modeled breach)
- dedupe on `(tx_hash, wallet, market, timestamp)`; zero duplicates observed
- aggregation: per `(coin, hour_utc)`: `liq_count`, `liq_long_count`, `liq_short_count`,
  `liq_fills`, `liq_notional_usd`
- normalization: raw USD notional and counts; no OI/volume rescaling of the label
- absence from the feed is **not** evidence of no liquidation

## Alignment protocol
- event `timestamp` (Arrow UTC datetime, ms precision) floored to the hour
- candle grid: 1h candles for the same coins, `timestamp` floored to hour
- funding and open interest joined on `(coin, hour_utc)`
- no cross-hour forward fill for labels; timezone fixed to UTC

## Frozen admissibility gates
| gate | threshold |
|---|---|
| g1 provenance | every source parquet sha256 recorded; cc-by-4.0; unauthenticated |
| g2 instruments | >= 5 coins with >= 1 observed liquidation |
| g3 depth | >= 3 complete months |
| g4 gaps | max coin-month 1h candle gap <= 20% |
| g5 labels | observed-only; no modeled/proxy column |
| g6 alignment | >= 95% of events join to a candle hour |

## Blindness statement
- `outcome_target_inspected_before_freeze = false` — no forward volatility, forecast,
  or model outcome was inspected before this freeze.
- `coverage_census_inspected_before_freeze = true` — row counts and month coverage were
  inspected during ingest to establish admissibility, which is the purpose of this session.
- Confirmatory design `FCLR-LIQ-TRACKA-CONFIRMATORY-01` is **not** registered here; it may
  only be registered after the 2026-05..2026-10 bulk extension and a re-run of this audit.
