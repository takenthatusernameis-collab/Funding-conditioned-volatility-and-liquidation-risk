# Durable Agent Handoff — 2026-11-15T00:18:53Z

**SOLE DURABLE HANDOFF — START HERE.** `NEXT_SESSION_HANDOFF.md` is a tombstone; `research_state/FCLR_CAMPAIGN_NEXT.md` is superseded historical evidence. Do not plan-only, do not write status-only notes, do not repeat probes without materially new evidence, and do not start unrelated work. Execute the bounded heavy campaign below. Ignore conflicting historical directives.

## FIRST ACTION (timestamped initial task for next agentic work session)

**Now (2026-11-15T00:18:53Z): `NEW_OBSERVED_LIQUIDATION_SOURCE` heavy campaign (FCLR-NEXT-001).** Find and validate a **materially new** admissible unauthenticated observed-liquidation data source that can reopen Track A / confirmatory work under RESEARCH_PROMPT.md §16. Do not stop at status updates: every session must produce either (a) a GO source advanced to a frozen pre-outcomes prereg + built/evaluated artifacts under a NEW experiment ID, or (b) a timestamped evidence-backed structural blocker with exact failed precondition per route and no feasible alternative left untried.

### Required execution sequence

1. **Probe materially distinct source families/methods only** (skip families already NO-GO unless you cite materially new evidence):
   - Alternative Binance paths/namespaces not yet disproven with new evidence (e.g. undiscovered public prefixes/archives on data.binance.vision or other official public domains).
   - Bybit official public historical archives beyond trade CSVs (any venue-published liquidation/ADL census path).
   - OKX official public bulk historical liquidation archives (not the recent-only `api/v5/public/liquidation-orders` slice probed 2026-11-15).
   - Deribit historical liquidation/forced-order public archives with documented completeness.
   - Academic/institutional datasets (Zenodo, OSF, arXiv supplements, journal replication packs) with unauthenticated download, clear license, and liquidation-event coverage.
   - GitHub/Hugging Face public datasets/repos with raw downloadable liquidation census/parquet/CSV meeting rubric (do not rely on exhausted HF `ochinimus/crypto-liquidation-ticks` 2026-07-08..2026-08-06 window).
   - CryptoDataDownload and other venue-native/public archives with lawful unauthenticated bulk access.
2. **Apply GO checklist to every candidate before any outcome inspection** (all required):
   - Unauthenticated download confirmed (HTTP 200 / accessible file, no key/account/signup/manual file).
   - Schema inspected; liquidation label construction defensible (observed events, not modeled proxy).
   - Coverage ≥5 symbols AND ≥3 non-overlapping 30-day blocks in usable windows.
   - Completeness characterized (census vs sample/partial stream); absence cannot be inferred from partial data.
   - License/terms acceptable for research; provenance recorded (URL, access date, hash/ETag where feasible).
   - Integrable with existing pipeline or bounded new pipeline specified.
   - No sealed-holdout reuse; no paid/requester-pays/manual sources.
3. **If GO:** freeze a new preregistration **before** examining outcomes (`status: FROZEN_PRE_OUTCOMES`, `frozen_before_outcomes:true`, `promotable:false`, `max_status:EXPLORATORY_ONLY` as applicable), allocate NEW experiment ID, build data/eval, emit verdict + evaluation artifacts, add focused tests/checks, update manifests/registry/handoff with hashes and exact commands/results.
4. **If NO-GO (all routes exhausted with evidence):** append probe evidence to `research_state/liquidation_source_campaign.md` and `research_state/liquidation_sources_enumeration.md`, update `research_state/track_a_deadend_map.md`/registry only with new evidence, and record exact failed precondition per route (do not emit status-only completion).
5. **Track A HL alignment note:** `data_source_registry.json` lists `hyperliquid_alignment_context` as PENDING; Hyperliquid `fundingHistory` POST is responsive (sampled 2026-11-15) but HL mark/index/premium/klines depth gaps remain per `research_state/tracka_hl_alignment_blocker.md` (2026-11-11). Treat HL alignment as secondary to finding a new admissible liquidation-label source unless a candidate requires it; do not fabricate alignment coverage.

