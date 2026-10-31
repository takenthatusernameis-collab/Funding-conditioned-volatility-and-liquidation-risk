# AGENT HANDOFF — SINGLE DURABLE HANDOFF (PRIORITIZED BY REPO NAME)

UPDATED: 2026-10-31T10:16:49Z
HEAD: 0ab2231d
REPO: Funding-conditioned-volatility-and-liquidation-risk
PRIORITY_SOURCE: Repository name inference (funding-conditioned volatility and liquidation risk)
PRIORITY_ORDER: Track C (funding-conditioned volatility forecasting) > Track A (observed liquidations) > Track B (modeled boundary breaches)
DURABLE_HANDOFF: SINGLE_SOURCE_OF_TRUTH
SESSION_GOAL: HEAVY_EVIDENCE_SYNTHESIS_CAMPAIGN — NO SHORTCUTS. FORCE AUDITABLE HEAVY WORK. MAXIMIZE DEFENSIBLE EVIDENCE.
BOTTLE_NECK_REMOVAL: MANDATORY — Remove any structural/efficiency blockers so significant progress continues. No status-only work.
STRICT_SEPARATION: Track A (observed), Track B (modeled/synthetic), Track C (volatility forecasting) — NEVER conflate.

## INITIAL TASK MESSAGE FOR THE NEXT AGENTIC WORK SESSION (COPY AND EXECUTE THIS VERBATIM)

**TASK_ID:** `HND-20261031-101552-FORCE-HEAVY-SYNTHESIS-CAMPAIGN`
**PRIORITY:** P0
**TIMESTAMP:** 2026-10-31T10:15:52Z
**MODE:** FORCED HEAVY WORK — EXPLICIT DIRECTIONS ABSENT; BUILD NEXT FOCUS CAMPAIGN SO FUTURE AGENTS CANNOT AVOID HEAVY WORK
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**MANDATE:** Leave the most relevant inferred timestamped clear initial task message for the next agentic work session in the single durable handoff. Prioritize strictly by repo name: Track C (funding-conditioned volatility forecasting) FIRST, then Track A (observed liquidations), then Track B (modeled boundary breaches). If sessions are blocked/inefficient, remove bottlenecks so significant progress continues. Status-only work is FORBIDDEN. Every iteration must produce measurable research/data/testing/engineering progress.

You are continuing from this SINGLE DURABLE handoff. **Prioritize strictly by repo name: Track C FIRST, then Track A, then Track B.**

### CURRENT KNOWN STATE (VERIFY, DO NOT TRUST BLINDLY)
- Tests: `python -m unittest discover -s tests -v` → **21/21 PASS** (must remain green). Verify at start and end.
- HEAD: 4c882a4f (main). Working tree clean except untracked `scripts/__pycache__/`, `tests/__pycache__/`.
- Track C (H001): **CLOSED_NEGATIVE / NOT_SUPPORTED**. FCLR-003 C2 vs B1 -3.78% (CI crosses zero), FCLR-006 -69.90% worse, FCLR-007 -3.42% worse (CI positive). Risk overlay INELIGIBLE. No reopen path without pre-registration/holdout discipline violation.
- Track A (H004): **STRUCTURALLY BLOCKED**. Machine-checkable firewall applied to all admissible unauthenticated sources - no source passes rubric (>=5 symbols, >=3 non-overlapping 30-day blocks, documented completeness, license OK, census). Sole reopen: NEW admissible unauthenticated source per RESEARCH_PROMPT.md §16 with evidence requirements.
- Track B (H003): **CLOSED_NEGATIVE**. FCLR-H003-EXT-001 no robust incremental skill after Holm correction across 16 cells. Strict separation enforced.
- Confirmatory program CLOSED. Forecast gate NOT_MET on all tested panels.

### BOTTLENECK REMOVAL MANDATE (RE-VERIFY AND HARDEN)
Identify and remove/irrefutably document any remaining blockers:
1. **Data access**: Track A firewall already applied; if any new candidate appears, test with machine-checkable GO/NO-GO immediately.
2. **Compute/analysis**: Use cached data in `research_state/data_cache/` and repo zips; restartable incremental work; never recompute sealed confirmatory results.
3. **Evidence**: Every claim needs provenance, hashes/splits, tests, file:line references. Gaps MUST be filled with heavy evidence work, not status.
4. **Handoff**: This file is SINGLE source of truth. Next agent must be unable to do status-only work.

### FORCED HEAVY EVIDENCE CAMPAIGN (EXECUTE ALL - CANNOT SKIP)

#### STEP 1: INTEGRITY CHECK (P0, ~2-5 min)
1. `python -m unittest discover -s tests -v` → MUST be 21/21 PASS. Record timestamp.
2. Verify cross-linked artifacts exist and consistent:
   - `research_state/hypothesis_registry.json`, `research_state/experiment_frontier.json`
   - `research_state/track_c_consolidated_dossier.md`, `research_state/track_c_final_synthesis_dossier.md`
   - `research_state/track_a_deadend_map.md`, `research_state/track_a_final_block_proof.md` (create if missing)
   - `research_state/track_b_definitive_separation_audit.md`, `research_state/track_b_separation_proof_hardened.md` (create/update)
   - `research_state/cross_track_decision_log.md`, `research_state/cross_track_decision_firewall.md`
   - `research_state/handoff_hardening_audit.md`
   - `research_state/negative_results_report.md`, `research_state/next_data_discovery_plan.md`
   - `research_state/final_confirmatory_verdict.md`, `research_state/structural_closure_verdict_heavy.md`
   - `research_state/AGENT_HANDOFF_OUTCOME.md`
