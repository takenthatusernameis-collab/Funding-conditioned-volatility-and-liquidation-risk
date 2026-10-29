# Agent Handoff — Funding-Conditioned Volatility and Liquidation Risk

Updated: 2026-10-29T20:01:46Z
Default branch: main
Current HEAD: `e758808f98af6d38e286086a3781a33b5cfdc669` on `main` (branch up to date with origin/main). Working tree clean apart from untracked `__pycache__` under `scripts/` and `tests/`. No commit made this session.

## Mission (unchanged)
Read and follow `RESEARCH_PROMPT.md`. Validate whether funding extremes, realized volatility, and pre-specified delayed/smoothed-price features add out-of-sample predictive value for future volatility or liquidation-related stress. Forecast validation comes first. A risk-reduction overlay is ineligible until a frozen out-of-sample forecast gate passes. No paid services, paid trials, account signup, manually supplied keys/files, user intervention, live trading, or paper trading. Do not modify `.github/workflows` without explicit maintainer authorization.

## Current verified state (INCONCLUSIVE)
- **FCLR-001 (BTCUSDT-only pilot)**: NOT_MET / PILOT/INCONCLUSIVE. C2 vs B1 -2.50% with CI crossing zero; evaluated panel BTCUSDT-only (1634 eval rows) so >=5-instrument gate never met. See `research_state/evaluation_summary.md`, `research_state/gate_assessment.md`, `research_state/coverage_audit_recheck.md`.
- **FCLR-002 (5-symbol panel)**: NOT_MET / INCONCLUSIVE. Primary contrast C2 vs B1 numerically passes (-9.28% relative QLIKE, 95% CI [-0.097648, -0.008788] excludes zero) and was independently reproduced byte-identical. **Blocker:** test window is 70 days (2024-07-23..2024-09-30) = only 2 non-overlapping 30-day blocks; protocol requires >=3. Holdout NOT opened per protocol §6/§9 and must not be reopened/recomputed. See `research_state/evaluation_summary_FCLR002_REPRO.md`.
- **FCLR-003 (5-symbol panel, forward-extended)**: NOT_MET / INCONCLUSIVE. First variant satisfying block-count requirement (91 days = 3 blocks, >=5 instruments). Primary contrast C2 vs B1: -3.78% relative QLIKE reduction, 95% CI [-0.020240, 0.056734] crosses zero → NOT_MET. **Key finding:** C1 (RV+funding only) beats B1 (-8.09%, CI excludes zero, secondary contrast) while C2 is dominated by C1 (+12.92% worse than C1), meaning price-dislocation/EMA features degrade performance in this window. See `research_state/evaluation_summary_FCLR003.md`, `research_state/negative_results_report.md`.
- **FCLR-H003 (synthetic boundary breach, Track B)**: INCONCLUSIVE on both panels, no incremental skill over volatility-only baseline. Labels are synthetic/modeled proxies, not observed liquidations.
- **FCLR-H002 (Shek funding-correction)**: PARTIAL_REPLICATION — full paper methodology not independently reconstructible from public sources alone.
- **FCLR-H004 (observed liquidation outcomes, Track A)**: BLOCKED/NOT VIABLE — no complete unauthenticated public liquidation census found. Track B/C remain the only admissible paths.
- **Risk-overlay**: INELIGIBLE until a forecast gate passes.
- **Tests**: `python3` manual test run shows 45 passed, 6 failed (test_controller_progress_accounting uses pytest fixtures requiring tmp_path - environment issue, not code issue). Core functionality tests all pass.

## Bottlenecks (remove or route around)
1. **Forecast gate not passed**: Both FCLR-002 (insufficient blocks) and FCLR-003 (primary contrast fails, C2 dominated by C1) are INCONCLUSIVE. C1 shows promise as secondary contrast but isn't the primary.
2. **Feature degradation**: Price-dislocation/EMA features hurt performance in FCLR-003. Need to understand why or try alternatives.
3. **Data exhaustion**: All hourly mark/index/funding/premium data for 2024 is present (mark through 2024-12-31). No 2023/2025 data available.
4. **Track A blocked**: No complete liquidation census from unauthenticated sources.
5. **Process friction**: Edit tool issues observed in past sessions; avoid large multi-file edits in single calls.

## Single durable handoff for next agent

