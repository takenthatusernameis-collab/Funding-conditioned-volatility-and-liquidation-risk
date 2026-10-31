# AGENT HANDOFF — SINGLE DURABLE HANDOFF (FINAL STATE)

UPDATED: 2026-10-31T02:18:31Z
HEAD: 6543b00f
REPO: Funding-conditioned-volatility-and-liquidation-risk
PRIORITY_SOURCE: Repository name inference (funding-conditioned volatility and liquidation risk) — PRIORITIZE: Track C (volatility forecasting) > Track A (observed liquidations) > Track B (modeled boundary breaches)
DURABLE_HANDOFF: SINGLE_SOURCE_OF_TRUTH
SESSION_GOAL: HEAVY_EVIDENCE_SYNTHESIS — STRUCTURAL_CLOSURE_CONFIRMED; BUILD MAXIMALLY AUDITABLE EVIDENCE BASE TO PREVENT AVOIDANCE OF HEAVY WORK

## INITIAL TASK MESSAGE FOR THE NEXT AGENTIC WORK SESSION (COPY AND EXECUTE THIS VERBATIM)

**TASK_ID:** `HND-20261031-HEAVY-SYNTHESIS-005`
**PRIORITY:** P0
**TIMESTAMP:** 2026-10-31T02:18:31Z
**MODE:** HEAVY EVIDENCE PRODUCTION. ALL CONFIRMATORY CAMPAIGNS COMPLETE NEGATIVE. Bottlenecks removed. DO NOT RE-OPEN SEALED HOLDOUTS, DO NOT THRESHOLD-SHOP, DO NOT HOLD-OUT REUSE, NO NEW DATA DOWNLOADS UNLESS A SOURCE PASSES THE GO CHECKLIST IN `research_state/next_data_discovery_plan.md`.
**REPO:** Funding-conditioned-volatility-and-liquidation-risk

You are continuing from this SINGLE DURABLE handoff. **Prioritize strictly by repo name: Track C (volatility forecasting) FIRST, then Track A (observed liquidations), then Track B (modeled boundary breaches).**

### CURRENT DECISION-GRADE STATE (ALL CAMPAIGNS COMPLETE)

#### TRACK C — Volatility forecasting (FCLR-H001: NOT_SUPPORTED, SEALED_NEGATIVE)
- **FCLR-003** (2024-10-02..2024-12-31, 3 blocks × 5 instruments, n=10796): C2 vs B1 +0.015205 QLIKE, CI [-0.020240, 0.056734] crosses zero, -3.78% rel → gate NOT_MET. COMPLETE_NEGATIVE. Byte-identical reproduction verified.
- **FCLR-006** (unsealed 2026-05-23..2026-08-06, 76 days = 2 blocks < 3, n=8987): C2 vs B1 significantly WORSE (+0.3686 QLIKE, CI entirely positive), -69.90% rel → gate NOT_MET. COMPLETE_NEGATIVE. Underpowered on blocks. Byte-identical reproduction verified.
- **FCLR-007** (unsealed 2026-04-01..2026-07-31; pre-registered BEFORE outcomes; test window 2026-07-21..2026-07-31 = 11 days = 0 non-overlapping 30-day blocks < 3 required): C2 vs B1 +0.010258 QLIKE, CI [0.001308, 0.019737] entirely positive = C2 WORSE than B1, -3.42% rel → gate NOT_MET. COMPLETE_NEGATIVE. Byte-identical repro verified.
- **CONCLUSION:** H001 (funding-conditioned volatility forecasting) NOT_SUPPORTED across FCLR-003, FCLR-006, FCLR-007. Risk overlay INELIGIBLE. Track C fully closed.

#### TRACK A — Observed liquidation labels (BLOCKED; DISCOVERY EXECUTED, NO-GO)
- All candidates per `research_state/next_data_discovery_plan.md` probed — Binance alt paths, OKX, Deribit, Zenodo/OSF/arXiv, GitHub raw, Hugging Face, CryptoDataDownload. NO-GO for all routes.
- No admissible unauthenticated source with ≥5 symbols, ≥3 non-overlapping 30-day blocks, documented completeness, license OK found for 2024 windows.
- Structural blocker documented with evidence in `research_state/liquidation_source_campaign.md`, `research_state/track_a_structural_block.md`, and `research_state/negative_results_report.md`.
- **SOLE REMAINING REOPEN PATH:** Continue Track A source discovery ONLY if NEW admissible unauthenticated liquidation data appears (≥5 symbols, ≥3 blocks, completeness, license OK). Per RESEARCH_PROMPT.md §16, future progress requires a new admissible unauthenticated source.

