# Track A Final Block Proof — Observed Liquidations (H004)

**Report ID:** FCLR-TRACKA-BLOCK-002 (strengthened)
**Date (UTC):** 2026-10-31T09:13:52Z
**HEAD:** 52506b1a
**Priority:** Track A (SECOND) per repo name inference (funding-conditioned volatility and liquidation risk)
**Status:** STRUCTURALLY BLOCKED — NO confirmatory admissible source for 2024 window
**Strict separation:** Track A (observed) NEVER conflated with Track B (modeled/synthetic)

## Machine-checkable rubric (ALL required)
A source is admissible for confirmatory Track A only if ALL of:
1. `unauthenticated == true` (no account/API key required)
2. `no_keys == true` (no personal API keys/manual tokens)
3. `symbols >= 5` (sufficient cross-section)
4. `blocks >= 3` (non-overlapping >=30-day blocks for power/robustness)
5. `completeness_doc == true` (documented coverage/completeness/gaps/census)
6. `license_ok == true` (lawful unauthenticated use)
7. `census_or_defensible == true` (census or defensible sample, not live-only stream reconstruction)

## Consolidated evidence (all candidates probed)
| Candidate | unauth | no_keys | symbols | blocks(>=30d) | completeness_doc | license_ok | census/defensible | HTTP/status/evidence | Notes | GO/NO-GO |
|-----------|--------|---------|---------|---------------|-------------------|------------|-------------------|----------------------|-------|----------|
| Binance fapi forceOrders/liquidation snapshots | true | true | varies | unknown/insufficient | no | unknown | no (live/recent) | 451 geo / paths checked; no 2024 bulk census | No historical census; blocked/geo-limited or requires auth in practice | NO-GO |
| Binance public-data repo (liquidation paths) | true | true | unknown | unknown | no | ok (repo) | no | paths 404/missing for required liquidation files | No confirmed files for 2024 confirmatory window | NO-GO |
| OKX public liquidation history/bulk | true | true | unknown | insufficient | no | unclear | no | probed; no bulk 2024 census found | No admissible bulk census | NO-GO |
| Bybit public liquidation data | true | true | unknown | insufficient | no | unclear | no | probed; no bulk 2024 census found | No admissible bulk census | NO-GO |
| Deribit public liquidation data | true | true | unknown | insufficient | no | unclear | no | probed; no bulk 2024 census found | No admissible bulk census | NO-GO |
| CryptoDataDownload (liquidations) | true | true | limited | insufficient | partial | unclear | partial | checked; coverage limited | <5 symbols or <3 blocks for 2024 | NO-GO |
| HuggingFace datasets (liquidations) | true | true | unknown | insufficient | varies | varies | unclear/no | checked; no confirmatory census | No admissible census | NO-GO |
| Zenodo/OSF/arXiv | true | true | unknown | insufficient | varies | varies | unclear/no | checked; no download admissible census | No admissible census | NO-GO |
| GitHub liquidation dumps/repos | true | true | unknown | insufficient | varies | varies | unclear/no | checked | No admissible census | NO-GO |
| ochinimus (FCLR-005 exploratory) | true | true | limited | 0 (<3) | partial | unclear | exploratory-only | 2026-07-08..2026-08-06; no incremental skill | Exhausted short window, underpowered, no confirmatory skill | NO-GO (confirmatory) |

## Confirmatory campaign outcomes
- **FCLR-004:** BLOCKED — no admissible 2024 census meeting rubric.
- **FCLR-005:** Exploratory-only on 2026 window (0 blocks). No demonstrated incremental skill of funding+price over RV-only. Cannot support confirmatory claims.

## Bottleneck removal (evidence-based)
All admissible unauthenticated candidates exhaustively probed per RESEARCH_PROMPT.md §16. Firewall is machine-checkable and enforced. No structural workaround exists without a new admissible source.

## Final determination
**NO candidate passes ALL rubric items. Track A remains STRUCTURALLY BLOCKED for confirmatory work.**

**SOLE REOPEN CONDITION (verbatim from RESEARCH_PROMPT.md):** A NEW admissible unauthenticated source with documented provenance/licenses/coverage, >=5 symbols, >=3 non-overlapping 30-day blocks, census or defensible sample, and machine-checkable evidence. If found, MUST freeze protocol and pre-register BEFORE examining outcomes. No relaxation of rubric.

## Artifacts (traceability)
- `research_state/liquidation_sources_enumeration.md`, `research_state/liquidation_source_campaign.md`, `research_state/track_a_deep_sweep.md`, `research_state/track_a_structural_block.md`, `research_state/track_a_deadend_map.md`
- `research_state/evaluation_summary_FCLR004_BLOCKED.md`, `research_state/evaluation_summary_FCLR005.md`
- `research_state/fclr_h004_tracka_viable.json`, `research_state/negative_results_report.md`
