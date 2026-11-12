# Alternative Liquidation-Label Source Probe Audit — 2026-11-12T19:14:00Z

**Campaign:** `FCLR_NEXT_ALTERNATIVE_LIQUIDATION_SOURCE_DISCOVERY` (frontier rank-0, ACTIVE_HEAVY_CAMPAIGN)
**Session scope:** bounded unauthenticated discovery/probe only (no outcome inspection, no preregistration, no sealed-holdout reuse).
**Gate 4 check:** `ls -1 research_state/fclr016_v5_terms_evidence_RESOLVED_*.json 2>/dev/null || echo "NO_VALID_GATE4_TRIGGER"` → `NO_VALID_GATE4_TRIGGER` (no valid `status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal-attested trigger). Gate 4 Branch 1 not eligible.

## Commands / artifacts inspected or produced
- `python3 scripts/hunt_alternative_liquidation_sources.py` → `research_state/alt_source_scan_latest.json` (candidates=22, source=cache; generated 20261112T191347Z using cached HF search).
- `python3 scripts/deep_review_alt_sources.py` → `research_state/alt_source_deep_review_latest.md` (cache_hits=0 cache_misses=14; probe URLs folded per script note).
- Inspected: `AGENT_HANDOFF.md`, `research_state/experiment_frontier.json`, `research_state/data_source_registry_alt_hunt.json`, `research_state/alt_source_deep_review_latest.md`, `research_state/url_probe_cache.json`, `research_state/hf_search_cache.json`, `research_state/next_data_discovery_plan.md`.
- Live unauthenticated HF metadata probes (API, 2026-11-12T19:14Z) for: `ironflow/hyperliquid-liquidations`, `PhysiAI/Bitcoin-Liquidation-Heatmapping{,-5m,-1h}`, `carrierone/verilex-defi-liquidations`, `Chainticks/defi-liquidations`, `ochinimus/crypto-liquidation-ticks`, `nick128373/crypto-liquidation-ticks`, `craftify2221/hyperliquid-builder-liquidation-panel`, `pCwOrM/werracle-oev-liquidation-dataset-2026`, `tanod/base-lending-liquidations`, `Gopher-Lab/bankless_Hasu__Hart_on_Oval__The_Recapturing_of_Billions_in_DeFi_Liquidations`.

## Acceptance minima (RESEARCH_PROMPT §5/§16, applied per handoff §4)
- ≥5 instruments, ≥1 complete month **or** ≥3 non-overlapping 30-day blocks
- Unauthenticated, no payment/credentials/manual intervention
- Provenance/license documented and acceptable for research use
- Observed liquidation labels only (no modeled/proxy/synthetic as observed)
- Venue-consistent with target design (no Binance/2024 conflation with Hyperliquid windows where joined)
- Completeness characterized (census vs sample) and joinable/admissible before prereg/outcomes (§16 audit before outcomes)

## Evidence by candidate family

| Source | Probe evidence (unauthenticated) | Minima assessment | GO/NO-GO |
|---|---|---|---|
| `ironflow/hyperliquid-liquidations` (HF, CC BY 4.0, lastModified 2026-11-07T10:18:25Z) | Events/fills 2025-05..2026-10 only (siblings confirm no 2026-11+). Known admissible on sealed HL windows but **no verified post-2026-10-31 observed-label extension**; HL 2025H1 observed-label path already closed by terminal stop. | Fails "new admissible source / new verified label extension" for advancing P2 beyond closed design; no new coverage. | **NO-GO (no new extension; exhausted for closed HL 2025H1 path)** |
| Hyperliquid public API (`api.hyperliquid.xyz/info`) | GET 405 (cached/probed); POST info/meta exists historically but **no historical liquidation census parquet/download path evidenced** meeting minima (per registry/deep review). | No evidenced unauthenticated observed liquidation-label census with required coverage/schema/provenance. | **NO-GO** (no admissible label dataset evidenced) |
| Binance Vision liquidationSnapshot | 404/NoSuchKey on probed paths (deep review/cache). | No accessible liquidation census at probed unauthenticated paths. | **NO-GO** |
| Bybit/OKX/Deribit/Coinglass/Tardis/Kaiko/CoinAPI/Glassnode/Laevitas/CryptoDataDownload/cryptofeed | Probes show 401/403/404/auth-missing/DNS/lib-only/site-only or paid/auth-gated signals (url_probe_cache + deep review). | Fails unauthenticated admissible historical liquidation-label dataset requirement (or not a dataset host). | **NO-GO** |
| `ochinimus/crypto-liquidation-ticks` (HF, CC BY 4.0, 2026-08-07, 800 symbols, Bybit/Binance/OKX, 2026-07-08T16:42:32Z..2026-08-06T23:59:42Z, ~29.3 days, 1.44M rows) | Unauthenticated metadata/readme indicates single snapshot window. | Fails **≥1 complete month** and fails **≥3 non-overlapping 30-day blocks** (<30 days total). Venue mix (CEX perps) would also require venue-consistency care vs HL-specific designs. | **NO-GO** (coverage window insufficient) |
| `nick128373/crypto-liquidation-ticks` (HF, CC BY 4.0) | Same file/window signature as `ochinimus` snapshot (coverage/liquidations_full_20260807.csv). | Same as above. | **NO-GO** (duplicate/insufficient window) |
| `PhysiAI/Bitcoin-Liquidation-Heatmapping*` (HF, Apache-2.0) | Repo contains only README/.gitattributes in siblings; metadata shows no data files; described as heatmapping/derived visualization-oriented artifacts. | Fails evidenced observed liquidation-label dataset availability/coverage/instrument minima; likely derived rather than census observed events. | **NO-GO** (no evidenced observed label dataset meeting minima) |
| `Chainticks/defi-liquidations` (HF, CC BY 4.0, parquet by date 2026-05-10.. visible) | On-chain **DeFi lending** liquidations (Aave/Compound/Venus/Morpho etc.), multi-chain protocol events, not perp-exchange funding/liquidation microstructure. | Not venue-/mechanism-consistent with perp funding-conditioned liquidation-risk designs in this repo; different label semantics; joinability/admissibility to HL/Binance perp funding panels not evidenced. | **NO-GO** (venue/mechanism mismatch; not admissible for current P2 design without new justified prereg + §16 audit proving comparability — none evidenced) |
| `craftify2221/hyperliquid-builder-liquidation-panel` (HF, ODC-BY, Hyperliquid account-day panel) | Observational account-day/builder-interface panel artifacts (parquet/csv/txt); research framing "does interface predict liquidation?" suggests derived panel/labels. | Not evidenced as raw observed liquidation-event census with required event-level completeness; label construction/observed-vs-derived status unverified from metadata alone — would require §16 audit before any use, but **no smoke-test evidence of admissible observed liquidation labels + required block structure**. | **NO-GO for this session** (label/coverage/completeness not evidenced as admissible; do not treat as observed without audit) |
| `pCwOrM/werracle-oev-liquidation-dataset-2026` (HF, CC BY 4.0) | OEV/DeFi liquidation execution records (Chainlink SVR, Base L2 etc., 513 liquidations / 105 txs per description). | Far below instrument/block minima for perp funding-conditioned panel; DeFi/mechanism mismatch. | **NO-GO** (coverage and mechanism mismatch) |
| `tanod/base-lending-liquidations` (HF, CC BY 4.0, rolling 30-day aggregate census copy 2026-10-11..2026-11-09) | Aggregate counts/USD by protocol on Base lending; ~30-day rolling window copy. | Fails instrument/block minima and event-level observed-label requirements for this design; lending/chain mismatch. | **NO-GO** |
| `carrierone/verilex-defi-liquidations` (HF, MIT, metadata/API-oriented) | Repo siblings only README/.gitattributes; API/product sample, not a downloadable historical observed-liquidation dataset meeting minima. | No evidenced unauthenticated historical dataset with required coverage/labels. | **NO-GO** |
| `Gopher-Lab/bankless_*DeFi_Liquidations` (HF, 2024, n<1K, transcript-like parquet) | Small/non-panel textual/transcript dataset. | No observed liquidation event panel meeting minima. | **NO-GO** |
| `french-open-data/caracteristiques-des-retraites-*` (HF) | Non-crypto retirement datasets; name collision on "liquidation". | Irrelevant domain. | **NO-GO** |

## Summary
- **Gate 4:** absent (`NO_VALID_GATE4_TRIGGER`).
- **New admissible observed-liquidation source passing smoke test:** **none identified** in this bounded session.
- **Material delta vs prior caches:** re-ran hunt/deep-review scripts (cache-backed) and performed targeted live HF metadata probes on discovered candidates; no candidate met §5/§16 minima for claim-worthy P2 advancement. Ironflow remains the only known admissible HL observed-label source on its sealed window but provides **no verified post-2026-10-31 extension** and cannot advance the closed HL 2025H1 `liq` design.
- **Required next evidence for GO:** a concrete source with (a) unauthenticated access proof, (b) documented provenance/license, (c) observed liquidation labels (not modeled/proxy), (d) ≥5 instruments and ≥1 complete month or ≥3 non-overlapping 30-day blocks, (e) venue/feature joinability and completeness characterization — followed by `research_state/<source>_admissibility_audit_<UTC>.{md,json}` **before** prereg/outcomes.

## Exact failing minima / stop
All probed non-ironflow candidates failed at least one hard minimum: insufficient coverage window/blocks, not an observed liquidation-label dataset, auth/payment/gated or inaccessible, wrong domain/mechanism/venue, or no evidenced dataset files/schema. No §16 admissibility audit warranted because no source passed smoke test. **Clean stop.**
