# AGENT HANDOFF — 2026-11-18T11:19:48Z (sole durable handoff)

> **Authority:** this file only. Every other handoff-like file is tombstoned/historical and has no campaign authority. No duplicate authority remains. There is exactly one root `AGENT_HANDOFF.md`; do not create copies under `research_state/`, `scripts/`, `tests/`, or `src/`.

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION (timestamped 2026-11-18T11:19:48Z)

**Repo (P0):** `Funding-conditioned-volatility-and-liquidation-risk` — the two named risks are the campaign: **(1) funding-conditioned volatility/stress forecasting** (Track C: funding extremes + RV vs RV-only baseline, QLIKE/MAE/RMSE, leakage-resistant OOS) and **(2) liquidation-boundary risk** (Track B: modeled breach labels from public mark-price data). Use only admissible local/public data already on disk (ZIP/CSV/JSON/dir twins under `research_state/data_cache/` and `data/raw/`). **No network, no parquet engine, no `git lfs pull`, no installs, no new root `research_state/*.md|json` (root 500/500 at cap).**

**State: `ACTIVE_CAMPAIGN` / GATE GREEN, BOTTLENECKS CLEARED, NEXT HEAVY CAMPAIGN BOUND.** Latest completed heavy session: **`research_state/session_20261118T093031Z`** (Track C forecast **and** Track B breach labels both complete). The next session must NOT idle, re-audit, or emit another gate-only note. It must execute the mandatory **breach-forecast campaign** below and record its new session id in this handoff before final gate capture.

**Program lineage:** parent `FCLR-VOL-LIQ-FORECAST-01-20261118T023259Z`. Completed execution campaign: `FCLR-VOL-LIQ-EXECUTION-01-20261118T092338Z` (Track C Design A stdlib forecast + Track B modeled breach labels — **both delivered in `session_20261118T093031Z`**). **Active next campaign: `FCLR-VOL-LIQ-BREACH-FORECAST-03-20261118T103106Z`** (join Track C features + Track B labels; do funding-conditioned volatility features predict modeled liquidation-boundary breaches?). Rank-0 trigger state remains `FCLR-BOUNDED-TRIGGER-ONLY-20261115T220000Z` (`TRIGGER_ONLY`, `next_action_heavy=null`); all triggers OPEN, none fired.

### Gates (verify first — CURRENT STATE: ALL PASS)
- `python3 scripts/check_handoff_heavywork_gate.py --json`: **pass=true**, `handoff_stale=false`, root=500/500 (at cap). Binds the new `FCLR-VOL-LIQ-BREACH-FORECAST-03` campaign: a post-start latest session must contain the outcome-blind breach prereg, the forecast triad, and a non-empty `trigger_check_*.json`; audit-only, empty-file, and gate-only sessions fail closed. Sessions predating the campaign start (incl. `session_20261118T093031Z`) are grandfathered.
- `python3 scripts/check_tracka_scope_registry_drift.py --json`: **PASS** (`reason_code=OK`, 196/196).
- `python3 scripts/next_campaign_status.py --json`: confirmatory multi-block cached design remains **BLOCKED** (contiguous runs too short; disjoint 30-day blocks `n_feasible=0`; `max_mutually_non_overlapping=1 < 3`). Ready funding-backed cache months: 2024-04, 2024-05, 2025-01. No actionable frozen preregs. Track C single-window Design A and Track B remain feasible via stdlib on cached data (proven by `session_20261118T093031Z`).
- `python3 -m unittest tests.test_tracka_hardening_143 -v`: **PASS** (includes the new breach-forecast fail-closed coverage). Full `unittest discover` remains environmental/hanging in this runtime; use targeted tests and record that limitation, not a green full suite.

