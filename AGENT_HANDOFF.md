# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF)
Timestamp (UTC): 20261104T203124Z
Git SHA (HEAD): 346e063b
Branch: main
Repo: Funding-conditioned-volatility-and-liquidation-risk
Handoff ID: FCLR-HANDOFF-20261104T203124Z | Priority: P0 - HEAVY WORK ENFORCED | Mode: CAMPAIGN-DRIVEN | Enforcement: NO-SKIP

## STATE SNAPSHOT (CURRENT VERIFIED)
- Tests: 166/166 pass (pytest/unittest). Working tree clean except untracked research probe artifacts (ironflow_probe_*.json, leave in place). __pycache__/*.pyc cleaned from git index and disk.
- Track C (FCLR-011) - FUNDING-CONDITIONED VOLATILITY: LOCKED. Gate PASSED, deeper validation + robustness complete on frozen splits. Independent recomputation confirms reproducibility (C2 vs B1 rel_imp ~+7.0%, CI excludes zero, monotonic funding-quartile effect). Final verdict: research_state/trackc_final_verdict_20261104T182830Z.md. Forward replication (FCLR-012-V) INCONCLUSIVE/blocked on data. Overlay remains HYPOTHETICAL_ONLY.
- Track A (FCLR-010) - LIQUIDATION RISK: SEALED/PASSED on frozen config. ON TRIGGER ONLY - monitor for new admissible unauthenticated ironflow/liquidation data >=2026-11. Strict preregister-before-outcomes enforced.
- Track B: NOT_SUPPORTED.
- Bottlenecks: Monitor/hunt hardened (ETag/TTL caching, extended candidates). Still blocked on external data availability.

## PRIORITY ORDER (BY REPO NAME: Funding-conditioned-volatility-and-liquidation-risk)
1. **TRACK C - Funding-conditioned volatility** (COMPLETE/LOCKED). No further work on frozen splits. Sanity-check only.
2. **TRACK A - Liquidation risk** (HIGHEST ACTIVE/BLOCKED). ON TRIGGER ONLY. Every session MUST produce heavy detection/hardening artifacts while blocked.
3. **INFRA/BOTTLENECKS** - Maintain green tests, eliminate inefficiencies, harden automation without creating schedulers/controllers/status-only files.

## MANDATORY INITIAL MESSAGE FOR NEXT AGENT (COPY/PASTE - DO NOT EDIT)
```text
TASK ID: FCLR-NEXT-073-TRACK-A-TRIGGER-HARDEN-004i-FORCE-HEAVY
PRIORITY: P0 - HEAVY WORK ENFORCED (REPO-NAME PRIORITIZED: FUNDING-CONDITIONED VOLATILITY DONE; LIQUIDATION RISK BLOCKED -> FORCE HEAVY HARDENING)
CAMPAIGN: TRACK A TRIGGER DETECTION HARDENING + PREREG DISCIPLINE (BLOCKED-DATA MODE)
TIMESTAMP (UTC): 20261104T203124Z
OBJECTIVE: Track C is LOCKED complete on frozen splits. Focus on Track A (liquidation risk). Data is blocked (ironflow data_through=2026-10, no >=2026-11 observed). You CANNOT stop for "no data" - you MUST harden detection, expand alternative sources, add tests, and produce verifiable blocker/frontier evidence every session. If ANY new admissible unauthenticated ironflow/liquidation data >=2026-11 appears OR a rubric-GO alternative source is found -> HALT inspection, PREREGISTER in research_state/fclr010_prereg_$(date -u +%Y%m%dT%H%M%SZ).json BEFORE inspecting outcomes with full hypothesis/frozen splits/metrics/stop rule, then run ONLY the frozen FCLR-010 harness (scripts/fclr010_execute.py or scripts/fclr010_harness.py) on existing sealed configuration. Do NOT merge sources, do NOT widen scope, do NOT re-tune on new data.
CONSTRAINTS: No credentials, no manual files, no .github/workflows changes, no polling loops/schedulers/status-only files, no data fabrication, leakage-safe, preregister-before-outcomes strictly enforced. Track C remains LOCKED - no re-tuning on frozen splits. Raw data out of git; only code/manifests/reports committed.
MANDATORY EVERY SESSION (EXECUTE ALL, IN ORDER - NO SKIPPING):
  1) STATE SWEEP (HEAVY): Read RESEARCH_PROMPT.md, AGENT_HANDOFF.md, experiment_frontier.json, research_state/liquidation_forward_validate_004_blocker_* (latest), research_state/tracka_trigger_audit_*, research_state/*tracka*, tests/, scripts/. Write research_state/campaign_sweep_tracka_$(date -u +%Y%m%dT%H%M%SZ).md (>=200 lines, concrete evidence, diff vs previous sweep).
  2) TRIGGER PROBE (HEAVY): Run scripts/monitor_ironflow_liquidations.py --quick AND scripts/deep_review_alt_sources.py AND scripts/hunt_alternative_liquidation_sources.py. Compare against last probes; list ALL files/paths checked with mtimes >=2026-10-01. If any >=2026-11: HALT, prereg FIRST, then frozen harness only. If none: document explicitly "NO NEW DATA - ON HOLD" with full probe tables.
  3) BOTTLENECK REMOVAL (HEAVY): Identify and fix at least one concrete inefficiency (caching/dedup/classification/retries/timeouts/lookahead). Prefer strengthening scripts/monitor_ironflow_liquidations.py and/or scripts/hunt_alternative_liquidation_sources.py. Evidence: diff + before/after timing/behavior.
  4) TEST HARDENING (HEAVY): Add/extend tests in tests/test_monitor_ironflow.py (or new targeted tests). Cover state-diff, ETag/TTL, month-windowing, candidate classification, failure modes. Run: python -m pytest tests/ -q OR python -m unittest discover -s tests -v. Must stay >=166 passing.
  5) BLOCKER + FRONTIER UPDATE (HEAVY): Write fresh research_state/liquidation_forward_validate_004_blocker_$(date -u +%Y%m%dT%H%M%SZ).md with complete probe tables (URLs, methods, status, headers, body previews), ETag/cached hits, exact checkable resume conditions (paths/patterns/URLs/months), >=3 concrete next actions. Update experiment_frontier.json with precise resume triggers, last_checked timestamp, refreshed blocked-cell status. Update AGENT_HANDOFF.md with timestamped next task.
STOP RULE: Complete all 5. Never stop early. If stuck, write blocker_evidence_$(date -u +%Y%m%dT%H%M%SZ).md with >=3 alternatives tried + concrete files/commands + single next action. Track C remains LOCKED.
```

## NEXT FOCUS CAMPAIGN: LIQUIDATION_TRIGGER_HARDEN_FORCE_HEAVY-005 (NON-SKIPPABLE, HEAVY WORK)
Campaign regenerated: 2026-11-04T200000Z | Data state: blocked (ironflow data_through=2026-10, consecutive_absent>=4). Future agents CANNOT avoid heavy work while blocked.

Every session while data remains blocked MUST complete ALL of the following before ending. Unchecked = session FAILED.

- [ ] State sweep written (>=200 lines, diff vs prior sweep)
- [ ] Trigger probe run (monitor quick + deep_review_alt_sources + hunt_alternative_liquidation_sources), full tables in blocker
- [ ] Bottleneck removed (concrete script improvement with evidence)
- [ ] Tests added/extended and all pass (>=166)
- [ ] Fresh blocker doc written with complete probe tables + checkable resume conditions
- [ ] experiment_frontier.json updated with precise resume triggers + last_checked
- [ ] AGENT_HANDOFF.md updated with clear timestamped next task
- [ ] No sealed artifacts touched (Track C locked); no Track B/C conflation; no .github/workflows changes
- [ ] Raw data out of git; only code/manifests/reports committed

## RESUME CONDITION (concrete, checkable - THE ONLY WAY TO UNBLOCK)
Ironflow publishes data/events/YYYY-MM.parquet and/or data/fills/YYYY-MM.parquet for any month >= 2026-11 with HTTP 200 on unauthenticated GET (verify via scripts/monitor_ironflow_liquidations.py), OR a NEW admissible unauthenticated source passes strict GO rubric (>=5 symbols, >=1 complete month OR >=3 non-overlapping 30-day blocks, documented completeness/coverage, permissive license, unauthenticated access no keys/signed/requester-pays, schema compatible with frozen FCLR-010). Hyperliquid-only for Track A.

## Verification commands
- `python -m pytest tests/ -q` (166 passed)
- `python -m unittest discover -s tests -v`
- `python scripts/monitor_ironflow_liquidations.py --quick`
- `python scripts/hunt_alternative_liquidation_sources.py`
- `git status`

## SESSION UPDATE (20261104T203124Z) - FCLR-NEXT-073 CAMPAIGN LOADED (FORCE HEAVY)
- Handoff regenerated to enforce heavy work while Track A blocked. Track C remains LOCKED.
- Priority locked by repo name: Funding-conditioned volatility complete -> Liquidation risk next (blocked).
- Bottleneck removal + test hardening + fresh blocker/frontier updates are mandatory every session.

### NEXT TASK (COPY/PASTE FOR NEXT AGENT)
```text
TASK ID: FCLR-NEXT-073-TRACK-A-TRIGGER-HARDEN-004i-FORCE-HEAVY
PRIORITY: P0 - HEAVY WORK ENFORCED
TIMESTAMP (UTC): 20261104T203124Z
OBJECTIVE: Track C LOCKED. Track A ON TRIGGER ONLY (ironflow 2026-10 latest, no 2026-11+). Blocked-data mode: CANNOT stop for absence of data - MUST harden detection (monitor/hunt), remove bottlenecks, extend tests, write fresh blocker+frontier. If ANY >=2026-11 ironflow appears OR rubric-GO alternative found -> HALT, PREREGISTER in research_state/fclr010_prereg_*.json BEFORE inspection, run ONLY frozen FCLR-010 harness. Never re-tune sealed tracks.
MANDATORY: 1) State sweep >=200 lines (diff) 2) Run monitor quick + deep_review_alt_sources + hunt_alternative_liquidation_sources with full tables 3) Concrete bottleneck removal in scripts 4) Add/extend tests, all green 5) Fresh blocker doc + frontier update + handoff update. Stop only after all artifacts written. No .github/workflows changes.
RESUME: ironflow data/events/YYYY-MM.parquet or data/fills/YYYY-MM.parquet >=2026-11 unauthenticated 200, OR rubric-GO alternative.
```
