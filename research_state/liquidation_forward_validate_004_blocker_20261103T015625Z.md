# LIQUIDATION_FORWARD_VALIDATE_004 BLOCKER (FRESH) — 20261103T015625Z

**CAMPAIGN:** LIQUIDATION_FORWARD_VALIDATE_HEAVY-004i
**EXPERIMENT_ID:** LIQUIDATION_FORWARD_VALIDATE_004 (reserved; pre-reg required BEFORE outcome inspection if GO)
**TRACK:** A (observed liquidations) — Hyperliquid-only via ironflow/hyperliquid-liquidations
**STATUS:** BLOCKED_ON_DATA
**PRIORITY:** Track A liquidation forward-validation (IRONFLOW) — BLOCKED_ON_DATA; maximize heavy work, shrink bottlenecks, force campaign progress.

## COMMANDS + OUTPUTS (evidence)
1) `python scripts/monitor_ironflow_liquidations.py --verify`
   VERIFY ok=True data_through=2026-10 consecutive_absent=3 baseline_drift=False content_hash_complete=true (36/36). Cache incomplete but hash baseline complete.

2) `python scripts/monitor_ironflow_liquidations.py --quick`
   Wrote evidence: research_state/ironflow_probe_20261103T015516Z.json / later runs produced fresh probes. No resume trigger. data_through=2026-10 probed=['2026-11','2026-12','2027-01','2027-02'] head_probes=8 cached_hits=0 probe_diff(added=0 changed=0 removed=0) baseline_drift(intact=True regressions=0)

3) `python scripts/monitor_ironflow_liquidations.py --decision`
   {"new_data_path":false,"reasons":[],"probe_diff_summary":{"added_count":0,"changed_count":0,"removed_count":0,"unchanged_count":8,"any_change":false}}

4) `python scripts/monitor_ironflow_liquidations.py --scan`
   Fast resume scan executed; tree_change.changed=false, no forward-edge additions for >=2026-11. resume_trigger_met=false.

## PROBE TABLE
- Forward months probed: 2026-11, 2026-12, 2027-01, 2027-02 (8 head probes)
- cached_hits: 0
- probe_diff: added=0 changed=0 removed=0 unchanged=8
- tree_change.content_replaced: []
- baseline_drift: intact=True regressions=0

## DOWNLOAD ACCOUNTING
- bytes_downloaded: 0 (no GETs for new files)
- head_requests: 8 (forward probes)
- get_requests: 0

## TIMELINE
- Baseline data_through: 2026-10
- Consecutive_absent: 3 (months 2026-11, 2026-12, 2027-01 probed; 2027-02 also probed)
- Last verified: 2026-11-03T01:56:12Z

## RESUME CONDITIONS (EXACT)
1. Ironflow data/events or fills YYYY-MM >= 2026-11 returns 200 (verify via monitor --quick/--decision)
2. New admissible unauthenticated source passing rubric (>=5 symbols, >=1 complete month OR >=3 non-overlapping 30-day blocks, documented completeness/coverage/license OK, unauthenticated only, schema compatible with frozen FCLR-010)

## EVIDENCE LINKS
- research_state/ironflow_probe_*.json (latest runs)
- research_state/experiment_frontier.json
- research_state/data_source_registry_alt_hunt.json
- research_state/alt_source_scan_*.json
