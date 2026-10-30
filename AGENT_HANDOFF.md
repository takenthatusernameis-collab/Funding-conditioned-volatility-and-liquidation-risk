# AGENT HANDOFF — Funding-Conditioned Volatility and Liquidation Risk

UPDATED: 2026-10-30T02:06:56Z
HEAD: e92aa7c2 (main)
REPO: Funding-conditioned-volatility-and-liquidation-risk

## REPO FOCUS (from name): LIQUIDATION RISK IS THE PRIORITY
This repo studies funding-conditioned volatility and liquidation risk. Given the name and current state, **liquidation risk (H004 / Track A)** is the only pillar that can still yield an answer about observed liquidation events. All forecast gates (FCLR-001–004) are sealed NOT_MET/BLOCKED — do not re-run them.

## SINGLE, TIMESTAMPED INITIAL TASK MESSAGE FOR NEXT AGENTIC SESSION (DURABLE)

> **[2026-10-30T02:06:56Z] CAMPAIGN: UNBLOCK H004 — OBSERVED LIQUIDATION LABELS (HEAVY, NO ESCAPE)**
>
> **Goal:** Find ANY admissible unauthenticated public source yielding observed forced-liquidation events for {BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT} covering 2024 with defensible provenance. If none exists for 2024, produce STRUCTURAL EVIDENCE (exact URLs/paths, HTTP codes, method, auth/terms, schema, coverage gaps) proving impossibility under constraints AND propose the SMALLEST defensible expansion (different venue/year/window) that IS admissible with a concrete label construction plan.
>
> **Non-negotiable:** No credentials, paid services, trials, manual files/keys, user intervention. No forecast gate re-runs. No .github/workflows changes. No trading/risk-overlay/simulation/merge tracks until a forecast gate passes (none do). Distinguish observed (Track A) from modeled (Track B) from volatility-only (Track C). Capped sample != census. Absence != zero.
>
> **Must do (heavy):**
> 1. Read: `research_state/liquidation_sources_enumeration.md`, `research_state/binance_source_probe.md`, `RESEARCH_PROMPT.md` §§5,7.2, `research_state/hypothesis_registry.json`, this handoff.
> 2. Probe exhaustively (unauthenticated): Binance data.binance.vision (UM/CM daily/monthly liquidationSnapshot/forceOrders variants), fapi.binance.com public endpoints, Bybit public.bybit.com (any liquidation/*), OKX public archives, Deribit public archives, HuggingFace/Zenodo/GitHub raw unauthenticated datasets (check older windows), venue-native public archives.
> 3. For EVERY probe record forensic evidence in `research_state/liquidation_sources_enumeration.md` (exact URL, time, method, HTTP code, auth Y/N, terms/license, schema, earliest/latest, symbols/venue, completeness/gaps/caps, admissible Y/N, complete-census plausible Y/N, rejection reason).
> 4. Decide: if VIABLE → write concrete plan + update/create `research_state/fclr_h004_tracka_viable.json`. If BLOCKED for 2024 → structural evidence + smallest admissible alternative scope OR state Tracks B/C only with no event-free inference.
> 5. Leave enumeration sufficient for next agent to act without re-probing from scratch.
>
> **Bottlenecks removed:** forecast gates sealed; duplicate H004 registry entry removed; workflows untouched; no overlay/sim/merge; no credentials; capped!=census enforced. Do NOT re-probe already-confirmed dead ends (Binance liquidationSnapshot 404, forceOrders 451, HF 2026-only) without new evidence — record once and move on.

## CURRENT STATE SNAPSHOT
- H001: INCONCLUSIVE (FCLR-001 pilot; FCLR-002 numerically passes CI but >=3-block requirement NOT met)
- H002: PARTIAL_REPLICATION (complete)
- H003: INCONCLUSIVE (both panels; no incremental skill over B0). Do NOT threshold-shop.
- H004 (Track A): BLOCKED for frozen 2024 windows → UNBLOCK VIA SOURCE DISCOVERY ONLY
- Forecast gates: NOT_MET/BLOCKED (sealed). Risk-overlay: INELIGIBLE.
- Tests: `python -m unittest tests.test_funding_correction_replication -v` passes (10/10)

## KEY EVIDENCE
- `research_state/liquidation_sources_enumeration.md` (current probes)
- `research_state/binance_source_probe.md`
- `research_state/hypothesis_registry.json` (H004)
- `RESEARCH_PROMPT.md`
- `research_state/h002_replication_report.md`, `research_state/run_manifest.json`

**START NOW. Do HEAVY work on H004 source discovery. Leave a clean, unambiguous handoff. Liquidation risk is the repo's namesake priority — this is the only path forward.**
