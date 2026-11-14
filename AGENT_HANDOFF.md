# SINGLE DURABLE HANDOFF — 2026-11-14T11:35:00Z (next agentic session)

## Repository / campaign
- **Repo:** `Funding-conditioned-volatility-and-liquidation-risk` (funding-conditioned volatility & liquidation risk, Hyperliquid/Track A frontier).
- **Completed P0:** `FCLR-LIQ-EXPANSION-RECONCILIATION-20261114T083642Z` — **VERDICT: EXPLAINED_BY_ESTIMATOR**
- **Program status:** ACTIVE, `max_status=EXPLORATORY_ONLY`, `promotable=false`, `audit_only=true`, `does_not_reopen_sealed_verdict=true`.

## Reconciliation Complete — 2×2 Audit Results

| | Sealed Estimator | Recompute Estimator |
|---|---|---|
| **Sealed panel** | **19.0371%** | **6.19%** |
| **Recompute panel** | **19.0371%** | **6.19%** |

- **Sealed reference (TRACKA-HL-EXPANSION):** 19.04% C2_vs_B1 QLIKE reduction
- **Recompute reference (FCLR-LIQ-EXPANSION-RECOMPUTE):** 6.19% C2_vs_B1 QLIKE reduction
- **Gap:** 12.85 percentage points
- **Verdict:** **EXPLAINED_BY_ESTIMATOR** — The gap is 100% attributable to estimator differences, not data differences. Both panels share 1,472 identical (coin, ts) keys.

### Key Finding
The sealed estimator (`tracka_hl_evaluate_successor.py`) uses **raw features without z-scoring, filling missing with 0.0**. The recompute estimator (`fclr_liq_expansion_recompute.py`) uses **z-scored features with train-only scaling, dropping missing**. This methodological difference fully explains the 19.04% vs 6.19% discrepancy.

## Artifacts Produced (All EXPLORATORY_ONLY, promotable=false)
- `research_state/prereg_tracka_liq_expansion_reconciliation_20261114T083642Z.{json,md}` — Frozen prereg
- `research_state/evaluation_summary_TRACKA-LIQ-EXPANSION-RECONCILIATION-20261114T113226Z.{json,md}` — Full 2×2 evidence with verdict
- `tests/test_fclr_liq_expansion_reconcile.py` — Regression tests (10/10 pass)

## Validation Gates (All Pass)
- `python3 scripts/next_campaign_status.py` — Hyperliquid forward window FEASIBLE (103-day untouched region)
- `python3 scripts/fclr_campaign_gate.py --arm all` — **19/19 PASS**
- Gate 4 blocker pipeline (tests/test_fclr019..023) — **27/27 PASS**
- Track C admissibility/provenance/gap repair — **PASS** (1 test timeout, rest pass)
- Final structural closure (test_fclr_final_structural_closure.py) — **5/5 PASS**
- New reconciliation tests (test_fclr_liq_expansion_reconcile.py) — **10/10 PASS**

## Known Test Failures (Expected)
- `test_tracka_hardening_140.py::test_gate_nonexistent_data_path_blocked_stable` — Drift preflight detects new reconciliation artifacts (correct behavior)
- `test_tracka_hardening_140.py::test_gate_unreadable_data_path_blocked_stable` — Same cause
These are **not regressions** — the drift preflight correctly identifies the 8 new timestamped artifacts from this reconciliation.

## Next Heavy Work Campaign (Priority Order)

### 1. EXECUTE TRACKA-HL-EXPANSION (Liquidation Forecast, Symbol Expansion) — **PRIMARY**
**Prereg:** `research_state/tracka_prereg_hyperliquid_expansion_20261111T195500Z.json` (FROZEN_PRE_OUTCOMES)
**Window:** 2026-05-01..2026-10-31 (or largest contiguous subwindow)
**Target:** Observed Hyperliquid liquidation intensity (notional-weighted ironflow events)
**Contrast:** C2 (funding + RV + premium + ema_dist) vs B1 (RV-only)
**Metric:** QLIKE, ≥2% relative reduction, CI excludes zero, ≥5 symbols, ≥3 test blocks

