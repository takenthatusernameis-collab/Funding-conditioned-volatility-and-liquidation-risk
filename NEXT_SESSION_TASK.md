# NEXT_SESSION_TASK.md — Single Durable Initial Task for Next Agentic Session
**Timestamp (UTC):** 2026-11-10T11:39:30Z
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Project priority (by repo name):** 1) liquidation risk — Track B modeled boundary breaches (untested, executable locally), 2) funding-conditioned volatility — Track C (concluded NOT_SUPPORTED), 3) Track A observed liquidations (STRUCTURALLY_BLOCKED).
**Authoritative handoff:** `AGENT_HANDOFF.md` (2026-11-10T11:39:30Z) — this file is the timestamped initial task message the next session must execute.

## Current verdict (do not relitigate)
- **Track B (modeled liquidation boundary breaches): UNTESTED — MANDATORY NEXT.** Repo-name liquidation leg. No modeled breach scenario has been preregistered before outcome inspection on an admissible local panel. Executable now on local data (mark/index/premium/klines + funding already present and provenance-verified). **This is the only heavy-work path that can advance repo-name scope without network/new data.**
- **Track C / H1_primary (funding-conditioned volatility forecast vs RV-only baseline): CONCLUDED UNDER CONSTRAINTS / NOT_SUPPORTED.** All locally available provenance-verified Track C panels with >=3 non-overlapping 30-day blocks tested (FCLR-003, FCLR-008, FCLR-009, FCLR-012-V, FCLR-013, FCLR-014). FCLR-014 (2025 H1, frozen prereg): C2 vs B1 rel QLIKE reduction **1.14%** (<2% floor), 95% CI **[-0.016361, 0.007728] crosses zero**, test window **17 days / 0 blocks** (<3). Forecast gate **NOT_MET**; overlay **INELIGIBLE**. `next_unfinished_task (Track C): NONE` pending a materially different, local, unauthenticated, provenance-verified data route.
- **Track A (observed liquidations): STRUCTURALLY_BLOCKED** — no admissible unauthenticated historical liquidation census covering required windows (see `research_state/track_a_structural_block.md`, `research_state/liquidation_sources_enumeration.md`). Track A ≠ Track B ≠ Track C.

## Removed/absent bottlenecks (verified; do not rebuild)
- Local provenance machine-verified: `provenance_verified=true`, `unmapped_count=0` across local funding data (36001 manifest records); funding schema/coverage OK for 2024-2025 panels used.
- Dep-light reproducibility gate: 48/48 PASS (`tests.test_volatility_features_splits`, `tests.test_synthetic_boundary_labels`, `tests.test_trackc_panel_admissibility_audit`, `tests.test_trackc_gap_repair_manifest`, `tests.test_trackc_funding_schema_audit`, `tests.test_trackc_panel_window_planner` selected, `tests.test_trackc_panel_deep_audit_orchestrator`, `tests.test_trackc_provenance_lineage`).
- Track B labeling primitive exists: `scripts/synthetic_boundary_labels.py` (+ tests) — modeled/synthetic breach proxy only, not observed liquidations.
- Local kline/price series present for BTCUSDT/ETHUSDT/BNBUSDT/SOLUSDT/XRPUSDT across 2024-01..2024-03 daily dirs and extensive 2024-2026 cache months; no network required.

## Mandatory initial task (heavy work) — execute in this order, produce verifiable artifacts
**Goal:** deliver one complete, evidence-backed Track B confirmatory cycle: admissibility-locked window → frozen prereg (before outcomes) → executed evaluation → gate verdict → registry/handoff update. A session that only documents status is non-compliant.

### Step 1 — Select & lock an admissible Track B panel (no outcome inspection)
- Choose window with **>=5 instruments** and **>=3 non-overlapping 30-day test blocks** in the test split, **distinct from sealed/reused inspected windows** (DO NOT reuse FCLR-009 inspected 2025-06-08..2025-12-31; avoid windows whose outcomes were already inspected for Track B-like breach labels). Prefer a window fully covered by local mark/index/premium/klines + funding (e.g. 2024 Q2-Q3 or another verified contiguous span with complete series).
- Machine-verify and save evidence to `research_state/trackb_<ID>_admissibility.json` (and/or deep-audit JSON): provenance `provenance_verified=true`, `unmapped_count=0` (`scripts/trackc_provenance_lineage.py`); funding schema/coverage OK, no required series gaps, >=5 symbols, >=3 blocks (`scripts/trackc_funding_schema_audit.py`, `scripts/trackc_panel_deep_audit_orchestrator.py` or equivalent checks).
- **Hard stop if not met:** record exact blocker evidence + next materially different local window; do not fabricate or relax thresholds.

