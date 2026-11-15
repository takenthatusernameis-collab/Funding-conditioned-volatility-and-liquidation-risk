# Durable Agent Handoff — 2026-11-15T00:16:16Z

**SOLE DURABLE HANDOFF — START HERE.** `NEXT_SESSION_HANDOFF.md` is a tombstone; `research_state/FCLR_CAMPAIGN_NEXT.md` is superseded historical evidence. Do not plan, do not explore, do not write status-only notes, and do not start unrelated work. Execute the bounded heavy campaign below immediately. Ignore conflicting historical directives.

## FIRST ACTION (timestamped initial task for next agentic work session)

**Now (2026-11-15T00:16:16Z):** execute the `NEW_OBSERVED_LIQUIDATION_SOURCE` resume trigger — probe new admissible unauthenticated data sources per `research_state/next_data_discovery_plan.md` (FCLR-NEXT-001) to unblock Track A / reopen the confirmatory program. Do these steps in order and complete (a) a GO source with pre-registered experiment + frozen protocol + evaluation artifact + verdict, or (b) a timestamped evidence-backed structural blocker with exact failed precondition for every exhausted route:

1. **Probe** — Execute the candidate source families in `research_state/next_data_discovery_plan.md` §5, each a materially distinct source family/method per RESEARCH_PROMPT.md §16:
   - Alternative Binance paths (liquidations/, liquidationHistory/, forceLiquidation/)
   - Bybit public archive locations (linear/liquidation/, trading/liquidation/)
   - OKX public archives/static CDN
   - Deribit historical data
   - Academic repos (Zenodo, OSF, arXiv supplements)
   - GitHub raw content search (CSV/Parquet liquidation/mark data)
   - Hugging Face datasets search (unauthenticated GET)
   - CryptoDataDownload products
   Do NOT re-probe families already NO-GO in `research_state/track_a_deadend_map.md` without materially new evidence.

2. **Validate** — For each candidate, confirm the GO checklist (§25 of next_data_discovery_plan.md): unauthenticated download (HTTP 200, no key/account), schema inspected, coverage ≥5 symbols AND ≥3 non-overlapping 30-day blocks, completeness characterized (census vs sample), license/terms acceptable, integration path with existing pipeline, no sealed-holdout reuse. Record every probe outcome in `research_state/liquidation_source_campaign.md` and `research_state/liquidation_sources_enumeration.md`.

3. **Resolve the Track A alignment precondition** — `research_state/data_source_registry.json` marks `hyperliquid_alignment_context` PENDING (candidate `scripts/hyperliquid_funding_fetch.py`, api.hyperliquid.xyz/info fundingHistory POST, untested for history depth/schema). Prove admissible provenance+coverage (2025-06..2026-10 mark/index/premium/klines + funding) or document a timestamped blocker in `research_state/tracka_hl_alignment_blocker.md`. Do not fabricate.

4. **Decide** — If a source meets GO criteria: allocate a NEW experiment ID (e.g. FCLR-NEXT-002), freeze a preregistration pre-outcomes (status: FROZEN_PRE_OUTCOMES, frozen_before_outcomes:true, promotable:false, max_status:EXPLORATORY_ONLY), build/eval/verdict under the new experiment ID, all artifacts emitted. If all routes exhausted: emit a timestamped structural blocker with exact failed precondition per route, update the dead-end map, and stop cleanly (no status-only completion).

## Verified state (as of 2026-11-15T00:16:16Z)

