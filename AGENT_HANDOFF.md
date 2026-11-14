# Agent Handoff — 2026-11-14T18:30:00Z

## Repository: Funding-conditioned-volatility-and-liquidation-risk

## Current State: READY_EXECUTE — frozen exploratory campaign open

**Rank 0:** `FCLR-FWD-VOL-2025-DISJOINT-CROSS-20261114T183000Z`
**Status:** `READY_EXECUTE` / `ACTIVE`
**Campaign type:** `EXPLORATORY_ONLY` (`promotable=false`)
**Gate 4 Binance v5 terms:** `EXTERNAL_BLOCKED` (no valid `RESOLVED_VERIFIED` trigger)

The previous rank-0 trigger-only sentinel `FCLR-BOUNDED-TRIGGER-ONLY-20261114T132741Z` is demoted to rank 1 with status `SUPERSEDED`. It was based on a false exhaustion: `scripts/next_campaign_status.py` only checked a contiguous 127-day rolling-origin design and undercounted nested CSVs. Independent 30-day test blocks are executable heavy work.

---

## Bottleneck removed this session

1. `scripts/next_campaign_status.py` now:
   - counts CSVs recursively (`**/*.csv`), so nested cache layouts are not reported empty;
   - detects disjoint 30-day test blocks with their own 30-day train window and 7-day embargo;
   - reports 4 feasible disjoint blocks: `2024-06`, `2025-06`, `2025-11`, `2025-12`.
2. The frozen prereg selects the three 2025 blocks:
   - `2025-06-01..2025-06-30`
   - `2025-11-01..2025-11-30`
   - `2025-12-01..2025-12-31`
3. Coverage audit confirms 5 symbols, 3 blocks, 3600 test rows per block, train rows 2760/3432/3552, all coverage checks pass.
4. A fail-closed definition-of-done gate exists:
   - `scripts/fclr_fwd_vol_2025_disjoint_cross_gate.py`
   - It currently FAILS because the executor, panel, build report, and evaluation summary do not exist yet. That is the next agent's heavy work.

`2024-06` is feasible but excluded from the prereg to keep a single 2025 regime and avoid early-funding warm-up.

---

## Initial Task for Next Agentic Session (2026-11-14T18:30:00Z) — durable handoff

**Objective:** Execute the frozen exploratory campaign. Produce the panel, build report, evaluation JSON+MD, and pass the definition-of-done gate. Do not stop at status output. Do not poll. Do not claim confirmatory status.

### Step 0 — Baseline (read first)
- `AGENT_HANDOFF.md` (this file)
- `research_state/experiment_frontier.json` rank 0
- `research_state/prereg_fclr_fwd_vol_2025_disjoint_cross_20261114T183000Z.json`
- `research_state/prereg_fclr_fwd_vol_2025_disjoint_cross_20261114T183000Z.md`
- `research_state/coverage_audit_fwd_vol_2025_disjoint_cross_20261114T183000Z.json`
- `scripts/fclr_fwd_vol_2025q1q2_cross.py` (executor pattern)
- `scripts/fclr_fwd_vol_2025_disjoint_cross_gate.py` (definition of done)

### Step 1 — Deterministic checks (<60s)
```bash
cd /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk
python3 scripts/next_campaign_status.py
ls research_state/fclr016_v5_terms_evidence_RESOLVED_*.json 2>/dev/null || echo "NO_VALID_GATE4_TRIGGER"
python3 scripts/fclr_fwd_vol_2025_disjoint_cross_gate.py || true
```

Interpretation:
- If a valid `fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` appears with `status=RESOLVED_VERIFIED`, `fabricated=false`, and human/legal attestation, stop this exploratory branch and follow the Gate 4 confirmatory process under a NEW experiment ID.
- Otherwise the campaign remains `EXPLORATORY_ONLY`. Continue to Step 2.

### Step 2 — Implement the executor (heavy)
Create `scripts/fclr_fwd_vol_2025_disjoint_cross.py` by adapting `scripts/fclr_fwd_vol_2025q1q2_cross.py`.

Required changes:
- PREREG path: `research_state/prereg_fclr_fwd_vol_2025_disjoint_cross_20261114T183000Z.json`
- Assert `status == "FROZEN_PRE_OUTCOMES"` and `outcome_data_inspected_before_freeze is False`.
- Assert `experiment_id == "FCLR-FWD-VOL-2025-DISJOINT-CROSS-20261114T183000Z"`.
- `DATA_START = "2025-04-25T00:00:00Z"`; `DATA_END = "2025-12-31T23:00:00Z"`.
- Read `train_start` and `train_end` per block from the prereg. Do not use a single global train start.
- Blocks:
  - block 0: train `2025-04-25..2025-05-24`, test `2025-06-01..2025-06-30`
  - block 1: train `2025-09-25..2025-10-24`, test `2025-11-01..2025-11-30`
  - block 2: train `2025-10-25..2025-11-23`, test `2025-12-01..2025-12-31`
