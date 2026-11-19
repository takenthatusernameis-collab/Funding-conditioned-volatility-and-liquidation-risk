# fclr_risk09_evaluation_20261119T095800Z — specification scan evaluation

Campaign: `FCLR-LIQ-RISK-ESCALATION-09-20261119T095305Z`
Session UTC: `20261119T095800Z`
Verdict: `UNDERPOWERED`
Power status: `UNDERPOWERED` (all scored blocks' mde_brier_80pct > PLAUSIBLE_EFFECT_BRIER=0.001)

## Result

The joint funding x RV x open-interest interaction family (6 members) was evaluated against the RV-only baseline on the frozen 12-month Track A panel (113,880 coin-hours; 13 coins; 2025-11..2026-10) under the binding common-sample rule (112,957 coin-hours kept after dropping null rv_lag/funding_lag/oi_change_lag rows).

Because the power gate failed for all scored blocks (block_2 mde 0.00409, block_3 mde 0.00389, pooled mde 0.00282 vs plausible effect 0.001), `models_run=false` and the campaign is declared UNDERPOWERED rather than claiming a negative result from an underpowered test. Honest evaluation artifacts are still written: all six family members return `NOT_MET` on block_3 (primary) and the scored blocks.

Family members (all NOT_MET):
1. funding_x_rv
2. funding_x_oi
3. rv_x_oi
4. three_way
5. funding_spline
6. decile_regime

## Design (frozen in fclr_risk09_prereg_20261119T095800Z)

- Scored blocks: block_2 (2026-02..04, train 2025-11..12), block_3 (2026-06..08, train 2025-11..2026-01, primary), pooled (block_2+block_3 test). block_1 cold-start anchor, power only.
- Models: intercept-only, RV-only (rv_lag), RV-only + each family member. Logistic regression by stdlib IRLS.
- Metrics: Brier (headline), log-loss, AUC, calibration OLS slope/intercept.
- Placebo: label-hour permutation within hour across coins, 1000 perms, seed 20261119.
- Multiplicity: Holm over members x scored blocks at alpha=0.05.
- Verdict per member: SUPPORT iff block_3 Brier improvement > 0, p_raw<0.05, p_holm<0.05, placebo 95th < improvement.

## Contingency (RISK-09 → UNDERPOWERED)

Next campaign `RISK-10` = power restoration design: pooled-block MDE audit, minimum-detectable-effect table by instrument count, and a preregistered decision on the smallest defensible effect; no outcome mining. See AGENT_HANDOFF.md (campaign `FCLR-LIQ-RISK-ESCALATION-10-20261119T095900Z`).

## Recompute

`fclr_risk09_recompute_20261119T095800Z.json`: n_discrepancies=0; panel matches certified preflight (113,880 rows, 13 coins, 12 months, funding 113,880/113,880, OI 113,035/113,880).
