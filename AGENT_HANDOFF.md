# Durable Agent Handoff — 2026-11-14T19:20:32Z

## Authority and scope

This is the single operative handoff for the next agentic session.

Repository focus: **funding-conditioned volatility and liquidation risk**. Do not start unrelated work, add schedulers, edit `.github/workflows/*`, fetch paid/credentialed/manual data, commit raw cache, or reopen sealed verdicts.

Evidence cutoff for this handoff: the current worktree at 2026-11-14T19:20:32Z. The latest completed experiment is `FCLR-FWD-VOL-2025-DISJOINT-CROSS-20261114T183000Z`, executed at 2026-11-14T19:16:15Z with verdict **EXPLORATORY_NULL**. It is not confirmatory and is not promotable.

## Initial task: run a heavy estimator/data reconciliation on the cached 2025 panel

Create a new campaign ID, for example `FCLR-FWD-VOL-2025-DISJOINT-RECONCILE-20261114T193000Z`, and use this sequence. The work is deliberately specified so it must be performed rather than replaced with a status-only check.

### 1. Freeze a pre-results protocol before inspecting any outcome

Write both JSON and Markdown prereg artifacts under `research_state/` with status `FROZEN_PRE_OUTCOMES`, `frozen_before_outcomes=true`, and `outcome_data_inspected_before_freeze=false`.

The protocol must:

- reuse the existing panel `research_state/tracka_fwd_vol_2025_disjoint_cross_panel_20261114T191615Z.parquet` (sha256 `de0ca73e7d092a205e5f8c1163d56437384d1b15d65b4a27bc54a57e21738cba`);
- use only these already materialized 30-day train/test blocks, with the same 7-day embargo:
  - train `2025-04-25..2025-05-24`, test `2025-06`;
  - train `2025-09-25..2025-10-24`, test `2025-11`;
  - train `2025-10-25..2025-11-23`, test `2025-12`;
- keep the frozen B0/B1/C1/C2 feature sets and primary C2 vs B1 24h QLIKE contract from `research_state/prereg_fclr_fwd_vol_2025_disjoint_cross_20261114T183000Z.json`;
- define a sealed-reference estimator arm (raw features, no leakage-safe scaling, no target-derived fills) and a corrected-estimator arm (train-only standardization, finite-feature masking, train-only log-target smearing, explicit missingness policy);
- run a two-by-two attribution matrix over {existing panel, a lineage-preserving cleaned copy} × {sealed estimator, corrected estimator};
- require row/key/lineage hashes and per-cell coverage before outcome fitting; any row-key or feature-lineage mismatch is `INCONCLUSIVE`, not a numeric result;
- report mean QLIKE differences, relative reductions, paired block-bootstrap CIs, Holm-adjusted p-values, LOIO, and funding-permutation placebo;
- classify the result as `EXPLAINED_BY_ESTIMATOR`, `EXPLAINED_BY_DATA`, `UNEXPLAINED`, or `INCONCLUSIVE`; all outputs remain `EXPLORATORY_ONLY` and `promotable=false`.

Do not inspect model predictions, contrasts, target summaries, metric values, or outcome distributions before the prereg is frozen. Coverage/arithmetic checks are allowed; outcome computation is not.

### 2. Implement and run the reconciliation

Implement a dedicated script under `scripts/` rather than modifying the sealed campaign. Reuse existing helpers where safe, but make the two estimator implementations explicit and independently testable. Add focused tests under `tests/` covering at least: frozen prereg identity, panel hash, train/test embargo, feature causality, finite-row masking, train-only scaling/smearing, deterministic bootstrap seed, and leakage audit.

Run at least a smoke execution and the full cached-panel execution. Emit:

- `research_state/prereg_<campaign>_<UTC>.json` and `.md`;
- `research_state/<campaign>_reconciliation_panel_<UTC>.parquet` if a cleaned copy is needed, plus a build report containing sha256, row count, key count, source hash, and coverage;
- `research_state/evaluation_summary_<campaign>_<UTC>.json` and `.md`;
- focused tests and their command output in the final report.

### 3. Decide the next bounded stage from the evidence

- If attribution is `EXPLAINED_BY_ESTIMATOR`, treat the existing null as an implementation-sensitive exploratory result, document the defensible estimator, and proceed to the single remaining untouched disjoint Binance block `2024-06` under a **new frozen prereg** (train `2024-04-25..2024-05-24`, test `2024-06-01..2024-06-30`). Report it as a singleton diagnostic, never as a fresh three-block confirmation.
- If attribution is `EXPLAINED_BY_DATA`, freeze a row-level lineage repair/audit before any further model evaluation.
- If attribution is `UNEXPLAINED`, run LOIO/per-block diagnostics and preserve the result; do not tune features or relax gates.
- If any design minimum fails, emit a timestamped `INCONCLUSIVE` or `NO_GO` with exact failing checks. A bounded negative result is valid completion; a status-only session is not.

## Required verification

Before reporting completion:

```bash
cd /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk
python3 scripts/next_campaign_status.py
python3 scripts/fclr_fwd_vol_2025_disjoint_cross_gate.py
python3 -m unittest tests.test_next_campaign_status tests.test_fclr_liq_expansion_recompute -v
# run the new reconciliation tests added by the session
```

Also verify that `NEXT_SESSION_HANDOFF.md` remains a tombstone, that `AGENT_HANDOFF.md` remains the sole active handoff, and that no sealed artifact hash changed.

## Hard evidence rules

- The existing 2025 disjoint result is **not** evidence of a practical edge: pooled C2-B1 mean difference `+0.006923`, relative reduction `-1.963%`, 95% CI `[-0.012604, 0.028030]`, Holm not passed, LOIO not passed, placebo passed.
- Gate 4 remains `EXTERNAL_BLOCKED` unless a valid `research_state/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` exists with `status=RESOLVED_VERIFIED`, `fabricated=false`, and human/legal attestation. Never fabricate or self-certify it.
- Do not re-run tested Binance windows: `2024-07-23..2024-09-30`, `2025-02-01..2025-05-31`, `2025-07-23..2025-10-15`, `2026-01-01..2026-04-01`, `2026-05-01..2026-08-31`, `2026-08-03..2026-10-31`, or the tested disjoint months `2025-06`, `2025-11`, `2025-12`.
- Do not relabel exploratory results as confirmatory, promote H1, invent provenance, or use future information for scaling, fitting, threshold selection, or imputation.
- Preserve all prior artifacts and null results. Update the frontier/registry atomically under the new experiment ID; never mutate sealed records.

## Completion contract

The next session is complete only when it has either (a) executed the frozen reconciliation and emitted the full artifact set with tests and a verdict, or (b) produced a timestamped evidence-backed blocker showing the exact failed precondition. Merely checking status, finding no trigger, or repeating this handoff is not completion.
