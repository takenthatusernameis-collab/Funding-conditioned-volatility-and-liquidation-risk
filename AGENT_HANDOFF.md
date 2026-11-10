# AGENT_HANDOFF.md — Single Durable Handoff (REPO-NAME PRIORITY: liquidation risk Track B first, then volatility Track C; Track A observed liquidations STRUCTURALLY_BLOCKED)

**Updated:** 2026-11-10T17:38:38Z — **SINGLE DURABLE HANDOFF (PROGRAM NOT CONCLUDED).** Track B confirmatory on untested TB1 window (2025-01-01..2026-10-31, 5 symbols, ~22 non-overlapping 30-day blocks) is the mandatory next heavy task (M5.2 prereg freeze before outcomes → M5.3 execution → M5.4 verdict). Track C H1_primary NOT_SUPPORTED (all claim-worthy panels exhausted); Track A STRUCTURALLY_BLOCKED; risk overlay INELIGIBLE. Provenance re-verified: `PROVENANCE_OK 161`. See `NEXT_SESSION_TASK.md`.

**Session preflight (last verified 2026-11-10T17:38:38Z):** `PROVENANCE_OK 161` (funding CSV lineage, unmapped=0). Canonical Track B/C/provenance tests green in-session context; rerun verification commands before execution. No env/data bottleneck — blocker is procedural M5.2 frozen prereg+hash recorded before outcomes on TB1.

**Correction vs prior handoff:** `next_unfinished_task` was incorrectly NONE. Untested admissible local Track B windows with >=3 non-overlapping 30-day blocks remain:
- TB1 panel 2025-01-01..2026-10-31, 5 symbols, provenance_verified=true (2065 files verified, unmapped_count=0), 22 estimated non-overlapping 30-day blocks — fully verified locally, **untested** for Track B confirmatory. (`research_state/trackb_TB1_admissibility.json`)
- 2024-01-01..2024-09-30 panel, 5 symbols, completeness 1.0, ~9 estimated blocks — fast-local signal only; needs deep admissibility + gap + funding-schema audit + checksum/provenance lineage before confirmatory. (`research_state/trackb_window_candidates_fast.json`)

The only blocker to confirmatory resume is the missing NEW frozen prereg (procedural), not data. No network/new data required. TB1 admissibility is already machine-verified; proceed directly to M5.2 frozen prereg then M5.3 execution.

---

## 🔴 INITIAL TASK MESSAGE FOR NEXT AGENTIC SESSION — 2026-11-10T17:38:38Z (supersedes prior; see NEXT_SESSION_TASK.md)

**Campaign:** `TRACKB-MODELED-BREACH-TB1-20261110T173838Z` — Track B modeled liquidation boundary-breach confirmatory on untested TB1 window (repo-name priority #1: liquidation risk). Execute M5 heavily; do not stop at planning.

**Mandatory steps (in order; skipping is non-compliant):**

**M5.1 Admissibility lock (verifiable):** TB1 panel 2025-01-01..2026-10-31 admissibility already saved at `research_state/trackb_TB1_admissibility.json` (provenance_verified=true, unmapped_count=0, 5 symbols BTCUSDT/ETHUSDT/BNBUSDT/SOLUSDT/XRPUSDT, 22 estimated non-overlapping 30-day blocks, all required series complete, funding schema OK). Verify with the provenance command below. If re-auditing the 2024-01-01..2024-09-30 fallback, use `trackc_panel_admissibility_audit`, `trackc_gap_repair_manifest`, `trackc_funding_schema_audit`, and checksum/provenance lineage. Require: >=5 instruments, contiguous mark/index/premium/klines + funding, >=3 non-overlapping 30-day blocks in test, not sealed / not previously outcome-inspected for this Track B design, `provenance_verified=true`, `unmapped_count==0`. Save `research_state/trackb_<ID>_admissibility.(json|md)`.

**M5.2 Freeze prereg BEFORE outcomes (verifiable):** Write `research_state/research_protocol_trackb_<ID>.md`: modeled breach definition (leverage/margin/horizon/side), predictors incl. funding-conditioned features, 60/20/20 chronological splits + 7-day purge/embargo, metrics, 2% materiality floor, Holm correction, block bootstrap >=2000 reps, explicit "synthetic proxy ≠ observed liquidation". Compute `prereg_hash` = sha256 of frozen protocol content. Record `prereg_hash` and `split_boundaries_trackb_<ID>.frozen_before_outcomes=true` in `research_state/run_manifest.json` **before** any outcome/label inspection.

**M5.3 Execute & evaluate (heavy):** Run Track B pipeline on the frozen panel (`scripts/run_trackb_evaluation.py` + `scripts/synthetic_boundary_labels.py`); output `research_state/evaluation_summary_trackb_<ID>.md` with point estimate, 95% CI, relative change, n_instruments, n_obs, n_test_blocks, materiality/gate decision.

**M5.4 Verdict & propagation:** Update `research_state/hypothesis_registry.json`, `research_state/experiment_frontier.json`, `research_state/negative_results_report.md`, `AGENT_HANDOFF.md`, `NEXT_SESSION_TASK.md`. Risk overlay NOT ELIGIBLE unless all gates pass. Record exact `next_unfinished_task`.

**Current state:** `next_unfinished_task` = Track B M5 on TB1 (2025-01-01..2026-10-31): freeze prereg+hash before outcomes → execute evaluation → verdict/propagation. TB1 admissibility verified (`research_state/trackb_TB1_admissibility.json`), provenance OK 161. Do not relitigate concluded tracks. No network/paid/manual/credentialed data; no fabricated data/provenance; no threshold shopping; no sealed-holdout reuse; no Track A/B/C conflation (synthetic proxy ≠ observed liquidation); no risk overlay before gate pass; no `.github/workflows` edits.

**Verification commands:**
- `python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_funding_schema_audit tests.test_trackc_provenance_lineage -v`
- Provenance: `python -c "from scripts.trackc_provenance_lineage import verify_paths_with_manifests; from pathlib import Path; res=verify_paths_with_manifests([str(p) for p in Path('research_state/data_cache').rglob('*-fundingRate-*.csv')], repo_root=Path('.')); assert res['provenance_verified'] and res['unmapped_count']==0; print('PROVENANCE_OK', res['files_considered'])"`