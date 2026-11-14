# Evaluation Summary — TRACKA-VOL-FORWARD-2026-11-14T03:30:40Z
**Generated (UTC):** 2026-11-14T03:30:40Z
**Campaign:** `FCLR-VOL-FORWARD-2026Q1Q2` — Arm A forward volatility (P1, exploratory)
**Experiment:** `TRACKA-VOL-FORWARD-2026Q1Q2-20261114T015222Z`
**Prereg:** `research_state/prereg_tracka_vol_forward_2026q1q2_20261114T015222Z.json` (frozen 2026-11-14T01:52:22Z, promotable=false, max EXPLORATORY_ONLY)
**Panel:** `research_state/tracka_vol_forward_panel_2026-11-14T03:30:40Z.parquet`

**Execution status:** `VALID_EXPLORATORY`
**Train rows:** 8897 | **Test rows:** 1485
**Scaling:** train_mean_std | **Fit split:** train_only
**Bootstrap n:** 1485 | **Block h:** 168 | **Holm method:** paired_permutation

**Verdict:** `EXPLORATORY_NULL` (EXPLORATORY_ONLY; never promotable)

## Universe (coverage-only, label-existence only)
- complete hourly candle+funding+OI over scoring window: 165 coins (['0G', '2Z', 'AAVE', 'ACE', 'ADA', 'AERO', 'AIXBT', 'ALGO', 'ALT', 'ANIME', 'APE', 'APEX', 'APT', 'AR', 'ARB', 'ASTER', 'ATOM', 'AVAX', 'AVNT', 'AXS', 'BABY', 'BANANA', 'BCH', 'BERA', 'BIGTIME', 'BIO', 'BLUR', 'BNB', 'BRETT', 'BSV', 'BTC', 'CAKE', 'CC', 'CELO', 'CFX', 'CHILLGUY', 'COMP', 'CRV', 'DASH', 'DOGE', 'DOOD', 'DOT', 'DYM', 'EIGEN', 'ENA', 'ENS', 'ETC', 'ETH', 'ETHFI', 'FARTCOIN', 'FET', 'FIL', 'FOGO', 'GALA', 'GAS', 'GMT', 'GMX', 'GOAT', 'GRASS', 'GRIFFAIN', 'HBAR', 'HEMI', 'HYPE', 'HYPER', 'ICP', 'IMX', 'INIT', 'INJ', 'IO', 'IP', 'JTO', 'JUP', 'KAITO', 'KAS', 'LAYER', 'LDO', 'LINEA', 'LINK', 'LIT', 'LTC', 'MANTA', 'ME', 'MELANIA', 'MERL', 'MET', 'MINA', 'MNT', 'MON', 'MOODENG', 'MORPHO', 'MOVE', 'NEAR', 'NEO', 'NIL', 'NXPC', 'ONDO', 'OP', 'ORDI', 'PAXG', 'PENDLE', 'PENGU', 'PEOPLE', 'PNUT', 'POL', 'POPCAT', 'PROMPT', 'PROVE', 'PUMP', 'PYTH', 'RENDER', 'RESOLV', 'REZ', 'RUNE', 'S', 'SAND', 'SEI', 'SKR', 'SKY', 'SNX', 'SOL', 'SOPH', 'SPX', 'STABLE', 'STBL', 'STRK', 'STX', 'SUI', 'SUPER', 'SUSHI', 'SYRUP', 'TAO', 'TIA', 'TON', 'TRB', 'TRUMP', 'TRX', 'TST', 'UMA', 'UNI', 'VINE', 'VIRTUAL', 'VVV', 'W', 'WCT', 'WIF', 'WLD', 'WLFI', 'XLM', 'XMR', 'XPL', 'XRP', 'YGG', 'ZEC', 'ZEN', 'ZEREBRO', 'ZETA', 'ZK', 'ZORA', 'ZRO', 'kBONK', 'kFLOKI', 'kLUNC', 'kNEIRO', 'kPEPE', 'kSHIB'])
- scoring blocks with data: 4/3

## Primary estimand: QLIKE reduction C2_vs_B1 (headline horizon 24h)
- rel reduction = -0.8919689279318814 % (floor 2.0%)
- block-bootstrap CI (168h, 2000 reps) = [-0.005794433958925705, -0.0017616914655115038], favours C2: False
- LOIO min rel reduction = -0.9644704437913616 %
- materiality met: False

## Primary family (12 cells: 4 horizons x 3 contrasts, Holm across family)
| horizon | contrast | rel_reduction_% |
| 6 | C2_vs_B1 | -1.9566558725582188 |
| 6 | C1_vs_B1 | -75.37482958142482 |
| 6 | C2_vs_C1 | 41.8635752257591 |
| 24 | C2_vs_B1 | -0.8919689279318814 |
| 24 | C1_vs_B1 | -69.12342595670444 |
| 24 | C2_vs_C1 | 40.34417860376114 |
| 72 | C2_vs_B1 | -0.23911571082219424 |
| 72 | C1_vs_B1 | -48.91725750729919 |
| 72 | C2_vs_C1 | 32.688046107813285 |
| 168 | C2_vs_B1 | -0.5770303778822055 |
| 168 | C1_vs_B1 | -40.17040442821994 |
| 168 | C2_vs_C1 | 28.24660042313937 |
- Holm reject flags: [True, True, False, True, True, False, False, True, False, True, True, False]
## Failing minima if EXPLORATORY_NULL
- rel_reduction_pct=-0.8919689279318814 (floor 2.0), ci_lo=-0.005794433958925705 (must be > 0), blocks=4/3
- Not promotable; not confirmatory; does not override sealed verdicts or the forward liq verdict.
