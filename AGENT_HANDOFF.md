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
- Out-of-sample result: RUN (research_state/evaluation_summary.md). Test QLIKE: B0=0.140791 (n=70), B1=0.147800 (n=70), C1=0.145083 (n=70), C2=0.144105 (n=70). Paired block bootstrap (2000 reps): C2 vs B1 mean diff -0.003695 (95% CI [-0.123401,0.158843]), relative reduction 2.50% but CI crosses zero; C1 vs B1 -1.84% (CI crosses zero); C2 vs C1 -0.67%. Gate: does not meet >=2% relative reduction with CI supporting improvement / minimum claim-worthy test requirements.
- Risk-overlay phase: INELIGIBLE.

## Research gates

- Direct liquidation labels: NOT VERIFIED.
- Synthetic hypothetical mark-price boundary labels: IMPLEMENTED (scripts/synthetic_boundary_labels.py; tests/test_synthetic_boundary_labels.py 5/5 passed).
- Future realized-volatility target: IMPLEMENTED (scripts/forecast_pipeline.py; tests/test_forecast_pipeline.py 7/7 passed).
- Funding-correction replication: IMPLEMENTED/PARTIAL (scripts/funding_correction_replication.py; tests/test_funding_correction_replication.py 4/4 passed).
- Frozen research protocol: FROZEN (research_state/research_protocol.md v1.0); split timestamps frozen.
- Out-of-sample result: RUN (research_state/evaluation_summary.md). Gate assessment in research_state/gate_assessment.md: PILOT/INCONCLUSIVE.
- Risk-overlay phase: INELIGIBLE.

## Decision (completed)

**Stop with inconclusive report (option a).** Forecast gate assessed in research_state/gate_assessment.md: C2 vs B1 relative QLIKE reduction 2.50% meets the 2% floor numerically, but 95% CI [-0.123401, 0.158843] crosses zero and test window (2024-03-27..2024-03-30, ~4 days) is a single block vs protocol requirement of >=3 non-overlapping 30-day blocks (>=5 instruments met). Direct liquidation labels remain unavailable. Risk-overlay phase remains INELIGIBLE. No tuning on holdout, no split changes. Chose stop over pre-registering protocol extension because available public data window does not support extending to >=3 non-overlapping 30-day blocks without changing scope beyond what is verifiably available under the constraints (no paid services, no user intervention).

## Unresolved blockers

- Direct liquidation labels unavailable.
- Forecast gate not met (PILOT/INCONCLUSIVE). CI crosses zero; insufficient test blocks per protocol requirements.

## Highest-value next task

**Produce final inconclusive report per protocol.**
- Acceptance check: Create/update a final report summarizing gates, evidence (evaluation_summary.md, gate_assessment.md), blockers, and conclusion (inconclusive; no risk-overlay). State explicitly that forecast improvement did not meet uncertainty/block requirements. Do not modify frozen splits/protocol or tune models. Update handoff to reflect completion state.

## Initial task message for next agent

Forecast gate has been decided as STOP (inconclusive). Evidence: research_state/gate_assessment.md concludes NOT MET (2.50% relative reduction but 95% CI crosses zero, single ~4-day block vs >=3x30-day blocks required). Direct liquidation labels unavailable; risk-overlay remains INELIGIBLE. No tuning on holdout, no split/protocol changes. Produce a final inconclusive report per protocol capturing gates, tests executed, evidence, blockers, and conclusion. Update handoff if needed; no further model changes or OOS extension attempted without new pre-registered protocol and sufficient data.

At the end of each session, replace this handoff with a concise update that preserves the verified state, summarizes only executed tests and evidence, records unresolved blockers, and names one highest-value next task with an exact acceptance check. Never claim an unexecuted command, unverified source, or incomplete workflow run succeeded.
