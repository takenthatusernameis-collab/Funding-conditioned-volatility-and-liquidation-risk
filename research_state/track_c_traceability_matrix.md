# Track C Traceability Matrix (Irrefutable) — H001 Funding-Conditioned Volatility

**Generated:** 2026-10-31T16:04:XXZ (campaign run)
**HEAD:** 7c248295
**Status:** NOT_SUPPORTED — CONFIRMATORY CLOSED
**Priority:** Track C (repo name inference) — FIRST

## 1) Frozen protocol / pre-registration (trace)
| Item | Value / reference | File:line / artifact |
|---|---|---|
| Hypothesis | H001; funding+RV+price dislocation improve OOS RV/stress vs RV-only | `research_state/hypothesis_registry.json` (H001) |
| Research protocol | Frozen before outcomes; chronological splits, >=7d embargo, purge overlapping | `research_state/research_protocol.md` (frozen) |
| Baselines/Candidates | B0(persistence), B1(HAR RV-only), C1(B1+funding), C2(B1+funding+price) | `research_state/track_c_final_synthesis_dossier.md`, `research_state/evaluation_summary_FCLR003.md` |
| Primary metric/gate | Paired QLIKE, C2 vs B1 block bootstrap (~24h blocks, 2000 reps), >=3 non-overlap 30d blocks, CI exclude zero or >=threshold | `research_state/evaluation_summary_FCLR003.md`, `research_state/gate_assessment.md` |

## 2) Splits / embargoes / blocks / paired n (FCLR-003 primary)
| Item | Value | Source (file:line/artifact) |
|---|---|---|
| Data range | 2024-01-01 .. 2024-12-31 | `research_state/evaluation_summary_FCLR003.md` |
| Train | 2024-04-01T00:00:00Z .. 2024-07-23T23:00:00Z | `research_state/evaluation_summary_FCLR003.md` |
| Val | 2024-07-31T00:00:00Z .. 2024-09-24T23:00:00Z | `research_state/evaluation_summary_FCLR003.md` |
| Test | 2024-10-02T00:00:00Z .. 2024-12-31T23:00:00Z (7d embargo) | `research_state/evaluation_summary_FCLR003.md` |
| Non-overlapping 30d blocks (test) | 3 (>=3) — meets power | `research_state/track_c_final_synthesis_dossier.md`, `research_state/evaluation_summary_FCLR003.md` |
| Paired n (C2 vs B1) | 10796 | `research_state/evaluation_summary_FCLR003.md` |
| Instruments | BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT (5) | `research_state/evaluation_summary_FCLR003.md`, `research_state/track_c_final_synthesis_dossier.md` |

## 3) QLIKE decomposition (all models) — FCLR-003
| Model | mean_QLIKE (n) | File:line/artifact |
|---|---|---|
| B0 | 0.487674 (n=10800) | `research_state/evaluation_summary_FCLR003.md` |
| B1 (RV-only) | 0.401884 (n=10796) | `research_state/evaluation_summary_FCLR003.md` |
| C1 (B1+funding) | 0.369366 (n=10796) | `research_state/evaluation_summary_FCLR003.md` (-8.09% vs B1) |
| C2 (B1+funding+price) | 0.417089 (n=10796) | `research_state/evaluation_summary_FCLR003.md` (+3.78% worse vs B1) |

## 4) Paired contrasts (block bootstrap ~24h blocks, 2000 reps)
| Contrast | Mean diff (modelA - modelB), QLIKE | 95% CI | Rel. reduction | Notes | Source |
|---|---|---|---|---|---|
| C2_vs_B1 (primary) | +0.015205 | [-0.020240, 0.056734] | -3.78% (worse) | CI crosses zero; gate NOT_MET | `research_state/evaluation_summary_FCLR003.md` |
| C1_vs_B1 | -0.032518 | [-0.045813, -0.020303] | +8.09% (better) | Funding alone helps | `research_state/evaluation_summary_FCLR003.md` |
| C2_vs_C1 | +0.047723 | [0.006214, 0.095465] | -12.92% (worse) | Full price+funding set degrades | `research_state/evaluation_summary_FCLR003.md` |

## 5) Cross-run robustness (power/gate)
| Run | Window | Blocks (30d non-overlap) | C2 vs B1 | Gate | Verdict | Source |
|---|---|---|---|---|---|---|
| FCLR-001 | 2024-01-24..2024-03-24 | 1 (<3) | -2.50% rel; CI crosses | NOT_MET (power) | INCONCLUSIVE | `research_state/track_c_final_synthesis_dossier.md` |
| FCLR-002 | 2024-07-23..2024-09-30 | 2 (<3) | -9.28% rel but underpowered; [-0.097648, -0.008788] excl zero but block count fails | NOT_MET (power) | INCONCLUSIVE | `research_state/evaluation_summary_FCLR002.md`, `research_state/track_c_final_synthesis_dossier.md` |
| FCLR-003 | 2024-10-02..2024-12-31 | 3 (>=3) | +0.015205, CI [-0.020240,0.056734] crosses zero (worse) | NOT_MET (improvement) | COMPLETE_NEGATIVE | `research_state/evaluation_summary_FCLR003.md` |
| FCLR-006 | 2026-05-23..2026-08-06 | 2 (<3) | +0.368588 [0.173748,0.615614] worse | NOT_MET | COMPLETE_NEGATIVE | `research_state/evaluation_summary_FCLR006.md`, `research_state/track_c_final_synthesis_dossier.md` |
| FCLR-007 | 2026-07-21..2026-07-31 | 0 (<3) | +0.010258 [0.001308,0.019737] worse | NOT_MET | COMPLETE_NEGATIVE | `research_state/evaluation_summary_FCLR007.md`, `research_state/track_c_final_synthesis_dossier.md` |

## 6) Leakage audit (trace)
| Check | Status | Evidence |
|---|---|---|
| Train-only normalization | ENFORCED | `research_state/leakage_audit.md`, `research_state/research_protocol.md` |
| >=7d embargo | ENFORCED | `research_state/evaluation_summary_FCLR003.md` (test starts 2024-10-02, embargo noted) |
| Purge overlapping windows | ENFORCED | `research_state/leakage_audit.md` |
| No threshold shopping/tuning/holdout reuse | VERIFIED | `research_state/track_c_final_synthesis_dossier.md`, `research_state/final_confirmatory_verdict.md` |
| Sealed holdouts, reproducible | VERIFIED | `research_state/final_confirmatory_verdict.md`, manifests in `research_state/run_manifest.json` |

## 7) Final verdict (irrefutable)
**H001 NOT_SUPPORTED — CONFIRMATORY CLOSED.** C2 fails primary gate vs B1 in powered window (CI crosses zero, worse). Funding alone (C1) helps, but adding price dislocation/smoothing degrades. Risk overlay INELIGIBLE per RESEARCH_PROMPT §9. No valid reopen without pre-registration + documented holdout discipline violations with evidence.

**Cross-linked:** `research_state/track_c_final_synthesis_dossier.md`, `research_state/evaluation_summary_FCLR003.md`, `research_state/gate_assessment.md`, `research_state/final_confirmatory_verdict.md`
