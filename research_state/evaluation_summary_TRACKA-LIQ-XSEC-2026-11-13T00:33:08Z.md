# Evaluation Summary — TRACKA-LIQ-XSEC-2026-11-13T00:33:08Z
**Generated (UTC):** 2026-11-13T00:33:08Z
**Campaign:** `FCLR-FULLHISTORY-VOL-LIQ-20261112T201536Z` — Arm B (P2, exploratory)
**Prereg:** `research_state/prereg_tracka_liq_xsec_20261112T201536Z.json` (frozen 2026-11-12T20:15:36Z, `promotable=false`, max `EXPLORATORY_ONLY`)
**Panel:** `research_state/tracka_liq_xsec_panel_2026-11-13T00:33:08Z.parquet`
**Decision:** `EXPLORATORY_NULL` (reported as EXPLORATORY_ONLY; never promotable)

## Universe (coverage-only, label-existence only)
- eligible coins (>= 20 liq-days, >= 100 liq events): 183
- complete hourly candle+funding coverage over test window: 158 coins
- universe = ['0G', '2Z', 'AAVE', 'ADA', 'AIXBT', 'ALGO', 'ALT', 'ANIME', 'APE', 'APEX', 'APT', 'AR'] ... (158 total)
## Primary estimand: Spearman rank IC(score_d, next-24h liquidation event count)
- mean IC across blocks = 0.01448372914185373
- pooled IC = 0.031906233705182994 (n=13588)
| Block | IC | n_rows | p_value (permutation) |
| 0 | 0.004149190506233616 | 4424 | 0.95875 |
| 1 | 0.07250601928088088 | 4582 | 0.3636896551724138 |
| 2 | -0.033204022361553315 | 4582 | 0.6743793103448276 |
- permutation null (1000 reps, seed 20261112): 5th=-0.013461472448436738, 95th=0.014874253414622408, pooled p=0.094
## Secondary: top-k minus bottom-k next-24h notional spread (k = 10% universe, floor 5)
- block 0: k=16, top=5563954.62, bottom=565417.12, spread=4998537.50
- block 1: k=16, top=1121.29, bottom=241.75, spread=879.54
- block 2: k=16, top=717495.27, bottom=1074778.53, spread=-357283.26
- spread sign consistent (positive) in >= 2/3 blocks: True (2/3)
## Materiality: |mean IC| >= 0.05 AND spread sign consistent >= 2/3 blocks
- |mean IC| = 0.01448372914185373 >= 0.05: False
- decision = EXPLORATORY_NULL
- If EXPLORATORY_NULL: null preserved; exact failing minima: mean_IC=0.01448372914185373, materiality floor 0.05, sign consistency 2/3
