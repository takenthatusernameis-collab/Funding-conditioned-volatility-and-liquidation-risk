# LIQUIDATION FORWARD VALIDATE - BLOCKER EVIDENCE (STEP 6)
Timestamp (UTC): __TS__
Git SHA (HEAD): 83e151d03dc1046b9af405e8c26f2c6b94c7614b
Branch: main
Handoff: AGENT_HANDOFF.md (single durable handoff)

## Probe tables (full)
### Ironflow monitor --quick (latest)
- data_through: 2026-10
- probed: ['2026-11', '2026-12', '2027-01', '2027-02']
- head_probes: 8
- cached_hits: 0
- probe_diff: added=0 changed=0 removed=0
- baseline_drift: intact=True regressions=0 content_replaced=0
- kaggle_mirror: updated=False triggered=False
- Auto-consolidation: executed (probe artifacts reduced)

### Deep review (alt sources)
- cache_hits: 13, cache_misses: 1
- Hyperliquid /info POST returns 200 (market metadata) - schema compatibility needs verification against FCLR-010
- HF dataset ironflow/hyperliquid-liquidations exists (metadata) - needs file inspection
- Other venues: mostly 404/401 or auth-required/no liquidation census

### Hunt (alt sources)
- Shared caches used (HF search cache, URL probe cache)
- Rubric enforced

## Caches/ETags
- URL probe cache: research_state/url_probe_cache.json (TTL 6h)
- HF search cache: research_state/hf_search_cache.json (TTL 24h)
- Ironflow monitor: ETag/tree cache, per-file caching active

## Resume conditions (ONLY UNBLOCK)
1. ironflow data/events/YYYY-MM.parquet or data/fills/YYYY-MM.parquet for any month >=2026-11 returns HTTP 200 unauthenticated (via monitor) OR
2. New admissible unauthenticated source passes strict GO rubric (>=5 symbols OR >=1 complete month OR >=3x30d blocks, documented completeness/coverage, permissive license, no keys/signed/requester-pays, schema compatible with frozen FCLR-010). Hyperliquid-only for Track A.

## GO rubric (strict)
- min_symbols >= 5 OR >=1 complete month with >=5 symbols OR >=3 non-overlapping 30-day blocks
- completeness_doc_required true
- license_ok true
- unauthenticated_only true
- no_requester_pays true
- schema_compatible_fclr010 true

## Dry-run results (FCLR-010 harness)
- Harness config loads (FCLR-010 frozen)
- tests/test_fclr010_harness.py: 4 passed
- Fixtures generated: tests/fixtures/tracka/ (train/val/test) - validates offline path
- fclr010_validate requires preregistration before inspecting outcomes on new data

## Tests
- python -m pytest tests/ -q: 180 passed (>=180 maintained)

## Next action (heavy)
If resume conditions met: PREREGISTER in research_state/fclr010_prereg_<TIMESTAMP>.json BEFORE inspecting outcomes (hypothesis, frozen splits from run_manifest, features/targets, metrics primary brier C2_vs_B1, stop rule, gates, data hashes), then run ONLY frozen FCLR-010 harness. Do NOT touch Track C/B. No schedulers/pollers/status-only files/wrappers/workflow changes.
