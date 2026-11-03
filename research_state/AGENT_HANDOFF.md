# AGENT_HANDOFF.md (SINGLE DURABLE SOURCE OF TRUTH)

**TIMESTAMP:** 20261103T070800Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**PRIORITY (by repo name):** LIQUIDATION REOPEN = MAXIMUM (Track A observed-liquidation labels blocked; H004 already SUPPORTED via FCLR-010 2025-11..2026-10 but forward edge blocked) | VOLATILITY H001 = INCONCLUSIVE (all confirmatory panels exhausted, overlay INELIGIBLE)

## SESSION GOAL
Remove/maintain Track A idle-wait. Ironflow forward months 2026-11,12,2027-01,02 all return 404 (consec_absent=3). No polling loops. Keep ironflow --quick as sole <1 min keep-alive.

## SESSION COMPLETED (20261103T070800Z)
- Phase 1: monitor_ironflow_liquidations.py --quick/--verify done. Tests 111/111 PASS.
- Phase 2: hunt_alternative_liquidation_sources.py refreshed. deep_review_alt_sources.py executed - all REVIEW_REQUIRED sources deep-reviewed with full rubric evidence.
- Result: NO NEW GO SOURCES FOUND. Fresh blocker evidence written.
- Artifacts: research_state/data_source_registry_alt_hunt.json, research_state/alt_source_scan_20261103T070646Z.json, research_state/alt_source_deep_review_20261103T070705Z.md, research_state/blocker_evidence_20261103T070800Z.md

## VERIFIED TRUTH
- Track A (observed): BLOCKED_ON_DATA (STRUCTURAL). FCLR-010 complete (2025-11..2026-10), gate PASSED, sealed. Forward 2026-11+ absent (404). Deep review of all alt sources found no admissible unauthenticated source passing full rubric.
- Track B: H001 INCONCLUSIVE, all confirmatory exhausted, overlay INELIGIBLE. Tests green.

## NEXT SESSION'S SINGLE HIGHEST-VALUE TASK
```bash
# < 1 min keep-alive only
python scripts/monitor_ironflow_liquidations.py --quick
python -m unittest discover -s tests -v | tail -2
# If resume trigger met (ironflow returns 200 for >=2026-11): pre-register fresh experiment ID, run frozen harness for Track A forward window, write evaluation_summary + gate assessment
# If still blocked: DO NOT poll. No other admissible unauthenticated liquidation source identified. Maintain evidence, stay idle on Track A, no heavy new searches without new leads.
```
**RESUME TRIGGERS:** Ironflow events/fills YYYY-MM >= 2026-11 return 200, OR new admissible unauthenticated source passes full FCLR rubric (>=5 symbols, >=1 complete month OR >=3 blocks, schema compatible with FCLR-010, unauthenticated only).
