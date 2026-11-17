# AGENT HANDOFF — 2026-11-17T13:17:51Z (sole durable handoff)

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION (do this first)

**Priority 0 — repository and rank-0 state.**
- Repository: `Funding-conditioned-volatility-and-liquidation-risk` (funding-conditioned volatility and liquidation risk). **Prioritize by repository name: Track C funding-conditioned volatility first.** Track A (observed-liquidation arm) is externally blocked (no admissible post-2026-10 labels/source; no agent-settable Gate 4 attestation). Track B is `COMPLETE_INCONCLUSIVE`.
- Program: `CLOSED_TERMINAL` — final structural closure `research_state/fclr_final_structural_closure_20261116T114626.{md,json}`; verdict `NO_CLAIM_WORTHY_RESULT_PROMOTABLE; ALL_P1_P2_P3_SEALED`. No feasible ≥3-block pre-registered design remains on cached confirmatory data (proven in `session_20261117T072040Z`).
- Rank-0: `FCLR-BOUNDED-TRIGGER-ONLY-20261115T220000Z` (`TRIGGER_ONLY` / `BOUNDED_TRIGGER_ONLY`, `next_action_heavy=null`). All cached-data confirmatory estimands are terminal.
- Consequence: **do not start or re-run any sealed cached-data confirmatory estimand; do not re-run FCLR-014, the replication synthesis, or FCLR-REPRO-SYNTH-05.** A trigger-check-only session, tests/gates-only session, copied bundle, static re-audit, handoff-only refresh, or "stop cleanly" is **NOT** completion.

**MANDATORY HEAVY WORK — `FCLR-FRONTIER-VERIFY-06` (non-skippable).**
All cached-data confirmatory work is terminal, so the next session must perform a new, independent quantitative verification of the certified design frontier. This is not a new outcome claim and must not read outcome data. It is a heavy reproducibility/robustness artifact that hardens the closure against the earlier contradictory 2-block/4-block sessions.

## NEXT FOCUS CAMPAIGN — `FCLR-FRONTIER-VERIFY-06-20261117T130551Z` (future agents cannot opt out)

This campaign binds every future session to heavy quantitative work. It is enforced by `scripts/check_handoff_heavywork_gate.py` and `scripts/check_tracka_scope_registry_drift.py`. No session may close without satisfying all of:

1. **New session dir required:** `research_state/session_<UTC>/` (actual UTC). `research_state/` root is **500/500** (fail-closed cap); ALL new artifacts go inside the session subdirectory only. Root-level `research_state/*.md|json` is prohibited.
2. **Trigger check exactly once (no network, no polling):** read `research_state/resume_trigger_registry.json` and `research_state/ironflow_monitor_state.json`. Record timestamp, each trigger status, `data_through`, and post-2026-10 classifications in the session dir. Current: all four triggers `OPEN`; Ironflow `data_through=2026-10`, `consecutive_absent=3`; 2026-11/2026-12/2027-01 `CONFIRMED_ABSENT`.
3. **No-trigger rule:** if no trigger is satisfied (current state), do NOT start or re-run any sealed cached-data confirmatory estimand, do NOT re-run FCLR-014/synthesis/FCLR-REPRO-SYNTH-05, and do NOT hold a no-op session. Closure is certified; the required work is the independent frontier audit below.
4. **Heavy-work floor:** produce a new quantitative artifact materially different from sealed work. The required artifact is `recompute_frontier_exhaustive_audit_<UTC>.{py,json,md}`, independently implemented in the session dir. Do not merely copy or re-audit `session_20261117T072040Z`; do not merely run gates/tests; do not write prose only. The artifact must include an independent raw-cache reconstruction, exhaustive subset enumeration, overlap analysis, and exact comparison against the canonical tool.
5. **Required audit content:**
   - Reconstruct complete mark+funding months and complete full-C2 months directly from `research_state/data_cache/` for the five symbols (`BTCUSDT`, `ETHUSDT`, `BNBUSDT`, `SOLUSDT`, `XRPUSDT`) using a stdlib-only, ZIP/CSV-aware reader. Do not import `scripts/next_campaign_status.py` for the computation; use it only as the comparison target.
   - Read the tested-window boundaries from the canonical script/JSON for exclusion, but recompute candidate feasibility independently. Do not treat any tested month as fresh.
   - Build 30d-train + 7d-embargo + 30d-test blocks. For each estimand family (full-C2 and mark+funding-only), enumerate **all subsets** of individually feasible test months (not a greedy shortcut) and compute the maximum mutually non-overlapping selection on `[train_start, test_end]`.
   - Compute all overlapping pairs, all maximal non-overlapping selections, contiguous untested month runs, and span vs `MIN_DESIGN_DAYS=127`.
   - Include a design-only sensitivity grid for block length 14/30 days and embargo 7 days, clearly labeled `EXPLORATORY_DESIGN_ONLY / NOT_A_PREREG / NOT_PROMOTABLE`. Do not inspect outcomes.
   - Compare independently computed values to `scripts/next_campaign_status.py --json` (`disjoint_block_frontier`, `markfund_frontier`) and to `session_20261117T072040Z/recompute_design_frontier_certificate_20261117T072040Z.json`. Record `exact_match` booleans per field.
