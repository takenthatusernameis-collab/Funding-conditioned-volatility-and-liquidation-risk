# Track C Traceability Matrix — Funding-Conditioned Volatility Forecasting (H001)

**Document type:** Decision-grade traceability matrix (heavy evidence artifact)
**Repository:** Funding-conditioned-volatility-and-liquidation-risk
**Generated:** 2026-10-31T14:16:58Z
**HEAD:** a915cd38 (main). Working tree clean except untracked `scripts/__pycache__/`, `tests/__pycache__/`.
**Hypothesis:** H001 (Track C) — funding + RV + price-dislocation/smoothing features improve OOS RV forecast vs RV-only baseline.
**Status:** NOT_SUPPORTED — CONFIRMATORY PROGRAM CLOSED. Risk overlay INELIGIBLE per RESEARCH_PROMPT.md §9.
**Priority:** Track C is P0 per repo-name inference ("Funding-conditioned-volatility-and-liquidation-risk"). Track C > Track A > Track B.

## Frozen protocol elements (pre-registered; verified before outcomes)
| Element | Specification | Evidence location |
|---|---|---|
| Splits/embargo | Chronological train/validation/final holdout; >=7d calendar-day purge/embargo; boundaries from data coverage only; frozen before outcomes | `research_state/run_manifest.json` (`frozen_before_outcomes: true`); `research_state/research_protocol.md`; `research_state/sealed_holdout_integrity.md` |
| Baselines | B0 persistence (forecast next-24h RV by preceding RV24h); B1 HAR-style OLS on log RV1h, log RV24h, log RV168h predicting log next-24h RV | `research_state/research_protocol.md` §FCLR-001; `research_state/track_c_final_synthesis_dossier.md:15-16` |
| Candidates | C1 = B1 + signed funding + 90-day abs-funding percentile; C2 = C1 + mark/index premium + mark/EMA24 distance | `research_state/research_protocol.md`; `research_state/track_c_final_synthesis_dossier.md:16` |
| Primary metric | Paired OOS QLIKE (lower better); C2 vs B1; block-bootstrap CI (blocks ~24h, 2000 deterministic-seed replicates); paired n, identical forecast origins | `research_state/track_c_final_synthesis_dossier.md:17` |
| Gate | Improvement over B1 with CI excluding zero AND >= pre-registered materiality threshold AND adequate power (>=3 non-overlapping 30-day blocks); Holm multiplicity across declared family | `research_state/research_protocol.md` §FCLR-001 gate; `research_state/gate_assessment.md` |

## Cross-run traceable results (numeric trace, byte-for-byte from artifacts)
| Run | Test window | Blocks (30d non-overlap) | Paired n | Instruments | C2 vs B1 ΔQLIKE (95% CI) | Rel. to B1 | C1 vs B1 | Gate | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| FCLR-001 (pilot) | 2024-01-24..2024-03-24 | 1 (<3) | — | — | CI crosses; -2.50% rel | -2.50% | — | NOT_MET (power) | INCONCLUSIVE |
| FCLR-002 | 2024-07-23..2024-09-30 | 2 (<3) | 8274 | 5 | -0.008788 [-0.097648, -0.008788] (excl zero but underpowered) | -9.28% | — | NOT_MET (block count) | INCONCLUSIVE |
| FCLR-003 (powered confirmatory) | 2024-10-02..2024-12-31 | 3 (>=3) | 10796 | BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,XRPUSDT | +0.015205 [-0.020240, 0.056734] crosses zero | -3.78% worse | -0.032518 [-0.045813,-0.020303] (+8.09%) | NOT_MET | COMPLETE_NEGATIVE |
| FCLR-006 (unsealed 2026) | 2026-05-23..2026-08-06 | 2 (<3) | 8987 | 5 | +0.368588 [0.173748, 0.615614] entirely positive | -69.90% worse | worse | NOT_MET | COMPLETE_NEGATIVE |
| FCLR-007 (unsealed 2026 short) | 2026-07-21..2026-07-31 | 0 (<3) | 1195 | 5 | +0.010258 [0.001308, 0.019737] entirely positive | -3.42% worse | worse | NOT_MET | COMPLETE_NEGATIVE |

