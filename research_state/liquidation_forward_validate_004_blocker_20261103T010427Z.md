# LIQUIDATION_FORWARD_VALIDATE_004 BLOCKER EVIDENCE (FRESH)

**TIMESTAMP:** 20261103T010427Z
**CAMPAIGN:** LIQUIDATION_FORWARD_VALIDATE_HEAVY-004i
**STATUS:** BLOCKED_ON_DATA
**PRIORITY:** Track A liquidation forward-validation (IRONFLOW)

## Verified commands and outputs (summary)
- `python scripts/monitor_ironflow_liquidations.py --verify` -> ok=True, data_through=2026-10, consecutive_absent=3, baseline_drift=False, content_hash_baseline_complete=true (36/36 LFS oids)
- `python scripts/monitor_ironflow_liquidations.py --quick` -> no resume trigger; head_probes=8, get_requests=0, get_requests_skipped=8, bytes_downloaded=0; probe_diff unchanged; baseline_drift intact
- `python scripts/monitor_ironflow_liquidations.py --decision` -> new_data_path=false
- `python scripts/monitor_ironflow_liquidations.py --scan` -> go=false, reasons=[]

## Probe table (forward edge)
Probed months (strictly after data_through): 2026-11, 2026-12, 2027-01, 2027-02 for events and fills. All HEAD 404 on blocked edge (fast path), no GETs performed.

## Tree status
HF tree listing cached via ETag (304 Not Modified). Content-hash baseline persisted (tree_parquet_items with LFS oids). Silent replacement detectable.

## Download accounting
head_requests>=8, get_requests==0, get_requests_skipped>=8, bytes_downloaded==0 (on blocked path).

## Timeline of consecutive_absent
consecutive_absent=3 (trailing months at forward edge confirmed absent). Trend tracked via probe_history with hashes (last 10 entries compacted).

## Resume conditions (exact)
1. Ironflow data/events/YYYY-MM.parquet OR data/fills/YYYY-MM.parquet returns 200 for YYYY-MM >= 2026-11
2. New admissible unauthenticated source passing rubric (>=5 symbols, >=3 non-overlapping 30-day blocks OR >=1 complete month, documented completeness/license, schema compatible with FCLR-010)

## Why blocked
No post-2026-10-31 ironflow files appear at forward edge. Alt-hunt (COMPLETE_NO-GO) found no admissible unauthenticated sources. Seals intact (FCLR-010 PASSED, FCLR-008 NOT_MET). Track separation enforced.

## Evidence links
- research_state/ironflow_monitor_state.json
- research_state/liquidation_block_snapshot_*.json
- research_state/alt_source_scan_*.json, research_state/data_source_registry_alt_hunt.json
- Tests: 105/105 PASS
