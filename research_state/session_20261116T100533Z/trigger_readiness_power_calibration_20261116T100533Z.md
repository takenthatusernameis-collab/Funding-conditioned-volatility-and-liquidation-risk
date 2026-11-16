# FCLR Trigger-Readiness & Design-Power Calibration — 20261116T100533Z

**Offline / read-only.** No network, no parquet/outcome reads. Derived only from published primary contrasts.

## Method
- `SE = (ci_hi - ci_lo) / (2*z0.975)`; `MDE_abs = (z0.975 + z0.80)*SE`; `MDE_rel% = MDE_abs / B1 * 100`.
- `n_required = n * (MDE_rel% / 2%)^2`; achieved power `= Phi(effect/SE - z0.975)` for a true 2% effect.
- Caveat: normal approximation on reported bootstrap CIs; a design-sizing ledger, **not** a new confirmatory result.

## Historical power ledger (primary C2 vs B1)

| experiment | rel% | B1 QLIKE | n_pairs | blocks | MDE rel% | powered for 2%? | n_req for 2% | power@2% |
|---|---:|---:|---:|---:|---:|:---:|---:|---:|
| FCLR-002 | 9.28 | 0.4874 | 8274 | 2 | 13.03 | no | 351140 | 0.063 |
| FCLR-003 | -10.98 | 0.4007 | 10796 | 3 | 16.36 | no | 722667 | 0.053 |
| FCLR-009 | -0.43 | 0.3408 | 24495 | 6 | 1.95 | YES | 23224 | 0.820 |
| FCLR-011_SEALED | 4.94 | 0.3333 | 10785 | 3 | 6.67 | no | 120118 | 0.131 |
| FCLR-013 | -1.32 | 0.4522 | 4199 | 1 | 5.35 | no | 29992 | 0.181 |
| FCLR-014 | 1.14 | 0.3387 | 1918 | 0 | 5.08 | no | 12392 | 0.196 |
| FCLR-LIQ-EXPANSION-RECOMPUTE | 6.19 | 3.1147 | 593 | 3 | 8.88 | no | 11689 | 0.092 |

## Key finding

Most historical windows were underpowered for the 2% materiality floor; only FCLR-009 (n=24495, 6 blocks) was adequately powered. The Track A liquidation recompute (n=593) needs ~11689 paired observations for a 2% MDE.

## Trigger-readiness matrix

| trigger | anchor | anchor MDE rel% | n_req for 2% | sizing rule |
|---|---|---:|---:|---|
| GATE4_BRANCH_1 | FCLR-009 | 1.95 | 23224 | paired_n >= 23224 (>=5 instruments, >=3 non-overlapping 30d blocks, 7d purge/embargo) |
| NEW_OBSERVED_LIQUIDATION_SOURCE | FCLR-LIQ-EXPANSION-RECOMPUTE | 8.88 | 11689 | paired_n >= 11689 (>=5 instruments, >=3 non-overlapping 30d blocks, 7d purge/embargo) |
| HL_LABEL_EXTENSION | FCLR-LIQ-EXPANSION-RECOMPUTE | 8.88 | 11689 | paired_n >= 11689 (>=5 instruments, >=3 non-overlapping 30d blocks, 7d purge/embargo) |
| EXPANSION_ROBUSTNESS_REDO | FCLR-LIQ-EXPANSION-RECOMPUTE | 8.88 | 11689 | paired_n >= 11689 (>=5 instruments, >=3 non-overlapping 30d blocks, 7d purge/embargo) |

## Per-trigger execution contract (pre-sized, outcome-blind)

### GATE4_BRANCH_1
- Estimand: Gate 4 funding-multisplit Track C confirmatory (C2 vs B1 next-24h RV QLIKE)
- Note: Binance terms/legal attestation is human-owned; the agent cannot set RESOLVED_VERIFIED. Design is pre-sized so execution is immediate once attested.
1. read resume_trigger_registry.json + ironflow_monitor_state.json once (no network)
2. run RESEARCH_PROMPT.md section 16 admissibility/source audit
3. instantiate prereg_template_trigger_gated_* as a NEW prereg with outcome_data_inspected_before_freeze=false
4. enforce paired_n >= 23224 (>=5 instruments, >=3 non-overlapping 30d blocks, 7d purge/embargo)
5. enumerate the Holm family pre-outcomes; freeze splits before outcomes
6. register any new scripts in BOTH scope registries; run all gates; record honest verdict

### NEW_OBSERVED_LIQUIDATION_SOURCE
- Estimand: Track A observed-liquidation intensity forecast (C2 vs B1 OOS QLIKE, ironflow-style labels)
- Note: Requires an admissible, unauthenticated observed-liquidation source with >=3 blocks and >=5 instruments.
1. read resume_trigger_registry.json + ironflow_monitor_state.json once (no network)
2. run RESEARCH_PROMPT.md section 16 admissibility/source audit
3. instantiate prereg_template_trigger_gated_* as a NEW prereg with outcome_data_inspected_before_freeze=false
4. enforce paired_n >= 11689 (>=5 instruments, >=3 non-overlapping 30d blocks, 7d purge/embargo)
5. enumerate the Holm family pre-outcomes; freeze splits before outcomes
6. register any new scripts in BOTH scope registries; run all gates; record honest verdict

### HL_LABEL_EXTENSION
- Estimand: Track A observed-liquidation intensity forecast on verified post-2026-10-31 Hyperliquid labels
- Note: Requires >=100-day verified label depth beyond 2026-10-31; currently absent.
1. read resume_trigger_registry.json + ironflow_monitor_state.json once (no network)
2. run RESEARCH_PROMPT.md section 16 admissibility/source audit
3. instantiate prereg_template_trigger_gated_* as a NEW prereg with outcome_data_inspected_before_freeze=false
4. enforce paired_n >= 11689 (>=5 instruments, >=3 non-overlapping 30d blocks, 7d purge/embargo)
5. enumerate the Holm family pre-outcomes; freeze splits before outcomes
6. register any new scripts in BOTH scope registries; run all gates; record honest verdict

### EXPANSION_ROBUSTNESS_REDO
- Estimand: Track A expansion robustness: LOIO>=6/8 AND placebo>95th percentile on a NEW preregistered design
- Note: Current 8-coin panel already failed twice; only a materially new design re-opens this. Size for 2% MDE before executing.
1. read resume_trigger_registry.json + ironflow_monitor_state.json once (no network)
2. run RESEARCH_PROMPT.md section 16 admissibility/source audit
3. instantiate prereg_template_trigger_gated_* as a NEW prereg with outcome_data_inspected_before_freeze=false
4. enforce paired_n >= 11689 (>=5 instruments, >=3 non-overlapping 30d blocks, 7d purge/embargo)
5. enumerate the Holm family pre-outcomes; freeze splits before outcomes
6. register any new scripts in BOTH scope registries; run all gates; record honest verdict
