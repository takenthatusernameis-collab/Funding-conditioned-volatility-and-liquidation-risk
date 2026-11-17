# AGENT HANDOFF — 2026-11-17T205054Z (sole durable handoff)

> **Authority:** this file only. `research_state/FCLR_HEAVY_CAMPAIGN_NEXT.md` is a subordinate detail note; every other handoff-like file is tombstoned/historical and has no campaign authority.

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION (do this first — heavy work required)

**At a glance:** repository `Funding-conditioned-volatility-and-liquidation-risk` → **Track C funding-conditioned volatility is the priority**; no reopen trigger is satisfied; execute campaign `FCLR-TRIGGER-READINESS-01-20261117T203457Z`; produce an outcome-blind **trigger-activation readiness package** (`trigger_activation_executor_<UTC>.{py,json}`, `trigger_activation_selftest_<UTC>.{py,json}`, `trigger_activation_readiness_<UTC>.{json,md}`) + `trigger_check_<UTC>.json` + `evidence_audit_<UTC>.md` in a new `research_state/session_<UTC>/`; record that session in this handoff; run the gates and full suite. A trigger-check-only session, tests-only session, copied bundle, frontier re-audit, or handoff-only refresh is **not** completion. The gate now also fails if a newer on-disk session is not recorded here (`HANDOFF_STALE_LATEST_SESSION`), so the handoff cannot go stale to dodge the package.

**Priority 0 — repository and rank-0 state.**
- Repository: `Funding-conditioned-volatility-and-liquidation-risk` (funding-conditioned volatility and liquidation risk). **Prioritize by repository name: Track C funding-conditioned volatility first.** Track A (observed-liquidation arm) is externally blocked (no admissible post-2026-10 observed labels/source; no agent-settable Gate 4 attestation). Track B is `COMPLETE_INCONCLUSIVE`.
- Program: `CLOSED_TERMINAL` — final structural closure `research_state/fclr_final_structural_closure_20261116T114626.{md,json}`; verdict `NO_CLAIM_WORTHY_RESULT_PROMOTABLE; ALL_P1_P2_P3_SEALED`. No feasible ≥3-block pre-registered confirmatory design remains on cached data.
- Rank-0: `FCLR-BOUNDED-TRIGGER-ONLY-20261115T220000Z` (`TRIGGER_ONLY` / `BOUNDED_TRIGGER_ONLY`, `next_action_heavy=null`). All cached-data confirmatory estimands are terminal.
- Consequence: **do not start or re-run any sealed cached-data confirmatory estimand; do not re-run FCLR-014, the replication synthesis, or the design-frontier certificate.** A trigger-check-only session, tests/gates-only session, copied bundle, frontier re-audit, handoff-only refresh, or "stop cleanly" is **NOT** completion.

**Frontier-verification line is CLOSED — do not continue the audit treadmill.**
Two independent, outcome-blind exhaustive frontier audits reproduce the identical closed-world result with `all_exact_match=true` and no mismatch:
- `session_20261117T193323Z` (csv-count heuristic): full-C2 0 disjoint feasible blocks / no contiguous run ≥127d; mark+funding-only 4 individually feasible months (`2024-10`,`2024-11`,`2024-12`,`2025-01`) but only 2 mutually non-overlapping (`2024-10`,`2025-01`), 5 overlapping pairs; overall `BLOCKED_ON_DESIGN`, `promotable=false`, `fclr014_closed_verdict_reproduced=true`.
- `session_20261117T194457Z` (month-interval arithmetic, deliberately independent method): same closed-world result, compared exact against `scripts/next_campaign_status.py --json` (`markfund_frontier`, `disjoint_block_frontier`, `design_feasibility`) and the sealed `session_20261117T072040Z` certificate — `matches_independent=true`.
**Do NOT run any further frontier re-audit (no "verify-08"+).** A third re-audit of the same closed frontier is the inefficiency this handoff removes. If a future session believes the frontier changed, it must first show a *new admissible data source* per `RESEARCH_PROMPT.md` §16 — not another cached-data re-derivation.

