# Evaluation Summary - Funding Ablations (Gate 4, multi-split pilot)

**Generated:** 2026-11-07T19:17:03Z
**Git SHA:** cec2d5ca3c5537c3c9a7977e4c795d10f466a762
**Pre-registration:** `research_state/pre_registration_gate4_funding_multisplit_v4_20261107T1845Z.md` (frozen before outcomes)
**Scope:** BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT, BNBUSDT, 2024-04-01 to 2024-09-30, 24h forward RV, 3 pre-registered walk-forward splits
**Model:** direct-variance OLS HAR (target = forward realized VARIANCE; train-only normalization per split; no log/exp transform)
**Verdict:** **PILOT/INCONCLUSIVE (data-sufficiency criteria not met; no claim-worthy inference)**

## Data Sufficiency (honest)
- instruments=5 (required >=5): MET
- claim-worthy: False
- shortfall: insufficient_30day_non_overlapping_test_blocks (ok_30d=0, required>=3, split_test_days=[14, 14, 14])

## Aggregate (mean across OK splits)
| Ablation | QLIKE | MAE | RMSE | ΔQLIKE vs A (pooled paired) | 95% block-bootstrap CI | n_obs/n_blocks |
|---|---|---|---|---|---|---|
| A_rv_only | None | None | None | — | — | — |
| B_rv_signed | None | None | None | NA | NA | 0/0 |
| C_rv_abs | None | None | None | NA | NA | 0/0 |
| D_rv_signed_abs | None | None | None | NA | NA | 0/0 |
| E_rv_funding_trails | None | None | None | NA | NA | 0/0 |

## Per-Split Paired ΔQLIKE vs A (instability visibility)
| Contrast | Split 0 | Split 1 | Split 2 | n_obs (0/1/2) |
|---|---:|---:|---:|---|
| B_rv_signed vs A | NA | NA | NA | 0/0/0 |
| C_rv_abs vs A | NA | NA | NA | 0/0/0 |
| D_rv_signed_abs vs A | NA | NA | NA | 0/0/0 |
| E_rv_funding_trails vs A | NA | NA | NA | 0/0/0 |

## Exploratory Sensitivity (NOT confirmatory; do not promote if unstable)
> Block-bootstrap block size sensitivity for paired ΔQLIKE vs A. Pre-registered primary remains block=24h, seed=12345, reps=2000.
| Contrast | block=12h CI | block=24h CI (primary) | block=48h CI |
|---|---|---|---|
| B_rv_signed vs A | NA | NA | NA |
| C_rv_abs vs A | NA | NA | NA |
| D_rv_signed_abs vs A | NA | NA | NA |
| E_rv_funding_trails vs A | NA | NA | NA |

## Per-Split Details
- Split 0 (('2024-01-01T00:00:00+00:00', '2024-01-28T23:59:59+00:00') -> ('2024-02-05T00:00:00+00:00', '2024-02-18T23:59:59+00:00')): INSUFFICIENT_DATA n_train=0 n_test=0
- Split 1 (('2024-01-15T00:00:00+00:00', '2024-02-11T23:59:59+00:00') -> ('2024-02-19T00:00:00+00:00', '2024-03-03T23:59:59+00:00')): INSUFFICIENT_DATA n_train=0 n_test=0
- Split 2 (('2024-01-29T00:00:00+00:00', '2024-02-25T23:59:59+00:00') -> ('2024-03-04T00:00:00+00:00', '2024-03-17T23:59:59+00:00')): INSUFFICIENT_DATA n_train=0 n_test=0

## Bootstrap (pre-registered)
- Paired ΔQLIKE (alt-base; negative = better for QLIKE) with circular block bootstrap on whole UTC time blocks, jointly across instruments.
- seed=12345, reps=2000, block_hours=24, alpha=0.05, two-sided percentile CI.

## Leakage/Alignment Notes
- Funding (8h) aligned to 1h via last-known value at/before each hour (ffill). NaN if missing.
- Trailing funding pct/z computed over rolling windows on aligned series (past-only).
- Chronological splits, 7d purge/embargo, train-only normalization per split.
- Basis/premium not included (no aligned admissible local series verified); missing treated as NaN per policy.

## Caveats (non-negotiable)
- **Verdict:** PILOT/INCONCLUSIVE (data-sufficiency criteria not met; no claim-worthy inference)
- **Data sufficiency:** instruments=5 (MET); ok_30day_splits=0 (required>=3) => meets_claim_worthy_data_sufficiency=False.
- **No economic value claim, no overlay, no Track A linkage.** Observed metrics are out-of-sample forecast evidence under pre-registered design; instability across splits/instrument sets must be reported honestly.
- If any leakage/alignment doubt exists, treat as non-confirmatory.
