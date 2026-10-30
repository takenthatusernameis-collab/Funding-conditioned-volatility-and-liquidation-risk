# AGENT HANDOFF — Funding-Conditioned Volatility and Liquidation Risk

UPDATED: 2026-10-30T03:06:00Z
HEAD: 2119505d (main, origin/main)
REPO: Funding-conditioned-volatility-and-liquidation-risk

## PRIORITY (repo name): LIQUIDATION RISK — H004 / TRACK A IS THE ONLY UNBLOCKED PATH

The repo studies funding-conditioned volatility and liquidation risk. Liquidation risk (observed labels, H004 / Track A) is the namesake priority and the only track that is neither sealed nor concluded. All forecast gates FCLR-001–004 are SEALED (NOT_MET/BLOCKED). Do NOT re-run them. Do NOT build risk overlays/simulations/merges until a forecast gate passes (none do). Do NOT touch .github/workflows/.

## SINGLE TIMESTAMPED INITIAL TASK — CAMPAIGN H004-20261030

> **[2026-10-30T03:02:50Z] CAMPAIGN: UNBLOCK H004 — OBSERVED LIQUIDATION LABELS (HEAVY WORK, NO ESCAPE HATCH)**

Mission: produce either (a) an admissible unauthenticated public source of observed forced-liquidation events covering the frozen 2024 test windows for {BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT} with defensible provenance, or (b) documented STRUCTURAL EVIDENCE proving Track A infeasible under constraints PLUS the smallest defensible scope expansion (venue / year / window) with a concrete label-construction plan.

Network is reachable in this session (curl to data.binance.vision returned HTTP 404, not a connection failure) — unauthenticated probes are executable now. Do not treat "no network" as an excuse.

Hard constraints:
- No credentials, paid services/trials, manually supplied keys/files, user intervention. No bypassing auth/rate limits/terms.
- No forecast gate re-runs (FCLR-001–004 sealed). No .github/workflows changes. No trading/risk-overlay/simulation/merge tracks.
- Observed (Track A) != modeled (Track B) != volatility-only (Track C). Capped sample != census. Absence != zero. Event-free intervals may never be inferred from missing data.

Execution order — do all, in order:
1. Absorb context: research_state/liquidation_sources_enumeration.md, research_state/binance_source_probe.md, RESEARCH_PROMPT.md §§5 and 7.2, research_state/hypothesis_registry.json (FCLR-H004), this handoff.
2. Dead ends already recorded once — DO NOT re-probe without NEW evidence (log "no new evidence" and proceed): Binance liquidationSnapshot daily/monthly HTTP 404 (UM + CM); Binance fapi forceOrders HTTP 451; Bybit public.bybit.com /lin/liquidation 404 and no liquidation directory; OKX no unauthenticated bulk liquidation census; Deribit none; HF crypto-liquidation-ticks covers only 2026 (admissible but wrong window); Zenodo no crypto liquidation events; GitHub code search 401.
3. Exhaustive probing (the heavy work):
   - Binance variants: all plausible unauthenticated data.binance.vision paths — daily/monthly liquidation*, force*, liq*; UM and CM; index pages recursively. HEAD/GET every candidate.
   - Other venues: Bybit public.bybit.com all subpaths, OKX public archives, Gate.io, KuCoin public archives; naming variants liquidation / forceOrder / liquidations / liquidationOrders.
   - Dataset repos: Hugging Face (search "liquidation binance 2024", all datasets, unauthenticated download paths), Zenodo, Figshare, Kaggle public (unauthenticated), GitHub raw, Internet Archive snapshots of known paths.
   - Any other venue-native public bulk endpoints; test index listings.
4. Forensic logging: for EVERY probe append to research_state/liquidation_sources_enumeration.md — exact URL, UTC timestamp, method, HTTP code, auth Y/N, terms/license, schema, earliest/latest, symbols/venue, completeness/gaps/caps, admissible Y/N, complete-census-plausible Y/N, rejection reason. Append only; never delete confirmed dead ends.
5. Decision & deliverable: VIABLE for 2024/frozen windows → research_state/fclr_h004_tracka_viable.json (provenance, coverage, label construction, caveats). BLOCKED for 2024 → structural evidence in enumeration + smallest admissible expansion (specific venue/year/window, exact sources to test) with concrete label-construction plan and feasibility checks.
6. Handoff readiness: leave enumeration complete enough that the next agent acts without re-probing from scratch; update AGENT_HANDOFF.md with precise next actions and new blockers.

Bottlenecks removed (enforced this session):
- Dead ends recorded once; no repeated re-probing without new evidence (stops session bouncing on concluded tracks).
- Forecast gates sealed — no re-runs, no overlay/sim/merge.
- Capped != census; absence != zero — prevents false "event-free" claims.
- Session scope: H004 source discovery ONLY. No exploration tangents.

Verification gate: `python -m unittest tests.test_funding_correction_replication -v` must stay green (10/10). research_state/liquidation_sources_enumeration.md must grow monotonically each session.