6. **Expected closed-world result (must be reproduced or explicitly contradicted):**
   - Full-C2: **0** disjoint feasible blocks; **no** contiguous run ≥127d; `campaign_feasible=false`.
   - Mark+funding-only: **4** individually feasible months — `2024-10`, `2024-11`, `2024-12`, `2025-01`; **2** mutually non-overlapping — `2024-10`, `2025-01`; **5** overlapping pairs; `campaign_feasible_non_overlapping=false`; no contiguous untested complete mark+funding run ≥127d.
   - Overall: `BLOCKED_ON_DESIGN`, `promotable=false`, `fclr014_closed_verdict_reproduced=true`.
   - If the independent audit disagrees with any of these, stop, record the exact mismatch and the evidence, do not edit sealed artifacts, and report `FRONTIER_VERIFICATION_MISMATCH` in the session audit and handoff. Do not silently "fix" the canonical tool without a failing test and a new session artifact.
7. **Evidence audit:** write `evidence_audit_<UTC>.md` confirming all carried-forward bundles are present and not re-run. Include the exact files read and the exact command outputs used for comparison.
8. **Gates + suite:** run and capture under the new session dir: `python3 scripts/check_handoff_heavywork_gate.py --json`, `python3 scripts/check_tracka_scope_registry_drift.py --json`, targeted `python3 -m unittest tests.test_active_campaign_gate tests.test_next_campaign_status tests.test_tracka_hardening_117 tests.test_tracka_hardening_118 tests.test_tracka_hardening_143`, and `python3 -m unittest discover -q` to completion (record count/skip/error/EXIT). **Baseline is environment-dependent.** The prior handoff recorded 1340 tests / 4 errors / 18 skipped / EXIT 1; the current sandbox run recorded **1119 tests, 62 errors, 9 failures, 14 skipped, EXIT 1** (mostly missing `numpy`/`pyarrow` and unresolved LFS fixtures). Record the actual run; never treat timeout/monitor cap or a missing-dependency error set as green. Revert any timestamp-only side effect to tracked files.
9. **Handoff update:** update only `AGENT_HANDOFF.md` after work; preserve sole-handoff contract, bundle refs, blockers, and this campaign intact. If `scripts/next_campaign_status.py` is changed, register it in both scope registries and add a regression test; otherwise do not touch it.

**Trigger-satisfied path:** if any trigger fires, follow `RESEARCH_PROMPT.md` §16 admissibility/source audit first; freeze a pre-sized prereg before inspecting outcomes (use `session_20261116T035833Z/prereg_template_trigger_gated_20261116T035833Z.json` and power floors in `session_20261116T100533Z/trigger_readiness_power_calibration_20261116T100533Z.md`: Gate4/TrackC `paired_n>=23224`, TrackA/expansion `paired_n>=11689`, ≥3 blocks, 7d purge/embargo, `outcome_data_inspected_before_freeze=false`); require a materially different estimand; execute; record an honest verdict; register any new `scripts/*.py` in both scope registries.

