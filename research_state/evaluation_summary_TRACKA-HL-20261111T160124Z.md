# Track A Successor Evaluation — TRACKA-HL-20261111T160124Z
**Timestamp (UTC):** 2026-11-11T16:01:25Z
**Experiment:** TRACKA-HL-S-20261111T133430Z (successor prereg)
**Prereg document:** tracka_prereg_hyperliquid_successor_20261111T133430Z.json
**Verdict:** `NOT_MET` — Track A successor pre-registered C2 vs B1 evaluation
**Panel (RV-augmented):** tracka_hl_aligned_panel_with_rv_20261111T145731Z.parquet (sha256 b60fb55bc30ad8f1...)

## 1. Determination

Pre-registered primary contrast **C2 vs B1** (QLIKE on next-24h observed liquidation intensity)
evaluated on the admissible overlap window `2026-05-01..2026-10-31` (9 *-PERP symbols).
Forecast gate: **NOT_MET**.
Incremental forecast skill NOT demonstrated at pre-registered materiality gate.

## 2. Panel & Coverage
- Total buckets: 1314 (9 symbols x 184 days)
- Buckets with label: 1138
- Buckets with RV24h: 1305
- Buckets complete (label+funding+RV): 1089
- Symbols with any label: ['AVAX', 'BNB', 'BTC', 'DOGE', 'ETH', 'LINK', 'SOL', 'SUI', 'XRP'] (n=9)

## 3. Test Set QLIKE (lower is better)

- B0: mean_QLIKE=59.478768 (n=615)
- B1: mean_QLIKE=72.133883 (n=693)
- C1: mean_QLIKE=181.501427 (n=693)
- C2: mean_QLIKE=274.514250 (n=693)

## 4. Paired comparisons (block bootstrap, 30-day blocks, seed=20261111, 2000 replications)

### C2_vs_B1
- Paired n: 693 across 3 test block(s)
- Mean diff (modelA - modelB), QLIKE: 202.380367
- 95% CI: [15.418948, 443.775055]
- Relative QLIKE reduction: -280.56%

### C1_vs_B1
- Paired n: 693 across 3 test block(s)
- Mean diff (modelA - modelB), QLIKE: 109.367544
- 95% CI: [10.840049, 235.230264]
- Relative QLIKE reduction: -151.62%

### C2_vs_C1
- Paired n: 693 across 3 test block(s)
- Mean diff (modelA - modelB), QLIKE: 93.012823
- 95% CI: [4.578899, 208.544790]
- Relative QLIKE reduction: -51.25%

## 5. Gate assessment (primary contrast C2 vs B1)

- >= 2.0% relative QLIKE reduction (C2 vs B1): NOT_MET
- Relative reduction: -280.56%
- 95% CI excludes zero (CI hi < 0 => C2 better): NOT_MET
- 95% CI for diff (C2-B1): [15.418948, 443.775055]
- >= 5 paired OOS instruments: PASS (9: AVAX, BNB, BTC, DOGE, ETH, LINK, SOL, SUI, XRP)
- >= 3 non-overlapping test blocks with data: PASS (3: blocks [0, 1, 2])
- Test window days: 91 (3 x ~30-day blocks with 7d embargo)
- Forecast gate (all criteria): **NOT_MET**

## 6. Compliance
- No outcome inspection before prereg freeze: PASS (prereg frozen pre-outcomes)
- No Binance/2024 conflation: PASS (Hyperliquid only, observed ironflow labels)
- No modeled/proxy/synthetic liquidation labels: PASS (observed ironflow events only)
- No threshold-shopping: PASS (pre-registered models, metrics, thresholds)
- No sealed-holdout reuse: PASS (Track A window distinct from FCLR-002/003/Track B)
- No `.github/workflows` edits: PASS
- No redundant network polling: PASS (candles fetched once, first-time acquisition)

## 7. Artifacts
- Panel: /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk/research_state/tracka_hl_aligned_panel_with_rv_20261111T145731Z.parquet
- Panel report: /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk/research_state/tracka_hl_panel_with_rv_build_report_20261111T160124Z.json
- Prereg: /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk/research_state/tracka_prereg_hyperliquid_successor_20261111T133430Z.json

---
**End of verdict.** Verdict ID: TRACKA-HL-20261111T160124Z
