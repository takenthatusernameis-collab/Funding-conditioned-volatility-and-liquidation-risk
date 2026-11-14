# NEXT SESSION HANDOFF — 2026-11-14T09:23:34Z

## ⚠ OBSOLETE — SUPERSEDED BY AGENT_HANDOFF.md (2026-11-14T13:15:35Z)

This file is STALE and must NOT be followed. It asserts an "ACTIVE FRONTIER" of an
untouched 103-day Hyperliquid forward window (2026-01-18..2026-04-30) and directs
execution of TRACKA-HL-EXPANSION Step 1. That forward region is ALREADY TESTED AND
EXHAUSTED by `TRACKA-LIQ-XSEC-FORWARD` (EXPLORATORY_NULL) and `TRACKA-VOL-FORWARD`
(EXPLORATORY_NULL/VALID_EXPLORATORY), and TRACKA-HL-EXPANSION is a sealed terminal
campaign (PASS but robustness FRAGILE; independent recompute INCONCLUSIVE; reconciled
EXPLAINED_BY_ESTIMATOR).

`scripts/next_campaign_status.py` and `tests/test_next_campaign_status.py` were updated
2026-11-14T13:27:41Z to mark the forward reserve as tested (`BULK_TESTED_WINDOWS`);
both now report "no feasible 3-block design in EITHER domain" (12/12 PASS).

Single durable handoff: `AGENT_HANDOFF.md`. Operative state: **bounded trigger-only**
(see `research_state/experiment_frontier.json` rank 0,
`research_state/structural_exhaustion_confirmation_20261114T132741Z.md`). No polling,
no repeated identical probes, no re-execution of tested windows, no status-only sessions.


### Executive Summary
This is a quantitative finance research repository studying funding-rate-conditioned volatility and liquidation risk in crypto perpetuals (Binance 5-symbol + Hyperliquid native perps via ironflow bulk cache). The campaign uses a **fail-closed gate architecture** to prevent premature closure declarations. Two data domains exist:

1. **Binance 5-symbol (BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT)** — EXHAUSTED for full 3-block design (no contiguous ≥127-day funding-backed run remains).
2. **Hyperliquid ironflow bulk (100+ native perps, hourly candles + funding + OI + observed liquidation events, CC BY 4.0, unauthenticated)** — **ACTIVE FRONTIER**: 103-day untouched forward window (2026-01-18..2026-04-30) fits a **forward-reduced 60/7/3×10 design (97 days minimum)**.

**Campaign status: EXECUTABLE HEAVY WORK REMAINS** (per `scripts/next_campaign_status.py` — all tests pass).

---

### Current Blockers (Must Not Be Ignored)

| Blocker | Status | Resolution Required |
|---------|--------|---------------------|
| **Gate 4 Branch 1 (terms/legal evidence)** | `EXTERNAL_BLOCKED` | Human/legal review required; agent CANNOT set `RESOLVED_VERIFIED`/`fabricated=true`. This blocks confirmatory Track C promotion but NOT Track A/B execution. |
| **TRACKA-HL-EXPANSION prereg** | `PREREGISTERD_FROZEN_PRE_OUTCOMES` | Frozen 2026-11-11T19:55:00Z. Covers 2026-05-01..2026-10-31. Requires execution per its `next_steps`. |
| **TRACKA-VOL-FULLHIST prereg** | `FROZEN_PRE_OUTCOMES` | Frozen 2026-11-12T20:15:36Z. Covers 2025-06-01..2026-01-17 (Arm A/B); reserves 2026-01-18..2026-04-30 untouched. Requires execution. |

**Critical**: The test `test_next_campaign_status.py::test_hyperliquid_bulk_frontier_detects_forward_window` **passes** and asserts the 103-day Hyperliquid forward window is feasible. Any session declaring "campaign exhausted" without executing this is a regression.

---

### Next Heavy Work Campaign (Priority Order)

#### 1. EXECUTE TRACKA-HL-EXPANSION (Liquidation Forecast, Symbol Expansion)
**Prereg**: `research_state/tracka_prereg_hyperliquid_expansion_20261111T195500Z.json`
**Window**: 2026-05-01..2026-10-31 (or largest contiguous subwindow)
**Target**: Observed Hyperliquid liquidation intensity (notional-weighted ironflow events)
**Contrast**: C2 (funding + RV + premium + ema_dist) vs B1 (RV-only)
**Metric**: QLIKE, ≥2% relative reduction, CI excludes zero, ≥5 symbols, ≥3 test blocks

