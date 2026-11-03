# AGENT_HANDOFF.md (SINGLE DURABLE SOURCE OF TRUTH)

**TIMESTAMP:** 20261103T031821Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**PRIORITY:** Track A liquidation forward-validation (IRONFLOW) — BLOCKED_ON_DATA; maximize heavy work, shrink bottlenecks, force campaign progress.
**CAMPAIGN:** LIQUIDATION_FORWARD_VALIDATE_HEAVY-004i — BLOCKED_ON_DATA (HEAVY-WORK-REFRESH-COMPLETE)
**SESSION GOAL FOR NEXT AGENT:** DO NOT COAST. No new data found (ironflow 2026-11+ absent; 17 alt candidates probed, 0 GO). MANDATORY HEAVY WORK A-F COMPLETED this session. Verify fresh artifacts and continue to shrink bottlenecks; if new data appears follow GO branch exactly.

## CLEAR INITIAL TASK (START NOW, IN ORDER)
1. `python scripts/monitor_ironflow_liquidations.py --verify`  (expect ok=True, data_through=2026-10, consecutive_absent>=3, baseline_drift=False, content_hash_baseline_complete=true)
2. `python scripts/monitor_ironflow_liquidations.py --quick`    (forward probe; capture evidence)
3. `python scripts/monitor_ironflow_liquidations.py --decision` (offline decision; expect new_data_path=false)
4. `python scripts/monitor_ironflow_liquidations.py --scan`     (fast resume scan; writes ironflow_resume_scan_*.json)
5. `python scripts/hunt_alternative_liquidation_sources.py`    (alt-hunt; writes alt_source_scan_*.json + data_source_registry_alt_hunt.json)
6. `python scripts/verify_heavy_work_004i.py`                 (non-skippable heavy-work gate; ALL CHECKS PASSED)
7. `python -m unittest discover -s tests -v`                 (expect ALL PASS)
8. Read latest `research_state/liquidation_forward_validate_004_blocker_*.md`, `research_state/experiment_frontier.json`, `research_state/data_source_registry_alt_hunt.json`, `research_state/alt_source_scan_*.json`.

## DECISION TREE (HARD RULES)
- **NEW DATA PATH (GO):** If probe-diff shows 404->200 for >=2026-11 OR tree_change.content_replaced non-empty OR new files for >=2026-11 → STOP blocked plan, pre-register BEFORE inspecting outcomes per `research_state/research_protocol_fclr010.md` v1.0, run `python scripts/fclr010_harness.py`, produce full evaluation, update frontier + cross-track log. NO tuning.
- **BLOCKED PATH (MANDATORY):** new_data_path=false → EXECUTE A–F IN FULL, ship >=1 NEW measurable artifact. Session with 0 new artifacts = failed.

## VERIFIED BASELINE (20261103T031821Z)
- Ironflow tree cached; forward edge 2026-11..2027-02 HEAD 404; tree ETag W/"2d38-AqkYNsWwxCKiOUmPgektdcJePJk" (304 not_modified); head_requests=8, get_requests=0, bytes_downloaded=0
- `--verify` ok=True, data_through=2026-10, consecutive_absent=3, baseline_drift=False, content_hash_complete=true (36/36)
- `--decision` new_data_path=false, probe_diff any_change=false (unchanged=8)
- `--scan` go=false, tree_change.changed=false, content_replaced=[], resume_trigger_met=false
- Tests: `python -m unittest discover -s tests -v` → 111/111 PASS
- Alt hunt COMPLETE_NO-GO (FCLR-NEXT-002). 17 additional candidates probed this session, 0 passed GO rubric. Sole reopen paths = ironflow >=2026-11 OR new admissible unauthenticated source passing rubric.
- Seals intact: FCLR-010 (PASSED), FCLR-008 (NOT_MET), cross-track firewall enforced.
- Heavy work executed this session (A-F): verify_heavy_work_004i.py gate PASSES, fresh blocker evidence, alt-hunt scans, frontier/handoff updated.

## MANDATORY HEAVY WORK (BLOCKED) — EXECUTE ALL
### A. AUTOMATION UPGRADE (>=1 concrete, measurable)
Harden monitor/hunt scripts: keep fast/resumable `--scan`, compact probe history with hashes/trends, actionable verify reasons.

