# AGENT HANDOFF — SINGLE DURABLE HANDOFF (PRIORITIZED BY REPO NAME)

UPDATED: 2026-10-31T08:22:04Z
HEAD: 5f49304d
REPO: Funding-conditioned-volatility-and-liquidation-risk
PRIORITY_SOURCE: Repository name inference (funding-conditioned volatility and liquidation risk)
PRIORITY_ORDER: Track C (funding-conditioned volatility forecasting) > Track A (observed liquidations) > Track B (modeled boundary breaches)
DURABLE_HANDOFF: SINGLE_SOURCE_OF_TRUTH
SESSION_GOAL: HEAVY_EVIDENCE_CAMPAIGN — NO SHORTCUTS. FORCE AUDITABLE HEAVY WORK. MAXIMIZE DEFENSIBLE EVIDENCE.
BOTTLE_NECK_REMOVAL: MANDATORY — Remove any structural/efficiency blockers so significant progress continues. No status-only work.

## INITIAL TASK MESSAGE FOR THE NEXT AGENTIC WORK SESSION (COPY AND EXECUTE THIS VERBATIM)

**TASK_ID:** `HND-20261031-082204-VERIFY-FINAL-CLOSEOUT-HEAVY`
**PRIORITY:** P0
**TIMESTAMP:** 2026-10-31T08:22:04Z
**MODE:** FORCED VERIFY-AND-CLOSEOUT CAMPAIGN — EXPLICIT DIRECTIONS ABSENT, BUILD NEXT FOCUS CAMPAIGN SO FUTURE AGENTS CANNOT AVOID HEAVY WORK
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**MANDATE:** Leave the most relevant inferred timestamped clear initial task message for the next agentic work session in the single durable handoff. Prioritize strictly by repo name: Track C (funding-conditioned volatility forecasting) FIRST, then Track A (observed liquidations), then Track B (modeled boundary breaches). If sessions are blocked/inefficient, remove bottlenecks so significant progress continues. Status-only work is FORBIDDEN.

You are continuing from this SINGLE DURABLE handoff. **Prioritize strictly by repo name: Track C FIRST, then Track A, then Track B.**

### CURRENT KNOWN STATE (DO NOT TRUST BLINDLY - VERIFY)
- Tests: `python -m unittest discover -s tests -v` → **21/21 PASS** (verified 2026-10-31T08:22:04Z). Must stay green.
- HEAD: 5f49304d (main). Working tree clean except untracked `scripts/__pycache__/`, `tests/__pycache__/`.
- Track C (H001): NOT_SUPPORTED (SEALED_NEGATIVE). All confirmatory panels negative:
  - FCLR-003 (powered, 2024-10-02..2024-12-31, 3 blocks, n=10796): C2 vs B1 +0.015205 QLIKE, CI [-0.020240, 0.056734] crosses zero, -3.78% rel → gate NOT_MET → COMPLETE_NEGATIVE.
  - FCLR-006 (unsealed 2026-05-23..2026-08-06, 2 blocks <3, n=8987): C2 vs B1 +0.368588 QLIKE, CI entirely positive → WORSE, -69.90% rel → gate NOT_MET → COMPLETE_NEGATIVE.
  - FCLR-007 (unsealed 2026-07-21..2026-07-31, 0 blocks <3, n=1195): C2 vs B1 +0.010258 QLIKE, CI [0.001308, 0.019737] entirely positive → WORSE, -3.42% rel → gate NOT_MET → COMPLETE_NEGATIVE.
  - Risk overlay INELIGIBLE. No reopen path without violating pre-registration/holdout discipline.
- Track A (H004): BLOCKED/EXPLORATORY (STRUCTURALLY BLOCKED). No admissible unauthenticated observed-liquidation census with ≥5 symbols, ≥3 non-overlapping 30-day blocks, documented completeness, license OK. Sole reopen path: NEW admissible unauthenticated source per RESEARCH_PROMPT.md §16. FCLR-005 was exploratory-only on exhausted 2026-07-08..2026-08-06 window (0 blocks, no incremental skill).
- Track B (H003): COMPLETE_NEGATIVE (SEALED_NEGATIVE). 16 cells, Holm correction, no robust incremental skill. Strict separation from Track A proven (track_b_definitive_separation_audit.md).
- Forecast gate NOT_MET on every tested panel. Confirmatory program CLOSED. Heavy evidence work (forensic/synthesis/audit/source-discovery/hardening) is mandatory and unavoidable.

