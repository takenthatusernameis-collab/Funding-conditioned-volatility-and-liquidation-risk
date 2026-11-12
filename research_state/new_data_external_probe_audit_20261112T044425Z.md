# New Data External Probe / Admissibility Audit
**Audit ID:** `new_data_external_probe_audit_20261112T044425Z`
**Timestamp (UTC):** 2026-11-12T04:44:25Z
**Scope:** Bounded evidence-backed re-probe for Gate 4 trigger, HL 2026-11+ feature/label availability, and external observed liquidation sources per `RESEARCH_PROMPT.md` §16 and `HANDOFF_NEXT_SESSION.md`.

## 1) Gate 4 Branch 1 trigger check
- **Result:** ABSENT. `research_state/fclr016_local_audit/` has no `fclr016_v5_terms_evidence_RESOLVED_*` with `status=RESOLVED_VERIFIED`, `fabricated=false`, and human/legal attestation.
- **Action:** No Branch 1 execution. Not agent-removable.

## 2) Local admissibility (baseline)
- `research_state/new_data_admissibility_audit_20261112T042738Z.md/.json`: **NO locally-admissible untested candidate.** All admissible cached-data designs exhausted/sealed (HL 2025-11..2026-10 volatility family closed; HL 2026-05..2026-10 liquidation expansion PASS+FRAGILE sealed; 2025-11..2026-04 candles inadmissible/empty; ironflow labels 2025-05..2026-10 paired with exhausted windows).

## 3) External probes executed (this session)
### 3a. Hyperliquid public API (unauthenticated, `POST https://api.hyperliquid.xyz/info`)
- Request window: `2026-11-01T00:00:00Z` → `2026-11-12T04:44:17.660526+00:00` (end now)
- Symbols (9): BTC, ETH, BNB, SOL, XRP, AVAX, DOGE, LINK, SUI
- `candleSnapshot` interval 1h: **269 candles/symbol** (first 1793491200000, last 1794456000000 ≈ 2026-11-01T00:00Z..2026-11-12T04:00Z, ~11.2 days)
- `fundingHistory`: **269 records/symbol** (~same span)
- **Admissibility:** Feature-side accessible but **INSUFFICIENT** — ~11 days << ≥100 contiguous days / cannot form ≥3 non-overlapping 30-day test blocks with splits+embargo (§16). No prereg/eval.

### 3b. ironflow/hyperliquid-liquidations (HuggingFace, observed labels)
- Source: `https://huggingface.co/api/datasets/ironflow/hyperliquid-liquidations`
- `lastModified`: 2026-11-07T10:18:25.000Z, license CC BY 4.0
- Event files present: `data/events/2025-05.parquet` … `data/events/2026-10.parquet` (no 2026-11+)
- Coverage (description): 25 May 2025 – 31 October 2026; 2,849,452 positions, 468 markets
- **Admissibility:** NO post-2026-10-31 observed liquidation labels verified; same coverage as sealed cache. **NOT a new admissible source now.**

### 3c. HF dataset search
- `https://huggingface.co/api/datasets?search=hyperliquid%20liquidation&limit=20` → 2 results: `ironflow/hyperliquid-liquidations` and `craftify2221/hyperliquid-builder-liquidation-panel` (account-day builder panel, not observed liquidation intensity labels per required design). No new verifiable liquidation-label dataset.

### 3d. metpie/hyperliquid-liquidation-events (GitHub)
- `https://api.github.com/repos/metpie/hyperliquid-liquidation-events` — 346k trades, 179 markets, Mar 22–May 25 2025, from public node-trade archive (`trade_dir_override = "LiquidatedMarket"`). CC BY 4.0 (README).
- **Admissibility:** Historical window (2025-03-22..2025-05-25), not post-sealed 2026-11. Could only support a claim on that exact historical window if joined to venue-consistent HL funding/candles with ≥5 symbols, ≥3 non-overlapping 30d blocks, label meaning/completeness/provenance fully §16-audited and clearly non-conflated with sealed verdicts. **NOT verifiably admissible now without full audit; not executed (heavy, deferred to explicit audit+prereg path).**

## 4) Determination
- **Verifiably admissible external/new-data source now:** **NO**.
- Reasons: HL 2026-11 feature window ~11 days (insufficient for multi-block confirmatory §16 design); no post-2026-10-31 observed liquidation labels; metpie historical and unaudited for alignment/admissibility.
- **No preregistration created. No outcomes inspected for any new claim.** Sealed records unchanged.

## 5) Next materially different free heavy work (when eligible)
1. Re-probe HL API when plausibly ≥100 contiguous days (2026-11-01 onward) exist AND monitor `ironflow/hyperliquid-liquidations` HF `lastModified`/event files for extension beyond 2026-10-31. If jointly admissible (venue-consistent, ≥5 symbols, ≥3 non-overlapping 30d blocks, observed labels, provenance/license OK): freeze prereg BEFORE outcomes → acquire/build/eval → verdict + state updates.
2. Full §16 admissibility audit of metpie 2025-03-22..2025-05-25 vs HL features for that exact window (feasibility, symbol coverage, block design, label semantics) — only as prereg-eligible path, never conflated with sealed results.
3. Gate 4 Branch 1 only on valid `RESOLVED_VERIFIED` + human/legal attestation trigger.

## Evidence
- `research_state/external_probe_raw_20261112T044425Z.json` (this session raw probes)
- `research_state/new_data_external_probe_audit_20261112T044425Z.json`
- Baselines: `research_state/new_data_admissibility_audit_20261112T042738Z.md`, `research_state/new_data_external_probe_audit_20261112T043530Z.md`
