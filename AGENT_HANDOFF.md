# AGENT HANDOFF — SINGLE DURABLE HANDOFF (PRIORITIZED BY REPO NAME)

UPDATED: 2026-10-31T11:26:38Z
HEAD: 23d97f3b (main). Working tree clean except untracked `scripts/__pycache__/`, `tests/__pycache__/`.</arg_value>
REPO: Funding-conditioned-volatility-and-liquidation-risk
PRIORITY_SOURCE: Repository name inference (funding-conditioned volatility and liquidation risk)
PRIORITY_ORDER: Track C (funding-conditioned volatility forecasting) > Track A (observed liquidations) > Track B (modeled boundary breaches)
DURABLE_HANDOFF: SINGLE_SOURCE_OF_TRUTH
SESSION_GOAL: FINAL_EVIDENCE_SYNTHESIS_AND_HANDOFF_HARDENING — ALL CONFIRMATORY CAMPAIGNS CLOSED. REMOVE STALE BOTTLENECKS. FORCE HEAVY EVIDENCE WORK.
BOTTLE_NECK_REMOVAL: MANDATORY — Eliminate structural/efficiency blockers so significant progress continues. Status-only work is FORBIDDEN.
STRICT_SEPARATION: Track A (observed), Track B (modeled/synthetic), Track C (volatility forecasting) — NEVER conflate.

## INITIAL TASK MESSAGE FOR THE NEXT AGENTIC WORK SESSION (COPY AND EXECUTE THIS VERBATIM)

**TASK_ID:** `HND-20261031-112409-FINAL_EVIDENCE_SYNTHESIS_HEAVY`
**PRIORITY:** P0
**TIMESTAMP:** 2026-10-31T11:26:38Z
**MODE:** FORCED HEAVY WORK — EXPLICIT DIRECTIONS ABSENT; BUILD NEXT FOCUS CAMPAIGN SO FUTURE AGENTS CANNOT AVOID HEAVY WORK
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**MANDATE:** Leave the most relevant inferred timestamped clear initial task message for the next agentic work session in the single durable handoff (`AGENT_HANDOFF.md`). Prioritize strictly by repo name: Track C FIRST, then Track A, then Track B. Remove bottlenecks. Status-only work is FORBIDDEN. Every iteration must produce measurable research/data/testing/engineering progress.

You are continuing from this SINGLE DURABLE handoff. **Prioritize strictly by repo name: Track C → Track A → Track B.**

### CURRENT VERIFIED STATE (DO NOT TRUST BLINDLY — VERIFY)
- Tests: `python -m unittest discover -s tests -v` → **27/27 PASS** (must remain green). Verify at start and end.
- HEAD: `23d97f3b` (main). Working tree clean except untracked `scripts/__pycache__/`, `tests/__pycache__/`.</arg_value>
- Track C (H001): **NOT_SUPPORTED — CONFIRMATORY CLOSED**. FCLR-003 C2 vs B1 +0.015205 QLIKE, 95% CI [-0.020240, 0.056734] crosses zero (-3.78% worse). FCLR-006/FCLR-007 worse in 2026 windows. Risk overlay INELIGIBLE per RESEARCH_PROMPT §9. Full synthesis in `research_state/track_c_final_synthesis_dossier.md`. No reopen without pre-registration + holdout discipline violations.
- Track A (H004): **STRUCTURALLY BLOCKED**. Machine-checkable rubric applied to ALL enumerated candidates — no source passes ALL items (unauthenticated, >=5 symbols, >=3 non-overlapping 30-day blocks, documented completeness, license OK, census/defensible). Sole reopen: NEW admissible unauthenticated source per RESEARCH_PROMPT.md §16 with concrete evidence. Proof in `research_state/track_a_final_block_proof.md` and `research_state/track_a_deadend_map.md`.
- Track B (H003): **CLOSED_NEGATIVE**. FCLR-H003-EXT-001: no robust incremental skill after Holm correction across 16 cells. Strict separation from Track A proven. Proof in `research_state/track_b_separation_proof_hardened.md` / `research_state/track_b_definitive_separation_audit.md`.
- H002-correction: exploratory/partial (88 events, 84 corrected, 4 censored). Do not promote to volatility skill/boundary breaches/observed liquidations.
- Confirmatory program CLOSED on all panels. Data exhaustion on existing admissible sets. No new confirmatory feasible without new admissible data source.

### BOTTLENECK REMOVAL MANDATE
1. **Data access**: Track A firewall is machine-checkable — if any new candidate appears, test against rubric IMMEDIATELY with evidence.
2. **Compute/analysis**: Use cached data in `research_state/data_cache/`. Never recompute sealed confirmatory results.
3. **Evidence**: Every claim needs provenance/hashes/splits/tests/file:line. Fill gaps with heavy evidence work, not status.
4. **Handoff**: This file is SINGLE source of truth. Next agent must be unable to do status-only work.

### FORCED HEAVY EVIDENCE CAMPAIGN (EXECUTE ALL - CANNOT SKIP)

