# NEXT_SESSION_TASK.md — SINGLE DURABLE HANDOFF (2026-11-10T18:40:04Z)

> **IMMEDIATE MANDATORY TASK (heavy, verifiable — start here, no narration-only work):**
> Execute **Track B TB2 confirmatory attempt** on local panel **2024-01-01..2024-09-30** (BTC/ETH/BNB/SOL/XRP, ~9 non-overlapping 30d blocks, deep-audited: contiguous required series, funding schema OK, `provenance_verified=true`, `unmapped_count=0` per `research_state/trackb_TB1_admissibility_2024q1q3.json`/`trackb_window_candidates_fast.json`).
> TB1 (`2025-01-01..2026-10-31`, 5x/24h long) is **DEGENERATE/INADMISSIBLE** — frozen test split had **0 synthetic breaches** (see `research_state/evaluation_summary_trackb_TB1_20261110T173838Z.md`). Do **not** rerun TB1 unchanged. TB2 must use a **NEW label+split design with >0 positive labels in the frozen test split** (report counts/evidence), defensible prereg rationale, and **no threshold shopping after freeze**.

**Repo:** `Funding-conditioned-volatility-and-liquidation-risk` (priority per name: 1. Track B liquidation risk, 2. Track C funding-conditioned volatility, 3. Track A observed liquidations)
**Campaign:** `TRACKB-TB2-2024Q1Q3-<NEW_ID_ON_FREEZE>`
**Program status:** `ACTIVE_TRACKB_MANDATORY` — NOT concluded.

## Verified state (2026-11-10T18:09–18:40Z context)
- **Track B / TB1:** DEGENERATE/INADMISSIBLE for confirmatory 5x/24h long (zero test breaches). Evidence: `research_state/evaluation_summary_trackb_TB1_20261110T173838Z.md`, `research_state/research_protocol_trackb_TB1_20261110T173838Z.md`, manifest `split_boundaries_trackb_TB1_20261110T173838Z`.
- **Track B / prior:** `TRACKB-20251110T154307Z` (2025-01-01..2025-10-31) NOT_MET/NOT_SUPPORTED.
- **Fallback local panel (untested, next route):** 2024-01-01..2024-09-30, 5 symbols, required series complete, schema/provenance OK. Evidence: `research_state/trackb_TB1_admissibility_2024q1q3.json`, `research_state/trackb_window_candidates_fast.json`.
- **Track C:** concluded NOT_SUPPORTED on claim-worthy local panels; `next_unfinished_task (Track C): NONE`.
- **Track A:** STRUCTURALLY_BLOCKED (no admissible unauthenticated observed-liquidation census).
- **Risk overlay:** INELIGIBLE (no gate-passing forecast).
- **Provenance:** funding lineage `PROVENANCE_OK 161` in `research_state/data_cache` (unmapped=0) — re-verify for all inputs actually used in TB2.
- **Canonical tests:** 35 PASS — `tests.test_volatility_features_splits`, `tests.test_synthetic_boundary_labels`, `tests.test_trackc_panel_admissibility_audit`, `tests.test_trackc_funding_schema_audit`, `tests.test_trackc_provenance_lineage`.

## Bottlenecks removed (do not relitigate)
- Stale/ambiguous "preferred TB1 window" and multi-path options collapsed to **one mandatory TB2 execution task** on 2024-01-01..2024-09-30. No relitigation of TB1/Track C/Track A.
- TB1 failure framed as label/test-event-adequacy issue forcing pre-freeze event-rate design (>0 test breaches required before freeze).
- Track C concluded NOT_SUPPORTED; Track A STRUCTURALLY_BLOCKED; overlay INELIGIBLE. Future agents must not idle on status docs, polling, or re-litigation of concluded tracks.

## Concrete execution steps (complete in order)

