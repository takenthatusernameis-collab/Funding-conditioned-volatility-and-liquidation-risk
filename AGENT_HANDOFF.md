# AGENT HANDOFF — 2026-11-13T22:32:30Z (authoritative, single durable handoff)

## START HERE — INITIAL TASK FOR NEXT SESSION (2026-11-13T22:32:30Z) — HEAVY WORK REQUIRED
- **Prior forward cell COMPLETE (this session):** `FCLR-FORWARD-LIQ-2026Q1Q2` Phases 1-4 executed offline on the on-disk ironflow Hyperliquid forward bulk cache. Prereg `research_state/prereg_tracka_liq_xsec_forward_2026q1q2_20261113T222859Z.json` frozen 2026-11-13T22:28:59Z before outcomes; builder `scripts/fclr_build_tracka_liq_xsec_forward.py` emitted `research_state/tracka_liq_xsec_forward_panel_2026-11-13T22:31:55Z.parquet` (107 coins, 6741 rows, sha256 `990598685617b088...`), build report, and `research_state/evaluation_summary_TRACKA-LIQ-XSEC-FORWARD-2026-11-13T22:31:55Z.{json,md}` **verdict `EXPLORATORY_NULL`** (mean IC -0.02703, pooled IC -0.02512, pooled p 0.031, spread sign 1/3; EXPLORATORY_ONLY, never promotable).
- **Current machine-checked state:** `python3 scripts/fclr_campaign_gate.py --arm all` → **16/16 PASS** (A0-A6, B1-B4, F0-F4). `python3 -m unittest -q tests.test_fclr_campaign_gate tests.test_active_campaign_gate` → **22/22 OK**.
- **Execute now (no planning-only, no status-only):** run the next materially different, admissible **unopened** heavy task. (P1) If any remaining untouched admissible observed-liquidation or volatility window exists on cached/on-disk data not previously tested, freeze a prereg before outcomes and execute build/eval to a recognized verdict with gate + deterministic tests. (P2) If a new unauthenticated observed-liquidation source passes minima (≥5 instruments, ≥1 complete month or ≥3 non-overlapping 30-day blocks, provenance/license, observed-only, venue-consistent), run §5 admissibility audit → freeze prereg → build/eval → verdict → atomic state updates under a new experiment ID. (P3) If and only if no admissible unopened route exists, emit a bounded structural NO_GO with exact failing minima per candidate (source/window + which minimum fails) and update frontier/handoff — still heavy, evidence-backed work, not a status memo.
- **Do not:** re-run terminal/consumed Binance or HL cells, probe sealed/Gate-4 paths, read May 2026, fabricate artifacts/thresholds/verdicts, weaken Arm F/gates, or stop after planning. Commit code/manifests/provenance/reports only (never raw parquet/caches).

## 1) Repo-priority context (name-driven)
Core claim: extreme funding/volatility/price-dislocation features improve **out-of-sample** forecasts of future volatility or
liquidation stress vs volatility-only baselines, on admissible data with frozen prereg + leakage-safe evaluation. All six cached
Binance funding-vol / FWD-VOL cells are terminal (NOT_REPLICATED / FRAGILE) and gated PASS — do not re-run them. The highest-value
unfinished frontier is the untouched ironflow Hyperliquid forward observed-liquidation window (below).

## 2) Verified state (2026-11-13T21:40:00Z)
- `python3 scripts/fclr_campaign_gate.py --arm all` → **12/16 PASS**, `blocking: F1, F3_panel, F3_report, F4`. A0-A6 and B1-B4 all pass
  (A0 bulk cache verified incl. pyarrow 26.0.1). Arm F is red **by design**: the forward cell is genuinely unbuilt. This is the correct
  pre-work state, not a regression.
- `python3 -m unittest -q tests.test_fclr_campaign_gate tests.test_active_campaign_gate` → **22/22 OK** (0.368s).
- `python3 scripts/next_campaign_status.py --json` → `hyperliquid_bulk_frontier.any_forward_feasible: true`;
  run `2026-01-18..2026-04-30` = 103 days ≥ `MIN_FORWARD_DESIGN_DAYS` (60 train + 7 embargo + 3×10 test = 97).