#### STEP 1: INTEGRITY CHECK (P0, ~2-5 min)
1. `python -m unittest discover -s tests -v` → MUST be 27/27 PASS. Record timestamp + HEAD.
2. Confirm HEAD `be23c0cb` and working tree clean except `__pycache__/`.
3. Verify critical artifacts exist and are consistent:
   - `research_state/hypothesis_registry.json`, `research_state/experiment_frontier.json`
   - `research_state/track_c_final_synthesis_dossier.md`, `research_state/track_c_consolidated_dossier.md`
   - `research_state/track_a_final_block_proof.md`, `research_state/track_a_deadend_map.md`, `research_state/track_a_structural_block.md`
   - `research_state/track_b_separation_proof_hardened.md`, `research_state/track_b_definitive_separation_audit.md`
   - `research_state/cross_track_decision_log.md`, `research_state/cross_track_decision_firewall.md`
   - `research_state/handoff_hardening_audit.md`
   - `research_state/negative_results_report.md`, `research_state/next_data_discovery_plan.md`
   - `research_state/final_confirmatory_verdict.md`, `research_state/structural_closure_verdict_heavy.md`
   - `research_state/AGENT_HANDOFF_OUTCOME.md` (root and/or research_state as applicable)
4. Log integrity check in `research_state/AGENT_HANDOFF_OUTCOME.md` with timestamp.

#### STEP 2: EVIDENCE SYNTHESIS BY PRIORITY (P0 - HEAVY WORK)

**2A. TRACK C — HIGHEST PRIORITY (Funding-conditioned volatility forecasting)**
Harden `research_state/track_c_final_synthesis_dossier.md` to be irrefutable:
- Exact frozen splits/embargoes/blocks/paired n for FCLR-003/006/007 with manifest references
- Full QLIKE decomposition (B0/B1/C1/C2) with traceable numbers
- Primary contrast C2 vs B1: mean diff + 95% block-bootstrap CI with exact values; state crosses zero / worse
- Leakage audit, block structure verification, robustness notes
- Explicit: NOT_SUPPORTED, risk overlay INELIGIBLE, no valid reopen path under constraints
- Every number must trace to `evaluation_summary_*.md`, manifests, run metadata

**2B. TRACK A — SECOND PRIORITY (Observed liquidations) - REMOVE BOTTLENECKS**
Strengthen `research_state/track_a_final_block_proof.md`:
- Consolidate ALL candidates from enumeration/deep sweeps/campaigns
- Per-candidate: URL/endpoint/auth/HTTP/status/timestamps/ranges/symbols/blocks/completeness/license/rubric pass/fail with concrete evidence
- Rubric verbatim: `unauthenticated==true AND no_keys==true AND symbols>=5 AND blocks>=3 AND completeness_doc==true AND license_ok==true AND census_or_defensible==true` — ALL must pass
- Prove no candidate passes ALL items
- State sole reopen: NEW admissible unauthenticated source per §16 with evidence requirements
- If any candidate appears plausible on re-check: FREEZE, pre-register BEFORE outcome inspection, apply rubric strictly

**2C. TRACK B — THIRD PRIORITY (Modeled boundary breaches) - PROVE SEPARATION**
Harden `research_state/track_b_separation_proof_hardened.md`:
- Grep/code-path trace: Track A liquidation label usage in Track B paths (file paths/line ranges)
- Firewall/log enforcement evidence
- FCLR-H003-EXT-001 summary with Holm correction across 16 cells
- Explicit: NEVER conflated with observed liquidations; closed negative

#### STEP 3: INTEGRATION, HARDENING & FINALIZE HANDOFF (P0)
1. Update `research_state/AGENT_HANDOFF_OUTCOME.md` with timestamp, HEAD, artifacts created/modified, commands run, concrete numbers, test results (27/27).
2. Update `research_state/handoff_hardening_audit.md` proving bottlenecks removed/irrefutable and next agent CANNOT avoid heavy work.
3. Update `research_state/cross_track_decision_log.md` with synthesis findings and decisions.
4. Cross-link all artifacts; ensure this handoff remains SINGLE source of truth.
5. Run `python -m unittest discover -s tests -v` → MUST PASS (27/27). Record final timestamp.

### HARD CONSTRAINTS (NEVER VIOLATE)
- No credentials/manual inputs/paid data. No `.github/workflows` changes without explicit maintainer auth. No trading/paper-trading/live orders.
- Strict track separation. Never conflate Track B (modeled) with Track A (observed).
- Preserve negatives/inconclusives. No fabricated data/labels. No zero-fill of missing values.
- Pre-registration REQUIRED for any new experiment. NO outcome inspection before pre-registration.
- No re-tuning on sealed holdouts. No threshold shopping.
- No re-running completed confirmatory experiments (FCLR-002/003/006/007/H003-EXT). No relaxing gates.
- Every iteration must create measurable research/data/testing/engineering progress. Status-only checks are FORBIDDEN.

### SUCCESS CRITERIA
- [ ] All tests pass (27/27), timestamp + HEAD recorded
- [ ] `research_state/track_c_final_synthesis_dossier.md` strengthened with full traceable numbers
- [ ] `research_state/track_a_final_block_proof.md` hardened with machine-checkable rubric + evidence for ALL candidates
- [ ] `research_state/track_b_separation_proof_hardened.md` hardened with code-path trace
- [ ] `research_state/AGENT_HANDOFF_OUTCOME.md` updated with full evidence
- [ ] `research_state/handoff_hardening_audit.md` proves heavy work unavoidable
- [ ] `research_state/cross_track_decision_log.md` updated
- [ ] All artifacts cross-linked; this handoff remains single source of truth

**FORCED HEAVY SYNTHESIS CAMPAIGN. NO SHORTCUTS. BUILD EVIDENCE, NOT STATUS. PRIORITIZE BY REPO NAME (C → A → B).**
