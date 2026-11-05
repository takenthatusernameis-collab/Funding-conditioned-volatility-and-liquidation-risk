# Track A Campaign Sweep — FCLR-NEXT-096 (No-Coast Watch Consolidation + Rubric Provenance)

**Timestamp (UTC):** 20261105T120604Z
**HEAD (baseline):** fe487722 (working tree modified by 096 hardening; not committed)
**Branch:** main
**Task:** FCLR-NEXT-096-TRACK-A-NO-COAST-WATCH-CONSOLIDATION-RUBRIC-PROVENANCE
**Objective:** Measurable hardening delta while Track A blocked (Hyperliquid data_through 2026-10). Volatility (Track C) SEALED/LOCKED; Liquidation Risk (Track A) only active objective.

## Before/after metrics (measured)
| Metric | 095 baseline | 096 after | Delta |
|---|---:|---:|---|
| `research_state` root `*.md+*.json` | 155 | **157** (added this sweep + 016 blocker; required evidence, counted) | +2 required evidence artifacts |
| Ironflow probes (`ironflow_probe_*.json` + `ironflow_probe_digest_latest.json`) | 2 | **2** | 0 (canonical held) |
| `python -m unittest discover tests` | 208 OK | **226 OK** (226 tests) | +18 additive tests |
| Rubric adversarial suites | 093+094+095 = 52 | **093+094+095+096 = 67** | +15 rubric adversarial (096) |
| Monitor verify/drift isolation tests | present | **+3 `TestVerifyAndDriftSafety`** in `tests/test_monitor_ironflow.py` | +3, all green |
| `python scripts/tracka_resume_check.py` | PASS <5s | **PASS <5s** (`"pass": true, "elapsed_s": 0.00076, network:false, writes_real_research_state:false`) | held |
| `research_state/watch/trigger_harden_20261104T*` | 28 files, 144315 bytes (095 inventory value) / 196K du prior to 096 run artifacts | **1 live file (`trigger_harden_20261104T113550Z.json`, 2156 bytes) + 27 archived** | **-27 live files; live bytes 2156 (−98.5% live); 144315 bytes preserved with provenance in archive** |
| New recurring timestamped probe/scan families | none added | **none added** (canonical outputs only) | 0 |

## Entry verification (exact commands)
- `python -m unittest discover tests` → **226 tests, OK**.
- `python scripts/tracka_resume_check.py` → JSON `{"checks":{"harness_cold":true,"fixture_manifest":true,"prereg_block":true,"rubric_fail_closed":true,"rubric_go":true},"elapsed_s":0.000755,"network":false,"pass":true,"writes_real_research_state":false}`.
- `python scripts/monitor_ironflow_liquidations.py --quick` → **No resume trigger**. `data_through=2026-10`, probed `['2026-11','2026-12','2027-01','2027-02']`, head_probes=8, cached_hits=0, probe_diff added=0 changed=0 removed=0, `baseline_drift(intact=True regressions=0 content_replaced=0 pairs_checked=0 method=state_only_tree_unchanged)`, kaggle_mirror unchanged/triggered false.
- `python scripts/deep_review_alt_sources.py` → wrote `research_state/alt_source_deep_review_latest.md` (cache_hits=13 cache_misses=1), canonical latest only.
- `python scripts/hunt_alternative_liquidation_sources.py` → wrote `research_state/alt_source_scan_latest.json` (candidates=11, source=cache), canonical latest only.

## Trigger probe evidence (irrefutable, 20261105T120604Z)
- Ironflow `--quick` probed missing months **2026-11, 2026-12, 2027-01, 2027-02** (`data/events/*.parquet`, `data/fills/*.parquet` pattern): **all absent**; `data_through=2026-10`. No HTTP-200 resume signal for month>=2026-11. No probe_diff change. Baseline drift intact. Kaggle mirror unchanged/triggered false.
- Deep review/hunt refreshed canonical latest outputs; **no rubric-GO source** found. No prereg created. **No outcome inspection**.

