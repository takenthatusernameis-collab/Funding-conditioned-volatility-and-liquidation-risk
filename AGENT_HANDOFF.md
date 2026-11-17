# AGENT HANDOFF — 2026-11-17T07:11:10Z (sole durable handoff)

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION (do this first)

**Priority 0 — repository and rank-0 state.**
- Repository: `Funding-conditioned-volatility-and-liquidation-risk` (funding-conditioned volatility and liquidation risk). **Prioritize by repo name: Track C funding-conditioned volatility first.** Track A (observed-liquidation arm) is externally blocked (no admissible post-2026-10 labels/source; no agent-settable Gate 4 attestation). Track B is `COMPLETE_INCONCLUSIVE`.
- Program: `CLOSED_TERMINAL` — final structural closure `research_state/fclr_final_structural_closure_20261116T114626.{md,json}`; verdict `NO_CLAIM_WORTHY_RESULT_PROMOTABLE; ALL_P1_P2_P3_SEALED`. No feasible ≥3-block pre-registered design remains on cached confirmatory data (now proven, see §"FCLR-014 resolution").
- Rank-0: `FCLR-BOUNDED-TRIGGER-ONLY-20261115T220000Z` (`TRIGGER_ONLY` / `BOUNDED_TRIGGER_ONLY`, `next_action_heavy=null`). All cached-data confirmatory estimands are terminal.
- Consequence: **do not start or re-run any sealed cached-data confirmatory estimand; do not re-run FCLR-014; do not re-run the replication synthesis.** A trigger-check-only session, a tests/gates-only session, a copied bundle, a re-audit of static bundles, or a prose-only "blocker confirmed" note is **NOT** completion.

**MANDATORY HEAVY WORK (non-skippable): campaign `FCLR-REPRO-SYNTH-05` — design-frontier hardening + replication robustness certificate.** Completion requires ALL of:
1. new `research_state/session_<UTC>/` (actual UTC);
2. `recompute_design_frontier_certificate_<UTC>.{py,json,md}` — a NEW quantitative artifact that implements a **mark+funding-only non-overlapping block frontier** (30d train + 7d embargo + 30d test per block; blocks must be mutually non-overlapping in `[train_start, test_end]`) and emits a machine-readable certificate with, per estimand (full-C2 and mark+funding-only): feasible-block count *with and without* the non-overlap constraint, contiguous-run feasibility vs `MIN_DESIGN_DAYS=127`, and `promotable=false`. It must reproduce the closed verdict for FCLR-014: full-C2 = 0 blocks; mark+funding-only = 4 individually-feasible but **2 mutually non-overlapping** (<3) → `BLOCKED_ON_DESIGN`.
3. `replication_robustness_<UTC>.{json,md}` — a NEW robustness artifact over the 7 completed recomputes: leave-one-out qualitative-corroboration rate + Wilson CI, sign-consistency of the C2-vs-B1 effects, and an explicit estimand-heterogeneity caveat (QLIKE vs Brier, different designs). Include the **boundary certificate**: the exact minimal change (which study, what effect, what block count) that would flip the programme from "no promotable result" to "promotable".
4. If you harden the tool itself (recommended): add the mark+funding-only non-overlapping frontier to `scripts/next_campaign_status.py` (new `--json` key `markfund_frontier`), add unit tests proving (a) non-overlap enforcement, (b) FCLR-014 → exactly 2 blocks, (c) no change to existing full-C2 frontier outputs. **Register any new `scripts/*.py` in BOTH scope registries** (`research_state/tracka_script_scope_registry.json` + the second registry used by `scripts/check_tracka_scope_registry_drift.py`). Do NOT weaken the completeness rule to fabricate feasibility.
5. `evidence_audit_<UTC>.md` + trigger-check record + gate/suite captures under the session dir;
6. this handoff updated with actual results and the queue ticked.

