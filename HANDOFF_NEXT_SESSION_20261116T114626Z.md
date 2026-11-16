# HANDOFF — Next Agentic Work Session
**Generated:** 2026-11-16T11:46:26Z
**Repository:** Funding-conditioned-volatility-and-liquidation-risk
**Program Status:** CLOSED_TERMINAL

---

## EXECUTIVE SUMMARY

The FCLR research program has reached **program terminal structural closure**. All priority campaigns (P1, P2, P3) are sealed with terminal verdicts. The final campaign gate **FCLR-NEXT-CAMPAIGN-20261113T063000Z has PASSED** with all three cells complete. No feasible 3-block pre-registered design exists in any data domain (Binance, Hyperliquid). The program is **exhausted** pending external reopen triggers.

---

## CAMPAIGN GATE STATUS: FCLR-NEXT-CAMPAIGN-20261113T063000Z ✅ PASSED

| Cell | Verdict | Key Evidence |
|------|---------|--------------|
| **LIQ-010-CONFIRM** | `NOT_REPLICATED` | 17-symbol independent recompute: 0.50% Brier rel reduction (floor 2%), LOIO 0/5, placebo FAIL |
| **EXP-ROBUST-REDO** | `FRAGILE` | Expansion panel: LOIO 4/8 (need ≥6), placebo null p95 21.89% ≥ true 19.04% |
| **FWD-VOL-2025-CROSS** | `NOT_REPLICATED` | 2025-02..05 window: 0.29% QLIKE rel reduction (floor 2%), CI crosses zero, LOIO 1/5, placebo FAIL |

All three cells have:
- ✅ Frozen prereg (`status: FROZEN_PRE_OUTCOMES`, `outcome_data_inspected_before_freeze: false`)
- ✅ Terminal evaluation artifact with verdict in allowed set
- ✅ Checks block present
- ✅ Corresponding script exists

---

## PROGRAM STRUCTURAL CLOSURE

**Generated:** `research_state/fclr_final_structural_closure_20261116T114626.md/.json`
**Registry:** `research_state/resume_trigger_registry.json`

- **Rows enumerated:** 58 (hypotheses + sealed verdicts + experiments + source audits)
- **§17 promotion conditions met:** 0/58 rows
- **All §17 conditions NOT met:** TRUE
- **Terminal verdict:** `NO_CLAIM_WORTHY_RESULT_PROMOTABLE; ALL_P1_P2_P3_SEALED`
- **Program status:** `CLOSED_TERMINAL`

---

## REOPEN TRIGGERS (Machine-Checkable — Act ONLY When Satisfied)

| Priority | Trigger ID | Condition | Required Evidence Artifact |
|----------|------------|-----------|----------------------------|
| 1 | `GATE4_BRANCH_1` | External/legal evidence resolves FCLR-016 terms | `fclr016_v5_terms_evidence_RESOLVED_*.json` with `status: RESOLVED_VERIFIED`, `fabricated: false` |
| 2 | `NEW_OBSERVED_LIQUIDATION_SOURCE` | New admissible observed-liquidation source (≥5 instruments, ≥3×30d blocks OR ≥1 complete month, unauthenticated, provenance/license, venue-consistent) | `<source>_admissibility_audit_<UTC>.json` with `status: ADMISSIBLE`, `observed_labels: true` |
| 3 | `HL_LABEL_EXTENSION` | Verified Hyperliquid ironflow labels post-2026-10-31, ≥100 days depth, observed only | `hl_label_extension_audit_<UTC>.{md,json}` |
| 4 | `EXPANSION_ROBUSTNESS_REDO` | Newly pre-registered design on sealed expansion panel: LOIO ≥6/8 AND placebo PASS (true effect > null p95) — **NOT** re-scoring sealed 19.04% | `expansion_robustness_redo_prereg_<UTC>.json` + `evaluation_summary_*.json` |

**Critical:** `do_not_act_until_satisfied: true` for ALL triggers. No agent may bypass, grep for trigger strings, or act on partial evidence.

---

## DATA FRONTIER EXHAUSTION (from `next_campaign_status.py`)

- **Binance 5-symbol (BTC/ETH/BNB/SOL/XRP):** No contiguous 3-block span; no feasible disjoint 30-day blocks (pre-2024-04 has no funding)
- **Hyperliquid Bulk (candles+funding+OI+liq):** 12 months but max contiguous span 24d (need ≥127d)
- **Hyperliquid Extended (17 symbols, 18 event months):** All usable months 2025-11..2026-10 are **tested**; no untouched contiguous region
- **Baseline-only (klines no funding):** 2024-01..2024-03 only — insufficient for funding-conditioned designs

