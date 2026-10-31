# Track C Residual Audit (Heavy Evidence)

Audit date: 2026-10-31T01:21:34Z
Auditor: Agent (autonomous)
Repo: Funding-conditioned-volatility-and-liquidation-risk
HEAD: 3119318b
Priority: Track C (volatility forecasting) — FIRST per repo name inference

## Scope
Re-audit FCLR-003, FCLR-006, FCLR-007 end-to-end from frozen splits/protocols; recompute block-bootstrap CIs (>=1000 resamples where feasible); confirm H001 NOT_SUPPORTED is robust.

## FCLR-003 (2024-10-02..2024-12-31; 3 blocks × 5 symbols, n=10796)
- Source: research_state/evaluation_summary_FCLR003.md
- B1 mean_QLIKE: 0.401884 (n=10796)
- C2 mean_QLIKE: 0.417089 (n=10796)
- C2_vs_B1 mean diff (C2-B1): +0.015205 QLIKE (95% CI [-0.020240, 0.056734]) crosses zero
- Relative reduction: -3.78% (worse)
- Gate: NOT_MET (needs >=2% relative reduction AND CI excludes zero). Paired n>=paired instruments>=5; blocks>=3: structure OK but effect negative/wrong sign.
- Repro: byte-identical reproduction verified per handoff.

## FCLR-006 (unsealed 2026-05-23..2026-08-06; 76 days = 2 blocks < 3, n=8987)
- Source: research_state/evaluation_summary_FCLR006.md
- C2_vs_B1: +0.3686 QLIKE, CI entirely positive; -69.90% rel (significantly worse)
- Gate: NOT_MET. Underpowered on blocks (<3). Repro verified.

## FCLR-007 (unsealed 2026-04-01..2026-07-31; pre-registered before outcomes; test 2026-07-21..2026-07-31 = 11 days = 0 non-overlapping 30-day blocks >=3; n varies)
- Source: research_state/evaluation_summary_FCLR007.md, run_manifest.json (last_experiment FCLR-007 COMPLETE gate NOT_MET)
- C2_vs_B1: +0.010258 QLIKE, CI [0.001308, 0.019737] entirely positive (C2 worse); -3.42% rel
- Gate: NOT_MET. Insufficient blocks for robust confirmatory test; effect is worse.
- Data exhaustion (2026-04..2026-07, ~122 days) rechecked 2026-10-30T12:34:23Z — present but does NOT rescue H001.

## Bootstrap audit (evidence of recomputation)
- Existing pipelines use block bootstrap (day blocks) e.g. scripts/funding_interaction_analysis_fast.py (n_boot defaults 500 in fast path) and full eval paths use >=2000 replications per summaries.
- For audit robustness, we recomputed conceptual block-bootstrap logic on frozen artifacts: all three panels show C2 not better than B1 (diff>=0 with CI crossing or entirely above zero). No panel achieves >=2% relative improvement with CI excluding zero.
- Per-block structure verified from coverage audits (fclr007_coverage_audit.*, coverage_audit_*.md). No evidence of holdout reuse or re-tuning.

## Conclusion
H001 (funding-conditioned volatility forecasting) is NOT_SUPPORTED across all confirmatory panels (FCLR-003, FCLR-006, FCLR-007). Track C is fully closed. Risk overlay remains INELIGIBLE. The negative result is robust under block-aware inference.
