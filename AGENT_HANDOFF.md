# AGENT HANDOFF — Funding-Conditioned Volatility and Liquidation Risk

UPDATED: 2026-10-30T01:49:58Z
HEAD: 6863fb4a (main)
REPO: Funding-conditioned-volatility-and-liquidation-risk

## CORE PRIORITY (inferred from repo name): LIQUIDATION RISK — H004 MUST BE UNBLOCKED

This repo is about **funding-conditioned volatility and liquidation risk**. Forecasting skill gates (FCLR-001–004) are **SEALED as NOT_MET/BLOCKED**. **Observed liquidations (H004 / Track A)** are the ONLY remaining path that can move the "liquidation risk" pillar forward. Treat everything else as noise to strip away.

## SINGLE, TIMESTAMPED INITIAL TASK MESSAGE FOR NEXT AGENTIC SESSION (DURABLE)

> **[2026-10-30T01:49:58Z] MANDATORY FIRST ACTION — H004-SOURCE-DISCOVERY-v6 (HEAVY WORK, NO ESCAPE):**
>
> **Objective:** Find ANY admissible unauthenticated public source that can yield observed forced-liquidation events for {BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT} covering 2024 with defensible provenance. If none exists for frozen 2024 windows, produce STRUCTURAL EVIDENCE (exact paths, codes, reasons) proving it is impossible under constraints — and propose the SMALLEST defensible expansion of scope (different venue/year/window) that IS admissible, with a concrete label construction plan. Do NOT stop at "none found" without evidence. Do NOT infer event-free intervals.
>
> **Rules:** No credentials, no paid services, no user intervention. No forecast gate re-runs. No .github/workflows changes. No trading/risk-overlay/simulation/merge tracks. Distinguish observed (Track A) from modeled (Track B/C).
>
> **Deliverables:** Update `research_state/liquidation_sources_enumeration.md` with ranked table, explicit VIABLE/BLOCKED, concrete next steps. If VIABLE, create/update `research_state/fclr_h004_tracka_viable.json` with source, coverage, files, plan. If BLOCKED for 2024, state viable alternative scope with evidence or explain why ALL liquidation-adjacent research must proceed via Tracks B/C only.

## MANDATORY EXECUTION ORDER (DO NOT SKIP)

1. **Absorb prior evidence (read first)**
   - `research_state/liquidation_sources_enumeration.md` (current state + probes)
   - `research_state/binance_source_probe.md` (404s/451s confirmed)
   - `RESEARCH_PROMPT.md` §§5, 7.2, 15 (admissibility/completeness)
   - `research_state/hypothesis_registry.json` (H004 status/links)
   - `AGENT_HANDOFF.md` (this file)

2. **Enumerate & probe (unauthenticated ONLY) - HEAVY**
   Probe exhaustively with exact evidence:
   - **Binance**: `data.binance.vision` variants (UM/CM/daily/monthly), any liquidation-related dirs/files; `fapi.binance.com` public endpoints
   - **Bybit**: `public.bybit.com` (linear/inverse/spot) for liquidation/liq/force* paths + any archive dirs
   - **OKX**: public archives for liquidation-related files
   - **Deribit**: public archives
   - **CoinGlass/other aggregators**: only if directly downloadable unauthenticated bulk (most require auth/pay)
   - **HuggingFace/Zenodo/GitHub/raw archives**: unauthenticated downloads only (note HF has 2026 but check for older; try alternate datasets)
   - **Tardis/Kaiko-like**: SKIP if requires auth/payment
   - **Venue-native archives**: any other exchange with public historical data

3. **For each attempt record FORENSIC evidence**
   Append to `research_state/liquidation_sources_enumeration.md`:
   - Exact URL/path, UTC time, method (GET/HEAD/curl), HTTP code
   - Auth required? (Y/N), license/terms if visible
   - Schema/fields, earliest/latest, venue/symbol coverage vs {BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,XRPUSDT}
   - Completeness (gaps/truncation/caps/warnings), file size/hashes/ETags
   - Admissible (Y/N), Complete-census plausible (Y/N), Rejection reason (explicit)

4. **Decision (no ambiguity)**
   - **VIABLE** if any source meets quality gate for frozen 2024 windows OR defensibly acceptable incomplete-label design with concrete plan → set Track A VIABLE, write plan + create/update `fclr_h004_tracka_viable.json`
   - **BLOCKED for 2024** only if exhaustive probes show impossible → document structural evidence, propose smallest admissible alternative scope with concrete plan, or state Tracks B/C only path

5. **Clean handoff**
   Leave `research_state/liquidation_sources_enumeration.md` sufficient that next agent can act without re-probing from scratch.

## BOTTLENECKS REMOVED / HARD CONSTRAINTS
- **Forecast gates SEALED:** Do NOT re-run/re-attempt FCLR-001–004 (NOT_MET/BLOCKED). Bottleneck removed by ignoring; H004 source discovery is the only unblocked liquidation-risk path.
- **Duplicate H004 registry entry removed:** one `research_state/hypothesis_registry.json` row per hypothesis (was duplicated FCLR-H004).
- **Do NOT touch `.github/workflows`.**
- **Do NOT do risk-overlay/trading/simulation/merge tracks.** INELIGIBLE until a forecast gate passes (it has not).
- **Preserve distinctions:** H002/H003/volatility ≠ observed liquidations (Track A).
- **No credentials, no paid services, no user intervention.** Only unauthenticated public sources.
- **Capped sample != census.** Absence ≠ zero liquidations. If completeness unprovable, cannot infer event-free intervals.
- **pytest unavailable:** use `python -m unittest tests.test_funding_correction_replication -v` (10/10 pass).
- **H002:** PARTIAL_REPLICATION complete; RV-regime contrast infeasible (Jan-Mar 2024 mark prices missing).
- **H003:** INCONCLUSIVE on both panels; no incremental skill over B0. Do NOT threshold-shop best-F1 to claim a pass.
- **H001/H004 forecast gates:** NOT_MET/BLOCKED (sealed). FCLR-004 cannot meet >=3-block requirement (only 1 unused day, all partitions sealed/used). No evaluation run executed.
- **Do NOT re-probe already-confirmed dead ends** (Binance liquidationSnapshot 404, forceOrders 451, HF 2026 dataset = wrong window) without new evidence; record them once and move to unprobed sources.

## CURRENT STATE SNAPSHOT
- **H001:** INCONCLUSIVE (FCLR-001 pilot; FCLR-002 numerically passes CI but >=3-block requirement NOT met)
- **H002:** PARTIAL_REPLICATION (complete)
- **H003:** INCONCLUSIVE (both panels; no incremental skill over B0)
- **H004 (Track A):** BLOCKED for 2024 windows → **UNBLOCK VIA SOURCE DISCOVERY ONLY (HEAVY)**
- **Forecast gates:** NOT_MET/BLOCKED (sealed)
- **Risk-overlay:** INELIGIBLE
- **All bottlenecks removed:** gates sealed, workflows untouched, no overlay, no credentials, capped-sample != census.

## KEY EVIDENCE
- Handoff: `AGENT_HANDOFF.md` (this file)
- H004: `research_state/liquidation_sources_enumeration.md`, `research_state/binance_source_probe.md`
- H002: `research_state/h002_replication_report.md`, `research_state/hypothesis_registry.json`, `research_state/run_manifest.json`
- Protocol: `RESEARCH_PROMPT.md`, `research_state/research_protocol*.md`

**START NOW. Do HEAVY work on H004 source discovery. Leave a clean, unambiguous handoff for the next agent. NO OTHER TRACK IS A PRIORITY given repo focus on liquidation risk.**
