# AGENT HANDOFF — 2026-11-18T14:24:09Z (SOLE DURABLE HANDOFF)

> **Authority:** this file only. Every other handoff-like file is tombstoned/historical and has no campaign authority. No duplicate `AGENT_HANDOFF*` exists under `research_state/`, `scripts/`, `tests/`, or `src/`.

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION (timestamped 2026-11-18T14:24:09Z)

**MANDATORY — do this first, do not idle/re-audit/gate-only/re-score sealed work:** create `research_state/session_<UTC>/` with UTC **strictly after** `20261118T132800Z` and execute **`FCLR-VOL-LIQ-ROBUST-05-20261118T132800Z`** (Track C sign-corrected multi-holdout robustness + placebo null, **stdlib-only**, cached/local data). Freeze the robust-05 prereg **before touching evaluation/outcomes**; then produce the required robust-05 prereg + robustness triad + trigger check + evidence audit + `recompute_*` (all **non-empty**) in that new session. Copy required carry-forward artifacts into the same session dir. Update this handoff's latest session id to the new session before final gate capture. If you do anything else instead of this heavy quantitative progress, the machine gate will fail the session closed.

**Repo priority (name = campaign):** `Funding-conditioned-volatility-and-liquidation-risk`
1. **Funding-conditioned volatility/stress forecasting (Track C, primary):** does funding predict future realized vol/stress vs RV-only? QLIKE/MAE/RMSE, leakage-resistant OOS. **Sign-corrected; QLIKE is a loss (lower is better).**
2. **Liquidation-boundary risk (Track B, secondary):** do funding-conditioned features predict modeled liquidation-boundary breaches?

**State:** `ACTIVE_CAMPAIGN` / gates green / bottlenecks cleared for the mandated next step. Latest completed heavy session: **`research_state/session_20261118T132800Z`** (`FCLR-VOL-LIQ-ROBUST-04`, EXPLORATORY/PILOT, **honest negative result + sign-inversion correction**). No newer unrecorded session on disk; no duplicate handoff authority; stale-handoff, empty-artifact, and audit/gate-only non-avoidance blockers remain closed.

**Critical sign correction (do not repeat the inverted claim):** `mean_delta_qlike_vs_A = mean(QLIKE_A − QLIKE_model)` and QLIKE is a loss, so `A − E > 0` means E is worse than RV-only. ROBUST-04 on 2024-09 holdout: mean QLIKE A = −6.1101 vs E = −6.0806, **A − E = −0.0294**, CI95 `[−0.0421, −0.0159]`, materiality floor **NOT met** (RV-only better). `session_20261118T093031Z` E=−0.3579 was likewise `A − E` (RV-only better). Correct claim: **RV-only outperforms funding-conditioned models on QLIKE** in tested cached holds.

**Program/campaign lineage:** parent `FCLR-VOL-LIQ-FORECAST-01-20261118T023259Z`. Completed: `FCLR-VOL-LIQ-EXECUTION-01-20261118T092338Z` (`session_20261118T093031Z`, Track C Design A + Track B modeled breach labels), `FCLR-VOL-LIQ-BREACH-FORECAST-03-20261118T103106Z` (`session_20261118T114500Z`, EXPLORATORY/PILOT negative), `FCLR-VOL-LIQ-ROBUST-04-20261118T120000Z` (`session_20261118T132800Z`, EXPLORATORY/PILOT negative + sign correction). **Active required next campaign:** `FCLR-VOL-LIQ-ROBUST-05-20261118T132800Z` (machine-enforced for any session after 132800Z). Rank-0 trigger state remains `FCLR-BOUNDED-TRIGGER-ONLY-20261115T220000Z` (`TRIGGER_ONLY`, `next_action_heavy=null`); all reopen triggers OPEN/none fired.

### Constraints / feasibility (verified 2026-11-18T14:24:09Z)
- **Confirmatory multi-block cached design:** infeasible in all domains (`python3 scripts/next_campaign_status.py --json` → `any_feasible=false`; contiguous runs too short; disjoint 30d blocks `n_feasible=0`; mark+funding-only `max_mutually_non_overlapping=1 < 3`; Hyperliquid exhausted). Certified closed — do not re-open without a machine-satisfied trigger.
- **Allowed path:** stdlib exploratory/pilot work on admissible cached/local data only (`research_state/data_cache/`, `data/raw/`, ZIP/CSV/JSON/dir twins). **No network, no parquet engine, no `git lfs pull`, no installs, no new root `research_state/*.md|json`** (root **498/500** at cap) — write all new artifacts under the session subdir.
- **Environment:** `numpy/pandas/scipy` absent; do not wait for them. Implement stdlib (`math/csv/json/zipfile`) and label EXPLORATORY/PILOT. Full `unittest discover` may hang; run targeted bounded tests and record limitation.