**Read first (in order):**
1. `research_state/resume_trigger_registry.json`
2. `research_state/ironflow_monitor_state.json`
3. `research_state/session_20261117T072040Z/evidence_audit_20261117T072040Z.md` + `recompute_design_frontier_certificate_20261117T072040Z.{py,json,md}` + `replication_robustness_20261117T072040Z.{py,json,md}`
4. `research_state/session_20261117T071110Z/` (baseline adjudication/synthesis)
5. `research_state/FCLR_HEAVY_CAMPAIGN_NEXT.md`
6. `scripts/next_campaign_status.py` (`TESTED_WINDOWS`, `MIN_DESIGN_DAYS`, `disjoint_block_frontier`, `markfund_frontier`, `ready_windows`)
7. `tests/test_next_campaign_status.py` (canonical frontier expectations)

## Completed work — do not repeat

- **FCLR-REPRO-SYNTH-05 — DONE (`session_20261117T072040Z`).** `recompute_design_frontier_certificate_20261117T072040Z.{py,json,md}`: full-C2 0 disjoint feasible blocks / no contiguous run ≥127d → `BLOCKED_ON_DESIGN`; mark+funding-only 4 individually feasible (2024-10/11/12, 2025-01) but **2 mutually non-overlapping** (2024-10, 2025-01) < 3, 5 overlapping pairs, contiguous untested <127d → `BLOCKED_ON_DESIGN`; overall `BLOCKED_ON_DESIGN`, `promotable=false`, `fclr014_closed_verdict_reproduced=true`. `replication_robustness_20261117T072040Z.{py,json,md}`: qualitative corroboration 7/7, Wilson95 [0.646,1.000], LOO 6/6 all-unity; sign consistency C2-vs-B1 positive 3 / negative 4 (mixed QLIKE/Brier); boundary certificate = no promotable result without a trigger-satisfied/pre-powered ≥3-block preregistered admissible design or a new design-feasible cached-data estimand passing confirmatory gates. Do not re-run.
- **FCLR-014 — DONE and BLOCKED-ON-DESIGN (`session_20261117T071110Z`, reproduced `session_20261117T072040Z`).** Canonical full-C2 0 feasible blocks / no ≥127d run; mark+funding-only 4 individually feasible but 2 mutually non-overlapping < 3; `permits_new_prereg=false`. **RETRACTED:** 4-block "freeze a prereg" claim (`session_20261117T051045Z`, corrected `session_20261117T041333Z`) — leakage-prone. Cite `session_20261117T071110Z`, do not re-litigate.
- **Replication synthesis — DONE (`session_20261117T071110Z`, robustness extended `session_20261117T072040Z`).** 7 studies: qualitative corroboration 7/7 (Wilson95 0.646–1.000); within-tolerance 2/7 (FCLR-006, FCLR-009); promotable positive results NONE. Do not re-run.
- FCLR-013 — `session_20261117T031656Z`; ZIP/CSV parquet-free recompute; NOT_REPLICATED (C2-vs-B1 rel -4.99%, CI crosses zero, 1 test block).
- FCLR-010 — `session_20261117T002014Z`; CSV/JSON parquet-free recompute; NOT_REPLICATED (0.50% vs sealed 2.21%).
- FCLR-002/003 — `session_20261117T000400Z`; exact values diverged beyond tolerance; NOT_MET corroborated.
- FCLR-009 — `session_20261116T125624Z` (`all_within_tolerance=true`).
- FCLR-006 — `session_20261116T185811Z` (`all_within_tolerance=true`; supersedes `session_20261116T140001Z`).
- FCLR-008 — `session_20261116T230140Z` (B0/B1 within tolerance; C1/C2 divergence documented; NOT_MET corroborated; `session_20261116T221127Z` superseded).
- FCLR-RCA-011 — complete bundle `session_20261116T100533Z`.

## Blocked-path warning (do not waste a session here)

- **No parquet engine is installed** (`pyarrow`, `fastparquet`, `duckdb`, `polars` all absent; network installs prohibited). Any task whose only input is `.parquet` is blocked unless a CSV/JSON/ZIP twin exists. Use the ZIP/CSV reader pattern from `session_20261117T031656Z` / `session_20261117T000400Z`.
- `research_state/research_protocol_fclr002.md` and `research_state/research_protocol_fclr003.md` **do not exist** — do not block on them.
- `research_state/run_manifest.json`, `run_manifest_FCLR002.json`, `data_cache/fclr002_panel*.json`, `data_cache/manifest_fclr002.json`, `data_cache/manifest_fclr003.json` are **unresolved Git-LFS pointers with no local object**. Do NOT run `git lfs pull` (network prohibited).
- **2024 cache format:** Apr–Jun 2024 mark/premium/index files are ZIPs; Jan–Mar and Jul–Nov 2024 are CSVs; 2025–2026 are ZIP+CSV. Use a ZIP-aware reader.
- Do NOT run `scripts/fclr_liq_010_confirm.py` (parquet-only; fails on import).

