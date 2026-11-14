# Agent Handoff — 2026-11-14T19:12:00Z

## Repository: Funding-conditioned-volatility-and-liquidation-risk

## Current State: READY_EXECUTE — frozen exploratory campaign open (heavy work unblocked)
- Rank 0: `FCLR-FWD-VOL-2025-DISJOINT-CROSS-20261114T183000Z` (`research_state/experiment_frontier.json`)
- Status: `READY_EXECUTE` / `ACTIVE` (prereg frozen `FROZEN_PRE_OUTCOMES`, `outcome_data_inspected_before_freeze=false`)
- Campaign: `EXPLORATORY_ONLY`, `promotable=false`, `max_status=EXPLORATORY_ONLY`
- Gate 4 Binance v5 terms: `EXTERNAL_BLOCKED` (no valid `research_state/fclr016_v5_terms_evidence_RESOLVED_*.json` with `status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal attestation). Do not claim confirmatory/promotion for H1.

## Bottlenecks removed (so far)
- `scripts/next_campaign_status.py` counts nested CSVs and detects disjoint 30d blocks (feasible: 2024-06, 2025-06, 2025-11, 2025-12).
- Prereg + coverage audit frozen: three 2025 blocks only (excludes 2024-06 warm-up): 2025-06-01..06-30 (train 2025-04-25..05-24), 2025-11-01..11-30 (train 2025-09-25..10-24), 2025-12-01..12-31 (train 2025-10-25..11-23). Coverage OK (5 symbols, 3600 test rows/block, train 2760/3432/3552).
- Fail-closed gate exists: `scripts/fclr_fwd_vol_2025_disjoint_cross_gate.py` (currently FAIL until executor + panel + build report + eval exist). This is the next agent’s work.

## Initial Task for Next Agentic Session (2026-11-14T19:12:00Z) — durable handoff
**Objective:** Execute the frozen exploratory campaign end-to-end. Produce panel/build report/eval, pass the gate, update frontier/handoff. No polling. No status-only output. Do not claim confirmatory/promotion.

### Step 0 — Baseline (read first)
- `AGENT_HANDOFF.md` (this file), `research_state/experiment_frontier.json` rank 0
- `research_state/prereg_fclr_fwd_vol_2025_disjoint_cross_20261114T183000Z.json` (+ `.md`)
- `research_state/coverage_audit_fwd_vol_2025_disjoint_cross_20261114T183000Z.json`
- Pattern: `scripts/fclr_fwd_vol_2025q1q2_cross.py`
- Gate: `scripts/fclr_fwd_vol_2025_disjoint_cross_gate.py`

### Step 1 — Deterministic checks (<60s)
```bash
cd /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk
python3 scripts/next_campaign_status.py
ls research_state/fclr016_v5_terms_evidence_RESOLVED_*.json 2>/dev/null || echo "NO_VALID_GATE4_TRIGGER"
python3 scripts/fclr_fwd_vol_2025_disjoint_cross_gate.py || true
```
Interpretation:
- If any valid `RESOLVED_VERIFIED` trigger appears (fabricated=false + human/legal attestation), stop this exploratory branch and follow Gate 4 confirmatory flow under a NEW experiment ID.
- Otherwise continue (exploratory only). Current expected: gate fails because `scripts/fclr_fwd_vol_2025_disjoint_cross.py`, panel, build report, eval are missing.

### Step 2 — Implement executor (heavy, required)
Create `scripts/fclr_fwd_vol_2025_disjoint_cross.py` by adapting `scripts/fclr_fwd_vol_2025q1q2_cross.py`.

Hard requirements:
- Assert prereg: `status == "FROZEN_PRE_OUTCOMES"`, `outcome_data_inspected_before_freeze is False`, `experiment_id == "FCLR-FWD-VOL-2025-DISJOINT-CROSS-20261114T183000Z"`.
- `DATA_START="2025-04-25T00:00:00Z"`, `DATA_END="2025-12-31T23:00:00Z"`. Use per-block `train_start/train_end` from prereg (do not use a single global train start).
- Blocks (from prereg):
  - b0: train 2025-04-25..2025-05-24, test 2025-06-01..2025-06-30
  - b1: train 2025-09-25..2025-10-24, test 2025-11-01..2025-11-30
  - b2: train 2025-10-25..2025-11-23, test 2025-12-01..2025-12-31
- Keep FCLR-011 model set, QLIKE, primary contrast C2 vs B1, 2000-rep day-block bootstrap, Holm family, LOIO, funding-permutation placebo, leakage audit.
- Verdicts only: `EXPLORATORY_SIGNAL | EXPLORATORY_NULL | INCONCLUSIVE | SMOKE`. Never `CONFIRMED`/`PROMOTED`. Every eval payload must include `promotable: false`, `max_status: "EXPLORATORY_ONLY"`.
- Emit (UTC-stamped names consistent with gate globs):
  - `research_state/tracka_fwd_vol_2025_disjoint_cross_panel_<UTC>.parquet`
  - `research_state/tracka_fwd_vol_2025_disjoint_cross_build_report_<UTC>.json` (must record `panel_sha256`)
  - `research_state/evaluation_summary_FCLR-FWD-VOL-2025-DISJOINT-CROSS-<UTC>.json`
  - `research_state/evaluation_summary_FCLR-FWD-VOL-2025-DISJOINT-CROSS-<UTC>.md`
- Eval JSON must include: `experiment_id`, `verdict`, `checks`, `primary`, `per_block`, `loio`, `placebo`, `leakage`, `n_symbols`, `n_blocks`, `promotable`, `max_status`.

### Step 3 — Run smoke then full
```bash
python3 scripts/fclr_fwd_vol_2025_disjoint_cross.py --smoke
python3 scripts/fclr_fwd_vol_2025_disjoint_cross.py
```
Expected: 5 symbols, 3 blocks, 3600 test rows/block, train rows 2760/3432/3552, no network, no sealed artifact mutation.

### Step 4 — Gate and tests
```bash
python3 scripts/fclr_fwd_vol_2025_disjoint_cross_gate.py
python3 -m pytest tests/test_next_campaign_status.py -v
python3 -m pytest tests/test_active_campaign_gate.py -v
```
Gate must PASS. If it fails, fix artifacts/metadata (do not weaken the gate).

### Step 5 — Atomic state updates
- Update `research_state/experiment_frontier.json` rank 0 to `COMPLETED_VALIDATED` or `SUPERSEDED` with verdict + artifact paths.
- Update `research_state/hypothesis_registry.json` only if repo convention requires a terminal/exploratory record for `H_fclr_fwd_vol_2025_disjoint_cross`; do not reopen sealed H1.
- Rewrite `AGENT_HANDOFF.md` (this file) with a new timestamped next task (or final summary if done). Update `NEXT_SESSION_HANDOFF.md` pointer timestamp if you change it.

## Verdict rules (enforce)
- `EXPLORATORY_SIGNAL`: materiality >= 2%, 95% CI excludes zero on improving side, Holm pass, LOIO >= 4/5, placebo pass, leakage pass, >=5 instruments, >=3 blocks.
- `EXPLORATORY_NULL`: materiality/CI fail with admissible data.
- `INCONCLUSIVE`: instruments<5 or blocks<3 or leakage fail or no finite primary rows.
- `SMOKE`: smoke only (not evidence). No `CONFIRMED`/`PROMOTED` while Gate 4 unresolved; `promotable=false` always.

## Hard stops
- Do not poll for Gate 4 triggers.
- Do not re-run tested/exhausted windows listed in prior handoffs (e.g. 2024-07-23..2024-09-30, 2025-02-01..2025-05-31, 2025-07-23..2025-10-15, 2026-01-01..2026-04-01, 2026-05-01..2026-08-31, 2026-08-03..2026-10-31, 2026-01-18..2026-04-30).
- Do not re-open sealed FCLR-011/012-V/013/014 artifacts.
- Do not produce status-only output.
- Do not commit raw cache. Do not edit `.github/workflows/*`.
- Every session ends with committed/state-updated work OR a bounded NO_GO + exact evidence.

## Verification snapshot (from prior session)
- `tests/test_next_campaign_status.py`: 15 passed; `tests/test_active_campaign_gate.py`: 5 passed (as of 2026-11-14T19:08:11Z). Re-run after changes.
