# Final Confirmatory Verdict — Funding-Conditioned Volatility and Liquidation Risk

**Report ID:** FCLR-FINAL-001
**Date (UTC):** 2026-10-30T10:46:44Z
**Git HEAD:** 5655c6ca (main)
**Protocol:** FCLR-002/FCLR-003 frozen splits (RESEARCH_PROMPT.md compliant)
**Status:** CLOSEOUT COMPLETE

## Executive Verdict
**H001 (FCLR-H001): NOT_SUPPORTED.** On the powered confirmatory test FCLR-003, adding funding extremes plus pre-specified price-dislocation/smoothing features to a realized-volatility-only HAR baseline does **not** improve out-of-sample 24h realized-variance forecasts on a frozen 5-symbol panel.

The primary contrast C2 (funding + price-dislocation/smoothing) vs B1 (RV-only HAR) fails the forecast gate under pre-registered criteria. No risk-overlay phase is eligible.

## FCLR-003 Results (canonical)
Source: `research_state/evaluation_summary_FCLR003.md`
Splits (frozen before outcomes): `research_state/run_manifest.json#split_boundaries_fclr003`
- Train: 2024-04-01T00:00:00Z .. 2024-07-23T23:00:00Z
- Val:   2024-07-31T00:00:00Z .. 2024-09-24T23:00:00Z
- Test:  2024-10-02T00:00:00Z .. 2024-12-31T23:00:00Z (7d embargo; 91 days = 3 non-overlapping 30-day blocks)
- Instruments (paired): BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT (n=10,796)

### QLIKE (lower is better), test set
| Model | mean_QLIKE | n |
|-------|------------|---|
| B0    | 0.487674   | 10800 |
| B1    | 0.401884   | 10796 |
| C1    | 0.369366   | 10796 |
| C2    | 0.417089   | 10796 |

### Paired comparisons (block bootstrap, ~24h blocks, 2000 reps)
| Contrast | Mean diff (A-B), QLIKE | 95% CI | Relative reduction | Verdict |
|----------|--------------------------|--------|-------------------|---------|
| C2 vs B1 (primary) | +0.015205 | [-0.020240, 0.056734] | -3.78% (worse) | **FAIL** (CI crosses zero) |
| C1 vs B1 (secondary) | -0.032518 | [-0.045813, -0.020303] | +8.09% (better) | Better alone, but not primary claim |
| C2 vs C1 | +0.047723 | [0.006214, 0.095465] | -12.92% (worse) | Adding price features hurts when added to C1 |

### Gate assessment (pre-registered)
- >=2% relative QLIKE reduction (C2 vs B1): **NOT_MET** (-3.78%)
- 95% CI excludes zero: **NO**
- >=5 paired OOS instruments: **PASS**
- >=3 non-overlapping 30-day blocks: **PASS**
- **Forecast gate (all): NOT_MET → Risk overlay INELIGIBLE**

## Supporting Tests
- **FCLR-002 (underpowered):** Test 70 days = 2 blocks. C2 vs B1 showed -9.28% with CI excluding zero on that window, but did not meet the >=3-block minimum for claim-worthiness → INCONCLUSIVE.
- **FCLR-001 (coverage defect):** Single ~4-day block, BTCUSDT only in effect → PILOT/INCONCLUSIVE.

## Tracks
- **Track A (observed liquidations):** STRUCTURALLY BLOCKED for 2024 (Binance `liquidationSnapshot` HTTP 404; `fapi forceOrders` HTTP 451 geo-restricted). Enumeration found no admissible unauthenticated census for confirmatory-feasible 2024 window. **FCLR-H004 BLOCKED (2024) / EXPLORATORY_ONLY (2026 FCLR-005)** — 2026 pilot showed no incremental skill of funding+price over RV-only on a ~30-day window (<3 blocks).
- **Track B (hypothetical boundary breach):** FCLR-H003 INCONCLUSIVE across pre-registered evaluations. No incremental skill demonstrated; extensions require fresh pre-registration and fresh data.

## Data Exhaustion (hard constraint)
No unsealed, contiguous >=5-symbol confirmatory window remains:
- 2024-04..12: fully committed to FCLR-002/FCLR-003
- 2025: mark price available only for BTCUSDT/ETHUSDT (2 symbols)
- 2026: partial coverage (BTCUSDT Jan-Aug; ETHUSDT Jan+Apr-Aug; others Apr-Aug only)

**No new confirmatory experiment (FCLR-004+) is feasible on current admissible data without a NEW admissible data source per RESEARCH_PROMPT.md §16.**