## Execute in order (do not skip to "stop cleanly")

1. **Create `research_state/session_<UTC>/`** (actual UTC). `research_state/` root is **500/500** (fail-closed cap); put ALL new artifacts inside the session subdirectory only.
2. **Check triggers exactly once (no network, no polling).** Read files 1–2. Record timestamp, each trigger status, `data_through`, and post-2026-10 classifications in the session dir. Current: all four `OPEN`; Ironflow `data_through=2026-10`, `consecutive_absent=3`; 2026-11/2026-12/2027-01 `CONFIRMED_ABSENT`.
3. **If no trigger is satisfied (current state):** do not start/re-run any sealed cached-data confirmatory estimand and do not re-run FCLR-014/synthesis/FCLR-REPRO-SYNTH-05. Perform the independent `FCLR-FRONTIER-VERIFY-06` audit exactly as specified above.
4. **If a trigger is satisfied:** follow `RESEARCH_PROMPT.md` §16 admissibility/source audit first; freeze a pre-sized prereg before inspecting outcomes (use `session_20261116T035833Z/prereg_template_trigger_gated_20261116T035833Z.json` and power floors in `session_20261116T100533Z/trigger_readiness_power_calibration_20261116T100533Z.md`: Gate4/TrackC `paired_n>=23224`, TrackA/expansion `paired_n>=11689`, ≥3 blocks, 7d purge/embargo, `outcome_data_inspected_before_freeze=false`); require a materially different estimand; execute and record an honest verdict; register any new `scripts/*.py` in both scope registries.
5. **Audit carried-forward evidence.** Confirm completed sessions listed above are present. Write `evidence_audit_<UTC>.md`.
6. **Run and capture gates under the new session dir:** `python3 scripts/check_handoff_heavywork_gate.py --json`, `python3 scripts/check_tracka_scope_registry_drift.py --json`, targeted `python3 -m unittest tests.test_active_campaign_gate tests.test_next_campaign_status tests.test_tracka_hardening_117 tests.test_tracka_hardening_118 tests.test_tracka_hardening_143`, and `python3 -m unittest discover -q` to completion (record count/skip/error/EXIT). **Baseline is environment-dependent.** The prior handoff recorded 1340 tests / 4 errors / 18 skipped / EXIT 1; the current sandbox run recorded **1119 tests, 62 errors, 9 failures, 14 skipped, EXIT 1** (mostly missing `numpy`/`pyarrow` and unresolved LFS fixtures). Record the actual run; never treat timeout/monitor cap or a missing-dependency error set as green. Revert timestamp-only side effect to tracked files.
7. **Update only this handoff** after work: replace timestamp/verification with actual results, keep sole-handoff contract, bundle refs, and blockers intact.

**Trigger-gated science is the only scientific advance — but must be pre-powered.** If no trigger is satisfied, do not advance or re-run a confirmatory estimand; the required holding action is the `FCLR-FRONTIER-VERIFY-06` independent frontier audit. If a trigger is satisfied, follow `RESEARCH_PROMPT.md` §16 admissibility/source audit first, freeze a pre-sized prereg before inspecting outcomes, require a materially different estimand, execute, register any new scripts in both scope registries, run all gates, and update frontier/hypothesis registries with an honest verdict.

## Reproducibility-audit queue (non-skippable; do in order)

