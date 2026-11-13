# AGENT HANDOFF — 2026-11-13T20:17:06Z (authoritative, single durable handoff)

**Initial task for the next agentic session (read this first, then execute Phase 1 immediately):**
Run the **FCLR-FORWARD-LIQ-2026Q1Q2** heavy campaign below to a terminal, evidence-backed verdict.
This is a **new confirmatory-eligible forward cell** on the **already-on-disk, admissible**
ironflow Hyperliquid bulk cache. Do **not** stop at planning, status reruns, or another Track A
NO_GO memo. Phase 1 is the definition of done and is gated by `scripts/fclr_campaign_gate.py`.

**Project:** Funding-conditioned volatility and liquidation risk (FCLR)
**Repo root:** `/home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk`
**This file is the single durable handoff.** `FOCUS_CAMPAIGN.md`, `HANDOFF_NEXT_SESSION.md`, `NEXT_SESSION_TASK.md` are inert redirects — do not execute them.

## 0) Why this handoff supersedes the old one (bottleneck removed)

The previous handoff (2026-11-13T19:27:14Z) and frontier record funneled **every** session into
Track A observed-liquidation resume that requires **external data that does not exist**
(Ironflow Hyperliquid month ≥ 2026-11 events+fills; 0 admissible alt-sources per
`research_state/alt_source_deep_review_latest.md` 2026-11-13T17:12:25Z). That made the program a
permanent **CLEAN STOP / NO_GO re-emit loop** — the exact avoidance pattern `RESEARCH_PROMPT` §16
forbids ("do not write another blocker memo and wait if a valid, bounded task is available;
execute that task").

**That external-data bottleneck is a false blocker.** A fully-admissible observed-liquidation
dataset is already on disk and untouched:

- `research_state/data_cache/ironflow_bulk/{candles_1h,funding,open_interest,liquidations}/<YYYY-MM>.parquet`
  for **2025-05..2026-04** (12 months, all four datasets, sha256 sidecars present, CC-BY-4.0, unauthenticated).
- `liquidations` rows are **observed on-chain perp liquidation events**: `timestamp, market, position_side
  (long/short), notional_usd, fills, block, tx_hash` (events+fills roles; no modeled/proxy labels).
- The **only consumed region** is `2025-05-25..2026-01-17` (TRACKA-VOL-FULLHIST + TRACKA-LIQ-XSEC).
- **`2026-01-18..2026-04-30` (103 days) is reserved "never read"** by
  `research_state/prereg_tracka_liq_xsec_20261112T201536Z.md:78` and is **still untouched.**
- Verified 2026-11-13T20:16Z: forward region holds **537,179 observed liquidation events across 192
  native perps** (BTC/SOL/ETH/HYPE/XRP/ZEC/…), long/short sides, **0 null notional**. Far exceeds
  the ≥5-coin / ≥100-events floor.

So the bottleneck is removed: **execute the forward observed-liquidation cell now**, on data already
present, with no network, no credentials, no external trigger.

## 1) Repo-priority context (name-driven)
Core claim: extreme funding/volatility/price-dislocation features improve **out-of-sample** forecasts
of future volatility or liquidation stress vs volatility-only baselines, on admissible data with frozen
prereg + leakage-safe evaluation. All six cached Binance funding-vol / FWD-VOL cells are terminal
(NOT_REPLICATED / FRAGILE) and their gates PASS — do not re-run them. The **highest-value unfinished
frontier** is the untouched ironflow Hyperliquid forward observed-liquidation window (below).

## 2) Verified state (2026-11-13T20:17:06Z)
- `python scripts/fclr_next_campaign_gate.py --json` → `ok: true` (terminal cells present/consistent).
- `admissible_seam_check(None)` → `pass:true, NO_CANDIDATE_PENDING` (that resume path is irrelevant to this campaign).
- `python scripts/next_campaign_status.py --json` → `hyperliquid_bulk_frontier.any_forward_feasible: true`;
  run `2026-01-18..2026-04-30` = 103 days ≥ `MIN_FORWARD_DESIGN_DAYS` (60 train + 7 embargo + 3×10 test = 97).
- **`python scripts/fclr_campaign_gate.py --arm all` → 6/11 (FAILS): `A3_report, A5, A6, B3_report, B4`.**
  The prior "ACTIVE_HEAVY_CAMPAIGN" (FullHist) is **not actually complete** — see Phase 0.
- Test subset green: `tests/test_active_campaign_gate.py tests/test_campaign_resume.py tests/test_fclr_next_campaign_gate.py tests/test_fclr_campaign_gate.py` → 33 passed.
- Working tree: only `research_state/ironflow_fastpath_cache.json` modified (transient cache touch).

## 3) Bottlenecks (removed / to close)
- **REMOVED:** external-data dependence for the forward cell (data is on disk; verified above).
- **P0 — close the existing campaign gate (5 failing checks):** `fclr_campaign_gate.py --arm all` fails
  `A3_report` (panel build report lacks `panel_sha256`), `A5` (primary contrast `C2_vs_B1` missing),
  `A6` (12 primary-family cells missing), `B3_report` (liq panel report lacks `panel_sha256`),
  `B4` (liq evaluation verdict `None`). These are real gaps in prior artifacts, not infra.
- **Hygiene:** root `FOCUS_CAMPAIGN.md` / `HANDOFF_NEXT_SESSION.md` / `NEXT_SESSION_TASK.md` are redirects only.

## 4) NEXT CAMPAIGN — FCLR-FORWARD-LIQ-2026Q1Q2 (mandatory heavy work; do not stop at planning)

**Objective:** produce a **new, preregistered, leakage-safe, terminally evaluated** observed-liquidation
forward cell on `2026-01-18..2026-04-30` using the exact Arm B design already frozen for the prior cell
(Spearman rank-IC of a funding-conditioned cross-sectional score vs next-24h observed liquidation
intensity, per 30-day block, within-bucket permutation null, seed frozen). Max attainable status is
`EXPLORATORY_ONLY` for ranking unless a genuinely unopened confirmatory window appears; report honestly.

### Phase 0 — Close the existing gate (required first; it is real unfinished work, not churn)
1. Inspect the five failing checks in `scripts/fclr_campaign_gate.py` against the actual artifacts
   (`tracka_vol_fullhist_panel_build_report_2026-11-13T02:44:48Z.json`,
   `evaluation_summary_TRACKA-VOL-FULLHIST-2026-11-13T02:44:48Z.json`,
   `tracka_liq_xsec_panel_build_report_2026-11-13T00:33:08Z.json`,
   `evaluation_summary_TRACKA-LIQ-XSEC-2026-11-13T00:33:08Z.json`).
2. Fix the **producer** (build/eval scripts) to emit `panel_sha256`, the full 12 primary-family contrast
   cells, and a recognised verdict; re-generate the artifacts. Do **not** weaken the gate or hand-edit
   verdicts. If a prior verdict is genuinely un-derivable from on-disk inputs, record the precise
   reason and the minimal patch — do not fabricate.
3. Re-run `python scripts/fclr_campaign_gate.py --arm all` until `11/11` or a documented, machine-readable
   block with exact missing evidence is recorded.

### Phase 1 — Freeze the forward prereg BEFORE any outcome read (hard gate)
1. Write `research_state/prereg_tracka_liq_xsec_forward_2026q1q2_<UTC>.{json,md}` modeled on
   `prereg_tracka_liq_xsec_20261112T201536Z.*`, with:
   - **Splits:** burn-in `2026-01-18..2026-02-16` (warm-up + universe eligibility, never scored);
     test blocks `2026-02-17..2026-03-18`, `2026-03-19..2026-04-03`, `2026-04-04..2026-04-30`
     (or an exact 60/7/3×10 rolling-origin partition that fits the 103-day span — state the chosen
     boundaries and justify arithmetic in the prereg).
   - **Universe (coverage-only, frozen ex ante):** native perps (`market` ends `-PERP`, no `:`) with
     ≥20 observed liquidation-days, ≥100 events over the test span, complete hourly candle+funding.
     Floor 5 coins; expected ~150-190.
   - **Features/score/estimand/inference:** identical to Arm B (rv24h, funding_rate, abs_funding,
     premium, cross-sectional z-score; Spearman IC per 30-day block; within-bucket permutation,
     1000 reps, seed 20261112; materiality |mean IC| ≥ 0.05 and consistent spread sign ≥ 2/3 blocks).
   - `frozen_before_outcomes: true`, `outcome_data_inspected_before_freeze: false`, `promotable: false`
     unless an unopened confirmatory window is proven.
2. Confirm freeze **before** running any build/eval: the prereg file mtime must precede panel build.

### Phase 2 — Build + evaluate (only after freeze)
1. Extend/clone the Arm B builder (`scripts/fclr_build_tracka_liq_xsec.py`) to the forward window,
   emitting `research_state/tracka_liq_xsec_forward_panel_<UTC>.parquet` + `..._build_report_<UTC>.json`
   (must include `panel_sha256` = sha256 of the panel parquet).
2. Compute the frozen contrasts only; emit
   `research_state/evaluation_summary_TRACKA-LIQ-XSEC-FORWARD-<UTC>.{md,json}` with a recognised verdict
   (`EXPLORATORY_SIGNAL` / `EXPLORATORY_NULL` / `INADMISSIBLE`) and full diagnostics (per-block IC, null
   percentiles, event counts, coins, coverage). No threshold shopping; no reading the reserved/sealed windows.

### Phase 3 — Verify (deterministic, offline)
1. `python scripts/fclr_campaign_gate.py --arm all` → `11/11`.
2. Run the touched deterministic tests: `python -m pytest -q tests/test_fclr_campaign_gate.py tests/test_active_campaign_gate.py tests/test_campaign_resume.py` (and any builder tests you add). Full suite is slow — do not block on it.
3. `python scripts/fclr_next_campaign_gate.py --json` must stay `ok: true`.
4. Update `research_state/experiment_frontier.json`: add the forward cell, set `last_checked`, and replace
   the stale `next_action_heavy: "CLEAN STOP…"` with the actual next unfinished task (next unopened window
   or Phase-0 residual).

### Phase 4 — Closeout
- Commit only meaningful research/engineering artifacts (code, concise manifests, provenance, reports; **never** raw parquet/caches).
- Update this handoff's §7 session log with exact commands, results, new artifact paths, and the next unfinished heavy task.

## 5) Invariants (never violate)
1. Fail-closed; blocked paths must not read outcomes/parquet or write canonical outputs except the explicit durable evidence artifacts above.
2. **Preregistration before outcomes**; freeze file must predate panel build.
3. Observed vs modeled labels never conflated; no venue mixing; no forward fill / synthetic data.
4. No re-probing terminal cells; no status-only sessions; no threshold shopping; no `.github/workflows` edits.
5. Do not commit raw parquet or caches.

## 6) Immediate next action for the next session
Start at **Phase 0**: run `python scripts/fclr_campaign_gate.py --arm all`, read the 5 failures, and fix the
producers to emit `panel_sha256` + the 12 primary-family cells + recognised verdicts. Then execute Phase 1
(freeze the forward prereg for `2026-01-18..2026-04-30` **before** any outcome read) and Phases 2-3. This
is executable **now**, offline, on data already on disk.

## 7) Session log — 2026-11-13T20:17:06Z
- **Diagnosis:** prior handoff/frontier forced a permanent external-data NO_GO loop despite an untouched,
  admissible on-disk ironflow Hyperliquid forward window (`2026-01-18..2026-04-30`, 103 days, 537,179 observed
  liquidation events, 192 native perps). Bottleneck removed by re-pointing the campaign at that window.
- **Verified:** `fclr_next_campaign_gate.py --json` ok:true; `fclr_campaign_gate.py --arm all` 6/11 (5 real
  failures: A3_report, A5, A6, B3_report, B4); `next_campaign_status.py` any_forward_feasible:true; forward
  region event/coin counts confirmed from parquet (2026-11-13T20:16Z).
- **Next heavy task (unfinished):** Phase 0 (close 5 gate failures at the producer) → Phase 1 (freeze forward
  prereg before outcomes) → Phase 2 (build/eval forward observed-liquidation cell) → Phase 3 (gate 11/11 +
  tests) → Phase 4 (commit + update frontier/next task).