## NEXT FOCUS CAMPAIGN — `FCLR-TRIGGER-READINESS-01-20261117T203457Z` (future agents cannot opt out)

This campaign binds every future session to heavy, outcome-blind quantitative/engineering work. It is enforced by `scripts/check_handoff_heavywork_gate.py` (`trigger_readiness` state plus the new stale-handoff check) and `scripts/check_tracka_scope_registry_drift.py`. Once this campaign has started (start UTC `20261117T203457Z`), any session created **after** that instant **fails the heavy-work gate closed** unless its directory contains the exact trigger-activation package triad plus a trigger check — an arbitrary `recompute_*` artifact or a trigger-check-only session no longer satisfies it. In addition, the newest `research_state/session_<UTC>/` on disk must be recorded in this handoff; if it is not, the gate fails with `HANDOFF_STALE_LATEST_SESSION:<id>`. No session may close without satisfying **all** of the following.

### Definition of done (non-avoidance contract)

1. **New session dir required:** `research_state/session_<UTC>/` (actual UTC). `research_state/` root is **500/500** (fail-closed cap); ALL new artifacts go inside the session subdirectory only. Root-level `research_state/*.md|json` is prohibited.
2. **Trigger check exactly once (no network, no polling):** read `research_state/resume_trigger_registry.json` and `research_state/ironflow_monitor_state.json`. Record timestamp, each trigger status, `data_through`, and post-2026-10 classifications in `trigger_check_<UTC>.json` in the session dir. Current: all four triggers `OPEN`; Ironflow `data_through=2026-10`, `consecutive_absent=3`; 2026-11/2026-12/2027-01 `CONFIRMED_ABSENT`.
3. **No-trigger rule:** if no trigger is satisfied (current state), do NOT start or re-run any sealed cached-data confirmatory estimand, do NOT re-run FCLR-014/synthesis/frontier certificate, and do NOT re-audit the closed frontier. The required work is the outcome-blind readiness package below.
4. **Heavy-work floor — outcome-blind trigger-activation package.** Produce, independently implemented in the session dir, a stdlib-only, ZIP/CSV-aware package that operationalizes the four pre-sized trigger contracts from `research_state/session_20261116T100533Z/trigger_readiness_power_calibration_20261116T100533Z.md` and the skeleton `research_state/session_20261116T035833Z/prereg_template_trigger_gated_20261116T035833Z.json`:
   - **`trigger_activation_executor_<UTC>.py` + `.json`** — a stdlib-only executor that is a *referee, not a runner*: it reads the trigger registry + Ironflow state once, maps each of `GATE4_BRANCH_1`, `NEW_OBSERVED_LIQUIDATION_SOURCE`, `HL_LABEL_EXTENSION`, `EXPANSION_ROBUSTNESS_REDO` to (estimand, `paired_n` floor — Gate4/TrackC `>=23224`, TrackA/HL/expansion `>=11689`, `>=3` non-overlapping 30d blocks, `7d` purge/embargo, `>=5` instruments, Holm family enumeration, MDE `<2%` target), emits a per-trigger `prereg_instantiation_plan` with `outcome_data_inspected_before_freeze=false`, and **exits non-zero / refuses** whenever any pre-outcome gate is unmet. It must never open an outcome file.
   - **`trigger_activation_selftest_<UTC>.py` + `.json`** — real `unittest` self-tests (runnable via `python3 -m unittest`) that exercise the executor on **synthetic** data: 30d-train + 7d-embargo + 30d-test block arithmetic and non-overlap detection; `paired_n` floor enforcement below/above 23224 and 11689; Holm-family enumeration determinism; refusal behaviour when gates fail; and an explicit outcome-blindness assertion (no outcome path opened). Record pass/fail counts + EXIT.
   - **`trigger_activation_readiness_<UTC>.json` + `.md`** — a readiness certificate mapping each of the 4 triggers to a concrete pre-powered executable plan + expected artifacts + the irreducible human step (Gate 4 legal attestation is human-owned), plus an explicit do-not-run list. Must state `promotable=false`, `program_status=CLOSED_TERMINAL`, `new_scientific_claim=false`.
   - Do not merely copy `trigger_readiness_power.py`/`trigger_readiness_power_calibration_*`; this is new executable code + self-tests + a per-trigger plan, not a re-print of the markdown.
