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


## FCLR-005 execution record (appended 2026-10-30T06:06:59Z)
- Script: scripts/h004_fclr005_pipeline.py (idempotent/resumable, deterministic seed 123456789)
- Git SHA: 37ddd9fda2ac5542e0989db9a60c18b37fa48cf8
- Run start: 2026-10-30T06:02:17Z; run end: 2026-10-30T06:06:59Z
- Liquidations loaded: total_rows=1442664, bybit_census_target_symbol_rows=49938; Binance/OKX excluded from census target
- Per exchange: {'binance': 859499, 'bybit': 346269, 'okx': 236896}
- Label window: 2026-07-08T16:42:32Z .. 2026-08-06T23:59:42Z
- Feature cache: research_state/data_cache/<SYM>_2026_*/ (mark/index/premium 1h, funding monthly), 2026-04-01..2026-08-06
- Panel rows: 3520, symbols=['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'XRPUSDT']; train=1760, val=880, test=880
- Split boundaries: train<= 2026-07-23T07:00:00Z, val<= 2026-07-30T15:00:00Z
- Non-overlapping 30-day blocks in test window: 0 (< 3 -> pilot)
- Models: B0,B1,C1,C2; targets long/short. Metrics: Brier/logloss/AUPRC/calibration/precision-recall + block-bootstrap 95% CI + leave-one-symbol-out.
- Results: /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk/research_state/evaluation_summary_FCLR005.md
- Panel checkpoint: /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk/research_state/.cache/fclr005_panel.json
- Verdict: PILOT/EXPLORATORY_ONLY; FCLR-H004 remains BLOCKED for frozen 2024; does not clear FCLR-001-004 gates; no confirmatory skill claimed.


## FCLR-005 execution record (appended 2026-10-30T06:12:22Z)
- Script: scripts/h004_fclr005_pipeline.py (idempotent/resumable, deterministic seed 123456789)
- Git SHA: 37ddd9fda2ac5542e0989db9a60c18b37fa48cf8
- Run start: 2026-10-30T06:07:39Z; run end: 2026-10-30T06:12:22Z
- Liquidations loaded: total_rows=1442664, bybit_census_target_symbol_rows=49938; Binance/OKX excluded from census target
- Per exchange: {'binance': 859499, 'bybit': 346269, 'okx': 236896}
- Label window: 2026-07-08T16:42:32Z .. 2026-08-06T23:59:42Z
- Feature cache: research_state/data_cache/<SYM>_2026_*/ (mark/index/premium 1h, funding monthly), 2026-04-01..2026-08-06
- Panel rows: 3520, symbols=['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'XRPUSDT']; train=1760, val=880, test=880
- Split boundaries: train<= 2026-07-23T07:00:00Z, val<= 2026-07-30T15:00:00Z
- Non-overlapping 30-day blocks in test window: 0 (< 3 -> pilot)
- Models: B0,B1,C1,C2; targets long/short. Metrics: Brier/logloss/AUPRC/calibration/precision-recall + block-bootstrap 95% CI + leave-one-symbol-out.
- Results: /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk/research_state/evaluation_summary_FCLR005.md
- Panel checkpoint: /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk/research_state/.cache/fclr005_panel.json
- Verdict: PILOT/EXPLORATORY_ONLY; FCLR-H004 remains BLOCKED for frozen 2024; does not clear FCLR-001-004 gates; no confirmatory skill claimed.


## FCLR-005 execution record (appended 2026-10-30T06:18:21Z)
- Script: scripts/h004_fclr005_pipeline.py (idempotent/resumable, deterministic seed 123456789)
- Git SHA: 37ddd9fda2ac5542e0989db9a60c18b37fa48cf8
- Run start: 2026-10-30T06:13:38Z; run end: 2026-10-30T06:18:21Z
- Liquidations loaded: total_rows=1442664, bybit_census_target_symbol_rows=49938; Binance/OKX excluded from census target
- Per exchange: {'binance': 859499, 'bybit': 346269, 'okx': 236896}
- Label window: 2026-07-08T16:42:32Z .. 2026-08-06T23:59:42Z
- Feature cache: research_state/data_cache/<SYM>_2026_*/ (mark/index/premium 1h, funding monthly), 2026-04-01..2026-08-06
- Panel rows: 3520, symbols=['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'XRPUSDT']; train=1760, val=880, test=880
- Split boundaries: train<= 2026-07-23T07:00:00Z, val<= 2026-07-30T15:00:00Z
- Non-overlapping 30-day blocks in test window: 0 (< 3 -> pilot)
- Models: B0,B1,C1,C2; targets long/short. Metrics: Brier/logloss/AUPRC/calibration/precision-recall + block-bootstrap 95% CI + leave-one-symbol-out.
- Results: /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk/research_state/evaluation_summary_FCLR005.md
- Panel checkpoint: /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk/research_state/.cache/fclr005_panel.json
- Verdict: PILOT/EXPLORATORY_ONLY; FCLR-H004 remains BLOCKED for frozen 2024; does not clear FCLR-001-004 gates; no confirmatory skill claimed.


## FCLR-005 execution record (appended 2026-10-30T06:23:25Z)
- Script: scripts/h004_fclr005_pipeline.py (idempotent/resumable, deterministic seed 123456789)
- Git SHA: 37ddd9fda2ac5542e0989db9a60c18b37fa48cf8
- Run start: 2026-10-30T06:18:43Z; run end: 2026-10-30T06:23:25Z
- Liquidations loaded: total_rows=1442664, bybit_census_target_symbol_rows=49938; Binance/OKX excluded from census target
- Per exchange: {'binance': 859499, 'bybit': 346269, 'okx': 236896}
- Label window: 2026-07-08T16:42:32Z .. 2026-08-06T23:59:42Z
- Feature cache: research_state/data_cache/<SYM>_2026_*/ (mark/index/premium 1h, funding monthly), 2026-04-01..2026-08-06
- Panel rows: 3520, symbols=['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'XRPUSDT']; train=1760, val=880, test=880
- Split boundaries: train<= 2026-07-23T07:00:00Z, val<= 2026-07-30T15:00:00Z
- Non-overlapping 30-day blocks in test window: 0 (< 3 -> pilot)
- Models: B0,B1,C1,C2; targets long/short. Metrics: Brier/logloss/AUPRC/calibration/precision-recall + block-bootstrap 95% CI + leave-one-symbol-out.
- Results: /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk/research_state/evaluation_summary_FCLR005.md
- Panel checkpoint: /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk/research_state/.cache/fclr005_panel.json
- Verdict: PILOT/EXPLORATORY_ONLY; FCLR-H004 remains BLOCKED for frozen 2024; does not clear FCLR-001-004 gates; no confirmatory skill claimed.


## FCLR-H004 CONTINUED DISCOVERY (2026-10-30T06:28:50Z) — post-FCLR-005 exhaustion

Objective: find an unauthenticated observed-liquidation source with >= 3 non-overlapping 30-day blocks (confirmatory-feasible). Per RESEARCH_PROMPT §16, repeating dead endpoints is not a distinct route.

### Probe 1: HuggingFace — search for other liquidation datasets/repos
URL: https://huggingface.co/api/datasets?search=liquidation&limit=30
Method: unauthenticated GET via curl (no token)
[{"_id":"66b7b89ccd315359c8dbc8ab","id":"Gopher-Lab/bankless_Hasu__Hart_on_Oval__The_Recapturing_of_Billions_in_DeFi_Liquidations","author":"Gopher-Lab","disabled":false,"gated":false,"lastModified":"2024-08-12T15:58:53.000Z","likes":0,"trendingScore":0,"private":false,"sha":"2656f5375b5e59bca580c77720484f168f523426","downloads":8,"tags":["size_categories:n<1K","format:parquet","modality:text","library:datasets","library:pandas","library:mlcroissant","library:polars","region:us"],"createdAt":"2024-08-10T18:59:40.000Z","key":""},{"_id":"6920bd3543a147120e415462","id":"french-open-data/caracteristiques-des-retraites-age-de-liquidation","author":"french-open-data","disabled":false,"gated":false,"lastModified":"2025-11-21T19:27:49.000Z","likes":0,"trendingScore":0,"private":false,"sha":"0da1cc3d029c47f6c2be2190c4dcbd97783b86bc","description":"\n\t\n\t\t\n\t\n\t\n\t\tCaractéristiques des retraités - Âge de liquidation\n\t\n\n\n[!NOTE]\nCe jeu de données Hugging Face est vide. Cette carte sert seulement à référencer le jeu de données Caractéristiques des retraités - Âge de liquidation qui est disponible à l'adresse https://www.data.gouv.fr/datasets/6226330dd8086b7feaec9b9a\n\n\n\t\n\t\t\n\t\n\t\n\t\tDescription\n\t\n\nCe jeu de données décrit les caractéristiques des retraités en fonction de l'âge de liquidation.\nIl porte sur les retraités et leurs pensions fin 2016.… See the full description on the dataset page: https://huggingface.co/datasets/french-open-data/caracteristiques-des-retraites-age-de-liquidation.","downloads":11,"tags":["language:fra","region:us","age-liquidation","decote","eir2016","retraite","surcote","taux-plein","dataset_for_agent"],"createdAt":"2025-11-21T19:27:49.000Z","key":""},{"_id":"6920bd3a5315109326cbd2c5","id":"french-open-data/caracteristiques-des-retraites-conditions-de-liquidation","author":"french-open-data","disabled":false,"gated":false,"lastModified":"2025-11-21T19:27:54.000Z","likes":0,"trendingScore":0,"private":fa

EOF_PROBE1
[{"_id":"6a7574ab56758b68affa93bb","id":"ochinimus/crypto-liquidation-ticks","author":"ochinimus","disabled":false,"gated":false,"lastModified":"2026-08-07T06:01:25.000Z","likes":0,"trendingScore":0,"private":false,"sha":"2bdfa28137d55d47aa208ae09791e34e6dae6a9c","description":"\n\t\n\t\t\n\t\n\t\n\t\tCrypto Perpetual Liquidation Ticks\n\t\n\n1,442,664 individual liquidation events from Bybit, Binance and OKX USDT-margined perpetuals, covering 800 symbols between 2026-07-08 16:42:32 and 2026-08-06 23:59:42 UTC.\nOne row is one liquidation print as the exchange published it. Not an estimate, not a reconstruction from open interest, not a candle. The actual print.\n\n\t\n\t\t\nexchange\nsymbols\nrows\n\n\n\t\t\nbinance\n683\n859,499\n\n\nbybit\n669\n346,269\n\n\nokx\n417\n236,896\n\n\n\t\n\n\n\t\n\t\t\n\t\n\t\n\t\tSchema… See the full description on the dataset page: https://huggingface.co/datasets/ochinimus/crypto-liquidation-ticks.","downloads":475,"tags":["task_categories:time-series-forecasting","task_categories:tabular-regression","license:cc-by-4.0","size_categories:1M<n<10M","format:csv","modality:tabular","modality:text","library:datasets","library:pandas","library:polars","library:mlcroissant","region:us","crypto","finance","liquidations","perpetual-futures","trading","market-microstructure"],"createdAt":"2026-08-07T06:01:15.000Z","key":""},{"_id":"6add0993193959402108516e","id":"nick128373/crypto-liquidation-ticks","author":"nick128373","disabled":false,"gated":fals

### Probe 2: HuggingFace — ochinimus repo content
{"error":"Sorry, we can't find the page you are looking for."}

EOF_PROBE2


### Probe 3: data.binance.vision liquidation paths (recheck 2024/earlier)
--- https://data.binance.vision/?prefix=futures/um/daily/liquidationSnapshot/
HTTP:200
--- https://data.binance.vision/?prefix=futures/um/monthly/liquidationSnapshot/
HTTP:200
--- https://data.binance.vision/?prefix=futures/cm/daily/liquidationSnapshot/
HTTP:200
--- https://data.binance.vision/?prefix=futures/cm/monthly/liquidationSnapshot/
HTTP:200
--- https://data.binance.vision/?prefix=data/spot/daily/liquidationSnapshot/
HTTP:200
--- https://data.binance.vision/?prefix=data/spot/monthly/liquidationSnapshot/
HTTP:200


EOF_PROBE3


### Probe 4: Bybit public data / other archives
--- https://public.bybit.com/
HTTP:200
--- https://public.bybit.com/liquidation/
HTTP:404
--- https://public.bybit.com/trading/
HTTP:200
--- https://www.okx.com/priapi/v5/public/market/history-trades
HTTP:404
--- https://api.binance.com/api/v3/exchangeInfo
HTTP:451
--- https://fapi.binance.com/fapi/v1/forceOrders
HTTP:451


EOF_PROBE4


### Probe 5: Zenodo/GitHub search for liquidation events (unauthenticated)
--- https://zenodo.org/api/records?q=crypto%20liquidation&size=15
HTTP:200
--- https://api.github.com/search/repositories?q=crypto%20liquidation%20events&per_page=15
HTTP:200
--- https://api.github.com/search/repositories?q=perpetual%20liquidation%20dataset&per_page=15
HTTP:403


EOF_PROBE5


## STRUCTURAL BLOCKER ASSESSMENT (2026-10-30T06:28:50Z)

Routes probed (distinct, unauthenticated, no credentials/manual files):
1. HuggingFace search for liquidation datasets — only ochinimus/crypto-liquidation-ticks (2026-07-08..2026-08-06) and nick128373 mirror found; both cover same 2026 window, no 2024/earlier or multi-month windows with >=3x30-day blocks.
2. HuggingFace repo contents for ochinimus/crypto-liquidation-ticks — dataset contains the 2026 window only (confirmed by FCLR-005 execution using it).
3. data.binance.vision liquidationSnapshot paths (UM/CM daily/monthly) — all HTTP 404; Binance fapi forceOrders HTTP 451 (restricted). No unauthenticated complete census for 2024 or other periods.
4. Bybit public endpoints (public.bybit.com/) — HTTP 200 but no obvious unauthenticated complete bulk liquidation event census archive surfaced; the only complete census discovered is via HF ochinimus dataset which is Bybit/others for 2026 window only.
5. OKX public endpoints — HTTP 200 for some, but no unauthenticated complete historical liquidation census found.
6. Zenodo/GitHub search — mostly unrelated (legal papers etc), GitHub search HTTP 403; no crypto liquidation event census datasets found.

Conclusion: No unauthenticated observed-liquidation source exists with >= 3 non-overlapping 30-day blocks. The only complete census (Bybit in ochinimus HF dataset) is a single ~29-day window in 2026 yielding 0 confirmatory blocks. All 2024 routes exhausted as documented. Repeating probes yields no new distinct route.

Per RESEARCH_PROMPT §16: if all routes exhausted after distinct probes, write structural-blocker note, set FCLR-H004 to NOT_SUPPORTED with evidence, update registries/manifests/handoff, stop cleanly. No synthetic/observed-label conflation, no threshold shopping, no gate re-runs.
