# FCLR Focus Campaign — `FCLR-FRONTIER-VERIFY-06-20261117T130551Z` — aligned 2026-11-17T16:15:09Z

**Frontier rank 0:** `FCLR-BOUNDED-TRIGGER-ONLY-20261115T220000Z` (`TRIGGER_ONLY` / `BOUNDED_TRIGGER_ONLY`, `all_terminal=true`, `next_action_heavy=null`).
**Sole durable handoff:** `AGENT_HANDOFF.md` (authoritative). This file is the detailed subordinate campaign note; if it conflicts with the handoff, the handoff wins.
**Governing rules:** `RESEARCH_PROMPT.md`. Never re-run concluded estimands, re-score sealed results, fabricate data, edit `.github/workflows/*`, poll, re-probe the HuggingFace tree, use paid/credentialed/manual outcome data, or run `git lfs pull`.
**Artifact rule:** write every new artifact to a new `research_state/session_<UTC>/`. The `research_state/` root is at **500/500** md/json; adding root files breaks the enforced churn cap.

## Current target (mandatory) — `FCLR-FRONTIER-VERIFY-06`

FCLR-014 and FCLR-REPRO-SYNTH-05 are **DONE / BLOCKED-ON-DESIGN** (`session_20261117T072040Z`). Do not repeat either.

Required NEW quantitative artifact in the next `research_state/session_<UTC>/`:

- `recompute_frontier_exhaustive_audit_<UTC>.{py,json,md}` — an independent, stdlib-only, ZIP/CSV-aware audit that:
  1. reconstructs complete mark+funding and full-C2 months directly from `research_state/data_cache/` for the five Binance symbols;
  2. rebuilds 30d-train + 7d-embargo + 30d-test candidate blocks;
  3. enumerates **all subsets** of individually feasible test months and computes the maximum mutually non-overlapping selection on `[train_start, test_end]`;
  4. reports all overlapping pairs, all maximal non-overlapping selections, contiguous untested runs, and span vs `MIN_DESIGN_DAYS=127`;
  5. compares exact values against `scripts/next_campaign_status.py --json` (`disjoint_block_frontier`, `markfund_frontier`) and `session_20261117T072040Z/recompute_design_frontier_certificate_20261117T072040Z.json`;
  6. includes a clearly labeled `EXPLORATORY_DESIGN_ONLY / NOT_A_PREREG / NOT_PROMOTABLE` sensitivity grid for 14/30-day block lengths with a 7-day embargo;
  7. does not inspect outcomes, does not import the canonical script for the computation, and does not modify sealed artifacts.

Expected closed-world result: full-C2 **0** disjoint feasible blocks / no ≥127d run; mark+funding-only **4** individually feasible months (`2024-10`, `2024-11`, `2024-12`, `2025-01`) but only **2** mutually non-overlapping (`2024-10`, `2025-01`), **5** overlapping pairs, `campaign_feasible_non_overlapping=false`; overall `BLOCKED_ON_DESIGN`, `promotable=false`, `fclr014_closed_verdict_reproduced=true`. If the independent audit disagrees, record `FRONTIER_VERIFICATION_MISMATCH`, do not edit sealed artifacts, and stop for adjudication.

## Completed work — do not repeat

- **FCLR-REPRO-SYNTH-05 — DONE (`session_20261117T072040Z`).** Design-frontier certificate and replication robustness complete; full-C2 0 blocks; mark+funding-only 4 individually / 2 mutually non-overlapping; qualitative corroboration 7/7 Wilson95 [0.646,1.000]; LOO 6/6 all-unity; sign mixed 3+/4-; `promotable=false`.
- **FCLR-014 — DONE / BLOCKED-ON-DESIGN (`session_20261117T071110Z`, reproduced `session_20261117T072040Z`).** The 4-block “freeze a prereg” claim is **RETRACTED** as leakage-prone. Cite `session_20261117T071110Z`.
- **Replication synthesis — DONE (`session_20261117T071110Z`).** 7/7 qualitative corroboration; 2/7 within tolerance; 0 promotable positives.
- FCLR-013 — `session_20261117T031656Z` (NOT_REPLICATED).
- FCLR-010 — `session_20261117T002014Z` (NOT_REPLICATED).
- FCLR-002/003 — `session_20261117T000400Z` (NOT_MET corroborated).
- FCLR-009 — `session_20261116T125624Z`; FCLR-006 — `session_20261116T185811Z`; FCLR-008 — `session_20261116T230140Z`; FCLR-RCA-011 — `session_20261116T100533Z`.

Incomplete / non-counting (do not resume/copy/count): `session_20261116T104644Z/`, `session_20261116T105341Z/`, `session_20261116T134957Z/` (trigger-only); `session_20261116T140001Z/` and `session_20261116T221127Z/` superseded; `session_20261117T060853Z/` PHANTOM (missing cited artifacts); `session_20261117T041333Z/` and `session_20261117T051045Z/` superseded by `session_20261117T071110Z`.

## Why this campaign exists (bottlenecks removed)

