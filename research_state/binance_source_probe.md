# Binance Source Probe (unauthenticated)

Date: 2026-10-25

## Feasible pipeline symbols
- BTCUSDT (UM perpetual), ETHUSDT likely same pattern.

## Verified archive URLs (HTTP 200)
- Funding rates (monthly): https://data.binance.vision/data/futures/um/monthly/fundingRate/BTCUSDT/BTCUSDT-fundingRate-2024-01.zip
  - SHA256: 3e0d30870672aa8f0f937881056e3cfd55913ae5c780cd50b33f2763aa0ba58e
  - Schema: calc_time (ms), funding_interval_hours, last_funding_rate
  - Sample: 1704067200000,8,0.00037409
- Mark price klines 1h (daily): https://data.binance.vision/data/futures/um/daily/markPriceKlines/BTCUSDT/1h/BTCUSDT-1h-2024-01-01.zip
  - Schema: open_time,open,high,low,close,volume,close_time,quote_volume,count,taker_buy_volume,taker_buy_quote_volume,ignore
- Index price klines 1h (daily): https://data.binance.vision/data/futures/um/daily/indexPriceKlines/BTCUSDT/1h/BTCUSDT-1h-2024-01-01.zip
  - Same kline schema.
- Premium index klines 1h (daily): https://data.binance.vision/data/futures/um/daily/premiumIndexKlines/BTCUSDT/1h/BTCUSDT-1h-2024-01-01.zip
  - Same kline schema.
- OHLCV klines 1h (daily): https://data.binance.vision/data/futures/um/daily/klines/BTCUSDT/1h/BTCUSDT-1h-2024-01-01.zip
  - SHA256: 09a24635f090c9b2ab17f4a61aa3c4d262a7ccc88e96ff0199ce66a54a8ab66b
  - Schema: open_time,open,high,low,close,volume,close_time,quote_volume,count,taker_buy_volume,taker_buy_quote_volume,ignore

## Date ranges probed
- Funding: 2024-01 (monthly archive).
- Klines/mark/index/premium: 2024-01-01 (daily archive).

## Forced liquidation availability verdict
NOT VERIFIED / NOT DIRECTLY DOWNLOADABLE. No liquidationSnapshot archive found under data/futures/um or cm (HTTP 404). Binance fapi forceOrders endpoint returns 451 restricted location in this environment. Direct historical liquidation labels remain unavailable without credentials; do not infer event-free intervals.
