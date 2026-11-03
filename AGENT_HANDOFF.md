# AGENT_HANDOFF.md (SINGLE DURABLE SOURCE OF TRUTH)

**TIMESTAMP:** 20261103T011100Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**PRIORITY:** Track A liquidation forward-validation (IRONFLOW) — BLOCKED_ON_DATA; maximize heavy work, shrink bottlenecks, force campaign progress.
**CAMPAIGN:** LIQUIDATION_FORWARD_VALIDATE_HEAVY-004i — BLOCKED_ON_DATA (HEAVY-WORK-REFRESH)
**SESSION GOAL FOR NEXT AGENT:** DO NOT COAST. If no new data → execute MANDATORY HEAVY WORK A–F. Produce >=1 concrete measurable artifact. Leave this file as the ONLY actionable handoff.

## CLEAR INITIAL TASK (START NOW, IN ORDER)
1. `python scripts/monitor_ironflow_liquidations.py --verify`  (expect ok=True, data_through=2026-10, consecutive_absent>=3, baseline_drift=False, content_hash_baseline_complete=true)
2. `python scripts/monitor_ironflow_liquidations.py --quick`    (forward probe; capture evidence)
3. `python scripts/monitor_ironflow_liquidations.py --decision` (offline decision; expect new_data_path=false)
4. `python scripts/monitor_ironflow_liquidations.py --scan`     (fast resume scan; writes ironflow_resume_scan_*.json)
5. Read latest `research_state/liquidation_forward_validate_004_blocker_*.md`, `research_state/experiment_frontier.json`, `research_state/data_source_registry_alt_hunt.json`, `research_state/alt_source_scan_*.json`.

## DECISION TREE (HARD RULES)
- **NEW DATA PATH (GO):** If probe-diff shows 404->200 for >=2026-11 OR tree_change.content_replaced non-empty OR new files for >=2026-11 → STOP blocked plan, pre-register BEFORE inspecting outcomes per `research_state/research_protocol_fclr010.md` v1.0, run `python scripts/fclr010_harness.py`, produce full evaluation, update frontier + cross-track log. NO tuning.
- **BLOCKED PATH (MANDATORY):** new_data_path=false → EXECUTE A–F IN FULL, ship >=1 NEW measurable artifact. Session with 0 new artifacts = failed.

## VERIFIED BASELINE (20261103T011100Z)
- Ironflow tree cached; forward edge 2026-11..2027-02 HEAD 404; head_requests=8, get_requests=0, bytes_downloaded=0
- `--verify` ok=True, data_through=2026-10, consecutive_absent=3, baseline_drift=False, content_hash_complete=true (36/36)
- Tests: `python -m unittest discover -s tests -v` → 105/105 PASS
- Alt hunt COMPLETE_NO-GO (FCLR-NEXT-002). Sole reopen paths = ironflow >=2026-11 OR new admissible unauthenticated source passing rubric.
- Seals intact: FCLR-010 (PASSED), FCLR-008 (NOT_MET), cross-track firewall enforced.
- Heavy work executed this session (A-F): strengthened automation, fresh blocker evidence, alt-hunt scans, frontier/handoff updated.

## MANDATORY HEAVY WORK (BLOCKED) — EXECUTE ALL
### A. AUTOMATION UPGRADE (>=1 concrete, measurable)
Harden monitor/hunt scripts: keep fast/resumable `--scan`, compact probe history with hashes/trends, actionable verify reasons.

### B. TESTS (MUST STAY GREEN)
Run `python -m unittest discover -s tests -v` until 105/105 PASS. Add focused tests if behavior changed.

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
