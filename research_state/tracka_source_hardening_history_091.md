# Track A Source Expansion/Hardening History (091)
Merged point-in-time source probe artifacts.
Generated 20261105T081200Z by consolidation.


## source_expansion_tracka_20261105T033025Z.md (26 lines, 1737 bytes)
```
# SOURCE EXPANSION + CLASSIFICATION HARDENING (STEP 4)
Timestamp (UTC): __TS__
Git SHA (HEAD): 83e151d03dc1046b9af405e8c26f2c6b94c7614b

## Caches (already hardened)
- hunt_alternative_liquidation_sources.py: HF search cache (SEARCH_CACHE_PATH, TTL 24h), URL probe cache (URL_CACHE_PATH, TTL 6h), POST cache keyed by URL+body, dedup across candidates
- monitor_ironflow_liquidations.py: ETag/tree cache, per-file caching, baseline-drift probe, consolidation
- deep_review_alt_sources.py: reuses shared URL probe cache (cache_hits observed)

## Rubric (strict, enforced)
From hunt/deep review: min_symbols>=5 OR >=1 complete month OR >=3x30d blocks; completeness_doc_required true; license_ok true; unauthenticated_only true; no_requester_pays true; schema_compatible_fclr010 true. Hyperliquid-only for Track A per experiment frontier.

## Current findings (from probes)
- Hyperliquid public API (/info) returns data but appears to be market metadata (universe/margin) not historical liquidation census parquet - needs schema compatibility check
- ironflow/hyperliquid-liquidations dataset exists on HF (metadata visible) but files/months need inspection; monitor will check
- Other venues (Bybit/OKX/Deribit/CoinAPI/Kaiko/Tardis/Coinglass) either require keys/auth, 404s, or not liquidation census data

## Classification hardening needed
- Distinguish liquidation events vs fills vs trades vs funding vs insurance fund vs ADL
- Schema mapping to FCLR-010 expected fields
- Fixture-based tests for classification edge cases
- Every probe cached (already implemented)

## Actions taken
- Reviewed existing hardening (caches/dedup/rubric). Existing implementation is already strong from 004i work.
- Will extend tests if needed in step 6.
```

## source_probe_heavy_tracka_20261103T140935Z.md (49 lines, 4061 bytes)
```
# Alternative Track A Liquidation-Label Source Probe (Heavy Work FCLR-NEXT-013)
Timestamp (UTC): 20261103T140935Z
Git SHA (HEAD): a9794e7c
Track: A (Hyperliquid observed liquidations) — no new ironflow data required; probe only
Firewall: NO Binance<->Hyperliquid merge; overlay HYPOTHETICAL_ONLY if used

## Objective
Find one admissible unauthenticated liquidation-label source NOT covered by existing source_probe files (existing: source_probe_FCLR-NEXT-002_*), document exact URL, no-auth result, schema, coverage, hash. Do not merge tracks.

## Probe (unauthenticated)
Target candidate: Hyperliquid public info endpoint for liquidation-related data? Or alternative public sources.
Checked existing probes in research_state:
- source_probe_FCLR-NEXT-002_20261102T065606Z.md exists
- Others may exist; focusing on non-duplicative probe.

Candidate explored (no-auth):
- URL: https://api.hyperliquid.xyz/info (Hyperliquid public API, unauthenticated)
- Method: POST with {"type":"meta"} or {"type":"liquidation"} style queries? Or check recent liquidations?
  Hyperliquid API: common types include "recentTrades", "l2Book", etc; liquidation events may appear in different forms. Alternatively check "userFills" patterns not directly public census. Or look for public datasets/indexers.

But more concretely, probing structure without pulling full data:
- Request: POST https://api.hyperliquid.xyz/info with body {"type":"meta"} (unauthenticated) - metadata about universe
- Also {"type":"spotMeta"}, {"type":"perpMeta"} give instrument lists
- Liquidation events: Hyperliquid doesn't have a simple public "all liquidations" unauth endpoint in the same form as some exchanges; ironflow is a known source. Another angle: check if there are public indexers (e.g., hypurrscan/hyperdash style) but those may have different access patterns. Or check public websocket data schemas? But unauthenticated REST probe required.

Alternatively probe: https://api.hyperliquid.xyz/info with {"type":"clearinghouseState", "user": "..."} requires specific user; not general census.
Another candidate: https://api.hyperliquid.xyz/info {"type":"historicalOrders"} not for all liquidations.

Conclusion for this probe: no single clean unauthenticated "all liquidation events" REST endpoint equivalent to ironflow census found via standard info calls. Documented below.

## Findings
| Item | Value |
|------|-------|
| Candidate URL(s) probed | https://api.hyperliquid.xyz/info (POST), unauthenticated |
| Probe body tested (schema) | {"type":"perpMeta"}, {"type":"meta"} (structure inspection only) |
```

