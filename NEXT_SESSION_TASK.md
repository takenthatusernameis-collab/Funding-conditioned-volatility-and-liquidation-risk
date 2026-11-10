# NEXT_SESSION_TASK.md — SINGLE DURABLE HANDOFF (INITIAL TASK MESSAGE)

**Timestamp (UTC):** 2026-11-10T18:55:10Z
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Program status:** `ACTIVE_TRACKB_MANDATORY` — NOT concluded. This is the single durable handoff; execute this task before any other work.

## IMMEDIATE MANDATORY TASK (heavy, verifiable — start now)
Execute **Track B TB2 confirmatory attempt** on local panel **2024-01-01..2024-09-30** (BTCUSDT/ETHUSDT/BNBUSDT/SOLUSDT/XRPUSDT). TB1 (`2025-01-01..2026-10-31`, 5x/24h long) is **DEGENERATE/INADMISSIBLE** for confirmatory evaluation because the frozen test split (2026-06-26..2026-10-31) had **0 synthetic breaches** across all symbols (`research_state/evaluation_summary_trackb_TB1_20261110T173838Z.md`). **Do not rerun TB1 unchanged. Do not relitigate Track C or Track A.**

**Objective:** produce a preregistered, leakage-resistant Track B verdict (or evidence-backed inadmissibility of this local route) using **modeled synthetic boundary breaches only** (never observed liquidations), with a NEW frozen design that has **>0 positive labels in the frozen test split** (counts reported with rationale) and no threshold shopping after freeze.

## Verified context (do not re-open concluded tracks)
- **Track B prior:** `TRACKB-20251110T154307Z` (2025-01-01..2025-10-31) NOT_MET/NOT_SUPPORTED; TB1 above DEGENERATE/INADMISSIBLE. `research_state/research_protocol_trackb_TB1_20261110T173838Z.md`, manifest `split_boundaries_trackb_TB1_20261110T173838Z`.
- **TB2 candidate panel (local, untested):** 2024-01-01..2024-09-30, 5 symbols, contiguous required series (mark/index/premium/klines + funding), ~9 non-overlapping 30d blocks est.; prior audits indicate schema OK and funding lineage `provenance_verified=true`/`unmapped_count=0` (PROVENANCE_OK 161). Evidence: `research_state/trackb_TB1_admissibility_2024q1q3.json`, `research_state/trackb_window_candidates_fast.json`. **Re-verify for all inputs actually used.**
- **Track C / H1:** concluded **NOT_SUPPORTED** on claim-worthy local panels; no untested claim-worthy Track C panels with >=3 blocks remain. `next_unfinished_task (Track C): NONE`.
- **Track A:** **STRUCTURALLY_BLOCKED** (no admissible unauthenticated observed-liquidation census; not locally repairable).
- **Risk overlay:** **INELIGIBLE** until a forecast gate passes under frozen prereg.

## Bottlenecks removed (cleared for progress)
- Multiple/ambiguous next steps collapsed to **one mandatory path:** TB2 on 2024-01-01..2024-09-30 (or evidence-backed inadmissibility of that route, then immediate pivot to next admissible local route with new ID/prereg).
- TB1 reframed as label/test-event-adequacy failure: pre-freeze event-rate design with >0 frozen-test breaches is required.
- `AGENT_HANDOFF.md`, `FOCUS_CAMPAIGN.md`, and this file synchronized as the canonical handoff set; no polling/status-only work.

## Execution steps (complete in order)

### 1) Re-verify admissibility + provenance (machine evidence)
- Confirm 2024-01-01..2024-09-30 contiguous, required series complete, schema/coverage OK, >=3 non-overlapping 30d blocks in test split, no sealed/reused/outcome-inspected holdout for this design.
- Verify `provenance_verified=true`, `unmapped_count=0` for every input used (funding lineage and other inputs as applicable). Record evidence.
- Save `research_state/trackb_<ID>_admissibility.(json|md)`.
- Tools: `scripts/trackc_panel_admissibility_audit.py`, `scripts/trackc_gap_repair_manifest.py`, `scripts/trackc_funding_schema_audit.py`, `scripts/trackc_provenance_lineage.py` (and relevant tests).

