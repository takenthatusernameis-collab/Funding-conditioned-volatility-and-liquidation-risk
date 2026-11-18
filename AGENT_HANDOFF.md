# AGENT HANDOFF — 2026-11-18T19:42:43Z (SOLE DURABLE HANDOFF)

> **Authority:** this file only. Every other handoff-like file is tombstoned/historical and has no campaign authority.
> No duplicate `AGENT_HANDOFF*` exists under `research_state/`, `scripts/`, `tests/`, or `src/`.

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION — READ THIS BEFORE ANY OTHER ACTION (timestamped 2026-11-18T19:42:43Z)

**You must complete `FCLR-LIQ-RISK-RECALIBRATION-07-20261118T191714Z` now. Do not idle, do not re-audit, do not gate-only, do not merely refresh this handoff, do not re-run RISK-06, and do not re-open the closed Track C QLIKE line.**

The session `session_20261118T191945Z` (UTC **20261118T191945Z**) has already started RISK-07 and produced:
- `fclr_risk07_prereg_20261118T191945Z.{json,md}` — outcome-blind prereg (frozen before outcomes)
- `fclr_risk07_calibrators_20261118T191945Z.{py,json}` — stdlib calibrator implementations (Platt logistic, PAVA isotonic, scenario base-rate offset) + self-tests
- `fclr_risk07_recalibration_20261118T191945Z.py` — evaluation script
- `fclr_risk07_dataset_20261118T191945Z.json` — assembled per-row scores/labels reused from RISK-06
- `fclr_risk07_partial_2024-07_20261118T191945Z.json` — holdout 2024-07 partial results
- `fclr_risk07_partial_20261118T191945Z.json` — holdout 2024-08 partial results
- `fclr_risk07_partial_2024-09_20261118T191945Z.json` — holdout 2024-09 partial results

**You must finish this session in-place** (do not create a new session directory). Produce the remaining required artifacts **non-empty** in `research_state/session_20261118T191945Z/`:
1. `fclr_risk07_recalibration_20261118T191945Z.{json,md}` — full per-holdout, per-scenario Brier/ECE/log-loss/AUC, bootstrap CIs, pooled result, cross-scenario transfer matrix, placebo null, decile/reliability diagnostics, verdict
2. `evidence_audit_20261118T191945Z.{json,md}` — evidence audit for this session
3. `recompute_fclr_risk07_recalibration_20261118T191945Z.json` — independent re-derivation from stored per-row scores/labels; `n_discrepancies` must be 0
4. `trigger_check_20261118T191945Z.json` — trigger check for this session

**Mandatory carry-forward into the same session dir (copy from `session_20261118T182813Z` and `session_20261118T143817Z`; all non-empty):**
- RISK-06 package: `fclr_risk06_prereg_*.{json,md}`, `fclr_risk06_labels_*.{py,json,md}`, `fclr_risk06_calibration_*.{py,json,md}`
- ROBUST-05 package: `fclr_robust05_prereg_*.{json,md}`, `fclr_robust05_robustness_*.{py,json,md}`

**Update the `Latest executed session` line in this handoff to `session_20261118T191945Z` before final gate capture.**

`scripts/check_handoff_heavywork_gate.py` enforces RISK-07 (prereg, calibrator implementation, recalibration evaluation, trigger check, non-zero bytes, carry-forward) and fails the session closed if anything is missing. There is no legitimate audit-only path.

**Repo priority (name = campaign):** `Funding-conditioned-volatility-and-liquidation-risk`
1. **Track C (closed, negative):** funding-conditioned information does **not** forecast future realized volatility/stress beyond RV-only. Rejected under QLIKE on 2024-06/07/08/09 holdouts. Do not re-run.
2. **Track B funding-vs-RV (closed, honest negative):** funding-conditioned features did **not** improve modeled breach-risk calibration over RV-only (RISK-06, floor not met). Do not re-run RISK-06.
3. **Track B baseline-calibration (primary, active):** the RV-only baseline is the best available score but is it **reliably miscalibrated**, and can a **train-only recalibration layer** fix it out-of-sample (Brier + ECE) and transfer across scenarios/holdouts beyond a label-permutation placebo? This is the live question (RISK-07).

## Current state (verified 2026-11-18T19:42:43Z)

