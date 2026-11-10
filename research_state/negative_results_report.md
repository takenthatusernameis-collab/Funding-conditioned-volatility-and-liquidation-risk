# Negative Results Report — FCLR-001

Date: 2026-10-26
Protocol: research_state/research_protocol.md v1.0 (FCLR-001, FROZEN)

This report preserves null, failed, and inconclusive outcomes with explanations.
No result below was obtained by tuning, threshold-shopping, or reuse of the sealed
holdout for selection. All outcomes use the frozen train/val/test split with a
7-calendar-day embargo.

---
## FCLR-014 (CONFIRMATORY TRACK C / H001, 2025 H1 PANEL) — 2026-11-10T10:38:27Z

- **Outcome:** NOT_SUPPORTED (forecast gate NOT_MET). Risk overlay INELIGIBLE.
- **Contrast:** C2 vs B1 on next-24-hour realized variance of mark-price returns,
  out-of-sample QLIKE. C2 = RV-HAR + signed funding + 90-day absolute-funding
  percentile + mark/index premium + mark/EMA24 distance; B1 = RV-HAR only.
- **Point estimate:** 1.14% relative QLIKE reduction (below the pre-registered 2%
  materiality floor).
- **Uncertainty:** paired block bootstrap (2000 reps, ~24h blocks across symbols)
  95% CI [-0.016361, 0.007728] — **crosses zero**.
- **Claim-worthiness minimums:** PARTIAL. Paired OOS instruments 5 (BNBUSDT, BTCUSDT,
  ETHUSDT, SOLUSDT, XRPUSDT) MET; test window 2025-05-22..2025-06-07 = 17 days =
  **0 non-overlapping 30-day blocks** (<3 required). The 2025 H1 panel provides
  only 17 test days due to the 7-day embargo at split boundaries; the full 2025
  panel (FCLR-009) had 207 test days and 6 blocks but was already inspected and
  returned NOT_MET. Holdout-reuse constraint prevents re-evaluation of the FCLR-009
  window.
- **Test-set QLIKE:** B0 0.373927 | B1 0.338659 | C1 0.334505 | C2 0.334792
  (n=1918 paired for B1/C1/C2; B0 n=1920).
- **Secondary contrasts (also cross zero):** C1 vs B1 +1.23% (CI [-0.011299, 0.003046]);
  C2 vs C1 -0.09% (CI [-0.007433, 0.008595]).
- **Data:** unauthenticated Binance public archive, cached locally under
  research_state/data_cache. Coverage-only audit
  research_state/trackc_deep_audit_2025_h1_check.json confirmed provenance_verified=true,
  5 symbols, 6 estimated blocks across 2025-01-01..2025-06-30; funding schema audit
  all_ok=true, missing=0 for 5 symbols x 6 months 2025-01..2025-06. No new downloads,
  no credentials, no network in the run.
- **Protocol discipline:** pre-registered in research_state/research_protocol_fclr014.md
  v2.0 BEFORE outcomes (prereg_hash=8563163c62524605cbf7f11603759aee2210d133f82c3742319a6dd85dfca597);
  splits frozen in run_manifest.json#split_boundaries_fclr014 with frozen_before_outcomes=true;
  no tuning on the test window; no sealed-holdout reuse; no threshold shopping.
- **Interpretation:** On the 2025 H1 confirmatory window (the only remaining untested
  local panel with provenance-verified data), adding funding extremes plus
  pre-specified price-dislocation/smoothing features to a realized-volatility-only
  HAR baseline yields no out-of-sample QLIKE improvement over the pre-registered 2%
  floor, the CI crosses zero, and the test window provides 0 non-overlapping 30-day
  blocks (protocol requires >=3). Consistent with the negative confirmatory verdicts
  of FCLR-003 (2024-12), FCLR-013 (2026 Q3), and FCLR-009 (full 2025), and with
  the directionally positive-but-inconclusive FCLR-012-V (2026 forward). H001 remains
  NOT_SUPPORTED across every claim-worthy panel executed.
- **Artifact:** research_state/evaluation_summary_FCLR-014.md;
  prereg research_state/research_protocol_fclr014.md;
  coverage research_state/trackc_deep_audit_2025_h1_check.json,
  research_state/funding_schema_audit_2025_h1.json;
  splits run_manifest.json#split_boundaries_fclr014.
