# FCLR-RISK-12 Evaluation — funding-shock transmission family

Campaign: `FCLR-LIQ-RISK-ESCALATION-12-20261119T175557Z`
Session UTC: `20261119T180650Z`
Verdict: `UNDERPOWERED`
Power status: `UNDERPOWERED`
Models run: `false`

## Summary

The funding-shock transmission family (funding innovations, not the funding level or the closed interaction) was evaluated on the frozen Track A panel.
The power gate determined UNDERPOWERED: all scored blocks' `mde_brier_80pct` exceed `PLAUSIBLE_EFFECT_BRIER=0.001`, so no model fitting was performed (`models_run=false`) and all six family members are NOT_MET.
This is an honest underpowered session — all 11 RISK-12 artifacts are emitted, including this evaluation.

## Smallest defensible effect

`0.0028144136231997873` — min `mde_brier_80pct` across scored blocks at full instrument count (block_3 primary). Effect defensible only if >= this MDE.

## Plausible effect

`PLAUSIBLE_EFFECT_BRIER = 0.001` (frozen).

## Data

Frozen Track A panel `session_20261119T022824Z` (113,880 coin-hours, 13 coins, 2025-11..2026-10), common-sample kept 112671 (dropped 1209).

## MDE brier_80pct (block-level)

block_2: mde_brier_80pct=0.004080395099931475, powered_block=False
block_3: mde_brier_80pct=0.003881560964664036, powered_block=False
pooled: mde_brier_80pct=0.0028144136231997873, powered_block=False

All > 0.001 -> UNDERPOWERED.

## Member verdicts (block_3 primary)

member_1 (funding_lag (level), declared n/a (positive control / replication anchor; prior campaigns found not detectable at 0.001)): NOT_MET (models_run=false)
member_2 (funding_change_1h, declared > 0): NOT_MET (models_run=false)
member_3 (funding_change_8h, declared > 0): NOT_MET (models_run=false)
member_4 (funding_change_24h, declared > 0): NOT_MET (models_run=false)
member_5 (abs_funding_change_8h (sign-agnostic shock magnitude), declared > 0): NOT_MET (models_run=false)
member_6 (funding_change_8h_x_rv (amplification in high-RV hours), declared > 0): NOT_MET (models_run=false)

## Evidence supported
None; power gate failed for all scored blocks, so no member can be declared SUPPORT.

## Evidence contradicted
None; no family member demonstrated block_3 Brier improvement over RV-only clearing p_raw<0.05, p_holm<0.05, and placebo-95th<improvement.

## Evidence unknown
Whether the true incremental Brier effect of funding-shock transmission over RV-only is exactly zero or merely below the ~0.0028144136231997873 MDE floor at this sample size.

## Strongest alternative explanation
Funding-shock innovations have negligible incremental out-of-sample forecast skill over realized-volatility-only at the detectable effect scale; any true effect is smaller than the plausible-effect threshold (0.001 Brier) and hence undetectable here.

## Dominating limitation
Statistical power (sample size x effect size), not data availability; the panel and labels are complete and admissible.

## Concrete falsifying test
RISK-13 per contingency ladder: advance to a distinct mechanism on the frozen panel (candidate queue: (i) liquidation-hazard persistence liq_count-at-t-1 state family; (ii) within-hour cross-sectional funding-intensity contrast; (iii) UTC-hour / market-wide-RV conditioning of the funding effect).

## Highest information gain task
Complete RISK-12 underpowered session (all 11 artifacts), record session, bump campaign to RISK-13, then execute the contingency-ladder distinct-mechanism campaign.

## Exact artifact
`research_state/session_20261119T180650Z/fclr_risk12_evaluation_20261119T180650Z.json`

## Verification command
`python3 scripts/check_handoff_heavywork_gate.py --json` (must PASS)
