# Track A Final Block Proof — Machine-Checkable (Observed Liquidations)

**Document type:** Decision-grade proof (irrefutable structural block)
**Repository:** Funding-conditioned-volatility-and-liquidation-risk
**Generated:** 2026-10-31T10:11:30Z
**Hypothesis:** FCLR-H004 (observed liquidation outcomes)
**Status:** BLOCKED/STRUCTURALLY BLOCKED (no admissible unauthenticated source)

## Machine-checkable rubric (verbatim)
For any candidate to be admissible for confirmatory Track A:
- unauthenticated == true AND no_keys == true
- symbols >= 5
- blocks >= 3 (non-overlapping 30-day blocks)
- completeness_doc == true
- license_ok == true
- census_or_defensible == true

**ALL must pass. If ANY fails → NO-GO.**

## Consolidated evidence (all candidates checked)

Sources enumerated/swept: `research_state/liquidation_sources_enumeration.md`, `research_state/liquidation_source_campaign.md`, `research_state/track_a_deep_sweep.md`, `research_state/track_a_structural_block.md`, `research_state/track_a_deadend_map.md`, `research_state/binance_source_probe.md`.

| Candidate | Auth/keys | Symbols | Blocks (30d non-overlap) | Completeness doc | License/ToS OK | Census/defensible | GO/NO-GO | Evidence |
|---|---|---|---|---|---|---|---|---|
| Binance forceOrders/fapi liquidation endpoints | Auth/geo-restricted / 451 in tested context or no public unauthenticated census | <5 usable or not census | <3 | Partial/unclear | Unclear/restricted | Not full census | NO-GO | binance_source_probe.md; 404/451 observed in probes |
| Bybit liquidation data (unauthenticated) | Mixed; public endpoints do not provide full historical unauthenticated census with required coverage | Varies | Insufficient for frozen 2024 window; 2026 only ~30-day window exhausted by FCLR-005 | Unclear | Unclear | Incomplete for confirmatory blocks | NO-GO | FCLR-005 used Bybit census for 2026 pilot only (single window, exhausted). No confirmatory-feasible multi-block window found. |
| OKX/Deribit unauthenticated liquidation history | No full unauthenticated historical census meeting rubric | Insufficient | <3 | No/unclear | Unclear | Not census | NO-GO | liquidation_sources_enumeration.md |
| HF/academic liquidation tick datasets (ochinimus etc.) | Often require access; unauthenticated availability does not yield >=3 blocks for frozen 2024 | Limited | 2026-07-08..2026-08-06 only (~1 block) exhausted by FCLR-005 | Partial | Varies | Single window, exhausted | NO-GO | FCLR-005 pilot used such data; confirmatory blocks unavailable |
| GitHub/Zenodo scraped liquidation datasets | Unauthenticated but incomplete coverage/time range; no >=3 non-overlapping 30d blocks for required window | Insufficient | <3 | Often missing | Varies | Not defensible as full census | NO-GO | liquidation_sources_enumeration.md §84-92 |
| Aggregators/third-party APIs | Require keys/auth or rate-limited with no free census | N/A | N/A | No | Unclear/restricted | No | NO-GO | Probed, no admissible path |

## Conclusion
**NO candidate passes ALL rubric items.** Track A remains **STRUCTURALLY BLOCKED**.

## Sole reopen condition (verbatim from RESEARCH_PROMPT.md §16)
> "If the only blocking item is observed-liquidation labels for Track A, explicitly state the minimal admissible evidence (>=5 symbols, >=3 non-overlapping 30-day blocks, documented completeness/coverage, license/ToS OK, unauthenticated or no_keys). Do not guess; if none exists under those constraints, say BLOCKED."

**Sole admissible reopen:** A NEW admissible unauthenticated source (no keys) meeting ALL rubric items above with concrete evidence (endpoint/docs, coverage table, license, census definition). Before any outcome inspection on such source, MUST pre-register experiment/protocol and run GO/NO-GO against rubric with machine-checkable evidence.

## Artifacts
- `research_state/track_a_deadend_map.md` (MACHINE_CHECKABLE_FIREWALL_20261031)
- `research_state/track_a_structural_block.md`
- `research_state/liquidation_sources_enumeration.md`
- `research_state/binance_source_probe.md`
- `research_state/evaluation_summary_FCLR005.md` (pilot/exploratory only, confirms single-window exhaustion)
