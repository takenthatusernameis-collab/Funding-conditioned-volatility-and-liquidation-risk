# NEXT_SESSION_TASK.md — SINGLE DURABLE HANDOFF (2026-11-10T17:14:34Z)

**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Priority (by repo name):** (1) Track B liquidation risk — modeled boundary breaches (**active, untested window remains**), (2) Track C funding-conditioned volatility (**concluded NOT_SUPPORTED on claim-worthy local panels**), (3) Track A observed liquidations (**STRUCTURALLY_BLOCKED**, no admissible unauthenticated census).
**Campaign:** `TRACKB-MODELED-BREACH-TB1-20261110T171434Z`
**Program status:** `ACTIVE_TRACKB_UNTESTED_WINDOW_REMAINS` — not concluded. Prior Track B `TRACKB-20251110T154307Z` (2025-01-01..2025-10-31) NOT_MET/NOT_SUPPORTED (C2 vs B1 +1.50% < 2%, 95% CI [-0.005,0.035], synthetic proxy only). Track C H1_primary NOT_SUPPORTED on all claim-worthy local panels; risk overlay **NOT ELIGIBLE**.

## SINGLE MANDATORY TASK — HEAVY EXECUTION (no planning-only, no relitigation)
**`next_unfinished_task`:** Run full confirmatory Track B M5 on **TB1: 2025-01-01..2026-10-31, symbols BTCUSDT/ETHUSDT/BNBUSDT/SOLUSDT/XRPUSDT, ~22 non-overlapping 30d blocks** (see `research_state/trackb_TB1_admissibility.json`). Deliver a verifiable gate verdict or evidence-backed window inadmissibility. **Do not** relitigate Track C/A, stop at narration, or declare conclusion while TB1 is admissible and untested for this design.

### 1) Admissibility & provenance lock (verify + record)
- Reconfirm TB1 admissibility evidence (`research_state/trackb_TB1_admissibility.json`, contiguous series/funding schema/22 blocks). If re-verification fails, stop TB1 with evidence and deep-audit fallback window 2024-01-01..2024-09-30 before confirmatory.
- **Machine-verify provenance now (record in artifacts):**
  `python -c "from scripts.trackc_provenance_lineage import verify_paths_with_manifests; from pathlib import Path; res=verify_paths_with_manifests([str(p) for p in Path('research_state/data_cache').rglob('*-fundingRate-*.csv')], repo_root=Path('.')); assert res['provenance_verified'] and res['unmapped_count']==0; print('PROVENANCE_OK', res['files_considered'])"`
  (verified PASS at 2026-11-10T17:14Z: `PROVENANCE_OK 161`).

### 2) Freeze prereg BEFORE any outcome/label computation (procedural blocker)
- Write new frozen protocol `research_state/research_protocol_trackb_TB1_<UTC>.md`: modeled breach definition (leverage/margin/horizon/side), predictors incl. funding-conditioned features, 60/20/20 chronological splits + 7-day purge/embargo, metrics, **2% materiality floor**, Holm multiplicity, block bootstrap >=2000, window/symbols/blocks, explicit **“synthetic proxy ≠ observed liquidation”**.
- Compute `prereg_hash = sha256(frozen protocol bytes)`.
- **Before running labels/evaluation/outcome inspection**, append/update `research_state/run_manifest.json` with `split_boundaries_trackb_TB1_<ID>` (or equivalent) containing `frozen_before_outcomes=true`, split boundaries, `prereg_hash`, `protocol_ref`, timestamp, `outcome_values_inspected=false`. Order must be provable.

### 3) Execute & evaluate (substantive heavy work)
- Run Track B pipeline on frozen TB1 panel using existing primitives (`scripts/run_trackb_evaluation.py`, `scripts/synthetic_boundary_labels.py`, `tests/test_synthetic_boundary_labels.py` PASS baseline) adapted as needed while preserving leakage safety and pre-registered design.
- Produce `research_state/evaluation_summary_trackb_TB1_<ID>.md` with point estimate, 95% CI, relative change, n_instruments, n_obs, n_test_blocks, materiality/gate decision, Holm/multiplicity, and explicit modeled-proxy caveat.

### 4) Verdict & propagation (single coherent state)
- Update `research_state/hypothesis_registry.json`, `research_state/experiment_frontier.json`, `research_state/negative_results_report.md`, `AGENT_HANDOFF.md`, and this `NEXT_SESSION_TASK.md`.
- Keep risk overlay **NOT ELIGIBLE** unless all pre-registered gates pass.
- Set singular, evidence-backed `next_unfinished_task`:
  - gates not met but another admissible untested >=3-block Track B window remains → that window + M5;
  - all admissible local >=3-block Track B/C routes exhausted with preserved results → `NONE — program concluded under constraints pending new admissible unauthenticated source` (Track A remains STRUCTURALLY_BLOCKED).

## Acceptance (session incomplete without)
- Machine-verified provenance/admissibility evidence for executed window (or evidence-backed stop).
- Frozen prereg file + hash and `frozen_before_outcomes=true` recorded in `run_manifest.json` **before** outcomes.
- `evaluation_summary_trackb_TB1_<ID>.md` with CIs/blocks/gate verdict.
- Registries + `AGENT_HANDOFF.md` + this file updated; `next_unfinished_task` singular and accurate.

## Verification commands
- `python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_funding_schema_audit tests.test_trackc_provenance_lineage -v`
- Provenance: `python -c "from scripts.trackc_provenance_lineage import verify_paths_with_manifests; from pathlib import Path; res=verify_paths_with_manifests([str(p) for p in Path('research_state/data_cache').rglob('*-fundingRate-*.csv')], repo_root=Path('.')); assert res['provenance_verified'] and res['unmapped_count']==0; print('PROVENANCE_OK', res['files_considered'])"`

## Hard constraints (NON-NEGOTIABLE)
No network/paid/manual/credentialed data; no fabricated data/provenance; no threshold shopping; no sealed-holdout reuse; no Track A/B/C conflation (Track B = modeled synthetic breach proxies, never observed liquidations); preregister before outcomes; no risk overlay until forecast gate passes; no `.github/workflows` edits. Future agents must deliver heavy, verifiable progress — not status-only updates.