1. ~~FCLR-009~~ — DONE (`session_20261116T125624Z`; `all_within_tolerance=true`).
2. ~~FCLR-006~~ — DONE (`session_20261116T185811Z`; `all_within_tolerance=true`).
3. ~~FCLR-008~~ — DONE (`session_20261116T230140Z`; NOT_MET corroborated).
4. ~~FCLR-002~~ — DONE (`session_20261117T000400Z`; diverged beyond tolerance; NOT_MET corroborated).
5. ~~FCLR-003~~ — DONE (`session_20261117T000400Z`; NOT_MET corroborated).
6. ~~FCLR-010~~ — DONE (`session_20261117T002014Z`; NOT_REPLICATED).
7. ~~FCLR-013~~ — DONE (`session_20261117T031656Z`; NOT_REPLICATED).
8. ~~FCLR-014 panel coverage audit + blocker resolution~~ — DONE (`session_20261117T041333Z`, `session_20261117T051045Z`, adjudicated in `session_20261117T071110Z`; **BLOCKED-ON-DESIGN**, 4-block feasibility retracted).
9. ~~FCLR-REPRO-SYNTH-05 design-frontier certificate + replication robustness~~ — DONE (`session_20261117T072040Z`; full-C2 0 blocks/no ≥127d run; mark+funding-only 4 individually / 2 mutually non-overlapping; FCLR-014 verdict reproduced; qualitative corroboration 7/7 Wilson95 [0.646,1.000], LOO 6/6 all-unity; sign mixed 3+/4-; boundary certificate emitted; `promotable=false`).
10. **FCLR-FRONTIER-VERIFY-06 — CURRENT.** Independent exhaustive frontier verification per the campaign above. No queued cached-data confirmatory heavy item remains; this is the next agent-removable heavy item.

A session that completes an item must (a) create `research_state/session_<UTC>/`, (b) emit a new quantitative artifact named per queue, (c) write evidence audit, (d) run all gates + full discovery suite to completion with recorded EXIT, (e) update this handoff and tick the queue item.

## Heavy-work evidence on disk (authoritative; do not redo)

- **FCLR-REPRO-SYNTH-05 — `research_state/session_20261117T072040Z/`:** `recompute_design_frontier_certificate_20261117T072040Z.{py,json,md}` (full-C2 0 blocks/no ≥127d run; mark+funding-only 4 individually feasible, 2 mutually non-overlapping 2024-10/2025-01, 5 pairs; FCLR-014 reproduced; `overall=BLOCKED_ON_DESIGN`, `promotable=false`), `replication_robustness_20261117T072040Z.{py,json,md}` (qualitative 7/7, Wilson95 [0.646,1.000], LOO 6/6 all-unity; C2-vs-B1 sign +3/-4 mixed QLIKE/Brier; boundary certificate), `trigger_check_20261117T072040Z.json`, `evidence_audit_20261117T072040Z.md`, gate/suite captures.
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
- `session_20261117T060853Z/` — PHANTOM (removed 2026-11-17T13:17Z; only `evidence_audit` + `trigger_check` existed). Do not recreate.
- `session_20261117T041333Z/` (FCLR-014 coverage + blocker, 2-block reading correct; its corrected JSON 4-block claim is retracted) and `session_20261117T051045Z/` (FCLR-014 coverage + blocker, 4-block feasibility RETRACTED) are **superseded by the adjudication in `session_20261117T071110Z`** — cite them as history, do not re-derive from them.

## Bottlenecks removed / prevented

- **Empty-session loop removed:** an empty non-counting session directory was removed during this refresh; it is no longer present and must not be recreated. Future sessions must not create a session dir until they have a concrete heavy artifact to write.
- **Stale handoff claim corrected:** the previous handoff said `scripts/next_campaign_status.py` had no mark+funding-only frontier. The canonical tool now exposes `markfund_frontier` and `tests/test_next_campaign_status.py` pins the closed verdict (4 individually feasible / 2 mutually non-overlapping / 5 overlapping pairs). The current campaign treats this as the comparison target, not as open work.
- **FCLR-014 design conflict RESOLVED:** contradictory resolutions (041333Z 2-block vs 051045Z 4-block) adjudicated against the canonical tool + explicit non-overlap constraint. Definitive: **BLOCKED-ON-DESIGN**; the 4-block "freeze a prereg" claim is **retracted** (overlapping train/test → cross-block leakage). Cite `session_20261117T071110Z`, not re-litigate.
- **Empty-session and phantom-artifact loops quarantined:** empty/phantom sessions are non-counting; do not resume or cite them as progress.
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
- Scientific blocker is external (no admissible post-2026-10 observed liquidation labels/source; no agent-settable Gate 4 attestation) AND design-admissibility (no feasible ≥3-block mutually-non-overlapping confirmatory design on cached data; certified `session_20261117T072040Z`). No agent-removable confirmatory cached-data work remains; next advance is trigger-gated under `RESEARCH_PROMPT.md` §16.

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

