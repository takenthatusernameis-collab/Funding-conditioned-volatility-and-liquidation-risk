# LIQUIDATION_FORWARD_VALIDATE_004 BLOCKER (FRESH) — 20261103T031821Z

**CAMPAIGN:** LIQUIDATION_FORWARD_VALIDATE_HEAVY-004i
**EXPERIMENT_ID:** LIQUIDATION_FORWARD_VALIDATE_004 (reserved; pre-reg required BEFORE outcome inspection if GO)
**TRACK:** A (observed liquidations) — Hyperliquid-only via ironflow/hyperliquid-liquidations
**STATUS:** BLOCKED_ON_DATA
**PRIORITY:** Track A liquidation forward-validation (IRONFLOW) — BLOCKED_ON_DATA; maximize heavy work, shrink bottlenecks, force campaign progress.

## COMMANDS + OUTPUTS (evidence, captured live this session)

1) `python scripts/monitor_ironflow_liquidations.py --verify`
   VERIFY ok=True data_through=2026-10 consecutive_absent=3 baseline_drift=False content_hash_complete=True (36/36). Cache incomplete but hash baseline complete. All 6 state-consistency checks pass.

2) `python scripts/monitor_ironflow_liquidations.py --quick`
   Wrote evidence: research_state/ironflow_probe_20261103T031543Z.json
   No resume trigger. data_through=2026-10 probed=['2026-11','2026-12','2027-01','2027-02'] head_probes=8 cached_hits=0 probe_diff(added=0 changed=0 removed=0) baseline_drift(intact=True regressions=0 content_replaced=0 pairs_checked=36)

3) `python scripts/monitor_ironflow_liquidations.py --decision`
   {"new_data_path":false,"reasons":[],"quick_check":{"timestamp_utc":"2026-11-03T03:10:37Z","triggered":false,"triggering_files":[],"months_probed":["2026-11","2026-12","2027-01","2027-02"],"head_probes":8,"cached_hits":0,"data_through":"2026-10"},"probe_diff_summary":{"added_count":0,"changed_count":0,"removed_count":0,"unchanged_count":8,"any_change":false}}

4) `python scripts/monitor_ironflow_liquidations.py --scan`
   Wrote: research_state/ironflow_resume_scan_20261103T031658Z.json
   {"scan_ts":"2026-11-03T03:17:57Z","go":false,"reasons":[],"data_through":"2026-10","consecutive_absent":3,"tree":{"status":304,"not_modified":true},"resume_check":{"triggered":false,"months_probed":["2026-11","2026-12","2027-01","2027-02"],"head_probes":8,"get_requests":0,"get_requests_skipped":8},"probe_diff":{"added_count":0,"changed_count":0,"removed_count":0,"unchanged_count":8,"any_change":false},"tree_change":{"changed":false,"added":[],"content_replaced":[],"tree_not_modified":true},"baseline_drift":{"drifted":false,"regression_count":0,"content_replaced_count":0,"checked":36,"content_replaced":[]}}

5) `python scripts/verify_heavy_work_004i.py`
   ALL CHECKS PASSED [20261103T031544Z] (handoff/frontier/monitor-state/checklist/blocker-docs all OK)

6) `python scripts/hunt_alternative_liquidation_sources.py`
   Wrote: research_state/data_source_registry_alt_hunt.json + alt_source_scan_20261103T031658Z.json
   17 candidates probed; 0 GO. Review-required sources (HF broad search, Zenodo, OSF, arXiv, Common Crawl, Kaggle, GitHub repo search, Coinglass, Hyblock, Coinank, Paradigm, TheBlock) — none passed strict GO rubric (>=5 symbols, >=1 complete month OR >=3 non-overlapping 30-day blocks, documented completeness/coverage/license OK, unauthenticated only, schema compatible with frozen FCLR-010). ironflow/hyperliquid-liquidations is the sole Track A source and remains blocked at >=2026-11.

7) `python -m unittest discover -s tests -v`
   Ran 111 tests — OK (111/111 PASS)

## PROBE TABLE
- Forward months probed: 2026-11, 2026-12, 2027-01, 2027-02 (8 head probes)
- cached_hits: 0
- probe_diff: added=0 changed=0 removed=0 unchanged=8
- tree_change.content_replaced: []
- tree status: 304 not_modified=true (ETag W/"2d38-AqkYNsWwxCKiOUmPgektdcJePJk")
- baseline_drift: intact=True regressions=0 content_replaced=0 pairs_checked=36

## DOWNLOAD ACCOUNTING
- bytes_downloaded: 0 (no GETs for new files)
- head_requests: 8 (forward probes)
- get_requests: 0
- get_requests_skipped: 8 (scan path)

## TIMELINE
- Baseline data_through: 2026-10
- Consecutive_absent: 3 (months 2026-11, 2026-12, 2027-01 probed; 2027-02 also probed)
- Last verified: 2026-11-03T03:18:21Z

## RESUME CONDITIONS (EXACT)
1. Ironflow data/events or fills YYYY-MM >= 2026-11 returns 200 (verify via monitor --quick/--decision/--scan)
2. New admissible unauthenticated source passing rubric (>=5 symbols, >=1 complete month OR >=3 non-overlapping 30-day blocks, documented completeness/coverage/license OK, unauthenticated only, schema compatible with frozen FCLR-010)

## EVIDENCE LINKS
- research_state/ironflow_probe_20261103T031543Z.json
- research_state/ironflow_resume_scan_20261103T031658Z.json
- research_state/alt_source_scan_20261103T031658Z.json
- research_state/data_source_registry_alt_hunt.json
- research_state/experiment_frontier.json
- research_state/heavy_work_checklist_004i.md

## BOTTLENECK STATUS
- Data bottleneck is STRUCTURAL, not operational: no post-2026-10 ironflow data exists; all 8 candidate source families previously probed NO-GO (FCLR-NEXT-002 COMPLETE_NO-GO); 17 additional candidates probed this session, 0 passed GO rubric.
- No polling loops, no re-probing dead routes, no .github/workflows changes, no raw data in git.
- Heavy work (automation, tests, blocker evidence, frontier, handoff) is the mandatory per-session path while blocked.
