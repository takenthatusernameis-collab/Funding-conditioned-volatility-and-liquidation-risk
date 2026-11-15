# Pre-Registration — FCLR-FWD-VOL-2025-DISJOINT-CORRECTED-AUDIT-2026-11-15T00:12:56Z

Generated: 2026-11-15T00:12:56Z
Campaign: `FCLR-FWD-VOL-2025-DISJOINT-CORRECTED-AUDIT`
Status: **FROZEN_PRE_OUTCOMES** (frozen before any outcome computation)

## Purpose

Test whether the 2025 disjoint EXPLORATORY_NULL / UNEXPLAINED reconcile (FCLR-FWD-VOL-2025-DISJOINT-CROSS-20261114T183000Z: pooled C2-B1 24h QLIKE relative reduction -1.963%, 95% CI [-0.012604, 0.028030]) is estimator-sensitive. Runs the corrected estimator (train-only standardization, finite-row masking, train-only log-target Duan smearing, drop-only missingness) on the frozen cached 2025 disjoint panel and contrasts against the recorded sealed reference from evaluation_summary_FCLR-FWD-VOL-2025-DISJOINT-CROSS-20261114T191615Z.json. No sealed scripts or artifacts are re-executed or mutated. All results EXPLORATORY_ONLY, promotable=false.

## Frozen inputs

- Panel: `research_state/tracka_fwd_vol_2025_disjoint_cross_panel_20261114T191615Z.parquet` (sha256 `de0ca73e7d092a205e5f8c1163d56437384d1b15d65b4a27bc54a57e21738cba`)
- Sealed reference: `research_state/evaluation_summary_FCLR-FWD-VOL-2025-DISJOINT-CROSS-20261114T191615Z.json` (rel_reduction -1.963%, CI [-0.012604, 0.028030])

## Frozen splits

- Block 0: train 2025-04-25T00:00:00Z .. 2025-05-24T23:00:00Z; test 2025-06-01T00:00:00Z .. 2025-06-30T23:00:00Z
- Block 1: train 2025-09-25T00:00:00Z .. 2025-10-24T23:00:00Z; test 2025-11-01T00:00:00Z .. 2025-11-30T23:00:00Z
- Block 2: train 2025-10-25T00:00:00Z .. 2025-11-23T23:00:00Z; test 2025-12-01T00:00:00Z .. 2025-12-31T23:00:00Z
- Embargo between train end and test start: 7 days

## Estimator arm

- Corrected estimator: train-only standardization, finite-row masking (drop row, never fill), train-only log-target Duan smearing, drop-only missingness.

## Primary analysis

- Contrast: C2 vs B1 on the 24h target, paired out-of-sample QLIKE, pooled across 3 blocks.
- Bootstrap: day-block, 2000 reps, seed 20261114; Holm over horizon x contrast family.
- LOIO (>= 4/5), funding-permutation placebo (200 reps, seed 20261114).

## Verdict rule

- EXPLAINED_BY_ESTIMATOR: corrected vs sealed reference swing >= 1.0 percentage point on the primary relative reduction, or sign flip with magnitude >= 1.0.
- NOT_EXPLAINED_BY_ESTIMATOR: corrected within 1.0 pp of sealed reference with no material sign flip.
- INCONCLUSIVE: panel hash/row-key/lineage check fails, or a cell cannot be fitted.

## Non-goals

- Not promotable, EXPLORATORY_ONLY, no sealed verdict reopened, no new test month consumed.