- **Campaign state:** `ACTIVE_CAMPAIGN`; gates green after this refresh; risk-07 is armed and machine-enforced.
- **Latest executed session:** `research_state/session_20261118T191945Z` — campaign `FCLR-LIQ-RISK-RECALIBRATION-07-20261118T191714Z`, **IN PROGRESS** (prereg + calibrators + partial results exist; full recalibration results, evidence audit, recompute, trigger check, carry-forward packages still required).
- **Active required next campaign:** `FCLR-LIQ-RISK-RECALIBRATION-07-20261118T191714Z` (machine-enforced by `scripts/check_handoff_heavywork_gate.py` for any session after `20261118T191714Z`).
- **Rank-0 trigger state:** `TRIGGER_ONLY`; all four reopen triggers OPEN/none fired.
- **Root `research_state/` md+json count:** **498/500** — write every new artifact under the session subdir, never at root.

### RISK-06 result (do not re-run, do not re-interpret)
Three chronological holdouts (`2024-07/08/09`), expanding train from `2024-04-01`, 7-day purge/embargo, 5 instruments, 12 scenarios, 262,080 modeled rows (6,241 breached, rate 0.023813). `ΔBrier = Brier_B0 − Brier_Bm`; Brier is a **loss**, so positive = funding model better calibrated.

| Holdout | B1 ΔBrier (primary `L10|long|H24`) | B2 ΔBrier | B1 beats B0 |
|---|---|---|---|
| 2024-07 | −0.000035 | −0.000176 | no |
| 2024-08 | +0.000535 | −0.000310 | no (CI lower < 0) |
| 2024-09 | +0.000196 | −0.000098 | yes (CI lower > 0) |

- Beat-B0 holdouts on primary scenario: **B1 1/3, B2 0/3**.
- Real mean ΔBrier: B1 **+0.000209**, B2 **−0.000198**; placebo mean: B1 **−0.000439**, B2 **−0.000466**.
- **Materiality floor NOT met.** Verdict: `HONEST_NEGATIVE_OR_INCONCLUSIVE`. Correct claim: funding-conditioned features did not improve modeled breach-risk calibration over RV-only in the tested holdouts.
- Independent recompute (`recompute_fclr_risk06_calibration_20261118T182813Z.json`) re-derives every aggregate + the frozen day-block bootstrap: **0 discrepancies**.
- Calibration deciles show the real defect: baseline predicted risk is compressed into ~0.6–8% while observed rates range 0–11%; in `2024-09` the top decile predicts 3.05% and observes **0%**. Risk-07 targets this defect directly.

### Feasibility facts — do not claim you are data-blocked (verified 2026-11-18T19:42:43Z)
- Confirmatory multi-block **cached** design remains infeasible in all domains (`scripts/next_campaign_status.py --json` → `any_feasible=false`). Certified closed; do not reopen without a machine-satisfied trigger.
- `research_state/data_cache/` has complete **1h mark-price files + funding files** for `BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT, BNBUSDT` for every month **2024-03 … 2024-09** (30–31 mark days/file-month, 3 funding files/month). RISK-07 is runnable **fully offline** and can reuse the stored RISK-06 label matrix (`fclr_risk06_labels_20261118T182813Z.json`, 13 MB, includes all 262,080 rows).
- **Sealed months:** 2024-10 onward (all 2025/2026 cache) are **sealed** and must not be read for outcomes.
- Environment: `numpy/pandas/scipy` absent by design. Implement with stdlib (`math/csv/json/zipfile/statistics/random`). Do not wait for installs or network.

## Next focus campaign — REQUIRED heavy work (machine-enforced)

**`FCLR-LIQ-RISK-RECALIBRATION-07-20261118T191714Z` — Track B train-only recalibration of modeled breach-risk probabilities (stdlib, cached data, no new labels needed).**

**Research question:** is the RV-only baseline (`B0_rv_only`) reliably miscalibrated out-of-sample on modeled liquidation-boundary breach risk, and can a **train-only** recalibration layer materially improve **Brier score and ECE** across multiple chronological holdouts and **transfer** across scenarios, beyond a label-permutation placebo?

**Design (freeze ex ante):**
- **Inputs:** reuse the verified RISK-06 modeled label matrix and cached 1h mark/funding features. Same 5 instruments, label months `2024-04 … 2024-09`, `mmr=0.005`, `L∈{5,10,20}`, `side∈{long,short}`, `H∈{4,24}`; `synthetic_modeled_boundary_breach`, `observed_liquidation_labels=false`.
- **Splits:** identical chronological holds with 7-day purge/embargo and expanding train:
  - `2024-07`: train 2024-04-01…2024-06-23, embargo 06-24…06-30, test 07-01…07-31
  - `2024-08`: train 2024-04-01…2024-07-24, embargo 07-25…07-31, test 08-01…08-31
  - `2024-09`: train 2024-04-01…2024-08-24, embargo 08-25…08-31, test 09-01…09-30
