# FCLR Focus Campaign — `FCLR-REPRO-SYNTH-05` — aligned 2026-11-17T07:11:10Z

**Frontier rank 0:** `FCLR-BOUNDED-TRIGGER-ONLY-20261115T220000Z` (`TRIGGER_ONLY` / `BOUNDED_TRIGGER_ONLY`, `all_terminal=true`, `next_action_heavy=null`).
**Sole durable handoff:** `AGENT_HANDOFF.md` (authoritative). This file is the detailed campaign note referenced by the frontier and the handoff.
**Governing rules:** `RESEARCH_PROMPT.md`. Never re-run concluded estimands, re-score sealed results, fabricate data, edit `.github/workflows/*`, poll, re-probe the HuggingFace tree, use paid/credentialed/manual outcome data, or run `git lfs pull`.
**Artifact rule:** write every new artifact to a new `research_state/session_<UTC>/`. The `research_state/` root is at **500/500** md/json; adding root files breaks the enforced churn cap.

## Current target (mandatory) — `FCLR-REPRO-SYNTH-05`

FCLR-014 is **DONE / BLOCKED-ON-DESIGN** (adjudicated in `session_20261117T071110Z`) and the replication synthesis is **DONE** (`session_20261117T071110Z`). Do not repeat either.

Required NEW quantitative artifacts in the next `research_state/session_<UTC>/`:
1. `recompute_design_frontier_certificate_<UTC>.{py,json,md}` — implement a **mark+funding-only non-overlapping block frontier** (30d train + 7d embargo + 30d test per block; blocks mutually non-overlapping in `[train_start, test_end]`) and emit a per-estimand certificate (full-C2 and mark+funding-only): feasible-block count *with and without* the non-overlap constraint, contiguous-run feasibility vs `MIN_DESIGN_DAYS=127`, `promotable=false`. Must reproduce: full-C2 = 0 blocks; mark+funding-only = 4 individually-feasible but **2 mutually non-overlapping** (<3) → `BLOCKED_ON_DESIGN`.
2. `replication_robustness_<UTC>.{json,md}` — leave-one-out qualitative-corroboration rate + Wilson CI, sign-consistency of the C2-vs-B1 effects, explicit estimand-heterogeneity caveat (QLIKE vs Brier), and a **boundary certificate** (the exact minimal change that would flip the programme to a promotable positive result). Build on `session_20261117T071110Z/replication_synthesis_20261117T071110Z.json`; do not re-run it.
3. (Recommended) Harden `scripts/next_campaign_status.py` with the mark+funding-only non-overlapping frontier (new `--json` key `markfund_frontier`) + unit tests; **register any new `scripts/*.py` in both scope registries**. Do not weaken the completeness rule.
4. `evidence_audit_<UTC>.md` + trigger-check record + gate/suite captures.

## Completed work — do not repeat

- **FCLR-014 — DONE / BLOCKED-ON-DESIGN (`session_20261117T071110Z`).** Canonical full-C2 = 0 feasible blocks / no ≥127d run; mark+funding-only = 4 individually-feasible (2024-10/11/12, 2025-01) but **2 mutually non-overlapping** (2024-10, 2025-01) < 3. The "freeze a new mark+funding-only prereg (2024-10/11/12)" claim (`session_20261117T051045Z`, corrected `session_20261117T041333Z`) is **RETRACTED** as leakage-prone (overlapping train/test windows). `permits_new_prereg=false`.
- **Replication synthesis — DONE (`session_20261117T071110Z`).** 7 studies; qualitative corroboration 7/7 (Wilson95 0.646–1.000); within-tolerance 2/7 (FCLR-006, FCLR-009); FCLR-002/003/008 diverge on exact values but agree on qualitative NOT_MET; FCLR-010/013 NOT_REPLICATED; **promotable positive results NONE**.
- **FCLR-013 — DONE (`session_20261117T031656Z`).** ZIP/CSV parquet-free recompute; NOT_REPLICATED (C2-vs-B1 rel -4.99%, CI crosses zero, 1 test block).
- **FCLR-010 — DONE (`session_20261117T002014Z`).** CSV/JSON parquet-free recompute; NOT_REPLICATED (0.50% vs sealed 2.21%).
- FCLR-002/003 — `session_20261117T000400Z` (diverged beyond tolerance; NOT_MET corroborated).
- FCLR-009 — `session_20261116T125624Z` (`all_within_tolerance=true`).
- FCLR-006 — `session_20261116T185811Z` (`all_within_tolerance=true`; supersedes `session_20261116T140001Z`).
- FCLR-008 — `session_20261116T230140Z` (B0/B1 within tolerance; C1/C2 divergence documented; NOT_MET corroborated). `session_20261116T221127Z` superseded.
- FCLR-RCA-011 — complete bundle `session_20261116T100533Z/`.

Incomplete / non-counting (do not resume/copy/count): `session_20261116T104644Z/`, `session_20261116T105341Z/`, `session_20261116T134957Z/` (trigger-only); `session_20261116T140001Z/` superseded; `session_20261116T221127Z/` superseded; **`session_20261117T050235Z/`, `session_20261117T060341Z/` EMPTY (0 files)**; **`session_20261117T060853Z/` PHANTOM (cites coverage/blocker artifacts that were never written)**; `session_20261117T041333Z/` and `session_20261117T051045Z/` superseded by the adjudication in `session_20261117T071110Z`.

## Why this campaign exists (bottlenecks removed)

