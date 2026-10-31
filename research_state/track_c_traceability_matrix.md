# Track C Traceability Matrix (H001) — Byte-Level Decomposition & Evidence

**Document type:** Traceability matrix (irrefutable)
**Repository:** Funding-conditioned-volatility-and-liquidation-risk
**Generated:** 2026-10-31T22:54:10Z
**HEAD:** 9b2b9335
**Status:** SEALED — NOT_SUPPORTED. Risk overlay INELIGIBLE per §9.

## Primary contrast (FCLR-003, powered confirmatory)
| Item | Value | Source (file:line/path) |
|---|---|---|
| Run ID | FCLR-003 | research_state/evaluation_summary_FCLR003.md, run_manifest.json |
| Test window | 2024-10-02..2024-12-31 | evaluation_summary_FCLR003.md |
| Non-overlapping 30d blocks | 3 (>=3) | evaluation_summary_FCLR003.md; gate_assessment.md |
| Paired n | 10796 | evaluation_summary_FCLR003.md |
| Instruments | BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,XRPUSDT | evaluation_summary_FCLR003.md |
| B0 (persistence) QLIKE | 0.487674 | evaluation_summary_FCLR003.md (decomposition) |
| B1 (HAR RV-only) QLIKE | 0.401884 | evaluation_summary_FCLR003.md (decomposition) |
| C1 (B1+funding) QLIKE | 0.369366 | evaluation_summary_FCLR003.md (decomposition) |
| C2 (B1+funding+price dislocation) QLIKE | 0.417089 | evaluation_summary_FCLR003.md (decomposition) |
| C2 vs B1 ΔQLIKE | +0.015205 (worse) | evaluation_summary_FCLR003.md |
| C2 vs B1 95% CI (block bootstrap, blocks~24h, 2000 reps) | [-0.020240, 0.056734] (crosses zero) | evaluation_summary_FCLR003.md |
| C1 vs B1 ΔQLIKE (95% CI) | -0.032518 [-0.045813, -0.020303] (+8.09%) | evaluation_summary_FCLR003.md |
| Relative C2 vs B1 | -3.78% (worse) | evaluation_summary_FCLR003.md |

## Cross-run traceability
| Run | Blocks | Paired n | C2 vs B1 ΔQLIKE (CI) | Notes |
|---|---|---|---|---|
| FCLR-002 | 2 (<3) | 8274 | -0.008788 [-0.097648, -0.008788] (excl zero but underpowered) | NOT_MET (power) — evaluation_summary_FCLR002.md |
| FCLR-003 | 3 (>=3) | 10796 | +0.015205 [-0.020240, 0.056734] (crosses zero, worse) | NOT_MET (gate) — evaluation_summary_FCLR003.md |
| FCLR-006 | 2 (<3) | 8987 | +0.368588 [0.173748, 0.615614] (worse) | NOT_MET — evaluation_summary_FCLR006.md |
| FCLR-007 | 0 (<3) | 1195 | +0.010258 [0.001308, 0.019737] (worse) | NOT_MET — evaluation_summary_FCLR007.md |

## Leakage/normalization/embargo checks
- Train-only normalization: ENFORCED (run_manifest.json, leakage_audit.md)
- Purge/embargo overlapping windows (>=7d): ENFORCED (research_protocol.md, leakage_audit.md)
- No threshold shopping/tuning/holdout reuse: VERIFIED (leakage_audit.md, gate_assessment.md)
- Pre-registered splits/frozen_before_outcomes: VERIFIED (run_manifest.json)
- Byte-identical reproductions: CONFIRMED (FCLR-002/FCLR-003/FCLR-006/FCLR-007)

## Verdict
NOT_SUPPORTED. Risk overlay INELIGIBLE (§9). Confirmatory CLOSED. No reopen without pre-registration + documented holdout discipline violations with evidence.
