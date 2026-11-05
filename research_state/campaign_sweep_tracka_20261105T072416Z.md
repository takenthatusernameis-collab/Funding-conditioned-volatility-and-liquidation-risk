# Campaign sweep - Track A (FCLR-NEXT-090)
TIMESTAMP (UTC): 20261105T072416Z
Git HEAD: 69d08ad5
Branch: main
Handoff: AGENT_HANDOFF.md (single durable handoff, FCLR-HANDOFF-20261105T071232Z)
Priority: P0 - REPO-NAME PRIORITIZED (Volatility SEALED/LOCKED; Liquidation Risk = ONLY ACTIVE OBJECTIVE)

## 1) ENTRY METRICS & BOTTLENECK BASELINE (IRREFUTABLE)

| Metric | Before | After | Delta |
|---|---|---|---|
| research_state md+json | 241 | 189 | -52 (-21.6%) |
| ironflow probe files (all) | 38 | 2 | -36 |
| ironflow_probe_digest_* (per-run) | 37 | 0 | -37 |
| canonical digest | absent | ironflow_probe_digest_latest.json | +1 (38 archived entries) |
| tests | 136 | 138 | +2 (090 fix) |

Bottleneck identified: `_consolidate_ironflow_probes` named the digest after the
*current* latest probe (`ironflow_probe_digest_<latest_ts>.json`), so every
`--quick` run wrote a new digest and never removed the prior one. By 07:14Z the
directory held 37 digest files, each a 1-entry archive of the immediately-removed
probe (all data_through=2026-10, all triggered=false). `generate_trend_report()`
merged all 37, so the 36 stale digests were pure artifact churn inflating every
`--report` run. This was NOT a consolidation gap -- it was the consolidation
mechanism itself generating the churn.

## 2) TRIGGER PROBE (EXHAUSTIVE, HYPERLIQUID-ONLY)
- `python scripts/monitor_ironflow_liquidations.py --quick` -> NO RESUME TRIGGER. data_through=2026-10; probed 2026-11,2026-12,2027-01,2027-02; head_probes=8; cached_hits=0; probe_diff(added=0 changed=0 removed=0); baseline_drift(intact=True regressions=0 content_replaced=0 pairs_checked=0 method=state_only_tree_unchanged); kaggle_mirror(updated=None triggered=None).
- `python scripts/deep_review_alt_sources.py` -> cache_hits=13 cache_misses=1.
- `python scripts/hunt_alternative_liquidation_sources.py` -> candidates=11, source=cache.
- `python scripts/monitor_ironflow_liquidations.py --verify` -> VERIFY ok=True data_through=2026-10 consecutive_absent=3 baseline_drift=False content_hash_complete=True known_months=18.
- Decision: NO NEW DATA - ON HOLD. No prereg created; no harness execution.

## 3) BOTTLENECK DEMOLITION (AGGRESSIVE)
- `scripts/migrate_digest_archive_090.py`: 38 legacy digest files -> 1 canonical
  `research_state/ironflow_probe_digest_latest.json` (38 unique archived entries;
  25 tree-304 + 12 tree-200 probes; consecutive_absent 0 and 3; all
  triggered=false). Offline, idempotent.
- `scripts/merge_redundant_artifacts_090.py`: 19 superseded Track A files ->
  4 archives (blocker history, trigger probe history, dry-run history, campaign
  sweep history), each recording removed files' name/size/first-40-lines.
- Dropped unreferenced 76-byte `trackc_recompute_audit_20261104T175619Z_20261104T175619Z.md`
  stub (duplicate title of the canonical 3,857-byte audit; verified unreferenced).
- Track C artifacts deliberately untouched: trackc_robustness_*,
  trackc_deeper_validation_*, leakage_audit_heavy_*, bottleneck_demolition_* are
  the sealed audit trail of the locked Track C conclusion.
- No schedulers/pollers/status-only files/repeated wrappers created.
- Stability proof: two consecutive `--quick` runs leave exactly 2 ironflow files.

## 4) SOURCE HARDENING + MAXIMALLY STRICT RUBRIC
- GO rubric enforced: unauthenticated + >=2026-11 + liquidation-specific + >=5
  symbols OR >=1 complete month OR >=3x30d blocks + permissive license + no
  keys/signed/requester-pays. Hyperliquid-only for Track A.
- No rubric-GO source identified. All probes unauthenticated.

## 5) HARNESS HARDENING + OFFLINE DRY-RUN
- FCLR-010 fixtures present (tests/fixtures/tracka); offline dry-run capable.
- Resume path: `python scripts/monitor_ironflow_liquidations.py --quick` (~10s cold
  start, bounded forward-edge probe only).

## 6) TESTS, EVIDENCE, HANDOFF UPDATE
- `python -m unittest discover tests`: 138 tests OK (2 new TestConsolidation
  cases pin the 090 fix). MUST remain green.
- Blocker doc: research_state/liquidation_forward_validate_010_blocker_20261105T072416Z.md
- experiment_frontier.json updated (last_checked 20261105T072416Z, artifact_churn_090 block).

## RESUME CONDITION (ONLY UNBLOCK)
ironflow data/events/YYYY-MM.parquet or data/fills/YYYY-MM.parquet for month>=2026-11 returns HTTP 200 unauthenticated OR admissible unauthenticated Hyperliquid source passes strict GO rubric. Hyperliquid-only.

## STOP RULE
All steps complete. Track C locked. Track B unsupported. No conflation. No schedulers/pollers/status-only/repeated wrappers/agent-controllers/workflow changes. Preregister BEFORE outcomes if triggered. Heavy work mandatory while blocked. NO COASTING. State left stricter than found.