# FCLR-LIVE-ARCHIVE-03 Evidence Audit (20261126T051548Z)

**Experiment:** FCLR-LIVE-ARCHIVE-03
**Campaign:** FCLR-LIVE-ARCHIVE-03-20261126T042519Z
**Verdict:** `NOT_SUPPORTED`
**Audit pass:** true
**Unresolved blockers:** none

## Checks
- Source verified (Binance public archive, unauthenticated): true
- Cache reused read-only (session_20261126T042519Z/raw/): true, 1200/1200 zips, 0 missing
- Checksums present and verified: true
- Prereg frozen before outcomes: true (outcome_data_inspected_before_freeze:false)
- Prereg hash-bound to source registry: true
- Train-only stress threshold (95th percentile of train next-24h RV): true
- Train-only scaling/standardization: true
- 7-day (168h) purge/embargo at all boundaries: true
- Paired contrast C2 vs B1 on test-set Brier score: true
- Block bootstrap >=2000 replicates (seed fixed): true
- Independent stdlib recompute: true, all_checks_match:true
- No zero-byte placeholders: true
- Stdlib only, no network: true

## Eval summary
- Brier B1 = 0.018753, Brier C2 = 0.018667
- Relative Brier reduction C2 vs B1 = 0.46% (floor 2%)
- 95% CI relative Brier reduction = [-0.97%, 1.97%] (includes 0)
- n_test = 35715, stress events = 748 (2.09%)
- Verdict: NOT_SUPPORTED (reduction < 2% floor and CI includes 0)

## Leakage audit
- Outcome data inspected before freeze: false
- Target built after prereg: true
- Threshold train-only: true
- Embargo applied at all boundaries: true
- Scaling train-only: true

## Notes
Funding + price features do not clear the frozen 2% relative Brier floor for the
next-24h realized-variance STRESS / tail-exceedance target on the 4-year (2021-2024)
Binance archive, 5-symbol cohort. A valid, publishable null. Independent stdlib
recompute reproduces Brier/log-loss levels and the NOT_SUPPORTED verdict.
