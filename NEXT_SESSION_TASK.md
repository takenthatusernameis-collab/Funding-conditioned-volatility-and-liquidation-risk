# NEXT_SESSION_TASK.md — Single Durable Initial Task for Next Agentic Session
**Timestamp (UTC):** 2026-11-10T16:16:08Z
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Project priority (by repo name):** 1) liquidation risk — Track B modeled boundary breaches, 2) funding-conditioned volatility — Track C (concluded NOT_SUPPORTED), 3) Track A observed liquidations (STRUCTURALLY_BLOCKED).

## Current verdicts (do not relitigate)
- **Track C / H1_primary: NOT_SUPPORTED.** All claim-worthy local panels tested (FCLR-003/008/009/012-V/013/014); forecast gate NOT_MET everywhere; overlay INELIGIBLE. `next_unfinished_task (Track C): NONE`.
- **Track A (observed liquidations): STRUCTURALLY_BLOCKED.** No admissible unauthenticated observed-liquidation census locally; not locally repairable.
- **Track B (modeled boundary breaches): PARTIALLY TESTED — NOT_SUPPORTED on the single executed window (TRACKB-20251110T154307Z, 2025-01-01..2025-10-31, C2 vs B1 rel improvement 1.50% < 2% floor, CI [-0.005,0.035] crosses zero; modeled synthetic proxy only). UNTESTED admissible local windows with >=3 blocks remain — this session's work.**

## Next unfinished task (single, mandatory)
**`next_unfinished_task: Track B confirmatory on an untested local window — M5.1 admissibility lock → M5.2 frozen prereg BEFORE outcomes → M5.3 execute & evaluate → M5.4 verdict & propagation.`**

Preferred window: **TB1 panel 2025-01-01..2026-10-31** (5 symbols, provenance_verified=true, 2065 files verified, unmapped_count=0, 22 estimated non-overlapping 30-day blocks — fully verified locally, untested). Fallback: re-audit **2024-01-01..2024-09-30** (~9 estimated blocks, completeness 1.0) via deep admissibility + gap + funding-schema audit before confirmatory.

## Steps (execute in order; skipping is non-compliant)

### 1. Admissibility lock (M5.1)
- Select untested local window; require >=5 instruments, contiguous mark/index/premium/klines + funding, >=3 non-overlapping 30-day blocks in test, not sealed/previously outcome-inspected for this Track B design.
- Prove `provenance_verified=true`, `unmapped_count==0`; schema/coverage OK; no required gaps.
- Save `research_state/trackb_<ID>_admissibility.(json|md)`. `<ID>` = UTC start timestamp, e.g. `trackb_20261110T163000Z`.

### 2. Freeze prereg BEFORE outcomes (M5.2)
- Write `research_state/research_protocol_trackb_<ID>.md`: modeled breach definition (leverage/margin/horizon/side), predictors, 60/20/20 chronological + 7-day purge/embargo, metrics, 2% materiality floor, Holm, block bootstrap >=2000 reps, explicit "synthetic proxy ≠ observed liquidation".
- Compute `prereg_hash` = sha256 of frozen protocol content. Record `prereg_hash` and `split_boundaries_trackb_<ID>.frozen_before_outcomes=true` in `research_state/run_manifest.json` **before** any outcome computation.

### 3. Execute & evaluate (M5.3, heavy)
- Run Track B pipeline on the frozen panel; output `research_state/evaluation_summary_trackb_<ID>.md` with point estimate, 95% CI, relative change, n_instruments, n_obs, n_test_blocks, materiality/gate decision.

### 4. Verdict & propagation (M5.4)
- Update hypothesis registry, experiment frontier, negative-results report, AGENT_HANDOFF.md, NEXT_SESSION_TASK.md with timestamped outcomes and a single `next_unfinished_task`.
- Overlay NOT ELIGIBLE unless all gates pass. Record gate verdict explicitly.

## Acceptance (all required)
- Frozen prereg with hash recorded before outcomes; admissibility evidence saved; evaluation summary with CIs/blocks; gate verdict explicit; registries + AGENT_HANDOFF + NEXT_SESSION_TASK updated.

## Verification commands
- `python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_funding_schema_audit tests.test_trackc_provenance_lineage -v`
- Provenance: `python -c "from scripts.trackc_provenance_lineage import verify_paths_with_manifests; from pathlib import Path; res=verify_paths_with_manifests([str(p) for p in Path('research_state/data_cache').rglob('*-fundingRate-*.csv')], repo_root=Path('.')); assert res['provenance_verified'] and res['unmapped_count']==0; print('PROVENANCE_OK', res['files_considered'])"`

## Hard constraints (NON-NEGOTIABLE)
No network/paid/manual/credentialed data; no fabricated data/provenance; no threshold shopping; no sealed-holdout reuse; no Track A/B/C conflation; preregister before outcomes; no risk overlay until forecast gate passes; no `.github/workflows` edits. Modeled Track B outputs are synthetic proxies, never observed liquidations.