### B. TESTS (MUST STAY GREEN)
Run `python -m unittest discover -s tests -v` until ALL PASS. Add focused tests if behavior changed.

### C. BLOCKER EVIDENCE (FRESH)
Write/update timestamped `research_state/liquidation_forward_validate_004_blocker_YYYYMMDDTHHMMSSZ.md` with commands+outputs, probe table, download accounting, timeline, resume conditions, evidence links.

### D. FRONTIER REFRESH
Update `research_state/experiment_frontier.json` rank 0.25 entry with new timestamp/artifacts/blockers/resume_triggers.

### E. CROSS-TRACK / DISCOVERY HARDENING
Run `hunt_alternative_liquidation_sources.py` producing timestamped `alt_source_scan_*.json` and update registry.

### F. HANDOFF UPDATE (THIS FILE)
Refresh timestamp + state + artifacts + acceptance criteria.

## ACCEPTANCE CRITERIA
- >=1 NEW measurable artifact
- `python -m unittest discover -s tests -v` ALL PASS
- `python scripts/verify_heavy_work_004i.py` ALL CHECKS PASSED
- No `.github/workflows/*` modified, no raw data committed
- FCLR-010/FCLR-008 seals preserved; Track separation enforced
- Handoff updated with concrete next command sequence

## RESUME CONDITIONS (EXACT)
1. Ironflow data/events or fills YYYY-MM >= 2026-11 returns 200
2. New admissible unauthenticated source passing rubric

## ARTIFACTS TO LEAVE BEHIND
- Fresh blocker doc (latest)
- Timestamped ironflow_resume_scan_*.json and updated probe history
- Timestamped alt_source_scan_*.json
- Updated experiment_frontier.json (rank 0.25)
- Updated this handoff

## NON-SKIPPABLE HEAVY-WORK CHECKLIST
The canonical checklist lives in `research_state/heavy_work_checklist_004i.md`. Every session while data remains blocked MUST complete ALL of: new evidence checked, automation strengthened, tests added/extended (all pass), blocker doc updated (fresh timestamp, complete probe tables, resume conditions), frontier updated (precise resume triggers, refreshed blocked-cell status), AGENT_HANDOFF.md updated with clear timestamped next task, no sealed artifacts touched, no Track B/C conflation, no .github/workflows changes, raw data out of git.

## BOTTLENECK REMOVAL (this session)
- Data bottleneck is STRUCTURAL, not operational: no post-2026-10 ironflow data exists (all 4 forward months 404); all 8 candidate source families previously probed NO-GO (FCLR-NEXT-002 COMPLETE_NO-GO); 17 additional candidates probed this session, 0 passed strict GO rubric. ironflow/hyperliquid-liquidations is the sole Track A source and remains blocked at >=2026-11.
- No polling loops, no re-probing dead routes, no .github/workflows changes, no raw data in git. Heavy work (automation, tests, blocker evidence, frontier, handoff) is the mandatory per-session path while blocked — no session may coast or wait on data without executing A-F.

## NEXT CAMPAIGN: FORWARD VALIDATION HOOK (when unblocked)
When resume trigger fires (ironflow >=2026-11 returns 200 OR new admissible source passes GO):
1. Pre-register BEFORE outcome inspection: `research_state/experiment_prereg_LIQUIDATION_FORWARD_VALIDATE_004_<timestamp>.json` (pre_registered_before_outcomes: true, frozen_before_outcomes: true, protocol `research_state/research_protocol_fclr010.md` v1.0, harness `scripts/fclr010_harness.py`, primary contrast C2_vs_B1, primary metric brier, bootstrap_reps 2000, rubric GO criteria).
2. Execute frozen harness: `python scripts/fclr010_harness.py` on new post-2026-10-31 data. Do NOT inspect outcomes before pre-registration exists.
3. Write evaluation summary: `research_state/evaluation_summary_LIQUIDATION_FORWARD_VALIDATE_004_<timestamp>.md` with calibration, LOO, concentration, block-bootstrap CIs (>=2000 reps), multiplicity (Holm), gate assessment.
4. Update frontier + commit evidence (code/manifests/reports — NOT raw data).
