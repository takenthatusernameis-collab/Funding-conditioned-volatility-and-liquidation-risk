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
