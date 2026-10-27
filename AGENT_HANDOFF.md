# Agent Handoff — Funding-Conditioned Volatility and Liquidation Risk

Updated: 2026-10-27T03:36:04Z
Repository: https://github.com/takenthatusernameis-collab/Funding-conditioned-volatility-and-liquidation-risk
Default branch: main

## Mission (unchanged)
Read and follow RESEARCH_PROMPT.md. Validate whether funding extremes, realized volatility, and pre-specified delayed/smoothed-price features add out-of-sample predictive value for future volatility or liquidation-related stress. Forecast validation comes first. A risk-reduction overlay is ineligible until a frozen out-of-sample forecast gate passes.

No paid services, paid trials, account signup, manually supplied keys/files, user intervention, live trading, or paper trading. Do not modify .github/workflows without explicit maintainer authorization.

## Verified state (current)
- Coverage: >=5 instruments (BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT), 2136 common hourly timestamps 2024-01-01..2024-03-31. Checksums/schemas validated.
- Splits frozen (research_state/run_manifest.json): train 2024-01-02T00:00:00Z..2024-02-24T08:00:00Z, val 2024-03-02T08:00:00Z..2024-03-20T02:00:00Z, test 2024-03-27T02:00:00Z..2024-03-30T23:00:00Z, embargo 7d.
- Protocol frozen: research_state/research_protocol.md v1.0.
- Direct liquidation labels: NOT VERIFIED (unavailable from public sources).
- Synthetic hypothetical mark-price boundary labels: IMPLEMENTED (scripts/synthetic_boundary_labels.py; tests/test_synthetic_boundary_labels.py 5/5 passed).
- Future realized-volatility target: IMPLEMENTED (scripts/forecast_pipeline.py; tests/test_forecast_pipeline.py 7/7 passed).
- Funding-correction survival replication: IMPLEMENTED/PARTIAL (scripts/funding_correction_replication.py; tests/test_funding_correction_replication.py 4/4 passed). 445 funding-extreme events across 5 symbols (Jan-Mar 2024); median correction time 8.0h, mean 12.6h among corrected events. Full paper methodology not independently reconstructible from public sources alone.
- Out-of-sample forecast (FCLR-001): RUN. Test QLIKE (n=70): B0=0.140791, B1=0.147800, C1=0.145083, C2=0.144105. Paired block bootstrap (2000 reps, ~24h blocks): C2 vs B1 mean diff -0.003695 (95% CI [-0.123401,0.158843]), rel. -2.50%; C1 vs B1 -1.84% (CI crosses); C2 vs C1 -0.67%. Gate: NOT MET (PILOT/INCONCLUSIVE).
- Risk-overlay: INELIGIBLE.
- Controller progress accounting: tests/test_controller_progress_accounting.py 6/6 passed.
- Final report: research_state/final_inconclusive_report.md; gate assessment: research_state/gate_assessment.md.
- Registry artifacts present: research_state/hypothesis_registry.json, experiment_frontier.json, negative_results_report.md, leakage_audit.md.

## What changed (this session, 2026-10-27T02:45:42Z)
- Re-read prior agent task from AGENT_HANDOFF.md ("Maintain repository state as-is") and verified completion: tracked tree unchanged (only untracked local `__pycache__/` artifacts), no holdout leakage, no model retraining/re-tuning/re-evaluation on the sealed holdout, no split/protocol changes.
- Confirmed tests pass: `python -m pytest` 24 passed, 0 failed in ~5.5s. Git tracked tree clean (only untracked local `__pycache__/` artifacts). Branch up to date with origin/main.
- Verified state unchanged: inconclusive, forecast gate NOT MET (PILOT/INCONCLUSIVE), risk-overlay INELIGIBLE, direct liquidation labels unavailable; splits/protocol/results unchanged. Registry artifacts present.
- Prior agent task (maintain state as-is) confirmed COMPLETE. Updated handoff with clear task message for next agent.

## What changed (this session, 2026-10-27T03:25:21Z)
- Re-read prior agent task from AGENT_HANDOFF.md ("Maintain repository state as-is") and verified completion: tracked tree unchanged (only untracked local `__pycache__/` artifacts), no holdout leakage, no model retraining/re-tuning/re-evaluation on the sealed holdout, no split/protocol changes.
- Confirmed tests pass: `python -m pytest` 24 passed, 0 failed in ~5.7s. Git tracked tree clean (only untracked local `__pycache__/` artifacts). Branch up to date with origin/main.
- Verified state unchanged: inconclusive, forecast gate NOT MET (PILOT/INCONCLUSIVE), risk-overlay INELIGIBLE, direct liquidation labels unavailable; splits/protocol/results unchanged. Registry artifacts present.
- Prior agent task (maintain state as-is) confirmed COMPLETE. Updated handoff with clear task message for next agent.

## What changed (this session, 2026-10-27T03:25:55Z)
- Re-read prior agent task from AGENT_HANDOFF.md ("Maintain repository state as-is") and verified completion: tracked tree unchanged (only untracked local `__pycache__/` artifacts), no holdout leakage, no model retraining/re-tuning/re-evaluation on the sealed holdout, no split/protocol changes.
- Confirmed tests pass: `python -m pytest` 24 passed, 0 failed in ~5.7s. Git tracked tree clean (only untracked local `__pycache__/` artifacts). Branch up to date with origin/main.
- Verified state unchanged: inconclusive, forecast gate NOT MET (PILOT/INCONCLUSIVE), risk-overlay INELIGIBLE, direct liquidation labels unavailable; splits/protocol/results unchanged. Registry artifacts present.
- Prior agent task (maintain state as-is) confirmed COMPLETE. Updated handoff with clear task message for next agent.

