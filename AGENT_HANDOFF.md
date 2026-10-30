# AGENT HANDOFF — Funding-Conditioned Volatility and Liquidation Risk

UPDATED: 2026-10-30T17:50:00Z
HEAD: fb7b0da1 (main) — working tree clean
REPO: Funding-conditioned-volatility-and-liquidation-risk
DURABLE_HANDOFF: SINGLE_SOURCE_OF_TRUTH
SESSION_GOAL: LIQUIDATION_RISK_FOCUS_CAMPAIGN

## PRIORITIZED INITIAL TASK (2026-10-30T17:50:00Z) — MANDATORY

**TASK_ID:** `HND-20261030-175000-LIQUIDATION_FOCUS`
**PRIORITY:** P0
**MODE:** HEAVY RESEARCH + ENGINEERING. NO MAINTENANCE-ONLY STOP.

### CONTEXT (inferred from repo name + evidence)
Repository name prioritizes **liquidation risk** as a first-class concern alongside funding-conditioned dynamics. H001 (funding-conditioned volatility improvement) is CLOSED: NOT_SUPPORTED across FCLR-003/FCLR-006 (overlay INELIGIBLE). Track A (observed liquidation labels) is BLOCKED/EXHAUSTED for 2024 frozen windows with all admissible unauthenticated sources tested. H003 (modeled boundary breaches) was INCONCLUSIVE with near-zero event rates under current assumptions. This campaign must focus on making **significant progress on liquidation risk** - either by finding new admissible liquidation data or by improving the modeled liquidation risk framework.

### IMMEDIATE OBJECTIVE
Build the next focus campaign to systematically advance liquidation risk prediction. Future agents MUST do heavy work on this - no more verification-only closure loops.

### EXECUTION PLAN (Execute in strict order)

1. **[BASELINE AUDIT]** Re-read all liquidation-related evidence
   - Read `research_state/liquidation_sources_enumeration.md` (full), `research_state/evaluation_summary_FCLR005.md`, `research_state/evaluation_summary_h003.md`, `research_state/binance_source_probe.md`
   - Understand exactly what was tried, why it failed, and what constraints exist
   - Map all attempted sources and their exact failure modes

2. **[BOTTLENECK REMOVAL - DATA DISCOVERY]** Hunt for NEW admissible liquidation data sources
   - **HuggingFace**: Search for other liquidation datasets beyond ochinimus/crypto-liquidation-ticks. Look for datasets with different time ranges, different venues, or different schemas. Check if there might be datasets not surfaced in previous searches.
   - **GitHub**: Search for repos with liquidation data CSVs/JSONs (be creative with search terms). Look in common locations.
   - **data.binance.vision**: Re-examine ALL paths - maybe liquidation data is stored differently? Check futures/cm, spot, different naming conventions, older paths.
   - **Other venues**: Bybit, OKX, Deribit, Gate.io public data - look for liquidation snapshots/trades that can be aggregated.
   - **Academic/Zenodo**: Deeper search for liquidation event datasets.
   - **On-chain/other**: Any other public unauthenticated sources.
   - For ANY new source found: verify it's unauthenticated, has no paywall/signup/keys, has sufficient coverage (>=5 symbols, >=3 non-overlapping 30-day blocks), document full provenance.

3. **[BOTTLENECK REMOVAL - METHODOLOGY]** If no new data found, improve modeled liquidation risk (H003)
   - **Rethink assumptions**: Current H003 used MMR 0.005, mark close as entry, 24h horizon. Try different MMR values, different entry assumptions, different horizons.
   - **Better features**: Incorporate funding rate (repo name says "Funding-conditioned" - funding might be critical for liquidation risk even if not for volatility). Add funding features to liquidation prediction.
   - **Different approach**: Instead of binary breach prediction, model distance to liquidation, time-to-liquidation, or liquidation intensity.
   - **Look at the data differently**: Maybe liquidation risk manifests differently than simple boundary crossings.
   - **Leverage existing data**: Use the funding/price data we already have in abundance to build better liquidation risk models.

4. **[HEAVY EXECUTION]** Don't just plan - EXECUTE
   - Write code to test new hypotheses
   - Run experiments with proper pre-registration
   - Create new evaluation scripts if needed
   - Generate results and update research state
   - Every session must produce MEASURABLE progress on liquidation risk

5. **[DOCUMENT & HANDOFF]** Leave clear trail
   - Update `research_state/liquidation_sources_enumeration.md` with any new findings
   - Create new experiment records if running experiments
   - Update AGENT_HANDOFF.md with next concrete steps
   - Commit nothing unless explicitly necessary, but DO record all progress in research_state/

### CONSTRAINTS (must follow)
- **NO CREDENTIALS**: Only use unauthenticated public sources. Never ask for API keys, logins, or manual downloads.
- **RESPECT EXISTING WORK**: Don't re-run sealed FCLR-001/002/003/006 or tune on sealed holds. H001 is done.
- **DISTINGUISH OUTCOMES**: Keep modeled vs observed liquidations separate. Never conflate them.
- **PRE-REGISTER**: If running new experiments with holdout data, pre-register experiment ID BEFORE examining outcomes per RESEARCH_PROMPT §16.
- **NO WORKFLOW CHANGES**: Don't modify `.github/workflows/*` without explicit maintainer authorization.
- **BE THOROUGH**: Don't stop at first failed search. Try multiple approaches. Remove bottlenecks.
- **HEAVY WORK REQUIRED**: Future agents must never avoid doing heavy working. This is a research campaign, not a verification task.

### SUCCESS CRITERIA
Significant progress means: either (a) finding a viable new liquidation data source that meets criteria, or (b) producing a working improved liquidation risk model with evidence of predictive value, or (c) clearly demonstrating why neither is possible with concrete evidence and proposing a specific next path.

**DO NOT STOP until you have made measurable progress on liquidation risk. The program is NOT closed - only H001 is closed. Liquidation risk remains open and is the priority.**
