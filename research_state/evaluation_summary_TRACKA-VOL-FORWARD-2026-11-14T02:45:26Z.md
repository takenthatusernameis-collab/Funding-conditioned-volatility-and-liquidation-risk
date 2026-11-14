# Evaluation Summary — TRACKA-VOL-FORWARD-2026-11-14T02:45:26Z
**Generated (UTC):** 2026-11-14T02:45:26Z
**Campaign:** `FCLR-VOL-FORWARD-2026Q1Q2` — Arm A forward volatility (P1, exploratory)
**Experiment:** `TRACKA-VOL-FORWARD-2026Q1Q2-20261114T015222Z`
**Prereg:** `research_state/prereg_tracka_vol_forward_2026q1q2_20261114T015222Z.json` (frozen 2026-11-14T01:52:22Z, promotable=false, max EXPLORATORY_ONLY)
**Panel:** `research_state/tracka_vol_forward_panel_2026-11-14T02:45:26Z.parquet`

**Verdict:** `EXPLORATORY_NULL` (EXPLORATORY_ONLY; never promotable)

## Universe (coverage-only, label-existence only)
- complete hourly candle+funding+OI over scoring window: 165 coins (['0G', '2Z', 'AAVE', 'ACE', 'ADA', 'AERO', 'AIXBT', 'ALGO', 'ALT', 'ANIME', 'APE', 'APEX', 'APT', 'AR', 'ARB', 'ASTER', 'ATOM', 'AVAX', 'AVNT', 'AXS', 'BABY', 'BANANA', 'BCH', 'BERA', 'BIGTIME', 'BIO', 'BLUR', 'BNB', 'BRETT', 'BSV', 'BTC', 'CAKE', 'CC', 'CELO', 'CFX', 'CHILLGUY', 'COMP', 'CRV', 'DASH', 'DOGE', 'DOOD', 'DOT', 'DYM', 'EIGEN', 'ENA', 'ENS', 'ETC', 'ETH', 'ETHFI', 'FARTCOIN', 'FET', 'FIL', 'FOGO', 'GALA', 'GAS', 'GMT', 'GMX', 'GOAT', 'GRASS', 'GRIFFAIN', 'HBAR', 'HEMI', 'HYPE', 'HYPER', 'ICP', 'IMX', 'INIT', 'INJ', 'IO', 'IP', 'JTO', 'JUP', 'KAITO', 'KAS', 'LAYER', 'LDO', 'LINEA', 'LINK', 'LIT', 'LTC', 'MANTA', 'ME', 'MELANIA', 'MERL', 'MET', 'MINA', 'MNT', 'MON', 'MOODENG', 'MORPHO', 'MOVE', 'NEAR', 'NEO', 'NIL', 'NXPC', 'ONDO', 'OP', 'ORDI', 'PAXG', 'PENDLE', 'PENGU', 'PEOPLE', 'PNUT', 'POL', 'POPCAT', 'PROMPT', 'PROVE', 'PUMP', 'PYTH', 'RENDER', 'RESOLV', 'REZ', 'RUNE', 'S', 'SAND', 'SEI', 'SKR', 'SKY', 'SNX', 'SOL', 'SOPH', 'SPX', 'STABLE', 'STBL', 'STRK', 'STX', 'SUI', 'SUPER', 'SUSHI', 'SYRUP', 'TAO', 'TIA', 'TON', 'TRB', 'TRUMP', 'TRX', 'TST', 'UMA', 'UNI', 'VINE', 'VIRTUAL', 'VVV', 'W', 'WCT', 'WIF', 'WLD', 'WLFI', 'XLM', 'XMR', 'XPL', 'XRP', 'YGG', 'ZEC', 'ZEN', 'ZEREBRO', 'ZETA', 'ZK', 'ZORA', 'ZRO', 'kBONK', 'kFLOKI', 'kLUNC', 'kNEIRO', 'kPEPE', 'kSHIB'])
- scoring blocks with data: 3/3

## Primary estimand: QLIKE reduction C2_vs_B1 (headline horizon 24h)
- rel reduction = -0.49489318869499405 % (floor 2.0%)
- block-bootstrap CI (168h, 2000 reps) = [nan, nan], favours C2: False
- LOIO min rel reduction = -4.27622814169203 %
- materiality met: False

## Primary family (12 cells: 4 horizons x 3 contrasts, Holm across family)
| horizon | contrast | rel_reduction_% |
| 6 | C2_vs_B1 | -2.6189439019496414 |
| 6 | C1_vs_B1 | 99.99999620705002 |
| 6 | C2_vs_C1 | -2705517879.375048 |
| 24 | C2_vs_B1 | -0.49489318869499405 |
| 24 | C1_vs_B1 | 99.9999996538599 |
| 24 | C2_vs_C1 | -29033011166.43182 |
| 72 | C2_vs_B1 | -0.5941418826889984 |
| 72 | C1_vs_B1 | 99.99999951134127 |
| 72 | C2_vs_C1 | -20585766285.69361 |
| 168 | C2_vs_B1 | -3.106889210745689e-08 |
| 168 | C1_vs_B1 | 99.99999566234203 |
| 168 | C2_vs_C1 | -2305391444.912545 |
- Holm reject flags: [False, False, False, False, False, False, False, False, False, False, False, False]
## Failing minima if EXPLORATORY_NULL
- rel_reduction_pct=-0.49489318869499405 (floor 2.0), ci_lo=nan (must be > 0), blocks=3/3
- Not promotable; not confirmatory; does not override sealed verdicts or the forward liq verdict.
