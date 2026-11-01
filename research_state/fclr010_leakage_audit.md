# FCLR-010 leakage / label-history audit

TIMESTAMP (UTC): 2026-11-01T14:24:32Z
Experiment: FCLR-010 (Track A, ironflow Hyperliquid)
Status: AUDITED

## Audit scope
- All predictors used in B0/B1/C1/C2
- Label history access (for any features derived from observed liquidations)
- Split boundaries and embargoes
- Cross-track firewall

## Findings
- Label source restricted to ironflow_hyperliquid_liquidation_events (Hyperliquid native perps). No Binance data merged.
- Features: protocol-specified causal/decision-time features. Any use of label history only up to decision time t (lagged aggregates) documented; no peeking into test labels.
- Splits frozen before outcomes: run_manifest.json#split_boundaries_fclr010 frozen_at 2026-11-01T05:39:07Z, frozen_before_outcomes=true. 7-day embargo at boundaries.
- Block-bootstrap inference by UTC time blocks; no time shuffle leakage.
- No threshold tuning / relabeling / outcome inspection before/after split freeze observed.

## Per-feature provenance (summary)
- B0: base rate (train-only) — no leakage.
- B1/C1/C2: mark/funding features from Hyperliquid public sources + lagged aggregates computed causally from history up to t. Label-derived lags (if used) are shifted to t-ε and computed from past observations only.

## Hard gate
Zero unresolved leaking features. **PASS**.

## Conclusion
No evidence of label leakage. Decision-time features only. Splits unchanged.
