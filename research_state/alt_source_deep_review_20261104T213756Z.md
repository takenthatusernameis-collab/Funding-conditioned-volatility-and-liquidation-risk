# DEEP REVIEW OF ALTERNATIVE LIQUIDATION SOURCES
**TIMESTAMP:** 20261104T213756Z
**RUBRIC:** {"min_symbols": 5, "min_complete_month_or_blocks": ">=1 complete month with >=5 symbols OR >=3 non-overlapping 30-day blocks", "completeness_doc_required": true, "license_ok": true, "unauthenticated_only": true, "no_requester_pays": true, "schema_compatible_fclr010": true}

## Probes
### https://api.hyperliquid.xyz/info [POST]
- status: 200 ok:True
- len: 20000
- preview: [{"universe":[{"szDecimals":5,"name":"BTC","maxLeverage":40,"marginTableId":56},{"szDecimals":4,"name":"ETH","maxLeverage":25,"marginTableId":55},{"szDecimals":2,"name":"ATOM","maxLeverage":5,"marginT

### https://api.hyperliquid.xyz/info [POST]
- status: 200 ok:True
- len: 17743
- preview: {"universe":[{"szDecimals":5,"name":"BTC","maxLeverage":40,"marginTableId":56},{"szDecimals":4,"name":"ETH","maxLeverage":25,"marginTableId":55},{"szDecimals":2,"name":"ATOM","maxLeverage":5,"marginTa

### https://api.hyperliquid.xyz/info [GET]
- status: 405 ok:False
- len: 0
- preview:

### https://public.bybit.com/spot/kline/ [GET]
- status: 404 ok:False
- len: 356
- preview: <html>
<head><title>404 Not Found</title></head>
<body>
<h1>404 Not Found</h1>
<ul>
<li>Code: NoSuchKey</li>
<li>Message: The specified key does not exist.</li>
<li>Key: spot/kline/index.html</li>
<li

### https://public.bybit.com/trading/linear/ [GET]
- status: 404 ok:False
- len: 360
- preview: <html>
<head><title>404 Not Found</title></head>
<body>
<h1>404 Not Found</h1>
<ul>
<li>Code: NoSuchKey</li>
<li>Message: The specified key does not exist.</li>
<li>Key: trading/linear/index.html</li>

### https://www.okx.com/api/v5/public/instruments?instType=SWAP [GET]
- status: 200 ok:True
- len: 20000
- preview: {"code":"0","data":[{"alias":"","auctionEndTime":"","baseCcy":"","category":"1","contTdSwTime":"1611916860000","ctMult":"1","ctType":"inverse","ctVal":"100","ctValCcy":"USD","expTime":"","floatPxLmtPc

### https://www.deribit.com/api/v2/public/get_instruments?currency=BTC&kind=future [GET]
- status: 200 ok:True
- len: 11787
- preview: {"jsonrpc":"2.0","result":[{"taker_commission":3.5e-4,"block_trade_tick_size":0.01,"base_currency":"BTC","quote_currency_uuid":"dc311642-e9fb-4ba9-a312-c75c1aef4ae1","state":"open","instrument_name":"

### https://open-api.coinglass.com/public/v2/liquidation_history?symbol=BTC&timeType=4h [GET]
- status: 200 ok:True
- len: 57
- preview: {"code":"30001","msg":"API key missing.","success":false}

### https://github.com/bmoscon/cryptofeed [GET]
- status: 200 ok:True
- len: 20000
- preview:





<!DOCTYPE html>
<html
  lang="en"

  data-color-mode="auto" data-light-theme="light" data-dark-theme="dark"
  data-a11y-animated-images="system" data-a11y-link-underlines="true"
  data-css-f

### https://api.tardis.dev/v1/markets [GET]
- status: 404 ok:False
- len: 104
- preview: {
  "code": 1,
  "message": "See Tardis.dev HTTP API reference docs: https://docs.tardis.dev/api/http"
}

### https://demo-api.kaiko.io/v1/ [GET]
- status: None ok:False
- error: <urlopen error [Errno -2] Name or service not known>
- len: None
- preview:

### https://rest.coinapi.io/v1/exchanges [GET]
- status: 401 ok:False
- len: 291
- preview: {
  "error": "You did not provided API Key or it is incorrectly formatted. You should do it in: query string parameter [apikey], in http header named [X-CoinAPI-Key], [X-APIBricks-Key], [X-APIKey], in

### https://laevitas.ch/ [GET]
- status: 200 ok:True
- len: 20000
- preview: <!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Laevitas - Derivatives Data Without The S

### https://studio.glassnode.com/ [GET]
- status: 403 ok:False
- len: 5400
- preview: <!DOCTYPE html><html lang="en-US"><head><title>Just a moment...</title><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"><meta http-equiv="X-UA-Compatible" content="IE=Edge"><meta nam

### https://www.cryptodatadownload.com/data/binance/ [GET]
- status: 200 ok:True
- len: 20000
- preview: <!DOCTYPE html>
<html class="wide wow-animation" lang="en">
  <head>

<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-RW03VFD87H"></script>
<script>
  wi

### https://data.binance.vision/data/futures/um/daily/liquidationSnapshot/ [GET]
- status: 404 ok:False
- len: 333
- preview: <?xml version="1.0" encoding="UTF-8"?>
<Error><Code>NoSuchKey</Code><Message>The specified key does not exist.</Message><Key>data/futures/um/daily/liquidationSnapshot/</Key><RequestId>7KH85JCR7915GSS9

## ASSESSMENT
- All sources tested unauthenticated only.
- Most require auth or don't have liquidation census data.
- Ironflow (hyperliquid-liquidations on HF) remains the only known admissible path found so far.
- NO NEW GO sources identified in this deep review.