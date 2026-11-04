# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF)
Timestamp (UTC): 20261104T183948Z
Git SHA (HEAD): 906f83ce
Branch: main
Repo: Funding-conditioned-volatility-and-liquidation-risk
Handoff ID: FCLR-HANDOFF-20261104T183948Z | Priority: P0 - HEAVY WORK ENFORCED | Mode: CAMPAIGN-DRIVEN | Enforcement: NO-SKIP

## STATE SNAPSHOT (CURRENT VERIFIED)
- Tests: 164/164 pass (pytest). Working tree clean (pyc cleaned).
- Track C (FCLR-011) - FUNDING-CONDITIONED VOLATILITY: LOCKED. Gate PASSED, deeper validation + robustness complete on frozen splits. Independent recomputation confirms reproducibility (C2 vs B1 rel_imp ~+7.0%, CI excludes zero, monotonic funding-quartile effect). Final verdict: research_state/trackc_final_verdict_20261104T182830Z.md. Forward replication (FCLR-012-V) INCONCLUSIVE/blocked on data (Binance ends 2026-11-02, 0 non-overlapping 30d blocks). Overlay remains HYPOTHETICAL_ONLY.
- Track A (FCLR-010) - LIQUIDATION RISK: COMPLETE_SEALED, FORECAST_GATE_PASSED (Brier rel -2.21%, CI excl zero). ON TRIGGER ONLY - monitor for new ironflow >=2026-11.
- Track B: NOT_SUPPORTED.
- Bottlenecks eliminated: caches cleaned, no new schedulers/controllers/status-only files.

## PRIORITY ORDER (BY REPO NAME: Funding-conditioned-volatility-and-liquidation-risk)
1. **TRACK C - Funding-conditioned volatility** (COMPLETE/LOCKED). No further work on frozen splits.
2. **TRACK A - Liquidation risk** (HIGHEST ACTIVE). ON TRIGGER ONLY - monitor for new ironflow >=2026-11; preregister-before-outcomes strictly enforced.
3. **INFRA/BOTTLENECKS** - Maintain 164/164 green, efficient trigger monitoring.

## MANDATORY INITIAL MESSAGE FOR NEXT AGENT (COPY/PASTE - DO NOT EDIT)
```text
TASK ID: FCLR-NEXT-071-TRACK-A-TRIGGER-MONITOR
PRIORITY: P0 - HEAVY WORK ENFORCED (REPO-NAME PRIORITIZED: FUNDING-CONDITIONED VOLATILITY DONE; LIQUIDATION RISK NEXT)
CAMPAIGN: TRACK A TRIGGER MONITORING + READINESS (PREREGISTER BEFORE INSPECTION IF NEW DATA)
TIMESTAMP (UTC): 20261104T183948Z
OBJECTIVE: Track C is LOCKED complete on frozen splits. Focus on Track A (liquidation risk). Monitor for new admissible unauthenticated ironflow/liquidation data >=2026-11. If ANY new files appear (>=2026-11), PREREGISTER in research_state/fclr010_prereg_$(date -u +%Y%m%dT%H%M%SZ).json BEFORE inspecting outcomes with full hypothesis/frozen splits/metrics/stop rule, then run ONLY the frozen FCLR-010 harness (scripts/fclr010_execute.py or scripts/fclr010_harness.py) on existing sealed configuration. Do NOT merge sources, do NOT widen scope, do NOT re-tune on new data. If no new data, produce heavy trigger audit with concrete resume conditions.
CONSTRAINTS: No credentials, no manual files, no .github/workflows changes, no polling loops/schedulers/status-only files, no data fabrication, leakage-safe, preregister-before-outcomes strictly enforced. Track C remains LOCKED - no re-tuning on frozen splits.
MANDATORY EVERY SESSION (EXECUTE ALL, IN ORDER - NO SKIPPING):
  1) STATE SWEEP (HEAVY): Read RESEARCH_PROMPT.md, AGENT_HANDOFF.md, run_manifest.json, research_state/* (trackc_final_verdict_*, track_a_fclr010_consolidated.md, ironflow_probe_*, alt_source_deep_review_*), tests/, scripts/. Write research_state/campaign_sweep_tracka_$(date -u +%Y%m%dT%H%M%SZ).md (>=150 lines, concrete evidence).
  2) TRACK A TRIGGER PROBE (HEAVY): Run scripts/monitor_ironflow_liquidations.py --quick AND scripts/deep_review_alt_sources.py. Compare against last probes; list all files with mtime >=2026-11-01. If none: write research_state/tracka_trigger_audit_$(date -u +%Y%m%dT%H%M%SZ).md with ETag/cached_hits, last data_through, resume conditions, and explicit "NO NEW DATA - ON HOLD". If any: HALT inspection, write prereg FIRST (fclr010_prereg_*.json) with frozen splits/hypothesis/metrics/guardrails, then proceed only via frozen harness.
  3) TRACK C SANITY CHECK (LIGHT BUT VERIFIABLE): Quick confirmation Track C remains locked (read verdict) - no modifications. Ensure no accidental re-runs of sealed Track C codepaths.
  4) BOTTLENECK ELIMINATION (HEAVY): Clean __pycache__/pyc, ensure 164/164 green, remove any inefficiencies blocking trigger monitoring. No new controllers/schedulers/status-only files.
  5) ARTIFACT CONSOLIDATION (HEAVY): Update experiment_frontier/run_manifest if needed with evidence links. All actions produce verifiable artifacts.
STOP RULE: Complete all 5. Never stop early. If stuck, write blocker_evidence_$(date -u +%Y%m%dT%H%M%SZ).md with >=3 alternatives tried + concrete files/commands + single next action.
```

