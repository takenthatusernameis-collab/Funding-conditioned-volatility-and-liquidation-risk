# FCLR-H003 Pre-Registration — Boundary-Breach Forecast on FCLR-002 Panel

Status: PRE-REGISTERED (scenarios frozen before outcome inspection)
Hypothesis: FCLR-H003
Experiment: FCLR-002-H003
Date: 2026-10-28
Protocol ref: research_state/research_protocol.md v1.0 (FCLR-002) for splits/embargo/leakage rules; research_state/fclr_h003_pre_registration.md for scenario definitions.

## Why this registration exists

The original FCLR-H003 evaluation (research_state/evaluation_summary_h003.md, 2026-10-27) ran on the FCLR-001 sealed test block only: 2024-03-27T02:00:00Z..2024-03-30T23:00:00Z, n=70 per scenario, BTCUSDT-only. Across all 8 leverage/side scenarios the observed base rate was 0.0000 (zero breach events in that calm 4-day window), so Brier/log-loss/AUPRC were degenerate and no inferential statement was possible. That run was correctly recorded as inconclusive-by-construction, not as evidence of predictability.

This pre-registration opens the same frozen scenario set on the FCLR-002 panel, which spans 5 symbols over 2024-04-01..2024-09-30 and contains real volatility episodes. This is a materially different sample, not a re-run of the same test.

## Scope and limitations (unchanged from FCLR-H003)

- Labels are synthetic modeled boundary breaches (scripts/synthetic_boundary_labels.py). They are NOT observed liquidations, account margin, or exchange execution.
- Long and short labels are evaluated separately; never pooled.
- FCLR-001 and FCLR-002 forecast gates remain NOT MET; this boundary forecast is a separate hypothesis and does NOT unblock the risk-overlay phase.
- No risk-overlay, no trading, no holdout reuse for selection.

## Entry / leverage scenarios (frozen, identical to FCLR-H003)

Maintenance margin rate = 0.005 for all scenarios (disclosed assumption).
Entry price = mark close at decision time t (no look-ahead).
Horizon = 24 hours (mark closes t+1..t+24).
Leverages (long and short, separate): 3x, 5x, 10x, 20x.
Fee/slippage assumption: none applied to boundary (disclosed: zero-cost boundary).

## Panel and splits (frozen, from FCLR-002 v1.0)

- Universe: BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT (Binance USD⌋-M perpetuals).
- Common paired panel: 4392 hourly timestamps 2024-04-01T00:00:00Z..2024-09-30T23:00:00Z (research_state/fclr002_coverage_audit.json).
- Splits (frozen, 7-day embargo): train 2024-04-01T00:00:00Z..2024-06-08T23:00:00Z; val 2024-06-16T00:00:00Z..2024-07-15T23:00:00Z; test 2024-07-23T00:00:00Z..2024-09-30T23:00:00Z.
- Model fitting (logistic, fixed lr/iter, zero init) on train only. Labels computed from mark closes t+1..t+24 only. No threshold selection on test: alert budget / decision thresholds are pre-specified at 0.00..1.00 grid with best-F1 reported as a descriptive diagnostic only, never used for a gate decision.

## Metrics (to be reported, per leverage/side/model)

Brier score, log-loss (clipped 1e-12..1-1e-12), calibration (reliability bins), precision-recall (AUPRC), base rate per scenario, and sample sizes. Long and short reported separately.

## Models

- B0: persistence/log-volatility baseline features only.
- C2: same features plus signed funding, past-only 90-day absolute-funding percentile, mark/index premium (0.0 where unavailable), mark/EMA24 distance.

## Acceptance

Pre-registered scenarios; metrics reported per leverage/side; long/short kept separate; assumptions disclosed; no claim of observed liquidations. If base rates are again ~0 across scenarios, report as inconclusive-by-construction and do not claim predictive value.

## Non-goals

No risk-overlay, no trading, no reuse of any sealed holdout for selection or tuning. Does not alter FCLR-001 or FCLR-002 frozen artifacts, splits, or evaluations.