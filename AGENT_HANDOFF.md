# Durable Agent Handoff — 2026-11-14T22:11:45Z

**Sole active handoff.** `NEXT_SESSION_HANDOFF.md` is a tombstone; `research_state/FCLR_CAMPAIGN_NEXT.md` is superseded historical evidence. Execute the campaign below and ignore conflicting historical directives.

## State (verified 2026-11-14T22:11:45Z)

- Repo focus: **funding-conditioned volatility and liquidation risk**. Do not start unrelated work, add schedulers, edit `.github/workflows/*`, fetch paid/credentialed/manual data, commit raw cache, or reopen sealed verdicts.
- Sealed/complete: `FCLR-FWD-VOL-2025-DISJOINT-CROSS-20261114T183000Z` (**EXPLORATORY_NULL**, not confirmatory/not promotable, gate PASS). `FCLR-FWD-VOL-2025-DISJOINT-RECONCILE-20261114T193000Z` (**UNEXPLAINED**, EXPLORATORY_ONLY, promotable=false) — full artifact set emitted; **do not re-run**.
- Health checks (passing): `python3 scripts/next_campaign_status.py` → executable heavy work remains (disjoint 30-day block `2024-06` FEASIBLE, untouched). `python3 scripts/fclr_fwd_vol_2025_disjoint_cross_gate.py` → PASS. `python3 -m unittest tests.test_next_campaign_status tests.test_fclr_liq_expansion_recompute tests.test_fclr_fwd_vol_2025_disjoint_reconcile -v` → 57 OK.
- Data/cache verified: 2024-04/05/06 complete for 5 symbols with mark/premium/index/funding (`research_state/data_cache/*_2024_04..06` present; `data/raw/*-fundingRate-2024-0{4,5,6}.csv` present). 2024-06 is the single remaining untouched disjoint Binance block (train `2024-04-25..2024-05-24`, test `2024-06-01..2024-06-30`, 7-day embargo).
- Hard evidence: pooled 2025 disjoint C2-B1 mean diff `+0.006923`, rel reduction `-1.963%`, 95% CI `[-0.012604, 0.028030]` (Holm not passed, LOIO not passed, placebo passed). Reconcile UNEXPLAINED (max estimator swing 2.127pp, max data swing 2.231pp) — bounded negative, preserved.
- Confirmatory program status: **COMPLETE / CONCLUDED** (final_synthesis_report.md 2026-11-10). No confirmatory gate passed. Track A (observed liquidations) STRUCTURALLY_BLOCKED. No risk overlay eligible.

## Initial task (heavy, mandatory): 2024-06 singleton diagnostic

Create campaign `FCLR-FWD-VOL-2024-DISJOINT-2024-06-<UTC>` and execute end-to-end as a **singleton diagnostic only** (never a fresh three-block confirmation). Do **not** run tested disjoint months `2025-06`, `2025-11`, `2025-12`.

### 1. Freeze pre-results protocol before inspecting any outcome

Write `research_state/prereg_<campaign>_<UTC>.json` and `.md` with `status: "FROZEN_PRE_OUTCOMES"`, `frozen_before_outcomes: true`, `outcome_data_inspected_before_freeze: false`, `promotable: false`, `max_status: "EXPLORATORY_ONLY"`.

Protocol must:
- Build panel from cached `2024-04`/`2024-05`/`2024-06` mark/premium/index/funding data (train `2024-04-25..2024-05-24`, test `2024-06-01..2024-06-30`, 7-day embargo); record source sha256, row count, key count, symbol set, span.
- Reuse frozen B0/B1/C1/C2 feature sets and primary C2 vs B1 24h QLIKE contract from the disjoint/reconcile preregs.
- Define same two estimator arms explicitly and independently testable: **sealed** (raw features, no scaling, no smearing) and **corrected** (train-only standardization, finite-row masking, train-only log-target smearing, drop-only missingness).
- Run paired out-of-sample QLIKE contrasts over the single 2024-06 block: C2 vs B1 (primary), C1 vs B1, C2 vs C1.
- Require row/key/lineage hashes and per-cell coverage before outcome fitting; any mismatch is `INCONCLUSIVE`, not numeric.
- Report mean QLIKE differences, relative reductions, day-block-bootstrap CIs (deterministic seed), Holm-adjusted p-values, LOIO, and funding-permutation placebo.
- Verdict space: `EXPLAINED_BY_ESTIMATOR` | `EXPLAINED_BY_DATA` | `UNEXPLAINED` | `INCONCLUSIVE`; all outputs `EXPLORATORY_ONLY`, `promotable=false`.

