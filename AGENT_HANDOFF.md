# AGENT HANDOFF — SINGLE DURABLE HANDOFF (PRIORITIZED BY REPO NAME)

UPDATED: 2026-10-31T15:17:39Z
HEAD: 7385221a (main). Working tree clean except untracked `scripts/__pycache__/`, `tests/__pycache__/`.
REPO: Funding-conditioned-volatility-and-liquidation-risk
PRIORITY_SOURCE: Repository name inference (funding-conditioned volatility and liquidation risk) — **FUNDING-CONDITIONED VOLATILITY FIRST**
PRIORITY_ORDER: Track C (Funding-conditioned volatility forecasting) > Track A (Observed liquidations) > Track B (Modeled boundary breaches) > H002 (Funding-extreme correction time, exploratory-only)
DURABLE_HANDOFF: SINGLE_SOURCE_OF_TRUTH
SESSION_GOAL: FORCED_HEAVY_EVIDENCE_CAMPAIGN — NO STATUS-ONLY PATH. EVERY ITERATION MUST PRODUCE MEASURABLE ARTIFACTS. REMOVE ALL BOTTLENECKS. MAKE FUTURE AGENTS UNABLE TO AVOID HEAVY WORK.
BOTTLE_NECK_REMOVAL: MANDATORY — Eliminate structural inefficiencies so significant progress continues.

## INITIAL TASK MESSAGE FOR THE NEXT AGENTIC WORK SESSION (COPY AND EXECUTE THIS VERBATIM)

**TASK_ID:** `HND-20261031-151739-FORCED_HEAVY_EVIDENCE_SYNTHESIS-V3`
**PRIORITY:** P0
**TIMESTAMP:** 2026-10-31T15:17:39Z
**MODE:** FORCED HEAVY WORK — INFERRED FROM REPO NAME. BUILD THE NEXT FOCUS CAMPAIGN SO FUTURE AGENTS CANNOT AVOID HEAVY WORK.
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**MANDATE:** SINGLE DURABLE HANDOFF. Prioritize strictly by repo name: **Track C → Track A → Track B → H002**. Remove bottlenecks. Status-only work FORBIDDEN. Every action must yield concrete artifacts with provenance (file paths, line ranges, hashes/manifests, timestamps, HEAD). No re-tuning on sealed holdouts.

You are continuing from this SINGLE DURABLE handoff. **Prioritize strictly by repo name: Track C → Track A → Track B → H002.**

### CURRENT VERIFIED STATE (VERIFY AT START - DO NOT TRUST BLINDLY)
- Tests: `python -m unittest discover -s tests -v` → **27/27 PASS** (must remain green). Verify at start and end.
- HEAD: `7385221a` (main). Working tree clean except untracked `__pycache__/`.
- Track C (H001, funding-conditioned volatility): **NOT_SUPPORTED — CONFIRMATORY CLOSED**. FCLR-003 C2 vs B1 +0.015205 QLIKE, 95% CI [-0.020240, 0.056734] crosses zero (-3.78% worse). FCLR-006/FCLR-007 worse in 2026 windows. Risk overlay INELIGIBLE per RESEARCH_PROMPT §9. Full synthesis in `research_state/track_c_final_synthesis_dossier.md`. **DO NOT REOPEN** without pre-registration + documented holdout discipline violations with evidence.
- Track A (H004, observed liquidations): **STRUCTURALLY BLOCKED**. Machine-checkable rubric applied to ALL enumerated candidates — no source passes ALL items (unauthenticated, >=5 symbols, >=3 non-overlapping 30-day blocks, documented completeness, license OK, census/defensible). Sole reopen: NEW admissible unauthenticated source per RESEARCH_PROMPT.md §16 with concrete evidence. Proof in `research_state/track_a_final_block_proof.md` and `research_state/track_a_deadend_map.md`.
- Track B (H003, modeled boundary breaches): **CLOSED_NEGATIVE**. FCLR-H003-EXT-001: no robust incremental skill after Holm correction across 16 cells. Strict separation from Track A proven. Proof in `research_state/track_b_separation_proof_hardened.md` / `research_state/track_b_definitive_separation_audit.md`.
- H002 (funding-extreme correction time): **EXPLORATORY/PARTIAL** (88 events, 84 corrected, 4 censored). Do not promote to volatility skill/boundary breaches/observed liquidations. Remaining open track — may advance to confirmatory ONLY via new pre-registration (RESEARCH_PROMPT §16).

