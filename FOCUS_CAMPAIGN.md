# FOCUS_CAMPAIGN.md — Heavy-Work Execution Plan (repo-name priority: Funding-conditioned Volatility & Liquidation Risk)

**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Priority order (per repo name):** 1) Track C / H001 funding-conditioned volatility forecast; 2) Track A/B liquidation tracks (secondary, only if admissible source appears)
**Effective:** 2026-11-10T09:30:00Z
**Constraints (NON-NEGOTIABLE):** no network/paid/manual/credentialed data; no fabricated provenance/outcomes; no threshold shopping; no sealed-holdout reuse; no Track A/B/C conflation; no risk overlay until forecast gate passes.

---

## CAMPAIGN MISSION

Produce a reproducible, honest out-of-sample forecast test of whether funding extremes + realized volatility + pre-specified price-dislocation/smoothing features improve next-24h realized-variance forecasting over an RV-only HAR baseline, on a **provenance-verified local panel with >=3 non-overlapping 30-day test blocks and >=5 instruments**, with a **frozen prereg registered before outcomes**. Preserve the null if the gate fails; do not promote.

---

## MILESTONES (execute in order; do not skip)

> **Status sync (2026-11-10T11:20:05Z):** Track C / H001 milestones M1–M4 **COMPLETE** (FCLR-014 frozen, executed, gate NOT_MET, overlay INELIGIBLE; Track C concluded under constraints). **M5/M6 now point to Track B heavy-work campaign** (repo-name liquidation leg) — untested, executable on verified local data with no network.

### M1 — Provenance & data admissibility lock — **COMPLETE (Track C / FCLR-014)**
Provenance machine-verified (`provenance_verified=true`, `unmapped_count=0`, 36001 manifest records), funding schema/coverage OK for 2025 H1 and full 2025 panels, no required series gaps. Evidence: `research_state/trackc_deep_audit_2025_h1_check.json`, `research_state/trackc_deep_audit_2025_full_check.json`, `research_state/funding_schema_audit_2025_h1.json`.

### M2 — Freeze protocol + prereg-before-outcomes — **COMPLETE (Track C / FCLR-014)**
`research_state/research_protocol_fclr014.md` v2.0 FROZEN_BEFORE_OUTCOMES; `prereg_hash=8563163c62524605cbf7f11603759aee2210d133f82c3742319a6dd85dfca597`; `split_boundaries_fclr014.frozen_before_outcomes=true` in `run_manifest.json`; no outcome inspection before freeze.

### M3 — Execute confirmatory Track C / H001 run — **COMPLETE (FCLR-014)**
`FCLR_EXPERIMENT=FCLR-014 python scripts/run_evaluation.py` (2026-11-10T10:38:27Z). Results recorded in `research_state/evaluation_summary_FCLR-014.md`; registries updated.

### M4 — Gate verdict & overlay eligibility — **COMPLETE (FCLR-014)**
C2 vs B1 rel QLIKE reduction **1.14%** (<2% floor), 95% CI **[-0.016361, 0.007728]** crosses zero, test window **17 days / 0 non-overlapping 30-day blocks** (<3). **Forecast gate: NOT_MET. Overlay: NOT ELIGIBLE.** H1_primary **NOT_SUPPORTED** across all claim-worthy local Track C panels.

### M5 — Track B liquidation campaign (REQUIRED, next heavy work — local data only)
**Goal:** Deliver a substantive, verifiable Track B result (modeled liquidation boundary breaches), UNTESTED and executable without network/new data.

**Tasks (in order):**
1. **Admissibility lock:** select verified local window with >=5 instruments and >=3 non-overlapping 30-day test blocks (distinct from sealed/reused windows). Prove `provenance_verified=true`, `unmapped_count=0`, schema/coverage OK, no required series gaps; record evidence in `research_state/`.
2. **Preregister before outcomes:** define modeled breach target + leverage/margin assumptions (Track B only, NOT observed liquidations), predictors, 60/20/20 splits + 7-day purge/embargo, metrics/gates/multiplicity. Write `research_state/research_protocol_trackb_<ID>.md`; record `prereg_hash` and `frozen_before_outcomes=true` in `run_manifest.json`. **No outcome inspection before freeze.**
3. **Execute confirmatory run:** produce `research_state/evaluation_summary_trackb_<ID>.md` with point estimate, 95% CI (block bootstrap), relative change, n_instruments, n_blocks, n_obs.
4. **Verdict:** apply forecast gate; update `hypothesis_registry.json`, `experiment_frontier.json`, `negative_results_report.md`; state overlay eligibility (NOT ELIGIBLE unless all gate conditions pass). Track A remains STRUCTURALLY_BLOCKED; do not conflate tracks.

