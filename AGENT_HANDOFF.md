# AGENT HANDOFF — 2026-11-18T18:26:17Z (SOLE DURABLE HANDOFF)

> **Authority:** this file only. Every other handoff-like file is tombstoned/historical and has no campaign authority.
> No duplicate `AGENT_HANDOFF*` exists under `research_state/`, `scripts/`, `tests/`, or `src/`.

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION — READ THIS BEFORE ANY OTHER ACTION (timestamped 2026-11-18T18:26:17Z)

**You must execute `FCLR-LIQ-RISK-CALIBRATION-06-20261118T182600Z` now. Do not idle, do not re-audit, do not gate-only, do not merely refresh this handoff, do not re-score sealed work, and do not re-run the closed QLIKE line.**

Create `research_state/session_<UTC>/` with UTC **strictly after** `20261118T182600Z`, freeze the risk-06 prereg **before touching evaluation/outcomes**, then produce the full risk-06 artifact set (all files **non-empty**) in that session. Update the **Latest executed session** line in this handoff to the new session id before final gate capture. `scripts/check_handoff_heavywork_gate.py` now enforces the risk-06 package and **fails the session closed** if any required artifact is missing or zero-byte. There is no legitimate audit-only path.

**Repo priority (name = campaign):** `Funding-conditioned-volatility-and-liquidation-risk`
1. **Track C (closed, negative):** funding-conditioned information does **not** forecast future realized volatility/stress beyond RV-only. Rejected under QLIKE on 2024-06/07/08/09 holdouts. Do not re-run.
2. **Track B (primary, active):** do funding-conditioned features forecast **modeled liquidation-boundary breach risk** with better out-of-sample probability calibration than RV-only? This is the live question.

## Current state (verified 2026-11-18T18:26:17Z)

- **Campaign state:** `ACTIVE_CAMPAIGN`; gates green after this refresh; mandated next step cleared of blockers.
- **Latest executed session:** `research_state/session_20261118T143817Z` — campaign `FCLR-VOL-LIQ-ROBUST-05-20261118T132800Z`, EXPLORATORY/PILOT, complete package (prereg + robustness triad + trigger check + evidence audit + independent recompute). ROBUST-05 is an **honest negative** and its artifact set remains gate-binding.
- **Active required next campaign:** `FCLR-LIQ-RISK-CALIBRATION-06-20261118T182600Z` (machine-enforced by `scripts/check_handoff_heavywork_gate.py` for any session after `20261118T182600Z`).
- **Rank-0 trigger state:** `TRIGGER_ONLY`; all four reopen triggers OPEN/none fired.

### ROBUST-05 result (do not re-run, do not re-interpret)
Four chronological holdouts, expanding train, 7-day purge/embargo, 5 instruments, stdlib OLS HAR + Duan smearing. `ΔQLIKE_vs_A = mean(QLIKE_A − QLIKE_model)`; QLIKE is a **loss**, so positive = model beats RV-only.

| Holdout | E mean ΔQLIKE vs A | bootstrap CI95 | E beats A |
|---|---|---|---|
| 2024-06 | −0.0632 | [−0.0915, −0.0344] | no |
| 2024-07 | −0.2166 | [−0.2839, −0.1491] | no |
| 2024-08 | −0.7476 | [−1.1282, −0.3058] | no |
| 2024-09 | −0.0293 | [−0.0418, −0.0161] | no |

- Pooled best model by QLIKE = **A_rv_only**; E pooled Δ = −0.2678 (CI95 [−0.3733, −0.1501]).
- Placebo (funding permuted, seed 12345): pooled Δ = −0.0934; real |Δ| = 0.2678 > placebo |Δ|.
- **Materiality floor NOT met (0 of 4).** Track C funding-conditioned volatility forecasting is **closed for exploratory purposes**. Correct claim: RV-only outperformed funding-conditioned models on QLIKE in every cached holdout tested.
- Independent recompute (`recompute_fclr_robust05_robustness_20261118T143817Z.json`) re-derives every aggregate + the frozen day-block bootstrap from stored loss arrays: **0 discrepancies**.

