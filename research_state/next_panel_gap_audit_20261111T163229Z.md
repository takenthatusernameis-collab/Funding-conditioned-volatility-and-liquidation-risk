# Next Panel Gap Audit — 20261111T163229Z

- **Generated (UTC):** 20261111T163229Z
- **Scope:** Branch 2 default heavy campaign while Gate 4 is externally blocked. Inventory/audit only; **no outcomes computed**, **no preregistration frozen by this document**.
- **Authoritative handoff:** `HANDOFF_NEXT_SESSION.md`

## Gate 4 status (Branch 1 trigger)
- **Status:** EXPLICIT_BLOCKER_UNRESOLVED (external, human/legal)
- **Blocker artifact:** `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json` (`fabricated=false`)
- **Execute Branch 1 only if:** valid `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` appears with all 8 verifiable fields, `fabricated=false`, `status=RESOLVED_VERIFIED`, human/legal attestation; then deterministic promotion + `--expect-go` validators and, on all-green GO, confirmatory Track C multi-split ablation + verdict + atomic state updates.

## Cached admissible assets (inventory)
### Ironflow observed liquidation events (Track A precedent, Hyperliquid)
- Path: `research_state/data_cache/ironflow_events/` — 18 monthly parquet files, 2025-05..2026-10
- Rows (cached): ~2,848,413; unique markets: 468
- Provenance/license note: ironflow/hyperliquid-liquidations, observed labels (CC BY 4.0 as recorded in prior state); hashes recorded in JSON audit. Hyperliquid venue only.
### Hyperliquid funding (cached)
- Path: `research_state/data_cache/hyperliquid_funding/` — 9 coins: AVAX, BNB, BTC, DOGE, ETH, LINK, SOL, SUI, XRP
- Approx coverage: ~2025-11-01T00:00:00Z..2026-10-31T23:00:00Z per sample timestamps (confirm per-coin in build/prereg). Hashes recorded in JSON audit.
### Hyperliquid 1h candles / RV context (cached)
- Path: `research_state/data_cache/hyperliquid_candles/` — 9 coins, months 2026-05..2026-10 per coin (6 files each). Hashes/sizes recorded in JSON audit.
- **Gap:** no candle cache found for 2025-05..2026-04 in this directory.

## Evaluated (closed, do not relitigate)
- `TRACKA-HL-S-20261111T133430Z` (2026-05-01..2026-10-31, 9 symbols): **NOT_MET** — `research_state/evaluation_summary_TRACKA-HL-20261111T160124Z.md` (panel `research_state/tracka_hl_aligned_panel_with_rv_20261111T160124Z.parquet`). No re-run without new pre-registered design/data.

## Unexploited gaps (admissibility-screened candidates)
### GAP-TRACKA-EARLY-OBSERVED-2025H2_2026Q1 — priority: HIGH (Track A / observed liquidation-risk)
- Candidate: Funding-conditioned features vs RV-only baseline for next-24h observed Hyperliquid liquidation intensity on a new pre-registered panel/window disjoint from evaluated 2026-05..2026-10 holdout design, using ironflow observed labels.
- Cached inputs: {"observed_labels": "ironflow_events 2025-05..2026-04 present (months 2025-05..2026-04 unexploited for this specific RV-augmented forecast design)", "funding": "hyperliquid_funding cached for 9 coins with coverage overlapping ~2025-11..2026-04 (confirm exact per-coin timestamps in prereg build)", "rv_price_context": "NOT cached for 2025-05..2026-04 in hyperliquid_candles/ (gap)"}
- Fillable by admissible acquisition: True
- Acquisition needed: Bounded first-time unauthenticated Hyperliquid candleSnapshot 1h fetch+cache with provenance (URL/access time/checksums/API-key/requester-pays/signature status) for required coins/months; no redundant polling of already-cached 2026-05..2026-10.
- Constraints: Pre-register BEFORE any outcome computation/panel alignment for the new claim; Maintain >=5 paired instruments and >=3 non-overlapping 30d test blocks if design requires (specify in prereg); document if infeasible; Observed labels only; no modeled/proxy presented as observed; Hyperliquid only, no Binance/2024 conflation; No sealed-holdout reuse
- Claim-worthy if: sufficient symbol-month overlap with complete funding+RV+label coverage and pre-registered minima/splits satisfied after deterministic build; otherwise document infeasibility.

### GAP-TRACKA-SYMBOL-EXPANSION-2026M05M10 — priority: MEDIUM-HIGH (Track A / observed liquidation-risk)
- Candidate: Expand symbol universe on 2026-05..2026-10 (or subwindow) for observed liquidation-intensity forecasting if additional liquid Hyperliquid markets have adequate label activity and matching predictors.
- Cached inputs: {"observed_labels": "ironflow_events 2026-05..2026-10 present (468 markets total in cache; prior panel used 9)", "funding": "cached for 9 coins only", "rv_price_context": "cached for 9 coins only (2026-05..2026-10)"}
- Fillable by admissible acquisition: POSSIBLY
- Acquisition needed: First-time unauthenticated Hyperliquid fundingHistory and/or candleSnapshot fetch+cache with provenance for candidate additional symbols present in ironflow with sufficient liquidation activity; must pass minima and avoid cherry-picking (pre-registered symbol selection rule).
- Constraints: New prereg required (different universe/design than NOT_MET successor); Pre-register symbol inclusion/exclusion and minima before outcomes; Beware sparse-liquidity/sparse-liquidation symbols; require event-adequacy checks as pre-registered; No outcome inspection before freeze
- Claim-worthy if: pre-registered universe yields >=5 paired instruments and >=3 non-overlapping 30d test blocks with adequate label variance; requires evidence-driven selection rules frozen ex ante.

