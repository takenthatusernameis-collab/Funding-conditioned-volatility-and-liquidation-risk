# AGENT_HANDOFF.md (SINGLE DURABLE SOURCE OF TRUTH)

**TIMESTAMP:** 20261103T050300Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**PRIORITY:** Track A liquidation forward-validation (IRONFLOW) — BLOCKED_ON_DATA (STRUCTURAL); maximize heavy work, shrink bottlenecks, force campaign progress.
**CAMPAIGN:** LIQUIDATION_FORWARD_VALIDATE_HEAVY-004i — BLOCKED_ON_DATA (HEAVY-WORK-REFRESH-VERIFIED)

## SESSION GOAL FOR NEXT AGENT
DO NOT COAST. Data path structurally blocked: ironflow forward edge 2026-11..2027-02 all 404 (consecutive_absent>=3, data_through 2026-10). All 8 source families NO-GO (FCLR-NEXT-002); 17 additional probed, 0 passed GO rubric. 12 REVIEW_REQUIRED remain to deep-verify. MANDATORY HEAVY WORK A-F. If new data appears or a rubric-passing source confirmed -> follow GO branch per FCLR-010.

## CLEAR INITIAL TASK (START NOW)
1. `python scripts/monitor_ironflow_liquidations.py --verify`
2. `python scripts/monitor_ironflow_liquidations.py --quick`
3. `python scripts/monitor_ironflow_liquidations.py --decision`
4. `python scripts/monitor_ironflow_liquidations.py --scan`
5. `python scripts/hunt_alternative_liquidation_sources.py`
6. `python scripts/verify_heavy_work_004i.py`
7. `python -m unittest discover -s tests -v`
8. Read latest blocker doc, alt_source_scan_*.json, data_source_registry_alt_hunt.json, experiment_frontier.json

## VERIFIED BASELINE (20261103T050300Z)
- Ironflow cached; forward 2026-11..2027-02 404; ETag present; baseline intact
- --verify ok=True data_through=2026-10 consecutive_absent=3 content_hash_complete=True
- --decision new_data_path=false; --scan go=false
- Tests 111/111 PASS; verify_heavy_work_004i.py ALL CHECKS PASSED
- Alt hunt written; 12 REVIEW_REQUIRED need deep verification

## MANDATORY HEAVY WORK
A) Automation hardening (resumable/fast probes, compact history)
B) Tests remain green (add if behavior changes)
C) Fresh blocker evidence with commands/outputs
D) Frontier refreshed with resume triggers
E) Deep-verify REVIEW_REQUIRED against strict rubric
F) Update this handoff

## RESUME CONDITIONS
1. Ironflow YYYY-MM>=2026-11 returns 200
2. New admissible unauthenticated source passing rubric (>=5 symbols, >=1 complete month OR >=3 non-overlapping 30-day blocks, completeness/coverage/license OK, no keys/signed/requester-pays, schema compatible FCLR-010)

## ARTIFACTS TO LEAVE BEHIND
- Fresh blocker doc (latest)
- ironflow_resume_scan_*.json + probe history
- alt_source_scan_*.json + updated registry
- experiment_frontier.json updated
- This handoff updated