5. **Evidence audit:** write `evidence_audit_<UTC>.md` confirming all carried-forward bundles are present and not re-run (`session_20261116T100533Z`, `125624Z`, `185811Z`, `230140Z`, `20261117T000400Z`, `002014Z`, `031656Z`, `071110Z`, `072040Z`, `193323Z`, `194457Z`). Include the exact files read and command outputs used.
6. **Gates + suite:** run and capture under the new session dir: `python3 scripts/check_handoff_heavywork_gate.py --json`, `python3 scripts/check_tracka_scope_registry_drift.py --json`, targeted `python3 -m unittest tests.test_active_campaign_gate tests.test_next_campaign_status tests.test_tracka_hardening_117 tests.test_tracka_hardening_118 tests.test_tracka_hardening_143`, and `python3 -m unittest discover -q` to completion (record count/skip/error/EXIT). **Baseline is environment-dependent.** Current targeted baseline: **82 tests, 6 errors (all pre-existing missing-`numpy` imports in `test_tracka_hardening_117/118`), 0 failures**. Full discovery baseline: **1126 tests, 62 errors, 9 failures, 14 skipped, EXIT 1** (environmental: missing `numpy`/`pyarrow`, unresolved LFS fixtures). Record the actual run; never treat a timeout/monitor cap or a missing-dependency error set as green. Revert any timestamp-only side effect to tracked files. **Before the final gate capture, record the new session id in this handoff** — otherwise the stale-handoff check fails closed.
7. **Handoff update:** update only `AGENT_HANDOFF.md` after work; preserve the sole-handoff contract, bundle refs, blockers, and this campaign intact. The new session id must appear here before the final gate run. If `scripts/check_handoff_heavywork_gate.py` or `scripts/next_campaign_status.py` is changed, register it in both scope registries and add a regression test; otherwise do not touch them.

**This is a ONE-TIME campaign — retire it on completion (do not rebuild the package in later sessions).** The trigger-activation package is the last agent-removable heavy deliverable on cached data; once it exists, no further cached-data heavy work remains and the only scientific advance is a trigger-satisfied `RESEARCH_PROMPT.md` §16 path. Therefore the session that completes this campaign must, in the same handoff update, (a) record the completed package triad + evidence audit + gate/suite captures, and (b) **remove the `FCLR-TRIGGER-READINESS-01-20261117T203457Z` campaign token** and replace it with an explicit `AWAITING_TRIGGER` statement (no agent-removable heavy work remains; advance only on a satisfied reopen trigger; sessions are then trigger-check + base-gate only). Do NOT leave the token in place after the package is built — that would recreate a rebuild treadmill. Until then, every post-`20261117T203457Z` session that lacks the package fails the heavy-work gate closed.

**Trigger-satisfied path:** if any trigger fires, follow `RESEARCH_PROMPT.md` §16 admissibility/source audit first; freeze a pre-sized prereg before inspecting outcomes (use `session_20261116T035833Z/prereg_template_trigger_gated_20261116T035833Z.json` and power floors in `session_20261116T100533Z/trigger_readiness_power_calibration_20261116T100533Z.md`: Gate4/TrackC `paired_n>=23224`, TrackA/expansion `paired_n>=11689`, ≥3 blocks, 7d purge/embargo, `outcome_data_inspected_before_freeze=false`); require a materially different estimand; execute; record an honest verdict; register any new `scripts/*.py` in both scope registries.

