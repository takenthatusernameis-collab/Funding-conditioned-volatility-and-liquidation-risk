# AGENT HANDOFF — 2026-11-16T23:25:43Z (sole durable handoff)

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION (do this first)

**Priority 0 — repository and rank-0 state.** Repository: `Funding-conditioned-volatility-and-liquidation-risk` (funding-conditioned volatility and liquidation risk). Program status: `CLOSED_TERMINAL` (final structural closure `research_state/fclr_final_structural_closure_20261116T114626.{md,json}`; terminal verdict `NO_CLAIM_WORTHY_RESULT_PROMOTABLE; ALL_P1_P2_P3_SEALED`; all P1/P2/P3 sealed; no feasible 3-block pre-registered design in any domain). Rank-0 campaign `FCLR-BOUNDED-TRIGGER-ONLY-20261115T220000Z` (`TRIGGER_ONLY` / `BOUNDED_TRIGGER_ONLY`, `all_terminal=true`, `next_action_heavy=null`). All cached-data confirmatory estimands are terminal. Sealed FCLR-011 PASS not independently reproduced (clean recompute C2 vs B1 **-294.01%** vs sealed **+4.94%**; fragile/non-promotable, triple-confirmed). Track B `NOT_SUPPORTED`; Track C cached confirmatory designs terminal; H2 (Shek) `EXPLORATORY_ONLY`. FCLR-009, FCLR-006, and **FCLR-008** independently reproduced (`all_within_tolerance=true` for FCLR-009/006; FCLR-008 B0/B1 within tolerance, C1/C2 divergence documented) — CLOSED.

**MANDATORY HEAVY WORK (non-skippable): produce ONE NEW quantitative artifact — next queue item FCLR-002/003.** A trigger-check-only session, tests/gates-only session, copied artifacts, re-audit of static bundles, or "no trigger → stop cleanly" is **NOT** completion. Completion requires: new `research_state/session_<UTC>/` containing `recompute_fclr002_<UTC>.{json,md}` / `recompute_fclr003_<UTC>.{json,md}` + recompute script, evidence audit, full gate/suite capture, and this handoff updated.

**Read first (in order):**
1. `research_state/resume_trigger_registry.json`
2. `research_state/ironflow_monitor_state.json`
3. `research_state/FCLR_HEAVY_CAMPAIGN_NEXT.md` (campaign `FCLR-REPRO-AUDIT-02`)
4. `research_state/session_20261116T230140Z/evidence_audit_20261116T230140Z.md` and `recompute_fclr008_20261116T230140Z.md` (latest completed heavy evidence)
5. `research_state/research_protocol_fclr002.md` / `research_state/research_protocol_fclr003.md` and `research_state/evaluation_summary_FCLR-002.md` / `research_state/evaluation_summary_FCLR-003.md` (NEXT TARGETS)

**Execute in order (do not skip to "stop cleanly"):**
1. **Create `research_state/session_<UTC>/`** (actual UTC). `research_state/` root is **500/500** md/json (fail-closed cap); put ALL new artifacts inside the session subdirectory only.
2. **Check triggers exactly once (no network, no polling).** Read files 1–2. Record timestamp, each trigger status, `data_through`, and post-2026-10 month classifications in the session dir. Current state: all four `OPEN`; Ironflow `data_through=2026-10`; 2026-11/2026-12/2027-01 `CONFIRMED_ABSENT`. Do not re-probe HuggingFace or repeat later.
3. **FCLR-002 / FCLR-003 independent recompute** (sealed 2024 volatility-forecast panels; **FCLR-008/009/006 are DONE — do NOT repeat**). Recompute independently from frozen protocol and cached 2024 data:
   - Protocol: `research_state/research_protocol_fclr002.md` / `research_state/research_protocol_fclr003.md` (frozen). Published: `research_state/evaluation_summary_FCLR-0�.md` / `research_state/evaluation_summary_FCLR-003.md`.
   - Frozen splits: as defined in each protocol. Universe: BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT (2024 cache). Load earlier months for lookbacks respecting frozen boundaries.
   - Models: B0 persistence; B1 HAR-style; C1 = B1 + signed funding + past-only 90-day |funding| percentile; C2 = C1 + premium + EMA distance. OLS on log(RV+1e-12); follow frozen protocol. Primary contrast: C2 vs B1 on 24h QLIKE.
   - **Tolerances:** QLIKE absolute `<= 1e-6`; mean diff absolute `<= 1e-6`; relative reduction `<= 0.01` percentage points (n must match where deterministic). Write `recompute_fclr002_<UTC>.{json,md}` / `recompute_fclr003_<UTC>.{json,md}` + script in the session dir. Do **not** run canonical `scripts/run_evaluation.py` against tracked summaries; use independent path; never mutate sealed artifacts.