## CONSOLIDATED 104 (20261105T1826Z, FCLR-NEXT-104 root-bound pre-evidence)
Consolidated unreferenced `source_probe_FCLR-NEXT-002_*` per-venue probe family (verified ref-free by exact name/stem scan vs AGENT_HANDOFF/frontier/manifest/scripts/tests). Provenance preserved as sha256+bytes+excerpt; originals deleted to regain root md+json slack.
<!-- CONSOLIDATED 104: source_probe_FCLR-NEXT-002_* family (provenance preserved) BEGIN -->
### source_probe_FCLR-NEXT-002_academic_archives.md (sha256=2d2ba771477d51385b7c40ebe96a19cc4970f919d9702965838aad463e9764a2 bytes=1800)
```
# Source Probe: FCLR-NEXT-002 — Family #5 — Academic / Institutional Archives

**Probe date:** 2026-11-02T01:00:00Z
**Source family:** Zenodo, OSF, arXiv supplements (dataset files, unauthenticated GET)
**Campaign:** FCLR-NEXT-002
**Rubric:** unauthenticated==true AND no_keys==true AND symbols>=5 AND blocks>=3 (non-overlapping 30-day blocks) AND completeness_doc==true AND license_ok==true AND census_or_defensible==true

## Endpoints tested

| Endpoint | HTTP status | Result |
|---|---|---|
| https://zenodo.org/api/ | 404 | API path not found at root |
| https://osf.io/api/v1/ | 404 | API path not found |
| https://arxiv.org/api/ | 302 | Redirect (not a direct dataset API) |

## Fields
N/A — no dataset files found.

## Coverage
- Symbols: 0 (no crypto perpetual liquidation datasets found)
- Blocks: 0 non-overlapping 30-day blocks
- Earliest/latest timestamp: N/A
- Cadence: N/A

## License / terms
Varies by dataset; no suitable dataset found to evaluate.

## Completeness
Cannot document — no matching dataset found.

## GO/NO-GO verdict
**NO-GO** — Rubric FAILS on: symbols>=5 (0), blocks>=3 (0), completeness_doc (false), census_or_defensible (false). No crypto perpetual liquidation event datasets found on Zenodo/OSF/arXiv with required coverage and license. Prior sweep (liquidation_sources_enumeration.md §84-92) confirms no match.

## Bottleneck / removal
Academic archives do not host crypto perpetual liquidation census datasets meeting the rubric. This bottleneck cannot be removed within the admissible-source constraint.

## Next materially different route
None within academic archives. Track A reopen requires a NEW admissible unauthenticated source outside academic archives (e.g., Hyperliquid ironflow via HuggingFace, already admissible and used in FCLR-010).
```

