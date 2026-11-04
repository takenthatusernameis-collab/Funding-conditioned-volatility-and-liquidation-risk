# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF)
Timestamp (UTC): 20261104T153545Z
Git SHA (HEAD): f128b157
Branch: main
Repo: Funding-conditioned-volatility-and-liquidation-risk
Handoff ID: FCLR-HANDOFF-20261104T153545Z | Priority: P0 - HEAVY WORK ENFORCED | Mode: CAMPAIGN-DRIVEN | Enforcement: NO-SKIP

## STATE SNAPSHOT (CURRENT VERIFIED)
- Tests: 164/164 pass (pytest, ~15.5s). HEAD: f128b157
- Track C (FCLR-011): FORECAST_GATE_PASSED. C2 vs B1 mean diff -0.016458 QLIKIE, 95% CI [-0.032546,-0.001418] EXCLUDES ZERO, relative reduction 4.94% (>=2% floor met), 5 instruments, 3 blocks (test 2026-05-08..2026-08-06). Splits frozen.
- Track C deeper validation (completed this session): research_state/trackc_deeper_validation_20261104T153049Z.md. Funding-quartile stratification shows monotonic improvement (Q1 +3.84% -> Q4 +11.40% C2 vs B1). Funding×RV and funding×EMA interactions show gains vs B1 with CIs excluding zero. Mark/index premium + EMA24 ablations included. Block-bootstrap>=2000 (2000 reps, block 24h), Holm correction applied.
- Track C forward (FCLR-012-V): INCONCLUSIVE - blocked on data (Binance archive ends 2026-11-02, 0 non-overlapping 30d blocks). No admissible forward data.
- Track A (FCLR-010): COMPLETE_SEALED, FORECAST_GATE_PASSED (Brier rel -2.21%, CI excl zero, 199 instruments, 5 blocks). Blocked on new ironflow >=2026-11 (last probe 304, data_through 2026-10).
- Track B: NOT_SUPPORTED.
- Bottlenecks eliminated: caches cleaned (__pycache__/pyc), sweep updated with concrete evidence, no new schedulers/controllers/status-only files.

## MANDATORY INITIAL MESSAGE FOR NEXT AGENT (COPY/PASTE - DO NOT EDIT)
```text
TASK ID: FCLR-NEXT-059-FUNDING-CONDITIONED-ROBUSTNESS-STABILITY
PRIORITY: P0 - HEAVY WORK ENFORCED (REPO-NAME PRIORITIZED = TRACK C)
CAMPAIGN: FUNDING-CONDITIONED VOLATILITY ROBUSTNESS & STABILITY (FROZEN SPLITS) -> DEEPER CONFIRMATION
TIMESTAMP (UTC): 20261104T153545Z
OBJECTIVE: Track C gate PASSED (FCLR-011). Deeper validation already done (funding quartiles + interactions + ablations). Execute robustness/stability checks on FROZEN FCLR-011/FCLR-002 splits ONLY to lock mechanism understanding without touching sealed outcomes. Focus: leave-one-symbol out, leave-one-time-block out, coefficient stability across regimes (funding sign/|funding|), funding lag sensitivity (t-1/t-2), winsorization sensitivity, alternative block-bootstrap (stationary/block sizes 12h/48h) with same deterministic seeds. Output research_state/trackc_robustness_$(date -u +%Y%m%dT%H%M%SZ).md with full tables, CIs, Holm correction. Do NOT re-run sealed FCLR-001/002/003/006/007/008/010/011. Do NOT threshold-shop. Track C overlay remains HYPOTHETICAL_ONLY.
CONSTRAINTS: No credentials, no manual files, no .github/workflows changes, no polling loops/schedulers/status-only files, no data fabrication, chronological/leakage-safe, preregister before outcomes if new data appears.
MANDATORY EVERY SESSION (EXECUTE ALL, IN ORDER - NO SKIPPING):
  1) STATE SWEEP (HEAVY): Read RESEARCH_PROMPT.md, AGENT_HANDOFF.md, run_manifest.json, research_state/* (especially trackc_deeper_validation_20261104T153049Z.md), tests/, scripts/. Reconcile any contradictions. Write research_state/campaign_sweep_$(date -u +%Y%m%dT%H%M%SZ).md (>=150 lines concrete evidence, file paths/lines).
  2) TRACK C ROBUSTNESS (HEAVY): On frozen splits only, run leave-one-symbol out, leave-one-block out, funding sign/|funding| regime coefficients, funding lag (1h/2h), winsor (1%/5%), block-bootstrap with block sizes 12h/48h + stationary bootstrap (>=2000 reps, deterministic). Compare vs frozen C2/B1, report delta QLIKE, 95% CI, p, Holm. Write research_state/trackc_robustness_$(date -u +%Y%m%dT%H%M%SZ).md with complete ablations table.
  3) TRACK A TRIGGER (HEAVY): Run scripts/monitor_ironflow_liquidations.py --quick AND scripts/deep_review_alt_sources.py. If ANY new files >=2026-11 appear (ironflow YYYY-MM.parquet or equivalent admissible unauthenticated source with events/fills), PREREGISTER in research_state/fclr010_prereg_$(date -u +%Y%m%dT%H%M%SZ).json BEFORE inspecting outcomes and only then run frozen harness. Else record probe evidence with resume condition.
  4) BOTTLENECK ELIMINATION (HEAVY): Fix any blocking inefficiencies, clean __pycache__/pyc, ensure 164/164 green. No new controllers/schedulers/status-only files. Every action verifiable artifact.
STOP RULE: Complete all 4. Never stop early. If stuck, write blocker_evidence_$(date -u +%Y%m%dT%H%M%SZ).md with >=3 alternatives tried + concrete files/commands + single next action.
```

## Priority Order (by repo name)
1. **TRACK C - Funding-conditioned volatility** (HIGHEST). Gate passed; do robustness/stability on frozen splits (leave-one-out, block sensitivity, lag/sign regimes). No new data needed.
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

## SESSION SUMMARY (20261104T153545Z - THIS HANDOFF)
- Prior session completed blocks 1-4: campaign sweep updated, deeper Track C validation done, Track A probed (no new data), caches cleaned, tests 164/164 green.
- Next focus: Track C robustness/stability on frozen splits (leave-one-out, bootstrap sensitivity, lags/signs) - heavy work, uses existing frozen data, directly extends passed gate.
