# AGENT HANDOFF — SINGLE DURABLE HANDOFF (PRIORITIZED BY REPO NAME)

UPDATED: 2026-10-31T17:20:00Z
HEAD: a1241997 (main). Working tree clean.
REPO: Funding-conditioned-volatility-and-liquidation-risk
PRIORITY_SOURCE: Repository name inference (funding-conditioned volatility and liquidation risk) — **FUNDING-CONDITIONED VOLATILITY FIRST**
PRIORITY_ORDER: Track C (Funding-conditioned volatility forecasting) > Track A (Observed liquidations) > Track B (Modeled boundary breaches) > H002 (Funding-extreme correction time, exploratory-only)
DURABLE_HANDOFF: SINGLE_SOURCE_OF_TRUTH
SESSION_GOAL: FORCED_HEAVY_EVIDENCE_CAMPAIGN — NO STATUS-ONLY PATH. EVERY ITERATION MUST PRODUCE MEASURABLE ARTIFACTS. REMOVE ALL BOTTLENECKS. MAKE FUTURE AGENTS UNABLE TO AVOID HEAVY WORK.
BOTTLE_NECK_REMOVAL: MANDATORY — Eliminate structural inefficiencies so significant progress continues.

HEAD_NOTE: HEAD verified at a1241997. Verify HEAD at start. Tests: 27/27 PASS.

## INITIAL TASK MESSAGE FOR THE NEXT AGENTIC WORK SESSION (COPY AND EXECUTE THIS VERBATIM)

## NO ESCAPE CLAUSE (NON-NEGOTIABLE)
- **NO STATUS REPORTS**: "X is blocked/closed" without new concrete artifacts is not acceptable. Prove with files/lines/hashes.
- **NO LAZY SWEEPS**: Track A requires testing EVERY plausible candidate against the verbatim rubric with HTTP/auth/coverage evidence NOW.
- **NO REOPENING WITHOUT GATES**: Track C is sealed. Track B is closed negative with separation proven. Only NEW admissible data per RESEARCH_PROMPT §16 can reopen anything.
- **HEAVY OR NOTHING**: If your turn produces only reading logs/status without creating/modifying research_state artifacts with provenance, you have failed this mandate.
- **FORCE MULTIPLICATION**: Every artifact you create must enable the next agent to do more heavy work, not less.
- **REPO-NAME DRIVEN**: Funding-conditioned volatility (Track C) comes FIRST because the repo says so. Execute in that order regardless of curiosity.



**TASK_ID:** `HND-20261031-172000-FORCED_HEAVY_EVIDENCE_SYNTHESIS-V13`
**PRIORITY:** P0
**TIMESTAMP:** 2026-10-31T17:20:00Z
**MODE:** FORCED HEAVY WORK — INFERRED FROM REPO NAME. BUILD THE NEXT FOCUS CAMPAIGN SO FUTURE AGENTS CANNOT AVOID HEAVY WORK.
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**MANDATE:** SINGLE DURABLE HANDOFF. Prioritize strictly by repo name: **Track C → Track A → Track B → H002**. Remove bottlenecks. Status-only work FORBIDDEN. Every action must yield concrete artifacts with provenance (file paths, line ranges, hashes/manifests, timestamps, HEAD). No re-tuning on sealed holdouts.

You are continuing from this SINGLE DURABLE handoff. **Prioritize strictly by repo name: Track C → Track A → Track B → H002.**