### Feasibility facts — do not claim you are data-blocked (verified 2026-11-18T18:26:17Z)
- Confirmatory multi-block **cached** design remains infeasible in all domains (`scripts/next_campaign_status.py --json` → `any_feasible=false`). Certified closed; do not reopen without a machine-satisfied trigger.
- `research_state/data_cache/` has complete **1h mark-price files + funding files** for `BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT, BNBUSDT` for every month **2024-04 … 2024-09** (30–31 mark days/file-month, 3 funding files/month). Risk-06 is runnable **fully offline**.
- **Sealed months:** 2024-10 onward (all 2025/2026 cache) are **sealed** and must not be read for outcomes.
- Environment: `numpy/pandas/scipy` absent by design. Implement with stdlib (`math/csv/json/zipfile/statistics/random`). Do not wait for installs or network.
- Root `research_state/` md+json count is **498/500**: write every new artifact under the session subdir.

## Next focus campaign — REQUIRED heavy work (machine-enforced)

**`FCLR-LIQ-RISK-CALIBRATION-06-20261118T182600Z` — Track B multi-month liquidation-breach risk calibration (stdlib, cached data).**

**Research question:** do funding-conditioned features improve **out-of-sample probabilistic calibration** (Brier score, log-loss) of **modeled liquidation-boundary breach risk** over an RV-only baseline across multiple chronological holdouts, and is any effect distinguishable from a funding-permutation placebo?

**Design (freeze ex ante):**
- Instruments: `BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT, BNBUSDT`.
- Label months (synthetic modeled labels, `observed_liquidation_labels=false`): `2024-04 … 2024-09`. Reuse/parameterize the verified Track B labeling code (entry at 1h mark close t; evaluate mark path t+1..t+H; `mmr=0.005`; L∈{5,10,20}; side∈{long,short}; H∈{4,24}; long boundary `P0*(1−1/L)/(1−mmr)`, short boundary `P0*(1+1/L)/(1+mmr)`).
- Chronological holds (7-day purge/embargo, expanding train):
  - `2024-07`: train 2024-04-01…2024-06-23, embargo 06-24…06-30, test 07-01…07-31
  - `2024-08`: train 2024-04-01…2024-07-24, embargo 07-25…07-31, test 08-01…08-31
  - `2024-09`: train 2024-04-01…2024-08-24, embargo 08-25…08-31, test 09-01…09-30
- Features (causal at t, train-only standardization): `lrv1, lrv24, lrv168` (RV block); funding block `fund, fund_abs, fmean, fewma`; funding-shock block `fund_shock=|fund−fewma|`, `fund_z=(fund−fmean)/trailing_sd`.
- Models (stdlib IRLS logistic, ridge `lambda=1e-6`, seed `12345`):
  - `B0_rv_only` = RV block.
  - `B1_funding_conditioned` = RV + funding block.
  - `B2_funding_shock` = RV + funding-shock block.
- Metrics: **Brier score (primary, lower better)**, log-loss, and AUC (secondary). Paired `ΔBrier = Brier_B0 − Brier_Bm` (**positive = funding model better calibrated**). Report the pre-registered primary scenario `L10|long|H24` and the equal-weight pooled result over all 12 scenarios.
- Uncertainty: UTC-day block bootstrap, seed `12345`, 2000 reps, percentile CI95; LOIO per holdout.
- Placebo: deterministic permutation of the funding series across entry timestamps (seed `12345`), identical pipeline; report its ΔBrier distribution.
- Calibration table: predicted vs observed breach rate by predicted-risk decile for the best model, per holdout.
- **Materiality floor (correct sign):** `B1` **or** `B2` beats `B0` (`ΔBrier > 0` with bootstrap CI95 lower bound > 0) in **≥2 of 3** holdouts on the primary scenario **and** real `|mean ΔBrier|` exceeds placebo `|mean ΔBrier|`. Otherwise report an honest negative result. Negative results are a valid completion; skipping the run is not.

