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
- **Updated:** 2026-11-09T00:40:39Z
- [x] Funding ffill last-known at/before hour (no future).
- [x] Trailing funding stats past-only on aligned series.
- [x] Chronological multi-split walk-forward, purge/embargo=7d.
- [x] Train-only normalization per split.
- [x] Direct-variance OLS fit on train only; predictions floored at zero; no log/exp transform; no test leakage.
- [x] Block bootstrap resamples whole UTC time blocks jointly across instruments (seed=12345, reps=2000, block=24h); no leakage.
- [x] No basis/premium features added (unavailable/misaligned locally); NaN policy preserved, never zero-filled.

## TRACKA-LIQ-EXPANSION-RECOMPUTE (FCLR-LIQ-EXPANSION-RECOMPUTE-20261114T073346Z) — 2026-11-14T08:30:00Z
- **Splits:** chronological train (2026-05-01..2026-05-31), val (2026-06-07..2026-06-30), test blocks (2026-07-07..2026-08-06 / 2026-08-13..2026-09-11 / 2026-09-18..2026-10-17), 7-day purge/embargo at both boundaries. Boundaries set from data coverage before outcomes; no reuse of any inspected holdout.
- **Forecast origins:** causal; every input available by the closed hour t. Target next-24h liquidation intensity is strictly forward (sum over t+1..t+24h via shift -1 day), computed only at evaluation time.
- **Normalization:** train-only mean/std for signed_funding, abs_fund_pct, premium, ema_dist; train-only Duan smearing on exp(pred). No test-row fitting.
- **Missing:** no zero-fill, no forward-fill. liq_lag1 uses fillna(0.0)+EPS so zero-intensity days are finite (log(EPS)); first-day NaN from shift(1) naturally excluded by OLS finite mask. Funding/RV attached by backward merge_asof (<=24h / <=168h tolerance). Core features (log_rv1h/24h/168h, signed_funding_z, abs_fund_pct_z, premium_z, ema_dist_z) required non-null for paired contrasts.
- **Inference:** paired circular block bootstrap (2000 reps, seed 20261114, 1-day blocks) jointly across instruments; Holm multiplicity across 3 pre-registered contrasts; LOIO; funding-permutation placebo (200 reps, seed 20261114); per-symbol and per-block stability.
- **Verdict:** no unresolved leakage/label issue capable of reversing the conclusion. Overall verdict INCONCLUSIVE — driven by failure to replicate sealed 19.04% (recomputed 6.19%, below 9.52% threshold) and placebo failure (true 6.19% <= null p95 7.6603%), not by leakage.