### 2) Pre-freeze label/split design (event-adequate, no threshold shopping)
- Compute breach/event rates for candidate configs (e.g. leverage 5x/10x/20x, side long/short, horizon 24h/72h/168h) and candidate splits **from local data**; select config+split with **>0 positive synthetic breaches in the frozen test split** and defensible support (report counts per split/symbol/overall).
- Fix all choices in prereg before outcomes; no post-freeze tuning/threshold shopping.

### 3) Freeze prereg BEFORE outcomes
- Write `research_state/research_protocol_trackb_<ID>.md` (**FROZEN_BEFORE_OUTCOMES**): modeled breach definition (`scripts/synthetic_boundary_labels.py`), predictors B1 (RV/price-only) vs C2 (funding-conditioned), 60/20/20 chronological splits + 7-day purge/embargo, metrics (Log Loss/Brier), 2% materiality floor, Holm correction, block bootstrap 2000, explicit "synthetic proxy ≠ observed liquidation".
- Compute `prereg_hash` (sha256 of protocol bytes) and record in `research_state/run_manifest.json` with `split_boundaries_trackb_<ID>.frozen_before_outcomes=true`, protocol ref, split boundaries, embargo/purge, timestamp, **`outcome_values_inspected=false` — before any confirmatory outcome computation**.

### 4) Run confirmatory evaluation (heavy)
- Execute Track B pipeline on frozen panel (`scripts/run_trackb_evaluation.py` + `scripts/synthetic_boundary_labels.py`, adapted to new ID/window/label as needed).
- Write `research_state/evaluation_summary_trackb_<ID>.md`: point estimate, 95% CI, relative change, n_instruments, n_obs, n_test_blocks, materiality/gate decision, Holm-adjusted results, synthetic-proxy caveat.

### 5) Propagate verdict and set singular next task
- Update `research_state/hypothesis_registry.json`, `research_state/experiment_frontier.json`, `research_state/negative_results_report.md`, `AGENT_HANDOFF.md`, and this file.
- State overlay eligibility (**NOT ELIGIBLE unless all gates pass**).
- Set one singular, evidence-backed `next_unfinished_task`.

## Fallback (only with evidence)
If 2024-01-01..2024-09-30 is proven inadmissible (e.g. cannot achieve >0 test breaches under any defensible local design, or provenance/schema/coverage fails): document evidence-backed inadmissibility and immediately pivot to the next locally admissible uninspected route with new ID and new prereg (do not stop at planning). Track C concluded NOT_SUPPORTED. Track A STRUCTURALLY_BLOCKED. Overlay INELIGIBLE.

## Acceptance (incomplete without all)
- New frozen prereg + `prereg_hash` recorded in manifest **before outcomes**.
- Machine-verified admissibility/provenance evidence for chosen window/inputs.
- `evaluation_summary_trackb_<ID>.md` with CIs, blocks, explicit gate verdict (or evidence-backed inadmissibility).
- Registries + `AGENT_HANDOFF.md` + `NEXT_SESSION_TASK.md` updated with singular `next_unfinished_task`.

## Verification commands
```bash
python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_funding_schema_audit tests.test_trackc_provenance_lineage -v
python -c "from scripts.trackc_provenance_lineage import verify_paths_with_manifests; from pathlib import Path; res=verify_paths_with_manifests([str(p) for p in Path('research_state/data_cache').rglob('*-fundingRate-*.csv')], repo_root=Path('.')); assert res['provenance_verified'] and res['unmapped_count']==0; print('PROVENANCE_OK', res['files_considered'])"
```

## Hard constraints (NON-NEGOTIABLE)
No network/paid/manual/credentialed data; no fabricated data/provenance; no threshold shopping; no sealed-holdout reuse; no Track A/B/C conflation (Track B = modeled synthetic breach proxies, never observed liquidations); preregister/freeze before outcomes; no risk overlay until forecast gate passes; no `.github/workflows` edits. Heavy, verifiable progress only.