### source_probe_FCLR-NEXT-002_binance_alt_paths.md (sha256=01aad398bb10274211e3377d42e4b26d8ebffecea70417e1301e209f3eba4a97 bytes=2235)
```
# Source Probe: FCLR-NEXT-002 — Family #1 — Alternative Binance Paths

**Probe date:** 2026-11-02T01:00:00Z
**Source family:** Alternative Binance public data archive paths (data.binance.vision)
**Campaign:** FCLR-NEXT-002
**Rubric:** unauthenticated==true AND no_keys==true AND symbols>=5 AND blocks>=3 (non-overlapping 30-day blocks) AND completeness_doc==true AND license_ok==true AND census_or_defensible==true

## Endpoints tested

| Endpoint | HTTP status | Result |
|---|---|---|
| https://data.binance.vision/data/futures/um/daily/liquidationSnapshot/ | 404 | NoSuchKey — path does not exist |
| https://data.binance.vision/data/futures/um/daily/liquidations/ | 404 | NoSuchKey — path does not exist |
| https://data.binance.vision/data/futures/um/daily/liquidationHistory/ | 404 | NoSuchKey — path does not exist |
| https://data.binance.vision/data/futures/um/daily/forceLiquidation/ | 404 | NoSuchKey — path does not exist |
| https://data.binance.vision/data/futures/um/monthly/liquidationSnapshot/ | 404 | NoSuchKey — path does not exist |
| https://fapi.binance.com/fapi/v1/forceOrders | 451 | Geo-restricted / unavailable in this environment |

## Fields
N/A — no downloadable files found.

## Coverage
- Symbols: 0 (no files)
- Blocks: 0 non-overlapping 30-day blocks
- Earliest/latest timestamp: N/A
- Cadence: N/A

## License / terms
Unclear — required data not present, so license cannot be evaluated.

## Completeness
Cannot document — no archive exists at tested paths.

## GO/NO-GO verdict
**NO-GO** — Rubric FAILS on: symbols>=5 (0), blocks>=3 (0), completeness_doc (false), census_or_defensible (false). No Binance liquidation census archive exists at any tested unauthenticated path.

## Bottleneck / removal
Binance liquidation labels are structurally unavailable unauthenticated. This bottleneck cannot be removed within the admissible-source constraint. Prior probe (binance_source_probe.md, 2026-10-25) confirms: liquidationSnapshot 404, fapi forceOrders 451.

## Next materially different route
None within Binance. Track A reopen requires a NEW admissible unauthenticated source outside Binance (e.g., Hyperliquid ironflow via HuggingFace, already admissible and used in FCLR-010).
```

### source_probe_FCLR-NEXT-002_bybit.md (sha256=673c77efda726360551bcbfcfd4a853aa30c7e203c685e3727c6f28d5ac9d892 bytes=2116)
```
# Source Probe: FCLR-NEXT-002 — Family #2 — Bybit

**Probe date:** 2026-11-02T01:00:00Z
**Source family:** Bybit public archive (public.bybit.com)
**Campaign:** FCLR-NEXT-002
**Rubric:** unauthenticated==true AND no_keys==true AND symbols>=5 AND blocks>=3 (non-overlapping 30-day blocks) AND completeness_doc==true AND license_ok==true AND census_or_defensible==true

## Endpoints tested

| Endpoint | HTTP status | Result |
|---|---|---|
| https://public.bybit.com/ | 200 | Site accessible |
| https://public.bybit.com/linear/liquidation/ | 404 | No liquidation directory |
| https://public.bybit.com/spot/liquidation/ | 404 | No liquidation directory |
| https://public.bybit.com/archive/linear/liquidation/ | 404 | No liquidation directory |

## Fields
N/A — no liquidation data directory found.

## Coverage
- Symbols: 0 usable for liquidation census (trade CSVs exist but are not liquidation events)
- Blocks: 0 non-overlapping 30-day liquidation blocks
- Earliest/latest timestamp: N/A
- Cadence: N/A

## License / terms
Public data terms checked; no liquidation census product available in required form.

## Completeness
Cannot document — trades are not liquidation events; trade→liquidation conversion requires venue rules not published as a census.

## GO/NO-GO verdict
**NO-GO** — Rubric FAILS on: symbols>=5 (insufficient), blocks>=3 (0), completeness_doc (false — trades != census), census_or_defensible (false). Bybit public archive provides trade-level CSVs only; no unauthenticated complete liquidation event census archive surfaced.

## Bottleneck / removal
Bybit lacks a published unauthenticated liquidation census. This bottleneck cannot be removed within the admissible-source constraint. Prior sweep (track_a_deadend_map.md) confirms: no `liquidation/` directory; trades cannot be converted to a complete liquidation census without venue rules.

## Next materially different route
None within Bybit public archive. Track A reopen requires a NEW admissible unauthenticated source outside Bybit (e.g., Hyperliquid ironflow via HuggingFace, already admissible and used in FCLR-010).
```

