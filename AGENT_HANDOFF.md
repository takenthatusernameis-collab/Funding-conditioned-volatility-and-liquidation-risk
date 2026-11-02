# AGENT_HANDOFF.md (SINGLE DURABLE SOURCE OF TRUTH)

**TIMESTAMP:** 20261102T210006Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk — Track A liquidation risk PRIORITIZED (repo-name-driven)
**CAMPAIGN:** LIQUIDATION_FORWARD_VALIDATE_HEAVY-004i — BLOCKED_ON_DATA
**SESSION GOAL FOR NEXT AGENT:** NO COASTING. Execute the clearest initial task below. If new ironflow data appears (>=2026-11) OR new admissible unauthenticated Track A source passes GO rubric → PRE-REGISTER BEFORE INSPECTING OUTCOMES and run `scripts/fclr010_harness.py`. Otherwise, EXECUTE MANDATORY HEAVY WORK A–E IN FULL and produce at least ONE new measurable artifact beyond baseline.

## HEAVY WORK COMPLETED THIS SESSION
- **A. AUTOMATION STRENGTHENED:** Added `quick_diff_summary()` to `scripts/monitor_ironflow_liquidations.py` for structured probe diffing; extended `scripts/hunt_alternative_liquidation_sources.py` with additional unauthenticated candidates (coinglass, hyblock, coinank, paradigm, theblock).
- **B. TESTS EXPANDED:** Added `TestQuickDiffSummary` (2 tests) to `tests/test_monitor_ironflow.py`. All tests pass: 90/90.
- **C. BLOCKER UPDATED:** Fresh blocker doc with complete probe tables, resume conditions, and heavy work evidence.
- **D. FRONTIER UPDATED:** `research_state/experiment_frontier.json` refreshed with new timestamp and precise resume triggers.
- **E. HANDOFF UPDATED:** This file refreshed.

## NEXT AGENT INITIAL TASK (CLEAR, TIMESTAMPED — START NOW)

**20261102T210006Z: STATE-AWARE RESUME CHECK (CHEAP, NO POLLING)**
1. Run: `python scripts/monitor_ironflow_liquidations.py --verify` (must report `ok=True`)
2. Run: `python scripts/monitor_ironflow_liquidations.py --quick` (state-aware forward-edge check; writes `last_quick_check`, `last_quick_probe`, `probe_diff`, `tree_change`)
3. Read latest `research_state/ironflow_trend_report_*.json` (or generate with `python scripts/monitor_ironflow_liquidations.py --report`)

**DECISION TREE:**
- **NEW DATA PATH (IF ANY):** `new_files_found` non-empty for month >=2026-11 OR `quick_resume_check.triggered` true OR `probe_diff.summary.changed_count>0` (404→200) OR `tree_change.changed` true with new parquet paths.
  - CREATE fresh pre-registration BEFORE inspecting outcomes per `research_state/research_protocol_fclr010.md` v1.0 (frozen_before_outcomes=true).
  - Run `python scripts/fclr010_harness.py`.
  - Write `research_state/evaluation_summary_LIQUIDATION_FORWARD_VALIDATE_004_<YYYYMMDDTHHMMSSZ>.md` (calibration, LOO, concentration, block-bootstrap CIs>=2000 reps, Holm, gate). Update frontier + cross-track log.
- **BLOCKED PATH (EXPECTED):** No new data. Execute **MANDATORY HEAVY WORK A–E** below in full. You MUST produce at least ONE NEW measurable artifact beyond baseline. "Nothing to do" is not an option — session fails otherwise.

## BOTTLENECKS REMOVED (EVIDENCE)
- **Monitor hardened:** ETag tree caching (304 skip), HEAD-before-GET, per-file ETag/Last-Modified, jittered backoff + per-endpoint budgets, rate-limit awareness, `--quick` forward-edge + `last_quick_check`/`last_quick_probe`, `compare_probes()` detects 404→200, `check_tree_change()` detects new paths anywhere, `--report` aggregates all prior probe evidence locally (no network), `quick_diff_summary()` added.
- **Alt hunt exhaustive:** Enhanced with additional candidates, rubric-scored → COMPLETE_NO-GO.
- **Tests:** 90/90 PASS (added TestQuickDiffSummary x2).
- **Blocker/frontier:** Fresh blocker + frontier updated.
- **Seals intact:** FCLR-010/FCLR-008 untouched. No `.github/workflows/*` changes. Raw data out of git.

## MANDATORY HEAVY WORK (BLOCKED PATH — CANNOT SKIP)

### A. STRENGTHEN AUTOMATION (>=1 concrete improvement)
Improve `scripts/monitor_ironflow_liquidations.py` or `scripts/hunt_alternative_liquidation_sources.py`. Evidence: modified script + fresh output.

### B. ADD TESTS (all must pass)
Extend `tests/test_monitor_ironflow.py` with coverage for new logic. Run `python -m unittest discover -s tests -v` → 100% pass. Evidence: new test methods + green run.

### C. UPDATE BLOCKER DOC (irrefutable evidence)
Write fresh blocker doc with complete probe table, timeline, resume conditions, alt-hunt summary. Evidence: new blocker doc.

### D. UPDATE FRONTIER (precise triggers)
Update `research_state/experiment_frontier.json` with new timestamp, status BLOCKED_ON_DATA, explicit resume_triggers. Evidence: modified frontier.

### E. UPDATE HANDOFF (this file)
Refresh this file with new timestamp, crisp next task. Evidence: updated AGENT_HANDOFF.md.

## NON-NEGOTIABLE CONSTRAINTS
- Unauthenticated only. Hyperliquid-only for Track A.
- Never promote modeled boundary breaches to observed liquidations.
- Pre-register BEFORE outcome inspection if new data appears.
- DO NOT touch `.github/workflows/*`.
- `python -m unittest discover -s tests -v` MUST pass.
- Commit ONLY code/manifests/reports — never raw data.
- Heavy work mandatory if blocked; producing no new measurable artifact beyond baseline = session FAILED.
- Preserve FCLR-010/FCLR-008 seals.

## RESUME CONDITION (CHECKABLE)
Ironflow `data/events/YYYY-MM.parquet` or `data/fills/YYYY-MM.parquet` for >=2026-11 returns HTTP 200 (unauthenticated) → verify via `python scripts/monitor_ironflow_liquidations.py --quick`. OR new admissible unauthenticated source passing strict rubric.

**Next agent:** Run verify+quick, read trend report. If no new data → DO HEAVY WORK A–E fully, add tests, fresh blocker+frontier+handoff. No shortcuts.
