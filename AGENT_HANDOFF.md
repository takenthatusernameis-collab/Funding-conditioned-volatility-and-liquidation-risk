# AGENT HANDOFF — SINGLE DURABLE HANDOFF (PRIORITIZED BY REPO NAME)

UPDATED: 2026-10-31T03:30:08Z
HEAD: ab7aa1870829ba23d0cc98ebf2c2f84e05c91780
REPO: Funding-conditioned-volatility-and-liquidation-risk
PRIORITY_SOURCE: Repository name inference (funding-conditioned volatility and liquidation risk)
PRIORITY_ORDER: Track C (volatility forecasting) > Track A (observed liquidations) > Track B (modeled boundary breaches)
DURABLE_HANDOFF: SINGLE_SOURCE_OF_TRUTH
SESSION_GOAL: HEAVY_EVIDENCE_DEFENSE — STRUCTURAL_CLOSURE_CONFIRMED. MAXIMIZE AUDITABLE EVIDENCE; NEVER AVOID HEAVY WORK

## INITIAL TASK MESSAGE FOR THE NEXT AGENTIC WORK SESSION (COPY AND EXECUTE THIS VERBATIM)

**TASK_ID:** `HND-20261031-HEAVY-DEFENSE-009`
**PRIORITY:** P0
**TIMESTAMP:** 2026-10-31T03:30:08Z
**MODE:** STRUCTURAL CLOSURE CONFIRMED — ALL CAMPAIGNS COMPLETE NEGATIVE. Bottlenecks removed. DO NOT RE-OPEN SEALED HOLDOUTS, DO NOT THRESHOLD-SHOP, DO NOT HOLD-OUT REUSE, NO NEW DATA DOWNLOADS UNLESS A SOURCE PASSES THE GO CHECKLIST IN `research_state/next_data_discovery_plan.md`.
**REPO:** Funding-conditioned-volatility-and-liquidation-risk

You are continuing from this SINGLE DURABLE handoff. **Prioritize strictly by repo name: Track C (volatility forecasting) FIRST, then Track A (observed liquidations), then Track B (modeled boundary breaches).**

### CURRENT DECISION-GRADE STATE (ALL CAMPAIGNS COMPLETE)

#### TRACK C — Volatility forecasting (FCLR-H001: NOT_SUPPORTED, SEALED_NEGATIVE)
- **FCLR-003, FCLR-006, FCLR-007:** All confirmatory runs show C2 vs B1 gate NOT_MET with consistent negative/underpowered results. Byte-identical reproductions verified. H001 NOT_SUPPORTED. Risk overlay INELIGIBLE. Track C fully closed. See `research_state/track_c_consolidated_dossier.md`.

#### TRACK A — Observed liquidation labels (BLOCKED; DISCOVERY EXECUTED, NO-GO)
- All candidates per `research_state/next_data_discovery_plan.md` probed exhaustively (Binance/OKX/Bybit/Deribit, Zenodo/OSF/arXiv, GitHub, HuggingFace, CryptoDataDownload, commercial). NO-GO for all routes.
- No admissible unauthenticated source with ≥5 symbols, ≥3 non-overlapping 30-day blocks, documented completeness, license OK found for 2024 windows.
- **SOLE REMAINING REOPEN PATH:** Continue Track A source discovery ONLY if NEW admissible unauthenticated liquidation data appears (≥5 symbols, ≥3 blocks, completeness, license OK). See `research_state/track_a_deadend_map.md`, `research_state/liquidation_source_campaign.md`.

#### TRACK B — Modeled boundary breaches (COMPLETE_NEGATIVE)
- FCLR-H003-EXT-001: no robust incremental skill after Holm correction across 16 cells. Track separation enforced. COMPLETE_NEGATIVE. See `research_state/track_b_definitive_separation_audit.md`.

### MANDATORY EXECUTION ORDER

