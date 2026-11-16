# AGENT HANDOFF — 2026-11-16T22:01:26Z (sole durable handoff; current next task FCLR-008 reproducibility recompute)

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION

**Priority 0 — repository and rank-0 state.** Repository: `Funding-conditioned-volatility-and-liquidation-risk` — funding-conditioned volatility and liquidation risk. Program status: `CLOSED_TERMINAL` (final structural closure `research_state/fclr_final_structural_closure_20261116T114626.{md,json}`; terminal verdict `NO_CLAIM_WORTHY_RESULT_PROMOTABLE; ALL_P1_P2_P3_SEALED`; all P1/P2/P3 sealed; no feasible 3-block pre-registered design in any domain). Rank-0 campaign `FCLR-BOUNDED-TRIGGER-ONLY-20261115T220000Z` (`TRIGGER_ONLY` / `BOUNDED_TRIGGER_ONLY`, `all_terminal=true`, `next_action_heavy=null`). All cached-data confirmatory estimands are terminal. Sealed FCLR-011 PASS was not independently reproduced (clean recompute C2 vs B1 **-294.01%** vs sealed **+4.94%**); fragile/non-promotable — triple-confirmed by a third numpy-only implementation path. Track B `NOT_SUPPORTED`; Track C cached confirmatory designs terminal; H2 (Shek) `EXPLORATORY_ONLY`. FCLR-009 (the only adequately powered Track C null, n=24,495, MDE 1.95%) independently reproduced (`research_state/session_20261116T125624Z/`, `all_within_tolerance=true`) — CLOSED. FCLR-006 independently reproduced (`research_state/session_20261116T185811Z/`, `all_within_tolerance=true`; C2 vs B1 mean diff 0.354989, rel -67.32%, n_pairs 8987; gate NOT_MET, H001 NOT_SUPPORTED) — CLOSED.

**Read these first, in order:**
1. `research_state/resume_trigger_registry.json`
2. `research_state/ironflow_monitor_state.json`
3. `research_state/FCLR_HEAVY_CAMPAIGN_NEXT.md` (campaign `FCLR-REPRO-AUDIT-02`)
4. `research_state/session_20261116T185811Z/evidence_audit_20261116T185811Z.md` and `recompute_fclr006_20261116T185811Z.md` (latest completed heavy evidence)
5. `research_state/research_protocol_fclr008.md`, `research_state/evaluation_summary_FCLR-008.md` (CURRENT TARGET — FCLR-008 protocol and published results)

**MANDATORY — campaign `FCLR-REPRO-AUDIT-02`, queue item 3: FCLR-008 independent recompute.** This is the only agent-removable heavy work. Do all steps in order. **A trigger check, unit tests only, bundle re-audit only, copied artifacts, or a "no trigger → stop cleanly" session is NOT completion. Completion requires a NEW `research_state/session_<UTC>/` containing a NEW quantitative artifact `recompute_fclr008_<UTC>.{json,md}` plus the recompute script.**

