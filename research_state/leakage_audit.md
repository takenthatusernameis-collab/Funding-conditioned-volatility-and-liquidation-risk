# Leakage Audit

**Status:** Initial checklist (to be completed as pipeline built)

## Checks
- [ ] Timestamps normalized to UTC; alignment verified per source
- [ ] Features computed using only information at forecast timestamp (rolling windows use past only)
- [ ] Normalization/scaling/quantiles fit on training folds only
- [ ] Purge/embargo applied for overlapping horizons
- [ ] No random splits; chronological only
- [ ] Holdout sealed; protocol frozen before examination
- [ ] Missing data treated as missing (no zero-filling of basis/spot)
- [ ] Track A/B separation enforced
