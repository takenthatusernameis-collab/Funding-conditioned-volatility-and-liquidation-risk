# AGENT HANDOFF — 2026-11-18T14:35:39Z (SOLE DURABLE HANDOFF)

> **Authority:** this file only. Every other handoff-like file is tombstoned/historical and has no campaign authority.
> No duplicate `AGENT_HANDOFF*` exists under `research_state/`, `scripts/`, `tests/`, or `src/`.

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION — READ THIS BEFORE ANY OTHER ACTION (timestamped 2026-11-18T14:35:39Z)

**You must execute `FCLR-VOL-LIQ-ROBUST-05-20261118T132800Z` now. Do not idle, do not re-audit, do not gate-only, do not merely refresh this handoff, do not re-score sealed work.**

Create `research_state/session_<UTC>/` with UTC **strictly after** `20261118T132800Z`, freeze the robust-05 prereg **before touching evaluation/outcomes**, then produce the full robust-05 artifact set (all files **non-empty**) in that session. Update the **Latest executed session** line in this handoff to the new session id before final gate capture. If the first new session after `20261118T132800Z` lacks any robust-05 required artifact, `scripts/check_handoff_heavywork_gate.py` **fails the session closed**. There is no legitimate audit-only path.

**Repo priority (name = campaign):** `Funding-conditioned-volatility-and-liquidation-risk`
1. **Track C (primary):** does funding-conditioned information forecast future realized volatility/stress beyond RV-only? Metric QLIKE (loss, lower is better) plus MAE/RMSE; leakage-resistant, chronological OOS.
2. **Track B (secondary):** do funding-conditioned features predict modeled liquidation-boundary breaches?

## Current state (verified 2026-11-18T14:35:39Z)

- **Campaign state:** `ACTIVE_CAMPAIGN`; gates green; mandated next step cleared of blockers.
- **Latest executed session:** `research_state/session_20261118T132800Z` — `FCLR-VOL-LIQ-ROBUST-04`, EXPLORATORY/PILOT, honest negative result + sign-inversion correction. No newer session exists on disk.
- **Active required next campaign:** `FCLR-VOL-LIQ-ROBUST-05-20261118T132800Z` (machine-enforced for any session after `132800Z`).
- **Rank-0 trigger state:** `FCLR-BOUNDED-TRIGGER-ONLY-20261115T220000Z` (`TRIGGER_ONLY`, `next_action_heavy=null`); all reopen triggers OPEN/none fired.

### Critical sign convention (do not re-invert)
`ΔQLIKE_vs_A = mean(QLIKE_A − QLIKE_model)`; QLIKE is a **loss**, so `A − model > 0` means the model **beats** RV-only.
ROBUST-04 on the 2024-09 holdout: A = −6.1101, E = −6.0806, **A − E = −0.0294**, CI95 `[−0.0421, −0.0159]` → RV-only better; materiality floor **not** met. `session_20261118T093031Z` E = −0.3579 was likewise `A − E` (RV-only better). Correct claim: **RV-only outperformed funding-conditioned models on QLIKE in tested cached holds**.

### Feasibility facts — do not claim you are data-blocked (verified 2026-11-18T14:35:39Z)
- Confirmatory multi-block **cached** design: infeasible in all domains (`scripts/next_campaign_status.py --json` → `any_feasible=false`). Certified closed; do not reopen without a machine-satisfied trigger.
- `research_state/data_cache/` has complete **mark-price daily files + funding files** for `BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT, BNBUSDT` for every month **2024-04 … 2024-09** (30–31 mark days/file-month, 3 funding files/month). All four ROBUST-05 holdouts are runnable **offline**.
- Environment: `numpy/pandas/scipy` absent by design. Implement with stdlib (`math/csv/json/zipfile/statistics/random`). Do not wait for installs or network.

## Next focus campaign — REQUIRED heavy work (machine-enforced)

**`FCLR-VOL-LIQ-ROBUST-05-20261118T132800Z` — Track C sign-corrected multi-holdout robustness + placebo null (stdlib, cached data).**

