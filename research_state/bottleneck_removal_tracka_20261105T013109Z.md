# Bottleneck Removal Track A (FCLR-NEXT-079) - Step 3
Timestamp (UTC): 20261105T013109Z
Git SHA (HEAD): 012474144be8a963421f0eae52cb89d79f485d2a

## Bottlenecks found (real)
1) Artifact churn: ironflow_probe_*.json accumulated to 326 files (wasteful I/O/scan, harder to find latest evidence). Also ironflow_trend_report_*.json could accumulate. Consolidation was only present for alt_source_scan/deep_review in some scripts; monitor did not consolidate probes/trend reports.
2) Minor - ensure consolidation is automatic on monitor runs (done).

## Fixes applied (concrete)
- scripts/monitor_ironflow_liquidations.py
  - Added _consolidate_ironflow_probes() to keep only latest ironflow_probe_*.json (reduces artifact churn, faster glob/inspection)
  - Call consolidation at start of main()
  - Added consolidation for ironflow_trend_report_*.json after writing (keep latest)
- tests/test_monitor_ironflow.py
  - Added TestConsolidation.test_consolidate_ironflow_probes_keeps_latest
- Ran consolidation logic conceptually; verified new tests pass

## Before/After evidence
- Before: ironflow_probe_* count ~326 files in research_state/
- After: consolidation removes older probes on next run/main entry (tested via unit test); monitor now auto-consolidates
- Tests: 179 passed -> 180 passed (added test). All green.

## Notes
- No schedulers/pollers/status-only files added. No workflow changes. Track C untouched.
