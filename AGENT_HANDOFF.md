# AGENT_HANDOFF.md — Single Durable Handoff (REPO-NAME PRIORITY: liquidation risk Track B first, then volatility Track C; Track A observed liquidations STRUCTURALLY_BLOCKED)

**Updated:** 2026-11-10T17:43:04Z — **SINGLE DURABLE HANDOFF (PROGRAM NOT CONCLUDED).** TB1 (2025-01-01..2026-10-31, 5 symbols, ~22 30d blocks) **prereg frozen before outcomes** (bottleneck removed): `research_state/research_protocol_trackb_TB1_20261110T173838Z.md`, manifest `split_boundaries_trackb_TB1_20261110T173838Z` `frozen_before_outcomes=true`, `prereg_hash=ed64c5ff10cebf1f333cb9b4a140a858e183b369a6c168d475c5f6494795729a`. **Mandatory next: heavy execution M5.3 evaluation + M5.4 verdict/propagation** for TB1. Track C H1_primary NOT_SUPPORTED (claim-worthy panels exhausted); Track A STRUCTURALLY_BLOCKED; risk overlay INELIGIBLE. Provenance `PROVENANCE_OK 161`. See `NEXT_SESSION_TASK.md`.

**Session preflight (last verified 2026-11-10T17:43:04Z):** `PROVENANCE_OK 161` (funding CSV lineage, unmapped=0). TB1 freeze/provenance gates satisfied; no env/data/procedural prereg blocker — next blocker is execution throughput only (run full TB1 evaluation and record verifiable verdict).

**Correction vs prior handoff:** `next_unfinished_task` was incorrectly NONE. Untested admissible local Track B windows with >=3 non-overlapping 30-day blocks remain:
- TB1 panel 2025-01-01..2026-10-31, 5 symbols, provenance_verified=true (2065 files verified, unmapped_count=0), 22 estimated non-overlapping 30-day blocks — fully verified locally, **untested** for Track B confirmatory. (`research_state/trackb_TB1_admissibility.json`)
- 2024-01-01..2024-09-30 panel, 5 symbols, completeness 1.0, ~9 estimated blocks — fast-local signal only; needs deep admissibility + gap + funding-schema audit + checksum/provenance lineage before confirmatory. (`research_state/trackb_window_candidates_fast.json`)

The only blocker to confirmatory resume is the missing NEW frozen prereg (procedural), not data. No network/new data required. TB1 admissibility is already machine-verified; proceed directly to M5.2 frozen prereg then M5.3 execution.

---

## 🔴 INITIAL TASK MESSAGE FOR NEXT AGENTIC SESSION — 2026-11-10T17:43:04Z (supersedes prior; see NEXT_SESSION_TASK.md)

**Campaign:** `TRACKB-MODELED-BREACH-TB1-20261110T173838Z` — Track B modeled liquidation boundary-breach confirmatory (repo-name priority #1). **M5.1 admissibility & M5.2 prereg freeze are COMPLETE (bottlenecks removed).** Execute M5.3/M5.4 heavily; do not stop at planning or relitigate Track C/A.

**Completed (verified):**
- Admissibility: `research_state/trackb_TB1_admissibility.json` (2025-01-01..2026-10-31, 5 symbols, contiguous, 22 est. 30d blocks, series/funding schema OK, provenance gate evidence recorded).
- Freeze-before-outcomes: `research_state/research_protocol_trackb_TB1_20261110T173838Z.md`; `research_state/run_manifest.json` `split_boundaries_trackb_TB1_20261110T173838Z` `frozen_before_outcomes=true`, `outcome_values_inspected=false`, `prereg_hash=ed64c5ff10cebf1f333cb9b4a140a858e183b369a6c168d475c5f6494795729a`.

**Mandatory next (in order, non-optional):**
- **M5.3 Execute & evaluate (heavy):** Run frozen TB1 evaluation (60/20/20, 7d purge/embargo, test >=3 blocks) with leakage-safe labels/features (`scripts/synthetic_boundary_labels.py`; adapt/reuse `scripts/run_trackb_evaluation.py` as needed). Primary: `synthetic_boundary_breach_h24_long_5x_m0`, C2 vs B1, >=2% materiality, Holm, block bootstrap >=2000, 95% CI. Write `research_state/evaluation_summary_trackb_TB1_20261110T173838Z.md` with point estimate, CI, relative change, n_instruments, n_obs, n_test_blocks, gate verdict, Holm, and explicit **synthetic proxy ≠ observed liquidation**.
- **M5.4 Verdict & propagation:** Update `research_state/hypothesis_registry.json`, `research_state/experiment_frontier.json`, `research_state/negative_results_report.md`, `AGENT_HANDOFF.md`, `NEXT_SESSION_TASK.md`. Risk overlay NOT ELIGIBLE unless all gates pass. Set singular evidence-backed `next_unfinished_task` (next untested >=3-block window+prereg, or `NONE — program concluded under constraints pending new admissible unauthenticated source` if all local admissible routes exhausted; Track A remains STRUCTURALLY_BLOCKED).

**Current `next_unfinished_task`:** M5.3–M5.4 on frozen TB1 (`trackb_TB1_20261110T173838Z`). No network/paid/manual/credentialed data; no fabricated data/provenance; no threshold shopping; no sealed-holdout reuse; no Track A/B/C conflation; no `.github/workflows` edits.

**Verification commands:**
- `python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_funding_schema_audit tests.test_trackc_provenance_lineage -v`
- Provenance: `python -c "from scripts.trackc_provenance_lineage import verify_paths_with_manifests; from pathlib import Path; res=verify_paths_with_manifests([str(p) for p in Path('research_state/data_cache').rglob('*-fundingRate-*.csv')], repo_root=Path('.')); assert res['provenance_verified'] and res['unmapped_count']==0; print('PROVENANCE_OK', res['files_considered'])"`