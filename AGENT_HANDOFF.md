# AGENT HANDOFF — 2026-11-18T13:31:00Z (SOLE DURABLE HANDOFF)

> **Authority:** this file only. Every other handoff-like file is tombstoned/historical and has no campaign authority. No duplicate `AGENT_HANDOFF*` exists under `research_state/`, `scripts/`, `tests/`, or `src/`.

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION (timestamped 2026-11-18T13:31:00Z)

**MANDATORY — do this first, do not idle/re-audit/gate-only:** create `research_state/session_<UTC>/` (UTC **after** `20261118T132800Z`) and execute **`FCLR-VOL-LIQ-ROBUST-05-20261118T132800Z`** (Track C sign-corrected multi-holdout robustness + placebo null, stdlib-only, cached data). Freeze the prereg before touching evaluation; produce the required robust-05 prereg + robustness triad + trigger check + evidence audit + `recompute_*` (all non-empty); record the new session id in this handoff before final gate capture. If you do anything else instead of heavy quantitative progress, the machine gate will fail the session closed.

**CRITICAL FINDING FROM THE PREVIOUS SESSION (`session_20261118T132800Z`, FCLR-VOL-LIQ-ROBUST-04):** the prior Track C headline was a **SIGN INVERSION**. The script defines `mean_delta_qlike_vs_A = mean(QLIKE_A − QLIKE_model)` and QLIKE is a **loss (lower is better)**. Therefore `E = −0.3579` in `session_20261118T093031Z` means `A − E = −0.3579`, i.e. **RV-only has LOWER QLIKE and the funding-trail model is WORSE by 0.3579** — not an improvement. ROBUST-04 on the 2024-09 holdout confirms it: `mean QLIKE A = −6.1101` vs `E = −6.0806`, `A − E = −0.0294`, CI95 `[−0.0421, −0.0159]`, materiality floor **NOT met**. **Do not repeat the inverted claim.** The next campaign must re-evaluate with the correct sign and a placebo null.

**CAMPAIGN STATUS CONFIRMED:** `python3 scripts/next_campaign_status.py --json` → **no feasible 3-block design in ANY domain** (Binance 5-symbol contiguous: exhausted; disjoint blocks: n_feasible=0; mark+funding-only: max_non_overlap=1 < 3; Hyperliquid bulk: exhausted; Hyperliquid extended: exhausted). The confirmatory multi-block campaign is CERTIFIED CLOSED. Only stdlib exploratory work (Track C/B) on cached data remains feasible — exactly the `FCLR-VOL-LIQ-ROBUST-05` mandate.

**Repo (P0):** `Funding-conditioned-volatility-and-liquidation-risk` — the repo name *is* the campaign. Two named risks, in this priority order:
1. **Funding-conditioned volatility/stress forecasting (Track C):** does funding predict future realized vol / stress vs an RV-only baseline? QLIKE/MAE/RMSE, leakage-resistant OOS. **Sign-corrected; lower QLIKE is better.**
2. **Liquidation-boundary risk (Track B):** do funding-conditioned features predict modeled liquidation-boundary breaches?

Use only admissible local/public data already on disk (ZIP/CSV/JSON/dir twins under `research_state/data_cache/` and `data/raw/`). **No network, no parquet engine, no `git lfs pull`, no installs, no new root `research_state/*.md|json` (root 500/500 at cap).**

**State: `ACTIVE_CAMPAIGN` / GATE GREEN, BOTTLENECKS CLEARED.** Latest completed heavy session: **`research_state/session_20261118T132800Z`** (FCLR-VOL-LIQ-ROBUST-04 executed: stdlib Track C funding-trail QLIKE robustness on the 2024-09 alternative holdout, sign-corrected, honest negative result + sign-inversion finding; Track C, Track B and breach-forecast artifacts carried forward). No newer unrecorded session exists; no duplicate handoff authority; stale/incomplete/unrecorded-session, empty-session-bypass, and audit/gate-only non-avoidance blockers are closed. Next session must produce new heavy work under `FCLR-VOL-LIQ-ROBUST-05`.

