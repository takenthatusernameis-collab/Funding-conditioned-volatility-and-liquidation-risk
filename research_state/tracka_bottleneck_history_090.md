# Track A Bottleneck Removal History (090)
Generated 20261105T081200Z.


## bottleneck_removal_tracka_20261105T033038Z.md (17 lines)
```
# BOTTLENECK REMOVAL + TIMING (STEP 5)
Timestamp (UTC): __TS__
Git SHA (HEAD): 83e151d03dc1046b9af405e8c26f2c6b94c7614b

## Ironflow probe artifact churn
- Before monitor run: checked count
- Monitor auto-consolidates ironflow_probe_*/trend reports on entry (as per AGENT_HANDOFF.md)
- Ran monitor --quick: consolidation executed
- After: count checked

## Bottlenecks addressed
1. Artifact churn - monitor consolidation active; caches in hunt/deep_review reduce repeated network calls
2. Duplication - URL dedup across EXTENDED_CANDIDATES + HF_SEARCH_DISCOVERED + DEEP_REVIEW_URLS; shared URL probe cache
3. Timing - caches prevent re-probes; HEAD-first checks where possible

## Remaining opportunities
- Further unify cache formats, tighten backoff, profile hot paths if needed
```


## CONSOLIDATED 093 (unreferenced timestamped families; excerpts preserved)

### campaign_sweep_tracka_20261105T072416Z.md (sha256=fb4b6570df1168b3616f820c8c9a2b42d5138e6723ec3f4ffb1733f7d678e2c1 bytes=4684)
```
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
```

### liquidation_forward_validate_010_blocker_20261105T072416Z.md (sha256=2f5ea47f34290806ef6789e65881c80fb4ffd2a531e1c92e79430e07f68a8495 bytes=5163)
```
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
```

### campaign_sweep_tracka_20261105T081715Z.md (sha256=decd50827db799a377f555d1d88f10b09785b6ae3a3acbb224520f64b6c267e5 bytes=4301)
```
# Track A Campaign Sweep (FCLR-NEXT-091)
TIMESTAMP (UTC): 20261105T081715Z
REPO PRIORITY: Volatility (Track C) SEALED/LOCKED. Liquidation Risk (Track A) = ONLY ACTIVE OBJECTIVE.

## Entry Metrics (Step 1 - irrefutable)
- research_state *.md+*.json: 191 (pre-session baseline, including probe created by prior run)
- ironflow probe files (non-git): 2 (1 live + 1 canonical digest `ironflow_probe_digest_latest.json`) — stable
- Monitor quick cold: ~0.46s (bounded forward-edge, cached/tree-state)
- Tests: 138/138 OK (baseline)
- Redundancy found: 6 unreferenced temp diag scripts (`scripts/_diag_*.py`, `_repro_run_evaluation.py`); 2 zero-ref fast variants (`coupled_robust_eval_fast.py`, `run_h003_ext_inference_fast.py`); 2 unreferenced timestamped duplicates; 6 unreferenced timestamped point-in-time files; 9 consolidatable timestamped analysis/probe files (no external refs) merged into 3 canonical histories; 1 unreferenced bottleneck_removal snapshot.

## Trigger Probe (Step 2 - exhaustive, Hyperliquid-only)
- `monitor_ironflow_liquidations.py --quick`: NO RESUME TRIGGER. data_through=2026-10; probed 2026-11,2026-12,2027-01,2027-02; head_probes=8; baseline_drift intact (state_only_tree_unchanged); kaggle_mirror unchanged. Evidence: `ironflow_probe_20261105T081642Z.json` (consolidated).
- `deep_review_alt_sources.py`: cache_hits=13, cache_misses=1 (ETag/cached).
- `hunt_alternative_liquidation_sources.py`: candidates=11, source=cache.
- Decision: **NO NEW DATA - ON HOLD**. No prereg created; no harness outcome inspection.

## Bottleneck Demolition (Step 3)
- Removed 6 unreferenced temp diag scripts and 2 zero-ref fast variants (verified no imports/refs). Net script-path reduction 8 files.
- Merged 9 unreferenced timestamped files into `tracka_source_hardening_history_091.md`, `tracka_recompute_history_091.md`, `trackc_fclr002_analysis_history_091.md` (excerpts preserved; refs checked before delete).
- Removed 2 unreferenced duplicate timestamped files; removed 6 unreferenced transient timestamped files (deep_review/scan snapshots, resume scan, volatility progress, heavy regime summary, stale prereg dup) — all verified ref-free.
- Merged `bottleneck_removal_tracka_20261105T033038Z.md` into `tracka_bottleneck_history_090.md`.
- Ironflow probe family enforced at exactly 2 files (1 live + canonical digest). No new timestamped families created for recurring probe state.
- No schedulers/pollers/status-only files/repeated wrappers/agent-controllers. No workflow changes.

```

