# AGENT_HANDOFF.md — Single Durable Handoff (Liquidation Risk Priority)

**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Updated:** 2026-11-10T18:09:05Z (handoff refresh 2026-11-10T18:13:13Z; no new outcomes/run — state & mandatory task reconfirmed)
**Authoritative initial task:** see `NEXT_SESSION_TASK.md` top banner + `next_unfinished_task` below.
**Priority (repo name):** 1) Track B liquidation risk (modeled boundary breaches) — **ACTIVE**, 2) Track C funding-conditioned volatility — **concluded NOT_SUPPORTED on claim-worthy local panels**, 3) Track A observed liquidations — **STRUCTURALLY_BLOCKED**.

## Session preflight (verified)
- `PROVENANCE_OK 161` for funding CSV lineage in `research_state/data_cache` (2026-11-10T18:05Z, `provenance_verified=true`, `unmapped_count=0`).
- Canonical tests: **35 PASS** — `tests.test_volatility_features_splits`, `tests.test_synthetic_boundary_labels`, `tests.test_trackc_panel_admissibility_audit`, `tests.test_trackc_funding_schema_audit`, `tests.test_trackc_provenance_lineage` (2026-11-10T18:09Z).
- No network/paid/manual/credentialed data available or permitted for repair; no `.github/workflows` edits.

## Current state
- **Track B / TB1 (`TRACKB-MODELED-BREACH-TB1-20261110T173838Z`, 2025-01-01..2026-10-31, 5 symbols, ~22 est. 30d blocks):** admissibility locked and prereg frozen before outcomes, but confirmatory evaluation is **DEGENERATE/INADMISSIBLE for 5x/24h long label** — frozen test split 2026-06-26..2026-10-31 had **ZERO synthetic breaches** across all symbols. Gate NOT_MET; comparative metrics not interpretable. Evidence: `research_state/evaluation_summary_trackb_TB1_20261110T173838Z.md`, `research_state/research_protocol_trackb_TB1_20261110T173838Z.md`, `research_state/trackb_TB1_admissibility.json`, `run_manifest.json` `split_boundaries_trackb_TB1_20261110T173838Z`.
- **Track B / prior:** `TRACKB-20251110T154307Z` (2025-01-01..2025-10-31) NOT_MET/NOT_SUPPORTED (C2 vs B1 +1.50% < 2%, CI crosses zero; synthetic proxy only).
- **Track B / next local route (heavy):** 2024-01-01..2024-09-30 panel (BTC/ETH/BNB/SOL/XRP) deep-audited contiguous, required series complete, funding schema OK, `provenance_verified=true`, `unmapped_count=0`, ~9 non-overlapping 30d blocks. Evidence: `research_state/trackb_TB1_admissibility_2024q1q3.json`, `research_state/trackb_window_candidates_fast.json`. **Untested for confirmatory Track B with a new frozen design.**
- **Track C (H1 volatility):** concluded **NOT_SUPPORTED** on claim-worthy local panels (FCLR-003/008/009/013/014 etc.); no untested claim-worthy panels with >=3 blocks remain locally.
- **Track A (observed liquidations):** **STRUCTURALLY_BLOCKED** (no admissible unauthenticated observed-liquidation census). Not locally repairable.
- **Risk overlay:** **INELIGIBLE** until a forecast gate passes under frozen prereg.

## Bottlenecks removed this handoff refresh
- Replaced ambiguous dual-option next step with a **single mandatory TB2 execution task** on the 2024-01-01..2024-09-30 panel (fallback only if re-audit proves it inadmissible).
- Made TB1's degenerate-test-set failure explicit as a label/window admissibility failure (not a data gap), preventing repeated idle relitigation.
- Consolidated evidence pointers and verification commands into one durable handoff (`NEXT_SESSION_TASK.md` + this file).

## 🔴 INITIAL TASK FOR NEXT AGENTIC SESSION (2026-11-10T18:09:05Z)
**Campaign:** Track B TB2 confirmatory (modeled boundary breaches, synthetic proxy ≠ observed liquidations).

**Mandatory (heavy, verifiable):** Execute TB2 on **2024-01-01..2024-09-30** with a NEW label design chosen for **test-split event adequacy** (>0 breaches in frozen test). Steps (in order): (1) re-verify deep admissibility + provenance for all inputs used; save `research_state/trackb_<ID>_admissibility.(json|md)`; (2) compute candidate breach rates and select label/split with positive test events (documented, no post-freeze shopping); (3) write frozen prereg `research_state/research_protocol_trackb_<ID>.md` and record `prereg_hash` + `split_boundaries_trackb_<ID>.frozen_before_outcomes=true` in `run_manifest.json` **before confirmatory outcome computation**; (4) run confirmatory evaluation → `research_state/evaluation_summary_trackb_<ID>.md` with point estimates, 95% CI, relative change, n_instruments, n_obs, n_test_blocks, gate verdict; (5) update hypothesis/frontier/negative-results and handoff files with singular `next_unfinished_task`.

**Do not:** relitigate Track C/A, stop at planning/narration, reuse sealed holdouts, inspect outcomes before freeze, conflate synthetic proxy with observed liquidations, or fabricate provenance/data.

## `next_unfinished_task`
Track B TB2: re-verify admissibility/provenance for 2024-01-01..2024-09-30, select a NEW label+split with >0 frozen-test synthetic breaches, freeze NEW prereg+hash in manifest before outcomes, execute confirmatory evaluation, and propagate verdict/evidence to registries and handoff (fallback to next locally admissible uninspected route only if 2024Q1-Q3 is proven inadmissible). Track C concluded NOT_SUPPORTED. Track A STRUCTURALLY_BLOCKED. Risk overlay INELIGIBLE.

## Key evidence
- `NEXT_SESSION_TASK.md` (this handoff's operative task)
- `FOCUS_CAMPAIGN.md`
- `research_state/evaluation_summary_trackb_TB1_20261110T173838Z.md`
- `research_state/research_protocol_trackb_TB1_20261110T173838Z.md`
- `research_state/trackb_TB1_admissibility.json`, `research_state/trackb_TB1_admissibility_2024q1q3.json`, `research_state/trackb_window_candidates_fast.json`
- `research_state/run_manifest.json`
- `research_state/hypothesis_registry.json`, `research_state/experiment_frontier.json`, `research_state/negative_results_report.md`

## Hard constraints (NON-NEGOTIABLE)
No network/paid/manual/credentialed data; no fabricated data/provenance; no threshold shopping; no sealed-holdout reuse; no Track A/B/C conflation; preregister/freeze before outcomes; no risk overlay until forecast gate passes; no `.github/workflows` edits. Future agents must deliver heavy, verifiable progress.