### source_probe_FCLR-NEXT-002_cryptodatadownload.md (sha256=9472a8758460c1d75971a5a68690db32c34846b547df0a85847ddce9ec44713d bytes=1719)
```
# Source Probe: FCLR-NEXT-002 — Family #8 — CryptoDataDownload / Venue-Native Archives

**Probe date:** 2026-11-02T01:00:00Z
**Source family:** CryptoDataDownload and other venue-native archives (all products, unauthenticated downloads)
**Campaign:** FCLR-NEXT-002
**Rubric:** unauthenticated==true AND no_keys==true AND symbols>=5 AND blocks>=3 (non-overlapping 30-day blocks) AND completeness_doc==true AND license_ok==true AND census_or_defensible==true

## Endpoints tested

| Endpoint | HTTP status | Result |
|---|---|---|
| https://www.cryptodatadownload.com/ | 200 | Site accessible |
| (scanned 170 links on homepage) | — | 0 liquidation links, 0 futures/perpetual links |

## Fields
N/A — no liquidation product found.

## Coverage
- Symbols: 0 (no liquidation product)
- Blocks: 0 non-overlapping 30-day blocks
- Earliest/latest timestamp: N/A
- Cadence: N/A

## License / terms
Unclear — no liquidation product available to evaluate.

## Completeness
Cannot document — no liquidation-label product found.

## GO/NO-GO verdict
**NO-GO** — Rubric FAILS on: symbols>=5 (0), blocks>=3 (0), completeness_doc (false), census_or_defensible (false). CryptoDataDownload homepage has no liquidation links and no futures/perpetual product links. No unauthenticated bulk liquidation census available.

## Bottleneck / removal
CryptoDataDownload does not offer liquidation-event data. This bottleneck cannot be removed within the admissible-source constraint.

## Next materially different route
None within CryptoDataDownload. Track A reopen requires a NEW admissible unauthenticated source outside CryptoDataDownload (e.g., Hyperliquid ironflow via HuggingFace, already admissible and used in FCLR-010).
```

### source_probe_FCLR-NEXT-002_deribit.md (sha256=4717162b526f046da91292435e09edba5295961267e9fab4249d090bc097ca78 bytes=1454)
```
# Source Probe: FCLR-NEXT-002 — Family #4 — Deribit

**Probe date:** 2026-11-02T01:00:00Z
**Source family:** Deribit historical data (historical.deribit.com)
**Campaign:** FCLR-NEXT-002
**Rubric:** unauthenticated==true AND no_keys==true AND symbols>=5 AND blocks>=3 (non-overlapping 30-day blocks) AND completeness_doc==true AND license_ok==true AND census_or_defensible==true

## Endpoints tested

| Endpoint | HTTP status | Result |
|---|---|---|
| https://historical.deribit.com/ | 000 | Connection failed (no response) |

## Fields
N/A — endpoint unreachable.

## Coverage
- Symbols: 0
- Blocks: 0 non-overlapping 30-day blocks
- Earliest/latest timestamp: N/A
- Cadence: N/A

## License / terms
Unclear — endpoint unreachable, cannot evaluate.

## Completeness
Cannot document — endpoint unreachable.

## GO/NO-GO verdict
**NO-GO** — Rubric FAILS: endpoint unreachable (connection error), symbols>=5 (0), blocks>=3 (0), completeness_doc (false), census_or_defensible (false). No admissible unauthenticated Deribit perp liquidation history accessible.

## Bottleneck / removal
Deribit historical endpoint unreachable in this environment. This bottleneck cannot be removed within the admissible-source constraint.

## Next materially different route
None within Deribit. Track A reopen requires a NEW admissible unauthenticated source outside Deribit (e.g., Hyperliquid ironflow via HuggingFace, already admissible and used in FCLR-010).
```

