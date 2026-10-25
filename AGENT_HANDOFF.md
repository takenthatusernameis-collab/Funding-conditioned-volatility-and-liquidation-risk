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
- Synthetic hypothetical mark-price boundary labels: IMPLEMENTED (scripts/synthetic_boundary_labels.py; tests/test_synthetic_boundary_labels.py 5/5 passed).
- Future realized-volatility target: IMPLEMENTED (scripts/forecast_pipeline.py + tests/test_forecast_pipeline.py, 7/7 passed).
- Funding-correction survival replication: NOT IMPLEMENTED.
- Out-of-sample result: NOT RUN.
- Risk-overlay phase: INELIGIBLE.

## Research gates

- Direct actual liquidation labels: NOT VERIFIED.
- Synthetic hypothetical mark-price boundary labels: IMPLEMENTED (scripts/synthetic_boundary_labels.py; tests/test_synthetic_boundary_labels.py 5/5 passed).
- Future realized-volatility target: IMPLEMENTED (scripts/forecast_pipeline.py; tests/test_forecast_pipeline.py 7/7 passed).
- Funding-correction survival replication: NOT IMPLEMENTED.
- Frozen research protocol: FROZEN (research_state/research_protocol.md v1.0); split timestamps frozen.
- Out-of-sample result: NOT RUN.
- Risk-overlay phase: INELIGIBLE.

## Unresolved blockers

- Direct liquidation labels unavailable.
- Funding-correction survival replication not yet implemented.

## Highest-value next task

**Implement funding-correction survival replication.**
- Reconstruct funding-extreme events and time-to-correction from admissible public data; compare high vs low realized-volatility conditions; report partial if exact methodology unavailable.
- Acceptance check: unit tests verify event definition and survival timing; script runs on small slice without leakage.

## Initial task message for next agent

Implement funding-correction survival replication with pre-specified event definition and unit tests; state partial if exact methodology unavailable.

At the end of each session, replace this handoff with a concise update that preserves the verified state, summarizes only executed tests and evidence, records unresolved blockers, and names one highest-value next task with an exact acceptance check. Never claim an unexecuted command, unverified source, or incomplete workflow run succeeded.
