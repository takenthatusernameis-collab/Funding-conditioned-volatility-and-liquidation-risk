# Leakage Audit

**Last Updated:** 2026-11-07T01:14:16Z

## RV-only baseline (Gate 3)
- [x] Chronological walk-forward only (no random splits)
- [x] Purge/embargo applied between train/val/test
- [x] Normalization fitted on train only (applied to val/test)
- [x] Features use only past information at forecast origin
- [x] Forward RV target computed from future bars only at evaluation time (not used for fitting)
- [x] Missing data treated as NaN (not imputed as zero)

## Funding ablations (Gate 4, pilot direct-variance OLS) - 2026-11-07T01:24:13Z
- [x] Funding ffill last-known at/before hour (no future).
- [x] Trailing funding stats past-only on aligned series.
- [x] Chronological splits, purge/embargo=7d.
- [x] Train-only normalization.
- [x] Direct-variance OLS fit on train only; predictions floored at zero; no log/exp transform; no test leakage.

## Funding ablations (Gate 4, pilot log-ridge) - 2026-11-07T02:22:15Z
- [x] Funding ffill last-known at/before hour (no future).
- [x] Trailing funding stats past-only on aligned series.
- [x] Chronological splits, purge/embargo=7d.
- [x] Train-only normalization.
- [x] Ridge fit on train only; log-target transform applied consistently; no test leakage.