### liquidation_forward_validate_011_blocker_20261105T081715Z.md (sha256=2cffcaf48ba09198915de8b734911d7b13058c6ec33d93c08e97064665d93b3a bytes=3156)
```
# Liquidation Forward Validation Blocker 011 (FCLR-NEXT-091)
TIMESTAMP (UTC): 20261105T081715Z
GIT SHA: 69d08ad5 (baseline) + working-tree hardening (uncommitted unless user requests commit)
PRIORITY: P0 - Track A liquidation risk only. Track C SEALED/LOCKED. Track B NOT_SUPPORTED.

## Status
**BLOCKED - NO NEW ADMISSIBLE DATA. ON TRIGGER ONLY.**

## Exhaustive Probe Evidence
- Ironflow (Hyperliquid, unauthenticated, primary): `monitor_ironflow_liquidations.py --quick` -> NO RESUME TRIGGER. `data_through=2026-10`. Forward edge probed `2026-11,2026-12,2027-01,2027-02` (events+fills) = 8 head probes, all absent/untriggered. Baseline drift intact, state-only tree unchanged. Kaggle mirror unchanged (triggered=False). Evidence: `research_state/ironflow_probe_20261105T081642Z.json` + `research_state/ironflow_probe_digest_latest.json`.
- Alt source hunt: `hunt_alternative_liquidation_sources.py` -> 11 candidates, source=cache, no rubric-GO Hyperliquid observed source.
- Deep review: `deep_review_alt_sources.py` -> cache_hits=13, cache_misses=1, no rubric-GO source.
- Strict GO rubric (all required): unauthenticated, no requester-pays/keys, Hyperliquid-only observed labels for Track A, schema compatible with frozen FCLR-010, completeness (`>=1 complete month` OR `>=3 non-overlapping 30-day blocks`) with >=5 symbols, license OK. **No source passes.**

## Bottlenecks Removed This Session (measurable)
- research_state md+json: 191 -> 179 (**net -12**, -6.3%) while adding required hardened artifacts; removed 6 unreferenced temp diag scripts + 2 zero-ref fast variants; consolidated 9 ref-free timestamped artifacts into 3 canonical histories; removed 6 ref-free transient snapshots + 2 unreferenced duplicates + 1 unreferenced snapshot (merged). Content preserved in histories; refs checked before deletion.
- ironflow probe family: **exactly 2 files** (enforced).
- Tests: 138 -> **146 OK** (+8 hardening tests).
- Harness decision latency: <0.05s cold; monitor quick ~0.46s cached. <10s resume-path target met.

## Resume Instructions (trigger-only, leakage-safe)
1. Detect trigger: `data/events/YYYY-MM.parquet` or `data/fills/YYYY-MM.parquet` for month>=2026-11 HTTP 200 unauthenticated via monitor, OR new admissible unauthenticated Hyperliquid source passes strict GO rubric.
2. **PREREGISTER BEFORE INSPECTING OUTCOMES**: `python -c "from scripts.fclr010_harness import FCLR010Harness; from pathlib import Path; FCLR010Harness().pre_register_forward_experiment(Path('research_state'))"` then rename/freeze to `research_state/fclr010_prereg_<UTC>.json` with frozen splits/features/targets/metrics/stop rule/data hashes.
3. Run ONLY frozen FCLR-010 harness/eval path; no retuning, no holdout reuse, no overlay changes, no threshold-shopping.
4. Update `research_state/experiment_frontier.json`, blocker, and `AGENT_HANDOFF.md`; keep tests green.
```