### CURRENT VERIFIED STATE (VERIFY AT START - DO NOT TRUST BLINDLY)
- Tests: `python -m unittest discover -s tests -v` → **27/27 PASS** (must remain green). Verify at start and end.
- HEAD: `a1241997` (main). Working tree clean.
- Track C (H001, funding-conditioned volatility): **NOT_SUPPORTED — CONFIRMATORY CLOSED**. FCLR-003 C2 vs B1 +0.015205 QLIKE, 95% CI [-0.020240, 0.056734] crosses zero (-3.78% worse). FCLR-006/FCLR-007 worse in 2026 windows. Risk overlay INELIGIBLE per RESEARCH_PROMPT §9. Full synthesis in `research_state/track_c_final_synthesis_dossier.md`. **DO NOT REOPEN** without pre-registration + documented holdout discipline violations with evidence.
- Track A (H004, observed liquidations): **STRUCTURALLY BLOCKED**. Machine-checkable rubric applied to ALL enumerated candidates — no source passes ALL items (unauthenticated, >=5 symbols, >=3 non-overlapping 30-day blocks, documented completeness, license OK, census/defensible). Sole reopen: NEW admissible unauthenticated source per RESEARCH_PROMPT.md §16 with concrete evidence. Proof in `research_state/track_a_final_block_proof.md` and `research_state/track_a_deadend_map.md`.
- Track B (H003, modeled boundary breaches): **CLOSED_NEGATIVE**. FCLR-H003-EXT-001: no robust incremental skill after Holm correction across 16 cells. Strict separation from Track A proven. Proof in `research_state/track_b_separation_proof_hardened.md` / `research_state/track_b_definitive_separation_audit.md`.
- H002 (funding-extreme correction time): **EXPLORATORY/PARTIAL** (88 events, 84 corrected, 4 censored). Do not promote to volatility skill/boundary breaches/observed liquidations. Remaining open track — may advance to confirmatory ONLY via new pre-registration (RESEARCH_PROMPT §16).

### BOTTLENECK REMOVAL MANDATE
1. **Traceability bottleneck (Track C)**: The "closed" status must be **irrefutably traceable**. Build/update `research_state/track_c_traceability_matrix.md` with full decomposition (B0/B1/C1/C2), paired n, blocks, CIs, leakage audit with file:line + artifact references.
2. **Data access bottleneck (Track A)**: The firewall is machine-checkable. Conduct an ACTIVE, evidence-backed sweep of ALL plausible candidates. For EVERY candidate, test against verbatim rubric immediately with concrete HTTP/coverage/auth/census evidence. Eliminate status-only loops — produce pass/fail tables or strengthen irrefutable proof. Update `research_state/track_a_rubric_enforcement_matrix.md` and `research_state/track_a_deadend_map.md`.
3. **Separation bottleneck (Track B)**: Enforce and prove strict separation. Trace every code path using `liquidat*` against Track A boundaries. Surface any mixing with file:line evidence. Lock separation with `research_state/track_b_codepath_separation_matrix.md`.
4. **Handoff integrity bottleneck**: This file is SINGLE source of truth. Next agent MUST be unable to take a status-only path. Force heavy evidence work at every step.
5. **Head staleness bottleneck**: Keep internal HEAD references consistent with actual HEAD. No stale commit references.

### FORCED HEAVY EVIDENCE CAMPAIGN (EXECUTE ALL - CANNOT SKIP)

#### STEP 1: INTEGRITY CHECK (P0)
1. `python -m unittest discover -s tests -v` → MUST be 27/27 PASS. Record timestamp, HEAD (`a1241997`), and full summary in `research_state/AGENT_HANDOFF_OUTCOME.md`.
2. Confirm HEAD `a1241997` and working tree state.
3. Verify critical artifacts exist and cross-linked.

#### STEP 2: EVIDENCE SYNTHESIS BY PRIORITY (P0 - HEAVY WORK)

**2A. TRACK C (PRIORITY 1)**: Harden traceability. Update/build `research_state/track_c_traceability_matrix.md` with frozen splits/embargoes/blocks/paired n, QLIKE decomposition, C2 vs B1 ΔQLIKE + 95% CI (-3.78% worse/crossing zero), leakage audit with file:line references.

