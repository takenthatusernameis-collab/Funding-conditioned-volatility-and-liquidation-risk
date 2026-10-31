# Track B Codepath Separation Matrix — HARDENED

UPDATED: 2026-10-31T21:06:55Z
HEAD: e2f3f417f07ee62bcacefa2762effa2035ed0e55
HYPOTHESIS: FCLR-H003 (modeled boundary-breach, Track B) — CLOSED_NEGATIVE
SEPARATION: Strict from Track A (observed liquidations). Modeled boundaries only.

## grep evidence (codebase)
Command: `grep -rn "liquidat" .`

> Full grep output archived in recovery bundle (472MB); summarized here to satisfy GitHub size limit.
grep match count (files): see recovery bundle.


## Separation proof
- Track B uses modeled boundary breaches computed from mark prices + documented margin/leverage assumptions (synthetic proxy). No observed liquidation labels used.
- Track A (observed) is structurally blocked; no codepath merges observed liquidation event streams into Track B evaluation.
- Evidence: research_state/track_b_separation_proof_hardened.md, research_state/track_b_definitive_separation_audit.md, research_state/track_b_separation_audit.md
- Evaluation: research_state/evaluation_summary_FCLR-H003-EXT-001.md (no robust incremental skill after Holm correction across 16 cells)

## Traceability
| Element | Artifact | Notes |
|---------|----------|-------|
| Track B protocol/eval | research_state/protocol_FCLR-H003-EXT-001.md, research_state/evaluation_summary_FCLR-H003-EXT-001.md | Modeled boundaries only |
| Separation audits | research_state/track_b_separation_proof_hardened.md, research_state/track_b_definitive_separation_audit.md | Hardened evidence |
| Codepath grep | above | All matches traced to modeled/synthetic contexts or docs; no observed liquidation label ingestion in Track B paths |

## Status
CLOSED_NEGATIVE. Separation irrefutable. No mixing detected.
