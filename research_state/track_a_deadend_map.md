# Track A Dead-End Map (Observed Liquidation Labels)

**Document type:** Complete probe map with explicit GO/NO-GO and rationale
**Generated:** 2026-10-31T02:24:27Z
**Status:** BLOCKED — NO ADMISSIBLE UNAUTHENTICATED SOURCE FOUND

Cross-linked: `research_state/liquidation_source_campaign.md`, `research_state/track_a_structural_block.md`, `research_state/negative_results_report.md`, `research_state/next_data_discovery_plan.md`

## Probes executed (exhaustive per plan)

| Candidate family | Access method (unauth) | Coverage tested | Completeness/notes | License/terms | GO/NO-GO | Rationale |
|---|---|---|---|---|---|---|
| Binance public data (alt paths) | GitHub/binance-public-data, direct archive paths | BTCUSDT/ETHUSDT/SOLUSDT/XRPUSDT, 2024 windows | No public liquidation snapshot/archive found in admissible unauth paths; paths checked per campaign | Public repo terms OK in principle but required data not present | NO-GO | Missing required liquidation labels; cannot satisfy ≥5 symbols, ≥3 blocks, documented completeness |
| OKX public data | Public endpoints/archives (unauth) | Spot/perp coverage checked | No defensible unauth historical liquidation label set found with required depth/completeness | Terms checked; data not available in required form | NO-GO | Insufficient/absent admissible labels |
| Deribit public data | Public endpoints/archives (unauth) | Checked | No admissible unauth liquidation history meeting requirements | Checked | NO-GO | Absent |
| Zenodo/OSF/arXiv | Direct download (unauth) | Searched for liquidation datasets | No dataset found matching venue/perp liquidation labels with required coverage/license for this study | N/A | NO-GO | No match |
| GitHub raw/search | Raw files/repos (unauth) | Broad search | No admissible curated liquidation label sets found | Varies; no suitable set found | NO-GO | No match |
| Hugging Face | Public datasets (unauth) | Searched | No admissible dataset with required provenance/completeness | Terms vary; no suitable set | NO-GO | No match |
| CryptoDataDownload | Public pages/downloads (unauth) | Checked | No liquidation-label product in admissible unauth form meeting requirements | Checked | NO-GO | Absent |

## Requirements (must meet for GO)
- ≥5 symbols (perp), ≥3 non-overlapping 30-day blocks in same windows
- Documented completeness/coverage (venue scope, gaps), provenance
- Admissible unauthenticated download path, license OK
- Defensible label construction (separate from modeled breaches)

## Conclusion
No route meets GO criteria. All candidates probed with evidence recorded. **SOLE REOPEN PATH:** New admissible unauthenticated liquidation data appearing that meets requirements (per RESEARCH_PROMPT.md §16). No pre-registered Track A experiment possible under current constraints.
