# FCLR Heavy Campaign (Trigger-Only) — 2026-11-15T22:57:29Z

**Frontier rank 0:** `FCLR-BOUNDED-TRIGGER-ONLY-20261115T220000Z` (TRIGGER_ONLY / BOUNDED_TRIGGER_ONLY, `next_action_heavy=null`, `all_terminal=true`).
**Sole handoff:** `AGENT_HANDOFF.md`. This is the durable bounded campaign note referenced by the frontier; it is **non-skippable while trigger-only**.
**Governing rules:** `RESEARCH_PROMPT.md`. Never re-run concluded estimands, never re-score sealed results, never fabricate data, never edit `.github/workflows/*`, no polling, no paid/credentialed/manual outcome data.

## Why this campaign exists (ground truth, verified 2026-11-15T22:57:29Z)
Every cached-data estimand in the program is terminal. This is not a hypothesis — it is recorded evidence:
- **Track A (observed liquidation):** all cross-sectional / combined estimands NOT_MET/SUPERSEDED — `FCLR-LIQ-XSEC-QLIKE-20261115T214949Z`, `FCLR-LIQ-XSEC-ORDERING-20261115T203507Z`, `FCLR-LIQ-COMBINED-20261115T185844Z`. Forward progress is blocked on external ironflow data (`data_through=2026-10`; 2026-11..2027-01 CONFIRMED_ABSENT).
- **Track B (modeled boundary breach):** `H_trackb_modeled_breaches` NOT_SUPPORTED / terminal. TB1 degenerate (zero test events); TB2 event-adequate but +1.68% < 2% floor and only 2 test blocks. All admissible local Track B routes executed.
- **Track C / H001 (funding-conditioned volatility):** `H1_primary` NOT_SUPPORTED; v3_30d is data-sufficient (5 instruments, 4 non-overlapping 30-day blocks) but null on the primary contrast. Risk overlay INELIGIBLE.
- **H2 (Shek replication):** EXPLORATORY_ONLY (`promotable=false`).

Therefore the agent-removable heavy work is **reproducibility, result-integrity, leakage, and program-level power/structural-shortfall synthesis**. A new confirmatory estimand is NOT available on cached data; do not invent one and do not re-run the concluded cells.

## Resume triggers (all OPEN unless evidenced)
Check **once** per session start via `research_state/resume_trigger_registry.json` + `research_state/ironflow_monitor_state.json` (no polling, no re-probe): `GATE4_BRANCH_1` (human/legal attestation; agent cannot set), `NEW_OBSERVED_LIQUIDATION_SOURCE` (ironflow `data_through=2026-10`, 2026-11+ absent), `HL_LABEL_EXTENSION`, `EXPANSION_ROBUSTNESS_REDO` (only a NEW prereg meeting stated conditions; never re-run/re-score sealed designs).

## Mandatory heavy work (default; do NOT stop after the trigger check)
A session that only runs the trigger check and the unit suite is **incomplete**. The session is complete only when every Phase B artifact below exists and Phase C is recorded.

### Phase A — Trigger check (once)
1. Read the two trigger files above; confirm `data_through=2026-10` and 2026-11..2027-01 absent. Record the check (timestamp + verdict) in `AGENT_HANDOFF.md`. Do not poll or re-probe.
2. If a trigger is satisfied with its required evidence artifact, jump to Phase D.

