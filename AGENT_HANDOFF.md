# Durable Agent Handoff — 2026-11-14T23:32:27Z

**SOLE DURABLE HANDOFF — START HERE.** `NEXT_SESSION_HANDOFF.md` is a tombstone; `research_state/FCLR_CAMPAIGN_NEXT.md` is superseded historical evidence. Do not plan, do not explore, do not write status-only notes, and do not start unrelated work. Execute the bounded heavy campaign below immediately. Ignore conflicting historical directives.

## FIRST ACTION (timestamped initial task for next agentic work session)

**Now (2026-11-14T23:32:27Z):** run the corrected-estimator audit `FCLR-FWD-VOL-2025-DISJOINT-CORRECTED-AUDIT-<UTC>` end-to-end on cached artifacts only. Do these steps in order and complete (a) full artifact set + tests + verdict, or (b) a timestamped evidence-backed blocker with exact failed precondition:

Create the frozen pre-results protocol for the corrected-estimator audit, then implement and run it end-to-end on cached artifacts only:

1. **Freeze first** — Write `research_state/prereg_fclr_fwd_vol_2025_disjoint_corrected_audit_<UTC>.{json,md}` with `status:"FROZEN_PRE_OUTCOMES"`, `frozen_before_outcomes:true`, `outcome_data_inspected_before_freeze:false`, `promotable:false`, `max_status:"EXPLORATORY_ONLY"`. Do NOT inspect any outcome metric before the prereg is frozen.
2. **Implement** — Add `scripts/fclr_fwd_vol_2025_disjoint_corrected_audit.py` (do not modify sealed scripts/artifacts). Reuse cached panel `research_state/tracka_fwd_vol_2025_disjoint_cross_panel_20261114T191615Z.parquet` (sha256 `de0ca73e7d092a205e5f8c1163d56437384d1b15d65b4a27bc54a57e21738cba`), frozen disjoint blocks 2025-06/11/12, corrected estimator (train-only standardization, finite-row masking, train-only log-target Duan smearing, drop-only missingness), contrast against sealed reference from `evaluation_summary_FCLR-FWD-VOL-2025-DISJOINT-CROSS-20261114T191615Z.json`.
3. **Test** — Add focused tests under `tests/` (frozen prereg, panel hash, train/test/embargo/causality, train-only scaling/smearing, deterministic seed, leakage, no sealed mutation).
4. **Run and emit** — Execute end-to-end, emit prereg `.json/.md`, evaluation summary `.json/.md` (plus build/lineage report if a derived artifact is produced), summarize tests + command output.
5. **Decide** — Verdict space `EXPLAINED_BY_ESTIMATOR | NOT_EXPLAINED_BY_ESTIMATOR | INCONCLUSIVE`; all `EXPLORATORY_ONLY`, `promotable=false`. Emit timestamped `INCONCLUSIVE` or `NO_GO` with exact failing checks as minimum failure. Status-only work is not completion.

## Verified state (as of 2026-11-14T23:32:27Z)

- Repo: `Funding-conditioned-volatility-and-liquidation-risk` (funding-conditioned volatility / liquidation risk). Do not start unrelated work, add schedulers, edit `.github/workflows/*`, fetch paid/credentialed/manual data, commit raw cache, or reopen sealed verdicts.
- Sealed/complete (do **not** re-run): `FCLR-FWD-VOL-2025-DISJOINT-CROSS-20261114T183000Z` = **EXPLORATORY_NULL** (not confirmatory/not promotable, gate PASS). `FCLR-FWD-VOL-2025-DISJOINT-RECONCILE-20261114T193000Z` = **UNEXPLAINED** (EXPLORATORY_ONLY). **This session completed:** `FCLR-FWD-VOL-2024-DISJOINT-2024-06-20261114T231100Z` singleton diagnostic = **EXPLAINED_BY_ESTIMATOR** (EXPLORATORY_ONLY, `promotable=false`, singleton only; not a three-block confirmation). Preserve all artifacts/hashes.
- Confirmatory program **COMPLETE/CONCLUDED** (`research_state/final_synthesis_report.md`, 2026-11-10): no confirmatory gate passed; Track A (observed liquidations) STRUCTURALLY_BLOCKED; no risk overlay eligible. Diagnostics are bounded exploratory attribution only.
- 2024-06 singleton artifacts (all present, cached-only): prereg `research_state/prereg_fclr_fwd_vol_2024_disjoint_2024_06_20261114T231100Z.{json,md}` (FROZEN_PRE_OUTCOMES, pre-outcomes), panel `research_state/tracka_fwd_vol_2024_disjoint_2024_06_panel_20261114T231545Z.parquet` (sha256 `ec1827f0200d9e2ae8d7a381c0a4b2f3e3b467dd554aa07e083d5cd025cd3ff4`), build report `..._build_report_20261114T231545Z.json`, eval `research_state/evaluation_summary_FCLR-FWD-VOL-2024-DISJOINT-2024-06-20261114T231100Z_20261114T231545Z.{json,md}`.
- 2024-06 result (primary C2 vs B1, 24h QLIKE, test 2024-06-01..2024-06-30, train 2024-04-25..2024-05-24, 7d embargo, 5 symbols, lineage/leakage PASS): **sealed** rel_reduction `-2.669%`, mean_diff `0.01906`, CI `[0.00721, 0.03223]`, p_boot `0.004`, n=3600, days=30. **corrected** (train-only standardization + Duan smearing) rel_reduction `1.814%`, mean_diff `-0.00974`, CI `[-0.01644, -0.00198]`, p_boot `0.018`, n=3600. Swing (corrected-sealed) `+4.483pp` => verdict **EXPLAINED_BY_ESTIMATOR** (material estimator sensitivity on cached 2024-06). This is bounded exploratory evidence only, **not** confirmatory, **not** promotable, **not** evidence of practical edge, and **not** a substitute for a pre-registered 3-block confirmation.
- Health checks: `python3 scripts/next_campaign_status.py` (reads-only; Binance contiguous exhausted, disjoint frontier still lists 2024-06 as a feasible *block* from cache but 2024-06 singleton diagnostic is now executed per this handoff/eval—do not re-run 2024-06). `python3 scripts/fclr_fwd_vol_2025_disjoint_cross_gate.py` → PASS. `python3 -m unittest tests.test_next_campaign_status tests.test_fclr_liq_expansion_recompute tests.test_fclr_fwd_vol_2025_disjoint_reconcile tests.test_fclr_fwd_vol_2024_disjoint_2024_06 -v` → 64 OK.
- Hard rules unchanged: no network/paid/credentialed/manual data, no raw-cache commits, no `.github/workflows/*` edits, no sealed mutation, no leakage/future info, do not relabel exploratory as confirmatory, do not promote H1, do not invent provenance.