**Acceptance:** Prereg frozen before outcomes, deterministic run/evidence recorded, gate verdict explicit, registries/handoff updated.

### M6 — Handoff update & next-session task (REQUIRED, every session)
Update `AGENT_HANDOFF.md` and `NEXT_SESSION_TASK.md` with timestamped initial task, exact outcomes/evidence, gate states, blockers, and single highest-value next task/verification commands. If Track B yields no gate pass and no materially different local route remains, set `next_unfinished_task: NONE — program concluded under constraints` (pending new admissible unauthenticated source). Commit code + manifests + reports (not raw data/caches).

---

## NON-NEGOTIABLE EXECUTION RULES

1. **Prereg before outcomes** — Never inspect outcomes for a window before freezing its protocol/splits. Violation = non-compliant session.
2. **No threshold shopping** — Do not relax block count, materiality floor, or multiplicity after seeing outcomes.
3. **No holdout reuse** — Sealed holdouts are inspected once; never re-used for selection/tuning/re-evaluation.
4. **No Track conflation** — Track A (observed liquidations) ≠ Track B (modeled breaches) ≠ Track C (volatility/stress).
5. **No fabricated provenance** — URL/manifest presence without content-hash match is not verification.
6. **No risk overlay** — Overlay only after forecast gate passes (FORECAST_GATE_PASSED).
7. **No network/paid/manual** — All data must be local, unauthenticated, already present.
8. **Preserve nulls** — Negative/inconclusive results are preserved, not explained away.
9. **Heavy work required** — Each session must deliver one substantive verifiable result (source-probe, tested adapter, validated dataset, preregistered experiment, completed test block, independent recomputation, or evidence-backed blocker + next valid task).
10. **No status-only activity** — Do not polish documentation, schedulers, pollers, or wrappers while the core data/baseline/gate remains unresolved.

---

## VERIFICATION COMMANDS (canonical)

```bash
# Dep-light gate (48 tests, must pass)
python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_gap_repair_manifest tests.test_trackc_funding_schema_audit tests.test_trackc_panel_window_planner.TestPanelWindowPlanner.test_contiguous_sequences tests.test_trackc_panel_window_planner.TestPanelWindowPlanner.test_cli_smoke tests.test_trackc_panel_deep_audit_orchestrator tests.test_trackc_provenance_lineage -v

# Provenance check on window data
python -c "
from scripts.trackc_provenance_lineage import verify_paths_with_manifests
from pathlib import Path
res = verify_paths_with_manifests([str(p) for p in Path('data/raw').glob('*-fundingRate-*.csv')], repo_root=Path('.'))
assert res['provenance_verified'] is True and res['unmapped_count'] == 0
print('PROVENANCE_OK')
"

# Funding schema audit for window
python scripts/trackc_funding_schema_audit.py --repo-root . --cache research_state/data_cache --symbols BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,XRPUSDT --months <MONTHS> --out research_state/funding_schema_audit_<WINDOW>.json

# Deep audit on window
python scripts/trackc_panel_deep_audit_orchestrator.py --cache research_state/data_cache --repo-root . --symbols BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,XRPUSDT --window-hint <WINDOW> --min-symbols 5 --min-blocks 3 --out research_state/trackc_deep_audit_<WINDOW>_check.json
```

---

## EXIT CRITERIA

The campaign ends when one of:
- FORECAST_GATE_PASSED → OVERLAY_ELIGIBLE (then overlay phase may begin under separate protocol).
- All locally available provenance-verified panels with >=3 blocks have been tested and H001 remains NOT_SUPPORTED → program concluded under constraints, `next_unfinished_task: NONE` pending new admissible unauthenticated data source.
- Environment materially changes with a new admissible unauthenticated data source → revisit per AGENT_HANDOFF.md §"IF A NEW ADMISSIBLE SOURCE APPEARS".

---

**Future agents: execute M1→M6 in order. Do not skip milestones. Do not replace heavy work with status documents. Record exact outcomes in AGENT_HANDOFF.md at the end of every session.**
