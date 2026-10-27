# Agent Handoff — Funding-Conditioned Volatility and Liquidation Risk

Updated: 2026-10-27T08:31:06Z
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

## What changed (this session, 2026-10-27T08:28:15Z)
- Re-read prior agent task from AGENT_HANDOFF.md ("Maintain repository state as-is") and verified completion: HEAD=1b675e82 on main, git tracked tree clean (only untracked __pycache__ caches), no holdout leakage, no model retraining/re-tuning/re-evaluation on the sealed holdout, no split/protocol changes.
- Confirmed tests pass: `python -m pytest` 24 passed, 0 failed in ~4.95s. Tracked tree clean.
- Verified state unchanged: inconclusive, forecast gate NOT MET (PILOT/INCONCLUSIVE), risk-overlay INELIGIBLE, direct liquidation labels unavailable; splits/protocol/results unchanged. Registry artifacts present.
- Investigated FCLR-002 coverage feasibility: data_cache holds 4174 zips / 7350 extracted CSVs across BTCUSDT/ETHUSDT/BNBUSDT/SOLUSDT/XRPUSDT for 2024-04..2024-09 (BTCUSDT also has 2024-04..2024-06 from an earlier cache). scripts/fclr002_download.py is idempotent and skips existing files, so it is safe to re-run; it would only fetch missing months (2024-10, 2024-11 for the 4 non-BTC symbols; BTCUSDT 2024-07..2024-11). No new downloads were executed and no network activity was performed. research_state/fclr002_coverage_audit.json regenerated deterministically (timestamp-only drift 08:27:44Z -> 08:28:30Z, no research change); restored to HEAD via `git checkout HEAD --` so tracked tree is byte-identical to the last checkpoint.
- Updated AGENT_HANDOFF.md with verification record and next-agent task.

## What changed (this session, 2026-10-27T08:31:06Z)
- Re-read prior agent task from AGENT_HANDOFF.md ("Maintain repository state as-is") and verified completion: HEAD=b8ea2189 on main, git tracked tree clean (only untracked __pycache__ caches), no holdout leakage, no model retraining/re-tuning/re-evaluation on the sealed holdout, no split/protocol changes.
- Confirmed tests pass: `python -m pytest` 24 passed, 0 failed in ~4.88s. Tracked tree clean.
- Verified state unchanged: inconclusive, forecast gate NOT MET (PILOT/INCONCLUSIVE), risk-overlay INELIGIBLE, direct liquidation labels unavailable; splits/protocol/results unchanged. Registry artifacts present.
- Updated AGENT_HANDOFF.md with verification record and next-agent task.

## Initial task message for next agent
**Task:** Maintain repository state as-is. Do not retrain, re-tune, or re-evaluate models on the current sealed holdout. Do not extend the OOS window or change splits/protocol. Risk-overlay remains INELIGIBLE. FCLR-002 coverage is confirmed sufficient (>=5 instruments, >=3 non-overlapping 30-day blocks feasible from 2024-04..2024-09) but FCLR-002 execution is NOT authorized unless explicitly requested with a pre-registered protocol version. Do not run scripts/fclr002_download.py or scripts/fclr002_coverage_audit.py unless explicitly instructed.

**Current verified state (as of 2026-10-27T08:28:15Z):**
- Repository is INCONCLUSIVE. Forecast gate NOT MET (PILOT/INCONCLUSIVE). Risk-overlay INELIGIBLE. Direct liquidation labels unavailable.
- Tests: `python -m pytest` 24 passed, 0 failed in ~4.95s. Git tracked tree: HEAD=1b675e82 on main; clean (only untracked __pycache__ caches). No research logic/split/protocol/results changes.
- Frozen splits/protocol/results unchanged: train 2024-01-02T00:00:00Z..2024-02-24T08:00:00Z, val 2024-03-02T08:00:00Z..2024-03-20T02:00:00Z, test 2024-03-27T02:00:00Z..2024-03-30T23:00:00Z (7d embargo); test QLIKE B0=0.140791, B1=0.147800, C1=0.145083, C2=0.144105; C2 vs B1 2.50% rel. reduction, 95% CI [-0.123401, 0.158843] crosses zero.
- Registry artifacts present: research_state/hypothesis_registry.json, experiment_frontier.json, negative_results_report.md, leakage_audit.md.
- FCLR-002 coverage (research_state/fclr002_coverage_audit.json @ 08:27:44Z, unchanged since 08:22:58Z): 5 symbols, 4392 common hourly timestamps, single contiguous window 2024-04-01T00:00:00Z..2024-09-30T23:00:00Z (~183 days). This satisfies the protocol's minimum claim-worthy test data requirement (>=5 instruments, >=3 non-overlapping 30-day blocks) but FCLR-002 has NOT been executed and its holdout has NOT been opened. scripts/fclr002_download.py is idempotent (skips existing files); data_cache holds 4174 zips / 7350 extracted CSVs. No network activity was performed this session.

