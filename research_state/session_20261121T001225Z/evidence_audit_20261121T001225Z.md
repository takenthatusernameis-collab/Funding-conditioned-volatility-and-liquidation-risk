# FCLR-XSEC-005 Evidence Audit

**Session UTC:** 20261121T001225Z
**Campaign:** FCLR-XSEC-005-20261121T001225Z

## Evidence Checks

| Check | Status | Details |
|-------|--------|---------|
| **Panel Hash Verified** | PASS | Expected: `81a100d5d0625832bebabaabea13b786e15319577721cfe8507da5b779ec7f14`, Actual: matches |
| **Freeze Precedes Outcomes** | PASS | Protocol frozen at 20261121T001225Z before any outcome inspection; `outcome_data_inspected_before_freeze=false` |
| **No Sealed Mutation** | PASS | `research_state/research_protocol.md` (sealed legacy FCLR-001 2024-01..03) untouched; no overwrite |
| **No Root-Level Artifacts** | PASS | Root md+json count 499/500; all new artifacts under `research_state/session_20261121T001225Z/` |
| **No Network / No Paid Data** | PASS | Pure local computation on frozen panel; zero network calls |
| **No Re-run of Terminal Campaigns** | PASS | FCLR-STARTER-001, FCLR-XSEC-001, FCLR-XSEC-002, FCLR-XSEC-003, FCLR-XSEC-004 NOT re-run |
| **Track Separation Maintained** | PASS | Observed liquidations only (Track A); no modeled boundary breaches (Track B); no RV forecast conflation |
| **Distinct Estimand from FCLR-XSEC-004** | PASS | XSEC-004: count-based (event count); XSEC-005: notional-weighted (sum notional_usd, dollar severity); same panel, regime conditioning, funding predictor |
| **Cross-Reference to FCLR-XSEC-004** | PASS | XSEC-004 low-RV: CI [448605.26, 841155.73], SUPPORTED; XSEC-005 low-RV: CI [452972.90, 850198.89], SUPPORTED — **strong agreement** |
| **Evaluation Artifacts Exist** | PASS | protocol_freeze.{json,md}, evaluation.{py,json}, recompute.{py,json} all present and non-empty |
| **Independent Recompute Reproduces** | PASS | Evaluation verdict: SUPPORTED; Recompute verdict: SUPPORTED; reproduction confirmed |
| **Gate Criteria Satisfied** | PASS | Low-RV funding contrast: CI excludes zero ✓, Holm passes ✓, materiality 0.80 ≥ 0.02 ✓ → gate passed ✓ |

## Overall Status

**ALL_CHECKS_PASS** — FCLR-XSEC-005 verdict: **SUPPORTED**

The notional-weighted (dollar severity) regime-conditioned cross-sectional funding effect on next-hour observed liquidation intensity is **SUPPORTED** in the low-RV regime, confirming the FCLR-XSEC-004 count-based finding survives the outcome transform. High-RV regime remains an honest null (CI includes zero).