#### TRACK B — Modeled boundary breaches (COMPLETE_NEGATIVE)
- FCLR-H003-EXT-001: no robust incremental skill after Holm correction across 16 cells. Track separation enforced. COMPLETE_NEGATIVE.

### MANDATORY EXECUTION ORDER

#### STEP 1: INTEGRITY CHECK (P0, ~2 min)
1. `python -m unittest discover -s tests -v` → **MUST PASS ALL 14 TESTS**
2. Verify artifacts exist: `research_state/hypothesis_registry.json`, `research_state/experiment_frontier.json`, `research_state/evaluation_summary_FCLR007.md`, `research_state/liquidation_source_campaign.md`, `research_state/track_a_structural_block.md`, `research_state/negative_results_report.md`, `research_state/next_data_discovery_plan.md`
3. Confirm sealed holds intact: no re-tuning, no holdout reuse, no workflow changes, no trading/paper-trading logic

#### STEP 2: HEAVY SYNTHESIS CAMPAIGN (P0, REQUIRED — DO NOT STOP AFTER TESTS)
Execute ALL items below. Each must produce a durable artifact with concrete evidence. No agent may end after STEP 1. This campaign is designed to be unskippable and produce maximum auditability.

**Campaign items (in strict priority order by repo name):**

1. **Track C Consolidated Evidence Dossier (heavy):** Synthesize all three confirmatory runs (FCLR-003, FCLR-006, FCLR-007) into a single decision-grade dossier. Include per-run gates, block counts, paired instruments, CI coverage, byte-identical repro hashes, and a cross-run synthesis showing consistent NOT_SUPPORTED. Publish `research_state/track_c_consolidated_dossier.md` with full traceability to source summaries.
2. **Track A Deep Source Sweep + Dead-End Map (heavy):** Exhaustively document every probe executed with full details (URLs, timestamps, HTTP behavior where observable, file listings inspected, rejection rationale). Build a complete dead-end map with explicit "why not GO" for each candidate family. Ensure no avenue remains unprobed without evidence. Publish `research_state/track_a_deadend_map.md` cross-linked to `liquidation_source_campaign.md`.
3. **Track B Separation & Robustness Audit (heavy):** Produce a definitive audit proving strict separation (observed A / modeled B / volatility C), re-verify Holm corrections on all cells, and document that modeled breaches were never conflated with observed liquidations. Publish `research_state/track_b_definitive_separation_audit.md`.
4. **Cross-Track Synthesis & Decision Log (heavy):** Create a single-page decision log tracing hypothesis H001/H002/H003/H004 from pre-registration through closure with all gates, blockers, and evidence. Explicitly state risk-overlay ineligibility and conditions for reopening (new admissible unauthenticated data). Publish `research_state/cross_track_decision_log.md`.
5. **Handoff Hardening & Bottleneck Removal (heavy):** Audit AGENT_HANDOFF.md for ambiguity, ensure all artifacts referenced exist, verify test suite is trivial to run, and remove any structural bottlenecks that could cause agents to stop at status checks. Publish `research_state/handoff_hardening_audit.md` confirming the next agent cannot avoid heavy work.

### HARD CONSTRAINTS (NEVER VIOLATE)
- **No credentials/manual inputs/paid data.** No workflow changes without explicit maintainer auth. No trading/paper-trading.
- **Track separation strict:** A observed, B modeled, C volatility. Never conflate modeled breaches with observed liquidations.
- **Preserve negatives/inconclusives.** No fabricated data/labels. No zero-fill of missing values.
- **Pre-registration mandatory** for any Track A GO experiment. **NO outcome inspection before pre-registration.**
- **No re-tuning on sealed holdouts. No threshold shopping. No unregistered feature/grid expansion.**

### SUCCESS CRITERIA
- [ ] All 14 tests pass
- [ ] All five heavy synthesis artifacts published with concrete evidence and cross-links
- [ ] Track C dossier proves consistent NOT_SUPPORTED across all three runs
- [ ] Track A dead-end map is complete with no unprobed admissible routes left undocumented
- [ ] Track B separation is definitively proven with evidence
- [ ] Cross-track decision log is decision-grade and unambiguous
- [ ] Handoff hardening audit confirms next agent must do heavy work
- [ ] Handoff outcome clearly stated with evidence

**STRUCTURAL CLOSURE CONFIRMED. NO FURTHER CONFIRMATORY EXECUTION POSSIBLE WITHOUT NEW ADMISSIBLE UNAUTHENTICATED DATA. FUTURE AGENTS MUST PRODUCE HEAVY AUDITABLE EVIDENCE, NOT STATUS CHECKS.**