- Forward region remains untouched/reserved. Verified 2026-11-13T21:40:00Z from the on-disk bulk cache:
  **377,110 observed native-perp liquidation events** across **192 native perps** in `2026-01-18..2026-04-30`, long/short sides,
  **0 null notional**; **113 coins** meet ≥20 liquidation-days and ≥100 events before the coverage filter. Candle/funding bulk
  coverage is present for the window. **Correction:** the earlier `537,179` figure was all markets (native + non-native) and must
  not be quoted as native events; the native count is 377,110.
- Labels end `2026-04-30T23:48:51Z`; the last scoreable decision day is `2026-04-29` (target `[2026-04-30, 2026-05-01)`).
- Both label caches are byte-identical for 2026-01..2026-04: `ironflow_bulk/liquidations` and `ironflow_events` carry the same rows
  and schema. The forward clone must use the **bulk** path (see Phase 2).
- No raw parquet/caches are tracked; the caches are local-only.

## 3) Bottlenecks (removed / to close)
- **REMOVED — external data:** the forward cell needs no download/credentials/network; the 2025-05..2026-04 ironflow bulk cache is on disk
  (candles_1h/funding/open_interest/liquidations + sha256 sidecars, CC-BY-4.0).
- **REMOVED — avoidable-work loophole:** the previous gate was 11/11 green on the two consumed cells alone, so a session could report
  "done" without ever touching the only unopened window. Arm F (F0-F4) now makes `--arm all` fail closed until the forward cell is
  built, so the green gate *means* the heavy work is finished. **Do not weaken Arm F, edit the gate to pass, or fabricate forward
  artifacts — build the cell.**
- **REMOVED — false regression signal in tests:** `tests/test_fclr_campaign_gate.py::test_empty_state_is_blocked` printed a live
  `0/9 blocking` banner into the repo's test output, which is indistinguishable from a real campaign regression and had already
  misled this session. It now redirects stdout and asserts on the captured text.
- **REMOVED — builder drift:** the old builder hard-codes the consumed window. Phase 2's exact clone deltas are specified above so the next
  session cannot stall on "how do I extend it"; do not rewrite the old cell or re-probe its terminal verdict.
- **Hygiene:** root `FOCUS_CAMPAIGN.md` / `HANDOFF_NEXT_SESSION.md` / `NEXT_SESSION_TASK.md` are redirects only.

## 4) Invariants (never violate)
1. Fail-closed; blocked paths must not read outcomes/parquet or write canonical outputs except the explicit durable evidence artifacts above.
2. **Preregistration before outcomes**; the freeze file must predate the panel build.
3. Observed vs modeled labels never conflated; no venue mixing; no forward fill / synthetic data; no reading May 2026 or sealed windows.
4. No re-probing terminal cells; no status-only sessions; no threshold shopping; no `.github/workflows` edits.
5. Do not commit raw parquet or caches.

## 5) Immediate next action for the next session
Start at **Phase 1**: write `research_state/prereg_tracka_liq_xsec_forward_2026q1q2_<UTC>.{json,md}` with the exact splits, universe,
features/score, estimand, inference, and flags above — **before any outcome read** — then execute Phases 2-4 in the same session.
This is executable offline on data already on disk; do not emit a NO_GO/status-only memo while it is executable.

## 6) Session log
### 2026-11-13T20:17:06Z
- **Diagnosis:** prior handoff/frontier forced a permanent external-data NO_GO loop despite an untouched, admissible on-disk ironflow
  Hyperliquid forward window (`2026-01-18..2026-04-30`, 103 days). Bottleneck removed by re-pointing the campaign at that window.
- **Verified:** `fclr_next_campaign_gate.py --json` ok:true; `fclr_campaign_gate.py --arm all` 6/11 (5 real failures); forward region
  untouched. **Next heavy task:** Phase 0 → Phase 1 → Phase 2 → Phase 3 → Phase 4.

