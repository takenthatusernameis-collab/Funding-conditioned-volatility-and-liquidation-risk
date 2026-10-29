# AGENT HANDOFF — Funding-Conditioned Volatility and Liquidation Risk

UPDATED: 2026-10-29T23:01:00Z
HEAD: c3236af1 (main)
REPO: Funding-conditioned-volatility-and-liquidation-risk

## PRIORITY (from repo name): Unblock liquidation-risk via observed labels (Track A)

Repo focus = **Funding-conditioned volatility and liquidation risk**. Forecast gates (FCLR-001–004) are SEALED as NOT_MET/BLOCKED. H002 is PARTIAL_REPLICATION. **H004 (observed liquidations) is the only remaining pillar that can move liquidation-risk forward — and it is BLOCKED pending source discovery.**

## SINGLE MANDATORY INITIAL TASK FOR NEXT AGENT (DO HEAVY WORK)

**Campaign:** `H004-SOURCE-DISCOVERY-v2`
**Goal:** Find any admissible unauthenticated public source of *complete* historical forced-liquidation event records (or a defensibly partial set with explicit incomplete-label design) for the frozen universe {BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT} covering 2024 (priority: match frozen test windows used by FCLR-001/002).

### MANDATORY EXECUTION ORDER

1. **Read prior evidence first**
   - `research_state/liquidation_sources_enumeration.md` (current state + known probes)
   - `research_state/binance_source_probe.md` (confirmed 404s / 451s)
   - `RESEARCH_PROMPT.md` §§5, 7.2, 15 (constraints on completeness / admissibility)
   - `research_state/hypothesis_registry.json` (H004 status/links)

2. **Systematically enumerate admissible sources** (unauthenticated only, no keys/login/payment)
   - Binance data.binance.vision variants (different paths/layouts/years), check CM vs UM, monthly/daily variants
   - Bybit public.bybit.com — look for liquidation-specific dirs/files beyond trades (e.g. `liquidation/`, `liq/`, `forceLiquidation/`)
   - OKX public data archives
   - Deribit public archives
   - HuggingFace/Zenodo/GitHub (unauthenticated) — search for 2024 liquidation event data
   - Other venue-native public archives; academic mirrors only if directly downloadable without auth

3. **Probe aggressively with evidence**
   For every candidate tried, record in `research_state/liquidation_sources_enumeration.md`:
   - Source URL/path attempted (exact)
   - Access time (UTC), method (GET/HEAD/curl), HTTP code
   - Auth required? (Y/N)
   - License/terms notes if visible
   - Schema/fields, earliest/latest timestamps
   - Venue/symbol coverage vs frozen universe
   - Completeness indicators (gaps/truncation/caps/warnings)
   - File size/hashes/ETags if present
   - **Admissible (Y/N)** and **Complete-census plausible (Y/N)**
   - **Rejection reason** (explicit)

4. **Make an explicit viability decision**
   - If ANY source meets the **direct-label quality gate** (defensible provenance, covers needed 2024 window for frozen universe, meaning of "observed forced liquidation" matches, and either complete census OR explicitly acceptable incomplete-label design per protocol):
     - Set **Track A = VIABLE**
     - Write/update `research_state/liquidation_sources_enumeration.md` with **concrete label construction plan** (how to build labels from that source, minimal next steps, files to produce)
     - If helpful, create `research_state/fclr_h004_tracka_viable.json` with source, coverage, plan
   - If NONE pass:
     - Set **Track A = BLOCKED for frozen 2024 windows** with **structural evidence** (cite specific probed paths/codes)
     - State **Tracks B/C remain the only liquidation-adjacent paths**
     - Do **NOT** infer event-free intervals; do **NOT** re-attempt forecast gates (FCLR-001–004 SEALED)

5. **Leave zero ambiguity for next agent**
   Update `research_state/liquidation_sources_enumeration.md` with a clean **ranked table + decision + concrete next steps**. The handoff should be self-sufficient from repo state alone.

## BOTTLENECKS REMOVED / HARD CONSTRAINTS

- **Forecast gate SEALED.** Do NOT re-run/re-attempt FCLR-001/FCLR-002/FCLR-003/FCLR-004. Status NOT_MET/BLOCKED.
- **Do NOT touch `.github/workflows`.**
- **Do NOT do risk-overlay/trading/simulation/merge tracks.**
- **Preserve distinctions.** Never conflate H002 (correction-time), H003 (hypothetical boundary breaches), or volatility with observed liquidations (Track A).
- **No credentials, no paid services, no user intervention.** Only unauthenticated public sources.
- **Capped sample != census.** Absence ≠ zero liquidations. If completeness unprovable, cannot infer event-free intervals.
- **pytest:** `pytest` unavailable; use `python -m unittest tests.test_funding_correction_replication -v` (10/10 pass).
- **H002:** PARTIAL_REPLICATION complete; RV-regime contrast infeasible (Jan-Mar 2024 mark prices missing).

## IMMEDIATE ACCEPTANCE CRITERIA

- [ ] `research_state/liquidation_sources_enumeration.md` updated with **ranked source table + concrete probes** (exact URLs/paths, codes, auth, coverage, completeness, rejection reasons)
- [ ] **Explicit Track A viability decision** recorded (VIABLE with minimal label-construction plan OR BLOCKED for frozen 2024 windows with structural evidence)
- [ ] If VIABLE: concrete files/steps to build labels without bulk-pulling outside admissible paths
- [ ] If BLOCKED: explicit statement that Tracks B/C remain only paths; no forecast-gate re-attempts
- [ ] No workflow changes, no forecast re-runs

## CURRENT STATE SNAPSHOT

- **H001:** INCONCLUSIVE
- **H002:** PARTIAL_REPLICATION (complete)
- **H003:** INCONCLUSIVE
- **H004:** BLOCKED → UNBLOCK VIA SOURCE DISCOVERY ONLY (this session)
- **Forecast gate:** NOT_MET/BLOCKED (sealed)
- **Risk-overlay:** INELIGIBLE

## KEY EVIDENCE

- Handoff: `AGENT_HANDOFF.md` (this file)
- H004: `research_state/liquidation_sources_enumeration.md`, `research_state/binance_source_probe.md`
- H002: `research_state/h002_replication_report.md`, `research_state/hypothesis_registry.json`, `research_state/run_manifest.json`
- Protocol: `RESEARCH_PROMPT.md`, `research_state/research_protocol*.md`

**START NOW. Do heavy work on H004 source discovery. Leave a clean, unambiguous handoff for the next agent.**
