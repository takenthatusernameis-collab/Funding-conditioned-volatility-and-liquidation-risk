# AGENT HANDOFF — 2026-11-15T23:13:19Z

**Project:** Funding-conditioned Volatility and Liquidation Risk (FCLR)
**Repository:** `Funding-conditioned-volatility-and-liquidation-risk`
**Sole durable handoff:** this file (`AGENT_HANDOFF.md`). `NEXT_SESSION_HANDOFF.md` and `NEXT_SESSION_TASK.md` = tombstones (no authority). `AGENT_HANDOFF_20261115T073240Z.md` = RETIRED/SUPERSEDED — ignore. `research_state/FCLR_CAMPAIGN_NEXT.md` = SUPERSEDED historical evidence.

## STATE (verified 2026-11-15T23:13:19Z, HEAD f839b2726, tree clean)
- **Full regression:** `python3 -m unittest discover -q` → `Ran 1341 tests`, `OK (skipped=1)`, 0 failures (baseline 371s; green on clean tree at HEAD f839b2726).
- **Scope drift:** `python3 scripts/check_tracka_scope_registry_drift.py` → `scripts=195 registry=195 reason=OK`.
- **Invariants:** `python3 -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_117 tests.test_tracka_hardening_118` → 38 tests OK.
- **Frontier rank 0:** `FCLR-BOUNDED-TRIGGER-ONLY-20261115T220000Z` | `TRIGGER_ONLY` | `program_status=BOUNDED_TRIGGER_ONLY` | `next_action_heavy=null` | `all_terminal=true`.
- **Concluded NOT_MET/SUPERSEDED (do not re-run):** `FCLR-LIQ-XSEC-QLIKE-20261115T214949Z`, `FCLR-LIQ-XSEC-ORDERING-20261115T203507Z`, `FCLR-LIQ-COMBINED-20261115T185844Z`. Hypotheses `H_fclr_liq_xsec_qlike_forecast`, `H_fclr_liq_xsec_ordering_forecast`, `H_fclr_liq_combined_panel_forecast` = NOT_MET.
- **Other terminal tracks:** `H1_primary` NOT_SUPPORTED (v3_30d data-sufficient but null); `H_trackb_modeled_breaches` NOT_SUPPORTED (TB1 degenerate, TB2 NOT_MET); `H2_shek_replication` EXPLORATORY_ONLY (`promotable=false`).
- **Triggers all OPEN (external):** `GATE4_BRANCH_1` (human/legal attestation), `NEW_OBSERVED_LIQUIDATION_SOURCE` (ironflow `data_through=2026-10`; 2026-11..2027-01 CONFIRMED_ABSENT), `HL_LABEL_EXTENSION`, `EXPANSION_ROBUSTNESS_REDO` (do not re-run sealed designs). See `research_state/resume_trigger_registry.json`, `research_state/ironflow_monitor_state.json`.
- **LFS state:** `research_state/run_manifest.json` restored to valid JSON (17,113 bytes) via `git lfs checkout`. The `run_manifest_funding_{v2_5sym,v3_30d,v3_30d_exploratory_v4,v4_exploratory_30d,explor_5sym,repro}.json` objects are NOT local and `git lfs fetch` could not retrieve them in this sandbox (environmental blocker; do not fabricate content).

## BOTTLENECKS REMOVED THIS SESSION
1. **Stale handoff traps neutralized.** `NEXT_SESSION_TASK.md` and `NEXT_SESSION_HANDOFF.md` still pointed at `FCLR-LIQ-XSEC-QLIKE-20261115T203550Z` as `READY_EXECUTE`/`ACTIVE` even though that cell concluded NOT_MET — a future agent could have re-run a concluded estimand. Both are now tombstones pointing here.
2. **`run_manifest.json` was an unmaterialized LFS pointer** (many scripts read it as JSON). Restored via `git lfs checkout`; verified valid JSON.
3. **Full suite was "started but not completed" in the prior handoff.** Now verified green end-to-end (1341 tests, 0 failures, 1 skipped).
4. **Reverted test-mutated cache timestamp** (`research_state/ironflow_fastpath_cache.json`) so the tree is clean for the next session.

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION (heavy, default — non-skippable)

**Repository mission (FCLR):** determine whether extreme perpetual-futures funding conditions, realized volatility, and pre-specified price-dislocation/smoothing features improve out-of-sample forecasts of future volatility and liquidation-related stress — using only admissible, free, unauthenticated data. Track A (observed liquidation) is externally blocked (`data_through=2026-10`; 2026-11..2027-01 CONFIRMED_ABSENT). All cached-data estimands are terminal. **The agent-removable heavy work is the bounded reproducibility/integrity/power campaign below — not a new estimand.**

