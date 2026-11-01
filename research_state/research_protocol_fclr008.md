# Research Protocol: FCLR-008 (CONFIRMATORY VOLATILITY)

Version: 1.0
Timestamp: 2026-11-01T00:50:00Z
Status: PRE-REGISTERED BEFORE OUTCOMES
Experiment ID: FCLR-008
Hypothesis: FCLR-H001 (incremental 24-hour volatility forecasting)

## Objective
Confirmatory test of funding-conditioned volatility forecasting (FCLR-H001) on the
unsealed 2026 panel. This is the decisive untested confirmatory cell: the widest
unsealed panel available (2026-01-01..2026-08-06, 5 symbols, 218 common days,
7 non-overlapping 30-day blocks), never confirmatory-tested. Prior sealed panels
(FCLR-003 powered 2024-12, FCLR-006 underpowered 2026 May-Aug, FCLR-007 11-day)
are NOT re-opened.

## Panel
- Period: 2026-01-01 .. 2026-08-06 (coverage-only audit: research_state/fclr008_coverage_audit.json)
- Symbols: BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT
- Common markPriceKlines timestamps: 5232 hourly, 218 days, 0 missing days
- Non-overlapping 30-day blocks in full panel: 7 (>=3 claim-worthy minimum met)

## Design (frozen, identical model family to FCLR-001/003/006/007)
- Models: B0 persistence, B1 RV-HAR, C1 funding-augmented, C2 combined
- Target: log(RV + 1e-12) of next-24h realized variance of mark-price returns
- Standardization: training-only means/stds; zero-variance columns handled pre-outcomes
- Primary contrast: C2 vs B1 on 24h out-of-sample QLIKE
- Minimum relative improvement floor: >=2% relative QLIKE reduction
- Multiplicity: Holm correction across the registered family
- Inference: block bootstrap, ~24h blocks, 2000 deterministic-seed replicates
- Minimums: >=5 instruments in paired OOS panel, >=3 non-overlapping 30-day blocks

## Splits (frozen before outcomes)
- Chronological train/val/test by unique UTC timestamps; 7-day purge/embargo at all boundaries
- Train: 2026-01-01T00:00:00Z .. 2026-03-17T23:00:00Z (76 days)
- Val: 2026-03-25T00:00:00Z .. 2026-04-30T23:00:00Z (37 days)
- Test: 2026-05-08T00:00:00Z .. 2026-08-06T23:00:00Z (91 days = 3 non-overlapping 30-day blocks)
- Embargo gaps: 2026-03-18..2026-03-24 (7d) and 2026-05-01..2026-05-07 (7d)
- Recorded in run_manifest.json#split_boundaries_fclr008 with frozen_before_outcomes=true

## Gates
- Gate MET only if C2 vs B1 shows >=2% relative QLIKE reduction with 95% CI excluding
  zero on the improving side, AND >=5 instruments, AND >=3 non-overlapping 30-day blocks.
- Otherwise NOT_MET; retain null/negative, do not threshold-shop, do not relax.

## Constraints
- No re-tuning, no model-family search, no regularization, no holdout reuse
- No sealed holdout (FCLR-001/002/003/005/006/007) re-opened or tuned
- Pre-registered before any outcome inspection; splits frozen before outcomes
- Track A (observed liquidations) remains structurally BLOCKED; not a prerequisite for Track C