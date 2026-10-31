# Track C Consolidated Evidence Dossier (FCLR-H001)

**Document type:** Decision-grade synthesis (sealed; no holdout reuse/tuning)
**Repository:** Funding-conditioned-volatility-and-liquidation-risk
**Generated:** 2026-10-31T02:24:27Z (restored full version 2026-10-31T02:26:45Z after truncation audit)
**Hypothesis:** H001 — Do funding extremes, realized volatility, and pre-specified price dislocation/smoothing features improve OOS forecasts of future realized volatility/stress vs RV-only baseline?
**Status:** NOT_SUPPORTED (all confirmatory campaigns complete negative). Risk overlay INELIGIBLE.

## Cross-run summary (byte-identical reproduction verified)

| Run | Window (test) | Blocks (30d, non-overlap) | Paired n | C2 vs B1 ΔQLIKE (CI) | Rel QLIKE | Gate | Verdict |
|---|---|---|---|---|---|---|---|
| FCLR-001 | 2024-01-24..2024-03-24 (sealed pilot) | 1 (<3) | — | -2.50% rel; CI [-0.123401, 0.158843] crosses zero | — | NOT_MET | PILOT/INCONCLUSIVE |
| FCLR-002 | 2024-07-23..2024-09-30 (sealed) | 2 (<3) | 8274 | -0.008788 [-0.097648, -0.008788] excludes zero | -9.28% | NOT_MET (block count) | INCONCLUSIVE |
| FCLR-003 | 2024-10-02..2024-12-31 (sealed, powered) | 3 | 10796 | +0.015205 [-0.020240, 0.056734] crosses zero | -3.78% | NOT_MET | COMPLETE_NEGATIVE |
| FCLR-006 | 2026-05-23..2026-08-06 (unsealed) | 2 (<3) | 8987 | +0.368588 [0.173748, 0.615614] entirely positive | -69.90% | NOT_MET (worse + underpowered) | COMPLETE_NEGATIVE |
| FCLR-007 | 2026-07-21..2026-07-31 (unsealed) | 0 (<3) | 1195 | +0.010258 [0.001308, 0.019737] entirely positive | -3.42% | NOT_MET (worse + underpowered) | COMPLETE_NEGATIVE |

**Conclusion:** Across all confirmatory runs, C2 (RV + funding + price features) does not meet the pre-registered gate vs B1 (RV-only). In the adequately-powered FCLR-003 window it is neutral (CI crosses zero); in the two unsealed 2026 windows it is statistically worse. No path to passing the gate without violating pre-registration (no tuning, no holdout reuse, no threshold shopping). H001 is NOT_SUPPORTED. Risk overlay INELIGIBLE per §9 of RESEARCH_PROMPT.md.

## Model definitions (frozen in protocol)
- B0: persistence — forecast next-24h RV using preceding RV24h.
- B1: HAR-style OLS on log RV1h, log RV24h, log RV168h → log next-24h RV.
- C1: B1 + signed funding + 90-day absolute-funding percentile.
- C2: C1 + mark/index premium + mark/EMA24 distance.
- Primary contrast: C2 vs B1 on paired OOS QLIKE. Secondary: C1 vs B1, C2 vs C1. Epsilon=1e-12 fixed; training-only standardization; documented smearing back-transform; no regularization/hyperparameter search.

## Traceability
- FCLR-001: `research_state/evaluation_summary.md`; protocol `research_state/research_protocol.md` v1.0
- FCLR-002: `research_state/evaluation_summary_FCLR002.md`; `research_state/fclr002_coverage_audit.json`; byte-identical repro 2026-10-28
- FCLR-003: `research_state/evaluation_summary_FCLR003.md` (2026-10-29T19:13:39Z); splits `run_manifest.json#split_boundaries_fclr003` (frozen_before_outcomes: true); independent re-run 2026-10-30 (bgp_18c914b78001ZWxMSjA8l35RtN)
- FCLR-006: `research_state/evaluation_summary_FCLR006.md` (2026-10-30T16:52:51Z); `research_state/reporting_errata_FCLR006.md`; protocol `research_state/research_protocol_fclr006.md`
- FCLR-007: `research_state/evaluation_summary_FCLR007.md` (2026-10-31T00:21:05Z); protocol `research_state/research_protocol_fclr007.md` v1.0 pre-registered BEFORE outcomes; coverage audit `research_state/fclr007_coverage_audit.md`
- All: `research_state/hypothesis_registry.json` (FCLR-H001), `research_state/run_manifest.json`, `research_state/gate_assessment.md`, `research_state/final_confirmatory_verdict.md`, `research_state/final_inconclusive_report.md`

## Decision
- Track C CLOSED (negative). Risk overlay INELIGIBLE.
- Reopen conditions: none. Reopening would require violating pre-registration/holdout discipline (forbidden by RESEARCH_PROMPT.md §8, §16).
- Multiplicity: Holm familywise correction applied across all registered contrasts and horizons; unadjusted and adjusted results disclosed.

## Verification
- `python -m unittest discover -s tests -v` → 14/14 PASS (re-verified 2026-10-31T02:26:45Z).
- Byte-identical reproduction confirmed for FCLR-002, FCLR-003, FCLR-006, FCLR-007 on independent re-runs.
- Sealed holds intact: no re-tuning, no holdout reuse, no threshold shopping, no workflow changes, no trading/paper-trading logic.