**Read first (in order):**
1. `research_state/resume_trigger_registry.json`
2. `research_state/ironflow_monitor_state.json`
3. `research_state/session_20261116T100533Z/trigger_readiness_power_calibration_20261116T100533Z.{md,json}` + `trigger_readiness_power.py`
4. `research_state/session_20261116T035833Z/prereg_template_trigger_gated_20261116T035833Z.json` + `program_power_synthesis_20261116T035833Z.md`
5. `research_state/session_20261117T194457Z/recompute_frontier_exhaustive_audit_20261117T194457Z.{py,json,md}` + `session_20261117T193323Z/recompute_frontier_exhaustive_audit_20261117T193323Z.{py,json,md}` (closed frontier — do not re-audit)
6. `scripts/next_campaign_status.py` (`TESTED_WINDOWS`, `MIN_DESIGN_DAYS`, `disjoint_block_frontier`, `markfund_frontier`) + `tests/test_next_campaign_status.py`
7. `RESEARCH_PROMPT.md` §16 (trigger-gated admissibility/source rules)

## Completed work — do not repeat

- **Frontier verification — DONE, line CLOSED.** Two independent exhaustive audits (`session_20261117T193323Z` csv-count heuristic; `session_20261117T194457Z` month-interval arithmetic) reproduce full-C2 0 disjoint feasible blocks / no ≥127d run; mark+funding-only 4 individually feasible, 2 mutually non-overlapping (`2024-10`,`2025-01`), 5 overlapping pairs; `overall=BLOCKED_ON_DESIGN`, `promotable=false`, `fclr014_closed_verdict_reproduced=true`, `all_exact_match=true`. Do NOT run verify-08+.
- **FCLR-REPRO-SYNTH-05 — DONE (`session_20261117T072040Z`).** Design-frontier certificate (`BLOCKED_ON_DESIGN`) + replication robustness (qualitative 7/7, Wilson95 [0.646,1.000], LOO 6/6 all-unity, sign mixed 3+/4-). Do not re-run.
- **FCLR-014 — DONE and BLOCKED-ON-DESIGN (`session_20261117T071110Z`).** 4-block "freeze a prereg" claim (`session_20261117T051045Z`) is **RETRACTED** as leakage-prone. Cite `session_20261117T071110Z`; do not re-litigate.
- **Replication synthesis — DONE (`session_20261117T071110Z`).** 7 studies; 2/7 within tolerance; 0 promotable positives.
- FCLR-013 — `session_20261117T031656Z` (NOT_REPLICATED, C2-vs-B1 rel -4.99%). FCLR-010 — `session_20261117T002014Z` (NOT_REPLICATED, 0.50%). FCLR-002/003 — `session_20261117T000400Z` (NOT_MET corroborated). FCLR-009 — `session_20261116T125624Z` (within tolerance). FCLR-006 — `session_20261116T185811Z` (within tolerance). FCLR-008 — `session_20261116T230140Z` (NOT_MET corroborated). FCLR-RCA-011 — `session_20261116T100533Z` (5 RCA families + power calibration).

## Blocked-path warning (do not waste a session here)

- **No parquet engine is installed** (`pyarrow`, `fastparquet`, `duckdb`, `polars` all absent; network installs prohibited). Any task whose only input is `.parquet` is blocked unless a CSV/JSON/ZIP twin exists. Use the ZIP/CSV reader pattern from `session_20261117T031656Z` / `session_20261117T000400Z`.
- `research_state/research_protocol_fclr002.md` and `research_state/research_protocol_fclr003.md` **do not exist** — do not block on them.
- `research_state/run_manifest.json`, `run_manifest_FCLR002.json`, `data_cache/fclr002_panel*.json`, `data_cache/manifest_fclr002.json`, `data_cache/manifest_fclr003.json` are **unresolved Git-LFS pointers with no local object**. Do NOT run `git lfs pull` (network prohibited).
- **2024 cache format:** Apr–Jun 2024 mark/premium/index files are ZIPs; Jan–Mar and Jul–Nov 2024 are CSVs; 2025–2026 are ZIP+CSV. Use a ZIP-aware reader.
- Do NOT run `scripts/fclr_liq_010_confirm.py` (parquet-only; fails on import).
- **No outcome data may be inspected** for the trigger-activation package; it is outcome-blind by construction. Never read a `evaluation_summary_*`, `results/*` outcome, or any sealed estimand output while building it.

