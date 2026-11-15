# NEXT SESSION INITIAL TASK MESSAGE — 2026-11-15T08:43:11Z
# SOLE DURABLE HANDOFF POINTER — DO NOT RE-EDIT HANDOFF PROSE BEFORE PRODUCING DELIVERABLES

## REPOSITORY CONTEXT
**Project:** Funding-conditioned-volatility-and-liquidation-risk (quantitative finance research on funding rates, volatility, and liquidation risk in crypto perpetuals)
**Status:** `scripts/next_campaign_status.py` → "no feasible 3-block design in ANY domain" (honest; forecast frontier exhausted, Shek sensitivity grid remains)
**Authoritative handoff:** `AGENT_HANDOFF.md` (sole active). `NEXT_SESSION_HANDOFF.md` = tombstone. `AGENT_HANDOFF_20261115T073240Z.md` = RETIRED/SUPERSEDED.

## INITIAL TASK FOR NEXT AGENTIC WORK SESSION

**Execute `FCLR-SHEK-SCALE-SENSITIVITY-GRID-20261115T073000Z` immediately (DEFAULT heavy path, NOT trigger-gated).**
Frozen prereg `research_state/prereg_fclr_shek_scale_20261115T063600Z.json` specifies the sensitivity grid, but headline artifacts `evaluation_summary_FCLR-SHEK-SCALE-20261115T071135Z.{json,md}` emitted only headline/primary-family results. This is required cache-only robustness work on frozen Shek samples (not a re-probe). Do not stop for triggers; do not re-summarise baseline; produce deliverables.

**Baseline re-verified 2026-11-15T08:43Z:** gates green (19/19, fwd-vol PASS), scope drift 186/186 OK, targeted suite 58/58 OK, frontier rank-0 `FCLR-SHEK-SCALE-SENSITIVITY-GRID-20261115T073000Z` `READY_EXECUTE`, no `research_state/*SENS*` artifacts present. No sealed artifacts mutated.

### MANDATORY START BLOCK (copy-paste, do not re-derive)
```bash
git status --short && git log -1 --oneline
python3 scripts/fclr_campaign_gate.py               # 19/19
python3 scripts/fclr_fwd_vol_2025_disjoint_cross_gate.py  # PASS
python3 scripts/check_tracka_scope_registry_drift.py      # 186/186
python3 -m unittest tests.test_fclr_shek_scale tests.test_active_campaign_gate tests.test_next_campaign_status tests.test_funding_correction_replication tests.test_tracka_hardening_117 -v
python3 scripts/next_campaign_status.py             # "no feasible 3-block design in ANY domain"
```

### MANDATORY START BLOCK (copy-paste, do not re-derive)
```bash
git status --short && git log -1 --oneline
python3 scripts/fclr_campaign_gate.py               # 19/19
python3 scripts/fclr_fwd_vol_2025_disjoint_cross_gate.py  # PASS
python3 scripts/check_tracka_scope_registry_drift.py      # 185/185
python3 -m unittest tests.test_fclr_shek_scale tests.test_active_campaign_gate tests.test_next_campaign_status tests.test_funding_correction_replication tests.test_tracka_hardening_117 -v
python3 scripts/next_campaign_status.py             # must print "no feasible 3-block design in ANY domain"
```
If green, proceed immediately to heavy execution — do not stop to re-summarise.

### HEAVY EXECUTION REQUIREMENTS (do in order, no shortcuts)
1. **Re-verify baseline** (commands above); record only if materially changed.
2. **No new prereg:** use frozen `prereg_fclr_shek_scale_20261115T063600Z` and headline results `evaluation_summary_FCLR-SHEK-SCALE-20261115T071135Z`. Do not tune thresholds, do not change headline, do not peek/select by outcomes.
3. **Compute full frozen sensitivity grid for BOTH arms** (Arm A Binance independent, Arm B ironflow cross-coin secondary never-promotable):
   - Percentiles: `[1,99]`, `[5,95]`, `[10,90]`
   - Censor max follow hours: `168`, `336`
   - RV split: `tercile`, `median`
   - Headline cell is `[5,95]/168h/tercile` — grid is reported ONLY, never used to select headline
   - 12 cells per arm = 24 total cells
4. **Emit timestamped artifacts** `research_state/evaluation_summary_FCLR-SHEK-SCALE-SENS-<UTC>.{json,md}` reporting each cell:
   - Event/regime counts per cell
   - KM/log-rank/CI/Holm or consistent contrast stats per cell
   - Verdict/materiality per cell
   - Consistency vs headline: Arm A `TAIL_SHAPE_EFFECT`, Arm B `REPLICATES_DIRECTION`
5. **Extend `scripts/fclr_shek_scale.py` or add a clearly-scoped companion script** registered in BOTH scope registries:
   - `research_state/tracka_script_scope_registry.json`
   - `tests/test_tracka_hardening_117.py` `SCRIPT_REGISTRY`
   - Keep drift check green (`scripts/check_tracka_scope_registry_drift.py` → 186/186 currently; must remain green)
