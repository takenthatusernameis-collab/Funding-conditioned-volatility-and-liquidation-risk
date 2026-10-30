# Liquidation Source Campaign (FCLR-NEXT-001) — Track A/H004

Updated: 2026-10-30T13:56:38Z
Status: ACTIVE DISCOVERY (no credentials, unauthenticated only) — NO NEW SOURCE FOUND YET; CAMPAIGN REQUIRES EXECUTION
Goal: Find admissible unauthenticated liquidation data that can support >=3 non-overlapping 30-day blocks across >=5 symbols. This is the ONLY remaining path to reopen the confirmatory program (H001 currently NOT_SUPPORTED).

## PROGRAM STATUS (context — do not repeat completed work)
- FCLR-H001: NOT_SUPPORTED, SEALED_NEGATIVE (FCLR-003 powered negative; FCLR-006 unsealed-2026 negative; 2 blocks < 3 required).
- FCLR-H002: PARTIAL_REPLICATION (SSRN HTTP 403 structural blocker).
- FCLR-H003: INCONCLUSIVE both panels, no incremental skill.
- FCLR-H004/Track A: BLOCKED for frozen 2024; EXPLORATORY_ONLY for 2026 (FCLR-005 pilot, no incremental skill).
- Risk-overlay: INELIGIBLE. Do NOT re-run sealed FCLR-001/002/003/005/006 holds; do not threshold-shop; no seal violations.

## Known blockers (evidence — do not re-probe these exact endpoints as a "distinct route")
- Binance data.binance.vision: `liquidationSnapshot` daily/monthly returns HTTP 404 (confirmed). `fapi forceOrders` returns HTTP 451 in this env.
- Bybit public.bybit.com: has trade CSVs under `trading/` but no `liquidation/` directory found (404). Trades cannot serve as complete census.
- HF ochinimus/crypto-liquidation-ticks (CC BY 4.0): exists but covers 2026-07-08..2026-08-06 only (used in FCLR-005). Binance/OKX undercounted; Bybit complete. No 2024 coverage. Single ~29-day window = 0 confirmatory blocks.
- Other venues (OKX/Deribit): no obvious unauthenticated complete census found.
- Per RESEARCH_PROMPT §16: repeating dead endpoints is not a distinct route. Each probe below must be a materially different source family/method.

## Candidate sources to probe (unauthenticated) — execute in order, document each result

| # | Source | URL pattern | Type | Auth | Completeness notes | Status |
|---|--------|-------------|------|------|-------------------|--------|
| 1 | Binance vision alt paths | `https://data.binance.vision/data/futures/um/daily/liquidations/`, `.../monthly/liquidations/`, cm variants | archives | none | none | NOT_YET_PROBED — probe |
| 2 | Bybit public alt | `https://public.bybit.com/linear/liquidation/`, `https://public.bybit.com/trading/liquidation/` | archives | none | no obvious dir; trades exist | NOT_YET_PROBED — probe |
| 3 | OKX public data | `https://www.okx.com/priapi/v5/public/...`, static.okx.com CDN | varies | unknown | often gated | NOT_YET_PROBED — probe |
| 4 | Deribit | `https://historical.deribit.com/` or public data | varies | unknown | none | NOT_YET_PROBED — probe |
| 5 | CryptoDataDownload | `https://www.cryptodatadownload.com/data/binance/` | aggregator | none | spot/futures OHLCV mostly; check liquidation | NOT_YET_PROBED — probe |
| 6 | HuggingFace (more datasets) | `https://huggingface.co/datasets?search=liquidation` | datasets | none | check other liquidation datasets; ochinimus already have (2026 only) | NOT_YET_PROBED — probe |
| 7 | GitHub raw | search for liquidation CSVs/Parquet in public repos | raw files | none | need to be careful about terms | NOT_YET_PROBED — probe |
| 8 | Zenodo/OSF/arXiv | academic supplements for crypto liquidation | datasets | unknown | likely paid/gated | NOT_YET_PROBED — probe |
| 9 | Academic repos | point-in-time perpetual liquidation/mark datasets 2024+ | datasets | unknown | verify 2024 coverage | NOT_YET_PROBED — probe |

## Probe commands (run without credentials — record HTTP status + body)
```bash
# Binance alt paths
curl -sI "https://data.binance.vision/data/futures/um/daily/liquidations/" 2>&1 | head -5
curl -sI "https://data.binance.vision/data/futures/um/monthly/liquidations/" 2>&1 | head -5
curl -sI "https://data.binance.vision/data/futures/cm/daily/liquidationSnapshot/" 2>&1 | head -5

# Bybit alt paths
curl -sI "https://public.bybit.com/linear/liquidation/" 2>&1 | head -5
curl -sI "https://public.bybit.com/trading/" 2>&1 | head -5

# OKX public data
curl -sI "https://static.okx.com/cdn/okex/traderecords/" 2>&1 | head -5

# CryptoDataDownload
curl -sI "https://www.cryptodatadownload.com/data/binance/" 2>&1 | head -5

# HuggingFace dataset search (unauthenticated)
curl -s "https://huggingface.co/api/datasets?search=liquidation&limit=30" 2>&1 | head -c 2000
```

## Requirements for GO (confirmatory-feasible)
- Unauthenticated download path (no API key, no account, no signup)
- Coverage: >=5 symbols (BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT) OR subset that can form >=5-symbol panel
- Time coverage: >=90 days total forming >=3 non-overlapping 30-day blocks
- Completeness: characterize as census vs sample; if sample/undercounted, document and cannot infer zeros
- Provenance/license documented
- Fits in repo structure without paid services

## Next actions (execute, do not merely document)
1. Run probes #1-#9 above; record HTTP status and whether directory listing/content exists
2. For any 200/OK with directory listing, inspect contents and download a small sample
3. Inspect schema of any promising sample
4. If a source meets GO requirements: pre-register a new experiment ID BEFORE examining outcomes, then execute frozen protocol
5. Document every finding here; if all routes exhausted, update AGENT_HANDOFF.md with structural blocker + evidence and stop cleanly

## Decision log
- 2026-10-30T12:00:20Z: Campaign created. HF 2026 data exists but wrong window; need 2024 or another confirmatory-feasible window.
- 2026-10-30T12:03:45Z: Probe results — Binance `liquidations/` dirs 404; Bybit `linear/liquidation/`, `trading/liquidation/` 404; OKX static paths 200 but empty; CryptoDataDownload OHLCV only; HF search found ochinimus (2026 only) + DeFi/Hyperliquid (wrong venue/product).
- 2026-10-30T13:56:38Z: Campaign refreshed. All 9 candidate sources marked NOT_YET_PROBED. Next agent must execute probes #1-#9 and record results; do not mark campaign complete without >=1 documented probe outcome per source family.
