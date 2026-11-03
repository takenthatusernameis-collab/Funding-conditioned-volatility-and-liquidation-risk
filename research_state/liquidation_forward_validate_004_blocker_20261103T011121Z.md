# LIQUIDATION_FORWARD_VALIDATE_004 BLOCKER (FRESH)

TIMESTAMP: 20261103T011100Z
CAMPAIGN: LIQUIDATION_FORWARD_VALIDATE_HEAVY-004i
STATUS: BLOCKED_ON_DATA
PRIORITY: Track A liquidation forward-validation (IRONFLOW) — BLOCKED_ON_DATA; heavy work executed.

## Verified commands + outputs (summary)
- `python scripts/monitor_ironflow_liquidations.py --verify` → ok=True, data_through=2026-10, consecutive_absent=3, baseline_drift=False, content_hash_complete=true (36/36)
- `python scripts/monitor_ironflow_liquidations.py --quick` → No resume trigger. data_through=2026-10 probed=[2026-11,2026-12,2027-01,2027-02] head_probes=8 cached_hits=0 probe_diff unchanged; evidence ironflow_probe_20261103T010958Z.json
- `python scripts/monitor_ironflow_liquidations.py --decision` → offline decision; new_data_path=false; probe_diff all unchanged
- `python scripts/monitor_ironflow_liquidations.py --scan` → resume_check.triggered=false, get_requests=0, get_requests_skipped=8; writes ironflow_resume_scan_*.json

## Probe table (forward edge)
| month | kind | HEAD | GET (attempted/skipped) |
|-------|------|------|------------------------|
| 2026-11 | events/fills | 404 (cached) | 0 attempted, 2 skipped |
| 2026-12 | events/fills | 404 (cached) | 0 attempted, 2 skipped |
| 2027-01 | events/fills | 404 (cached) | 0 attempted, 2 skipped |
| 2027-02 | events/fills | 404 (cached) | 0 attempted, 2 skipped |
Total: head_probes=8, get_requests=0, bytes_downloaded=0

## Tree status
- Tree cached (ETag-based); forward edge 2026-11..2027-02 HEAD 404
- Baseline content hashes complete (36/36 LFS oids) — silent replacement detectable
- No tree changes / no content replacement detected

## Timeline of consecutive_absent
- Consecutive absent months beyond data_through=2026-10: 3 (2026-11, 2026-12, 2027-01) with 2027-02 also probed (HEAD 404). Streak remains >=3.

## Download accounting
- bytes_downloaded=0; get_requests_skipped=8 (HEAD-404 fast path active). No wasted bandwidth.

## Resume conditions (exact)
1. Ironflow data/events/YYYY-MM.parquet or data/fills/YYYY-MM.parquet returns 200 for YYYY-MM >= 2026-11 (detect via --quick/--decision/--scan/probe-diff)
2. New admissible unauthenticated source passing rubric: >=5 symbols, >=3 non-overlapping 30-day blocks OR >=1 complete month, documented completeness/license, schema compatible with FCLR-010

## Why blocked
No post-2026-10-31 ironflow data available at probed forward edge; all HEAD probes return 404 with cached hits; offline decision confirms no resume trigger. Alternative hunt (FCLR-NEXT-002) complete NO-GO — no new admissible unauthenticated source found. FCLR-010/FCLR-008 seals intact; Track separation enforced.

## Evidence links
- research_state/ironflow_probe_20261103T010958Z.json
- research_state/ironflow_resume_scan_*.json (latest from --scan)
- research_state/ironflow_monitor_state.json (probe history, trends, hashes)
- research_state/alt_source_scan_20261103T011046Z.json
- research_state/data_source_registry_alt_hunt.json
- AGENT_HANDOFF.md (updated)