### Gates (current)
- `python3 scripts/check_handoff_heavywork_gate.py --json`: **PASS** (`reason_code=OK`, `handoff_stale=false`, root 498/500). Binds completed ROBUST-04/BREACH/EXECUTION campaigns and declares ROBUST-05 (grandfathered for latest session == start; **next post-start session must emit robust-05 artifacts or fail closed**).
- `python3 scripts/check_tracka_scope_registry_drift.py --json`: **PASS** (`OK`, 196/196).
- `python3 scripts/next_campaign_status.py --json`: confirmatory blocked; Track C/B stdlib exploratory feasible on cached data.
- `python3 -m unittest tests.test_tracka_hardening_143 -v`: **PASS**. `python3 -m unittest tests.test_tracka_hardening_125 -v`: **PASS**.

## Next focus campaign — REQUIRED heavy-work (machine-enforced)

**`FCLR-VOL-LIQ-ROBUST-05-20261118T132800Z` — Track C sign-corrected multi-holdout robustness + placebo null (stdlib, cached data).**

**Research question:** under the correct QLIKE sign convention (lower is better), does **any** funding-conditioned model (B/C/D/E) beat RV-only (A) across **multiple chronological holdouts** (2024-06, 2024-07, 2024-08, 2024-09), each with expanding train ending 7 days before holdout start and 7d purge/embargo? Does a **placebo** (deterministic permutation of funding history, seed 12345) produce a null centered near zero?

**Execution discipline:** freeze prereg before any metric computation; do not stop at audit/gate/test-only work. If blocked by code/environment, still create session dir + prereg + script + partial JSON/MD documenting the exact blocker with **non-empty** evidence in the same session (never empty files).

**Prereg (freeze first):** `fclr_robust05_prereg_<UTC>.json` + `.md`. Fix ex ante: instruments, holdouts {2024-06,2024-07,2024-08,2024-09}, expanding-train rule (train ends 7d before holdout start; embargo 7d), features (lrv1/lrv24/lrv168/fund/fund_abs/fmean/fewma, causal at t), model family (stdlib OLS HAR, Duan smearing), metric (ΔQLIKE = mean QLIKE_A − QLIKE_model vs RV-only; MAE, RMSE), block bootstrap (UTC-day, seed 12345, 2000 reps), LOIO, placebo construction (deterministic funding permutation, seed 12345), materiality floor. Record `outcome_data_inspected_before_freeze=false`. No future bars, no full-sample normalization, no sealed months.

**Models/eval (stdlib only):** for each holdout fit on expanding train, evaluate on holdout month; report per-holdout and pooled funding-trail ΔQLIKE (correct sign) with bootstrap CI95 and LOIO; run placebo and report its ΔQLIKE distribution.

**Materiality floor (correct sign):** E beats A (`mean QLIKE_A − QLIKE_E > 0`, bootstrap CI95 lower bound > 0) in **≥3 of 4** holdouts, **and** real funding-trail `|mean ΔQLIKE|` exceeds placebo `|mean ΔQLIKE|`. Otherwise report honest negative result.

**Required artifacts (exact prefixes; all non-empty) in new `research_state/session_<UTC>/` (UTC > 20261118T132800Z):**
- `fclr_robust05_prereg_<UTC>.json`
- `fclr_robust05_prereg_<UTC>.md`
- `fclr_robust05_robustness_<UTC>.py`
- `fclr_robust05_robustness_<UTC>.json`
- `fclr_robust05_robustness_<UTC>.md`
- `trigger_check_<UTC>.json`
- `evidence_audit_<UTC>.json` + `evidence_audit_<UTC>.md`
- a `recompute_*` summary (e.g. `recompute_fclr_robust05_robustness_<UTC>.json`)

**Carry forward (copy, do not recompute) into the new session dir (all non-empty):** from `session_20261118T132800Z` — `trackc_design_a_forecast_*.{py,json,md}`, `trackb_breach_labels_*.{py,json,md}`, `trackbc_breach_prereg_*.json`, `trackbc_breach_forecast_*.{py,json,md}`, `fclr_robust04_prereg_*.{json,md}`, `fclr_robust04_robustness_*.{py,json,md}`.

### Record, verify, hand off
1. Create `research_state/session_<UTC>/` (UTC after 132800Z) with all artifacts above.
2. Update this handoff's **latest session id** to the new session before final gate capture.
3. Run targeted tests only (bounded): `python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_125 -v`.
4. Re-run gates and record exact outcomes: `python3 scripts/check_handoff_heavywork_gate.py --json`, `python3 scripts/check_tracka_scope_registry_drift.py --json`, `python3 scripts/next_campaign_status.py --json`.
5. Update only `AGENT_HANDOFF.md` and the new session directory. No sealed artifacts/closure JSON/registries/.github/workflows modified.

