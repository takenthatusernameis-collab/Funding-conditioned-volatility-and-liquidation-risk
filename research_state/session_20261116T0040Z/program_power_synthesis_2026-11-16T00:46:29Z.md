# Program Power & Structural-Shortfall Synthesis — 2026-11-16T00:46:29Z

**Program:** FCLR (Funding-conditioned Volatility and Liquidation Risk)
**Scope:** terminal tracks A/B/C/H2
**MDE method:** MDE(80% power, two-sided alpha=0.05) = (z_{0.975}+z_{0.80}) * SE, SE=(CI_hi-CI_lo)/(2*z_{0.975}); relative MDE = MDE / baseline-mean

## Per-track synthesis

| Track | Experiment | Achieved sample | Observed effect | Materiality floor | MDE (rel) | Classification |
|---|---|---|---|---|---|---|
| A_observed_liquidation_combined | FCLR-LIQ-COMBINED-20261115T185844Z | 15 instr; 3 blocks; 1221 events | rel_reduction_pct=-17.1, mean_diff_qlike=10.2516, p=0.085 | 2.0% | 25.37 | UNDERPOWERED (MDE ~25.4% >> 2% floor; CI spans 0) |
| A_observed_liquidation_xsec_qlike | FCLR-LIQ-XSEC-QLIKE-20261115T214949Z | 15 instr; ? blocks; ? events | rel_improvement_pct=-75.56, ci_hi=86.08 | 2.0% | n/a | UNDERPOWERED / DEGENERATE (only 2 of 3 blocks evaluable; CI spans 0; NOT_MET) |
| B_modeled_boundary_breach_TB2 | trackb_TB2_20261110T190405Z | 5 instr; 2 blocks; 619 events | rel_ll_reduction_pct=1.6781, ll_diff=-0.000932, p=0.488 | 2.0% | 3.44 | UNDERPOWERED (MDE ~3.4% > 2% floor; only 2 test blocks < 3 required) |
| B_modeled_boundary_breach_TB1 | trackb_TB1_20261110T173838Z | 5 instr; 4 blocks; 0 events | test_prevalence=0.0, note=zero test-set breach events | 2.0% | n/a | DEGENERATE (zero test events -> metrics undefined) |
| C_funding_conditioned_volatility_H1 | run_funding_ablations v3_30d + FCLR-011 | 5 instr; 4 blocks; 12969 events | E_vs_A_point=0.4879, A_qlike=0.7983, FCLR011_sealed_rel_pct=4.94, FCLR011_forward=NOT_REPLICATED, FCLR011_independent_re | 2.0% | 110.97 | TRUE NULL / NON-REPRODUCIBLE (E vs A CI spans 0; MDE ~111% >> 2% floor; sealed FCLR-011 does not replicate forward and does not independently reproduce) |
| H2_shek_replication | FCLR-SHEK-SCALE-20261115T071135Z | scaled exploratory arms A/B | status=EXPLORATORY_ONLY, promotable=False | None% | n/a | EXPLORATORY_ONLY (not a confirmatory test; promotable=false) |

## Structural read

- **Externally blocked:** Track A forward progress requires new observed liquidation data (ironflow data_through=2026-10; 2026-11..2027-01 absent).
- **Underpowered / degenerate:** Tracks A and B achieved MDEs far above their 2% materiality floors; TB1 is degenerate (zero events), TB2 has only 2 test blocks, xsec has only 2 of 3 evaluable blocks.
- **True absence of skill:** Track C H1 is a true null on the data-sufficient v3_30d design; the sealed FCLR-011 PASS does not replicate forward and does not independently reproduce.
- **Exploratory:** H2 remains EXPLORATORY_ONLY / not promotable.

## Next heavy action

No agent-removable confirmatory estimand remains on cached data. The only honest heavy work is (1) preserve the bounded reproducibility/integrity/power campaign (this artifact + manifest/result-integrity/leakage artifacts + green suite) and (2) hold rank-0 TRIGGER_ONLY until an external trigger fires. Do not invent a new estimand or re-run concluded cells. If a trigger fires (new observed liquidation source, HL label extension, legal attestation, or a genuinely new EXPANSION_ROBUSTNESS_REDO prereg), freeze a NEW pre-outcomes prereg with adequate power (>=3 blocks, MDE below the 2% floor) and execute it as rank 0.

## Evidence

- `research_state/evaluation_summary_FCLR-LIQ-COMBINED-20261115T185844Z.md`
- `research_state/evaluation_summary_FCLR-LIQ-XSEC-QLIKE-20261115T214949Z.json`
- `research_state/evaluation_summary_trackb_TB2_20261110T190405Z.md`
- `research_state/evaluation_summary_trackb_TB1_20261110T173838Z.md`
- `research_state/evaluation_summary_funding_v3_30d.md`
- `research_state/session_20261116T0040Z/reproducibility_recompute_2026-11-16T00:45:10Z.json`
- `research_state/evaluation_summary_FCLR-SHEK-SCALE-20261115T071135Z.json`