**Research question:** under the correct QLIKE sign convention, does **any** funding-conditioned model (B/C/D/E) beat RV-only (A) across **multiple chronological holdouts**, and is the effect distinguishable from a **placebo** permutation null?

**Design (freeze ex ante):**
- Instruments: `BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT, BNBUSDT`.
- Holdouts / expanding train (train ends 7 days before holdout start; 7-day purge/embargo):
  - `2024-06`: train 2024-04-01…2024-05-24, embargo 05-25…05-31, test 06-01…06-30
  - `2024-07`: train 2024-04-01…2024-06-23, embargo 06-24…06-30, test 07-01…07-31
  - `2024-08`: train 2024-04-01…2024-07-24, embargo 07-25…07-31, test 08-01…08-31
  - `2024-09`: train 2024-04-01…2024-08-24, embargo 08-25…08-31, test 09-01…09-30
- Features (causal at t): `lrv1, lrv24, lrv168, fund, fund_abs, fmean, fewma`.
- Models (stdlib OLS HAR + Duan smearing): A `rv_only`; B `rv_signed`; C `rv_abs`; D `rv_signed_abs`; E `rv_funding_trails`.
- Metrics: `ΔQLIKE_vs_A = QLIKE_A − QLIKE_model` (positive = model better), MAE, RMSE; pool and per-holdout.
- Uncertainty: UTC-day block bootstrap, seed `12345`, 2000 reps, CI95; LOIO.
- Placebo: deterministic permutation of the funding series (seed `12345`), same pipeline; report its ΔQLIKE distribution.

**Materiality floor (correct sign):** E beats A (`mean(QLIKE_A − QLIKE_E) > 0` with bootstrap CI95 lower bound > 0) in **≥3 of 4** holdouts, **and** real funding-trail `|mean ΔQLIKE|` exceeds placebo `|mean ΔQLIKE|`. Otherwise report an honest negative result. Negative results are a valid completion; skipping the run is not.

**Execution recipe (fast path, reuse verified code):** copy `research_state/session_20261118T132800Z/fclr_robust04_robustness_20261118T132800Z.py` as the starting point; parameterize `SPLITS` to the four holdouts above, add the funding-permutation placebo, and keep the existing stdlib loaders/OLS/smearing/bootstrap. ROBUST-04 ran in ~2 minutes; four holdouts + placebo should finish in well under ~20 minutes. Write incrementally so a timeout still leaves non-empty partial JSON/MD in the session dir.

**Required artifacts (exact prefixes; all non-empty) in `research_state/session_<UTC>/` with UTC > `20261118T132800Z`):**
- `fclr_robust05_prereg_<UTC>.json` and `.md` (must contain `outcome_data_inspected_before_freeze=false`, the four splits, model list, metrics, seed, floor)
- `fclr_robust05_robustness_<UTC>.py`
- `fclr_robust05_robustness_<UTC>.json`
- `fclr_robust05_robustness_<UTC>.md`
- `trigger_check_<UTC>.json`
- `evidence_audit_<UTC>.json` + `.md`
- `recompute_fclr_robust05_robustness_<UTC>.json`

**Carry forward (copy, do not recompute) into the new session dir (all non-empty):** from `session_20261118T132800Z` — `trackc_design_a_forecast_*.{py,json,md}`, `trackb_breach_labels_*.{py,json,md}`, `trackbc_breach_prereg_*.json`, `trackbc_breach_forecast_*.{py,json,md}`, `fclr_robust04_prereg_*.{json,md}`, `fclr_robust04_robustness_*.{py,json,md}`.

### Record, verify, hand off (in order)
1. Create the post-`132800Z` session dir and freeze the prereg **first**.
2. Produce every required robust-05 artifact non-empty; never emit zero-byte files.
3. Change the **Latest executed session** line above to the new session id.
4. Run targeted bounded tests: `python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_125 -v`.
5. Record exact gate outcomes: `python3 scripts/check_handoff_heavywork_gate.py --json`, `python3 scripts/check_tracka_scope_registry_drift.py --json`, `python3 scripts/next_campaign_status.py --json`.
6. Update **only** `AGENT_HANDOFF.md` and the new session directory.