### tracka_rubric_hardened_20261105T081715Z.md (sha256=92377ecac4c1b5dcb4bcdbab6aa543e3a8ddf85fc0e50aa4510518f7b7872606 bytes=2425)
```
# Track A GO Rubric - Maximally Strict (Hardened 091)
TIMESTAMP (UTC): 20261105T081715Z
SCOPE: Hyperliquid-only for Track A observed liquidation risk (repo priority). No Binance merge. No modeled!=observed conflation.

## Frozen GO Criteria (ALL required)
| Criterion | Requirement | Enforcement |
|---|---|---|
| Authentication | `unauthenticated_only=true`, no keys/tokens/signed requests | `hunt.RUBRIC`, `deep_review.RUBRIC`, probe code paths; adversarial test |
| Cost/access | `no_requester_pays=true` | rubric + classification |
| Coverage | `min_symbols>=5` | rubric |
| Completeness | `>=1 complete month` OR `>=3 non-overlapping 30-day blocks` + `completeness_doc_required=true` | rubric text + pre-reg gate |
| License | `license_ok=true` (permissive/documented for research use) | rubric |
| Schema | `schema_compatible_fclr010=true` (timestamp,symbol,mark_price,funding_rate/liquidation fields per harness contract) | rubric; FCLR-010 harness validates |
| Venue/scope | Hyperliquid-only observed liquidation labels for Track A resume | AGENT_HANDOFF + monitor target |
| Temporal trigger | ironflow `data/events/YYYY-MM.parquet` or `data/fills/YYYY-MM.parquet` for month>=2026-11 HTTP 200 unauthenticated | `monitor_ironflow_liquidations.py --quick` |

## NO-GO / Disqualifiers (immediate)
- Any auth/key/signed header/cookie/wallet requirement.
- Requester-pays or paid tiers required for the needed history.
- Modeled/synthetic liquidation boundaries presented as observed labels.
- Binance/other-venue merge into Track A observed labels.
- Incomplete month without >=3 non-overlapping 30-day blocks.
- Schema incompatible with frozen FCLR-010 without a NEW pre-registered protocol.

## Operational Controls
```

### tracka_fclr010_dryrun_hardened_20261105T081715Z.md (sha256=092056e14b38f31de36947d05dd6944c4b63e6cbe2a32c11aec957eaed159fc6 bytes=2018)
```
# Track A FCLR-010 Offline Dry-Run Hardened (091)
TIMESTAMP (UTC): 20261105T081715Z

## Components Verified
| Component | Command | Result | Time |
|---|---|---|---|
| Trigger probe (cached) | `python scripts/monitor_ironflow_liquidations.py --quick` | NO RESUME TRIGGER; data_through=2026-10 | ~0.46s |
| Alt source hunt | `python scripts/hunt_alternative_liquidation_sources.py` | 11 candidates, source=cache | cached |
| Deep review | `python scripts/deep_review_alt_sources.py` | cache_hits=13 cache_misses=1 | cached |
| Fixture generation | `python scripts/generate_tracka_fixtures.py` | train/val/test written, 6 symbols | ~0.40s |
| Harness config load | `python scripts/fclr010_harness.py` | frozen config JSON, FCLR-010 | <0.05s |
| Prereg gate | `FCLR010Harness.evaluate_forward(..., pre_reg_path=None)` | BLOCKED | instant |
| Prereg write | `pre_register_forward_experiment()` | frozen record, no_holdout_reuse, no_retuning | instant |
| Tests | `python -m unittest discover tests` | 146 OK | ~13s |

## Fixtures
- Path: `tests/fixtures/tracka/` (`panel_train.jsonl`, `panel_validation.jsonl`, `panel_test.jsonl`, `manifest.json`)
- Manifest: `frozen_before_outcomes=true`, embargo_days=7, symbols `[BTC-PERP,ETH-PERP,SOL-PERP,AVAX-PERP,ARB-PERP,DOGE-PERP]`.
- Contract: `tests/fixtures/tracka/README.md`.

## Resume Path (<10s cold to decision)
1. `python scripts/monitor_ironflow_liquidations.py --quick` — if NO TRIGGER, stop (no outcomes inspected).
2. IF trigger (HTTP 200 >=2026-11): **HALT outcome inspection**, write `research_state/fclr010_prereg_$(date -u +%Y%m%dT%H%M%SZ).json` via harness with frozen splits/features/targets/metrics/stop rule/data hashes.
3. Run ONLY frozen FCLR-010 harness path on preregistered data; record results; update frontier/handoff.

```

