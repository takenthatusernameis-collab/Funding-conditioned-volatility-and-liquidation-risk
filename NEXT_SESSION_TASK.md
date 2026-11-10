# NEXT_SESSION_TASK.md — SINGLE DURABLE HANDOFF (2026-11-10T17:13:13Z)
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Priority (by name):** 1) liquidation risk — **Track B modeled boundary breaches** (active), 2) funding-conditioned volatility — Track C concluded NOT_SUPPORTED, 3) Track A observed liquidations — STRUCTURALLY_BLOCKED (no admissible unauthenticated census).
**Campaign:** `TRACKB-MODELED-BREACH-NEXT-20261110T171313Z`
**Program status:** `ACTIVE_TRACKB_UNTESTED_WINDOW_REMAINS` (not concluded). Prior Track B window `TRACKB-20251110T154307Z` (2025-01-01..2025-10-31, 4/5 effective) is NOT_MET/NOT_SUPPORTED (C2 vs B1 +1.50% < 2% floor, 95% CI [-0.005,0.035], synthetic proxy only). Track C H1_primary NOT_SUPPORTED on all claim-worthy local panels; risk overlay INELIGIBLE.

## SINGLE MANDATORY TASK — HEAVY EXECUTION REQUIRED (no planning-only session)
**`next_unfinished_task`:** Execute Track B confirmatory M5 on untested local window **TB1 (2025-01-01..2026-10-31, 5 symbols BTCUSDT/ETHUSDT/BNBUSDT/SOLUSDT/XRPUSDT, ~22 non-overlapping 30d blocks)**. Do not relitigate Track C/A. Do not stop at status narration.

### M5.1 Admissibility & provenance lock (verify, record evidence)
- TB1 admissibility evidence exists: `research_state/trackb_TB1_admissibility.json` (+ `.md`) — contiguous mark/index/premium/klines + funding, 5 symbols, ~22 blocks, schema OK, not sealed/not previously outcome-inspected for this design.
- **Machine-verify now:** `python -c "from scripts.trackc_provenance_lineage import verify_paths_with_manifests; from pathlib import Path; res=verify_paths_with_manifests([str(p) for p in Path('research_state/data_cache').rglob('*-fundingRate-*.csv')], repo_root=Path('.')); assert res['provenance_verified'] and res['unmapped_count']==0; print('PROVENANCE_OK', res['files_considered'])"` (verified OK 161 files at 2026-11-10T17:12Z). Record/confirm verification in your M5 artifacts.
- Fallback only if TB1 fails re-verification: deep re-audit 2024-01-01..2024-09-30 (admissibility + gap + funding schema + lineage) before confirmatory.

### M5.2 FREEZE PREREG BEFORE ANY OUTCOME/LABEL COMPUTATION (procedural blocker — non-optional)
- Author **new** frozen protocol `research_state/research_protocol_trackb_TB1_<UTC>.md` (modeled breach definition: leverage/margin/horizon/side; predictors/features incl. funding-conditioned; 60/20/20 chronological splits + 7-day purge/embargo; metrics; **2% materiality floor**; Holm; block bootstrap >=2000; explicit **“synthetic proxy ≠ observed liquidation”**; window/symbols/blocks).
- Compute `prereg_hash = sha256(frozen protocol bytes)`.
- Record in `research_state/run_manifest.json` **before** running labels/evaluation/outcome inspection: a `split_boundaries_trackb_TB1_<ID>` (or equivalent) entry with `frozen_before_outcomes=true`, split boundaries, `prereg_hash`, `protocol_ref`, timestamp, and `outcome_values_inspected=false`. Ordering must be provably before outcomes.

### M5.3 Execute & evaluate (substantive, heavy)
- Run Track B pipeline on the frozen TB1 panel using existing primitives (`scripts/run_trackb_evaluation.py`, `scripts/synthetic_boundary_labels.py`) adapted as needed for TB1/window/splits while preserving leakage safety and pre-registered design.
- Produce `research_state/evaluation_summary_trackb_TB1_<ID>.md` with: point estimate, 95% CI, relative change, n_instruments, n_obs, n_test_blocks, materiality/gate decision, Holm/multiplicity, and explicit modeled-proxy caveat.

### M5.4 Verdict & propagation (single coherent state)
- Update `research_state/hypothesis_registry.json`, `research_state/experiment_frontier.json`, `research_state/negative_results_report.md`, `AGENT_HANDOFF.md`, and this `NEXT_SESSION_TASK.md`.
- Set risk overlay **NOT ELIGIBLE** unless all pre-registered gates pass.
- Record a single, evidence-backed `next_unfinished_task`:
  - if gates not met but another admissible untested >=3-block Track B window remains: that window + M5 cycle;
  - if all admissible local >=3-block Track B/C routes exhausted with preserved results: `NONE — program concluded under constraints pending new admissible unauthenticated source` (Track A remains STRUCTURALLY_BLOCKED).

## Verifiable acceptance (session incomplete without)
- Provenance/admissibility evidence for executed window (machine-verified).
- Frozen prereg file + hash and `frozen_before_outcomes=true` in `run_manifest.json` recorded **before** outcomes.
- `evaluation_summary_trackb_TB1_<ID>.md` with CIs/blocks/gate verdict (or evidence-backed inadmissibility stopping the window).
- Registries + both handoffs updated; frontier `next_unfinished_task` singular and accurate.

## Verification commands
- `python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_funding_schema_audit tests.test_trackc_provenance_lineage -v`
- Provenance: `python -c "from scripts.trackc_provenance_lineage import verify_paths_with_manifests; from pathlib import Path; res=verify_paths_with_manifests([str(p) for p in Path('research_state/data_cache').rglob('*-fundingRate-*.csv')], repo_root=Path('.')); assert res['provenance_verified'] and res['unmapped_count']==0; print('PROVENANCE_OK', res['files_considered'])"`

## Hard constraints (NON-NEGOTIABLE)
No network/paid/manual/credentialed data; no fabricated data/provenance; no threshold shopping; no sealed-holdout reuse; no Track A/B/C conflation (Track B = modeled synthetic breach proxies, never observed liquidations); preregister before outcomes; no risk overlay until forecast gate passes; no `.github/workflows` edits. Future agents must deliver heavy, verifiable progress — not relitigation or status-only updates.
