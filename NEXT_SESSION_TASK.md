# NEXT_SESSION_TASK.md
**Timestamp:** 2026-11-10T11:20:05Z
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Status:** Track C / H001 concluded under constraints (exit criteria 2, forecast gate NOT_MET, `next_unfinished_task: NONE` pending new admissible unauthenticated source). **Next mandatory heavy work: Track B modeled liquidation boundary-breach campaign (UNTESTED, executable on verified local data only).**

## Authoritative state (do not re-litigate)
- **Track C / H001 (repo priority) — NOT_SUPPORTED / CONCLUDED.** All locally available provenance-verified panels with >=3 non-overlapping 30-day blocks tested (FCLR-003, FCLR-008, FCLR-012-V, FCLR-013, FCLR-014). FCLR-014: C2 vs B1 rel QLIKE reduction **1.14%** (<2% floor), 95% CI **[-0.016361, 0.007728] crosses zero**, test window **17 days / 0 blocks** (<3). Forecast gate **NOT_MET**, overlay **INELIGIBLE**. No claim-worthy Track C panels remain locally.
- **Track A:** STRUCTURALLY_BLOCKED (no admissible unauthenticated historical liquidation source). **Track B:** UNTESTED (no modeled breach scenario preregistered before outcome inspection). **Track C ≠ liquidation validation.**
- **Bottlenecks removed:** local provenance machine-verified (`provenance_verified=true`, `unmapped_count=0`, 36001 manifest records, 161+ funding files), 2025 H1/full schema & coverage OK, FCLR-014 frozen pre-outcomes, dep-light gate 48/48 PASS. **Track B needs no new data** — mark/index/premium klines and funding are provenance-verified locally.

## Do not do (non-negotiable)
- No network/paid/manual/credentialed data; no fabricated provenance/outcomes; no threshold shopping; no sealed-holdout reuse.
- Do not re-inspect FCLR-009 window (2025-06-08..2025-12-31). Do not conflate Track A/B/C. No `.github/workflows` edits. No risk overlay (gate not passed).
- **Do not inspect Track B outcomes before prereg freeze** (`frozen_before_outcomes=true`, `prereg_hash` recorded in `run_manifest.json`).

## Single next heavy-work campaign — Track B modeled liquidation boundary breaches (LOCAL DATA ONLY)
Track C concluded; Track A needs a new data source; **Track B is the repo-name liquidation leg, UNTESTED, and unblocked by local data.** Execute in order (each step substantive/verifiable):

1. **Admissibility lock:** choose a verified local window with >=5 instruments and >=3 non-overlapping 30-day test blocks, distinct from sealed/reused inspected windows. Machine-verify: `scripts/trackc_provenance_lineage.py` → `provenance_verified=true`, `unmapped_count=0`; `scripts/trackc_funding_schema_audit.py` and `scripts/trackc_panel_deep_audit_orchestrator.py` → schema OK, no required series gaps, >=5 symbols, >=3 blocks. Save evidence to `research_state/` (e.g. `trackc_deep_audit_trackb_<ID>_check.json`).
2. **Preregister BEFORE outcomes (new Track B ID/window):** define modeled breach target and leverage/margin assumptions (explicitly Track B, **NOT observed liquidations**), predictors (funding extremes, RV, premium/index dislocation), 60/20/20 chronological splits with 7-day purge/embargo, primary metric, >=2% materiality floor, Holm multiplicity, block bootstrap 2000 reps. Write `research_state/research_protocol_trackb_<ID>.md`; record `prereg_hash` and `split_boundaries_trackb_<ID>.frozen_before_outcomes=true` in `research_state/run_manifest.json`. No outcome inspection before freeze.
3. **Execute confirmatory run:** run Track B evaluation on frozen panel; write `research_state/evaluation_summary_trackb_<ID>.md` with point estimate, 95% CI (block bootstrap), relative change, n_instruments, n_blocks, n_obs.
4. **Verdict & handoff:** apply forecast gate; update `research_state/hypothesis_registry.json` (Track B status), `research_state/experiment_frontier.json`, append `research_state/negative_results_report.md` (preserve nulls), and update `AGENT_HANDOFF.md` + this file with exact outcomes, overlay eligibility (NOT ELIGIBLE unless all gate conditions pass), and `next_unfinished_task` (next materially different route or "NONE — program concluded under constraints" if no local route remains). Commit code/manifests/reports only.

## Verification (resume checks)
```bash
# Dep-light gate (must pass 48/48)
python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_gap_repair_manifest tests.test_trackc_funding_schema_audit tests.test_trackc_panel_window_planner.TestPanelWindowPlanner.test_contiguous_sequences tests.test_trackc_panel_window_planner.TestPanelWindowPlanner.test_cli_smoke tests.test_trackc_panel_deep_audit_orchestrator tests.test_trackc_provenance_lineage -v

# Provenance on local funding data
python -c "from scripts.trackc_provenance_lineage import verify_paths_with_manifests; from pathlib import Path; files=list(Path('research_state/data_cache').rglob('*-fundingRate-*.csv')); res=verify_paths_with_manifests([str(p) for p in files], repo_root=Path('.')); assert res['provenance_verified'] and res['unmapped_count']==0; print('PROVENANCE_OK', res['files_considered'])"

# Canonical Track C conclusion / Track B untested
grep -n 'H1_primary' research_state/hypothesis_registry.json
sed -n '1,40p' research_state/evaluation_summary_FCLR-014.md
```

**Canonical handoff:** `AGENT_HANDOFF.md` (2026-11-10T11:20:05Z). This file is the timestamped initial task message for the next session.