### BOTTLENECK REMOVAL MANDATE (ALREADY EXECUTED — RE-VERIFY, DO NOT RE-OPEN)
Bottlenecks identified and removed or proven irremovable with evidence (see `research_state/handoff_hardening_audit.md`, `research_state/track_a_deadend_map.md`, `research_state/track_c_consolidated_dossier.md`, `research_state/track_b_definitive_separation_audit.md`):
1. **Data access bottlenecks**: ALL admissible unauthenticated sources for Track A probed with machine-checkable GO/NO-GO (HTTP codes, timestamps, coverage math). No source passes rubric → irrefutable dead-end evidence. Do NOT loop retries.
2. **Compute/analysis bottlenecks**: Cached data in `research_state/data_cache/` and repo zips available; restartable incremental analyses; do NOT recompute sealed results.
3. **Evidence bottlenecks**: Every claim needs provenance, hashes/splits, tests. Artifacts carry concrete numbers (track_c_consolidated_dossier.md FORENSIC_REAUDIT_20261031; track_a_deadend_map.md MACHINE_CHECKABLE_FIREWALL_20261031; track_b_definitive_separation_audit.md SEPARATION_AUDIT_20261031).
4. **Handoff bottlenecks**: This file is single source of truth. Impossible for next agent to do status-only work. If blocked, remove bottleneck or produce irrefutable evidence — do NOT report "blocked" without concrete evidence and attempted removals.

### MANDATORY HEAVY EVIDENCE CAMPAIGN (EXECUTE ALL - CANNOT SKIP)

**STEP 1: INTEGRITY CHECK (P0, ~2-5 min)**
1. `python -m unittest discover -s tests -v` → **MUST PASS ALL TESTS** (currently 21 tests). Verify and record timestamp.
2. Verify key artifacts exist and are cross-linked: `research_state/hypothesis_registry.json`, `research_state/experiment_frontier.json`, `research_state/track_c_consolidated_dossier.md` (FORENSIC_REAUDIT_20261031 section with numbers), `research_state/track_a_deadend_map.md` (MACHINE_CHECKABLE_FIREWALL_20261031), `research_state/track_b_definitive_separation_audit.md` (SEPARATION_AUDIT_20261031), `research_state/cross_track_decision_log.md`, `research_state/cross_track_decision_firewall.md`, `research_state/handoff_hardening_audit.md`, `research_state/negative_results_report.md`, `research_state/next_data_discovery_plan.md`, `research_state/final_confirmatory_verdict.md`, `research_state/structural_closure_verdict_heavy.md`.
3. Confirm constraints: no workflow changes, no trading logic, strict track separation, preserve negatives. Log integrity check in `research_state/AGENT_HANDOFF_OUTCOME.md`.

**STEP 2: VERIFY CLOSURE EVIDENCE & CLOSE GAPS (P0, PRIORITIZE BY REPO NAME)**
Prioritize Track C → Track A → Track B. For each track, confirm closure evidence is complete and concrete; if any gap/missing number/missing artifact is found, EXECUTE the corresponding heavy work before closing:

**2A. TRACK C — FUNDING-CONDITIONED VOLATILITY (FIRST - HIGHEST PRIORITY)**
- Confirm `FORENSIC_REAUDIT_20261031` section in `research_state/track_c_consolidated_dossier.md` contains: exact splits/embargoes/blocks/paired n per run, full QLIKE decomposition (B0/B1/C1/C2), C2 vs B1 means + 95% CIs (block bootstrap), leakage checks, block structure verification.
- Confirm `research_state/evaluation_summary.md`, `research_state/negative_results_report.md`, `research_state/final_confirmatory_verdict.md` carry concrete numbers/tables for FCLR-003/006/007.
- Any alternative ablation/robustness stress test that does NOT touch sealed holdouts may be added with numbers; anything touching sealed holdouts is BLOCKED and documented with evidence.
- Track C remains CLOSED (NOT_SUPPORTED), risk overlay INELIGIBLE — no reopen without pre-registration violation.