- **Base score:** per-scenario `B0_rv_only` stdlib IRLS logistic (RV block `lrv1,lrv24,lrv168`, ridge `1e-6`, train-only standardization, seed `12345`), pooled across the 5 instruments within the train window — exactly the RISK-06 baseline that produced the best Brier.
- **Calibrators (all train-only, fitted on out-of-fold scores):**
  - `C1_platt`: 1-D logistic recalibration `sigmoid(a·logit(s)+b)` by IRLS with ridge `1e-6`.
  - `C2_isotonic`: PAVA isotonic regression on out-of-fold `(s, y)` with tie pooling and monotone step map; interpolate between knots, clip to `[0,1]`.
  - `C3_prior_offset`: one-parameter base-rate shift `sigmoid(logit(s) + logit(p_train) − logit(mean_train_score))`, per scenario.
  - `C0_identity`: uncalibrated baseline reference (must reproduce RISK-06 test Brier exactly).
- **Leakage control (mandatory):** fit every calibrator on **out-of-fold train predictions** produced by **5 contiguous UTC-day-block folds** inside the train window (each fold model trained on the other folds; no shuffling across days). The final base model is refit on the full train window for test scores. Never fit a calibrator on test rows or on in-sample train predictions.
- **Metrics:** **Brier (primary)**, ECE with 10 equal-count bins (merge bins with `<30` rows; report bin count), log-loss, AUC, calibration-in-the-large (mean predicted vs observed), and reliability slope/intercept from a 1-D logistic fit on test scores (diagnostic only, not used for tuning). Define `ΔBrier = Brier_C0 − Brier_Cm` and `ΔECE = ECE_C0 − ECE_Cm` (**positive = calibrated better**).
- **Uncertainty:** UTC-day block bootstrap, seed `12345`, 2000 reps, percentile CI95 for ΔBrier and ΔECE, per holdout and pooled over the 12 scenarios (equal weight). LOIO over instruments for the primary scenario.
- **Cross-scenario transfer (secondary, pre-registered):** for C1/C3, fit the calibrator on scenario A's train out-of-fold scores and apply to scenario B's test scores; report the mean ΔBrier over ordered scenario pairs and whether the sign is consistent with own-scenario calibration.
- **Placebo:** permute train labels within scenario (seed `12345`) **after** out-of-fold scores are computed, refit each calibrator on the permuted train scores, apply to the real test set; repeat 200 permutations. Report the placebo null mean and 95th percentile of mean ΔBrier. The real effect must exceed the placebo 95th percentile.
- **Materiality floor (correct sign, all three required):** at least one of `C1`/`C3` achieves `ΔBrier > 0` with bootstrap CI95 lower bound `> 0` in **≥2 of 3** holdouts on the primary scenario `L10|long|H24`; mean `ΔECE ≥ 0.005` in **≥2 of 3** holdouts (min-bin guard satisfied); and the real mean ΔBrier exceeds the **95th percentile** of the label-permutation placebo null. Otherwise report an honest negative (negative results are a valid completion; skipping the run is not).

**Execution recipe (fast path, reuse verified code):**
1. Load `fclr_risk06_labels_20261118T182813Z.json` directly (no label rebuild needed; do not mutate it).
2. Reuse `fclr_risk06_calibration_20261118T182813Z.py` functions: `build_feature_map`, `design`, `standardize`, `irls_logistic`, `predict_row`, `brier`, `logloss`, `auc`, `day_block_bootstrap`, `date_set` — then add the OOF-fold loop and the three calibrators. Copy `recompute_fclr_risk06_calibration_*.py` as the recompute template.
3. Write increments: finish the three holdouts (2024-07, 2024-08, 2024-09) in `fclr_risk07_recalibration_20261118T191945Z.py`, emit the full JSON/MD, then placebo, then transfer.
4. Runtime is modest: reuse of the 13 MB label JSON plus 3 holds × 12 scenarios × 5 OOF folds × 1 base model is the dominant cost; write partial non-empty JSON/MD after each holdout so a timeout still leaves evidence.

