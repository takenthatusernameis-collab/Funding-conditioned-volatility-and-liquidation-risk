# Pre-Registration — FCLR-FWD-VOL-2025-DISJOINT-RECONCILE-20261114T193000Z

Generated: 2026-11-14T20:15:00Z
Campaign: `FCLR-FWD-VOL-2025-DISJOINT-RECONCILE-20261114T193000Z`
Status: **FROZEN_PRE_OUTCOMES** (frozen before any outcome computation)

## Purpose

Attribute the EXPLORATORY_NULL of the 2025 disjoint cross (FCLR-FWD-VOL-2025-DISJOINT-CROSS-20261114T183000Z: pooled C2-B1 mean diff +0.006923, relative reduction -1.963%, 95% CI [-0.012604, 0.028030]) to estimator behaviour or to a data-lineage defect on the cached 2025 panel. Two-by-two attribution matrix over {existing panel, cleaned lineage copy} x {sealed estimator, corrected estimator}. All results EXPLORATORY_ONLY, promotable=false. Does not reopen any sealed verdict.

## Frozen inputs

- Existing panel: `research_state/tracka_fwd_vol_2025_disjoint_cross_panel_20261114T191615Z.parquet` (sha256 `de0ca73e7d092a205e5f8c1163d56437384d1b15d65b4a27bc54a57e21738cba`)
- Source prereg: `research_state/prereg_fclr_fwd_vol_2025_disjoint_cross_20261114T183000Z.json`
- Source evaluation: `research_state/evaluation_summary_FCLR-FWD-VOL-2025-DISJOINT-CROSS-20261114T191615Z.json`

## Frozen splits

- Block 0: train 2025-04-25T00:00:00Z .. 2025-05-24T23:00:00Z; test 2025-06-01T00:00:00Z .. 2025-06-30T23:00:00Z
- Block 1: train 2025-09-25T00:00:00Z .. 2025-10-24T23:00:00Z; test 2025-11-01T00:00:00Z .. 2025-11-30T23:00:00Z
- Block 2: train 2025-10-25T00:00:00Z .. 2025-11-23T23:00:00Z; test 2025-12-01T00:00:00Z .. 2025-12-31T23:00:00Z
- Embargo between train end and test start: 7 days

## Estimator arms

- Sealed estimator: raw features, ridge-stabilised normal equations, no scaling, no smearing, no target-derived fills.
- Corrected estimator: train-only standardization, finite-row masking, train-only log-target smearing, missingness drop-only.

## Panel arms

- Existing panel: exactly the frozen file above.
- Cleaned panel: removes the corrupted XRPUSDT mark rows for 2025-10-19 (close column holds premium-index values), recomputes XRP rolling RV/forward targets after removal, imputes nothing.

## Primary analysis

- Contrast: C2 vs B1 on the 24h target, paired out-of-sample QLIKE.
- Bootstrap: day-block, 2000 reps, seed 20261114; Holm over the horizon x contrast family.
- LOIO (>= 4/5), funding-permutation placebo (200 reps, seed 20261114).

## Verdict rule

- EXPLAINED_BY_ESTIMATOR / EXPLAINED_BY_DATA: a >= 1.0 percentage-point swing on the primary relative reduction that is >= 3x the opposite dimension's swing.
- UNEXPLAINED: no material dominant swing.
- INCONCLUSIVE: row-key/lineage check fails or a cell cannot be fitted.

## Non-goals

- Not promotable, EXPLORATORY_ONLY, no sealed verdict reopened, no new test month consumed.
