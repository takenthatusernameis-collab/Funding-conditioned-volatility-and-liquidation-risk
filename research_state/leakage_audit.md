# Leakage Audit

**Last Updated:** 2026-11-07T01:14:16Z

## RV-only baseline (Gate 3)
- [x] Chronological walk-forward only (no random splits)
- [x] Purge/embargo applied between train/val/test
- [x] Normalization fitted on train only (applied to val/test)
- [x] Features use only past information at forecast origin
- [x] Forward RV target computed from future bars only at evaluation time (not used for fitting)
- [x] Missing data treated as NaN (not imputed as zero)

## FCLR-013 confirmatory reopen (2026-11-07T11:07:34Z) — leakage check
- **Splits:** chronological train/val/sealed-test, frozen_before_outcomes=true in `run_manifest.json` under `split_boundaries_fclr013`, matching `pre_registration_fclr013_20261107T094132Z.md` exactly (train 2026-07-01..2026-08-05; val 2026-08-06..2026-08-25; sealed test 2026-08-26..2026-09-30; purge/embargo 7d >= max horizon 24h). Boundaries set from data coverage before outcomes; no reuse of any inspected holdout.
- **Forecast origins:** causal; every input available by the closed hour t; next-24h RV target uses future bars t+1..t+24 only at evaluation time.
- **Normalization:** train-only means/stds; smearing correction for back-transform (train-fitted).
- **Missing:** core RV-missing rows dropped from comparison; no zero-fill of invented values; missing != 0 preserved where protocol allows.
- **Inference:** paired block bootstrap (24h blocks, 2000 reps, deterministic seed) jointly across instruments; Holm multiplicity across pre-registered family; no look-ahead.
- **Verdict:** no unresolved leakage/label issue capable of reversing the conclusion. Gate NOT_MET on outcome criteria (CI crosses zero, relative reduction -1.32% < 2% floor, only 1 non-overlapping 30-day test block < 3), not on leakage.

## Funding ablations (Gate 4, multi-split pilot, direct-variance OLS)
- **Updated:** 2026-11-08T20:25:00Z
- [x] Funding ffill last-known at/before hour (no future).
- [x] Trailing funding stats past-only on aligned series.
- [x] Chronological multi-split walk-forward, purge/embargo=7d.
- [x] Train-only normalization per split.
- [x] Direct-variance OLS fit on train only; predictions floored at zero; no log/exp transform; no test leakage.
- [x] Block bootstrap resamples whole UTC time blocks jointly across instruments (seed=12345, reps=2000, block=24h); no leakage.
- [x] No basis/premium features added (unavailable/misaligned locally); NaN policy preserved, never zero-filled.
