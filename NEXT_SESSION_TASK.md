# NEXT_SESSION_TASK.md
**Timestamp:** 2026-11-10T10:44:50Z
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Status:** PROGRAM CONCLUDED UNDER CONSTRAINTS (exit criteria 2). No active confirmatory task.

## Authoritative state (do not re-litigate)
- **Track C / H001 (repo priority): NOT_SUPPORTED.** FCLR-014 (2025-01-01..2025-06-07, 5 symbols, frozen prereg, provenance/schema verified) executed 2026-11-10T10:38:27Z: C2 vs B1 rel QLIKE reduction **1.14%** (<2% floor), 95% CI **[-0.016361, 0.007728]** crosses zero, test window **17 days / 0 non-overlapping 30-day blocks** (<3). Forecast gate **NOT_MET**, overlay **INELIGIBLE**.
- All locally available provenance-verified panels with >=3 blocks tested (FCLR-003, FCLR-009, FCLR-013, plus FCLR-014/others as recorded): H001 remains **NOT_SUPPORTED/INCONCLUSIVE** where applicable.
- **Track A:** STRUCTURALLY_BLOCKED (no admissible unauthenticated historical liquidation source). **Track B:** UNTESTED (no modeled breach scenario registered before outcome inspection). **Track C ≠ liquidation validation.**
- **Bottlenecks already removed:** local provenance machine-verified (`provenance_verified=true`, 36001 manifest records, 161+ funding files), 2025 H1 schema/coverage OK, FCLR-014 protocol frozen pre-outcomes (`prereg_hash=8563163c62524605cbf7f11603759aee2210d133f82c3742319a6dd85dfca597`), dep-light gate 48/48 PASS (at last run). No local repairable bottleneck remains.

## Do not do (non-negotiable)
- No network/paid/manual/credentialed data; no fabricated provenance/outcomes; no threshold shopping; no sealed-holdout reuse.
- Do not re-inspect FCLR-009 window (2025-06-08..2025-12-31). Do not conflate Track A/B/C. No `.github/workflows` edits. No risk overlay (gate not passed).

## Single next heavy-work campaign — ONLY if a new admissible unauthenticated source appears
`next_unfinished_task: NONE` until a materially different, local/unauthenticated, verifiable data route exists. If a new admissible source is added locally:
1. **Provenance & admissibility lock:** obtain/verify sha256 sidecars + manifest mapping; run `trackc_provenance_lineage.py` → `provenance_verified=true`, `unmapped_count=0`; run `trackc_funding_schema_audit.py` and `trackc_panel_deep_audit_orchestrator.py` to prove >=5 instruments and >=3 non-overlapping 30-day test blocks with no required series gaps. Record evidence in `research_state/`.
2. **Preregister before outcomes (new ID/window):** freeze protocol + 60/20/20 splits (7-day purge/embargo), record `prereg_hash` and `frozen_before_outcomes=true` in `research_state/run_manifest.json`; never inspect outcomes before freeze.
3. **Confirmatory run:** `FCLR_EXPERIMENT=<NEW_ID> python scripts/run_evaluation.py`; write `evaluation_summary_<NEW_ID>.md`; apply forecast gate (>=2% rel QLIKE, CI supports direction after Holm, >=3 blocks, >1 instrument, no leakage/source defect).
4. **Verdict & handoff:** update `hypothesis_registry.json`, `negative_results_report.md` (preserve nulls), and `AGENT_HANDOFF.md` with exact outcomes; state overlay eligibility (only if ALL 6 gate conditions pass).

## Verification (resume checks)
```bash
# Dep-light gate (must pass 48/48)
python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_gap_repair_manifest tests.test_trackc_funding_schema_audit tests.test_trackc_panel_window_planner.TestPanelWindowPlanner.test_contiguous_sequences tests.test_trackc_panel_window_planner.TestPanelWindowPlanner.test_cli_smoke tests.test_trackc_panel_deep_audit_orchestrator tests.test_trackc_provenance_lineage -v

# Provenance on local funding data
python -c "from scripts.trackc_provenance_lineage import verify_paths_with_manifests; from pathlib import Path; files=list(Path('research_state/data_cache').rglob('*-fundingRate-*.csv')); res=verify_paths_with_manifests([str(p) for p in files], repo_root=Path('.')); assert res['provenance_verified'] and res['unmapped_count']==0; print('PROVENANCE_OK', res['files_considered'])"

# Canonical results
grep -n 'H1_primary' research_state/hypothesis_registry.json
sed -n '1,40p' research_state/evaluation_summary_FCLR-014.md
```

**Canonical handoff:** `AGENT_HANDOFF.md` (2026-11-10T10:38:27Z). This file is the timestamped initial task message for the next session.