- **Stale handoff corrected:** the previous handoff claimed `scripts/next_campaign_status.py` had no mark+funding-only frontier. The canonical tool now exposes `markfund_frontier` and `tests/test_next_campaign_status.py` pins the closed verdict. The current campaign uses that as the comparison target, not as open work.
- **Empty-session loop removed:** an empty non-counting session directory was removed; no session dir should be created until a concrete heavy artifact is ready.
- **FCLR-014 design conflict resolved:** 041333Z (2 blocks) vs 051045Z (4 blocks) adjudicated to **BLOCKED-ON-DESIGN**; the 4-block feasibility claim is retracted. Do not re-litigate.
- **Parquet engine absent:** use ZIP/CSV twins; network installs prohibited.
- **Root churn:** 500/500 — session-only writes.
- **Handoff authority:** `AGENT_HANDOFF.md` only.

## Non-skippable execution contract

### Phase A — Check external triggers once

Read only `research_state/resume_trigger_registry.json` and `research_state/ironflow_monitor_state.json`. Record timestamp and verdict in the new session dir. No network/polling/HF re-probe. Current: all four OPEN; Ironflow `data_through=2026-10`, `consecutive_absent=3`; 2026-11/12/2027-01 `CONFIRMED_ABSENT`.

### Phase B — Emit the new quantitative artifact

No trigger fired → produce `recompute_frontier_exhaustive_audit_<UTC>.{py,json,md}` exactly as specified above. Do not re-run FCLR-014, the synthesis, or FCLR-REPRO-SYNTH-05. If a trigger fired → `RESEARCH_PROMPT.md` §16 admissibility/source audit, freeze a pre-sized prereg from `session_20261116T035833Z/prereg_template_trigger_gated_20261116T035833Z.json` per `session_20261116T100533Z/trigger_readiness_power_calibration_20261116T100533Z.md` (Gate4/TrackC `paired_n>=23224`, TrackA/expansion `paired_n>=11689`, ≥3 blocks, 7d purge/embargo, `outcome_data_inspected_before_freeze=false`), then execute and record an honest verdict.

### Phase C — Verify and hand off

1. Create `research_state/session_<UTC>/` (all new artifacts inside).
2. Audit carried-forward bundles: `session_20261116T100533Z/`, `session_20261116T125624Z/`, `session_20261116T185811Z/`, `session_20261116T230140Z/`, `session_20261117T000400Z/`, `session_20261117T002014Z/`, `session_20261117T031656Z/`, `session_20261117T071110Z/`, `session_20261117T072040Z/`.
3. Write concise `evidence_audit_<UTC>.md`.
4. Run and capture under the session dir: `check_handoff_heavywork_gate.py --json`, `check_tracka_scope_registry_drift.py --json`, targeted `python3 -m unittest tests.test_active_campaign_gate tests.test_next_campaign_status tests.test_tracka_hardening_117 tests.test_tracka_hardening_118 tests.test_tracka_hardening_143`, and `python3 -m unittest discover -q` to completion (record count/skip/error/EXIT). **Baseline is environment-dependent:** prior handoff recorded 1340 tests / 4 errors / 18 skipped / EXIT 1; current sandbox recorded 1119 tests / 62 errors / 9 failures / 14 skipped / EXIT 1 (mostly missing `numpy`/`pyarrow` and unresolved LFS fixtures). Record the actual run; never treat timeout/monitor cap or a missing-dependency error set as green. Revert timestamp-only tracked-file side effects.
5. Update only `AGENT_HANDOFF.md`; preserve sole-handoff contract and blockers.

Trigger checks, tests/gates, copied bundles, static re-audits, re-runs of FCLR-014 or the synthesis, “no trigger → stop cleanly”, and handoff-only refreshes are **not** completion.

## Verification record — 2026-11-17T16:15:09Z

- Handoff refreshed: `AGENT_HANDOFF.md` is the sole durable handoff; `FCLR-FRONTIER-VERIFY-06` remains the active mandatory heavy campaign.
- `check_handoff_heavywork_gate.py --json`: **PASS** (`reason_code: OK`, root 500/500, latest session `session_20261117T072040Z`).
- `check_tracka_scope_registry_drift.py --json`: **PASS** (196 scripts, no drift).
- Targeted guard tests: `tests.test_tracka_hardening_099 tests.test_tracka_hardening_143 tests.test_active_campaign_gate` — 32 tests, OK, EXIT 0 (before the new frontier-gate tests); `tests.test_tracka_hardening_143` alone after hardening — 17 tests, OK, EXIT 0.
- Gate hardening: `scripts/check_handoff_heavywork_gate.py` now fails closed for post-start sessions lacking the exact `recompute_frontier_exhaustive_audit_<UTC>.{py,json,md}` triad or a trigger check. Current pre-start session remains green.
- Full `python3 -m unittest discover -q` was not rerun for this documentation-only refresh; the recorded sandbox baseline remains **1119 tests, 62 errors, 9 failures, 14 skipped, EXIT 1** (mostly missing `numpy`/`pyarrow` and unresolved LFS fixtures; no failure attributable to these documentation edits). The prior 1340/4/18 baseline is not reproducible in this sandbox.
- No new session artifact produced in this refresh; the next session must satisfy `FCLR-FRONTIER-VERIFY-06`.