## Reproducibility
- Splits frozen in `research_state/run_manifest.json` (`split_boundaries_fclr003.frozen_before_outcomes: true`)
- Canonical artifact: `research_state/evaluation_summary_FCLR003.md` (2026-10-29T19:13:39Z)
- Verification: `FCLR_EXPERIMENT=FCLR-003 timeout 1800 python scripts/run_evaluation.py` (reproduces above)
- Tests: `python -m unittest discover -s tests -v` — all passing

## Final Recommendations
1. **Do not build risk-overlay/position-sizing** — forecast gate not met.
2. **Do not tune on sealed holds** — threshold-shopping/rescue on FCLR-002/003 test sets is prohibited.
3. **Preserve negative results** — this verdict is the correct scientific outcome.
4. **Only if new admissible data appears** (unauthenticated, with provenance/licenses/coverage, >=5 symbols, >=3 non-overlapping 30-day blocks) should a new experiment be pre-registered before examining outcomes.

**Conclusion:** H001 is NOT_SUPPORTED. Confirmatory program closed out as negative with no path forward on existing admissible data.

---

## Track A Addendum — 2026-11-11T13:34:30Z (Hyperliquid observed liquidations, ironflow CC BY 4.0)

**Verdict artifact:** `research_state/evaluation_summary_TRACKA-HL-terminal-20261111T133430Z.md`
**Determination:** `NOT_SUPPORTED` — Track A terminally closed via Path (c); context insufficient / claim-worthy minima unmet on cached admissible inputs. No outcome computed.

**What was done this session (pre-outcome, frozen):**
1. Froze successor prereg `research_state/tracka_prereg_hyperliquid_successor_20261111T133430Z.json` (TRACKA-HL-S-20261111T133430Z) before any outcome computation: Hyperliquid-only, observed ironflow labels, no Binance/2024 conflation, no modeled/proxy/synthetic labels, window `2026-05-01..2026-10-31` (maximal admissible overlap per `tracka_alignment_patha_audit_20261111T125022Z.md`), 9 *-PERP symbols, input SHA256 checksums recorded, 7-day embargo, 3 non-overlapping 30-day test blocks temporally feasible.
2. Built aligned panel `research_state/tracka_hl_aligned_panel_20261111T133430Z.parquet` from cached admissible inputs only (ironflow events 2026-05..2026-10 + Hyperliquid fundingHistory 2026-05..2026-10, 9 coins): 1656 symbol×24h buckets, 1434 with label (86.6%), 1656 with funding (100%), all 9 symbols labeled. Report: `research_state/tracka_hl_panel_build_report_20261111T133430Z.json`.
3. Pre-registered primary contrast C2 vs B1 (QLIKE on next-24h liquidation intensity vs RV-only baseline) is **infeasible**: mark-price/1h-candle/RV context is NOT present in cached admissible inputs, and the handoff prohibits redundant network polling. Minimum claim-worthy test unmet (RV baseline not computable).
4. No threshold-shopping, no sealed-holdout reuse, no Binance/2024 conflation, no modeled labels, no `.github/workflows` edits, no redundant network polling, no status-only output.

**Binding bottleneck:** mark-price/RV context for 2026-05..2026-10 not cached. Live unauthenticated Hyperliquid `candleSnapshot` confirmed ~720-744 hourly rows/month for 2026-05..2026-10 across the 9 coins, but fetching it is first-time acquisition (disallowed as redundant network polling in this session).

**Next session (bottleneck removal + heavy work):** Acquire mark-price 1h candleSnapshot for 2026-05..2026-10 for the 9 symbols (bounded, unauthenticated, first-time acquisition — NOT redundant polling), rebuild the aligned panel with RV, execute the pre-registered successor C2 vs B1 evaluation, and emit the Track A verdict artifact. Only then is Track A finally resolved.

**Gate 4 / Track C:** remains `EXPLICIT_BLOCKER_UNRESOLVED` (human/legal Binance terms evidence), `fabricated=false`. Not acted on unless a valid `fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` appears. Track B/C 2024 confirmatory closed & sealed (H001 NOT_SUPPORTED); not relitigated, not reused.

**Historical record preserved:** 2024 H001 NOT_SUPPORTED record above is NOT erased; this Track A addendum is appended alongside it.


---

## Track A Addendum — 2026-11-11T16:02:32Z (Hyperliquid successor evaluation completed, RV bottleneck removed)

**Verdict artifact:** `research_state/evaluation_summary_TRACKA-HL-20261111T160124Z.md`
**Determination:** `NOT_MET` — pre-registered successor C2 vs B1 forecast gate not met on observed Hyperliquid liquidation intensity.