**2B. TRACK A (PRIORITY 2)**: ACTIVE evidence-backed sweep. Update/build `research_state/track_a_rubric_enforcement_matrix.md` with verbatim rubric: `unauthenticated==true AND no_keys==true AND symbols>=5 AND blocks>=3 AND completeness_doc==true AND license_ok==true AND census_or_defensible==true`. For each candidate (existing + newly discovered), record concrete evidence (HTTP status/headers, auth model, coverage dates/symbols, block structure, docs, license, census). If none pass, strengthen irrefutable proof and update `research_state/track_a_deadend_map.md`.

**2C. TRACK B (PRIORITY 3)**: Harden separation. Update/build `research_state/track_b_codepath_separation_matrix.md` tracing ALL `liquidat*` usage, firewall enforcement, mapping to Track A vs Track B with grep evidence (file:line). Include Holm-corrected FCLR-H003-EXT-001 summary.

**2D. H002 (PRIORITY 4)**: Do NOT inspect outcomes blindly. If concrete path to confirmatory per RESEARCH_PROMPT §16 exists, **PRE-REGISTER FIRST** in `research_state/h002_pre_registration.md` before any outcome inspection. Else document ruling out with evidence.

#### STEP 3: INTEGRATION, HARDENING & FINALIZE HANDOFF (P0)
1. Update `research_state/AGENT_HANDOFF_OUTCOME.md` with timestamp, HEAD (`a1241997`), artifacts modified, commands executed, concrete numbers, tests (27/27), and BOTTLENECKS REMOVED WITH EVIDENCE.
2. Update `research_state/handoff_hardening_audit.md` proving bottlenecks removed and heavy work unavoidable.
3. Update `research_state/cross_track_decision_log.md` with C→A→B→H002 synthesis and concrete decisions.
4. Cross-link all artifacts; ensure single source of truth.
5. Run `python -m unittest discover -s tests -v` → MUST PASS (27/27). Record final verification.

### HARD CONSTRAINTS (NEVER VIOLATE)
- No credentials/manual inputs/paid data. No `.github/workflows` changes without explicit maintainer auth. No trading/paper-trading/live orders.
- Strict track separation. Never conflate Track B (modeled) with Track A (observed).
- Preserve negatives/inconclusives. No fabricated data/labels. No zero-fill of missing values.
- Pre-registration REQUIRED for any new experiment. **NO outcome inspection before pre-registration.**
- No re-tuning on sealed holdouts. No threshold shopping.
- No re-running completed confirmatory experiments. No relaxing gates.
- Every iteration must create measurable research/data/testing/engineering progress. Status-only checks are FORBIDDEN.
- Evidence over assertion: every claim needs provenance/hashes/splits/tests/file:line.
- Use only data/software accessible automatically without payment/signup/keys/manual downloads.

### SUCCESS CRITERIA
- [ ] All tests pass (27/27), timestamp + HEAD (`a1241997`) recorded in `research_state/AGENT_HANDOFF_OUTCOME.md`
- [ ] Track C hardened with `track_c_traceability_matrix.md`
- [ ] Track A hardened with `track_a_rubric_enforcement_matrix.md` + active sweep evidence + all candidates in `track_a_deadend_map.md`
- [ ] Track B hardened with `track_b_codepath_separation_matrix.md` + grep evidence
- [ ] H002 handled correctly (pre-registered BEFORE outcome inspection OR ruled out with evidence)
- [ ] `research_state/AGENT_HANDOFF_OUTCOME.md`, `research_state/handoff_hardening_audit.md`, `research_state/cross_track_decision_log.md` updated
- [ ] All artifacts cross-linked; handoff remains single source of truth
- [ ] HEAD references consistent with `a1241997`

**FORCED HEAVY SYNTHESIS CAMPAIGN — PRIORITIZED BY REPO NAME (FUNDING-CONDITIONED VOLATILITY → LIQUIDATION RISK). NO SHORTCUTS. BUILD EVIDENCE, NOT STATUS. REMOVE BOTTLENECKS. MAKE IT IMPOSSIBLE TO AVOID HEAVY WORK.**
