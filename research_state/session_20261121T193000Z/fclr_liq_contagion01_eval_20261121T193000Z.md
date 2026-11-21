# FCLR-LIQ-CONTAGION-001 — Cross-Coin Liquidation Contagion Evaluation
- **Experiment ID:** FCLR-LIQ-CONTAGION-001-20261121T193000Z
- **Session:** session_20261121T193000Z
- **Generated (UTC):** 2026-11-21T19:30:00Z
- **Campaign:** FCLR-LIQ-CONTAGION-001 (rank-0)

## Frozen input (sha256 asserted before any read)
- Panel: `/home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk/research_state/fclr_liq_combined_panel_20261115T181405Z.parquet`
- sha256: `81a100d5d0625832bebabaabea13b786e15319577721cfe8507da5b779ec7f14` (matches prereg)
- Rows: 1,740,415 events | Coins: 15 | Span: 2025-03-22 -> 2026-10-31

## Methodology (executed per prereg)
- Hourly aggregation: 211,188 hourly coin-observations (0 hours dropped for no prior funding)
- Lead-lag matrix: 15x15 x 24 lags = 5040 coefficients
- Granger causality: 210 directed pairs, VAR(6), numpy OLS F-test
- Permutation test: 1000 permutations per pair (210,000 null statistics)
- Bonferroni alpha: 4.8e-05 across 210 tests
- Materiality floor: 2% relative (frozen, not relaxed)
- Funding-tercile conditioning (low/medium/high)
- Volatility spillover: rv24h(src) -> liq_count(tgt)
- Temporal stability: rolling 90-day windows, 30-day step

## Results
- Granger-significant directed edges (Bonferroni): 155/210 (density 0.7381)
- Permutation-significant pairs: 16/210
- Final contagion network edges: 11/210 (density 0.0524)
- Funding-tercile monotonicity: 38/112 pairs (0.339)
- Volatility spillover significant pairs: 19/210
- Temporal stability windows: 17, mean density 0.3445

### Top contagion edges
| src -> tgt | Granger F | Granger p | Empirical p |
|---|---:|---:|---:|
| ADA -> DOGE | 21.856 | 9.9e-26 | 0 |
| CRV -> ETH | 21.405 | 3.6e-25 | 0 |
| AVAX -> CRV | 18.529 | 1.4e-21 | 0 |
| XRP -> ETH | 12.581 | 3.3e-14 | 0 |
| BTC -> DOGE | 12.083 | 1.4e-13 | 0 |
| CRV -> LINK | 9.741 | 9.8e-11 | 0 |
| BTC -> ETH | 9.402 | 2.5e-10 | 0 |
| ETH -> XRP | 8.364 | 4.5e-09 | 0 |
| BTC -> NEAR | 8.154 | 8e-09 | 0 |
| SOL -> BTC | 7.285 | 8.7e-08 | 0 |

## Hypothesis verdicts
- **H_contagion_liq:** SUPPORTED (edges=11, density=0.0524, floor=2%)
- **H_contagion_funding:** NOT_SUPPORTED (monotonic rate=0.339)
- **Overall:** NOT_SUPPORTED

## Hard constraints honored
- outcome_data_inspected_before_freeze=false · panel sha256 asserted · materiality floor 0.02 frozen · observed liquidations only (Track A) · no external trigger · no network/paid data/credentials · no root-level md/json · no .github/workflows modification · no overwrite of research_state/research_protocol.md
