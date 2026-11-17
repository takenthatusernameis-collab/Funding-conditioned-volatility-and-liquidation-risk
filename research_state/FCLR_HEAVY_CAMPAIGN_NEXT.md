# FCLR Focus Campaign — `FCLR-REPRO-AUDIT-04` — aligned 2026-11-17T04:09:17Z

**Frontier rank 0:** `FCLR-BOUNDED-TRIGGER-ONLY-20261115T220000Z` (`TRIGGER_ONLY` / `BOUNDED_TRIGGER_ONLY`, `all_terminal=true`, `next_action_heavy=null`).
**Sole durable handoff:** `AGENT_HANDOFF.md` (authoritative). This file is the detailed campaign note referenced by the frontier and the handoff.
**Governing rules:** `RESEARCH_PROMPT.md`. Never re-run concluded estimands, re-score sealed results, fabricate data, edit `.github/workflows/*`, poll, re-probe the HuggingFace tree, use paid/credentialed/manual outcome data, or run `git lfs pull`.
**Artifact rule:** write every new artifact to a new `research_state/session_<UTC>/`. The `research_state/` root is at **500/500** md/json; adding root files breaks the enforced churn cap.

## Current target (mandatory)

**Primary heavy artifact: FCLR-014 panel coverage audit + blocker resolution.** FCLR-013 and FCLR-010 are **DONE** and must not be repeated.

Required quantitative artifacts in the next `research_state/session_<UTC>/`:
1. `fclr014_panel_coverage_audit_<UTC>.{json,md}` — per-symbol × per-month coverage matrix over `research_state/data_cache/` for BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT (mark/index/premium day counts, funding presence, `admissible_for_fclr014` boolean: mark+funding complete for all 5).
2. `fclr014_panel_blocker_resolution_<UTC>.{json,md}` — corrected blocker: prereg `pre_registration_fclr014_confirmatory_funding_vol_20261109T181124Z.json` is frozen `NO_GO` with FCLR-002-copied 70-day/2-block splits; cache holds complete 5-symbol mark+funding for 2024-04..2024-11 and mark+index+premium+funding for 2025-01..2026-10, but a contiguous 3-block confirmatory design requires an untested run >= `MIN_DESIGN_DAYS` (127d) avoiding every `TESTED_WINDOWS` region in `scripts/next_campaign_status.py`. Enumerate candidate windows as `AVAILABLE` / `CONSUMED_BY_SEALED_CELL` / `INCOMPLETE_TRAIN` and state whether a **new pre-registered design** (not a re-score) can be frozen before outcomes. If a valid untested contiguous run >=127d exists, freeze a NEW prereg (copy `session_20261116T035833Z/prereg_template_trigger_gated_20261116T035833Z.json`, set `outcome_data_inspected_before_freeze=false`) and **STOP before outcomes**.
3. `evidence_audit_<UTC>.md` + trigger-check record + gate/suite captures.

**Do not attempt an FCLR-014 confirmatory recompute or re-score.** Document the corrected design-admissibility blocker (not a false "no data" claim).

## Completed work — do not repeat

- **FCLR-013 — DONE (`session_20261117T031656Z`).** ZIP/CSV parquet-free recompute. Verdict **NOT_REPLICATED**: C2-vs-B1 QLIKE mean diff 0.017010 (CI `[-0.000523,0.034809]`, crosses zero), rel **-4.99%** vs sealed **-1.32%** (NOT_MET); 1 test block; materiality <2%; LOIO/placebo fail; n_pairs=4200, 5 symbols, 36 test days.
- **FCLR-010 — DONE (`session_20261117T002014Z`).** CSV/JSON parquet-free recompute. Verdict **NOT_REPLICATED**: Brier rel reduction 0.50% vs sealed 2.21%; LOIO/placebo fail.
- FCLR-002 — `session_20261117T000400Z` (exact values diverged; C2-vs-B1 directionally positive; gate NOT_MET).
- FCLR-003 — `session_20261117T000400Z` (B0/B1 match; C1/C2 diverge; NOT_MET corroborated).
- FCLR-009 — `session_20261116T125624Z` (`all_within_tolerance=true`).
- FCLR-006 — `session_20261116T185811Z` (`all_within_tolerance=true`; supersedes `session_20261116T140001Z`).
- FCLR-008 — `session_20261116T230140Z` (B0/B1 within tolerance; C1/C2 divergence documented; NOT_MET corroborated). `session_20261116T221127Z` superseded (do not count/resume).
- FCLR-RCA-011 — complete bundle `session_20261116T100533Z/`.

Incomplete trigger-only/non-counting sessions (do not resume/copy/count): `session_20261116T104644Z/`, `session_20261116T105341Z/`, `session_20261116T134957Z/`.

## Why this campaign exists (bottlenecks removed)

