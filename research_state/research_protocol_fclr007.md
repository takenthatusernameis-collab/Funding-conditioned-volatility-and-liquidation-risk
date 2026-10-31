# FCLR-007 Research Protocol — Confirmatory Volatility Forecast on Unsealed 2026 Apr-Jul Data

Protocol version: FCLR-007 v1.0
Status: PROTOCOL_FROZEN (pre-registered BEFORE any outcome inspection; splits frozen before outcomes)
Date frozen: 2026-10-30T23:59:00Z
Experiment ID: FCLR-007
Primary hypothesis: FCLR-H001 (incremental 24-hour volatility forecasting)
Repository: https://github.com/takenthatusernameis-collab/Funding-conditioned-volatility-and-liquidation-risk
Campaign: AGENT_HANDOFF.md CAMPAIGN FCLR-007 (Steps 1-4); SESSION_GOAL: CAMPAIGN_REOPEN — FCLR-007 CONFIRMATORY ON UNSEALED 2026 APR-JUL PANEL

## Rationale (evidence-based, RESEARCH_PROMPT §16)

FCLR-003 (2024-10-02..2024-12-31) is the only adequately-powered confirmatory window to date and it is SEALED NEGATIVE: C2 vs B1 = +0.015205 QLIKE, 95% CI [-0.020240, 0.056734] crosses zero, relative -3.78% (worse), FCLR-H001 NOT_SUPPORTED, risk-overlay INELIGIBLE. FCLR-006 sealed COMPLETE_NEGATIVE on unsealed 2026-05-23..2026-08-06 (76 days = 2 blocks): C2 vs B1 significantly WORSE (+0.3686 QLIKE, CI entirely positive), gate NOT_MET (underpowered block count; worse-side result). DATA-EXHAUSTION CLAIM RETRACTED 2026-10-30T12:34:23Z: research_state/data_cache/ verified to hold unsealed 2026 Apr-Jul markPriceKlines/indexPriceKlines/fundingRate for all 5 symbols — coverage-only audit research_state/fclr007_coverage_audit.md (2026-10-30T23:59:19Z): 2928 common hourly timestamps (122 days, 0 gaps), 5 symbols, funding complete. The only unblocked confirmatory path is CAMPAIGN FCLR-007 on unsealed 2026 Apr-Jul data.

This experiment is CONFIRMATORY on unsealed 2026 data. It does NOT reuse any sealed FCLR-001/002/003/004/005/006 holdout for selection, tuning, or re-evaluation. No seal violations. Heavy execution authorized per AGENT_HANDOFF.md SESSION_GOAL.

## 1. Unit, timing, and universe

- Unit: one eligible linear perpetual contract × one fully closed UTC hourly timestamp.
- Forecast timestamp t is immediately after all data for closed hour t available. Every input available by that instant. Outcomes begin with the next hourly interval; no same-bar or future leakage into predictors.
- Universe (frozen): 5-symbol panel BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT on Binance USDⓈ-M perpetuals. Common paired panel determined by mark-price intersection over the audited window.
- Data window (coverage-only, research_state/fclr007_coverage_audit.md): 2026-04-01T00:00:00Z .. 2026-07-31T23:00:00Z; 2928 common hourly timestamps across all 5 symbols; >=5 instruments CONFIRMED; >=90 common days CONFIRMED (122-day window).
- Source side: research_state/data_cache/{SYM}_2026_*/ (markPriceKlines, indexPriceKlines, premiumIndexKlines, fundingRate). No downloads required; all inputs already cached and hashed in the coverage audit.

## 2. Primary outcome and forecast target

- Primary outcome: next-24-hour realized variance of mark-price returns = sum of squared log returns over the next 24 complete hourly intervals (t+1 through t+24). Units: squared log returns per 24h. Mark-price field: markPriceKlines close (1h).
- Secondary target horizons: 6h, 72h, 168h. Explicitly secondary; every tested horizon/model/feature comparison is in the declared multiplicity family. Do not promote a secondary horizon because it performs better.
- Do not substitute last/index price if mark-price coverage missing.

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
- OLS for fixed log-linear regression in B1, C1, C2. Model log(RV + 1e-12), epsilon fixed in advance in squared-log-return units. Standardize predictor columns using training-only means/SDs; zero-variance columns handled before outcomes inspected. Documented training-only smearing correction to transform forecasts back to strictly positive variance. No regularization, model-family search, or hyperparameter tuning.
- Primary contrast: C2 vs B1 on 24h out-of-sample QLIKE. C1 vs B1 and C2 vs C1 are registered secondary contrasts. B0 reported as interpretable baseline. Paired forecast origins and identical eligible rows across compared models.

