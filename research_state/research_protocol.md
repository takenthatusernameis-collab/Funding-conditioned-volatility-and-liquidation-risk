# FCLR-001 Research Protocol — Funding-Conditioned Volatility Forecast

Protocol version: FCLR-001 v1.0
Status: PROTOCOL_FROZEN (methodology frozen; exact split timestamps pending coverage audit, no outcomes computed)
Date frozen: 2026-10-25
Experiment ID: FCLR-001
Primary hypothesis: FCLR-H001 (incremental 24-hour volatility forecasting)
Repository: https://github.com/takenthatusernameis-collab/Funding-conditioned-volatility-and-liquidation-risk

## 1. Unit, timing, and universe

- Unit: one eligible linear perpetual contract × one fully closed UTC hourly timestamp.
- Forecast timestamp t is immediately after all data for the closed hour t are available. Every input must have been available by that instant. Outcomes begin with the next hourly interval; no same-bar or future data may enter a predictor.
- Universe: broadest defensible expanding universe of linear perpetual contracts discoverable automatically from public listing/instrument metadata and historical archives, including delisted contracts where evidence exists. No fixed top-N cutoff. Record first verified listing, last verified eligibility, migrations, symbol reuse, contract type, source coverage, missing periods. Current survivors alone are not a valid historical universe.
- Historical market-cap rankings are NOT a hard dependency. If credible free point-in-time ranks exist, maintain a separate descending-cap universe arm; never substitute present-day ranks or merge a restricted arm into the primary venue-native universe without a new protocol version.
- All model comparisons use identical forecast origins and a common eligible sample. Report coverage gained/lost by feature group. Missing features remain missing; do not zero-fill or forward-fill.

## 2. Primary outcome and forecast target

- Primary outcome: next-24-hour realized variance of mark-price returns = sum of squared log returns over the next 24 complete hourly intervals (t+1 through t+24). Units: squared log returns per 24h. Mark-price field: markPriceKlines close (1h).
- Secondary target horizons: 6h, 72h, 168h. Explicitly secondary; every tested horizon/model/feature comparison is in the declared multiplicity family. Do not promote a secondary horizon because it performs better.
- If trustworthy historic mark-price data cannot support adequate coverage, do not silently substitute last/index price: register a separate price-source version.

## 3. Frozen predictor definitions (causal, per contract, data ending no later than t)

- RV1h, RV24h, RV168h: trailing realized variances from hourly mark-price log returns.
- Signed funding: latest funding observation whose availability timestamp <= t, retaining sign and source cadence.
- Funding extremeness: percentile rank of absolute funding versus that contract's preceding 90 calendar days only. Require >= 30 valid historical funding observations before emitting percentile; record actual observation count. Keep signed funding separately.
- Premium: mark price / index price - 1, only when valid contemporaneous alignment under frozen tolerance.
- Smoothing/dislocation: mark price / 24h EMA - 1, EMA from prior/current fully closed bars only.
- No direct price-delay measurement. Mark/index premium and EMA distance are observable proxies only.
- Feature standardization, scaling, transformations, missing-data eligibility fitted/calculated using training information only. Common panel for paired comparisons.

## 4. Frozen baseline and nested model comparisons

- B0 (persistence): forecast next-24h realized variance using preceding RV24h.
- B1 (volatility): fixed-form HAR-style model using log RV1h, log RV24h, log RV168h as predictors of log next-24h realized variance.
- C1 (funding-augmented): same form as B1 plus signed funding and past-only 90-day absolute-funding percentile.
- C2 (combined): same form plus C1 features and mark/index premium and mark/EMA24 distance.
- OLS for fixed log-linear regression in B1, C1, C2. Model log(RV + 1e-12), epsilon fixed in advance in squared-log-return units. Standardize predictor columns using training-only means/SDs; specify handling for zero-variance columns before outcomes inspected. Documented training-only smearing correction to transform forecasts back to strictly positive variance. No regularization, model-family search, or hyperparameter tuning.
- Primary contrast: C2 vs B1 on 24h out-of-sample QLIKE. C1 vs B1 and C2 vs C1 are registered secondary contrasts. B0 reported as interpretable baseline. Paired forecast origins and identical eligible rows across compared models.

## 5. Splits, embargo, and inference