## NEXT FOCUS CAMPAIGN: LIQUIDATION_FORWARD_VALIDATE_HEAVY-004i
Campaign generated: 2026-11-02T12:48:00Z | Data state: blocked (ironflow data_through=2026-10, consecutive_absent=3, no post-2026-10 data)

Every session while data remains blocked MUST complete ALL of the following before ending:
  4A. STRENGTHEN AUTOMATION: Improve scripts/monitor_ironflow_liquidations.py (skip re-listing when tree ETag unchanged, wider/faster lookahead, smarter failure classification) AND/OR scripts/hunt_alternative_liquidation_sources.py. Add retry/backoff robustness, broader unauthenticated probes, new detection logic. Evidence: modified script + fresh probe output.
  4B. ADD TESTS: Extend tests/test_monitor_ironflow.py or add new tests covering state-diff, ETag caching, month-window, classification. All must pass: python -m unittest discover -s tests -v. Evidence: new test methods + green test run.
  4C. UPDATE BLOCKER DOC: Write research_state/liquidation_forward_validate_004_blocker_<new_timestamp>.md with complete probe tables (all URLs tried, status codes, headers, body previews), explicit checkable resume conditions (exact paths/patterns/URLs/months to watch), concrete timestamps. Evidence: new blocker doc file.
  4D. UPDATE FRONTIER: Update research_state/experiment_frontier.json with precise resume triggers and refreshed blocked-cell status. Evidence: modified frontier JSON.

NON-SKIPPABLE CHECKLIST (checked off in AGENT_HANDOFF.md at session end; unchecked = session FAILED):
- [ ] New evidence checked (ironflow_monitor_state.json read, new_files_found evaluated)
- [ ] Automation strengthened (monitor and/or hunt script improved)
- [ ] Tests added/extended (all pass: python -m unittest discover -s tests -v)
- [ ] Blocker doc updated (fresh timestamp, complete probe tables, resume conditions)
- [ ] Frontier updated (precise resume triggers, refreshed blocked-cell status)
- [ ] AGENT_HANDOFF.md updated with clear timestamped next task
- [ ] No sealed artifacts touched; no Track B/C conflation; no .github/workflows changes
- [ ] Raw data out of git; only code/manifests/reports committed

RESUME CONDITION (concrete, checkable - THE ONLY WAY TO UNBLOCK): Ironflow publishes data/events/YYYY-MM.parquet and/or data/fills/YYYY-MM.parquet for any month >= 2026-11 with HTTP 200 on unauthenticated GET (verify via scripts/monitor_ironflow_liquidations.py), OR a NEW admissible unauthenticated source passes strict GO rubric (>=5 symbols, >=1 complete month OR >=3 non-overlapping 30-day blocks, documented completeness/coverage, permissive license, unauthenticated access no keys/signed/requester-pays, schema compatible with frozen FCLR-010). Hyperliquid-only for Track A.

## Verification commands
- `python -m pytest tests/ -q` (164 passed)
- `python scripts/monitor_ironflow_liquidations.py --quick`
- `git status`

## Next Focus
- Maintain readiness for Track A trigger with strict preregistration discipline.
- Track C remains locked; forward replication blocked pending admissible new data.