# AGENT_HANDOFF (DURABLE - SINGLE SOURCE OF TRUTH)

**Created:** 2026-11-02T10:55:47Z
**HEAD:** 5369f085
**Status:** ACTIVE_HANDOFF
**Priority:** FOCUS_CAMPAIGN_FCLR_NEXT_HEAVY

## INITIAL TASK MESSAGE FOR NEXT AGENTIC SESSION (TIMESTAMPED, CLEAR, ACTIONABLE)

**TASK_ID:** FCLR-NEXT-HEAVY-001
**PRIORITY:** P0 - HEAVY WORKING CAMPAIGN (NO AVOIDANCE)

### OBJECTIVE
Execute a concrete, heavy-working campaign that advances the project goal ("Funding-conditioned-volatility-and-liquidation-risk") using only admissible free data. All confirmatory gates are resolved; do not reopen closed tracks without NEW admissible data + fresh pre-registration before outcome inspection.

### REPOSITORY CONTEXT (PRIORITIZE BY NAME)
Project: Funding-conditioned-volatility-and-liquidation-risk
Focus areas: funding-conditioned volatility forecasting + liquidation risk (observed vs modeled).
Current state: Track A (ironflow Hyperliquid observed liquidations) FCLR-010 gate PASSED, overlay HYPOTHETICAL_ONLY. Track C H001 INCONCLUSIVE but panels exhausted. Track B CLOSED_NEGATIVE. H002 PARTIAL (SSRN blocked). FCLR-HEAVY-001 just completed. Ironflow monitor active.

### MANDATORY FIRST ACTIONS (BLOCKING)
1. **Read firewall/state**: `research_state/cross_track_decision_log.md`, `research_state/hypothesis_registry.json`, `research_state/experiment_frontier.json`, `research_state/ironflow_monitor_state.json`. Respect firewall: Hyperliquid ironflow ONLY for Track A observed; no Binance merge; modeled != observed.
2. **Check ironflow data**: Monitor `ironflow/hyperliquid-liquidations` on HF - see if 2026-11/12/2027-01 appear (currently absent per monitor). If new months appear, DO NOT just note - plan ingestion.
3. **Verify tests**: Run `python -m unittest discover -s tests -v` and record result. Must stay green.

### CAMPAIGN PLAN (HEAVY WORKING - DO NOT SKIP STEPS)
**Campaign:** FCLR-NEXT-HEAVY-001 - "Ironflow deepening + liquidation-funding coupling stress tests"
**Scope:** Track A only (admissible). Hypothetical-only. No sealed panel modification.

**Steps (execute in order, produce artifacts):**
1. **COUPLING STRENGTHENING**: Extend FCLR-HEAVY-001 coupling analysis with block-bootstrap (>=2000), regime stratification (funding z-score terciles), and interaction terms. Test stability across symbols/blocks. Artifact: `research_state/fclr_next_heavy001_coupling.md`, `results/fclr_next_heavy001/*`.
2. **LEAKAGE/ROBUSTNESS HARDENING**: Adversarial checks on FCLR-010 panel - label timing, embargoes, survivor bias, OI/volume denominators if available. Document all checks. Artifact: `research_state/fclr_next_heavy001_leakage_robust.md`.
3. **MICROSTRUCTURE INTEGRATION**: Leverage FCLR-LIQMICRO-002 panel (ironflow + Hyperliquid funding). Test whether funding×liquidation microstructure features improve the Track A observed model beyond current spec, with multiplicity control. Pre-register analysis plan BEFORE inspecting outcomes if adding new cells. Artifact: `research_state/fclr_next_heavy001_micro_int.md`.
4. **COVERAGE AUDIT**: Re-audit ironflow coverage (symbols/time/blocks) against rubric. Update `research_state/fclr_next_heavy001_coverage_audit.json`.
5. **INTEGRITY LOCK-IN**: Re-verify sealed FCLR-010 artifacts unchanged (hashes/mtimes). Update `experiment_frontier.json` with campaign status. All outputs hypothetical-only.

### CONSTRAINTS (HARD)
- Firewall: ironflow Hyperliquid ONLY. NO Binance merge. Modeled != observed.
- No re-test of sealed confirmatory gates (H001/FCLR-003/FCLR-006/FCLR-007/FCLR-008/FCLR-010) without NEW admissible data + fresh pre-registration BEFORE outcome inspection.
- H002 permanently blocked (SSRN 403). Do not waste cycles on it.
- Track B closed negative. Track C exhausted.
- All Track A enhancements must be hypothetical-only; no profitability claims.
- If new ironflow months appear, treat as potential NEW admissible data - must pre-register experiment ID BEFORE outcome inspection.
- Keep tests green (27/27). No workflow changes unless absolutely necessary and justified.

### SUCCESS CRITERIA
- All 5 steps completed with concrete artifacts (files created/updated with evidence).
- `experiment_frontier.json` updated with FCLR-NEXT-HEAVY-001 status.
- Tests pass. Sealed artifacts unchanged.
- Clear summary of findings, limitations, next steps.

**DO NOT STOP AT ANALYSIS - DO HEAVY WORKING. BUILD ARTIFACTS.**