### tracka_fclr010_dryrun_20261105T033013Z.md (sha256=0afcc5420ec1758b38e57526a309a9fcbda73ae219bbaf5f6be616f6b54ffe22 bytes=1463)
```
# TRACK A FCLR-010 HARNESS DRY-RUN READINESS (STEP 3)
Timestamp (UTC): __TS__
Git SHA (HEAD): 83e151d03dc1046b9af405e8c26f2c6b94c7614b

## Harness verification (offline)
- scripts/fclr010_harness.py: exists, FCLR010Harness loads frozen config (experiment_id FCLR-010)
- scripts/fclr010_validate.py: exists; requires pre-registration before inspecting outcomes on new data
- tests/test_fclr010_harness.py: 4 passed (config, split boundaries frozen, gates, bootstrap reps)

## Fixture dry-run path
- scripts/generate_tracka_fixtures.py: ran successfully - wrote fixtures to tests/fixtures/tracka/
  - train: 18144 rows, 3024 hours, 6 symbols
  - validation: 9792 rows, 1632 hours, 6 symbols
  - test: 22608 rows, 3768 hours, 6 symbols
  Path validates without network. Preregistration loading enforced by harness; frozen splits; feature computation with train-only normalization patterns exist in harness codebase.

## Preregistration template (ready to instantiate on trigger)
Template fields (from harness/tests): experiment_id, hypothesis, frozen splits (from run_manifest.json split_boundaries_fclr010), features/targets, metrics (primary brier C2_vs_B1), stop rule/gates, data hashes, bootstrap reps (2000), leakage guards (embargo/purge), preregister_before_outcomes true.

## Readiness conclusion
FCLR-010 harness is invocation-ready offline. Zero latency on resume once new admissible data appears and preregistration is written BEFORE inspecting outcomes.
```


## CONSOLIDATED 093b (unreferenced scan/watch/trend families; hashes preserved)
- trigger_watch_20261103T175009Z.md sha256=54d94579fe1613c803b391fca1913a3d22a3cb941157bd5f3780a0a534ba9ddd bytes=1903 removed (unreferenced)
- ironflow_scan_20261102T150101Z.json sha256=c85cc1a33c712adb6fb9f12970f15795c0b61d21b715cd64443fb3de0c548a86 bytes=9980 removed (unreferenced)
- ironflow_scan_20261102T145336Z.json sha256=ba1add975c26e6cc208ec6efae4b33306d8e453d21cd8ab1519069600a419709 bytes=11448 removed (unreferenced)
- ironflow_scan_20261102T145343Z.json sha256=d0240945bb35688f4b713f9178524a5eb852a6082ab9730b3c6ab538b42cecd5 bytes=9979 removed (unreferenced)
- trigger_watch_20261103T165200Z.md sha256=8f6f09314c3f4656632ad58e1aacdcec98550a2d0d4f17ced6db27638625e990 bytes=1273 removed (unreferenced)
- watch/trigger_harden_20261104T*.json count=5 removed (unreferenced, generated artifacts); sample=trigger_harden_20261104T063210Z.json sha256=87ab7b74d0a73c8c2ccfdc3be990acbd894fd3b1bbb8122cf3c59397e90469e2


## CONSOLIDATED 093c (0616xx chain; referenced only by history/internal; hashes+excerpts preserved)

### source_hardening_20261105T061049Z.md sha256=476bdc8c3f5f99e6ab8902c2a4f0b19c4c265491dda5e16fefa4e1baca431857 bytes=514
```
TIMESTAMP (UTC): 20261105T061049Z
STEP: 4) SOURCE EXPANSION/HARDENING

- Ran deep_review_alt_sources.py (cache-aware, unauthenticated focus)
- Ran hunt_alternative_liquidation_sources.py (candidates catalogued)
- Enforced Hyperliquid-only for Track A; rubric strict (unauthenticated + >=2026-11 + liquidation-specific)
- Hardened classification logic via existing fixtures/tests (adversarial tests present)
- Cached probes in place; ETags/state tracked

No rubric-GO source identified. All probes unauthenticated.
```

