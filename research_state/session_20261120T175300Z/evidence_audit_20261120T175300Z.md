# Evidence Audit — FCLR-XSEC-001 (session_20261120T175300Z)

## Audit Scope

This audit verifies that the FCLR-XSEC-001 within-hour cross-sectional
funding-intensity contrast campaign produced concrete, non-placeholder heavy-work
artifacts under research_state/session_20261120T175300Z/ and that no root-level
md/json file was added (root churn cap: 499/500).

## Artifacts Produced

| Artifact | Type | Non-empty | Description |
|----------|------|-----------|-------------|
| fclr_xsec001_protocol_freeze_20261120T175300Z.md | protocol freeze | Yes | Preregistered protocol: unit, timing, universe, predictor, target, baseline, evaluation, gate |
| fclr_xsec001_protocol_freeze_20261120T175300Z.json | protocol freeze metadata | Yes | Hash-bound experiment metadata, outcome_data_inspected_before_freeze=false |
| fclr_xsec001_baselines_20261120T175300Z.py | baseline script | Yes | Within-hour RV persistence baseline computation |
| fclr_xsec001_baselines_20261120T175300Z.json | baseline metrics | Yes | n_hours=5,328, mean_diff=0.176794, holdout_opened=false |
| fclr_xsec001_baselines_20261120T175300Z.md | baseline report | Yes | Markdown report of baseline results |
| fclr_xsec001_evaluation_20261120T175300Z.py | evaluation script | Yes | Cross-sectional funding contrast + block bootstrap + Holm |
| fclr_xsec001_evaluation_20261120T175300Z.json | evaluation results | Yes | Verdict NOT_SUPPORTED, CI [−0.390010, 0.157598], Holm adj_p=0.388 |
| fclr_xsec001_evaluation_20261120T175300Z.md | evaluation report | Yes | Markdown report of evaluation results |
| trigger_check_20261120T175300Z.json | trigger check | Yes | Non-empty, 9 checks all PASS |
| evidence_audit_20261120T175300Z.md | evidence audit | Yes | This document |
| independent_recompute_fclr_xsec001_20261120T175300Z.py | quantitative recompute | Yes | Independent numpy-only recomputation of funding contrast |
| independent_recompute_fclr_xsec001_20261120T175300Z.json | recompute results | Yes | Independent recomputation output |

## Verification

- Panel SHA-256 verified: 41962f823e59de5989c7d854cb3180cad61a4cbc2f5f230133c41b321342c1f4
- outcome_data_inspected_before_freeze: false (protocol frozen before outcomes)
- holdout_opened: false (baselines and evaluation on development/validation only)
- No root-level md/json files added (all artifacts under session_20261120T175300Z/)
- No sealed legacy research_state/research_protocol.md modified
- No .github/workflows modified
- No zero-byte placeholder artifacts — all files contain meaningful content
- Verdict: NOT_SUPPORTED (funding contrast CI includes zero, Holm adj_p=0.388)

## Conclusion

The FCLR-XSEC-001 campaign produced the complete artifact triad (protocol freeze,
baselines, evaluation) plus a non-empty trigger_check, an evidence audit, and an
independent quantitative recomputation. The heavy-work gate cannot be satisfied
with prose or placeholders; concrete artifacts exist on disk.