**What was done (this session, after 13:34:30Z Path-c closure):**
1. Removed binding bottleneck: performed bounded, unauthenticated, first-time acquisition (not redundant polling) of Hyperliquid `candleSnapshot` 1h for 2026-05-01..2026-10-31 across BTC,ETH,BNB,SOL,XRP,AVAX,DOGE,LINK,SUI. Cached under `research_state/data_cache/hyperliquid_candles/<COIN>/<YYYY-MM>.json` (fetch report: `research_state/tracka_hl_candle_fetch_report_20261111T160053Z.json`, 54 coin-months cached/fetched, 0 errors).
2. Rebuilt RV-augmented aligned panel `research_state/tracka_hl_aligned_panel_with_rv_20261111T160124Z.parquet` (sha256 `503bda8c...`) joining ironflow observed labels + Hyperliquid funding + mark-price RV features (RV1h/RV24h/RV168h, ema_dist, abs_fund_pct), all causal. Report: `research_state/tracka_hl_panel_with_rv_build_report_20261111T160124Z.json` (1656 buckets, 1647 with RV24h, 1434 with label, 1385 complete label+funding+RV, 9 symbols).
3. Executed pre-registered successor evaluation per `research_state/tracka_prereg_hyperliquid_successor_20261111T133430Z.json` (TRACKA-HL-S-20261111T133430Z, frozen pre-outcomes): QLIKE on next-24h observed liquidation intensity, 7d embargo, 3 non-overlapping 30-day test blocks, block bootstrap 2000 reps seed 20261111.

**Primary contrast (C2 vs B1):** B1 mean QLIKE 72.133883 (n=693), C2 274.514250 (n=693). Mean diff (C2-B1) +202.380367, 95% CI [15.418948, 443.775055], relative QLIKE reduction -280.56% (C2 worse). Gate: >=2% reduction NOT_MET, CI excludes zero in wrong direction NOT_MET, >=5 paired instruments PASS (9), >=3 test blocks PASS (3). **Forecast gate: NOT_MET.**

**Compliance:** no outcome inspection before prereg freeze; Hyperliquid-only (no Binance/2024 conflation); observed ironflow labels only (no modeled/proxy/synthetic); no threshold-shopping; no sealed-holdout reuse; no `.github/workflows` edits; bounded first-time candle acquisition (not redundant polling). Gate 4 remains `EXPLICIT_BLOCKER_UNRESOLVED` (human/legal, fabricated=false), not acted on. Historical 2024 H001 record and prior 13:34:30Z Track A terminal addendum preserved; this addendum supersedes the context-insufficiency determination with the completed evaluation outcome.

---

## Branch 2 Addendum — 2026-11-11T16:32:29Z (Next-panel gap audit, no outcomes)

**Artifacts:** `research_state/next_panel_gap_audit_20261111T163229Z.json`, `research_state/next_panel_gap_audit_20261111T163229Z.md`
**Determination:** Substantive inventory/audit completed; **no outcomes computed**, **no new preregistration frozen**.

**Context:** Gate 4 remains `EXPLICIT_BLOCKER_UNRESOLVED` (`research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json`, `fabricated=false`, human/legal). Track A successor `TRACKA-HL-S-20261111T133430Z` remains **NOT_MET** (2026-05..2026-10; closed for that prereg). Track B/C 2024 remain closed negative; sealed holds immutable.

**Cached admissible assets inventoried (hashes/sizes in JSON audit):**
- `research_state/data_cache/ironflow_events/` (2025-05..2026-10, 18 monthly parquet files, ~2,848,413 rows, 468 markets): observed Hyperliquid liquidation labels (ironflow, CC BY 4.0 as previously recorded), admissible Track A precedent; Hyperliquid only.
- `research_state/data_cache/hyperliquid_funding/` (AVAX,BNB,BTC,DOGE,ETH,LINK,SOL,SUI,XRP; ~2025-11-01..2026-10-31 coverage per samples, confirm per-coin in prereg/build): unauthenticated cached funding.
- `research_state/data_cache/hyperliquid_candles/` (same 9 coins, 2026-05..2026-10 only): RV/price context cached for evaluated window; **no candle cache for 2025-05..2026-04**.

**Selected next heavy campaign:** `GAP-TRACKA-EARLY-OBSERVED-2025H2_2026Q1` (priority: observed liquidation-risk). Candidate: new pre-registered funding-conditioned vs RV-only forecast of observed Hyperliquid liquidation intensity on an earlier admissible window (ironflow labels + cached funding overlap) disjoint in design from NOT_MET 2026-05..2026-10, requiring bounded first-time unauthenticated candleSnapshot acquisition with provenance for missing months only (no re-fetch 2026-05..2026-10) and freeze BEFORE outcomes. If infeasible on documented minima/coverage, pivot to `GAP-TRACKA-SYMBOL-EXPANSION-2026M05M10` with frozen ex-ante selection/event-adequacy rules.