- Keep the FCLR-011 model set, QLIKE, C2 vs B1 primary contrast, 2000-rep day-block bootstrap, Holm family, LOIO, funding-permutation placebo, and leakage audit.
- Verdicts must be `EXPLORATORY_SIGNAL`, `EXPLORATORY_NULL`, `INCONCLUSIVE`, or `SMOKE`. Never `CONFIRMED` or `PROMOTED`.
- Evaluation payload must include `promotable: false` and `max_status: "EXPLORATORY_ONLY"`.
- Emit:
  - `research_state/tracka_fwd_vol_2025_disjoint_cross_panel_<UTC>.parquet`
  - `research_state/tracka_fwd_vol_2025_disjoint_cross_build_report_<UTC>.json`
  - `research_state/evaluation_summary_FCLR-FWD-VOL-2025-DISJOINT-CROSS-<UTC>.json`
  - `research_state/evaluation_summary_FCLR-FWD-VOL-2025-DISJOINT-CROSS-<UTC>.md`
- The build report must record `panel_sha256`.
- The evaluation JSON must include `experiment_id`, `verdict`, `checks`, `primary`, `per_block`, `loio`, `placebo`, `leakage`, `n_symbols`, `n_blocks`, `promotable`, `max_status`.

### Step 3 — Run smoke, then full
```bash
python3 scripts/fclr_fwd_vol_2025_disjoint_cross.py --smoke
python3 scripts/fclr_fwd_vol_2025_disjoint_cross.py
```

Expected:
- 5 symbols
- 3 blocks
- 3600 test rows per block
- train rows 2760/3432/3552
- no network
- no sealed artifact mutation

### Step 4 — Gate and tests
```bash
python3 scripts/fclr_fwd_vol_2025_disjoint_cross_gate.py
python3 -m pytest tests/test_next_campaign_status.py -v
python3 -m pytest tests/test_active_campaign_gate.py -v
```

The new gate must PASS. If it fails, fix the missing artifact or metadata; do not weaken the gate.

### Step 5 — Atomic state updates
- Update `research_state/experiment_frontier.json`: rank 0 status `COMPLETED_VALIDATED` or `SUPERSEDED` with the evaluation verdict and artifact paths.
- Update `research_state/hypothesis_registry.json` only if the repo convention requires a terminal/exploratory record for `H_fclr_fwd_vol_2025_disjoint_cross`; do not reopen sealed H1.
- Rewrite `AGENT_HANDOFF.md` with the next timestamped task.
- Update `NEXT_SESSION_HANDOFF.md` pointer timestamp.

---

## Verdict rules (must be enforced)

- `EXPLORATORY_SIGNAL`: materiality >= 2%, 95% CI excludes zero on the improving side, Holm pass, LOIO >= 4/5, placebo pass, leakage pass, >= 5 instruments, >= 3 blocks.
- `EXPLORATORY_NULL`: materiality or CI fails with admissible data.
- `INCONCLUSIVE`: instruments < 5, blocks < 3, leakage fail, or no finite primary rows.
- `SMOKE`: smoke run only; not evidence.

No `CONFIRMED` or `PROMOTED` verdict is permitted while Gate 4 Binance v5 terms evidence is unresolved. `promotable=false` in every artifact.

---

## Hard stop rules

- Do not poll for Gate 4 triggers.
- Do not re-run tested/exhausted windows (`2024-07-23..2024-09-30`, `2025-02-01..2025-05-31`, `2025-07-23..2025-10-15`, `2026-01-01..2026-04-01`, `2026-05-01..2026-08-31`, `2026-08-03..2026-10-31`, `2026-01-18..2026-04-30`).
- Do not re-open sealed FCLR-011/012-V/013/014 artifacts.
- Do not produce status-only output.
- Do not commit raw cache.
- Do not edit `.github/workflows/*`.
- Every session must end with committed/state-updated work or a bounded NO_GO plus exact evidence.

---

## Verification status this session

- `tests/test_next_campaign_status.py`: 15 passed
- `tests/test_active_campaign_gate.py`: 5 passed
- `scripts/next_campaign_status.py`: reports executable disjoint heavy work
- `scripts/fclr_fwd_vol_2025_disjoint_cross_gate.py`: FAIL as expected (executor/panel/eval not yet produced)

## Key files

1. `research_state/experiment_frontier.json` — rank 0 is the new disjoint campaign
2. `research_state/prereg_fclr_fwd_vol_2025_disjoint_cross_20261114T183000Z.json` — frozen prereg
3. `research_state/coverage_audit_fwd_vol_2025_disjoint_cross_20261114T183000Z.json` — coverage audit
4. `scripts/fclr_fwd_vol_2025q1q2_cross.py` — executor pattern
5. `scripts/fclr_fwd_vol_2025_disjoint_cross_gate.py` — definition-of-done gate
6. `scripts/next_campaign_status.py` — fixed status tool
7. `tests/test_next_campaign_status.py` — regression tests
8. `tests/test_active_campaign_gate.py` — frontier invariant guard