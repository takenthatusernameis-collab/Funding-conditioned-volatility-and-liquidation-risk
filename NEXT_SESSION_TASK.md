# NEXT_SESSION_TASK.md — SINGLE DURABLE HANDOFF (INITIAL TASK MESSAGE)

**Timestamp (UTC):** 2026-11-10T18:58:30Z
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Program status:** `ACTIVE_TRACKB_MANDATORY` — NOT concluded. This file is the **single authoritative initial task message** for the next agentic session. Execute it before any other work. Do not relitigate concluded tracks, do not poll, and do not produce status-only output.

## IMMEDIATE MANDATORY TASK (heavy, verifiable — start now)
Execute **Track B TB2 confirmatory attempt** on local panel **2024-01-01..2024-09-30** (BTCUSDT/ETHUSDT/BNBUSDT/SOLUSDT/XRPUSDT). **TB1 is resolved as DEGENERATE/INADMISSIBLE** for confirmatory evaluation (frozen test split 2026-06-26..2026-10-31 had 0 synthetic breaches at 5x/24h long; `research_state/evaluation_summary_trackb_TB1_20261110T173838Z.md`). **Do not rerun TB1 unchanged.**

**Objective:** produce a preregistered, leakage-resistant Track B verdict (or evidence-backed inadmissibility of this local route) using **modeled synthetic boundary breaches only** (never observed liquidations). The NEW frozen design must have **>0 positive labels in the frozen test split** (report counts per split/symbol/overall with rationale). No threshold shopping after freeze.

## Verified context (do not reopen)
- **Track B:** TB1 DEGENERATE/INADMISSIBLE; prior `TRACKB-20251110T154307Z` NOT_MET/NOT_SUPPORTED. TB2 candidate panel 2024-01-01..2024-09-30 appears locally present (contiguous required series, funding months/files, ~9 non-overlapping 30d blocks) but **must be re-verified** for all inputs used.
- **Starting evidence (re-verify, do not trust blindly):** `research_state/trackb_TB2_admissibility.json`, `research_state/trackb_TB2_admissibility_2024q1q3.json`, `research_state/trackb_TB1_admissibility_2024q1q3.json`, `research_state/trackb_window_candidates_fast.json`.
- **Track C / H1:** concluded **NOT_SUPPORTED** on claim-worthy local panels; no untested claim-worthy Track C panels with >=3 blocks remain (`next_unfinished_task (Track C): NONE`).
- **Track A:** **STRUCTURALLY_BLOCKED** (no admissible unauthenticated observed-liquidation census; not locally repairable).
- **Risk overlay:** **INELIGIBLE** until a forecast gate passes under frozen prereg.

## Bottlenecks removed / execution cleared
- Single mandatory path: TB2 on 2024-01-01..2024-09-30 (or evidence-backed inadmissibility of that route, then immediate pivot to next admissible local uninspected route with new ID/prereg).
- TB1 reframed as event-adequacy failure: pre-freeze breach-rate analysis and >0 frozen-test positives are required.
- Canonical handoffs synchronized (`AGENT_HANDOFF.md`, `FOCUS_CAMPAIGN.md`, this file). No polling, no status-only loops, no relitigation of Track A/C or prior TB verdicts.

## Execution steps (complete in order; heavy work only)

### 1) Re-verify admissibility + provenance (machine evidence)
- Confirm 2024-01-01..2024-09-30 is contiguous and complete for required series (mark/index/premium/klines + funding) for BTCUSDT/ETHUSDT/BNBUSDT/SOLUSDT/XRPUSDT, schema/coverage OK, >=3 non-overlapping 30d blocks in the intended test split, and not sealed/reused/outcome-inspected for this TB2 design.
- Verify `provenance_verified=true`, `unmapped_count=0` for every input actually used (funding lineage and other inputs as applicable). Record evidence.
- Save/refresh `research_state/trackb_TB2_<ID>_admissibility.(json|md)` with verified results.
- Tools: `scripts/trackc_panel_admissibility_audit.py`, `scripts/trackc_gap_repair_manifest.py`, `scripts/trackc_funding_schema_audit.py`, `scripts/trackc_provenance_lineage.py` (and Track B helpers as needed).

### 2) Pre-freeze label/split design (event-adequate, no threshold shopping)
- Compute synthetic breach/event rates for candidate configs (e.g. leverage 5x/10x/20x, side long/short, horizons 24h/72h/168h) and candidate splits **from local data**.
- Select config + split with **>0 positive synthetic breaches in the frozen test split** and defensible support (report counts per split/symbol/overall). If no defensible local design yields >0 test breaches for this window, treat as inadmissible (see Fallback).
- Fix all choices in prereg before outcomes; no post-freeze tuning/threshold shopping.

### 3) Freeze prereg BEFORE outcomes
- Write `research_state/research_protocol_trackb_<ID>.md` (**FROZEN_BEFORE_OUTCOMES**): modeled breach definition (`scripts/synthetic_boundary_labels.py`), predictors B1 (RV/price-only) vs C2 (funding-conditioned), 60/20/20 chronological splits + 7-day purge/embargo, metrics (Log Loss/Brier), 2% materiality floor, Holm correction, block bootstrap 2000, explicit "synthetic proxy ≠ observed liquidation".
- Compute `prereg_hash` (sha256 of protocol bytes) and record in `research_state/run_manifest.json` with `split_boundaries_trackb_<ID>.frozen_before_outcomes=true`, protocol ref, split boundaries, embargo/purge, timestamp, and **`outcome_values_inspected=false` — all before any confirmatory outcome computation**.

### 4) Run confirmatory evaluation (heavy)
- Execute Track B pipeline on frozen panel (`scripts/run_trackb_evaluation.py` + `scripts/synthetic_boundary_labels.py`, adapted to new ID/window/label as needed).
- Write `research_state/evaluation_summary_trackb_<ID>.md`: point estimate, 95% CI, relative change, n_instruments, n_obs, n_test_blocks, materiality/gate decision, Holm-adjusted results, synthetic-proxy caveat.

### 5) Propagate verdict and set singular next task
- Update `research_state/hypothesis_registry.json`, `research_state/experiment_frontier.json`, `research_state/negative_results_report.md`, `AGENT_HANDOFF.md`, and this file.
- State overlay eligibility (**NOT ELIGIBLE unless all gates pass**).
- Set one singular, evidence-backed `next_unfinished_task`.

## Fallback (only with evidence)
If 2024-01-01..2024-09-30 is proven inadmissible (cannot achieve >0 frozen-test breaches under any defensible local design, or provenance/schema/coverage fails): document evidence-backed inadmissibility and immediately pivot to the next locally admissible uninspected route with new ID and new prereg (do not stop at planning). Track C concluded NOT_SUPPORTED. Track A STRUCTURALLY_BLOCKED. Overlay INELIGIBLE.

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
