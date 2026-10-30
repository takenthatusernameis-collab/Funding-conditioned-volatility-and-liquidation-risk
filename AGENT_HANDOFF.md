# AGENT HANDOFF — Funding-Conditioned Volatility and Liquidation Risk

UPDATED: 2026-10-30T03:00:00Z
HEAD: 11a73a28 (main)
REPO: Funding-conditioned-volatility-and-liquidation-risk

## REPO FOCUS (from name): LIQUIDATION RISK IS THE PRIORITY
This repo studies funding-conditioned volatility and liquidation risk. Given the name and current state, **liquidation risk (H004 / Track A)** is the ONLY pillar that can still yield an answer about observed liquidation events. All forecast gates (FCLR-001–004) are sealed NOT_MET/BLOCKED — do NOT re-run them. Do NOT build risk overlays/simulations/merges until a forecast gate passes (none do).

## SINGLE, TIMESTAMPED INITIAL TASK MESSAGE FOR NEXT AGENTIC SESSION (DURABLE)

> **[2026-10-30T03:00:00Z] CAMPAIGN: UNBLOCK H004 — OBSERVED LIQUIDATION LABELS (HEAVY, NO ESCAPE)**
>
> **Mission:** Find ANY admissible unauthenticated public source yielding observed forced-liquidation events for {BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT} covering 2024 with defensible provenance. If none exists for 2024, produce STRUCTURAL EVIDENCE (exact URLs/paths, HTTP codes, method, auth/terms, schema, coverage gaps) proving impossibility under constraints AND propose the SMALLEST defensible expansion (different venue/year/window) that IS admissible with a concrete label construction plan. DO NOT claim "event-free" from absence.
>
> **Hard constraints (non-negotiable):**
> - No credentials, paid services, trials, manual files/keys, user intervention. No bypassing auth/rate limits/terms.
> - No forecast gate re-runs (FCLR-001-004 sealed). No .github/workflows changes. No trading/risk-overlay/simulation/merge tracks.
> - Distinguish observed (Track A) from modeled (Track B) from volatility-only (Track C). Capped sample != census. Absence != zero.
> - Only unauthenticated public sources. Verify actual download paths, not just API docs.
>
> **Must do (heavy work, leave no stone unturned):**
> 1. **Absorb context:** Read `research_state/liquidation_sources_enumeration.md`, `research_state/binance_source_probe.md`, `RESEARCH_PROMPT.md` §§5,7.2, `research_state/hypothesis_registry.json` (FCLR-H004), this handoff. Understand prior probes (Binance liquidationSnapshot 404, forceOrders 451, HF 2026-only).
> 2. **Exhaustive probing:** Check unauthenticated paths across Binance data.binance.vision (all UM/CM daily/monthly variants), fapi.binance.com public endpoints, Bybit public.bybit.com, OKX public archives, Deribit, Gate.io/KuCoin public archives if obvious, HuggingFace/Zenodo/GitHub raw unauthenticated datasets (expand beyond 2026), academic repos, any venue-native public archives. Try alternative naming (e.g., `liquidation`, `forceOrder`, `liquidations`).
> 3. **Forensic logging:** For EVERY probe, record in `research_state/liquidation_sources_enumeration.md` (exact URL, timestamp UTC, method, HTTP code, auth Y/N, terms/license, schema, earliest/latest, symbols/venue, completeness/gaps/caps, admissible Y/N, complete-census plausible Y/N, rejection reason). Update existing entries if you get new evidence.
> 4. **Decision:** If VIABLE for 2024 (or frozen windows) → write concrete plan + create/update `research_state/fclr_h004_tracka_viable.json` with provenance, coverage, label construction, caveats. If BLOCKED for 2024 → add structural evidence + propose SMALLEST admissible expansion (specific venue/year/window) with concrete label construction plan + feasibility checks. Do NOT infer event-free.
> 5. **Handoff readiness:** Leave enumeration complete enough that next agent acts without re-probing from scratch. Update AGENT_HANDOFF.md with precise next actions and any new blockers.

> **Bottlenecks removed / enforced:**
> - Forecast gates sealed (do not touch). Duplicate H004 registry cleaned conceptually; focus on source discovery.
> - Workflows untouched. No overlay/sim/merge. No credentials. Capped!=census enforced. Absence!=zero.
> - Do NOT re-probe already-confirmed dead ends (Binance liquidationSnapshot 404, forceOrders 451, HF 2026-only) without NEW evidence — record once and move to other sources.
> - Tests pass: `python -m unittest tests.test_funding_correction_replication -v` (10/10). Don't break them.

## CURRENT STATE SNAPSHOT
- H001: INCONCLUSIVE (FCLR-001 pilot; FCLR-002 numerically passes CI but >=3-block requirement NOT met)
- H002: PARTIAL_REPLICATION (complete; tests pass)
- H003: INCONCLUSIVE (no incremental skill over B0)
- H004 (Track A): BLOCKED for frozen 2024 windows → **UNBLOCK VIA SOURCE DISCOVERY ONLY**
- Forecast gates: NOT_MET/BLOCKED (sealed). Risk-overlay: INELIGIBLE.
- Tests: `python -m unittest tests.test_funding_correction_replication -v` passes (10/10)

## KEY EVIDENCE
- `research_state/liquidation_sources_enumeration.md` (current probes, needs expansion)
- `research_state/binance_source_probe.md`
- `research_state/hypothesis_registry.json` (FCLR-H004)
- `RESEARCH_PROMPT.md` §§5,7.2
- `research_state/h002_replication_report.md`, `research_state/run_manifest.json`

**START NOW. Do HEAVY work on H004 source discovery. Leave a clean, unambiguous handoff. Liquidation risk is the repo's namesake priority — this is the only path forward.**
