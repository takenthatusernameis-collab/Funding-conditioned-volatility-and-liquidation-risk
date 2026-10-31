# Track C Traceability Matrix (Irrefutable)

UPDATED: 2026-10-31T17:16:00Z
HEAD: 096d1601
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
| Protocol/splits/embargoes/blocks | research_state/research_protocol.md, research_state/final_confirmatory_verdict.md | Frozen pre-holdout; leakage audit enforced |
| Evaluation (FCLR003) | research_state/evaluation_summary_FCLR003.md | C2 vs B1 numbers and CI |
| Consolidated synthesis | research_state/track_c_consolidated_dossier.md | Cross-experiment trace |
| Final synthesis | research_state/track_c_final_synthesis_dossier.md | Closure rationale, no-reopen |
| Leakage audit | research_state/leakage_audit.md | Timestamp/label/split/universe/transformation checks |
| Tests | tests/* (27/27 passing) | Deterministic checks green |

## Paired/block structure
Reported with paired comparisons across blocks; CI from block/bootstrap as documented in synthesis. Full numeric breakdown preserved in cited artifacts.

## Decision
Track C: NOT_SUPPORTED — CONFIRMATORY CLOSED. Do NOT reopen without pre-registration + documented holdout discipline violations with concrete evidence.