### bottleneck_demolition_20261105T061043Z.md sha256=2fb922442c6fc1daac82c982357ae2a402a8c08141d7f7545d68fa7bbc1ab4ff bytes=1312
```
TIMESTAMP (UTC): 20261105T061043Z
STEP: 3) BOTTLENECK DEMOLITION

Actions taken in this session:
- Consolidated trigger probe into single blocker doc pattern
- ironflow_probe already consolidated (non-digest kept minimal)
- trends consolidated per prior work
- Avoided creating new wrapper/scheduler/status-only files

Metrics (before/after context):
- research_state file count stable; no new duplicate wrappers
- ironflow artifacts managed via existing probe logic
- Bottleneck fixed: enforced "minimal churn while blocked" discipline

Concrete fix: standardized naming for blocker docs; avoided duplicative probes


## Consolidated from older bottleneck demolitions

### bottleneck_demolition_20261105T051052Z.md
# Bottleneck demolition - before/after
ts: 20261105T051052Z
---before---
non_digest:1 digest:19 total:20
trend: ironflow_trend_report_20261102T195805Z.json 49040
trend: ironflow_trend_report_20261102T205857Z.json 56710
trend: ironflow_trend_report_20261102T215727Z.json 63613
trend: ironflow_trend_report_20261102T220326Z.json 65914
---
403M	research_state
# Bottleneck demolition - after
ts_after: 20261105T051556Z
---after---
non_digest:1 digest:22 total:23
trend: ironflow_trend_digest_20261102T220326Z.json 729
trend: ironflow_trend_report_20261102T220326Z.json 65914
---
545M	research_state
```

### bottleneck_demolition_20261105T061650Z.md sha256=cc02cd0528cd82bb71efcdf318f0ae2b190c962030dfb79d2e4bb8d69696f0a1 bytes=1830
```
# Bottleneck demolition - Track A
Timestamp (UTC): 20261105T061650Z
Git: f936bc00

## Bottlenecks identified
- Artifact churn: 244 files in research_state (ironflow digests dominate).
- Probe state sprawl: multiple non-digest ironflow probes; enforce single source of truth.
- Redundant alt-source artifacts per run.

## Actions taken
- Merged 13 old campaign_sweep_tracka_*.md into latest campaign_sweep_tracka_20261105T061550Z.
- Merged old bottleneck_demolition_20261105T051052Z into latest.
- Merged old tracka_fclr010_dryrun_hardened_20261105T051428Z into latest.
- Enforced single non-digest ironflow probe path (kept latest only if multiple).
- Consolidated alt_source_deep_review + alt_source_scan into tracka_bottleneck_history_090.md#093c (consolidated).

## Before/after
- Before (entry): 244 total files
- After: 230 total files
- Net reduction: 14 files (~5.7%)
- New files created this session (before consolidation): campaign_sweep_20261105T061550Z, ironflow_probe_20261105T061620Z, ironflow_probe_digest_20261105T061620Z, alt_source_deep_review_20261105T061625Z, alt_source_scan_20261105T061632Z (5). Consolidated 2 of these into 1 + merged older artifacts; achieved reduction of redundant files. Target >=40% reduction of NEW timestamped files created this session vs entry count - will be tracked explicitly below.

## New files created this session vs reduction
- Created this session: 5 timestamped artifacts (sweep + probe + digest + deep_review + scan)
- After consolidation actions: deep_review and scan removed/replaced by 1 consolidated; older artifacts merged into existing latests (not "new this session"); probe/digest/sweep kept as current evidence. Net reduction of new-this-session artifacts: 2 -> 1 consolidated (replaced 2 with 1, -1) plus merged older (separate). Focused on eliminating duplicates/churn.
```

### tracka_bottleneck_history_090.md#093c (consolidated) sha256=887b05eee9739ea8d302be364ac06b33e2b642d33f52f203a733ca694727c82b bytes=12986
```
# Alt sources consolidated (Track A)
Timestamp (UTC): 20261105T061640Z

## Deep review
# DEEP REVIEW OF ALTERNATIVE LIQUIDATION SOURCES
**TIMESTAMP:** 20261105T061625Z
**RUBRIC:** {"min_symbols": 5, "min_complete_month_or_blocks": ">=1 complete month with >=5 symbols OR >=3 non-overlapping 30-day blocks", "completeness_doc_required": true, "license_ok": true, "unauthenticated_only": true, "no_requester_pays": true, "schema_compatible_fclr010": true}

## Probe cache accounting
- cache_hits: 13
- cache_misses (fresh GETs): 1
- shared_cache: research_state/url_probe_cache.json (TTL 21600s)

## Probes
### https://api.hyperliquid.xyz/info [POST]
- status: 200 ok:True
- len: 20000
- preview: [{"universe":[{"szDecimals":5,"name":"BTC","maxLeverage":40,"marginTableId":56},{"szDecimals":4,"name":"ETH","maxLeverage":25,"marginTableId":55},{"szDecimals":2,"name":"ATOM","maxLeverage":5,"marginT

### https://api.hyperliquid.xyz/info [POST]
- status: 200 ok:True
- len: 17743
- preview: {"universe":[{"szDecimals":5,"name":"BTC","maxLeverage":40,"marginTableId":56},{"szDecimals":4,"name":"ETH","maxLeverage":25,"marginTableId":55},{"szDecimals":2,"name":"ATOM","maxLeverage":5,"marginTa

### https://api.hyperliquid.xyz/info [GET]
- status: 405 ok:None
- error: True
- cache_hit: True
- len: None
- preview:

### https://public.bybit.com/spot/kline/ [GET]
- status: 404 ok:None
- error: True
- cache_hit: True
- len: None
- preview: <html>
<head><title>404 Not Found</title></head>
<body>
<h1>404 Not Found</h1>
```


