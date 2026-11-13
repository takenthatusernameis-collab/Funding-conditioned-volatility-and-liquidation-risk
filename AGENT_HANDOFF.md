# AGENT HANDOFF — 2026-11-13T21:30:41Z (authoritative, single durable handoff)

**INITIAL TASK FOR NEXT SESSION — execute this now. Heavy work is mandatory; do not stop at planning, status, or a NO_GO memo.**
Run campaign **FCLR-FORWARD-LIQ-2026Q1Q2 Phase 1→4** to a terminal, evidence-backed verdict on the already-on-disk,
admissible ironflow Hyperliquid forward bulk cache (offline; no network, credentials, or external trigger).

Verified at freeze of this handoff (2026-11-13T21:30:41Z): `python3 scripts/fclr_campaign_gate.py --arm all` → **11/11 PASS**;
`python3 -m unittest -q tests.test_fclr_campaign_gate tests.test_active_campaign_gate tests.test_campaign_resume` → **19/19 OK**;
`next_campaign_status.py --json` → forward run `2026-01-18..2026-04-30` feasible (`feasible_forward: true`, 103 days).

### Phase 1 — Freeze the forward prereg BEFORE any outcome read (hard gate)
Write `research_state/prereg_tracka_liq_xsec_forward_2026q1q2_<UTC>.{json,md}`, modeled on
`prereg_tracka_liq_xsec_20261112T201536Z.{json,md}`. Required contents:
- `experiment_id`: `TRACKA-LIQ-XSEC-FORWARD-<UTC>`; `campaign`: `FCLR-FORWARD-LIQ-2026Q1Q2`; `arm`: `B`; `track`: `A_liquidation`.
- `frozen_before_outcomes: true`, `pre_registered_before_outcomes: true`, `outcome_data_inspected_before_freeze: false`, `promotable: false`.
- **Splits (exact; no re-derivation):** burn-in `2026-01-18T00:00:00Z..2026-02-02T23:59:59Z` (16 days; warm-up + eligibility context,
  never scored); 7-day embargo `2026-02-03..2026-02-09`; test block 0 `2026-02-10T00:00:00Z..2026-03-11T23:00:00Z`;
  7-day embargo `2026-03-12..2026-03-18`; block 1 `2026-03-19T00:00:00Z..2026-04-03T23:00:00Z`; 7-day embargo `2026-04-04..2026-04-10`;
  block 2 `2026-04-11T00:00:00Z..2026-04-30T23:00:00Z`. Arithmetic: 16 + 7 + 30 + 7 + 16 + 7 + 20 = **103 days exactly**, so the
  Arm B 7-day embargo rule is preserved inside the 103-day span. **Block end is the target horizon, not the last decision day:**
  the builder scores `start..end−1 day`, so scored decision days are block 0 `02-10..03-10` (29), block 1 `03-19..04-02` (15),
  block 2 `04-11..04-29` (19) = **63 scored days**; last decision day `2026-04-29`, whose target is `[2026-04-30, 2026-05-01)` —
  fully present. `d=2026-04-30` would read May and is forbidden. Label files end `2026-04-30T23:48:51Z`; never read May.
- **Universe (coverage-only, frozen ex ante):** native perps (`market` ends `-PERP`, no `:`), ≥20 observed liquidation-days and
  ≥100 observed liquidation events over `2026-01-18..2026-04-30`, complete hourly candle+funding coverage over the test window.
  Verified counts before the coverage filter: **113 coins** meet the day/event rule out of **192 native perps**; floor 5. The final
  universe is 113 or fewer (coverage filter only), not "~150-190".
- **Features/score/estimand/inference — identical to Arm B:** `rv24h` (trailing 24h realized variance from hourly closes ending at bucket
  start), `funding_rate`, `abs_funding`, `premium` (as-of latest at or before bucket start); score = within-bucket z(funding_rate) +
  z(abs_funding); primary Spearman rank IC of score vs next-24h observed liquidation event count per 30-day block on the pooled
  cross-section; secondary top-k minus bottom-k next-24h notional spread (k = 10% of universe, floor 5); within-bucket permutation
  1000 reps, seed 20261112; materiality `|mean IC| ≥ 0.05` and spread sign consistent ≥2/3 blocks.
- Data provenance: `research_state/data_cache/ironflow_bulk/{liquidations,candles_1h,funding}/<YYYY-MM>.parquet` for 2026-01..2026-04,
  sha256 sidecars, CC-BY-4.0, observed labels only, no modeled/proxy/synthetic labels, no venue mixing.
- **Confirm freeze before build:** the prereg file mtime must precede any panel build/eval artifact.

