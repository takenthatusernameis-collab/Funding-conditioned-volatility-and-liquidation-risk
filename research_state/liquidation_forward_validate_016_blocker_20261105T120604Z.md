# Track A Forward Validation Blocker — 016 (FCLR-NEXT-096)

**Timestamp (UTC):** 20261105T120604Z
**Task:** FCLR-NEXT-096-TRACK-A-NO-COAST-WATCH-CONSOLIDATION-RUBRIC-PROVENANCE
**Status:** **BLOCKED (data-gated, no rubric-GO source)** — measurable hardening delta delivered; no resume trigger.
**HEAD (baseline):** fe487722

## Blocker (irrefutable)
- `python scripts/monitor_ironflow_liquidations.py --quick` (20261105T120604Z): **No resume trigger**. `data_through=2026-10`. Probed `2026-11,2026-12,2027-01,2027-02` (events/fills parquet paths) — **absent**. head_probes=8, cached_hits=0, probe_diff added=0/changed=0/removed=0. `baseline_drift(intact=True regressions=0 content_replaced=0 pairs_checked=0 method=state_only_tree_unchanged)`. kaggle_mirror unchanged/triggered false.
- `python scripts/deep_review_alt_sources.py` / `python scripts/hunt_alternative_liquidation_sources.py`: canonical latest refreshed (cache); **no rubric-GO admissible unauthenticated Hyperliquid observed-liquidation source**.
- **No prereg created. No outcome inspection.** Resume condition unmet.

## Measured hardening delta (096)
| Area | Before (095) | After (096) | Evidence |
|---|---:|---:|---|
| Root `research_state/*.md+*.json` | 155 | 157 (+2 required evidence) | `campaign_sweep_tracka_20261105T120604Z.md`, this blocker |
| Ironflow probes | 2 | 2 | canonical digest+latest only |
| Tests | 208 OK | **226 OK** | `python -m unittest discover tests` |
| Rubric adversarial | 52 (093-095) | **67** (+096=15) | `tests/test_tracka_adversarial_rubric_096.py` |
| Monitor isolation | prior coverage | **+3** `TestVerifyAndDriftSafety` | `tests/test_monitor_ironflow.py` |
| Resume check | PASS <5s | **PASS <5s** JSON contract | `python scripts/tracka_resume_check.py` |
| Watch `trigger_harden_20261104T*` live | 28 files / 144315 bytes | **1 live (2156 bytes) + 27 archived with sha256/excerpt** | `research_state/watch/archive/trigger_harden_20261104T_096_archive.json`; live kept `trigger_harden_20261104T113550Z.json` for generator glob compatibility |

## Watch consolidation compatibility/provenance
Superseded 20261104T trigger_harden files moved to `watch/archive/` (27 files). Non-recursive generator globs (`write_trigger_harden_successor.py`, `track_c_inventory_harden.py`) still resolve `prev` to kept live `trigger_harden_20261104T113550Z.json`. Per-file bytes/sha256/excerpt recorded in `trigger_harden_20261104T_096_archive.json`.

## Rubric hardening (096)
`scripts/tracka_rubric.py`: additive fail-closed strict-manifest checks for access/dataset provenance (`observed_access_provenance_missing`), label-definition/observed semantics (`label_definition_missing`), machine-verifiable month/block coverage evidence (`coverage_month_evidence_missing`, `block_count_evidence_insufficient`), claimed-symbols normalization proof completeness (`symbol_normalization_proof_incomplete`), raw-epoch normalization/unit evidence (`timestamp_unit_ambiguous`). `schema_mismatch` preserved. All existing 093-095 tests green.

## Resume instructions
- **Condition:** Hyperliquid `data/events/YYYY-MM.parquet` or `data/fills/YYYY-MM.parquet` month>=2026-11 HTTP 200 unauthenticated **OR** admissible unauthenticated Hyperliquid source passes strict GO rubric. Hyperliquid-only.
- **Before outcomes:** PREREGISTER (freeze splits/metrics/gates; no threshold-shopping). No inspection of outcomes before prereg.
- **On resume:** `python scripts/tracka_resume_check.py`; `monitor --quick`; `deep_review`; `hunt`; full `python -m unittest discover tests`; freeze prereg; execute FCLR-010 harness path per rubric; update frontier/handoff.

## Noncompliance guard
No "blocked/no data" status-only output: this blocker includes measured deltas, archive provenance, test/rubric/resume/isolation proof, and canonical probe evidence. Track C locked. Track B unsupported. No conflation. No workflow/scheduler/poller changes.
