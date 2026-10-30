# Liquidation Source Campaign (FCLR-NEXT-001) — Track A/H004

Updated: 2026-10-30T12:00:20Z
Status: ACTIVE DISCOVERY (no credentials, unauthenticated only)
Goal: Find admissible unauthenticated liquidation data that can support >=3 non-overlapping 30-day blocks across >=5 symbols.

## Known blockers (evidence)
- Binance data.binance.vision: `liquidationSnapshot` daily/monthly returns HTTP 404 (confirmed). `fapi forceOrders` returns HTTP 451 in this env.
- Bybit public.bybit.com: has trade CSVs under `trading/` but no `liquidation/` directory found (404). Trades cannot serve as complete census.
- HF ochinimus/crypto-liquidation-ticks (CC BY 4.0): exists but covers 2026-07-08..2026-08-06 only (used in FCLR-005). Binance/OKX undercounted; Bybit complete. No 2024 coverage.
- Other venues (OKX/Deribit): no obvious unauthenticated complete census found.

## Candidate sources to probe (unauthenticated)

| Source | URL pattern | Type | Coverage guess | Auth | Completeness notes | Status |
|--------|-------------|------|----------------|------|-------------------|--------|
| Binance vision (alt paths) | `https://data.binance.vision/data/futures/um/daily/liquidations/`, `.../monthly/`, cm variants | archives | unknown | none | tried liquidationSnapshot; try other names | UNKNOWN - probe |
| Bybit public | `https://public.bybit.com/linear/liquidation/`, `https://public.bybit.com/trading/liquidation/` | archives | unknown | none | no obvious dir; trades exist | UNKNOWN - probe |
| OKX public | `https://www.okx.com/priapi/v5/public/instruments` etc not bulk; check `https://www.okx.com/docs-v5/` data links or public downloads | varies | unknown | none | often gated | UNKNOWN - probe |
| Deribit | `https://historical.deribit.com/` or public data | varies | unknown | none | less common for perps liquidation census | UNKNOWN - probe |
| CryptoDataDownload | `https://www.cryptodatadownload.com/` | aggregator | spot/futures OHLCV mostly | none | check for liquidation | UNKNOWN - probe |
| CoinAPI/other aggregators | public endpoints vary | API | may need key | often key | avoid paid/keyed | SKIP if auth required |
| HuggingFace (more datasets) | `https://huggingface.co/datasets` search terms | datasets | varies | none for public | check other liquidation datasets | UNKNOWN - probe |
| Kaggle | requires account/download | datasets | varies | auth/account | violates "no account/signup" constraint | SKIP |
| GitHub raw | search for liquidation CSVs in public repos | raw files | varies | none | need to be careful about terms | UNKNOWN - probe |
| Tardis | commercial | vendor | good coverage | paid | violates constraints | SKIP |

## Probe commands (run without credentials)
```bash
# Binance alt paths
curl -sI "https://data.binance.vision/data/futures/um/daily/liquidations/" 2>&1 | head -5
curl -sI "https://data.binance.vision/data/futures/um/monthly/liquidations/" 2>&1 | head -5
curl -sI "https://data.binance.vision/data/futures/cm/daily/liquidationSnapshot/" 2>&1 | head -5

# Bybit alt paths
curl -sI "https://public.bybit.com/linear/liquidation/" 2>&1 | head -5
curl -sI "https://public.bybit.com/trading/" 2>&1 | head -5
curl -sI "https://public.bybit.com/derivatives/linear/liquidation/" 2>&1 | head -5

# OKX public data
curl -sI "https://static.okx.com/cdn/okex/traderecords/" 2>&1 | head -5

# CryptoDataDownload
curl -sI "https://www.cryptodatadownload.com/data/binance/" 2>&1 | head -5
```

## Requirements for GO
- Unauthenticated download path (no API key, no account)
- Coverage: >=5 symbols (BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT) OR subset that can form >=5-symbol panel
- Time coverage: >=90 days total forming >=3 non-overlapping 30-day blocks (confirmatory-feasible) OR we need to pre-register with justification
- Completeness: can characterize as census vs sample; if sample/undercounted, must document and cannot infer zeros
- Provenance/license documented
- Fits in repo structure without paid services

## Next actions
1. Run probes above
2. For any 200/OK with directory listing, inspect contents
3. If promising, download small sample, inspect schema
4. Pre-register before expanding to full window if viable
5. Document everything in this file

## Decision log
- 2026-10-30T12:00:20Z: Campaign created. HF 2026 data exists but wrong window; need 2024 or another window.

## Probe results (2026-10-30T12:03:45Z)
- Binance `liquidations/` dirs: 404 (both daily/monthly). CM liquidationSnapshot also 404.
- Bybit `linear/liquidation/`, `trading/liquidation/`: 404. Trades exist under `trading/` but not liquidation census.
- OKX static paths: 200 but empty (0 bytes) - not useful.
- CryptoDataDownload: accessible but primarily OHLCV; no obvious liquidation section.
- HF search: found `ochinimus/crypto-liquidation-ticks` (2026 only, already have), `PhysiAI/Bitcoin-Liquidation-Heatmapping` (minimal), `Chainticks/defi-liquidations` (DeFi on-chain), `craftify2221/hyperliquid-builder-liquidation-panel` (Hyperliquid specific). None cover Binance perps 2024 with census quality.

## Assessment
**No viable unauthenticated source for 2024 Binance perp liquidation census found.** HF 2026 data is usable for pilot (done as FCLR-005) but not confirmatory-feasible alone and wrong window. DeFi/Hyperliquid different venues/products.

## Recommendation
Track A remains BLOCKED for frozen 2024 windows. Focus on: (1) H002 dossier (document partial replication fully), (2) H003 feasibility, (3) see if any other HF/academic source has 2024 perp liquidation data. Also check if there might be other naming in data.binance.vision or alternative mirrors.
