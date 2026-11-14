# Durable Agent Handoff — 2026-11-14T21:25:00Z

## Authority and scope

This is the single operative handoff for the next agentic session.
Repository focus: **funding-conditioned volatility and liquidation risk**. Do not start unrelated work, add schedulers, edit `.github/workflows/*`, fetch paid/credentialed/manual data, commit raw cache, or reopen sealed verdicts.

Evidence cutoff for this handoff: worktree verified at 2026-11-14T21:25:00Z.
Latest completed experiments:
- `FCLR-FWD-VOL-2025-DISJOINT-CROSS-20261114T183000Z` (executed 2026-11-14T19:16:15Z, verdict **EXPLORATORY_NULL**, not confirmatory/not promotable). Gate PASS.
- `FCLR-FWD-VOL-2025-DISJOINT-RECONCILE-20261114T193000Z` (executed 2026-11-14T19:30:00Z; panel build 2026-11-14T20:40:00Z, verdict **UNEXPLAINED**, promotable=false, EXPLORATORY_ONLY). Full artifact set emitted: prereg json/md, evaluation json/md, cleaned panel + build report. LOIO + per-block diagnostics complete. **This stage is COMPLETE; do not re-run.**

Sealed state is healthy: `scripts/fclr_fwd_vol_2025_disjoint_cross_gate.py` PASS, `python3 scripts/next_campaign_status.py` shows executable heavy work remains (disjoint 30-day test blocks feasible incl. 2024-06 untouched), targeted tests `test_next_campaign_status` + `test_fclr_liq_expansion_recompute` + `test_fclr_fwd_vol_2025_disjoint_reconcile` PASS (57 tests).

## Initial task (heavy, mandatory): 2024-06 singleton diagnostic under a new frozen prereg

The reconcile stage is complete with verdict UNEXPLAINED: neither estimator conventions nor the cleaned data copy produce a material, dominant swing; the EXPLORATORY_NULL is preserved as a bounded negative result; LOIO/per-block diagnostics are done; do not tune features or relax gates.

Create campaign `FCLR-FWD-VOL-2024-DISJOINT-2024-06-<UTC>` (UTC start timestamp) and execute it end-to-end as a **singleton diagnostic only** — never a fresh three-block confirmation. This is the single remaining untouched disjoint Binance block (FEASIBLE per `scripts/next_campaign_status.py`; not in the forbidden tested-months list `2025-06/2025-11/2025-12`).

### 1. Freeze pre-results protocol before inspecting any outcome

Write both JSON and Markdown prereg artifacts under `research_state/` with status `FROZEN_PRE_OUTCOMES`, `frozen_before_outcomes=true`, and `outcome_data_inspected_before_freeze=false`.

Protocol must:
- build the 2024-06 panel from the cached `2024-04`/`2024-05`/`2024-06` mark/premium/index/funding CSVs (train `2024-04-25..2024-05-24`, test `2024-06-01..2024-06-30`, 7-day embargo), recording source sha256, row count, key count, symbol set, span;
- reuse the frozen B0/B1/C1/C2 feature sets and primary C2 vs B1 24h QLIKE contract from the reconcile prereg;
- define the same two estimator arms (sealed: raw features, no scaling, no smearing; corrected: train-only standardization, finite-row masking, train-only log-target smearing, drop-only missingness);
- run paired out-of-sample QLIKE contrasts over the single 2024-06 block: C2 vs B1 (primary), C1 vs B1, C2 vs C1;
- require row/key/lineage hashes and per-cell coverage before outcome fitting; any mismatch is `INCONCLUSIVE`, not a numeric result;
- report mean QLIKE differences, relative reductions, day-block-bootstrap CIs (deterministic seed), Holm-adjusted p-values, LOIO, and funding-permutation placebo;
- classify result as `EXPLAINED_BY_ESTIMATOR`, `EXPLAINED_BY_DATA`, `UNEXPLAINED`, or `INCONCLUSIVE`; all outputs remain `EXPLORATORY_ONLY` and `promotable=false`.

Do not inspect model predictions, contrasts, target summaries, metric values, or outcome distributions before prereg freeze. Coverage/arithmetic checks are allowed; outcome computation is not.

### 2. Implement and run the 2024-06 diagnostic

