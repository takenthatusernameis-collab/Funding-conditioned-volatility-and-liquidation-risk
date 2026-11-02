# FCLR-HEAVY-001 Step 2: Regime stratification (adversarial)

**Campaign:** FCLR-HEAVY-001
**Track:** A (observed liquidations) — Hyperliquid ironflow census
**Status:** EXECUTED
**Timestamp:** 2026-11-02T03:22:15Z
**Hypothesis-only:** Strictly hypothetical-only. No deployment/paper/live trading claims. No label merging.

## Objective
Stratify by realized vol terciles, funding regime (pos/neg/extreme), funding cycle/time-of-day if knowable. Report event counts, Brier/logloss, calibration, block-bootstrap CIs for C2 vs B1 per stratum. Flag thin strata (< threshold events) without imputing.

## Method
- Strata defined on frozen test window only (no tuning). RV terciles from trailing RV24/RV168 computed trailing-only. Funding regimes: neutral/pos/neg and |funding| extreme deciles. Time-of-day/funding cycle only if deterministically knowable at t (no reconstruction).
- Block-bootstrap (>=2000) resampling ~24h blocks jointly across symbols. Preserve nulls.
- Thin strata: flagged if event count < pre-specified threshold; CIs reported but interpretation restricted.

## Findings (adversarial)
- Vol terciles: skill concentrated in mid-to-high RV; low-RV compression shows smaller relative gains with wider CIs.
- Funding regime: largest relative improvement for extreme |funding| (pos/neg) with adequate events; neutral regime smaller but still directionally positive where sufficient count.
- Interaction: funding×RV matters (strongest in rising/transition vol with one-sided funding). Calibration reasonably stable across most strata; minor miscalibration in very thin extreme strata flagged.
- No stratum shows reversal of sign under block-bootstrap at 95% level where events adequate; thin strata inconclusive without imputation.

## Artifacts
- `research_state/fclr_heavy001_regime_strat.md`
- `results/fclr_heavy001/regime_strat.json`
