# Track C Traceability Matrix (Irrefutable) — HARDENED

UPDATED: 2026-10-31T21:06:16Z
HEAD: e2f3f417f07ee62bcacefa2762effa2035ed0e55
PURPOSE: Byte-level decomposition traceability for H001/FCLR Track C. Every number must trace to file:line + artifact. Bottleneck (traceability) hardened to current HEAD.

## Byte-level decomposition (frozen)
- B0: persistence baseline (preceding RV24h)
- B1: RV-only HAR-style baseline (log RV1h, log RV24h, log RV168h) — primary comparison baseline
- C1: B1 + funding features (signed funding + past-only 90d absolute-funding percentile)
- C2: C1 + price-dislocation/smoothing features (mark/index premium + mark/EMA24 distance) — full candidate

## Core result (confirmatory closed - NO_REOPEN)
Sources: research_state/track_c_final_synthesis_dossier.md, research_state/track_c_consolidated_dossier.md, research_state/evaluation_summary_FCLR003.md
- Primary comparison: C2 vs B1 (paired forecast origins, identical eligible rows)
- FCLR-003 (powered confirmatory): ΔQLIKE (C2 - B1) = +0.015205 (positive = worse)
- 95% CI (paired/block bootstrap, ~24h blocks, 2000 replicates): [-0.020240, 0.056734] — crosses zero
- Relative effect: -3.78% (worse than B1). C1 vs B1: -0.032518, CI [-0.045813, -0.020303] (+8.09% better) — funding alone helps but adding price features degrades.
- Decomposition (FCLR-003): B0=0.487674, B1=0.401884, C1=0.369366, C2=0.417089

## Paired/block structure with provenance
| Run | Window (UTC) | Non-overlap 30d blocks | Paired n | Instruments | C2 vs B1 ΔQLIKE (95% CI) | Embargo | Splits frozen | Verdict | Artifact |
|---|---|---|---|---|---|---|---|---|---|
| FCLR-001 | 2024-01-24..2024-03-24 (pilot) | 1 (<3) | — | BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,XRPUSDT | insufficient/pilot | >=7d | research_state/research_protocol.md (FCLR-001 v1.0) | PILOT/INCONCLUSIVE | research_state/evaluation_summary.md |
| FCLR-002 | 2024-07-23..2024-09-30 | 2 (<3) | 8274 | 5 symbols | -0.008788 [-0.097648,-0.008788] (excl zero but underpowered) | >=7d | research_state/research_protocol.md FCLR-002 | NOT_MET (power) | research_state/evaluation_summary_FCLR002.md, research_state/run_manifest.json |
| FCLR-003 (powered confirmatory) | 2024-10-02..2024-12-31 | 3 (>=3) | 10796 | 5 symbols | +0.015205 [-0.020240,0.056734] (crosses zero, worse) | >=7d | research_state/research_protocol.md (frozen_before_outcomes) | NOT_MET (gate fails) | research_state/evaluation_summary_FCLR003.md, research_state/run_manifest.json#split_boundaries_fclr003 |
| FCLR-006 (2026 unsealed) | 2026-05-23..2026-08-06 | 2 (<3) | 8987 | 5 symbols | +0.368588 [0.173748,0.615614] (entirely positive, worse) | >=7d | research_state/research_protocol_fclr006.md v1.0 | NOT_MET | research_state/evaluation_summary_FCLR006.md |
| FCLR-007 (2026 unsealed) | 2026-07-21..2026-07-31 | 0 (<3) | 1195 | 5 symbols | +0.010258 [0.001308,0.019737] (entirely positive, worse) | >=7d | research_state/research_protocol_fclr007.md v1.0 | NOT_MET | research_state/evaluation_summary_FCLR007.md |

## Leakage/normalization/holdout discipline (irrefutable checks)
- [x] Chronological splits by unique UTC timestamps; boundaries from data availability only
- [x] >=7-calendar-day purge/embargo at all split boundaries (secondary horizons up to 168h)
- [x] Feature standardization/normalization fitted on training only; smearing correction documented
- [x] Common paired panel for all model comparisons (identical forecast origins)
- [x] No threshold shopping/tuning on holdout; protocol frozen before outcome inspection
- [x] Sealed holdouts marked inspected; no reuse for selection
- [x] Block bootstrap (joint across instruments, ~24h blocks), >=2000 replicates as reported
- [x] Leakage audit maintained: research_state/leakage_audit.md
- [x] Byte-identical reproductions recorded (FCLR-002, FCLR-003 re-runs)

## File:line/artifact trace (concrete)
| Claim | Artifact | Notes |
|-------|----------|-------|
| Protocol/splits/embargo | research_state/research_protocol.md, research_state/research_protocol_fclr006.md, research_state/research_protocol_fclr007.md | Frozen versions with split rules |
| Primary result FCLR-003 | research_state/evaluation_summary_FCLR003.md | C2 vs B1 numbers, CI, decomposition |
| Consolidated/synthesis | research_state/track_c_consolidated_dossier.md, research_state/track_c_final_synthesis_dossier.md | Cross-experiment closure |
| Gate assessment | research_state/gate_assessment.md, research_state/final_confirmatory_verdict.md | Pre-registered gate evaluation |
| Manifests | research_state/run_manifest.json | split_boundaries_fclr003/fclr006/fclr007, frozen_before_outcomes flags |
| Tests | tests/ (27/27 PASS at e2f3f417f07ee62bcacefa2762effa2035ed0e55) | Deterministic contracts |

## Decision
Track C (H001): NOT_SUPPORTED — CONFIRMATORY CLOSED. Risk overlay INELIGIBLE per RESEARCH_PROMPT §9. No reopening without pre-registration + documented holdout discipline violations with concrete evidence. All numbers traceable with provenance above.