### 2026-11-13T20:29:00Z
- **Change:** Phase 0 closed — fixed `scripts/fclr_build_tracka_vol_fullhist.py` and `scripts/fclr_build_tracka_liq_xsec.py` to emit
  `panel_sha256`, `contrasts.C2_vs_B1`, 12 `primary_family_cells`, and a recognised `verdict`; regenerated artifacts. Arm B regen at
  `2026-11-13T20:24:18Z` reproduces EXPLORATORY_NULL exactly; Arm A NOT_MET unchanged. No results/thresholds/verdicts fabricated.
- **Verified:** gate 11/11 PASS (was 6/11); 33 deterministic tests passed. **Next heavy task:** Phase 1 freeze forward prereg.

### 2026-11-13T20:32:32Z
- **State confirmation:** Phase 0 CLOSED; no external data required. Consumed region only `2025-05-25..2026-01-17`; forward region
  `2026-01-18..2026-04-30` reserved/untouched. **Next heavy task:** Phase 1 → Phase 4.

### 2026-11-13T21:26:30Z (handoff hardening)
- **Verified:** gate 11/11 PASS; 19 deterministic tests OK; `next_campaign_status.py` forward feasible. Made this file the single
  timestamped initial task and synced `experiment_frontier.json` rank 0 to actual state so future sessions cannot drift into status loops.

### 2026-11-13T21:30:41Z (verification + accuracy correction)
- **Verified (this session):** gate **11/11 PASS**; tests **19/19 OK**; forward run feasible (`feasible_forward: true`, 103 days).
  Recomputed the forward cache from parquet: **377,110 native-perp liquidation events** (192 native perps, 0 null notional; 113 coins
  meet ≥20 days/≥100 events) — the earlier `537,179` was all markets (native + non-native) and is corrected. Labels end
  `2026-04-30T23:48:51Z`, so the last scoreable decision day is `2026-04-29`.
- **Split inconsistency resolved:** the prior proposed `30 + 16 + 27` contiguous blocks silently dropped Arm B's 7-day embargo and did not
  fit 103 days. Frozen ex ante: burn-in 16d (`01-18..02-02`) + 3×7d embargoes + 30/16/20-day blocks = **16+7+30+7+16+7+20 = 103 days exactly**;
  block ends are target horizons, so scored decision days are 29 + 15 + 19 = 63, ending `2026-04-29`.
- **Bottleneck:** none blocking. Phase 0 closed; data on disk; builder clone deltas specified.
- **Next heavy task (unfinished):** **FCLR-FORWARD-LIQ-2026Q1Q2 Phase 1→4** — freeze the forward prereg before outcomes, clone/parameterize
  the Arm B builder to `2026-01-18..2026-04-30` (last scored day `2026-04-29`), evaluate with the frozen contrasts, pass gate 16/16 +
  deterministic tests, commit code/manifests/provenance/reports (no raw parquet), and set the next actionable heavy task in
  `experiment_frontier.json`.

### 2026-11-13T21:40:00Z (bottleneck removal: gate now enforces the forward cell)
- **Diagnosis:** the "definition of done" was 11/11 green on the two already-consumed cells (Arm A FULLHIST, Arm B XSEC). The only
  remaining unopened window (`2026-01-18..2026-04-30`) had **no gate coverage**, so a session could truthfully report "gate 11/11 PASS"
  while doing zero heavy work. That is the avoidable-work loophole this handoff exists to close.
- **Change 1 — Arm F added to `scripts/fclr_campaign_gate.py`:** new checks `F0` (four forward bulk months present, from filename stems
  only), `F1` (frozen forward prereg `prereg_tracka_liq_xsec_forward_*.json`), `F3` (forward panel + report with matching `panel_sha256`),
  `F4` (forward eval JSON with a recognised verdict). `--arm all` is now 16 checks. Arm F is metadata-only: it never opens the reserved
  parquet bodies and never computes an outcome, so it cannot leak the forward window. No existing check was weakened.