**Program lineage:** parent `FCLR-VOL-LIQ-FORECAST-01-20261118T023259Z`. Completed execution campaign: `FCLR-VOL-LIQ-EXECUTION-01-20261118T092338Z` (Track C Design A stdlib forecast + Track B modeled breach labels — both delivered in `session_20261118T093031Z`). Completed breach-forecast campaign: `FCLR-VOL-LIQ-BREACH-FORECAST-03-20261118T103106Z` (joined Track C features + Track B labels; executed in `session_20261118T114500Z`, EXPLORATORY/PILOT, honest negative result — funding-conditioned features did NOT improve modeled breach discrimination; materiality floor NOT met). Completed robustness campaign: `FCLR-VOL-LIQ-ROBUST-04-20261118T120000Z` (executed in `session_20261118T132800Z`, EXPLORATORY/PILOT, honest negative result + **sign-inversion correction**). **Active next focus campaign: `FCLR-VOL-LIQ-ROBUST-05-20261118T132800Z`** (sign-corrected multi-holdout Track C robustness + placebo null; see Next Focus Campaign section). Rank-0 trigger state remains `FCLR-BOUNDED-TRIGGER-ONLY-20261115T220000Z` (`TRIGGER_ONLY`, `next_action_heavy=null`); all triggers OPEN, none fired.

### Gates (verify first — CURRENT STATE: ALL PASS)
- `python3 scripts/check_handoff_heavywork_gate.py --json`: **pass=true**, `handoff_stale=false`, root=500/500 (at cap). Binds `FCLR-VOL-LIQ-ROBUST-04-20261118T120000Z` (satisfied by `session_20261118T132800Z` robust-04 triad + trigger check), the prior `FCLR-VOL-LIQ-BREACH-FORECAST-03` and `FCLR-VOL-LIQ-EXECUTION-01` (carried forward), and the next focus campaign `FCLR-VOL-LIQ-ROBUST-05-20261118T132800Z` (start = current latest session → grandfathered; **any session after 132800Z must emit the robust-05 prereg + robustness triad + trigger check or fail closed**). Audit-only, empty-file, and gate-only sessions fail closed.
- `python3 scripts/check_tracka_scope_registry_drift.py --json`: **PASS** (`reason_code=OK`, 196/196).
- `python3 scripts/next_campaign_status.py --json`: confirmatory multi-block cached design remains **BLOCKED** (contiguous runs too short; disjoint 30-day blocks `n_feasible=0`; `max_mutually_non_overlapping=1 < 3`). Ready funding-backed cache months: 2024-04, 2024-05, 2025-01. No actionable frozen preregs. Track C single-window Design A and Track B remain feasible via stdlib on cached data (proven by `session_20261118T093031Z`, `session_20261118T114500Z`, `session_20261118T132800Z`).
- `python3 -m unittest tests.test_tracka_hardening_143 -v`: **PASS** (handoff + heavy-work + campaign gates, incl. the robust-05 fail-closed coverage). Full `unittest discover` remains environmental/hanging in this runtime; use targeted tests and record that limitation, not a green full suite.

