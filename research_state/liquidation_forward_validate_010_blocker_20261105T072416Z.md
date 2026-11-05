# Liquidation forward validation blocker - Track A (FCLR-NEXT-090)
TIMESTAMP (UTC): 20261105T072416Z

## Summary
Track A liquidation risk is the only active focus (repo-name prioritized). Volatility (Track C) sealed/locked; Track B NOT_SUPPORTED. No resume trigger; on heavy hold while blocked. This session's deliverable is a **measurable bottleneck removal**, not another monitor pass: the ironflow probe artifact family was the single largest remaining source of churn and it is now provably stable at 2 files.

## Baseline/metrics (step 1)
- research_state md+json before: 241 | after: 189 (-52, -21.6%)
- ironflow probe files before: 38 (37 digest + 1 live) | after: 2 (1 live + 1 canonical digest)
- Tests before: 136 | after: 138 (+2 new TestConsolidation cases for the 090 fix), all green

## Trigger probe (step 2)
- `python scripts/monitor_ironflow_liquidations.py --quick`: NO RESUME TRIGGER. data_through=2026-10; probed 2026-11,2026-12,2027-01,2027-02; head_probes=8; cached_hits=0; probe_diff(added=0 changed=0 removed=0); baseline_drift(intact=True regressions=0 content_replaced=0 pairs_checked=0 method=state_only_tree_unchanged); kaggle_mirror(updated=None triggered=None).
- `python scripts/deep_review_alt_sources.py`: cache_hits=13 cache_misses=1.
- `python scripts/hunt_alternative_liquidation_sources.py`: candidates=11, source=cache.
- `python scripts/monitor_ironflow_liquidations.py --verify`: VERIFY ok=True data_through=2026-10 consecutive_absent=3 baseline_drift=False content_hash_complete=True known_months=18.
- Decision: NO NEW DATA - ON HOLD. No prereg created; no harness execution.

## ROOT CAUSE FIXED (the actual bottleneck)
The prior "consolidation" was not consolidation. `_consolidate_ironflow_probes` named the digest after the *current* latest probe (`ironflow_probe_digest_<latest_ts>.json`), so every `--quick` run wrote a NEW digest file and never removed the previous one. By 07:14Z the directory held 37 digest files, each a 1-entry archive of the immediately-removed probe (all data_through=2026-10, all triggered=false). `generate_trend_report()` merges every one of them, so the 36 stale digests were pure artifact churn inflating every `--report` run. The fix makes the digest a single running archive at `ironflow_probe_digest_latest.json` that merges entries (de-duplicated by probe_id) and deletes stale per-run digests. Verified stable: two consecutive `--quick` runs leave exactly 2 ironflow files.

## Bottleneck demolition (step 3)
- `scripts/migrate_digest_archive_090.py`: folded 38 legacy digest files into `research_state/ironflow_probe_digest_latest.json` (38 unique archived entries; 25 tree-304 + 12 tree-200 probes; consecutive_absent 0 and 3; all triggered=false). Offline, idempotent.
- `scripts/merge_redundant_artifacts_090.py`: merged 19 superseded Track A files into 4 archives (blocker history, trigger probe history, dry-run history, campaign sweep history), preserving each removed file's name/size/first-40-lines. Dropped the unreferenced 76-byte `trackc_recompute_audit_20261104T175619Z_20261104T175619Z.md` stub (duplicate title of the canonical 3,857-byte audit; verified unreferenced by any canonical doc).
- Track C artifacts deliberately untouched: trackc_robustness_*, trackc_deeper_validation_*, leakage_audit_heavy_*, bottleneck_demolition_* are the sealed audit trail of the locked Track C conclusion and must not be consolidated.
- No schedulers/pollers/status-only files/repeated wrappers created. Churn minimized.

## Source expansion/hardening (step 4)
- Hyperliquid-only for Track A; GO rubric enforced (unauthenticated + >=2026-11 + liquidation-specific + >=5 symbols OR >=1 complete month OR >=3x30d blocks + permissive license + no keys/signed/requester-pays).
- No rubric-GO source identified. All probes unauthenticated.

## Harness hardening + dry-run (step 5)
- FCLR-010 fixtures present (tests/fixtures/tracka); offline dry-run capable.
- Resume path: `python scripts/monitor_ironflow_liquidations.py --quick` (now ~10s cold start, bounded forward-edge probe only).

## Tests
- `python -m unittest discover tests`: 138 tests OK (adversarial tests present). MUST remain green.
- New tests: `test_consolidation_single_canonical_digest`, `test_consolidation_merges_prior_canonical_digest` (TestConsolidation) pin the 090 fix.

## Resume conditions (only unblock)
- ironflow data/events/YYYY-MM.parquet or data/fills/YYYY-MM.parquet for any month >=2026-11 returns HTTP 200 unauthenticated (via monitor) OR
- new admissible unauthenticated source passes strict GO rubric (Hyperliquid-only for Track A)

## Next actions (heavy while blocked)
- Continue unauthenticated source discovery/hardening; keep fixtures+tests updated.
- Keep churn minimal: new evidence goes into the canonical digest + one blocker doc per session. No new timestamped families.
- On trigger: HALT, preregister in research_state/fclr010_prereg_$(date -u +%Y%m%dT%H%M%SZ).json BEFORE inspecting outcomes (hypothesis, frozen splits, features/targets, metrics, stop rule, data hashes), run ONLY frozen FCLR-010 harness.
- Update experiment_frontier.json last_checked and keep AGENT_HANDOFF current.