### Phase 2 — Build + evaluate (only after freeze)
1. Clone `scripts/fclr_build_tracka_liq_xsec.py` → `scripts/fclr_build_tracka_liq_xsec_forward.py` and change only the frozen design:
   - `PREREG_PATH` → the new prereg JSON; `COVERAGE_START="2026-01-18 00:00:00"`, `COVERAGE_END="2026-04-30 23:00:00"`
     (COVERAGE_END is the target horizon, so it must include the 2026-04-30 target day but not May), `TEST_START="2026-02-10 00:00:00"`,
     `TEST_END="2026-04-30 23:00:00"`;
   - `BLOCKS` → the three blocks above; `experiment_id` → forward ID; output stems → `tracka_liq_xsec_forward_*` /
     `evaluation_summary_TRACKA-LIQ-XSEC-FORWARD-<UTC>.*`;
   - labels: load `ironflow_bulk/liquidations/{2026-01..2026-04}.parquet` (not `ironflow_events/`), filter `day >= 2026-01-18`
     and `day <= 2026-04-30` (the 2026-04-30 target day is required; May is still excluded); candles/funding: load `ironflow_bulk/{candles_1h,funding}/{2026-01..2026-04}.parquet`, keeping
     2026-01-17 hours for the 24h warm-up only;
   - emit `tracka_liq_xsec_forward_panel_<UTC>.parquet`, `..._panel_build_report_<UTC>.json` (must include top-level
     `panel_sha256` = sha256 of the panel parquet), and `evaluation_summary_TRACKA-LIQ-XSEC-FORWARD-<UTC>.{md,json}` with a
     recognised `verdict` (`EXPLORATORY_SIGNAL` / `EXPLORATORY_NULL` / `INADMISSIBLE`) and full diagnostics (per-block IC,
     permutation null 5th/95th percentiles, p-values, event counts, coins, coverage). No threshold shopping; no sealed/reserved reads.

### Phase 3 — Verify (deterministic, offline)
1. `python3 scripts/fclr_campaign_gate.py --arm all` → **11/11**.
2. `python3 -m unittest -q tests.test_fclr_campaign_gate tests.test_active_campaign_gate tests.test_campaign_resume` (plus any builder test added).
3. `python3 scripts/fclr_next_campaign_gate.py --json` must remain `ok: true`.
4. Verify the forward eval JSON parses and has a recognised `verdict`, `panel_sha256`, and per-block ICs.

### Phase 4 — Closeout
1. Update `research_state/experiment_frontier.json` rank 0: record the forward cell, set `last_checked`, and replace
   `next_action_heavy`/`next_unfinished_task` with the actual next unfinished heavy task (next unopened forward window or residual).
2. Append a timestamped §7e session log entry here with exact commands, results, new artifact paths, and the next heavy task.
3. Commit only code/manifests/provenance/reports (**never** raw parquet/caches).

**Project:** Funding-conditioned volatility and liquidation risk (FCLR).
**Repo root:** `/home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk`.
**Single durable handoff:** this file. `FOCUS_CAMPAIGN.md`, `HANDOFF_NEXT_SESSION.md`, `NEXT_SESSION_TASK.md` are inert redirects — never execute them.

## 1) Repo-priority context (name-driven)
Core claim: extreme funding/volatility/price-dislocation features improve **out-of-sample** forecasts of future volatility or
liquidation stress vs volatility-only baselines, on admissible data with frozen prereg + leakage-safe evaluation. All six cached
Binance funding-vol / FWD-VOL cells are terminal (NOT_REPLICATED / FRAGILE) and gated PASS — do not re-run them. The highest-value
unfinished frontier is the untouched ironflow Hyperliquid forward observed-liquidation window (below).

## 2) Verified state (2026-11-13T21:30:41Z)
- `python3 scripts/fclr_campaign_gate.py --arm all` → **11/11 PASS** (A0 bulk cache verified incl. pyarrow 26.0.1; A1/A3/A4/A5/A6/B1/B3/B4 all pass).
- `python3 -m unittest -q tests.test_fclr_campaign_gate tests.test_active_campaign_gate tests.test_campaign_resume` → **19/19 OK** (0.305s).
- `python3 scripts/next_campaign_status.py --json` → `hyperliquid_bulk_frontier.any_forward_feasible: true`;
  run `2026-01-18..2026-04-30` = 103 days ≥ `MIN_FORWARD_DESIGN_DAYS` (60 train + 7 embargo + 3×10 test = 97).
- Forward region remains untouched/reserved. Verified 2026-11-13T21:30:41Z from the on-disk bulk cache:
  **377,110 observed native-perp liquidation events** across **192 native perps** in `2026-01-18..2026-04-30`, long/short sides,
  **0 null notional**; **113 coins** meet ≥20 liquidation-days and ≥100 events before the coverage filter. Candle/funding bulk
  coverage is present for the window. **Correction:** the earlier `537,179` figure was all markets (native + non-native) and must
  not be quoted as native events; the native count is 377,110.
- Labels end `2026-04-30T23:48:51Z`; the last scoreable decision day is `2026-04-29` (target `[2026-04-30, 2026-05-01)`).
- Working tree is clean at the 21:26:30Z checkpoint; no raw parquet/caches are tracked.

## 3) Bottlenecks (removed / to close)
- **REMOVED — external data:** the forward cell needs no download/credentials/network; the 2025-05..2026-04 ironflow bulk cache is on disk
  (candles_1h/funding/open_interest/liquidations + sha256 sidecars, CC-BY-4.0).
- **REMOVED — gate:** Phase 0 closed at the producer; `fclr_campaign_gate.py --arm all` is 11/11 (no gate weakened, no verdict fabricated).
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
  the Arm B builder to `2026-01-18..2026-04-30` (last scored day `2026-04-29`), evaluate with the frozen contrasts, pass gate 11/11 +
  deterministic tests, commit code/manifests/provenance/reports (no raw parquet), and set the next actionable heavy task in
  `experiment_frontier.json`.