- Repo: `Funding-conditioned-volatility-and-liquidation-risk` (funding-conditioned volatility / liquidation risk). Do not start unrelated work, add schedulers, edit `.github/workflows/*`, fetch paid/credentialed/manual data, commit raw cache, or reopen sealed verdicts.
- Active heavy campaign **COMPLETE**: corrected-estimator audit on cached 2025 disjoint panel (`FCLR-FWD-VOL-2025-DISJOINT-CORRECTED-AUDIT-2026-11-15T00:12:56Z`) executed end-to-end on cached artifacts only. Verdict: **NOT_EXPLAINED_BY_ESTIMATOR** (EXPLORATORY_ONLY, promotable=false). Corrected estimator reproduces sealed 2025 CROSS reference exactly (swing 0.000pp, no sign flip); 2025 EXPLORATORY_NULL/UNEXPLAINED NOT attributable to estimator conventions. Preserved as bounded negative result.
- Sealed/complete (do **not** re-run): `FCLR-FWD-VOL-2025-DISJOINT-CROSS-20261114T183000Z` = EXPLORATORY_NULL (gate PASS). `FCLR-FWD-VOL-2025-DISJOINT-RECONCILE-20261114T193000Z` = UNEXPLAINED (EXPLORATORY_ONLY). `FCLR-FWD-VOL-2024-DISJOINT-2024-06-20261114T231100Z` singleton = EXPLAINED_BY_ESTIMATOR (EXPLORATORY_ONLY, promotable=false, singleton only; not a three-block confirmation). Preserve all artifacts/hashes.
- Confirmatory program **COMPLETE/CONCLUDED** (`research_state/final_synthesis_report.md`, 2026-11-10): no confirmatory gate passed; Track A (observed liquidations) STRUCTURALLY_BLOCKED; no risk overlay eligible. Diagnostics are bounded exploratory attribution only. H001 NOT_SUPPORTED across every claim-worthy panel executed.
- Health checks (last run): `python3 scripts/next_campaign_status.py` → exit 0 (no feasible 3-block design in Binance domain; Hyperliquid bulk frontier regions tested/exhausted). `python3 scripts/fclr_fwd_vol_2025_disjoint_cross_gate.py` → GATE: PASS (15/15). `python3 -m unittest ... -v` → 88 OK. Sealed hashes unchanged (panel de0ca73e..., cross eval 78537585..., cross prereg fcf3e7e5...).
- Artifacts emitted this session (all new; no sealed artifact mutated): `research_state/prereg_fclr_fwd_vol_2025_disjoint_corrected_audit_2026-11-15T00:12:56Z.{json,md}`, `scripts/fclr_fwd_vol_2025_disjoint_corrected_audit.py`, `research_state/tracka_fwd_vol_2025_disjoint_corrected_audit_build_report_20261115T001256Z.json`, `research_state/evaluation_summary_FCLR-FWD-VOL-2025-DISJOINT-CORRECTED-AUDIT-2026-11-15T00:12:56Z.{json,md}`, `tests/test_fclr_fwd_vol_2025_disjoint_corrected_audit.py` (24 tests).

## Resume triggers (act only when satisfied)

1. `GATE4_BRANCH_1`: valid resolved terms evidence (`RESOLVED_VERIFIED`, `fabricated==false`, human/legal attestation) → execute Gate 4 Branch 1 per gate scripts/tests. (Not agent-settable; requires external/legal evidence.)
2. `NEW_OBSERVED_LIQUIDATION_SOURCE`: materially new candidate → formal §16 admissibility audit proving ALL minima BEFORE prereg/outcomes; if ADMISSIBLE → freeze prereg pre-outcomes → build/eval/verdict under NEW experiment ID. **(THIS SESSION'S FOCUS — execute now.)**
3. `HL_LABEL_EXTENSION`: Hyperliquid ≥100d depth AND verified post-2026-10-31 observed liquidation labels → bounded reprobe only. (Time-gated: only ~15 days post-2026-10-31 available as of 2026-11-15; not yet satisfiable to 100d depth.)
4. `EXPANSION_ROBUSTNESS_REDO`: newly preregistered design meeting §17 promotion conditions (conditional, non-priority).

## Bottlenecks removed / no longer blocking

- Cached Binance 5-symbol panel exhausted → no re-proposal of disjoint months 2024-06, 2025-06/11/12; no fresh three-block confirmation on cache. (Removed by completed audit.)
- Track A dead-end map complete → all candidate families probed with evidence; sole reopen path is a NEW admissible unauthenticated source meeting the rubric (≥5 symbols, ≥3 blocks, documented completeness, license OK, census-or-defensible). (Next session executes this path.)
- No status-only completion: every session must end with a verdict artifact, evaluation artifact, or timestamped evidence-backed blocker.

## Verification before completion

```bash
cd /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk
python3 scripts/next_campaign_status.py
python3 scripts/fclr_fwd_vol_2025_disjoint_cross_gate.py
python3 -m unittest tests.test_next_campaign_status tests.test_fclr_liq_expansion_recompute tests.test_fclr_fwd_vol_2025_disjoint_reconcile tests.test_fclr_fwd_vol_2024_disjoint_2024_06 tests.test_fclr_fwd_vol_2025_disjoint_corrected_audit -v
```
Verify `NEXT_SESSION_HANDOFF.md` remains tombstone, this file remains the sole active handoff, and no sealed artifact hash changed.

## Completion contract

Complete only when (a) a NEW admissible unauthenticated liquidation source passes the §16 admissibility audit with a frozen pre-outcomes prereg, full artifact set, tests, and verdict under a NEW experiment ID, or (b) a timestamped evidence-backed structural blocker with exact failed precondition for every exhausted route is emitted and the session stops cleanly. Status-only work is not completion.
