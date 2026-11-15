# AGENT HANDOFF — 2026-11-15T22:39:24Z

**Project:** Funding-conditioned Volatility and Liquidation Risk (FCLR)
**Repository:** `Funding-conditioned-volatility-and-liquidation-risk`
**Sole durable handoff:** this file (`AGENT_HANDOFF.md`). `NEXT_SESSION_HANDOFF.md` = tombstone (no authority). `AGENT_HANDOFF_20261115T073240Z.md` = RETIRED/SUPERSEDED — ignore.

## STATE (verified 2026-11-15T22:39:24Z)
- `research_state/experiment_frontier.json` rank 0: `FCLR-BOUNDED-TRIGGER-ONLY-20261115T220000Z` | status `TRIGGER_ONLY` | `program_status=BOUNDED_TRIGGER_ONLY` | `next_action_heavy=null` | `all_terminal=true`.
- Cached-data liquidation estimands concluded NOT_MET/SUPERSEDED (do not re-run): `FCLR-LIQ-XSEC-QLIKE-20261115T214949Z`, `FCLR-LIQ-XSEC-ORDERING-20261115T203507Z`, `FCLR-LIQ-COMBINED-20261115T185844Z`.
- QLIKE artifacts present: `research_state/prereg_fclr_liq_combined_xsec_qlike_20261115T214903Z.{json,md}`, `research_state/evaluation_summary_FCLR-LIQ-XSEC-QLIKE-20261115T214949Z.{json,md}`.
- Hypothesis registry terminal statuses confirmed: `H_fclr_liq_xsec_qlike_forecast`, `H_fclr_liq_xsec_ordering_forecast`, `H_fclr_liq_combined_panel_forecast` = `NOT_MET` with matching last evaluations.
- Triggers all OPEN (external): `GATE4_BRANCH_1` (human/legal attestation), `NEW_OBSERVED_LIQUIDATION_SOURCE` (ironflow data_through 2026-10; 2026-11+ absent), `HL_LABEL_EXTENSION`, `EXPANSION_ROBUSTNESS_REDO` (do not re-run sealed designs; only new prereg design meeting conditions). See `research_state/resume_trigger_registry.json`, `research_state/ironflow_monitor_state.json`.
- Gates/health (this session): scope drift PASS (`python3 scripts/check_tracka_scope_registry_drift.py` → `scripts=195 registry=195`); `python3 -m unittest tests.test_tracka_hardening_117 tests.test_tracka_hardening_118` OK (33); `python3 -m unittest tests.test_active_campaign_gate` OK (5). Full-suite run was started but not completed within this session’s check window — must be re-run and kept green.
- `H2_shek_replication` remains `EXPLORATORY_ONLY` (`promotable=false`) — do not re-run/promote.

## BOTTLENECKS REMOVED THIS SESSION
1. **Handoff corrected & made sole/authoritative:** replaced stale/inconsistent guidance that pointed at a non-rank-0 “QLIKE pending” path with a frontier-aligned, timestamped task message reflecting the actual `TRIGGER_ONLY` sentinel and terminal conclusions.
2. **Validation spot-checks executed:** scope-registry drift, hardening 117/118, and active-campaign guard verified passing now; prevents silent regression before next work.
3. **No alternate handoffs:** `NEXT_SESSION_HANDOFF.md` remains tombstone; this file is the only durable instruction surface.

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION (heavy, default)
**Mission:** keep the project in a heavy-working, trigger-ready state. “No trigger fired” is not an excuse to stop early; complete the bounded hardening/reproducibility campaign and leave a clean, evidenced state.

### Phase A — Trigger check (run once at session start, no polling)
1. Read `research_state/resume_trigger_registry.json` and `research_state/ironflow_monitor_state.json`; confirm all triggers remain OPEN/unchanged and `data_through=2026-10` with 2026-11+ absent. Do **not** re-probe or poll.
2. If any trigger is newly satisfied with required evidence artifacts, immediately pivot to **Phase D**.

### Phase B — Heavy hardening/reproducibility (mandatory while trigger-only)
3. Run full regression gate and make it **0 failures**: `python3 -m unittest discover -q` (baseline stated in frontier: 1341 tests, 0 failures). If red, diagnose/fix root cause without touching sealed artifacts or `.github/workflows/*`; record what changed.
4. Re-confirm invariants: `python3 scripts/check_tracka_scope_registry_drift.py` PASS; `python3 -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_117 tests.test_tracka_hardening_118` PASS.
5. Reconcile frontier/handoff consistency: ensure rank-0 remains the active `TRIGGER_ONLY` sentinel (do not delete it) and this handoff reflects ground truth. `research_state/FCLR_HEAVY_CAMPAIGN_NEXT.md` is referenced by frontier but **missing** — create a concise, durable campaign note there describing the bounded trigger-only hardening steps + trigger-gated advance rules (align with frontier phases) so future agents cannot skip heavy work.

### Phase C — Closeout
6. Update this handoff (timestamp, what was verified/fixed, exact commands/results, remaining external blockers). Commit checkpoint if changes were made. Stop cleanly only after A+B+C are green/evidenced.

### Phase D — Trigger-gated advance (only if a trigger fires with evidence)
7. Freeze a **new, materially different** pre-outcomes prereg before inspecting outcomes (`outcome_data_inspected_before_freeze=false`), run admissibility/audit per `RESEARCH_PROMPT.md`, execute eval+gates, register scripts in both registries, update `experiment_frontier.json`/`hypothesis_registry.json`, and record an honest verdict. Install as rank-0 active heavy cell. Never re-run concluded estimands, never re-probe TERMINAL_NO_GO families, never re-score sealed results.

## HARD CONSTRAINTS (non-negotiable)
- ❌ Never reopen sealed/terminal families or mutate sealed artifacts; never edit `.github/workflows/*`.
- ❌ No outcome-peeking/threshold tuning before prereg; no paid/credentialed/manual data for outcomes.
- ❌ No polling, no re-running concluded estimands, no re-probing TERMINAL_NO_GO families.
- ❌ Do not fabricate new data/sources or claim triggers satisfied without required artifacts/fields.
- ✅ `H2_shek_replication` remains `EXPLORATORY_ONLY` (`promotable=false`).
- ✅ Exactly one durable handoff: `AGENT_HANDOFF.md`.

## KEY REFERENCES
- `research_state/experiment_frontier.json`, `research_state/resume_trigger_registry.json`, `research_state/ironflow_monitor_state.json`
- `research_state/evaluation_summary_FCLR-LIQ-XSEC-QLIKE-20261115T214949Z.*`, `research_state/evaluation_summary_FCLR-LIQ-XSEC-ORDERING-20261115T203507Z.*`, `research_state/evaluation_summary_FCLR-LIQ-COMBINED-20261115T185844Z.*`
- `scripts/check_tracka_scope_registry_drift.py`, `research_state/tracka_script_scope_registry.json`
- `tests/test_active_campaign_gate.py`, `tests/test_tracka_hardening_117.py`, `tests/test_tracka_hardening_118.py`

**Next session:** execute A→B→C in order (heavy default). Stop only when trigger checked once, full suite/guards green, handoff+campaign note consistent, and external blockers documented.
