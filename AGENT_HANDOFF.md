# Durable Agent Handoff — 2026-11-14T21:06:23Z

## Authority and scope

This is the single operative handoff for the next agentic session.

Repository focus: **funding-conditioned volatility and liquidation risk**. Do not start unrelated work, add schedulers, edit `.github/workflows/*`, fetch paid/credentialed/manual data, commit raw cache, or reopen sealed verdicts.

Evidence cutoff for this handoff: worktree verified at 2026-11-14T21:06:23Z. Latest completed experiment is `FCLR-FWD-VOL-2025-DISJOINT-CROSS-20261114T183000Z` (executed 2026-11-14T19:16:15Z, verdict **EXPLORATORY_NULL**, not confirmatory/not promotable). Sealed state is healthy: `scripts/fclr_fwd_vol_2025_disjoint_cross_gate.py` PASS, `python3 scripts/next_campaign_status.py` shows executable heavy work remains (disjoint 30-day test blocks feasible incl. 2024-06 untouched), targeted tests `test_next_campaign_status` + `test_fclr_liq_expansion_recompute` PASS (21 tests).

## Initial task (heavy, mandatory): estimator/data reconciliation on cached 2025 disjoint panel

Create campaign `FCLR-FWD-VOL-2025-DISJOINT-RECONCILE-20261114T210623Z` (or a later UTC timestamp if rerun) and execute it end-to-end. Do not stop at status checks, planning, or repeating this handoff.

### 1. Freeze pre-results protocol before inspecting any outcome

Write both JSON and Markdown prereg artifacts under `research_state/` with status `FROZEN_PRE_OUTCOMES`, `frozen_before_outcomes=true`, and `outcome_data_inspected_before_freeze=false`.

Protocol must:
- reuse existing panel `research_state/tracka_fwd_vol_2025_disjoint_cross_panel_20261114T191615Z.parquet` (sha256 `de0ca73e7d092a205e5f8c1163d56437384d1b15d65b4a27bc54a57e21738cba`);
- use only these already materialized 30-day train/test blocks with the same 7-day embargo:
  - train `2025-04-25..2025-05-24`, test `2025-06`
  - train `2025-09-25..2025-10-24`, test `2025-11`
  - train `2025-10-25..2025-11-23`, test `2025-12`
- keep frozen B0/B1/C1/C2 feature sets and primary C2 vs B1 24h QLIKE contract from `research_state/prereg_fclr_fwd_vol_2025_disjoint_cross_20261114T183000Z.json`;
- define a sealed-reference estimator arm (raw features, no leakage-safe scaling, no target-derived fills) and a corrected-estimator arm (train-only standardization, finite-feature masking, train-only log-target smearing, explicit missingness policy);
- run a two-by-two attribution matrix over {existing panel, a lineage-preserving cleaned copy} × {sealed estimator, corrected estimator};
- require row/key/lineage hashes and per-cell coverage before outcome fitting; any row-key or feature-lineage mismatch is `INCONCLUSIVE`, not a numeric result;
- report mean QLIKE differences, relative reductions, paired block-bootstrap CIs, Holm-adjusted p-values, LOIO, and funding-permutation placebo;
- classify result as `EXPLAINED_BY_ESTIMATOR`, `EXPLAINED_BY_DATA`, `UNEXPLAINED`, or `INCONCLUSIVE`; all outputs remain `EXPLORATORY_ONLY` and `promotable=false`.

Do not inspect model predictions, contrasts, target summaries, metric values, or outcome distributions before prereg freeze. Coverage/arithmetic checks are allowed; outcome computation is not.

### 2. Implement and run the reconciliation

Implement a dedicated script under `scripts/` (do not modify sealed campaign scripts/artifacts). Reuse helpers only where safe; make the two estimator implementations explicit and independently testable. Add focused tests under `tests/` covering at least: frozen prereg identity, panel hash, train/test embargo, feature causality, finite-row masking, train-only scaling/smearing, deterministic bootstrap seed, and leakage audit.

Run at least a smoke execution and the full cached-panel execution. Emit:
- `research_state/prereg_<campaign>_<UTC>.json` and `.md`
- `research_state/<campaign>_reconciliation_panel_<UTC>.parquet` if cleaned copy needed, plus build report (sha256, row count, key count, source hash, coverage)
- `research_state/evaluation_summary_<campaign>_<UTC>.json` and `.md`
- focused tests and command output in final report

### 3. Decide next bounded stage from evidence

- `EXPLAINED_BY_ESTIMATOR`: treat existing null as implementation-sensitive exploratory result, document defensible estimator, then run the single remaining untouched disjoint Binance block `2024-06` under a **new frozen prereg** (train `2024-04-25..2024-05-24`, test `2024-06-01..2024-06-30`) as a singleton diagnostic only (never a fresh three-block confirmation).
- `EXPLAINED_BY_DATA`: freeze row-level lineage repair/audit before further model evaluation.
- `UNEXPLAINED`: run LOIO/per-block diagnostics and preserve result; do not tune features or relax gates.
- Design minimum failure: emit timestamped `INCONCLUSIVE` or `NO_GO` with exact failing checks.

A bounded negative result is valid completion; a status-only session is not.

## Required verification before completion

```bash
cd /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk
python3 scripts/next_campaign_status.py
python3 scripts/fclr_fwd_vol_2025_disjoint_cross_gate.py
python3 -m unittest tests.test_next_campaign_status tests.test_fclr_liq_expansion_recompute -v
# plus all new reconciliation tests added this session
```

Verify `NEXT_SESSION_HANDOFF.md` remains a tombstone, `AGENT_HANDOFF.md` remains sole active handoff, and no sealed artifact hash changed.

## Hard evidence rules

- Existing 2025 disjoint result is **not** evidence of practical edge: pooled C2-B1 mean diff `+0.006923`, relative reduction `-1.963%`, 95% CI `[-0.012604, 0.028030]`, Holm not passed, LOIO not passed, placebo passed.
- Gate 4 remains `EXTERNAL_BLOCKED` unless valid `research_state/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` exists with `status=RESOLVED_VERIFIED`, `fabricated=false`, and human/legal attestation. Never fabricate/self-certify.
- Do not re-run tested Binance windows: `2024-07-23..2024-09-30`, `2025-02-01..2025-05-31`, `2025-07-23..2025-10-15`, `2026-01-01..2026-04-01`, `2026-05-01..2026-08-31`, `2026-08-03..2026-10-31`, or tested disjoint months `2025-06`, `2025-11`, `2025-12`.
- Do not relabel exploratory results as confirmatory, promote H1, invent provenance, or use future information for scaling/fitting/threshold selection/imputation.
- Preserve all prior artifacts and null results. Update frontier/registry atomically under new experiment IDs; never mutate sealed records.

## Completion contract

Session is complete only when it has either (a) executed the frozen reconciliation and emitted full artifact set with tests and verdict, or (b) produced a timestamped evidence-backed blocker showing exact failed precondition. Status-only work is not completion.
