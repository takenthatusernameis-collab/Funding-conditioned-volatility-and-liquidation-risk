# FCLR-014 Research Protocol — Track C / H001 Confirmatory (frozen BEFORE outcomes)

**Experiment ID:** FCLR-014
**Protocol version:** v2.0
**Frozen at:** 2026-11-10T10:26:25Z
**Status:** FROZEN_BEFORE_OUTCOMES
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk` — Track C / H001 priority (funding-conditioned volatility forecast vs RV-only baseline)

---

## 1. Mission

Reproduce an honest out-of-sample forecast test of whether funding extremes + realized volatility + pre-specified price-dislocation/smoothing features improve next-24h realized-variance forecasting over an RV-only HAR baseline, on a provenance-verified local panel with >=3 non-overlapping 30-day test blocks and >=5 instruments, with a frozen preregistration registered before outcomes. Preserve the null if the gate fails; do not promote.

---

## 2. Constraints (NON-NEGOTIABLE)

- No network/paid/manual/credentialed data; no fabricated provenance/outcomes; no threshold shopping; no sealed-holdout reuse; no Track A/B/C conflation; no risk overlay until forecast gate passes.
- Preregister before outcomes — never inspect outcomes for this window before freezing this protocol/splits.
- Do not relax block count, materiality floor, or multiplicity after seeing outcomes.
- Do not reuse the FCLR-009 test window (2025-06-08..2025-12-31); this window (2025-01-01..2025-06-07) is untested as an out-of-sample confirmatory panel.
- Track C results are volatility/stress only, NEVER observed-liquidation validation.

---

## 3. Unit, timing, and universe

- **Unit:** one eligible linear perpetual contract × one fully closed UTC hourly timestamp.
- **Forecast timestamp t:** immediately after all data for closed hour t are available; every input available by that instant. Outcomes begin with the next hourly interval; no same-bar or future data in predictors.
- **Universe:** 5 symbols (BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT), venue-native archival coverage from public local archives; current survivors alone are not a valid historical universe; no market-cap ranking dependency.
- **Venue:** binance_um_perp; unauthenticated Binance public archive (data.binance.vision / binance-public-data); klines 1h, fundingRate, indexPriceKlines, markPriceKlines, premiumIndexKlines.

---

## 4. Data window and admissibility

- **Data window:** 2025-01-01T00:00:00Z .. 2025-06-07T23:00:00Z (158 days).
- **Admissibility (pre-computed, machine-verified):**
  - Provenance: `provenance_verified=true`, `unmapped_count=0`, 36001 manifest records indexed, adjacent `.sha256` sidecars on all funding CSVs (`research_state/trackc_deep_audit_2025_h1_check.json`).
  - Funding schema: 5 symbols × 6 months, `all_ok=true`, `missing=0`, `schema_bad=0` (`research_state/funding_schema_audit_2025_h1.json`).
  - Panel: 5 symbols, 181 days per symbol (range 2025-01-01..2025-06-30 per deep audit cache), `required_series_complete=true`, `panel_non_overlapping_30d_blocks_estimate=6` (>=3 required).
  - No outcomes have been inspected for this window.

---

## 5. Frozen splits (60/20/20 chronological, 7-day purge/embargo)

Boundaries determined from data coverage only, frozen before outcomes. No random splits; unique UTC timestamps.

| Partition | Start | End | Days |
|---|---|---|---|
| Train | 2025-01-01T00:00:00Z | 2025-04-05T23:00:00Z | ~95 |
| Embargo | 2025-04-06T00:00:00Z | 2025-04-12T23:00:00Z | 7 |
| Validation | 2025-04-13T00:00:00Z | 2025-05-14T23:00:00Z | ~32 |
| Embargo | 2025-05-15T00:00:00Z | 2025-05-21T23:00:00Z | 7 |
| Test | 2025-05-22T00:00:00Z | 2025-06-07T23:00:00Z | ~17 |

- **Embargo rationale:** 7-calendar-day purge/embargo at all split boundaries because the registered secondary horizon extends to 168 hours. No target interval overlaps train/validation/test folds.
- **Block requirement:** >=3 non-overlapping 30-day out-of-sample evaluation blocks in the test window across >=5 instruments. (Panel-wide estimate: 6 non-overlapping 30-day blocks across 2025-01-01..2025-06-30 per `trackc_deep_audit_2025_h1_check.json`; test-window block count computed by `scripts/run_evaluation.py` at M3.)
- **frozen_before_outcomes:** true
- **frozen_at:** 2026-11-10T10:26:25Z

---

## 6. Primary outcome and forecast target

- **Primary outcome:** next-24-hour realized variance of mark-price returns: sum of squared log returns over the next 24 complete hourly intervals, from t+1 through t+24.
- **Target units:** squared log-return units (mark-price close field).
- **Secondary horizons:** 6h, 72h, 168h (explicitly secondary; every tested horizon/model/feature comparison included in the declared multiplicity family; no promotion of a secondary horizon because it performs better).

---

## 7. Frozen predictor definitions (causal, computed per contract from data ending no later than t)

- **RV1h, RV24h, RV168h:** trailing realized variances from hourly mark-price log returns.
- **Signed funding:** latest funding observation whose availability timestamp is no later than t, retaining sign.
- **Absolute funding rate |funding|:** distinct feature, not a replacement for signed values.
- **Trailing absolute-funding percentile:** percentile rank vs preceding 90 calendar days only; require >=30 valid historical funding observations before emitting; record actual count; signed funding kept separately.
- **Premium feature:** mark price / index price − 1, only when valid contemporaneous alignment under frozen tolerance.
- **Smoothing/dislocation feature:** mark price / 24-hour EMA − 1, EMA computed from prior/current fully closed bars only.
- **No invented delay:** mark/index premium and EMA distance are observable dislocation proxies only.
- **Missing features remain missing:** no zero-fill/forward-fill to make models comparable.

---

## 8. Frozen baseline and nested model comparisons

- **B0 (persistence):** forecast next-24h realized variance using preceding RV24h.
- **B1 (RV-only baseline):** fixed-form HAR-style OLS on log RV1h, log RV24h, log RV168h predicting log next-24h realized variance.
- **C1 (funding-augmented):** B1 form + signed funding + past-only 90-day absolute-funding percentile.
- **C2 (combined candidate):** B1 form + C1 features + mark/index premium + mark/EMA24 distance.

**Fitting:** OLS fixed-form log-linear regression; model log(RV + 1e-12) with epsilon fixed in advance; standardize predictor columns using training-only mean/std; zero-variance column handling frozen before outcomes; documented training-only smearing correction for back-transformation; no regularization, no model-family search, no hyperparameter tuning.

**Primary contrast:** C2 versus B1 on paired out-of-sample test QLIKE (absolute difference and relative reduction).
**Secondary contrasts:** C1 versus B1; C2 versus C1.

---

## 9. Inference and uncertainty

- **Method:** block bootstrap resampling complete UTC time blocks jointly across instruments (preserves common market shocks and serial dependence).
- **Replicates:** 2000, deterministic seed frozen before outcomes.
- **Diagnostics:** instrument concentration sensitivity, leave-one-instrument-out, regime/time-block stability.

---

## 10. Multiplicity

- **Method:** Holm familywise-error correction across the whole declared family (all primary/secondary targets, feature ablations, thresholds, model versions, price-source arms, universe arms).
- **Reporting:** raw and adjusted results; every failed/not-run cell with reasons.

---

## 11. Decision gates (forecast gate)

All conditions must pass for FORECAST_GATE_PASSED:

1. **Data gate:** >=5 instruments in paired out-of-sample panel; >=3 non-overlapping 30-day OOS blocks; valid uncertainty estimation.
2. **Practical materiality:** at least 2% relative reduction in primary QLIKE vs B1, pre-registered; smaller apparent gain does not pass unless a different justified threshold was frozen in advance.
3. **Uncertainty condition:** two-sided uncertainty interval for paired loss difference supports improvement.
4. **Multiplicity condition:** predeclared Holm correction passes.
5. **Concentration condition:** skill not dominated by one coin, one venue, one brief crisis, or one time block.
6. **Leakage condition:** no unresolved leakage, source, label, or timestamp defect.

**Forecast gate:** all conditions required before any risk-overlay phase; otherwise retain NOT_SUPPORTED / INCONCLUSIVE / EXPLORATORY_ONLY. Overlay eligibility: NOT ELIGIBLE unless gate passes.

---

## 12. Outcome accounting

- `outcome_values_inspected`: false (no outcomes inspected for this window before this freeze).
- `holdout_status`: sealed final holdout not opened; cannot be treated as untouched evidence once inspected.
- Do not inspect zero outcome values before this freeze is recorded.
- Do not promote exploratory results (FCLR-002 C2-vs-B1 +4.588% rel QLIKE, 2 blocks; FCLR-009 -0.43% rel QLIKE, CI crosses zero; FCLR-013 -1.32% rel QLIKE) to confirmatory.
- Do not relax the >=3-block rule after seeing outcomes.
- Do not threshold-shop or reuse sealed holdouts.
- Do not conflate Track C volatility outcomes with observed liquidations (Track A) or modeled boundary breaches (Track B).

---

## 13. Next action (M3)

- Execute `FCLR_EXPERIMENT=FCLR-014 python scripts/run_evaluation.py` on the frozen panel.
- Write `research_state/evaluation_summary_FCLR-014.md` with full metrics and uncertainty.
- Update `research_state/hypothesis_registry.json` H1_primary status.
- Record gate verdict and overlay eligibility.

---

**END OF PROTOCOL. This document is frozen before outcomes. Any change to question, feature, outcome, universe, split, data source, model family, or parameter after outcome inspection requires a new protocol/experiment ID.**
