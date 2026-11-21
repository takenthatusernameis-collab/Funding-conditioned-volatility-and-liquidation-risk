# FCLR-SESSION-SYNTHESIS-01 — Quantitative Meta-Analysis Report

- **Experiment ID:** FCLR-SESSION-SYNTHESIS-01-20261121T080000Z
- **Design:** outcome-blind inverse-variance fixed-effect + DerSimonian-Laird random-effects
- **Outcome data inspected before freeze:** `false` · **Generates no new outcomes:** `true`

## 1. Inputs

Both frozen panels were loaded and their sha256 asserted before any computation:

- FCLR-001: `41962f823e59de5989c7d854cb3180cad61a4cbc2f5f230133c41b321342c1f4`
  (29,136 rows × 22 cols, 5 coins, 5,832 hours)
- Combined liquidation: `81a100d5d0625832bebabaabea13b786e15319577721cfe8507da5b779ec7f14`
  (1,740,415 rows, 15 coins, 10,052 hourly buckets)

Terminal test statistics were loaded from the completed session evaluation JSONs for FCLR-XSEC-002,
FCLR-XSEC-004, FCLR-XSEC-005, and FCLR-XSEC-006 → **17 terminal funding-conditioning contrasts**.

## 2. Effect-size definition

Per terminal test: standardized funding-conditioning effect
`d = mean_diff_high_minus_low / mean_abs_outcome`.
Approximate variance from the CI half-width converted to the standardized scale.

## 3. Results

| Pillar | k | Fixed-effect pooled d (95% CI) | Random-effects DL pooled d (95% CI) | Cochran Q | I² |
|--------|---|-------------------------------|--------------------------------------|-----------|-----|
| RV | 2 | 1.237 (−0.187, 2.662) | 1.237 (−0.187, 2.662) | 0.99 | 0.0% |
| Liquidation | 15 | 0.379 (0.336, 0.422) | 0.228 (−0.046, 0.502) | 551.85 | 97.5% |
| Joint | 17 | 0.380 (0.337, 0.423) | 0.254 (−0.017, 0.525) | 554.22 | 97.1% |

## 4. Interpretation (scientific finding)

- **RV pillar:** the fixed-effect pooled d is large (1.237) but its 95% CI *includes zero*
  (k=2, the high-RV and low-RV contrasts). The RV funding-conditioning effect is not robustly
  non-zero once both regimes are combined — consistent with XSEC-002 being SUPPORTED only in the
  high-RV regime and the low-RV contrast including zero.

- **Liquidation pillar:** the fixed-effect pooled d (0.379) has a CI excluding zero, suggesting a
  real average funding-conditioning association. **However, heterogeneity is extreme
  (I² = 97.5%, Cochran Q = 551.85 on 14 df).** Under the DerSimonian-Laird random-effects model
  (which is the appropriate model under such heterogeneity), the pooled d drops to 0.228 and its 95%
  CI *includes zero* (−0.046, 0.502). The cross-sectional liquidation associations are therefore
  individually significant but **not homogeneous** — they vary so much across regimes/buckets that a
  single average effect is not robustly distinguishable from zero under random effects.

- **Joint pillar:** same pattern — fixed-effect excludes zero, random-effects includes zero, I²=97.1%.

## 5. Synthesis verdict

`CONSOLIDATORY_ONLY` — descriptive. The quantitative meta-analysis confirms that:

1. The cross-sectional funding-conditioning associations are statistically detectable in specific
   regimes (high-RV for RV; low-RV + UTC buckets for liquidation), consistent with the SUPPORTED
   XSEC-002/004/005/006 verdicts.
2. **They are not homogeneous** (I² ≈ 97%) and the random-effects pooled effect includes zero for
   both pillars.
3. Combined with the FAILED out-of-sample forward/forecast gates (FCLR-LIQ-OOS-FORECAST-001 QLIKE
   FAIL; all RV forward confirmations NOT_REPLICATED), the consolidated evidence does **not**
   support a promotable funding-conditioned forecast skill.

This meta-analysis does NOT promote any terminal hypothesis. It carries forward every honest
terminal verdict unchanged. Reopening requires `NEW_OBSERVED_LIQUIDATION_SOURCE`.

## 6. Cross-reference

FCLR-STARTER-001, FCLR-XSEC-001..008, FCLR-LIQ-OOS-FORECAST-001, FCLR-LIQ-COMBINED-PANEL,
Track A, Track B. Independent verification: `fclr_session_synth01_recompute_20261121T080000Z.json`
(stdlib-only recomputation of the fixed-effect pooled d per pillar).