### source_probe_FCLR-NEXT-002_github_raw.md (sha256=56d1db45d74f0a58cd544b5e0d9160f7434228ba070c4e82bb08afd887d96013 bytes=2578)
```
# Source Probe: FCLR-NEXT-002 — Family #6 — GitHub Raw

**Probe date:** 2026-11-02T01:00:00Z
**Source family:** Public GitHub repos containing CSV/Parquet liquidation or perp mark-price data (raw content, unauthenticated)
**Campaign:** FCLR-NEXT-002
**Rubric:** unauthenticated==true AND no_keys==true AND symbols>=5 AND blocks>=3 (non-overlapping 30-day blocks) AND completeness_doc==true AND license_ok==true AND census_or_defensible==true

## Endpoints tested

| Endpoint | HTTP status | Result |
|---|---|---|
| https://api.github.com/search/repositories?q=crypto+liquidation+data&per_page=10 | 200 (rate-limited search) | Repos found but code search requires auth (401) |
| https://raw.githubusercontent.com/ | 301 | Redirect (raw content accessible) |

## Repos surfaced (not liquidation census datasets)

| Repo | Stars | Description | Assessment |
|---|---|---|---|
| SpiralDevelopment/crypto-hft-data | 78 | WebSocket HFT data collector | Real-time collector, not historical census |
| ruleaker/awesome-derivatives-data | 3 | Curated list of crypto derivatives data resources | Index/link list, not a dataset |
| Co-Messi/HyperData-Terminal | 26 | Trading terminal for multiple venues | Tool, not a dataset |
| DevAkhil/Crypto-Liquidation-API | 2 | .NET Core API via Selenium | Requires scraping, not a census archive |
| afelder11/crypto-liquidation-datastream | 0 | Live liquidation datastream | Live stream, not historical census |

## Fields
N/A — no raw CSV/Parquet liquidation census files found.

## Coverage
- Symbols: 0 (no census dataset with ≥5 symbols)
- Blocks: 0 non-overlapping 30-day blocks
- Earliest/latest timestamp: N/A
- Cadence: N/A

## License / terms
Varies by repo; no suitable dataset found to evaluate.

## Completeness
Cannot document — no curated liquidation label set found.

## GO/NO-GO verdict
**NO-GO** — Rubric FAILS on: symbols>=5 (0), blocks>=3 (0), completeness_doc (false), census_or_defensible (false). GitHub code search requires authentication (401); raw content is accessible but no public repo with ≥5 symbols, ≥3 non-overlapping 30-day blocks, documented completeness liquidation census surfaced.

## Bottleneck / removal
GitHub lacks a curated unauthenticated liquidation census dataset meeting the rubric. This bottleneck cannot be removed within the admissible-source constraint.

## Next materially different route
None within GitHub raw. Track A reopen requires a NEW admissible unauthenticated source outside GitHub (e.g., Hyperliquid ironflow via HuggingFace, already admissible and used in FCLR-010).
```

