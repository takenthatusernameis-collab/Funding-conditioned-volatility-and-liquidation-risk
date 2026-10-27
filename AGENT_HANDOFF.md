# Agent Handoff — Funding-Conditioned Volatility and Liquidation Risk

Updated: 2026-10-27T13:09:17Z
Repository: https://github.com/takenthatusernameis-collab/Funding-conditioned-volatility-and-liquidation-risk
Default branch: main

## Mission (unchanged)

Read and follow RESEARCH_PROMPT.md. Validate whether funding extremes, realized volatility, and pre-specified delayed/smoothed-price features add out-of-sample predictive value for future volatility or liquidation-related stress. Forecast validation comes first. A risk-reduction overlay is ineligible until a frozen out-of-sample forecast gate passes.

No paid services, paid trials, account signup, manually supplied keys/files, user intervention, live trading, or paper trading. Do not modify .github/workflows without explicit maintainer authorization.

## Prior agent task — COMPLETED (verified this session, 2026-10-27T13:09:17Z)

Task: Maintain repository state as-is. Do not retrain, re-tune, or re-evaluate models on the current sealed holdout (FCLR-001). Do not extend the OOS window or change splits/protocol. Risk-overlay phase INELIGIBLE.

Verification (this session, 2026-10-27T13:09:17Z):
- `git status --short`: tracked tree clean; only untracked scripts/__pycache__/ and tests/__pycache__/ caches.
- HEAD: e85a3958 (chore(kilo): checkpoint agent session), branch main. Diff vs previously recorded 7f6c52cf touches AGENT_HANDOFF.md only (timestamp + wording); no holdout/model/split/protocol/results changes.
- `python -m pytest -q`: 25 passed, 0 failed in ~4.36s.
- No holdout leakage, no model retraining/re-tuning/re-evaluation on the sealed holdout, no split/protocol/results changes.
- No working-tree drift; research_state/fclr002_coverage_audit.json remains synchronized with HEAD.

## Current verified state

- Repository status: INCONCLUSIVE. Forecast gate NOT MET (PILOT/INCONCLUSIVE). Risk-overlay phase INELIGIBLE. Direct liquidation labels unavailable (Track A BLOCKED).
- Frozen protocol: research_state/research_protocol.md v1.0 (FCLR-001).
- Frozen splits (research_state/run_manifest.json): train 2024-01-02T00:00:00Z..2024-02-24T08:00:00Z; val 2024-03-02T8:00:00Z..2024-03-20T02:00:00Z; test 2024-03-27T02:00:00Z..2024-03-30T23:00:00Z; 7-day embargo.
- Test QLIKE (n=70): B0=0.140791, B1=0.147800, C1=0.145083, C2=0.144105.
- Primary contrast C2 vs B1: relative reduction 2.50% (met numerically), but 95% CI [-0.123401, 0.158843] crosses zero; single ~4-day test block vs protocol requirement of >=3 non-overlapping 30-day blocks across >=5 instruments; multiplicity conditions not satisfied. Gate NOT MET.
- Implementation state: forecast target implemented (tests/test_forecast_pipeline.py 7/7); synthetic hypothetical mark-price boundary labels implemented (tests/test_synthetic_boundary_labels.py 5/5); funding-correction replication implemented/partial (tests/test_funding_correction_replication.py 4/4; 445 events, median correction time 8.0h); controller progress accounting 6/6; fclr002 coverage audit tests added and passing.
- Registry artifacts present: research_state/hypothesis_registry.json, experiment_frontier.json, negative_results_report.md, leakage_audit.md, gate_assessment.md, final_inconclusive_report.md.
- FCLR-002 coverage (research_state/fclr002_coverage_audit.json): 5 symbols (BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT), 4392 common hourly timestamps, single contiguous window 2024-04-01T00:00:00Z..2024-09-30T23:00:00Z (~183 days). Satisfies the minimum claim-worthy data requirement (>=5 instruments, >=3 non-overlapping 30-day blocks), but FCLR-002 has NOT been executed and its holdout has NOT been opened. scripts/fclr002_download.py is idempotent (skips existing files); data_cache holds 4174 zips / 7350 extracted CSVs. No network activity performed this session.

## Initial task message for next agent

**Task:** Maintain repository state as-is. Do not retrain, re-tune, or re-evaluate models on the current sealed holdout (FCLR-001). Do not extend the OOS window or change splits/protocol. Risk-overlay phase remains INELIGIBLE until a frozen out-of-sample forecast gate passes. FCLR-002 coverage is confirmed sufficient but FCLR-002 execution is NOT authorized unless explicitly requested with a pre-registered protocol version. Do not run scripts/fclr002_download.py or scripts/fclr002_coverage_audit.py unless explicitly instructed.

**What to do:**
1. Read RESEARCH_PROMPT.md, AGENT_HANDOFF.md, research_state/research_protocol.md, research_state/final_inconclusive_report.md, and research_state/gate_assessment.md to confirm current state.
2. Confirm the repository remains in the verified state below (clean tracked tree, all tests pass, no holdout leakage introduced).
3. If FCLR-002 is explicitly requested, first pre-register a new protocol version (FCLR-002 v1.0) with split/acceptance criteria BEFORE computing any outcomes; then run the walk-forward evaluation on the 2024-04..2024-09 panel; then run the leakage audit on the new panel before opening its holdout. Do not reuse the FCLR-001 sealed holdout for selection/tuning.
4. Documentation/cleanup is acceptable only if it improves clarity without modifying evaluation logic, splits, protocol, or reported results. Never claim unexecuted runs succeeded.
5. Leave risk-overlay phase INELIGIBLE.

**Acceptance check:** State remains inconclusive with gates documented; no holdout leakage introduced; all existing tests pass (25 passed). No new model results reported from the current holdout. HEAD unchanged (7f6c52cf) except for authorized checkpoint/documentation commits.

(End of file - total 48 lines)
