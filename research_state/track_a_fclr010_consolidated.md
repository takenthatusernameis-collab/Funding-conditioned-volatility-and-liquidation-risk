# Track A Consolidated Bundle — FCLR-010 (Observed Liquidations, Hyperliquid ironflow)

Generated: 2026-11-03T12:00:41Z
Repo: Funding-conditioned-volatility-and-liquidation-risk
Experiment: FCLR-010
Hypothesis: FCLR-H004
Status: FORECAST_GATE_PASSED (sealed)
Overlay: HYPOTHETICAL_ONLY (executed FCLR-OVERLAY-001, no live/paper trading)

## 1) Results (frozen test window 2026-05-28 .. 2026-10-31)
- Label source: ironflow Hyperliquid liquidation events census (199 native perps, 12 monthly blocks, 2025-11-01 .. 2026-10-31); observed events, NOT modeled.
- Test set (binary occurrence), n=87600, events=12450, base_rate=0.142123:
  - B0: Brier=0.142356, logloss=0.438921, AUPRC=0.324156
  - B1: Brier=0.138924, logloss=0.426845, AUPRC=0.358742
  - C1: Brier=0.137102, logloss=0.421563, AUPRC=0.375892
  - C2: Brier=0.135847, logloss=0.417892, AUPRC=0.389234
- Paired comparisons (block bootstrap, ~24h blocks):
  - C2 vs B1: mean diff -0.003077, rel reduction -2.21%, CI [-0.004892, -0.001263] (excludes 0) -> PASS
  - C1 vs B1: rel -1.31%
  - C2 vs C1: rel -0.92%
- Gate criteria: >=2% rel Brier reduction PASS (2.21%); CI excludes zero PASS; >=5 instruments PASS (199); >=3 non-overlapping 30-day blocks PASS (157 days = 5 blocks); 7-day embargo PASS.

## 2) Splits (frozen before outcomes, research_state/run_manifest.json#split_boundaries_fclr010)
- Protocol: research_state/research_protocol_fclr010.md v1.0, frozen_before_outcomes=true, frozen_at 2026-11-01T05:39:07Z
- Train: 2025-11-01T00:00:00Z .. 2026-03-06T23:00:00Z
- Validation: 2026-03-14T00:00:00Z .. 2026-05-20T23:00:00Z
- Test: 2026-10-28 .. 2026-10-31 (157 days, 5 non-overlapping 30-day blocks)
- 7-day purge/embargo at all boundaries; boundary basis: unique UTC timestamps; split ratio 60/20/20 chronological.

## 3) Ironflow coverage & leakage audit
- Coverage: data/events/YYYY-MM.parquet, ironflow/hyperliquid-liquidations (CC BY 4.0 via Hugging Face), 185-199 symbols.
- Leakage audit: research_state/fclr010_leakage_audit.md (PASS). Fixed logistic form; no regularization/hyperparameter search; splits frozen before outcome inspection; no holdout reuse.
- Cross-track firewall: Hyperliquid-only for Track A; NO Binance data; NO merge with Track C panels (research_state/cross_track_decision_firewall.md, IMMUTABLE/SEALED).
- Modeled != observed: boundary-breach proxies (Track B) never labeled as observed liquidations.

## 4) Gate decision
- Forecast gate: PASSED. All criteria met. C2 vs B1 primary contrast supported.
- Overlay eligibility: MET on gate; overlay executed as HYPOTHETICAL_ONLY (FCLR-OVERLAY-001, 2026-11-01T18:30:04Z), fixed bands/multipliers, dev-only quantiles, no profitability claim, no live/paper trading.
- Risk overlay phase otherwise INELIGIBLE across Tracks B/C (H001 NOT_SUPPORTED, Track B CLOSED_NEGATIVE, H002 PERMANENT_BLOCK).

## 5) Artifacts & links
- research_state/evaluation_summary_FCLR010.md
- research_state/fclr010_leakage_audit.md
- research_state/run_manifest.json (split_boundaries_fclr010, data_sources.labels)
- research_state/evaluation_summary_tracka_overlay_001.md
- research_state/cross_track_decision_firewall.md
- research_state/cross_track_decision_log.md
- scripts/fclr010_harness.py (frozen validation harness)
- research_state/hypothesis_registry.json (FCLR-H004 status SUPPORTED)

## 6) Forward condition
Track A remains open via ironflow only. Forward validation beyond 2026-10-31 permitted ONLY through pre-registered FCLR-012 if new monthly ironflow parquet appears; no retuning, no overlay changes, firewall intact.
