# FCLR-STARTER-001 frozen protocol — RESEARCH_PROMPT.md §14 verbatim

## 14. Mandatory frozen starter protocol: FCLR-001

Before computing any target outcome, create research_state/research_protocol.md and preregister the following starter study. First inspect source availability, but do not inspect outcome summaries or choose cutoffs based on forecast results. Freeze exact timestamp cutoffs and source hashes after a coverage-only audit and before target generation. If a material detail below is infeasible, record the precise reason and register a separate pilot/alternative version before computing its outcomes.

### Unit, timing, and universe

- Unit: one eligible linear perpetual contract × one fully closed UTC hourly timestamp.
- Forecast timestamp t is immediately after all data for the closed hour t are available. Every input must have been available by that instant. Outcomes begin with the next hourly interval; no same-bar or future data may enter a predictor.
- Build the broadest defensible, expanding universe of linear perpetual contracts discoverable automatically from public listing/instrument metadata and historical archives, including delisted contracts where evidence is available. There is no fixed top-N cutoff. Record first verified listing, last verified eligibility, migrations, symbol reuse, contract type, source coverage, and missing periods. Current survivors alone are not a valid historical universe.
- Do not make historical market-cap rankings a hard dependency for this mechanism. If credible free point-in-time ranks exist, maintain a separate descending-cap universe arm; never substitute present-day ranks for historical ranks or merge a restricted arm into the primary venue-native universe without a new protocol version.
- All model comparisons use identical forecast origins and a common eligible sample. Separately report coverage gained or lost by each feature group. Missing features remain missing; do not zero-fill or forward-fill them to make models comparable.

### Primary outcome and forecast target

The single primary outcome is the next-24-hour realized variance of mark-price returns, defined as the sum of squared log returns over the next 24 complete hourly intervals, from t+1 through t+24. Record target units and the exact mark-price field. If trustworthy historic mark-price data cannot support adequate coverage, do not silently substitute last price or index price: register a separate price-source version and label it accordingly.

Secondary target horizons are 6 hours, 72 hours and 168 hours. They are explicitly secondary; include every tested horizon/model/feature comparison in the declared multiplicity family. Do not promote a secondary horizon because it happens to perform better than the primary target.

### Frozen predictor definitions

All features are causal and computed per contract from data ending no later than t:
- RV1h, RV24h and RV168h: trailing realized variances from hourly mark-price log returns.
- Signed funding: the latest funding observation whose availability timestamp is no later than t, retaining sign and its source cadence.
- Funding extremeness: the percentile rank of absolute funding versus that contract's preceding 90 calendar days only. Require at least 30 valid historical funding observations before emitting the percentile; record the actual observation count. Also keep the signed funding value separately.
- Premium feature: mark price divided by index price minus one, only when the two fields have a valid, contemporaneous alignment under a frozen tolerance.
- Smoothing/dislocation feature: mark price divided by a 24-hour exponential moving average minus one, with the EMA computed from prior/current fully closed bars only.
- Do not invent a direct price-delay measurement. Mark/index premium and EMA distance are observable dislocation proxies, not proof that a price was delayed. Any extra predictors require a new registered version or must be declared in the original protocol before any results are inspected.

Feature standardization, scaling, transformations and missing-data eligibility must be fitted or calculated using training information only. Use the same common panel for paired comparisons to prevent coverage differences from masquerading as forecasting skill.

### Frozen baseline and nested model comparisons

Evaluate these fixed model definitions:
- B0, persistence baseline: forecast the next-24-hour realized variance using the preceding RV24h.
- B1, volatility baseline: a fixed-form HAR-style model using log RV1h, log RV24h and log RV168h as predictors of log next-24-hour realized variance.
- C1, funding-augmented model: the same model form and fitting procedure as B1, plus signed funding and the past-only 90-day absolute-funding percentile.
- C2, combined candidate: the same model form and fitting procedure, plus the C1 features and the mark/index premium and mark/EMA24 distance.

Use ordinary least squares (OLS) for the fixed log-linear regression in B1, C1 and C2. Model log(RV + 1e-12), with epsilon fixed in advance in squared-log-return units; standardize predictor columns using training-only means and standard deviations, and specify handling for zero-variance columns before outcomes are inspected. Use a documented training-only smearing correction to transform forecasts back to strictly positive variance. Do not use regularization, model-family searches, or hyperparameter tuning in FCLR-001. Freeze missingness rules and fitting procedures before outcome calculation.

Primary contrast: C2 versus B1 on 24-hour out-of-sample QLIKE. C1 versus B1 and C2 versus C1 are registered secondary contrasts. B0 supplies a simple, interpretable baseline; report all baselines, not only the weakest one. Use paired forecast origins and identical eligible rows across the compared models.

### Splits, embargo, and inference

- Determine date boundaries from data availability alone, store them in the preregistration, and hash/freeze the eligible panel before computing results.
- Use chronological development/training, validation, and final holdout partitions in time order. Use a 60%/20%/20% chronological split as the default when the audited coverage supports it; boundaries are based on unique UTC timestamps, not randomly sampled rows.
- Apply a 7-calendar-day purge/embargo at all split boundaries because the registered secondary horizon extends to 168 hours. No target interval can overlap training, validation and test folds.
- Any feature selection or model correction is done on development/validation data. The final holdout is opened once for the frozen protocol and then permanently marked as inspected/development evidence for subsequent research.
- The minimum claim-worthy test requires at least five instruments represented in the paired out-of-sample panel, at least three non-overlapping 30-day evaluation blocks, and valid uncertainty estimation. If these are not met, report PILOT/INCONCLUSIVE and state the exact data shortfall; do not relax thresholds after seeing outcomes.
- Primary metric: paired out-of-sample QLIKE difference, defined consistently and reported as both absolute difference and relative reduction. Secondary metrics: MAE/RMSE on the stated target and rank/error diagnostics where appropriate. Event predictions additionally require Brier score, log loss, calibration, and precision-recall analysis.
- Estimate uncertainty with a reproducible block bootstrap that resamples complete UTC time blocks jointly across instruments (preserving common market shocks and serial dependence), with at least 2,000 deterministic-seed replicates if sample size permits. Report sensitivity to instrument concentration, leave-one-instrument-out results, and regime/time-block stability. If the method is infeasible, disclose why and use a pre-registered dependence-aware alternative; never replace invalid inference with an ordinary IID standard error without qualification.
- Pre-register a minimum practically meaningful improvement—default at least 2% relative reduction in primary QLIKE—before the holdout is opened. A smaller apparent gain does not pass the forecast gate unless a different justified materiality threshold was frozen in advance.
- Use a two-sided uncertainty interval for the paired loss difference and require the interval to support improvement, the practical threshold to be met, and the predeclared multiplicity rule to pass. No significance claim based on an in-sample coefficient alone.

The exact timestamp boundaries, cutoff, eligible sample definition, regression/back-transformation details, bootstrap configuration, and source hashes must be recorded in research_state/research_protocol.md before computing holdout outcomes. Changes thereafter require a new protocol/experiment ID.
