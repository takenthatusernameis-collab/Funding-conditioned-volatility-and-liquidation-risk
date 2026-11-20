# FCLR-XSEC-001 Cross-Sectional Funding-Intensity Contrast Evaluation

**Session:** session_20261120T175300Z
**Experiment:** FCLR-XSEC-001-20261120T175300Z
**Verdict:** NOT_SUPPORTED

## Evaluation Definition

Within-hour cross-sectional funding-intensity contrast. For each closed UTC hour t,
rank the 5 eligible perpetual contracts by signed funding rate observed at or before t.
Compare next-hour realized variance (rv1h at t+1) of high-funding vs low-funding coins
within the same hour. Isolates the funding effect from common market shocks (all coins
share the same hour), avoiding the serial correlation and non-stationarity that plagued
the time-series 24h forward RV forecast in FCLR-STARTER-001 (verdict NOT_SUPPORTED).

Distinct estimand from FCLR-STARTER-001. Per RESEARCH_PROMPT.md §16, this is the
designated next step after a NOT_SUPPORTED confirmatory verdict.

## Panel

- Path: research_state/fclr011_recompute_panel_20261115T234700Z.parquet
- SHA-256: 41962f823e59de5989c7d854cb3180cad61a4cbc2f5f230133c41b321342c1f4
- Hash verified: true
- Coins: BNBUSDT, BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT (5)
- Coverage: 2026-01-01 through 2026-08-31 (5,785 hourly timestamps)
- Rows with next-hour target: 23,558

## Funding Contrast (Primary)

| Metric | Value |
|--------|-------|
| n_hours | 5,334 |
| mean diff (high_funding − low_funding) | −0.125751 |
| 95% CI (block bootstrap, 2,000 reps, seed 20261120) | [−0.390010, 0.157598] |
| p_value | 0.388 |
| Holm adj_p | 0.388 |
| positive diffs | 2,290 / 5,334 (42.93%) |
| CI excludes zero | False |
| Holm passes | False |

## RV Persistence Baseline (Secondary)

| Metric | Value |
|--------|-------|
| n_hours | 5,328 |
| mean diff (high_rv − low_rv) | 0.176794 |
| 95% CI (block bootstrap, 2,000 reps, seed 20261120) | [−0.121076, 0.487735] |
| p_value | 0.257 |
| Holm adj_p | 0.514 |
| positive diffs | 3,200 / 5,328 (60.06%) |
| CI excludes zero | False |
| Holm passes | False |

## Multiplicity

- Family size: 2 (funding contrast, RV persistence baseline)
- Correction: Holm familywise-error

## Gate Criteria

| Criterion | Required | Result |
|-----------|----------|--------|
| CI excludes zero | Yes | False |
| Holm adj_p < 0.05 | Yes | False (0.388) |
| ≥5 instruments | Yes | True (5) |
| ≥3 blocks | Yes | True |

## Verdict: NOT_SUPPORTED

Neither the funding contrast nor the RV persistence baseline passes the gate.
CI includes zero for both; Holm correction fails. Null result preserved; no
threshold shopping.

Outcome data inspected before freeze: false.