### BOTTLENECK REMOVAL MANDATE
1. **Traceability bottleneck (Track C)**: The "closed" status must be **irrefutably traceable**. Eliminate any ambiguity by building a complete decomposition matrix with file:line references to every number that justifies closure.
2. **Data access bottleneck (Track A)**: The firewall is machine-checkable. Conduct an ACTIVE, evidence-backed sweep of ALL plausible candidates. For EVERY candidate discovered, test against the rubric IMMEDIATELY with concrete HTTP/coverage/auth/census evidence. Eliminate "status check" loops — produce pass/fail tables or strengthen irrefutable proof.
3. **Separation bottleneck (Track B)**: Enforce and prove strict separation. Trace every code path using `liquidat*` against Track A boundaries. Surface any mixing with file:line evidence. Lock separation with concrete matrix.
4. **Handoff integrity bottleneck**: This file is SINGLE source of truth. Next agent MUST be unable to take a status-only path. Force heavy evidence work at every step.

### FORCED HEAVY EVIDENCE CAMPAIGN (EXECUTE ALL - CANNOT SKIP)

#### STEP 1: INTEGRITY CHECK (P0, ~2-5 min)
1. `python -m unittest discover -s tests -v` → MUST be 27/27 PASS. Record timestamp, HEAD (`7385221a`), and full summary in `research_state/AGENT_HANDOFF_OUTCOME.md`.
2. Confirm HEAD `7385221a` and working tree clean except `__pycache__/`.
3. Verify critical artifacts exist and are consistent (all listed artifacts must be present and cross-linked).
4. Log integrity check in `research_state/AGENT_HANDOFF_OUTCOME.md` with timestamp and HEAD.

#### STEP 2: EVIDENCE SYNTHESIS BY PRIORITY (P0 - HEAVY WORK)

**2A. TRACK C (PRIORITY 1 - FUNDING-CONDITIONED VOLATILITY)**: Harden traceability to the point of irrefutability. Build/update `research_state/track_c_traceability_matrix.md` with:
- Frozen splits/embargoes/blocks/paired n for all folds
- Full QLIKE decomposition (B0/B1/C1/C2) with exact values
- C2 vs B1 ΔQLIKE + 95% CI crossing zero (-3.78% worse) with block-aware CI details
- Leakage audit (timestamp, label, purge/embargo, normalization) with file:line references
- Every row must have file:line + artifact references (manifests, eval summaries, run manifests)

**2B. TRACK A (PRIORITY 2 - OBSERVED LIQUIDATIONS)**: Conduct ACTIVE evidence-backed sweep. Build/update `research_state/track_a_rubric_enforcement_matrix.md` with verbatim rubric: `unauthenticated==true AND no_keys==true AND symbols>=5 AND blocks>=3 AND completeness_doc==true AND license_ok==true AND census_or_defensible==true`. For each candidate (existing + newly discovered from web/archive scans), record concrete evidence (HTTP status/headers, auth model, coverage dates/symbols, block structure, docs, license, census). Test exhaustively with evidence. If any candidate plausibly meets criteria, test fully. If none do, strengthen irrefutable block proof with new evidence and update `research_state/track_a_deadend_map.md`. **ELIMINATE status-only checks.**

**2C. TRACK B (PRIORITY 3 - MODELED BOUNDARY BREACHES)**: Harden separation. Build/update `research_state/track_b_codepath_separation_matrix.md` tracing ALL `liquidat*` usage, firewall enforcement, and explicit mapping to Track A vs Track B. Include grep evidence with file:line. Include Holm-corrected FCLR-H003-EXT-001 summary with cell-level numbers and file:line references. Prove no mixing exists.

