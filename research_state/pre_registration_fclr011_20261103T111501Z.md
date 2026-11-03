# Pre-Registration: FCLR-011 (CONFIRMATORY VOLATILITY)

Version: 1.0
Timestamp: 2026-11-03T11:15:01Z
Status: PRE-REGISTERED BEFORE OUTCOMES
Experiment ID: FCLR-011
Hypothesis: FCLR-H001 (incremental 24-hour volatility forecasting)

## Objective
Resolve the FCLR-002 block-count bottleneck by constructing a new confirmatory cell from available data (2026 archives already on disk) with >=3 non-overlapping 30-day test blocks. If infeasible to meet criteria, produce machine-checkable impossibility proof - no fabricated data.

## Data sources (to be verified)
- markPriceKlines / indexPriceKlines / premiumIndexKlines / klines under research_state/data_cache/* by symbol/month (2026 Jan-Aug)
- fundingRate archives under research_state/data_cache/* and any funding zips
- Root 2024 daily archives (as fallback) if needed, but focus on 2026 per handoff

## Design (frozen, identical to FCLR-008/FCLR-003)
- Models: B0 persistence, B1 RV-HAR, C1 funding-augmented, C2 combined
- Target: log(RV + 1e-12) of next-24h realized variance of mark-price returns (HORIZON=24)
- Standardization: training-only means/stds; zero-variance columns handled pre-outcomes
- Primary contrast: C2 vs B1 on 24h out-of-sample QLIKE
- Minimum relative improvement floor: >=2% relative QLIKE reduction
- Multiplicity: Holm correction across registered family
- Inference: block bootstrap, ~24h blocks, 2000 deterministic-seed replicates
- Minimums: >=5 instruments, >=3 non-overlapping 30-day blocks

## Splits (frozen BEFORE outcomes)
- Chronological train/val/test by unique UTC timestamps; >=7-day purge/embargo at all boundaries
- Candidate splits to be determined after coverage audit but MUST be frozen in this prereg before building panel/outcomes. If using 2026 data similar to FCLR-008: Train 2026-01-01..2026-03-17, Val 2026-03-25..2026-04-30, Test 2026-05-08..2026-08-06 with 7d embargo gaps. Alternatively if different window needed, splits must be chosen to maximize blocks while respecting embargo/purge and written to this prereg with timestamp before outcome computation.
- All split boundaries will be recorded in research_state/run_manifest.json and in pre-reg update before evaluation.

## Gates
- Gate MET only if C2 vs B1 shows >=2% relative QLIKE reduction with 95% CI excluding zero on improving side, AND >=5 instruments, AND >=3 non-overlapping 30-day blocks.
- Otherwise NOT_MET; retain null/negative.

## Constraints
- Pre-register BEFORE any outcome inspection
- Leakage-resistant: forecast timestamp t only uses data available <= t, trailing-only features, training-only normalization
- Purge/embargo >=7 days
- No re-tuning/re-opens of sealed experiments
- Track A remains blocked/monitor-only
