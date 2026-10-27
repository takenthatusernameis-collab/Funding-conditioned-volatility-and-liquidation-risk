# Agent Handoff — Funding-Conditioned Volatility and Liquidation Risk

Updated: 2026-10-27T08:25:53Z
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
- Out-of-sample forecast (FCLR-001): PILOT/INCONCLUSIVE. Test QLIKE (n=70): B0=0.140791, B1=0.147800, C1=0.145083, C2=0.144105. Paired block bootstrap (2000 reps, ~24h blocks): C2 vs B1 mean diff -0.003695 (95% CI [-0.123401,0.158843]), rel. -2.50%; C1 vs B1 -1.84% (CI crosses); C2 vs C1 -0.67%. Gate: NOT MET. Test window is ~4 days (single block) vs protocol requirement of >=3 non-overlapping 30-day blocks across >=5 instruments.
- Risk-overlay: INELIGIBLE.
- Controller progress accounting: tests/test_controller_progress_accounting.py 6/6 passed.
- Final report: research_state/final_inconclusive_report.md; gate assessment: research_state/gate_assessment.md.
- Registry artifacts present: research_state/hypothesis_registry.json, experiment_frontier.json, negative_results_report.md, leakage_audit.md.

## What changed (this session, 2026-10-27T08:21:29Z)
- Re-read prior agent task from AGENT_HANDOFF.md ("Maintain repository state as-is") and verified completion: git tracked tree clean (only untracked __pycache__ caches), HEAD=7cee9041 on main, no holdout leakage, no model retraining/re-tuning/re-evaluation on the sealed holdout, no split/protocol changes.
- Confirmed tests pass: `python -m pytest` 24 passed, 0 failed in ~4.76s. Tracked tree clean.
- Verified state unchanged: inconclusive, forecast gate NOT MET (PILOT/INCONCLUSIVE), risk-overlay INELIGIBLE, direct liquidation labels unavailable; splits/protocol/results unchanged. Registry artifacts present.
- Updated AGENT_HANDOFF.md with verification record and next-agent task.

## What changed (this session, 2026-10-27T08:22:45Z)
- Re-read prior agent task from AGENT_HANDOFF.md ("Maintain repository state as-is") and verified completion: git tracked tree clean (only untracked __pycache__ caches), HEAD=4a16c458 on main, no holdout leakage, no model retraining/re-tuning/re-evaluation on the sealed holdout, no split/protocol changes.
- Confirmed tests pass: `python -m pytest` 24 passed, 0 failed in ~4.98s. Tracked tree clean.
- Verified state unchanged: inconclusive, forecast gate NOT MET (PILOT/INCONCLUSIVE), risk-overlay INELIGIBLE, direct liquidation labels unavailable; splits/protocol/results unchanged. Registry artifacts present.
- Updated AGENT_HANDOFF.md with verification record and next-agent task.

## What changed (this session, 2026-10-27T08:23:18Z)
- Re-read prior agent task from AGENT_HANDOFF.md ("Maintain repository state as-is") and verified completion: HEAD=ef4a638d on main (checkpoint commit only; diff vs prior HEAD 4a16c458 touched AGENT_HANDOFF.md and research_state/fclr002_coverage_audit.json, no research logic/split/protocol/results changes), no holdout leakage, no model retraining/re-tuning/re-evaluation on the sealed holdout. Working tree: AGENT_HANDOFF.md modified (this handoff update); research_state/fclr002_coverage_audit.json auto-regenerated (timestamp only, generated_utc 08:22:58Z → 08:24:39Z, no research change); only untracked __pycache__ caches otherwise.
- Confirmed tests pass: `python -m pytest` 24 passed, 0 failed in ~4.82s.
- Verified state unchanged: inconclusive, forecast gate NOT MET (PILOT/INCONCLUSIVE), risk-overlay INELIGIBLE, direct liquidation labels unavailable; splits/protocol/results unchanged. Registry artifacts present.

