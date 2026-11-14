# AGENT HANDOFF — 2026-11-14T08:36:42Z (single durable handoff)

## INITIAL TASK FOR NEXT AGENTIC WORK SESSION (MANDATORY, HEAVY, OFFLINE, UNBLOCKED)

**Campaign:** `FCLR-LIQ-EXPANSION-RECONCILIATION-20261114T083642Z`
**Experiment ID:** `FCLR-LIQ-EXPANSION-RECONCILIATION-20261114T083642Z`

**Start here. Do not write a status-only, inventory-only, or planning-only response. Do not re-run Phase B. Do not wait for Gate 4 or a new data source.**

### Why this is the highest-value next task

The repository is `Funding-conditioned-volatility-and-liquidation-risk`. Phase B completed the independent recomputation of the sealed Track A liquidation-expansion PASS, but it returned **INCONCLUSIVE**:

- Sealed `TRACKA-HL-EXPANSION-20261111T202344Z`: C2-vs-B1 relative QLIKE reduction **19.0371%**, CI `[-5.088102, -0.477660]`, 593 pairs, 3 blocks, 8 instruments.
- Recomputed `TRACKA-LIQ-EXPANSION-RECOMPUTE-20261114T083000Z`: **6.19%**, CI `[-0.42074401, -0.03377946]`, 593 pairs, 3 blocks; placebo FAIL (true 6.19% <= null p95 7.6603%); LOIO 7/8.

The panels have the same 1,472 `(coin, ts)` keys and the same observed liquidation labels, funding, candles, and base features. The unresolved scientific question is therefore not “run Phase B again”; it is:

> **Is the sealed 19.04% result an estimator artifact, a data-lineage artifact, or a genuinely non-reproducible result?**

The leading alternative explanation is the estimator difference: the sealed evaluation used raw features, no training-only scaling, no smearing correction, and zero-filled missing funding/premium/EMA values; the recompute used train-only z-scoring, Duan smearing, and complete-case rows. A frozen 2×2 reconciliation can attribute the 19.04% → 6.19% gap without reopening the sealed verdict.

### Exact sequence (do all of it in this session)

1. **Freeze a prereg before computing any outcome.** Create:
   - `research_state/prereg_tracka_liq_expansion_reconciliation_20261114T083642Z.json`
   - `research_state/prereg_tracka_liq_expansion_reconciliation_20261114T083642Z.md`

   Required fields:
   - `experiment_id`: `FCLR-LIQ-EXPANSION-RECONCILIATION-20261114T083642Z`
   - `campaign`: `FCLR-FUND-VOL-LIQ-REDTEAM-20261114T042139Z`
   - `status`: `FROZEN_PRE_OUTCOMES`
   - `frozen_before_outcomes`: `true`
   - `pre_registered_before_outcomes`: `true`
   - `outcome_data_inspected_before_freeze`: `false`
   - `promotable`: `false`
   - `max_status`: `EXPLORATORY_ONLY`
   - `audit_only`: `true`
   - `does_not_reopen_sealed_verdict`: `true`
   - `panels`: sealed SHA-256 `39916a72dfc37d15b6cc886d4e43ed878e0b8e1c2f22936fc4ebf8edd366f699`; recompute SHA-256 `a4d73c79683550a15e616f3f5fbd93128db1c5498944f9139226f543cfe96715`
   - `estimators`: exact `sealed_like` and `recompute_like` definitions below
   - `grid`: `{sealed_panel, recompute_panel} × {sealed_like, recompute_like}`
   - `verdict_space`: `EXPLAINED_BY_ESTIMATOR|EXPLAINED_BY_DATA|UNEXPLAINED|INCONCLUSIVE`
   - `stop_rule`: both panels must retain 1,472 keys; aligned keys must match; >=5 instruments; >=3 test blocks; core coverage >=0.80; otherwise bounded `INADMISSIBLE` with exact failing minima.