- **Overlay eligibility:** NOT ELIGIBLE (gate NOT_MET).

---
## FCLR-009 (CONFIRMATORY VOLATILITY, UNSEALED 2025 PANEL) — 2026-11-10T00:15:40Z

- **Outcome:** NOT_MET (negative). Forecast gate NOT MET. Risk overlay INELIGIBLE.
- **Contrast:** C2 vs B1 on next-24-hour realized variance of mark-price returns,
  out-of-sample QLIKE. C2 = RV-HAR + signed funding + 90-day absolute-funding
  percentile + mark/index premium + mark/EMA24 distance; B1 = RV-HAR only.
- **Point estimate:** -0.43% relative QLIKE (negative diff = improvement, i.e. C2
  marginally better on average but far below the pre-registered 2% materiality floor).
- **Uncertainty:** paired block bootstrap (2000 reps, ~24h blocks across symbols)
  95% CI [-0.003120, 0.006165] — **crosses zero**.
- **Claim-worthiness minimums:** MET. Paired OOS instruments 5 (BNBUSDT, BTCUSDT,
  ETHUSDT, SOLUSDT, XRPUSDT); test window 2025-06-08..2025-12-31 = 207 days =
  **6 non-overlapping 30-day blocks** (>=3 required). This is the widest
  claim-worthy panel evaluated to date (365 common days, 8760 hourly timestamps).
- **Test-set QLIKE:** B0 0.367906 | B1 0.340756 | C1 0.339628 | C2 0.342205
  (n=24495 paired for B1/C1/C2; B0 n=24648).
- **Secondary contrasts (also cross zero):** C1 vs B1 +0.33% (CI [-0.004738, 0.002440]);
  C2 vs C1 -0.76% (CI [-0.001426, 0.006739]).
- **Data:** unauthenticated Binance public archive, cached locally under
  research_state/data_cache. Coverage-only audit
  research_state/fclr009_coverage_audit.json confirmed contiguous 2025-01-01..2025-12-31
  across all 5 symbols (mark/index/premium/klines present; funding 12 month files).
  No new downloads, no credentials, no network in the run.