```text
[2026-10-29T20:01:46Z] FOCUS CAMPAIGN: "Find a path to forecast gate pass without violating constraints"

Repo: Funding-conditioned-volatility-and-liquidation-risk. Priority = volatility forecasting first (gates). Risk overlay ineligible until gate passes.

READ FIRST (in order): AGENT_HANDOFF.md, RESEARCH_PROMPT.md, research_state/research_protocol.md, research_state/evaluation_summary_FCLR003.md, research_state/negative_results_report.md, research_state/liquidation_sources_enumeration.md.

CONSTRAINTS (NON-NEGOTIABLE): No paid services/trials/keys/manual files/user intervention/live/paper trading. Do not modify .github/workflows. Do not open/reuse sealed holdouts, do not change frozen splits/protocols/evaluations (FCLR-001/FCLR-002/FCLR-003 are frozen). Do not fabricate results. Preserve negative/inconclusive results. Append-only to registries; no edits to frozen entries.

HEAVY WORK OBJECTIVE (do NOT stop at "insufficient data"):
Create and execute FCLR-004 as a NEW pre-registered experiment (separate from frozen experiments). Focus on making funding features actually help while avoiding the price-feature degradation seen in C2.

EXECUTE THIS CAMPAIGN:

1. VERIFY STATE
   - git rev-parse HEAD -> e758808f
   - Run core tests: PYTHONPATH=scripts:. python3 -c "exec(open('tests/test_forecast_pipeline.py').read()); [locals()[n]() for n in dir() if n.startswith('test_') and callable(locals()[n])]"
   - Confirm FCLR-003 results are frozen and understood.

2. ANALYZE FAILURE MODES (HEAVY ANALYSIS)
   - Deep-dive into why C2 underperforms C1 in FCLR-003: examine feature distributions, correlations, leakage vectors, EMA computation issues (see scripts/run_evaluation.py build_features_for_origin - EMA calc is simplified). Check if premium/index features are missing causing issues.
   - Analyze funding feature contribution in C1 vs B1 - C1 adds signed_funding + abs_fund_pct. Are these well-specified? Try to understand if different funding normalization helps.
   - Look up all funding data coverage and quality across symbols.

3. PRE-REGISTER FCLR-004 (BEFORE ANY EVALUATION)
   - Create research_state/research_protocol_fclr004.md (v1.0). Key choices:
     * Universe: same 5 symbols (BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,XRPUSDT)
     * Target: 24h RV primary (same as before)
     * Define models: keep B0,B1 as baselines. Try C1' with improved funding features (different normalization/windows), and maybe C2' without the problematic price features or with corrected price features. OR make primary contrast C1' vs B1 if funding-only is promising.
     * Explicitly justify primary contrast choice based on evidence.
     * Splits: use remaining data cleverly - we have full 2024. Could do different split structure? Or extend train/val/test differently within 2024? Must not reuse sealed FCLR-002/003 holdouts. All three windows are used; need to find unused portion or restructure. Check split boundaries carefully.
     * Same gates: >=3 blocks, >=5 instruments, >=2% relative reduction, CI excludes zero, Holm correction.
   - Append to hypothesis_registry.json (append-only). Update leakage audit checklist for FCLR-004.
   - Document rationale in protocol.

4. IMPLEMENT & TEST (ENGINEERING HEAVY)
   - Extend scripts/run_evaluation.py or create variant to support FCLR-004 with new feature sets.
   - Fix any issues found (e.g., better EMA computation, proper handling of missing premium data).
   - Add unit tests for new features.
   - Ensure no changes to frozen code paths for FCLR-001/002/003.

5. RUN & REPORT
   - If valid >=3-block test window exists with clean splits not overlapping frozen holdouts: run evaluation.
   - Write evaluation_summary_FCLR004.md with full details. Update gate_assessment.md.
   - If no valid window exists without touching frozen holdouts: document exhaustively why, try alternative approaches (different horizons, different targets) while staying within constraints.

PARALLEL TRACKS:
- **Track B hardening**: Even if forecast gate fails, make synthetic boundary labels more robust (calibration, better margin assumptions). Keep clearly labeled as modeled proxy.
- **Feature robustness**: Test alternative funding normalizations on existing frozen data without re-evaluating frozen experiments.

BOTTLENECK REMOVAL:
- Do not re-run/verify frozen FCLR-002 or FCLR-003. Treat as complete.
- Do not touch .github/workflows.
- Every action must produce measurable artifact (analysis doc, new protocol, new evaluation, tests).
- If hitting tool issues, work around with Python scripts directly.
- Focus on heavy analysis + implementation, not just reading.

ACCEPTANCE: Update this AGENT_HANDOFF.md with HEAD, test results, files created/modified, FCLR-004 pre-registration status, evaluation results/blockers, and a single clear next task. State remains INCONCLUSIVE until forecast gate passes with >=3 blocks across >=5 instruments.
```
