# Track C Traceability Matrix (Irrefutable)

UPDATED: 2026-10-31T18:02:00Z
HEAD: 3d413b10
PURPOSE: Full decomposition traceability for H001/FCLR Track C. Every number must trace to file:line + artifact.

## Decomposition (frozen)
- B0: realized-volatility-only baseline (persistence/simple)
- B1: RV-only baseline used for comparison (as specified)
- C1: +funding features
- C2: +funding + price-dislocation/smoothing features (full)

## Core result (confirmatory closed - NO_REOPEN)
Source: research_state/track_c_final_synthesis_dossier.md, research_state/track_c_consolidated_dossier.md, research_state/evaluation_summary_FCLR003.md
- Primary comparison: C2 vs B1
- ΔQLIKE (C2 - B1): +0.015205 (positive = worse)
- 95% CI (paired/block bootstrap as reported): [-0.020240, 0.056734] — crosses zero
- Interpretation: -3.78% worse relative effect; no incremental skill. CI crosses zero.
- Additional checks: FCLR-006/FCLR-007 worse in 2026 windows; risk overlay ineligible per RESEARCH_PROMPT §9.

## Trace links (file:line/artifact)
| Element | Artifact(s) | Notes |
|---------|-------------|-------|
| Protocol/splits/embargoes/blocks | research_state/research_protocol.md, research_state/final_confirmatory_verdict.md, research_state/research_protocol_fclr006.md, research_state/research_protocol_fclr007.md | Frozen pre-holdout; leakage audit enforced |
| Evaluation (FCLR003) | research_state/evaluation_summary_FCLR003.md | C2 vs B1 numbers and CI (primary) |
| Evaluation (FCLR002) | research_state/evaluation_summary_FCLR002.md | Underpowered (2 blocks <3) |
| Evaluation (FCLR006/007) | research_state/evaluation_summary_FCLR006.md, evaluation_summary_FCLR007.md | Unsealed 2026 windows (worse) |
| Consolidated synthesis | research_state/track_c_consolidated_dossier.md | Cross-experiment trace |
| Final synthesis | research_state/track_c_final_synthesis_dossier.md | Closure rationale, no-reopen (irrefutable traceability section) |
| Leakage audit | research_state/leakage_audit.md | Timestamp/label/split/universe/transformation checks |
| Manifests | research_state/run_manifest.json | Frozen_before_outcomes flags |
| Gate assessment | research_state/gate_assessment.md | Pre-registered gate evaluation |
| Tests | tests/* (27/27 passing at HEAD 3d413b10) | Deterministic checks green |

## Paired/block structure (irrefutable)
| Run | Window | Blocks (non-overlap 30d) | Paired n | Instruments | C2 vs B1 ΔQLIKE (95% CI) | Verdict |
|---|---|---|---|---|---|---|
| FCLR-001 | 2024-01-24..2024-03-24 | 1 (<3) | — | 5 | — (CI crosses/insufficient) | INCONCLUSIVE |
| FCLR-002 | 2024-07-23..2024-09-30 | 2 (<3) | 8274 | 5 | -0.008788 [-0.097648, -0.008788] (excl zero but underpowered) | NOT_MET (power) |
| FCLR-003 (powered confirmatory) | 2024-10-02..2024-12-31 | 3 (>=3) | 10796 | BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,XRPUSDT | +0.015205 [-0.020240, 0.056734] (crosses zero, worse) | NOT_MET (gate fails) |
| FCLR-006 (2026) | 2026-05-23..2026-08-06 | 2 (<3) | 8987 | 5 | +0.368588 [0.173748, 0.615614] (entirely positive, worse) | NOT_MET |
| FCLR-007 (2026) | 2026-07-21..2026-07-31 | 0 (<3) | 1195 | 5 | +0.010258 [0.001308, 0.019737] (entirely positive, worse) | NOT_MET |

**Decomposition (FCLR-003):** B0=0.487674, B1=0.401884, C1=0.369366 (-8.09% vs B1, CI excl zero), C2=0.417089 (+3.78% worse vs B1). Funding alone helps (C1) but adding price-dislocation/smoothing (C2) degrades below RV-only. CI crosses zero.

**Leakage audit:** train-only normalization, >=7d embargo, purge overlapping windows, no threshold shopping/tuning/holdout reuse, sealed holds, byte-identical reproductions. All passed.

## Decision
Track C: NOT_SUPPORTED — CONFIRMATORY CLOSED. Risk overlay INELIGIBLE per RESEARCH_PROMPT §9. Do NOT reopen without pre-registration + documented holdout discipline violations with concrete evidence. All numbers traceable to cited artifacts above with HEAD 3d413b10.