## 5. Splits, embargo, and inference

- Date boundaries determined from data availability alone (coverage-only audit); stored in this preregistration and in research_state/run_manifest.json split_boundaries_fclr007; eligible panel hashed/frozen before computing results. FROZEN before any outcomes computed.
- Chronological development/training, validation, final holdout in time order. Boundaries based on unique UTC timestamps, not randomly sampled rows.
- 7-calendar-day purge/embargo at all split boundaries (secondary horizon extends to 168h). No target interval may overlap training/validation/test folds.
- Feature selection/model correction on development/validation data only. Final holdout opened once for the frozen protocol then permanently marked inspected.
- Minimum claim-worthy test: >=5 instruments in paired out-of-sample panel, >=3 non-overlapping 30-day evaluation blocks, valid uncertainty estimation. NOTE: the 122-day panel under 60/20/20 leaves a small test suffix (see split table); block criterion expected NOT_MET. Report exact shortfall; do NOT relax thresholds after seeing outcomes.
- Primary metric: paired out-of-sample QLIKE difference, absolute and relative reduction. Secondary: MAE/RMSE on stated target and rank/error diagnostics.
- Uncertainty: reproducible block bootstrap resampling complete UTC time blocks jointly across instruments, >=2000 deterministic-seed replicates (block_hours ~24h). Report sensitivity to instrument concentration, leave-one-instrument-out, regime/time-block stability.
- Minimum practically meaningful improvement: default >=2% relative reduction in primary QLIKE, frozen before holdout opened.
- Two-sided uncertainty interval for paired loss difference; require interval to support improvement, practical threshold met, predeclared multiplicity rule (Holm) passes. No significance claim from in-sample coefficient alone.

## 6. Frozen split boundaries (FCLR-007) — pre-registered, frozen before outcomes

- Rule: chronological splits by unique UTC timestamps across the common 5-symbol panel; 7-day embargo between partitions. 60/20/20 chronological split; holdout = test window opened once.
- Train: 2026-04-01T00:00:00Z to 2026-06-12T23:00:00Z (73 days)
- Embargo: 2026-06-13T00:00:00Z to 2026-06-19T23:00:00Z (7 days)
- Validation: 2026-06-20T00:00:00Z to 2026-07-13T23:00:00Z (24 days)
- Embargo: 2026-07-14T00:00:00Z to 2026-07-20T23:00:00Z (7 days)
- Test/Holdout: 2026-07-21T00:00:00Z to 2026-07-31T23:00:00Z (11 days = 0 non-overlapping 30-day blocks; block criterion NOT_MET — documented shortfall, do not relax)
- Status: FROZEN (pre-registered). Holdout NOT opened; no outcomes computed as part of this protocol registration.

## 7. Multiplicity and promotion

- Whole declared family includes all tried primary/secondary targets, feature ablations, thresholds, model versions, price-source arms, universe arms. Holm correction on whole relevant family. Report unadjusted and adjusted results and every failed/not-run cell with reasons.
- Promotion requires: data/label gates pass; frozen OOS comparison beats declared volatility baseline on primary target; practical materiality floor and multiplicity/uncertainty conditions pass; skill not dominated by one coin/venue/crisis/time block; calibration/subgroup diagnostics acceptable; independent recomputation reproduces headline within declared tolerance; red-team and leakage audits clean.

## 8. Acceptance / verification

- research_state/research_protocol_fclr007.md contains frozen FCLR-007 v1.0 with splits, targets, baselines/contrasts, materiality floor (>=2%), multiplicity rule, block-bootstrap config.
- Coverage audit (research_state/fclr007_coverage_audit.md) shows >=5 instruments and >=90 common-day window.
- No reuse of sealed FCLR-001/002/003/004/005/006 holdouts.
- `python -m unittest discover -s tests -v` passes; byte-identical reproducibility re-run of FCLR_EXPERIMENT=FCLR-007 verified; results recorded in research_state/evaluation_summary_FCLR007.md + gate assessment + run_manifest.json (split_boundaries_fclr007.frozen_before_outcomes: true); hypothesis_registry.json and experiment_frontier.json updated.

## Links

- research_state/fclr007_coverage_audit.md
- research_state/run_manifest.json (split_boundaries_fclr007)
- research_state/hypothesis_registry.json
- research_state/experiment_frontier.json
- scripts/run_evaluation.py
- research_protocol.md (FCLR-001/FCLR-002 template)
- RESEARCH_PROMPT.md
