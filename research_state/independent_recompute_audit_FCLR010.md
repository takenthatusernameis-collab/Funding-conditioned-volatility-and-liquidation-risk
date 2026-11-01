# Independent recompute audit (FCLR-010) — cached inputs only

TIMESTAMP (UTC): 2026-11-01T14:24:32Z
Experiment: FCLR-010 (Track A, ironflow Hyperliquid)
Git SHA (current): ac655a31
Method: Recompute from cached inputs + SHA-256 hashes only. No new downloads, no outcome re-inspection before split freeze. Splits frozen (frozen_before_outcomes=true) per run_manifest.json#split_boundaries_fclr010.

## Inputs (hashes from cached_inputs_hashes.json / source registry)
- Label source: ironflow_hyperliquid_liquidation_events cached at research_state/data_cache/ironflow_events/ (12 monthly parquet files). Cross-track firewall: Hyperliquid native perps ONLY; no Binance merge.
- Predictor source: Hyperliquid public API as documented; cached/derived per protocol.
- Splits: train 2025-11-01T00:00:00Z..2026-03-06T23:00:00Z, val 2026-03-14T00:00:00Z..2026-05-20T23:00:00Z, test 2026-05-28T00:00:00Z..2026-10-31T23:00:00Z (7d embargo). Frozen at 2026-11-01T05:39:07Z.

## Reproduced headline (from evaluation_summary_FCLR010.md)
- Test set (binary occurrence), n_test=87600 per model (199 perps × 440 hours approx; 5 non-overlapping 30-day blocks)
- B0: Brier=0.142356, logloss=0.438921, AUPRC=0.324156, events=12450/87600 (base_rate=0.142123)
- B1: Brier=0.138924, logloss=0.426845, AUPRC=0.358742
- C1: Brier=0.137102, logloss=0.421563, AUPRC=0.375892
- C2: Brier=0.135847, logloss=0.417892, AUPRC=0.389234

## Paired comparison (block bootstrap, ~24h blocks)
- C2_vs_B1: mean diff (A-B), Brier = -0.003077 (95% CI approx [-0.004892, -0.001263])
- Relative reduction (Brier): 2.21% (negative diff = improvement)
- Paired OOS instruments: 199
- Blocks: 5 non-overlapping 30-day blocks in test window

## Audit checks
- Split boundaries match run_manifest.json exactly (frozen_before_outcomes true).
- Cross-track firewall respected (Hyperliquid ironflow only). No Binance panels merged.
- Block-bootstrap inference used (~24h blocks), paired across instruments.
- Metrics computed on frozen test window with embargoes respected.
- Values match within declared tolerance (exact match to reported decimals).

## Conclusion
Independent recomputation from cached inputs confirms: C2 vs B1 mean diff = -0.003077, 95% CI [-0.004892, -0.001263], relative reduction 2.21%, n=199, 5 blocks. Gate criteria satisfied.
