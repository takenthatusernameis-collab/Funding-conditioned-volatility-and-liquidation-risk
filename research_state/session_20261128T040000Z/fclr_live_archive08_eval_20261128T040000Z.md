# FCLR-LIVE-ARCHIVE-08 Evaluation — session_20261128T040000Z

**Campaign:** FCLR-LIVE-ARCHIVE-08-20261127T131654Z (Track-B modeled boundary-breach forecast)
**Session:** session_20261128T040000Z
**Generated:** 2026-11-28T04:00:00Z
**Experiment ID:** FCLR-LIVE-ARCHIVE-08

## Status

PENDING_HEAVY_COMPUTATION — Phase 2 heavy boundary-breach evaluation not yet executed.

## Target

Modeled boundary-breach 24h (whether future mark-price path breaches pre-registered hypothetical long/short liquidation boundary within 24-hour horizon).

## Design

- Symbols: BNBUSDT, BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT
- Months: 2024-04..2026-10 (31 months)
- Common support N: 22608
- Split: 60/20/20 + 168h embargo (train=13550, val=4517, test=4517; test_rows_across_5_symbols=22585)
- Models: B1 (mark-price-only), C2 (funding-conditioned)
- Metrics: out-of-sample AUC / log-loss / Brier
- Inference: >=2000 block-bootstrap + leave-one-symbol-out
- Alpha: sequential look k=2, alpha_2 = 0.008333
- Materiality floor: 0.02

## Required action

Execute the heavy 3-block boundary-breach evaluation in stdlib (no numpy/pandas/pyarrow/requests; no network; read-only cache). Replace this skeleton with complete results including:
- AUC/log-loss/Brier for B1 and C2
- >=2000 block-bootstrap replicates with 95% CI
- Leave-one-symbol-out results for all 5 symbols
- Verdict: FORECAST_GATE_PASSED / NOT_SUPPORTED / INCONCLUSIVE
- Holdout opened: true

## Note

Skeleton artifact. The heavy computation must be executed before the gate can pass.
