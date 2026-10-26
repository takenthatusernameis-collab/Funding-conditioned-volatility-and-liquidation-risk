# Agent Handoff — Funding-Conditioned Volatility and Liquidation Risk

Updated: 2026-10-26T01:05:00Z
Repository: https://github.com/takenthatusernameis-collab/Funding-conditioned-volatility-and-liquidation-risk
Default branch: main

## Mission (unchanged)
Read and follow RESEARCH_PROMPT.md. Validate whether funding extremes, realized volatility, and pre-specified delayed/smoothed-price features add out-of-sample predictive value for future volatility or liquidation-related stress. Forecast validation comes first. A risk-reduction overlay is ineligible until a frozen out-of-sample forecast gate passes.

No paid services, paid trials, account signup, manually supplied keys/files, user intervention, live trading, or paper trading. Do not modify .github/workflows without explicit maintainer authorization.

## Verified state (current)
- Coverage: >=5 instruments (BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT), 2136 common hourly timestamps 2024-01-01..2024-03-31. Checksums/schemas validated; gaps in coverage_audit_multi.
- Splits frozen (research_state/run_manifest.json): train 2024-01-02T00:00:00Z..2024-02-24T08:00:00Z, val 2024-03-02T08:00:00Z..2024-03-20T02:00:00Z, test 2024-03-27T02:00:00Z..2024-03-30T23:00:00Z, embargo 7d.
- Protocol frozen: research_state/research_protocol.md v1.0.
- Direct liquidation labels: NOT VERIFIED (unavailable from public sources).
- Synthetic hypothetical mark-price boundary labels: IMPLEMENTED (scripts/synthetic_boundary_labels.py; tests/test_synthetic_boundary_labels.py 5/5 passed).
- Future realized-volatility target: IMPLEMENTED (scripts/forecast_pipeline.py; tests/test_forecast_pipeline.py 7/7 passed).
- Funding-correction survival replication: IMPLEMENTED/PARTIAL (scripts/funding_correction_replication.py; tests/test_funding_correction_replication.py 4/4 passed). 445 funding-extreme events across 5 symbols (Jan-Mar 2024); median correction time 8.0h, mean 12.6h among corrected events. Full paper methodology not independently reconstructible from public sources alone.
- Out-of-sample forecast: RUN. Test QLIKE (n=70): B0=0.140791, B1=0.147800, C1=0.145083, C2=0.144105. Paired block bootstrap (2000 reps, ~24h blocks): C2 vs B1 mean diff -0.003695 (95% CI [-0.123401,0.158843]), rel. -2.50%; C1 vs B1 -1.84% (CI crosses); C2 vs C1 -0.67%. Gate: NOT MET (PILOT/INCONCLUSIVE).
- Risk-overlay: INELIGIBLE.
- Controller progress accounting: tests/test_controller_progress_accounting.py 6/6 passed.
- Final report: research_state/final_inconclusive_report.md; gate assessment: research_state/gate_assessment.md.

## Decision
Stop with inconclusive report (option a). No tuning on holdout, no split/protocol changes. Risk-overlay remains ineligible.

## Unresolved blockers
- Direct liquidation labels unavailable from admissible public sources.
- Forecast gate not met: C2 vs B1 shows 2.50% relative QLIKE reduction numerically but 95% CI crosses zero; test window is ~4 days (single block) vs protocol requirement of >=3 non-overlapping 30-day blocks across >=5 instruments.

## Initial task message for next agent
**Task:** Maintain repository state as-is. Do not retrain, re-tune, or re-evaluate models on the current holdout. Do not extend the OOS window or change splits/protocol.

**What to do (if anything):**
1. Read RESEARCH_PROMPT.md, this handoff, research_state/final_inconclusive_report.md, and research_state/gate_assessment.md to confirm current state.
2. If asked to produce any new analysis, only do so under a new pre-registered protocol (new version) with sufficient data (>=3 non-overlapping 30-day blocks, >=5 instruments) and explicit acceptance criteria; do not reuse the sealed holdout for selection/tuning.
3. Documentation/cleanup is acceptable if it improves clarity without modifying evaluation logic, splits, or protocol. Never claim unexecuted runs succeeded.
4. Leave risk-overlay phase INELIGIBLE.

**Acceptance check:** State remains inconclusive with gates documented; no holdout leakage introduced; tests still pass (or document if environment changed). No new model results reported from current holdout.
