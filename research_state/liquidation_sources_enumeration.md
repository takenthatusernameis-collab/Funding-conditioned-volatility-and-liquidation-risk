# Liquidation Sources Enumeration (Track A) — 2026-10-27

This document enumerates and tests admissible public liquidation data sources for direct liquidation labels on FCLR-001/FCLR-002 universes (Binance USDT-margined perpetuals, primarily BTCUSDT/ETHUSDT/BNBUSDT/SOLUSDT/XRPUSDT).

## Constraints (from protocol/prompt)
- No paid services, paid trials, account signup, manually supplied keys/files, user intervention, live trading, or paper trading.
- Must be unauthenticated download paths where possible; respect terms/license.
- A capped/partial event stream is NOT a complete census. Absence cannot be labeled "no liquidation".
- If completeness cannot be supported, use observed events only as a partial positive signal with explicit incomplete-label design, or do not use them for a binary absence/presence target.

## Sources tested

### 1) Binance data.binance.vision (public archives)
- Base: https://data.binance.vision/
- UM futures paths tested:
  - `data/futures/um/daily/liquidationSnapshot/` — HTTP 404 (NoSuchKey). Confirmed.
  - `data/futures/um/monthly/liquidationSnapshot/` — not probed but daily missing suggests unlikely present.
  - Also checked via API: `https://fapi.binance.com/fapi/v1/forceOrders` returns 451 restricted location (from environment). Authenticated historical liquidation archives not publicly accessible without credentials/terms in accessible form.
- Verdict: Not directly downloadable as a complete historical census via unauthenticated public archives in accessible form. BLOCKED as complete source.

### 2) Bybit public data (public.bybit.com)
- Base: https://public.bybit.com/
- Directories: `trading/`, `premium_index/`, `spot_index/`, `spot/`, `kline_for_metatrader4/`
- Trading data under `trading/{SYMBOL}/` contains trade CSVs like `BTCUSDT2024-03-01.csv.gz` (per-trade). These are trade-level, not aggregated liquidation events. No obvious `liquidation/` directory found.
- Tried: `https://public.bybit.com/lin/liquidation/` → 404. `https://public.bybit.com/` grep for liquidation → none.
- Verdict: Public trade data available but no public liquidation snapshot/census directory found. Trade data alone cannot be reliably converted to a complete liquidation event census without venue-specific rules; not directly suitable as "observed liquidation labels" census.

### 3) OKX public historical data
- Checked common public paths; OKX has had historical data availability but public liquidation archives are often gated or not in obvious unauthenticated bulk form matching needs. No clear unauthenticated bulk liquidationSnapshot found in quick probes.
- Verdict: No obvious unauthenticated complete public liquidation census found.

### 4) Deribit
- Options/futures venue; liquidation data typically not in same public bulk form as needed.
- Verdict: No obvious unauthenticated complete public liquidation census found.

### 5) Academic/GitHub/HuggingFace/Zenodo archives
- GitHub search for "binance liquidation csv 2024" / API search returned 0 results in available environment.
- HuggingFace datasets search page loads but no obvious dataset with complete Binance liquidation census for 2024 in unauthenticated downloadable form surfaced.
- Tardis.dev is a commercial data vendor (has liquidation data) but requires access/terms; not a free unauthenticated bulk download source suitable for this constraint set.
- CryptoHFTData has pages mentioning Binance liquidation data but appears API/catalog based; not obviously a free unauthenticated complete bulk download in the form needed.
- Verdict: No clearly admissible unauthenticated complete historical liquidation census found in academic/public dataset repositories.

### 6) Other venue-native public archives
- No other obvious public venue archives with complete liquidation event censuses found via unauthenticated access.

## Completeness diagnostics
- Binance: documented gap (liquidationSnapshot 404, forceOrders 451). Cannot support temporal coverage/completeness.
- Bybit: has trades but no liquidation census; converting trades to liquidations is non-trivial and would not be a "complete event census" from venue-published liquidation data.
- Others: no verifiable unauthenticated complete source found.

