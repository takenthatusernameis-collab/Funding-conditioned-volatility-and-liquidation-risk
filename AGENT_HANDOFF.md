# AGENT_HANDOFF.md (SINGLE DURABLE SOURCE OF TRUTH)

**TIMESTAMP:** 20261102T230440Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk — Track A liquidation risk PRIORITIZED
**CAMPAIGN:** LIQUIDATION_FORWARD_VALIDATE_HEAVY-004i — BLOCKED_ON_DATA (IRONFLOW)
**SESSION GOAL FOR NEXT AGENT:** DO NOT COAST. Blocked path → MANDATORY HEAVY WORK A–E. Produce >=1 new measurable artifact or session fails.

## NEXT AGENT INITIAL TASK (CLEAR, TIMESTAMPED — START NOW)
1. `python scripts/monitor_ironflow_liquidations.py --verify` (expect ok=True, data_through=2026-10, consecutive_absent=3, baseline_drift=False)
2. `python scripts/monitor_ironflow_liquidations.py --quick` (forward edge check; confirm get_requests_skipped=8, get_requests=0, bytes_downloaded=0 on the blocked path)
3. `python scripts/monitor_ironflow_liquidations.py --decision` (offline decision tree; expect new_data_path=false)
4. Read latest `research_state/ironflow_trend_report_*.json` + latest blocker doc + `research_state/liquidation_block_snapshot_*.json`

## DECISION TREE
- **NEW DATA PATH:** If `--quick`/`--decision` shows new files for >=2026-11 OR probe_diff changed_count>0 OR tree_change has forward-edge added paths → pre-register BEFORE outcomes per `research_state/research_protocol_fclr010.md` v1.0, run `python scripts/fclr010_harness.py`, full evaluation + gate. Update frontier+cross-track.
- **BLOCKED PATH (MANDATORY):** No new data → EXECUTE A–E IN FULL, >=1 new measurable artifact. Session without a new artifact is a failed session.

## VERIFIED STATE (20261102T230440Z)
- `--verify` ok=True, data_through=2026-10, consecutive_absent=3, baseline_drift=False
- `--quick` probed ['2026-11','2026-12','2027-01','2027-02'] all 404, tree 304, no changes; accounting: head_requests=8, get_requests=0, get_requests_skipped=8, bytes_downloaded=0
- `--decision` new_data_path=false
- `python -m unittest discover -s tests -v` 105/105 PASS
- Alt hunt COMPLETE_NO-GO. Seals FCLR-010/FCLR-008 intact. No workflow changes.

## BOTTLENECKS REMOVED
- Offline `--decision` and `--simulate` modes (no HF dependency for block confirmation)
- ETag tree caching, HEAD-before-GET, probe-diff, baseline drift checks
- Machine-readable state persistence (last_quick_check/last_quick_probe/last_tree_change)
- `write_blocker_snapshot()` + `--snapshot` producing timestamped `liquidation_block_snapshot_*.json` (offline)
- **NEW:** HEAD-404 fast path (`probe_month` + `check_resume_condition`): HEAD 404 is definitive CONFIRMED_ABSENT, skips the wasteful GET body download; per-session download accounting persisted in `--quick` evidence (head_requests/get_requests/get_requests_skipped/bytes_downloaded). Removes the per-session wasted-download bottleneck on the blocked forward edge.

## MANDATORY HEAVY WORK (BLOCKED)
### A. STRENGTHEN AUTOMATION (>=1 concrete improvement)
Improve `scripts/monitor_ironflow_liquidations.py` or `scripts/hunt_alternative_liquidation_sources.py`. Add measurable capability + evidence (this session: HEAD-404 fast path + download accounting).
### B. ADD TESTS
Extend tests for new logic; `python -m unittest discover -s tests -v` must pass 100%.
### C. UPDATE BLOCKER DOC
Create/update fresh timestamped blocker under `research_state/` with probe table, timeline, resume conditions, evidence.
### D. UPDATE FRONTIER
Update `research_state/experiment_frontier.json` with timestamp/status/BLOCKED_ON_DATA + precise resume_triggers.
### E. UPDATE HANDOFF (this file)
Refresh timestamp + crisp next task.

## ACCEPTANCE CRITERIA
- >=1 NEW measurable artifact beyond baseline
- All tests pass
- No `.github/workflows/*` modified
- No raw data committed
- FCLR-010/FCLR-008 seals preserved
- Track separation enforced

## RESUME CONDITIONS
1. Ironflow >=2026-11 events/fills returns 200 → verify via `--quick`/`--decision`/`--simulate`
2. New admissible unauthenticated source passing rubric (>=5 symbols, >=1 month or >=3x30d blocks, schema compatible with FCLR-010)

**ON TRIGGER:** Pre-register before inspecting outcomes; run `fclr010_harness.py`; write full evaluation with calibration/LOO/concentration/block-bootstrap CIs>=2000/Holm/gate.
