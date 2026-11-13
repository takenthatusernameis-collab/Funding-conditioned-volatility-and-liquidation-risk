# Alternative Observed-Liquidation Source Deep Review
**timestamp_utc:** 2026-11-13T17:12:25Z
**session_task:** TASK-20261113T162742Z (bounded alt-source discovery, RESEARCH_PROMPT §5/§16)
**inputs:** `scripts/hunt_alternative_liquidation_sources.py` (scan `generated_utc=20261113T171152Z`, source=cache, 22 candidates, HF search generated 2026-11-13T09:01:05Z), `scripts/deep_review_alt_sources.py` (deep review `20261113T171217Z`, 14 fresh probes, 0 cache hits)
**probe_cache:** `research_state/url_probe_cache.json` (68 entries)
**§16 admissibility minima (observed labels only):** unauthenticated download, provenance+license, venue-consistent perpetual liquidation events (not DeFi lending/on-chain OEV, not modeled/heatmap), ≥5 instruments, ≥1 complete month OR ≥3 non-overlapping 30-day blocks, schema compatible with Track A observed-label use.

## Probe evidence (deep review 20261113T171217Z, 14 fresh GET/POST probes)
| URL | Method | Status | Key evidence | §16 failing minima / note |
|---|---|---:|---|---|
| `https://api.hyperliquid.xyz/info` (meta/universe) | POST | 200 | live instrument metadata (BTC/ETH/ATOM..., maxLeverage etc.), no historical liquidation census | not a liquidation-label dataset; missing observed liquidation events/history/blocks |
| `https://api.hyperliquid.xyz/info` (candles/meta variant) | POST | 200 | market metadata/candle-like payload, no liquidation labels | missing liquidation events, provenance as label source N/A for Track A census |
| `https://api.hyperliquid.xyz/info` | GET | 405 | POST-only endpoint | unauth GET path unusable; no historical liquidation census |
| `https://public.bybit.com/spot/kline/` | GET | 404 | NoSuchKey | no liquidation data path; fails coverage/schema |
| `https://public.bybit.com/trading/linear/` | GET | 404 | NoSuchKey | no liquidation data path; fails coverage/schema |
| `https://www.okx.com/api/v5/public/instruments?instType=SWAP` | GET | 200 | instrument list JSON, no liquidation labels | missing liquidation events/history/blocks |
| `https://www.deribit.com/api/v2/public/get_instruments?currency=BTC&kind=future` | GET | 200 | instrument list JSON, no liquidation labels | venue/instrument scope mismatch risk + missing liquidation events |
| `https://open-api.coinglass.com/public/v2/liquidation_history?symbol=BTC&timeType=4h` | GET | 200 | `{"code":"30001","msg":"API key missing.","success":false}` | **authentication required**; fails unauthenticated |
| `https://github.com/bmoscon/cryptofeed` | GET | 200 | library repo, not a dataset host | fails provenance-as-dataset, no historical observed liquidation census |
| `https://api.tardis.dev/v1/markets` | GET | 404 | "See Tardis.dev HTTP API reference docs..." | commercial/API-service path; no unauth historical liquidation download evidenced |
| `https://demo-api.kaiko.io/v1/` | GET | DNS error | `<urlopen error [Errno -2] Name or service not known>` | endpoint unavailable; commercial provider → fails unauth/provenance/download |
| `https://rest.coinapi.io/v1/exchanges` | GET | 401 | "You did not provided API Key..." | **authentication required** |
| `https://laevitas.ch/` | GET | 200 | marketing/web UI page | no unauth machine-downloadable liquidation census; provenance/schema/coverage unverified |
| `https://studio.glassnode.com/` | GET | 403 | Cloudflare "Just a moment..." / access restriction | **access restricted/auth-like barrier**; not unauth dataset |
| `https://www.cryptodatadownload.com/data/binance/` | GET | 200 | web listing (Binance data), no liquidation census evidence | fails observed liquidation-label coverage/schema for Track A |
| `https://data.binance.vision/data/futures/um/daily/liquidationSnapshot/` | GET | 404 | `NoSuchKey` | no accessible liquidationSnapshot archive path; fails coverage/download |