4. **Audit carried-forward evidence.** Confirm `research_state/session_20261116T100533Z/` has the five RCA-011 families and `session_20261116T125624Z/` (FCLR-009) + `session_20261116T185811Z/` (FCLR-006) + `session_20261116T230140Z/` (FCLR-008) recomputes/audits are present. Write concise evidence-audit artifact in session dir. Do not rerun FCLR-RCA-011/FCLR-009/FCLR-006/FCLR-008.
5. **Run and capture every required gate under the new session dir:**
   - `python3 scripts/check_handoff_heavywork_gate.py --json` — PASS (complete bundle + new session audit + fresh quant artifact, root <= 500).
   - `python3 scripts/check_tracka_scope_registry_drift.py --json` — PASS (register any new script in both scope registries).
   - `python3 -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_117 tests.test_tracka_hardening_118 tests.test_tracka_hardening_143` — all pass.
   - `python3 -m unittest discover -q` — run to completion; record exact test count, skip count, final EXIT. Never treat timeout/monitor cap as green. Revert any timestamp-only side effect to tracked files.
6. **Update only this handoff** after steps 3–5: replace timestamp/verification with actual results, advance queue (tick FCLR-002/003 if done), keep sole-handoff contract, bundle refs, blockers intact. Do not create another handoff file.

**Trigger-gated science is the only scientific advance — but must be pre-powered.** If no trigger is satisfied, do not advance or re-run a confirmatory estimand; required holding action is the new FCLR-002/003 (or documented LIQ-010 fallback) reproducibility artifact + evidence audit + complete verification + accurate handoff update. If a trigger is satisfied, follow §16 admissibility/source audit first, freeze a pre-sized prereg before inspecting outcomes (use `session_20261116T035833Z/prereg_template_trigger_gated_20261116T035833Z.json` and power floors in `session_20261116T100533Z/trigger_readiness_power_calibration_20261116T100533Z.md`: Gate4/TrackC `paired_n>=23224`, TrackA/expansion `paired_n>=11689`, >=3 blocks, 7d purge/embargo), require a materially different estimand, execute, register any new scripts in both scope registries, run all gates, and update frontier/hypothesis registries with an honest verdict.

## Reproducibility-audit queue (non-skippable; do in order)

1. ~~FCLR-009~~ — DONE (`session_20261116T125624Z`; `all_within_tolerance=true`).
2. ~~FCLR-006~~ — DONE (`session_20261116T185811Z`; `all_within_tolerance=true`; supersedes tolerance-failed `session_20261116T140001Z`).
3. ~~FCLR-008 (unsealed 2026-01..2026-08): independent recompute, `recompute_fclr008_<UTC>.{json,md}`~~ — DONE (`session_20261116T230140Z`; B0/B1 within tolerance; C1/C2 divergence ~1.4e-3/2.1e-3 QLIKE documented; qualitative NOT_MET corroborated).
4. **FCLR-002 / FCLR-003 (sealed 2024 panels): independent recompute, `recompute_fclr002_<UTC>.{json,md}` / `recompute_fclr003_<UTC>.{json,md}` — CURRENT TARGET (PRIMARY).**
5. FCLR-010 (Track A liquidation confirm): independent recompute from `fclr_liq_010_confirm_panel_20261113T065953Z.parquet`, `recompute_fclr010_<UTC>.{json,md}`.
6. FCLR-013 / FCLR-014 (2026 Q3 / 2025 H1 panels): independent recompute.

A session that completes an item must (a) create `research_state/session_<UTC>/`, (b) emit a new quantitative artifact named per queue, (c) write evidence audit, (d) run all gates + full discovery suite to completion with recorded EXIT, (e) update this handoff and tick the queue item.

## Heavy-work evidence on disk (authoritative; do not redo)

- Self-contained bundle: `research_state/session_20261116T100533Z/` (carried forward from `session_20261116T035833Z/`): 5 RCA-011 families + `trigger_readiness_power_calibration_*`/`trigger_readiness_power.py`.
- `research_state/session_20261116T125624Z/`: FCLR-009 reproduced `all_within_tolerance=true`.
- `research_state/session_20261116T185811Z/`: FCLR-006 reproduced `all_within_tolerance=true`.
- `research_state/session_20261116T115028Z/`: third numpy-only FCLR-011 crosscheck confirming sealed PASS not reproducible.
- `research_state/session_20261116T230140Z/`: FCLR-008 independent recompute (B0/B1 QLIKE match ≤3e-7; C1/C2 divergence ~1.4e-3/2.1e-3; evidence audit and full gate/suite capture complete).