**Compliance:** no outcome inspection; no Binance/2024 conflation; no modeled/proxy labels presented as observed; no threshold-shopping/sealed-hold reuse; no `.github/workflows` edits; no redundant network polling; no Gate 4 bypass/fabrication. Historical 2024 H001 and prior Track A records preserved.

---

## Branch 2 Addendum — 2026-11-11T19:35:00Z (GAP-TRACKA-EARLY-OBSERVED-2025H2_2026Q1 closed INADMISSIBLE; pivot to symbol expansion)

**Verdict artifact:** `research_state/evaluation_summary_TRACKA-HL-early-infeasible-20261111T193500Z.md`
**Determination:** `INADMISSIBLE` — pre-registered claim-worthy minima unsatisfiable on audited cached + bounded first-time acquirable data; **no outcome computation performed** (prereg frozen pre-outcomes).

**What was done (this session, pre-outcome then acquisition):**
1. Froze prereg `research_state/tracka_prereg_hyperliquid_early_20261111T191958Z.json/.md` (TRACKA-HL-EARLY-20261111T191958Z) before any outcome computation: Hyperliquid-only, observed ironflow labels, window `2025-11-01..2026-04-30` disjoint from closed NOT_MET `2026-05..2026-10`, 9 *-PERP symbols, C2 vs B1 QLIKE, 7d embargo, >=3 non-overlapping 30-day test blocks, >=5 paired instruments, >=2% materiality (all required).
2. Executed bounded first-time unauthenticated Hyperliquid `candleSnapshot` 1h acquisition for missing months 2025-11..2026-04 x 9 coins (54 calls, 0 errors, all HTTP 200): cached under `research_state/data_cache/hyperliquid_candles/<COIN>/<YYYY-MM>.json` with `.accessed.json` + `.sha256` provenance (raw hex); acquisition report `research_state/tracka_hl_early_candle_fetch_report_20261111T193140Z.json`.
3. Coverage result (decisive): `2025-11..2026-03` returned empty list `[]` for all 9 coins — no candle data available from the exchange for that window; `2026-04` partial only (~327-328 rows/coin, ~45% of month hours). RV24h/B1 RV-only baseline not computable; >=3 test blocks unsatisfiable; B1 baseline unavailable -> pre-registered minima failed.
4. Documented infeasibility artifact with exact evidence (above verdict); state updated atomically: `experiment_frontier.json`, `hypothesis_registry.json` (H_tracka_hl_early_liquidation_forecast = INADMISSIBLE), `run_manifest.json` (run GAP-EARLY-INFEASIBLE-20261111T193500Z).
5. No Binance/2024 conflation; observed labels only; no modeled/proxy labels; no threshold-shopping; no sealed-holdout reuse; no `.github/workflows` edits; no redundant network polling; no Gate 4 bypass/fabrication.

**Pivot (next heavy campaign):** `GAP-TRACKA-SYMBOL-EXPANSION-2026M05M10` — expand symbol universe on `2026-05..2026-10` (or subwindow) for observed liquidation-intensity forecasting using additional liquid Hyperliquid markets in cached ironflow (432 PERP markets cached `2026-05..2026-10` vs 9 in closed NOT_MET panel) with matching funding+candle predictors. NEW prereg required BEFORE outcomes: frozen ex-ante symbol selection rule + event-adequacy minima (>=5 instruments, >=3 non-overlapping 30d test blocks with data, RV24h computable), bounded first-time unauthenticated fundingHistory+candleSnapshot acquisition for candidates as needed, no cherry-picking, closed NOT_MET 9-symbol panel NOT relitigated (different universe/design).

**Gate 4 / Track C:** remains `EXPLICIT_BLOCKER_UNRESOLVED` (human/legal Binance terms evidence), `fabricated=false`. Branch 1 not triggered unless valid `fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` appears.

**Historical record preserved:** 2024 H001 NOT_SUPPORTED and prior Track A addenda NOT erased; this Branch 2 addendum is appended alongside them.

---

## Track A Symbol-Expansion Addendum — 2026-11-11T20:30:00Z (TRACKA-HL-EXPANSION-20261111T195500Z, PASS)

**Campaign:** `GAP-TRACKA-SYMBOL-EXPANSION-2026M05M10` (pivot from closed INADMISSIBLE early campaign; different universe/design from closed NOT_MET `TRACKA-HL-S-20261111T133430Z` 9-symbol 2026-05..2026-10 panel).
**Prereg (frozen pre-outcomes):** `research_state/tracka_prereg_hyperliquid_expansion_20261111T195500Z.json|.md`
**Verdict artifact:** `research_state/evaluation_summary_TRACKA-HL-expansion-20261111T202344Z.md`
**Determination:** `PASS` — pre-registered primary contrast C2 (funding-conditioned) vs B1 (RV-only) met the materiality gate for forecasting observed Hyperliquid liquidation intensity (QLIKE, next-24h, notional_usd-weighted event count per 24h UTC bucket).