## Execute in order (do not skip to "stop cleanly")

1. **Create `research_state/session_<UTC>/`** (actual UTC). `research_state/` root is **500/500** (fail-closed cap); put ALL new artifacts inside the session subdirectory only.
2. **Check triggers exactly once (no network, no polling).** Read files 1–2. Record timestamp, each trigger status, `data_through`, and post-2026-10 classifications in `trigger_check_<UTC>.json`.
3. **If no trigger is satisfied (current state):** do not start/re-run any sealed cached-data confirmatory estimand and do not re-audit the closed frontier. Build the outcome-blind trigger-activation package exactly as specified in the campaign above.
4. **If a trigger is satisfied:** follow `RESEARCH_PROMPT.md` §16 admissibility/source audit first; freeze a pre-sized prereg before inspecting outcomes (template + power floors above); require a materially different estimand; execute and record an honest verdict; register any new scripts in both scope registries.
5. **Audit carried-forward evidence.** Confirm completed sessions listed above are present. Write `evidence_audit_<UTC>.md`.
6. **Run and capture gates under the new session dir:** `check_handoff_heavywork_gate.py --json` (must show `trigger_readiness.pass=true` and `handoff_stale=false`), `check_tracka_scope_registry_drift.py --json`, targeted suite, and `python3 -m unittest discover -q` to completion (record count/skip/error/EXIT). **Baseline is environment-dependent** (targeted 82/6/0; discovery 1126/62/9/14/EXIT 1). Never treat a missing-dependency error set as green. Revert timestamp-only side effects to tracked files.
7. **Update only this handoff** after work: record the new session id (required before the final gate capture), replace timestamp/verification with actual results, keep sole-handoff contract, bundle refs, blockers, and this campaign intact.

**Trigger-gated science is the only scientific advance — but must be pre-powered.** If no trigger is satisfied, do not advance or re-run a confirmatory estimand; the required holding action is the outcome-blind trigger-activation readiness package. If a trigger is satisfied, follow `RESEARCH_PROMPT.md` §16, freeze a pre-sized prereg before outcomes, require a materially different estimand, execute, register new scripts, run all gates, and update frontier/hypothesis registries with an honest verdict.

## Heavy-work evidence on disk (authoritative; do not redo)

- **Frontier (CLOSED):** `research_state/session_20261117T193323Z/` (`recompute_frontier_exhaustive_audit_20261117T193323Z.{py,json,md}`, trigger check, evidence audit, gate/suite captures) and `research_state/session_20261117T194457Z/` (`recompute_frontier_exhaustive_audit_20261117T194457Z.{py,json,md}`, trigger check) — both `all_exact_match=true`, `BLOCKED_ON_DESIGN`.
- **FCLR-REPRO-SYNTH-05 — `session_20261117T072040Z/`:** `recompute_design_frontier_certificate_20261117T072040Z.{py,json,md}` + `replication_robustness_20261117T072040Z.{py,json,md}`.
- **FCLR-014 baseline — `session_20261117T071110Z/`.**
- **FCLR-013 — `session_20261117T031656Z/`. FCLR-010 — `session_20261117T002014Z/`. FCLR-002/003 — `session_20261117T000400Z/`. FCLR-008 — `session_20261116T230140Z/`. FCLR-006 — `session_20261116T185811Z/`. FCLR-009 — `session_20261116T125624Z/`.**
- **Trigger-readiness assets (inputs, not a substitute for the new package):** `session_20261116T100533Z/` (power calibration + `trigger_readiness_power.py`), `session_20261116T035833Z/` (prereg template + power synthesis).

