# Leakage Audit

**Last Updated:** 2026-11-07T00:30:45Z

## RV-only baseline (Gate 3)
- [x] Chronological walk-forward only (no random splits)
- [x] Purge/embargo applied between train/val/test
- [x] Normalization fitted on train only (applied to val/test)
- [x] Features use only past information at forecast origin
- [x] Forward RV target computed from future bars only at evaluation time (not used for fitting)
- [x] Missing data treated as NaN (not imputed as zero)
