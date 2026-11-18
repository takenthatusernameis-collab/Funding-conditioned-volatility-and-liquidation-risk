# AGENT HANDOFF — 2026-11-18T12:21:30Z (sole durable handoff)

> **Authority:** this file only. Every other handoff-like file is tombstoned/historical and has no campaign authority. No duplicate authority remains. There is exactly one root `AGENT_HANDOFF.md`; do not create copies under `research_state/`, `scripts/`, `tests/`, or `src/`.

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION (timestamped 2026-11-18T12:21:30Z)

**Repo (P0):** `Funding-conditioned-volatility-and-liquidation-risk` — the repo name *is* the campaign. Two named risks, in this priority order:
1. **Funding-conditioned volatility/stress forecasting (Track C):** does funding predict future realized vol / stress vs an RV-only baseline? QLIKE/MAE/RMSE, leakage-resistant OOS.
2. **Liquidation-boundary risk (Track B):** do funding-conditioned features predict modeled liquidation-boundary breaches?

Use only admissible local/public data already on disk (ZIP/CSV/JSON/dir twins under `research_state/data_cache/` and `data/raw/`). **No network, no parquet engine, no `git lfs pull`, no installs, no new root `research_state/*.md|json` (root 500/500 at cap).**

**State: `ACTIVE_CAMPAIGN` / GATE GREEN, BOTTLENECK CLEARED (stale handoff resolved via `session_20261118T114500Z`), NEXT HEAVY CAMPAIGN BOUND.** Latest completed heavy session: **`research_state/session_20261118T114500Z`** (Track C forecast + Track B breach labels carried forward from `session_20261118T093031Z`, **and** the breach-forecast campaign `FCLR-VOL-LIQ-BREACH-FORECAST-03` executed — EXPLORATORY/PILOT, honest negative result, materiality floor NOT met). The next session must NOT idle, re-audit, or emit another gate-only note. It must execute the mandatory **next focus campaign `FCLR-VOL-LIQ-ROBUST-04`** below and record its new session id in this handoff before final gate capture.

**Program lineage:** parent `FCLR-VOL-LIQ-FORECAST-01-20261118T023259Z`. Completed execution campaign: `FCLR-VOL-LIQ-EXECUTION-01-20261118T092338Z` (Track C Design A stdlib forecast + Track B modeled breach labels — both delivered in `session_20261118T093031Z`). Completed breach-forecast campaign: `FCLR-VOL-LIQ-BREACH-FORECAST-03-20261118T103106Z` (joined Track C features + Track B labels; executed in `session_20261118T114500Z`, EXPLORATORY/PILOT, honest negative result — funding-conditioned features did NOT improve modeled breach discrimination; materiality floor NOT met). **Active next focus campaign: `FCLR-VOL-LIQ-ROBUST-04-20261118T120000Z`** (stdlib robustness confirmation of Track C funding-trail QLIKE on an alternative chronological holdout; see Next Focus Campaign section). Rank-0 trigger state remains `FCLR-BOUNDED-TRIGGER-ONLY-20261115T220000Z` (`TRIGGER_ONLY`, `next_action_heavy=null`); all triggers OPEN, none fired.

### Gates (verify first — CURRENT STATE: ALL PASS)
- `python3 scripts/check_handoff_heavywork_gate.py --json`: **pass=true**, `handoff_stale=false`, root=500/500 (at cap). Binds `FCLR-VOL-LIQ-BREACH-FORECAST-03` (post-start: `session_20261118T114500Z` > campaign start 103106Z → required; prereg + forecast triad + trigger check all present and non-empty → PASS) and the next focus campaign `FCLR-VOL-LIQ-ROBUST-04-20261118T120000Z` (future start 120000Z; `session_20261118T114500Z` is grandfathered; any session after 120000Z must emit the robust-04 prereg + robustness recompute triad + trigger check or fail closed). Audit-only, empty-file, and gate-only sessions fail closed. Sessions predating the campaign start (incl. `session_20261118T093031Z`) are grandfathered.
- `python3 scripts/check_tracka_scope_registry_drift.py --json`: **PASS** (`reason_code=OK`, 196/196).
- `python3 scripts/next_campaign_status.py --json`: confirmatory multi-block cached design remains **BLOCKED** (contiguous runs too short; disjoint 30-day blocks `n_feasible=0`; `max_mutually_non_overlapping=1 < 3`). Ready funding-backed cache months: 2024-04, 2024-05, 2025-01. No actionable frozen preregs. Track C single-window Design A and Track B remain feasible via stdlib on cached data (proven by `session_20261118T093031Z` and `session_20261118T114500Z`).
- `python3 -m unittest tests.test_tracka_hardening_143 -v`: **PASS** (includes the new breach-forecast fail-closed coverage). Full `unittest discover` remains environmental/hanging in this runtime; use targeted tests and record that limitation, not a green full suite.