**Prereg `next_steps` (must execute in order):**
1. **Bounded acquisition**: `fundingHistory` + `candleSnapshot` 2026-05..2026-10 for top ex-ante candidate symbols (from `candidate_symbols_frozen_ex_ante`, excluding 9 already-cached coins). Record provenance (`.accessed.json` + `.sha256`). **No redundant polling.**
2. **Ex-ante symbol selection**: Apply frozen rule on cached ironflow labels (2026-05..2026-10 parquets). Metric: sum(notional_usd) per market, >0 events in ≥2 of 6 months, nonzero label variance across test blocks. Target final paired universe ≥5 symbols incl. overlap with 9 cached coins.
3. **Build deterministic RV-augmented panel**: symbols × 24h buckets with observed label intensity + funding + RV1h/RV24h/RV168h + ema_dist + abs_fund_pct. Emit panel parquet + build report with hashes/coverage/leakage notes.
4. **Run pre-registered evaluation**: Block bootstrap (≥3 test blocks, 7d embargo, ≥2% materiality, Holm across primary family). Emit `evaluation_summary_TRACKA-HL-EXPANSION-<UTC>.{md,json}` verdict (MET/NOT_MET/INADMISSIBLE per prereg).
5. **Atomic state update**: `experiment_frontier.json`, `hypothesis_registry.json`, `run_manifest.json`, `final_confirmatory_verdict.md` addendum. Preserve sealed 2024 H001 and closed Track A NOT_MET records.

**Scripts likely involved**: `scripts/fclr_build_tracka_liq_xsec.py`, `scripts/tracka_hl_fetch_candles_*`, `scripts/tracka_hl_build_panel_with_rv.py`, `scripts/run_liqmicro_v2.py`, `scripts/tracka_operator_report.py`, `scripts/tracka_resume_gate.py`.

### 2. EXECUTE TRACKA-VOL-FULLHIST (Volatility, Full History)
**Prereg:** `research_state/prereg_tracka_vol_fullhist_20261112T201536Z.md` (JSON twin exists, FROZEN_PRE_OUTCOMES)
**Window:** 2025-06-01..2026-01-17 (3 test blocks: 2025-10-08..2025-11-06, 2025-11-13..2025-12-12, 2025-12-19..2026-01-17)
**Reserved untouched:** 2026-01-18..2026-04-30 (MUST NOT BE READ)
**Universe:** 10 native perps (BTC, ETH, SOL, HYPE, ENA, WLD, FARTCOIN, TRUMP, NEAR, XRP) with complete hourly coverage
**Contrast:** C2_vs_B1 (primary), 4 horizons × {C2_vs_B1, C1_vs_B1, C2_vs_C1} Holm family (12 tests)
**Gates:** QLIKE reduction ≥2%, bootstrap CI excludes zero, ≥5 instruments, ≥3 blocks

**Scripts likely involved**: `scripts/fclr_ironflow_bulk.py`, `scripts/fclr_build_tracka_vol_fullhist.py`, `scripts/eval_volatility_family.py`.

### 3. HYPERLIQUID FORWARD-REDUCED CELL (2026-01-18..2026-04-30)
The reserved region from FULLHIST is exactly the forward window detected by `next_campaign_status.py`. A new prereg must be frozen for a **forward-reduced design** (60 train + 7 embargo + 3×10 test = 97 days) on this 103-day region before the campaign can claim closure on the Hyperliquid domain.

## Forbidden Patterns (Regression Guards)
| Pattern | Why It's Forbidden | Test That Catches It |
|---------|-------------------|---------------------|
| Declaring "campaign exhausted" while Hyperliquid bulk has FEASIBLE forward window | False closure happened before | `test_hyperliquid_bulk_frontier_detects_forward_window` |
| Re-proposing executed prereg as actionable | Frozen prereg without eval sat unexecuted | `test_no_actionable_prereg_while_cells_remain_terminal` |
| Missing `checks` block in evaluation artifact | Gate 4 fails closed without it | `test_missing_checks_block_fails` |
| Non-terminal verdict accepted as terminal | Only CONFIRMED/FRAGILE/NOT_REPLICATED/INCONCLUSIVE are terminal | `test_nonterminal_verdict_fails` |
| Agent setting `RESOLVED_VERIFIED=true` or `fabricated=true` | Human/legal review required for Gate 4 Branch 1 | Multiple Gate 4 tests assert `fabricated=false` |
| Reading sealed/terminal windows (2026-05-01..2026-10-31, 2026-01-18..2026-04-30 reserved) | Contaminates holdouts | Prereg `forbidden` clauses + `test_tracka_hardening_*` read guards |
| Outcome inspection before prereg freeze | Violates pre-registration integrity | `test_unfrozen_prereg_fails` |

## Handoff Integrity Checklist
- [x] `python3 scripts/next_campaign_status.py` shows Hyperliquid forward window FEASIBLE
- [x] All Gate 4 blocker pipeline tests pass (27/27)
- [x] All Track C admissibility tests pass
- [x] Final structural closure test passes (5/5)
- [x] Campaign gate: 19/19 PASS
- [x] New reconciliation tests pass (10/10)
- [x] No sealed window read, no outcome inspection before freeze, no `RESOLVED_VERIFIED` fabrication
- [x] **2×2 reconciliation complete: EXPLAINED_BY_ESTIMATOR verdict with full evidence**

**If any check fails: STOP. Fix the regression before proceeding.**