### Bottlenecks resolved in this handoff (2026-11-18T13:31:00Z)
- **Sign-inversion bottleneck in the prior Track C headline (CLEARED / CORRECTED):** `session_20261118T093031Z` reported `E = −0.3579` as an "improvement" while its own `mean_delta_qlike_vs_A = mean(QLIKE_A − QLIKE_E)`; since QLIKE is a loss (lower is better), the negative value means RV-only is better and E is worse. `session_20261118T132800Z` (ROBUST-04) re-ran the estimand on the 2024-09 holdout with the correct sign and confirmed RV-only wins (`A − E = −0.0294`, CI95 `[−0.0421, −0.0159]`). The inverted claim is now explicitly flagged in `evidence_audit` and `sign_audit` and must not be repeated.
- **Latest-session / handoff freshness (CLEARED):** `session_20261118T132800Z` is recorded in this handoff and carries the complete carried-forward bundle (Track C + Track B + breach-forecast + trigger check) plus the robust-04 triad, evidence audit and fresh recompute. `latest_disk_session == latest_handoff_session == session_20261118T132800Z` → `handoff_stale=false`.
- **Empty-session bypass (still closed):** campaign gates reject zero-byte required artifacts by name and size; empty placeholders can never satisfy the heavy-work contract.
- **Audit-only / gate-only non-avoidance (closed):** the `FCLR-VOL-LIQ-ROBUST-04` and `FCLR-VOL-LIQ-ROBUST-05` campaigns require their prereg + robustness triad + trigger check + evidence audit in the latest post-start session, not a generic recompute.
- **Estimand-execution blocker (`numpy`/`pandas`/`scipy` absent, installs prohibited):** remains an environment constraint, not a data/design constraint. Do not wait for numpy. Implement the stdlib fallback (`math`/`csv`/`json`/`zipfile`) and label results EXPLORATORY/PILOT.

### Progress recorded at 2026-11-18T13:28:00Z (`session_20261118T132800Z`, read-only cache, no network)
- **Track C — FCLR-VOL-LIQ-ROBUST-04 alternative-holdout robustness (COMPLETE, EXPLORATORY/PILOT):** stdlib OLS HAR, 5 instruments (BTC/ETH/SOL/XRP/BNB), train 2024-04..08 (2024-04-01..2024-08-24), 7d purge/embargo (2024-08-25..2024-08-31), holdout test 2024-09-01..2024-09-30, 2000-rep UTC-day block bootstrap (seed 12345), LOIO. **Result (correct sign):** mean QLIKE A_rv_only = −6.1101, E_rv_funding_trails = −6.0806; **A − E = −0.0294 (E is WORSE)**, bootstrap CI95 `[−0.0421, −0.0159]`, materiality floor (A − E > 0, CI95 lower > 0) **NOT met**. Funding-trail features do **not** improve QLIKE on 2024-09. This is the honest, sign-corrected result.
- **Sign audit:** `session_20261118T093031Z` `E=−0.3579` is `A − E`, i.e. RV-only better by 0.3579 in every split (split means `A−E` = −0.1120, −0.2217, −0.7401). The prior "funding-trail improves QLIKE" claim is a sign inversion. Corrected claim: **RV-only outperforms funding-conditioned models on QLIKE**.
- **Track B (carried forward, `session_20261118T093031Z`):** synthetic modeled boundary-breach labels, 41,760 rows, 1,418 breached, 3.40% overall; `observed_liquidation_labels=false`.
- **Breach forecast (carried forward, `session_20261118T114500Z`):** pooled mean ΔAUC (funding-conditioned − RV-only) = −0.0661; materiality floor NOT met; honest negative result.

## Next focus campaign — REQUIRED heavy-work (non-avoidable; machine-enforced by gate)

**`FCLR-VOL-LIQ-ROBUST-05-20261118T132800Z` — Track C sign-corrected multi-holdout robustness + placebo null (stdlib, cached data). MUST be executed in the next post-start session (UTC after 20261118T132800Z).**
Research question: under the **correct QLIKE sign convention (lower is better)**, does **any** funding-conditioned model (B/C/D/E) beat RV-only (A) across **multiple chronological holdouts** (2024-06, 2024-07, 2024-08, 2024-09), each with an expanding train ending 7 days before the holdout month and a 7d purge/embargo, and does a **placebo** (funding-trail features replaced by a deterministic permutation of the funding history, seed 12345) produce a null centered near zero? This directly resolves the sign inversion found in ROBUST-04.

**Execution discipline (to prevent avoidance):** freeze prereg before any metric computation; do not stop at audit/gate/test-only work; if blocked by code/environment, create the session dir + prereg + script + partial JSON/MD documenting the exact blocker with non-empty evidence in the same session (never an empty file). Root `research_state/` is at 500/500 — all new artifacts go in the session subdir only.

