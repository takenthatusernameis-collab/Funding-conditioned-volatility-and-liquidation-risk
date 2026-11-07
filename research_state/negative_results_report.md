# Negative Results Report — FCLR-001

Date: 2026-10-26
Protocol: research_state/research_protocol.md v1.0 (FCLR-001, FROZEN)

This report preserves null, failed, and inconclusive outcomes with explanations.
No result below was obtained by tuning, threshold-shopping, or reuse of the sealed
holdout for selection. All outcomes use the frozen train/val/test split with a
7-calendar-day embargo.

---
## FCLR-012-V (FORWARD VOLATILITY, UNSEALED 2026 PANEL) — 2026-11-04T00:52Z

- **Outcome:** INCONCLUSIVE (PILOT). Forecast gate NOT MET.
- **Contrast:** C2 vs B1 on next-24-hour realized variance, out-of-sample QLIKE.
- **Point estimate:** 15.19% relative QLIKE reduction (favors C2; direction
  consistent with sealed FCLR-011's +4.94%).
- **Uncertainty:** paired block bootstrap (2000 reps, ~24h blocks) 95% CI
  [-0.360564, 0.059434] crosses zero.
- **Block requirement:** NOT MET. Test window 2026-10-29..2026-11-02 = 5 days =
  0 non-overlapping 30-day blocks, versus the protocol requirement of >=3
  non-overlapping 30-day evaluation blocks across >=5 instruments.
- **Data:** genuinely new unsealed Binance panel 2026-08-07..2026-11-02 (not a
  reuse of any sealed holdout). 2026-10-28/29 mark days are genuinely absent from
  the archive (HTTP 404 on live probe 2026-11-04T00:45Z) and were NOT imputed.
- **Interpretation:** Encouraging forward signal on new data, but far too short an
  evaluation window and too wide a dependence-aware CI to support a confirmatory
  claim. Retain the null for confirmatory purposes. Do NOT promote.
- **Artifact:** research_state/evaluation_summary_FCLR-012-V.md;
  prereg research_state/pre_registration_fclr012v_20261104T005000Z.md;
  coverage research_state/fclr012v_coverage_audit.json.

Secondary contrasts (also CIs cross zero):
- C1 vs B1: -1.31% (95% CI [-0.066153, 0.051887]).
- C2 vs C1: 16.28% (95% CI [-0.294411, 0.019843]).

---

## GATE4-FUND-VOL-ABLATIONS-MSPLIT-V3-30D (Track C, funding-conditioned volatility) — 2026-11-07T03:45:53Z (repro verified 2026-11-07T04:35Z)
- **Type:** Pre-registered multi-split ablation (PILOT/data-sufficiency target met; forecast skill NOT demonstrated). Local admissible data only; no credentials/paid/auth-bypass/manual/network in run.
- **Pre-registration (frozen before outcomes):** `research_state/pre_registration_gate4_funding_multisplit_v3_30d_20261107T033500Z.md` (2026-11-07T03:35:00Z).
- **Data sufficiency (MET):** instruments=5 (BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT, BNBUSDT); `ok_30day_splits=4` (required >=3), 7d purge/embargo; 2024-04-01..2024-09-30 local panel; 4 non-overlapping 30-day walk-forward test blocks.
- **Method:** Direct-variance OLS HAR RV-only baseline (A) vs funding-augmented ablations B/C/D/E; primary contrast E_rv_funding_trails vs A; ΔQLIKE block bootstrap, seed=12345, reps=2000, block=24h (joint time blocks), alpha=0.05.
- **Result (null preserved; no incremental forecast skill):** Aggregate QLIKE A_rv_only=0.798319018412711 (best). B_rv_signed=12.183624184348375, CI(B-A)=[0.4805228898986025, 32.31258288091912] entirely positive (funding harmful). C_rv_abs CI(C-A)=[-0.37159501419674296, 0.2707987870777943] spans 0. D_rv_signed_abs CI=[-0.25396005567122193, 7.512202577246805] spans 0. **Primary E vs A:** point +0.4879023125556385, 95% CI [-0.042160777324701186, 1.1973379300276015], n_obs=12969, n_blocks=120 — spans 0. Per-split deltas unstable in sign/scale.
- **Verdict:** DATA-SUFFICIENT PILOT / INCONCLUSIVE ON PRIMARY CONTRAST (claim-worthy data-sufficiency met; no improvement claim). H001 (funding-conditioned volatility forecast vs RV-only) remains **NOT_SUPPORTED** across all claim-worthy panels (FCLR-003, FCLR-008, v3). Risk overlay **INELIGIBLE** (gate not met). No economic value claim, no overlay, no Track A linkage.
- **Artifacts:** `research_state/evaluation_summary_funding_v3_30d.md`, `research_state/run_manifest_funding_v3_30d.json` (sha256 774e4a9f85205116cbdab4e3bfa71d57e84f07e8d2bd21fc31056c4e080573f5 / 9fd540bd5391f59ad8d3f8e7c9cd48aa6c542e400d3284d4ed2f33217a48c56e). Reproduction `--start 2024-04-01 --end 2024-09-30 --include-cache` (implicit via v3) matched key metrics; wrote `research_state/run_manifest_funding_repro_20261107.json` (non-overwriting). v1/v2 preserved.
- **Leakage/alignment:** clean per v3 manifest/audit traceability (chronological, 7d purge/embargo, train-only normalization per split, last-known funding at/before hour; missing!=0). Do not re-run v1/v2 variants chasing significance (threshold shopping).

## 1. Primary forecast test (FCLR-H001)

- **Outcome:** INCONCLUSIVE (PILOT). Forecast gate NOT MET.
- **Contrast:** C2 vs B1 on next-24-hour realized variance, out-of-sample QLIKE.
- **Point estimate:** 2.50% relative QLIKE reduction (favors C2).
- **Uncertainty:** paired block bootstrap (2000 reps, ~24h blocks) 95% CI
  [-0.123401, 0.158843] crosses zero.
- **Block requirement:** NOT MET. Test window is a single ~4-day block
  (2024-03-27..2024-03-30) versus the protocol requirement of >=3 non-overlapping
  30-day evaluation blocks across >=5 instruments.
- **Interpretation:** The numerical improvement is not distinguishable from noise
  given the dependence-aware uncertainty, and the evaluation window is too short
  and too concentrated to support a claim. Retain the null.

Secondary contrasts (also inconclusive, CIs cross zero):
- C1 vs B1: -1.84% (95% CI [-0.134702, 0.175329]).
- C2 vs C1: -0.67% (95% CI [-0.016485, 0.011301]).

## 2. Baselines

- B0 (persistence) test QLIKE = 0.140791, lower than B1 (0.147800). The simple
  persistence baseline outperforms the HAR-style volatility baseline on this
  short test window. This is a null/negative finding for the B1 model form on the
  frozen panel and is preserved rather than omitted.

## 3. Funding-correction replication (FCLR-H002)

- **Outcome:** PARTIAL replication, not a confirmatory result.
- **Finding:** 445 funding-extreme events across 5 symbols (Jan-Mar 2024); median
  correction time 8.0h, mean 12.6h among corrected events.
- **Limitation:** The working paper's full methodology (event definition, censoring
  rules, volatility-regime split, contract set) is not independently
  reconstructible from admissible public sources alone. The reconstructed numbers
  are therefore not an exact replication and cannot be promoted to a confirmatory
  claim. Correction time is not evidence on volatility forecast skill, boundary
  breaches, or observed liquidations.