## Watch `trigger_harden_20261104T*` consolidation (generator-compatible, tested behavior preserved)
- **Problem (095):** 28 files / 144315 bytes, `zero-safe-removable=0` because generators use `glob('trigger_harden_*.json')` for previous snapshot.
- **Action:** moved 27 superseded 20261104T files to `research_state/watch/archive/` (non-matching glob path). Kept **1 live** latest: `research_state/watch/trigger_harden_20261104T113550Z.json` so `scripts/write_trigger_harden_successor.py` and `scripts/track_c_inventory_harden.py` previous-snapshot glob behavior remains deterministic.
- **Compatibility proof:** `glob('research_state/watch/trigger_harden_*.json')` now returns only the kept live file (non-recursive); simulated generator `prev` resolves to `trigger_harden_20261104T113550Z.json`. Archive path does not match `trigger_harden_*.json` in watch root.
- **Provenance:** `research_state/watch/archive/trigger_harden_20261104T_096_archive.json` records consolidated_utc, generator_compat note, kept_live, archived_count=27, archived_total_bytes, per-file filename/bytes/sha256/excerpt.
- **Delta:** watch root 20261104T count **28 → 1** (−27), live bytes **2156**. Archived bytes preserved with sha256/excerpt.

## Stricter adversarial rubric (096, additive fail-closed) — `scripts/tracka_rubric.py`
Added 096 checks (opt-in strict manifest flags to preserve legacy 093–095 fixture semantics while hardening full admissibility manifests): `access_provenance_required` → fail-closed when observed Hyperliquid source/dataset/access provenance missing (`observed_access_provenance_missing`) and label definition missing (`label_definition_missing`); `label_definition_required` / `strict_observed_semantics` → `label_definition_missing`; `coverage_evidence_required` + `coverage_months>=1` requires machine-verifiable `complete_months_list`; `claims_3x30d_blocks` requires `block_count>=3` and `block_evidence` list with >=3 entries; `symbol_proof_covers_claimed_required` rejects incomplete symbol normalization proof vs claimed symbols (`symbol_normalization_proof_incomplete`); `raw_epoch_fields`/`epoch_timestamp_fields` without `timestamp_normalized_utc` → `timestamp_unit_ambiguous`. Restored `schema_mismatch` in canonical position. **Additive tests:** `tests/test_tracka_adversarial_rubric_096.py` = 15 tests, all green. Existing suites remain green (093=17, 094=17, 095=18). Total rubric adversarial **67**.

## Safe side-effect/churn isolation proof
- Added `tests.test_monitor_ironflow.TestVerifyAndDriftSafety` (3 tests): `verify_state` pure/in-memory with tmp `EVIDENCE_DIR`/`STATE_PATH` creates no files; `check_baseline_drift` state-only with tmp dir writes no files; verify/drift function calls with tmp isolation leave real `research_state` `ironflow_probe_*` mtimes and root `*.md+*.json` count unchanged. All green.
- `scripts/tracka_resume_check.py` remains offline/no-network/no-real-writes, PASS <5s (machine-readable JSON contract intact).

## Rubric cases added (096)
15 deterministic fail-closed/positive cases in `tests/test_tracka_adversarial_rubric_096.py`: strict access provenance missing/present, strict label missing/required flag, coverage months without machine evidence/with complete_months_list, 3x30d claims insufficient count/missing list/with evidence, symbol proof incomplete/covers all (opt-in), raw epoch without/with normalization, strict observed semantics label, base GO.

## Resume instructions (concrete)
1. Run `python scripts/tracka_resume_check.py` (must PASS <5s, no network/writes).
2. Trigger condition only: Ironflow `data/events/YYYY-MM.parquet` or `data/fills/YYYY-MM.parquet` for month>=2026-11 HTTP 200 unauthenticated **OR** admissible unauthenticated Hyperliquid candidate passes strict GO rubric (Hyperliquid-only; observed/modeled never conflated).
3. **PREREGISTER BEFORE INSPECTING OUTCOMES** (freeze splits/metrics/gates; no threshold-shopping; no sealed Track C/B changes). Use existing harness/prereg flow; no outcome inspection before prereg.
4. Re-run `--quick`, `deep_review`, `hunt`, `tracka_resume_check`, full tests; update frontier + single durable handoff with timestamped 097 task.

## Constraints honored
No credentials/manual files/.github/workflows changes. Track C SEALED/LOCKED, Track B NOT_SUPPORTED. Raw data/caches out of git. Canonical outputs only. No new recurring probe/scan timestamped families. No schedulers/pollers/status files/repeated wrappers/agent-controllers. No scope drift.