### source_probe_FCLR-NEXT-002_huggingface.md (sha256=16d584d7625e574e74303f8e76e5b86fb30fbe5aaa9e80cd05282617883abf34 bytes=4828)
```
# Source Probe: FCLR-NEXT-002 — Family #7 — Hugging Face Datasets

**Probe date:** 2026-11-02T01:00:00Z
**Source family:** Hugging Face unauthenticated API search + download for liquidation/perp datasets
**Campaign:** FCLR-NEXT-002
**Rubric:** unauthenticated==true AND no_keys==true AND symbols>=5 AND blocks>=3 (non-overlapping 30-day blocks) AND completeness_doc==true AND license_ok==true AND census_or_defensible==true

## Endpoints tested

| Endpoint | HTTP status | Result |
|---|---|---|
| https://huggingface.co/api/datasets?search=liquidation&limit=30 | 200 | 11 datasets surfaced |
| https://huggingface.co/api/datasets?search=funding%20rate&limit=20 | 200 | No funding-rate datasets surfaced |
| https://huggingface.co/api/datasets?search=perpetual&limit=20 | 200 | linxy/USDT-M_Perpetual_Futures (price data, not liquidation labels) |

## Datasets evaluated

| Dataset | License | Size | Format | Coverage | Assessment |
|---|---|---|---|---|---|
| ironflow/hyperliquid-liquidations | CC BY 4.0 | 10M<n<100M | parquet | 2025-11-01..2026-10-31, 185-199 symbols, 12 monthly blocks | **ALREADY ADMISSIBLE** — passes ALL rubric items. Census of every Hyperliquid perpetual liquidation. Used in FCLR-010 (gate PASSED). Not a NEW source for FCLR-NEXT-002; already the Track A reopen path. |
| ochinimus/crypto-liquidation-ticks | CC BY 4.0 | 1M<n<10M | csv | 2026-07-08..2026-08-06 (~1 block), 800 symbols | NO-GO — single ~30-day window, 0 non-overlapping 30-day blocks, exhausted by FCLR-005. Does not cover 2024 frozen windows. |
| nick128373/crypto-liquidation-ticks | CC BY 4.0 | 1M<n<10M | csv | Similar to ochinimus | NO-GO — same limitations as ochinimus. |
| Chainticks/defi-liquidations | CC BY 4.0 | 1K<n<10K | parquet | DeFi lending (Aave, Compound) | NO-GO — DeFi lending liquidations, NOT perpetual futures liquidations. Wrong outcome type. |
| carrierone/verilex-defi-liquidations | MIT | — | — | DeFi lending (Aave, Compound, x402) | NO-GO — DeFi lending liquidations, not perp futures. |
| PhysiAI/Bitcoin-Liquidation-Heatmapping | Apache 2.0 | — | — | Bitcoin-only | NO-GO — 1 symbol only (<5), empty data files (.gitattributes + 28-byte README only). |
| PhysiAI/Bitcoin-Liquidation-Heatmapping-1h | Apache 2.0 | — | — | Bitcoin-only | NO-GO — 1 symbol only (<5). |
| craftify2221/hyperliquid-builder-liquidation-panel | ODC-BY | 1M<n<10M | parquet/csv | Hyperliquid builder liquidations | NO-GO — builder-specific subset, overlaps with ironflow (same venue), not a complete census distinct from ironflow. |
| linxy/USDT-M_Perpetual_Futures | MIT | 10M<n<100M | — | Binance USDT-M perp price data | NO-GO for Track A — price/klines data, NOT liquidation labels. Useful for Track C only (already available via data.binance.vision). |
| pCwOrM/werracle-oev-liquidation-dataset-2026 | CC BY 4.0 | 1K<n<10K | csv | DeFi MEV (Morpho Blue, Aave v3) | NO-GO — DeFi MEV liquidations, not perp futures. |
| Gopher-Lab/bankless_Hasu__Hart... | — | n<1K | parquet | DeFi liquidations analysis | NO-GO — DeFi, not perp futures; n<1K symbols coverage insufficient. |
| french-open-data/caracteristiques-des-retraites-* | — | — | — | French retirement data | NO-GO — unrelated domain. |

## Coverage (best admissible candidate: ironflow/hyperliquid-liquidations)
- Symbols: 185 native perpetual markets (199 total incl. HIP-3 builder markets) — PASS (>=5)
- Blocks: 12 monthly blocks (2025-11..2026-10) — PASS (>=3 non-overlapping 30-day blocks)
- Completeness doc: TRUE — dataset card states "Every liquidation on Hyperliquid perpetuals from 1 November 2025 to 30 October 2026: 2,167,823 liquidated positions across 460 markets and 422,181 wallets, $29.9 billion in liquidated notional"
- License OK: TRUE — CC BY 4.0
- Census/defensible: TRUE — each row is a fill Hyperliquid marked as a liquidation
- Unauthenticated: TRUE — HuggingFace resolve/main download, no keys
- no_keys: TRUE

## GO/NO-GO verdict
**ironflow/hyperliquid-liquidations: GO** — passes ALL rubric items. ALREADY USED in FCLR-010 (gate PASSED).
**All other HF datasets: NO-GO** — none meet ALL rubric items. No NEW admissible liquidation source beyond ironflow found on Hugging Face.

## Bottleneck / removal
The only admissible unauthenticated liquidation census on Hugging Face is ironflow/hyperliquid-liquidations, already exploited via FCLR-010. No additional distinct source family found. This bottleneck (no second independent liquidation census) cannot be removed within current admissible sources.

## Next materially different route
Track A is already open via ironflow (FCLR-010 COMPLETE, gate PASSED, overlay EXECUTED). No further source discovery needed for Track A reopen. FCLR-NEXT-002 confirms no additional independent liquidation census exists beyond ironflow.
```

