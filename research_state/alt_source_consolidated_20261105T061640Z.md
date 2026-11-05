# Alt sources consolidated (Track A)
Timestamp (UTC): 20261105T061640Z

## Deep review
# DEEP REVIEW OF ALTERNATIVE LIQUIDATION SOURCES
**TIMESTAMP:** 20261105T061625Z
**RUBRIC:** {"min_symbols": 5, "min_complete_month_or_blocks": ">=1 complete month with >=5 symbols OR >=3 non-overlapping 30-day blocks", "completeness_doc_required": true, "license_ok": true, "unauthenticated_only": true, "no_requester_pays": true, "schema_compatible_fclr010": true}

## Probe cache accounting
- cache_hits: 13
- cache_misses (fresh GETs): 1
- shared_cache: research_state/url_probe_cache.json (TTL 21600s)

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
- status: 405 ok:None
- error: True
- cache_hit: True
- len: None
- preview:

### https://public.bybit.com/spot/kline/ [GET]
- status: 404 ok:None
- error: True
- cache_hit: True
- len: None
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
- status: 404 ok:None
- error: True
- cache_hit: True
- len: None
- preview: <html>
<head><title>404 Not Found</title></head>
<body>
<h1>404 Not Found</h1>
<ul>
<li>Code: NoSuchKey</li>
<li>Message: The specified key does not exist.</li>
<li>Key: trading/linear/index.html</li>