### GAP-ALTERNATIVE-OBSERVED-LIQUIDATION-SOURCES — priority: MEDIUM (Track A)
- Candidate: None identified in current cache without new admissible source verification.
- Cached inputs: {"notes": "No other verified observed-liquidation datasets with matching Hyperliquid decision-time predictors found in data_cache beyond ironflow. prior liquidation forward-validate notes are blockers; treat as historical unless revalidated with provenance."}
- Fillable by admissible acquisition: UNKNOWN
- Acquisition needed: Only if a verifiable unauthenticated observed-liquidation source with license/provenance and alignable predictors is found; requires pre-outcome admissibility review and prereg.
- Constraints: Observed only, verifiable provenance, no requester-pays/auth ambiguity unresolved

### GAP-VOLATILITY-UNTESTED-ADMISSIBLE-PANELS — priority: LOWER than Track A while Gate 4 blocked
- Candidate: Volatility forecasting on admissible untested Hyperliquid (or other admissible unauthenticated) panels where funding+RV+targets can be constituted without Binance 2024/Track C conflation.
- Cached inputs: {"notes": "HL funding/candles overlap limited (candles 2026-05..2026-10 for 9 coins; funding to ~2026-10-31). Any volatility claim must be a new pre-registered design on an untested admissible panel and must not reuse sealed holds."}
- Fillable by admissible acquisition: POSSIBLY with candle/funding extension (see GAP-TRACKA-EARLY-OBSERVED-2025H2_2026Q1 acquisition pattern) but claim is secondary to liquidation-risk priority.
- Constraints: No Track C/Gate 4 bypass; No 2024 Binance conflation; Pre-register before outcomes

## Recommended next heavy work (execute now, Branch 2)
- **Selected candidate:** `GAP-TRACKA-EARLY-OBSERVED-2025H2_2026Q1`
- **Rationale:** Repo priority is liquidation-risk forecasting co-equal with volatility on observed admissible data. Ironflow observed labels already cached for 2025-05..2026-04 and HL funding appears cached into that range for 9 coins; primary missing input is RV/price context (candles) for an earlier window. This is potentially fillable by bounded first-time unauthenticated Hyperliquid candleSnapshot acquisition with provenance, enabling a genuinely new pre-registered Track A evaluation (not a relitigation of NOT_MET 2026-05..2026-10).
- **Required sequence (no outcome computation before freeze):**
  - 1) Define frozen preregistration (JSON+md) BEFORE any outcome computation: hypothesis, exact window/symbols, observed label definition/aggregation horizon, feature set, splits/embargo (>=7d), baselines/contrasts (e.g. B1 RV-only vs C2 funding-conditioned), metric, materiality threshold, minima (>=5 instruments, >=3 non-overlapping 30d test blocks if feasible), symbol/data inclusion rules, and handling of missingness.
  - 2) If candle gaps remain, perform bounded first-time unauthenticated Hyperliquid candleSnapshot fetch for prereg-specified coins/months only; cache under research_state/data_cache/hyperliquid_candles/ (or documented path) and record provenance manifest (endpoint, params, access time UTC, HTTP/status, checksums, unauthenticated/no-key/no-requester-pays/signature status). Do not re-fetch 2026-05..2026-10.
  - 3) Build deterministic aligned panel from cached inputs; emit panel parquet/json + build report with hashes/coverage/leakage-guard notes.
  - 4) Run pre-registered evaluation only after freeze artifacts exist; compute required splits/embargo and bootstrap CIs per prereg; emit evaluation_summary_<UTC>.md and verdict.
  - 5) Update experiment_frontier.json, hypothesis_registry.json, run_manifest.json, final_confirmatory_verdict.md atomically to reflect new prereg/run/verdict; keep prior NOT_MET and sealed records intact.
  - 6) If prereg minima cannot be satisfied on audited cached+acquirable data, emit a concrete infeasibility/exhaustion addendum (with evidence) rather than status-only output and select next candidate gap (symbol expansion) under same rules.
- **Stop/pivot conditions:** Valid Gate 4 RESOLVED_VERIFIED terms evidence appears -> switch to Branch 1 immediately; Any required source fails admissibility/provenance verification -> do not use; document and pivot

## Explicit non-claims
- This audit does **not** assert forecast improvement, does **not** inspect target outcomes for a new claim, and does **not** resolve Gate 4.
- 2024 Binance and Hyperliquid panels/claims must remain distinct. Modeled/proxy liquidation labels must not be presented as observed.

## Artifacts
- JSON: `research_state/next_panel_gap_audit_20261111T163229Z.json`
- Markdown: `research_state/next_panel_gap_audit_20261111T163229Z.md`