- Date boundaries determined from data availability alone; stored in preregistration; eligible panel hashed/frozen before computing results.
- Chronological development/training, validation, final holdout in time order. Default 60%/20%/20% chronological split when audited coverage supports it; boundaries based on unique UTC timestamps, not randomly sampled rows.
- 7-calendar-day purge/embargo at all split boundaries (secondary horizon extends to 168h). No target interval may overlap training/validation/test folds.
- Feature selection/model correction on development/validation data only. Final holdout opened once for frozen protocol then permanently marked inspected.
- Minimum claim-worthy test: >=5 instruments in paired out-of-sample panel, >=3 non-overlapping 30-day evaluation blocks, valid uncertainty estimation. Otherwise report PILOT/INCONCLUSIVE with exact shortfall; do not relax thresholds after seeing outcomes.
- Primary metric: paired out-of-sample QLIKE difference, absolute and relative reduction. Secondary: MAE/RMSE on stated target and rank/error diagnostics. Event predictions additionally Brier, log loss, calibration, precision-recall.
- Uncertainty: reproducible block bootstrap resampling complete UTC time blocks jointly across instruments, >=2000 deterministic-seed replicates if sample size permits. Report sensitivity to instrument concentration, leave-one-instrument-out, regime/time-block stability. If infeasible, disclose and use pre-registered dependence-aware alternative; never replace invalid inference with ordinary IID SE without qualification.
- Minimum practically meaningful improvement: default >=2% relative reduction in primary QLIKE, frozen before holdout opened.
- Two-sided uncertainty interval for paired loss difference; require interval to support improvement, practical threshold met, predeclared multiplicity rule passes. No significance claim from in-sample coefficient alone.

## 6. Split boundaries (frozen)

Exact UTC split timestamps are frozen (coverage-only audit). No outcomes have been computed.

- Provisional earliest data: 2024-01-01 (from binance_source_probe.md; funding monthly archive 2024-01; klines daily 2024-01-01). Coverage extended to >=5 instruments (BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT) across 2024-01-01..2024-03-31 with paired OOS panel.
- Rule: boundaries on unique UTC timestamps; 60% train / 20% validation / 20% holdout by timestamp count; 7-calendar-day embargo between each partition.
- Common paired panel timestamps: 0 across the declared 5-symbol universe (BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT) in 2024-01-01..2024-03-31. Per research_state/coverage_audit_recheck.md the true 5-symbol mark-price intersection is 0 timestamps; only BTCUSDT has mark-price rows in this window (2160). The previously recorded 2136 figure is not reproducible from the working tree. The frozen split boundaries below are BTCUSDT-anchored and remain valid; the >=5-instruments gate in §5 was never met.
- Train: 2024-01-02T00:00:00Z to 2024-02-24T08:00:00Z (count=1281)
- Validation: 2024-03-02T08:00:00Z to 2024-03-20T02:00:00Z (count=427) [7d embargo after train]
- Test/Holdout: 2024-03-27T02:00:00Z to 2024-03-30T23:00:00Z (count=94) [7d embargo after validation]
- Status: FROZEN. No outcomes computed.


## 7. Multiplicity and promotion

- Whole declared family includes all tried primary/secondary targets, feature ablations, thresholds, model versions, price-source arms, universe arms. Holm correction (or explicitly justified method) on whole relevant family. Report unadjusted and adjusted results and every failed/not-run cell with reasons.
- Promotion requires: data/label gates pass; frozen OOS comparison beats declared volatility baseline on primary target; practical materiality floor and multiplicity/uncertainty conditions pass; skill not dominated by one coin/venue/crisis/time block; calibration/subgroup diagnostics acceptable for probability forecast; independent recomputation reproduces headline within declared tolerance; red-team and leakage audits show no unresolved issue capable of reversing conclusion.

## 8. Acceptance / verification

- test -s research_state/research_protocol.md
- File contains frozen split rule, target definition, baselines, and primary contrast.
- Research gates: Direct liquidation labels NOT VERIFIED; synthetic boundary labels NOT IMPLEMENTED; future realized-volatility target NOT IMPLEMENTED; funding-correction replication NOT IMPLEMENTED; out-of-sample result NOT RUN; risk-overlay phase INELIGIBLE.
