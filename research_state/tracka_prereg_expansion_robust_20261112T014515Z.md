# TRACKA-EXP-ROBUST-20261112T014515Z — Preregistration (Frozen Pre-Outcomes)

**Preregistered UTC:** 2026-11-12T01:45:15Z
**Campaign:** LIQUIDATION_EXPANSION_ROBUSTNESS_FALSIFICATION
**Track:** A
**Status:** PREREGISTERED_FROZEN_PRE_OUTCOMES

**Pivoted from:** Sealed PASS: `TRACKA-HL-EXPANSION-20261111T195500Z` (C2 vs B1 rel QLIKE reduction 19.04%, 95% CI [-5.088,-0.478], n=593, 8 instruments, 3 blocks, 2026-05..2026-10). Volatility family `TRACKA-VOL-FAMILY-20261112T005111Z` completed NOT_MET.

**Claim:** The sealed Track A liquidation expansion PASS (`TRACKA-HL-EXPANSION-20261111T195500Z`) is robust to: (1) leave-one-instrument-out sensitivity, (2) placebo/permutation on funding features, (3) alternative pre-specified block/bootstrap settings. All checks evaluated on the SAME frozen panel `research_state/tracka_hl_expansion_panel_20261111T202344Z.parquet` (sha256 `39916a72dfc37d15b6cc886d4e43ed878e0b8e1c2f22936fc4ebf8edd366f699`) with identical splits and features as the sealed PASS.

**Hypothesis ID:** `H_tracka_hl_expansion_robustness` (primary_tracka_expansion_robustness)
**Venue:** hyperliquid_perpetuals
**Data Source:** ironflow/hyperliquid-liquidations (CC BY 4.0, unauthenticated HF bulk parquet, observed_only=true, modeled_or_proxy=false)

## Panel (Frozen, Identical to Sealed PASS)
- **Panel Artifact:** `research_state/tracka_hl_expansion_panel_20261111T202344Z.parquet`
- **Panel SHA256:** `39916a72dfc37d15b6cc886d4e43ed878e0b8e1c2f22936fc4ebf8edd366f699`
- **Build Report:** `research_state/tracka_hl_expansion_panel_build_report_20261111T202344Z.json`
- **Universe Symbols:** ZEC, NEAR, UNI, AAVE, CRV, ADA, LTC, BCH (8 instruments)
- **Time Window:** 2026-05-01T00:00:00Z .. 2026-10-31T23:59:59Z
- **Label:** observed_hyperliquid_liquidation_event_intensity (notional_usd-weighted observed ironflow liquidation event count per symbol per 24h UTC bucket)
- **Target:** next-24h observed liquidation intensity per symbol per 24h UTC bucket

### Split Boundaries (IDENTICAL to Sealed PASS, Frozen Pre-Outcomes)
- **Train:** 2026-05-01T00:00:00Z .. 2026-05-31T23:00:00Z
- **Validation:** 2026-06-07T00:00:00Z .. 2026-06-30T23:00:00Z (7-day embargo)
- **Test Blocks (3, 30-day each with 7-day embargo):**
  1. 2026-07-07T00:00:00Z .. 2026-08-06T23:00:00Z
  2. 2026-08-13T00:00:00Z .. 2026-09-11T23:00:00Z
  3. 2026-09-18T00:00:00Z .. 2026-10-17T23:00:00Z
- **n_test_blocks:** 3

## Models & Contrast
- **Baselines:** B1 (RV-only: log(rv1h), log(rv24h), log(rv168h))
- **Models:** C2 (B1 + fundingRate, abs_fund_pct, premium, ema_dist)
- **Primary Contrast:** C2 vs B1
- **Primary Target:** next-24h observed liquidation intensity
- **Metric:** QLIKE (lower is better)

## Original Sealed PASS Results (Reference)
- **Rel QLIKE Reduction:** 19.04%
- **95% CI:** [-5.088, -0.478] (excludes zero, favors C2)
- **Paired n:** 593
- **Test Blocks:** 3
- **Instruments:** 8

## Robustness Checks (Pre-Registered Ex-Ante with Pass/Fail Criteria)

### Check 1: Leave-One-Instrument-Out (LOIO) Sensitivity
**Procedure:** For each held-out instrument in [ZEC, NEAR, UNI, AAVE, CRV, ADA, LTC, BCH]: build panel subset excluding that instrument; run pre-registered C2 vs B1 evaluation (identical features, splits, bootstrap seed=20261111, 2000 reps) on the remaining 7 instruments; record rel QLIKE reduction % and 95% CI.

