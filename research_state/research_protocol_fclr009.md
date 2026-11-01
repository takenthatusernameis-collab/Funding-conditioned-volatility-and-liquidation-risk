# Research Protocol: FCLR-009 (CONFIRMATORY VOLATILITY)

Version: 1.0
Timestamp: 2026-11-01T03:00:00Z
Status: PRE-REGISTERED BEFORE OUTCOMES
Experiment ID: FCLR-009
Hypothesis: FCLR-H001 (incremental 24-hour volatility forecasting)

## Objective
Confirmatory test of funding-conditioned volatility forecasting (FCLR-H001) on the
unsealed 2025 panel. This is the second widest untested confirmatory cell and the
first full-calendar-year panel: 2025-01-01..2025-12-31, 5 symbols, 365 common days,
12 non-overlapping 30-day blocks. Prior sealed panels (FCLR-003 powered 2024-12,
FCLR-006 underpowered 2026 May-Aug, FCLR-007 11-day) and the unsealed FCLR-008
(2026-01-01..2026-08-06, +4.30% but CI crosses zero) are NOT re-opened.

FCLR-008 left H001 INCONCLUSIVE: first unsealed panel with a positive direction
(C2 vs B1 +4.30% relative QLIKE) but the 95% CI crossed zero. FCLR-009 is the
independent out-of-sample extension that can resolve that inconclusiveness on a
materially different, longer window. It is pre-registered here BEFORE any outcome
inspection and BEFORE split freezing.

## Panel
- Period: 2025-01-01 .. 2025-12-31 (coverage-only audit: research_state/fclr009_coverage_audit.json)
- Symbols: BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT
- Common markPriceKlines timestamps: 8760 hourly, 365 days, 0 missing days per symbol
- Non-overlapping 30-day blocks in full panel: 12 (>=3 claim-worthy minimum met; test window alone yields 6)

## Design (frozen, identical model family to FCLR-001/003/006/007/008)
- Models: B0 persistence, B1 RV-HAR, C1 funding-augmented, C2 combined
- Target: log(RV + 1e-12) of next-24h realized variance of mark-price returns
- Standardization: training-only means/stds; zero-variance columns handled pre-outcomes
- Primary contrast: C2 vs B1 on 24h out-of-sample QLIKE
- Minimum relative improvement floor: >=2% relative QLIKE reduction
- Multiplicity: Holm correction across the registered family
- Inference: block bootstrap, ~24h blocks, 2000 deterministic-seed replicates
- Minimums: >=5 instruments in paired OOS panel, >=3 non-overlapping 30-day blocks

## Splits (frozen before outcomes)
- Chronological train/val/test by unique UTC timestamps across the common 5-symbol panel; 7-day purge/embargo at all boundaries
- Train: 2025-01-01T00:00:00Z .. 2025-04-05T23:00:00Z (96 days)
- Val: 2025-04-13T00:00:00Z .. 2025-05-31T23:00:00Z (49 days)
- Test: 2025-06-08T00:00:00Z .. 2025-12-31T23:00:00Z (206 days = 6 non-overlapping 30-day blocks: Jun 8-Jul 7, Jul 8-Aug 7, Aug 8-Sep 6, Sep 7-Oct 6, Oct 7-Nov 5, Nov 6-Dec 5; +26-day remainder)
- Embargo gaps: 2025-04-06..2025-04-12 (7d) and 2025-06-01..2025-06-07 (7d)
- Recorded in run_manifest.json#split_boundaries_fclr009 with frozen_before_outcomes=true

## Gates
- Gate MET only if C2 vs B1 shows >=2% relative QLIKE reduction with 95% CI excluding
  zero on the improving side, AND >=5 instruments, AND >=3 non-overlapping 30-day blocks.
- Otherwise NOT_MET; retain null/negative, do not threshold-shop, do not relax.
- FCLR-009 is a distinct estimand window from FCLR-008; a NOT_MET here does NOT
  rescue or invalidate FCLR-008, and vice versa. Both are reported independently.

## Constraints
- No re-tuning, no model-family search, no regularization, no holdout reuse
- No sealed holdout (FCLR-001/002/003/005/006/007) re-opened or tuned; FCLR-008 not re-run
- Pre-registered before any outcome inspection; splits frozen before outcomes
- Track A (observed liquidations) remains structurally BLOCKED; not a prerequisite for Track C
- No new downloads, no credentials, no sealed holdouts; data already cached in research_state/data_cache/