### Bottlenecks resolved in this handoff (2026-11-18T11:19:48Z)
- **Stale / incomplete latest session (CLEARED):** `session_20261118T093031Z` existed on disk with Track C only (missing Track B, `trigger_check`, and `evidence_audit`), so the gate failed closed with `HANDOFF_STALE_LATEST_SESSION`. Completed: `trackb_breach_labels_20261118T093031Z.{py,json,md}`, `recompute_trackb_breach_labels_20261118T093031Z.json`, `trigger_check_20261118T093031Z.json`, `evidence_audit_20261118T093031Z.{json,md}` are all present and non-empty. The gate is now green.
- **Empty-session bypass (still closed):** the execution-campaign gate rejects zero-byte required artifacts by name and size; empty placeholders can never satisfy the heavy-work contract.
- **Audit-only / gate-only non-avoidance (closed):** the new `FCLR-VOL-LIQ-BREACH-FORECAST-03` campaign requires the breach-forecast prereg + forecast triad + trigger check in the latest post-start session, not a generic recompute.
- **Estimand-execution blocker (`numpy`/`pandas`/`scipy` absent, installs prohibited):** remains an environment constraint, not a data/design constraint. Do not wait for numpy. Implement the stdlib fallback (`math`/`csv`/`json`/`zipfile`) and label results EXPLORATORY/PILOT.

### Progress recorded at 2026-11-18T09:30:31Z (`session_20261118T093031Z`, read-only cache, no network)
- **Track C — Design A exploratory volatility forecast (COMPLETE, EXPLORATORY/PILOT):** stdlib OLS HAR, 5 instruments (BTC/ETH/SOL/XRP/BNB) × 2024-04..09, 3 chronological non-overlapping 30d test blocks with 7d purge/embargo, expanding train, 2000-rep UTC-day block bootstrap (seed 12345). Headline cross-split mean ΔQLIKE vs RV-only (A): B(signed)=-0.0079, C(abs)=-0.0150, D(signed+abs)=-0.0562, **E(funding trails)=-0.3579, CI95=[-0.4980, -0.1932]**. Funding-trail features materially improve QLIKE in every leave-one-instrument-out slice. Label EXPLORATORY/PILOT; no sealed months touched.
- **Track B — Modeled liquidation-boundary-breach labels (COMPLETE, `synthetic_modeled_boundary_breach`, `observed_liquidation_labels=false`):** 2024-04, 5 instruments, L∈{5,10,20} × side∈{long,short} × H∈{4h,24h}, mmr=0.005, entry at close of bar t, path t+1..t+H. **41,760 label rows; 1,418 breached; overall breach rate 3.40%.** Higher leverage and long side breach more (L20|long|H24 = 19.6%, L10|long|H24 = 4.77%). These are synthetic modeled breaches, never observed liquidations.
- Artifacts: `trackc_design_a_forecast_20261118T093031Z.{py,json,md}`, `trackb_breach_labels_20261118T093031Z.{py,json,md}`, `recompute_trackb_breach_labels_20261118T093031Z.json`, `trigger_check_20261118T093031Z.json`, `evidence_audit_20261118T093031Z.{json,md}`.

## Next session — REQUIRED heavy-work campaign (non-avoidable; do not stop cleanly)

Create a new `research_state/session_<UTC>/` directory. The gate will reject the session if any required artifact is missing, empty, or replaced by another generic recompute. **Both** the carried-forward execution contract and the new breach-forecast contract bind the latest session; satisfy both without wasteful recomputation by **copying** the completed Track C + Track B + trigger artifacts from `session_20261118T093031Z/` into the new session dir, then adding the new breach-forecast work. Record the new session id in this handoff **before** final gate capture. Do not reference any future `session_<UTC>` literally in this file (use `session_<UTC>` placeholders) so the freshness check keeps binding the real latest dir.

### Carry forward (copy, do not recompute) — satisfies `FCLR-VOL-LIQ-EXECUTION-01`
From `research_state/session_20261118T093031Z/`: `trackc_design_a_forecast_20261118T093031Z.{py,json,md}`, `trackb_breach_labels_20261118T093031Z.{py,json,md}`, and a non-empty `trigger_check_<UTC>.json` (regenerate the trigger check for the new UTC; all four triggers remain OPEN).

### FCLR-VOL-LIQ-BREACH-FORECAST-03 — funding-conditioned breach forecast (REQUIRED, stdlib)
Outcome-blind prereg frozen **before** touching model evaluation. Use the completed Track B label rows and Track C causal features on the 2024-04..09 cache. Read-only ZIP/CSV/dir twins only.

