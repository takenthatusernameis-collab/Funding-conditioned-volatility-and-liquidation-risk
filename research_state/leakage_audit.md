# Leakage Audit

**Last Updated:** 2026-11-07T01:14:16Z

## RV-only baseline (Gate 3)
- [x] Chronological walk-forward only (no random splits)
- [x] Purge/embargo applied between train/val/test
- [x] Normalization fitted on train only (applied to val/test)
- [x] Features use only past information at forecast origin
- [x] Forward RV target computed from future bars only at evaluation time (not used for fitting)
- [x] Missing data treated as NaN (not imputed as zero)

## Funding ablations (Gate 4, multi-split pilot, direct-variance OLS)
- **Updated:** 2026-11-07T03:29:01Z (latest run: v2 5-symbol side run; v1 4-symbol outputs preserved separately)
- **v1 prereg:** `research_state/pre_registration_gate4_funding_multisplit_20261107.md` (unchanged). **v2 prereg (frozen before outcomes):** `research_state/pre_registration_gate4_funding_multisplit_v2_5sym_20261107T032439Z.md`.
- [x] Funding ffill last-known at/before hour (no future).
- [x] Trailing funding stats past-only on aligned series.
- [x] Chronological multi-split walk-forward, purge/embargo=7d.
- [x] Train-only normalization per split.
- [x] Direct-variance OLS fit on train only; predictions floored at zero; no log/exp transform; no test leakage.
- [x] Block bootstrap resamples whole UTC time blocks jointly across instruments (seed=12345, reps=2000, block=24h); no leakage.
- [x] No basis/premium features added (unavailable/misaligned locally); NaN policy preserved, never zero-filled.