**2B. TRACK A — OBSERVED LIQUIDATIONS (SECOND — REMOVE BOTTLENECKS)**
- Confirm machine-checkable firewall applied to ALL candidates in `research_state/liquidation_sources_enumeration.md` with evidence fields filled (URLs, HTTP codes, timestamps, coverage math, sizes, attempt logs) in `research_state/track_a_deadend_map.md`.
- Confirm NO source passes rubric: `unauthenticated == true AND no_keys == true AND symbols>=5 AND blocks>=3 AND completeness_doc == true AND license_ok == true AND census_or_defensible == true`.
- If any source passes rubric: FREEZE protocol (pre-register) BEFORE examining outcomes, then test. Never peek first. Document GO/NO-GO with evidence.
- Otherwise Track A remains STRUCTURALLY BLOCKED with irrefutable dead-end evidence; sole reopen: new admissible unauthenticated source per RESEARCH_PROMPT.md §16.

**2C. TRACK B — MODELED BREACHES (THIRD)**
- Confirm separation evidence in `research_state/track_b_definitive_separation_audit.md` with concrete file paths/line references (Track B never consumes Track A liquidation labels).
- Confirm `research_state/cross_track_decision_firewall.md` and `research_state/cross_track_decision_log.md` enforce strict separation.
- Sensitivity analysis (margin/leverage/funding assumptions) documented with numbers; results labeled synthetic/model proxy, never conflated with observed liquidations.

**STEP 3: DOCUMENTATION & HARDENING (P0)**
1. Create/update `research_state/AGENT_HANDOFF_OUTCOME.md` with timestamp, HEAD (5f49304d), detailed evidence summary of ALL work done (artifacts modified/created, commands run, numbers).
2. Update `research_state/handoff_hardening_audit.md` proving bottlenecks removed and next agent CANNOT avoid heavy work (specific blockers identified+removed or irrefutable dead-ends).
3. Update `research_state/cross_track_decision_log.md` with new findings.
4. Ensure all artifacts cross-linked.
5. Run tests again: `python -m unittest discover -s tests -v` → MUST PASS. Record final test result with timestamp.

### HARD CONSTRAINTS (NEVER VIOLATE)
- No credentials/manual inputs/paid data. No `.github/workflows` changes without explicit maintainer auth. No trading/paper-trading/live orders.
- Strict track separation. Never conflate modeled breaches (B) with observed liquidations (A).
- Preserve negatives/inconclusives. No fabricated data/labels. No zero-fill of missing values.
- Pre-registration REQUIRED for any new experiment. NO outcome inspection before pre-registration.
- No re-tuning on sealed holdouts. No threshold shopping.
- No re-running completed confirmatory experiments. No relaxing the ≥3-block/≥2%-relative-QLIKE gate.
- Every iteration must create measurable research/data/testing/engineering progress. Status-only checks are FORBIDDEN.

### SUCCESS CRITERIA
- [ ] All tests pass (record timestamp/HEAD)
- [ ] All key artifacts present and cross-linked (integrity check logged)
- [ ] Track C: closure evidence with concrete tables/numbers verified; FORENSIC_REAUDIT_20261031 present (or heavy gap-filling work executed)
- [ ] Track A: machine-checkable firewall applied to ALL candidates; dead-end irrefutable OR GO experiment pre-registered and executed per rules
- [ ] Track B: separation proven with concrete code-path evidence (file paths/lines)
- [ ] Bottlenecks identified and removed (documented with evidence) - no unsubstantiated "blocked"
- [ ] `research_state/AGENT_HANDOFF_OUTCOME.md` created/updated with full evidence (artifacts, commands, numbers)
- [ ] `research_state/handoff_hardening_audit.md` proves heavy work unavoidable
- [ ] `research_state/cross_track_decision_log.md` updated
- [ ] This handoff remains single source of truth

**FORCED HEAVY CAMPAIGN. NO SHORTCUTS. BUILD EVIDENCE, NOT STATUS.**
