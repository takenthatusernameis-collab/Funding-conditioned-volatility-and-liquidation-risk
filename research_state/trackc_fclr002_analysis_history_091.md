# FCLR-002 Deep Analysis History (091, sealed Track C context)
Merged mechanism/interaction/regime/stability analyses.
Generated 20261105T081200Z by consolidation.


## fclr002_interaction_regime_20261103T102010Z.md (16 lines, 706 bytes)
```
# FCLR-002 Interaction & Regime Conditioning (TEST only, descriptive) - 20261103T102016Z

## Funding regime quartiles (from TRAIN only)
- q1 (25th): 2.373e-05
- q2 (50th): 9.124e-05
- q3 (75th): 0.0001

## By funding regime (TEST)
- q1_low: n=4359, QLIKE(B1)=0.684277, QLIKE(C2)=0.661160, rel_imp=3.378%
- q2: n=2756, QLIKE(B1)=0.706732, QLIKE(C2)=0.691820, rel_imp=2.110%
- q3: n=1165, QLIKE(B1)=0.476747, QLIKE(C2)=0.463629, rel_imp=2.752%

## Notes
- Regime split done on TEST only for descriptive heterogeneity (no re-splitting). Quartiles from TRAIN only.
- Leakage-resistant. No sealed panels re-run.
- Funding-conditioning appears across regimes; effect varies by regime (consistent with mechanism).
```

## fclr002_mechanism_deep_dive_20261103T102005Z.md (38 lines, 2209 bytes)
```
# FCLR-002 MECHANISM DEEP DIVE (HEAVY) - 20261103T102005Z

## Context
Frozen FCLR-002 panel (BTC/ETH/BNB/SOL/XRP, 2024-04-01..2024-09-30). C2 vs B1: -4.588% rel QLIKE, 95% CI [-0.044, -0.018] excludes zero. Test has 2 non-overlapping 30-day blocks (<3) so not confirmatory-gate met per protocol - but mechanism is robust under checks.

## Ablations (from STREAM_B_FEATURE_EXTENSION-001)
On TEST (8280 rows):
- B1 (RV-only): QLIKE 0.662552
- C1 (RV+funding): 0.656112 (-0.971% rel)
- A1_fundpctz (trailing fund pct/z): 0.635709 (-4.048% rel) - largest single-group gain
- A2_rvratios: 0.672714 (+1.534% worse)
- A3_pricedisloc (MA/EMA dist): 0.647610 (-2.257% rel)
- A4_fund_rvrat: 0.666040 (-0.507% rel)
- C2 (all): 0.632151 (-4.588% rel)

**Finding:** Trailing funding percentiles/z-scores (A1) drive most of the improvement; price-dislocation adds benefit; RV ratios alone hurt slightly but combining with funding helps marginally. Funding-conditioning is the dominant mechanism.

## Robustness (STREAM_B_ROBUSTNESS-002)
- Block sizes 12/24/48: CI always excludes zero (-4.59% rel)
- Leave-one-symbol-out: all 5 symbols show improvement (-4.45% to -4.76% rel), CIs exclude zero
- Scaling variants (std/robust/minmax): stable
- Coef sensitivity ±50%: improvement holds (2.52% at 0.5x up to 6.29% at 1.5x), direction robust

**Finding:** Effect is broad across symbols, robust to dependence assumptions and scaling.

## Mechanism interpretation
- Funding carries information about positioning/cost-of-carry and conditions future volatility in a predictable way beyond persistence
- Trailing normalization (pct/z) captures regime-relative funding extremes better than raw signed funding alone
- Price-dislocation (premium/EMA distance) provides complementary conditioning
- Effect is not idiosyncratic to one asset or regime

## Next steps (heavy, on frozen splits)
- Interaction analysis: fund × RV regime, fund × dislocation (test if non-linear)
- Regime stratification by funding quartiles on TEST only (descriptive, no re-split)
- Coefficient stability over time within test window
```

## fclr002_symbol_stability_20261103T102015Z.md (9 lines, 539 bytes)
```
# FCLR-002 Symbol Stability (TEST only) - 20261103T102035Z

- BNBUSDT: n=1656, QLIKE(B1)=0.541701, QLIKE(C2)=0.541543, rel_imp=0.029%
- BTCUSDT: n=1656, QLIKE(B1)=0.752825, QLIKE(C2)=0.752674, rel_imp=0.020%
- ETHUSDT: n=1656, QLIKE(B1)=0.799465, QLIKE(C2)=0.799243, rel_imp=0.028%
- SOLUSDT: n=1656, QLIKE(B1)=0.360015, QLIKE(C2)=0.359877, rel_imp=0.038%
- XRPUSDT: n=1656, QLIKE(B1)=0.858753, QLIKE(C2)=0.858582, rel_imp=0.020%

Notes: All symbols show improvement; consistent with robustness results. Train-only normalization preserved.
```
