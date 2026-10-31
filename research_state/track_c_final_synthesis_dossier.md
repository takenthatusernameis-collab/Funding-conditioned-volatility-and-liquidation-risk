# Track C Final Synthesis Dossier — Funding-Conditioned Volatility Forecasting (H001)

**Document type:** Final synthesis (sealed; no holdout reuse/tuning)
**Repository:** Funding-conditioned-volatility-and-liquidation-risk
**Generated:** 2026-10-31T09:13:52Z
**HEAD:** 52506b1a
**Hypothesis:** H001 — Do funding extremes, realized volatility, and pre-specified price dislocation/smoothing features improve OOS forecasts of future realized volatility/stress vs RV-only baseline?
**Status:** NOT_SUPPORTED — CONFIRMATORY PROGRAM CLOSED. Risk overlay INELIGIBLE per §9 of RESEARCH_PROMPT.md.

## Priority rationale (repo name inference)
Repo name "Funding-conditioned-volatility-and-liquidation-risk" prioritizes Track C (funding-conditioned volatility). This dossier is the definitive synthesis for Track C.

## Frozen protocol elements (pre-registered, verified)
- **Splits/embargo:** Chronological, training-only normalization, >=7d embargo, block structure enforced. `frozen_before_outcomes: true` verified in manifests.
- **Baselines:** B0 persistence, B1 HAR-style on log RV1h,RV24h,RV168h (RV-only).
- **Candidates:** C1 = B1 + signed funding + 90-day absolute-funding percentile; C2 = C1 + mark/index premium + mark/EMA24 distance.
- **Primary metric:** Paired out-of-sample QLIKE (lower better), C2 vs B1 with block bootstrap CIs (blocks ~24h, 2000 replicates).
- **Gate:** Improvement over B1 with CI excluding zero and >= pre-registered threshold; adequate power (>=3 non-overlapping 30-day blocks). Multiplicity via Holm correction.
- **Leakage controls:** Purge/embargo overlapping windows, fit on train only, no tuning/threshold shopping/holdout reuse.

## Cross-run traceable results
| Run | Test window | Blocks (30d non-overlap) | Paired n | Instruments | C2 vs B1 ΔQLIKE (95% CI) | Rel. | C1 vs B1 | Gate | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| FCLR-001 (pilot) | 2024-01-24..2024-03-24 | 1 (<3) | — | 5 | — / CI crosses; -2.50% rel | -2.50% | — | NOT_MET | INCONCLUSIVE |
| FCLR-002 | 2024-07-23..2024-09-30 | 2 (<3) | 8274 | 5 | -0.008788 [-0.097648, -0.008788] (excl zero but underpowered) | -9.28% | — | NOT_MET (block count) | INCONCLUSIVE |
| FCLR-003 (powered confirmatory) | 2024-10-02..2024-12-31 | 3 (>=3) | 10796 | BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,XRPUSDT | +0.015205 [-0.020240, 0.056734] crosses zero | -3.78% (worse) | -0.032518 [-0.045813,-0.020303] better (+8.09%) | NOT_MET | COMPLETE_NEGATIVE |
| FCLR-006 (unsealed 2026) | 2026-05-23..2026-08-06 | 2 (<3) | 8987 | 5 | +0.368588 [0.173748, 0.615614] entirely positive | -69.90% (worse) | worse | NOT_MET (worse+underpowered) | COMPLETE_NEGATIVE |
| FCLR-007 (unsealed 2026 short) | 2026-07-21..2026-07-31 | 0 (<3) | 1195 | 5 | +0.010258 [0.001308, 0.019737] entirely positive | -3.42% (worse) | worse | NOT_MET (worse+severely underpowered) | COMPLETE_NEGATIVE |

## Decomposition (FCLR-003, traceable)
- QLIKE: B0=0.487674, B1=0.401884, C1=0.369366, C2=0.417089
- C2 vs B1: +0.015205 (worse). C2 vs C1: +0.047723 [-0.006214, 0.095465] worse. Funding helps alone in some specs (C1 better) but full price+funding set (C2) degrades over RV-only.
- Paired coverage complete; block bootstrap defensible.

## Leakage/audit checks (all passed, no evidence of leakage)
- Normalization fitted on train only; embargoes applied (>=7d); purge of overlapping windows.
- Timestamp alignment verified; features available at forecast time only.
- No holdout tuning, threshold shopping, or re-tuning on sealed holds.
- Sealed holdout integrity confirmed; byte-identical reproductions (FCLR-002, FCLR-003, FCLR-006, FCLR-007).

## Multiplicity & robustness
- Holm correction across registered family; unadjusted/adjusted disclosed.
- Cross-window consistency: only underpowered/biased windows show apparent patterns; powered confirmatory is neutral/worse.
- Instrument concentration checked; no single instrument drives result.

## Conclusion
**H001 NOT_SUPPORTED.** Across all confirmatory evaluations, C2 does not meet the pre-registered forecast gate vs B1. In the adequately-powered window (FCLR-003) effect is neutral with CI crossing zero on the worse side; in 2026 windows worse. No defensible reopen path under RESEARCH_PROMPT.md constraints (would require pre-registration/holdout discipline violations). **Risk overlay INELIGIBLE (§9). Track C CLOSED.**

## Artifacts (traceability)
- Protocols: `research_state/research_protocol.md`, `research_state/research_protocol_fclr006.md`, `research_state/research_protocol_fclr007.md`
- Evaluations: `research_state/evaluation_summary_FCLR002.md`, `research_state/evaluation_summary_FCLR003.md`, `research_state/evaluation_summary_FCLR006.md`, `evaluation_summary_FCLR007.md`
- Manifests/audits: `research_state/run_manifest.json` (fclr003/fclr006/fclr007), `research_state/gate_assessment.md`, `research_state/final_confirmatory_verdict.md`, `research_state/final_inconclusive_report.md`, `research_state/track_c_consolidated_dossier.md`, `research_state/leakage_audit.md`
- Tests: `python -m unittest discover -s tests -v` (21/21 PASS as of 2026-10-31T09:13:52Z)
