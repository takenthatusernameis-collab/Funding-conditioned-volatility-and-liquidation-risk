# Evaluation Summary (FCLR-012-V)

Experiment: FCLR-012-V (FORWARD VOLATILITY — UNSEALED 2026 PANEL)
Data range: 2026-08-07 .. 2026-11-02
Generated: 2026-11-04T00:52:00Z
Pre-registration: research_state/pre_registration_fclr012v_20261104T005000Z.md v1.0
Status: PRE-REGISTERED BEFORE OUTCOMES -> INCONCLUSIVE (PILOT)

## Splits (frozen BEFORE outcomes)
- Train: 2026-08-07T00:00:00Z .. 2026-09-16T23:00:00Z
- Val: 2026-09-24T00:00:00Z .. 2026-10-21T23:00:00Z
- Test: 2026-10-29T00:00:00Z .. 2026-11-02T23:00:00Z (7d embargo)

## Test set QLIKE (lower is better)

- B0: mean_QLIKE=0.587464 (n=360)
- B1: mean_QLIKE=0.539492 (n=360)
- C1: mean_QLIKE=0.546570 (n=360)
- C2: mean_QLIKE=0.457563 (n=360)

## Paired comparisons (block bootstrap, ~24h blocks, 2000 replications)

### C2_vs_B1
- Paired n: 360
- Mean diff (modelA - modelB), QLIKE: -0.081929 (95% CI [-0.360564, 0.059434])
- Relative reduction (QLIKE): 15.19% (negative diff means improvement)

### C1_vs_B1
- Paired n: 360
- Mean diff (modelA - modelB), QLIKE: 0.007078 (95% CI [-0.066153, 0.051887])
- Relative reduction (QLIKE): -1.31% (negative diff means improvement)

### C2_vs_C1
- Paired n: 360
- Mean diff (modelA - modelB), QLIKE: -0.089007 (95% CI [-0.294411, 0.019843])
- Relative reduction (QLIKE): 16.28% (negative diff means improvement)

## Gate assessment (primary contrast C2 vs B1)

- Primary contrast C2 vs B1 meets >=2% relative QLIKE reduction: PASS
- Relative reduction: 15.19%
- 95% CI for diff (C2-B1): [-0.360564, 0.059434] (excludes zero: no)
- Paired OOS instruments: 5 (BNBUSDT, BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT) -> >=5: PASS
- Test window: 2026-10-29 .. 2026-11-02 = 5 days = 0 non-overlapping 30-day block(s) -> >=3: NOT_MET
- Forecast gate (all criteria): NOT_MET

## Verdict
INCONCLUSIVE / PILOT. The point estimate is encouraging (15.19% relative QLIKE
reduction, direction consistent with FCLR-011's +4.94%), but the 95% CI spans zero
and the test window is only 5 days (0 non-overlapping 30-day blocks). Per the frozen
preregistration the block-count criterion fails a priori, so the gate CANNOT pass
and the result must NOT be promoted to confirmatory. This is a forward replication
signal on genuinely new data, not a sealed-holdout reuse.

## Notes
- All results use frozen splits only; no tuning on holdout.
- Features with missing values filled with 0.0 where protocol allows or rows dropped if core RV features missing.
- Mark/index premium not fully integrated where source missing; EMA distance computed from mark prices.
- 2026-10-28 and 2026-10-29 mark days are genuinely absent from the Binance archive
  (HTTP 404 on live probe 2026-11-04T00:45Z); they are NOT imputed, which is why the
  test window starts 2026-10-29 rather than 2026-10-28.
- Archive genuinely ends 2026-11-02 (2026-11-03/04 probed -> 404); no newer admissible
  Binance data exists as of 2026-11-04T00:45Z.