**Prereg `next_steps` (must execute in order):**
1. **Bounded acquisition**: `fundingHistory` (full coverage) + `candleSnapshot` 2026-05..2026-10 for top ex-ante candidate symbols (from `candidate_symbols_frozen_ex_ante`, excluding the 9 already-cached coins). Record provenance (`.accessed.json` + `.sha256`). **No redundant polling.**
2. **Ex-ante symbol selection**: Apply frozen rule on cached ironflow labels (2026-05..2026-10 parquets). Metric: sum(notional_usd) per market, >0 events in ≥2 of 6 months, nonzero label variance across test blocks. Target final paired universe ≥5 symbols incl. overlap with 9 cached coins.
3. **Build deterministic RV-augmented panel**: symbols × 24h buckets with observed label intensity + funding + RV1h/RV24h/RV168h + ema_dist + abs_fund_pct. Emit panel parquet + build report with hashes/coverage/leakage notes.
4. **Run pre-registered evaluation**: Block bootstrap (≥3 test blocks, 7d embargo, ≥2% materiality, Holm across primary family). Emit `evaluation_summary_TRACKA-HL-EXPANSION-<UTC>.{md,json}` verdict (MET/NOT_MET/INADMISSIBLE per prereg).
5. **Atomic state update**: `experiment_frontier.json`, `hypothesis_registry.json`, `run_manifest.json`, `final_confirmatory_verdict.md` addendum. Preserve sealed 2024 H001 and closed Track A NOT_MET records.

**Scripts likely involved**: `scripts/fclr_build_tracka_liq_xsec.py`, `scripts/tracka_hl_fetch_candles_*`, `scripts/tracka_hl_build_panel_with_rv.py`, `scripts/run_liqmicro_v2.py`, `scripts/tracka_operator_report.py`, `scripts/tracka_resume_gate.py`.

#### 2. EXECUTE TRACKA-VOL-FULLHIST (Volatility, Full History)
**Prereg**: `research_state/prereg_tracka_vol_fullhist_20261112T201536Z.md` (JSON twin exists)
**Window**: 2025-06-01..2026-01-17 (3 test blocks: 2025-10-08..2025-11-06, 2025-11-13..2025-12-12, 2025-12-19..2026-01-17)
**Reserved untouched**: 2026-01-18..2026-04-30 (MUST NOT BE READ)
**Universe**: 10 native perps (BTC, ETH, SOL, HYPE, ENA, WLD, FARTCOIN, TRUMP, NEAR, XRP) with complete hourly coverage
**Contrast**: C2_vs_B1 (primary), 4 horizons × {C2_vs_B1, C1_vs_B1, C2_vs_C1} Holm family (12 tests)
**Gates**: QLIKE reduction ≥2%, bootstrap CI excludes zero, ≥5 instruments, ≥3 blocks

**Scripts likely involved**: `scripts/fclr_ironflow_bulk.py`, `scripts/fclr_build_tracka_vol_fullhist.py`, `scripts/eval_volatility_family.py`.

#### 3. HYPERLIQUID FORWARD-REDUCED CELL (2026-01-18..2026-04-30)
The reserved region from FULLHIST is exactly the forward window detected by `next_campaign_status.py`. A new prereg must be frozen for a **forward-reduced design** (60 train + 7 embargo + 3×10 test = 97 days) on this 103-day region before the campaign can claim closure on the Hyperliquid domain.

---

### Validation Gates (Must Pass Before Declaring Progress)

