# Agent Handoff — Funding-Conditioned Volatility and Liquidation Risk

Updated: 2026-10-27T14:10:31Z
Repository: https://github.com/takenthatusernameis-collab/Funding-conditioned-volatility-and-liquidation-risk
Default branch: main

## Mission (unchanged)

Read and follow RESEARCH_PROMPT.md. Validate whether funding extremes, realized volatility, and pre-specified delayed/smoothed-price features add out-of-sample predictive value for future volatility or liquidation-related stress. Forecast validation comes first. A risk-reduction overlay is ineligible until a frozen out-of-sample forecast gate passes.

No paid services, paid trials, account signup, manually supplied keys/files, user intervention, live trading, or paper trading. Do not modify .github/workflows without explicit maintainer authorization.

## Prior agent task — COMPLETED (re-verified this session, 2026-10-27T14:10:31Z)

Task: Read the prior agent task from the durable handoff and complete it. Then update the handoff and write a clear initial task message for the next agent.

Re-verification (this session, 2026-10-27T14:10:31Z):
- `git log --oneline -3`: 57cce092, 8a65320e, b3dd0c7d (HEAD at 57cce092).
- `git status --short`: clean tracked tree; only untracked scripts/__pycache__/ and tests/__pycache__/ caches (no tracked changes).
- `python -m pytest -q`: 25 passed, 0 failed (~0.9s).
- Confirmed handoff/registry/state: repo INCONCLUSIVE (PILOT/INCONCLUSIVE), forecast gate NOT MET, risk-overlay INELIGIBLE, FCLR-001 frozen, no holdout leakage; FCLR-002 coverage sufficient but unexecuted/not authorized; no model results recomputed on the sealed FCLR-001 holdout.
- AGENT_HANDOFF.md verification and timestamp refreshed; initial task message for next agent retained below.

## Current verified state

- Repository status: INCONCLUSIVE. Forecast gate NOT MET (PILOT/INCONCLUSIVE). Risk-overlay phase INELIGIBLE. Direct liquidation labels unavailable (Track A BLOCKED).
- Frozen protocol: research_state/research_protocol.md v1.0 (FCLR-001).
- Frozen splits (research_state/run_manifest.json): train 2024-01-02T00:00:00Z..2024-02-24T08:00:00Z; val 2024-03-02T08:00:00Z..2024-03-20T02:00:00Z; test 2024-03-27T02:00:00Z..2024-03-30T23:00:00Z; 7-day embargo.
- Test QLIKE (n=70): B0=0.140791, B1=0.147800, C1=0.145083, C2=0.144105. C2 vs B1: -2.50% rel, 95% CI [-0.123401, 0.158843] crosses zero; single ~4-day block vs requirement >=3 non-overlapping 30-day blocks; multiplicity not satisfied.
- Implementation: forecast pipeline (7/7), synthetic boundary labels (5/5), funding-correction replication partial (4/4; 445 events, median 8.0h). Controller progress accounting 6/6.
- Registry: hypothesis_registry.json, experiment_frontier.json, negative_results_report.md, leakage_audit.md, gate_assessment.md, final_inconclusive_report.md present.
- FCLR-002: coverage audit shows 5 symbols (BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT), 4392 common hourly timestamps, contiguous window 2024-04-01T00:00:00Z..2024-09-30T23:00:00Z (~183 days). Coverage sufficient in principle, but NOT executed and holdout NOT opened. scripts/fclr002_download.py idempotent; no network activity performed. Data present in data_cache (4174 zips / 7350 extracted CSVs).

## Initial task message for next agent

**Current state (do not alter):** Repository is INCONCLUSIVE. Forecast gate NOT MET (PILOT/INCONCLUSIVE). Risk-overlay phase INELIGIBLE. Direct liquidation labels unavailable (Track A BLOCKED). Frozen protocol: research_state/research_protocol.md v1.0 (FCLR-001). FCLR-001 sealed holdout must NOT be retrained, re-tuned, or re-evaluated. The OOS window must NOT be extended and splits/protocol must NOT be changed.

**FCLR-002 status:** Coverage audit (research_state/fclr002_coverage_audit.json) confirms 5 instruments (BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT), 4392 common hourly timestamps, contiguous window 2024-04-01T00:00:00Z..2024-09-30T23:00:00Z (~183 days), sufficient in principle for >=3 non-overlapping 30-day blocks. Coverage sufficient, but FCLR-002 execution is NOT authorized unless explicitly requested with a pre-registered protocol version (FCLR-002 v1.0) specifying splits and acceptance criteria BEFORE computing any outcomes. Do not run scripts/fclr002_download.py or scripts/fclr002_coverage_audit.py unless explicitly instructed. Do not reuse the FCLR-001 sealed holdout for selection/tuning.

**What to do:**
1. Read RESEARCH_PROMPT.md, AGENT_HANDOFF.md, research_state/research_protocol.md, research_state/final_inconclusive_report.md, research_state/gate_assessment.md to confirm current state.
2. Confirm repository remains in verified state: clean tracked tree (or only untracked caches), all tests pass (25 passed), no holdout leakage introduced.
3. If FCLR-002 is explicitly requested, first pre-register a new protocol version (FCLR-002 v1.0) with split/acceptance criteria BEFORE computing any outcomes; run walk-forward evaluation on the 2024-04..2024-09 panel; run leakage audit on the new panel before opening its holdout.
4. Documentation/cleanup acceptable only if it improves clarity without modifying evaluation logic, splits, protocol, or reported results. Never claim unexecuted runs succeeded.
5. Leave risk-overlay phase INELIGIBLE.

**Acceptance check:** State remains inconclusive with gates documented; no holdout leakage introduced; all existing tests pass (25 passed). No new model results reported from the current holdout. HEAD unchanged except for authorized checkpoint/documentation commits.