**Conclusion:** No feasible 3-block pre-registered design exists in ANY domain. The experimental frontier is closed.

---

## NEXT SESSION FOCUS — MANDATORY

### DO NOT:
- ❌ Launch new experiments, preregistrations, or evaluations
- ❌ Search for "workarounds" to the 3-block requirement
- ❌ Re-score sealed verdicts (NOT_REPLICATED, FRAGILE, NOT_MET)
- ❌ Lower materiality floors (2%), LOIO thresholds, or placebo bars
- ❌ Use live/network data — cached only per protocol

### DO:
1. **Monitor reopen triggers** — Run `scripts/fclr_final_structural_closure.py` periodically (e.g., weekly) to regenerate closure and check if any trigger predicate is satisfied by new artifacts in `research_state/`
2. **Validate trigger satisfaction** — If a trigger predicate evaluates TRUE, verify the required evidence artifact exists and meets all `required_fields` before any action
3. **Document trigger resolution** — If GATE4_BRANCH_1 resolves, follow RESEARCH_PROMPT Gate 4 Branch 1 protocol (human/legal attestation required)
4. **Archive/maintain** — Ensure `research_state/` artifacts remain intact and hashed for determinism audit

### If a trigger IS satisfied:
- The corresponding `reopen_requires` mapping in `REOPEN_MAP` identifies which hypotheses/experiments could be revisited
- A **wholly new protocol** outside the four triggers is required for any hypothesis not mapped
- All new work must pre-register BEFORE outcome inspection per §16

---

## KEY FILES FOR NEXT SESSION

| Purpose | Path |
|---------|------|
| Final closure (MD) | `research_state/fclr_final_structural_closure_20261116T114626.md` |
| Final closure (JSON) | `research_state/fclr_final_structural_closure_20261116T114626.json` |
| Trigger registry | `research_state/resume_trigger_registry.json` |
| Campaign gate | `scripts/fclr_next_campaign_gate.py` |
| Closure generator | `scripts/fclr_final_structural_closure.py` |
| Frontier scanner | `scripts/next_campaign_status.py` |
| Campaign test | `tests/test_fclr_next_campaign_gate.py` |

---

## VERIFICATION COMMANDS

```bash
# Verify campaign gate still passes
python3 scripts/fclr_next_campaign_gate.py

# Verify closure regenerates deterministically (except timestamp)
python3 scripts/fclr_final_structural_closure.py

# Check data frontier
python3 scripts/next_campaign_status.py

# Run campaign gate tests
python3 -m pytest tests/test_fclr_next_campaign_gate.py -v
```

---

## CONTEXT FOR FUTURE AGENTS

This repository implements a **rigorous, pre-registered, fail-closed research program** studying whether funding rates in crypto perpetual futures predict volatility and liquidation risk. The methodology enforces:

- **Pre-registration before outcomes** (frozen preregs with `outcome_data_inspected_before_freeze: false`)
- **Terminal verdicts only** (CONFIRMED/FRAGILE/NOT_REPLICATED/INCONCLUSIVE — no "promising" or "trending")
- **Materiality floors** (≥2% relative metric reduction)
- **Robustness gates** (LOIO, placebo/permutation, bootstrap CI, leakage audit, Holm multiplicity)
- **No threshold shopping** — rules fixed in prereg
- **Cached data only** — no network access during evaluation
- **Structural closure** — program stops when all P1/P2/P3 sealed AND no feasible design frontier

The three-track structure:
- **Track A:** Observed liquidation forecasting (Hyperliquid ironflow census)
- **Track B:** Modeled breach forecasting (Bybit/Others — exhausted, no admissible source)
- **Track C:** Funding-conditioned volatility forecasting (Binance mark-price archive)

**All tracks are sealed.** The program achieved its design goal: a definitive, auditable answer to whether funding-conditioned models generalize. The answer is **no** — effects are period-specific, fragile, or non-replicable under independent recomputation.

---

**This handoff is durable and self-contained.** The next agent must read this file, verify the gate passes, verify the closure regenerates, and then enter monitoring mode. No experimental work is authorized until a reopen trigger predicate is satisfied by concrete evidence artifacts in `research_state/`.

**End of handoff — 2026-11-16T11:46:26Z**