### Step 2 — Preregister BEFORE any outcome/label inspection (freeze)
- Create `research_state/research_protocol_trackb_<ID>.md` defining: Track B **modeled** breach target (leverage/margin scenario(s), e.g. 5x/10x long/short, maintenance margin assumption), horizon (e.g. next-24h/next-7d breach), predictors (funding extremes, RV, premium/index dislocation — pre-specified), universe, 60/20/20 chronological splits with **7-day purge/embargo**, primary metric/contrast, **>=2% materiality floor**, Holm multiplicity, block bootstrap 2000 reps, and explicit statement: **synthetic boundary proxy ≠ observed liquidation**.
- Compute and record `prereg_hash` and set `split_boundaries_trackb_<ID>.frozen_before_outcomes=true` in `research_state/run_manifest.json` **before** computing breach labels/outcomes on the chosen window. Save split boundaries with exact UTC timestamps.
- **Non-negotiable:** no threshold shopping, no inspecting outcomes before freeze, no holdout reuse.

### Step 3 — Execute confirmatory Track B evaluation
- Implement/run the minimal evaluation path (script/notebook-equivalent in `scripts/`) that: loads frozen panel from local verified data, constructs features with leakage-safe transforms, generates modeled breach labels via pre-specified `synthetic_boundary_labels` logic, trains baseline vs funding-conditioned models on train only, evaluates on frozen test with block bootstrap CI, and writes `research_state/evaluation_summary_trackb_<ID>.md`.
- Required report fields: point estimate(s), 95% CI, relative change vs baseline, n_instruments, n_obs, n_test_blocks (>=3), materiality vs 2% floor, Holm-adjusted conclusions, and exact data/provenance refs.

### Step 4 — Verdict, registries, and handoff (must complete)
- Apply forecast/materiality/multiplicity gate; state overlay eligibility (**NOT ELIGIBLE unless all gate conditions pass**).
- Update `research_state/hypothesis_registry.json` (Track B modeled-breach hypothesis status + evidence), `research_state/experiment_frontier.json`, append preserved result to `research_state/negative_results_report.md` (null/inconclusive preserved, not explained away).
- Update `AGENT_HANDOFF.md` and this `NEXT_SESSION_TASK.md` with timestamp, exact outcomes/artifacts, gate state, blockers, and `next_unfinished_task`.
  - If Track B gate passes: `next_unfinished_task` = preregistered overlay/next confirmatory step per protocol (still no overlay before gate pass evidence recorded).
  - If Track B fails/inconclusive and no other uninspected admissible local Track B window with >=3 blocks remains: `next_unfinished_task: NONE — program concluded under constraints pending new admissible unauthenticated source`.
  - Otherwise: name the single next materially different Track B window/route.

## Verification commands (run at session start)
```bash
# Dep-light gate (expect 48/48 OK)
python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_gap_repair_manifest tests.test_trackc_funding_schema_audit tests.test_trackc_panel_window_planner.TestPanelWindowPlanner.test_contiguous_sequences tests.test_trackc_panel_window_planner.TestPanelWindowPlanner.test_cli_smoke tests.test_trackc_panel_deep_audit_orchestrator tests.test_trackc_provenance_lineage -v

# Provenance (expect verified, unmapped==0)
python -c "from scripts.trackc_provenance_lineage import verify_paths_with_manifests; from pathlib import Path; files=list(Path('research_state/data_cache').rglob('*-fundingRate-*.csv')); res=verify_paths_with_manifests([str(p) for p in files], repo_root=Path('.')); print(res); assert res['provenance_verified'] and res['unmapped_count']==0"

# Track B primitive present
python -m unittest tests.test_synthetic_boundary_labels -v
```

## Non-negotiable constraints
- No network/paid/manual/credentialed data, no `.github/workflows` edits, no live/paper trading.
- No fabricated provenance/outcomes, no threshold shopping, no sealed-holdout reuse.
- **Preregister before outcomes** (`frozen_before_outcomes=true`, `prereg_hash` recorded) — violation invalidates confirmatory claim.
- Do not conflate Track A/B/C; label modeled breaches as synthetic proxy, never observed liquidations. No risk overlay until forecast gate passes.
- Commit code/manifests/reports only (not raw data/caches). Each session must leave one substantive verifiable result.