### https://www.okx.com/api/v5/public/instruments?instType=SWAP [GET]
- status: 200 ok:None
- cache_hit: True
- len: None
- preview: {"code":"0","data":[{"alias":"","auctionEndTime":"","baseCcy":"","category":"1","contTdSwTime":"1611916860000","ctMult":"1","ctType":"inverse","ctVal":"100","ctValCcy":"USD","expTime":"","floatPxLmtPc

### https://www.deribit.com/api/v2/public/get_instruments?currency=BTC&kind=future [GET]
- status: 200 ok:None
- cache_hit: True
- len: None
- preview: {"jsonrpc":"2.0","result":[{"underlying_type":"crypto","is_active":true,"settlement_period":"perpetual","maker_commission":1.5e-4,"expiration_timestamp":32503708800000,"state":"open","instrument_name"

### https://open-api.coinglass.com/public/v2/liquidation_history?symbol=BTC&timeType=4h [GET]
- status: 200 ok:None
- cache_hit: True
- len: None
- preview: {"code":"30001","msg":"API key missing.","success":false}

### https://github.com/bmoscon/cryptofeed [GET]
- status: 200 ok:None
- cache_hit: True
- len: None
- preview:





<!DOCTYPE html>
<html
  lang="en"

  data-color-mode="auto" data-light-theme="light" data-dark-theme="dark"
  data-a11y-animated-images="system" data-a11y-link-underlines="true"
  data-css-f

### https://api.tardis.dev/v1/markets [GET]
- status: 404 ok:None
- error: True
- cache_hit: True
- len: None
- preview: {
  "code": 1,
  "message": "See Tardis.dev HTTP API reference docs: https://docs.tardis.dev/api/http"
}

### https://demo-api.kaiko.io/v1/ [GET]
- status: None ok:None
- error: <urlopen error [Errno -2] Name or service not known>
- len: None
- preview: <urlopen error [Errno -2] Name or service not known>

### https://rest.coinapi.io/v1/exchanges [GET]
- status: 401 ok:None
- error: True
- cache_hit: True
- len: None
- preview: {
  "error": "You did not provided API Key or it is incorrectly formatted. You should do it in: query string parameter [apikey], in http header named [X-CoinAPI-Key], [X-APIBricks-Key], [X-APIKey], in

### https://laevitas.ch/ [GET]
- status: 200 ok:None
- cache_hit: True
- len: None
- preview: <!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Laevitas - Derivatives Data Without The S

### https://studio.glassnode.com/ [GET]
- status: 403 ok:None
- error: True
- cache_hit: True
- len: None
- preview: <!DOCTYPE html><html lang="en-US"><head><title>Just a moment...</title><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"><meta http-equiv="X-UA-Compatible" content="IE=Edge"><meta nam

### https://www.cryptodatadownload.com/data/binance/ [GET]
- status: 200 ok:None
- cache_hit: True
- len: None
- preview: <!DOCTYPE html>
<html class="wide wow-animation" lang="en">
  <head>

<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-RW03VFD87H"></script>
<script>
  wi

### https://data.binance.vision/data/futures/um/daily/liquidationSnapshot/ [GET]
- status: 404 ok:None
- error: True
- cache_hit: True
- len: None
- preview: <?xml version="1.0" encoding="UTF-8"?>
<Error><Code>NoSuchKey</Code><Message>The specified key does not exist.</Message><Key>data/futures/um/daily/liquidationSnapshot/</Key><RequestId>M2C7MJ94QX6N09R3

## ASSESSMENT
- All sources tested unauthenticated only.
- Most require auth or don't have liquidation census data.
- Ironflow (hyperliquid-liquidations on HF) remains the only known admissible path found so far.
- NO NEW GO sources identified in this deep review.
- Deep-review URLs are now folded into hunt_alternative_liquidation_sources.py's candidate set so each URL is probed exactly once per session.

## Hunt scan (JSON)
```json
{
  "generated_utc": "20261105T061632Z",
  "cache_info": {
    "source": "cache",
    "generated_utc": "2026-11-04T20:47:35.774882+00:00",
    "queries": [
      "liquidation",
      "liquidations",
      "crypto liquidation",
      "perpetual liquidation",
      "hyperliquid liquidation",
      "funding liquidation",
      "crypto perpetual liquidation",
      "liquidation ticks",
      "perpetual futures liquidation"
    ],
    "stale": false
  },
  "errors": [],
  "candidates": [
    {
      "name": "coinapi_free_liquidations",
      "type": "api_docs",
      "url": "https://docs.coinapi.io/",
      "notes": "Check unauthenticated history; many require keys - treat as NO-GO unless explicit unauthenticated historical download exists with >=5 symbols and >=1 complete month.",
      "probes": [
        "https://rest.coinapi.io/v1/ohlcv/BINANCE_SPOT_BTC_USDT/latest?period_id=1DAY&limit=1"
      ]
    },
    {
      "name": "cryptofeed_docs",
      "type": "docs",
      "url": "https://github.com/bmoscon/cryptofeed",
      "notes": "Library not a dataset host; NO-GO as data source.",
      "probes": []
    },
    {
      "name": "tardis_dev_docs",
      "type": "docs",
      "url": "https://tardis.dev/",
      "notes": "Commercial/requires access in general; check unauthenticated download paths. Likely NO-GO unless explicit free historical download exists.",
      "probes": [
        "https://api.tardis.dev/v1/"
      ]
    },
    {
      "name": "kaiko_docs",
      "type": "docs",
      "url": "https://www.kaiko.com/",
      "notes": "Paid; NO-GO.",
      "probes": []
    },
    {
      "name": "glassnode_docs",
      "type": "docs",
      "url": "https://docs.glassnode.com/",
      "notes": "Paid/auth; NO-GO.",
      "probes": []
    },
    {
      "name": "coinglass_public_pages",
      "type": "web",
      "url": "https://www.coinglass.com/",
      "notes": "Check for downloadable historical liquidation data without login/payment; often requires signup/API - probe cautiously.",
      "probes": [
        "https://www.coinglass.com/"
      ]
    },
    {
      "name": "bybit_public_archive_check",
      "type": "exchange",
      "url": "https://public.bybit.com/",
      "notes": "Bybit public data archive exists but check liquidation data specifically; unauthenticated downloads possible for some datasets.",
      "probes": [
        "https://public.bybit.com/"
      ]
    },
    {
      "name": "okx_public_data",
      "type": "exchange",
      "url": "https://www.okx.com/",
      "notes": "Check public historical data; liquidation history may require specific endpoints - probe.",
      "probes": [
        "https://www.okx.com/"
      ]
    },
    {
      "name": "hf_discovered__Gopher-Lab_bankless_Hasu__Hart_on_Oval__The_Recapturing_of_Billions_in_DeFi_Liquidations",
      "urls": [
        "https://huggingface.co/api/datasets/Gopher-Lab/bankless_Hasu__Hart_on_Oval__The_Recapturing_of_Billions_in_DeFi_Liquidations",
        "https://huggingface.co/datasets/Gopher-Lab/bankless_Hasu__Hart_on_Oval__The_Recapturing_of_Billions_in_DeFi_Liquidations/resolve/main/README.md"
      ],
      "notes": "Discovered via live HF /api/datasets?search=liquidation enumeration (query='liquidation'). Description: . Verify schema/coverage/license/unauthenticated access before scoring GO."
    },
    {
      "name": "hf_discovered__ochinimus_crypto-liquidation-ticks",
      "urls": [
        "https://huggingface.co/api/datasets/ochinimus/crypto-liquidation-ticks",
        "https://huggingface.co/datasets/ochinimus/crypto-liquidation-ticks/resolve/main/README.md"
      ],
      "notes": "Discovered via live HF /api/datasets?search=crypto liquidation enumeration (query='crypto liquidation'). Description: . Verify schema/coverage/license/unauthenticated access before scoring GO."
    },
    {
      "name": "hf_discovered__craftify2221_hyperliquid-builder-liquidation-panel",
      "urls": [
        "https://huggingface.co/api/datasets/craftify2221/hyperliquid-builder-liquidation-panel",
        "https://huggingface.co/datasets/craftify2221/hyperliquid-builder-liquidation-panel/resolve/main/README.md"
      ],
      "notes": "Discovered via live HF /api/datasets?search=hyperliquid liquidation enumeration (query='hyperliquid liquidation'). Description: . Verify schema/coverage/license/unauthenticated access before scoring GO."
    }
  ],
  "deep_review_urls": [
    {
      "name": "deep_review__api.hyperliquid.xyz_info",
      "urls": [
        "https://api.hyperliquid.xyz/info"
      ],
      "notes": "Hyperliquid info endpoint (GET; POST variants probed separately by deep_review)."
    },
    {
      "name": "deep_review__tardis_dev_v1_markets",
      "urls": [
        "https://api.tardis.dev/v1/markets"
      ],
      "notes": "Tardis public markets root (auth-gated for historical data)."
    },
    {
      "name": "deep_review__binance_vision_liquidationSnapshot",
      "urls": [
        "https://data.binance.vision/data/futures/um/daily/liquidationSnapshot/"
      ],
      "notes": "Binance archive liquidation-snapshot directory probe."
    },
    {
      "name": "deep_review__kaiko_demo",
      "urls": [
        "https://demo-api.kaiko.io/v1/"
      ],
      "notes": "Kaiko demo root (auth-gated)."
    },
    {
      "name": "deep_review__cryptofeed_repo",
      "urls": [
        "https://github.com/bmoscon/cryptofeed"
      ],
      "notes": "Library repo, not a dataset host."
    },
    {
      "name": "deep_review__laevitas_ch",
      "urls": [
        "https://laevitas.ch/"
      ],
      "notes": "Public site probe."
    },
    {
      "name": "deep_review__coinglass_public_liquidation_history",
      "urls": [
        "https://open-api.coinglass.com/public/v2/liquidation_history?symbol=BTC&timeType=4h"
      ],
      "notes": "Coinglass public API probe (often auth/JS-gated)."
    },
    {
      "name": "deep_review__bybit_public_spot_kline",
      "urls": [
        "https://public.bybit.com/spot/kline/"
      ],
      "notes": "Bybit public archive spot-kline directory probe."
    },
    {
      "name": "deep_review__bybit_public_trading_linear",
      "urls": [
        "https://public.bybit.com/trading/linear/"
      ],
      "notes": "Bybit public archive trading-linear directory probe."
    },
    {
      "name": "deep_review__coinapi_exchanges",
      "urls": [
        "https://rest.coinapi.io/v1/exchanges"
      ],
      "notes": "CoinAPI root (auth-gated)."
    },
    {
      "name": "deep_review__glassnode_studio",
      "urls": [
        "https://studio.glassnode.com/"
      ],
      "notes": "Glassnode studio (auth-gated)."
    },
    {
      "name": "deep_review__cryptodatadownload_binance",
      "urls": [
        "https://www.cryptodatadownload.com/data/binance/"
      ],
      "notes": "CryptoDataDownload Binance directory probe."
    },
    {
      "name": "deep_review__deribit_get_instruments",
      "urls": [
        "https://www.deribit.com/api/v2/public/get_instruments?currency=BTC&kind=future"
      ],
      "notes": "Deribit public instruments probe."
    },
    {
      "name": "deep_review__okx_public_instruments",
      "urls": [
        "https://www.okx.com/api/v5/public/instruments?instType=SWAP"
      ],
      "notes": "OKX public instruments probe."
    }
  ]
}
```
