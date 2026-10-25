# Agent Handoff — Funding-Conditioned Volatility and Liquidation Risk

Updated: 2026-10-25
Repository: https://github.com/takenthatusernameis-collab/Funding-conditioned-volatility-and-liquidation-risk
Default branch: main

## Mission

Read and follow RESEARCH_PROMPT.md. Validate whether funding extremes, realized volatility, and pre-specified delayed/smoothed-price features add out-of-sample predictive value for future volatility or liquidation-related stress. Forecast validation comes first. A risk-reduction overlay is ineligible until a frozen out-of-sample forecast gate passes.

No paid services, paid trials, account signup, manually supplied keys/files, user intervention, live trading, or paper trading. Do not modify .github/workflows without explicit maintainer authorization.

## Current verified state

- Coverage audit extended to >=5 instruments (BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT) with paired daily archives across 2024-01-01..2024-03-31 (2136 common hourly timestamps). All checksums verified, schemas validated, normalized to UTC; gaps recorded in coverage_audit_multi.
- Split boundaries frozen in research_state/research_protocol.md section 6 and research_state/run_manifest.json (train 2024-01-02T00:00:00Z..2024-02-24T08:00:00Z, val 2024-03-02T08:00:00Z..2024-03-20T02:00:00Z, test 2024-03-27T02:00:00Z..2024-03-30T23:00:00Z, embargo 7d).
- Protocol still frozen; splits now frozen.
- Controller progress accounting script present; tests 6/6 passed.
- Direct liquidation labels: NOT VERIFIED.
- Synthetic hypothetical mark-price boundary labels: NOT IMPLEMENTED.
- Future realized-volatility target: NOT IMPLEMENTED.
- Funding-correction survival replication: NOT IMPLEMENTED.
- Out-of-sample result: NOT RUN.
- Risk-overlay phase: INELIGIBLE.

## Research gates

- Direct actual liquidation labels: NOT VERIFIED.
- Synthetic hypothetical mark-price boundary labels: NOT IMPLEMENTED.
- Future realized-volatility target: NOT IMPLEMENTED.
- Funding-correction survival replication: NOT IMPLEMENTED.
- Frozen research protocol: FROZEN (research_state/research_protocol.md v1.0); split timestamps frozen.
- Out-of-sample result: NOT RUN.
- Risk-overlay phase: INELIGIBLE.

## Unresolved blockers

- Only coverage/splits frozen; targets/features/pipeline not yet implemented.
- Direct liquidation labels unavailable.

## Highest-value next task

**Implement future realized-volatility target and build the forecast pipeline skeleton.**
- Implement next-24h realized variance target from mark-price hourly returns per protocol (section 2), with proper alignment (outcome from t+1..t+24), no leakage.
- Implement frozen predictors (RV1h/RV24h/RV168h, signed funding, funding extremeness 90d past-only, premium, mark/EMA24) with training-only standardization/scaling.
- Build data loader over frozen splits with 7-day embargo enforcement and common panel.
- Acceptance check: unit tests for target construction and leakage checks pass; pipeline can load frozen splits and produce features/targets on a small slice without computing final OOS results. No promotion to risk-overlay phase.

## Initial task message for next agent

Implement future realized-volatility target and build the forecast pipeline skeleton. Compute next-24h realized variance of mark-price returns (sum of squared log returns over t+1..t+24) using markPriceKlines close, with strict causal alignment. Implement frozen predictors (RV1h/RV24h/RV168h, signed funding, 90d past-only absolute funding percentile, premium mark/index, mark/EMA24), training-only standardization, missing-data handling per protocol. Enforce frozen splits and 7-day embargo. Add leakage/unit tests. Acceptance: tests pass; loader works on frozen splits with no target outcomes promoted.

At the end of each session, replace this handoff with a concise update that preserves the verified state, summarizes only executed tests and evidence, records unresolved blockers, and names one highest-value next task with an exact acceptance check. Never claim an unexecuted command, unverified source, or incomplete workflow run succeeded.