## Read first
1. `RESEARCH_PROMPT.md` §1–§6, §16–§17.
2. `research_state/session_20261118T132800Z/{fclr_robust04_prereg,fclr_robust04_robustness,evidence_audit,trigger_check,recompute_fclr_robust04_robustness}_20261118T132800Z.*` (ROBUST-04 + sign audit).
3. `research_state/session_20261118T093031Z/{trackc_design_a_forecast,trackb_breach_labels,evidence_audit,trigger_check}_20261118T093031Z.*` (Track C/B carried forward).
4. `research_state/session_20261118T114500Z/{trackbc_breach_prereg,trackbc_breach_forecast,evidence_audit,trigger_check}_20261118T114500Z.*` (breach-forecast carried forward).
5. `research_state/evaluation_summary.md`, `research_state/data_source_registry.json`, `research_state/fclr_final_structural_closure_20261116T114626.{md,json}`, `research_state/resume_trigger_registry.json`.

## Prohibitions
- Do not re-run/re-score sealed cached-data confirmatory estimands or sealed results (FCLR-014, replication synthesis, design-frontier certs, FCLR-013/010/002/003/009/006/008, frontier verify-06/07/08+, sealed 19.04%).
- No polling/HF re-probe, no paid/credentialed/manual outcome data, no network installs/fetches, no `git lfs pull`.
- No mutation of sealed artifacts/closure JSON/`.github/workflows/*`; no root-level `research_state/*.md|json` (500/500 cap); no duplicate `AGENT_HANDOFF*` files.
- No `statsmodels` or unpinned heavy deps in core path. Do not run parquet-only scripts without a CSV/JSON/ZIP twin.
- Do not treat missing-numpy/environmental discovery errors as green. Never inspect outcomes while producing outcome-blind preregs. **Never emit empty/zero-byte artifacts.**
- **Do not repeat the sign-inverted "funding-trail improves QLIKE" claim.** QLIKE is a loss; lower is better.
- Do not leave a session recorded in this handoff without its required execution artifacts present and non-empty on disk.

## Reopen triggers (machine-checkable — all OPEN)
- `GATE4_BRANCH_1`: `research_state/fclr016_v5_terms_evidence_RESOLVED_*.json` (`status=RESOLVED_VERIFIED`, `fabricated=false`).
- `NEW_OBSERVED_LIQUIDATION_SOURCE`: `research_state/<source>_admissibility_audit_<UTC>.{md,json}` (`status=ADMISSIBLE`, `observed_labels=true`, ≥5 instruments, ≥3 blocks or ≥1 complete month).
- `HL_LABEL_EXTENSION`: `research_state/hl_label_extension_audit_<UTC>.{md,json}` (post-2026-10-31 observed ironflow labels, ≥100-day depth).
- `EXPANSION_ROBUSTNESS_REDO`: `research_state/expansion_robustness_redo_prereg_<UTC>.json` + evaluation summary (LOIO≥6/8 AND placebo>95th null).

## Verification record — 2026-11-18T14:24:09Z (handoff refresh)
- `python3 scripts/check_handoff_heavywork_gate.py --json`: **PASS** — `pass=true`, `reason_code=OK`, `handoff_stale=false`, `root_count=498/500`, latest `session_20261118T132800Z`; `robust_04`, `breach_forecast`, `vol_liq_execution` PASS; `robust_05` declared but not yet required for latest session (start == latest → grandfathered). **Next post-start session must satisfy robust-05 artifacts or fail closed.**
- `python3 scripts/check_tracka_scope_registry_drift.py --json`: **PASS** (`reason_code=OK`, 196/196).
- `python3 scripts/next_campaign_status.py --json`: confirmatory multi-block cached design **BLOCKED** (`any_feasible=false`); stdlib exploratory Track C/B feasible on cached data.
- Targeted tests: `python3 -m unittest tests.test_tracka_hardening_143 -v` **PASS** (37 tests); `python3 -m unittest tests.test_tracka_hardening_125 -v` **PASS**. Full `unittest discover` environmental/hanging in this runtime (not a green full suite).
- Bottleneck check: **no blocking bottleneck for mandated next campaign** — sole durable handoff (`AGENT_HANDOFF.md`), no duplicates, latest disk session == latest handoff session (`session_20261118T132800Z`), required prior artifacts present/non-empty, gates/tests green, root at cap handled by session-subdir-only rule. Sign-inversion corrected and flagged. Confirmatory multi-block remains infeasible by data (closed) and does not block `FCLR-VOL-LIQ-ROBUST-05`.
- Action taken: refreshed sole durable handoff with timestamped mandatory initial task message for next session (`FCLR-VOL-LIQ-ROBUST-05`), reconfirmed gate/test state, and cleared no additional blockers. No sealed artifacts, workflows, or registries modified.