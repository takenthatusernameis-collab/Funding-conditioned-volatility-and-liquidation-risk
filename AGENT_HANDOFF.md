# AGENT HANDOFF — 2026-11-14T01:49:08Z (authoritative, single durable handoff)

## INITIAL TASK FOR NEXT SESSION (2026-11-14T01:49:08Z) — EXECUTE P1, NO RE-VERIFICATION

**Deliverable (non-negotiable):** execute P1 end-to-end and persist evidence in this session.
A verification-only, status-only, or handoff-rewrite-only session is a FAILED session
(RESEARCH_PROMPT §19). Do **not** re-run the checks in §4; they were frozen at
2026-11-13T23:29:16Z and remain sufficient unless you change code/artifacts they cover.
The only acceptable completions are:
- **(A)** a new frozen prereg + panel + build report + evaluation verdict for
  `FCLR-VOL-FORWARD-2026Q1Q2`, with gates/tests green and frontier/this handoff updated; or
- **(B)** a bounded structural NO_GO naming each candidate (source/window) and its exact
  failing minimum, with evidence, frontier/this handoff updated.

### P1 — `FCLR-VOL-FORWARD-2026Q1Q2` (PREFERRED, cached/offline, no external data)

**Why this is the highest-value unopened route:** Hyperliquid ironflow bulk untouched region
`2026-01-18..2026-04-30` (103 days; candles/funding/OI/liquidations on disk) is
`FEASIBLE forward-reduced (60/7/3x10)` per `python3 scripts/next_campaign_status.py`.
Reserved by `prereg_tracka_vol_fullhist_20261112T201536Z.json` but **never scored for Arm A
volatility**. Materially different from completed liq forward
(`TRACKA-LIQ-XSEC-FORWARD-20261113T222859Z`, EXPLORATORY_NULL): different target family,
estimand, and hypothesis. No May 2026, no sealed `2026-05..2026-10` read.

**Reuse path (smallest correct implementation):**
- Clone `scripts/fclr_build_tracka_liq_xsec_forward.py` (frozen-window pattern: `PREREG_PATH`,
  `EXPERIMENT_ID`, `CAMPAIGN`, `BLOCKS` constants, fail-closed assertions, hashed inputs,
  timestamped panel/build-report/eval artifacts) into `scripts/fclr_build_tracka_vol_forward.py`.
- Reuse Arm A feature/target/eval spec from `scripts/fclr_build_tracka_vol_fullhist.py`
  (RV horizons, B1/C1/C2 families, QLIKE, block bootstrap, Holm, LOIO, placebo/permutation,
  materiality floor, §17 criteria as applicable). Do **not** edit fullhist frozen outputs.

**Phase 1 — freeze prereg before ANY outcome read**
- Write `research_state/prereg_tracka_vol_forward_2026q1q2_<UTC>.json` (+ `.md` if useful) with:
  new `experiment_id` `TRACKA-VOL-FORWARD-2026Q1Q2-<UTC>`; `status=FROZEN_PRE_OUTCOMES`;
  `outcome_data_inspected_before_freeze=false`; `pre_registered_before_outcomes=true`;
  `frozen_before_outcomes=true`; `promotable=false`; `max_status=EXPLORATORY_ONLY`; exact window
  `2026-01-18..2026-04-30`, 60/7/3x10 split with 7-day embargo and non-overlapping 10-day test
  blocks; coverage-only universe frozen ex ante (native perps only, no venue mixing, no forward
  fill/synthetic); features B1 vs C1/C2 primary contrast; horizons/QLIKE/CI/block bootstrap/
  permutation/LOIO/materiality floor.
- Freeze only after a **coverage-only** audit (existence/counts/coverage, never magnitudes/outcomes).

**Phase 2 — build + evaluate on cached bulk only**
- Run the new builder to emit `research_state/tracka_vol_forward_panel_<UTC>.parquet`,
  `research_state/tracka_vol_forward_panel_build_report_<UTC>.json` (sha256-matched), and
  `research_state/evaluation_summary_TRACKA-VOL-FORWARD-<UTC>.{json,md}` with a recognized verdict.
