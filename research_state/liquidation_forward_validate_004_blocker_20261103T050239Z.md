# Liquidation Forward Validate 004 — Blocker Evidence (HEAVY-WORK-REFRESH)
TIMESTAMP: $(date -u +%Y%m%dT%H%M%SZ)
CAMPAIGN: LIQUIDATION_FORWARD_VALIDATE_HEAVY-004i
STATE: BLOCKED_ON_DATA (STRUCTURAL)
SEALS: FCLR-010 PASSED; FCLR-008 NOT_MET; cross-track firewall enforced

## Summary
- Sole Track A source (ironflow/hyperliquid-liquidations) cached; forward edge 2026-11..2027-02 all 404.
- Consecutive absent >= 3 (data_through 2026-10). No resume trigger.
- All prior source families probed NO-GO (FCLR-NEXT-002 COMPLETE_NO-GO). Alt hunt this session scanned 12 REVIEW_REQUIRED; none confirmed GO.
- Tests 111/111 PASS. verify_heavy_work_004i.py ALL CHECKS PASSED.

## Commands Executed (evidence)
1. python scripts/monitor_ironflow_liquidations.py --verify -> ok=True, data_through=2026-10, consecutive_absent=3, content_hash_complete=True
2. python scripts/monitor_ironflow_liquidations.py --quick -> no resume trigger, probe_diff any_change=false
3. python scripts/monitor_ironflow_liquidations.py --decision -> new_data_path=false
4. python scripts/monitor_ironflow_liquidations.py --scan -> go=false, tree_not_modified=true
5. python scripts/hunt_alternative_liquidation_sources.py -> alt_source_scan_*.json + data_source_registry_alt_hunt.json written
6. python scripts/verify_heavy_work_004i.py -> ALL CHECKS PASSED
7. python -m unittest discover -s tests -v -> Ran 111 tests, OK

## Resume Conditions
1. Ironflow data/events or fills YYYY-MM >= 2026-11 returns 200
2. New admissible unauthenticated source passing rubric (>=5 symbols, >=1 complete month OR >=3 non-overlapping 30-day blocks, documented completeness/coverage, permissive license, no keys/signed/requester-pays, schema compatible with frozen FCLR-010)

## Next Actions (MANDATORY HEAVY WORK)
- Continue deep-verification of REVIEW_REQUIRED alt sources against rubric with concrete evidence.
- Keep automation/resumability hardened; no polling loops.
- Maintain tests green; update frontier/handoff on material changes.