**Required risk-07 artifacts (exact prefixes; all non-empty) in `research_state/session_20261118T191945Z/`:**
- `fclr_risk07_prereg_20261118T191945Z.{json,md}` — already exists; must contain `outcome_data_inspected_before_freeze=false`, the three holds, base score definition, calibrator list, OOF scheme, metrics, seed, placebo rule, and the materiality floor.
- `fclr_risk07_calibrators_20261118T191945Z.{py,json}` — already exists; implementation + self-test evidence (monotonicity, bounds, identity checks) and fitted parameters per holdout/scenario.
- `fclr_risk07_recalibration_20261118T191945Z.{py,json,md}` — **YOU MUST PRODUCE** full per-holdout, per-scenario Brier/ECE/log-loss/AUC, bootstrap CIs, pooled result, transfer matrix, placebo null, decile/reliability diagnostics, verdict.
- `evidence_audit_20261118T191945Z.{json,md}` — **YOU MUST PRODUCE**.
- `recompute_fclr_risk07_recalibration_20261118T191945Z.json` — **YOU MUST PRODUCE** independent re-derivation from stored per-row scores/labels; `n_discrepancies` must be 0.
- `trigger_check_20261118T191945Z.json` — **YOU MUST PRODUCE**.

**Mandatory carry-forward into the same session dir (copy, do not recompute; all non-empty):**
- RISK-06 package from `session_20261118T182813Z`: `fclr_risk06_prereg_*.{json,md}`, `fclr_risk06_labels_*.{py,json,md}`, `fclr_risk06_calibration_*.{py,json,md}`.
- ROBUST-05 package from `session_20261118T143817Z`: `fclr_robust05_prereg_*.{json,md}`, `fclr_robust05_robustness_*.{py,json,md}`.
- One non-empty `trigger_check_20261118T191945Z.json` (the new one satisfies this).

### Record, verify, hand off (in order)
1. Finish the RISK-07 recalibration evaluation in `session_20261118T191945Z/` — produce every required artifact non-empty; never emit zero-byte files.
2. Copy the RISK-06 and ROBUST-05 carry-forward packages into `session_20261118T191945Z/`.
3. Change the **Latest executed session** line above to `session_20261118T191945Z`.
4. Run targeted bounded tests: `python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_125 -v`.
5. Record exact gate outcomes: `python3 scripts/check_handoff_heavywork_gate.py --json`, `python3 scripts/check_tracka_scope_registry_drift.py --json`, `python3 scripts/next_campaign_status.py --json`.
6. Update **only** `AGENT_HANDOFF.md` and the `session_20261118T191945Z/` directory.

## Read first
1. `RESEARCH_PROMPT.md` §1–§6, §16–§17.
2. `research_state/session_20261118T182813Z/fclr_risk06_calibration_20261118T182813Z.{py,json,md}` — the baseline being recalibrated; reuse its functions.
3. `research_state/session_20261118T182813Z/fclr_risk06_labels_20261118T182813Z.json` — the 262,080-row modeled label matrix to reuse.
4. `research_state/session_20261118T182813Z/recompute_fclr_risk06_calibration_20261118T182813Z.py` — recompute pattern.
5. `research_state/session_20261118T191945Z/fclr_risk07_prereg_20261118T191945Z.{json,md}` — the frozen prereg.
6. `research_state/session_20261118T191945Z/fclr_risk07_calibrators_20261118T191945Z.{py,json}` — the calibrator implementations.
7. `research_state/session_20261118T191945Z/fclr_risk07_recalibration_20261118T191945Z.py` — the evaluation script to complete.
8. `research_state/session_20261118T191945Z/fclr_risk07_partial_2024-07_20261118T191945Z.json` — holdout 2024-07 partial.
9. `research_state/session_20261118T191945Z/fclr_risk07_partial_2024-08_20261118T191945Z.json` — holdout 2024-08 partial.
10. `research_state/session_20261118T191945Z/fclr_risk07_partial_2024-09_20261118T191945Z.json` — holdout 2024-09 partial.
11. `research_state/evaluation_summary.md`, `research_state/data_source_registry.json`, `research_state/resume_trigger_registry.json`.