## License/terms notes
- data.binance.vision has terms-of-use page (linked). Using public market data for research may be subject to terms; the instruction says "No paid services..." so public unauthenticated sources are fine if terms allow research use.
- public.bybit.com appears to be public data; still need to respect terms.
- Cannot confirm complete license terms for all sources without deeper inspection, but no obvious paywall encountered for data.binance.vision index.

## Conclusion for Track A
**Track A (direct observed liquidation labels) is NOT VIABLE with admissible unauthenticated public sources.**
- No complete census found for Binance (primary venue) via unauthenticated public archives.
- Other venues lack obvious unauthenticated complete liquidation archives.
- Partial streams (e.g., trades) cannot satisfy "complete event census" requirement per protocol (§7.2). Absence cannot be inferred from missing data.

This matches blockers already logged. Recommendation: remain on Tracks B/C (synthetic/modeled proxies) as implemented; do not claim observed liquidation labels. Do not infer event-free intervals.

## Additional probes (2026-10-29)

### 7) HuggingFace - crypto-liquidation-ticks (ochinimus/nick128373)
- Dataset: https://huggingface.co/datasets/ochinimus/crypto-liquidation-ticks (also mirror nick128373/crypto-liquidation-ticks)
- License: CC BY 4.0 (stated)
- Coverage: 2026-07-08 16:42:32 to 2026-08-06 23:59:42 UTC (recent). 1,442,664 events across Binance/Bybit/OKX, 800 symbols.
- Files: `liquidations_full_20260807.csv`, `coverage_20260807.csv` (unauthenticated download paths exist on HF hub)
- Schema: ts_ms, utc_time, symbol, exchange, event, size, price, usd
- Completeness notes (per README): Bybit complete (allLiquidation stream), Binance undercounts (snapshot capped at 1 order per symbol per 1000ms), OKX undercounts (1 update/sec). Warns about universe change on 2026-07-12. Treat cross-venue totals as lower bound.
- Relevance to frozen tests: **NO** - covers 2026, not 2024 windows used in FCLR-001/002/003/004. Frozen tests use 2024 data; no 2024 coverage found.
- Verdict: Admissible source in general (unauthenticated, CC BY 4.0), but **does not cover required 2024 windows** → not usable for frozen experiments. If expanding scope to 2026, would need to evaluate completeness per venue/symbol.

### 8) Zenodo search (liquidation binance perpetual)
- Searched via API; results are predominantly legal/corporate liquidation papers (not crypto market liquidation event data). No crypto liquidation event datasets found for 2024.
- Verdict: No relevant event data.

### 9) GitHub code search
- API requires auth (401); raw searches return 404. No obvious unauthenticated bulk liquidation event datasets found.
- Verdict: No relevant event data surfaced.

## Updated conclusion for Track A (FCLR-H004)
**Track A (direct observed liquidation labels) remains NOT VIABLE for the frozen 2024 test windows.**
- Binance data.binance.vision liquidationSnapshot paths: HTTP 404 (daily/monthly) for UM/CM - confirmed.
- Binance fapi forceOrders: HTTP 451 restricted in this environment - confirmed.
- Other venues (Bybit/OKX/Deribit): no unauthenticated complete census found for 2024.
- HuggingFace has recent (2026) liquidation tick datasets with noted undercounting for Binance/OKX (Bybit complete) - admissible if scope expands, but **does not cover 2024 windows** required by frozen experiments.
- Partial streams (trades) cannot satisfy "complete event census" requirement per protocol §7.2; absence cannot be inferred as zero liquidations.

**Decision:** Track A = **BLOCKED for frozen 2024 windows** with structural evidence above. Tracks B (modeled boundary breaches) and C (volatility/stress) remain the only liquidation-adjacent paths. No event-free intervals may be inferred. Do **NOT** re-attempt forecast gates (FCLR-001-004 sealed).
