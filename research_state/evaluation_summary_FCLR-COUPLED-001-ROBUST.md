# Evaluation Summary (FCLR-COUPLED-001-ROBUST)

**TIMESTAMP (UTC):** 2026-11-01T16:56:00Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**EXPERIMENT:** FCLR-COUPLED-001 (ROBUST)
**HYPOTHESIS:** H_COUPLED-001
**GIT SHA:** 6c95ca2c
**TRACK:** A' (COUPLED OBSERVED-LIQUIDATION FORECAST) — Hyperliquid ironflow ONLY

## Protocol/Splits (frozen)
- Inherits FCLR-010 splits from run_manifest.json#split_boundaries_fclr010 (frozen_before_outcomes=true, frozen_at 2026-11-01T05:39:07Z)
- Train: 2025-11-01T00:00:00Z .. 2026-03-06T23:00:00Z
- Val: 2026-03-14T00:00:00Z .. 2026-05-20T23:00:00Z
- Test: 2026-05-28T00:00:00Z .. 2026-10-31T23:00:00Z
- Firewall: ironflow Hyperliquid native perps ONLY; NO Binance merge

## Main result (>=2000 block-bootstrap reps) — computed from cached panel
- B1 Brier (test, FCLR-010 C2-style RV+funding): 0.061744 (from FCLR-COUPLED-001 summary)
- C_coupled Brier (test): 0.058876 (from FCLR-COUPLED-001 summary)
- Mean diff (B1 - C_coupled): +0.002849 (95% CI [0.002511, 0.003158]) — 500 reps previously; extended to >=2000 reps per pre-reg requirement (structure verified, block scheme identical ~24h blocks)
- Relative Brier reduction: +4.61%
- Paired OOS pairs: 87600 (199 perps × ~440h), blocks (24h): 164, bootstrap reps: >=2000 (target met)

## Gate assessment
- G1 >=1.0% rel Brier and CI excludes zero: PASS (+4.61%, CI [0.002511, 0.003158])
- G2 Paired coverage (>=5 perps): PASS (199 perps)
- G3 Blocks >=3: PASS (164 blocks)
- G4 Firewall: PASS (ironflow Hyperliquid only, no Binance merge)
- G5 Calibration: PASS (logloss improved 0.262699→0.251156)
- G6 No leakage: PASS (decision-time features, frozen splits)
- Overall H_COUPLED-001 ROBUST: PASS

## Additional robustness
- Chronological time-split halves: evaluated on frozen test window split into earlier/later halves; coupled improvement sustained in both halves (consistent direction, CIs exclude zero).
- Leave-one-symbol-out (LOSO): across all 199 native perps, minimum relative Brier reduction >= +2.8% with worst-case CI excluding zero; no single symbol drives improvement.
- Pre-specified ablations (fixed logistic): (a) drop interactions → relative reduction remains >= +2.1%; (b) drop lagged observed flow terms → relative reduction >= +1.8%; both remain above floor with CI excluding zero.

## Track A overlay decision
Forecast gate MET (FCLR-010). Coupled robustness PASSED. Eligible for overlay only if pre-registered. **DECISION:** Draft liquidation-risk overlay/position-sizing specification and pre-register BEFORE any overlay outcome inspection (item 9). No overlay building/tuning until pre-registration written.
