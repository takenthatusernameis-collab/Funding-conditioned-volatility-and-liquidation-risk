# Liquidation Forward Validate Blocker 004 (20261104T233200Z)

Timestamp: 20261104T233200Z
Git SHA: f15adc3f
Track: A (liquidation risk) - BLOCKED on data
Campaign: FCLR-NEXT-078

## Latest probe evidence
- ironflow_probe_20261104T233118Z.json (from monitor_ironflow_liquidations.py --quick)
  - tree_url: https://huggingface.co/api/datasets/ironflow/hyperliquid-liquidations/tree/main?recursive=true (ETag W/"2d38-..." recorded)
  - data_through: 2026-10 (events/fills present through 2026-10)
  - quick_resume_check months_probed: [2026-11, 2026-12, 2027-01, 2027-02]
  - all HEAD/GET probes: 404 (CONFIRMED_ABSENT)
  - probe_diff: added=0 changed=0 removed=0
  - baseline_drift: intact=True, method=state_only_tree_unchanged (tree unchanged relative to cached state)
  - kaggle_mirror: not triggered

## Alternative sources
- alt_source_scan_20261104T233120Z.json / alt_source_deep_review_20261104T233119Z.md (consolidated to latest)
- No rubric-GO unauthenticated source found. Ironflow/hyperliquid-liquidations remains the only admissible path identified.

## Exact checkable resume conditions
Resume Track A forward (FCLR-010) ONLY if ANY of:
1. ironflow data/events/YYYY-MM.parquet or data/fills/YYYY-MM.parquet for month >= 2026-11 returns HTTP 200 unauthenticated (HEAD or GET succeeds). Monitor will detect via tree change + forward probe.
2. New admissible unauthenticated source passes strict GO rubric:
- unauthenticated + no keys
- >=5 symbols
- >=1 complete month OR >=3x30d blocks
- documented coverage/completeness
- permissive license
- schema compatible with frozen FCLR-010 (observed liquidation events/fills, not modeled)
- Hyperliquid-only constraint remains if we must stay consistent with frozen FCLR-010 firewall; do NOT merge with Binance panels.

## Bottlenecks addressed this session
- Consolidated alt_source_scan/deep_review to single latest (added auto-consolidation in hunt/deep_review)
- Verified monitor/deep_review/hunt hardened with caches/ETags/HEAD-fast-path
- No redundant status-only files/schedulers/pollers/wrappers added

## Next action
While blocked, continue bottleneck removal and hardening. Do not guess. Preregister BEFORE inspecting outcomes if resume condition met.
