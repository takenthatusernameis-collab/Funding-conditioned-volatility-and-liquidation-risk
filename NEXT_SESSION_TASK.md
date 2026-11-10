# NEXT_SESSION_TASK.md — SINGLE DURABLE HANDOFF (2026-11-10T18:09:05Z)

**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Priority (repo-name):** 1) Track B liquidation risk (modeled boundary breaches) — **ACTIVE**, 2) Track C funding-conditioned volatility — **concluded NOT_SUPPORTED on claim-worthy local panels**, 3) Track A observed liquidations — **STRUCTURALLY_BLOCKED**.
**Campaign:** `TRACKB-TB2-2024Q1Q3-<NEW_ID_ON_FREEZE>` (next confirmatory attempt)
**Program status:** `ACTIVE_TRACKB_MANDATORY` — not concluded.

## STATE (verified 2026-11-10T18:09:05Z)
- **TB1 (`TRACKB-MODELED-BREACH-TB1-20261110T173838Z`, 2025-01-01..2026-10-31, 5 symbols):** executed; **DEGENERATE/INADMISSIBLE for confirmatory 5x/24h long label** — frozen test split 2026-06-26..2026-10-31 has **ZERO synthetic breaches** (all symbols). Gate NOT_MET; metrics uninterpretable. Evidence: `research_state/evaluation_summary_trackb_TB1_20261110T173838Z.md`, `research_state/research_protocol_trackb_TB1_20261110T173838Z.md`, manifest `split_boundaries_trackb_TB1_20261110T173838Z` (prereg_hash `5e0759...`, frozen_before_outcomes=true).
- **Prior Track B:** `TRACKB-20251110T154307Z` (2025-01-01..2025-10-31) NOT_MET/NOT_SUPPORTED.
- **Fallback local panel (deep-audited, untested):** 2024-01-01..2024-09-30, 5 symbols (BTC/ETH/BNB/SOL/XRP), contiguous, required series complete, funding schema OK, `provenance_verified=true`, `unmapped_count=0`, `panel_non_overlapping_30d_blocks_estimate=9`. Evidence: `research_state/trackb_TB1_admissibility_2024q1q3.json`, `research_state/trackb_window_candidates_fast.json`. Procedural blockers only: needs NEW frozen prereg before outcomes + machine-verified provenance checksums recorded in that session's evidence.
- **Provenance (repo cache):** `PROVENANCE_OK 161` for funding CSV lineage (2026-11-10T18:05Z, unmapped=0). For any confirmatory window, record/verify provenance for all required inputs actually used.
- **Track C:** concluded NOT_SUPPORTED (no untested claim-worthy panels with >=3 blocks). `next_unfinished_task (Track C): NONE`.
- **Track A:** STRUCTURALLY_BLOCKED (no admissible unauthenticated observed-liquidation census). No local repair.
- **Risk overlay:** INELIGIBLE (no gate-passing forecast).
- **Canonical tests:** 35 PASS (`tests.test_volatility_features_splits`, `tests.test_synthetic_boundary_labels`, `tests.test_trackc_panel_admissibility_audit`, `tests.test_trackc_funding_schema_audit`, `tests.test_trackc_provenance_lineage`, 2026-11-10T18:09Z).

## SINGLE MANDATORY INITIAL TASK (heavy, verifiable — do not narrate, do not relitigate)
**`next_unfinished_task`:** Execute Track B confirmatory attempt TB2 on local panel **2024-01-01..2024-09-30** with a **NEW label design selected for test-window event adequacy**: (1) re-verify deep admissibility + provenance for this exact window/inputs, (2) inspect full-window/test-window breach rates for candidate label configs (leverage/side/horizon) and choose one with >0 test-split events and defensible prereg rationale, (3) freeze NEW prereg + manifest `split_boundaries_trackb_<ID>` with `prereg_hash` and `frozen_before_outcomes=true` **before any outcome computation used for confirmatory evaluation**, (4) run confirmatory evaluation and write `research_state/evaluation_summary_trackb_<ID>.md` with point estimates, 95% CI, relative change, n_instruments, n_obs, n_test_blocks, and explicit gate verdict, (5) update hypothesis/frontier/negative-results and this handoff with singular next step.