**Prereg (freeze first, before touching evaluation):** `fclr_robust05_prereg_<UTC>.json` (+ `.md` companion). Fix ex ante: instruments, holdout months {2024-06, 2024-07, 2024-08, 2024-09}, expanding train rule (train ends 7d before holdout start; embargo 7d), feature set (lrv1/lrv24/lrv168/fund/fund_abs/fmean/fewma, causal at t), model family (stdlib OLS HAR, Duan smearing), metric (ΔQLIKE = mean QLIKE_A − QLIKE_model vs RV-only, MAE, RMSE), block bootstrap (UTC-day, seed 12345, 2000 reps), leave-one-instrument-out, placebo construction (deterministic funding permutation, seed 12345), materiality floor. Record `outcome_data_inspected_before_freeze=false`. No future bars, no full-sample normalization, no sealed months.

**Model + evaluation:** stdlib only (`math`/`csv`/`json`/`zipfile`). For each holdout: fit on expanding train, evaluate on the holdout month; report per-holdout and pooled funding-trail ΔQLIKE (correct sign) with bootstrap CI95 and LOIO; run the placebo and report its ΔQLIKE distribution.

**Materiality floor (correct sign):** E beats A (`mean QLIKE_A − QLIKE_E > 0`, bootstrap CI95 lower bound > 0) in **at least 3 of 4** holdouts, **and** the real funding-trail |mean ΔQLIKE| exceeds the placebo |mean ΔQLIKE|. If not met, report the honest negative result.

**Required artifacts (exact prefixes; all non-empty) in the new `research_state/session_<UTC>/` dir (UTC after campaign start 132800Z):**
- `fclr_robust05_prereg_<UTC>.json`
- `fclr_robust05_prereg_<UTC>.md`
- `fclr_robust05_robustness_<UTC>.py`
- `fclr_robust05_robustness_<UTC>.json`
- `fclr_robust05_robustness_<UTC>.md`
- `trigger_check_<UTC>.json`
- `evidence_audit_<UTC>.json` + `evidence_audit_<UTC>.md`
- a `recompute_*` summary (e.g. `recompute_fclr_robust05_robustness_<UTC>.json`) to satisfy the new-style heavy check

**Carry forward (copy, do not recompute) into the new session dir:** `trackc_design_a_forecast_*.{py,json,md}`, `trackb_breach_labels_*.{py,json,md}`, `trackbc_breach_prereg_*.json`, `trackbc_breach_forecast_*.{py,json,md}`, `fclr_robust04_prereg_*.{json,md}`, `fclr_robust04_robustness_*.{py,json,md}` (from `session_20261118T132800Z`). All carried-forward files must remain non-empty.

### Record, verify, hand off
1. Create `research_state/session_<UTC>/` (UTC after 132800Z) with all artifacts above (copied + new robust-05 work).
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
2. `research_state/session_20261118T132800Z/{fclr_robust04_prereg,fclr_robust04_robustness,evidence_audit,trigger_check,recompute_fclr_robust04_robustness}_20261118T132800Z.*` (executed ROBUST-04 + sign audit + audit).
3. `research_state/session_20261118T093031Z/{trackc_design_a_forecast,trackb_breach_labels,evidence_audit,trigger_check}_20261118T093031Z.*` (carried-forward Track C + Track B + audit).
4. `research_state/session_20261118T114500Z/{trackbc_breach_prereg,trackbc_breach_forecast,evidence_audit,trigger_check}_20261118T114500Z.*` (carried-forward breach-forecast campaign + audit).
5. `research_state/evaluation_summary.md`, `research_state/data_source_registry.json`, `research_state/fclr_final_structural_closure_20261116T114626.{md,json}`, `research_state/resume_trigger_registry.json`.

