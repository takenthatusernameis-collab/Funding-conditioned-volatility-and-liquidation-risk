# Track A Alternate Volatility Evaluation — TRACKA-ALT-VOL-20261112T020322Z
**Timestamp (UTC):** 2026-11-12T02:03:24Z
**Experiment:** TRACKA-ALT-VOL-20261112T015546Z (prereg frozen pre-outcomes)
**Prereg Document:** tracka_prereg_alt_volatility_20261112T015546Z.json
**Verdict:** `NOT_MET` — Alternate volatility design on cached panel: 6h horizon, C2_ALT (adds rv72h), 5 test blocks
**Panel:** tracka_vol_panel_20261111T234918Z.parquet (sha256: bd6b9924...)

## Panel & Coverage
- Total rows: 31815
- Symbols: 9 (AVAX, BNB, BTC, DOGE, ETH, LINK, SOL, SUI, XRP)
- Test rows: 20349

## Test Set QLIKE (lower is better)
- B1: mean_QLIKE=0.969875 (n=20268)
- C2_ALT: mean_QLIKE=0.913882 (n=20268)

## Paired Comparison (C2_ALT vs B1, block bootstrap)
- Paired n: 20268 across 5 test block(s)
- Mean diff (C2_ALT-B1) QLIKE: -0.055993
- 95% CI: [-0.121154, 0.033865]
- Relative QLIKE reduction: 5.77%

## Gate Assessment
- >= 2.0% relative QLIKE reduction: PASS
- 95% CI excludes zero (hi < 0): NOT_MET
- >= 5 paired instruments: PASS (9)
- >= 3 test blocks: PASS (5)
- **Forecast gate (all): NOT_MET**

## Compliance
- Prereg frozen pre-outcomes: PASS
- No threshold-shopping: PASS
- No sealed-holdout reuse: PASS
- Hyperliquid only, observed mark prices: PASS
- Bounded compute (fixed seeds, pre-specified reps): PASS
- No agent-set RESOLVED_VERIFIED/fabricated=true: PASS
- Note: Prereg specified 2025-11..2026-10 window but candle data only available 2026-05..2026-10; used available window with adjusted splits (5 test blocks)

---
**End of verdict.** Verdict ID: TRACKA-ALT-VOL-20261112T020322Z