**Execution recipe (fast path, reuse verified code):** copy `research_state/session_20261118T143817Z/trackb_breach_labels_20261118T093031Z.py` and `trackbc_breach_forecast_20261118T114500Z.py` into the new session dir; parameterize the label month over 2024-04…09, reuse the stdlib IRLS logistic / `brier` / day-block bootstrap, and add the funding-shock block + permutation placebo. The one-month forecast ran in minutes; 6 label months × 3 holds × 3 models + placebo should finish in ~10–25 minutes. Write incrementally so a timeout still leaves non-empty partial JSON/MD.

**Required artifacts (exact prefixes; all non-empty) in `research_state/session_<UTC>/` with UTC > `20261118T182600Z`):**
- `fclr_risk06_prereg_<UTC>.json` and `.md` (must contain `outcome_data_inspected_before_freeze=false`, the three holds, label months, model list, metrics, seed, floor)
- `fclr_risk06_labels_<UTC>.py`, `.json`, `.md` (multi-month modeled breach labels; `.json` must contain the per-scenario breach counts)
- `fclr_risk06_calibration_<UTC>.py`, `.json`, `.md`
- `trigger_check_<UTC>.json`
- `evidence_audit_<UTC>.json` + `.md`
- `recompute_fclr_risk06_calibration_<UTC>.json`

**Carry forward (copy, do not recompute) into the new session dir (all non-empty):** from `session_20261118T143817Z` — `trackc_design_a_forecast_*.{py,json,md}`, `trackb_breach_labels_*.{py,json,md}`, `trackbc_breach_prereg_*.json`, `trackbc_breach_forecast_*.{py,json,md}`, `fclr_robust05_prereg_*.{json,md}`, `fclr_robust05_robustness_*.{py,json,md}`.

### Record, verify, hand off (in order)
1. Create the post-`182600Z` session dir and freeze the prereg **first**.
2. Produce every required risk-06 artifact non-empty; never emit zero-byte files.
3. Change the **Latest executed session** line above to the new session id.
4. Run targeted bounded tests: `python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_125 -v`.
5. Record exact gate outcomes: `python3 scripts/check_handoff_heavywork_gate.py --json`, `python3 scripts/check_tracka_scope_registry_drift.py --json`, `python3 scripts/next_campaign_status.py --json`.
6. Update **only** `AGENT_HANDOFF.md` and the new session directory.

## Read first
1. `RESEARCH_PROMPT.md` §1–§6, §16–§17.
2. `research_state/session_20261118T143817Z/` — `fclr_robust05_robustness_20261118T143817Z.{py,json,md}`, `recompute_*`, `evidence_audit_*` (closed Track C baseline).
3. `research_state/session_20261118T143817Z/trackb_breach_labels_20261118T093031Z.py` and `trackbc_breach_forecast_20261118T114500Z.{py,json,md}` — the code to extend for risk-06.
4. `research_state/evaluation_summary.md`, `research_state/data_source_registry.json`, `research_state/resume_trigger_registry.json`.

## Prohibitions
- Do not re-run/re-score sealed cached-data confirmatory estimands or sealed results (FCLR-014, replication synthesis, design-frontier certs, FCLR-013/010/002/003/009/006/008, frontier verify-06/07/08+, sealed 19.04%).
- **Do not read sealed months 2024-10 … 2026-11 for outcomes.** Risk-06 uses only 2024-04…2024-09.
- Do not re-open the Track C QLIKE question: it is closed negative. No funding-trail "improvement" claim in either sign.
- No polling/HF re-probe, no paid/credentialed/manual outcome data, no network installs/fetches, no `git lfs pull`.
- No mutation of sealed artifacts/closure JSON/`.github/workflows/*`; no root-level `research_state/*.md|json` (root is **498/500** — write all new artifacts under the session subdir); no duplicate `AGENT_HANDOFF*`.
- No `statsmodels` or unpinned heavy deps in the core path. Do not run parquet-only scripts without a CSV/JSON/ZIP twin.
- Do not treat missing-numpy/environmental discovery errors as green.
- Never inspect outcomes while producing outcome-blind preregs. **Never emit empty/zero-byte artifacts.**
- Do not treat **modeled** breach labels as observed liquidations (`observed_liquidation_labels=false` must stay explicit).
- Do not leave a session recorded in this handoff without its required execution artifacts present and non-empty on disk.
- **Do not spend a session on handoff refresh / audit / gate-only work. That is the known failure loop. The only acceptable output of the next session is the executed RISK-06 package.**