### Concrete execution steps
1. **Admissibility/provenance (re-verify, machine evidence):** confirm 2024-01-01..2024-09-30 still meets: 5 symbols, contiguous required series (mark/index/premium/klines + funding), schema OK, >=3 non-overlapping 30d test blocks, no sealed/reused/outcome-inspected holdout for this design, `provenance_verified=true`, `unmapped_count=0` for all inputs used. Save `research_state/trackb_<ID>_admissibility.(json|md)`.
2. **Label & window design (must avoid TB1 degenerate failure):** using only local data, compute breach/event rates for candidate configs (e.g. 5x/10x/20x, long/short, 24h/72h/168h) over candidate splits; select config+split with >0 positive labels in frozen test split and adequate support (report counts). Document choice in prereg; no threshold shopping after freeze.
3. **Freeze prereg BEFORE outcomes:** write `research_state/research_protocol_trackb_<ID>.md` (FROZEN_BEFORE_OUTCOMES) specifying modeled breach definition, predictors (B1 vs C2), 60/20/20 chronological splits + 7-day purge/embargo, metrics, 2% materiality floor, Holm, block bootstrap 2000, and "synthetic proxy ≠ observed liquidation". Record `prereg_hash` and `split_boundaries_trackb_<ID>.frozen_before_outcomes=true` in `research_state/run_manifest.json` prior to confirmatory outcome computation.
4. **Run & evaluate:** execute Track B pipeline on frozen panel; output `research_state/evaluation_summary_trackb_<ID>.md` (estimates, 95% CI, relative change, n_instruments, n_obs, n_test_blocks, materiality/gate).
5. **Verdict & propagation:** update `research_state/hypothesis_registry.json`, `research_state/experiment_frontier.json`, `research_state/negative_results_report.md`, `AGENT_HANDOFF.md`, `NEXT_SESSION_TASK.md`. State overlay eligibility (NOT ELIGIBLE unless all gates pass). Set singular `next_unfinished_task`.

### Fallback only if 2024-01-01..2024-09-30 fails re-audit
If this panel is shown inadmissible with evidence, pivot to the next locally admissible uninspected window/label design (new ID, new prereg) and document why 2024Q1-Q3 failed; do not stop at planning.

## Acceptance (session incomplete without)
- New frozen prereg with `prereg_hash` recorded in manifest before outcomes.
- Machine-verified provenance/admissibility evidence for chosen window and inputs.
- `evaluation_summary_trackb_<ID>.md` with CIs, blocks, and explicit gate verdict (or evidence-backed inadmissibility if no admissible route remains).
- Registries + handoff files updated; `next_unfinished_task` singular and evidence-backed.

## Verification
```bash
python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_funding_schema_audit tests.test_trackc_provenance_lineage -v
python -c "from scripts.trackc_provenance_lineage import verify_paths_with_manifests; from pathlib import Path; res=verify_paths_with_manifests([str(p) for p in Path('research_state/data_cache').rglob('*-fundingRate-*.csv')], repo_root=Path('.')); assert res['provenance_verified'] and res['unmapped_count']==0; print('PROVENANCE_OK', res['files_considered'])"
```

## Hard constraints (NON-NEGOTIABLE)
No network/paid/manual/credentialed data; no fabricated data/provenance; no threshold shopping; no sealed-holdout reuse; no Track A/B/C conflation (Track B = modeled synthetic breach proxies, never observed liquidations); preregister/freeze before outcomes; no risk overlay until forecast gate passes; no `.github/workflows` edits. Deliver heavy, verifiable progress only.