### Step 1 — Re-verify admissibility + provenance (machine evidence)
- Confirm 2024-01-01..2024-09-30 is contiguous, required series complete (mark/index/premium/klines + funding), schema OK, >=3 non-overlapping 30d test blocks, no sealed/reused/outcome-inspected holdout for this design, `provenance_verified=true`, `unmapped_count=0` for every input used.
- Save `research_state/trackb_<ID>_admissibility.(json|md)`.
- Verify via: `scripts/trackc_panel_admissibility_audit.py`, `scripts/trackc_gap_repair_manifest.py`, `scripts/trackc_funding_schema_audit.py`, `scripts/trackc_provenance_lineage.py`.

### Step 2 — Label/window design (pre-freeze, event-adequate)
- Compute breach/event rates for candidate configs (leverage 5x/10x/20x, side long/short, horizon 24h/72h/168h) and splits from local data; select config+split with **>0 positive synthetic breaches in frozen test split** and adequate support (report counts).
- Document rationale in prereg. No threshold shopping after freeze.

### Step 3 — Freeze prereg BEFORE outcomes
- Write `research_state/research_protocol_trackb_<ID>.md` (FROZEN_BEFORE_OUTCOMES): modeled breach definition (`scripts/synthetic_boundary_labels.py`), predictors (B1 vs C2), 60/20/20 chronological splits + 7-day purge/embargo, metrics (Log Loss / Brier), 2% materiality floor, Holm, block bootstrap 2000, explicit "synthetic proxy ≠ observed liquidation".
- Record `prereg_hash` (sha256 of protocol bytes) and `split_boundaries_trackb_<ID>.frozen_before_outcomes=true` in `research_state/run_manifest.json` **prior to any confirmatory outcome computation**.
- Manifest entry must include `outcome_values_inspected=false`.

### Step 4 — Run confirmatory evaluation (heavy)
- Execute Track B pipeline on frozen panel (`scripts/run_trackb_evaluation.py` + `scripts/synthetic_boundary_labels.py`, adapted to the new ID/window/label).
- Write `research_state/evaluation_summary_trackb_<ID>.md` with point estimate, 95% CI, relative change, n_instruments, n_obs, n_test_blocks, materiality/gate decision, Holm-adjusted results.

### Step 5 — Propagate verdict
- Update `research_state/hypothesis_registry.json`, `research_state/experiment_frontier.json`, `research_state/negative_results_report.md`, `AGENT_HANDOFF.md`, and this file.
- State overlay eligibility (NOT ELIGIBLE unless all gates pass).
- Set one singular `next_unfinished_task`.

## Fallback only if 2024Q1-Q3 fails re-audit
Pivot to the next locally admissible uninspected window/label design with evidence-backed inadmissibility for 2024Q1-Q3; new ID, new prereg, same rigor. Do not stop at planning. Track C concluded NOT_SUPPORTED. Track A STRUCTURALLY_BLOCKED. Overlay INELIGIBLE.

## Acceptance (session incomplete without)
- New frozen prereg with `prereg_hash` recorded in manifest before outcomes.
- Machine-verified admissibility/provenance evidence for chosen window/inputs.
- `evaluation_summary_trackb_<ID>.md` with CIs, blocks, and explicit gate verdict (or evidence-backed inadmissibility if no admissible local route remains).
- Registries + `AGENT_HANDOFF.md` + `NEXT_SESSION_TASK.md` updated with singular, evidence-backed `next_unfinished_task`.

## Verification commands
```bash
python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_funding_schema_audit tests.test_trackc_provenance_lineage -v
python -c "from scripts.trackc_provenance_lineage import verify_paths_with_manifests; from pathlib import Path; res=verify_paths_with_manifests([str(p) for p in Path('research_state/data_cache').rglob('*-fundingRate-*.csv')], repo_root=Path('.')); assert res['provenance_verified'] and res['unmapped_count']==0; print('PROVENANCE_OK', res['files_considered'])"
```

## Hard constraints (NON-NEGOTIABLE)
No network/paid/manual/credentialed data; no fabricated data/provenance; no threshold shopping; no sealed-holdout reuse; no Track A/B/C conflation (Track B = modeled synthetic breach proxies, never observed liquidations); preregister/freeze before outcomes; no risk overlay until forecast gate passes; no `.github/workflows` edits. Heavy, verifiable progress only.