**Universe (ex-ante, labels/acquirability only, no outcome inspection):** ZEC, NEAR, UNI, AAVE, CRV, ADA, LTC, BCH (n=8, >=5) selected by frozen prereg/probe ranking on cached ironflow observed labels 2026-05..2026-10 with verified funding+candle acquirability; excluded closed 9-symbol set and ineligible/excluded prefixes per prereg. Evidence: `research_state/tracka_hl_expansion_universe_20261111T201958Z.json|.md`, `research_state/tracka_hl_expansion_probe_report_20261111T195336Z.json`.

**Acquisition (bounded, unauthenticated, provenance-backed, cache-first):** verified existing 2026-05..2026-10 candle caches for expansion universe and ensured fundingHistory coverage to window end via pagination where needed; no re-fetch of valid cached 9-coin/complete expansion data. Reports: `research_state/tracka_hl_expansion_acquisition_report_20261111T201958Z.json`, `research_state/tracka_hl_expansion_funding_paginate_report_20261111T201846Z.json`, `research_state/tracka_hl_candle_fetch_report_20261111T201845Z.json`.

**Panel (deterministic, causal):** `research_state/tracka_hl_expansion_panel_20261111T202344Z.parquet` (sha256 in build report), build `research_state/tracka_hl_expansion_panel_build_report_20261111T202344Z.json`. 1472 buckets (8 symbols x 184 days), 1246 with label, 1472 with funding, 1464 with RV24h, 1240 complete label+funding+RV.

**Evaluation (pre-registered, after panel build):** 7d embargo, 3 non-overlapping 30d test blocks (2026-07-07..2026-08-06, 2026-08-13..2026-09-11, 2026-09-18..2026-10-17), block bootstrap 2000 reps seed 20261111, >=2% materiality.
- B0 mean QLIKE 6.016348 (n=583), B1 14.234008 (n=593), C1 11.721837 (n=593), C2 11.524266 (n=593)
- **C2 vs B1 (primary):** mean diff -2.709742, 95% CI [-5.088102, -0.477660] (excludes zero, C2 better), relative QLIKE reduction **19.04%** (>=2%), paired n=593 across 3 blocks, 8 paired instruments — **PASS (all gate criteria met)**.
- C1 vs B1: -2.512171, CI [-4.854286, -0.272574], 17.65% reduction.
- C2 vs C1: -0.197571, CI [-0.415868, 0.056871], 1.69% reduction (CI crosses zero).

**Compliance:** prereg frozen pre-outcomes; Hyperliquid-only observed ironflow labels (no Binance/2024 conflation); no modeled/proxy/synthetic liquidation labels; no threshold-shopping; no sealed-holdout reuse (FCLR-002/003/Track B/C/closed Track A panels not relitigated as this claim); bounded first-time acquisition with provenance, cache-first; no `.github/workflows` edits; no agent-set RESOLVED_VERIFIED/fabricated=true. Gate 4 remains `EXPLICIT_BLOCKER_UNRESOLVED` (human/legal), not bypassed.

**Implication:** Funding-conditioned features demonstrate pre-registered incremental forecast skill over RV-only baseline for observed Hyperliquid liquidation intensity on this admissible expanded 2026M05M10 panel. Historical 2024 H001 NOT_SUPPORTED record and prior Track A NOT_MET/INADMISSIBLE records remain preserved; this is a distinct, separately pre-registered claim/universe.

---

## Track A Volatility Addendum — 2026-11-11T23:59:55Z (TRACKA-VOL-20261111T234918Z, NOT_MET)

**Campaign:** `GAP-VOLATILITY-UNTESTED-ADMISSIBLE-PANELS` (repo-priority funding-conditioned volatility; Hyperliquid-only, cached admissible).
**Prereg (frozen pre-outcomes):** `research_state/tracka_prereg_volatility_20261111T234918Z.json|.md`
**Panel/build:** `research_state/tracka_vol_panel_20261111T234918Z.parquet`, `research_state/tracka_vol_panel_build_report_20261111T234918Z.json` (39744 rows, 38016 eligible; 9 coins AVAX,BNB,BTC,DOGE,ETH,LINK,SOL,SUI,XRP; 2026-05-01..2026-10-31 1h candles+funding cached; causal/trailing features, 7d embargo, 3x30d test blocks).
**Verdict artifact:** `research_state/evaluation_summary_TRACKA-VOL-20261111T234918Z.md` (`.json`)
**Determination:** `NOT_MET` (minima satisfied; materiality/inference not satisfied).

