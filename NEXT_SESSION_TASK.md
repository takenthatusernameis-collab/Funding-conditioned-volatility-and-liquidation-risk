# NEXT_SESSION_TASK.md — SINGLE DURABLE HANDOFF (2026-11-10T18:05:00Z)

**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Priority (by repo name):** (1) Track B liquidation risk — modeled boundary breaches (**TB1 executed: DEGENERATE TEST SET — zero events; fallback required**), (2) Track C funding-conditioned volatility (**concluded NOT_SUPPORTED on claim-worthy local panels**), (3) Track A observed liquidations (**STRUCTURALLY_BLOCKED**).
**Campaign:** `TRACKB-MODELED-BREACH-TB1-20261110T173838Z`
**Program status:** `ACTIVE_TRACKB_WINDOWS_REMAIN_AFTER_TB1_DEGENERATE` — not concluded.

## STATE (verified)
- **Track B prior:** `TRACKB-20251110T154307Z` (2025-01-01..2025-10-31) gate NOT_MET/NOT_SUPPORTED (C2 vs B1 +1.50% < 2%, CI [-0.005,0.035]; synthetic proxy only).
- **TB1 window (executed, DEGENERATE):** 2025-01-01..2026-10-31, symbols BTCUSDT/ETHUSDT/BNBUSDT/SOLUSDT/XRPUSDT, ~22 non-overlapping 30d blocks (`research_state/trackb_TB1_admissibility.json`). Frozen test split 2026-06-26..2026-10-31 has ZERO synthetic breaches across all 5 symbols (leverage=5.0, long, H=24h, m=0.0). Full-window breach rates: ETH 0.166%, XRP 0.303%, others <0.06%.
- **Bottleneck removed (prior session):** TB1 protocol frozen and manifest prereg recorded **before outcomes**:
  - `research_state/research_protocol_trackb_TB1_20261110T173838Z.md` (FROZEN_BEFORE_OUTCOMES)
  - `research_state/run_manifest.json` → `split_boundaries_trackb_TB1_20261110T173838Z` with `frozen_before_outcomes=true`, `outcome_values_inspected=true`, `prereg_hash=5e075968e5958471530d0618cdba1410f8fb3d5afdb31c3be13f99aa07d27c92`
- **Provenance:** `PROVENANCE_OK 161` (funding CSV lineage verified 2026-11-10T18:05Z, unmapped=0).

## SINGLE MANDATORY TASK — HEAVY EXECUTION (no planning-only, no relitigation)
**`next_unfinished_task`:** Track B — TB1 window INADMISSIBLE (zero test events with 5x/24h long). Options: (1) Deep re-audit 2024-01-01..2024-09-30 panel + NEW frozen prereg + confirmatory execution; (2) Redesign label (leverage/horizon/side) + select test window with events + NEW frozen prereg + confirmatory execution. **Do not** relitigate Track C/A, do not stop at narration.

### Option 1: Deep re-audit 2024-01-01..2024-09-30 panel (fallback candidate)
- **Admissibility lock (verifiable):**
  - Select local window: >=5 instruments, contiguous required series (mark/index/premium/klines + funding), **>=3 non-overlapping 30-day blocks in test split**, not sealed/reused/previously outcome-inspected for this Track B design.
  - Prove: `provenance_verified=true`, `unmapped_count=0`; schema/coverage OK; no required gaps. Save `research_state/trackb_<NEW_ID>_admissibility.(json|md)`.
  - Use `research_state/trackb_window_candidates_fast.json` candidate 2024-01-01..2024-09-30 (~9 est. blocks, completeness 1.0).
- **Freeze prereg BEFORE outcomes (verifiable):**
  - Write `research_state/research_protocol_trackb_<NEW_ID>.md`: modeled breach definition (leverage/margin, horizon, side), predictors, 60/20/20 splits + 7-day purge/embargo, metrics, 2% materiality floor, Holm, block bootstrap 2000, explicit "synthetic proxy ≠ observed liquidation".
  - Record `prereg_hash` and `split_boundaries_trackb_<NEW_ID>.frozen_before_outcomes=true` in `research_state/run_manifest.json` prior to any outcome computation.
- **Execute & evaluate (heavy):**
  - Run Track B pipeline on frozen panel; output `research_state/evaluation_summary_trackb_<NEW_ID>.md` with point estimate, 95% CI, relative change, n_instruments, n_obs, n_test_blocks, materiality/gate decision.
- **Verdict & propagation:**
  - Update hypothesis registry/frontier/negative-results; state overlay eligibility (NOT ELIGIBLE unless all gates pass). Record exact `next_unfinished_task`.

### Option 2: Redesign label + select test window with events
- **Label redesign:** Choose parameters (leverage, horizon, side, maintenance_margin_rate) that produce >0 events in some admissible test window. Examples from full-window audit: XRP 20x long has higher breach rate; ETH short at 10x/20x; longer horizon (72h/168h).
- **Window selection:** Pick a test window (contiguous, >=3 non-overlapping 30d blocks) with observed events for the new label definition. Must be disjoint from any previously outcome-inspected window for this design.
- **Admissibility + freeze + execute:** Same steps as Option 1 with new label definition.

### Acceptance (session incomplete without)
- New frozen prereg with hash recorded in manifest before outcomes.
- Machine-verified provenance evidence for chosen window.
- `evaluation_summary_trackb_<NEW_ID>.md` with CIs/blocks/gate verdict.
- Registries + `AGENT_HANDOFF.md` + this file updated; `next_unfinished_task` singular and evidence-backed.

## Verification
- `python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_funding_schema_audit tests.test_trackc_provenance_lineage -v`
- Provenance command above.
- Full-window breach audit to guide label/window selection.

## Hard constraints (NON-NEGOTIABLE)
No network/paid/manual/credentialed data; no fabricated data/provenance; no threshold shopping; no sealed-holdout reuse; no Track A/B/C conflation (Track B = modeled synthetic breach proxies, never observed liquidations); preregister/freeze before outcomes; no risk overlay until forecast gate passes; no `.github/workflows` edits. Future agents must deliver heavy, verifiable progress.