2. **Write** `scripts/fclr_liq_expansion_reconcile.py` (new file; ~500–800 lines is fine; mirror the rigor of `scripts/fclr_liq_expansion_recompute.py`).

   **Read-only inputs:**
   - `research_state/tracka_hl_expansion_panel_20261111T202344Z.parquet` (sealed; SHA-256 `39916a72...f699`)
   - `research_state/tracka_liq_expansion_recompute_panel_20261114T083000Z.parquet` (recompute; SHA-256 `a4d73c79...6715`)

   **Panel alignment checks (fail closed):**
   - Verify both SHA-256s before loading.
   - Assert both have 1,472 rows and identical `(coin, ts)` keys.
   - Derive `target_next_intensity = liq_notional_usd.groupby(coin).shift(-1)` on both panels; assert the recompute panel’s stored target matches the derived target within `1e-9` relative tolerance.
   - Compare `liq_notional_usd`, `fundingRate`, `premium`, `rv1h`, `rv24h`, `rv168h`, `ema_dist`, and `abs_fund_pct`; report max absolute difference, count of mismatched cells, and any row-key differences.
   - Derive splits from the frozen timestamps exactly as the sealed evaluation did:
     - train `2026-05-01..2026-05-31`
     - validation `2026-06-07..2026-06-30`
     - test blocks `2026-07-07..2026-08-06`, `2026-08-13..2026-09-11`, `2026-09-18..2026-10-17`
     - 7-day purge/embargo at boundaries.

   **`sealed_like` estimator (must match the sealed evaluation path):**
   - Model rows: target > 0; B1 requires `rv1h`, `rv24h`, `rv168h` all non-null and > 0.
   - C2 = B1 + `fundingRate`, `abs_fund_pct`, `premium`, `ema_dist`; **missing values become 0.0**, exactly as the sealed evaluation did.
   - OLS on `log(target + 1e-12)`; no training-only scaling; no smearing; prediction `exp(X @ beta)`.
   - Fit on train rows only; evaluate on the three test blocks.
   - QLIKE = `y/yhat - log(y/yhat) - 1`; paired block bootstrap with seed `20261111`, 2,000 reps, blocks as in the sealed evaluation; relative reduction = `-mean_diff / mean_QLIKE(B1) * 100`.

   **`recompute_like` estimator (must match the current recompute path):**
   - Complete-case train rows for `CORE_FEATURES = [log_rv1h, log_rv24h, log_rv168h, signed_funding_z, abs_fund_pct_z, premium_z, ema_dist_z]`, target > 0.
   - Train-only mean/std scaling for `signed_funding`, `abs_fund_pct`, `premium`, `ema_dist`; train-only Duan smearing.
   - Models B0/B1/C1/C2 as in `scripts/fclr_liq_expansion_recompute.py`; evaluate on complete-case positive test rows.
   - Paired circular block bootstrap, seed `20261114`, 2,000 reps, 1-day blocks; Holm across the three contrasts.

   **Run the 2×2 grid:**
   - sealed panel × sealed_like
   - sealed panel × recompute_like
   - recompute panel × sealed_like
   - recompute panel × recompute_like

   For each cell report: `n_train`, `n_test`, `n_pairs`, `B1_QLIKE`, `C2_QLIKE`, `mean_diff`, `rel_reduction_pct`, `ci_lo`, `ci_hi`, `passes_materiality`, `ci_excludes_zero`, and `matches_sealed` / `matches_recompute` at a declared tolerance of **±0.5 percentage points**.

   **Attribution:**
   - `panel_effect = (recompute_panel × sealed_like) - (sealed_panel × sealed_like)`
   - `estimator_effect = (sealed_panel × recompute_like) - (sealed_panel × sealed_like)`
   - `interaction = (recompute_panel × recompute_like) - (recompute_panel × sealed_like) - estimator_effect`
   - State which effect explains the 19.0371% → 6.19% gap. If the estimator effect dominates, say so explicitly and do **not** call the sealed result “refuted”; call it an estimator-dependent result preserved under its sealed status.

3. **Emit** `research_state/evaluation_summary_TRACKA-LIQ-EXPANSION-RECONCILIATION-<UTC>.{json,md}` with:
   - `verdict`: one of `EXPLAINED_BY_ESTIMATOR|EXPLAINED_BY_DATA|UNEXPLAINED|INCONCLUSIVE`
   - `status`: `VALID_EXPLORATORY`
   - `promotable: false`, `max_status: EXPLORATORY_ONLY`, `audit_only: true`, `does_not_reopen_sealed_verdict: true`
   - the full 2×2 table, attribution terms, and an explicit sentence: “The sealed 19.04% survives / does not survive the corrected common-row, train-only-scaled, smearing estimator.”

4. **Add** `tests/test_fclr_liq_expansion_reconcile.py` (unittest style) covering:
   - both panel SHA-256s and key alignment;
   - `sealed_like` and `recompute_like` produce deterministic, finite predictions on a small synthetic fixture;
   - the 2×2 result has all four cells and all required fields;
   - sealed artifacts remain byte-identical (hash check).