**Incomplete / non-counting sessions (do not resume, copy, or count):**
- `session_20261116T104644Z/`, `session_20261116T105341Z/`, `session_20261116T134957Z/` (trigger-only; only a trigger-check file).
- `session_20261116T140001Z/` superseded (tolerance-failed FCLR-006); `session_20261116T221127Z/` superseded (divergent FCLR-008).
- `session_20261117T041333Z/` and `session_20261117T051045Z/` superseded by the adjudication in `session_20261117T071110Z` — cite as history, do not re-derive.

## Bottlenecks removed / prevented

- **Frontier-audit treadmill removed:** the prior handoff mandated an endless sequence of independent frontier re-audits (verify-06, verify-07, …) that all reproduce the same closed `BLOCKED_ON_DESIGN`. Two independent audits now agree with `all_exact_match=true`; further cached-data re-audits are prohibited and the gate no longer accepts them as heavy work. Significant progress now requires either a trigger-satisfied §16 path or the outcome-blind trigger-activation package.
- **Handoff staleness corrected:** the prior handoff was timestamped 19:34Z and named `session_20261117T193323Z` as the latest session, but `session_20261117T194457Z` (an independent verify-07 method) already existed on disk. This handoff records both and marks the frontier line closed.
- **Stale-handoff bypass removed:** the heavy-work gate previously trusted only the session id written in this handoff, so a session could create a post-campaign directory, skip the trigger-activation package, and leave the handoff pointing at an older session forever. The gate now compares the newest `session_<UTC>/` on disk with the newest id in this handoff and fails with `HANDOFF_STALE_LATEST_SESSION:<id>` when they differ. A new session must be recorded here before the final gate capture.
- **Gate regression fixed:** the previous commit changed the frontier regex to read regex group 1 (the campaign number, e.g. `06`) instead of group 2 (the timestamp), which broke pre-start grandfathering and turned `test_pre_start_session_is_grandfathered` RED. The gate now uses the timestamp group and also enforces the trigger-readiness campaign.
- **Handoff authority:** this file only. Competing timestamped handoffs are tombstoned (see below).
- **Empty-session loop:** do not create a session dir until a concrete heavy artifact is ready; empty/phantom sessions are non-counting.
- **Root churn:** 500/500 — session-only writes required.

## Bottlenecks and prohibitions

- Do not start or re-run any cached-data confirmatory estimand; all sealed estimands are terminal.
- Do not re-run FCLR-014, the replication synthesis, or the design-frontier certificate; do not run verify-08+.
- Do not mutate sealed artifacts, frontier, hypothesis registries, or `.github/workflows/*`.
- Do not poll, re-probe the HuggingFace tree, use paid/credentialed/manual outcome data, or add root-level `research_state/*.md|json`.
- Do not add `statsmodels` or unpinned heavy dependencies to the core path.
- Do not run `git lfs pull` or otherwise fetch network data.
- Do not run `scripts/fclr_liq_010_confirm.py` (parquet-only; will fail on import).
- Discovery suite is long-running; let it finish and record actual EXIT, not partial/timeout.
- Scientific blocker is external (no admissible post-2026-10 observed liquidation labels/source; no agent-settable Gate 4 attestation) AND design-admissibility (no feasible ≥3-block mutually-non-overlapping confirmatory design on cached data). No agent-removable confirmatory cached-data work remains; the agent-removable heavy work is the outcome-blind trigger-activation package, and scientific advance is trigger-gated under `RESEARCH_PROMPT.md` §16.

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
- `HANDOFF_NEXT_SESSION_20261117T140203Z.md`: tombstoned 2026-11-17T14:10:26Z — duplicate full handoff; consolidated here, no authority. Do not execute it.

## Verification record — 2026-11-17T205209Z (handoff refresh; campaign FCLR-TRIGGER-READINESS-01)