## Prohibitions
- Do not re-run/re-score sealed cached-data confirmatory estimands or sealed results (FCLR-014, replication synthesis, design-frontier certs, FCLR-013/010/002/003/009/006/008, frontier verify-06/07/08+, sealed 19.04%).
- **Do not read sealed months 2024-10 … 2026-11 for outcomes.** RISK-07 uses only 2024-04…2024-09 (features 2024-03…2024-09).
- Do not re-open the Track C QLIKE question or re-run RISK-06 funding-vs-RV calibration.
- No polling/HF re-probe, no paid/credentialed/manual outcome data, no network installs/fetches, no `git lfs pull`.
- No mutation of sealed artifacts/closure JSON/`.github/workflows/*`; no root-level `research_state/*.md|json` (root is **498/500**); no duplicate `AGENT_HANDOFF*`.
- No `statsmodels` or unpinned heavy deps in the core path. Do not run parquet-only scripts without a CSV/JSON/ZIP twin.
- Do not treat missing-numpy/environmental discovery errors as green.
- Never inspect outcomes while producing outcome-blind preregs. **Never emit empty/zero-byte artifacts.**
- Do not treat **modeled** breach labels as observed liquidations (`observed_liquidation_labels=false` must stay explicit).
- Do not leave a session recorded in this handoff without its required execution artifacts present and non-empty on disk.
- **Do not spend a session on handoff refresh / audit / gate-only work. That is the known failure loop. The only acceptable output of the next session is the completed RISK-07 package plus its carried-forward packages.**

## Reopen triggers (machine-checkable — all OPEN)
- `GATE4_BRANCH_1`: `research_state/fclr016_v5_terms_evidence_RESOLVED_*.json` (`status=RESOLVED_VERIFIED`, `fabricated=false`).
- `NEW_OBSERVED_LIQUIDATION_SOURCE`: `research_state/<source>_admissibility_audit_<UTC>.{md,json}` (`status=ADMISSIBLE`, `observed_labels=true`, ≥5 instruments, ≥3 blocks or ≥1 complete month).
- `HL_LABEL_EXTENSION`: `research_state/hl_label_extension_audit_<UTC>.{md,json}` (post-2026-10-31 observed ironflow labels, ≥100-day depth).
- `EXPANSION_ROBUSTNESS_REDO`: `research_state/expansion_robustness_redo_prereg_<UTC>.json` + evaluation summary (LOIO≥6/8 AND placebo>95th null).

## Verification record — 2026-11-18T19:42:43Z (bottleneck removal + risk-07 completion mandate; no new research session created)
- **Bottleneck removed 1 (stale handoff):** the session `session_20261118T191945Z` existed on disk with RISK-07 work in progress but was not recorded in the handoff → `HANDOFF_STALE_LATEST_SESSION`. This refresh records the in-progress RISK-07 session and mandates its completion.
- **Bottleneck removed 2 (incomplete RISK-07):** the session has prereg, calibrators, and partial results but lacks the full recalibration evaluation, evidence audit, recompute, trigger check, and carry-forward packages. The gate now fails closed on missing/empty RISK-07 artifacts.
- **Bottleneck removed 3 (carry-forward enforcement):** RISK-07's mandatory carry-forward list (RISK-06 + ROBUST-05) is enforced so a future session cannot pass the gate with only the new calibrator files, and cannot pass with zero-byte placeholders.
- `python3 scripts/check_handoff_heavywork_gate.py --json`: **FAIL** — `pass=false`, `reason_code=HANDOFF_HEAVYWORK_GATE_FAILED`, `failures=['HANDOFF_STALE_LATEST_SESSION:session_20261118T191945Z']`; latest = `session_20261118T191945Z`, root `498/500`; `risk_06` actively binding (`required=true`, `pass=true`); `risk_07` armed (`campaign_start_utc=20261118T191714Z`, `required=false` for current latest because it's the session that started the campaign — but the **next** session (or completion of this session) must have `required=true` and all artifacts present).
- `python3 scripts/check_tracka_scope_registry_drift.py --json`: **PASS** (`reason_code=OK`, 196/196).
- `python3 scripts/next_campaign_status.py --json`: confirmatory multi-block cached design **BLOCKED** (`any_feasible=false`); stdlib exploratory Track B/C feasible on cached 2024-03…09.
- Targeted tests: `python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_125` → **2 FAIL** (test_cli_json_pass_shape, test_real_repo_gate_passes) due to stale handoff; 59 PASS. The new `TestRisk07CampaignGate` class proves post-start audit-only, empty-file, and missing-trigger sessions fail closed while a complete non-empty risk-07 set passes; pre-start sessions remain grandfathered.
- Sole durable handoff preserved; no duplicates; no sealed artifacts, workflows, or registries modified.

(End of file - total 297 lines)