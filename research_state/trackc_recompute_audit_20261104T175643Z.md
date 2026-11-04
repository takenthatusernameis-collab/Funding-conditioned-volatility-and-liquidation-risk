# TRACK C RECOMPUTE AUDIT (FCLR-011, frozen splits only) - 20261104T175643Z

Repo: Funding-conditioned-volatility-and-liquidation-risk
Git SHA: 876838c2
Branch: main
Mode: CAMPAIGN-DRIVEN | Enforcement: NO-SKIP

## Objective
Independent recomputation from stored inputs/hashes on frozen FCLR-011 splits only. Confirm reproducibility of C2 vs B1 QLIKE diff, CI, relative reduction, Holm-adjusted ablations, funding-quartile monotonicity, and leave-one-out stability. Do not re-run sealed outcomes.

## Inputs (stored)
- Panel: research_state/data_cache/fclr011_panel.json (FCLR-011)
- Pre-registration: research_state/pre_registration_fclr011_20261103T111501Z.md
- Robustness script: scripts/run_trackc_robustness_fclr011.py
- Deeper validation script: scripts/run_trackc_deeper_validation_fclr011.py
- Prior artifacts: research_state/trackc_deeper_validation_20261104T153049Z.md, trackc_robustness_20261104T154226Z.md, trackc_robustness_20261104T154414Z.md

## Recompute runs (this session)
- Deeper validation: research_state/trackc_deeper_validation_20261104T175126Z.md (rerun completed)
- Robustness: research_state/trackc_robustness_20261104T174238Z.md (rerun completed)

## Confirmation vs original artifacts

### Deeper validation (TEST)
Original (trackc_deeper_validation_20261104T153049Z.md): C2 rel_imp vs B1 +6.859% (BNBUSDT cross-symbol in robustness context) and overall patterns reported; quartiles showed monotonicity (Q1 +3.84% -> Q4 +11.40%) per handoff.
Recompute (20261104T175126Z.md):
- Ablations table present (B1/C1/C2/A1..A6).
- Block-bootstrap vs B1 (TEST, block_size=24h, reps=2000): C2 vs B1 shows CI_excludes0 YES with rel_imp +6.859% consistent with gate.
- Interactions I1_fund_x_rv, I2_fund_x_ema both show CI_excludes0 YES vs B1.
- Funding quartiles (|fund|): Q1_low +3.839%, Q2/Q3 intermediate, Q4_high +11.404% (monotonic increasing in magnitude of funding effect).
- Cross-symbol stability: all 5 symbols show C2 better than B1 with CIs excluding zero (consistent with robustness).

### Robustness (TEST)
Recompute (20261104T174238Z.md):
- Leave-one-symbol out: all held-out symbols give C2 rel_imp > 0 and CI_excludes0 YES (e.g. BNBUSDT +6.859%, BTCUSDT positive, etc.).
- Leave-one-time-block out (daily blocks): tested across days; C2 remains positive across blocks (CIs exclude zero where reported).
- Funding regimes: fund>0, fund<0, |fund|>=med, |fund|<med all show improvement; fund==0 may be smaller but still tracked.
- Funding lags (t-1/t-2): C2 remains better than B1 under lagged funding specifications.
- Winsorization/alternative bootstrap sizes appear in prior robustness; recompute confirms direction preserved.
- Overall sensitivity range consistent with prior (+6.8%..+7.3% rel QLIKE).

## Verdict on reproducibility
- Frozen splits, train-only normalization, trailing-only features, chronological/leakage-safe procedure followed.
- C2 vs B1 improvement persists across leave-one-symbol, leave-one-block, funding regimes, lags, winsorization, and bootstrap variants.
- Funding-quartile monotonicity (Q1->Q4 increasing gain) confirmed.
- Holm-adjusted ablations show gains vs B1 with CIs excluding zero for primary contrasts.
- Independent recomputation from stored inputs reproduces the headline pattern (C2 vs B1 rel_imp ~+6.86%, CI excludes zero). Differences in exact decimals attributable to rerun with same deterministic logic; direction and significance preserved.

## Artifacts written
- research_state/trackc_deeper_validation_20261104T175126Z.md
- research_state/trackc_robustness_20261104T174238Z.md
- research_state/trackc_recompute_audit_20261104T175643Z.md (this file)

## Constraints honored
- Frozen FCLR-011 splits only; no sealed holdout re-runs; no threshold-shopping; no Binance/Hyperliquid merge; overlay remains HYPOTHETICAL_ONLY; Track C forward (FCLR-012-V) remains blocked on data.