- **Change 2 — test hygiene:** `tests/test_fclr_campaign_gate.py::test_empty_state_is_blocked` now redirects stdout and asserts on the
  captured text, so the real campaign's output is no longer polluted with a fake `0/9 blocking` banner. Added three forward-arm tests
  (independence from A/B, complete-passes, hash-mismatch-fails) + a forward-label fixture helper. Suite is now 17 tests.
- **Verified (this session):** `fclr_campaign_gate.py --arm all` → **12/16 PASS**, `blocking: F1, F3_panel, F3_report, F4`
  (the honest pre-work state; A0-A6/B1-B4 all pass). `unittest tests.test_fclr_campaign_gate tests.test_active_campaign_gate` → **22/22 OK**.
  Independently recomputed the forward cache: 377,110 native events, 192 native perps, 113 coins ≥20d/≥100ev, 0 null notional,
  labels end `2026-04-30T23:48:51Z`; confirmed `ironflow_bulk/liquidations` and `ironflow_events` are byte-identical for 2026-01..2026-04.
- **Bottleneck:** none blocking the forward build. The gate now *requires* it; data on disk; exact clone deltas in Phase 2.
- **Next heavy task (unfinished):** **FCLR-FORWARD-LIQ-2026Q1Q2 Phase 1→4**, now enforced by Arm F. Green 16/16 is only reachable by
  building the forward cell.

### 2026-11-13T22:32:30Z (FCLR-FORWARD-LIQ-2026Q1Q2 Phases 1-4 executed)
- **Commands:** `python3 scripts/fclr_campaign_gate.py --arm all` (pre: 12/16, F1/F3/F4); `python3 -m unittest -q tests.test_fclr_campaign_gate tests.test_active_campaign_gate` (22/22 OK); `python3 scripts/fclr_build_tracka_liq_xsec_forward.py`.
- **Phase 1 (freeze before outcomes):** wrote `research_state/prereg_tracka_liq_xsec_forward_2026q1q2_20261113T222859Z.{json,md}` (frozen 2026-11-13T22:28:59Z, `frozen_before_outcomes/outcome_data_inspected_before_freeze=false/promotable=false`, exact burn-in/embargo/block splits, universe/estimand/inference per spec).
- **Phase 2 (build+eval):** added `scripts/fclr_build_tracka_liq_xsec_forward.py` (cloned from Arm B builder; EVENTS=`ironflow_bulk/liquidations`, BULK load 2025-12..2026-04, labels 2026-01..2026-04, blocks 02-10..03-11/03-19..04-03/04-11..04-30, target-horizon semantics). Emitted `research_state/tracka_liq_xsec_forward_panel_2026-11-13T22:31:55Z.parquet` (107 coins, 6741 rows), `research_state/tracka_liq_xsec_forward_panel_build_report_2026-11-13T22:31:55Z.json` (panel_sha256 `990598685617b088...`), `research_state/evaluation_summary_TRACKA-LIQ-XSEC-FORWARD-2026-11-13T22:31:55Z.{json,md}`.
- **Result:** verdict **EXPLORATORY_NULL** (EXPLORATORY_ONLY). Mean IC -0.02703 (|.|<0.05), pooled IC -0.02512, pooled p 0.031 (permutation 1000, seed 20261112), per-block ICs block0 -0.01884 / block1 -0.01200 / block2 -0.05025; spread sign consistency 1/3 (block1 positive only). 107/113 coverage-eligible coins.
- **Phase 3:** `fclr_campaign_gate.py --arm all` → **16/16 PASS**; deterministic tests **22/22 OK**. Forward eval JSON parses with recognised verdict, `panel_sha256`, per-block ICs.
- **Phase 4:** updated `research_state/experiment_frontier.json` (forward cell COMPLETED, next heavy task set to materially different admissible unopened route or bounded structural NO_GO). No raw parquet/caches committed.
- **Next heavy task (unfinished):** execute next materially different admissible unopened design on cached/on-disk data with prereg-before-outcomes (or, if none, bounded structural NO_GO with exact failing minima per candidate). Do not reopen terminal cells or weaken gates.
