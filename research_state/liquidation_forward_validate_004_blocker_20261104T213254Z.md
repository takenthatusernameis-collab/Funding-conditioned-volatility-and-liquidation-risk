# Track A Liquidation Forward Validation - Blocker Report (004i refresh)
Timestamp (UTC): 20261104T213254Z
Git SHA (HEAD): 0b4e112b
Branch: main
Campaign: LIQUIDATION_FORWARD_VALIDATE_HEAVY-004i
Priority: P0 - REPO-NAME PRIORITIZED (Track A liquidation risk NEXT; Track C volatility LOCKED)

## Status
BLOCKED - NO NEW DATA. On trigger only. Track A (FCLR-010) sealed/passed; forward validation cannot execute without admissible new data. Never conclude "no data" and stop; while blocked, remove bottlenecks and harden triggers so unblocking is instantaneous.

## Evidence (fresh probe tables this session)

### Ironflow (Hyperliquid liquidations) - primary Track A source (unauthenticated HF)
- Dataset: ironflow/hyperliquid-liquidations
- Tree URL: https://huggingface.co/api/datasets/ironflow/hyperliquid-liquidations/tree/main?recursive=true
- Events template: https://huggingface.co/datasets/ironflow/hyperliquid-liquidations/resolve/main/data/events/%s.parquet
- Fills template: https://huggingface.co/datasets/ironflow/hyperliquid-liquidations/resolve/main/data/fills/%s.parquet
- Fresh monitor probe (--quick): research_state/ironflow_probe_20261104T213437Z.json
- Tree status: 200, ETag W/"2d38-AqkYNsWwxCKiOUmPgektdcJePJk"
- Available months (both data/events/*.parquet and data/fills/*.parquet present): 2025-05 through 2026-10 (18 months each). No 2026-11, 2026-12, 2027-01, 2027-02.
- data_through: 2026-10
- consecutive_absent (forward edge): >=4 (2026-11, 2026-12, 2027-01, 2027-02 all probed absent)
- Head probes (2026-11, 2026-12, 2027-01, 2027-02): no resume trigger
- Baseline drift: intact=True, regressions=0, content_replaced=0, pairs_checked=18, method=state_only_tree_unchanged
- Kaggle mirror: updated=False, last=2026-11-01T06:18:48.21Z, triggered=False
- Resume trigger (PRIMARY): ironflow publishes data/events/YYYY-MM.parquet and/or data/fills/YYYY-MM.parquet for any month >= 2026-11 with HTTP 200 on unauthenticated GET. Verify via `python scripts/monitor_ironflow_liquidations.py --quick` (NEW_AVAILABLE).

### Alternative sources (deep review) - unchanged since 20261104T192914Z sweep
- Reviewed: research_state/alt_source_deep_review_*.md and research_state/alt_source_scan_*.json (2026-11-04 sessions).
- Binance public archives, Bybit, OKX: no admissible unauthenticated historical liquidation event parquet meeting strict rubric.
- CoinAPI, Tardis, Kaiko, Glassnode, Coinglass: require keys/payment/auth/signup or are not dataset hosts - NO-GO.
- No alternative source passes all 7 rubric criteria below.

## Strict GO rubric (Track A) - all must hold
1. Unauthenticated access only (no keys/signed/requester-pays)
2. Observed liquidation labels (not synthetic) with provenance (Hyperliquid-only for Track A)
3. >=5 symbols
4. >=1 complete month OR >=3 non-overlapping 30-day blocks
5. Documented completeness/coverage, permissible license/terms
6. Schema compatible with frozen FCLR-010
7. Adequate coverage for forward validation

If a rubric-GO alternative appears: HALT inspection, PREREGISTER in research_state/fclr010_prereg_$(date -u +%Y%m%dT%H%M%SZ).json BEFORE inspecting outcomes (full hypothesis/frozen splits/metrics/stop rule), then run ONLY frozen FCLR-010 harness. No merging sources, no widening scope, no re-tuning.

## Resume conditions (concrete, checkable)
- PRIMARY: ironflow month >=2026-11 returns HTTP 200 unauthenticated via monitor (--quick shows NEW_AVAILABLE/resume trigger).
- ALTERNATIVE: new admissible unauthenticated source passes strict GO rubric + preregistered before outcome inspection.
- Until then: Track A stays MONITOR_ONLY; campaigns re-run each session, bottlenecks removed, tests kept green.

## Bottlenecks removed this session (20261104T213254Z)
1. Fixed failing test tests/test_alt_source_hunt_cache.py::TestUrlProbeCache::test_cache_get_returns_none_for_missing_and_bad: Path.write_text was called on the mkdtemp directory (IsADirectoryError); now writes to the cache file path. Suite: 175/175 pass.
2. De-tracked scripts/__pycache__/*.pyc and tests/__pycache__/*.pyc from git (git rm --cached, staged, not committed) so working-tree status is no longer noisy.

## Next actions (heavy, non-skippable, in order)
1) STATE SWEEP: read RESEARCH_PROMPT.md, AGENT_HANDOFF.md, research_state/*, scripts/monitor_ironflow_liquidations.py, scripts/hunt_alternative_liquidation_sources.py, scripts/deep_review_alt_sources.py; write research_state/campaign_sweep_tracka_<UTC>.md with concrete evidence and diff vs prior sweep.
2) TRIGGER PROBE (FULL TABLES): run the three scripts; log every URL/path/pattern, status/headers/mtime/body previews, ETag/TTL, cached hits. If resume trigger appears -> preregister FIRST, then run only frozen FCLR-010 harness. Else write "NO NEW DATA - ON HOLD" with complete tables.
3) BOTTLENECK REMOVAL: find >=1 real bottleneck in scripts/; fix with before/after evidence (diff + timing/behavior). No schedulers/pollers/status-only files.
4) TEST HARDENING: add/extend tests in tests/test_monitor_ironflow.py (state-diff, ETag/TTL, month-windowing, candidate classification, failure modes); run python -m pytest tests/ -q (must remain >=166 passing; currently 175).
5) BLOCKER+FRONTIER+HANDOFF: write fresh blocker doc (this file); update experiment_frontier.json resume triggers/last_checked/blocked-cell status; update AGENT_HANDOFF.md with timestamped next task.

## Artifacts
- research_state/ironflow_probe_20261104T213437Z.json (fresh monitor evidence)
- research_state/ironflow_monitor_state.json
- research_state/experiment_frontier.json (TRACK_A last_checked 2026-11-04T21:32:54Z)
- AGENT_HANDOFF.md (single durable handoff, timestamp 20261104T213254Z)
- tests/test_monitor_ironflow.py (82 tests passing; suite 175/175)
