# FCLR-H003 Pre-Registration — Hypothetical Boundary-Breach Forecast

Status: PRE-REGISTERED (scenarios frozen before outcome inspection)
Hypothesis: FCLR-H003
Date: 2026-10-27
Protocol ref: research_state/research_protocol.md v1.0 (FCLR-001) for leakage/embargo rules; this document registers scenarios only.

## Scope and limitations
- Labels are synthetic modeled boundary breaches (scripts/synthetic_boundary_labels.py). They are NOT observed liquidations, account margin, or exchange execution.
- Long and short labels are evaluated separately; never pooled.
- FCLR-001 forecast gate remains NOT MET; this boundary forecast is a separate hypothesis and does not unblock the risk-overlay phase.

## Entry / leverage scenarios (frozen)
Maintenance margin rate = 0.005 for all scenarios (disclosed assumption).
Entry price = mark close at decision time t (no look-ahead).
Horizon = 24 hours (mark closes t+1..t+24).
Leverages (long and short, separate): 3x, 5x, 10x, 20x.
Fee/slippage assumption: none applied to boundary (disclosed: zero-cost boundary).

## Panel
- Use existing frozen FCLR-001 panel (BTCUSDT mark-price, 2024-01-02..2024-03-30) for in-sample construction only.
- Out-of-sample evaluation window: FCLR-001 sealed test block (2024-03-27T02:00:00Z..2024-03-30T23:00:00Z). No re-tuning on test.

## Metrics (to be reported)
Brier score, log-loss (clipped 1e-12..1-1e-12), calibration (reliability bins), precision-recall (AUPRC), base rate per scenario.

## Acceptance
Pre-registered scenarios; metrics reported per leverage/side; long/short kept separate; assumptions disclosed. No claim of observed liquidations.

## Non-goals
No risk-overlay, no trading, no holdout reuse for selection.
