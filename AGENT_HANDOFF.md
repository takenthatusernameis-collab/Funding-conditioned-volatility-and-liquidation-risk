# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF)
Timestamp (UTC): 20261104T173620Z
Git SHA (HEAD): 876838c2
Branch: main
Repo: Funding-conditioned-volatility-and-liquidation-risk
Handoff ID: FCLR-HANDOFF-20261104T173620Z | Priority: P0 - HEAVY WORK ENFORCED | Mode: CAMPAIGN-DRIVEN | Enforcement: NO-SKIP

## STATE SNAPSHOT (CURRENT VERIFIED)
- Tests: 164/164 pass (pytest, ~16.6s). HEAD: 876838c2. Working tree clean except deleted __pycache__/*.pyc (bottleneck removed, not yet staged).
- Track C (FCLR-011): FORECAST_GATE_PASSED. C2 vs B1 mean diff -0.016458 QLIKE, 95% CI [-0.032546,-0.001418] EXCLUDES ZERO, relative reduction 4.94% (>=2% floor met), 5 instruments, 3 blocks (test 2026-05-08..2026-08-06). Splits frozen.
- Track C deeper validation (completed): research_state/trackc_deeper_validation_20261104T153049Z.md. Funding-quartile stratification monotonic (Q1 +3.84% -> Q4 +11.40% C2 vs B1). Funding×RV and funding×EMA interactions gains vs B1, CIs exclude zero. Mark/index premium + EMA24 ablations included. Block-bootstrap>=2000 (2000 reps, block 24h), Holm correction applied.
- Track C robustness (completed, two rounds): research_state/trackc_robustness_20261104T154226Z.md and trackc_robustness_20261104T154414Z.md. Leave-one-symbol out, leave-one-block out, funding sign/|funding| regimes, funding lags (t-1/t-2), winsorization (1%/5%), circular bootstrap 12h/24h/48h + stationary bootstrap (>=2000 reps, deterministic). C2 vs B1 remains positive across tested sensitivities on frozen splits (+6.8%..+7.3% rel QLIKE).
- Track C forward (FCLR-012-V): INCONCLUSIVE - blocked on data (Binance archive ends 2026-11-02, 0 non-overlapping 30d blocks). No admissible forward data.
- Track A (FCLR-010): COMPLETE_SEALED, FORECAST_GATE_PASSED (Brier rel -2.21%, CI excl zero, 199 instruments, 5 blocks). Blocked on new ironflow >=2026-11 (last probe 304, data_through 2026-10).
- Track B: NOT_SUPPORTED.
- Bottlenecks eliminated: caches cleaned (__pycache__/pyc), sweep updated with concrete evidence, no new schedulers/controllers/status-only files.

## MANDATORY INITIAL MESSAGE FOR NEXT AGENT (COPY/PASTE - DO NOT EDIT)
```text
TASK ID: FCLR-NEXT-060-TRACK-C-RECOMPUTE-FINALIZE-FROZEN-SPLITS
PRIORITY: P0 - HEAVY WORK ENFORCED (REPO-NAME PRIORITIZED = TRACK C / FUNDING-CONDITIONED VOLATILITY)
CAMPAIGN: TRACK C INDEPENDENT RECOMPUTATION + FINAL VERDICT (FROZEN FCLR-011/FCLR-002 SPLITS ONLY)
TIMESTAMP (UTC): 20261104T173620Z
OBJECTIVE: Track C gate PASSED (FCLR-011) and deeper validation + robustness already complete on frozen splits. Execute independent recomputation: re-run the robustness/deeper-validation pipeline from stored inputs + data hashes (research_state/data_cache/fclr011_panel.json, research_state/pre_registration_fclr011_20261103T111501Z.md, scripts/run_trackc_robustness_fclr011.py, scripts/run_trackc_deeper_validation_fclr011.py) to confirm reproducibility of C2 vs B1 QLIKE diff (-0.042908), rel reduction (~+7.0%), 95% CI exclusion of zero, Holm-adjusted ablations, funding-quartile monotonicity, and leave-one-out stability. Then write research_state/trackc_final_verdict_$(date -u +%Y%m%dT%H%M%SZ).md consolidating the complete Track C evidence base (gate result, deeper validation, robustness, recomputation audit, limitations, HYPOTHETICAL_ONLY overlay status). Do NOT re-run sealed FCLR-001/002/003/006/007/008/010/011 outcomes. Do NOT threshold-shop. Do NOT open sealed holdouts. Do NOT merge Binance and Hyperliquid. Track C overlay remains HYPOTHETICAL_ONLY.
CONSTRAINTS: No credentials, no manual files, no .github/workflows changes, no polling loops/schedulers/status-only files, no data fabrication, chronological/leakage-safe, preregister before outcomes if new data appears. Use existing frozen data only (no new downloads needed).
MANDATORY EVERY SESSION (EXECUTE ALL, IN ORDER - NO SKIPPING):
  1) STATE SWEEP (HEAVY): Read RESEARCH_PROMPT.md, AGENT_HANDOFF.md, run_manifest.json, research_state/* (especially trackc_deeper_validation_20261104T153049Z.md, trackc_robustness_20261104T154414Z.md, run_manifest.json, experiment_frontier.json), tests/, scripts/. Reconcile contradictions. Write research_state/campaign_sweep_$(date -u +%Y%m%dT%H%M%SZ).md (>=150 lines concrete evidence, file paths/lines).
  2) TRACK C INDEPENDENT RECOMPUTATION (HEAVY): On frozen FCLR-011 splits only, re-run robustness pipeline from stored inputs/hashes; confirm C2 vs B1 QLIKE diff, CI, rel reduction, Holm-adjusted ablations, funding-quartile monotonicity, leave-one-symbol/block stability, funding lags, winsorization, block-bootstrap (12h/24h/48h + stationary, >=2000 reps, deterministic). Write research_state/trackc_recompute_audit_$(date -u +%Y%m%dT%H%M%SZ).md with full tables and pass/fail vs original artifacts.
  3) TRACK C FINAL VERDICT (HEAVY): Write research_state/trackc_final_verdict_$(date -u +%Y%m%dT%H%M%SZ).md consolidating complete Track C evidence base (gate, deeper validation, robustness, recomputation audit, limitations, overlay HYPOTHETICAL_ONLY). Mark Track C as locked on frozen splits; forward replication (FCLR-012-V) remains INCONCLUSIVE/blocked on data.
  4) TRACK A TRIGGER (HEAVY): Run scripts/monitor_ironflow_liquidations.py --quick AND scripts/deep_review_alt_sources.py. If ANY new files >=2026-11 appear, PREREGISTER in research_state/fclr010_prereg_$(date -u +%Y%m%dT%H%M%SZ).json BEFORE inspecting outcomes and only then run frozen harness. Else record probe evidence with resume condition.
  5) BOTTLENECK ELIMINATION (HEAVY): Fix any blocking inefficiencies, clean __pycache__/pyc, ensure 164/164 green. No new controllers/schedulers/status-only files. Every action verifiable artifact.
STOP RULE: Complete all 5. Never stop early. If stuck, write blocker_evidence_$(date -u +%Y%m%dT%H%M%SZ).md with >=3 alternatives tried + concrete files/commands + single next action.
```

## Priority Order (by repo name)
1. **TRACK C - Funding-conditioned volatility** (HIGHEST, REPO-NAME PRIORITIZED). Gate passed; independent recomputation + final verdict on frozen splits (no new data needed).
2. **TRACK A - Liquidation risk** (ON TRIGGER ONLY). Only on new admissible unauthenticated >=2026-11 data; preregister before outcomes.
3. **INFRA/BOTTLENECKS** - Only if enable 1 or 2, keep 164/164 green.

## Bottleneck Elimination Plan
- Mine existing caches first (Binance zips, data_cache) - no unnecessary downloads
- Efficient probing via cached ETag (304) - no polling loops
- All heavy work with concrete artifacts
- No bloat files

## Verification commands
- `python -m pytest tests/ -q` (164 passed)
- `python scripts/monitor_ironflow_liquidations.py --quick`
- `git status` (clean except pyc)

## SESSION SUMMARY (20261104T154810Z - robustness complete)
- Campaign sweep written: research_state/campaign_sweep_20261104T154810Z.md (step 1 complete)
- Track C robustness (frozen FCLR-011 splits only): research_state/trackc_robustness_20261104T154226Z.md written with leave-one-symbol out, leave-one-block out, funding sign/|funding| regimes, funding lags (t-1/t-2), winsorization (1%/5%), circular bootstrap block sizes 12h/24h/48h and stationary bootstrap (>=2000 reps, deterministic). C2 vs B1 remains positive across tested sensitivities on frozen splits.
- Track A trigger probe: monitor_ironflow_liquidations.py --quick (ironflow_probe_20261104T154633Z.json), deep_review_alt_sources.py (alt_source_deep_review_20261104T154741Z.md). No new files >=2026-11 observed (cached_hits 0, added 0); remains ON TRIGGER ONLY with preregistration before outcomes if they appear.
- Bottlenecks: __pycache__/pyc cleaned, tests 164/164 green. No new schedulers/controllers/status-only files.

## NEXT FOCUS CAMPAIGN (this handoff)
- Independent recomputation of Track C from stored inputs/hashes (scripts/run_trackc_robustness_fclr011.py, scripts/run_trackc_deeper_validation_fclr011.py) on frozen FCLR-011 splits only -> research_state/trackc_recompute_audit_<UTC>.md
- Final Track C verdict consolidating gate + deeper validation + robustness + recomputation -> research_state/trackc_final_verdict_<UTC>.md
- Track A remains on trigger; Track C forward (FCLR-012-V) blocked on data until new admissible Binance panel beyond 2026-11-02 appears.
- Maintain leakage-safety, no threshold-shopping, overlay HYPOTHETICAL_ONLY.