1. **Create `research_state/session_<UTC>/`** (actual UTC). `research_state/` root is **500/500** md/json (fail-closed cap); put ALL new artifacts inside the session subdirectory only.
2. **Check triggers exactly once (no network, no polling).** Read files 1–2 above. Record timestamp, each trigger status, `data_through`, and post-2026-10 month classifications in the session dir. Current state: all four `OPEN`; Ironflow `data_through=2026-10`; 2026-11/2026-12/2027-01 `CONFIRMED_ABSENT`. Do not re-probe HuggingFace or repeat later.
3. **Produce ONE NEW quantitative artifact — FCLR-008** (unsealed 2026-01..2026-08 volatility-forecast panel; **FCLR-009 and FCLR-006 are DONE — do NOT repeat**). Recompute independently from frozen protocol and cached 2026 data:
   - Protocol: `research_state/research_protocol_fclr008.md` (frozen). Published: `research_state/evaluation_summary_FCLR-008.md`.
   - Frozen splits (do not relax): train `2026-01-01T00:00:00Z..2026-03-17T23:00:00Z`; 7d embargo `2026-03-18..2026-03-24`; val `2026-03-25T00:00:00Z..2026-04-30T23:00:00Z`; 7d embargo `2026-05-01..2026-05-07`; test `2026-05-08T00:00:00Z..2026-08-06T23:00:00Z` (91 days, 3×30d blocks).
   - Universe: BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT. Data: `research_state/data_cache/{SYM}_2026_0{1,2,3,4,5,6,7,8}/` (markPriceKlines 1h, indexPriceKlines, premiumIndexKlines, fundingRate). Funding lookback may require earlier 2026 months present in cache — load as needed but respect frozen test boundary.
   - Models: B0 persistence (preceding RV24h); B1 HAR-style OLS on log RV1h/RV24h/RV168h; C1 = B1 + signed funding + past-only 90-day |funding| percentile; C2 = C1 + mark/index premium + mark/EMA24 distance. OLS on log(RV+1e-12); follow frozen protocol semantics (training-only standardization/smearing where specified). Primary contrast: C2 vs B1 on 24h QLIKE; secondary: C1 vs B1, C2 vs C1. Block bootstrap ~24h blocks, 2000 deterministic-seed replicates.
   - **Published values to reproduce (from `evaluation_summary_FCLR-008.md`):** B0 QLIKE `0.330127` (n=10800), B1 `0.333314` (n=10785), C1 `0.330164` (n=10785), C2 `0.318996` (n=10785). C2_vs_B1 mean diff `-0.014318` (95% CI `[-0.029938, 0.000524]`), rel reduction `4.30%`, paired n `10785`. C1_vs_B1 mean diff `-0.003150` (CI `[-0.010051, 0.003832]`), rel `0.94%`, n `10785`. C2_vs_C1 mean diff `-0.011168` (CI `[-0.026088, 0.002175]`), rel `3.38%`, n `10785`. Gate (C2 vs B1 >=2% rel reduction AND CI excludes zero AND >=5 instruments AND >=3 blocks): **NOT_MET** (CI does not exclude zero). Reproduce direction/magnitudes/n within tolerance.
   - **Tolerances:** QLIKE absolute `<= 1e-6`; mean diff absolute `<= 1e-6`; relative reduction `<= 0.01` percentage points (n must match where deterministic). Write `recompute_fclr008_<UTC>.{json,md}` + script in the session dir. Do **not** run canonical `scripts/run_evaluation.py` against tracked `evaluation_summary_FCLR-008.md`; use an independent path; never mutate sealed artifacts.
   - **Fallback only if required cache input missing:** record exact path/hash and instead recompute `FCLR-LIQ-010-CONFIRM` from `research_state/fclr_liq_010_confirm_panel_20261113T065953Z.parquet` (still heavy work). Missing fallback doc/prose alone is not completion.
4. **Audit carried-forward evidence.** Confirm `research_state/session_20261116T100533Z/` has the five RCA-011 families (`rca011_feature_attribution_*`, `rca011_impl_crosscheck_*`, `rca011_sealed_bridge_*`, `prereg_template_trigger_gated_*`, `program_power_synthesis_*`) and `session_20261116T125624Z/` (FCLR-009) + `session_20261116T185811Z/` (FCLR-006) recomputes/audits are present. Write concise evidence-audit artifact in session dir (bundle path, families found, integrity conclusion: RCA complete; FCLR-011 not reproducible/promotable; FCLR-009 & FCLR-006 independently reproduced; `next_action_heavy=null` on cached data). Do not rerun FCLR-RCA-011/FCLR-009/FCLR-006.
5. **Run and capture every required gate under the new session dir:**
   - `python3 scripts/check_handoff_heavywork_gate.py --json` — PASS with complete `session_20261116T100533Z` bundle, new session as latest (audit + fresh quant artifact), root <= 500.
   - `python3 scripts/check_tracka_scope_registry_drift.py --json` — PASS (register any new script in both scope registries).
   - `python3 -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_117 tests.test_tracka_hardening_118 tests.test_tracka_hardening_143` — all pass.
   - `python3 -m unittest discover -q` — run to completion; record exact test count, skip count, final EXIT. Never treat timeout/monitor cap as green. Revert any timestamp-only side effect to tracked files (e.g. `research_state/ironflow_fastpath_cache.json`, `experiment_frontier.json`).
6. **Update only this handoff** after steps 3–5: replace timestamp/verification with actual results, advance queue (tick FCLR-008 if done), keep sole-handoff contract, bundle refs, blockers intact. Do not create another handoff file and do not execute tombstoned instructions.

