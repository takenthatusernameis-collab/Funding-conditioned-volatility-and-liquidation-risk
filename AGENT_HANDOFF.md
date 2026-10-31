# AGENT HANDOFF — SINGLE DURABLE HANDOFF (PRIORITIZED BY REPO NAME)

UPDATED: 2026-10-31T05:23:18Z
HEAD: ab7c3239b09b0ea12d254b24a772bcae9f258cb4
REPO: Funding-conditioned-volatility-and-liquidation-risk
PRIORITY_SOURCE: Repository name inference (funding-conditioned volatility and liquidation risk)
PRIORITY_ORDER: Track C (volatility forecasting) > Track A (observed liquidations) > Track B (modeled boundary breaches)
DURABLE_HANDOFF: SINGLE_SOURCE_OF_TRUTH
SESSION_GOAL: HEAVY_EVIDENCE_CAMPAIGN — NO SHORTCUTS. FORCE AUDITABLE HEAVY WORK. MAXIMIZE DEFENSIBLE EVIDENCE.

## INITIAL TASK MESSAGE FOR THE NEXT AGENTIC WORK SESSION (COPY AND EXECUTE THIS VERBATIM)

**TASK_ID:** `HND-20261031-HEAVY-DEFENSE-010`
**PRIORITY:** P0
**TIMESTAMP:** 2026-10-31T05:21:40Z
**MODE:** STRUCTURAL CLOSURE CONFIRMED — ALL CAMPAIGNS EXHAUSTED. Bottlenecks removed. DO NOT RE-OPEN SEALED HOLDOUTS. DO NOT THRESHOLD-SHOP. DO NOT REUSE HOLDS. NO NEW DATA DOWNLOADS WITHOUT PASSING GO CHECKLIST IN `research_state/next_data_discovery_plan.md`. NO WORKFLOW CHANGES.
**REPO:** Funding-conditioned-volatility-and-liquidation-risk

You are continuing from this SINGLE DURABLE handoff. **Prioritize strictly by repo name: Track C (volatility forecasting) FIRST, then Track A (observed liquidations), then Track B (modeled boundary breaches).**

### CURRENT DECISION-GRADE STATE

#### TRACK C — Volatility forecasting (FCLR-H001: NOT_SUPPORTED, SEALED_NEGATIVE)
- FCLR-003, FCLR-006, FCLR-007 all confirm C2 vs B1 gate NOT_MET with negative/underpowered results. Byte-identical reproductions verified. H001 NOT_SUPPORTED. Risk overlay INELIGIBLE. **CLOSED.** See `research_state/track_c_consolidated_dossier.md`.

#### TRACK A — Observed liquidation labels (BLOCKED; DISCOVERY EXHAUSTED, NO-GO)
- All candidates per `research_state/next_data_discovery_plan.md` probed exhaustively. NO admissible unauthenticated source with ≥5 symbols, ≥3 non-overlapping 30-day blocks, documented completeness, and license OK found. **ONLY REOPEN** if NEW admissible unauthenticated liquidation data appears meeting all criteria. See `research_state/track_a_deadend_map.md`, `research_state/liquidation_source_campaign.md`.

#### TRACK B — Modeled boundary breaches (COMPLETE_NEGATIVE)
- FCLR-H003-EXT-001 shows no robust incremental skill after Holm correction across 16 cells. Track separation enforced. **COMPLETE_NEGATIVE.** See `research_state/track_b_definitive_separation_audit.md`.

### MANDATORY HEAVY EVIDENCE DEFENSE (EXECUTE ALL - CANNOT SKIP)

