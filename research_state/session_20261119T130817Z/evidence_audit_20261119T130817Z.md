# FCLR-RISK-11 Evidence Audit

Campaign: `FCLR-LIQ-RISK-ESCALATION-11-20261119T120000Z`
Session UTC: `20261119T130817Z`
Audit kind: evidence_audit per RESEARCH_PROMPT.md §19

## Verdict

`NOT_MET-with-bound` — power status UNDERPOWERED; models_run=false.

## Summary

The funded×RV×OI interaction family has now been scanned twice (RISK-09, RISK-10) with no detectable signal (all brier_improvement=0.0, p=1.0) and insufficient power for the plausible effect even at full instrument count (pooled MDE 0.0028 > 0.001). RISK-11 formally bounds that interaction effect and closes out the hypothesis.

## Smallest defensible effect

`0.002817725360790807` — min `mde_brier_80pct` across scored blocks at full instrument count (block_3 primary). Effect defensible only if >= this MDE.

## Plausible effect

`PLAUSIBLE_EFFECT_BRIER = 0.001` (frozen).

## Data

Frozen Track A panel `session_20261119T022824Z` (113,880 coin-hours, 13 coins, 2025-11..2026-10), common-sample kept 112,957.

## MDE brier_80pct

block_2: 0.004085, block_3: 0.003886, pooled: 0.002818. All > 0.001 → UNDERPOWERED.

## Member verdicts (block_3 primary)

All 6 members: NOT_MET.

## Evidence supported

None; power gate failed for all scored blocks, so no member can be declared SUPPORT.

## Evidence contradicted

None; no family member demonstrated block_3 Brier improvement over RV-only clearing p_raw<0.05, p_holm<0.05, and placebo-95th<improvement.

## Evidence unknown

Whether the true incremental Brier effect of funding-conditioned interactions over RV-only is exactly zero or merely below the ~0.0028–0.0041 MDE floor at this sample size.

## Strongest alternative explanation

The funding-conditioned interaction has negligible incremental out-of-sample forecast skill over realized-volatility-only at the detectable effect scale; any true effect is smaller than the plausible-effect threshold (0.001 Brier) and hence undetectable here.

## Dominating limitation

Statistical power (sample size × effect size), not data availability; the panel and labels are complete and admissible.

## Concrete falsifying test

RISK-12 per ladder rule — advance only if MDE <= plausible effect via MDE-by-instrument-count redesign or a larger/deeper panel; otherwise the null is preserved.

## Highest information gain task

Campaign RISK-11 interaction effect-bound / null-confirmation complete; no outcome mining; preserve the NOT_MET-with-bound null.

## Exact artifact

`research_state/session_20261119T130817Z/fclr_risk11_evaluation_20261119T130817Z.json`

## Verification command

`python3 scripts/check_handoff_heavywork_gate.py --json` (must PASS) and `python3 research_state/session_20261119T130817Z/fclr_risk11_evaluation_20261119T130817Z.py` (regenerates evaluation/power/recompute JSONs)
