# AGENT HANDOFF — Funding-Conditioned Volatility and Liquidation Risk

UPDATED: 2026-10-29T23:51:30Z
HEAD: c3236af1 (main)
REPO: Funding-conditioned-volatility-and-liquidation-risk

## CORE PRIORITY (inferred from repo name): LIQUIDATION RISK — H004 MUST BE UNBLOCKED

This repo is about **funding-conditioned volatility and liquidation risk**. Forecasting skill (FCLR-001–004) is SEALED as NOT_MET/BLOCKED. **Observed liquidations (H004 / Track A)** are the ONLY remaining path that can move the "liquidation risk" pillar forward. Everything else that would spin on forecast gates is a bottleneck to remove — do NOT re-attempt them.

## SINGLE, TIMESTAMPED INITIAL TASK MESSAGE FOR NEXT AGENTIC SESSION

> **[2026-10-29T23:51:30Z] INITIAL MANDATORY TASK: H004-SOURCE-DISCOVERY-v3 — Find an admissible unauthenticated public source of complete (or defensibly partial with explicit incomplete-label design) historical forced-liquidation events for {BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT} covering 2024 to construct observed liquidation labels for the frozen test windows. Do HEAVY work: enumerate, probe with exact evidence, make an explicit VIABLE/BLOCKED decision, and leave zero ambiguity. Do not re-run sealed forecast gates.**

## MANDATORY EXECUTION ORDER (DO NOT SKIP)

1. **Absorb prior evidence (read first)**
   - `research_state/liquidation_sources_enumeration.md` (current state + probes)
   - `research_state/binance_source_probe.md` (404s/451s confirmed)
   - `RESEARCH_PROMPT.md` §§5, 7.2, 15 (admissibility/completeness)
   - `research_state/hypothesis_registry.json` (H004 status/links)
   - `AGENT_HANDOFF.md` (this file)

2. **Enumerate admissible sources (unauthenticated ONLY)**
   Systematically probe:
   - **Binance**: `data.binance.vision` variants (UM/CM, daily/monthly, different dirs), also check any liquidation-related paths; note `fapi.binance.com/fapi/v1/forceOrders` returns 451 in this env.
   - **Bybit**: `public.bybit.com` — check `linear/`, `inverse/`, `spot/` for `liquidation/`, `liq/`, `forceLiquidation/` across years/months.
   - **OKX**: public archives for liquidation-related files
   - **Deribit**: public archives (less likely)
   - **HuggingFace/Zenodo/GitHub**: unauthenticated downloads only (note HF has 2026 liquidation ticks but NOT 2024)
   - **Other venue-native public archives**; academic mirrors only if directly downloadable without auth

3. **Probe with forensic evidence (record EVERYTHING)**
   For each candidate tried, append to `research_state/liquidation_sources_enumeration.md`:
   - Source URL/path attempted (exact)
   - Access time (UTC), method (GET/HEAD/curl), HTTP code
   - Auth required? (Y/N)
   - License/terms notes if visible
   - Schema/fields, earliest/latest timestamps
   - Venue/symbol coverage vs frozen universe {BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT}
   - Completeness indicators (gaps/truncation/caps/warnings)
   - File size/hashes/ETags if present
   - **Admissible (Y/N)** and **Complete-census plausible (Y/N)**
   - **Rejection reason** (explicit)

4. **Make explicit viability decision (no ambiguity)**
   - **If ANY source meets the direct-label quality gate** (defensible provenance, covers needed 2024 window for frozen universe, meaning of "observed forced liquidation" matches, complete census OR explicitly acceptable incomplete-label design per protocol):
     - Set **Track A = VIABLE**
     - Write/update `research_state/liquidation_sources_enumeration.md` with **concrete label construction plan** (source, coverage table, transformation steps, files to produce, minimal next steps)
     - If helpful create/update `research_state/fclr_h004_tracka_viable.json`
   - **If NONE pass:**
     - Set **Track A = BLOCKED for frozen 2024 windows** with **structural evidence** citing specific probed paths/codes
     - State **Tracks B/C remain the only liquidation-adjacent paths**
     - Do **NOT** infer event-free intervals; do **NOT** re-attempt forecast gates (FCLR-001–004 SEALED)

5. **Leave a clean handoff**
   Update `research_state/liquidation_sources_enumeration.md` with a clean **ranked table + decision + concrete next steps**. The repo state alone must be sufficient for the next agent.

## BOTTLENECKS REMOVED / HARD CONSTRAINTS

- **Forecast gates SEALED.** Do NOT re-run/re-attempt FCLR-001/FCLR-002/FCLR-003/FCLR-004 (NOT_MET/BLOCKED). Remove this bottleneck by ignoring them.
- **Do NOT touch `.github/workflows`.**
- **Do NOT do risk-overlay/trading/simulation/merge tracks.**
- **Preserve distinctions.** Never conflate H002 (correction-time), H003 (hypothetical boundary breaches), or volatility with observed liquidations (Track A).
- **No credentials, no paid services, no user intervention.** Only unauthenticated public sources.
- **Capped sample != census.** Absence ≠ zero liquidations. If completeness unprovable, cannot infer event-free intervals.
- **pytest unavailable:** use `python -m unittest tests.test_funding_correction_replication -v` (10/10 pass).
- **H002:** PARTIAL_REPLICATION complete; RV-regime contrast infeasible (Jan-Mar 2024 mark prices missing).

## CURRENT STATE SNAPSHOT

- **H001:** INCONCLUSIVE
- **H002:** PARTIAL_REPLICATION (complete)
- **H003:** INCONCLUSIVE
- **H004 (Track A):** BLOCKED → UNBLOCK VIA SOURCE DISCOVERY ONLY
- **Forecast gates:** NOT_MET/BLOCKED (sealed)
- **Risk-overlay:** INELIGIBLE

## KEY EVIDENCE

- Handoff: `AGENT_HANDOFF.md` (this file)
- H004: `research_state/liquidation_sources_enumeration.md`, `research_state/binance_source_probe.md`
- H002: `research_state/h002_replication_report.md`, `research_state/hypothesis_registry.json`, `research_state/run_manifest.json`
- Protocol: `RESEARCH_PROMPT.md`, `research_state/research_protocol*.md`

**START NOW. Do heavy work on H004 source discovery. Leave a clean, unambiguous handoff for the next agent. No other track is a priority given the repo focus on liquidation risk.**