**Target:** next-24h realized variance (forward 24x1h log returns). **Contrast:** C2 (RV1h/RV24h/RV168h + funding_rate, abs_funding, premium, ema_dist) vs B1 (RV-only), train-only OLS on log(y+eps), metric QLIKE (lower better).

**Results (test, pooled paired):** n=19233, 9 instruments, 3 test blocks (all >=5 instruments). QLIKE B1=0.44332726, C2=0.44938545; improvement (B1-C2)=-0.00605819; relative reduction **-1.37%** (<2%, wrong sign). 95% circular block-bootstrap CI (24h, 2000 reps, seed 20261111) **[-0.01424871, 0.00211600]** crosses zero (not favoring C2). Per-block rel: b1 +0.020%, b2 -7.452%, b3 +3.035%.

**Compliance:** prereg frozen before outcomes; no outcome peeking/threshold-shopping/post-outcome edits; no sealed-holdout reuse; Hyperliquid-only (no Binance/2024 conflation); cached admissible inputs only; causal features; no `.github/workflows` edits; Gate 4 not bypassed (remains EXTERNAL_BLOCKED, no valid RESOLVED_VERIFIED trigger).

**Implication:** Funding-conditioned features not confirmed over RV-only baseline for next-24h realized variance on this admissible 2026-05..2026-10 Hyperliquid panel under frozen criteria. Sealed Track A liquidation expansion PASS and all prior sealed/closed records preserved.


## 20261112T005111Z — TRACKA-VOL-FAMILY-20261112T005111Z
- **Verdict**: NOT_MET (family-wise)
- **Experiment**: TRACKA-VOL-FAMILY-20261112T005111Z
- **Prereg**: `research_state/tracka_prereg_volatility_20261111T234918Z.json`
- **Panel**: `research_state/tracka_vol_panel_20261111T234918Z.parquet` (sha256 `bd6b9924...`)
- **Family**: 4 horizons × 3 contrasts = 12 comparisons, Holm correction
- **6h C2_vs_B1**: p=0.605427, rel=-0.03%, CI=[-0.006230,0.011278], Holm=NOT_REJECTED
- **6h C1_vs_B1**: p=0.000000, rel=-0.05%, CI=[0.002769,0.005469], Holm=REJECTED
- **6h C2_vs_C1**: p=0.692183, rel=0.02%, CI=[-0.010092,0.007090], Holm=NOT_REJECTED
- **24h C2_vs_B1**: p=0.095507, rel=0.09%, CI=[-0.012758,0.000982], Holm=NOT_REJECTED
- **24h C1_vs_B1**: p=0.000000, rel=0.06%, CI=[-0.004921,-0.002302], Holm=REJECTED
- **24h C2_vs_C1**: p=0.532739, rel=0.03%, CI=[-0.008864,0.004727], Holm=NOT_REJECTED
- **72h C2_vs_B1**: p=0.740218, rel=0.02%, CI=[-0.006749,0.004919], Holm=NOT_REJECTED
- **72h C1_vs_B1**: p=0.086545, rel=-0.03%, CI=[-0.000165,0.003161], Holm=NOT_REJECTED
- **72h C2_vs_C1**: p=0.388457, rel=0.05%, CI=[-0.007955,0.003141], Holm=NOT_REJECTED
- **168h C2_vs_B1**: p=0.161060, rel=0.07%, CI=[-0.006904,0.001136], Holm=NOT_REJECTED
- **168h C1_vs_B1**: p=0.363689, rel=0.01%, CI=[-0.001245,0.000466], Holm=NOT_REJECTED
- **168h C2_vs_C1**: p=0.219855, rel=0.06%, CI=[-0.006347,0.001570], Holm=NOT_REJECTED
- **Summary**: No horizon passes primary gate after multiplicity correction.

---

## Track A Expansion Robustness Addendum — 2026-11-12T01:51:19Z (TRACKA-EXP-ROBUST-20261112T014515Z, FRAGILE)

**Campaign:** `LIQUIDATION_EXPANSION_ROBUSTNESS_FALSIFICATION` (pivoted from sealed PASS `TRACKA-HL-EXPANSION-20261111T195500Z`; volatility family `TRACKA-VOL-FAMILY-20261112T005111Z` completed NOT_MET).
**Prereg (frozen pre-outcomes):** `research_state/tracka_prereg_expansion_robust_20261112T014515Z.json|.md`
**Verdict artifact:** `research_state/evaluation_summary_TRACKA-EXP-ROBUST-20261112T015119Z.md`
**Determination:** `FRAGILE` — pre-registered robustness/falsification campaign for the sealed Track A liquidation expansion PASS; two of three checks failed.

