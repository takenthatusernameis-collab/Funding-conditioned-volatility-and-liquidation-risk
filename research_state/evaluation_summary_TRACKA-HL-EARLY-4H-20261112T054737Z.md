# Track A Early 4h Evaluation — TRACKA-HL-EARLY-4H-20261112T054737Z
**Timestamp (UTC):** 2026-11-12T06:39:07Z
**Verdict:** `INCONCLUSIVE_PILOT_SHORTFALL`
**Prereg:** `tracka_prereg_hyperliquid_early_4h_20261112T054737Z.json` (sha256 909590bb96ed9dc3...)
**Panel:** `tracka_hl_early_4h_panel_20261112T054737Z.parquet` (sha256 ddb223307f1483a1...)

## Determination
PILOT/INCONCLUSIVE — <3 non-overlapping 30-day test blocks within 2025-11-01..2026-04-30 window (blocks with data: 2, required: 3). Primary gate cannot be satisfied per prereg; results reported for transparency, not confirmatory PASS.

## Metrics (QLIKE, lower better)
- B1 mean QLIKE: 76.50737384841467 (n=362)
- C2 mean QLIKE: 100.71437567012083 (n=362)
- C2 vs B1 mean diff: 24.207001821706154 (95% CI [22.037348458330037, 25.408226216021685], n_pairs=362, n_blocks=2)
- Relative QLIKE reduction (C2 vs B1): -31.64008984240903%

## Gate Assessment (primary C2 vs B1)
- >=2% rel reduction: NOT_MET (-31.64008984240903)
- 95% CI excludes zero (C2 better): NOT_MET
- >=5 paired instruments: PASS (9: ['AVAX', 'BNB', 'BTC', 'DOGE', 'ETH', 'LINK', 'SOL', 'SUI', 'XRP'])
- >=3 non-overlapping 30d test blocks: NOT_MET (2: [0, 1])
- Forecast gate (all): NOT_MET

## Compliance
- no_outcome_inspection_before_freeze: True
- no_threshold_shopping: True
- no_binance_2024_conflation: True
- no_modeled_proxy_labels: True
- venue_consistent: Hyperliquid-only

**Caveat:** Block 2 extends beyond 2026-04-30 window; effective test blocks within window are 0 and 1 only (2 < 3).
