# Agent Handoff — Funding-Conditioned Volatility and Liquidation Risk

Updated: 2026-10-26
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
- Funding-correction survival replication: IMPLEMENTED (scripts/funding_correction_replication.py; tests/test_funding_correction_replication.py 4/4 passed). Replication is PARTIAL - based on pre-specified event definition using rolling percentile thresholds on available funding data; full paper methodology not independently reconstructible from public sources alone. Found 445 funding-extreme events across 5 symbols (Jan-Mar 2024); median correction time 8.0h, mean 12.6h among corrected events.
- Out-of-sample result: RUN (research_state/evaluation_summary.md). Test QLIKE: B0=0.140791 (n=70), B1=0.147800 (n=70), C1=0.145083 (n=70), C2=0.144105 (n=70). Paired block bootstrap (2000 reps): C2 vs B1 mean diff -0.003695 (95% CI [-0.123401,0.158843]), relative reduction 2.50% but CI crosses zero; C1 vs B1 -1.84% (CI crosses zero); C2 vs C1 -0.67%. Gate: does not meet >=2% relative reduction with CI supporting improvement.
- Risk-overlay phase: INELIGIBLE.

## Research gates

- Direct liquidation labels: NOT VERIFIED.
- Synthetic hypothetical mark-price boundary labels: IMPLEMENTED (scripts/synthetic_boundary_labels.py; tests/test_synthetic_boundary_labels.py 5/5 passed).
- Future realized-volatility target: IMPLEMENTED (scripts/forecast_pipeline.py; tests/test_forecast_pipeline.py 7/7 passed).
- Funding-correction replication: IMPLEMENTED/PARTIAL (scripts/funding_correction_replication.py; tests/test_funding_correction_replication.py 4/4 passed).
- Frozen research protocol: FROZEN (research_state/research_protocol.md v1.0); split timestamps frozen.
- Out-of-sample result: RUN (research_state/evaluation_summary.md). Test QLIKE: B0=0.140791 (n=70), B1=0.147800 (n=70), C1=0.145083 (n=70), C2=0.144105 (n=70). Paired block bootstrap (2000 reps): C2 vs B1 mean diff -0.003695 (95% CI [-0.123401,0.158843]), relative reduction 2.50% but CI crosses zero; C1 vs B1 -1.84% (CI crosses zero); C2 vs C1 -0.67%. Gate: does not meet >=2% relative reduction with CI supporting improvement.
- Risk-overlay phase: INELIGIBLE.

## Unresolved blockers

- Direct liquidation labels unavailable.
- Forecast gate not passed (C2 vs B1 +2.50% relative QLIKE reduction but 95% CI [-0.123, 0.159] crosses zero; does not meet practical threshold with supporting uncertainty).

## Highest-value next task

**Investigate and document forecast gate outcome / consider pre-registered alternatives or additional robustness.**
- Review evaluation_summary.md and assess if gate criteria are satisfied per protocol (>=2% relative reduction with interval supporting improvement). If not met, document clearly and do not proceed to risk-overlay phase. Consider pre-registered sensitivity (leave-one-instrument-out, block structure) or report pilot/inconclusive if thresholds unmet.
- Acceptance check: update handoff with gate conclusion and concrete next action; if gate fails, explicitly state risk-overlay remains ineligible and propose any pre-registered follow-up or stop condition.

## Initial task message for next agent

The frozen out-of-sample evaluation has been run and written to research_state/evaluation_summary.md. Primary contrast C2 vs B1 shows +2.50% relative QLIKE reduction on test but 95% block-bootstrap CI crosses zero (-0.123 to 0.159), so the forecast gate is not met. Direct liquidation labels remain unavailable. Risk-overlay phase remains ineligible. Review the evaluation details and protocol requirements, document the gate outcome clearly, and propose the next pre-registered action (or conclude inconclusive per protocol) without modifying splits or tuning on holdout.

At the end of each session, replace this handoff with a concise update that preserves the verified state, summarizes only executed tests and evidence, records unresolved blockers, and names one highest-value next task with an exact acceptance check. Never claim an unexecuted command, unverified source, or incomplete workflow run succeeded.