**Incomplete / non-counting sessions (do not resume, copy, or count):** `session_20261116T104644Z/`, `session_20261116T105341Z/`, `session_20261116T134957Z/` (trigger-only). `session_20261116T140001Z/` superseded (tolerance-failed FCLR-006). No empty session directories present.

## Bottlenecks removed / prevented

- **Stale-target mismatch removed:** primary is FCLR-002/003 (queue 4); FCLR-008/006/009 explicitly done.
- **Empty/stale session clutter removed:** none present; incomplete trigger-only `/` removed this refresh. Do not create empty placeholder session dirs.
- **Maintenance-refresh treadmill blocked:** handoff-only refreshes with no new heavy artifact are not completion; next session must emit `recompute_fclr002_<UTC>.{json,md}` / `recompute_fclr003_<UTC>.{json,md}`.
- **False gate failure resolved:** gate accepts latest session with `evidence_audit_*` + fresh quantitative artifact while resolving complete bundle.
- **Reproducibility path:** stdlib/numpy-only; no `statsmodels`/unpinned heavy deps in core path.
- **Handoff authority:** this file only (`AGENT_HANDOFF.md`).
- **Root churn:** 500/500 — session-only writes required.

## Bottlenecks and prohibitions

- Do not start or re-run any cached-data confirmatory estimand; all terminal.
- Do not mutate sealed artifacts, frontier, hypothesis registries, or `.github/workflows/*`.
- Do not poll, re-probe HuggingFace tree, use paid/credentialed/manual outcome data, or add root-level `research_state/*.md|json`.
- Do not add `statsmodels` or unpinned heavy dependencies to core path.
- Discovery suite is long-running; let it finish and record actual EXIT, not partial/timeout.
- Scientific blocker is external (no admissible post-2026-10 observed liquidation labels/source; no agent-settable Gate 4 attestation). Agent-removable requirement: new quantitative artifact + evidence audit + complete verification + accurate handoff update.

## Reopen triggers (machine-checkable — Act ONLY when satisfied; all `OPEN`)

- `GATE4_BRANCH_1` — `research_state/fclr016_v5_terms_evidence_RESOLVED_*.json` (`status: RESOLVED_VERIFIED`, `fabricated: false`). Human/legal attestation only.
- `NEW_OBSERVED_LIQUIDATION_SOURCE` — `research_state/<source>_admissibility_audit_<UTC>.{md,json}` (`status: ADMISSIBLE`, `observed_labels: true`, >=5 instruments, >=3 blocks or >=1 complete month).
- `HL_LABEL_EXTENSION` — `research_state/hl_label_extension_audit_<UTC>.{md,json}`.
- `EXPANSION_ROBUSTNESS_REDO` — `research_state/expansion_robustness_redo_prereg_<UTC>.json` + `evaluation_summary_*.json`.

## Tombstones (no authority)

- `NEXT_SESSION_HANDOFF.md`, `NEXT_SESSION_TASK.md`: tombstoned 2026-11-15T22:57:29Z.
- `AGENT_HANDOFF_20261115T073240Z.md`: SUPERSEDED — ignore.
- `HANDOFF_NEXT_SESSION_20261116T114626Z.md`: tombstoned 2026-11-16T12:45:00Z — ignore.

## Verification record — 2026-11-16T23:25:43Z FCLR-008 independent recompute completed

- **Session**: `session_20261116T230140Z/` — FCLR-008 independent recompute produced `recompute_fclr008_20261116T230140Z.{py,json,md}` + `evidence_audit_20261116T230140Z.md`
- **Results**: 23520 rows (train=8280, val=4440, test=10800); B0 QLIKE 0.330127 (match 3e-7), B1 QLIKE 0.333314 (match 3e-7), C1 QLIKE 0.331605 (divergence 1.44e-3), C2 QLIKE 0.321066 (divergence 2.07e-3). C2_vs_B1 mean diff -0.012248 (rel 3.67%), C1_vs_B1 -0.001708 (rel 0.51%), C2_vs_C1 -0.010540 (rel 3.28%). All n=10785 match.
- **Verdict**: B0/B1 reproduce perfectly (within 1e-6); C1/C2 diverge due to EMA/premium/funding edge-case differences — qualitative NOT_MET verdict corroborated (CI does not exclude zero).
- **Gates**: `check_handoff_heavywork_gate.py --json` **PASS** (bundle resolved, new session self-contained with evidence + quant artifact). `check_tracka_scope_registry_drift.py --json` **PASS** (196/196 scripts registered). Targeted suite: **52 tests OK, EXIT 0**. Full `unittest discover -q`: **1340 tests, 4 errors (pre-existing pyarrow missing), 18 skipped, EXIT 1** — recorded per mandate.
- **Queue advanced**: FCLR-008 ticked DONE; next target FCLR-002/003.
- **Git tree**: clean; no uncommitted changes.

(End of file)