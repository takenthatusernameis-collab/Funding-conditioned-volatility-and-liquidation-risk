# Step 5 — Power/Coverage Audit, Label Ceiling, Concentration

**Campaign:** FCLR-EARLY4H-2025H1-LIQ-GLM v1 (parent)
**Generated (UTC):** 2026-11-12T16:52:10Z
**Parent verdict:** `INCONCLUSIVE_NUMERICAL_INSTABILITY`
**Parent eval:** `research_state/evaluation_summary_EARLY4H-2025H1-LIQ-GLM-20261112T164926Z.{md,json}`

This is the Step 5 follow-up required by the frozen `liq`-glm prereg. It is diagnostic only; no new gate is declared here.

## 1. Power / coverage

- 9 instruments, 394,167 observed events, ~$23.38B notional, 2025-05-25..2025-10-31.
- Every test block has 246-261 positive `t1_liq` days (270 rows each). **Power is not the binding constraint.**
- BTC+ETH = **63.6% of events / 83.6% of notional**. Per-coin reporting is mandatory; no PASS may be BTC/ETH-only.
- Top-5 sub-cohort (BTC, ETH, SOL, XRP, DOGE) = 94.2% of events; adequately powered but more concentrated than the full 9-coin panel. Not preferred.

## 2. Where the instability comes from

The `liq`-GLM failure is **localized, not global**:

| Model | Rows with QLIKE > 1e6 | Max row QLIKE | Location |
|---|---|---|---|
| B1 (RV-only) | 0 / 1016 | 212.8 | none |
| C1 | 1 / 1016 | 4.83e6 | block 3 / SOL |
| C2 | 2 / 1016 | 3.48e9 | block 3 / SOL, DOGE |

All offending rows are in **test block 3 (2025-09-29..2025-10-28, the Oct-2025 funding spike)**. There:

- `fundingRate` min `-0.001315` vs train max magnitude `4.75e-5` → **~27.7× outside the training range**.
- `premium` min `-0.01102` vs train min `-0.000880` → **~12.5× outside**.
- `ema_dist` max `0.390` vs train max `0.0860` → **~4.5× outside**.

Blocks 0-2 are entirely inside the training range and are stable. The log-link linear predictor extrapolates only where the raw features leave the training support. This is a bounded-feature problem, not a sample-size or label problem.

## 3. Label ceiling (2024-08..2025-04 extension)

Observed ironflow liquidation labels exist only for **2025-05-25 .. 2026-10-31**. There are **no labels before 2025-05-25**. The 2024-08..2025-04 4h-candle/funding extension is therefore structurally impossible for an observed-label test; do not fabricate, proxy, or model it.

## 4. Concentration

BTC+ETH are ~63.6% of events and ~83.6% of notional. Any future PASS must show per-coin stability and must not be driven by BTC/ETH alone.

## 5. Binding constraint and next focus campaign

**Binding constraint:** out-of-range extrapolation of raw `fundingRate` / `premium` / `ema_dist` in block 3 — not sample size, not label availability.

**Next campaign — `FCLR-EARLY4H-2025H1-LIQ-GLM-ROBUST v1` (`TRACKA-HL-EARLY4H-2025H1-LIQ-GLM-ROBUST`):**
- Same Poisson/quasi-Poisson log-link IRLS, same panel/splits/universe.
- Clip each continuous feature (`fundingRate`, `abs_fund_pct`, `premium`, `ema_dist`) to the **training-set observed [min, max]** (computed on positive-`t1_liq` train rows), then standardize by training mean/std. RV log features unchanged.
- New frozen prereg required before any outcome (a new estimator form).
- Gate: ≥2% relative QLIKE reduction AND 95% CI upper < 0 AND ≥5 instruments AND ≥3 blocks AND Holm across the family AND no single-coin driver AND max row QLIKE ≤ 1e6.
- If again `INCONCLUSIVE_NUMERICAL_INSTABILITY`: emit a timestamped evidenced structural-blocker document with the exact failing minima and stop; do not iterate estimator forms without a materially new source or a new preregistered design.