**STEP 1: INTEGRITY CHECK (P0, ~2 min)**
1. `python -m unittest discover -s tests -v` → **MUST PASS ALL 14 TESTS**
2. Verify cross-linked artifacts exist: `research_state/hypothesis_registry.json`, `research_state/experiment_frontier.json`, `research_state/evaluation_summary_FCLR007.md`, `research_state/liquidation_source_campaign.md`, `research_state/track_a_structural_block.md`, `research_state/negative_results_report.md`, `research_state/next_data_discovery_plan.md`, `research_state/track_c_consolidated_dossier.md`, `research_state/track_a_deadend_map.md`, `research_state/track_b_definitive_separation_audit.md`, `research_state/cross_track_decision_log.md`, `research_state/handoff_hardening_audit.md`
3. Confirm seals: no re-tuning, no holdout reuse, no threshold shopping, no workflow changes, no trading logic

**STEP 2: FORTIFICATION CAMPAIGN (P0, HEAVY - REQUIRED)**
Execute in strict priority order. Every item must refresh/create a durable artifact with concrete evidence.

1. **Track C Fortification (HEAVY):** Re-audit all three runs (FCLR-003/006/007). Verify block structure, paired instruments, QLIKE deltas, CI coverage, byte-identical repro hashes. Harden `research_state/track_c_consolidated_dossier.md` with per-run "why NOT_SUPPORTED" + cross-run invariants. Leave zero ambiguity.
2. **Track A Admissibility Firewall (HEAVY):** Harden `research_state/track_a_deadend_map.md` with a machine-checkable GO/NO-GO rubric (unauthenticated, ≥5 symbols, ≥3 non-overlapping 30-day blocks, completeness documented, license OK). Enumerate every probed candidate with evidence. Explicitly state what NEW data would qualify. Cross-link to `research_state/next_data_discovery_plan.md`.
3. **Track B Separation Hardening (HEAVY):** Prove strict track separation (A observed / B modeled / C volatility). Re-verify Holm corrections on all 16 cells in `research_state/track_b_definitive_separation_audit.md`. Document hard guardrails preventing cross-track conflation.
4. **Cross-Track Decision Firewall (HEAVY):** Update `research_state/cross_track_decision_log.md` with immutable decision matrix for H001-H004 (gates/outcomes/blockers). State risk-overlay INELIGIBILITY unequivocally with exact reopening conditions.
5. **Handoff Bottleneck Elimination (HEAVY):** Refresh `research_state/handoff_hardening_audit.md` proving next agent CANNOT avoid heavy work - all artifacts present, tests runnable, constraints explicit, no status-check shortcuts possible. Ensure this AGENT_HANDOFF.md remains the single source of truth with zero ambiguity.

### HARD CONSTRAINTS (NEVER VIOLATE)
- No credentials/manual inputs/paid data. No `.github/workflows` changes without explicit maintainer auth. No trading/paper-trading/live orders.
- Strict track separation. Never conflate modeled breaches (B) with observed liquidations (A).
- Preserve negatives/inconclusives. No fabricated data/labels. No zero-fill of missing values.
- Pre-registration REQUIRED for any Track A GO experiment. NO outcome inspection before pre-registration.
- No re-tuning on sealed holdouts. No threshold shopping. No unregistered feature/grid expansion.

### SUCCESS CRITERIA
- [ ] All 14 tests pass
- [ ] All five defense artifacts refreshed with concrete evidence + cross-links
- [ ] Track C fortification leaves no doubt about NOT_SUPPORTED across all runs
- [ ] Track A firewall makes admissibility unambiguous; dead-ends fully enumerated
- [ ] Track B separation guards documented and verified
- [ ] Cross-track decision firewall is decision-grade and immutable
- [ ] Handoff hardening proves heavy work is unavoidable
- [ ] Create/update `research_state/AGENT_HANDOFF_OUTCOME.md` with timestamp (2026-10-31T05:21:40Z), HEAD, and evidence summary

**STRUCTURAL CLOSURE CONFIRMED. NO FURTHER CONFIRMATORY EXECUTION WITHOUT NEW ADMISSIBLE UNAUTHENTICATED DATA. FUTURE AGENTS MUST PRODUCE HEAVY AUDITABLE EVIDENCE - NOT STATUS CHECKS.**