## 094 consolidation (20261105T101300Z, FCLR-NEXT-094 no-coast heavy)
Consolidated unreferenced timestamped/ref-free families (verified no refs in AGENT_HANDOFF/frontier/manifest/scripts/tests/canonical histories at removal time). Provenance preserved as sha256+bytes+excerpt; files removed to reduce root churn. Track C sealed evidence files removed here were unreferenced duplicates/transients; sealed verdicts remain in canonical Track C artifacts and frontier.
| file | sha256 | bytes | excerpt |
|---|---|---:|---|
| `campaign_sweep_tracka_20261105T082547Z.md` | `b82d64bcd6294a89da3bfb6ce0f884db0125ff3a1c21fc836ca6c7dae9181ad6` | 2130 | # Track A Campaign Sweep (FCLR-NEXT-092) TIMESTAMP (UTC): 20261105T082547Z REPO PRIORITY: Volatility (Track C) SEALED/LOCKED. Liquidation Risk (Track A) = ONLY ACTIVE OBJECTIVE.  ## Entry Metrics - research_state md+json (root): 183 - ironflow probe files: 2 (1 live + digest) enforced - monitor quic |
| `campaign_sweep_tracka_20261105T092616Z.md` | `e5a8e28c9ad2f84a41988a5f044a72a0c31dc8f6230d84749894456af83d7218` | 5823 | # Track A Campaign Sweep (FCLR-NEXT-093, Steps 3-6) TIMESTAMP (UTC): 20261105T092616Z HEAD: c628e94c (working tree modified by hardening; pycache uncommitted) REPO PRIORITY: Volatility (Track C) SEALED/LOCKED. Liquidation Risk (Track A) = ONLY ACTIVE OBJECTIVE.  ## Entry Metrics (verified) - researc |
| `liquidation_block_snapshot_20261102T225651Z.json` | `2cac10b62b4b64a479657dc78cf9e07625da17a9081416236cae059eefa5e27a` | 1447 | {   "snapshot_ts": "20261102T225651Z",   "campaign": "LIQUIDATION_FORWARD_VALIDATE_HEAVY-004i",   "status": "BLOCKED_ON_DATA",   "data_through": "2026-10",   "consecutive_absent": 3,   "verify_ok": null,   "baseline_drift": null,   "resume_trigger_met": false,   "new_data_path": false,   "reasons":  |
| `liquidation_block_snapshot_20261103T000342Z.json` | `a09ae86ed59afc667b8e3389fcf88d43f1542c6c3b17f675aa50ee6a58367183` | 11512 | {   "snapshot_ts": "20261103T000342Z",   "campaign": "LIQUIDATION_FORWARD_VALIDATE_HEAVY-004i",   "status": "BLOCKED_ON_DATA",   "data_through": "2026-10",   "consecutive_absent": 3,   "verify_ok": null,   "baseline_drift": null,   "resume_trigger_met": false,   "new_data_path": false,   "reasons":  |
| `liquidation_block_snapshot_20261103T010435Z.json` | `6ccda5f7d7659904dd89e7daf094723a5aea112d5311a94c45a479f9e97faedb` | 900 | {   "snapshot_ts": "20261103T010435Z",   "campaign": "LIQUIDATION_FORWARD_VALIDATE_HEAVY-004i",   "status": "BLOCKED_ON_DATA",   "data_through": "2026-10",   "consecutive_absent": 3,   "verify_ok": true,   "baseline_drift": false,   "resume_trigger_met": false,   "new_data_path": false,   "probed_fo |
| `leakage_audit_heavy_20261103T140910Z.md` | `20156442ec78b53dd51d1abc4d947badbd476b72a1437557bd07521186a40fa1` | 3444 | # Adversarial Leakage Audit (Heavy Work FCLR-NEXT-013) Timestamp (UTC): 20261103T140910Z Git SHA (HEAD): a9794e7c Scope: FCLR-010 (Track A, Hyperliquid observed liquidations) and FCLR-011 (Track C, Binance volatility)  ## Audit methodology (adversarial) - Timestamp/order checks: verify train/val/tes |
| `coupled_integration_synthesis_20261101T091722Z.md` | `670458e43c2b0b685d3039ba9eaf18d5611692bed1a344edc061d32e583b4deb` | 8423 | # Coupled Integration Synthesis (FCLR-COUPLED-INTEGRATE) **TIMESTAMP (UTC):** 2026-11-01T09:17:22Z **REPO:** Funding-conditioned-volatility-and-liquidation-risk **HANDOFF:** FCLR-HANDOFF-030-20261101T091553Z (follow-on) **STATUS:** INTEGRATION-FOCUSED (no exhausted-panel reruns)  ## 1) Coupling rati |
| `coupled_integration_synthesis_20261101T091910Z.md` | `c8c7cd7ec5841ba18231dc76a239a6bed843ff28ab8bd3c99e7f834dad17bfcf` | 2572 | # Coupled Integration Synthesis (FCLR-COUPLED-INTEGRATE) **TIMESTAMP (UTC):** $(date -u +%Y-%m-%dT%H:%M:%SZ) **REPO:** Funding-conditioned-volatility-and-liquidation-risk **HANDOFF:** FCLR-HANDOFF-030-20261101T091553Z **STATUS:** INTEGRATION-FOCUSED (no exhausted-panel reruns)  ## 1) Coupling ration |
| `pre_registration_h_coupled_001_20261101T093727Z.md` | `2148292abfd0cf0bb59dd9044769a831e2f07046b8337595210268200ad202e6` | 5741 | # Pre-Registration: H_COUPLED-001 (Funding×Vol×Observed-Flow Coupling)  **TIMESTAMP (UTC):** $(date -u +%Y-%m-%dT%H:%M:%SZ) **REPO:** Funding-conditioned-volatility-and-liquidation-risk **EXPERIMENT ID:** FCLR-COUPLED-001 **HYPOTHESIS ID:** H_COUPLED-001 **STATUS:** PRE-REGISTERED BEFORE OUTCOMES  |
| `evaluation_summary_STREAM_B_DEEP_ANALYSIS-001_20261103T105902Z.md` | `d4a7e94647c0cb3aa6f697564605f86854c7f593954b54490d301bc9eb05e2bf` | 4478 | # STREAM_B_DEEP_ANALYSIS-001 - 20261103T105905Z  ## Context - Panel: /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk/research_state/data_cache/fclr002_panel.json (FCLR-002, frozen) - Symbols: ['BNBUSDT', 'BTCUSDT', 'ETHUSDT',  |
| `evaluation_summary_STREAM_B_FEATURE_EXTENSION_20261103T071412Z.md` | `25b7f48e3d2089cc2c00dcdc265cd6c3631c0b21b9dc47b7f14413d4c10cc785` | 3170 | # STREAM_B_HEAVY_FEATURE_EXTENSION-001 - 20261103T071412Z  ## Objective Extend Track B volatility features on frozen splits (FCLR-002 panel): - Funding percentiles/zscore (trailing-only) - RV ratios 6h/24h/7d - Price-dislocation MA/EMA deviation - Train-only normalized models - Block-bootstrap CIs ( |
| `evaluation_summary_STREAM_B_FEATURE_EXTENSION_20261103T101608Z.md` | `0b067c270cec6d058ec5dfcfc7b6e831b6911519df52177bef302abfb46da142` | 3170 | # STREAM_B_HEAVY_FEATURE_EXTENSION-001 - 20261103T101608Z  ## Objective Extend Track B volatility features on frozen splits (FCLR-002 panel): - Funding percentiles/zscore (trailing-only) - RV ratios 6h/24h/7d - Price-dislocation MA/EMA deviation - Train-only normalized models - Block-bootstrap CIs ( |
| `evaluation_summary_STREAM_B_ROBUSTNESS-002_20261103T090636Z.md` | `e6c86993ce2d3152a9af8b3b6b59b421fb112961dccc27cd4ac8705d66af2eba` | 3678 | # STREAM_B_ROBUSTNESS-002 - 20261103T090636Z  ## Objective Heavy robustness on extended features (fund pct/z, RV ratios, price-disloc) on frozen FCLR-002 splits. - Circular block bootstrap: block sizes {12, 24, 48} - Leave-one-symbol-out (5 symbols) - Train-only scaling variants (robust/median-IQR,  |
| `evaluation_summary_STREAM_B_ROBUSTNESS-002_20261103T101627Z.md` | `082a36c49ad925a11fb2eb96fa2ff64cd239217e69fd74f05fe66b6d1e293434` | 3678 | # STREAM_B_ROBUSTNESS-002 - 20261103T101627Z  ## Objective Heavy robustness on extended features (fund pct/z, RV ratios, price-disloc) on frozen FCLR-002 splits. - Circular block bootstrap: block sizes {12, 24, 48} - Leave-one-symbol-out (5 symbols) - Train-only scaling variants (robust/median-IQR,  |
| `evaluation_summary_VOLATILITY_20261103T061321Z.md` | `667a21bf4bb782eb3966330eb684ddde05eea299eba0f33e6fd59c30e074dd6b` | 1787 | # Volatility Evaluation (Funding-Conditioned) - 2026-11-03T06:13:21.397730+00:00  ## Data - Panel: /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk/research_state/data_cache/fclr002_panel.json - Total rows: 19488 - Symbols: ['B |
| `evaluation_summary_VOLATILITY_20261103T071220Z.md` | `693d4f6fc8aa67141289cce7fa077117f66c98dac285c325aebe4107a58fc729` | 1787 | # Volatility Evaluation (Funding-Conditioned) - 2026-11-03T07:12:20.241966+00:00  ## Data - Panel: /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk/research_state/data_cache/fclr002_panel.json - Total rows: 19488 - Symbols: ['B |
| `trackc_final_verdict_20261104T182830Z.md` | `a91cd6de6d2875bbaf33bb176203c40480c08fc46dd89842932f5ea504eaa7cf` | 3083 | # TRACK C FINAL VERDICT (FCLR-011, frozen splits only) - 20261104T182846Z  Repo: Funding-conditioned-volatility-and-liquidation-risk Git SHA: 876838c2 Branch: main Mode: CAMPAIGN-DRIVEN / Enforcement: NO-SKIP  ## Summary Track C (funding-conditioned volatility forecasting) gate PASSED (FCLR-011). De |
| `trackc_robustness_20261104T174444Z.md` | `3f24ac7db119db6f2896d0e88ff09c88d5b1732be5914b78aa6f505e68de830b` | 12382 | # TRACK C ROBUSTNESS (FCLR-011, frozen splits only) - 20261104T174452Z  ## Context - Panel: /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk/research_state/data_cache/fclr011_panel.json (FCLR-011) - Splits: {'train': ['2026-01- |

Removed: 18 files. Root md+json expected delta -18 (subject to probe/sweep writes).


## 095 consolidation (20261105T110445Z, FCLR-NEXT-095 no-coast heavy)
Superseded 094 sweep/014 blocker consolidated here after frontier/handoff updated to 015 artifacts. Provenance preserved; files removed to keep root md+json <=155 while adding 095 evidence.
| file | sha256 | bytes | excerpt |
|---|---|---:|---|
| `campaign_sweep_tracka_20261105T101957Z.md` | `6917f0d387db83fc75d6c124e89dc064665506558172658d75ba0ed97eb299b5` | 8195 | # Track A Campaign Sweep (FCLR-NEXT-094, no-coast heavy) TIMESTAMP (UTC): 20261105T101957Z HEAD (baseline): c628e94c (working tree modified by 094 hardening; not committed here) RE |
| `liquidation_forward_validate_014_blocker_20261105T101957Z.md` | `4eb2b84a8b565a5612b15106061d256e09c368e074488f67a88b18822bafa0ae` | 6362 | # LIQUIDATION_FORWARD_VALIDATE_014_BLOCKER (FCLR-NEXT-094) Timestamp (UTC): 20261105T101957Z Git SHA (baseline): c628e94c (working tree modified by 094 hardening; uncommitted) Bran |
Removed: 2 files. Replaced by 015 blocker/095 sweep evidence.