START NOW. HEAVY WORK ON H004. Liquidation risk is the repo's namesake priority — this is the only path forward.

## SECONDARY PATH (only if H004 is structurally exhausted across all source families)

H001's ≥3-block gate can be unblocked WITHOUT new downloads: research_state/data_cache holds cached Q4-2024 data (Oct–Dec) for all 5 symbols and run_manifest.json records pre-registered FCLR-003 splits (test 2024-10-02T00:00:00Z..2024-12-31T23:00:00Z, ~91 days = 3 non-overlapping 30-day blocks). Unblock route: coverage-only audit of the cached Q4 panel → frozen protocol version FCLR-003 v1.0 → run frozen pipeline → record canonical numbers. This does NOT open any sealed holdout for selection and does NOT change the INCONCLUSIVE verdict unless the gate passes. Do not let this distract from H004.

## CURRENT STATE SNAPSHOT

- H001 (incremental 24h volatility): INCONCLUSIVE. FCLR-002 primary contrast C2 vs B1 numerically passes (-9.28% rel QLIKE, CI [-0.097648,-0.008788] excludes zero, independently reproduced 2026-10-28 byte-identical) but minimum claim-worthy test NOT met: FCLR-001 window panel is BTCUSDT-only (true 5-symbol mark-price intersection = 0 timestamps per coverage_audit_recheck.md; run_manifest.json's 2136 figure is not reproducible); FCLR-002 test window = 70 days = 2 non-overlapping 30-day blocks (<3 required).
- H002 (funding-extreme correction-time replication): PARTIAL_REPLICATION (complete). 88 events Jan–Mar 2024, 5 symbols; median 8.0 h; 10/10 tests pass. SSRN HTTP 403 blocks exact replication; RV-regime contrast infeasible.
- H003 (hypothetical boundary-breach): INCONCLUSIVE. No incremental skill over B0 on any pre-specified metric (FCLR-001 degenerate; FCLR-002 real events at 5x/10x/20x but C2 does not beat B0).
- H004 Track A (observed liquidation labels): BLOCKED for frozen 2024 windows — structural evidence complete (see KEY EVIDENCE). UNBLOCK VIA SOURCE DISCOVERY ONLY.
- Forecast gates FCLR-001–004: NOT_MET/BLOCKED (sealed). Risk overlay: INELIGIBLE.
- Conflicting evaluation summaries (evaluation_summary.md vs evaluation_summary_FCLR002.md) flagged UNTRUSTED in research_state/evaluation_summary_conflict.md; neither verified; do not cite.
- Tests: `python -m unittest tests.test_funding_correction_replication -v` passes 10/10.

## KEY EVIDENCE

- research_state/liquidation_sources_enumeration.md — Track A source enumeration (expand exhaustively per campaign)
- research_state/binance_source_probe.md — Binance verified URLs + liquidation verdict (NOT VERIFIED / not directly downloadable)
- research_state/coverage_audit_recheck.md — FCLR-001 panel BTCUSDT-only; 5-symbol intersection 0 timestamps Jan–Mar 2024
- research_state/hypothesis_registry.json — FCLR-H001..H004 statuses and next falsification tests
- RESEARCH_PROMPT.md §§5, 7.2, 12 — constraints, source tracks, handoff contract
- research_state/data_cache/ — cached Q4-2024 panel for all 5 symbols (H001 secondary unblock path)

## DURABLE HANDOFF CONTRACT (per RESEARCH_PROMPT §12)

1. What changed and why: session state inspected; H001 unblock path identified (cached Q4 panel + pre-registered FCLR-003 splits); network reachability confirmed; AGENT_HANDOFF.md refreshed with timestamped H004 campaign and enforced bottleneck removals.
2. What was actually tested, exact outcomes: `python -m unittest tests.test_funding_correction_replication -v` → 10/10 OK; curl data.binance.vision → HTTP 404 (reachable, path missing).
3. Evidence added: none new this session beyond reachability confirmation and H001 unblock documentation; enumeration unchanged — next session must grow research_state/liquidation_sources_enumeration.md.
4. Current state of each research gate: H001 INCONCLUSIVE (≥3-block gate NOT met); H002 PARTIAL_REPLICATION; H003 INCONCLUSIVE; H004 BLOCKED; forecast gates sealed NOT_MET; overlay INELIGIBLE.
5. Single highest-value next task: H004 source-discovery campaign (this file, §CAMPAIGN H004-20261030).
6. Precise verification command: `python -m unittest tests.test_funding_correction_replication -v` (10/10 required) + monotonic growth of research_state/liquidation_sources_enumeration.md with dated probe records.
7. Blocker with evidence and next free route: direct liquidation labels unavailable for frozen 2024 windows (Binance liquidationSnapshot 404, forceOrders 451 — research_state/binance_source_probe.md; enumeration §1–4). Next free route: Bybit/OKX/Gate.io/KuCoin archives, HF/Zenodo/Figshare/Kaggle/Internet Archive, then smallest admissible venue/year/window expansion if all fail.

FOCUS: H004 source discovery only. Heavy work required. No escape hatch.