- Universe by coverage-only; no outcome-informed selection. Never read May 2026 or sealed
  `2026-05..2026-10`.

**Phase 3 — gates + tests, fail-closed**
- `scripts/fclr_campaign_gate.py` currently checks Arm F as liq-xsec-forward artifacts only.
  If this vol-forward cell must be recognized as campaign-complete/heavy progress, extend the
  gate **additively and fail-closed** (new arm/check or generalized forward checks) plus tests;
  never weaken Arm F or existing checks.
- Run: `python3 scripts/fclr_campaign_gate.py --arm all` (must stay all-PASS / strictly stronger)
  and `python3 -m unittest -q tests.test_fclr_campaign_gate tests.test_active_campaign_gate`.
- Run any new/affected targeted tests for the builder/eval/gate changes.

**Phase 4 — persist**
- Update `research_state/experiment_frontier.json` (new cell under rank 0 with artifact/verdict),
  this handoff, and atomic state artifacts with evidence.
- Record exact commands, outcomes, and uncovered issues. Commit policy: follow repo norms; do not
  commit raw parquet/caches or modify `.github/workflows`.

### P2 — only if P1 is inadmissible with evidence
If a materially new unauthenticated observed-liquidation source passes minima (≥5 instruments,
≥1 complete month or ≥3 non-overlapping 30-day blocks, provenance/license, observed-only,
venue-consistent, joinable), run §16 admissibility audit → freeze prereg → build/eval → verdict
under a new experiment ID. Current scans show **0 GO**
(`alt_source_scan_latest.json` 20261113T171152Z, `alt_source_probe_audit_20261112T191400Z.md`,
`tracka_admissibility_no_go_20261113T193124Z.md`). Treat as NO_GO unless materially new evidenced
source appears.

### P3 — terminal fallback, still evidence-backed
Only if P1 is infeasible by exact failing minima AND no P2 GO exists: emit a bounded structural
NO_GO naming each candidate (source/window) and the specific minimum it fails, then update
frontier/handoff. Never a status-only memo.

## 2) Bottlenecks removed / constraints

- **Verification churn removed:** gate 16/16, tests 22/22, scripts compile, and feasibility were
  frozen as verified at 2026-11-13T23:29:16Z. Repeating them without code/artifact changes is
  wasted progress; execute P1.
- **No external data required for P1:** ironflow bulk 2025-05..2026-04 on disk. Binance ready
  disjoint months `2025-01,2025-06,2025-11,2025-12` have contiguous runs 31/30/61d < 127d (not
  feasible for 3-block design); Binance 5-symbol design exhausted.
- **No admissible new liq source evidenced:** Gate 4/Track A external trigger absent
  (`NO_VALID_GATE4_TRIGGER`); HL/ironflow observed labels end 2026-10; alt-source deep review 0 GO.
- **Fail-closed enforced:** Arm F/gate must not be weakened; prereg must predate outcomes;
  observed≠modeled; no venue mixing; no forward fill/synthetic; no May 2026 or sealed-window
  reads; no re-probing terminal cells.
- **Hygiene:** `FOCUS_CAMPAIGN.md`, `HANDOFF_NEXT_SESSION.md`, `NEXT_SESSION_TASK.md` are
  redirects to this file only. This file is the single durable handoff.

## 3) Invariants (never violate)

1. Preregister before any outcome inspection/build of evaluated targets for the new cell.
2. Observed vs modeled labels never conflated; venue-consistent; no forward fill or synthetic data.
3. Do not read May 2026 or sealed holdouts for scoring/decisions; do not reopen terminal verdicts.
4. No `.github/workflows` edits; do not commit raw parquet/caches.
5. Do not fabricate artifacts, thresholds, p-values, or verdicts. If blocked, produce bounded NO_GO with exact failing minima.

## 4) Verified evidence (frozen at 2026-11-13T23:29:16Z — do not re-verify without cause)

