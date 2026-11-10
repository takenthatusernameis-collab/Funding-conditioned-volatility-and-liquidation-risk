# FOCUS_CAMPAIGN.md — Heavy-Work Execution Plan (Funding-conditioned Volatility & Liquidation Risk)

**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Priority (per repo name):** 1) Track B liquidation boundary risk (modeled) — liquidation risk first per repo name, 2) Track C / H1 funding-conditioned volatility forecast, 3) Track A observed liquidations (blocked).
**Campaign timestamp:** 2026-11-10T16:16:08Z (refreshed; program NOT concluded — untested admissible Track B windows remain)
**Hard constraints (NON-NEGOTIABLE):** no network/paid/manual/credentialed data; no fabricated provenance/outcomes; no threshold shopping; no sealed-holdout reuse; no Track A/B/C conflation; preregister before outcomes; no risk overlay until forecast gate passes; no `.github/workflows` edits.

## Mission (non-optional)
Advance the repo's core question to a reproducible, auditable, out-of-sample verdict using only local verified data: (a) funding-conditioned volatility vs RV-only baseline — **done/concluded NOT_SUPPORTED**, (b) liquidation risk via **Track B modeled boundary breaches** — **PARTIALLY TESTED (one window NOT_SUPPORTED); untested admissible local windows with >=3 blocks remain, so M5 is NEXT and MANDATORY**, or record evidence-backed inadmissibility if every local window is exhausted. Future agents must not idle on status docs, polling, or re-litigation of concluded tracks.

## Current state (verified 2026-11-10T11:30:05Z)
- **Track C / H1_primary: CONCLUDED UNDER CONSTRAINTS, NOT_SUPPORTED.** Panels tested: FCLR-003, FCLR-008, FCLR-009 (NOT_MET), FCLR-012-V (INCONCLUSIVE, 0 blocks), FCLR-013 (NOT_SUPPORTED), FCLR-014 (NOT_MET: 1.14% < 2%, CI crosses zero, 17d/0 blocks). No untested claim-worthy Track C panels with >=3 blocks remain locally. `next_unfinished_task (Track C): NONE`.
- **Track A: STRUCTURALLY_BLOCKED** (no admissible unauthenticated observed-liquidation census). Not locally repairable.
- **Track B: PARTIALLY TESTED** — one confirmatory window executed (TRACKB-20251110T154307Z, 2025-01-01..2025-10-31): gate NOT_MET / NOT_SUPPORTED (C2 vs B1 rel improvement 1.50% < 2%, CI [-0.005, 0.035] crosses zero; modeled proxy only; 4/5 symbols had zero synthetic breaches). **Untested admissible local windows with >=3 blocks remain:** TB1 panel 2025-01-01..2026-10-31 (5 symbols, provenance_verified=true, 2065 files verified, unmapped_count=0, 22 estimated blocks) and 2024-01-01..2024-09-30 (~9 estimated blocks, completeness 1.0). Unblocked by local data (`scripts/synthetic_boundary_labels.py`, 8/8 tests present). **M5 active/mandatory next on an untested window.**
- **Bottlenecks removed:** stale "program concluded / next_unfinished_task: NONE" declaration corrected (see `AGENT_HANDOFF.md`, `NEXT_SESSION_TASK.md`); provenance machine-verified (`provenance_verified=true`, `unmapped_count=0`); funding schema/coverage audited; dep-light gate 48/48 PASS; Track B label primitive + tests present.

## Execution milestones (execute in order; skipping is non-compliant)

### M1 — Track C provenance & admissibility lock — COMPLETE
Evidence: `research_state/trackc_deep_audit_2025_h1_check.json`, `research_state/trackc_deep_audit_2025_full_check.json`, `research_state/funding_schema_audit_2025_h1.json`, provenance lineage checks.

### M2 — Track C prereg before outcomes (FCLR-014) — COMPLETE
`research_state/research_protocol_fclr014.md` v2.0 FROZEN_BEFORE_OUTCOMES; `prereg_hash=8563163c62524605cbf7f11603759aee2210d133f82c3742319a6dd85dfca597`; `split_boundaries_fclr014.frozen_before_outcomes=true`.

### M3 — Track C confirmatory execution (FCLR-014) — COMPLETE
`research_state/evaluation_summary_FCLR-014.md`; gate NOT_MET; H1_primary NOT_SUPPORTED.

### M4 — Track C verdict, registries, handoff — COMPLETE
`research_state/hypothesis_registry.json`, `research_state/experiment_frontier.json`, `research_state/negative_results_report.md`, `AGENT_HANDOFF.md`, `NEXT_SESSION_TASK.md` updated. Overlay INELIGIBLE.

### M5 — Track B modeled liquidation boundary-breach campaign — **ACTIVE / MANDATORY NEXT**
**Objective:** produce a confirmatory, preregistered Track B result (or evidence-backed inadmissibility on all local windows) with no network/new data. **Preferred window:** TB1 panel 2025-01-01..2026-10-31 (fully provenance-verified locally, untested, 22 estimated blocks). Fallback: re-audit 2024-01-01..2024-09-30 (~9 estimated blocks) via deep admissibility + gap + funding-schema audit before confirmatory.

**M5.1 Admissibility lock (verifiable):**
- Select local window: >=5 instruments, contiguous required series (mark/index/premium/klines + funding), **>=3 non-overlapping 30-day blocks in test split**, not sealed/reused/previously outcome-inspected for this Track B design.
- Prove: `provenance_verified=true`, `unmapped_count=0`; schema/coverage OK; no required gaps. Save `research_state/trackb_<ID>_admissibility.(json|md)`.

**M5.2 Freeze prereg BEFORE outcomes (verifiable):**
- Write `research_state/research_protocol_trackb_<ID>.md`: modeled breach definition (leverage/margin, horizon, side), predictors, 60/20/20 splits + 7-day purge/embargo, metrics, 2% materiality floor, Holm, block bootstrap 2000, explicit "synthetic proxy ≠ observed liquidation".
- Record `prereg_hash` and `split_boundaries_trackb_<ID>.frozen_before_outcomes=true` in `research_state/run_manifest.json` prior to any outcome computation. Compute hash from frozen protocol content.

**M5.3 Execute & evaluate (heavy):**
- Run Track B pipeline on frozen panel; output `research_state/evaluation_summary_trackb_<ID>.md` with point estimate, 95% CI, relative change, n_instruments, n_obs, n_test_blocks, materiality/gate decision.

**M5.4 Verdict & propagation:**
- Update hypothesis registry/frontier/negative-results; state overlay eligibility (NOT ELIGIBLE unless all gates pass). Record exact `next_unfinished_task`.

**Acceptance (all required for M5 completion):** frozen prereg with hash recorded before outcomes; admissibility evidence saved; evaluation summary with CIs/blocks; gate verdict explicit; registries + AGENT_HANDOFF + NEXT_SESSION_TASK updated.

### M6 — Program conclusion or next route — CONDITIONAL
- If Track B passes gate: preregister next confirmatory/overlay-eligibility step per protocol (no premature overlay).
- If Track B fails/inconclusive on all admissible local windows with >=3 blocks: set `next_unfinished_task: NONE — program concluded under constraints pending new admissible unauthenticated source`; keep Track A STRUCTURALLY_BLOCKED, Track C concluded.
- If a materially different local window remains: M5 repeats on that window only (new ID, new prereg).

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