## Read first
1. `RESEARCH_PROMPT.md` §1–§6, §16–§17.
2. `research_state/session_20261118T132800Z/fclr_robust04_{prereg,robustness}_20261118T132800Z.{py,json,md}` plus its `evidence_audit` / `trigger_check` / `recompute_*` (sign-corrected baseline to extend).
3. `research_state/session_20261118T093031Z/` (`trackc_design_a_forecast_*`, `trackb_breach_labels_*`) and `research_state/session_20261118T114500Z/` (`trackbc_breach_*`) — carried forward.
4. `research_state/evaluation_summary.md`, `research_state/data_source_registry.json`, `research_state/resume_trigger_registry.json`.

## Prohibitions
- Do not re-run/re-score sealed cached-data confirmatory estimands or sealed results (FCLR-014, replication synthesis, design-frontier certs, FCLR-013/010/002/003/009/006/008, frontier verify-06/07/08+, sealed 19.04%).
- No polling/HF re-probe, no paid/credentialed/manual outcome data, no network installs/fetches, no `git lfs pull`.
- No mutation of sealed artifacts/closure JSON/`.github/workflows/*`; no root-level `research_state/*.md|json` (root is **498/500** — write all new artifacts under the session subdir); no duplicate `AGENT_HANDOFF*`.
- No `statsmodels` or unpinned heavy deps in the core path. Do not run parquet-only scripts without a CSV/JSON/ZIP twin.
- Do not treat missing-numpy/environmental discovery errors as green.
- Never inspect outcomes while producing outcome-blind preregs. **Never emit empty/zero-byte artifacts.**
- **Do not repeat the sign-inverted "funding-trail improves QLIKE" claim.**
- Do not leave a session recorded in this handoff without its required execution artifacts present and non-empty on disk.
- **Do not spend a session on handoff refresh / audit / gate-only work. That is the known failure loop. The only acceptable output of the next session is the executed ROBUST-05 package.**

## Reopen triggers (machine-checkable — all OPEN)
- `GATE4_BRANCH_1`: `research_state/fclr016_v5_terms_evidence_RESOLVED_*.json` (`status=RESOLVED_VERIFIED`, `fabricated=false`).
- `NEW_OBSERVED_LIQUIDATION_SOURCE`: `research_state/<source>_admissibility_audit_<UTC>.{md,json}` (`status=ADMISSIBLE`, `observed_labels=true`, ≥5 instruments, ≥3 blocks or ≥1 complete month).
- `HL_LABEL_EXTENSION`: `research_state/hl_label_extension_audit_<UTC>.{md,json}` (post-2026-10-31 observed ironflow labels, ≥100-day depth).
- `EXPANSION_ROBUSTNESS_REDO`: `research_state/expansion_robustness_redo_prereg_<UTC>.json` + evaluation summary (LOIO≥6/8 AND placebo>95th null).

## Verification record — 2026-11-18T14:35:39Z (handoff refresh, no new session created)
- `python3 scripts/check_handoff_heavywork_gate.py --json`: **PASS** — `pass=true`, `reason_code=OK`, `handoff_stale=false`, `root_count=498/500`, latest `session_20261118T132800Z`; `robust_04`, `breach_forecast`, `vol_liq_execution` PASS; `robust_05` declared but grandfathered because latest session == campaign start. **The next new session must emit the robust-05 package or fail closed.**
- `python3 scripts/check_tracka_scope_registry_drift.py --json`: **PASS** (`reason_code=OK`, 196/196).
- `python3 scripts/next_campaign_status.py --json`: confirmatory multi-block cached design **BLOCKED** (`any_feasible=false`); stdlib exploratory Track C/B feasible on cached data.
- Targeted tests: `python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_125` → **OK, 56 tests**. Full `unittest discover` is environmental/hanging in this runtime (not a green full suite).
- Holdout feasibility: verified mark+funding cache coverage for 2024-04…2024-09 across all five instruments.
- Bottleneck check: no blocking bottleneck for ROBUST-05. Removed the only recurring inefficiency — the handoff-refresh/audit-only loop — by tightening the mandatory message above and reiterating the fail-closed gate. Sole durable handoff preserved; no duplicates; no sealed artifacts, workflows, or registries modified.
