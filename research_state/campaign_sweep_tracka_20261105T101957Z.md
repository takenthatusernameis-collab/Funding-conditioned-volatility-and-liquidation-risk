# Track A Campaign Sweep (FCLR-NEXT-094, no-coast heavy)
TIMESTAMP (UTC): 20261105T101957Z
HEAD (baseline): c628e94c (working tree modified by 094 hardening; not committed here)
REPO PRIORITY: Volatility (Track C) SEALED/LOCKED. Liquidation Risk (Track A) = ONLY ACTIVE OBJECTIVE.

## Entry Metrics (verified, irrefutable)
| Metric | Before 094 (post-093 state) | After 094 | Delta |
|---|---:|---:|---:|
| research_state root `*.md+*.json` | 153 (pre-artifact count this session; 093 reported 169/171 evolving with probes/caches) | 155 (includes this sweep + 014 blocker; canonical outputs only) | +2 required evidence artifacts; **-18 unreferenced timestamped families removed** (net churn reduction vs 153+18 potential) |
| ironflow probe artifacts | 2 (`ironflow_probe_20261105T101210Z.json` + `ironflow_probe_digest_latest.json`) | 2 (unchanged) | 0 |
| recurring timestamped probe/scan families (non-canonical) | 0 created; 18 unreferenced timestamped files found removable | 0 | 18 consolidated/removed |
| full test suite | 173 OK baseline context (093) | **190 tests OK** (`python -m unittest discover tests`) | +17 new 094 adversarial/resume tests |
| harness cold / offline resume proof | rubric+harness import path ~20ms observed | rubric+harness+manifest+prereg-block command block **~0.040s real** (<10s) | proven+enforced |
| monitor quick trigger | NO RESUME TRIGGER (cached/state check) | NO RESUME TRIGGER | no new data |

## Trigger Probe Evidence (exhaustive, no outcome inspection)
- `python scripts/monitor_ironflow_liquidations.py --quick`: **NO RESUME TRIGGER**. `data_through=2026-10`; probed `2026-11,2026-12,2027-01,2027-02`; `head_probes=8`; `cached_hits=0`; `probe_diff(added=0 changed=0 removed=0)`; `baseline_drift(intact=True regressions=0 content_replaced=0 pairs_checked=18 method=state_only_tree_unchanged)`; `kaggle_mirror(updated=False last=2026-11-01T06:18:48.21Z triggered=False)`. Live probe retained canonical: `research_state/ironflow_probe_20261105T101210Z.json`; digest `ironflow_probe_digest_latest.json`.
- `python scripts/deep_review_alt_sources.py`: canonical `research_state/alt_source_deep_review_latest.md` updated; `cache_hits=13 cache_misses=1`; **no GO**.
- `python scripts/hunt_alternative_liquidation_sources.py`: canonical `research_state/alt_source_scan_latest.json`; `candidates=11, source=cache`; **no GO**.
- Decision: **NO NEW DATA - ON HOLD**. No prereg created. No outcomes inspected.

## Step 2 — Churn/Artifact Audit (measurable, zero removable ambiguity)
Timestamped root inventory (pre-removal scan): 35 timestamped root `md+json` names; **19 unreferenced** candidates identified by corpus check across `AGENT_HANDOFF.md`, `experiment_frontier.json`, `run_manifest.json`, scripts/tests, and canonical Track A histories. `ironflow_trend_digest_20261102T220326Z.json`/`ironflow_trend_report_20261102T220326Z.json` **kept** (referenced by history/digest refs). The live probe `ironflow_probe_20261105T101210Z.json` is canonical (not removable).

**Removed 18 unreferenced timestamped files** (sha256+bytes+excerpt preserved in `research_state/tracka_bottleneck_history_090.md` §094): `campaign_sweep_tracka_20261105T082547Z.md`, `campaign_sweep_tracka_20261105T092616Z.md`, `liquidation_block_snapshot_20261102T225651Z.json`, `liquidation_block_snapshot_20261103T000342Z.json`, `liquidation_block_snapshot_20261103T010435Z.json`, `leakage_audit_heavy_20261103T140910Z.md`, `coupled_integration_synthesis_20261101T091722Z.md`, `coupled_integration_synthesis_20261101T091910Z.md`, `pre_registration_h_coupled_001_20261101T093727Z.md`, `evaluation_summary_STREAM_B_DEEP_ANALYSIS-001_20261103T105902Z.md`, `evaluation_summary_STREAM_B_FEATURE_EXTENSION_20261103T071412Z.md`, `evaluation_summary_STREAM_B_FEATURE_EXTENSION_20261103T101608Z.md`, `evaluation_summary_STREAM_B_ROBUSTNESS-002_20261103T090636Z.md`, `evaluation_summary_STREAM_B_ROBUSTNESS-002_20261103T101627Z.md`, `evaluation_summary_VOLATILITY_20261103T061321Z.md`, `evaluation_summary_VOLATILITY_20261103T071220Z.md`, `trackc_final_verdict_20261104T182830Z.md`, `trackc_robustness_20261104T174444Z.md`. Track C/B sealed conclusions remain in canonical frontier/artifacts; removed Track C/stream-b files were unreferenced duplicates/transients.