Do not inspect predictions/contrasts/target summaries/metric values/outcome distributions before prereg freeze. Coverage/arithmetic checks allowed; outcome computation is not.

### 2. Implement and run

- Add dedicated script under `scripts/` (do not modify sealed campaign scripts/artifacts). Reuse helpers only where safe; make estimator arms explicit and independently testable.
- Add focused tests under `tests/` covering at least: frozen prereg identity, panel hash, train/test embargo, feature causality, finite-row masking, train-only scaling/smearing, deterministic bootstrap seed, leakage audit.
- Run smoke and full 2024-06 execution. Emit:
  - `research_state/prereg_<campaign>_<UTC>.json` and `.md`
  - `research_state/<campaign>_panel_<UTC>.parquet` + build report (sha256, row count, key count, source hash, coverage)
  - `research_state/evaluation_summary_<campaign>_<UTC>.json` and `.md`
  - focused tests and command output in final report

### 3. Decide from evidence (bounded)

- Preserve result as bounded negative / UNEXPLAINED / INCONCLUSIVE as warranted; all outputs EXPLORATORY_ONLY, promotable=false.
- Do NOT re-open sealed 2025 reconcile/CROSS verdicts. Do NOT run `2025-06/2025-11/2025-12`. Do NOT run a fresh three-block confirmation on 2024-06.
- Minimum failure: emit timestamped `INCONCLUSIVE` or `NO_GO` with exact failing checks. Bounded negative result is valid completion; status-only session is not.

## Verification before completion

```bash
cd /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk
python3 scripts/next_campaign_status.py
python3 scripts/fclr_fwd_vol_2025_disjoint_cross_gate.py
python3 -m unittest tests.test_next_campaign_status tests.test_fclr_liq_expansion_recompute tests.test_fclr_fwd_vol_2025_disjoint_reconcile -v
# plus all new 2024-06 diagnostic tests added this session
```

Verify `NEXT_SESSION_HANDOFF.md` remains tombstone, this file remains sole active handoff, and no sealed artifact hash changed.

## Hard rules

- 2025 disjoint result is **not** evidence of practical edge. Reconcile verdict **UNEXPLAINED** preserved.
- Gate 4 remains `EXTERNAL_BLOCKED` unless valid `research_state/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` exists with `status=RESOLVED_VERIFIED`, `fabricated=false`, and human/legal attestation. Never fabricate/self-certify.
- Do not re-run tested Binance windows: `2024-07-23..2024-09-30`, `2025-02-01..2025-05-31`, `2025-07-23..2025-10-15`, `2026-01-01..2026-04-01`, `2026-05-01..2026-08-31`, `2026-08-03..2026-10-31`, or tested disjoint months `2025-06/2025-11/2025-12`. `2024-06` is untouched and is this session's task.
- No leakage: no future information for scaling/fitting/threshold selection/imputation. Do not relabel exploratory as confirmatory, promote H1, or invent provenance.
- Preserve all prior artifacts and null results. Update frontier/registry atomically under new experiment IDs; never mutate sealed records.

## Resume triggers (act only when satisfied)

1. `GATE4_BRANCH_1`: valid `research_state/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` appears (`RESOLVED_VERIFIED`, `fabricated==false`, human/legal attestation) → execute Gate 4 Branch 1 per gate scripts/tests.
2. `NEW_OBSERVED_LIQUIDATION_SOURCE`: materially new candidate → formal §16 admissibility audit proving ALL minima BEFORE prereg/outcomes; if ADMISSIBLE → freeze prereg pre-outcomes → build/eval/verdict under NEW experiment ID.
3. `HL_LABEL_EXTENSION`: Hyperliquid ≥100d depth AND verified post-2026-10-31 observed liquidation labels → bounded reprobe only.
4. `EXPANSION_ROBUSTNESS_REDO`: cached-panel robustness with NEW frozen prereg pre-outcomes (if trigger arrives).

## Completion contract

Complete only when (a) frozen 2024-06 singleton diagnostic executed with full artifact set + tests + verdict, or (b) timestamped evidence-backed blocker with exact failed precondition emitted. Status-only work is not completion.

## Next agent guardrails (enforceable)

- If the next agent finds this handoff superseded by a newer timestamped AGENT_HANDOFF.md, follow the newer one.
- If no newer handoff exists, this is the binding directive. Do not "plan" or "explore" — execute the 2024-06 singleton diagnostic per §1-3 above.
- The repository contains all necessary cached data for 2024-04/05/06. No network access is required or permitted.
- The confirmatory program is concluded. This diagnostic is a bounded, exploratory-only attribution cell — not a path to confirmatory status.