#### STEP 1: INTEGRITY CHECK (P0, ~2 min)
1. `python -m unittest discover -s tests -v` → **MUST PASS ALL 14 TESTS**
2. Verify all decision artifacts exist and are cross-linked: `research_state/hypothesis_registry.json`, `research_state/experiment_frontier.json`, `research_state/evaluation_summary_FCLR007.md`, `research_state/liquidation_source_campaign.md`, `research_state/track_a_structural_block.md`, `research_state/negative_results_report.md`, `research_state/next_data_discovery_plan.md`, `research_state/track_c_consolidated_dossier.md`, `research_state/track_a_deadend_map.md`, `research_state/track_b_definitive_separation_audit.md`, `research_state/cross_track_decision_log.md`, `research_state/handoff_hardening_audit.md`, `AGENT_HANDOFF_OUTCOME.md`
3. Confirm sealed holds intact: no re-tuning, no holdout reuse, no workflow changes, no trading/paper-trading logic

#### STEP 2: HEAVY EVIDENCE DEFENSE CAMPAIGN (P0, REQUIRED — DO NOT STOP AFTER TESTS)
Execute ALL items below. Each must produce/refresh a durable artifact with concrete evidence. This is a defense/fortification campaign - you MUST NOT avoid heavy work.

**Campaign items (in strict priority order):**

1. **Track C Fortification (heavy):** Re-audit all three runs for traceability. Verify block structure, paired instruments, QLIKE deltas, CI coverage, and byte-identical repro hashes. Strengthen `research_state/track_c_consolidated_dossier.md` with explicit "why NOT_SUPPORTED" per run and cross-run invariants. Leave no ambiguity.
2. **Track A Admissibility Firewall (heavy):** Harden `research_state/track_a_deadend_map.md` with a machine-checkable GO/NO-GO rubric applied to every probed candidate (unauthenticated, >=5 symbols, >=3 non-overlapping 30-day blocks, completeness documented, license OK). Explicitly list what would count as NEW admissible data and why current candidates fail. Cross-link to `next_data_discovery_plan.md`.
3. **Track B Separation Hardening (heavy):** Prove track separation with concrete references (file paths, configs, evaluation code paths). Re-verify Holm corrections on all 16 cells in `track_b_definitive_separation_audit.md`. Document guardrails that prevent cross-track conflation.
4. **Cross-Track Decision Firewall (heavy):** Update `research_state/cross_track_decision_log.md` with an immutable decision matrix (H001-H004) showing gates, outcomes, blockers. State risk-overlay ineligibility unequivocally and exact conditions for reopening.
5. **Handoff & Bottleneck Elimination Audit (heavy):** Refresh `research_state/handoff_hardening_audit.md` to prove next agent cannot avoid heavy work - verify all artifacts exist, tests runnable, constraints explicit, no status-check shortcuts possible. Ensure AGENT_HANDOFF.md is the single source of truth with no ambiguity.

### HARD CONSTRAINTS (NEVER VIOLATE)
- **No credentials/manual inputs/paid data.** No workflow changes without explicit maintainer auth. No trading/paper-trading.
- **Track separation strict:** A observed, B modeled, C volatility. Never conflate modeled breaches with observed liquidations.
- **Preserve negatives/inconclusives.** No fabricated data/labels. No zero-fill of missing values.
- **Pre-registration mandatory** for any Track A GO experiment. **NO outcome inspection before pre-registration.**
- **No re-tuning on sealed holdouts. No threshold shopping. No unregistered feature/grid expansion.**

### SUCCESS CRITERIA
- [ ] All 14 tests pass
- [ ] All five defense artifacts refreshed with concrete evidence and cross-links
- [ ] Track C fortification leaves no doubt about NOT_SUPPORTED across all runs
- [ ] Track A firewall makes admissibility test unambiguous; dead-ends fully enumerated
- [ ] Track B separation guards documented and verified
- [ ] Cross-track decision firewall is decision-grade and immutable
- [ ] Handoff hardening proves heavy work is unavoidable
- [ ] Update `AGENT_HANDOFF_OUTCOME.md` with timestamp, HEAD, evidence summary

**STRUCTURAL CLOSURE CONFIRMED. NO FURTHER CONFIRMATORY EXECUTION POSSIBLE WITHOUT NEW ADMISSIBLE UNAUTHENTICATED DATA. FUTURE AGENTS MUST PRODUCE HEAVY AUDITABLE EVIDENCE, NOT STATUS CHECKS.**
