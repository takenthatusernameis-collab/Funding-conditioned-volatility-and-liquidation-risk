# Campaign Sweep Track A — FCLR-NEXT-084 Baseline Metrics
Timestamp (UTC): 2026-11-05T04:26:00Z
Git HEAD: e5f060f9de9cf22190c2c65942b459c4a68aebb3

## Baseline artifact metrics (before FCLR-NEXT-084 work)

| Metric | Value |
|---|---|
| ironflow_probe_*.json (live probes) | 13 |
| ironflow_probe_digest_*.json (archived) | 12 |
| ironflow_trend_report_*.json | 4 |
| ironflow_scan_*.json | 3 |
| campaign_sweep_tracka_*.md | 9 |
| liquidation_forward_validate_*blocker*.md | 6 |
| total research_state files | 34,694 |
| research_state total size | 545 MB |
| research_state/data_cache size | 483 MB |
| research_state/data_cache file count | 34,427 |
| non-data_cache research_state file count | 267 |
| url_probe_cache.json size | 97,956 bytes |
| hf_search_cache.json size | 2,061 bytes |
| ironflow_monitor_state.json size | 72 KB |
| cached_inputs_hashes.json size | 3.4 MB |
| run_manifest_FCLR002.json size | 1.5 MB |
| run_manifest.json.bak_fclr001 size | 1.5 MB |

## Bottleneck target
- Reduce ironflow_probe_*.json count by >=40% from 13 (target <=7, ideally 1-2 after consolidation).
- Reduce research_state non-data_cache file count measurably.
- Unify URL probe caches so hunt/deep_review/monitor share one cache (already partially done; enforce).
- Reduce per-session --quick wall time.

## Notes
- data_cache (483 MB, 34,427 files) is raw downloaded data — must stay out of git and is NOT a bottleneck target (it is required frozen baseline panel).
- Artifact churn is in the non-data_cache layer: probe/digest/trend/report files.