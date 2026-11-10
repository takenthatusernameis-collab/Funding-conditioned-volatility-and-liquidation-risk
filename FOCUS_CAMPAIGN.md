# FOCUS_CAMPAIGN.md — Heavy-Work Execution Plan (Funding-conditioned Volatility & Liquidation Risk)

**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Priority (per repo name):** 1) Track B liquidation boundary risk (modeled) — **ACTIVE/MANDATORY**, 2) Track C / H1 funding-conditioned volatility forecast — concluded NOT_SUPPORTED, 3) Track A observed liquidations — STRUCTURALLY_BLOCKED.
**Campaign timestamp:** 2026-11-10T18:55:10Z (refreshed; program NOT concluded — TB1 degenerate; TB2 mandatory on 2024-01-01..2024-09-30)
**Single durable handoff (authoritative):** `NEXT_SESSION_TASK.md` (+ `AGENT_HANDOFF.md` pointer). Execute `NEXT_SESSION_TASK.md` as the initial task message.
**Hard constraints (NON-NEGOTIABLE):** no network/paid/manual/credentialed data; no fabricated provenance/outcomes; no threshold shopping; no sealed-holdout reuse; no Track A/B/C conflation; preregister before outcomes; no risk overlay until forecast gate passes; no `.github/workflows` edits.

## Mission (non-optional)
Advance the repo's core question to a reproducible, auditable, out-of-sample verdict using only local verified data: (a) funding-conditioned volatility vs RV-only baseline — **done/concluded NOT_SUPPORTED**, (b) liquidation risk via **Track B modeled boundary breaches** — **MANDATORY NEXT (TB2)** after TB1 degenerate test split, or record evidence-backed inadmissibility if every local route is exhausted. Future agents must not idle on status docs, polling, or re-litigation of concluded tracks.

## Current state (verified 2026-11-10T18:09:05Z)
- **Track C / H1_primary: CONCLUDED UNDER CONSTRAINTS, NOT_SUPPORTED.** No untested claim-worthy Track C panels with >=3 blocks remain locally. `next_unfinished_task (Track C): NONE`.
- **Track A: STRUCTURALLY_BLOCKED** (no admissible unauthenticated observed-liquidation census). Not locally repairable.
- **Track B: PARTIALLY TESTED / ACTIVE**
  - `TRACKB-20251110T154307Z` (2025-01-01..2025-10-31): NOT_MET/NOT_SUPPORTED (modeled proxy).
  - `TRACKB-MODELED-BREACH-TB1-20261110T173838Z` (2025-01-01..2026-10-31): **DEGENERATE/INADMISSIBLE** for confirmatory 5x/24h long label — frozen test split 2026-06-26..2026-10-31 had ZERO synthetic breaches (all symbols). Gate NOT_MET; metrics uninterpretable. (`research_state/evaluation_summary_trackb_TB1_20261110T173838Z.md`)
  - **Next local route (heavy, untested):** 2024-01-01..2024-09-30, 5 symbols (BTC/ETH/BNB/SOL/XRP), contiguous required series complete, funding schema OK, `provenance_verified=true`/`unmapped_count=0` (funding lineage PROVENANCE_OK 161), ~9 non-overlapping 30d blocks. Evidence: `research_state/trackb_TB1_admissibility_2024q1q3.json`, `research_state/trackb_window_candidates_fast.json`.
- **Bottlenecks removed:** stale "preferred TB1 window" replaced by TB1-degenerate finding; single mandatory TB2 path set; handoff consolidated in `NEXT_SESSION_TASK.md`/`AGENT_HANDOFF.md`; provenance + canonical tests re-verified (35 PASS, 2026-11-10T18:09Z).

## Execution milestones (execute in order; skipping is non-compliant)

### M1–M4 — Track C provenance, prereg, execution, verdict — COMPLETE
Track C concluded NOT_SUPPORTED on claim-worthy local panels (see `NEXT_SESSION_TASK.md`/`AGENT_HANDOFF.md`). Overlay INELIGIBLE.

### M5 — Track B modeled liquidation boundary-breach campaign (TB2) — **ACTIVE / MANDATORY NEXT**
**Objective:** produce a confirmatory, preregistered Track B result on local panel **2024-01-01..2024-09-30** (or evidence-backed inadmissibility) with no network/new data. **TB1 (2025-01-01..2026-10-31) is resolved as DEGENERATE** for 5x/24h long label (zero test breaches) — do not rerun TB1 without a materially different frozen design justified by pre-freeze event-adequacy evidence.