## Verification record — 2026-11-17T13:17:51Z (handoff refresh; FCLR-FRONTIER-VERIFY-06 active)

- **Current trigger check (once, no network/polling):** `resume_trigger_registry.json` + `ironflow_monitor_state.json` read at 2026-11-17T13:17Z; all four triggers **OPEN** (`GATE4_BRANCH_1`, `NEW_OBSERVED_LIQUIDATION_SOURCE`, `HL_LABEL_EXTENSION`, `EXPANSION_ROBUSTNESS_REDO`); Ironflow `data_through=2026-10`, `consecutive_absent=3`; 2026-11/2026-12/2027-01 `CONFIRMED_ABSENT`. No trigger fired; no confirmatory estimand advanced/re-scored.
- **Last completed heavy session:** `research_state/session_20261117T072040Z/` (FCLR-REPRO-SYNTH-05 DONE). Queue 1–9 complete; **current mandatory heavy item is FCLR-FRONTIER-VERIFY-06** — independent exhaustive frontier audit `recompute_frontier_exhaustive_audit_<UTC>.{py,json,md}` in a new `research_state/session_<UTC>/`.
- **Bottlenecks removed this pass:** removed phantom non-counting session `research_state/session_20261117T060853Z/` (contained only `evidence_audit` + `trigger_check`, no heavy artifact; previously flagged PHANTOM). No empty/phantom session dirs remain. Handoff/campaign authority consolidated in `AGENT_HANDOFF.md` + `research_state/FCLR_HEAVY_CAMPAIGN_NEXT.md`.
- **Gates (read-only, this pass):** `check_handoff_heavywork_gate.py --json` **PASS** (`reason_code: OK`, root 500/500, latest session `session_20261117T072040Z`); `check_tracka_scope_registry_drift.py --json` **PASS** (196 scripts, no drift). Targeted/full suites not rerun this maintenance pass (no new quantitative artifact produced); environment baseline recorded as **1119 tests, 62 errors, 9 failures, 14 skipped, EXIT 1** (missing `numpy`/`pyarrow`, unresolved LFS fixtures). Next session that performs FCLR-FRONTIER-VERIFY-06 must run and capture targeted + full discovery gates to completion per campaign step 8 and record actual EXIT.
- **Prior heavy verification (unchanged, `session_20261117T072040Z`):** design-frontier certificate `BLOCKED_ON_DESIGN`/`promotable=false` (full-C2 0 blocks/no ≥127d; mark+funding-only 4 individually feasible, 2 mutually non-overlapping 2024-10/2025-01, 5 pairs); replication robustness qualitative 7/7 Wilson95 [0.646,1.000], LOO 6/6 all-unity, sign mixed 3+/4-; FCLR-014 verdict reproduced. Artifact refs unchanged.
- **Canonical tool state:** `scripts/next_campaign_status.py` exposes `markfund_frontier` (4 individually feasible / 2 mutually non-overlapping / 5 overlapping pairs), matching certified closure. No tool change made.
- **Evidence audit (carried forward, not rerun):** `session_20261116T100533Z/`, `125624Z/`, `185811Z/`, `230140Z/`, `20261117T000400Z/`, `002014Z/`, `031656Z/`, `071110Z/`, `072040Z/`.
- **Campaign state:** Programme remains `CLOSED_TERMINAL`/trigger-gated; blockers unchanged (external triggers OPEN + cached-data design-admissibility certified). **`FCLR-FRONTIER-VERIFY-06-20261117T130551Z` active** — no session may close without a new quantitative frontier-audit artifact + evidence audit + gate/suite captures (or a trigger-satisfied §16-compliant preregistered path). "No trigger → stop cleanly" is **not** completion.
- **Git tree:** tracked changes this pass: `AGENT_HANDOFF.md` updated; removed phantom `research_state/session_20261117T060853Z/`. No sealed artifacts modified. No root-level `research_state/*.md|json` added (500/500 cap).

---

**This handoff is the single durable artifact for the next session. Execute the INITIAL TASK MESSAGE above. Do not create additional handoff files. Update only `AGENT_HANDOFF.md` after completion.**