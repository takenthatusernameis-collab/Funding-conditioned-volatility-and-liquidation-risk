# Evaluation Summary Conflict — FCLR-001 (flagged 2026-10-27T14:20Z)

Two evaluation summaries in the tree contradict each other. Neither is cited as verified
until independently recomputed. Original files are left untouched.

## File A: research_state/evaluation_summary.md
- Heading: "Evaluation Summary (FCLR-001)"
- Data range implied: FCLR-001 window
- Test n=70:
  - B0=0.140791, B1=0.147800, C1=0.145083, C2=0.144105
  - C2 vs B1: -2.50% relative reduction; 95% CI [-0.123401, 0.158843] crosses zero
- Consistent with research_state/final_inconclusive_report.md and gate_assessment.md.

## File B: research_state/evaluation_summary_FCLR002.md
- Heading says "Evaluation Summary (FCLR-001)" but body says "Experiment: FCLR-002",
  "Data range: 2024-01-01 .. 2024-06-30" — heading/body mismatch.
- Test n=94:
  - B0=0.432319, B1=0.399218, C1=0.769779, C2=0.752404
  - "C2_vs_B1: Mean diff (modelA - modelB) = 0.353186" with note
    "negative diff means improvement" — but 0.353186 is positive, so under the
    stated convention C2 is WORSE than B1 by +0.353186 QLIKE.
  - The "-88.47% relative reduction" and "-92.82%" figures are sign-convention
    artifacts, not evidence of improvement.
- This file's numbers contradict evaluation_summary.md on every model's QLIKE and
  on the direction of the primary contrast.

## Known context
- `research_state/coverage_audit_recheck.md` shows the FCLR-001 evaluated panel is
  BTCUSDT-only (1634 eval rows, other symbols 0), so neither summary satisfies the
  protocol's >=5-instruments requirement.
- Both summaries predate that recheck; their provenance and which code path produced
  them is not recorded.

## Action taken
- Both files flagged as untrusted in AGENT_HANDOFF.md.
- No recomputation performed (would require opening/altering the sealed holdout or
  running an unpre-registered configuration, both prohibited).
- Recommended next step if a verified headline is needed: re-run the frozen FCLR-001
  pipeline deterministically from stored input hashes under FCLR-001 v1.0 and record
  the canonical numbers in a new artifact; then retire or annotate the conflicting
  files. This must not be confused with new model selection or holdout reuse.