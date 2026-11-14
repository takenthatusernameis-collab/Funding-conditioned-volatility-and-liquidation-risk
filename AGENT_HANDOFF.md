# SINGLE DURABLE HANDOFF — 2026-11-14T11:13:54Z (initial task for next agentic session)

## Repository / campaign
- **Repo:** `Funding-conditioned-volatility-and-liquidation-risk` (funding-conditioned volatility & liquidation risk, Hyperliquid/Track A frontier).
- **Active P0 (READY_EXECUTE, not complete):** `FCLR-LIQ-EXPANSION-RECONCILIATION-20261114T083642Z`
- **Program status:** ACTIVE, `max_status=EXPLORATORY_ONLY`, `promotable=false`, `audit_only=true`, `does_not_reopen_sealed_verdict=true`.
- **Single durable handoff:** this file only. `HANDOFF_NEXT_SESSION.md`, `NEXT_SESSION_TASK.md`, `FOCUS_CAMPAIGN.md`, `HANDOFF_20261114T101715Z.md` are REDIRECTs and must remain so. Do **not** declare campaign exhausted/complete or do status-only work until reconciliation artifacts exist and gates pass.

## Bottlenecks removed
- `HANDOFF_20261114T101715Z.md` false-closure ("CAMPAIGN COMPLETE / NO ACTIONABLE WORK REMAINS") is redirected/superseded here. No agent-removable blocker remains for this reconciliation: all inputs are cached on disk, deterministic, no network/Gate4/new liquidation source required.

## Required heavy work (do this; no deferral/relabel)
Attribute the **19.04% vs 6.19%** C2_vs_B1 QLIKE gap (sealed expansion vs recompute, shared 1,472 `(coin, ts)` keys). Produce a 2×2 audit: **{Sealed panel, Recompute panel} × {Sealed estimator, Recompute estimator}** with verdict in {`EXPLAINED_BY_ESTIMATOR`,`EXPLAINED_BY_DATA`,`UNEXPLAINED`,`INCONCLUSIVE`}.

### Execute in order
1. **Freeze prereg (before any outcome/reconciliation computation):** write `research_state/prereg_tracka_liq_expansion_reconciliation_20261114T083642Z.{json,md}` with `status=FROZEN_PRE_OUTCOMES`, `frozen_before_outcomes=true`, `outcome_data_inspected_before_freeze=false`, `promotable=false`, `max_status=EXPLORATORY_ONLY`, `audit_only=true`, `does_not_reopen_sealed_verdict=true`. Validate frozen state first.
2. **Implement** `scripts/fclr_liq_expansion_reconcile.py`: 2×2 cells, each reporting C2_vs_B1 relative QLIKE reduction + 2000-rep paired circular block bootstrap (`block_h=1`, seed `20261114`), Holm across 3 contrasts, LOIO, funding-permutation placebo (200 reps), per-symbol/per-block stability, leakage audit. **Frozen splits:** train 2026-05-01..2026-05-31, val 2026-06-07..2026-06-30, test blocks 2026-07-07..2026-08-06 / 2026-08-13..2026-09-11 / 2026-09-18..2026-10-17, 7-day purge/embargo. **Stop rule:** instruments ≥5, test blocks ≥3, core_coverage ≥0.80 else `INADMISSIBLE` with exact failing minima.
3. **Emit** `research_state/evaluation_summary_TRACKA-LIQ-EXPANSION-RECONCILIATION-<UTC>.{json,md}` with verdict + full 2×2 evidence; all `EXPLORATORY_ONLY`, `promotable=false`. Never mutate sealed artifacts.
4. **Add tests:** `tests/test_fclr_liq_expansion_reconcile.py` covering reconciliation logic, schema, and 2×2 cell production.
5. **Validate:** run relevant unittests and `python3 scripts/fclr_campaign_gate.py --arm all` (expect 19/19 PASS) if environment allows; record results.

### Inputs (cached, read-only)
| Artifact | Path | SHA256 / note |
|---|---|---|
| Sealed expansion panel | `research_state/tracka_hl_expansion_panel_20261111T202344Z.parquet` | `39916a72dfc37d15b6cc886d4e43ed878e0b8e1c2f22936fc4ebf8edd366f699` |
| Sealed expansion eval/result | `research_state/tracka_hl_expansion_eval_result_20261111T202344Z.json` (+ `.md`/build report) | sealed C2_vs_B1 19.0371%, CI [-5.088,-0.478], n_pairs=593, n_blocks=3, LOIO 4/8, placebo FAIL |
| Recompute panel | `research_state/tracka_liq_expansion_recompute_panel_20261114T083000Z.parquet` | `a4d73c79683550a15e616f3f5fbd93128db1c5498944f9139226f543cfe96715` |
| Recompute eval | `research_state/evaluation_summary_TRACKA-LIQ-EXPANSION-RECOMPUTE-20261114T083000Z.json` | `58b2ae2326e7358080cc073f7f98eb74b8f6e02c36a0329e06f1b5bf92fe2272` (INCONCLUSIVE, C2_vs_B1 6.19%, CI [-0.421,-0.034], n_pairs=593, n_blocks=3, LOIO 7/8, placebo FAIL) |

Panels share 1,472 `(coin, ts)` keys; base label/funding/RV features present in both. Question is estimator vs data attribution.

### Non-negotiable constraints
- No network; no outcome inspection before prereg freeze; no threshold relaxation; no sealed artifact mutation; no re-freeze/re-split/re-acquire if partial — continue from same frozen prereg and same two panels.

### If cannot finish this session
Leave code/tests/prereg/eval artifacts progressed on disk with exact failing step; next session continues same prereg+panels. No status-only closure.
