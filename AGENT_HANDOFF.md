# AGENT HANDOFF — Funding-Conditioned Volatility and Liquidation Risk

UPDATED: 2026-10-30T17:45:30Z
HEAD: fb7b0da1 (main) — working tree clean (only untracked __pycache__/)
REPO: Funding-conditioned-volatility-and-liquidation-risk
DURABLE_HANDOFF: SINGLE_SOURCE_OF_TRUTH
SESSION_GOAL: LIQUIDATION_RISK_FOCUS_CAMPAIGN

## PRIORITIZED INITIAL TASK (2026-10-30T17:45:30Z) — MANDATORY, HEAVY WORK

**TASK_ID:** `HND-20261030-174530-LIQUIDATION_RISK_CAMPAIGN`
**PRIORITY:** P0
**MODE:** HEAVY RESEARCH + ENGINEERING. NO VERIFICATION-ONLY CLOSURE.

### REPO PRIORITY (inferred from name)
Repository name **Funding-conditioned-volatility-and-liquidation-risk** puts **liquidation risk** first. Despite H001 (volatility forecasting) being SEALED_NEGATIVE/NOT_SUPPORTED, liquidation risk remains open and is the priority.

### CURRENT STATE (evidence-based)
- **H001 (volatility forecasting):** SEALED_NEGATIVE / NOT_SUPPORTED. FCLR-003 powered confirmatory: C2 vs B1 = -3.78% rel QLIKE, CI crosses zero (gate NOT_MET). FCLR-006 unsealed-2026 negative. Do **NOT** re-run sealed holds.
- **H002 (funding correction time):** PARTIAL_REPLICATION only (SSRN HTTP 403 blocks full methodology).
- **H003 (modeled boundary breach / Track B):** INCONCLUSIVE on both panels, no incremental skill over baselines. Extensions (longer horizons 72h/168h, lower MMR tiers, event-intensity target) are **untested** but require fresh pre-registration before outcome inspection.
- **H004 / Track A (observed liquidation labels):** **BLOCKED/EXHAUSTED for 2024 confirmatory-feasible windows.** Full probe campaign completed 2026-10-30T17:45:12Z (probes #1-#9). No unauthenticated complete census found for Binance/Bybit/OKX/Deribit with >=5 symbols, >=90 days, >=3 non-overlapping 30-day blocks. Only ochinimus HF dataset (2026-07-08..2026-08-06, CC BY 4.0) exists but is 2026-only and was used as exploratory pilot (FCLR-005) with no confirmatory skill. **Do not repeat dead endpoints.**
- **Risk overlay:** INELIGIBLE (forecast gate not met).

**BOTTLENECKS REMOVED/ACKNOWLEDGED:** Track A discovery exhausted with evidence logged. Unsealed 2026 data exists in `research_state/data_cache/` for markPriceKlines/indexPriceKlines/fundingRate (Apr-Aug 2026) across all 5 symbols - this is the only remaining unsealed panel for liquidation-adjacent work.

### MANDATORY EXECUTION PLAN (do in order, HEAVY WORK)

**STEP 1: PRE-REGISTER H003 EXTENSIONS ON UNSEALED 2026 PANEL (P0)**
- Use unsealed 2026 data (Apr-Aug) in `research_state/data_cache/` - verified present for BTCUSDT/ETHUSDT/BNBUSDT/SOLUSDT/XRPUSDT.
- **Pre-register BEFORE outcome inspection:** Create new experiment ID (e.g., `FCLR-H003-EXT-001`) in `research_state/experiment_frontier.json` and write frozen protocol in `research_state/` (hypotheses, features, targets, horizons 72h/168h, MMR tiers, event-intensity vs binary breach, train/val/test boundaries from coverage, leakage controls).
- Do **NOT** reuse sealed panel boundaries/results. Do **NOT** threshold-shop.
- Distinguish modeled boundary breaches (Track B) from observed liquidations (Track A). Never conflate them.

**STEP 2: IMPLEMENT AND EXECUTE H003 EXTENSIONS**
- Extend boundary-breach logic to 72h/168h horizons with proper purging/embargo for longer horizons.
- Add lower MMR tiers and event-intensity target (notional-normalized) if feasible with public mark/index data.
- Use chronological splits on unsealed 2026 panel. Compute block-aware CIs, calibration, precision/recall for rare events.
- Compare against B0/B1 baselines with ablations (funding + price features). Report incremental value.

**STEP 3: IF H003 EXTENSIONS SHOW PROMISE OR REMAIN INCONCLUSIVE**
- If signal emerges: rigorously validate with leave-one-symbol-out, block bootstrap, multiple-comparison correction. Document uncertainty.
- If still inconclusive: try alternative feature sets (funding term structure, volatility regimes) with fresh pre-registration - but only if justified by evidence.
- **Do not** build risk overlay regardless of results until explicit forecast gate is met per protocol.

**STEP 4: DOCUMENT & HANDOFF (DURABLE)**
- Update `research_state/experiment_frontier.json` with new experiment record
- Write results to `research_state/evaluation_summary_*.md` (separate from sealed summaries)
- Update `research_state/hypothesis_registry.json` with status transitions
- Update this `AGENT_HANDOFF.md` with concrete next steps and evidence
- Record all commands/results in research_state artifacts

### HARD CONSTRAINTS
- **NO CREDENTIALS:** Only unauthenticated public sources. Never ask for keys/logins/manual downloads.
- **RESPECT SEALS:** Do NOT re-run/re-tune FCLR-001/002/003/005/006 or inspect sealed holds for threshold choices.
- **DISTINGUISH TRACKS:** Modeled (B) vs observed (A) liquidations must remain separate. No event-free inference.
- **PRE-REGISTER:** Any new experiment with holdout data requires pre-registration BEFORE outcome inspection.
- **NO WORKFLOW CHANGES:** Do not modify `.github/workflows/*` without explicit maintainer authorization.
- **NO TRADING:** No live/paper trading, orders, accounts, wallets.
- **HEAVY WORK REQUIRED:** Every session must produce measurable progress on liquidation risk. Do not stop at verification.

### SUCCESS CRITERIA
Significant progress = (a) pre-register and execute H003 extensions on unsealed 2026 panel with full evaluation artifacts, OR (b) find evidence for/against liquidation predictability with proper uncertainty quantification, OR (c) if structurally blocked, document with concrete evidence and propose a specific non-dead-end path.

**H001 is closed. Liquidation risk (H003 extensions / Track A if any unexhausted path emerges with evidence) is the ONLY open priority. DO HEAVY WORK.**

### VERIFICATION
`python -m unittest discover -s tests -v` (must pass)