6. **Add/extend deterministic, fixture-based, tmp-isolated, no-network tests** covering grid-cell computation and verdict-consistency logic (extend `tests/test_fclr_shek_scale.py` or add registered companion test). Keep `H2_shek_replication` `EXPLORATORY_ONLY`, `promotable=false`, never terminal-promote.
7. **Advance frontier:** move `FCLR-SHEK-SCALE-SENSITIVITY-GRID-20261115T073000Z` to `COMPLETED_VALIDATED` with evidence and install the next heavy cell at rank 0. If no cache-heavy estimand remains, install a truthful trigger-only sentinel (only after grid actually completed).
8. **Full verification before commit:**
   ```bash
   python3 -m unittest tests.test_fclr_shek_scale tests.test_active_campaign_gate tests.test_next_campaign_status tests.test_funding_correction_replication tests.test_tracka_hardening_117 -v
   python3 scripts/fclr_campaign_gate.py               # 19/19
   python3 scripts/fclr_fwd_vol_2025_disjoint_cross_gate.py  # PASS
   python3 scripts/check_tracka_scope_registry_drift.py      # OK
   python3 scripts/next_campaign_status.py             # "no feasible 3-block design in ANY domain"
   ```
   Commit only meaningful work (no workflow/status-only edits).

### HARD CONSTRAINTS (violation = regression)
- Never reopen sealed/terminal families (H1 terminal absent valid trigger/new source; external liquidation hunt TERMINAL_NO_GO; vol/liq forecast 3-block frontier exhausted)
- Never mutate sealed artifacts
- Never edit `.github/workflows/*`
- Never use paid/credentialed/manual data
- Never relabel as forecast skill / boundary-breach / observed-liquidation prediction
- "No trigger → stop cleanly" is **NOT** completion
- Do not re-edit this file's prose before producing the grid artifacts

### BASELINE VERIFIED (2026-11-15T07:37:00Z, retained)
- Campaign gate 19/19 PASS; fwd-vol gate PASS; scope drift 185/185 OK; `next_campaign_status.py` honest
- Headline artifacts: `evaluation_summary_FCLR-SHEK-SCALE-20261115T071135Z.{json,md}` (prereg frozen 2026-11-15T06:36:00Z, EXPLORATORY_ONLY/promotable=false)
- Arm A (Binance 5 symbols, 847 events): **TAIL_SHAPE_EFFECT** — pooled high KM 8.00000028h vs low 8.0h, median diff 2.78e-07h < 4.0h threshold (material=false); log-rank χ²=18.899 p=1.378e-05 Holm 1.103e-04; CI [-2.78e-07,1.94e-06]
- Arm B (ironflow 160 coins, 39021 events, never-promotable): **REPLICATES_DIRECTION** — pooled high KM 1.999995h vs low 1.000025h, material diff 0.99997h; log-rank χ²=384.365 p=0 Holm 0
- Unfinished heavy work: frozen sensitivity grid not emitted → rank-0 `FCLR-SHEK-SCALE-SENSITIVITY-GRID-20261115T073000Z` (READY_EXECUTE)

### BOTTLENECKS REMOVED (do not recreate)
1. **Phantom extended Hyperliquid frontier** (2026-05-01..2026-10-31 falsely reported FEASIBLE) — fixed by adding FCLR-011 + forward-walk windows to `BULK_TESTED_WINDOWS` in `next_campaign_status.py`; guarded by `test_extended_frontier_excludes_fclr011_tested_windows` + `test_bulk_tested_windows_cover_fclr011`
2. **Shek scaled Arm A funding silently unloaded** (nested cache layout) — fixed in `funding_correction_replication.py` fallback; guarded by `test_nested_cache_funding_loads_for_scaled_sample` + `test_scaled_month_range_nonzero_events`
3. **Frontier rank-0 invalid status** (prior `ACTIVE_WAITING` → fixed to `READY_EXECUTE`)
4. **"Cached heavy-work frontier exhausted / stop cleanly if no trigger"** — removed as completion path; Shek correction-hazard is a distinct unexhausted estimand
5. **Handoff churn** (4+ sessions produced zero deliverables, only edited handoff prose) — fixed by INITIAL TASK MESSAGE guard
6. **Scope-registry drift** (`fclr_shek_scale.py` unregistered → 184/185 FAIL) — fixed by registering in both registries
7. **Headline run omitted frozen sensitivity grid** — installed `FCLR-SHEK-SCALE-SENSITIVITY-GRID-20261115T073000Z` at rank 0
8. **Conflicting second handoff** (`AGENT_HANDOFF_20261115T073240Z.md` proposing Track C) — RETIRED/SUPERSEDED; never start Track C while grid is rank-0

### OPTIONAL PREEMPT TRIGGERS (do NOT block default heavy campaign)
- `GATE4_BRANCH_1`: valid `fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` with `status=RESOLVED_VERIFIED`, `fabricated=false`, required human/legal attestation
- `NEW_OBSERVED_LIQUIDATION_SOURCE`: materially new source family (not re-probe of exhausted families in `liquidation_source_campaign.md`, `track_a_deadend_map.md`) passing §16 audit before prereg/outcomes
- Absence of trigger = continue default heavy campaign

### FIRST ACTION FOR NEXT SESSION (timestamped, mandatory)
**`2026-11-15T08:36:03Z` — Run the START block above, then execute the frozen sensitivity grid (24 cells, both arms) and emit timestamped SENS evaluation artifacts.**

---
**This is the sole durable handoff. Do not write status-only notes. Do not re-probe exhausted families. Do not reopen sealed verdicts. Heavy work is the default path.**