## 4. Hypothetical boundary-breach forecast (FCLR-H003)

- **Outcome:** NOT STARTED. Labels are implemented
  (scripts/synthetic_boundary_labels.py, 5/5 tests passed) but no out-of-sample
  breach evaluation has been run. No margin/leverage scenario has been registered
  before outcome inspection, as required. This cell must not be reported as a null
  result; it is untested.

## 5. Observed liquidation outcomes (FCLR-H004)

- **Outcome:** BLOCKED. Direct historical liquidation labels are unavailable from
  admissible public sources.
- **Evidence:** research_state/binance_source_probe.md. No liquidationSnapshot
  archive found under data/futures/um or cm (HTTP 404). Binance fapi forceOrders
  endpoint returns 451 restricted location in this environment.
- **Handling:** Absence of data is NOT evidence of zero liquidations. Track A is
  not viable for a binary absence/presence target. Track B (modeled boundary
  breaches) and Track C (volatility/stress outcomes) proceed independently and
  must never be described as observed-liquidation validation.

## 6. Exclusions and known shortfalls

- Test window is a single ~4-day block; protocol requires >=3 non-overlapping
  30-day blocks across >=5 instruments. The frozen 2024-01-01..2024-03-31
  coverage does not support the required block structure at the frozen split rule.
- Direct liquidation labels unavailable.
- No claim of forecast skill, edge, or economic benefit is supported by any
  result in this report.

## 7. What must not be repeated

- Do not reuse the sealed holdout for model selection, threshold choice, or
  re-evaluation.
- Do not relax the block/multiplicity/uncertainty gates after seeing outcomes.
- Do not relabel exploratory or partial results as confirmatory.
- Do not report unexecuted cells (H003, H004) as completed or null.

---

# FCLR-002 (superseding note) and FCLR-003

Date: 2026-10-29
Protocols: FCLR-002 v1.0 and FCLR-003 v1.0 (frozen splits recorded in
`research_state/run_manifest.json` under `split_boundaries` and
`split_boundaries_fclr003` respectively). Both use the same frozen
feature/target/model definitions as FCLR-001 v1.0 (B0/B1/C1/C2, OLS on
log RV, 7-day embargo) and were executed by `scripts/run_evaluation.py` with
`FCLR_EXPERIMENT=FCLR-002` / `FCLR_EXPERIMENT=FCLR-003`. No tuning, no
holdout reuse, no split changes.