**What to do:**
1. Read RESEARCH_PROMPT.md, AGENT_HANDOFF.md, research_state/research_protocol.md, research_state/final_inconclusive_report.md, and research_state/gate_assessment.md to confirm current state.
2. If FCLR-002 is explicitly requested, first pre-register a new protocol version (FCLR-002 v1.0) with split/acceptance criteria BEFORE computing any outcomes; then run the walk-forward evaluation on the 2024-04..2024-09 panel; then run the leakage audit on the new panel before opening its holdout. Do not reuse the FCLR-001 sealed holdout for selection/tuning.
3. Documentation/cleanup is acceptable only if it improves clarity without modifying evaluation logic, splits, protocol, or reported results. Never claim unexecuted runs succeeded.
4. Leave risk-overlay phase INELIGIBLE.

**Acceptance check:** State remains inconclusive with gates documented; no holdout leakage introduced; all existing tests pass (24 passed). No new model results reported from the current holdout.

## What changed (this session, 2026-10-27T09:17:10Z)
- Re-read prior agent task from AGENT_HANDOFF.md ("Maintain repository state as-is") and verified completion: HEAD=416faf7d on main, git tracked tree clean (only untracked __pycache__ caches), no holdout leakage, no model retraining/re-tuning/re-evaluation on the sealed holdout, no split/protocol changes.
- Confirmed tests pass: `python -m pytest` 24 passed, 0 failed in ~4.74s. Tracked tree clean.
- Verified state unchanged: inconclusive, forecast gate NOT MET (PILOT/INCONCLUSIVE), risk-overlay INELIGIBLE, direct liquidation labels unavailable; splits/protocol/results unchanged. Registry artifacts present.
- Updated AGENT_HANDOFF.md with verification record and next-agent task.

## Initial task message for next agent
**Task:** Maintain repository state as-is. Do not retrain, re-tune, or re-evaluate models on the current sealed holdout. Do not extend the OOS window or change splits/protocol. Risk-overlay remains INELIGIBLE. FCLR-002 coverage is confirmed sufficient (>=5 instruments, >=3 non-overlapping 30-day blocks feasible from 2024-04..2024-09) but FCLR-002 execution is NOT authorized unless explicitly requested with a pre-registered protocol version. Do not run scripts/fclr002_download.py or scripts/fclr002_coverage_audit.py unless explicitly instructed.

**Current verified state (as of 2026-10-27T09:17:10Z):**
- Repository is INCONCLUSIVE. Forecast gate NOT MET (PILOT/INCONCLUSIVE). Risk-overlay INELIGIBLE. Direct liquidation labels unavailable.
- Tests: `python -m pytest` 24 passed, 0 failed in ~4.74s. Git tracked tree: HEAD=416faf7d on main; clean (only untracked __pycache__ caches). No research logic/split/protocol/results changes.
- Frozen splits/protocol/results unchanged: train 2024-01-02T00:00:00Z..2024-02-24T08:00:00Z, val 2024-03-02T08:00:00Z..2024-03-20T02:00:00Z, test 2024-03-27T02:00:00Z..2024-03-30T23:00:00Z (7d embargo); test QLIKE B0=0.140791, B1=0.147800, C1=0.145083, C2=0.144105; C2 vs B1 2.50% rel. reduction, 95% CI [-0.123401, 0.158843] crosses zero.
- Registry artifacts present: research_state/hypothesis_registry.json, experiment_frontier.json, negative_results_report.md, leakage_audit.md.
- FCLR-002 coverage (research_state/fclr002_coverage_audit.json): 5 symbols, 4392 common hourly timestamps, single contiguous window 2024-04-01T00:00:00Z..2024-09-30T23:00:00Z (~183 days). This satisfies the protocol's minimum claim-worthy test data requirement (>=5 instruments, >=3 non-overlapping 30-day blocks) but FCLR-002 has NOT been executed and its holdout has NOT been opened. scripts/fclr002_download.py is idempotent (skips existing files); data_cache holds 4174 zips / 7350 extracted CSVs. No network activity was performed this session.

