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
- Out-of-sample result: NOT RUN.
- Risk-overlay phase: INELIGIBLE.

## Research gates

- Direct liquidation labels: NOT VERIFIED.
- Synthetic hypothetical mark-price boundary labels: IMPLEMENTED (scripts/synthetic_boundary_labels.py; tests/test_synthetic_boundary_labels.py 5/5 passed).
- Future realized-volatility target: IMPLEMENTED (scripts/forecast_pipeline.py; tests/test_forecast_pipeline.py 7/7 passed).
- Funding-correction replication: IMPLEMENTED/PARTIAL (scripts/funding_correction_replication.py; tests/test_funding_correction_replication.py 4/4 passed).
- Frozen research protocol: FROZEN (research_state/research_protocol.md v1.0); split timestamps frozen.
- Out-of-sample result: NOT RUN.
- Risk-overlay phase: INELIGIBLE.

## Unresolved blockers

- Direct liquidation labels unavailable.
- Out-of-sample forecast evaluation not yet run against frozen splits.

## Highest-value next task

**Run frozen out-of-sample forecast evaluation (FCLR-001).**
- Execute forecast pipeline on frozen train/val/test splits with volatility-only baseline and funding/price-feature ablations per frozen protocol.
- Acceptance check: produce evaluation_summary.md with QLIKE metrics for B0/B1/C1/C2, paired comparisons, block bootstrap uncertainty, and gate assessment; all results must use frozen splits only, no tuning on holdout.

## Initial task message for next agent

Run the frozen out-of-sample forecast evaluation per FCLR-001 protocol using frozen splits (train/val/test with 7d embargo). Compute baselines (persistence, HAR-style RV-only) and ablations (funding, funding+price features), report QLIKE with block-bootstrap uncertainty, assess the forecast gate, and update evaluation_summary.md with complete results. Do not tune on holdout or modify splits.

At the end of each session, replace this handoff with a concise update that preserves the verified state, summarizes only executed tests and evidence, records unresolved blockers, and names one highest-value next task with an exact acceptance check. Never claim an unexecuted command, unverified source, or incomplete workflow run succeeded.