## Candidate assessment (22 enumerated; per-source §16 minima)

### Static/exchange/API candidates
| Candidate | Evidence (timestamped probe/cache) | Unauth | Observed perp liq labels | ≥5 instr & ≥1 month / ≥3×30d blocks | Provenance+license | Venue-consistent | Verdict | Exact failing minima |
|---|---|---:|---:|---:|---:|---:|---|---|
| `coinapi_free_liquidations` | probe 401 API key required (`rest.coinapi.io` 401, 20261113T171217Z) | NO | NO (no dataset) | NO | NO | N/A | **NO-GO** | authentication required; no unauth historical liquidation census |
| `cryptofeed_docs` | GitHub repo HTML 200, library not dataset host | YES (repo) | NO | NO | NO (not a dataset) | N/A | **NO-GO** | not a historical observed-liquidation dataset; fails labels/coverage/provenance-as-data |
| `tardis_dev_docs` | `/v1/markets` 404 + docs pointer; commercial service | NO (usable hist download) | unverified/NO | unverified/NO | restricted | N/A | **NO-GO** | no evidenced unauth historical download meeting minima; commercial access model |
| `kaiko_docs` | demo endpoint DNS fail; paid provider | NO | NO | NO | restricted | N/A | **NO-GO** | no unauth access; paid/restricted |
| `glassnode_docs` | studio 403 challenge | NO | NO | NO | restricted | N/A | **NO-GO** | access restricted; no unauth liquidation census |
| `coinglass_public_pages` | liquidation API probe 200 with `API key missing` (cache) | NO (data API) | unverified | unverified | restricted | N/A | **NO-GO** | liquidation history requires API key; unauth census not evidenced |
| `bybit_public_archive_check` | `public.bybit.com` spot/linear paths 404 NoSuchKey | YES (site paths probed) | NO evidence | NO | N/A | N/A | **NO-GO** | no liquidation census files found at probed public paths; fails labels/coverage/schema |
| `okx_public_data` | instruments 200, no liquidation labels | YES (instruments) | NO | NO | N/A | N/A | **NO-GO** | liquidation label dataset not evidenced; fails observed labels/coverage |

