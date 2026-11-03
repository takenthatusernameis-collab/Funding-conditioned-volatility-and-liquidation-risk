# AGENT_HANDOFF.md (SINGLE DURABLE SOURCE OF TRUTH)

**TIMESTAMP:** 20261103T001200Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**PRIORITY:** Track A liquidation forward-validation (IRONFLOW) — BLOCKED_ON_DATA; maximize heavy work, shrink bottlenecks, force campaign progress.
**CAMPAIGN:** LIQUIDATION_FORWARD_VALIDATE_HEAVY-004i — BLOCKED_ON_DATA
**SESSION GOAL FOR NEXT AGENT:** DO NOT COAST. If no new data → execute MANDATORY HEAVY WORK A–F. Produce >=1 concrete measurable artifact. Leave this file as the ONLY actionable handoff.

## CLEAR INITIAL TASK (START NOW, IN ORDER)
1. `python scripts/monitor_ironflow_liquidations.py --verify`  (expect ok=True, data_through=2026-10, consecutive_absent>=3, baseline_drift=False, content_hash_baseline_complete=true)
2. `python scripts/monitor_ironflow_liquidations.py --quick`    (forward probe; confirm head_requests>=8, get_requests==0 on blocked path; capture evidence)
3. `python scripts/monitor_ironflow_liquidations.py --decision` (offline decision; expect new_data_path=false)
4. Read `research_state/liquidation_block_snapshot_*` (latest), latest `liquidation_forward_validate_004_blocker_*.md`, `research_state/experiment_frontier.json`, `research_state/data_source_registry_alt_hunt.json`. Do NOT inspect label outcomes.

## DECISION TREE (HARD RULES)
- **NEW DATA PATH (GO):** If `--quick`/`--decision` shows files for >=2026-11 OR probe_diff.changed_count>0 OR content replaced/new paths → **STOP** blocked plan, pre-register BEFORE inspecting outcomes per `research_state/research_protocol_fclr010.md` v1.0, run `python scripts/fclr010_harness.py`, produce full evaluation (calibration/LOO/concentration/block-bootstrap>=2000/Holm/gate), update frontier + cross-track log. NO tuning.
- **BLOCKED PATH (MANDATORY):** new_data_path=false → **EXECUTE A–F IN FULL**, ship >=1 NEW measurable artifact. Session with 0 new artifacts = failed.

## VERIFIED BASELINE (20261103T000629Z / latest)
- Ironflow tree 304, forward edge 2026-11..2027-02 all HEAD 404; head_requests=8, get_requests=0, get_requests_skipped=8, bytes_downloaded=0
- `--verify` ok=True, data_through=2026-10, consecutive_absent=3, baseline_drift=False, content_hash_baseline_complete=true (36/36 LFS oids)
- Tests: `python -m unittest discover -s tests -v` → 105/105 PASS
- Alt hunt COMPLETE_NO-GO (FCLR-NEXT-002). Sole reopen path = ironflow >=2026-11 OR new admissible unauthenticated source passing rubric.
- Seals intact: FCLR-010 (PASSED), FCLR-008 (NOT_MET), cross-track firewall enforced.

## BOTTLENECKS REMOVED (DO NOT REINTRODUCE)
- HEAD-404 fast path + download accounting (no wasted GETs on blocked edge)
- ETag tree caching, probe-diff, baseline drift, content-hash baseline (silent replacement detectable)
- Offline `--decision`/`--simulate` (no HF dependency to confirm block)
- Machine-readable state + snapshots

## MANDATORY HEAVY WORK (BLOCKED) — EXECUTE ALL
### A. AUTOMATION UPGRADE (>=1 concrete, measurable)
Strengthen `scripts/monitor_ironflow_liquidations.py` OR `scripts/hunt_alternative_liquidation_sources.py`:
- Add a **fast resume scan**: `--scan` that checks forward edge + tree in one pass, writes `research_state/ironflow_resume_scan_YYYYMMDDTHHMMSSZ.json` with `go: bool`, reasons, diff summary, timing.
- Add **probe history compaction**: keep last N probe evidence (default 10) in `ironflow_monitor_state.json` with hashes (prevents unbounded growth), surface `consecutive_absent` trend.
- Add **content-hash regression test coverage** if missing; ensure `verify_state` reports actionable reasons on failure.

### B. TESTS (MUST STAY GREEN)
Add >=1 focused test for new automation. Run `python -m unittest discover -s tests -v` until 105/105 PASS. Do not weaken assertions.

### C. BLOCKER EVIDENCE (FRESH)
Write/update timestamped `research_state/liquidation_forward_validate_004_blocker_YYYYMMDDTHHMMSSZ.md` with: verified commands+outputs summary, probe table, tree status, download accounting, timeline of consecutive_absent, resume conditions, explicit "why blocked", evidence links.

### D. FRONTIER REFRESH
Update `research_state/experiment_frontier.json` rank 0.25 entry with new timestamp, concrete artifacts, blockers, precise resume_triggers. Keep history.

### E. CROSS-TRACK / DISCOVERY HARDENING
Harden `hunt_alternative_liquidation_sources.py` with rubric enforcement + write `research_state/alt_source_scan_YYYYMMDDTHHMMSSZ.json` (even if NO-GO). Record per-candidate evidence (status/headers/body preview). Update `data_source_registry_alt_hunt.json` if new evidence.

### F. HANDOFF UPDATE (THIS FILE)
Refresh timestamp + "NEXT AGENT INITIAL TASK", verified state, artifacts produced, acceptance criteria. Leave crisp, unambiguous.

## ACCEPTANCE CRITERIA
- >=1 NEW measurable artifact (beyond snapshots/blocker refreshes that are routine) — e.g. new script behavior + evidence JSON
- `python -m unittest discover -s tests -v` ALL PASS
- No `.github/workflows/*` modified
- No raw data committed
- FCLR-010/FCLR-008 seals preserved; Track separation enforced
- Handoff updated with concrete next command sequence

## RESUME CONDITIONS (EXACT)
1. Ironflow `data/events/YYYY-MM.parquet` OR `data/fills/YYYY-MM.parquet` returns 200 for YYYY-MM >= 2026-11 (detect via `--quick` tree/probe-diff or `--decision`)
2. New admissible unauthenticated source passing rubric: >=5 symbols, >=3 non-overlapping 30-day blocks OR >=1 complete month, documented completeness/license, schema compatible with frozen FCLR-010

**ON TRIGGER:** Pre-register before outcomes; run `scripts/fclr010_harness.py`; full evaluation + gate. Update frontier/cross-track log.

## ARTIFACTS TO LEAVE BEHIND
- New evidence JSON(s) from A/E
- Fresh blocker doc (C)
- Updated frontier (D)
- Updated this handoff (F)