- **FCLR-014 design conflict RESOLVED:** 041333Z (2 blocks) vs 051045Z (4 blocks) adjudicated against the canonical tool + explicit non-overlap constraint. Definitive **BLOCKED-ON-DESIGN**; the 4-block feasibility claim is retracted (train/test overlap → cross-block leakage). Cite `session_20261117T071110Z`.
- **Stale handoff corrected:** the 06:18:09Z handoff ignored five newer sessions; this campaign records them.
- **Empty/phantom sessions quarantined:** `050235Z`, `060341Z` (empty) and `060853Z` (phantom refs) are non-counting.
- **`next_campaign_status.py` enumeration gap (open — this campaign's hardening target):** `ready_windows()` only evaluates the full-C2 completeness rule and never computes the mark+funding-only non-overlapping frontier, so sessions improvised and disagreed. Close it by adding the frontier + tests (register any `scripts/*.py`). Do NOT weaken the completeness rule to fabricate feasibility.
- **Parquet engine absent:** no `pyarrow`/`fastparquet`/`duckdb`/`polars`; network installs prohibited. Use ZIP/CSV reader patterns from `session_20261117T031656Z`/`session_20261117T000400Z`.
- **Unresolved LFS / missing protocols:** `run_manifest.json`, `run_manifest_FCLR002.json`, `data_cache/fclr002_panel*.json`, `data_cache/manifest_fclr002.json`, `data_cache/manifest_fclr003.json` are pointers with no local object (no `git lfs pull`); `research_protocol_fclr002.md`/`fclr003.md` do not exist.
- **2024 format:** Apr–Jun 2024 mark/premium/index are ZIPs; Jan–Mar/Jul–Nov CSVs; 2025–2026 ZIP+CSV — ZIP-aware readers required.
- **Root churn:** 500/500 — session-only writes.
- **Handoff authority:** `AGENT_HANDOFF.md` only.

## Non-skippable execution contract

### Phase A — Check external triggers once
Read only `research_state/resume_trigger_registry.json` and `research_state/ironflow_monitor_state.json`. Record timestamp and verdict in the new session dir. No network/polling/HF re-probe. Current: all four OPEN; Ironflow `data_through=2026-10`, `consecutive_absent=3`; 2026-11/12/2027-01 `CONFIRMED_ABSENT`.

### Phase B — Emit new quantitative artifacts (heavy work)
No trigger fired → produce `recompute_design_frontier_certificate_<UTC>.{py,json,md}` and `replication_robustness_<UTC>.{json,md}` per "Current target". Do not read `run_manifest.json`, do not use parquet, do not re-score sealed summaries, do not re-run FCLR-014 or the synthesis. If a trigger fired → `RESEARCH_PROMPT.md` §16 admissibility/source audit, freeze a pre-sized prereg from `session_20261116T035833Z/prereg_template_trigger_gated_20261116T035833Z.json` per `session_20261116T100533Z/trigger_readiness_power_calibration_20261116T100533Z.md` (Gate4/TrackC `paired_n>=23224`, TrackA/expansion `paired_n>=11689`, ≥3 blocks, 7d purge/embargo, `outcome_data_inspected_before_freeze=false`), then execute and record an honest verdict.

### Phase C — Verify and hand off
1. Create `research_state/session_<UTC>/` (all new artifacts inside).
2. Audit carried-forward bundles: `session_20261116T100533Z/`, `session_20261116T125624Z/`, `session_20261116T185811Z/`, `session_20261116T230140Z/`, `session_20261117T000400Z/`, `session_20261117T002014Z/`, `session_20261117T031656Z/`, `session_20261117T071110Z/`.
3. Write concise `evidence_audit_<UTC>.md`.
4. Run and capture under session dir: `check_handoff_heavywork_gate.py --json`, `check_tracka_scope_registry_drift.py --json`, targeted unittests, and `python3 -m unittest discover -q` to completion (record count/skip/error/EXIT). Baseline: **1340 tests, 4 pre-existing pyarrow errors (`tests.test_fclr_liq_combined_admissibility_audit`), 18 skipped, EXIT 1**; success = same set, no new failures/errors. Never treat timeout/monitor cap as green. Revert timestamp-only tracked-file side effects.
5. Update only `AGENT_HANDOFF.md`; preserve sole-handoff contract and blockers.

Trigger checks, tests/gates, copied bundles, static re-audits, re-runs of FCLR-014 or the synthesis, "no trigger → stop cleanly", or handoff-only refreshes are **not** completion.

## Design-power summary
- Only FCLR-009 (n=24,495, 6 blocks, MDE 1.95%) was powered for the 2% floor.
- Per-trigger floors: Gate4/TrackC `paired_n>=23224`; TrackA/expansion `paired_n>=11689`; all with ≥3 blocks and 7d purge/embargo.

## Verification record — 2026-11-17T07:11:10Z (campaign rebuild)
- Removed bottleneck: FCLR-014 conflict adjudicated to **BLOCKED-ON-DESIGN** (`session_20261117T071110Z`); the 4-block "freeze a prereg" claim retracted. Quarantined empty sessions (`050235Z`, `060341Z`) and phantom session (`060853Z`). Corrected the stale latest-session pointer.
- Aligned this note to `AGENT_HANDOFF.md`: FCLR-014 DONE; replication synthesis DONE; new target `FCLR-REPRO-SYNTH-05` (design-frontier certificate + replication robustness + optional tool hardening).
- `check_handoff_heavywork_gate.py --json`: **PASS** (root 500/500, `reason_code: OK`). `check_tracka_scope_registry_drift.py --json`: **PASS** (196 scripts, no drift). Targeted 52 OK; full suite 1340 tests / 4 pre-existing pyarrow errors / 18 skipped / EXIT 1 (baseline).
- Heavy artifacts this session: `recompute_fclr014_design_admissibility_20261117T071110Z.{py,json,md}` + `replication_synthesis_20261117T071110Z.{json,md}` + `recompute_replication_synthesis_20261117T071110Z.py` + `trigger_check` + `evidence_audit` under `session_20261117T071110Z/`.