### Bottlenecks resolved in this handoff (2026-11-18T12:21:30Z)
- **Stale / incomplete latest session (CLEARED):** `session_20261118T093031Z` existed on disk with Track C only (missing Track B, `trigger_check`, and `evidence_audit`), so the gate failed closed with `HANDOFF_STALE_LATEST_SESSION`. Completed: `trackb_breach_labels_20261118T093031Z.{py,json,md}`, `recompute_trackb_breach_labels_20261118T093031Z.json`, `trigger_check_20261118T093031Z.json`, `evidence_audit_20261118T093031Z.{json,md}` are all present and non-empty. The gate is now green.
- **Newer unrecorded session bottleneck (CLEARED):** `session_20261118T114500Z` existed on disk (breach-forecast execution) but was not recorded in this handoff, causing `HANDOFF_STALE_LATEST_SESSION:session_20261118T114500Z`. Completed: session `114500Z` now carries the breach-forecast prereg + forecast triad + trigger check + evidence audit + fresh `recompute_*` quant, all non-empty, and is recorded below as the latest session. The stale-handoff bypass is closed.
- **Empty-session bypass (still closed):** the execution-campaign gate rejects zero-byte required artifacts by name and size; empty placeholders can never satisfy the heavy-work contract.
- **Audit-only / gate-only non-avoidance (closed):** the `FCLR-VOL-LIQ-BREACH-FORECAST-03` and `FCLR-VOL-LIQ-ROBUST-04` campaigns require their prereg + forecast/robustness triad + trigger check + evidence audit in the latest post-start session, not a generic recompute.
- **Estimand-execution blocker (`numpy`/`pandas`/`scipy` absent, installs prohibited):** remains an environment constraint, not a data/design constraint. Do not wait for numpy. Implement the stdlib fallback (`math`/`csv`/`json`/`zipfile`) and label results EXPLORATORY/PILOT.

### Progress recorded at 2026-11-18T09:30:31Z (`session_20261118T093031Z`, read-only cache, no network)
- **Track C — Design A exploratory volatility forecast (COMPLETE, EXPLORATORY/PILOT):** stdlib OLS HAR, 5 instruments (BTC/ETH/SOL/XRP/BNB) × 2024-04..09, 3 chronological non-overlapping 30d test blocks with 7d purge/embargo, expanding train, 2000-rep UTC-day block bootstrap (seed 12345). Headline cross-split mean ΔQLIKE vs RV-only (A): B(signed)=-0.0079, C(abs)=-0.0150, D(signed+abs)=-0.0562, **E(funding trails)=-0.3579, CI95=[-0.4980, -0.1932]**. Funding-trail features materially improve QLIKE in every leave-one-instrument-out slice. Label EXPLORATORY/PILOT; no sealed months touched.
- **Track B — Modeled liquidation-boundary-breach labels (COMPLETE, `synthetic_modeled_boundary_breach`, `observed_liquidation_labels=false`):** 2024-04, 5 instruments, L∈{5,10,20} × side∈{long,short} × H∈{4h,24h}, mmr=0.005, entry at close of bar t, path t+1..t+H. **41,760 label rows; 1,418 breached; overall breach rate 3.40%.** Higher leverage and long side breach more (L20|long|H24 = 19.6%, L10|long|H24 = 4.77%). These are synthetic modeled breaches, never observed liquidations.

### Progress recorded at 2026-11-18T11:45:00Z (`session_20261118T114500Z`, read-only cache, no network)
- **Track B/C breach-forecast campaign `FCLR-VOL-LIQ-BREACH-FORECAST-03` (EXECUTED, EXPLORATORY/PILOT):** joined Track C causal RV features (lrv1/lrv24/lrv168/fund/fund_abs/fmean/fewma) with Track B modeled breach labels (2024-04, 5 instruments, 12 scenarios × 2 chronological splits, 7d purge/embargo). Stdlib IRLS logistic (ridge λ=1e-6, seed 12345). RV-only baseline B0 vs funding-conditioned candidate B1. **Honest negative result:** pooled mean ΔAUC (B1−B0) = −0.0661 across 2 splits; bootstrap CI95 straddles/below zero; LOIO ΔAUC negative for all 5 instruments; prereg materiality floor (ΔAUC ≥ +0.01, CI95 lower bound > 0) **NOT met**. Funding-conditioned features did NOT improve modeled breach discrimination. Single labeled month = pilot quality; not confirmatory; no forecast-gate pass claim. No sealed months touched; no observed liquidations.
- Artifacts: `trackbc_breach_prereg_20261118T114500Z.{json,md}`, `trackbc_breach_forecast_20261118T114500Z.{py,json,md}`, `trigger_check_20261118T114500Z.json`, `evidence_audit_20261118T114500Z.{json,md}`, `recompute_trackbc_breach_forecast_20261118T114500Z.json`, plus carried-forward Track C + Track B + recompute from `session_20261118T093031Z`.

