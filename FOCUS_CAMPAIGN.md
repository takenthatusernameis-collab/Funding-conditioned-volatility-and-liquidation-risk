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

### M1 — Provenance & data admissibility lock (REQUIRED, unblocked)

**Goal:** Confirm all local data for the chosen confirmatory window has machine-verifiable sha256 provenance and passes funding schema audit.

**Tasks:**
1. Verify `scripts/repair_local_provenance.py` output: 36001 `.sha256` sidecars present, `manifest_extended.json` + `manifest_extract.json` are real JSON with 36001 records combined.
2. Run `trackc_provenance_lineage.py` on every funding CSV + kline zip in the chosen window → `provenance_verified=true`, `unmapped_count=0`.
3. Run `trackc_funding_schema_audit.py` for all 5 symbols × all months in the window → `all_ok=true`, `missing=0`, `schema_bad=0`.
4. Run `trackc_gap_repair_manifest.py` → document any series gaps; confirm `any_required_series_gaps=false`.

**Acceptance:** `provenance_verified=true` for all files in window; funding schema OK for all symbol-months; no required series gaps. Evidence written to `research_state/`.

**Command:**
```bash
python scripts/trackc_funding_schema_audit.py --repo-root . --cache research_state/data_cache --symbols BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,XRPUSDT --months <WINDOW_MONTHS> --out research_state/funding_schema_audit_<WINDOW>.json
python scripts/trackc_panel_deep_audit_orchestrator.py --cache research_state/data_cache --repo-root . --symbols BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,XRPUSDT --window-hint <WINDOW> --min-symbols 5 --min-blocks 3 --out research_state/trackc_deep_audit_<WINDOW>_check.json
```

---

### M2 — Freeze protocol v2 + prereg-before-outcomes (REQUIRED)

**Goal:** Register a new protocol version (new ID, e.g. FCLR-014-v2) with frozen splits, features, models, metrics, gates, BEFORE any outcome inspection.

**Tasks:**
1. Select a local window with >=3 non-overlapping 30-day test blocks and >=5 instruments (candidate: 2024-10-02..2024-12-31 = 91 days = 3 blocks, used by FCLR-003; or 2025-01-01..2025-12-31 used by FCLR-009).
2. Write `research_state/research_protocol_fclr014_v2.md` (or next available ID): unit, timing, universe, primary outcome (next-24h RV), predictors (B0/B1/C1/C2), splits (60/20/20 chronological, 7-day purge/embargo), metrics (QLIKE primary, block bootstrap 2000 reps), materiality floor (>=2% relative QLIKE reduction), multiplicity rule (Holm).
3. Freeze splits via `scripts/freeze_fclr009_splits.py` pattern → record `split_boundaries_<id>` in `run_manifest.json` with `frozen_before_outcomes=true`.
4. Record `prereg_hash` (sha256 of the prereg file) in the experiment registry.

**Acceptance:** Protocol file exists with `frozen_before_outcomes=true`; split boundaries recorded in run_manifest before outcomes; prereg_hash recorded; NO outcome has been inspected for this window.

**Non-negotiable:** If any outcome for this window was already inspected, choose a different window or register a new pilot ID. Do not reuse sealed holdouts.

---

### M3 — Execute confirmatory Track C / H001 run (REQUIRED)

**Goal:** Run the frozen C2 vs B1 contrast (and C1 vs B1, C2 vs C1 secondary) on the M2-frozen panel.

**Tasks:**
1. Execute `scripts/run_evaluation.py` with `FCLR_EXPERIMENT=<ID>` on the frozen panel.
2. Record results: point estimate, 95% CI (block bootstrap), relative QLIKE reduction, n_instruments, n_blocks, n_obs.
3. Write `research_state/evaluation_summary_<ID>.md` with full metrics and uncertainty.
4. Update `research_state/hypothesis_registry.json` H1_primary status: NOT_SUPPORTED / INCONCLUSIVE / (gate pass only if all criteria met).
5. Update `research_state/experiment_frontier.json` with terminal status for this cell.

**Acceptance:** Run completes deterministically; summary written; registry updated; no threshold shopping; no holdout reuse.

**Command:**
```bash
FCLR_EXPERIMENT=<ID> python scripts/run_evaluation.py
# then verify summary file and registry
```

---

### M4 — Gate verdict & overlay eligibility (REQUIRED)

**Goal:** Apply the forecast gate (research_protocol.md §9) and decide overlay eligibility.

**Gate conditions (ALL must pass):**
1. Meaningful OOS improvement over RV-only baseline on primary target (>=2% relative QLIKE reduction).
2. Uncertainty supports improvement (CI supports direction) after multiplicity treatment.
3. Acceptable calibration (if event probabilities).
4. Evidence across multiple time blocks and >1 instrument.
5. No unresolved leakage/source/label/timestamp defect.
6. Practical relevance for decision horizon.

**Tasks:**
1. Check each gate condition against M3 results.
2. Record verdict: FORECAST_GATE_PASSED or NOT_SUPPORTED / INCONCLUSIVE.
3. Overlay eligibility: OVERLAY_ELIGIBLE only if gate passed; otherwise NOT ELIGIBLE.
4. Write verdict to `research_state/negative_results_report.md` (if null) and update `AGENT_HANDOFF.md`.

**Acceptance:** Explicit gate verdict recorded; overlay eligibility stated; no promotion without all 6 conditions.

---

### M5 — Track A / Track B status confirmation (CONDITIONAL)

**Goal:** Confirm liquidation tracks remain blocked/untested; do not conflate with Track C.

**Tasks:**
1. Verify Track A: no admissible unauthenticated historical liquidation source (already STRUCTURALLY_BLOCKED per `research_state/liquidation_sources_enumeration.md`).
2. Verify Track B: no margin/leverage scenario registered before outcome inspection (UNTESTED — do not report as null).
3. Document that Track C results are volatility/stress only, NOT observed-liquidation validation.

**Acceptance:** Track A = STRUCTURALLY_BLOCKED (evidence cited); Track B = UNTESTED (scenario not registered); Track C results never described as liquidation validation.

---

### M6 — Handoff update & next-session task (REQUIRED, every session)

**Goal:** Leave a clear, timestamped initial task message for the next agentic session.

**Tasks:**
1. Update `AGENT_HANDOFF.md`: what changed, what was tested with exact outcomes, evidence added, gate states, single highest-value next task, verification command, blockers.
2. If M3/M4 complete, set `next_unfinished_task` to the next materially different route (e.g. new panel, new protocol version) or "NO CONFIRMATORY TASK — program concluded under constraints" if all local panels exhausted.
3. Commit code + manifests + reports (not raw data/caches).

**Acceptance:** AGENT_HANDOFF.md has a dated, actionable initial task message; next session can continue without user intervention.

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