**What to do:**
1. Read RESEARCH_PROMPT.md, AGENT_HANDOFF.md, research_state/research_protocol.md, research_state/final_inconclusive_report.md, and research_state/gate_assessment.md to confirm current state.
2. If FCLR-002 is explicitly requested, first pre-register a new protocol version (FCLR-002 v1.0) with split/acceptance criteria BEFORE computing any outcomes; then run the walk-forward evaluation on the 2024-04..2024-09 panel; then run the leakage audit on the new panel before opening its holdout. Do not reuse the FCLR-001 sealed holdout for selection/tuning.
3. Documentation/cleanup is acceptable only if it improves clarity without modifying evaluation logic, splits, protocol, or reported results. Never claim unexecuted runs succeeded.
4. Leave risk-overlay phase INELIGIBLE.

**Acceptance check:** State remains inconclusive with gates documented; no holdout leakage introduced; all existing tests pass (24 passed). No new model results reported from the current holdout.

## What changed (this session, 2026-10-27T09:19:05Z)
- Re-read prior agent task from AGENT_HANDOFF.md ("Maintain repository state as-is") and verified completion: HEAD=b6a87be4 on main, git tracked tree clean (only untracked __pycache__ caches), no holdout leakage, no model retraining/re-tuning/re-evaluation on the sealed holdout, no split/protocol changes.
- Confirmed tests pass: `python -m pytest` 24 passed, 0 failed in ~4.73s. Tracked tree clean (research_state/fclr002_coverage_audit.json restored to HEAD).
- Verified state unchanged: inconclusive, forecast gate NOT MET (PILOT/INCONCLUSIVE), risk-overlay INELIGIBLE, direct liquidation labels unavailable; splits/protocol/results unchanged. Registry artifacts present.
- Updated AGENT_HANDOFF.md with verification record and next-agent task.

## Initial task message for next agent
**Task:** Maintain repository state as-is. Do not retrain, re-tune, or re-evaluate models on the current sealed holdout. Do not extend the OOS window or change splits/protocol. Risk-overlay remains INELIGIBLE. FCLR-002 coverage is confirmed sufficient (>=5 instruments, >=3 non-overlapping 30-day blocks feasible from 2024-04..2024-09) but FCLR-002 execution is NOT authorized unless explicitly requested with a pre-registered protocol version. Do not run scripts/fclr002_download.py or scripts/fclr002_coverage_audit.py unless explicitly instructed.

**Current verified state (as of 2026-10-27T09:19:05Z):**
- Repository is INCONCLUSIVE. Forecast gate NOT MET (PILOT/INCONCLUSIVE). Risk-overlay INELIGIBLE. Direct liquidation labels unavailable.
- Tests: `python -m pytest` 24 passed, 0 failed in ~4.73s. Git tracked tree: HEAD=b6a87be4 on main; clean (only untracked __pycache__ caches). No research logic/split/protocol/results changes.
- Frozen splits/protocol/results unchanged: train 2024-01-02T00:00:00Z..2024-02-24T08:00:00Z, val 2024-03-02T08:00:00Z..2024-03-20T02:00:00Z, test 2024-03-27T02:00:00Z..2024-03-30T23:00:00Z (7d embargo); test QLIKE B0=0.140791, B1=0.147800, C1=0.145083, C2=0.144105; C2 vs B1 2.50% rel. reduction, 95% CI [-0.123401, 0.158843] crosses zero.
- Registry artifacts present: research_state/hypothesis_registry.json, experiment_frontier.json, negative_results_report.md, leakage_audit.md.
- FCLR-002 coverage (research_state/fclr002_coverage_audit.json): 5 symbols, 4392 common hourly timestamps, single contiguous window 2024-04-01T00:00:00Z..2024-09-30T23:00:00Z (~183 days). This satisfies the protocol's minimum claim-worthy test data requirement (>=5 instruments, >=3 non-overlapping 30-day blocks) but FCLR-002 has NOT been executed and its holdout has NOT been opened. scripts/fclr002_download.py is idempotent (skips existing files); data_cache holds 4174 zips / 7350 extracted CSVs. No network activity was performed this session.

**What to do:**
1. Read RESEARCH_PROMPT.md, AGENT_HANDOFF.md, research_state/research_protocol.md, research_state/final_inconclusive_report.md, and research_state/gate_assessment.md to confirm current state.
2. If FCLR-002 is explicitly requested, first pre-register a new protocol version (FCLR-002 v1.0) with split/acceptance criteria BEFORE computing any outcomes; then run the walk-forward evaluation on the 2024-04..2024-09 panel; then run the leakage audit on the new panel before opening its holdout. Do not reuse the FCLR-001 sealed holdout for selection/tuning.
3. Documentation/cleanup is acceptable only if it improves clarity without modifying evaluation logic, splits, protocol, or reported results. Never claim unexecuted runs succeeded.
4. Leave risk-overlay phase INELIGIBLE.