## Next focus campaign — REQUIRED heavy-work (non-avoidable; machine-enforced by gate)

**`FCLR-VOL-LIQ-ROBUST-04-20261118T120000Z` — Track C funding-trail robustness confirmation (stdlib, cached data).**
Research question: does the Track C Design A funding-trail QLIKE improvement (E = −0.3579 vs RV-only) hold under an alternative chronological holdout (2024-09 holdout, train 2024-04..08) on the cached 2024-04..09 panel? Same 5 instruments, stdlib OLS HAR, expanding train, block bootstrap seed 12345. Label EXPLORATORY/PILOT; no confirmatory/forecast-gate claim; no sealed months.

**Prereg (freeze first, before touching evaluation):** `fclr_robust04_prereg_<UTC>.json` (+ `.md` companion). Fix ex ante: instruments, holdout month 2024-09, train window 2024-04..08, entry-origin rule, feature set (lrv1/lrv24/lrv168/fund/fund_abs/fmean/fewma, causal at t), model family (stdlib OLS HAR, Duan smearing), metric (ΔQLIKE vs RV-only, MAE, RMSE), block bootstrap (UTC-day, seed 12345, 2000 reps), leave-one-instrument-out, materiality floor. Record `outcome_data_inspected_before_freeze=false`. No future bars, no full-sample normalization, no sealed months.

**Model + evaluation:** stdlib only (`math`/`csv`/`json`/`zipfile`). Fit on train 2024-04..08, evaluate on holdout 2024-09; report funding-trail ΔQLIKE vs RV-only with bootstrap CI95 and LOIO.

**Required artifacts (exact prefixes; all non-empty) in the new `research_state/session_<UTC>/` dir (UTC after campaign start 120000Z):**
- `fclr_robust04_prereg_<UTC>.json`
- `fclr_robust04_prereg_<UTC>.md`
- `fclr_robust04_robustness_<UTC>.py`
- `fclr_robust04_robustness_<UTC>.json`
- `fclr_robust04_robustness_<UTC>.md`
- `trigger_check_<UTC>.json`
- `evidence_audit_<UTC>.json` + `evidence_audit_<UTC>.md`
- a `recompute_*` summary (e.g. `recompute_fclr_robust04_robustness_<UTC>.json`) to satisfy the new-style heavy check

Carry forward (copy, do not recompute) from `session_20261118T093031Z` or `session_20261118T114500Z`: `trackc_design_a_forecast_*.{py,json,md}`, `trackb_breach_labels_*.{py,json,md}`, and a non-empty `trigger_check_<UTC>.json`.

### Record, verify, hand off
1. Create `research_state/session_<UTC>/` (UTC after 120000Z) with all artifacts above (copied + new robust-04 work).
2. Update this handoff's latest session id to the new session before running the final gate.
3. Run targeted tests only: `python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_125 -v` (bounded; full discover hangs in this env).
4. Re-run all three gates; confirm PASS and paste the exact outcomes into the verification record.
5. Update only `AGENT_HANDOFF.md` and the new session directory. Do not modify sealed artifacts, closure JSON, registries, or `.github/workflows/*`.

## Upgrade path (only if numerical runtime becomes available)
Freeze an outcome-blind exploratory prereg for Track C Design A using the `trackc_extension_design` schema, verify per-symbol bar completeness and tested-window non-conflict (already PASS), then run per-split metrics + evaluation summary. Label EXPLORATORY/PILOT until all §17 gates pass.

