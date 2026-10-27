# Agent Handoff — Funding-Conditioned Volatility and Liquidation Risk

Updated: 2026-10-27T13:20:20Z
Repository: https://github.com/takenthatusernameis-collab/Funding-conditioned-volatility-and-liquidation-risk
Default branch: main

## Mission (unchanged)

Read and follow RESEARCH_PROMPT.md. Validate whether funding extremes, realized volatility, and pre-specified delayed/smoothed-price features add out-of-sample predictive value for future volatility or liquidation-related stress. Forecast validation comes first. A risk-reduction overlay is ineligible until a frozen out-of-sample forecast gate passes.

No paid services, paid trials, account signup, manually supplied keys/files, user intervention, live trading, or paper trading. Do not modify .github/workflows without explicit maintainer authorization.

## Prior agent task — COMPLETED (verified this session, 2026-10-27T13:20:20Z)

Task: Read the prior agent task from the durable handoff and complete it. Then update the handoff and write a clear initial task message for the next agent.

Verification (this session, 2026-10-27T13:20:20Z):
- `git log --oneline -3`: b3dd0c7d, ce22e8ee, 9418b2cf (HEAD at b3dd0c7d).
- `git status --short`: clean tracked tree; only untracked scripts/__pycache__/ and tests/__pycache__/ caches (no tracked changes).
- `python -m pytest -q`: 25 passed, 0 failed in ~4.55s.
- Confirmed handoff/registry/state: repo INCONCLUSIVE (PILOT/INCONCLUSIVE), forecast gate NOT MET, risk-overlay INELIGIBLE, FCLR-001 frozen, no holdout leakage; FCLR-002 coverage sufficient but unexecuted/not authorized.
- Updated AGENT_HANDOFF.md timestamp and verification above; initial task message retained for next agent.

## Current verified state

- Repository status: INCONCLUSIVE. Forecast gate NOT MET (PILOT/INCONCLUSIVE). Risk-overlay phase INELIGIBLE. Direct liquidation labels unavailable (Track A BLOCKED).
- Frozen protocol: research_state/research_protocol.md v1.0 (FCLR-001).
- Frozen splits (research_state/run_manifest.json): train 2024-01-02T00:00:00Z..2024-02-24T08:00:00Z; val 2024-03-02T08:00:00Z..2024-03-20T02:00:00Z; test 2024-03-27T02:00:00Z..2024-03-30T23:00:00Z; 7-day embargo.
- Test QLIKE (n=70): B0=0.140791, B1=0.147800, C1=0.145083, C2=0.144105. C2 vs B1: -2.50% rel, 95% CI [-0.123401, 0.158843] crosses zero; single ~4-day block vs requirement >=3 non-overlapping 30-day blocks; multiplicity not satisfied.
- Implementation: forecast pipeline (7/7), synthetic boundary labels (5/5), funding-correction replication partial (4/4; 445 events, median 8.0h). Controller progress accounting 6/6.
- Registry: hypothesis_registry.json, experiment_frontier.json, negative_results_report.md, leakage_audit.md, gate_assessment.md, final_inconclusive_report.md present.
- FCLR-002: coverage audit shows 5 symbols (BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT), 4392 common hourly timestamps, contiguous window 2024-04-01T00:00:00Z..2024-09-30T23:00:00Z (~183 days). Coverage sufficient in principle, but NOT executed and holdout NOT opened. scripts/fclr002_download.py idempotent; no network activity performed. Data present in data_cache (4174 zips / 7350 extracted CSVs).

## Initial task message for next agent

**Task:** Maintain repository state as-is. Do not retrain, re-tune, or re-evaluate models on the current sealed holdout (FCLR-001). Do not extend the OOS window or change splits/protocol. Risk-overlay phase remains INELIGIBLE until a frozen out-of-sample forecast gate passes.

FCLR-002 coverage is confirmed sufficient, but FCLR-002 execution is NOT authorized unless explicitly requested with a pre-registered protocol version (FCLR-002 v1.0) specifying splits/acceptance criteria BEFORE computing any outcomes. Do not run scripts/fclr002_download.py or scripts/fclr002_coverage_audit.py unless explicitly instructed.

**What to do:**
1. Read RESEARCH_PROMPT.md, AGENT_HANDOFF.md, research_state/research_protocol.md, research_state/final_inconclusive_report.md, research_state/gate_assessment.md to confirm current state.
2. Confirm repository remains in verified state: clean tracked tree (or only untracked caches), all tests pass (25 passed), no holdout leakage introduced.
3. If FCLR-002 is explicitly requested, first pre-register a new protocol version (FCLR-002 v1.0) with split/acceptance criteria BEFORE computing any outcomes; run walk-forward evaluation on 2024-04..2024-09 panel; run leakage audit on new panel before opening its holdout. Do not reuse the FCLR-001 sealed holdout for selection/tuning.
4. Documentation/cleanup acceptable only if it improves clarity without modifying evaluation logic, splits, protocol, or reported results. Never claim unexecuted runs succeeded.
5. Leave risk-overlay phase INELIGIBLE.

**Acceptance check:** State remains inconclusive with gates documented; no holdout leakage introduced; all existing tests pass (25 passed). No new model results reported from the current holdout. HEAD unchanged except for authorized checkpoint/documentation commits.
