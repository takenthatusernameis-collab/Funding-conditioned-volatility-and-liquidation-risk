# FCLR Replication Meta-Synthesis — 2026-11-17T07:12:34Z

**Campaign:** `FCLR-REPRO-SYNTH-05`
**Studies:** 7 independent recomputes
**Qualitative corroboration:** 7/7 (Wilson95 0.646–1.000)

## Per-study results (C2 vs B1 unless noted)

| Study | Rel reduction % | 95% CI | n | Mat>=2% | Blocks>=3 | LOIO | Placebo | Tolerance | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| FCLR-002 | 8.599 | [-0.09339, -0.005759] | 8274 | True | None | None | None | False | DIVERGED_BEYOND_TOLERANCE |
| FCLR-003 | -11.846 | [0.004045, 0.09761] | 10796 | True | None | None | None | False | DIVERGED_BEYOND_TOLERANCE |
| FCLR-006 | -67.323 | [0.1683, 0.5919] | 8987 | True | None | None | None | True | REPRODUCED_WITHIN_TOLERANCE |
| FCLR-008 | 0.686 | [-0.06363, -0.02577] | 10800 | False | None | None | None | False | DIVERGED_BEYOND_TOLERANCE |
| FCLR-009 | -0.425 | [-0.00312, 0.006165] | 24495 | False | None | None | None | True | REPRODUCED_WITHIN_TOLERANCE |
| FCLR-010 | 0.501 | [-0.001106, -0.0003164] | 64056 | False | True | False | False | None | NOT_REPLICATED |
| FCLR-013 | -4.989 | [-0.000523, 0.03481] | 4200 | False | False | False | True | None | NOT_REPLICATED |

## Summary
- Qualitative corroboration: 7/7 (Wilson95 0.646–1.000)
- Reproduced within tolerance: 2/7 -> ['FCLR-006', 'FCLR-009'] (Wilson95 0.082–0.641)
- Diverged beyond tolerance (exact values, qualitative NOT_MET agrees): ['FCLR-002', 'FCLR-003', 'FCLR-008']
- Promotable positive results (materiality>=2% AND blocks>=3): NONE

## Program verdict
All 7 completed independent recomputes corroborate the sealed qualitative programme verdict (no sealed NOT_MET / NOT_REPLICATED result is overturned into a promotable positive claim). Exact within-tolerance reproduction holds for 2/7 (FCLR-006, FCLR-009); FCLR-002/003/008 diverge beyond tolerance on exact values but agree on the qualitative NOT_MET direction; FCLR-010/013 are fresh recomputes returning NOT_REPLICATED. No study clears both the 2% materiality floor and the >=3-block requirement, so no promotable positive result exists. The programme remains CLOSED_TERMINAL with no claim-worthy promotable result.

## Per-study notes
- **FCLR-002**: Recomputed values diverge beyond tolerance; the divergence is a finding, not a tuning target.
- **FCLR-003**: Recomputed values diverge beyond tolerance; the divergence is a finding, not a tuning target.
- **FCLR-006**: Independent recompute reproduces all published FCLR-006 QLIKE values, n, and the C2-vs-B1 contrast (mean diff, relative reduction, CI, n_pairs) within declared tolerance. The FCLR-006 NOT_MET terminal headline (block criterion 2 < 3 blocks) is corroborated by an independent code path.
- **FCLR-008**: Independent recompute diverged from published FCLR-008 values beyond tolerance; investigate feature construction / row eligibility / OLS details.
- **FCLR-009**: Independent recompute reproduces all published FCLR-009 QLIKE values, n, and the C2-vs-B1 contrast (mean diff, relative reduction, CI, n_pairs) within declared tolerance. The FCLR-009 NOT_MET terminal headline is corroborated by an independent code path.
- **FCLR-013**: Independent recompute complete; verdict issued honestly without re-scoring sealed summary.
