# FCLR-XSEC-001 Within-Hour RV Persistence Baseline

**Session:** session_20261120T175300Z
**Experiment:** FCLR-XSEC-001-20261120T175300Z
**Baseline:** within_hour_rv_persistence

## Baseline Definition

Within-hour RV persistence: for each closed UTC hour t, split the 5 eligible
perpetual contracts by their own rv1h at t (percentile rank within hour,
<= 0.5 = high_rv, > 0.5 = low_rv). Compare next-hour realized variance
(rv1h at t+1) of high-rv vs low-rv coins within the same hour. Same paired
within-hour structure as the funding-contrast evaluation.

## Panel

- Path: research_state/fclr011_recompute_panel_20261115T234700Z.parquet
- SHA-256: 41962f823e59de5989c7d854cb3180cad61a4cbc2f5f230133c41b321342c1f4
- Hash verified: true
- Hash verified before target generation: true
- Coins: BNBUSDT, BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT (5)
- Coverage: 2026-01-01 through 2026-08-31 (5,785 hourly timestamps)
- Rows with next-hour target: 23,558

## Results

| Metric | Value |
|--------|-------|
| n_hours with both RV groups | 5,328 |
| mean diff (high_rv − low_rv) | 0.176794 |
| std diff | 11.301422 |
| positive diffs | 3,200 / 5,328 (60.06%) |

## Notes

- Holdout NOT opened.
- No model fitting; pure within-hour comparison. No train-only normalization needed.
- Positive diff share (60.06%) suggests high-rv coins tend to have higher next-hour RV, but no block-bootstrap CI or Holm correction applied at the baseline stage (those are applied in the evaluation phase).
- All inputs causal at t; no look-ahead.