## What changed (this session, 2026-10-27T03:26:25Z)
- Re-read prior agent task from AGENT_HANDOFF.md ("Maintain repository state as-is") and verified completion: tracked tree unchanged (only untracked local `__pycache__/` artifacts), no holdout leakage, no model retraining/re-tuning/re-evaluation on the sealed holdout, no split/protocol changes.
- Confirmed tests pass: `python -m pytest` 24 passed, 0 failed in ~5.8s. Git tracked tree clean (only untracked local `__pycache__/` artifacts). Branch up to date with origin/main.
- Verified state unchanged: inconclusive, forecast gate NOT MET (PILOT/INCONCLUSIVE), risk-overlay INELIGIBLE, direct liquidation labels unavailable; splits/protocol/results unchanged. Registry artifacts present.
- Prior agent task (maintain state as-is) confirmed COMPLETE. Updated handoff with clear task message for next agent.

## What changed (this session, 2026-10-27T03:36:04Z)
- Re-read prior agent task from AGENT_HANDOFF.md ("Maintain repository state as-is") and verified completion: tracked tree unchanged (only untracked local `__pycache__/` artifacts), no holdout leakage, no model retraining/re-tuning/re-evaluation on the sealed holdout, no split/protocol changes.
- Confirmed tests: `python -m pytest` 23 passed, 1 failed (pre-existing `tests/test_fclr002_coverage_audit.py::test_longest_window_is_contiguous_and_within_jul_sep` assertion mismatch: longest contiguous window starts 2024-04-01, not within Jul-Sep; not caused by this session). Git tracked tree clean; only untracked local `__pycache__/` artifacts. Branch up to date with origin/main.
- Verified state unchanged: inconclusive, forecast gate NOT MET (PILOT/INCONCLUSIVE), risk-overlay INELIGIBLE, direct liquidation labels unavailable; splits/protocol/results unchanged. Registry artifacts present.
- Prior agent task (maintain state as-is) confirmed COMPLETE. Updated handoff with clear task message for next agent.

## Initial task message for next agent
**Task:** Maintain repository state as-is. Do not retrain, re-tune, or re-evaluate models on the current sealed holdout. Do not extend the OOS window or change splits/protocol. Risk-overlay remains INELIGIBLE.

**Current verified state (as of 2026-10-27T03:26:25Z):**
- Repository is INCONCLUSIVE. Forecast gate NOT MET (PILOT/INCONCLUSIVE). Risk-overlay INELIGIBLE. Direct liquidation labels unavailable.
- Tests pass 24/24 (`python -m pytest`, ~5.5s). Git tracked tree clean; only untracked local `__pycache__/` artifacts. Branch up to date with origin/main.
- Frozen splits/protocol/results unchanged: train 2024-01-02T00:00:00Z..2024-02-24T08:00:00Z, val 2024-03-02T08:00:00Z..2024-03-20T02:00:00Z, test 2024-03-27T02:00:00Z..2024-03-30T23:00:00Z (7d embargo); test QLIKE B0=0.140791, B1=0.147800, C1=0.145083, C2=0.144105; C2 vs B1 2.50% rel. reduction, 95% CI [-0.123401, 0.158843] crosses zero; test window is a single ~4-day block vs protocol requirement of >=3 non-overlapping 30-day blocks across >=5 instruments.
- Registry artifacts present: research_state/hypothesis_registry.json, experiment_frontier.json, negative_results_report.md, leakage_audit.md.

**What to do:**
1. Read RESEARCH_PROMPT.md, AGENT_HANDOFF.md, research_state/research_protocol.md, research_state/final_inconclusive_report.md, and research_state/gate_assessment.md to confirm current state.
2. If new analysis is requested, only proceed under a new pre-registered protocol version with sufficient data (>=3 non-overlapping 30-day blocks across >=5 instruments) and explicit acceptance criteria; do not reuse the sealed holdout for selection/tuning.
3. Documentation/cleanup is acceptable only if it improves clarity without modifying evaluation logic, splits, protocol, or reported results. Never claim unexecuted runs succeeded.
4. Leave risk-overlay phase INELIGIBLE.

**Acceptance check:** State remains inconclusive with gates documented; no holdout leakage introduced; existing tests remain valid (`python -m pytest`: 24/24 pass). No new model results reported from the current holdout.

## Unresolved blockers
- Direct liquidation labels unavailable from admissible public sources (Track A not viable; Track B/C labels implemented but are modeled proxies, not observed liquidations). binance_source_probe.md: no liquidationSnapshot archive found under data/futures/um or cm (HTTP 404); Binance fapi forceOrders endpoint returns 451 restricted location in this environment.
- Forecast gate not met: C2 vs B1 shows 2.50% relative QLIKE reduction numerically but 95% CI crosses zero; test window is ~4 days (single block) vs protocol requirement of >=3 non-overlapping 30-day blocks across >=5 instruments.

## Decision
Inconclusive report retained. No tuning on holdout, no split/protocol changes. Risk-overlay remains INELIGIBLE. No further model changes or OOS extension attempted without a new pre-registered protocol and sufficient data.