### source_probe_FCLR-NEXT-002_okx.md (sha256=e3b80535bc62855651f153cbfb5aa2375671b53e303a8cfdd0b8bbfbae8cd7c5 bytes=1653)
```
# Source Probe: FCLR-NEXT-002 — Family #3 — OKX

**Probe date:** 2026-11-02T01:00:00Z
**Source family:** OKX public data endpoints and static.okx.com CDN
**Campaign:** FCLR-NEXT-002
**Rubric:** unauthenticated==true AND no_keys==true AND symbols>=5 AND blocks>=3 (non-overlapping 30-day blocks) AND completeness_doc==true AND license_ok==true AND census_or_defensible==true

## Endpoints tested

| Endpoint | HTTP status | Result |
|---|---|---|
| https://www.okx.com/ | 200 | Site accessible |
| https://static.okx.com/ | 403 | CDN access denied |
| https://www.okx.com/api/v5/public/data | 404 | No public bulk data endpoint |

## Fields
N/A — no downloadable liquidation data found.

## Coverage
- Symbols: 0 (no liquidation files)
- Blocks: 0 non-overlapping 30-day blocks
- Earliest/latest timestamp: N/A
- Cadence: N/A

## License / terms
Unclear — no liquidation product available to evaluate.

## Completeness
Cannot document — no historical liquidation census found.

## GO/NO-GO verdict
**NO-GO** — Rubric FAILS on: symbols>=5 (0), blocks>=3 (0), completeness_doc (false), census_or_defensible (false). OKX has no obvious public bulk liquidation history comparable to Binance's data.binance.vision; API requires auth for many endpoints; static CDN returns 403.

## Bottleneck / removal
OKX lacks an unauthenticated bulk liquidation census. This bottleneck cannot be removed within the admissible-source constraint.

## Next materially different route
None within OKX. Track A reopen requires a NEW admissible unauthenticated source outside OKX (e.g., Hyperliquid ironflow via HuggingFace, already admissible and used in FCLR-010).
```
<!-- CONSOLIDATED 104: source_probe_FCLR-NEXT-002_* family (provenance preserved) END -->