Sources: `research_state/evaluation_summary_FCLR002.md`, `research_state/evaluation_summary_FCLR003.md`, `research_state/evaluation_summary_FCLR006.md`, `research_state/evaluation_summary_FCLR007.md`; `research_state/track_c_final_synthesis_dossier.md:22-28`.

## Decomposition (FCLR-003, traceable)
| Model | QLIKE | Relation to B1 | Source |
|---|---|---|---|
| B0 (persistence) | 0.487674 | baseline | `research_state/track_c_final_synthesis_dossier.md:31` |
| B1 (HAR RV-only) | 0.401884 | RV-only baseline | `research_state/track_c_final_synthesis_dossier.md:31` |
| C1 (B1 + funding) | 0.369366 | -8.09% vs B1 (better) | `research_state/track_c_final_synthesis_dossier.md:31` |
| C2 (B1 + funding + price dislocation) | 0.417089 | +3.78% vs B1 (worse) | `research_state/track_c_final_synthesis_dossier.md:31` |

C2 vs B1 ΔQLIKE = +0.015205 (worse); 95% block-bootstrap CI [-0.020240, 0.056734] crosses zero. C1 shows funding helps alone but full C2 specification degrades below RV-only. Gate NOT MET. Source: `research_state/track_c_final_synthesis_dossier.md:30-33, 57-93`.

## Leakage audit (all passed; no evidence of leakage)
| Check | Result | Evidence |
|---|---|---|
| Normalization fitted on train only | passed | `research_state/track_c_final_synthesis_dossier.md:36` |
| >=7d embargo applied | passed | `research_state/track_c_final_synthesis_dossier.md:36` |
| Purge of overlapping windows | passed | `research_state/track_c_final_synthesis_dossier.md:36` |
| Timestamp alignment (features at forecast time only) | passed | `research_state/track_c_final_synthesis_dossier.md:37` |
| No holdout tuning/threshold shopping/retuning on sealed holds | passed | `research_state/track_c_final_synthesis_dossier.md:38` |
| Sealed holdout integrity; byte-identical reproductions (FCLR-002/003/006/007) | passed | `research_state/track_c_final_synthesis_dossier.md:39`; `research_state/sealed_holdout_integrity.md` |

## Multiplicity & robustness
- Holm correction across registered family; unadjusted/adjusted disclosed (`research_state/track_c_final_synthesis_dossier.md:42`)
- Cross-window consistency: only underpowered/biased windows show apparent patterns; powered confirmatory neutral/worse (`research_state/track_c_final_synthesis_dossier.md:43`)
- Instrument concentration checked; no single instrument drives result (`research_state/track_c_final_synthesis_dossier.md:44`)

## Verdict (sealed)
**H001 NOT_SUPPORTED.** Across all confirmatory evaluations C2 does not meet the pre-registered forecast gate vs B1. In the adequately-powered window (FCLR-003) effect is neutral with CI crossing zero on the worse side; in 2026 windows worse. No defensible reopen path under RESEARCH_PROMPT.md constraints (would require pre-registration/holdout discipline violations — forbidden). **Risk overlay INELIGIBLE (§9). Track C CLOSED.**

## Artifacts (traceability)
- Protocols: `research_state/research_protocol.md`, `research_state/research_protocol_fclr006.md`, `research_state/research_protocol_fclr007.md`
- Evaluations: `research_state/evaluation_summary_FCLR002.md`, `research_state/evaluation_summary_FCLR003.md`, `research_state/evaluation_summary_FCLR006.md`, `research_state/evaluation_summary_FCLR007.md`
- Manifests/audits: `research_state/run_manifest.json`, `research_state/gate_assessment.md`, `research_state/final_confirmatory_verdict.md`, `research_state/final_inconclusive_report.md`, `research_state/track_c_consolidated_dossier.md`, `research_state/leakage_audit.md`, `research_state/sealed_holdout_integrity.md`
- Tests: `python -m unittest discover -s tests -v` → 27/27 PASS at HEAD a915cd38

**CONCLUSION (SEALED):** Track C closed negative. Heavy evidence synthesis complete. No sealed-holdout re-run, no threshold shopping, no gate relaxation.
