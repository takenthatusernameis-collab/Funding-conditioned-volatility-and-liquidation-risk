# AGENT_HANDOFF.md (SINGLE DURABLE SOURCE OF TRUTH)

**TIMESTAMP:** 2026-11-02T20:54:44Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk — Track A liquidation risk PRIORITIZED (repo-name-driven)
**CAMPAIGN:** LIQUIDATION_FORWARD_VALIDATE_HEAVY-004i — BLOCKED_ON_DATA
**SESSION GOAL FOR NEXT AGENT:** NO COASTING. Execute the clearest initial task below. If new ironflow data appears (>=2026-11) OR new admissible unauthenticated Track A source passes GO rubric → PRE-REGISTER BEFORE INSPECTING OUTCOMES and run `scripts/fclr010_harness.py`. Otherwise, EXECUTE MANDATORY HEAVY WORK A–E IN FULL and produce at least ONE new measurable artifact beyond: `scripts/monitor_ironflow_liquidations.py` now has `--report` trend mode + `check_tree_change` + probe-diff + `last_quick_probe`; `ironflow_trend_report_20261102T195805Z.json`; `tests/test_monitor_ironflow.py` has TestTrendReport x4 + TestTreeChange x3 + TestCompareProbes x6; `run_manifest.json` fixed (valid JSON); blocker/frontier/handoff refreshed.

## NEXT AGENT INITIAL TASK (CLEAR, TIMESTAMPED — START NOW)

**2026-11-02T20:08:17Z: STATE-AWARE RESUME CHECK (CHEAP, NO POLLING)**
1. Run: `python scripts/monitor_ironflow_liquidations.py --verify` (must report `ok=True`)
2. Run: `python scripts/monitor_ironflow_liquidations.py --quick` (state-aware forward-edge check; writes `last_quick_check`, `last_quick_probe`, `probe_diff`, `tree_change`)
3. Read `research_state/ironflow_monitor_state.json`, `research_state/ironflow_trend_report_20261102T195805Z.json` (or latest `ironflow_trend_report_*.json`)

**DECISION TREE:**
- **NEW DATA PATH (IF ANY):** `new_files_found` non-empty for month >=2026-11 OR `quick_resume_check.triggered` true OR `probe_diff.summary.changed_count>0` (404→200) OR `tree_change.changed` true with new parquet paths.
  - CREATE fresh pre-registration BEFORE inspecting outcomes per `research_state/research_protocol_fclr010.md` v1.0 (frozen_before_outcomes=true).
  - Run `python scripts/fclr010_harness.py`.
  - Write `research_state/evaluation_summary_LIQUIDATION_FORWARD_VALIDATE_004_<YYYYMMDDTHHMMSSZ>.md` (calibration, LOO, concentration, block-bootstrap CIs>=2000 reps, Holm, gate). Update frontier + cross-track log.
- **BLOCKED PATH (EXPECTED):** No new data. Execute **MANDATORY HEAVY WORK A–E** below in full. You MUST produce at least ONE NEW measurable artifact beyond the baseline listed above. "Nothing to do" is not an option — session fails otherwise.

## BOTTLENECKS REMOVED (EVIDENCE)
- **Monitor hardened:** ETag tree caching (304 skip), HEAD-before-GET, per-file ETag/Last-Modified, jittered backoff + per-endpoint budgets, rate-limit awareness, `--quick` forward-edge + `last_quick_check`/`last_quick_probe`, `compare_probes()` detects 404→200, `check_tree_change()` detects new paths anywhere, `--report` aggregates all prior probe evidence locally (no network). Fresh trend: `ironflow_trend_report_20261102T195805Z.json` (65 runs, 0 triggered, streak 52).
- **Alt hunt exhaustive:** 12 families probed, rubric-scored → COMPLETE_NO-GO (`research_state/data_source_registry_alt_hunt.json`).
- **Tests:** 88/88 PASS (`python -m unittest discover -s tests -v`). Fixed 4 `test_fclr010_harness` errors (run_manifest.json was Git LFS pointer → rewritten as valid JSON).
- **Blocker/frontier:** Fresh blocker `research_state/liquidation_forward_validate_004_blocker_20261102T195818Z.md`, frontier refreshed `research_state/experiment_frontier.json` (2026-11-02T19:58:18Z context; update now).
- **Seals intact:** FCLR-010/FCLR-008 untouched. No `.github/workflows/*` changes. Raw data out of git.

## MANDATORY HEAVY WORK (BLOCKED PATH — CANNOT SKIP)

### A. STRENGTHEN AUTOMATION (>=1 concrete improvement)
Improve `scripts/monitor_ironflow_liquidations.py` or `scripts/hunt_alternative_liquidation_sources.py`. Ideas: better tree-change heuristics, richer `--quick` diff output, faster forward lookahead, tighter probe classification, or new unauthenticated probes with strict rubric filtering. Evidence: modified script + fresh output.

### B. ADD TESTS (all must pass)
Extend `tests/test_monitor_ironflow.py` with coverage for any new logic (e.g. new diff fields). Run `python -m unittest discover -s tests -v` → 100% pass. Evidence: new test methods + green run.

### C. UPDATE BLOCKER DOC (irrefutable evidence)
Write `research_state/liquidation_forward_validate_004_blocker_<YYYYMMDDTHHMMSSZ>.md` with complete probe table (URLs/methods/status/headers/body hashes), timeline of all probes, exact resume conditions, alt-hunt summary, verify command, trend report reference. Evidence: new blocker doc.

### D. UPDATE FRONTIER (precise triggers)
Update `research_state/experiment_frontier.json`: set `generated` to new timestamp, status `BLOCKED_ON_DATA`, explicit `resume_triggers` (ironflow >=2026-11 200 OR new source passing GO rubric), refreshed `blockers` with evidence refs. No Track B/C conflation. Evidence: modified frontier.

### E. UPDATE HANDOFF (this file)
Refresh this file with new timestamp, crisp next task, checked-off intent. Evidence: updated AGENT_HANDOFF.md.

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
Ironflow `data/events/YYYY-MM.parquet` or `data/fills/YYYY-MM.parquet` for >=2026-11 returns HTTP 200 (unauthenticated) → verify via `python scripts/monitor_ironflow_liquidations.py --quick`. OR new admissible unauthenticated source: >=5 symbols, >=1 complete month OR >=3 non-overlapping 30-day blocks, documented completeness/coverage/license OK, no keys/signed/requester-pays, schema compatible with frozen FCLR-010.

## MANDATORY READS
1. `AGENT_HANDOFF.md` (this file)
2. `research_state/heavy_work_checklist_004i.md`
3. `research_state/ironflow_monitor_state.json`
4. `research_state/ironflow_trend_report_20261102T195805Z.json`
5. Latest `research_state/liquidation_forward_validate_004_blocker_*.md`
6. `research_state/experiment_frontier.json`
7. `research_state/data_source_registry_alt_hunt.json`
8. `research_state/research_protocol_fclr010.md`
9. `scripts/monitor_ironflow_liquidations.py`, `scripts/hunt_alternative_liquidation_sources.py`

**Next agent:** Run verify+quick, read trend report. If no new data → DO HEAVY WORK A–E fully, add tests, fresh blocker+frontier+handoff. No shortcuts.
