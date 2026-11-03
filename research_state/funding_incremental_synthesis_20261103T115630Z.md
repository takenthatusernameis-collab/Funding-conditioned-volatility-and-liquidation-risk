# Funding-Conditioned Volatility Incremental Synthesis — FCLR-011

Generated: 2026-11-03T11:56:30Z
Repo: Funding-conditioned-volatility-and-liquidation-risk
Experiment: FCLR-011
Hypothesis: FCLR-H001 (primary contrast C2 vs B1)
Status: FORECAST_GATE_PASSED
Panel: 2026 panel, BNBUSDT/BTCUSDT/ETHUSDT/SOLUSDT/XRPUSDT

## 1) Question
Do funding extremes plus price-dislocation/smoothing features improve out-of-sample forecasts of forward realized volatility over a realized-volatility-only baseline? The incremental value of funding + price features over RV-only is the claim; standalone association is not sufficient.

## 2) Data (Binance UM perpetual, 2026 panel)
- Instruments: BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT (5 instruments)
- Range: 2026-01-01 .. 2026-08-06 (218 days, 7 non-overlapping 30-day blocks)
- Sources: klines, markPriceKlines, indexPriceKlines, premiumIndexKlines, fundingRate (free unauthenticated Binance public archive)
- Mark/price alignment on UTC hourly timestamps; missing treated as missing (no zero-fill of core RV features).

## 3) Splits (frozen before outcomes)
- Protocol: research_state/pre_registration_fclr011_20261103T111501Z.md v1.0
- Train: 2026-01-01T00:00:00Z .. 2026-03-17T23:00:00Z
- Validation: 2026-03-25T00:00:00Z .. 2026-04-30T23:00:00Z
- Test: 2026-05-08T00:00:00Z .. 2026-08-06T23:00:00Z (91 days = 3 non-overlapping 30-day blocks)
- 7-day purge/embargo at all boundaries; frozen_before_outcomes=true, frozen_at 2026-11-03T11:15:01Z.

## 4) Features (causal, available by forecast timestamp t)
- RV1h, RV24h, RV168h: trailing realized variances of hourly mark-price log returns.
- Signed funding: latest funding observation available no later than t (sign retained).
- Absolute funding percentile: trailing-only 90-calendar-day percentile of |funding|, requires >=30 prior valid funding obs.
- Premium: mark/index - 1 under frozen alignment tolerance.
- EMA24 distance: mark / 24h EMA - 1, EMA from fully closed prior bars.
- No direct price-delay variable invented.

## 5) Models (fixed OLS log-linear, no regularization/tuning)
- B0: persistence (preceding RV24h).
- B1: RV-only HAR-style (log RV1h, log RV24h, log RV168h) -> log(next-24h RV).
- C1: B1 + signed funding + abs funding percentile.
- C2: C1 + mark/index premium + mark/EMA24 distance.
- log(RV + 1e-12), training-only standardization, training-only smearing correction back to positive variance.

## 6) Test-set QLIKE (lower is better), n=10785 paired (C1/C2), n=10800 (B0)
- B0: 0.330127
- B1: 0.333314
- C1: 0.328788
- C2: 0.316855

## 7) Paired comparisons (block bootstrap, ~24h blocks, 2000 reps)
- C2 vs B1: mean diff -0.016458, 95% CI [-0.032546, -0.001418] (excludes 0), rel reduction -4.94% -> PASS (>=2% floor, CI supports improvement)
- C1 vs B1: rel -1.36%, CI [-0.008260, -0.001111]
- C2 vs C1: rel -3.63%, CI [-0.027256, 0.001778]

## 8) Gate assessment
- Primary contrast C2 vs B1 >=2% rel QLIKE reduction: PASS (4.94%)
- CI excludes zero: PASS
- >=5 instruments: PASS (5)
- >=3 non-overlapping 30-day blocks: PASS (3)
- Forecast gate: PASSED (all criteria)

## 9) Reproducibility
- Canonical artifact: research_state/evaluation_summary_FCLR-011_20261103T111743Z.md
- Run manifest: research_state/run_manifest.json (run_id FCLR-011-20261103T111738Z, git_sha f79c9767..., status COMPLETE, gate FORECAST_GATE_PASSED, split_boundaries_fclr011 frozen)
- Preregistration: research_state/pre_registration_fclr011_20261103T111501Z.md
- All results from frozen splits only; no tuning on holdout.

## 10) Caveats
- Mark/index premium not fully integrated where source missing; EMA distance computed from mark prices.
- Features with missing values filled with 0.0 where protocol allows or rows dropped if core RV features missing.
- Incremental skill confirmed on this panel; separate forward test required before any overlay claim (no overlay changes in FCLR-012).