**Pass Criterion:** PASS if **≥6 of 8** LOIO runs show rel QLIKE reduction **≥2%** AND 95% CI excludes zero (hi < 0) favoring C2. FAIL otherwise.

**Seed:** 20261111 | **Bootstrap Reps:** 2000

### Check 2: Placebo/Permutation on Funding Features
**Procedure:** For each of the 8 instruments independently: within the panel, permute the `fundingRate` column across timestamps (random permutation without replacement within that instrument). Do the same for `abs_fund_pct`. Keep all other features (RV, premium, ema_dist) and the target unchanged. Re-run C2 vs B1 evaluation (identical features except permuted funding, identical splits, bootstrap seed=20261112, 2000 reps). Repeat for **1000 placebo permutations** to build null distribution of rel QLIKE reduction.

**Pass Criterion:** PASS if the **TRUE (original, non-permuted) rel QLIKE reduction (19.04%) > 95th percentile** of the placebo null distribution. FAIL if true reduction ≤ 95th percentile (i.e., p ≥ 0.05).

**Seed:** 20261112 | **Permutations:** 1000 | **Bootstrap Reps:** 2000

### Check 3: Alternative Block/Bootstrap Settings
**Procedure:** Run C2 vs B1 evaluation on the full 8-instrument panel with three alternative pre-specified bootstrap configurations:

| Setting | Method | Block Size / Mean Block | Reps | Seed |
|---------|--------|------------------------|------|------|
| (a) | circular | 48h | 5000 | 20261111 |
| (b) | stationary | 24h (mean) | 5000 | 20261112 |
| (c) | circular | 24h | 5000 | 20261111 |

**Pass Criterion:** PASS if **ALL THREE** settings yield rel QLIKE reduction **≥2%** AND 95% CI excludes zero (hi < 0) favoring C2. FAIL if any setting fails either criterion.

**Note:** Original PASS used circular block_size=24h, 2000 reps, seed=20261111. This check tests robustness to block size doubling, stationary bootstrap, and increased reps.

## Overall Verdict Rule
- **ROBUST:** All three checks (LOIO, Placebo/Permutation, Bootstrap Settings) PASS.
- **FRAGILE:** Any one check FAILS. Document exact failure mode.
- **INCONCLUSIVE:** Computational infeasibility (e.g., memory/time exhaustion) prevents completion of any check. Document specific infeasibility.

## Next on FRAGILE
If FRAGILE: document exact failure mode; preregister and attempt next best admissible untested claim in-session (e.g., alternate volatility design on cached HL 2025-11..2026-10 with different pre-specified horizon/features/splits) repeating Steps 1-4. Do not stop at first failure.

## Materiality Gate (Identical to Sealed PASS)
- min_relative_reduction_pct: 2.0
- ci_excludes_zero: true
- min_paired_instruments: 5
- min_test_blocks: 3
- all_required: true

## Event Adequacy Rule
Same as sealed PASS: claim-worthy only if ≥5 paired instruments with label coverage in test blocks, ≥3 non-overlapping 30-day test blocks with data, RV24h/B1 computable for test blocks, label variance >0 across test blocks.

## Forbidden (Binding)
- No outcome inspection before preregistration freeze
- No threshold-shopping on test set
- No sealed-holdout reuse (FCLR-002/FCLR-003/Track B/C test sets sealed)
- No Binance/2024 conflation (Hyperliquid only, admissible overlap)
- No modeled/proxy/synthetic liquidation labels (observed ironflow events only)
- No redundant network polling (panel is cached and frozen)
- No post-hoc symbol selection based on outcomes/forecast results
- No agent-set RESOLVED_VERIFIED/fabricated=true; no Gate 4 bypass
- No mutation of sealed/closed verdicts (TRACKA-HL-EXPANSION-20261111T195500Z, TRACKA-VOL-FAMILY-20261112T005111Z, etc.)

## Atomic State Updates Required (Mandatory)
1. `research_state/experiment_frontier.json`
2. `research_state/hypothesis_registry.json` (add `H_tracka_hl_expansion_robustness` status)
3. `research_state/run_manifest.json` (run `EXP-ROBUST-20261112T014515Z`)
4. `research_state/final_confirmatory_verdict.md` (append addendum)

## Gate 4 Note
Gate 4 Branch 1 remains EXTERNAL_BLOCKED (no valid RESOLVED_VERIFIED terms evidence; human/legal review required; agent cannot set RESOLVED_VERIFIED). This prereg executes the robustness/falsification campaign only.