`research_state/watch/` contains 28 `trigger_harden_20261104T*.json` (unchanged; generator scripts unchanged) plus 6 non-trigger files (`exhaustive_binance_probe_*`, `fclr002_replication_summary_*`, `gap_analysis_*`, `prereg_gating_proof_*`) — retained (not new this session). No new timestamped families created.

## Step 3 — Stricter Adversarial Rubric + Resume Proof (concrete)
- `scripts/tracka_rubric.py` hardened (additive fail-closed): normalized Hyperliquid venue aliases (`hyperliquid|hl|hyperliquid_perp|hyperliquid-perp`) with explicit `venue_alias_spoof` rejection; duplicate symbol detection; conflicting `symbol_count` claims rejected; `partial_month_coverage`/`coverage_complete_months` claim rejection; `schema_conflicts` (bool/list) rejection; `row_mix_observed_modeled` rejection; `timestamp_normalized_utc=false` rejection when schema present; deterministic sorted failures.
- `tests/test_tracka_adversarial_rubric_094.py` added (**17 tests**, all green): partial month coverage flag/zero-complete-months, conflicting schema fields (list/bool), duplicate symbols, symbol alias casing normalization accepted, conflicting symbol-count claim, mixed observed+modeled rows, missing timestamp normalization, venue casing accepted, `HL` alias accepted, venue alias spoof rejected, unknown venue alias rejected, fail-closed missing fields, deterministic sorted failures. Combined with 093 (17 tests): **34 rubric adversarial tests** green.
- Offline resume proof (single command block, enforced): rubric import/assess + fixture manifest load + `FCLR010Harness` cold + `evaluate_forward(..., pre_reg_path=None)` blocked. **~0.040s real** (<10s). CLI `scripts/fclr010_harness.py` <10s. Enforced by `TestOfflineResumeProof094`.
- Proven command: `python -c "from scripts.tracka_rubric import assess_candidate; from scripts.fclr010_harness import FCLR010Harness; import json,tempfile; from pathlib import Path; assess_candidate({'venue':'hyperliquid','unauthenticated':True,'requires_api_key':False,'requires_signature':False,'requester_pays':False,'observed_liquidations':True,'modeled_or_proxy':False,'merges_non_hyperliquid':False,'symbol_count':6,'completeness_documented':True,'license_ok':True,'schema_fields':['timestamp','symbol','liquidation_notional'],'timestamp_normalized_utc':True}); json.load(open('tests/fixtures/tracka/manifest.json')); h=FCLR010Harness(); assert h.evaluate_forward(Path('/nonexistent'),Path(tempfile.mkdtemp()),pre_reg_path=None)['status']=='BLOCKED'; print('ok')"`

## Step 4 — Safe Side-Effect Churn Reduction (proof)
- Existing monitor isolation tests verified green: `TestQuickPathPersistence` (2) + `TestProbeArtifactSafety` (1) — run with temp `EVIDENCE_DIR/STATE_PATH`; assert **no real `research_state/ironflow_probe_*` artifacts created outside tmp dirs** and real probe artifact count remains 2. Full suite green (**190 OK**). No unsafe monitor code-path changes made; isolation proof is test-enforced.
- Hunt/deep_review canonical latest outputs preserved (`alt_source_scan_latest.json`, `alt_source_deep_review_latest.md`); caches used (`cache_hits` observed).

## Resume Condition (only)
- ironflow `data/events/YYYY-MM.parquet` or `data/fills/YYYY-MM.parquet` for month>=2026-11 returns HTTP 200 unauthenticated, OR
- admissible unauthenticated Hyperliquid-only source passes strict GO rubric (`scripts/tracka_rubric.py`): Hyperliquid venue (normalized aliases allowed, spoof rejected), observed-only, no modeled/proxy/mixed rows, no auth/key/signature/requester-pays, completeness documented, schema compatible (`timestamp,symbol,liquidation_notional`), `timestamp_normalized_utc` when schema present, >=5 unique symbols, no partial-month/coverage/schema conflicts, license OK, Hyperliquid-only firewall.
- **PREREGISTER BEFORE INSPECTING OUTCOMES**. No holdout reuse/retuning/threshold-shopping/track merge. No workflow/scheduler/poller/controller changes.