**Acceptance check:** State remains inconclusive with gates documented; no holdout leakage introduced; all existing tests pass (24 passed). No new model results reported from the current holdout.


## What changed (this session, 2026-10-27T09:19:34Z)
- Re-read prior agent task from AGENT_HANDOFF.md ("Maintain repository state as-is") and verified completion: HEAD=f090587a on main, git tracked tree clean (only untracked __pycache__ caches), no holdout leakage, no model retraining/re-tuning/re-evaluation on the sealed holdout, no split/protocol changes.
- Confirmed tests pass: `python -m pytest` 24 passed, 0 failed in ~5.21s. Tracked tree clean.
- Verified state unchanged: inconclusive, forecast gate NOT MET (PILOT/INCONCLUSIVE), risk-overlay INELIGIBLE, direct liquidation labels unavailable; splits/protocol/results unchanged. Registry artifacts present.
- Updated AGENT_HANDOFF.md with verification record and next-agent task.

## Initial task message for next agent
**Task:** Maintain repository state as-is. Do not retrain, re-tune, or re-evaluate models on the current sealed holdout. Do not extend the OOS window or change splits/protocol. Risk-overlay remains INELIGIBLE. FCLR-002 coverage is confirmed sufficient (>=5 instruments, >=3 non-overlapping 30-day blocks feasible from 2024-04..2024-09) but FCLR-002 execution is NOT authorized unless explicitly requested with a pre-registered protocol version. Do not run scripts/fclr002_download.py or scripts/fclr002_coverage_audit.py unless explicitly instructed.

**Current verified state (as of 2026-10-27T09:19:34Z):**
- Repository is INCONCLUSIVE. Forecast gate NOT MET (PILOT/INCONCLUSIVE). Risk-overlay INELIGIBLE. Direct liquidation labels unavailable.
- Tests: `python -m pytest` 24 passed, 0 failed in ~5.21s. Git tracked tree: HEAD=f090587a on main; clean (only untracked __pycache__ caches). No research logic/split/protocol/results changes.
- Frozen splits/protocol/results unchanged: train 2024-01-02T00:00:00Z..2024-02-24T08:00:00Z, val 2024-03-02T08:00:00Z..2024-03-20T02:00:00Z, test 2024-03-27T02:00:00Z..2024-03-30T23:00:00Z (7d embargo); test QLIKE B0=0.140791, B1=0.147800, C1=0.145083, C2=0.144105; C2 vs B1 2.50% rel. reduction, 95% CI [-0.123401, 0.158843] crosses zero.
- Registry artifacts present: research_state/hypothesis_registry.json, experiment_frontier.json, negative_results_report.md, leakage_audit.md.
- FCLR-002 coverage (research_state/fclr002_coverage_audit.json): 5 symbols, 4392 common hourly timestamps, single contiguous window 2024-04-01T00:00:00Z..2024-09-30T23:00:00Z (~183 days). This satisfies the protocol's minimum claim-worthy test data requirement (>=5 instruments, >=3 non-overlapping 30-day blocks) but FCLR-002 has NOT been executed and its holdout has NOT been opened. scripts/fclr002_download.py is idempotent (skips existing files); data_cache holds 4174 zips / 7350 extracted CSVs. No network activity was performed this session.

**What to do:**
1. Read RESEARCH_PROMPT.md, AGENT_HANDOFF.md, research_state/research_protocol.md, research_state/final_inconclusive_report.md, and research_state/gate_assessment.md to confirm current state.
2. If FCLR-002 is explicitly requested, first pre-register a new protocol version (FCLR-002 v1.0) with split/acceptance criteria BEFORE computing any outcomes; then run the walk-forward evaluation on the 2024-04..2024-09 panel; then run the leakage audit on the new panel before opening its holdout. Do not reuse the FCLR-001 sealed holdout for selection/tuning.
3. Documentation/cleanup is acceptable only if it improves clarity without modifying evaluation logic, splits, protocol, or reported results. Never claim unexecuted runs succeeded.
4. Leave risk-overlay phase INELIGIBLE.

**Acceptance check:** State remains inconclusive with gates documented; no holdout leakage introduced; all existing tests pass (24 passed). No new model results reported from the current holdout.
