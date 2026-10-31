# Track A Dead-End Map (Observed Liquidation Labels)

**Document type:** Complete probe map with explicit GO/NO-GO and rationale
**Generated:** 2026-10-31T02:24:27Z (restored full version 2026-10-31T02:26:45Z after truncation audit)
**Status:** BLOCKED — NO ADMISSIBLE UNAUTHENTICATED SOURCE FOUND

Cross-linked: `research_state/liquidation_source_campaign.md`, `research_state/track_a_structural_block.md`, `research_state/negative_results_report.md`, `research_state/next_data_discovery_plan.md`, `research_state/liquidation_sources_enumeration.md`, `research_state/binance_source_probe.md`

## Probes executed (exhaustive per plan)

| Candidate family | Access method (unauth) | Coverage tested | Completeness/notes | License/terms | GO/NO-GO | Rationale |
|---|---|---|---|---|---|---|
| Binance public data (alt paths) | GitHub/binance-public-data, data.binance.vision, fapi v1 | BTCUSDT/ETHUSDT/SOLUSDT/XRPUSDT, 2024 windows | liquidationSnapshot daily/monthly → HTTP 404 (NoSuchKey); fapi/v1/forceOrders → HTTP 451 geo-restricted; no public liquidation snapshot/archive in admissible unauth paths | Public repo terms OK in principle but required data not present | NO-GO | Missing required liquidation labels; cannot satisfy ≥5 symbols, ≥3 blocks, documented completeness |
| OKX public data | Public endpoints/archives (unauth) | Spot/perp coverage checked | No defensible unauth historical liquidation label set with required depth/completeness | Terms checked; data not available in required form | NO-GO | Insufficient/absent admissible labels |
| Bybit public data | public.bybit.com | Trade CSVs (BTCUSDT2024-03-01.csv.gz etc.) | Trade-level only; no `liquidation/` directory (404 on /lin/liquidation/); trades cannot be converted to a complete liquidation census without venue rules | Public data terms; not a census | NO-GO | Trades are not liquidation events; cannot satisfy completeness |
| Deribit public data | Public endpoints/archives (unauth) | Checked | No admissible unauth liquidation history meeting requirements | Checked | NO-GO | Absent |
| Zenodo/OSF/arXiv | Direct download (unauth) | Searched for liquidation datasets | No dataset found matching venue/perp liquidation labels with required coverage/license for this study | N/A | NO-GO | No match |
| GitHub raw/search | Raw files/repos (unauth) | Broad search; GitHub code search 401 | No admissible curated liquidation label sets found | Varies; no suitable set found | NO-GO | No match |
| Hugging Face | Public datasets (unauth) | ochinimus/crypto-liquidation-ticks (CC BY 4.0) | Covers 2026-07-08..2026-08-06 only; already exhausted by FCLR-005; no 2024 data | CC BY 4.0 OK but wrong period | NO-GO | Wrong time period; insufficient blocks for 2024 confirmatory |
| CryptoDataDownload | Public pages/downloads (unauth) | Checked | No liquidation-label product in admissible unauth form meeting requirements | Checked | NO-GO | Absent |
| Tardis.dev / CryptoHFTData | Vendor catalogs | Checked | Commercial; requires access/terms; not free unauthenticated bulk download | Paywalled | NO-GO | Not admissible under free-data constraint |

## Requirements (must meet for GO)
- ≥5 symbols (perp), ≥3 non-overlapping 30-day blocks in same windows
- Documented completeness/coverage (venue scope, gaps), provenance
- Admissible unauthenticated download path, license OK
- Defensible label construction (separate from modeled breaches)

## Completeness diagnostics
- Binance: liquidationSnapshot 404 + forceOrders 451 → cannot support temporal coverage/completeness.
- Bybit: trades present but no census; trade→liquidation conversion non-trivial and not a venue-published census.
- Others: no verifiable unauthenticated complete source found.
- Partial streams (incl. HF 2026 ticks) cannot satisfy the "complete event census" requirement (RESEARCH_PROMPT.md §15). Absence cannot be inferred from missing data.

## Conclusion
No route meets GO criteria. All candidate families probed with evidence recorded in `liquidation_source_campaign.md`, `liquidation_sources_enumeration.md`, `binance_source_probe.md`, and `negative_results_report.md`. **SOLE REOPEN PATH:** New admissible unauthenticated liquidation data appearing that meets requirements (≥5 symbols, ≥3 blocks, documented completeness, license OK) — per RESEARCH_PROMPT.md §16. No pre-registered Track A experiment is possible under current constraints.

## Traceability
- `research_state/liquidation_source_campaign.md`
- `research_state/track_a_structural_block.md`
- `research_state/liquidation_sources_enumeration.md`
- `research_state/binance_source_probe.md`
- `research_state/negative_results_report.md`
- `research_state/next_data_discovery_plan.md`
- `research_state/cross_track_decision_log.md`