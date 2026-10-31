# Track C Residual Audit (Heavy Evidence)
AUDIT_ID: FCLR-TRC-AUDIT-001
TIMESTAMP: 2026-10-31T01:26:30Z
SCOPE: FCLR-003, FCLR-006, FCLR-007 (H001)
PRIORITY: Track C FIRST per repo name inference

## Executive summary
H001 NOT_SUPPORTED. C2 vs B1 worse or CI crosses zero across all confirmatory/unsealed windows. C1 (RV+funding) beats B1 on powered window but C2 degrades when adding price-dislocation/EMA features. Track C fully closed.

## FCLR-003 (POWERED CONFIRMATORY, 2024-10-02..12-31)
- Window: 3 blocks × 5 symbols, n=10796 (as reported)
- Models: B1 (RV-only HAR), C1 (RV+funding), C2 (RV+funding+price-dislocation/EMA)
- C2 vs B1: QLIKE_diff = +0.015205, 95% CI [-0.020240, 0.056734] crosses zero
- Relative: -3.78% (C2 worse). Gate NOT_MET.
- C1 vs B1: +8.09% better (secondary only). C2 vs C1: -12.92%.
- Repro: byte-identical verified. Source: evaluation_summary_FCLR003.md, hypothesis_registry.json

## FCLR-006 (UNSEALED 2026-05-23..08-06, 2 blocks < 3)
- n=8987, 2 non-overlapping 30d blocks
- C2 vs B1: +0.3686 QLIKE, CI entirely positive → C2 significantly worse
- Relative: -69.90%. Gate NOT_MET. Underpowered on blocks.
- Byte-identical reproduction verified. Source: evaluation_summary_FCLR006.md

## FCLR-007 (UNSEALED 2026-07-21..07-31, 0 blocks < 3; PRE-REGISTERED BEFORE OUTCOMES)
- Test window 11 days = 0 non-overlapping 30d blocks (minimum 3 required)
- C2 vs B1: +0.010258 QLIKE, CI [0.001308, 0.019737] entirely positive → worse
- Relative: -3.42%. Gate NOT_MET.
- Pre-registered in research_protocol_fclr007.md before examining outcomes. Byte-identical repro verified.
- Coverage audit: fclr007_coverage_audit.json/md confirm window/blocks.

## Block bootstrap (methodology check)
- Paired block bootstrap over time blocks (clustered by symbol/time blocks) as implemented in forecast pipeline; seeds deterministic per experiment.
- CIs recomputed as reported; FCLR-003 CI crosses zero (decisive for powered). FCLR-006/007 entirely positive (worse).
- Hashes: see run_manifest.json (git SHA 6543b00f), experiment artifacts; byte-identical verification recorded in outcome/handoff artifacts.

## Conclusion
Track C residuals confirm H001 NOT_SUPPORTED. No path to rescue on sealed holdouts without unregistered re-tuning (forbidden). Risk overlay INELIGIBLE.
