# FCLR-LIQ-RISK-RECALIBRATION-07 — Train-Only Recalibration of Modeled Breach Risk

**Session:** `session_20261118T191945Z`
**Campaign:** `FCLR-LIQ-RISK-RECALIBRATION-07-20261118T191714Z`
**Label:** EXPLORATORY/PILOT — **not confirmatory**.
**Outcome:** `synthetic_modeled_boundary_breach`, `observed_liquidation_labels=false`.
**Stdlib only**; no network; no parquet; no sealed months.

**Verdict:** `HONEST_NEGATIVE_OR_INCONCLUSIVE`

## Materiality floor

| Calibrator | ΔBrier sig. holdouts (of 3) | ΔECE≥0.005 holdouts (of 3) | real mean ΔBrier | placebo p95 | floor met |
|---|---|---|---|---|---|
| C1_platt | 1 | 0 | -0.000076 | -0.000437 | False |
| C3_prior_offset | 1 | 0 | -0.000006 | -0.000006 | False |

## Primary scenario `L10|long|H24` — ΔBrier / ΔECE vs uncalibrated base

| Holdout | Calibrator | ΔBrier | CI95 | ΔECE | CI95 | Brier C0 | Brier Cm |
|---|---|---|---|---|---|---|---|
| 2024-07 | C1_platt | -0.000203 | [-0.000836, 0.000140] | -0.001600 | [-0.003132, 0.005625] | 0.020497 | 0.020700 |
| 2024-07 | C2_isotonic | -0.000041 | [-0.000085, 0.000019] | 0.002810 | [-0.007265, 0.006536] | 0.020497 | 0.020538 |
| 2024-07 | C3_prior_offset | -0.000001 | [-0.000011, 0.000003] | 0.000009 | [-0.000015, 0.000122] | 0.020497 | 0.020499 |
| 2024-08 | C1_platt | 0.001173 | [0.000027, 0.002575] | -0.004137 | [-0.006823, 0.008312] | 0.034902 | 0.033729 |
| 2024-08 | C2_isotonic | -0.003381 | [-0.008152, -0.000398] | -0.020168 | [-0.033369, -0.000635] | 0.034902 | 0.038284 |
| 2024-08 | C3_prior_offset | 0.000124 | [-0.000244, 0.000438] | 0.000367 | [-0.001540, 0.002503] | 0.034902 | 0.034778 |
| 2024-09 | C1_platt | -0.000033 | [-0.000052, -0.000013] | -0.000910 | [-0.001319, -0.000533] | 0.000992 | 0.001025 |
| 2024-09 | C2_isotonic | -0.000043 | [-0.000061, -0.000027] | -0.001034 | [-0.001309, -0.000710] | 0.000992 | 0.001035 |
| 2024-09 | C3_prior_offset | 0.000021 | [0.000020, 0.000022] | 0.000528 | [0.000519, 0.000535] | 0.000992 | 0.000970 |

## Pooled equal-weight deltas over 12 scenarios (mean inside each holdout)

| Holdout | Calibrator | mean ΔBrier | mean ΔECE | mean Δlogloss |
|---|---|---|---|---|
| 2024-07 | C1_platt | -0.000061 | -0.000781 | -0.000997 |
| 2024-07 | C2_isotonic | -0.000095 | -0.001941 | -0.001319 |
| 2024-07 | C3_prior_offset | -0.000048 | -0.000363 | -0.000379 |
| 2024-08 | C1_platt | -0.000068 | -0.003366 | 0.007371 |
| 2024-08 | C2_isotonic | -0.000686 | -0.004582 | 0.002257 |
| 2024-08 | C3_prior_offset | 0.000014 | 0.000028 | -0.001280 |
| 2024-09 | C1_platt | -0.000100 | -0.001166 | -0.000713 |
| 2024-09 | C2_isotonic | -0.000073 | -0.002840 | -0.000513 |
| 2024-09 | C3_prior_offset | 0.000016 | 0.000248 | 0.000137 |

## Label-permutation placebo (200 draws, mean over scenarios)

| Holdout | Calibrator | real mean ΔBrier | null mean | null p95 |
|---|---|---|---|---|
| 2024-07 | C1_platt | -0.000061 | -0.000300 | -0.000256 |
| 2024-07 | C2_isotonic | -0.000095 | -0.000247 | -0.000185 |
| 2024-07 | C3_prior_offset | -0.000048 | -0.000048 | -0.000048 |
| 2024-08 | C1_platt | -0.000068 | -0.000911 | -0.000839 |
| 2024-08 | C2_isotonic | -0.000686 | -0.000797 | -0.000709 |
| 2024-08 | C3_prior_offset | 0.000014 | 0.000014 | 0.000014 |
| 2024-09 | C1_platt | -0.000100 | -0.000236 | -0.000216 |
| 2024-09 | C2_isotonic | -0.000073 | -0.000217 | -0.000184 |
| 2024-09 | C3_prior_offset | 0.000016 | 0.000016 | 0.000016 |

## Cross-scenario transfer (fit on A train OOF, apply to B test)

| Holdout | Calibrator | mean ΔBrier over ordered pairs | sign agreement |
|---|---|---|---|
| 2024-07 | C1_platt | -0.028246 | 0.553030303030303 |
| 2024-07 | C3_prior_offset | -0.000123 | 0.5984848484848485 |
| 2024-08 | C1_platt | -0.002837 | 0.7121212121212122 |
| 2024-08 | C3_prior_offset | -0.000176 | 0.553030303030303 |
| 2024-09 | C1_platt | -0.010457 | 0.3409090909090909 |
| 2024-09 | C3_prior_offset | -0.000015 | 0.5984848484848485 |

## Honest status

EXPLORATORY/PILOT. Modeled boundary breaches only; not observed liquidations. Three chronological holdouts, 7-day purge/embargo; train-only recalibration on OOF scores; UTC-day block bootstrap; label-permutation placebo. No confirmatory claim.

Calibration deciles / reliability diagnostics and per-scenario metrics are in the JSON.