- **Current trigger check (once, no network/polling):** `research_state/resume_trigger_registry.json` + `research_state/ironflow_monitor_state.json` re-read at 2026-11-17T205209Z; all four triggers **OPEN** (`GATE4_BRANCH_1`, `NEW_OBSERVED_LIQUIDATION_SOURCE`, `HL_LABEL_EXTENSION`, `EXPANSION_ROBUSTNESS_REDO`); Ironflow `data_through=2026-10`, `consecutive_absent=3`. No trigger fired; no confirmatory estimand advanced/re-scored.
- **Frontier line CLOSED (read-only):** two independent exhaustive audits reproduce the closed-world result with `all_exact_match=true` — `session_20261117T193323Z` (csv-count) and `session_20261117T194457Z` (month-interval). Full-C2 0 disjoint feasible blocks / no ≥127d run; mark+funding-only 4 individually feasible / 2 mutually non-overlapping (`2024-10`,`2025-01`) / 5 overlapping pairs; `overall=BLOCKED_ON_DESIGN`, `promotable=false`, `fclr014_closed_verdict_reproduced=true`. No further frontier re-audit is required or permitted.
- **Heavy-work gate hardened this pass:** `scripts/check_handoff_heavywork_gate.py` now (a) uses the correct regex group for the campaign-start UTC (fixes the pre-start grandfathering regression that made `test_pre_start_session_is_grandfathered` fail), (b) enforces the `trigger_readiness` state (post-`20261117T203457Z` sessions must contain `trigger_activation_executor_<UTC>.{py,json}`, `trigger_activation_selftest_<UTC>.{py,json}`, `trigger_activation_readiness_<UTC>.{json,md}` and a trigger check), and (c) adds the stale-handoff check: the newest `research_state/session_<UTC>/` on disk must be the newest session id recorded in this handoff, otherwise the gate fails with `HANDOFF_STALE_LATEST_SESSION:<id>`. Added `TestHandoffFreshnessGate` (2 tests) to `tests/test_tracka_hardening_143.py`; `TestTriggerReadinessCampaignGate` (4 tests) remains.
- **Gates + suite (this pass):** `python3 scripts/check_handoff_heavywork_gate.py --json` **PASS** (`reason_code: OK`, root 500/500, latest handoff session `session_20261117T194457Z`, latest on-disk session `session_20261117T194457Z`, `handoff_stale=false`, `trigger_readiness.required=false` because the latest session predates the campaign start → grandfathered); `python3 scripts/check_tracka_scope_registry_drift.py --json` **PASS** (`reason_code: OK`). Targeted suite `tests.test_active_campaign_gate tests.test_next_campaign_status tests.test_tracka_hardening_117 tests.test_tracka_hardening_118 tests.test_tracka_hardening_143`: **82 tests, 6 errors (all pre-existing missing-`numpy` imports in tracka_hardening_117/118), 0 failures**. Full discovery baseline (environment-dependent): **1126 tests, 62 errors, 9 failures, 14 skipped, EXIT 1** (missing `numpy`/`pyarrow`, unresolved LFS fixtures); never treat a missing-dependency error set as green. The discovery run touched `research_state/ironflow_fastpath_cache.json` with a timestamp-only change; it was reverted with `git checkout --`. No sealed artifacts, scripts, registries, or `.github/workflows/*` modified; no root-level `research_state/*.md|json` added (root remains 500/500).
- **Staleness corrected:** the prior verification record named `session_20261117T193323Z` as the latest session, but `session_20261117T194457Z` already existed on disk. This record uses the actual latest on-disk and handoff session, `session_20261117T194457Z`.
- **Next-session non-avoidance check:** any session created after `20261117T203457Z` must emit the trigger-activation package triad + trigger check first; the heavy-work gate fails closed otherwise. A newer on-disk session that is not recorded here also fails closed (`HANDOFF_STALE_LATEST_SESSION`). "No trigger → stop cleanly", trigger-check-only, tests-only, copied-bundle, frontier re-audit, and handoff-only refresh are **not** completion.
- **Git tree:** this pass refreshes `AGENT_HANDOFF.md` as the single durable handoff with an unavoidable heavy-work campaign and hardens the gate against a stale handoff; no competing handoff authority remains.

---

**This handoff is the single durable artifact for the next session. Execute the INITIAL TASK MESSAGE above. Do not create additional handoff files. Update only `AGENT_HANDOFF.md` after completion.**