# Research Protocol: FCLR-007 (CONFIRMATORY VOLATILITY)

Version: 1.0
Timestamp: 2026-10-31T00:18:25Z
Status: PRE-REGISTERED BEFORE OUTCOMES

## Objective
Confirmatory test of funding-conditioned volatility forecasting (FCLR-H001) on unsealed 2026 panel.

## Panel
- Period: 2026-04-01 .. 2026-07-31 (~122 days)
- Symbols: BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT
- Blocks: >=4 non-overlapping 30-day blocks (>=3 required)

## Design (copy of FCLR-001/FCLR-006)
- Models: B0 persistence, B1 RV-HAR, C1 funding-augmented, C2 combined
- Target: log RV + 1e-12
- Standardization: training-only
- Primary contrast: C2 vs B1 on 24h QLIKE
- Minimum relative improvement floor: >=2%
- Multiplicity: Holm correction
- Inference: block bootstrap 2000 replicates (deterministic seed)
- Minimums: >=5 instruments, >=3 non-overlapping 30-day blocks

## Splits
- Chronological 60/20/20
- 7-day purge/embargo
- Frozen before outcomes; recorded in split_boundaries_fclr007

## Gates
- Gate MET only if C2 vs B1 shows improvement >=2% relative on QLIKE with CI not crossing zero under stated design
- Otherwise NOT_MET

## Constraints
- No re-tuning, no holdout reuse, no threshold shopping
- Pre-registered before outcome inspection
