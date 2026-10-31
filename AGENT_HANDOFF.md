# AGENT HANDOFF — SINGLE DURABLE HANDOFF (PRIORITIZED BY REPO NAME)
UPDATED: 2026-10-31T20:10:37Z
HEAD: 68142043 (main). Working tree clean (untracked __pycache__ ignored).
REPO: Funding-conditioned-volatility-and-liquidation-risk
PRIORITY_SOURCE: Repository name inference (funding-conditioned volatility and liquidation risk) — FUNDING-CONDITIONED VOLATILITY FIRST
PRIORITY_ORDER: Track C (Funding-conditioned volatility forecasting) > Track A (Observed liquidations) > Track B (Modeled boundary breaches) > H002 (Funding-extreme correction time, exploratory-only)
DURABLE_HANDOFF: SINGLE_SOURCE_OF_TRUTH
SESSION_GOAL: FORCED_HEAVY_EVIDENCE_CAMPAIGN — NO STATUS-ONLY PATH. EVERY ITERATION MUST PRODUCE MEASURABLE ARTIFACTS. REMOVE ALL BOTTLENECKS. MAKE FUTURE AGENTS UNABLE TO AVOID HEAVY WORK.
BOTTLE_NECK_REMOVAL: MANDATORY

HEAD_NOTE: HEAD verified at 68142043. All prior stale HEAD references superseded by this handoff. Handoff is single durable source of truth.

## INITIAL TASK MESSAGE FOR THE NEXT AGENTIC WORK SESSION (COPY AND EXECUTE THIS VERBATIM)

## NO ESCAPE CLAUSE (NON-NEGOTIABLE)
- NO STATUS REPORTS: "X is blocked/closed" without new concrete artifacts is not acceptable. Prove with files/lines/hashes/manifests.
- NO LAZY SWEEPS: Track A requires testing EVERY plausible candidate against the verbatim rubric with HTTP/auth/coverage/evidence NOW.
- NO REOPENING WITHOUT GATES: Track C is sealed. Track B is closed negative with separation proven. Only NEW admissible data per RESEARCH_PROMPT §16 can reopen anything.
- HEAVY OR NOTHING: If your turn produces only reading logs/status without creating/modifying research_state artifacts with provenance, you have failed this mandate.
- FORCE MULTIPLICATION: Every artifact you create must enable the next agent to do more heavy work, not less.
- REPO-NAME DRIVEN: Funding-conditioned volatility (Track C) comes FIRST because the repo says so. Execute in that order regardless of curiosity.

TASK_ID: HND-20261031-200311-FORCED_HEAVY_EVIDENCE_SYNTHESIS-V20
PRIORITY: P0
TIMESTAMP: 2026-10-31T20:03:11Z
MODE: FORCED HEAVY WORK — INFERRED FROM REPO NAME. BUILD THE NEXT FOCUS CAMPAIGN SO FUTURE AGENTS CANNOT AVOID HEAVY WORK.
REPO: Funding-conditioned-volatility-and-liquidation-risk
MANDATE: SINGLE DURABLE HANDOFF. Prioritize strictly by repo name: Track C → Track A → Track B → H002. Remove bottlenecks. Status-only work FORBIDDEN. Every action must yield concrete artifacts with provenance (file paths, line ranges, hashes/manifests, timestamps, HEAD). No re-tuning on sealed holdouts.

You are continuing from this SINGLE DURABLE handoff. Prioritize strictly by repo name: Track C → Track A → Track B → H002.

### CURRENT VERIFIED STATE (VERIFY AT START - DO NOT TRUST BLINDLY)
- Tests: `python -m unittest discover -s tests -v` → 27/27 PASS (must remain green). Verify at start and end.
- HEAD: `68142043` (main). Working tree clean. All prior stale HEAD references superseded.
- Track C (H001, funding-conditioned volatility): NOT_SUPPORTED — CONFIRMATORY CLOSED. FCLR-003 C2 vs B1 +0.015205 QLIKE, 95% CI [-0.020240, 0.056734] crosses zero (-3.78% worse). FCLR-006/FCLR-007 worse in 2026 windows. Risk overlay INELIGIBLE per RESEARCH_PROMPT §9. Full synthesis in `research_state/track_c_final_synthesis_dossier.md`. DO NOT REOPEN without pre-registration + documented holdout discipline violations with evidence. Traceability matrix MUST stay hardened.
- Track A (H004, observed liquidations): STRUCTURALLY BLOCKED. Machine-checkable rubric applied to ALL enumerated candidates — no source passes ALL items (unauthenticated, >=5 symbols, >=3 non-overlapping 30-day blocks, documented completeness, license OK, census/defensible). Sole reopen: NEW admissible unauthenticated source per RESEARCH_PROMPT.md §16 with concrete evidence. Proof in `research_state/track_a_final_block_proof.md`, `research_state/track_a_rubric_enforcement_matrix.md`, and `research_state/track_a_deadend_map.md`. ACTIVE SWEEP REQUIRED - do not just read old evidence.
- Track B (H003, modeled boundary breaches): CLOSED_NEGATIVE. FCLR-H003-EXT-001: no robust incremental skill after Holm correction across 16 cells. Strict separation from Track A proven. Proof in `research_state/track_b_separation_proof_hardened.md`, `research_state/track_b_definitive_separation_audit.md`, and `research_state/track_b_codepath_separation_matrix.md`.
- H002 (funding-extreme correction time): EXPLORATORY/PARTIAL (88 events, 84 corrected, 4 censored). Do not promote to volatility skill/boundary breaches/observed liquidations. Remaining open track — may advance to confirmatory ONLY via new pre-registration (RESEARCH_PROMPT §16) with concrete admissible design. Must pre-register BEFORE outcome inspection.