**Trigger-gated science is the only scientific advance — but it must be pre-powered.** If no trigger is satisfied, do not advance or re-run a confirmatory estimand. The required holding action is the new FCLR-008 reproducibility artifact (or documented LIQ-010 fallback) plus the evidence audit, complete gate run, and accurate handoff update. If a trigger is satisfied, follow §16 admissibility/source audit first, freeze the pre-sized prereg before inspecting outcomes, require a materially different estimand and the power ledger's sample floor, then execute, register any new scripts in both scope registries, run all gates, and update the frontier/hypothesis registries with an honest verdict.

**Heavy-work mandate (future agents cannot avoid this):** Completion of any session under this handoff requires a *new* `research_state/session_<UTC>/` containing a *new* quantitative artifact — normally `recompute_fclr008_<UTC>.{json,md}` (next: `recompute_fclr002_<UTC>`/`recompute_fclr003_<UTC>`, then FCLR-010, then FCLR-013/FCLR-014). Re-auditing the static bundle, re-running gates alone, copying old artifacts, redoing FCLR-009/FCLR-006, or a trigger-check-only session is explicitly **NOT** completion. The gate is a floor; the new artifact is the requirement.

**Heavy-work evidence on disk (authoritative).** Self-contained bundle: `research_state/session_20261116T100533Z/` (carried forward from `session_20261116T035833Z/`): `rca011_feature_attribution_*` (funding increment **-342.67%**, EMA24 **+9.75%**, joint **-294.01%**), `rca011_impl_crosscheck_*` (OLS/lstsq agree ~1e-12–1e-17), `rca011_sealed_bridge_*` (sealed **+4.94%** vs clean **-294.01%**; 120-row eligibility delta; sealed panel unavailable/LFS-pointer artifact), `prereg_template_trigger_gated_*`, `program_power_synthesis_*` (FCLR-011 fragile/non-promotable; `next_action_heavy=null`), plus `trigger_readiness_power_calibration_*`/`trigger_readiness_power.py` (pre-sized per-trigger floors: Gate4/TrackC `paired_n>=23224`, TrackA/expansion `paired_n>=11689`, >=3 blocks, 7d purge/embargo; only FCLR-009 powered for 2% MDE).
- `session_20261116T125624Z/`: `recompute_fclr009_20261116T125624Z.{py,json,md}` + `evidence_audit_20261116T125624Z.md` — FCLR-009 reproduced `all_within_tolerance=true` (B0 0.367906 n=24648, B1 0.340756 n=24495, C1 0.339628, C2 0.342205; C2-vs-B1 diff 0.001449, rel -0.425%, CI [-0.003120,0.006165], n_pairs 24495). 4 files; no suite capture.
- `session_20261116T185811Z/`: `recompute_fclr006_20261116T185811Z.{py,json,md}` + `evidence_audit_20261116T185811Z.md` + `trigger_check.json` + `unittest_discover.txt` + gate outputs — FCLR-006 reproduced `all_within_tolerance=true` (B0 0.518169 n=9000, B1 0.527290 n=8987, C1 0.620158, C2 0.882279; C2-vs-B1 diff 0.354989, rel -67.32%, n_pairs 8987, errata CI [0.173748,0.615614]; gate NOT_MET 2 blocks < 3; H001 NOT_SUPPORTED).
- `session_20261116T115028Z/`: third numpy-only FCLR-011 crosscheck (`independent_recompute_fclr011_*`) confirming sealed PASS not reproducible; funding drives harm.
- `session_20261116T140001Z/`: FCLR-006 attempt with `all_within_tolerance=false` (row-count/alignment discrepancy) — **superseded** by `session_20261116T185811Z`; do not treat as queue completion.

