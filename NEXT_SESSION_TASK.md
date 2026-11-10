# NEXT_SESSION_TASK.md — SINGLE DURABLE HANDOFF (2026-11-10T17:43:04Z)

**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Priority (by repo name):** (1) Track B liquidation risk — modeled boundary breaches (**active, TB1 prereg frozen; execution pending**), (2) Track C funding-conditioned volatility (**concluded NOT_SUPPORTED on claim-worthy local panels**), (3) Track A observed liquidations (**STRUCTURALLY_BLOCKED**).
**Campaign:** `TRACKB-MODELED-BREACH-TB1-20261110T173838Z`
**Program status:** `ACTIVE_TRACKB_TB1_FROZEN_PENDING_EXECUTION` — not concluded.

## STATE (verified)
- **Track B prior:** `TRACKB-20251110T154307Z` (2025-01-01..2025-10-31) gate NOT_MET/NOT_SUPPORTED (C2 vs B1 +1.50% < 2%, CI [-0.005,0.035]; synthetic proxy only).
- **TB1 window (untested confirmatory design):** 2025-01-01..2026-10-31, symbols BTCUSDT/ETHUSDT/BNBUSDT/SOLUSDT/XRPUSDT, ~22 non-overlapping 30d blocks (`research_state/trackb_TB1_admissibility.json`).
- **Bottleneck removed (this session):** TB1 protocol frozen and manifest prereg recorded **before outcomes**:
  - `research_state/research_protocol_trackb_TB1_20261110T173838Z.md` (FROZEN_BEFORE_OUTCOMES)
  - `research_state/run_manifest.json` → `split_boundaries_trackb_TB1_20261110T173838Z` with `frozen_before_outcomes=true`, `outcome_values_inspected=false`, `prereg_hash=ed64c5ff10cebf1f333cb9b4a140a858e183b369a6c168d475c5f6494795729a`
- **Provenance:** `PROVENANCE_OK 161` (funding CSV lineage verified 2026-11-10T17:38Z, unmapped=0).

## SINGLE MANDATORY TASK — HEAVY EXECUTION (no planning-only, no relitigation)
**`next_unfinished_task`:** Execute full confirmatory Track B M5 on frozen TB1 (`trackb_TB1_20261110T173838Z`), produce evaluation + verdict, and propagate state. **Do not** recompute/reinspect outcomes before trusting frozen manifest state (freeze is recorded), do not relitigate Track C/A, do not stop at narration.

### 1) Confirm freeze/provenance (quick gate)
- Confirm manifest has `split_boundaries_trackb_TB1_20261110T173838Z.frozen_before_outcomes==true` and hash matches protocol.
- Re-run provenance verification and record result in evaluation artifacts:
  `python -c "from scripts.trackc_provenance_lineage import verify_paths_with_manifests; from pathlib import Path; res=verify_paths_with_manifests([str(p) for p in Path('research_state/data_cache').rglob('*-fundingRate-*.csv')], repo_root=Path('.')); assert res['provenance_verified'] and res['unmapped_count']==0; print('PROVENANCE_OK', res['files_considered'])"`

### 2) Execute evaluation (substantive heavy work)
- Run Track B pipeline for TB1 frozen design (2025-01-01..2026-10-31, 60/20/20 chronological, 7d purge/embargo, test >=3 non-overlapping 30d blocks) using `scripts/synthetic_boundary_labels.py` and existing Track B primitives (`scripts/run_trackb_evaluation.py` as reference/adapt as needed) with train-only fitting and leakage-safe labeling.
- Primary: `synthetic_boundary_breach_h24_long_5x_m0` (C2 vs B1), materiality floor 2%, Holm across pre-specified contrasts, block bootstrap >=2000, 95% CI.
- Output `research_state/evaluation_summary_trackb_TB1_20261110T173838Z.md` with: point estimate, 95% CI, relative change, n_instruments, n_obs, n_test_blocks, materiality/gate decision, Holm, and explicit **"synthetic proxy ≠ observed liquidation"** caveat.

### 3) Verdict & propagation (single coherent state)
- Update `research_state/hypothesis_registry.json`, `research_state/experiment_frontier.json`, `research_state/negative_results_report.md`, `AGENT_HANDOFF.md`, and this file.
- Keep risk overlay **NOT ELIGIBLE** unless all pre-registered gates pass.
- Set singular `next_unfinished_task`:
  - gates not met but another admissible untested >=3-block Track B window remains → that specific window + frozen prereg then M5;
  - all admissible local >=3-block Track B/C routes exhausted with preserved results → `NONE — program concluded under constraints pending new admissible unauthenticated source` (Track A remains STRUCTURALLY_BLOCKED).

## Acceptance (session incomplete without)
- TB1 frozen prereg + hash verified in manifest before-outcomes (done; must remain intact).
- Machine-verified provenance evidence recorded.
- `evaluation_summary_trackb_TB1_20261110T173838Z.md` with CIs/blocks/gate verdict.
- Registries + `AGENT_HANDOFF.md` + this file updated; `next_unfinished_task` singular and evidence-backed.

## Verification
- `python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_funding_schema_audit tests.test_trackc_provenance_lineage -v`
- Provenance command above.

## Hard constraints (NON-NEGOTIABLE)
No network/paid/manual/credentialed data; no fabricated data/provenance; no threshold shopping; no sealed-holdout reuse; no Track A/B/C conflation (Track B = modeled synthetic breach proxies, never observed liquidations); preregister/freeze before outcomes; no risk overlay until forecast gate passes; no `.github/workflows` edits. Future agents must deliver heavy, verifiable progress.
