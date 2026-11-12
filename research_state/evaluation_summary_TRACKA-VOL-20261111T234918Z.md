# Evaluation Summary — TRACKA-VOL-20261111T234918Z
**Generated (UTC):** 2026-11-11T23:59:49Z
**Verdict:** **NOT_MET**

## Design (pre-registered)
- Prereg: `research_state/tracka_prereg_volatility_20261111T234918Z.json` (frozen pre-outcomes)
- Panel: `research_state/tracka_vol_panel_20261111T234918Z.parquet` (cached Hyperliquid candles+funding, 2026-05..2026-10, 9 coins)
- Target: next-24h realized variance (forward 24x1h log returns)
- Contrast: C2 (RV+funding+premium+ema_dist) vs B1 (RV-only), train-only OLS on log(y+eps), metric QLIKE (lower better)
- Splits: chronological, 3x30-day test blocks with 7-day embargo; block bootstrap (24h, 2000 reps, seed 20261111)

## Results
- Test pairs (eligible): 19233 | Paired instruments: 9 | Test blocks: 3 (all >=5 instruments: True)
- QLIKE B1: 0.44332726 | QLIKE C2: 0.44938545
- Improvement (B1-C2): -0.00605819 | Relative reduction: -1.3665%
- 95% block-bootstrap CI (B1-C2, favors C2 if >0): [-0.01424871, 0.00211600] | excludes zero favoring C2: False

## Per-block
- test_b1: n=6480, instruments=9, QLIKE B1=0.38792580, C2=0.38784986, rel=0.0196%
- test_b2: n=6480, instruments=9, QLIKE B1=0.44068267, C2=0.47352433, rel=-7.4525%
- test_b3: n=6273, instruments=9, QLIKE B1=0.50328876, C2=0.48801620, rel=3.0346%

## Criteria
- min_paired_instruments>=5: True
- min_test_blocks>=3: True
- all_blocks_ge5_instruments: True
- rel_reduction>=2pct: False
- ci95_excludes_zero_favors_c2: False

## Verdict
Pre-registered minima satisfied but materiality/inference criteria not fully satisfied; C2 not confirmed over B1 under frozen thresholds.

## Provenance/Integrity
- Panel sha256: `bd6b9924e2f76dfa9ea5cecd9737e62f32c0a76b663695bd9fc161cc1257b837`
- Cached Hyperliquid data only; causal features; no outcome peeking before prereg freeze; no threshold shopping; no sealed-holdout reuse; Hyperliquid-only.