Run these **before** any "done" claim:
```bash
# 1. Campaign truth — must show FEASIBLE forward window
python3 scripts/next_campaign_status.py

# 2. Track A hardening parity (CLI/guarded/gate refusal contract)
python3 -m pytest tests/test_tracka_hardening_140.py tests/test_tracka_hardening_142.py -v

# 3. Gate 4 blocker pipeline integrity (draft-only, fail-closed)
python3 -m pytest tests/test_fclr019_gate4_evidence_bundle_index.py \
                   tests/test_fclr020_gate4_readiness_action_matrix.py \
                   tests/test_fclr021_gate4_blocker_resolution_checklist_validator.py \
                   tests/test_fclr022_gate4_blocker_resolution_evidence_preflight.py \
                   tests/test_fclr023_gate4_blocker_resolution_action_plan.py -v

# 4. Track C admissibility/provenance/gap repair
python3 -m pytest tests/test_trackc_panel_admissibility_audit.py \
                   tests/test_trackc_gap_repair_manifest.py \
                   tests/test_trackc_provenance_lineage.py \
                   tests/test_trackc_funding_schema_audit.py \
                   tests/test_trackc_panel_window_planner.py -v

# 5. Final structural closure guard
python3 -m pytest tests/test_fclr_final_structural_closure.py -v
```

**All above tests currently PASS.** Any new work must not break them.

---

### Forbidden Patterns (Regression Guards)

| Pattern | Why It's Forbidden | Test That Catches It |
|---------|-------------------|---------------------|
| Declaring "campaign exhausted" while Hyperliquid bulk has FEASIBLE forward window | Happened before (false closure) | `test_hyperliquid_bulk_frontier_detects_forward_window` |
| Re-proposing executed prereg as actionable | Frozen prereg without eval artifact sat unexecuted for ~1hr | `test_no_actionable_prereg_while_cells_remain_terminal` |
| Missing `checks` block in evaluation artifact | Gate 4 fails closed without it | `test_missing_checks_block_fails` |
| Non-terminal verdict accepted as terminal | Only CONFIRMED/FRAGILE/NOT_REPLICATED/INCONCLUSIVE are terminal | `test_nonterminal_verdict_fails` |
| Agent setting `RESOLVED_VERIFIED=true` or `fabricated=true` | Human/legal review required for Gate 4 Branch 1 | Multiple Gate 4 tests assert `fabricated=false` |
| Reading sealed/terminal windows (2026-05-01..2026-10-31, 2026-01-18..2026-04-30 reserved) | Contaminates holdouts | Prereg `forbidden` clauses + `test_tracka_hardening_*` read guards |
| Outcome inspection before prereg freeze | Violates pre-registration integrity | `test_unfrozen_prereg_fails` |

---

### Key Files to Read First (Context Loading)

| File | Purpose |
|------|---------|
| `scripts/next_campaign_status.py` | Campaign truth — run first every session |
| `research_state/tracka_prereg_hyperliquid_expansion_20261111T195500Z.json` | Active Track A liquidation expansion prereg |
| `research_state/prereg_tracka_vol_fullhist_20261112T201536Z.md` | Active Track A volatility full-history prereg |
| `research_state/hypothesis_registry.json` | All hypothesis statuses |
| `research_state/experiment_frontier.json` | Executed experiment ledger |
| `scripts/tracka_resume_gate.py` | CLI gate for Track A execution |
| `scripts/fclr010_guarded_entry.py` | Guarded execute (refuse-before-load) |
| `scripts/fclr010_harness.py` | Track A evaluation harness |

---

### Immediate Next Action for This Session

**Execute Step 1 of TRACKA-HL-EXPANSION**: Bounded first-time acquisition of Hyperliquid fundingHistory + candleSnapshot for top ex-ante candidate symbols (from the 50+ frozen candidate list, excluding the 9 already-cached coins). Target: confirm admissibility/acquirability for ≥5 final paired symbols.

**Do not** proceed to panel build or evaluation until acquisition + symbol selection are complete and documented with provenance.

**Do not** touch Gate 4 Branch 1 (terms/legal) — it remains externally blocked. Track A/B execution is independent.

---

### Handoff Integrity Checklist

- [ ] `python3 scripts/next_campaign_status.py` shows Hyperliquid forward window FEASIBLE
- [ ] All Track A hardening tests pass (140, 142)
- [ ] All Gate 4 blocker pipeline tests pass (019-023)
- [ ] All Track C admissibility tests pass
- [ ] Final structural closure test passes
- [ ] No sealed window read, no outcome inspection before freeze, no `RESOLVED_VERIFIED` fabrication

**If any check fails: STOP. Fix the regression before proceeding.**