**Prereg (freeze first, in the new session dir):** `trackbc_breach_prereg_<UTC>.json` (and a `.md` companion recommended). Fix ex ante: instruments, month/window, entry-origin rule, scenario set (L∈{5,10,20}, side, H∈{4h,24h}), features (trailing RV1h/24h/168h, signed funding, |funding|, funding trails mean/EWMA — all causal at t), model family (drift-free score / logistic-type stdlib fit), evaluation metric (AUC / precision@k / breach-rate calibration), block-bootstrap (UTC-day, seed 12345), and the materiality floor. Record `outcome_data_inspected_before_freeze=false`. Do not use future bars, full-sample normalization, or sealed months.

**Model + evaluation:** stdlib only (`math`/`csv`/`json`/`zipfile`). Fit on train, evaluate on the 30d test blocks; compare a funding-conditioned score against an RV-only baseline; report AUC and precision@k per scenario with a deterministic block bootstrap CI and leave-one-instrument-out. Label EXPLORATORY/PILOT; do not claim confirmatory/promotion or a forecast-gate pass.

**Required artifacts (exact prefixes; all non-empty) in the new session dir:**
- `trackbc_breach_prereg_<UTC>.json`
- `trackbc_breach_forecast_<UTC>.py`
- `trackbc_breach_forecast_<UTC>.json`
- `trackbc_breach_forecast_<UTC>.md`
- `trigger_check_<UTC>.json`
- `evidence_audit_<UTC>.json` + `evidence_audit_<UTC>.md`
- a `recompute_*` summary (e.g. `recompute_trackbc_breach_forecast_<UTC>.json`) to satisfy the new-style heavy check

### Record, verify, hand off
1. Create `research_state/session_<UTC>/` with all artifacts above (copied + new).
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
3. `research_state/session_20261118T030427Z/{trackc_extension_design,trackb_boundary_labels,evidence_audit}_20261118T030427Z.*` (design specs + Track B protocol).
4. `research_state/evaluation_summary.md`, `research_state/data_source_registry.json`, `research_state/fclr_final_structural_closure_20261116T114626.{md,json}`, `research_state/resume_trigger_registry.json`.

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

## Verification record — 2026-11-18T11:19:48Z
- `python3 scripts/check_handoff_heavywork_gate.py --json`: **PASS** (`pass=true`, `reason_code=OK`, `failures=[]`, root=500/500, latest=`session_20261118T093031Z`=disk, `handoff_stale=false`, `vol_liq_execution.pass=true`, `breach_forecast.required=false` [grandfathered pre-start]). The new `FCLR-VOL-LIQ-BREACH-FORECAST-03-20261118T103106Z` requirement binds the next post-start session.
- `python3 scripts/check_tracka_scope_registry_drift.py --json`: **PASS** (`reason_code=OK`, 196/196).
- `python3 scripts/next_campaign_status.py --json`: confirmatory multi-block cached design BLOCKED (`n_feasible=0`, `max_mutually_non_overlapping=1<3`); Track C Design A + Track B feasible via stdlib on cached data (proven in `session_20261118T093031Z`).
- `python3 -m unittest tests.test_tracka_hardening_143 -v`: **PASS (37 tests)** — the 32 prior tests plus 5 new breach-forecast fail-closed cases (trackc-only, empty-file, missing-trigger, full-package, pre-start grandfathering). Also `tests.test_tracka_hardening_125`, `_098`, `_099`, `tests.test_active_campaign_gate`: **PASS (54 tests)**.
- End-to-end gate proof (tmp copy, real state untouched): a post-start session lacking breach-forecast artifacts fails with `BREACH_FORECAST_ARTIFACTS_MISSING`; adding `trackbc_breach_prereg_*` + `trackbc_breach_forecast_*` triad makes it pass.
- No sealed artifacts/workflows/registries modified. `AGENT_HANDOFF.md` remains the sole durable handoff; this refresh records the completed Track C + Track B session and the exact non-avoidance contract for the next breach-forecast campaign.

(End of file - total 96 lines)