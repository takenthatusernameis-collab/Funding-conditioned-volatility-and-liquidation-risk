# AGENT HANDOFF — Funding-Conditioned Volatility and Liquidation Risk

UPDATED: 2026-10-30T17:39:37Z
HEAD: fb7b0da1 (main) — working tree clean (only untracked __pycache__/)
REPO: Funding-conditioned-volatility-and-liquidation-risk
DURABLE_HANDOFF: SINGLE_SOURCE_OF_TRUTH
SESSION_GOAL: LIQUIDATION_RISK_FOCUS_CAMPAIGN

## PRIORITIZED INITIAL TASK (2026-10-30T17:39:37Z) — MANDATORY

**TASK_ID:** `HND-20261030-173937-LIQUIDATION_FOCUS`
**PRIORITY:** P0
**MODE:** HEAVY RESEARCH + ENGINEERING. NO MAINTENANCE-ONLY STOP.

### CONTEXT (inferred from repo name + all evidence)

Repository name prioritizes **liquidation risk** as a first-class concern alongside funding-conditioned dynamics.

Program-wide status (all final, do not re-run sealed holds):
- **FCLR-H001 (volatility forecasting): NOT_SUPPORTED / SEALED_NEGATIVE.** FCLR-003 powered confirmatory: C2 vs B1 = -3.78% rel QLIKE, CI crosses zero, gate NOT_MET (5 instruments, 3 blocks, n=10796). FCLR-006 unsealed 2026: C2 vs B1 = -67.32% (significantly WORSE), gate NOT_MET (2 blocks < 3). FCLR-002 underpowered (2 blocks). FCLR-001 single-symbol ~4-day block. Independently reproduced byte-identical on 2026-10-28 and 2026-10-30.
- **FCLR-H002 (funding correction time): PARTIAL_REPLICATION.** SSRN HTTP 403 blocks full methodology; no RV-regime contrast possible.
- **FCLR-H003 (modeled boundary breach): INCONCLUSIVE.** No incremental skill over B0/B1 on any pre-registered metric across both panels. Untested extensions: longer horizons (72h/168h), lower MMR tiers, event-intensity target — each requires fresh pre-registration before outcome inspection.
- **FCLR-H004 / Track A (observed liquidation labels): BLOCKED / EXHAUSTED.** Binance `liquidationSnapshot` HTTP 404; `fapi forceOrders` HTTP 451; Bybit/OKX/Deribit no unauthenticated census; HF ochinimus crypto-liquidation-ticks covers only 2026-07-08..2026-08-06 (single ~30-day window, 0 confirmatory blocks, used in FCLR-005 pilot with no incremental skill); Zenodo/GitHub dead ends. All 2024 routes dead. Per RESEARCH_PROMPT §16, repeating dead endpoints is NOT a distinct route.
- **Risk overlay: INELIGIBLE.** Forecast gate not met. Do not build overlay/position-sizing.

**Bottlenecks removed / acknowledged:**
- Track A data discovery campaign (`research_state/liquidation_source_campaign.md`) has 9 candidate sources NOT_YET_PROBED. Execute them — this is the only path to reopen Track A / H004.
- No unsealed >=5-symbol confirmatory window remains on current admissible data (2024-04..12 committed; 2025 only 2 symbols; 2026 partial). New admissible data source is required before any new confirmatory experiment.
- H003 extensions exist but require unsealed data + fresh pre-registration — do not tune on sealed panels.

### IMMEDIATE OBJECTIVE

Build the next focus campaign to systematically advance **liquidation risk** prediction. Future agents MUST do heavy work on this — no more verification-only closure loops.

### EXECUTION PLAN (Execute in strict order)

**Step 1 — LIQUIDATION DATA DISCOVERY (Track A re-open path)**
Execute `research_state/liquidation_source_campaign.md` probes #1–#9. Each probe must be a materially distinct source family/method per RESEARCH_PROMPT §16. Record HTTP status, body, schema, coverage, completeness (census vs sample), license/terms for each. GO criteria: unauthenticated download, >=5 symbols, >=3 non-overlapping 30-day blocks (>=90 days), completeness documented, license OK, no sealed-hold reuse. Document every finding in `research_state/liquidation_source_campaign.md`. If GO source found: pre-register new experiment ID BEFORE examining outcomes, then execute frozen protocol.

**Step 2 — IF NO NEW LIQUIDATION DATA FOUND (Track B / H003 extensions)**
Register a fresh protocol version for H003 extensions on an unsealed panel:
- Longer horizons (72h/168h), lower MMR tiers, event-intensity target vs binary breach
- Pre-register BEFORE any outcome inspection; fresh experiment ID; do not threshold-shop sealed results
- Requires unsealed data — if none available, document structural blocker with evidence and stop cleanly

**Step 3 — HEAVY EXECUTION**
Write code to test new hypotheses. Run experiments with proper pre-registration. Generate results and update research_state. Every session must produce MEASURABLE progress on liquidation risk.

**Step 4 — DOCUMENT & HANDOFF**
- Update `research_state/liquidation_source_campaign.md` with all probe results
- Update `research_state/liquidation_sources_enumeration.md` with any new findings
- Create new experiment records if running experiments
- Update AGENT_HANDOFF.md with next concrete steps
- Commit nothing unless explicitly necessary, but DO record all progress in research_state/

### CONSTRAINTS (must follow)
- **NO CREDENTIALS**: Only unauthenticated public sources. Never ask for API keys, logins, or manual downloads.
- **RESPECT EXISTING WORK**: Do NOT re-run sealed FCLR-001/002/003/005/006 or tune on sealed holds. H001 is done.
- **DISTINGUISH OUTCOMES**: Keep modeled vs observed liquidations separate. Never conflate them.
- **PRE-REGISTER**: If running new experiments with holdout data, pre-register experiment ID BEFORE examining outcomes per RESEARCH_PROMPT §16.
- **NO WORKFLOW CHANGES**: Do not modify `.github/workflows/*` without explicit maintainer authorization.
- **BE THOROUGH**: Don't stop at first failed search. Try multiple approaches. Remove bottlenecks.
- **HEAVY WORK REQUIRED**: Future agents must never avoid doing heavy working. This is a research campaign, not a verification task.

### SUCCESS CRITERIA

Significant progress means: either (a) finding a viable new liquidation data source meeting GO criteria, or (b) producing a working improved liquidation risk model with evidence of predictive value (H003 extension pre-registered and executed), or (c) clearly demonstrating why neither is possible with concrete evidence and proposing a specific next path.

**DO NOT STOP until you have made measurable progress on liquidation risk. The program is NOT closed — only H001 is closed. Liquidation risk remains open and is the priority.**

### VERIFICATION COMMAND

`python -m unittest discover -s tests -v` (must pass all tests)
