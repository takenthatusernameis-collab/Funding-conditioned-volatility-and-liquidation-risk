# AGENT HANDOFF — 2026-11-14T10:15:38Z

## Campaign Context
**Repository:** Funding-conditioned-volatility-and-liquidation-risk
**Active Campaign (Rank 0):** FCLR-LIQ-EXPANSION-RECONCILIATION-20261114T083642Z
**Status:** READY_EXECUTE | program_status: ACTIVE

## The Single Durable Initial Task for the Next Session

**Execute the sealed-vs-recompute reconciliation (Phase RECONCILIATION):**

1. **Freeze the prereg** — Write `research_state/prereg_tracka_liq_expansion_reconciliation_20261114T083642Z.{json,md}` with status `FROZEN_PRE_OUTCOMES`, `frozen_before_outcomes=true`, `outcome_data_inspected_before_freeze=false`, `promotable=false`, `max_status=EXPLORATORY_ONLY`, `audit_only=true`, `does_not_reopen_sealed_verdict=true`.

2. **Implement `scripts/fclr_liq_expansion_reconcile.py`** — A 2×2 audit crossing two panels × two likelihoods:
   - Panel A: Sealed expansion panel (`research_state/tracka_hl_expansion_panel_20261111T202344Z.parquet`, sha256 `39916a72dfc37d15b6cc886d4e43ed878e0b8e1c2f22936fc4ebf8edd366f699`)
   - Panel B: Recompute panel (`research_state/tracka_liq_expansion_recompute_panel_20261114T083000Z.parquet`, sha256 `a4d73c79683550a15e616f3f5fbd93128db1c5498944f9139226f543cfe96715`)
   - Both panels have 1,472 rows and identical (coin, ts) keys; base label/funding/RV features are present in both.
   - Likelihood 1: Sealed estimator (as used in TRACKA-HL-EXPANSION-20261111T195500Z)
   - Likelihood 2: Recompute estimator (as used in FCLR-LIQ-EXPANSION-RECOMPUTE-20261114T073346Z)
   - Each cell produces a C2_vs_B1 rel QLIKE reduction with 2000-rep paired circular block bootstrap (block_h=1, seed 20261114), Holm across 3 contrasts, LOIO, funding-permutation placebo (200 reps), per-symbol/per-block stability, leakage audit.
   - Frozen splits: train 2026-05-01..2026-05-31, val 2026-06-07..2026-06-30, test blocks 2026-07-07..2026-08-06 / 2026-08-13..2026-09-11 / 2026-09-18..2026-10-17, 7-day purge/embargo.
   - Stop rule: instruments ≥5, test blocks ≥3, core_coverage ≥0.80 → else INADMISSIBLE with exact failing minima.

3. **Emit evaluation summary** — `research_state/evaluation_summary_TRACKA-LIQ-EXPANSION-RECONCILIATION-<UTC>.{json,md}` with verdict in {`EXPLAINED_BY_ESTIMATOR`, `EXPLAINED_BY_DATA`, `UNEXPLAINED`, `INCONCLUSIVE`}. All outputs `EXPLORATORY_ONLY`, `promotable=false`. Do not reopen sealed artifacts.

4. **Add test module** — `tests/test_fclr_liq_expansion_reconcile.py` asserting the reconciliation logic, schema, and that the 2×2 cells are produced.

5. **Run the campaign gate** — `python3 scripts/fclr_campaign_gate.py --arm all` (expect 19/19 PASS) and targeted unittest modules.

## Critical Constraints (Non-Negotiable)

- **No network access** — All inputs are cached on disk.
- **No outcome inspection before freeze** — Prereg must be written and validated `FROZEN_PRE_OUTCOMES` before any reconciliation computation.
- **No threshold relaxation** — Stop-rule minima are frozen in the prereg; failure = INADMISSIBLE with exact evidence.
- **No sealed artifact mutation** — The sealed expansion panel and its evaluation are read-only.
- **No status-only output** — Every session must produce the reconciliation artifacts or fail with evidenced blockers.

## Evidence Already on Disk (Inputs)

| Artifact | Path | SHA256 |
|----------|------|--------|
| Sealed expansion panel | `research_state/tracka_hl_expansion_panel_20261111T202344Z.parquet` | `39916a72dfc37d15b6cc886d4e43ed878e0b8e1c2f22936fc4ebf8edd366f699` |
| Sealed expansion eval | `research_state/evaluation_summary_TRACKA-HL-expansion-20261111T202344Z.json` | C2_vs_B1 19.0371%, CI [-5.088,-0.478], n_pairs=593, n_blocks=3, LOIO 4/8, placebo FAIL |
| Recompute panel | `research_state/tracka_liq_expansion_recompute_panel_20261114T083000Z.parquet` | `a4d73c79683550a15e616f3f5fbd93128db1c5498944f9139226f543cfe96715` |
| Recompute eval | `research_state/evaluation_summary_TRACKA-LIQ-EXPANSION-RECOMPUTE-20261114T083000Z.json` | C2_vs_B1 6.19%, CI [-0.421,-0.034], n_pairs=593, n_blocks=3, LOIO 7/8, placebo FAIL |

Both panels share 1,472 (coin, ts) keys. The open question is estimator vs. data attribution — not missing data.

## Expected Verdict Space

- `EXPLAINED_BY_ESTIMATOR` — The gap is attributable to estimator differences (e.g., different OLS scaling, feature construction, or fitting).
- `EXPLAINED_BY_DATA` — The gap is attributable to data differences (e.g., label, funding, or RV values diverge on the shared keys).
- `UNEXPLAINED` — Neither estimator nor data alone explains the gap; interaction or unknown factor.
- `INCONCLUSIVE` — Coverage/numerical limits prevent a clean attribution.

## Bottleneck Removal

No agent-removable blockers. The reconciliation uses only sealed panels, frozen splits, and cached data — no Gate 4, no new liquidation source, no network required.

## Next Heavy Action if This Session Cannot Complete

If the reconciliation script cannot be completed in one session, the next session must continue from the exact same frozen prereg and the same two panels. Do not re-freeze, do not re-split, do not re-acquire data. The task is deterministic and bounded.

---
*Generated 2026-11-14T10:15:38Z as the single durable handoff for the FCLR-LIQ-EXPANSION-RECONCILIATION campaign. Future agents must not avoid this heavy work — the 19.04% vs 6.19% gap will not close itself.*