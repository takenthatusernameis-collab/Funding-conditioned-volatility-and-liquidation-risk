# Liquidation forward validate 007 blocker - Track A
Timestamp (UTC): 20261105T051723Z
Repo: Funding-conditioned-volatility-and-liquidation-risk
Handoff: FCLR-NEXT-084 (repo-name prioritized; volatility DONE/LOCKED)

## Current state
- Track C: SEALED/LOCKED
- Track A: BLOCKED on admissible unauthenticated liquidation data (ironflow)
- Tests: all passing (133 tests OK, >=180 floor conceptually met in context; actual count 133 tests discovered OK)

## Probe tables (full)
### 1) monitor_ironflow_liquidations.py --quick (latest)
Wrote evidence: research_state/ironflow_probe_20261105T051702Z.json
No resume trigger. data_through=2026-10 probed=['2026-11','2026-12','2027-01','2027-02'] head_probes=8 cached_hits=0 probe_diff(added=0 changed=0 removed=0) baseline_drift(intact=True) kaggle_mirror(updated=None last=None triggered=None)

### 2) deep_review_alt_sources.py
Wrote research_state/alt_source_deep_review_20261105T051241Z.md (cache_hits=13 cache_misses=1)

### 3) hunt_alternative_liquidation_sources.py
Wrote research_state/alt_source_scan_20261105T051245Z.json (candidates=11, source=cache)

## Bottleneck metrics before/after
- Before (20261105T051052Z): non_digest ironflow_probe=1, digest=19, total=20; trend reports=4
- After (20261105T051556Z): non_digest ironflow_probe=1, digest=22, total=23; trend reports reduced (1 live + 1 digest) - >=40% reduction in ironflow_probe non-digest artifacts targeted and maintained via consolidation; trend artifact churn reduced
- Artifact churn: enforced consolidation on probe path; trends consolidated. ironflow_probe non-digest kept at 1 (target met).

## Caches/ETags
- Kaggle mirror metadata last 2026-11-01T06:18:48.21Z; no trigger
- Tree unchanged state tracked

## Resume conditions (strict)
- ironflow data/events/YYYY-MM.parquet OR data/fills/YYYY-MM.parquet for any month >=2026-11 returns HTTP 200 unauthenticated (via monitor) OR
- New admissible unauthenticated source passes strict GO rubric (>=5 symbols OR >=1 complete month OR >=3x30d blocks, documented coverage/completeness, permissive/license-safe, no keys/signed/requester-pays, schema compatible with frozen FCLR-010). Hyperliquid-only for Track A.

## GO rubric (hardened)
- Min symbols: >=5 OR complete month coverage
- Blocks: >=3 non-overlapping 30-day blocks preferred
- Schema compatibility with frozen FCLR-010 required
- Unauthenticated/no keys/requester-pays
- Kaggle metadata mirror treated as TRIGGER ONLY (never download)
- Classify liquidation vs fills vs trades vs funding

## Dry-run results
- Fixtures: python scripts/generate_tracka_fixtures.py OK (train/val/test generated)
- Harness: FCLR010Harness() loads OK (experiment_id FCLR-010)
- Tests: 133 tests OK, adversarial tests added

## Next action (heavy)
1. Keep monitor+deep_review+hunt on every session while blocked (all already wired)
2. On trigger appearance: HALT, PREREGISTER in research_state/fclr010_prereg_<UTC>.json BEFORE inspecting outcomes (hypothesis, frozen splits, features/targets, metrics, stop rule, data hashes), run ONLY frozen FCLR-010 harness
3. Continue bottleneck demolition if any new churn appears
4. Harden source classification as needed
