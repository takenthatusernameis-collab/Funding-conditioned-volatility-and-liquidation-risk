# LIQUIDATION FORWARD VALIDATE 004 - BLOCKER (FRESH)
Timestamp (UTC): 20261104T232408Z
Git SHA: 754e74f69a63516ebfcae87c301fe76a563b792e
Campaign: FCLR-NEXT-078-TRACK-A-FORCE-BOTTLENECKS-REMOVE-HEAVY

## STATUS
TRACK A: BLOCKED ON DATA (ON TRIGGER/MONITOR ONLY)
Track C: LOCKED/COMPLETE
Track B: NOT_SUPPORTED

## IRONFLOW PROBE (FULL TABLES)
Latest probe: research_state/ironflow_probe_20261104T231731Z.json
- data_through: 2026-10
- probed months (forward edge): ['2026-11', '2026-12', '2027-01', '2027-02']
- head_probes: 8, cached_hits: 0
- probe_diff: added=0 changed=0 removed=0
- baseline_drift: intact=True regressions=0 content_replaced=0 pairs_checked=18 (method=state_only_tree_unchanged)
- kaggle_mirror: updated=False triggered=False
- NO NEW FILES >=2026-11 (events/fills)

URLs checked:
- Tree: https://huggingface.co/api/datasets/ironflow/hyperliquid-liquidations/tree/main?recursive=true (ETag cached)
- Events pattern: https://huggingface.co/datasets/ironflow/hyperliquid-liquidations/resolve/main/data/events/YYYY-MM.parquet
- Fills pattern: https://huggingface.co/datasets/ironflow/hyperliquid-liquidations/resolve/main/data/fills/YYYY-MM.parquet

## ALTERNATIVE SOURCES (FULL SCAN)
- Latest scan: research_state/alt_source_scan_20261104T232109Z.json
- Latest deep review: research_state/alt_source_deep_review_20261104T232118Z.md
- Shared URL cache in use (hunt+deep_review), cache_hits=13 on deep review
- Rubric: min_symbols>=5, >=1 complete month OR >=3x30d blocks, completeness doc, license ok, unauthenticated only, no requester-pays, schema compatible with FCLR-010, Hyperliquid-only for Track A
- Result: NO GO sources found. No admissible unauthenticated source passes strict rubric.

## EXACT CHECKABLE RESUME CONDITIONS (UNBLOCK ONLY)
1. Ironflow: data/events/YYYY-MM.parquet OR data/fills/YYYY-MM.parquet for ANY month >=2026-11 returns HTTP 200 unauthenticated (detected by monitor_ironflow_liquidations.py --quick/--verify). Triggers preregistration BEFORE outcome inspection.
2. OR new admissible unauthenticated source passes strict GO rubric (>=5 symbols, >=1 complete month OR >=3x30d blocks, documented coverage/completeness, permissive license, no keys/signed/requester-pays, schema compatible with frozen FCLR-010). Hyperliquid-only for Track A.

## BOTTLENECKS REMOVED (THIS SESSION)
- Consolidated alt_source_scan_*.json to 1 latest (removed 2 old)
- Consolidated alt_source_deep_review_*.md to 1 latest (removed 1 old)
- Consolidated campaign_sweep_tracka_*.md to 1 latest (removed 2 old)
- Scripts already hardened with caching/dedup/shared caches (verified in use)

## RECOMMENDATION
Remain in ON TRIGGER/MONITOR ONLY mode. Do NOT relax constraints. Track C remains LOCKED. On data appearance, HALT and preregister per FCLR-010 before inspecting outcomes.