### HF-discovered candidates (enumeration cache 2026-11-13T09:01:05Z; API/README probes in `url_probe_cache.json`)
| Candidate | Evidence | Unauth | Observed perp liq labels | ≥5 instr & ≥1 month / ≥3×30d blocks | Provenance+license | Venue-consistent | Verdict | Exact failing minima |
|---|---|---:|---:|---:|---:|---:|---|---|
| `hf_discovered__ironflow_hyperliquid-liquidations` | HF API/README/parquet probes 200 (cache); known in-repo admissible source family, **already exhausted/terminal** for HL designs here | YES | YES (observed HL liqs) | previously audited/used; not a *new* source | YES | YES (HL) | **NO-GO (NOT NEW)** | fails novelty: already integrated/exhausted; HL label extension trigger remains OPEN (needs ≥100d depth & verified post-2026-10-31 labels) |
| `hf_discovered__craftify2221_hyperliquid-builder-liquidation-panel` | HF API/README/liq parquet probes 200 (cache) | YES | HL-builder/panel scope (not verified as general HL perp liquidation census for Track A) | unverified vs §16 minima; overlaps HL venue | partial/unverified | HL-related but design overlap risk | **NO-GO (UNVERIFIED/OVERLAP)** | not shown to provide ≥5-instrument, ≥3×30d-block observed perp liquidation census beyond exhausted HL designs; admissibility not established pre-outcomes |
| `hf_discovered__ochinimus_crypto-liquidation-ticks` | API 200, README cc-by-4.0, `coverage_20260807.csv` shows e.g. ETHUSDT/BTCUSDT Binance rows ~2026-07-10→2026-08-06 (~27 days) | YES | ticks (exchange liq ticks) but scope/definition unverified for Track A census | **NO** (coverage ~27 days < 30d block; not ≥3 blocks / not ≥1 complete month) | license present (cc-by-4.0) | Binance ticks (venue differs from HL; mixing forbidden without design) | **NO-GO** | fails blocks/month minimum (<1 complete month, <3×30d) and instrument/block sufficiency not evidenced; requires §16 audit before use (not started) |
| `hf_discovered__nick128373_crypto-liquidation-ticks` | API 200, README cc-by-4.0 (cache) | YES | liquidation ticks claimed, unverified | **unverified** (no coverage evidence showing ≥5 instr & ≥1 month/3 blocks) | license present | likely multi-exchange/unknown; venue consistency unverified | **NO-GO** | fails evidenced coverage/instruments/blocks/provenance completeness for §16; cannot admit without audit evidence |
| `hf_discovered__PhysiAI_Bitcoin-Liquidation-Heatmapping` / `-5m` / `-1h` | API/README 200, apache-2.0, minimal docs | YES | **NO (heatmap/derived)** | **NO** (BTC-only, derived) | license present | N/A | **NO-GO** | modeled/derived heatmap, not observed liquidation events; <5 instruments; no event-level census |
| `hf_discovered__carrierone_verilex-defi-liquidations` | API/README 200 (MIT, DeFi liquidation signals/Aave/Compound etc.) | YES | **NO (DeFi lending signals)** | N/A | license present | **NO (not perp exchange venue-consistent)** | **NO-GO** | wrong domain (DeFi lending/on-chain), not observed perpetual futures liquidation census |
| `hf_discovered__Chainticks_defi-liquidations` | API/README 200 (cc-by-4.0, DeFi) | YES | **NO (DeFi)** | N/A | license present | **NO** | **NO-GO** | wrong domain (DeFi), not venue-consistent perp liquidations |
| `hf_discovered__pCwOrM_werracle-oev-liquidation-dataset-2026` | API/README 200 (cc-by-4.0, OEV liquidation dataset) | YES | **NO (OEV/on-chain liquidation context)** | unverified/likely NO | license present | **NO** | **NO-GO** | not observed perpetual-futures exchange liquidation census; venue/domain mismatch |
| `hf_discovered__tanod_base-lending-liquidations` | README 200 (cc-by-4.0, Base lending liquidation census) | YES | **NO (DeFi lending)** | N/A | license present | **NO** | **NO-GO** | DeFi lending liquidations, not perp futures; venue inconsistent |
| `hf_discovered__Gopher-Lab_bankless_Hasu__Hart_on_Oval__The_Recapturing_of_Billions_in_DeFi_Liquidations` | README shows transcript features (speaker/text) | YES | **NO** | NO | N/A | NO | **NO-GO** | text/transcript dataset, not liquidation event data |
| `hf_discovered__french-open-data_caracteristiques-des-retraites-age-de-liquidation` | README FR pension "retraite/liquidation" (retirement) | YES | **NO** | NO | N/A | NO | **NO-GO** | semantic false positive (pension liquidation), unrelated domain |
| `hf_discovered__french-open-data_caracteristiques-des-retraites-conditions-de-liquidation` | README FR pension retirement dataset | YES | **NO** | NO | N/A | NO | **NO-GO** | semantic false positive, unrelated domain |

## Summary
- **Total candidates reviewed:** 22 (8 static/exchange/API + 14 HF-discovered).
- **GO / admissible new sources (§16):** **0**.
- **Closest but still failing:** `ochinimus/crypto-liquidation-ticks` has unauth access + license but evidenced coverage ~27 days (<1 complete month, <3×30d blocks) and unverified instrument/block sufficiency/Track-A schema fit; `nick128373/crypto-liquidation-ticks` lacks evidenced coverage meeting minima. Any of these would require a formal §16 admissibility audit artifact **before** prereg/outcomes — none warranted by current evidence.
- **Terminal/exhausted (not new):** `ironflow/hyperliquid-liquidations`.
- **No action taken:** no prereg created, no outcomes computed, no terminal cells re-run, no Gate 4 polling.

## Required next action (if new evidence appears)
Only on a **materially new** candidate not falsified above: perform `research_state/<source>_admissibility_audit_<UTC>.{md,json}` proving all §16 minima → if `status=ADMISSIBLE` freeze prereg pre-outcomes → build/eval → gate → atomic registry/frontier updates. If no new admissible source appears, remain in clean stop (cache frontier exhausted; external triggers only).