3. Log integrity check in `research_state/AGENT_HANDOFF_OUTCOME.md`.

#### STEP 2: EVIDENCE SYNTHESIS BY PRIORITY (P0 - HEAVY WORK)
**PRIORITIZE Track C → Track A → Track B**

**2A. TRACK C — FUNDING-CONDITIONED VOLATILITY FORECASTING (HIGHEST PRIORITY)**
Strengthen/synthesize a single **SYNTHESIS DOSSIER** (`research_state/track_c_final_synthesis_dossier.md`) with exact frozen splits/embargoes/blocks/paired n per FCLR-003/006/007, full QLIKE decomposition (B0/B1/C1/C2), C2 vs B1 means + 95% block-bootstrap CIs with exact numbers, leakage audit, robustness notes, gate assessment. Explicit conclusion: NOT_SUPPORTED, risk overlay INELIGIBLE, no valid reopen path. Every number must trace to existing artifacts (file:line/manifest keys). NO recomputation of sealed holdouts.

**2B. TRACK A — OBSERVED LIQUIDATIONS (SECOND - REMOVE BOTTLENECKS)**
Harden into **MACHINE-CHECKABLE FINAL BLOCK** (`research_state/track_a_final_block_proof.md`): consolidate ALL candidates from enumeration/deep sweeps/maps; per-candidate URL/endpoint/auth/HTTP/status/timestamps/ranges/symbol coverage/block counts/completeness/license/GO-NO-GO with rubric; prove no candidate passes ALL rubric items with concrete evidence; document rubric verbatim (`unauthenticated==true AND no_keys==true AND symbols>=5 AND blocks>=3 AND completeness_doc==true AND license_ok==true AND census_or_defensible==true`); state sole reopen condition from RESEARCH_PROMPT.md §16 + evidence requirements. If any candidate appears to pass on re-check, FREEZE protocol and pre-register BEFORE outcome inspection.

**2C. TRACK B — MODELED BOUNDARY BREACHES (THIRD - PROVE SEPARATION)**
Strengthen separation proof (`research_state/track_b_separation_proof_hardened.md`): code-path trace grepping for Track A liquidation label usage in Track B paths with file paths/line ranges; prove firewall/log enforcement; summarize FCLR-H003-EXT-001 with Holm correction; explicitly state NEVER conflated with observed liquidations.

#### STEP 3: INTEGRATION, HARDENING & FINALIZE HANDOFF (P0)
1. Update `research_state/AGENT_HANDOFF_OUTCOME.md` with timestamp, HEAD, all artifacts created/modified, commands run, concrete numbers, test results.
2. Update `research_state/handoff_hardening_audit.md` proving bottlenecks removed/irrefutable and next agent CANNOT avoid heavy work.
3. Update `research_state/cross_track_decision_log.md` with synthesis findings.
4. Cross-link all new artifacts; ensure handoff remains single source of truth.
5. Run `python -m unittest discover -s tests -v` → MUST PASS (21/21). Record final timestamp.

### HARD CONSTRAINTS (NEVER VIOLATE)
- No credentials/manual inputs/paid data. No `.github/workflows` changes without explicit maintainer auth. No trading/paper-trading/live orders.
- Strict track separation. Never conflate Track B (modeled) with Track A (observed).
- Preserve negatives/inconclusives. No fabricated data/labels. No zero-fill of missing values.
- Pre-registration REQUIRED for any new experiment. NO outcome inspection before pre-registration.
- No re-tuning on sealed holdouts. No threshold shopping.
- No re-running completed confirmatory experiments (FCLR-002/003/006/007/H003-EXT). No relaxing gates.
- Every iteration must create measurable research/data/testing/engineering progress. Status-only checks are FORBIDDEN.

### SUCCESS CRITERIA
- [ ] All tests pass (21/21), timestamp + HEAD recorded
- [ ] `research_state/track_c_final_synthesis_dossier.md` strengthened with full traceable numbers
- [ ] `research_state/track_a_final_block_proof.md` created/updated with machine-checkable rubric + evidence for ALL candidates
- [ ] `research_state/track_b_separation_proof_hardened.md` created/updated with code-path trace
- [ ] `research_state/AGENT_HANDOFF_OUTCOME.md` updated with full evidence
- [ ] `research_state/handoff_hardening_audit.md` proves heavy work unavoidable
- [ ] `research_state/cross_track_decision_log.md` updated
- [ ] All artifacts cross-linked; this handoff remains single source of truth

**FORCED HEAVY SYNTHESIS CAMPAIGN. NO SHORTCUTS. BUILD EVIDENCE, NOT STATUS. PRIORITIZE BY REPO NAME.**
