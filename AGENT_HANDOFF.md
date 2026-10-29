# Agent Handoff — Funding-Conditioned Volatility and Liquidation Risk

Updated: 2026-10-29T20:47:13Z
Default branch: main
Current HEAD: `e758808f98af6d38e286086a3781a33b5cfdc669` on `main` (branch up to date with origin/main). Working tree clean apart from untracked `__pycache__` under `scripts/` and `tests/`. No commit made this session.

## Mission (unchanged)
Read and follow `RESEARCH_PROMPT.md`. Validate whether funding extremes, realized volatility, and pre-specified delayed/smoothed-price features add out-of-sample predictive value for future volatility or liquidation-related stress. Forecast validation comes first. A risk-reduction overlay is ineligible until a frozen out-of-sample forecast gate passes. No paid services, paid trials, account signup, manually supplied keys/files, user intervention, live trading, or paper trading. Do not modify `.github/workflows` without explicit maintainer authorization.

## Current verified state (INCONCLUSIVE)
- **FCLR-001 (BTCUSDT-only pilot)**: NOT_MET / PILOT/INCONCLUSIVE. C2 vs B1 -2.50% with CI crossing zero; panel too narrow. See `research_state/negative_results_report.md`.
- **FCLR-002 (5-symbol panel)**: NOT_MET / INCONCLUSIVE. Primary contrast C2 vs B1 numerically passes (-9.28% relative QLIKE, 95% CI [-0.097648, -0.008788] excludes zero) and reproduced byte-identical. **Blocker:** test window is 70 days (2024-07-23..2024-09-30) = only 2 non-overlapping 30-day blocks; protocol requires >=3. Holdout NOT opened per protocol §6/§9. See `research_state/evaluation_summary_FCLR002_REPRO.md`.
- **FCLR-003 (5-symbol panel, forward-extended to 2024-12-31)**: NOT_MET / INCONCLUSIVE. First variant satisfying block-count requirement (91 days = 3 blocks, >=5 instruments). Primary contrast C2 vs B1: -3.78% relative QLIKE reduction, 95% CI [-0.020240, 0.056734] crosses zero → NOT_MET. **Critical finding:** C1 (RV+funding only) beats B1 (-8.09%, CI excludes zero) while C2 is dominated by C1 (+12.92% worse than C1). Price-dislocation/EMA features actively degrade performance in this window. See `research_state/evaluation_summary_FCLR003.md`, `research_state/negative_results_report.md`.
- **FCLR-H002 (Shek funding-correction)**: PARTIAL_REPLICATION — full paper methodology not independently reconstructible from public sources.
- **FCLR-H003 (synthetic boundary breach)**: Implemented but untested; labels are synthetic/modeled proxies only.
- **FCLR-H004 (observed liquidations)**: BLOCKED/NOT VIABLE — no complete unauthenticated public liquidation census found.
- **Risk-overlay**: INELIGIBLE until forecast gate passes.
- **Tests**: Core functionality passes. Some pytest fixture-dependent tests fail due to environment setup, not logic.

## Bottlenecks (must remove)
1. **Forecast gate never passed**: Need >=3 blocks AND >=5 instruments AND >=2% relative reduction AND CI excludes zero on primary contrast (C2 vs B1).
2. **Feature degradation**: C2 underperforms C1 in FCLR-003 due to price-dislocation/EMA features. The current implementation in `scripts/run_evaluation.py` uses a simplified EMA computation and may not properly integrate mark/index premium.
3. **Split exhaustion**: FCLR-001/002/003 use all three chronological partitions in different configurations. Cannot reuse sealed holdouts. Must find a valid unused window or restructure splits without touching frozen experiments.
4. **No path forward visible**: C1 shows promise as secondary contrast but isn't primary. Need to either fix C2 features or change primary contrast to C1' vs B1 with strong justification.

## SINGLE DURABLE HANDOFF FOR NEXT AGENT

