# FCLR-LIQ-OOS-FORECAST-001 — Evidence Audit

**Session:** 20261121T055825Z
**Campaign:** FCLR-LIQ-OOS-FORECAST-001-20261121T055825Z (rank-0)
**Audited:** 2026-11-21T06:54:00Z

## Artifacts (all present, non-empty, under research_state/session_20261121T055825Z/)
- fclr_liq_oos001_protocol_freeze_20261121T055825Z.{json,md} — preregistered protocol freeze (pre-outcomes)
- fclr_liq_oos001_evaluation_20261121T055825Z.{py,json,md} — OOS evaluation
- fclr_liq_oos001_recompute_20261121T055825Z.{py,json} — independent recompute (numpy/stdlib-only)
- evidence_audit_20261121T055825Z.{json,md} — this audit
- trigger_check_20261121T055825Z.json — non-empty trigger check

## Panel hashes (asserted in script headers before any computation)
- Combined liquidation panel: `fclr_liq_combined_panel_20261115T181405Z.parquet`, sha256 `81a100d5d0625832bebabaabea13b786e15319577721cfe8507da5b779ec7f14`
- FCLR-001 panel: `fclr011_recompute_panel_20261115T234700Z.parquet`, sha256 `41962f823e59de5989c7d854cb3180cad61a4cbc2f5f230133c41b321342c1f4`

## Freeze order
outcome_data_inspected_before_freeze = false. Protocol freeze precedes evaluation/recompute; no holdout outcomes inspected before freeze.

## Recompute concurrence
Independent numpy/stdlib-only code path reproduces the evaluation verdict:
- evaluation verdict: NOT_SUPPORTED
- recompute verdict: NOT_SUPPORTED
- concurrence: true

## Verdict integrity
- Verdict: NOT_SUPPORTED (honest null preserved)
- QLIKE gate: FAIL (relative reduction -5.88%, CI includes zero, materiality not met)
- Brier gate: PASS (+11.48% relative reduction favoring C2)
- LogLoss gate: PASS (+8.63% relative reduction favoring C2)
- Joint gate requires ALL three metrics -> NOT_SUPPORTED
- Materiality floor (2%) NOT relaxed after seeing outcomes; no threshold-shopping

## Constraints honored
- No sealed mutation: research_state/research_protocol.md untouched
- No .github/workflows modifications
- No root-level research_state/*.md or *.json added (all artifacts under the session dir; root churn cap 499/500 respected)
- No terminal campaigns re-run (FCLR-STARTER-001, FCLR-XSEC-001..008; FCLR-XSEC-009 not triggered)
- No network calls, no paid data, no credentials, no new data acquisition
- Track separation: observed liquidations only; no conflation with Track B modeled boundary breaches or RV forecasts

## Cross-references
Explicitly cross-references FCLR-XSEC-002/004/005/006/007/008, FCLR-LIQ-COMBINED-PANEL, Track A combined panel, Track B modeled breaches.

## Distinguishing note
This campaign forecasts OBSERVED liquidation intensity out-of-sample (funding-conditioned vs RV-only baseline), distinct from the terminal cross-sectional XSEC associations and from Track B modeled boundary-breach forecasts.
