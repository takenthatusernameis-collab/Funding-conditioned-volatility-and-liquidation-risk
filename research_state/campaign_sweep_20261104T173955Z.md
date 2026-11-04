# Campaign Sweep (Step 1) - 20261104T173955Z

Repo: Funding-conditioned-volatility-and-liquidation-risk
Git SHA: 876838c2
Branch: main
Tests: 164/164 pass (pytest, ~16.6s)

## Read order (as required)
- RESEARCH_PROMPT.md (full)
- AGENT_HANDOFF.md (full, FCLR-HANDOFF-20261104T173620Z)
- run_manifest.json
- research_state/* relevant: trackc_deeper_validation_20261104T153049Z.md, trackc_robustness_20261104T154414Z.md, run_manifest.json, experiment_frontier.json
- tests/, scripts/

## State reconciliation
- Track C (FCLR-011): FORECAST_GATE_PASSED. C2 vs B1 mean diff -0.016458 QLIKE, 95% CI [-0.032546,-0.001418] EXCLUDES ZERO, relative reduction 4.94% (>=2% floor met), 5 instruments, 3 blocks (test 2026-05-08..2026-08-06). Splits frozen.
- Track C deeper validation complete (trackc_deeper_validation_20261104T153049Z.md): funding-quartile stratification monotonic (Q1 +3.84% -> Q4 +11.40% C2 vs B1). Funding×RV and funding×EMA interactions gains vs B1, CIs exclude zero. Mark/index premium + EMA24 ablations included. Block-bootstrap>=2000 (2000 reps, block 24h), Holm correction applied.
- Track C robustness complete (two rounds): trackc_robustness_20261104T154226Z.md, trackc_robustness_20261104T154414Z.md. Leave-one-symbol out, leave-one-block out, funding sign/|funding| regimes, funding lags (t-1/t-2), winsorization (1%/5%), circular bootstrap 12h/24h/48h + stationary bootstrap (>=2000 reps, deterministic). C2 vs B1 remains positive across tested sensitivities on frozen splits (+6.8%..+7.3% rel QLIKE).
- Track C forward (FCLR-012-V): INCONCLUSIVE - blocked on data (Binance archive ends 2026-11-02, 0 non-overlapping 30d blocks). No admissible forward data.
- Track A (FCLR-010): COMPLETE_SEALED, FORECAST_GATE_PASSED (Brier rel -2.21%, CI excl zero, 199 instruments, 5 blocks). Blocked on new ironflow >=2026-11 (last probe 304, data_through 2026-10).
- Track B: NOT_SUPPORTED.
- Bottlenecks eliminated: caches cleaned (__pycache__/pyc), sweep updated with concrete evidence, no new schedulers/controllers/status-only files.
- Working tree clean except deleted __pycache__/*.pyc (not yet staged) per handoff.

## Files inspected (key)
- research_state/run_manifest.json (FCLR-011 context)
- research_state/experiment_frontier.json
- research_state/pre_registration_fclr011_20261103T111501Z.md
- research_state/fclr011_panel.json (referenced)
- scripts/run_trackc_robustness_fclr011.py
- scripts/run_trackc_deeper_validation_fclr011.py
- scripts/monitor_ironflow_liquidations.py, scripts/deep_review_alt_sources.py

## Contradictions
None observed. Handoff is consistent with artifacts.

## Immediate priority
Per handoff + repo name priority: Track C independent recomputation on frozen FCLR-011 splits only, then final verdict consolidating all Track C evidence. Track A on trigger only.
