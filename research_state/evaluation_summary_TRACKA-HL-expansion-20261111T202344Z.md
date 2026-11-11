# Track A Symbol-Expansion Evaluation — TRACKA-HL-expansion-20261111T202344Z
**Timestamp (UTC):** 2026-11-11T20:23:48Z
**Experiment:** TRACKA-HL-EXPANSION-20261111T195500Z
**Prereg:** tracka_prereg_hyperliquid_expansion_20261111T195500Z.json
**Verdict:** `PASS` — C2 vs B1 on observed Hyperliquid liquidation intensity (expanded universe)
**Panel:** tracka_hl_expansion_panel_20261111T202344Z.parquet (sha256 39916a72dfc37d15...)

## Universe
- Selected (n=8): ZEC, NEAR, UNI, AAVE, CRV, ADA, LTC, BCH
- Symbols with any label in panel: ['AAVE', 'ADA', 'BCH', 'CRV', 'LTC', 'NEAR', 'UNI', 'ZEC']
- Label buckets: 953, RV24h buckets: 1160, complete label+funding+RV: 918

## Test Set QLIKE
- B0: mean_QLIKE=10.912079 (n=515)
- B1: mean_QLIKE=14.234009 (n=593)
- C1: mean_QLIKE=12.856237 (n=593)
- C2: mean_QLIKE=11.524267 (n=593)

## Paired comparisons (block bootstrap, 7d embargo, seed=20261111, 2000 reps)
### C2_vs_B1
- Paired n: 593 across 3 block(s)
- Mean diff (A-B) QLIKE: -2.709742
- 95% CI: [-5.088102, -0.477660]
- Relative QLIKE reduction: 19.04%

### C1_vs_B1
- Paired n: 593 across 3 block(s)
- Mean diff (A-B) QLIKE: -1.377772
- 95% CI: [-3.174861, -0.204874]
- Relative QLIKE reduction: 9.68%

### C2_vs_C1
- Paired n: 593 across 3 block(s)
- Mean diff (A-B) QLIKE: -1.331970
- 95% CI: [-1.913241, -0.272786]
- Relative QLIKE reduction: 10.36%

## Gate assessment (primary C2 vs B1)
- >= 2.0% relative QLIKE reduction: PASS (19.04%)
- 95% CI excludes zero (hi < 0): PASS ([-5.088102, -0.477660])
- >= 5 paired instruments: PASS (8: AAVE, ADA, BCH, CRV, LTC, NEAR, UNI, ZEC)
- >= 3 test blocks with data: PASS (3: [0, 1, 2])
- Forecast gate (all): **PASS**

## Compliance
- Prereg frozen pre-outcomes; evaluation run after panel build complete: PASS
- Hyperliquid observed ironflow labels only; no Binance/2024 conflation: PASS
- No modeled/proxy/synthetic labels; no threshold-shopping; no sealed-holdout reuse: PASS
- Bounded first-time acquisition with provenance for missing expansion inputs; no re-fetch valid cached 9-coin/complete data: PASS

## Artifacts
- Prereg: research_state/tracka_prereg_hyperliquid_expansion_20261111T195500Z.json
- Universe: research_state/tracka_hl_expansion_universe_20261111T201958Z.json
- Acquisition: research_state/tracka_hl_expansion_acquisition_report_20261111T201958Z.json
- Panel: research_state/tracka_hl_expansion_panel_20261111T202344Z.parquet
- Build report: research_state/tracka_hl_expansion_panel_build_report_20261111T202344Z.json
