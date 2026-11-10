# NEXT_SESSION_TASK.md — SINGLE DURABLE HANDOFF (INITIAL TASK MESSAGE)

**Timestamp (UTC):** 2026-11-10T19:04:05Z
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Program status:** `ACTIVE_TRACKB_MANDATORY` — NOT concluded. This file is the **single authoritative initial task message** for the next agentic session. Execute it before any other work. Do not relitigate concluded tracks, do not poll, and do not produce status-only output.

## IMMEDIATE MANDATORY TASK (heavy, verifiable — start now)
Execute **Track B TB2 confirmatory evaluation** on the frozen local panel **2024-01-01..2024-09-30** (BTCUSDT/ETHUSDT/BNBUSDT/SOLUSDT/XRPUSDT). **TB1 is resolved as DEGENERATE/INADMISSIBLE** for confirmatory evaluation (frozen test split 2026-06-26..2026-10-31 had 0 synthetic breaches at 5x/24h long; `research_state/evaluation_summary_trackb_TB1_20261110T173838Z.md`). **Do not rerun TB1 unchanged.**

**Pre-freeze state (already locked — do not reopen):**
- Admissibility+provenance verified: `research_state/trackb_TB2_admissibility.json` + `_2024q1q3.json` (5 symbols, 274 days, >=3 test blocks, required_series_complete, provenance_verified=true, unmapped_count=0).
- Label/split selected pre-freeze with **>0 frozen-test positives**: leverage=10.0, side=long, horizon=168h, m=0.0 → test 619/4925 positives (12.6%), all 5 symbols >0. Candidate-scan evidence: `research_state/trackb_TB2_label_design_scan.json`. **No threshold shopping after freeze.**
- Frozen prereg: `research_state/research_protocol_trackb_TB2_20261110T190405Z.md` (`FROZEN_BEFORE_OUTCOMES`); `prereg_hash=9de16e7d2b2c80f6ac57d87b6eb150c145bfe9f3168d7ac3d94472f740f7b91f` recorded in `research_state/run_manifest.json` with `split_boundaries_trackb_TB2_20261110T190405Z.frozen_before_outcomes=true` and `outcome_values_inspected=false` — **all before any confirmatory outcome computation**.
- Splits: train 2024-01-01..2024-06-12 / val 2024-06-19..2024-08-06 / test 2024-08-13..2024-09-30 (7-day purge/embargo).

**Objective:** produce a preregistered, leakage-resistant Track B verdict (or evidence-backed inadmissibility of this local route) using **modeled synthetic boundary breaches only** (never observed liquidations). Report counts per split/symbol/overall with rationale.

## Execution steps (complete in order; heavy work only)

### 1) Run confirmatory evaluation on frozen panel (heavy)
- Execute Track B pipeline on frozen TB2 panel (`scripts/run_trackb_evaluation.py` + `scripts/synthetic_boundary_labels.py`, adapted to TB2 ID/window/label/splits as needed). No post-freeze tuning/threshold shopping.
- Write `research_state/evaluation_summary_trackb_TB2_20261110T190405.md`: point estimate, 95% CI, relative change, n_instruments, n_obs, n_test_blocks, materiality/gate decision, Holm-adjusted results, synthetic-proxy caveat.

### 2) Propagate verdict and set singular next task
- Update `research_state/hypothesis_registry.json`, `research_state/experiment_frontier.json`, `research_state/negative_results_report.md`, `AGENT_HANDOFF.md`, and this file.
- State overlay eligibility (**NOT ELIGIBLE unless all gates pass**).
- Set one singular, evidence-backed `next_unfinished_task`.

## Fallback (only with evidence)
If 2024-01-01..2024-09-30 is proven inadmissible (cannot achieve >0 frozen-test breaches under the frozen defensible design, or provenance/schema/coverage fails): document evidence-backed inadmissibility and immediately pivot to the next locally admissible uninspected route with new ID and new prereg (do not stop at planning). Track C concluded NOT_SUPPORTED. Track A STRUCTURALLY_BLOCKED. Overlay INELIGIBLE.

## Acceptance (incomplete without all)
- Confirmatory evaluation run on frozen TB2 splits with no post-freeze tuning.
- `evaluation_summary_trackb_TB2_20261110T190405.md` with CIs, blocks, explicit gate verdict (or evidence-backed inadmissibility).
- Registries + `AGENT_HANDOFF.md` + `NEXT_SESSION_TASK.md` updated with singular `next_unfinished_task`.

## Verification commands
```bash
python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_funding_schema_audit tests.test_trackc_provenance_lineage -v
python -c "from scripts.trackc_provenance_lineage import verify_paths_with_manifests; from pathlib import Path; res=verify_paths_with_manifests([str(p) for p in Path('research_state/data_cache').rglob('*-fundingRate-*.csv')], repo_root=Path('.')); assert res['provenance_verified'] and res['unmapped_count']==0; print('PROVENANCE_OK', res['files_considered'])"
```

## Hard constraints (NON-NEGOTIABLE)
No network/paid/manual/credentialed data; no fabricated data/provenance; no threshold shopping; no sealed-holdout reuse; no Track A/B/C conflation (Track B = modeled breach proxy only, never observed liquidations); preregister/freeze before outcomes; no risk overlay until forecast gate passes; no `.github/workflows` edits. Heavy, verifiable progress only.
