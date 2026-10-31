# Track A Final Block Proof — Observed Liquidations

**Report ID:** FCLR-TRACKA-BLOCK-001
**Date (UTC):** 2026-10-31T09:10:42Z
**HEAD:** 52506b1a
**Priority:** Track A (SECOND) per repo name inference
**Status:** STRUCTURALLY BLOCKED — NO-GO for 2024 confirmatory window
**Reopen:** ONLY if NEW admissible unauthenticated source appears meeting rubric

## Rubric (machine-checkable)
A source is admissible for confirmatory Track A only if ALL of:
1. `unauthenticated == true` (no account/API key required)
2. `no_keys == true` (no personal API keys/manual tokens)
3. `symbols >= 5` (sufficient cross-section)
4. `blocks >= 3` (non-overlapping >=30-day blocks for power/robustness)
5. `completeness_doc == true` (documented coverage/completeness/gaps)
6. `license_ok == true` (lawful unauthenticated use)
7. `census_or_defensible == true` (census or defensible sample, not live-only stream reconstruction claim)

## Evidence sources consolidated
- `research_state/liquidation_sources_enumeration.md`
- `research_state/liquidation_source_campaign.md`
- `research_state/track_a_deep_sweep.md`
- `research_state/track_a_structural_block.md`
- `research_state/track_a_deadend_map.md`
- `research_state/fclr004_blocked.md`, `research_state/evaluation_summary_FCLR004_BLOCKED.md`
- `research_state/evaluation_summary_FCLR005.md`
- `research_state/negative_results_report.md`

## Machine-checkable probe results (consolidated)
| Candidate | unauth | no_keys | symbols | blocks(>=30d) | completeness_doc | license_ok | census/defensible | HTTP/status | Notes | GO/NO-GO |
|-----------|--------|---------|---------|---------------|-------------------|------------|-------------------|-------------|-------|----------|
| Binance fapi forceOrders (liquidation snapshots/orders) | true | true | varies | unknown/insufficient | no | unknown | live-only/recent | 451 (geo) / 404 in places | No historical census for 2024 window; requires auth in practice or blocked | NO-GO |
| Binance public-data repo liquidation paths | true | true | unknown | unknown | no | ok | unclear | 404/paths missing | No confirmed liquidation files for required window | NO-GO |
| OKX public liquidation history | true | true | unknown | insufficient | no | unclear | live-only | varies; no bulk 2024 census found | No admissible bulk census | NO-GO |
| Bybit public liquidation data | true | true | unknown | insufficient | no | unclear | unclear | no confirmed bulk | No admissible bulk census | NO-GO |
| Deribit public liquidation data | true | true | unknown | insufficient | no | unclear | unclear | no confirmed bulk | No admissible bulk census | NO-GO |
| CryptoDataDownload liquidation files | true | true | limited | insufficient | partial | unclear | partial | checked | No >=5-symbol >=3-block 2024 census | NO-GO |
| HuggingFace datasets (liquidations) | true | true | unknown | insufficient | varies | varies | unclear | checked | No admissible confirmatory census found | NO-GO |
| Zenodo/OSF/arXiv datasets | true | true | unknown | insufficient | varies | varies | unclear | checked (no download) | No admissible confirmatory census found | NO-GO |
| GitHub repos with liquidation dumps | true | true | unknown | insufficient | varies | varies | unclear | checked | No admissible confirmatory census found | NO-GO |
| ochinimus (2026 only) | true | true | limited | 0 (<3) for confirmatory | partial | unclear | exploratory only | used in FCLR-005 | 2026-07-08..2026-08-06 window; 0 blocks, exploratory-only, no incremental skill shown | NO-GO (confirmatory) |

## Confirmatory outcome
- FCLR-004: BLOCKED (no admissible 2024 census)
- FCLR-005: EXPLORATORY-ONLY on exhausted 2026 window (<3 blocks) — no incremental skill of funding+price over RV-only demonstrated

## Final determination
**NO source passes the full rubric. Track A remains STRUCTURALLY BLOCKED for confirmatory work.**

**SOLE REOPEN CONDITION (verbatim):** New admissible unauthenticated data source per RESEARCH_PROMPT.md §16 with documented provenance/licenses/coverage, >=5 symbols, >=3 non-overlapping 30-day blocks, census or defensible sample, and machine-checkable evidence. If such source appears, MUST freeze protocol and pre-register BEFORE examining outcomes.