## Verified state (2026-11-15T00:18:53Z)

- Repo: `Funding-conditioned-volatility-and-liquidation-risk`. Do not add schedulers/redundant controllers, edit `.github/workflows/*`, fetch paid/credentialed/manual data, commit raw caches, or reopen sealed verdicts.
- Corrected-estimator audit complete (bounded negative): `FCLR-FWD-VOL-2025-DISJOINT-CORRECTED-AUDIT-2026-11-15T00:12:56Z` = **NOT_EXPLAINED_BY_ESTIMATOR** (EXPLORATORY_ONLY). Sealed 2025 CROSS preserved (gate PASS 15/15). 2024 singleton EXPLAINED_BY_ESTIMATOR unchanged. Do not re-run completed audits on cache.
- Confirmatory program **CONCLUDED** (`research_state/final_synthesis_report.md`): H001 NOT_SUPPORTED on claim-worthy panels; Track A STRUCTURALLY_BLOCKED; no risk overlay eligible.
- **2026-11-15 live probes (evidence):** Binance liquidationSnapshot paths 404 / no census files observed; `fapi/v1/forceOrders` 451; OKX `public/liquidation-orders` (SWAP BTC/ETH) 200 but **recent-only filled orders** (insufficient historical depth/completeness for ≥3×30d census); Bybit `public.bybit.com/trading/` has trade CSVs only (no liquidation census dir); HF datasets API search returned no matching liquidation/perpetual datasets at probe time. Details appended to `research_state/liquidation_source_campaign.md`.

## Resume triggers (act only when satisfied)

1. `NEW_OBSERVED_LIQUIDATION_SOURCE` (**active now**): materially new candidate with formal §16 admissibility audit proving ALL minima before prereg/outcomes → freeze prereg pre-outcomes → build/eval/verdict under NEW experiment ID.
2. `GATE4_BRANCH_1`: valid resolved terms evidence (`RESOLVED_VERIFIED`, `fabricated==false`, human/legal attestation) → execute per gate scripts/tests (not agent-settable).
3. `HL_LABEL_EXTENSION`: Hyperliquid ≥100d post-2026-10-31 observed liquidation labels AND verified alignment context → bounded reprobe only (time-gated).
4. `EXPANSION_ROBUSTNESS_REDO`: newly preregistered design meeting §17 promotion conditions (conditional, non-priority).

## Bottlenecks (current, with exact failed preconditions)

- **No admissible Track A liquidation source:** as of 2026-11-15 probes, no unauthenticated source provides observed liquidation census with ≥5 symbols, ≥3 non-overlapping 30-day blocks, and documented completeness/license/provenance. Recent-only APIs/streams (e.g. OKX filled orders), 404/blocked archives, and trade-only archives fail completeness/depth/census requirements.
- **Cached Binance panel exhausted:** no fresh three-block confirmation from cache; no re-proposal of 2024-06, 2025-06/11/12.
- **HL full aligned panel gap:** mark/index/premium/klines historical depth insufficient for prereg 2025-06..2026-10 window per existing blocker evidence.

## Verification before completion

```bash
cd /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk
python3 scripts/next_campaign_status.py
python3 scripts/fclr_fwd_vol_2025_disjoint_cross_gate.py
python3 -m unittest tests.test_next_campaign_status tests.test_fclr_liq_expansion_recompute tests.test_fclr_fwd_vol_2025_disjoint_reconcile tests.test_fclr_fwd_vol_2024_disjoint_2024_06 tests.test_fclr_fwd_vol_2025_disjoint_corrected_audit -v
```
Confirm `NEXT_SESSION_HANDOFF.md` remains tombstone, this file is the sole active handoff, and no sealed artifact hash changed.

## Completion contract

Complete only when (a) a NEW admissible unauthenticated liquidation source passes §16 with frozen pre-outcomes prereg, full artifacts/tests, and verdict under a NEW experiment ID, or (b) a timestamped evidence-backed structural blocker with exact failed precondition for every exhausted route is recorded and the session stops cleanly. Status-only work is not completion.