Implement a dedicated script under `scripts/` (do not modify sealed campaign scripts/artifacts). Reuse helpers only where safe; make the two estimator implementations explicit and independently testable. Add focused tests under `tests/` covering at least: frozen prereg identity, panel hash, train/test embargo, feature causality, finite-row masking, train-only scaling/smearing, deterministic bootstrap seed, and leakage audit.

Run at least a smoke execution and the full 2024-06 execution. Emit:
- `research_state/prereg_<campaign>_<UTC>.json` and `.md`
- `research_state/<campaign>_panel_<UTC>.parquet` plus build report (sha256, row count, key count, source hash, coverage)
- `research_state/evaluation_summary_<campaign>_<UTC>.json` and `.md`
- focused tests and command output in final report

### 3. Decide next bounded stage from evidence

- Any verdict: preserve result as bounded negative / UNEXPLAINED / INCONCLUSIVE; all outputs EXPLORATORY_ONLY, promotable=false.
- Do NOT re-open the sealed 2025 reconcile or CROSS verdicts. Do NOT run tested disjoint months `2025-06`, `2025-11`, `2025-12`. Do NOT run a fresh three-block confirmation on 2024-06 (singleton only).
- Design minimum failure: emit timestamped `INCONCLUSIVE` or `NO_GO` with exact failing checks.

A bounded negative result is valid completion; a status-only session is not.

## Required verification before completion

```bash
cd /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk
python3 scripts/next_campaign_status.py
python3 scripts/fclr_fwd_vol_2025_disjoint_cross_gate.py
python3 -m unittest tests.test_next_campaign_status tests.test_fclr_liq_expansion_recompute tests.test_fclr_fwd_vol_2025_disjoint_reconcile -v
# plus all new 2024-06 diagnostic tests added this session
```

Verify `NEXT_SESSION_HANDOFF.md` remains a tombstone, `AGENT_HANDOFF.md` remains sole active handoff, and no sealed artifact hash changed.

## Hard evidence rules

- Existing 2025 disjoint result is **not** evidence of practical edge: pooled C2-B1 mean diff `+0.006923`, relative reduction `-1.963%`, 95% CI `[-0.012604, 0.028030]`, Holm not passed, LOIO not passed, placebo passed.
- Reconcile verdict **UNEXPLAINED**: max estimator swing 2.127pp, max data swing 2.231pp; no material dominant swing; preserved as bounded negative result.
- Gate 4 remains `EXTERNAL_BLOCKED` unless valid `research_state/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` exists with `status=RESOLVED_VERIFIED`, `fabricated=false`, and human/legal attestation. Never fabricate/self-certify.
- Do not re-run tested Binance windows: `2024-07-23..2024-09-30`, `2025-02-01..2025-05-31`, `2025-07-23..2025-10-15`, `2026-01-01..2026-04-01`, `2026-05-01..2026-08-31`, `2026-08-03..2026-10-31`, or tested disjoint months `2025-06`, `2025-11`, `2025-12`. 2024-06 is untouched and FEASIBLE — it is the subject of this session's initial task.
- Do not relabel exploratory results as confirmatory, promote H1, invent provenance, or use future information for scaling/fitting/threshold selection/imputation.
- Preserve all prior artifacts and null results. Update frontier/registry atomically under new experiment IDs; never mutate sealed records.

## Completion contract

Session is complete only when it has either (a) executed the frozen 2024-06 singleton diagnostic and emitted the full artifact set with tests and verdict, or (b) produced a timestamped evidence-backed blocker showing exact failed precondition. Status-only work is not completion.

## Next session resume triggers (act only when satisfied)

1. `GATE4_BRANCH_1`: valid `research_state/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` appears (`status==RESOLVED_VERIFIED`, `fabricated==false`, human/legal attestation) → execute Gate 4 Branch 1 per gate scripts/tests.
2. `NEW_OBSERVED_LIQUIDATION_SOURCE`: materially new candidate → formal §16 admissibility audit artifact proving ALL minima BEFORE any prereg/outcomes; if ADMISSIBLE → freeze prereg pre-outcomes → build/eval/verdict under a NEW experiment ID.
3. `HL_LABEL_EXTENSION`: Hyperliquid ≥100d depth AND verified post-2026-10-31 observed liquidation labels → bounded reprobe only.