## If and only if a reopen trigger becomes machine-satisfied (outcome-gated)
1. Create `research_state/session_<UTC>/` and record id in handoff before final gate capture.
2. **GATE4_BRANCH_1:** `fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` (`status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal).
3. **NEW_OBSERVED_LIQUIDATION_SOURCE:** `<source>_admissibility_audit_<UTC>.{md,json}` proving `status=ADMISSIBLE`, `observed_labels=true`, unauthenticated, provenance/license/venue-consistent, ≥5 instruments and (≥3 blocks or ≥1 complete month). Admissibility audit BEFORE prereg/outcomes.
4. **HL_LABEL_EXTENSION:** verified post-2026-10-31 observed ironflow labels (≥100 days) + `hl_label_extension_audit_<UTC>.{md,json}` + newly preregistered design.
5. **EXPANSION_ROBUSTNESS_REDO:** newly preregistered design achieving LOIO≥6/8 AND placebo>95th null — **re-scoring sealed 19.04% forbidden**.

## Read first
1. `RESEARCH_PROMPT.md` §1–§6, §16–§17.
2. `research_state/session_20261118T093031Z/{trackc_design_a_forecast,trackb_breach_labels,evidence_audit,trigger_check}_20261118T093031Z.*` (completed Track C + Track B + audit).
3. `research_state/session_20261118T114500Z/{trackbc_breach_prereg,trackbc_breach_forecast,evidence_audit,trigger_check}_20261118T114500Z.*` (executed breach-forecast campaign + audit).
4. `research_state/session_20261118T030427Z/{trackc_extension_design,trackb_boundary_labels,evidence_audit}_20261118T030427Z.*` (design specs + Track B protocol).
5. `research_state/evaluation_summary.md`, `research_state/data_source_registry.json`, `research_state/fclr_final_structural_closure_20261116T114626.{md,json}`, `research_state/resume_trigger_registry.json`.

## Prohibitions
- Do not re-run sealed cached-data confirmatory estimands or re-score sealed results (FCLR-014, replication synthesis, design-frontier certs, FCLR-013/010/002/003/009/006/008, frontier verify-06/07/08+, sealed 19.04%).
- No polling/HF re-probe, no paid/credentialed/manual outcome data, no network installs/fetches, no `git lfs pull`.
- No mutation of sealed artifacts/closure JSON/`.github/workflows/*`; no root-level `research_state/*.md|json` (root 500/500 cap); no duplicate `AGENT_HANDOFF*` files.
- No `statsmodels` or unpinned heavy deps in core path. Do not run parquet-only scripts without a CSV/JSON/ZIP twin.
- Do not treat missing-numpy/environmental discovery errors as green. Never inspect outcomes while producing outcome-blind preregs. **Do not emit empty/zero-byte artifacts; content is mandatory.**
- Do not leave a session recorded in this handoff without its required execution artifacts present and non-empty on disk.

## Reopen triggers (machine-checkable — all OPEN)
- `GATE4_BRANCH_1`: `research_state/fclr016_v5_terms_evidence_RESOLVED_*.json` (`status=RESOLVED_VERIFIED`, `fabricated=false`).
- `NEW_OBSERVED_LIQUIDATION_SOURCE`: `research_state/<source>_admissibility_audit_<UTC>.{md,json}` (`status=ADMISSIBLE`, `observed_labels=true`, ≥5 instruments, ≥3 blocks or ≥1 complete month).
- `HL_LABEL_EXTENSION`: `research_state/hl_label_extension_audit_<UTC>.{md,json}` (post-2026-10-31 observed ironflow labels, ≥100-day depth).
- `EXPANSION_ROBUSTNESS_REDO`: `research_state/expansion_robustness_redo_prereg_<UTC>.json` + evaluation summary (LOIO≥6/8 AND placebo>95th null).

## Verification record — 2026-11-18T12:21:30Z
- `python3 scripts/check_handoff_heavywork_gate.py --json`: **PASS (confirmed 2026-11-18T12:21:30Z)** — `pass=true`, `handoff_stale=false`, `root_count=500/500` [at cap], latest session `session_20261118T114500Z`; `breach_forecast` required=true PASS (machine-enforced, prereg+forecast triad+trigger check all non-empty); `robust_04` future start 120000Z → grandfathered for current session; `vol_liq_execution` PASS (trigger check present, non-empty).
- `python3 scripts/check_tracka_scope_registry_drift.py --json`: **PASS** (`reason_code=OK`).
- `python3 scripts/next_campaign_status.py --json`: confirmatory multi-block cached design remains **BLOCKED** (`any_feasible=false`).
- `python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_125`: **PASS (56 tests, confirmed 2026-11-18T12:21:30Z)**; full discover hangs in this runtime; record limitation, not a green full suite.
- Bottleneck status this refresh: **no unresolved bottleneck blocks the next campaign.** The stale/incomplete-session, newer-unrecorded-session, empty-session-bypass, and audit/gate-only non-avoidance blockers are all closed. The only remaining constraints are the data-bound confirmatory design (insufficient contiguous funded history) and the numpy/pandas/scipy-absent environment — both handled by the stdlib exploratory path, not by idling.
- No sealed artifacts/workflows/registries modified. `AGENT_HANDOFF.md` remains the sole durable handoff. The next session must execute `FCLR-VOL-LIQ-ROBUST-04` and record its new session id here.