### Phase B — Reproducibility & result-integrity hardening (heavy, mandatory)
3. **Materialize LFS artifacts.** Run `git lfs checkout -- research_state/run_manifest.json` and `git lfs checkout -- research_state/run_manifest*.json`; run `git lfs ls-files` to list every pointer. For any object whose content is not local (`git lfs fetch` fails), record the exact path + pointer oid as an environmental blocker in the report — never fabricate content. (As of 2026-11-15T22:57:29Z, `run_manifest.json` is restored to valid JSON, 17,113 bytes; the `run_manifest_funding_v2_5sym`, `v3_30d`, `v3_30d_exploratory_v4`, `v4_exploratory_30d`, `explor_5sym`, `repro` objects are NOT local and `git lfs fetch` could not retrieve them in this sandbox.)
4. **Manifest/JSON validation.** Parse every materialized `research_state/*.json` manifest plus `experiment_frontier.json` and `hypothesis_registry.json`; write `research_state/manifest_validation_<UTC>.json` with path, parse status, byte size, and schema-key presence. Zero parse failures required (LFS-pointer-only files are reported as `UNMATERIALIZED`, not silently skipped).
5. **Independent recomputation.** Recompute the program's canonical headline metrics end-to-end from cached inputs with the existing deterministic scripts, then compare to the stored summaries within the declared numerical tolerance:
   - `python3 scripts/fclr011_recompute_audit.py --out-utc <UTC>` — independent recomputation of the only volatility gate PASS (FCLR-011, C2 vs B1 QLIKE).
   - `python3 scripts/run_funding_ablations.py --split-design v3_30d --start 2024-04-01 --end 2024-09-30 --include-cache --out-suffix _repro_<UTC>` — reproduction of the data-sufficient funding ablation (v3_30d).
   - Write `research_state/reproducibility_recompute_<UTC>.json` with per-metric expected / observed / abs-diff / tolerance / pass. A mismatch beyond tolerance is a blocking defect to diagnose, not to explain away.
6. **Result-integrity reconciliation.** Confirm every expected model/feature/target/fold combination has exactly one terminal status — no duplicates, no missing keys, no silently skipped failures — across the result ledger, frontier, hypothesis registry, and evaluation summaries. Write `research_state/result_integrity_<UTC>.json`.
7. **Leakage / adversarial audit refresh.** Re-run the leakage audit (`python3 scripts/run_gate4_v4_leakage_audit.py`) and the scope-drift check; confirm no unresolved timestamp, purge/embargo, survivorship, or alignment issue. Write `research_state/leakage_audit_<UTC>.md`.
8. **Regression gates green.** `python3 -m unittest discover -q` (0 failures; baseline 1341 tests, 1 skipped), `python3 scripts/check_tracka_scope_registry_drift.py` PASS, and `python3 -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_117 tests.test_tracka_hardening_118` PASS. Keep the rank-0 TRIGGER_ONLY sentinel active — never delete it.

### Phase C — Program-level power & structural-shortfall synthesis (heavy analysis, mandatory)
9. Produce `research_state/program_power_synthesis_<UTC>.{json,md}`: for each terminal track (A/B/C/H2), record the estimand, the achieved sample (instruments, test blocks, events), the observed effect + uncertainty, the pre-registered materiality floor, and the **minimum detectable effect** given the achieved sample. State plainly whether each null is (a) a true absence of skill, (b) an underpowered/degenerate design, or (c) externally blocked. Cite the exact artifacts.
10. Conclude with a single `next_action_heavy` recommendation that is honest about the external-data dependency. Do **not** manufacture a new estimand to escape the trigger-only state; if no materially different, adequately-powered design exists on cached data, say so with evidence.

### Phase D — Trigger-gated advance (only if a trigger fires)
Pre-outcomes prereg first (`outcome_data_inspected_before_freeze=false`); §16 admissibility audit; materially different estimand only; execute eval+gates; register new scripts in both scope registries; update `experiment_frontier.json` / `hypothesis_registry.json`; install as rank-0 active heavy cell with an honest verdict. Forbidden: re-run concluded estimands, re-probe TERMINAL_NO_GO families, mutate sealed artifacts, edit `.github/workflows/*`, paid/credentialed/manual outcome data, polling.

## Session closeout (all boxes required)
- [ ] Trigger checked once, verdict recorded.
- [ ] Phase B artifacts written: `manifest_validation_<UTC>.json`, `reproducibility_recompute_<UTC>.json`, `result_integrity_<UTC>.json`, `leakage_audit_<UTC>.md`.
- [ ] Phase C `program_power_synthesis_<UTC>.{json,md}` written with per-track MDE and structural classification.
- [ ] Full suite + drift + guards green.
- [ ] `AGENT_HANDOFF.md` updated with exact commands/results and remaining blockers.
Stop cleanly ONLY when all boxes are checked. Never leave the suite red, never delete the rank-0 sentinel, never claim completion from prose alone.