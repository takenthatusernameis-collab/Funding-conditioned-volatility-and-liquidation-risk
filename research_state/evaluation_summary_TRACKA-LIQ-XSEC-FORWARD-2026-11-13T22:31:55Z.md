# Evaluation Summary — TRACKA-LIQ-XSEC-FORWARD-2026-11-13T22:31:55Z
**Generated (UTC):** 2026-11-13T22:31:55Z
**Campaign:** `FCLR-FORWARD-LIQ-2026Q1Q2` — Arm B forward (P2, exploratory)
**Experiment:** `TRACKA-LIQ-XSEC-FORWARD-20261113T222859Z`
**Prereg:** `research_state/prereg_tracka_liq_xsec_forward_2026q1q2_20261113T222859Z.json` (frozen 2026-11-13T22:28:59Z, promotable=false, max EXPLORATORY_ONLY)
**Panel:** `research_state/tracka_liq_xsec_forward_panel_2026-11-13T22:31:55Z.parquet`
**Verdict:** `EXPLORATORY_NULL` (EXPLORATORY_ONLY; never promotable)

## Universe (coverage-only, label-existence only)
- eligible coins (>= 20 liq-days, >= 100 liq events): 113
- complete hourly candle+funding coverage over test window: 107 coins
- universe (first 12): ['0G', 'AAVE', 'ADA', 'AERO', 'AIXBT', 'ALGO', 'APE', 'APT', 'AR', 'ARB', 'ASTER', 'ATOM'] ... (107 total)

## Primary estimand: Spearman rank IC(score_d, next-24h liquidation event count)
- mean IC across blocks = -0.027030556677033815
- pooled IC = -0.025121866063245266 (n=6634)
| Block | IC | n_rows | p_value (permutation) |
| 0 | -0.04092235444458491 | 2996 | 0.026 |
| 1 | -0.03124730002096616 | 1605 | 0.189 |
| 2 | -0.008922015565550372 | 2033 | 0.686 |
- permutation null (1000 reps, seed 20261112): 5th=-0.020772393084283722, 95th=0.01899805497678097, pooled p=0.031
## Secondary: top-k minus bottom-k next-24h notional spread
- block 0: k=11, top=141.58, bottom=2396345.49, spread=-2396203.91
- block 1: k=11, top=45663.27, bottom=3811.55, spread=41851.71
- block 2: k=11, top=3071.57, bottom=23442.02, spread=-20370.45
- spread sign consistent (positive) in >= 2/3 blocks: False (1/3)
## Materiality / Decision
- |mean IC| = 0.027030556677033815 >= 0.05: False
- verdict = EXPLORATORY_NULL
- failing minima if EXPLORATORY_NULL: mean_IC=-0.027030556677033815, floor 0.05, sign consistency 1/3
- Not promotable; not confirmatory; does not override sealed verdicts.