## FCLR-002 (test 2024-07-23..2024-09-30, 5 symbols, n=8274 paired)

- **Outcome:** INCONCLUSIVE. Forecast gate NOT MET.
- **Primary contrast C2 vs B1:** -9.28% relative QLIKE reduction; 95% CI
  [-0.097648, -0.008788] excludes zero. Numerically met and independently
  reproduced byte-identical (`evaluation_summary_FCLR002_REPRO.md`).
- **Block requirement:** NOT MET. Test window 2024-07-23..2024-09-30 = 70 days
  = 2 non-overlapping 30-day blocks (+10-day remainder); protocol requires >=3.
  Instrument requirement (>=5) IS met.
- **Interpretation:** The primary contrast passes on the numerical and
  uncertainty criteria on this panel, but the minimum claim-worthy test is not
  satisfied, so the gate does not pass. Retain INCONCLUSIVE. Do not promote.
- Secondary contrasts: C1 vs B1 ~0.00% (CI crosses zero); C2 vs C1 -9.28%
  (CI excludes zero) -- the incremental gain over C1 is what drives the C2 vs
  B1 improvement, i.e. the price-dislocation/EMA feature set, not funding alone.

## FCLR-003 (test 2024-10-02..2024-12-31, 5 symbols, n=10796 paired)

- **Outcome:** INCONCLUSIVE. Forecast gate NOT MET. This is the first variant to
  satisfy the minimum claim-worthy test on sample design.
- **Primary contrast C2 vs B1:** -3.78% relative QLIKE reduction; 95% CI
  [-0.020240, 0.056734] crosses zero -> NOT MET on uncertainty.
- **Minimum claim-worthy test:** MET on design (5 instruments; test window
  2024-10-02..2024-12-31 = 91 days = 3 non-overlapping 30-day blocks). The
  gate fails purely on the outcome criteria.
- **Registered secondary contrasts:**
  - C1 vs B1: -8.09% (95% CI [-0.045813, -0.020303], excludes zero) -- funding
    features DO add incremental skill in this window.
  - C2 vs C1: +12.92% (95% CI [0.006214, 0.095465], excludes zero) -- adding the
    price-dislocation/EMA features to C1 makes forecasts measurably WORSE.
- **Interpretation:** The frozen candidate C2 (volatility + funding + price
  dislocation) is dominated by C1 (volatility + funding only) on the FCLR-003
  panel. The price-dislocation features do not add incremental value here and
  actively degrade it. This is a durable negative result for the C2 model form
  on a >=3-block panel; it is preserved rather than explained away. The
  funding-only candidate C1 beats B1 in this window, but C1 is a registered
  secondary contrast, not the primary, and the protocol's primary contrast is
  C2 vs B1.
- **Cross-experiment note:** C2 vs B1 improves on FCLR-002 (-9.28%, CI excludes
  zero) and degrades on FCLR-003 (-3.78%, CI crosses zero). The sign flip across
  two frozen, non-overlapping test windows is itself evidence that the apparent
  FCLR-002 edge does not generalize. No single window supports a gate pass.

## Baselines (FCLR-003)

- B0 (persistence) test QLIKE = 0.487674 vs B1 = 0.401884. B1 beats B0 on this
  panel (unlike the FCLR-001 window where B0 won), so the HAR-style baseline is
  the stronger of the two baselines here. C1 (0.369366) beats both.

## What must not be repeated (all experiments)

- Do not reuse any sealed holdout for selection, tuning, or re-evaluation.
- Do not relax the block/multiplicity/uncertainty gates after seeing outcomes.
- Do not relabel exploratory or partial results as confirmatory.
- Do not report unexecuted cells (H003 alternate horizons/tiers, H004) as
  completed or null.
- Do not promote the FCLR-002 C2-vs-B1 point estimate to a gate pass; the
  >=3-block criterion is not met there.
- Do not claim the FCLR-003 C1-vs-B1 result as a primary-gate pass; C1 is a
  registered secondary contrast and the primary contrast (C2 vs B1) fails.

## FCLR-004 (2026-10-29T21:53:30Z) — BLOCKED
- Attempted to run FCLR-004 per pre-registration; pivoted to 6h primary due to 24h split reuse.
- Exhaustive timestamp audit of 5-symbol common panel shows all partitions consumed; only 2024-10-01 unused (1 day). No >=30-day contiguous window outside sealed partitions.
- Cannot satisfy >=3 non-overlapping 30-day blocks without reusing sealed holdouts -> forbidden.
- Result: BLOCKED with full evidence; gate remains not met.