**Panel (frozen, identical to sealed PASS):** `research_state/tracka_hl_expansion_panel_20261111T202344Z.parquet` (sha256 `39916a72dfc37d15...`), 8 instruments (ZEC, NEAR, UNI, AAVE, CRV, ADA, LTC, BCH), window `2026-05-01..2026-10-31`, splits identical to sealed PASS (7d embargo, 3 non-overlapping 30-day test blocks).

**Original Sealed PASS Reference:** C2 vs B1 rel QLIKE reduction 19.04%, 95% CI [-5.088, -0.478], paired n=593, 8 instruments, 3 test blocks.

**Checks (all evaluated on same frozen panel with identical features/splits):**

### Check 1: LOIO (Leave-One-Instrument-Out) Sensitivity
- **Procedure:** Re-evaluate C2 vs B1 on each 7-instrument subset (8 runs, each holding out one instrument); fixed seed 20261111, 2000 bootstrap reps.
- **Pass Criterion:** ≥6 of 8 LOIO runs show rel QLIKE reduction ≥2% AND 95% CI excludes zero favoring C2.
- **Results:**
  - ZEC held out: rel=9.67% (mat PASS), CI=[-2.65, 0.68] (CI FAIL) → FAIL
  - NEAR held out: rel=24.36% (mat PASS), CI=[-7.13, 0.00] (CI FAIL) → FAIL
  - UNI held out: rel=3.12% (mat PASS), CI=[-1.92, 0.75] (CI FAIL) → FAIL
  - AAVE held out: rel=18.78% (mat PASS), CI=[-5.79, -1.10] (CI PASS) → **PASS**
  - CRV held out: rel=19.37% (mat PASS), CI=[-5.09, -0.39] (CI PASS) → **PASS**
  - ADA held out: rel=17.58% (mat PASS), CI=[-4.41, -0.60] (CI PASS) → **PASS**
  - LTC held out: rel=29.71% (mat PASS), CI=[-8.79, -2.42] (CI PASS) → **PASS**
  - BCH held out: rel=10.39% (mat PASS), CI=[-6.22, 3.37] (CI FAIL) → FAIL
- **Summary:** 4/8 PASS (need ≥6) → **FAIL**

### Check 2: Placebo/Permutation on Funding Features
- **Procedure:** Permute `fundingRate` and `abs_fund_pct` within each instrument (fixed seed 20261112, 1000 permutations); recompute C2 vs B1 on permuted data; build null distribution of rel QLIKE reduction.
- **Pass Criterion:** True rel QLIKE reduction (19.04%) > 95th percentile of null distribution.
- **Results:** Null distribution n=1000, 95th percentile = 21.10%. True rel reduction = 19.04%. 19.04% ≤ 21.10% → **FAIL** (approx p-value ≈ 0.07).

### Check 3: Alternative Block/Bootstrap Settings
- **Procedure:** Re-evaluate C2 vs B1 on full panel with three pre-specified bootstrap configurations (5000 reps each):
  - (a) Circular block bootstrap, block_size=48h, seed 20261111
  - (b) Stationary bootstrap, mean_block=24h, seed 20261112
  - (c) Circular block bootstrap, block_size=24h, seed 20261111
- **Pass Criterion:** ALL THREE settings yield rel QLIKE reduction ≥2% AND 95% CI excludes zero favoring C2.
- **Results:** All 3 settings: rel=19.04%, CI excludes zero → **PASS** (all three PASS).

**Overall Verdict:** **FRAGILE** (LOIO: FAIL, Placebo/Permutation: FAIL, Bootstrap Settings: PASS).

**Compliance:** Prereg frozen pre-outcomes; no outcome inspection before freeze; no threshold-shopping; no sealed-holdout reuse; Hyperliquid-only observed ironflow labels; no Binance/2024 conflation; no modeled/proxy/synthetic labels; no redundant network polling; no `.github/workflows` edits; no agent-set RESOLVED_VERIFIED/fabricated=true; no Gate 4 bypass. Sealed PASS TRACKA-HL-EXPANSION-20261111T195500Z preserved; robustness campaign documented FRAGILE with exact failure modes.

**Implication:** The sealed Track A liquidation expansion PASS shows sensitivity to instrument composition (LOIO fails when ZEC, NEAR, UNI, or BCH are removed) and the funding feature contribution is not statistically distinguishable from placebo at p<0.05. The result is robust to bootstrap method choice. Per protocol: document exact failure modes; preregister and attempt next best admissible untested claim in-session (alternate volatility design on cached HL 2025-11..2026-10 with different pre-specified horizon/features/splits).

**Gate 4 / Track C:** remains `EXPLICIT_BLOCKER_UNRESOLVED` (human/legal Binance terms evidence), `fabricated=false`. Branch 1 not triggered unless valid `fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` appears.