5. **Run verification:**
   ```bash
   /tmp/fclr-venv/bin/python scripts/fclr_liq_expansion_reconcile.py --out-utc 2026-11-14T08:36:42Z
   /tmp/fclr-venv/bin/python scripts/fclr_campaign_gate.py --arm all
   /tmp/fclr-venv/bin/python -m unittest tests.test_active_campaign_gate tests.test_fclr_campaign_gate tests.test_fclr_liq_expansion_recompute tests.test_fclr_liq_expansion_reconcile
   ```
   Expected: gate **19/19 PASS**; all targeted tests pass.

6. **Atomically update after the run:**
   - `research_state/experiment_frontier.json`: advance the rank-0 reconciliation entry with the verdict, artifacts, and next action; keep rank 0 truthful and non-terminal.
   - `research_state/hypothesis_registry.json`: append an audit hypothesis `H_tracka_liq_expansion_reconciliation` with status `EXPLORATORY_ONLY`; do **not** alter the sealed `H_tracka_hl_symbol_expansion_liquidation_forecast` status.
   - Append to `research_state/negative_results_report.md` and `research_state/leakage_audit.md`.
   - Append a dated session log entry to this file.

### Definition of done for this session

- Frozen prereg exists with `FROZEN_PRE_OUTCOMES` and the exact fields above.
- `scripts/fclr_liq_expansion_reconcile.py` exists and runs end-to-end offline.
- All four 2×2 cells are present with finite metrics.
- The attribution verdict is one of the four allowed values and is backed by the table.
- `tests/test_fclr_liq_expansion_reconcile.py` passes; gate is 19/19; targeted tests pass.
- Sealed panel and sealed evaluation remain byte-identical.
- No status-only or planning-only output.

### What not to do

- **Do not** modify `research_state/tracka_hl_expansion_panel_20261111T202344Z.parquet` or `research_state/tracka_hl_expansion_eval_result_20261111T202344Z.json`.
- **Do not** re-run Phase B or Phase A; their outcomes are already recorded.
- **Do not** wait for Gate 4, a new liquidation source, or HL label extension; this campaign is fully offline.
- **Do not** promote anything; all outputs are `EXPLORATORY_ONLY` and `promotable=false`.
- **Do not** use `ironflow_bulk` (stops 2026-04) or invent missing funding/premium/EMA values.
- **Do not** replace the sealed 19.04% number in the sealed artifact.

### After reconciliation (next heavy work, same session if time permits)

- If `EXPLAINED_BY_ESTIMATOR`: freeze a corrected-estimator audit protocol and run the same 2×2 on the cached 9-symbol successor panel (if present) to test whether the estimator effect generalizes. Keep it `EXPLORATORY_ONLY`; the sealed holdout is already inspected, so no confirmatory claim.
- If `EXPLAINED_BY_DATA`: freeze a row-level data-lineage audit that isolates the mismatched buckets/features and quantifies their contribution to the gap.
- If `UNEXPLAINED`: run leave-one-instrument-out and per-block diagnostics on the 2×2 to find which symbol/block drives the gap; freeze that diagnostic before looking at outcomes.

---

## VERIFIED CURRENT STATE (2026-11-14T08:36:42Z)

| Item | Verified state | Evidence |
|---|---|---|
| Phase B recompute | **COMPLETE / VALID_EXPLORATORY / INCONCLUSIVE** | `evaluation_summary_TRACKA-LIQ-EXPANSION-RECOMPUTE-20261114T083000Z.{json,md}` |
| Phase B headline | C2-vs-B1 **6.19%** vs sealed **19.0371%**; placebo FAIL (null p95 7.6603%); LOIO 7/8 | same |
| Phase B panel | 1,472 buckets; 1,203 with label; 1,168 complete label+funding+RV; 8 instruments; 3 test blocks | `tracka_liq_expansion_recompute_panel_build_report_20261114T083000Z.json` |
| Sealed Track A | PASS, FRAGILE; unchanged | `tracka_hl_expansion_eval_result_20261111T202344Z.json`; `evaluation_summary_TRACKA-EXP-ROBUST-20261112T015119Z.md` |
| Campaign gate | **19/19 PASS** | `/tmp/fclr-venv/bin/python scripts/fclr_campaign_gate.py --arm all` |
| Targeted tests | **40/40 OK** after frontier rank-0 repair | `/tmp/fclr-venv/bin/python -m unittest tests.test_active_campaign_gate tests.test_fclr_campaign_gate tests.test_fclr_liq_expansion_recompute` |
| Environment | Use `/tmp/fclr-venv/bin/python`; system `python3` lacks `pyarrow`; `pytest` not installed; tests are `unittest` | handoff environment facts |

### Current research-gate state