### Phase A — Trigger check (run once at session start, no polling)
1. Read `research_state/resume_trigger_registry.json` and `research_state/ironflow_monitor_state.json`; confirm all 4 triggers remain OPEN and `data_through=2026-10` with 2026-11..2027-01 absent. Record timestamp + verdict in `AGENT_HANDOFF.md`. Do not re-probe or poll.
2. If any trigger is newly satisfied with its required evidence artifact, pivot immediately to Phase D.

### Phase B — Heavy reproducibility & integrity (mandatory while trigger-only)
3. Materialize/validate LFS manifests: `git lfs checkout -- research_state/run_manifest.json`; `git lfs ls-files`; write `research_state/manifest_validation_<UTC>.json` (zero parse failures; unmaterialized objects reported, never faked).
4. Independent recomputation: `python3 scripts/fclr011_recompute_audit.py --out-utc <UTC>` and `python3 scripts/run_funding_ablations.py --split-design v3_30d --start 2024-04-01 --end 2024-09-30 --include-cache --out-suffix _repro_<UTC>`; write `research_state/reproducibility_recompute_<UTC>.json` with per-metric expected/observed/tolerance/pass.
5. Result-integrity reconciliation → `research_state/result_integrity_<UTC>.json`; leakage audit → `research_state/leakage_audit_<UTC>.md`.
6. Regression gates green: `python3 -m unittest discover -q` (0 failures), scope-drift PASS, active-campaign/hardening guards PASS. Keep the rank-0 TRIGGER_ONLY sentinel active.

### Phase C — Program-level power & structural-shortfall synthesis (mandatory)
7. Write `research_state/program_power_synthesis_<UTC>.{json,md}`: per-track estimand, achieved sample, effect + uncertainty, materiality floor, minimum detectable effect, and classification (true null vs underpowered/degenerate vs externally blocked). Do not invent a new estimand to escape trigger-only.

### Phase D — Trigger-gated advance (only if a trigger fires)
8. Freeze a NEW, materially different pre-outcomes prereg (`outcome_data_inspected_before_freeze=false`), run admissibility/audit per `RESEARCH_PROMPT.md`, execute eval+gates, register scripts in both registries, update `experiment_frontier.json`/`hypothesis_registry.json`, install as rank-0 heavy cell. Never re-run concluded estimands, never re-probe TERMINAL_NO_GO families, never re-score sealed results.

### Phase E — Closeout
9. Update this handoff (timestamp, verified/fixed items, exact commands/results, remaining external blockers). Commit a checkpoint only if repository convention/permissions require it; otherwise leave the tree clean and documented.

**Stop cleanly ONLY when:** trigger checked once + every Phase B/C artifact written + full suite/guards green + this handoff reflects ground truth with external blockers documented. "No trigger → stop cleanly" is NOT completion. Phase B and Phase C are non-skippable heavy work.

## HARD CONSTRAINTS (non-negotiable)
- ❌ Never reopen sealed/terminal families or mutate sealed artifacts; never edit `.github/workflows/*`.
- ❌ No outcome-peeking/threshold tuning before prereg; no paid/credentialed/manual data for outcomes.
- ❌ No polling, no re-running concluded estimands, no re-probing TERMINAL_NO_GO families.
- ❌ Do not fabricate new data/sources or claim triggers satisfied without required artifacts/fields.
- ✅ `H2_shek_replication` remains `EXPLORATORY_ONLY` (`promotable=false`).
- ✅ Exactly one durable handoff: `AGENT_HANDOFF.md`.

## KEY REFERENCES
- `research_state/experiment_frontier.json`, `research_state/resume_trigger_registry.json`, `research_state/ironflow_monitor_state.json`
- `research_state/FCLR_HEAVY_CAMPAIGN_NEXT.md` (authoritative heavy campaign), `research_state/negative_results_report.md`
- `research_state/evaluation_summary_funding_v3_30d.md`, `research_state/evaluation_summary_trackb_TB1_20261110T173838Z.md`, `research_state/evaluation_summary_FCLR-011.md`
- `scripts/fclr011_recompute_audit.py`, `scripts/run_funding_ablations.py`, `scripts/run_gate4_v4_leakage_audit.py`
- `scripts/check_tracka_scope_registry_drift.py`, `research_state/tracka_script_scope_registry.json`
- `tests/test_active_campaign_gate.py`, `tests/test_tracka_hardening_117.py`, `tests/test_tracka_hardening_118.py`

**Next session:** execute A→B→C→E in order (heavy default). Stop only when the trigger is checked once, every Phase B/C artifact is written, the full suite/guards are green, and this handoff reflects ground truth with external blockers documented.