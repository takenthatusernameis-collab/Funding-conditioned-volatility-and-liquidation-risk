# Liquidation Forward Validate 005 Blocker (FCLR-NEXT-079) - Step 5
Timestamp (UTC): 20261105T013124Z
Git SHA (HEAD): 012474144be8a963421f0eae52cb89d79f485d2a

## Full probe tables
### 1) Ironflow (Hyperliquid liquidations) - monitor_ironflow_liquidations.py --quick
Evidence: research_state/ironflow_probe_20261105T012638Z.json
- data_through: 2026-10
- forward edge probed: ['2026-11', '2026-12', '2027-01', '2027-02']
- head_probes: 8, cached_hits: 0
- probe_diff: added=0 changed=0 removed=0
- baseline_drift: intact=True regressions=0 content_replaced=0 pairs_checked=18 method=state_only_tree_unchanged
- kaggle_mirror: updated=False last=2026-11-01T06:18:48.21Z triggered=False
- Classification: ALL forward-edge CONFIRMED_ABSENT (404/HEAD-404 fast path). No resume trigger.

### 2) Alternative sources deep review
Evidence: research_state/alt_source_deep_review_20261105T012642Z.md (cache_hits=13 cache_misses=1). Consolidated latest.

### 3) Alternative sources hunt/scan
Evidence: research_state/alt_source_scan_20261105T012649Z.json (candidates=11, source=cache). Consolidated latest.

## ETag/cache state
- monitor uses tree ETag caching (304 fast path), per-file ETag/LM caching, HEAD-404 fast path, baseline-drift state-only skip on 304, forward-edge-only resume probe, fastpath cache. Consolidation added to reduce probe churn.
- hunt uses 24h HF search cache, 6h per-URL probe cache, URL dedup
- deep_review reuses hunt shared probe cache

## Exact checkable resume conditions (ONLY UNBLOCK)
1. ironflow data/events/YYYY-MM.parquet OR data/fills/YYYY-MM.parquet for ANY month >= 2026-11 returns HTTP 200 unauthenticated when probed by scripts/monitor_ironflow_liquidations.py (or equivalent unauthenticated probe). Check via monitor resume trigger.
2. OR new admissible unauthenticated source passes strict GO rubric:
- >=5 symbols
- >=1 complete month OR >=3x30d blocks
- documented coverage/completeness
- permissive license
- no keys/signed/requester-pays
- schema compatible with frozen FCLR-010 (Hyperliquid-only track for Track A)
If triggered: HALT inspection, PREREGISTER in research_state/fclr010_prereg_20261105T013124Z.json BEFORE inspecting outcomes (hypothesis/frozen splits/metrics/stop rule), run ONLY frozen FCLR-010 harness.

## Status
BLOCKED - no new data. On HOLD per Step 2. Bottlenecks removed/hardened. Tests green (180 passed).