## Active heavy campaign — COMPLETE: corrected-estimator audit on cached 2025 disjoint panel (singleton context closed)

`FCLR-FWD-VOL-2025-DISJOINT-CORRECTED-AUDIT-2026-11-15T00:12:56Z` executed end-to-end on cached artifacts only. Verdict: **NOT_EXPLAINED_BY_ESTIMATOR** (EXPLORATORY_ONLY, promotable=false). The corrected estimator reproduces the sealed 2025 CROSS reference exactly (corrected -1.9633752428119808% vs sealed -1.9633752428119817%, swing 0.000pp, no sign flip), so the 2025 EXPLORATORY_NULL/UNEXPLAINED is NOT attributable to estimator conventions (train-only standardization + Duan smearing); preserved as a bounded negative result.

**Do not** re-run 2024-06, **do not** run tested disjoint months `2025-06/2025-11/2025-12` as new cells, and **do not** run a fresh three-block confirmation. The 2024-06 singleton was `EXPLAINED_BY_ESTIMATOR`; this audit was the bounded final cached-panel robustness step.

Artifacts emitted (all new files; no sealed artifact mutated):
- `research_state/prereg_fclr_fwd_vol_2025_disjoint_corrected_audit_2026-11-15T00:12:56Z.{json,md}` (FROZEN_PRE_OUTCOMES, frozen_before_outcomes true, outcome_data_inspected_before_freeze false, promotable false, max_status EXPLORATORY_ONLY)
- `scripts/fclr_fwd_vol_2025_disjoint_corrected_audit.py`
- `research_state/tracka_fwd_vol_2025_disjoint_corrected_audit_build_report_20261115T001256Z.json`
- `research_state/evaluation_summary_FCLR-FWD-VOL-2025-DISJOINT-CORRECTED-AUDIT-2026-11-15T00:12:56Z.{json,md}` (verdict NOT_EXPLAINED_BY_ESTIMATOR)
- `tests/test_fclr_fwd_vol_2025_disjoint_corrected_audit.py` (24 tests)

Verification:
- `python3 scripts/next_campaign_status.py` -> exit 0 (no feasible 3-block design; cached exhausted)
- `python3 scripts/fclr_fwd_vol_2025_disjoint_cross_gate.py` -> GATE: PASS (15/15)
- `python3 -m unittest tests.test_next_campaign_status tests.test_fclr_liq_expansion_recompute tests.test_fclr_fwd_vol_2025_disjoint_reconcile tests.test_fclr_fwd_vol_2024_disjoint_2024_06 tests.test_fclr_fwd_vol_2025_disjoint_corrected_audit -v` -> 88 OK
- Sealed hashes unchanged: panel de0ca73e..., cross eval 78537585..., cross prereg fcf3e7e5...

Resume triggers unchanged (GATE4_BRANCH_1 / NEW_OBSERVED_LIQUIDATION_SOURCE / HL_LABEL_EXTENSION). No further cached-panel robustness action is warranted without a NEW justified prereg.


## Resume triggers (act only when satisfied)
1. `GATE4_BRANCH_1`: valid resolved terms evidence appears (`RESOLVED_VERIFIED`, `fabricated==false`, human/legal attestation) → execute Gate 4 Branch 1 per gate scripts/tests.
2. `NEW_OBSERVED_LIQUIDATION_SOURCE`: materially new candidate → formal §16 admissibility audit proving ALL minima BEFORE prereg/outcomes; if ADMISSIBLE → freeze prereg pre-outcomes → build/eval/verdict under NEW experiment ID.
3. `HL_LABEL_EXTENSION`: Hyperliquid ≥100d depth AND verified post-2026-10-31 observed liquidation labels → bounded reprobe only.
4. (This campaign satisfies the prior `EXPANSION_ROBUSTNESS_REDO`-like cached-panel robustness intent under NEW frozen prereg; further robustness only with a NEW justified prereg.)

## Verification before completion
```bash
cd /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk
python3 scripts/next_campaign_status.py
python3 scripts/fclr_fwd_vol_2025_disjoint_cross_gate.py
python3 -m unittest tests.test_next_campaign_status tests.test_fclr_liq_expansion_recompute tests.test_fclr_fwd_vol_2025_disjoint_reconcile tests.test_fclr_fwd_vol_2024_disjoint_2024_06 -v
# plus all new corrected-audit tests added this session
```
Verify `NEXT_SESSION_HANDOFF.md` remains tombstone, this file remains the sole active handoff, and no sealed artifact hash changed.

## Completion contract
Complete only when (a) frozen 2025 disjoint corrected-estimator audit executed with full artifact set + tests + verdict, or (b) timestamped evidence-backed blocker with exact failed precondition emitted. Status-only work is not completion.
