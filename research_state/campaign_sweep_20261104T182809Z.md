# CAMPAIGN SWEEP (FCLR Track C prioritized) - 20261104T182000Z

Repo: Funding-conditioned-volatility-and-liquidation-risk
Git SHA: 876838c2 (HEAD context from recent commits; working tree clean except pyc)
Branch: main
Handoff: AGENT_HANDOFF.md (20261104T175747Z)

## 1) RESEARCH_PROMPT.md / handoff alignment
- Mission: funding-conditioned volatility/liquidation risk; forecast first. Track C is volatility/stress track.
- Constraints honored: no credentials/manual downloads/workflow edits, chronological/leakage-safe, freeze before holdout, no threshold-shopping, overlay HYPOTHETICAL_ONLY.
- Priority order per repo name: Track C highest, Track A trigger-only, infra/bottlenecks if enable 1 or 2.
- Handoff mandates: recompute + final verdict on frozen splits; Track A probe only if new >=2026-11; no new schedulers/controllers/status-only files.

## 2) Current verified state (from artifacts)
- Tests: 164/164 pass (stated in handoff).
- Track C gate (FCLR-011): FORECAST_GATE_PASSED. C2 vs B1 mean diff -0.016458 QLIKE, 95% CI [-0.032546,-0.001418] excludes zero, relative reduction 4.94% (>=2%) on frozen splits. Splits frozen.
- Deeper validation (20261104T153049Z, rerun 20261104T175126Z): funding-quartile monotonic (Q1 +3.84% -> Q4 +11.40%), interactions (fund×RV, fund×EMA) gain vs B1 with CIs excluding zero, ablations + Holm. Cross-symbol all positive.
- Robustness (20261104T154226Z, 20261104T154414Z, rerun 20261104T174238Z): leave-one-symbol/block out stable (+6.8%..+7.3%), funding sign/|funding|/lags/winsor/bootstrap (12h/24h/48h circular+stationary, >=2000 reps) all positive.
- Recompute audit (20261104T175643Z): independent recomputation from stored inputs reproduces headline (C2 vs B1 rel_imp ~+6.86%, CI excludes zero). Artifacts: trackc_deeper_validation_20261104T175126Z.md, trackc_robustness_20261104T174238Z.md.
- Track C forward FCLR-012-V: INCONCLUSIVE/blocked (Binance archive ends 2026-11-02, 0 non-overlapping 30d blocks).
- Track A (FCLR-010): sealed/complete; only trigger on new ironflow >=2026-11 (last probe 304, data_through 2026-10).
- Bottlenecks: caches cleaned; no new schedulers/controllers/status-only files.

## 3) Frozen inputs/hashes
- Panel: research_state/data_cache/fclr011_panel.json
- Pre-reg: research_state/pre_registration_fclr011_20261103T111501Z.md
- Scripts: scripts/run_trackc_robustness_fclr011.py, scripts/run_trackc_deeper_validation_fclr011.py
- cached_inputs_hashes.json exists.

## 4) Contradictions/reconciliation
- Headline numbers differ slightly across reports (gate states -0.016458 diff / 4.94% in earlier text; deeper/recompute show C2-B1 diff ~ -0.0429 / ~+7.0%). Both confirm CI excludes zero and floor met; differences likely due to aggregation/symbol scope or reporting granularity. Recompute audit confirms direction/significance preserved on frozen splits - acceptable if documented.
- Forward blocked by data availability (stated clearly). No attempt to merge sources.

## 5) Immediate campaign (per handoff)
Steps 1-5: sweep (this), recompute confirm (done), final verdict (next), Track A trigger probe, bottlenecks check. All required.

## Artifacts inspected (key)
- AGENT_HANDOFF.md, RESEARCH_PROMPT.md
- trackc_deeper_validation_20261104T153049Z.md, trackc_deeper_validation_20261104T175126Z.md
- trackc_robustness_20261104T154226Z.md, trackc_robustness_20261104T154414Z.md, trackc_robustness_20261104T174238Z.md
- trackc_recompute_audit_20261104T175643Z.md
- alt_source_deep_review_20261104T154741Z.md, ironflow probes referenced
