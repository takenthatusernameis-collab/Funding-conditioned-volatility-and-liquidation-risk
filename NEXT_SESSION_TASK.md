# NEXT_SESSION_TASK.md
**Timestamp:** 2026-11-10T11:16:16Z
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Status:** Track C / H001 concluded under constraints (exit criteria 2, forecast gate NOT_MET). Track B / liquidation-risk campaign is the next mandatory heavy-work task (UNTESTED, executable with local data only).

## Authoritative state (do not re-litigate)
- **Track C / H001 (repo priority): NOT_SUPPORTED.** All locally available provenance-verified panels with >=3 non-overlapping 30-day blocks tested (FCLR-003, FCLR-008, FCLR-012-V, FCLR-013, FCLR-014). FCLR-014: C2 vs B1 rel QLIKE reduction **1.14%** (<2% floor), 95% CI **[-0.016361, 0.007728] crosses zero**, test window **17 days / 0 blocks** (<3). Forecast gate **NOT_MET**, overlay **INELIGIBLE**. `next_unfinished_task: NONE` for Track C pending new admissible unauthenticated data source.
- **Track A:** STRUCTURALLY_BLOCKED (no admissible unauthenticated historical liquidation source). **Track B:** UNTESTED (no modeled breach scenario registered before outcome inspection). **Track C ≠ liquidation validation.**
- **Bottlenecks removed:** local provenance machine-verified (`provenance_verified=true`, 36001 manifest records, 161+ funding files), 2025 H1 schema/coverage OK, FCLR-014 protocol frozen pre-outcomes, dep-light gate 48/48 PASS. Track B requires no new data — all inputs (mark/index/premium klines, funding) already provenance-verified locally.

## Do not do (non-negotiable)
- No network/paid/manual/credentialed data; no fabricated provenance/outcomes; no threshold shopping; no sealed-holdout reuse.
- Do not re-inspect FCLR-009 window (2025-06-08..2025-12-31). Do not conflate Track A/B/C. No `.github/workflows` edits. No risk overlay (gate not passed). Do not inspect Track B outcomes before prereg freeze (`frozen_before_outcomes=true`).

## Single next heavy-work campaign — Track B modeled liquidation boundary breaches (LOCAL DATA ONLY)
Track C is concluded; Track A needs a new data source; Track B is UNTESTED and needs no new source. Execute in order:

1. **Provenance & admissibility lock for Track B panel:** choose a local window with >=3 non-overlapping 30-day blocks and >=5 instruments from verified local panels. Run `trackc_provenance_lineage.py` → `provenance_verified=true`, `unmapped_count=0`; run `trackc_funding_schema_audit.py` and `trackc_panel_deep_audit_orchestrator.py` to prove >=5 instruments and >=3 non-overlapping 30-day test blocks with no required series gaps. Record evidence in `research_state/`.
2. **Preregister before outcomes (new Track B ID/window):** freeze protocol + 60/20/20 splits (7-day purge/embargo), record `prereg_hash` and `frozen_before_outcomes=true` in `research_state/run_manifest.json`; never inspect outcomes before freeze.
3. **Confirmatory run:** write `research_state/evaluation_summary_trackb_<ID>.md` with point estimate, 95% CI (block bootstrap), relative change, n_instruments, n_blocks, n_obs; apply forecast gate (materiality floor, CI supports direction after Holm, >=3 blocks, >1 instrument, no leakage/source defect).
4. **Verdict & handoff:** update `hypothesis_registry.json` (Track B status), `experiment_frontier.json` (terminal cell status), `negative_results_report.md` (preserve nulls), and `AGENT_HANDOFF.md` with exact outcomes; state overlay eligibility (only if ALL gate conditions pass). Set `next_unfinished_task` to next materially different route or "NONE — program concluded under constraints".

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

**Canonical handoff:** `AGENT_HANDOFF.md` (2026-11-10T11:16:16Z). This file is the timestamped initial task message for the next session.