**Read first (in order):**
1. `research_state/resume_trigger_registry.json`
2. `research_state/ironflow_monitor_state.json`
3. `research_state/session_20261117T071110Z/evidence_audit_20261117T071110Z.md` + `recompute_fclr014_design_admissibility_20261117T071110Z.md` + `replication_synthesis_20261117T071110Z.md` (this session's completed heavy work — the authoritative baseline you build on)
4. `research_state/FCLR_HEAVY_CAMPAIGN_NEXT.md` (detailed campaign note)
5. `scripts/next_campaign_status.py` (`TESTED_WINDOWS`, `MIN_DESIGN_DAYS`, `disjoint_block_frontier`, `ready_windows`) — the canonical frontier to extend
6. `research_state/pre_registration_fclr014_confirmatory_funding_vol_20261109T181124Z.json` (frozen `NO_GO`; splits are an FCLR-002 2-block copy)

**Completed work — do not repeat:**
- **FCLR-014 — DONE and BLOCKED-ON-DESIGN (`session_20261117T071110Z`).** Definitive adjudication: canonical full-C2 tool = 0 feasible blocks / no ≥127d run; mark+funding-only = 4 individually-feasible months (2024-10/11/12, 2025-01) but only **2 mutually non-overlapping** (2024-10, 2025-01) < 3 → no ≥3-block confirmatory design can be frozen; `permits_new_prereg=false`. **RETRACTED:** the "FEASIBLE / freeze a new mark+funding-only prereg using 2024-10, 2024-11, 2024-12" claim in `session_20261117T051045Z` and the corrected `session_20261117T041333Z` JSON — those blocks overlap in train/test windows (leakage). Do NOT freeze a prereg on it.
- **Replication synthesis — DONE (`session_20261117T071110Z`).** 7 studies: qualitative corroboration 7/7 (Wilson95 0.646–1.000); within-tolerance 2/7 (FCLR-006, FCLR-009); FCLR-002/003/008 diverge on exact values but agree on qualitative NOT_MET; FCLR-010/013 NOT_REPLICATED; **promotable positive results NONE**. Do not re-run.
- FCLR-013 — `session_20261117T031656Z`; ZIP/CSV parquet-free recompute; NOT_REPLICATED (C2-vs-B1 rel -4.99%, CI crosses zero, 1 test block).
- FCLR-010 — `session_20261117T002014Z`; CSV/JSON parquet-free recompute; NOT_REPLICATED (0.50% vs sealed 2.21%).
- FCLR-002/003 — `session_20261117T000400Z`; exact values diverged beyond tolerance; NOT_MET corroborated.
- FCLR-009 — `session_20261116T125624Z` (`all_within_tolerance=true`).
- FCLR-006 — `session_20261116T185811Z` (`all_within_tolerance=true`; supersedes `session_20261116T140001Z`).
- FCLR-008 — `session_20261116T230140Z` (B0/B1 within tolerance; C1/C2 divergence documented; NOT_MET corroborated; `session_20261116T221127Z` superseded).
- FCLR-RCA-011 — complete bundle `session_20261116T100533Z`.

**Blocked-path warning (do not waste a session here):**
- **No parquet engine is installed** (`pyarrow`, `fastparquet`, `duckdb`, `polars` all absent; network installs prohibited). Any task whose only input is `.parquet` is blocked unless a CSV/JSON/ZIP twin exists. Use the ZIP/CSV reader pattern from `session_20261117T031656Z` / `session_20261117T000400Z`.
- `research_state/research_protocol_fclr002.md` and `research_state/research_protocol_fclr003.md` **do not exist** — do not block on them.
- `research_state/run_manifest.json`, `run_manifest_FCLR002.json`, `data_cache/fclr002_panel*.json`, `data_cache/manifest_fclr002.json`, `data_cache/manifest_fclr003.json` are **unresolved Git-LFS pointers with no local object**. Do NOT run `git lfs pull` (network prohibited).
- **2024 cache format:** Apr–Jun 2024 mark/premium/index files are ZIPs; Jan–Mar and Jul–Nov 2024 are CSVs; 2025–2026 are ZIP+CSV. Use a ZIP-aware reader.
- Do NOT run `scripts/fclr_liq_010_confirm.py` (parquet-only; fails on import).

**Execute in order (do not skip to "stop cleanly"):**
1. **Create `research_state/session_<UTC>/`** (actual UTC). `research_state/` root is **500/500** (fail-closed cap); put ALL new artifacts inside the session subdirectory only. Do NOT add root-level `research_state/*.md|json`.
2. **Check triggers exactly once (no network, no polling).** Read files 1–2. Record timestamp, each trigger status, `data_through`, and post-2026-10 classifications in the session dir. Current: all four `OPEN`; Ironflow `data_through=2026-10`, `consecutive_absent=3`; 2026-11/2026-12/2027-01 `CONFIRMED_ABSENT`.
3. **Emit `recompute_design_frontier_certificate_<UTC>.{py,json,md}`** (primary heavy artifact) per MANDATORY item 2 above. Reproduce the FCLR-014 closed verdict; emit per-estimand with/without non-overlap counts.
4. **Emit `replication_robustness_<UTC>.{json,md}`** per MANDATORY item 3 (LOO + sign-consistency + heterogeneity caveat + boundary certificate). Do not re-run the synthesis; build on `session_20261117T071110Z/replication_synthesis_20261117T071110Z.json`.
5. **(Recommended) Harden `scripts/next_campaign_status.py`** with the mark+funding-only non-overlapping frontier + tests; register in both scope registries. If you skip the tool patch, still emit the certificate artifact in step 3.
6. **Audit carried-forward evidence.** Confirm the sessions listed under "Completed work" are present. Write a concise `evidence_audit_<UTC>.md`.
7. **Run and capture every required gate under the new session dir:**
   - `python3 scripts/check_handoff_heavywork_gate.py --json` — PASS (complete bundle + new session audit + fresh `recompute_*` artifact, root ≤ 500). **The gate resolves the lexicographically-latest `session_<UTC>` id mentioned in this handoff and requires that session to hold `evidence_audit_*` + a `recompute_*`/quant artifact.**
   - `python3 scripts/check_tracka_scope_registry_drift.py --json` — PASS (register any new `scripts/*.py` in both scope registries).
   - `python3 -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_117 tests.test_tracka_hardening_118 tests.test_tracka_hardening_143` — all pass (52 tests).
   - `python3 -m unittest discover -q` — run to completion; record exact test count, skip count, error list, and final EXIT. **Baseline:** 1340 tests, 4 pre-existing errors (all `tests.test_fclr_liq_combined_admissibility_audit`, missing `pyarrow`; environmental), 18 skipped, EXIT 1. Success = identical set with no new failures/errors. Never treat timeout/monitor cap as green. Revert any timestamp-only side effect to tracked files.
8. **Update only this handoff** after steps 3–7: replace timestamp/verification with actual results, tick the queue, keep sole-handoff contract, bundle refs, and blockers intact. Do not create another handoff file.

**Trigger-gated science is the only scientific advance — but must be pre-powered.** If no trigger is satisfied, do not advance or re-run a confirmatory estimand; required holding action is the `FCLR-REPRO-SYNTH-05` artifacts above. If a trigger is satisfied, follow `RESEARCH_PROMPT.md` §16 admissibility/source audit first, freeze a pre-sized prereg before inspecting outcomes (use `session_20261116T035833Z/prereg_template_trigger_gated_20261116T035833Z.json` and power floors in `session_20261116T100533Z/trigger_readiness_power_calibration_20261116T100533Z.md`: Gate4/TrackC `paired_n>=23224`, TrackA/expansion `paired_n>=11689`, ≥3 blocks, 7d purge/embargo), require a materially different estimand, execute, register any new scripts in both scope registries, run all gates, and update frontier/hypothesis registries with an honest verdict.

## Reproducibility-audit queue (non-skippable; do in order)

1. ~~FCLR-009~~ — DONE (`session_20261116T125624Z`; `all_within_tolerance=true`).
2. ~~FCLR-006~~ — DONE (`session_20261116T185811Z`; `all_within_tolerance=true`).
3. ~~FCLR-008~~ — DONE (`session_20261116T230140Z`; NOT_MET corroborated).
4. ~~FCLR-002~~ — DONE (`session_20261117T000400Z`; diverged beyond tolerance; NOT_MET corroborated).
5. ~~FCLR-003~~ — DONE (`session_20261117T000400Z`; NOT_MET corroborated).
6. ~~FCLR-010~~ — DONE (`session_20261117T002014Z`; NOT_REPLICATED).
7. ~~FCLR-013~~ — DONE (`session_20261117T031656Z`; NOT_REPLICATED).
8. ~~FCLR-014 panel coverage audit + blocker resolution~~ — DONE (`session_20261117T041333Z`, `session_20261117T051045Z`, adjudicated in `session_20261117T071110Z`; **BLOCKED-ON-DESIGN**, 4-block feasibility retracted).
9. **FCLR-REPRO-SYNTH-05 design-frontier certificate + replication robustness — CURRENT** (this handoff's MANDATORY heavy work).

A session that completes an item must (a) create `research_state/session_<UTC>/`, (b) emit a new quantitative artifact named per queue, (c) write evidence audit, (d) run all gates + full discovery suite to completion with recorded EXIT, (e) update this handoff and tick the queue item.

## Heavy-work evidence on disk (authoritative; do not redo)

- **FCLR-REPRO-SYNTH-05 baseline — `research_state/session_20261117T071110Z/`:** `recompute_fclr014_design_admissibility_20261117T071110Z.{py,json,md}` (BLOCKED-ON-DESIGN), `replication_synthesis_20261117T071110Z.{json,md}` + `recompute_replication_synthesis_20261117T071110Z.py` (7/7 corroboration, 2/7 tolerance, 0 promotable), `trigger_check_20261117T071110Z.json`, `evidence_audit_20261117T071110Z.md`, gate/suite captures.
- **FCLR-013 — `research_state/session_20261117T031656Z/`:** ZIP/CSV parquet-free recompute; NOT_REPLICATED.
- **FCLR-010 — `research_state/session_20261117T002014Z/`:** CSV/JSON parquet-free recompute; NOT_REPLICATED.
- FCLR-002/FCLR-003 — `research_state/session_20261117T000400Z/`.
- FCLR-008 — `research_state/session_20261116T230140Z/`.
- FCLR-006 — `research_state/session_20261116T185811Z/`.
- FCLR-009 — `research_state/session_20261116T125624Z/`.
- Self-contained bundle: `research_state/session_20261116T100533Z/` (5 RCA-011 families + power calibration).
- `research_state/session_20261116T115028Z/`: third numpy-only FCLR-011 crosscheck confirming sealed PASS not reproducible.

**Incomplete / non-counting sessions (do not resume, copy, or count):**
- `session_20261116T104644Z/`, `session_20261116T105341Z/`, `session_20261116T134957Z/` (trigger-only).
- `session_20261116T140001Z/` superseded (tolerance-failed FCLR-006).
- `session_20261116T221127Z/` superseded (divergent FCLR-008).
- **`session_20261117T050235Z/`, `session_20261117T060341Z/` — EMPTY (0 files), wasted loops, non-counting.**
- **`session_20261117T060853Z/` — PHANTOM: its evidence audit cites `fclr014_panel_coverage_audit_20261117T060853Z.{json,md}` and `fclr014_panel_blocker_resolution_20261117T060853Z.{json,md}` that were never written (only `evidence_audit` + `trigger_check` exist). Non-counting.**
- `session_20261117T041333Z/` (FCLR-014 coverage + blocker, 2-block reading correct; its corrected JSON 4-block claim is retracted) and `session_20261117T051045Z/` (FCLR-014 coverage + blocker, 4-block feasibility RETRACTED) are **superseded by the adjudication in `session_20261117T071110Z`** — cite them as history, do not re-derive from them.

## Bottlenecks removed / prevented

- **FCLR-014 "blocked-on-data" misclassification corrected earlier:** the cache holds complete 5-symbol mark+funding for 2024-04..2026-10 and full mark+index+premium+funding for 2025-01..2026-10; the blocker is **design admissibility**, not data absence.
- **FCLR-014 design conflict RESOLVED this session:** contradictory resolutions (041333Z 2-block vs 051045Z 4-block) adjudicated against the canonical tool + an explicit non-overlap constraint. Definitive: **BLOCKED-ON-DESIGN**; the 4-block "freeze a prereg" claim is **retracted** (overlapping train/test → cross-block leakage). Future agents must cite `session_20261117T071110Z`, not re-litigate.
- **Stale-handoff bottleneck removed:** the 06:18:09Z handoff named `session_20261117T031656Z` as latest while five newer sessions existed; this handoff records all of them and points at a live frontier (`FCLR-REPRO-SYNTH-05`).
- **Empty-session and phantom-artifact loops quarantined:** `session_20261117T050235Z`, `session_20261117T060341Z` (empty) and `session_20261117T060853Z` (phantom refs) are marked non-counting so they cannot be mistaken for progress or resumed.
- **`next_campaign_status.py` enumeration gap (documented, still open — target of the next campaign):** `ready_windows()` only evaluates the full-C2 completeness rule and never computes the mark+funding-only non-overlapping frontier, which is why sessions improvised and disagreed. The next session should close this by adding the frontier + tests (register any `scripts/*.py`).
- **Parquet engine absent:** no `pyarrow`/`fastparquet`/`duckdb`/`polars`; network installs prohibited. Use CSV/JSON/ZIP twins; never fabricate.
- **Nonexistent protocol paths / unresolved LFS:** `research_protocol_fclr002.md` / `fclr003.md` do not exist; `run_manifest*.json`, `fclr002_panel*.json`, `manifest_fclr002/003.json` are pointers with no local object. Do not block or `git lfs pull`.
- **2024 ZIP/CSV bottleneck:** Apr–Jun 2024 files are ZIPs; use a ZIP-aware reader.
- **Root churn:** 500/500 — session-only writes required.
- **Handoff authority:** this file only (`AGENT_HANDOFF.md`).

## Bottlenecks and prohibitions

- Do not start or re-run any cached-data confirmatory estimand; all sealed estimands are terminal.
- Do not re-run FCLR-014 or the replication synthesis; do not freeze a prereg on the retracted 4-block claim.
- Do not mutate sealed artifacts, frontier, hypothesis registries, or `.github/workflows/*`.
- Do not poll, re-probe the HuggingFace tree, use paid/credentialed/manual outcome data, or add root-level `research_state/*.md|json`.
- Do not add `statsmodels` or unpinned heavy dependencies to the core path.
- Do not run `git lfs pull` or otherwise fetch network data.
- Do not run `scripts/fclr_liq_010_confirm.py` (parquet-only; will fail on import).
- Discovery suite is long-running; let it finish and record actual EXIT, not partial/timeout.
- Scientific blocker is external (no admissible post-2026-10 observed liquidation labels/source; no agent-settable Gate 4 attestation) AND design-admissibility (no contiguous untested ≥127d window under `TESTED_WINDOWS`). Agent-removable requirement: `FCLR-REPRO-SYNTH-05` design-frontier certificate + replication robustness + evidence audit + complete verification + accurate handoff update.

## Reopen triggers (machine-checkable — Act ONLY when satisfied; all `OPEN`)

- `GATE4_BRANCH_1` — `research_state/fclr016_v5_terms_evidence_RESOLVED_*.json` (`status: RESOLVED_VERIFIED`, `fabricated: false`). Human/legal attestation only.
- `NEW_OBSERVED_LIQUIDATION_SOURCE` — `research_state/<source>_admissibility_audit_<UTC>.{md,json}` (`status: ADMISSIBLE`, `observed_labels: true`, ≥5 instruments, ≥3 blocks or ≥1 complete month).
- `HL_LABEL_EXTENSION` — `research_state/hl_label_extension_audit_<UTC>.{md,json}`.
- `EXPANSION_ROBUSTNESS_REDO` — `research_state/expansion_robustness_redo_prereg_<UTC>.json` + `evaluation_summary_*.json`.

## Tombstones (no authority)

- `NEXT_SESSION_HANDOFF.md`, `NEXT_SESSION_TASK.md`: tombstoned 2026-11-15T22:57:29Z.
- `AGENT_HANDOFF_20261115T073240Z.md`: SUPERSEDED — ignore.
- `HANDOFF_NEXT_SESSION_20261116T114626Z.md`: tombstoned 2026-11-16T12:45:00Z — ignore.
- `HANDOFF_NEXT_SESSION_20261117T033007Z.md`: tombstoned 2026-11-17T04:09:17Z — ignore.

## Verification record — 2026-11-17T07:11:10Z handoff rebuild

- **Changed:** rebuilt the sole durable handoff with current timestamp and a repo-name-prioritized initial task message. Recorded the five previously-unrecorded sessions (`041333Z`, `050235Z`, `051045Z`, `060341Z`, `060853Z`).
- **FCLR-014 — resolved to `BLOCKED_ON_DESIGN`** in new `session_20261117T071110Z/`: canonical full-C2 tool = 0 feasible blocks / no ≥127d run; mark+funding-only = 4 individually-feasible months but **2 mutually non-overlapping** (<3); the "FEASIBLE / freeze a new mark+funding-only prereg" claim (`session_20261117T051045Z`, corrected `session_20261117T041333Z`) is **RETRACTED** as leakage-prone. `permits_new_prereg=false`.
- **Replication synthesis — DONE** in `session_20261117T071110Z/`: 7 studies, qualitative corroboration **7/7** (Wilson95 0.646–1.000), within-tolerance **2/7** (FCLR-006, FCLR-009), **promotable positive results NONE**; programme `CLOSED_TERMINAL`.
- **Bottlenecks removed:** FCLR-014 conflict adjudicated; empty sessions (`050235Z`, `060341Z`) and phantom session (`060853Z`) quarantined as non-counting; stale latest-session pointer corrected.
- **Baseline gates (verified this session):** `check_handoff_heavywork_gate.py --json` **PASS** (root 500/500, `reason_code: OK`); `check_tracka_scope_registry_drift.py --json` **PASS** (196 scripts, no drift). Targeted tests **52 OK**. Full suite **1340 tests, 4 pre-existing pyarrow errors, 18 skipped, EXIT 1** (identical to baseline; no regression).
- **Next focus campaign:** `FCLR-REPRO-SYNTH-05` — design-frontier certificate + replication robustness (+ optional `next_campaign_status.py` hardening), with a non-skippable heavy-work completion floor.
- **Queue:** FCLR-009/006/008/002/003/010/013/014 DONE; FCLR-REPRO-SYNTH-05 CURRENT.
- **Git tree:** new session artifacts under `research_state/session_20261117T071110Z/` only; no tracked source file modified beyond this handoff and the campaign note.

---

**This handoff is the single durable artifact for the next session. Execute the INITIAL TASK MESSAGE above. Do not create additional handoff files. Update only `AGENT_HANDOFF.md` after completion.**