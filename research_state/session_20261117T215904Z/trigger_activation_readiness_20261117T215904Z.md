# Trigger-Activation Readiness Certificate — 20261117T215904Z (FCLR-TRIGGER-READINESS-01)

**Campaign:** `FCLR-TRIGGER-READINESS-01-20261117T203457Z`
**Session:** `research_state/session_20261117T215904Z/`
**Generated UTC:** 2026-11-17T21:59:04Z
**Outcome-blind:** yes — this certificate references only pre-sized trigger contracts, power floors, and machine state; it opens no outcome file.

## Programme verdict

- `promotable=false`
- `program_status=CLOSED_TERMINAL`
- `new_scientific_claim=false`
- `campaign_status=COMPLETE — FCLR-TRIGGER-READINESS-01 retired; successor state AWAITING_TRIGGER`

## Trigger contracts (pre-sized, outcome-blind)

Each trigger maps to a pre-powered executable plan. None may be executed until its reopen trigger is satisfied per `RESEARCH_PROMPT.md` §16 (admissibility/source audit first, prereg frozen before outcomes, `outcome_data_inspected_before_freeze=false`).

| trigger | estimand | paired_n floor | blocks | purge/embargo | instruments | holm family | MDE target | irreducible human step | gate decision (current) |
|---|---|---|---|---|---|---|---|---|---|
| `GATE4_BRANCH_1` | Gate 4 funding-multisplit Track C confirmatory: C2 vs B1 next-24h RV QLIKE on funding-conditioned volatility | >=23224 | >=3 non-overlapping 30d test blocks | 7d purge/embargo | >=5 | `C1_vs_B1_next24h_RV_QLIKE_secondary`, `C2_vs_B1_next24h_RV_QLIKE_primary`, `C2_vs_C1_next24h_RV_QLIKE_secondary` | <2% rel | Gate 4 v5 legal attestation: `fclr016_v5_terms_evidence_RESOLVED_*.json` with `status=RESOLVED_VERIFIED`, `fabricated=false` (human/legal-owned; agent cannot set) | REFUSE (trigger OPEN) |
| `NEW_OBSERVED_LIQUIDATION_SOURCE` | Track A observed-liquidation intensity forecast: C2 vs B1 OOS QLIKE on admissible observed-liquidation labels | >=11689 | >=3 non-overlapping 30d test blocks | 7d purge/embargo | >=5 | `B0_vs_B1_OOS_QLIKE_secondary`, `C2_vs_B1_OOS_QLIKE_primary` | <2% rel | Admissible unauthenticated source audit: `research_state/<source>_admissibility_audit_<UTC>.{md,json}` with `status=ADMISSIBLE`, `observed_labels=true`, >=5 instruments, >=3 blocks or >=1 complete month | REFUSE (trigger OPEN) |
| `HL_LABEL_EXTENSION` | Track A observed-liquidation intensity forecast on verified post-2026-10-31 Hyperliquid labels | >=11689 | >=3 non-overlapping 30d test blocks | 7d purge/embargo | >=5 | `B0_vs_B1_OOS_QLIKE_secondary`, `C2_vs_B1_OOS_QLIKE_primary` | <2% rel | Verified label extension audit: `research_state/hl_label_extension_audit_<UTC>.{md,json}` on post-2026-10-31 labels with >=100-day depth | REFUSE (trigger OPEN) |
| `EXPANSION_ROBUSTNESS_REDO` | Track A expansion robustness redo: LOIO >= 6 of 8 subsets AND placebo/permutation true effect > 95th percentile of null, on a newly preregistered design | >=11689 | >=3 non-overlapping 30d test blocks | 7d purge/embargo | >=5 | `LOIO_ge_6_of_8_primary`, `placebo_gt_95th_null_secondary` | <2% rel | Newly preregistered design with LOIO>=6/8 and placebo>95th percentile; re-scoring sealed 19.04% result forbidden | REFUSE (trigger OPEN) |

## Executable artifacts (this session dir)

- `trigger_activation_executor_20261117T215904Z.py` + `.json` — stdlib-only referee: reads `research_state/resume_trigger_registry.json` + `research_state/ironflow_monitor_state.json` once, emits one `prereg_instantiation_plan` per trigger with `outcome_data_inspected_before_freeze=false`, REFUSEs (exit 2) whenever any pre-outcome gate is unmet. Never opens an outcome file.
- `trigger_activation_selftest_20261117T215904Z.py` + `.json` — real `unittest` suite (13 tests, 0 failures, 0 errors, EXIT 0): 30d-train + 7d-embargo + 30d-test block arithmetic, non-overlap detection, `paired_n` floor enforcement (23224 / 11689), Holm-family enumeration determinism, refusal behaviour, outcome-blindness assertion.
- `trigger_check_20261117T215904Z.json` — one-shot trigger check: all four triggers `OPEN`; Ironflow `data_through=2026-10`, `consecutive_absent=3`; 2026-11/2026-12/2027-01 `CONFIRMED_ABSENT`; `any_trigger_fired=false`; `network=false`; `polling=false`.

## Do-not-run list (enforced by this certificate)

Do NOT:
- Start or re-run any sealed cached-data confirmatory estimand (FCLR-014, replication synthesis, FCLR-REPRO-SYNTH-05, FCLR-013, FCLR-010, FCLR-002/003, FCLR-009, FCLR-006, FCLR-008).
- Re-run any frontier re-audit (verify-06 / verify-07 line is CLOSED; `all_exact_match=true` reproduced twice).
- Open any outcome file (`evaluation_summary_*`, `results/*`, sealed panel, holdout) while building or executing the trigger-activation package.
- Poll the HuggingFace tree, re-probe alternative sources, use paid/credentialed/manual outcome data, or run `git lfs pull`.
- Add root-level `research_state/*.md|json` (root at 500/500 churn cap).
- Add `statsmodels` or unpinned heavy dependencies to the core path.

## Reopen-trigger path (if a trigger fires)

Follow `RESEARCH_PROMPT.md` §16: source/admissibility audit first; freeze a pre-sized prereg from `research_state/session_20261116T035833Z/prereg_template_trigger_gated_20261116T035833Z.json` with power floors from `research_state/session_20261116T100533Z/trigger_readiness_power_calibration_20261116T100533Z.md` (Gate4/TrackC `paired_n>=23224`; TrackA/HL/expansion `paired_n>=11689`; >=3 blocks; 7d purge/embargo; `outcome_data_inspected_before_freeze=false`); require a materially different estimand; execute; record an honest verdict; register any new scripts in both scope registries.

## Files read (read-only)

- `research_state/resume_trigger_registry.json` (4 triggers, all OPEN)
- `research_state/ironflow_monitor_state.json` (data_through=2026-10)
- `research_state/session_20261116T100533Z/trigger_readiness_power_calibration_20261116T100533Z.md` (power floors)
- `research_state/session_20261116T035833Z/prereg_template_trigger_gated_20261116T035833Z.json` (prereg skeleton)

## Completeness statement

The trigger-activation package triad (executor + selftest + readiness certificate) plus the trigger check is complete in this session dir. No cached-data confirmatory work remains agent-removable; scientific advance is trigger-gated only. `AGENT_HANDOFF.md` is the sole durable handoff; this certificate is subordinate to it.