**M5.1 Admissibility lock (verifiable):**
- Re-verify 2024-01-01..2024-09-30: 5 symbols, contiguous required series (mark/index/premium/klines + funding), schema/coverage OK, `provenance_verified=true`, `unmapped_count=0` for all inputs used, >=3 non-overlapping 30d blocks in test split, not sealed/reused/outcome-inspected for this Track B design.
- Save `research_state/trackb_<ID>_admissibility.(json|md)`.

**M5.2 Label design & freeze prereg BEFORE outcomes (verifiable):**
- Compute candidate breach/event rates (leverage/side/horizon, split options) from local data and select a config with **>0 positive labels in the frozen test split** and defensible support (report counts). No threshold shopping after freeze.
- Write `research_state/research_protocol_trackb_<ID>.md` (FROZEN_BEFORE_OUTCOMES): modeled breach definition, predictors (B1 vs C2), 60/20/20 splits + 7-day purge/embargo, metrics, 2% materiality floor, Holm, block bootstrap 2000, explicit "synthetic proxy ≠ observed liquidation".
- Record `prereg_hash` and `split_boundaries_trackb_<ID>.frozen_before_outcomes=true` in `research_state/run_manifest.json` prior to any confirmatory outcome computation.

**M5.3 Execute & evaluate (heavy):**
- Run Track B pipeline on frozen panel; output `research_state/evaluation_summary_trackb_<ID>.md` with point estimate, 95% CI, relative change, n_instruments, n_obs, n_test_blocks, materiality/gate decision.

**M5.4 Verdict & propagation:**
- Update `hypothesis_registry.json`, `experiment_frontier.json`, `negative_results_report.md`; state overlay eligibility (NOT ELIGIBLE unless all gates pass). Record exact `next_unfinished_task`. Update `AGENT_HANDOFF.md` + `NEXT_SESSION_TASK.md`.

**Acceptance (all required):** frozen prereg+hash before outcomes; admissibility/provenance evidence; evaluation summary with CIs/blocks and explicit gate verdict (or evidence-backed inadmissibility); registries + handoffs updated.

### M6 — Program conclusion or next route — CONDITIONAL
- If Track B passes gate: preregister next confirmatory/overlay-eligibility step per protocol (no premature overlay).
- If 2024Q1-Q3 and all other admissible local routes are exhausted/inadmissible with evidence: set `next_unfinished_task: NONE — program concluded under constraints pending new admissible unauthenticated source`; keep Track A STRUCTURALLY_BLOCKED, Track C concluded.
- If another materially different admissible local route remains: M5 repeats on that route only (new ID, new prereg).

## Execution rules (enforced)
1. **Prereg before outcomes:** no label/outcome inspection before freeze+hash in manifest.
2. **No threshold shopping / no holdout reuse.**
3. **No Track conflation:** Track B outputs are modeled breach proxies, never observed liquidations.
4. **No fabricated provenance, no network/paid/manual data.**
5. **Preserve nulls/inconclusive results** in `research_state/negative_results_report.md`.
6. **Heavy work only:** every session delivers a substantive verifiable result (admissibility evidence, frozen prereg, executed eval, recomputation, or evidence-backed blocker on a specific local route).
7. **Single durable handoff:** keep `AGENT_HANDOFF.md` + `NEXT_SESSION_TASK.md` current with timestamp, evidence paths, gate states, and one `next_unfinished_task`.

## Canonical verification
```bash
python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_gap_repair_manifest tests.test_trackc_funding_schema_audit tests.test_trackc_panel_window_planner.TestPanelWindowPlanner.test_contiguous_sequences tests.test_trackc_panel_window_planner.TestPanelWindowPlanner.test_cli_smoke tests.test_trackc_panel_deep_audit_orchestrator tests.test_trackc_provenance_lineage -v
python -c "from scripts.trackc_provenance_lineage import verify_paths_with_manifests; from pathlib import Path; files=list(Path('research_state/data_cache').rglob('*-fundingRate-*.csv')); res=verify_paths_with_manifests([str(p) for p in files], repo_root=Path('.')); assert res['provenance_verified'] and res['unmapped_count']==0; print('PROVENANCE_OK', res['files_considered'])"
python -m unittest tests.test_synthetic_boundary_labels -v
```

## Exit criteria
Campaign ends only when: (1) a gate-passing Track B/Track C result is recorded with full evidence and eligible next step preregistered, OR (2) all admissible local Track B/C routes with >=3 blocks are exhausted with preserved results and `next_unfinished_task: NONE` pending a new admissible unauthenticated source, with Track A structural block documented. No other stopping condition is acceptable.