**2D. H002 (PRIORITY 4 - CORRECTION TIME)**: Do NOT inspect outcomes blindly. If there is ANY concrete path to advancing H002 to confirmatory per RESEARCH_PROMPT §16, **PRE-REGISTER FIRST** in `research_state/h002_pre_registration.md` (frozen event definition, censoring rules, eligible contracts, volatility split, uncertainty method, stopping rules, pre-registered comparisons) **BEFORE any outcome inspection**. If no concrete admissible path exists with evidence, document this with evidence and do not pre-register speculatively.

#### STEP 3: INTEGRATION, HARDENING & FINALIZE HANDOFF (P0)
1. Update `research_state/AGENT_HANDOFF_OUTCOME.md` with timestamp, HEAD (`7385221a`), artifacts modified, commands executed, concrete numbers, tests (27/27), and **BOTTLENECKS REMOVED WITH EVIDENCE**.
2. Update `research_state/handoff_hardening_audit.md` proving bottlenecks removed and heavy work unavoidable (explicitly show what would have been status-only and how it was forced into evidence work).
3. Update `research_state/cross_track_decision_log.md` with C→A→B→H002 synthesis and concrete decisions.
4. Cross-link all artifacts; ensure single source of truth.
5. Run `python -m unittest discover -s tests -v` → MUST PASS (27/27). Record final verification with timestamp.

### HARD CONSTRAINTS (NEVER VIOLATE)
- No credentials/manual inputs/paid data. No `.github/workflows` changes without explicit maintainer auth. No trading/paper-trading/live orders.
- Strict track separation. Never conflate Track B (modeled) with Track A (observed).
- Preserve negatives/inconclusives. No fabricated data/labels. No zero-fill of missing values.
- Pre-registration REQUIRED for any new experiment. **NO outcome inspection before pre-registration.**
- No re-tuning on sealed holdouts. No threshold shopping.
- No re-running completed confirmatory experiments (FCLR-002/003/006/007/H003-EXT). No relaxing gates.
- Every iteration must create measurable research/data/testing/engineering progress. Status-only checks are FORBIDDEN.
- Evidence over assertion: every claim needs provenance/hashes/splits/tests/file:line.
- Use only data/software accessible automatically without payment/signup/keys/manual downloads.

### SUCCESS CRITERIA
- [ ] All tests pass (27/27), timestamp + HEAD (`7385221a`) recorded in `research_state/AGENT_HANDOFF_OUTCOME.md`
- [ ] Track C synthesis hardened with full traceable numbers + `track_c_traceability_matrix.md`
- [ ] Track A block proof hardened with machine-checkable rubric + `track_a_rubric_enforcement_matrix.md` + active sweep evidence + all candidates in `track_a_deadend_map.md`
- [ ] Track B separation hardened with `track_b_codepath_separation_matrix.md` + grep evidence
- [ ] H002 handled correctly (pre-registered BEFORE outcome inspection OR ruled out with evidence in `h002_pre_registration.md`)
- [ ] `research_state/AGENT_HANDOFF_OUTCOME.md` updated with evidence + bottlenecks removed
- [ ] `research_state/handoff_hardening_audit.md` proves heavy work unavoidable
- [ ] `research_state/cross_track_decision_log.md` updated with C→A→B→H002
- [ ] All artifacts cross-linked; handoff remains single source of truth

**FORCED HEAVY SYNTHESIS CAMPAIGN — PRIORITIZED BY REPO NAME (FUNDING-CONDITIONED VOLATILITY → LIQUIDATION RISK). NO SHORTCUTS. BUILD EVIDENCE, NOT STATUS. REMOVE BOTTLENECKS. MAKE IT IMPOSSIBLE TO AVOID HEAVY WORK.**