**Bottlenecks removed (2026-11-16T21:15:19Z refresh; reaffirmed).**
- **Empty/stale session clutter removed:** three empty post-handoff session directories created after the last handoff (0 entries, untracked) were removed this refresh. They were incomplete trigger-only placeholders and must never be recreated as empty shells.
- **Maintenance-refresh treadmill called out:** prior refreshes (20:06, 20:14, 20:59, 21:09) were handoff-only maintenance with no new heavy artifact. That is acceptable only when followed by a real FCLR-008 session; do not repeat the pattern. The next session MUST emit `recompute_fclr008_<UTC>.{json,md}`.
- **Stale primary target removed:** FCLR-006/FCLR-009 DONE; primary is **FCLR-008** (queue item 3) with explicit published values embedded above. `FCLR_HEAVY_CAMPAIGN_NEXT.md` aligned in this refresh to prevent rework.
- **Stale/incomplete session ambiguity removed:** trigger-only sessions (see campaign note for exact ids) are incomplete/superseded — must not be resumed, copied, or counted. `session_20261116T140001Z/` superseded by 185811Z.
- **False gate failure / treadmill / design-on-trigger / dependency / handoff-authority / root-churn bottlenecks** remain resolved as before (gate accepts latest session with audit+fresh quant while resolving complete bundle; stdlib/numpy-only reproducibility path; no statsmodels in core; this file sole authority; root 500/500 session-only writes).

**Bottlenecks and prohibitions.**
- Do not start or re-run any cached-data confirmatory estimand; all are terminal.
- Do not mutate sealed artifacts, the frontier, hypothesis registries, or `.github/workflows/*`.
- Do not poll, re-probe the HuggingFace tree, use paid/credentialed/manual outcome data, or add root-level `research_state/*.md|json`.
- Do not add `statsmodels` or other unpinned heavy dependencies to the core path; install only `requirements.txt` if a documented gate needs it.
- The discovery suite is long-running; let it finish and record its actual EXIT, not a partial result.
- The scientific blocker is external: no admissible post-2026-10 observed liquidation labels/source and no agent-settable Gate 4 attestation. The agent-removable requirement is the new quantitative artifact, evidence audit, complete verification, and accurate handoff update.

**Reopen triggers (machine-checkable — Act ONLY when satisfied).** All four are `OPEN`. Do not act until the predicate is satisfied by a concrete evidence artifact in `research_state/`: `GATE4_BRANCH_1` (`fclr016_v5_terms_evidence_RESOLVED_*.json` with `status: RESOLVED_VERIFIED`, `fabricated: false`), `NEW_OBSERVED_LIQUIDATION_SOURCE` (`<source>_admissibility_audit_<UTC>.json` with `status: ADMISSIBLE`, `observed_labels: true`), `HL_LABEL_EXTENSION` (`hl_label_extension_audit_<UTC>.{md,json}`), `EXPANSION_ROBUSTNESS_REDO` (`expansion_robustness_redo_prereg_<UTC>.json` + `evaluation_summary_*.json`).

**Verification record — 2026-11-16T21:15:19Z handoff refresh (maintenance; no new heavy research artifact produced this session).**
- Purpose: refreshed sole durable handoff points unambiguously to **FCLR-008 independent recompute** (`recompute_fclr008_<UTC>.{json,md}`) as mandatory next heavy work; removed three empty post-handoff session dirs; flagged the tracked trigger-only session as non-counting. FCLR-006/FCLR-009 remain DONE and must not be repeated.
- Triggers/monitor read (no network): all 4 `OPEN`; Ironflow `data_through=2026-10`; 2026-11/12/2027-01 `CONFIRMED_ABSENT`.
- Inputs verified present: `research_state/research_protocol_fclr008.md`, `research_state/evaluation_summary_FCLR-008.md`, and `research_state/data_cache/{BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,XRPUSDT}_2026_0{1..8}/` all present. Fallback panel `fclr_liq_010_confirm_panel_20261113T065953Z.parquet` present (6,051,126 bytes).
- Gates rechecked: `python3 scripts/check_handoff_heavywork_gate.py --json` **PASS** (heavy_session `session_20261116T100533Z`, latest_session `session_20261116T185811Z`, root 500/500). `python3 scripts/check_tracka_scope_registry_drift.py --json` **PASS** (196/196). Targeted suite `tests.test_active_campaign_gate tests.test_tracka_hardening_117 tests.test_tracka_hardening_118 tests.test_tracka_hardening_143` **52 tests OK, EXIT 0**. No code/script changes; full `unittest discover` remains mandatory in the next heavy session per contract.

## Reproducibility-audit queue (non-skippable heavy work; do in order)

