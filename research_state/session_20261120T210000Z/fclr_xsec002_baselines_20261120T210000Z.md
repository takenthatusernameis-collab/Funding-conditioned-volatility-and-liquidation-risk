# FCLR-XSEC-002 Within-Regime RV Persistence Baselines

**Session:** session_20261120T210000Z
**Experiment:** FCLR-XSEC-002-20261120T210000Z
**Baseline:** within_regime_rv_persistence

## Baseline Definition

Within-regime RV persistence: for each closed UTC hour t, compute the market-wide
RV at t as the cross-sectional mean of coin rv1h across the 5 eligible coins.
Split hours into high vs low market-wide-RV tercile. Within each regime and hour,
split coins by their own rv1h at t (percentile rank within hour within regime,
<= 0.5 = high_rv, > 0.5 = low_rv). Compare next-hour realized variance
(rv1h at t+1) of high-rv vs low-rv coins within the same hour and regime. Same
paired within-hour structure as the funding-contrast evaluation, now computed
per regime.

## Panel

- Path: research_state/fclr011_recompute_panel_20261115T234700Z.parquet
- SHA-256: 41962f823e59de5989c7d854cb3180cad61a4cbc2f5f230133c41b321342c1f4
- Hash verified: true
- Hash verified before target generation: true
- Coins: BNBUSDT, BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT (5)
- Coverage: 2026-01-01 through 2026-08-31 (5,832 distinct hourly timestamps)
- Hours with target: 4,638 (rows with next-hour target: 21,650)
- Hours regime-eligible (>= 3 coins with valid rv1h): 3,092
- Market-wide RV tercile low boundary: 4.232e-06
- Market-wide RV tercile high boundary: 1.896e-05

## Per-Regime Results

| Metric | high_rv_regime | low_rv_regime |
|--------|---------------|---------------|
| n_hours in regime | 1,546 | 1,546 |
| n_rows with target | 6,813 | 7,484 |
| n_hours with both RV groups | 1,546 | 1,546 |
| mean diff (high_rv − low_rv) | 0.264239 | 0.134265 |
| std diff | 6.060799 | 5.277209 |
| positive diffs | 1,065 / 1,546 (68.89%) | 797 / 1,546 (51.55%) |

## Notes

- Holdout NOT opened.
- No model fitting; pure within-hour comparison within regime. No train-only normalization needed.
- Middle tercile hours excluded from primary contrast; registered robustness cuts (high/low median split, UTC-session buckets) are computed in the evaluation phase.
- All inputs causal at t; no look-ahead.
