# Track C — Volatility Forecast Extension (heavy-work package)

**Session:** `session_20261118T030427Z`
**Timestamp (UTC):** 2026-11-18T03:04:27Z
**Campaign:** `FCLR-VOL-LIQ-FORECAST-01-20261118T023259Z` (ACTIVE_CAMPAIGN)
**Network:** none. **Parquet engine:** none (not required). **Installs/LFS:** none.

## Objective
Close the two data-sufficiency gaps blocking claim-worthy funding-ablation inference in the RV baseline/ablation line:
- `instruments=4 < 5` (BNBUSDT available on disk but not used in prior ablation)
- `ok_30d_non_overlapping_test_blocks=0 < 3` (prior 3 splits had 14-day tests)

Compare funding+RV feature sets vs RV-only baseline with QLIKE (primary), MAE, RMSE under leakage-resistant chronological splits (purge/embargo >= 7d, train-only normalization, funding last-known at/before hour).

## On-disk evidence (read-only audit)
Source: `research_state/data_cache/*_2024_*` (Binance-style monthly caches; ZIP/CSV/dir). See `data_coverage_audit_20261118T030427Z.json`.

| Instrument | 2024 funded months (funding+mark/klines) | Notes |
|---|---:|---|
| BTCUSDT | 04-12 (9) | 01-03 no funding files |
| ETHUSDT | 04-12 (9) | 01-03 no funding files |
| SOLUSDT | 04-12 (9) | 01-03 no funding files |
| XRPUSDT | 04-12 (9) | 01-03 no funding files |
| BNBUSDT | 04-12 (9) | present on disk; 5th instrument available |

- **Common funded window (all 5):** 2024-04-01..2024-12-31 (contiguous 9 months).
- **Provenanced-confirmatory subset per `run_funding_ablations` constants (FCLR-015):** 2024-04-01..2024-09-30.
- **10-12:** funded on disk but outside `PROVENANCED_CONFIRMATORY_RANGES`; overlaps sealed FCLR-003 test context — exploratory-only with explicit caveat, not confirmatory.

## Proposed executable designs (leakage-aware, not yet run)
Full machine-readable spec: `trackc_extension_design_20261118T030427Z.json`.

### Design A (primary, EXPLORATORY, 5 instruments, provenanced window)
- **Window:** 2024-04-01..2024-09-30 (183 days), 5 instruments.
- **Models:** A_rv_only (HAR direct-variance OLS), B_rv_signed, C_rv_abs, D_rv_signed_abs, E_rv_funding_trails.
- **Metrics:** QLIKE (primary), MAE, RMSE, ΔQLIKE vs A with block-bootstrap CI (resample whole UTC time blocks jointly across instruments).
- **Splits (chronological, 7d purge/embargo, 30d non-overlapping tests):**
  1. train 2024-04-01..05-15 (45d) | embargo 05-16..05-22 | test 05-23..06-21 (30d)
  2. train 2024-04-01..06-21 (82d) | embargo 06-22..06-28 | test 06-29..07-28 (30d)
  3. train 2024-04-01..07-28 (119d) | embargo 07-29..08-04 | test 08-05..09-03 (30d)
- **Gaps addressed:** instruments 4→5, ok_30d blocks 0→3. **Reserve:** 2024-09-04..09-30 unused.
- **Risks:** early train windows short (45d) — pilot quality; per-symbol bar completeness must be verified before run.

### Design B (EXPLORATORY extended 04-12)
- Extends to 2024-12-31 for longer trains but 10-12 carry provenance/sealed-window caveats; confirmatory guard will refuse 10-12. Keep exploratory with explicit non-conflict/leakage audit.

### Design C (RV-only 5-instrument Q1)
- 2024-01-01..2024-03-31, 5 instruments, Persistence vs RV-HAR only (no funding in Q1). Closes RV baseline instrument-count gap; does not close funding-ablation block gap.

## Execution blockers (why estimands not run this session)
- **Environment:** `numpy`, `pandas`, `scipy` absent; `scripts/run_funding_ablations.py`/`forecast_pipeline.py` import at module level. No network installs permitted.
- **Tests:** full discovery baseline is environment-dependent (prior 1126 tests / 62 missing-numpy errors / 9 failures / EXIT 1); cannot be treated as green here.
- **Gates:** `run_funding_ablations.py` confirmatory seam/guard will refuse ranges outside provenanced constants or unprovenanced windows for confirmatory intent — any run must be explicitly exploratory/pilot-labeled with outcome-blind prereg in session dir.

## Recommended next executable step (heavy, mandatory carry-forward)
1. In an environment with numpy/pandas/scipy (no unpinned core deps added; use approved env), freeze an **outcome-blind exploratory prereg** in a new session dir for Design A (instrument list, split calendar, features, horizon, metrics, bootstrap spec, leakage checklist, tested-window conflict check).
2. Run Design A via existing pipeline/scripts adapted only as needed (stdlib-compatible path preferred; do not add `statsmodels`), producing per-split metrics, pooled ΔQLIKE CIs, and an evaluation summary artifact in session dir.
3. Record bar-completeness/leakage audit, gate captures, and targeted tests. Do not promote to confirmatory without §17 conditions and admissible provenance; report honest verdict (likely PILOT/EXPLORATORY given short early trains).

## Status
**HEAVY WORK (planning/design + data audit) COMPLETE; ESTIMAND EXECUTION BLOCKED by missing numpy/pandas/scipy runtime (environmental).** Gaps are demonstrably closeable on cached data per Designs A-C.