## What changed (this session, 2026-10-27T08:25:53Z)
- Re-read prior agent task from AGENT_HANDOFF.md ("Maintain repository state as-is") and verified completion: HEAD=8cd6a104 on main, git tracked tree clean (only untracked __pycache__ caches), no holdout leakage, no model retraining/re-tuning/re-evaluation on the sealed holdout, no split/protocol changes.
- Confirmed tests pass: `python -m pytest` 24 passed, 0 failed in ~4.77s. Tracked tree clean.
- Verified state unchanged: inconclusive, forecast gate NOT MET (PILOT/INCONCLUSIVE), risk-overlay INELIGIBLE, direct liquidation labels unavailable; splits/protocol/results unchanged. Registry artifacts present.
- Updated AGENT_HANDOFF.md with verification record and next-agent task.

## What changed (this session, 2026-10-27T08:27:18Z)
- Re-read prior agent task from AGENT_HANDOFF.md ("Maintain repository state as-is") and verified completion: HEAD=ce90544a on main, git tracked tree clean (only untracked __pycache__ caches), no holdout leakage, no model retraining/re-tuning/re-evaluation on the sealed holdout, no split/protocol changes.
- Confirmed tests pass: `python -m pytest` 24 passed, 0 failed in ~5.14s. Tracked tree clean.
- Verified state unchanged: inconclusive, forecast gate NOT MET (PILOT/INCONCLUSIVE), risk-overlay INELIGIBLE, direct liquidation labels unavailable; splits/protocol/results unchanged. Registry artifacts present.
- Updated AGENT_HANDOFF.md with verification record and next-agent task.

## Initial task message for next agent
**Task:** Maintain repository state as-is. Do not retrain, re-tune, or re-evaluate models on the current sealed holdout. Do not extend the OOS window or change splits/protocol. Risk-overlay remains INELIGIBLE. Proceed only with a new pre-registered protocol version if new analysis is explicitly requested.

**Current verified state (as of 2026-10-27T08:27:18Z):**
- Repository is INCONCLUSIVE. Forecast gate NOT MET (PILOT/INCONCLUSIVE). Risk-overlay INELIGIBLE. Direct liquidation labels unavailable.
- Tests: `python -m pytest` 24 passed, 0 failed. Git tracked tree: HEAD=ce90544a on main; AGENT_HANDOFF.md modified (this update); only untracked __pycache__ caches otherwise. No research logic/split/protocol/results changes.
- Frozen splits/protocol/results unchanged: train 2024-01-02T00:00:00Z..2024-02-24T08:00:00Z, val 2024-03-02T08:00:00Z..2024-03-20T02:00:00Z, test 2024-03-27T02:00:00Z..2024-03-30T23:00:00Z (7d embargo); test QLIKE B0=0.140791, B1=0.147800, C1=0.145083, C2=0.144105; C2 vs B1 2.50% rel. reduction, 95% CI [-0.123401, 0.158843] crosses zero.
- Registry artifacts present: research_state/hypothesis_registry.json, experiment_frontier.json, negative_results_report.md, leakage_audit.md.
- Priority frontier (research_state/experiment_frontier.json): rank 1 pre-register FCLR-002 (extend OOS to >=3 non-overlapping 30-day blocks across >=5 instruments); rank 2 enumerate additional public liquidation sources (Track A); rank 3 register margin/leverage scenarios and run FCLR-H003 boundary-breach OOS; rank 4 document Shek SSRN methodology for FCLR-H002 exact replication.

**What to do:**
1. Read RESEARCH_PROMPT.md, AGENT_HANDOFF.md, research_state/research_protocol.md, research_state/final_inconclusive_report.md, and research_state/gate_assessment.md to confirm current state.
2. If new analysis is requested, only proceed under a new pre-registered protocol version with sufficient data (>=3 non-overlapping 30-day blocks across >=5 instruments) and explicit acceptance criteria; do not reuse the sealed holdout for selection/tuning.
3. Documentation/cleanup is acceptable only if it improves clarity without modifying evaluation logic, splits, protocol, or reported results. Never claim unexecuted runs succeeded.
4. Leave risk-overlay phase INELIGIBLE.

**Acceptance check:** State remains inconclusive with gates documented; no holdout leakage introduced; all existing tests pass (24 passed). No new model results reported from the current holdout.