- **Protocol discipline:** pre-registered in research_state/research_protocol_fclr009.md
  BEFORE outcomes; splits frozen by scripts/freeze_fclr009_splits.py BEFORE outcomes
  (run_manifest.json#split_boundaries_fclr009, frozen_before_outcomes=true); no tuning
  on the test window; no sealed-holdout reuse; no threshold shopping.
- **Interpretation:** On the widest available claim-worthy panel, adding funding
  extremes plus pre-specified price-dislocation/smoothing features to a realized-
  volatility-only HAR baseline yields no out-of-sample QLIKE improvement over the
  pre-registered 2% floor and a CI that crosses zero. Consistent with the negative
  confirmatory verdicts of FCLR-003 (2024-12) and FCLR-013 (2026 Q3), and with the
  directionally positive-but-inconclusive unsealed FCLR-008. H001 remains NOT_SUPPORTED
  across every claim-worthy window tested. Retain the null; do NOT promote.
- **Artifact:** research_state/evaluation_summary_FCLR009.md;
  prereg research_state/research_protocol_fclr009.md;
  coverage research_state/fclr009_coverage_audit.json;
  splits run_manifest.json#split_boundaries_fclr009.

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

## FCLR-013 (2026-11-07T11:07:34Z) — Track C funding-conditioned volatility confirmatory reopen — gate NOT_MET (negative, preserved)
- **Outcome:** NOT_SUPPORTED (forecast gate NOT_MET). Confirmatory reopen on the frozen GO-candidate 2026 Q3 5-symbol panel (BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT; 2026-07-01..2026-09-30, 92 days). Prereg frozen before outcomes: `research_state/pre_registration_fclr013_20261107T094132Z.md` v1.0 (git af8c2eb2). Splits registered frozen_before_outcomes=true in `research_state/run_manifest.json` under `split_boundaries_fclr013`. No outcomes inspected before registration; no tuning on sealed test; no overlay; no threshold shopping; no credentials/paid/manual/network in claim run.
- **Primary contrast C2 vs B1 (next-24h RV QLIKE, lower better):** paired block bootstrap (24h blocks, 2000 reps, deterministic seed), paired n=4199.
  - Mean diff (C2 - B1): +0.005953 (C2 higher QLIKE = worse).
  - 95% CI [-0.011716, 0.022101] — crosses zero -> uncertainty does NOT support improvement.
  - Relative QLIKE reduction: -1.32% -> below the frozen >=2% materiality floor.
  - Gate criterion "CI supports improvement AND relative reduction >= 2%": NOT_MET.
- **Claim-worthiness:** instruments=5 (PASS >=5). Test window 2026-08-26..2026-09-30 = 36 days = 1 non-overlapping 30-day block -> >=3: NOT_MET (only 1 block; equivalent coverage not satisfied).
- **Secondary contrasts:** C1 vs B1 -0.015018 (CI [-0.030304,-0.003729], excludes zero, 3.32% improvement — secondary only, not the primary); C2 vs C1 +0.020971 (CI [0.003206,0.039391], C2 measurably WORSE than C1; price-dislocation/EMA features degrade the forecast).
- **Interpretation:** C2 (RV+funding+dislocation) is dominated by C1 (RV+funding) on this panel; dislocation features add no incremental value and actively hurt. H001 (funding-conditioned volatility forecast vs RV-only) remains NOT_SUPPORTED on every claim-worthy panel executed (FCLR-003, FCLR-008, v3 30d/5sym, FCLR-013). Risk overlay INELIGIBLE (gate not met). Preserve the null; do not promote; do not relabel as positive.
- **Artifact:** `research_state/evaluation_summary_FCLR-013.md` sha256 `107bc981ebb6f519205b42f94ce778e14b445036f4758995914dabb0ef6bd08a` (generated 2026-11-07T11:07:34Z). No `run_manifest_fclr013_*.json` emitted by `scripts/run_evaluation.py`; split key already present in `run_manifest.json`.
- **What must not be repeated:** do not relax block/multiplicity/materiality gates after seeing outcomes; do not chase the C1-vs-B1 secondary as a primary pass; do not build/tune an overlay on this sealed holdout.

---
## Track B — Hypothetical boundary-breach forecast (FCLR-H003, FCLR-002) — 2026-11-09T15:27:50Z

- **Outcome:** COMPLETE_INCONCLUSIVE. Out-of-sample evaluation completed; null preserved. Not a gate pass; not promotable.
- **Contrast:** C2 (RV + funding + price-dislocation/EMA) vs B0 (persistence, lagged RV24) on synthetic modeled boundary-breach labels, out-of-sample test block 2024-07-23..2024-09-30.
- **Scenarios:** 4 leverages (3x, 5x, 10x, 20x) × 2 sides (long, short), evaluated separately. MMR=0.005, horizon=24h, zero-cost boundary, entry = mark close at decision time t.
- **Panel:** 5 symbols (BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT); test n=8274 paired rows per scenario (B0 n=8280 includes origins without feature coverage).
- **Labels:** synthetic modeled boundary breaches from `scripts/synthetic_boundary_labels.py` (8/8 tests pass). NOT observed liquidations, NOT account margin, NOT exchange execution. Long/short kept separate.
- **Results (representative):**
  - lev3 long/short: base_rate=0.0000 — no events; B0 and C2 both NOT_EVALUABLE for meaningful discrimination.
  - lev5 long: B0 base_rate=0.0036, Brier=0.003625; C2 base_rate=0.0036, Brier=0.003615 — C2 negligibly lower Brier but AUPRC unchanged (0.008473 vs 0.008949), best-F1 precision/recall lower (TP=5→3).
  - lev5 short: B0 Brier=0.003240, AUPRC=0.012571; C2 Brier=0.003244, AUPRC=0.015339 — mixed, no consistent direction.
  - lev10 long: B0 Brier=0.016589, AUPRC=0.029867; C2 Brier=0.016517, AUPRC=0.037114 — C2 slightly better Brier/AUPRC but lower recall at best F1.
  - lev10 short: B0 Brier=0.014434, AUPRC=0.152279; C2 Brier=0.014613, AUPRC=0.169984 — mixed.
  - lev20 long: B0 Brier=0.108023, AUPRC=0.188117; C2 Brier=0.107891, AUPRC=0.190336 — marginal, no consistent skill.
  - lev20 short: B0 Brier=0.088904, AUPRC=0.242194; C2 Brier=0.089042, AUPRC=0.243350 — C2 slightly worse Brier, marginally better AUPRC.
- **Interpretation:** No consistent incremental forecast skill of C2 over B0 across leverage/side scenarios. Differences are marginal and directionally inconsistent. Null result preserved. Does not satisfy any forecast gate; risk overlay remains INELIGIBLE.
- **Artifact:** `research_state/evaluation_summary_h003_FCLR002.md` (regenerated 2026-11-09T15:27:50Z via `H003_EXPERIMENT=FCLR-002 python scripts/run_h003.py`; perf fix: single mark-price index vs per-day rglob).
- **Cell registered:** `research_state/experiment_frontier.json` entry `FCLR-H003-FCLR-002` (status COMPLETE_INCONCLUSIVE).

---
## Track C — Funding-conditioned volatility deeper validation (FUNDING_CONDITIONING_DEEPER_VALIDATION-002) — 2026-11-09T16:39:00Z

- **Outcome:** COMPLETE_INCONCLUSIVE (EXPLORATORY_ONLY). Forecast gate NOT MET — not confirmatory, not promotable.
- **Contrast:** C2 (RV + funding + price-dislocation/EMA) vs B1 (HAR-style RV-only) on next-24-hour realized variance, out-of-sample QLIKE, frozen FCLR-002 splits (train 2024-04-01..2024-06-08, val 2024-06-16..2024-07-15, test 2024-07-23..2024-09-30; 5 symbols BTC/ETH/BNB/SOL/XRP).
- **Aggregate test (STREAM_B_DEEP_ANALYSIS-001):** C2 vs B1 +4.588% relative QLIKE reduction; 95% CI [-0.044345, -0.018402] excludes 0 (YES). All 5 symbols improve +4.0%..+5.0%; SOLUSDT marginal.
- **Regime-stratified test (STREAM_B_DEEP_ANALYSIS-002, train-only quartile thresholds, no look-ahead):** Q1 extreme-funding regimes show robust funding-conditioned volatility skill (CI excludes 0 YES):
  - Q1_low_abs_pos: CI excludes 0 YES for all 5 symbols (BNB +5.081%, BTC +4.374%, ETH +5.816%, SOL +6.923%, XRP +5.370%); aggregate +5.346% (CI [-0.057688,-0.023675], YES).
  - Q1_low_abs_neg: CI excludes 0 YES for XRP (+9.192%); aggregate +4.890% (CI [-0.080391,-0.003577], YES).
  - Q2_pos: CI excludes 0 YES for BTC/ETH/XRP; aggregate +3.969% (CI [-0.037703,-0.009791], YES).
  - Q2_neg: aggregate -2.218% (NO). Q4_high_abs_neg: aggregate -4.696% (NO). Q3/Q4_high_abs_pos: 0 rows (train quartile boundaries degenerate).
- **Block requirement:** NOT MET. FCLR-002 test window 2024-07-23..2024-09-30 = 70 days = 2 non-overlapping 30-day blocks; protocol requires >=3. Confirmatory gate not met.
- **Interpretation:** Q1 extreme-funding regimes show robust incremental skill of funding + price features over RV-only baseline (CI excludes 0, rel_imp > 0 consistently), but with only 2 test blocks the result is EXPLORATORY only. Do NOT promote to confirmatory. Do NOT relax the block-count criterion. No threshold shopping. No conflation with observed liquidations — Track C is volatility/stress outcomes only.
- **Artifacts:** `research_state/evaluation_summary_STREAM_B_DEEP_ANALYSIS-001_20261109T162703Z.md` (ran 2026-11-09T16:27:03Z); `research_state/evaluation_summary_STREAM_B_DEEP_ANALYSIS-002_20261109T163517Z.md` (ran 2026-11-09T16:35:17Z).
- **Cell registered:** `research_state/experiment_frontier.json` entry `FUNDING_CONDITIONING_DEEPER_VALIDATION-002` set to COMPLETE_INCONCLUSIVE (exploratory) 2026-11-09T16:39:00Z.

## TRACKB-20251110T154307Z (Track B — modeled boundary breaches, synthetic proxy) — 2026-11-10T16:06:03Z
- Panel: 2025-01-01 .. 2025-10-31, 5 symbols (BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,XRPUSDT), provenance_verified=true, unmapped_count=0
- Splits (frozen before outcomes, prereg_hash 3c91885038e79345d7fdb28396505a5b7e57a6e7de146b9c3323d59bbfca0dc3): 40/20/40 chronological + 7d purge/embargo, test 3 non-overlapping 30-day blocks
- Primary contrast C2 vs B1 (synthetic breach 24h/5x/long/m0): rel improvement 1.50% < 2% materiality, 95% CI [-0.005000,0.035000] crosses zero → gate NOT_MET
- Verdict: NOT_SUPPORTED (modeled proxy only, not observed liquidations). No risk overlay eligible.

---
## trackb_TB1_20261110T173838Z (Track B — modeled boundary breaches, synthetic proxy) — 2026-11-10T18:05:00Z
- Panel: 2025-01-01 .. 2026-10-31, 5 symbols (BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,XRPUSDT), provenance_verified=true, unmapped_count=0, PROVENANCE_OK 161
- Splits (frozen before outcomes, prereg_hash 5e075968e5958471530d0618cdba1410f8fb3d5afdb31c3be13f99aa07d27c92): 60/20/20 chronological + 7d purge/embargo
- Test split: 2026-06-26T00:00:00Z .. 2026-10-31T23:00:00Z (4 non-overlapping 30-day blocks, PASS)
- Primary target: synthetic_boundary_breach_h24_long_5x_m0 (leverage=5.0, side=long, maintenance_margin_rate=0.0, horizon=24h)
- **CRITICAL FINDING**: Frozen test split contains ZERO synthetic boundary breaches across all 5 instruments (prevalence = 0.0000%). Full-window breach rates: BTC 0.000%, ETH 0.166%, BNB 0.010%, SOL 0.055%, XRP 0.303%.
- The 5x/24h long boundary requires a 20% adverse move within 24h, which simply did not occur in the test period. This makes the binary classification task degenerate — both B1 and C2 trivially predict "no breach" with near-perfect accuracy.
- Primary contrast C2 vs B1: Log Loss diff = -0.000010 (95% CI [-0.000030, 0.000006]); Brier diff = ~0. Relative improvements (1.58% LL, 9.47% Brier) are NOT INTERPRETABLE due to zero positive labels.
- Gate assessment: >=5 instruments PASS (5), >=3 test blocks PASS (4), >=2% materiality NOT_MET (metrics uninterpretable), 95% CI excludes null NOT_MET (CI crosses zero and metric degenerate). **Overall gate: NOT_MET**.
- Verdict: NOT_SUPPORTED_DEGENERATE_TEST. This window is INADMISSIBLE for confirmatory Track B with the 5x/24h long label definition. The test split provides no confirmatory evidence.
- Artifacts: research_state/evaluation_summary_trackb_TB1_20261110T173838Z.md, research_state/research_protocol_trackb_TB1_20261110T173838Z.md, run_manifest.json#split_boundaries_trackb_TB1_20261110T173838Z
- Next Track B routes: (1) Deep re-audit 2024-01-01..2024-09-30 panel (~9 est. blocks) + NEW frozen prereg + confirmatory; (2) Redesign label (leverage/horizon/side) + select test window with observed events + NEW frozen prereg + confirmatory. No network/paid/manual data.

---
## trackb_TB2_20261110T190405Z (Track B — modeled boundary breaches, synthetic proxy) — 2026-11-10T20:00:21Z

- **Outcome:** NOT_SUPPORTED (forecast gate NOT_MET). Risk overlay INELIGIBLE. No risk overlay is eligible; null result preserved; no threshold shopping; no sealed-holdout reuse.
- **Panel:** 2024-01-01 .. 2024-09-30, 5 symbols (BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT), provenance_verified=true, unmapped_count=0 (161 funding CSVs checked). No network / no paid / no manual / no credentialed data.
- **Label (frozen, pre-freeze):** synthetic_boundary_breach_h168_long_10x_m0 (leverage=10.0, side=long, maintenance_margin_rate=0.0, horizon=168h; mark-closes strictly after t, t+1..t+168h). Modeled synthetic boundary-breach proxy only — NOT observed liquidations, not account margin, not exchange execution.
- **Event adequacy (pre-freeze, >0 frozen-test positives):** Train 19565 origins/19565 labeled; Val 5765/5765; Test 5765 origins, 5040 labeled, **619 positives / 4421 negatives (prevalence 12.3%), all 5 symbols >0** (BTC 64, ETH 205, BNB 96, SOL 184, XRP 70). Matches pre-freeze label design scan (619/4925 over full window). Design is event-adequate; no threshold shopping after freeze.
- **Splits (frozen before outcomes; 7-day purge/embargo):** train 2024-01-01..2024-06-12 / val 2024-06-19..2024-08-06 / test 2024-08-13..2024-09-30. prereg_hash=46dcfb56c279e853230e75f6cb246ed878d765d2b399ea9a2e21c41581194adb (sha256 of frozen protocol file; mismatch with prior 9de16e7d... corrected in run_manifest.json before any outcome computation; outcome_values_inspected=false).
- **Predictors (training-only standardization; missing remains missing):** B1 (RV-only) = RV1h/RV24h/RV168h from mark-price log returns. C2 (funding-conditioned) = B1 + signed funding rate + abs funding percentile (prior 90d, >=30 obs) + mark/index premium + mark/EMA24 distance. Common eligible test sample = 5040 paired origins (B1 and C2 evaluated on identical rows).
- **Fit:** logistic MLE on train only (fixed 1e-6 ridge for numerical stability, not a tuned hyperparameter), no holdout tuning.
- **Test-set results (frozen holdout, paired C2 vs B1):** Pooled Log Loss B1=0.292447, C2=0.287540; Pooled Brier B1=0.073713, C2=0.072569. Paired mean Log Loss diff (C2-B1) = -0.000932; Brier diff = -0.000315. **Relative Log Loss reduction vs B1 = +1.68%, below the pre-registered >=2% materiality floor (NOT_MET).**
- **Uncertainty:** block bootstrap, 2000 deterministic-seed replicates, 30-day blocks (2 non-overlapping test blocks). Log Loss 95% CI for paired diff = [-0.010997, 0.003094] — **crosses zero, does not exclude null in favorable direction (NOT_MET)**, p=0.488. Brier p=0.488.
- **Multiplicity:** Holm across 2 pre-specified metrics — FAILS (Log Loss p=0.488 vs alpha=0.025; Brier p=0.488 vs alpha=0.05).
- **Claim-worthiness minimums:** >=5 instruments PASS (5). >=3 non-overlapping 30-day test blocks NOT_MET (2). >=2% materiality NOT_MET. CI excludes null favorable NOT_MET. Holm NOT_MET.
- **Forecast gate (ALL criteria):** NOT_MET. Unmet criteria: test_blocks_ge3, ll_materiality_ge2pct, ll_ci_excludes_null_favorable, holm_pass.
- **Verdict:** FORECAST_GATE_NOT_MET / NOT_SUPPORTED. C2 funding-conditioned model shows a small favorable point estimate (+1.68% rel Log Loss) but it is below the materiality floor, the CI crosses zero, and Holm does not pass; no incremental forecast skill is established. Consistent with Track C H001 NOT_SUPPORTED across all claim-worthy panels.
- **Artifact:** research_state/evaluation_summary_trackb_TB2_20261110T190405Z.md; prereg research_state/research_protocol_trackb_TB2_20261110T190405Z.md; splits/run record run_manifest.json#split_boundaries_trackb_TB2_20261110T190405Z and #tb2_confirmatory_run.
- **Overlay eligibility:** NOT ELIGIBLE (forecast gate NOT_MET).
- **Program status:** All admissible local routes exhausted with evidence — Track A STRUCTURALLY_BLOCKED, Track C concluded NOT_SUPPORTED, Track B TB2 confirmatory gate NOT_MET, Track B TB1 degenerate/inadmissible. Program concluded under constraints pending a new admissible unauthenticated source. No threshold shopping; no sealed-holdout reuse; no .github/workflows edits.
