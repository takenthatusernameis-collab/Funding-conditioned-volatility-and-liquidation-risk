# FCLR Evidence Audit — 2026-11-17T07:11:10Z

Session: `research_state/session_20261117T071110Z/`
Generated: 2026-11-17T07:11:10Z
Campaign: `FCLR-REPRO-SYNTH-05` (successor to `FCLR-REPRO-AUDIT-04`)

## 1. Trigger check (Phase A)

- Sources: `research_state/resume_trigger_registry.json` + `research_state/ironflow_monitor_state.json` (read only; no network, no polling, no HF re-probe).
- All four reopen triggers **OPEN**: `GATE4_BRANCH_1`, `NEW_OBSERVED_LIQUIDATION_SOURCE`, `HL_LABEL_EXTENSION`, `EXPANSION_ROBUSTNESS_REDO`.
- Ironflow: `data_through=2026-10`, `consecutive_absent=3`; 2026-11/2026-12/2027-01 `CONFIRMED_ABSENT`.
- No trigger fired → no confirmatory estimand advanced or re-scored.
- Artifact: `trigger_check_20261117T071110Z.json`.

## 2. New quantitative artifacts (Phase B — heavy work)

### 2a. FCLR-014 design-admissibility adjudication (bottleneck resolution)
- Artifacts: `recompute_fclr014_design_admissibility_20261117T071110Z.{py,json,md}`.
- Method: stdlib-only, deterministic; invokes `scripts/next_campaign_status.py --json` for the canonical full-C2 verdict and independently recomputes the mark+funding-only block frontier with an explicit **mutual non-overlap** constraint (30d train + 7d embargo + 30d test per block; blocks must not overlap in `[train_start, test_end]`).
- Result:
  - Canonical full-C2 (mark+index+premium+funding): **0 feasible disjoint blocks; no contiguous untested run ≥127d** (`design_feasibility.any_feasible=false`, `disjoint_block_frontier.campaign_feasible=false`).
  - Mark+funding-only (B0/B1/C1): **4 individually feasible months** (2024-10, 2024-11, 2024-12, 2025-01) but **only 2 mutually non-overlapping** (2024-10, 2025-01) < 3 required. All 5 pairwise windows overlap (cross-block leakage).
  - **Verdict: `BLOCKED_ON_DESIGN`, `permits_new_prereg=false`.**
- Conflict resolution: the "FEASIBLE / freeze a new mark+funding-only prereg (2024-10/11/12)" claim in `session_20261117T051045Z` and the corrected `session_20261117T041333Z` JSON is **RETRACTED** — it counts individually-feasible months whose train windows overlap a neighbouring block's test month (leakage), which a confirmatory ≥3-block design forbids. The original 2-block reading (041333Z markdown) is the correct one.

### 2b. Replication meta-synthesis (new programme-level artifact)
- Artifacts: `recompute_replication_synthesis_20261117T071110Z.py`, `replication_synthesis_20261117T071110Z.{json,md}`.
- Scope: all 7 completed independent recomputes (FCLR-002/003/006/008/009/010/013).
- Result: **qualitative corroboration 7/7** (Wilson95 0.646–1.000); **within-tolerance reproduction 2/7** (FCLR-006, FCLR-009; Wilson95 0.082–0.641); FCLR-002/003/008 diverge on exact values but agree on the qualitative NOT_MET direction; FCLR-010/013 fresh NOT_REPLICATED. **Promotable positive results (materiality≥2% AND blocks≥3): NONE.** Programme remains `CLOSED_TERMINAL` / `NO_CLAIM_WORTHY_RESULT_PROMOTABLE`.

## 3. Carried-forward bundle audit (Phase C)

| Session | Experiment | Status |
|---------|------------|--------|
| `session_20261116T100533Z/` | FCLR-RCA-011 (5 families) | Complete bundle present |
| `session_20261116T125624Z/` | FCLR-009 | `all_within_tolerance=true` |
| `session_20261116T185811Z/` | FCLR-006 | `all_within_tolerance=true` |
| `session_20261116T230140Z/` | FCLR-008 | B0/B1 within tolerance; C1/C2 divergence documented; NOT_MET corroborated |
| `session_20261117T000400Z/` | FCLR-002/003 | exact values diverged beyond tolerance; NOT_MET corroborated |
| `session_20261117T002014Z/` | FCLR-010 | parquet-free CSV/JSON recompute; NOT_REPLICATED |
| `session_20261117T031656Z/` | FCLR-013 | ZIP/CSV parquet-free recompute; NOT_REPLICATED |

No recompute was re-run for any carried-forward session. No sealed artifact was mutated.

## 4. Bottlenecks removed / prevented this session

- **FCLR-014 conflict adjudicated:** two contradictory resolutions (041333Z 2-block vs 051045Z 4-block) reconciled against the canonical tool. Definitive verdict: **BLOCKED-ON-DESIGN**; the 4-block feasibility claim is retracted as leakage-prone.
- **Stale handoff corrected:** the previous handoff (06:18:09Z) referenced `session_20261117T031656Z` as latest but five newer sessions existed and were unrecorded; this handoff records them and points the next session at a live frontier.
- **Empty sessions quarantined:** `session_20261117T050235Z` and `session_20261117T060341Z` are empty (0 files) → non-counting, do not resume/copy/count.
- **Phantom-artifact session flagged:** `session_20261117T060853Z` cites `fclr014_panel_coverage_audit_20261117T060853Z.{json,md}` and `fclr014_panel_blocker_resolution_20261117T060853Z.{json,md}` that were never written (only `evidence_audit` + `trigger_check` exist) → non-counting.
- **Root churn cap:** `research_state/` root at 500/500 md+json; all new artifacts written under `session_20261117T071110Z/` only.
- **Parquet engine absent (unchanged):** no `pyarrow`/`fastparquet`/`duckdb`/`polars`; network installs prohibited. This session's artifacts are stdlib-only (no parquet).
- **Missing protocols / LFS pointers (unchanged):** `research_protocol_fclr002.md`/`fclr003.md` absent; `run_manifest*.json`, `fclr002_panel*.json`, `manifest_fclr002/003.json` are unresolved LFS pointers; not accessed; no `git lfs pull`.

## 5. Verification

- `python3 scripts/check_handoff_heavywork_gate.py --json` → **PASS** (see `heavywork_gate.json`).
- `python3 scripts/check_tracka_scope_registry_drift.py --json` → **PASS** (see `scope_drift.json`).
- Targeted: `python3 -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_117 tests.test_tracka_hardening_118 tests.test_tracka_hardening_143` → **52 tests OK**.
- Full: `python3 -m unittest discover -q` → **Ran 1340 tests, FAILED (errors=4, skipped=18), EXIT 1** — identical to baseline (4 pre-existing `tests.test_fclr_liq_combined_admissibility_audit` errors from missing `pyarrow`; environmental, not agent-caused). See `unittest_discover.txt` / `unittest_exit.txt`.

## 6. Next steps

- Execute the `INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION` in `AGENT_HANDOFF.md` (campaign `FCLR-REPRO-SYNTH-05`).
- Do NOT re-run FCLR-014 or the replication synthesis; do NOT freeze a prereg on the retracted 4-block claim.