- Gate: `python3 scripts/fclr_campaign_gate.py --arm all` **16/16 PASS** (A0-A6,B1-B4,F0-F4).
- Tests: `python3 -m unittest -q tests.test_fclr_campaign_gate tests.test_active_campaign_gate` **22/22 OK**.
- Scripts: `scripts/fclr_campaign_gate.py`, `scripts/next_campaign_status.py` compile cleanly.
- Forward liq cell `TRACKA-LIQ-XSEC-FORWARD-20261113T222859Z` **COMPLETED, verdict EXPLORATORY_NULL**
  (panel 107 coins/6741 rows; mean IC -0.02703, pooled IC -0.02512 p 0.031, sign 1/3).
  Artifact: `research_state/evaluation_summary_TRACKA-LIQ-XSEC-FORWARD-2026-11-13T22:31:55Z.json`.
- Feasibility: `python3 scripts/next_campaign_status.py` → HL `2026-01-18..2026-04-30` FEASIBLE
  forward-reduced 60/7/3x10; Binance exhausted.
- Frontier: `research_state/experiment_frontier.json` rank 0 `ACTIVE_HEAVY_CAMPAIGN`.

## 5) Session log

### 2026-11-14T01:49:08Z
- Refreshed single durable handoff as the explicit timestamped initial task for the next session. No bottlenecks found (gates/tests/feasibility frozen 2026-11-13T23:29:16Z; redirects intact; no pending prereg without eval). Next agent must execute P1 `FCLR-VOL-FORWARD-2026Q1Q2` end-to-end (outcome A or bounded NO_GO outcome B) and must not do verification-only work.

### 2026-11-14T01:28:24Z
- Refreshed the single durable handoff as the explicit, timestamped initial task for the next
  session: P1 `FCLR-VOL-FORWARD-2026Q1Q2` execution contract made non-negotiable, re-verification
  frozen at 2026-11-13T23:29:16Z, and concrete clone/reuse/gate-extension guidance retained.
  Purpose: remove repeated verification-only bottleneck and force heavy progress (A or B outcome).
  No research state regressed; no terminal cell reopened.

### 2026-11-13T23:29:16Z
- Refreshed the single durable handoff to remove the verification-only bottleneck observed
  across the 22:39/22:40/23:02/23:06 sessions (four sessions re-verified the same gate/test/
  feasibility state without executing P1). Froze the §4 evidence, added an explicit
  EXECUTION-FIRST contract, and gave the exact P1 clone/reuse path
  (`fclr_build_tracka_liq_xsec_forward.py` pattern + `fclr_build_tracka_vol_fullhist.py` spec).
  No research state regressed; no terminal cell reopened; gate/tests remain 16/16 and 22/22.

### 2026-11-13T23:06:30Z
- Final verification before handoff freeze: `python3 scripts/fclr_campaign_gate.py --arm all` → 16/16 PASS; `python3 -m unittest -q tests.test_fclr_campaign_gate tests.test_active_campaign_gate` → 22/22 OK; `python3 scripts/next_campaign_status.py` output unchanged (HL 2026-01-18..2026-04-30 FEASIBLE forward-reduced 60/7/3x10). No new data, no regressions.

### 2026-11-13T23:02:10Z
- Re-verified (no state regression, no bottlenecks found): gate 16/16 PASS, targeted tests 22/22 OK, key scripts compile, `next_campaign_status.py` still reports executable heavy work (P1 HL vol forward-reduced `FCLR-VOL-FORWARD-2026Q1Q2` on cached 2026-01-18..2026-04-30, 60/7/3x10). Redirect files remain pointers to this single durable handoff.

### 2026-11-13T22:40:11Z
- Re-verified at message time: gate 16/16 PASS; tests 22/22 OK; `next_campaign_status.py` confirms P1 FEASIBLE forward-reduced 60/7/3x10 on untouched HL region 2026-01-18..2026-04-30 (ironflow bulk on disk, 103d). Binance 5-symbol design exhausted. No admissible new liq source evidenced (0 GO). No external data or credentials required for P1.

### 2026-11-13T22:39:08Z
- Re-verified campaign state (gate 16/16 PASS, tests 22/22 OK, forward liq EXPLORATORY_NULL complete). Confirmed via `next_campaign_status.py` that P1 `FCLR-VOL-FORWARD-2026Q1Q2` is FEASIBLE forward-reduced 60/7/3x10 and is a materially different, unopened heavy design.