## Prohibitions
- Do not re-run sealed cached-data confirmatory estimands or re-score sealed results (FCLR-014, replication synthesis, design-frontier certs, FCLR-013/010/002/003/009/006/008, frontier verify-06/07/08+, sealed 19.04%).
- No polling/HF re-probe, no paid/credentialed/manual outcome data, no network installs/fetches, no `git lfs pull`.
- No mutation of sealed artifacts/closure JSON/`.github/workflows/*`; no root-level `research_state/*.md|json` (root 500/500 cap); no duplicate `AGENT_HANDOFF*` files.
- No `statsmodels` or unpinned heavy deps in core path. Do not run parquet-only scripts without a CSV/JSON/ZIP twin.
- Do not treat missing-numpy/environmental discovery errors as green. Never inspect outcomes while producing outcome-blind preregs. **Do not emit empty/zero-byte artifacts; content is mandatory.**
- **Do not repeat the sign-inverted "funding-trail improves QLIKE" claim.** QLIKE is a loss; lower is better; the prior E=−0.3579 is RV-only better by 0.3579.
- Do not leave a session recorded in this handoff without its required execution artifacts present and non-empty on disk.

## Reopen triggers (machine-checkable — all OPEN)
- `GATE4_BRANCH_1`: `research_state/fclr016_v5_terms_evidence_RESOLVED_*.json` (`status=RESOLVED_VERIFIED`, `fabricated=false`).
- `NEW_OBSERVED_LIQUIDATION_SOURCE`: `research_state/<source>_admissibility_audit_<UTC>.{md,json}` (`status=ADMISSIBLE`, `observed_labels=true`, ≥5 instruments, ≥3 blocks or ≥1 complete month).
- `HL_LABEL_EXTENSION`: `research_state/hl_label_extension_audit_<UTC>.{md,json}` (post-2026-10-31 observed ironflow labels, ≥100-day depth).
- `EXPANSION_ROBUSTNESS_REDO`: `research_state/expansion_robustness_redo_prereg_<UTC>.json` + evaluation summary (LOIO≥6/8 AND placebo>95th null).

## Verification record — 2026-11-18T13:31:00Z (refresh)
- `python3 scripts/check_handoff_heavywork_gate.py --json`: **PASS** — `pass=true`, `reason_code=OK`, `handoff_stale=false`, `root_count=500/500`, latest `session_20261118T132800Z`; `robust_04`, `breach_forecast` and `vol_liq_execution` PASS; `robust_05` not yet required for this latest session (start == latest session → grandfathered) — **next post-start session must satisfy robust-05 artifacts or fail closed**.
- `python3 scripts/check_tracka_scope_registry_drift.py --json`: **PASS** (`reason_code=OK`, 196/196).
- `python3 scripts/next_campaign_status.py --json`: confirmatory multi-block cached design **BLOCKED** (`any_feasible=false`); Track C/B stdlib exploratory path remains feasible on cached data.
- `python3 -m unittest tests.test_tracka_hardening_143 -v`: **PASS** (handoff + heavy-work + campaign gates, including robust-05 fail-closed coverage). `python3 -m unittest tests.test_tracka_hardening_125 -v`: **PASS**. Full `unittest discover` remains environmental/hanging in this runtime; record limitation, not a green full suite.
- Bottlenecks: **none blocking next campaign** — sole durable handoff confirmed (no duplicates), no unrecorded/newer session beyond `session_20261118T132800Z`, required artifacts non-empty, gates/tests green. The prior Track C sign inversion is corrected and flagged. Remaining constraints (root 500/500 cap, numpy/pandas/scipy absent, confirmatory multi-block infeasible) are documented and handled by the stdlib/session-dir exploratory workflow.
- Action taken: executed `FCLR-VOL-LIQ-ROBUST-04` (sign-corrected alternative-holdout robustness) in `session_20261118T132800Z`; corrected the prior sign-inverted headline; declared and machine-enforced `FCLR-VOL-LIQ-ROBUST-05`; refreshed the timestamped initial task message. No sealed artifacts/workflows/registries modified.