- **H1 primary volatility:** `NOT_SUPPORTED` (terminal; sealed FCLR-011 PASS does not generalize forward).
- **Track A observed liquidation:** sealed expansion `SUPPORTED_PASS_PRIMARY_GATE` but `FRAGILE`; independent recompute `INCONCLUSIVE`; reconciliation is now the active audit.
- **Track A volatility:** `NOT_MET` (terminal).
- **Track B modeled breach:** `NOT_SUPPORTED` (terminal).
- **Funding-correction replication (H2):** `EXPLORATORY_ONLY` / PARTIAL (terminal).
- **Gate 4 / new observed-liquidation source:** external/legal trigger absent; not a blocker for the offline reconciliation.
- **Program status:** ACTIVE; the next task is the 2×2 estimator/data reconciliation above.

### Environment facts (do not rediscover)

- Use **`/tmp/fclr-venv/bin/python`** for anything needing `pyarrow`/`pandas`/`numpy`/`scipy`.
- System `python3` fails with `ModuleNotFoundError: pyarrow`.
- `pytest` is not installed; tests are `unittest`; run targeted modules.
- No network. No `.github/workflows/*` edits. No raw parquet/cache commits. No sealed-artifact overwrites. No fabricated artifacts/thresholds/p-values/verdicts.
- Unresolved Git-LFS pointer: `research_state/data_cache/fclr011_panel.json`; do not wait for LFS.

### Invariants

- Preregister before outcome inspection.
- Observed Hyperliquid liquidation labels only; no modeled/proxy/synthetic labels; no venue mixing.
- No forward-fill, no zero-fill of missing market features in the corrected estimator.
- Train-only fit/scaling/smearing.
- No May 2026 / sealed-holdout reuse as fresh confirmation.
- No terminal verdict reopening; sealed artifacts remain byte-identical.

---

## Session log

### 2026-11-14T08:36:42Z — Durable handoff rewritten as an execution-forcing reconciliation campaign
- Replaced the previous “Phase B complete; verify then await trigger / bounded NO_GO” handoff. That instruction was a bottleneck: it would have ended the next session without doing heavy work even though a high-information offline task remains.
- Added `FCLR-LIQ-EXPANSION-RECONCILIATION-20261114T083642Z`: a frozen 2×2 audit of sealed vs recomputed panel × sealed-like vs recompute-like estimator, with exact artifacts, tests, and acceptance criteria.
- Repaired the failing active-campaign gate: `tests.test_active_campaign_gate` requires exactly one rank-0 entry with `status=READY_EXECUTE` and `program_status=ACTIVE`; the frontier was updated to the new reconciliation campaign and the old Phase B entry was demoted to rank 1 with a terminal status.
- Re-ran verification: campaign gate **19/19 PASS**; targeted tests **40/40 OK** after the frontier repair.
- No sealed artifact modified; no outcome computation performed in this session.

### 2026-11-14T08:30:00Z — Phase B recompute completed (INCONCLUSIVE)
- `scripts/fclr_liq_expansion_recompute.py` implemented and run; frozen prereg `prereg_tracka_liq_expansion_recompute_20261114T073346Z.{json,md}`; panel `tracka_liq_expansion_recompute_panel_20261114T083000Z.parquet` (sha256 `a4d73c79...cfe96715`); evaluation summary emitted.
- C2-vs-B1 rel reduction **6.19%** (CI `[-0.42074401, -0.03377946]`, n_pairs=593, n_blocks=3, holm_p=0.036) vs sealed **19.0371%** — does NOT reproduce sealed (6.19% < 9.52% = sealed × 0.5).
- LOIO 7/8 (sealed 4/8) — passes. Placebo FAIL: true 6.19% <= null p95 7.6603%. core_coverage 0.9959; instruments 8; test blocks 3 — all stop-rule minima met.
- All outputs `EXPLORATORY_ONLY`, `promotable=false`; sealed artifacts unchanged.

### 2026-11-14T07:33:46Z — Prior handoff (superseded)
- Promoted Phase B as the primary heavy task; kept Phase A secondary/capped. Phase B has since completed; this entry is retained as history only.

### 2026-11-14T06:35:00Z — Prior bottleneck removal (superseded)
- Corrected the false claim that Phase A was ready and Phase B was blocked on `ironflow_bulk`; documented the Phase A 168h train-window dead end and the real Phase B input caches.

### 2026-11-14T04:21:39Z — Red-team campaign installed (superseded)
- Installed `FCLR-FUND-VOL-LIQ-REDTEAM-20261114T042139Z` with Phase A/B; repaired the artifact-count guard and removed the hardcoded active-campaign test.