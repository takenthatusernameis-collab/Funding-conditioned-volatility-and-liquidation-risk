# Track C Consolidated Evidence Dossier (FCLR-H001)

**Document type:** Decision-grade synthesis (sealed; no holdout reuse/tuning)
**Repository:** Funding-conditioned-volatility-and-liquidation-risk
**Generated:** 2026-10-31T02:24:27Z
**Hypothesis:** H001 — Do funding extremes, realized volatility, and pre-specified price dislocation/smoothing features improve OOS forecasts of future realized volatility/stress vs RV-only baseline?
**Status:** NOT_SUPPORTED (all confirmatory campaigns complete negative). Risk overlay INELIGIBLE.

## Cross-run summary (byte-identical reproduction verified)

| Run | Window (test) | Blocks (30d, non-overlap) | Paired n | C2 vs B1 ΔQLIKE (CI) | Rel QLIKE | Gate | Verdict |
|---|---|---|---|---|---|---|---|
| FCLR-003 | 2024-10-02 .. 2024-12-31 (91d) | 3 | 10796 | +0.015205 [-0.020240, 0.056734] | -3.78% | NOT_MET (CI crosses zero; improvement criteria fail) | COMPLETE_NEGATIVE |
| FCLR-006 | 2026-05-23 .. 2026-08-06 (76d) | 2 (<3) | 8987 | +0.354989 [0.168263, 0.591948] | -67.32% | NOT_MET (worse, underpowered blocks) | COMPLETE_NEGATIVE |
| FCLR-007 | 2026-07-21 .. 2026-07-31 (11d) | 0 (<3) | 1195 | +0.010258 [0.001308, 0.019737] | -3.42% | NOT_MET (worse, entirely positive CI, underpowered) | COMPLETE_NEGATIVE |

**Conclusion:** Across all three confirmatory runs, C2 (RV + funding + price features) does not meet the pre-registered gate vs B1 (RV-only). In some windows it is neutral-to-worse; in the most recent unsealed windows it is statistically worse. No path to passing gate without violating pre-registration (no tuning/holdout reuse). H001 is NOT_SUPPORTED.

## Traceability
- FCLR-003: `research_state/evaluation_summary_FCLR003.md` (generated 2026-10-29T19:13:39Z)
- FCLR-006: `research_state/evaluation_summary_FCLR006.md` (generated 2026-10-30T16:52:51Z), `research_state/reporting_errata_FCLR006.md`
- FCLR-007: `research_state/evaluation_summary_FCLR007.md` (generated 2026-10-31T00:21:05Z)
- Protocols/splits frozen pre-outcome; byte-identical reproduction verified per handoff.

## Decision
- Track C CLOSED (negative). Risk overlay INELIGIBLE per §9 of RESEARCH_PROMPT.md.