### BOTTLENECK REMOVAL MANDATE (FORCE HEAVY WORK)
1. Traceability bottleneck (Track C): Keep `research_state/track_c_traceability_matrix.md` fully updated with decomposition (B0/B1/C1/C2), paired n, blocks, CIs, leakage audit with file:line + artifact references and HEAD consistency at 68142043. Verify no re-tuning on holdouts.
2. Data access bottleneck (Track A): CONDUCT ACTIVE evidence-backed sweep of ALL plausible candidates. For EVERY candidate test against verbatim rubric immediately with concrete HTTP/coverage/auth/census evidence. Eliminate status-only loops — produce pass/fail tables. Update `research_state/track_a_rubric_enforcement_matrix.md` and `research_state/track_a_deadend_map.md`. Do NOT assume old probes are sufficient - re-probe if anything changed.
3. Separation bottleneck (Track B): Enforce and prove strict separation. Trace every code path using `liquidat*` against Track A boundaries. Surface any mixing with file:line evidence. Harden `research_state/track_b_codepath_separation_matrix.md`. Run grep across codebase for liquidat usage.
4. Handoff integrity bottleneck: This file is SINGLE source of truth. Next agent MUST be unable to take a status-only path. Force heavy evidence work at every step. Update all cross-links.
5. H002 gating bottleneck: Never inspect outcomes blindly. If a concrete path to confirmatory exists per RESEARCH_PROMPT §16, PRE-REGISTER FIRST in `research_state/h002_pre_registration.md` before any outcome inspection. Otherwise rule out with evidence. Keep exploratory scope.

### HARD CONSTRAINTS (NEVER VIOLATE)
- No credentials/manual inputs/paid data. No `.github/workflows` changes without explicit maintainer auth. No trading/paper-trading/live orders.
- Strict track separation. Never conflate Track B (modeled) with Track A (observed).
- Preserve negatives/inconclusives. No fabricated data/labels. No zero-fill of missing values.
- Pre-registration REQUIRED for any new experiment. NO outcome inspection before pre-registration.
- No re-tuning on sealed holdouts. No threshold shopping.
- No re-running completed confirmatory experiments. No relaxing gates.
- Every iteration must create measurable research/data/testing/engineering progress. Status-only checks are FORBIDDEN.
- Evidence over assertion: every claim needs provenance/hashes/splits/tests/file:line.

### SUCCESS CRITERIA
- [ ] All tests pass (27/27), timestamp + HEAD (68142043) recorded in `research_state/AGENT_HANDOFF_OUTCOME.md`
- [ ] Track C hardened with irrefutable traceability
- [ ] Track A hardened with rubric enforcement + active sweep evidence + all candidates in deadend map (irrefutable block)
- [ ] Track B hardened with codepath separation matrix + grep evidence (strict separation proven)
- [ ] H002 handled correctly (pre-registered BEFORE outcome inspection OR ruled out with evidence)
- [ ] `research_state/AGENT_HANDOFF_OUTCOME.md`, `research_state/handoff_hardening_audit.md`, `research_state/cross_track_decision_log.md` updated
- [ ] All artifacts cross-linked; handoff remains single source of truth
- [ ] HEAD references consistent with 68142043

FORCED HEAVY SYNTHESIS CAMPAIGN — PRIORITIZED BY REPO NAME (FUNDING-CONDITIONED VOLATILITY → LIQUIDATION RISK). NO SHORTCUTS. BUILD EVIDENCE, NOT STATUS. REMOVE BOTTLENECKS. MAKE IT IMPOSSIBLE TO AVOID HEAVY WORK.