- **FCLR-014 "blocked-on-data" misclassification corrected:** cache has complete 5-symbol mark+funding for 2024-04..2026-10 and full mark+index+premium+funding for 2025-01..2026-10; blocker is design admissibility under `TESTED_WINDOWS`, not data absence.
- **`next_campaign_status.py` enumeration gap (documented):** drops 2024-11/12 because 4/5 symbols miss index/premium for the completeness threshold; do not weaken the rule to fabricate feasibility. Any `scripts/*.py` patch must be registered in both scope registries.
- **Parquet engine absent:** no `pyarrow`/`fastparquet`/`duckdb`/`polars`; network installs prohibited. Never run `scripts/fclr_liq_010_confirm.py`. Use ZIP/CSV reader patterns from `session_20261117T031656Z`/`session_20261117T000400Z`.
- **Unresolved LFS / missing protocols:** `run_manifest.json`, `run_manifest_FCLR002.json`, `data_cache/fclr002_panel*.json`, `data_cache/manifest_fclr002.json`, `data_cache/manifest_fclr003.json` are pointers with no local object (no `git lfs pull`); `research_protocol_fclr002.md`/`fclr003.md` do not exist.
- **2024 format:** Apr–Jun 2024 mark/premium/index are ZIPs; Jan–Mar/Jul–Nov CSVs; 2025–2026 ZIP+CSV — ZIP-aware readers required.
- **Root churn:** 500/500 — session-only writes.
- **Handoff authority:** `AGENT_HANDOFF.md` only. Tombstones: `NEXT_SESSION_HANDOFF.md`, `NEXT_SESSION_TASK.md`, `AGENT_HANDOFF_20261115T073240Z.md`, `HANDOFF_NEXT_SESSION_20261116T114626Z.md`, `HANDOFF_NEXT_SESSION_20261117T033007Z.md`.

## Non-skippable execution contract

### Phase A — Check external triggers once
Read only `research_state/resume_trigger_registry.json` and `research_state/ironflow_monitor_state.json`. Record timestamp and verdict in the new session dir. No network/polling/HF re-probe. Current: all four OPEN; Ironflow `data_through=2026-10`, `consecutive_absent=3`; 2026-11/12/2027-01 `CONFIRMED_ABSENT`.

### Phase B — Emit new quantitative artifacts (heavy work)
No trigger fired → produce `fclr014_panel_coverage_audit_<UTC>.{json,md}` and `fclr014_panel_blocker_resolution_<UTC>.{json,md}` per "Current target" above. Do not read `run_manifest.json`, do not use parquet, do not re-score sealed summaries. If a valid untested contiguous >=127d window is found, freeze a NEW prereg and stop before outcomes. Trigger fired → `RESEARCH_PROMPT.md` §16 admissibility/source audit, freeze pre-sized prereg from `session_20261116T035833Z/prereg_template_trigger_gated_20261116T035833Z.json` per `session_20261116T100533Z/trigger_readiness_power_calibration_20261116T100533Z.md` (Gate4/TrackC `paired_n>=23224`, TrackA/expansion `paired_n>=11689`, >=3 blocks, 7d purge/embargo, `outcome_data_inspected_before_freeze=false`), then execute and record honest verdict.

### Phase C — Verify and hand off
1. Create `research_state/session_<UTC>/` (all new artifacts inside).
2. Audit carried-forward bundles: `session_20261116T100533Z/`, `session_20261116T125624Z/`, `session_20261116T185811Z/`, `session_20261116T230140Z/`, `session_20261117T000400Z/`, `session_20261117T002014Z/`, `session_20261117T031656Z/`.
3. Write concise `evidence_audit_<UTC>.md`.
4. Run and capture under session dir: `check_handoff_heavywork_gate.py --json`, `check_tracka_scope_registry_drift.py --json`, targeted unittests, and `python3 -m unittest discover -q` to completion (record count/skip/error/EXIT). Baseline: ~1340 tests, 4 pre-existing pyarrow errors (`tests.test_fclr_liq_combined_admissibility_audit`), ~18 skipped, EXIT 1; success = same set, no new failures/errors. Never treat timeout/monitor cap as green. Revert timestamp-only tracked-file side effects.
5. Update only `AGENT_HANDOFF.md`; preserve sole-handoff contract and blockers.

Trigger checks, tests/gates, copied bundles, static re-audits, "no trigger → stop cleanly", or handoff-only refreshes are **not** completion.

## Design-power summary
- Only FCLR-009 (n=24,495, 6 blocks, MDE 1.95%) was powered for the 2% floor.
- Per-trigger floors: Gate4/TrackC `paired_n>=23224`; TrackA/expansion `paired_n>=11689`; all with >=3 blocks and 7d purge/embargo.

## Verification record — 2026-11-17T04:09:17Z (alignment maintenance)
- Removed bottleneck: tombstoned `HANDOFF_NEXT_SESSION_20261117T033007Z.md` and aligned this campaign note to `AGENT_HANDOFF.md` (FCLR-013 DONE; FCLR-014 = coverage audit + blocker resolution, not confirmatory recompute).
- `check_handoff_heavywork_gate.py --json`: **PASS** (`root_count` 500/500, `reason_code: OK`, latest `session_20261117T031656Z` has `recompute_fclr013_*` + audit).
- No heavy quantitative artifact produced this maintenance turn; next session must produce the FCLR-014 artifacts above.