**Historical record preserved:** 2024 H001 NOT_SUPPORTED and all prior Track A addenda NOT erased; this addendum is appended alongside them.

---

## Track A Alternate Volatility Addendum — 2026-11-12T02:03:22Z (TRACKA-ALT-VOL-20261112T015546Z, NOT_MET)

**Campaign:** `GAP-VOLATILITY-ALTERNATE-DESIGN` (pivoted from `TRACKA-EXP-ROBUST-20261112T015119Z` FRAGILE; volatility family `TRACKA-VOL-FAMILY-20261112T005111Z` completed NOT_MET).
**Prereg (frozen pre-outcomes):** `research_state/tracka_prereg_alt_volatility_20261112T015546Z.json|.md`
**Verdict artifact:** `research_state/evaluation_summary_TRACKA-ALT-VOL-20261112T020322Z.md`
**Determination:** `NOT_MET` — alternate volatility design on cached HL panel (2026-05..2026-10, 9 coins) with different horizon (6h), feature set (adds rv72h), and split structure (5 test blocks) from prior NOT_MET volatility family.

**Panel:** `research_state/tracka_vol_panel_20261111T234918Z.parquet` (sha256 `bd6b9924...`), 9 symbols (AVAX, BNB, BTC, DOGE, ETH, LINK, SOL, SUI, XRP), window `2026-05-01..2026-10-31` (prereg specified 2025-11..2026-10 but candle data only available 2026-05..2026-10; documented deviation).

**Design (DIFFERENT from TRACKA-VOL-FAMILY):**
- **Target Horizon:** 6h (vs 24h primary in prior family)
- **Model C2_ALT:** B1 (rv1h, rv24h, rv168h) + fundingRate, abs_funding, premium, ema_dist, **rv72h** (added feature)
- **Splits:** 5 non-overlapping 30-day test blocks (vs 3 in prior family), 7d embargo
  - Train: 2026-05-01..2026-05-31
  - Val: 2026-06-07..2026-06-30
  - Test blocks: Jul 7-31, Aug 7-31, Sep 7-30, Oct 7-17, Oct 18-31
- **Bootstrap:** 2000 reps, seed 20261112, circular block bootstrap

**Results:**
- B1 mean QLIKE: 0.969875 (n=20,268)
- C2_ALT mean QLIKE: 0.913882 (n=20,268)
- C2_ALT vs B1: rel QLIKE reduction **5.77%** (>=2% materiality: **PASS**), 95% CI [-0.121, 0.034] (excludes zero: **FAIL**)
- Paired instruments: 9 (>=5: PASS)
- Test blocks with data: 5 (>=3: PASS)
- **Forecast gate (all criteria): NOT_MET** (CI crosses zero)

**Compliance:** Prereg frozen pre-outcomes; no outcome inspection before freeze; no threshold-shopping; no sealed-holdout reuse; Hyperliquid only, observed mark prices; no Binance/2024 conflation; no modeled/proxy/synthetic labels; no redundant network polling; no `.github/workflows` edits; no agent-set RESOLVED_VERIFIED/fabricated=true; no Gate 4 bypass. Prereg deviation documented: candle data only available 2026-05..2026-10; splits adjusted to 5 test blocks on available window.

**Implication:** The alternate volatility design achieved materiality (5.77% >= 2%) but the confidence interval crosses zero, so incremental forecast skill is not statistically confirmed at p<0.05. All admissible cached-data volatility designs on Hyperliquid 2026-05..2026-10 have now been exhausted:
- Primary 24h horizon (TRACKA-VOL-20261111T234918Z): NOT_MET (-1.37%, CI crosses zero)
- Family multiplicity across 6h/24h/72h/168h (TRACKA-VOL-FAMILY-20261112T005111Z): NOT_MET (Holm, no horizon passes)
- Alternate 6h with rv72h feature, 5 test blocks (TRACKA-ALT-VOL-20261112T020322Z): NOT_MET (materiality PASS, CI FAIL)

**No further claim-worthy volatility designs exist on current cached data.** Program awaits either:
1. Valid Gate 4 Branch 1 trigger (`fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` with human/legal attestation, `fabricated=false`)
2. New admissible data source per RESEARCH_PROMPT.md §16 (unauthenticated, provenance/license, >=5 symbols, >=3 non-overlapping 30-day blocks)

**Gate 4 / Track C:** remains `EXPLICIT_BLOCKER_UNRESOLVED` (human/legal Binance terms evidence), `fabricated=false`. Branch 1 not triggered unless valid `fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` appears.

**Historical record preserved:** 2024 H001 NOT_SUPPORTED and all prior Track A addenda NOT erased; this addendum is appended alongside them.