## Reopen triggers (machine-checkable — all OPEN)
- `GATE4_BRANCH_1`: `research_state/fclr016_v5_terms_evidence_RESOLVED_*.json` (`status=RESOLVED_VERIFIED`, `fabricated=false`).
- `NEW_OBSERVED_LIQUIDATION_SOURCE`: `research_state/<source>_admissibility_audit_<UTC>.{md,json}` (`status=ADMISSIBLE`, `observed_labels=true`, ≥5 instruments, ≥3 blocks or ≥1 complete month).
- `HL_LABEL_EXTENSION`: `research_state/hl_label_extension_audit_<UTC>.{md,json}` (post-2026-10-31 observed ironflow labels, ≥100-day depth).
- `EXPANSION_ROBUSTNESS_REDO`: `research_state/expansion_robustness_redo_prereg_<UTC>.json` + evaluation summary (LOIO≥6/8 AND placebo>95th null).

## Verification record — 2026-11-18T18:26:17Z (handoff refresh + bottleneck removal; no new research session created)
- **Bottleneck removed 1 (gate was failing):** the previous handoff recorded `session_20261118T132800Z` while `session_20261118T143817Z` existed on disk → `HANDOFF_STALE_LATEST_SESSION`. This refresh records the executed ROBUST-05 session.
- **Bottleneck removed 2 (incomplete ROBUST-05 package):** `session_20261118T143817Z` lacked the required `evidence_audit_*` and `recompute_fclr_robust05_robustness_*` artifacts. Both were produced from the stored results; the recompute re-derives every aggregate and the frozen bootstrap with **0 discrepancies**.
- **Bottleneck removed 3 (avoidance):** `scripts/check_handoff_heavywork_gate.py` now enforces `FCLR-LIQ-RISK-CALIBRATION-06` (prereg, multi-month labels triad, calibration triad, trigger check, no zero-byte files); a post-`182600Z` session cannot pass without the heavy package.
- `python3 scripts/check_handoff_heavywork_gate.py --json`: **PASS** — `pass=true`, `reason_code=OK`, `failures=[]`, `handoff_stale=false`, latest = `session_20261118T143817Z`, root `498/500`; `robust_05` is actively binding (`required=true`, `pass=true`); `risk_06` is armed (`campaign_start_utc=20261118T182600Z`, grandfathered for the current latest session).
- `python3 scripts/check_tracka_scope_registry_drift.py --json`: **PASS** (`reason_code=OK`, 196/196).
- `python3 scripts/next_campaign_status.py --json`: confirmatory multi-block cached design **BLOCKED** (`any_feasible=false`); stdlib exploratory Track B/C feasible on cached 2024-04…09.
- Targeted tests: `python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_125` → **OK, 56 tests**. Full `unittest discover` is environmental/hanging in this runtime (not a green full suite).
- Holdout feasibility: verified mark+funding cache coverage for 2024-04…2024-09 across all five instruments (30–31 mark days/file-month, 3 funding files/month).
- Risk-06 enforcement self-tested: a simulated post-`182600Z` session with no risk-06 files (or with a zero-byte placeholder) fails; a complete non-empty set plus `trigger_check` passes.
- Sole durable handoff preserved; no duplicates; no sealed artifacts, workflows, or registries modified.