1. ~~FCLR-009~~ — DONE (`session_20261116T125624Z`; all_within_tolerance=true).
2. ~~FCLR-006~~ — DONE (`session_20261116T185811Z`; `all_within_tolerance=true`; recompute_fclr006_20261116T185811Z.{py,json,md} produced; C2_vs_B1 mean diff 0.354989, rel -67.32%, n_pairs 8987 all match; gate NOT_MET, H001 NOT_SUPPORTED).
3. **FCLR-008 (unsealed 2026-01..2026-08): independent recompute, `recompute_fclr008_<UTC>.{json,md}` — CURRENT TARGET.**
4. FCLR-002 / FCLR-003 (sealed 2024 panels): independent recompute, `recompute_fclr002_<UTC>.{json,md}` / `recompute_fclr003_<UTC>.{json,md}`.
5. FCLR-010 (Track A liquidation confirm): independent recompute from `fclr_liq_010_confirm_panel_*.parquet`, `recompute_fclr010_<UTC>.{json,md}`.
6. FCLR-013 / FCLR-014 (2026 Q3 / 2025 H1 panels): independent recompute.

A session that completes an item must (a) create a new `research_state/session_<UTC>/`, (b) emit a new quantitative artifact named per the queue, (c) write an evidence audit, (d) run all gates + full discovery suite to completion, (e) update this handoff's verification record and tick the queue item. Trigger check + tests alone is not completion. "No trigger → stop cleanly" is NOT completion.

## Tombstones (no authority)

- `NEXT_SESSION_HANDOFF.md`, `NEXT_SESSION_TASK.md`: tombstoned 2026-11-15T22:57:29Z.
- `AGENT_HANDOFF_20261115T073240Z.md`: SUPERSEDED — ignore.
- `HANDOFF_NEXT_SESSION_20261116T114626Z.md`: tombstoned 2026-11-16T12:45:00Z — ignore; this file is the sole durable handoff.

**Verification record — 2026-11-16T21:09:12Z handoff refresh.**
- Purpose: reaffirmed sole durable handoff points unambiguously to **FCLR-008 independent recompute** (`recompute_fclr008_<UTC>.{json,md}`) as mandatory next heavy work; cleared/flagged no resumable trigger-only/incomplete sessions. FCLR-006/FCLR-009 remain DONE and must not be repeated.
- Triggers/monitor read (no network): all 4 `OPEN`; Ironflow `data_through=2026-10`; 2026-11/12/2027-01 `CONFIRMED_ABSENT`.
- Gates rechecked: `python3 scripts/check_handoff_heavywork_gate.py --json` **PASS** (heavy_session `session_20261116T100533Z`, latest_session `session_20261116T185811Z`, root 500/500). `python3 scripts/check_tracka_scope_registry_drift.py --json` **PASS** (196/196). No code/script changes; full verification remains mandatory in next heavy session per contract.

**Verification record — 2026-11-16T20:59:36Z handoff refresh (maintenance; no new heavy research artifact produced this session).**
- Purpose: reaffirmed sole durable handoff points unambiguously to **FCLR-008 independent recompute** (`recompute_fclr008_<UTC>.{json,md}`) as mandatory next heavy work. FCLR-006/FCLR-009 remain DONE and must not be repeated.
- Triggers/monitor read (no network): all 4 `OPEN`; Ironflow `data_through=2026-10`; 2026-11/12/2027-01 `CONFIRMED_ABSENT`.
- Gates rechecked: `python3 scripts/check_handoff_heavywork_gate.py --json` **PASS**; `python3 scripts/check_tracka_scope_registry_drift.py --json` **PASS** (196/196). No code/script changes; full verification remains mandatory in next heavy session per contract.

## Reopen triggers summary (machine-checkable)

All four are `OPEN`; act ONLY when the registry-defined predicate is satisfied by a concrete artifact:
- `GATE4_BRANCH_1` — `research_state/fclr016_v5_terms_evidence_RESOLVED_*.json` (`status: RESOLVED_VERIFIED`, `fabricated: false`). Human/legal attestation only; never agent-set.
- `NEW_OBSERVED_LIQUIDATION_SOURCE` — `research_state/<source>_admissibility_audit_<UTC>.{md,json}` (`status: ADMISSIBLE`, `observed_labels: true`, >=5 instruments, >=3 blocks or >=1 complete month).
- `HL_LABEL_EXTENSION` — `research_state/hl_label_extension_audit_<UTC>.{md,json}`.
- `EXPANSION_ROBUSTNESS_REDO` — `research_state/expansion_robustness_redo_prereg_<UTC>.json` + `evaluation_summary_*.json`.

(End of file)