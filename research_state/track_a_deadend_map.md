# Track A Dead-End Map (Observed Liquidation Labels)

**Generated:** 2026-10-31T02:18:31Z
**Status:** BLOCKED / NO-GO — Structural blocker; no admissible unauthenticated source found
**Tracks:** A (observed liquidations) | Priority: P1 (after Track C)

## Goal
Find admissible unauthenticated historical liquidation records (≥5 symbols, ≥3 non-overlapping 30-day blocks, documented completeness, license OK) for 2024 windows to enable Track A evaluation.

## Probes Executed (Evidence)

### Binance (official/public)
- **data.vision / public data archives:** Probed for liquidation/futures liquidation archives. HTTP 404s observed for liquidationSnapshot paths; no accessible bulk liquidation history found via unauthenticated paths.
- **fapi v1 forceOrders / liquidation endpoints:** Required authentication / geo-restricted (451) in tested paths; not unauthenticated.
- **Source:** `research_state/binance_source_probe.md`, `research_state/liquidation_sources_enumeration.md`

### OKX
- **Public endpoints / bulk archives:** Probed; no freely downloadable historical liquidation tick/aggregate archives with sufficient coverage found via unauthenticated access.

### Bybit
- **Public archives / APIs:** Probed; no admissible unauthenticated historical liquidation dataset identified.

### Deribit
- **Public archives:** Probed; no suitable unauthenticated historical liquidation records found.

### Academic/Repo Archives
- **Zenodo:** Searched; no matching admissible dataset with required coverage/license identified.
- **OSF:** Searched; no admissible dataset found.
- **arXiv:** Searched; no dataset release matching requirements.
- **GitHub raw/search:** Probed; no admissible unauthenticated liquidation archives found.

### ML/Data Platforms
- **Hugging Face:** Probed (e.g. ochinimus/crypto-liquidation-ticks census) — covers 2026-07-08..2026-08-06 only (exhausted by FCLR-005 exploratory work), insufficient for 2024 windows and not meeting >=3 blocks for 2024 confirmatory needs.
- **CryptoDataDownload:** Probed; no liquidation labels found.

## Dead-End Summary
| Candidate Family | Unauthenticated? | 2024 Coverage | >=5 symbols | >=3 blocks | Completeness documented | License OK | GO/NO-GO | Rationale |
|-------------------|-------------------|---------------|-------------|------------|--------------------------|------------|-----------|-----------|
| Binance data.vision liquidation archives | No/404 | Unknown/None | Unknown | Unknown | No | Unknown | NO-GO | Paths return 404; no accessible bulk archive found |
| Binance fapi forceOrders | No (auth/451) | N/A | N/A | N/A | N/A | N/A | NO-GO | Requires auth/geo-restriction |
| OKX bulk/liquidations | Unclear/No | None found | No | No | No | Unknown | NO-GO | No admissible unauthenticated historical set found |
| Bybit archives | Unclear/No | None found | No | No | No | Unknown | NO-GO | No admissible unauthenticated historical set found |
| Deribit archives | Unclear/No | None found | No | No | No | Unknown | NO-GO | No admissible unauthenticated historical set found |
| Zenodo/OSF/arXiv | Yes (if present) | None found | No | No | No | Unknown | NO-GO | No matching datasets found |
| GitHub raw | Yes | None found | No | No | No | Unknown | NO-GO | No admissible liquidation archives found |
| HuggingFace (ochinimus) | Yes | 2026 only | Yes (partial) | 1 block (exhausted) | Partial | Unknown | NO-GO | Wrong time period; insufficient for 2024; already exhausted by exploratory FCLR-005 |
| CryptoDataDownload | Yes | None found | No | No | No | Unknown | NO-GO | No liquidation labels found |

## Conclusion
**Structural blocker confirmed.** All candidate routes probed with no GO. Per RESEARCH_PROMPT.md §16 and AGENT_HANDOFF, Track A can only reopen if NEW admissible unauthenticated liquidation data appears (≥5 symbols, ≥3 blocks, documented completeness, license OK). No such source exists currently.

## Traceability
- `research_state/liquidation_source_campaign.md`
- `research_state/track_a_structural_block.md`
- `research_state/next_data_discovery_plan.md`
- `research_state/binance_source_probe.md`
- `research_state/liquidation_sources_enumeration.md`
- `research_state/negative_results_report.md`
