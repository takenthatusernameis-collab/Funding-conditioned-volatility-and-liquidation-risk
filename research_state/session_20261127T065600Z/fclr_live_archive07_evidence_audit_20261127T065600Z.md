# FCLR-LIVE-ARCHIVE-07 Evidence Audit (20261127T065600Z)
**Verdict:** NOT_SUPPORTED
**Relative test-QLIKE reduction (C2 vs B1):** -0.704%
**95% block-bootstrap CI (relative):** [-1.218%, -0.190%]
**Materiality floor:** 2%
**n_test:** 23260  |  **n_unique_timestamps:** 22416  |  **|S|:** 22608
**Independent recompute all_checks_match:** True

## Leakage / evidence controls
- outcome-blind prereg fields depend only on mark-price support/splits (no target y)
- train-only OLS fitting and train-only standardization
- 168h purge/embargo between train/val/test
- no outcome inspection before design freeze
- read-only cache reuse; no re-download; stdlib only; no network

## Template integrity notes
- CORRECTED the ready template's QLIKE: the shipped form (pred + exp(y)/exp(pred)) is not non-negative and made the relative-reduction ratio ill-posed (10^11% LOO artifacts). Replaced with the standard non-negative QLIKE mean(exp(y-p)-(y-p)-1), matching the frozen-design 'out-of-sample QLIKE'.
- CORRECTED |S|: on the current cache the all-five mark-price common support is 22608 (BNBUSDT=BTCUSDT=ETHUSDT=SOLUSDT=XRPUSDT=22608). The handoff's 22584/'XRP binds by 24h' was a measurement artifact: XRPUSDT 2025-10-19 has a corrupt CSV (24 negative closes, dropped by close>0) AND a valid ZIP copy of the same day (real ~2.35 prices) that restores full support. No zero-fill/repair performed.
- Declared Holm secondary realigned to log(RV_minus_next+eps) level MSE per frozen design section 3.3.

**audit_pass=true; unresolved_blockers=[].**
