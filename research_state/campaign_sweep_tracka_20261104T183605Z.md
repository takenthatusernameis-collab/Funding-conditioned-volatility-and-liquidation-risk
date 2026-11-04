# CAMPAIGN SWEEP - TRACK A (HEAVY, MANDATORY) - 20261104T183605Z

Repo: Funding-conditioned-volatility-and-liquidation-risk
Git SHA (HEAD): ade33dd0
Branch: main
Handoff ID: FCLR-HANDOFF-20261104T183334Z
Mode: CAMPAIGN-DRIVEN | Enforcement: NO-SKIP | Priority: P0

## 1) STATE SNAPSHOT (VERIFIED)
- Tests: 164/164 pass (pytest). Working tree clean (pyc cleaned).
- Track C (FCLR-011): LOCKED COMPLETE on frozen splits. Final verdict present (trackc_final_verdict_20261104T182830Z.md). Forward replication FCLR-012-V INCONCLUSIVE/blocked on data (Binance ends 2026-11-02, 0 non-overlapping 30d blocks). Overlay HYPOTHETICAL_ONLY. No re-tuning on frozen splits.
- Track A (FCLR-010): COMPLETE_SEALED, FORECAST_GATE_PASSED (Brier rel -2.21%, CI excl zero). Consolidated artifact present. Blocked on new ironflow >=2026-11 (last probe no new files). ON TRIGGER ONLY.
- Track B: NOT_SUPPORTED.
- Bottlenecks: no new schedulers/controllers/status-only files observed. Caches cleaned per handoff.

## 2) TRACK A TRIGGER READINESS
- Handoff mandates: monitor for new admissible unauthenticated ironflow/liquidation data >=2026-11. If ANY new files appear (>=2026-11), PREREGISTER before inspecting outcomes with full hypothesis/frozen splits/metrics/stop rule, then run ONLY frozen FCLR-010 harness. If no new data -> heavy trigger audit with concrete resume conditions.
- Last probes mentioned in prior sweeps show no new files >=2026-11; need fresh probe now.

## 3) EVIDENCE FILES INSPECTED
- AGENT_HANDOFF.md (current)
- RESEARCH_PROMPT.md (read - constraints enforced)
- run_manifest.json (FCLR-010 COMPLETE_SEALED, FCLR-011 LOCKED, FCLR-012-V INCONCLUSIVE)
- research_state/trackc_final_verdict_20261104T182830Z.md
- research_state/track_a_fclr010_consolidated.md (referenced)
- Prior campaign_sweeps present

## 4) CONSTRAINTS REMINDER (ENFORCED)
- No credentials, no manual files, no .github/workflows changes
- No polling loops/schedulers/status-only files
- No data fabrication, leakage-safe
- Preregister-before-outcomes strictly enforced if new data
- Track C remains LOCKED - no modifications/re-runs on sealed codepaths
- No merging sources; Hyperliquid-only for Track A per firewall

## 5) NEXT ACTIONS (MANDATORY)
1. Run Track A trigger probe (scripts/monitor_ironflow_liquidations.py --quick, scripts/deep_review_alt_sources.py). Compare against last probes; list files with mtime >=2026-11-01.
2. If none: write tracka_trigger_audit with ETag/cached_hits, last data_through, resume conditions, explicit "NO NEW DATA - ON HOLD". If any: HALT, preregister FIRST with frozen splits/hypothesis/metrics/guardrails, proceed only via frozen harness.
3. Track C sanity check (read-only).
4. Bottleneck elimination (pyc clean, tests green).
5. Consolidate artifacts.

NO SKIP. HEAVY WORK ENFORCED.
