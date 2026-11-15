# FCLR Power/MDE Calibration — FCLR-POWER-CALIBRATION-2026-11-15T01:34:12Z

- generated_utc: `2026-11-15T01:34:12Z`
- status: `VALID_EXPLORATORY`  verdict: `INCONCLUSIVE`  max_status: `EXPLORATORY_ONLY`  promotable: `False`
- prereg: `research_state/prereg_fclr_power_calibration_2026-11-15T01:34:12Z.json`
- No model re-fit, no sealed-contrast recomputation, no sealed verdict changed.

## Volatility forward (2025 disjoint)
- track verdict (primary h24 C2_vs_B1): **NULL_UNDERPOWERED**
- primary h24 C2_vs_B1: SE=0.010469953, MDE80=0.029332466 QLIKE, floor=0.007052315476086073, power=0.103379
- per-horizon C2_vs_B1:
  - h6: n=10800 days=90 SE=0.011721151 MDE80=0.032837804 floor=0.01351799321902876 power=0.210855 verdict=NULL_UNDERPOWERED
  - h24: n=10800 days=90 SE=0.010469953 MDE80=0.029332466 floor=0.007052315476086073 power=0.103379 verdict=NULL_UNDERPOWERED
  - h72: n=10560 days=88 SE=0.003521863 MDE80=0.009866801 floor=0.0038899113888369793 power=0.197238 verdict=NULL_UNDERPOWERED
  - h168: n=10080 days=84 SE=0.003147352 MDE80=0.008817575 floor=0.002903074401991548 power=0.151707 verdict=NULL_UNDERPOWERED

## Observed liquidation cross-section (forward)
- track verdict (pooled): **INCONCLUSIVE**
- pooled: SE=0.012089358, MDE80=0.033869366 IC, floor=0.05, power=0.985219, symmetry_pass=False (mid=-0.000887169, frac=0.0223072)
- sign consistency: 3/3 same sign (met=True), ICs=[-0.04092235444458491, -0.03124730002096616, -0.008922015565550372]
- per-block (SE is pooled-null n-scaled approximation, flagged):
  - block_0: n=2996 ic=-0.0409224 SE~0.017989540 MDE80~0.050399230 power~0.793730 verdict=NULL_UNDERPOWERED
  - block_1: n=1605 ic=-0.0312473 SE~0.024578391 MDE80~0.068858457 power~0.529664 verdict=NULL_UNDERPOWERED
  - block_2: n=2033 ic=-0.00892202 SE~0.021838473 MDE80~0.061182344 power~0.629150 verdict=NULL_UNDERPOWERED

## Known-answer self-test
- recovered=True (SE 0.1 vs 0.1, power 0.850839) — NOT market evidence

## Interpretation guardrails
- EXPLORATORY_ONLY, promotable=false; does not reopen sealed verdicts or claim a market effect.