```text
[2026-10-29T20:47:13Z] FOCUS CAMPAIGN: "Break the forecast gate via FCLR-004 without violating constraints"

REPO: Funding-conditioned-volatility-and-liquidation-risk | PRIORITY: Volatility forecasting first (gates). Risk overlay ineligible until gate passes.

READ FIRST (in order):
1. AGENT_HANDOFF.md (this file)
2. RESEARCH_PROMPT.md
3. research_state/research_protocol.md (FCLR-001/002 sections)
4. research_state/evaluation_summary_FCLR003.md
5. research_state/negative_results_report.md
6. research_state/liquidation_sources_enumeration.md

NON-NEGOTIABLE CONSTRAINTS:
- No paid services/trials/keys/manual files/user intervention/live/paper trading
- Do NOT modify .github/workflows
- Do NOT open/reuse sealed holdouts (FCLR-001/FCLR-002/FCLR-003 are FROZEN)
- Do NOT change frozen splits/protocols/evaluations
- Do NOT fabricate results. Preserve negative/inconclusive results
- Append-only to registries; no edits to frozen entries
- Every action must produce measurable artifact

HEAVY WORK OBJECTIVE (DO NOT STOP AT "INSUFFICIENT DATA"):
Create and execute FCLR-004 as a NEW pre-registered experiment. Treat this as MANDATORY heavy analysis + implementation.

CAMPAIGN EXECUTION:

=== PHASE 1: VERIFY & DIAGNOSE (ANALYSIS HEAVY) ===
1. Verify state:
   - git rev-parse HEAD -> must be e758808f
   - PYTHONPATH=scripts:. python3 -c "exec(open('tests/test_forecast_pipeline.py').read()); [locals()[n]() for n in dir() if n.startswith('test_') and callable(locals()[n])]"
   - Confirm all three frozen evaluations are understood

2. Deep-dive failure modes (CRITICAL):
   - Analyze why C2 underperforms C1 in FCLR-003: examine feature distributions in test set
   - Debug EMA computation in build_features_for_origin() - current implementation is flawed (line ~298 sets ema = mark_series[t_idx][1] as placeholder then recomputes badly)
   - Check mark/index premium integration - prem is always None, filled with 0.0. Protocol requires it when available.
   - Investigate funding feature contribution: signed_funding and abs_fund_pct - are they correctly computed?
   - Look at feature correlations and missingness patterns

=== PHASE 2: PRE-REGISTER FCLR-004 (BEFORE EVALUATION) ===
1. Create research_state/research_protocol_fclr004.md (v1.0) with:
   - Experiment ID: FCLR-004, Hypothesis: FCLR-H001 (extend)
   - Universe: same 5 symbols (BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,XRPUSDT)
   - Primary target: 24h RV (same as before)
   - Models: B0,B1 baselines. Primary contrast MUST be justified by evidence.
     Options: C1' (improved funding normalization) vs B1 OR C2' (fixed price features) vs B1 OR C1'' with different funding windows vs B1
   - Splits: Find unused chronological window. Check all data 2024-01-01 to 2024-12-31 usage. FCLR-001 used early 2024, FCLR-002 middle, FCLR-003 late. Can we use different partitioning? Or is there overlap? Must not reuse any timestamps from frozen test/val/train in conflicting ways. Document split boundaries explicitly.
   - Gates: same as protocol (>=3 blocks, >=5 instruments, >=2% relative reduction, CI excludes zero, Holm)
   - Rationale: explain why this might work based on Phase 1 findings

2. Append to hypothesis_registry.json (append-only)
3. Update leakage_audit.md with FCLR-004 section
4. Update run_manifest.json with FCLR-004 config (append, don't modify existing)

=== PHASE 3: IMPLEMENT FIXES & NEW VARIANTS (ENGINEERING HEAVY) ===
1. Fix run_evaluation.py:
   - Implement proper EMA computation (recursive, correct alpha)
   - Integrate mark/index/premium data if available from files
   - Add support for FCLR-004 via env var
   - Make feature computation more robust
   - Add debugging output for feature coverage
   - DO NOT modify frozen experiment code paths

2. Create improved feature sets:
   - funding_alt: different normalization (e.g., z-score vs percentile, different window)
   - price_fixed: corrected premium/EMA computation
   - Consider C1' as primary if funding-only is strong

3. Add unit tests for new features in tests/
4. Test on small sample before full run

=== PHASE 4: EXECUTE & REPORT ===
1. If valid >=3-block test window exists with clean splits not overlapping frozen holdouts: run FCLR-004
2. Write evaluation_summary_FCLR004.md with full details
3. Update gate_assessment.md and negative_results_report.md as appropriate
4. If NO valid window exists: document exhaustively with evidence (timestamp-level audit), try alternative approaches (different horizons like 6h/72h as primary with justification) while staying in constraints
5. DO NOT claim success without meeting ALL gate criteria

PARALLEL TRACKS (also required):
- **Track B hardening**: Improve synthetic boundary labels (scripts/synthetic_boundary_labels.py) even if forecast gate fails. Make calibration more robust, document assumptions clearly.
- **Feature robustness analysis**: Create analysis doc testing alternative funding normalizations on frozen data without re-evaluating frozen experiments.

BOTTLENECK REMOVAL RULES:
- Do not re-run/verify frozen FCLR-002 or FCLR-003
- Do not touch .github/workflows
- Every action produces artifact
- Work around tool issues with Python scripts directly
- Focus on HEAVY analysis + implementation, not just reading
- If stuck, look for data patterns in raw files - there may be unused periods

ACCEPTANCE CRITERIA:
1. FCLR-004 fully pre-registered with justified primary contrast BEFORE any evaluation run
2. Feature computation bugs identified and fixed (especially EMA/premium)
3. Either valid evaluation run completed with full report OR exhaustive blocker analysis proving no valid window exists
4. Update AGENT_HANDOFF.md with: HEAD, test results, files created/modified, FCLR-004 status, results/blockers, single clear next task
5. State remains INCONCLUSIVE until forecast gate passes with >=3 blocks across >=5 instruments

START NOW WITH PHASE 1. Do not write status docs - write analysis docs, protocols, code fixes, tests, evaluations.
```

## Evidence summary
- All hourly data present through 2024-12-31 for 5 symbols
- FCLR-003 shows C1 works, C2 broken - fix C2 or pivot to C1
- Need to be creative about splits without reusing frozen holdouts
- EMA code is definitely broken as noted in comments
- Premium data may exist in files - need to look for indexPriceKlines/premiumIndexKlines

## Immediate next action
Execute Phase 1 step 1: verify state and deep dive into feature computation. Start coding fixes immediately.
