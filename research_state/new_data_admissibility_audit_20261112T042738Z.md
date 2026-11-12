# NEW DATA ADMISSIBILITY AUDIT
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk` (priority: funding-conditioned volatility AND liquidation risk — repo-name-prioritized)
**Audit timestamp (UTC):** 2026-11-12T04:27:38Z
**Supersedes / derives from:** `HANDOFF_NEXT_SESSION.md` §(B) step 2; `RESEARCH_PROMPT.md` §16 admissibility requirements
**Gate 4 trigger check (verified):** absent — no `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_RESOLVED_*.json` with `status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal attestation. Highest local artifact is `fclr016_v5_terms_evidence_UNRESOLVED_20261108T204000Z.json` (`confirmatory_claim_go=NO_GO`, `confirmatory_provenance_go=false`, `status=UNRESOLVED`, reviewer_role=pending_human_legal_maintainer). Gate 4 Branch 1 NOT executable this session; not agent-removable. Do not wait/poll.

## Admissibility requirements (RESEARCH_PROMPT.md §16)
Unauthenticated/public; provenance + license/terms documented; sufficient for the claim (observed labels where required; no modeled/proxy/synthetic liquidation labels as observed); coverage ≥5 symbols/instruments and ≥3 non-overlapping 30-day test blocks, non-overlapping train/val/test + embargo as applicable; venue-consistent with artifacts; not conflated with sealed Binance 2024 verdicts.

## Inventory — candidates examined (this session)

| # | Candidate (path) | Venue | Symbols | Coverage | Label type | Provenance/license evidence locally | Admissible? | Untested claim enabled? | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `research_state/data_cache/hyperliquid_funding/*.json` (23 coins) | hyperliquid | AAVE,ADA,AVAX,BCH,BNB,BTC,CRV,DOGE,ETH,LINK,LTC,NEAR,SOL,SUI,UNI,XRP,ZEC (+) | verified BTC/ETH/SOL/BNB/XRP: 8668 hourly records each, 2025-11-01..2026-10-30 | funding (feature) | `.sha256` + `.accessed.json` per coin; source `api.hyperliquid.xyz/info` fundingHistory POST (unauthenticated) | PARTIAL (feature only) | NO — same 2025-11..2026-10 window already cached; no observed liquidation labels | INADMISSIBLE for new claim (feature-only, window exhausted) |
| 2 | `research_state/data_cache/hyperliquid_candles/*/` (17 symbol subdirs) | hyperliquid | AAVE,ADA,AVAX,BCH,BNB,BTC,CRV,DOGE,ETH,LINK,LTC,NEAR,SOL,SUI,UNI,XRP,ZEC | BTC/ETH: empty 2025-11..2026-03, partial 2026-04 (~45KB), full 2026-05..2026-10 (~114-118KB/month) | candles (RV feature) | `.sha256` + `.accessed.json` per month; `hyperliquid_candles_manifest_20261111T145106Z.json` (git-lfs pointer) | PARTIAL | NO — window 2026-05..2026-10 exhausted (all volatility designs NOT_MET); 2025-11..2026-04 INADMISSIBLE (candles empty → RV24h/B1 uncomputable) | INADMISSIBLE for new claim (window/symbols exhausted) |
| 3 | `research_state/data_cache/ironflow_events/*.parquet` (18 monthly) | hyperliquid (ironflow) | all liquidation events | 2025-05..2026-10 monthly | observed liquidation labels | CC BY 4.0 (per hypothesis_registry H_tracka_hl_liquidation_forecast) | PARTIAL | NO — labels exist but pair only with exhausted candle window 2026-05..2026-10 | INADMISSIBLE for new claim (outcome labels only, no new feature window) |
| 4 | `research_state/data_cache/craftify_liq/liq_2025-10.parquet`, `liq_2026-01.parquet` | unknown/secondary | unknown | 2 months only (2025-10, 2026-01) | liquidation (claimed) | No local provenance/license documentation; coverage <3 non-overlapping 30-day blocks | INADMISSIBLE | NO — coverage insufficient, provenance unverified | INADMISSIBLE (coverage + provenance) |
| 5 | `data/raw/` (BTCUSDT/ETHUSDT 2024-01 klines + fundingRate) + `research_state/data_cache/BTCUSDT_2024_..`/`BTCUSDT_2025_..`/`BTCUSDT_2026_..` (5 sym × monthly) | binance | BTC,ETH,SOL,XRP,BNB | 2024-01..2026-11 | market data | local zips, extraction tested | INADMISSIBLE for Track A | NO — Track A is Hyperliquid-only 2025-06..2026-10; Binance/2024 conflation forbidden; Track B/C 2024 sealed NOT_SUPPORTED | SEALED / INADMISSIBLE |
| 6 | Acquisition-path scripts (`scripts/hyperliquid_funding_fetch.py`, `tracka_hl_fetch_candles_*.py`, `h004_download_2026.py`, `download_extended.py`, `exhaustive_binance_probe.py`, `hunt_alternative_liquidation_sources.py`, `monitor_ironflow_liquidations.py`) | — | — | — | — | — | define paths only | NO — all local caches already populated/exhausted; no new local window/symbols uncovered | NOT a data candidate |

## Sealed / exhausted records (do not reopen)
- Track A liquidation expansion `TRACKA-HL-EXPANSION-20261111T195500Z` = PASS (rel QLIKE -19.04%, CI [-5.088,-0.478], n=593, 8 instruments, 3 blocks, 2026-05..2026-10). Sealed. Robustness FRAGILE (LOIO FAIL 4/8, Placebo FAIL p≈0.07, Bootstrap PASS 3/3). Sealed.
- Track A volatility primary 24h `TRACKA-VOL-20261111T234918Z` = NOT_MET (rel -1.37%, CI crosses zero). Sealed.
- Track A volatility family `TRACKA-VOL-FAMILY-20261112T005111Z` = NOT_MET (Holm, 12 comparisons). Sealed.
- Track A alternate volatility `TRACKA-ALT-VOL-20261112T020322Z` = NOT_MET (rel 5.77%, CI crosses zero). Sealed.
- Track A 9-symbol 2026-05..2026-10 = NOT_MET (closed). Track A early 2025-11..2026-04 = INADMISSIBLE (closed).
- Track B/C 2024 and H1/FCLR-002/003 contexts sealed/closed negative; H1 primary NOT_SUPPORTED on tested panels. Immutable.
- 2024 Binance confirmatory FCLR-003 = NOT_SUPPORTED (`research_state/final_confirmatory_verdict.md`). Immutable.

## Determination
**NO locally-admissible untested candidate exists.** All admissible cached-data volatility/liquidation designs on current Hyperliquid/Binance caches are EXHAUSTED/SEALED. Per HANDOFF_NEXT_SESSION.md §(B) step 4, proceed to exhausted-local documentation + minimal external acquisition specification (below). Do NOT fabricate, download unverified data, or guess provenance. No new experiments on exhausted cached data.

## Minimal external acquisition needed to unblock a new claim (specification, not execution)
To open a new claim-worthy experiment, the next session must acquire ONE new admissible source/window meeting ALL of §16:

| Requirement | Specification |
|---|---|
| Venue/product | Perpetual futures venue with unauthenticated public historical funding + mark/index price history (candles) AND observed liquidation labels, OR a genuinely new venue; NOT Binance 2024, NOT conflated with sealed Binance verdicts |
| Symbols/instruments | ≥5 instruments (ex-ante selected, not outcome-dependent) |
| Date range | A window NOT already sealed: either (a) Hyperliquid 2026-11 onward (post-panel), or (b) a different venue/window with ≥3 non-overlapping 30-day test blocks plus train/val/test + 7-day embargo |
| Fields | funding rate (signed, timestamped), mark price, index price (for premium/EMA), observed liquidation notional/count where Track A, else realized-volatility-only Track C target |
| License/provenance proof required | Exact URL/endpoint, access date UTC, license/terms, file hashes/ETags, schema, cadence, gaps; human/legal review where terms require it (Gate 4 pattern) |
| Access constraint | Unauthenticated, bounded, no payment/signup/manual download/requester-pays; fully evidenced; no fabricated/proxy/synthetic liquidation labels as observed |

### Required next artifacts (next session)
1. Bounded network probe(s) of the selected new source, fully evidenced (endpoint, status, schema sample, coverage, license/terms), saved to `research_state/` with timestamp.
2. If admissible: freeze preregistration BEFORE outcomes (`research_state/track*_prereg_*_<UTC>.json` + `.md`) with hypothesis, data/feature/label definitions, splits/embargo/blocks, primary metric/gate, multiplicity plan, pass/fail criteria; then build+eval in-session if feasible; emit verdict + atomic state updates (`experiment_frontier.json`, manifests/registry).
3. If no admissible external source is verifiable: document structural exhaustion with evidence, name the next materially different free route, and keep `program_status=ACTIVE_HEAVY_CAMPAIGN` with `next_unfinished_task=EXTERNAL_NEW_DATA_SOURCE`.

## Bottleneck status
| Bottleneck | Status | Removal/action |
|---|---|---|
| Gate 4 Branch 1 (external/legal Binance terms) | BLOCKED, not agent-removable | Verified absent 2026-11-12T04:27:38Z. Execute Branch 1 only on valid RESOLVED trigger (`status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal attestation). Do not wait/poll. |
| No untested admissible cached-data experiment | EXHAUSTED | Inventory complete this session → this audit artifact. Next: external new-data acquisition spec (above). |
| Competing root handoff docs / session ambiguity | REMOVED | `HANDOFF_NEXT_SESSION.md` sole durable root handoff; `AGENT_HANDOFF.md`, `FOCUS_CAMPAIGN.md`, `NEXT_SESSION_TASK.md` are redirects. |
| Prior campaign items (volatility family, expansion robustness, alternate volatility) | COMPLETED/SEALED | Do not reopen/retune/relitigate. |

## Hard bans (binding, carried forward)
- No outcome inspection before prereg freeze. No threshold-shopping. No sealed-holdout reuse.
- No Binance/2024 conflation; venue-consistent artifacts only.
- No modeled/proxy/synthetic liquidation labels as observed.
- No `.github/workflows` edits. No redundant network polling. No agent-set `RESOLVED_VERIFIED`/`fabricated=true`; no Gate 4 bypass.
- **No status-only output.** Every session must deliver: Gate 4 Branch 1 if triggered, OR prereg + (build+eval or documented infeasibility with evidence) + state updates, OR a concrete timestamped new-data admissibility audit (+ prereg/external-spec as applicable).
- **No new experiments on exhausted cached data.** Any new claim requires NEW admissible data/source with provenance/license/coverage per RESEARCH_PROMPT.md §16.

---
**Execute now:** this audit is complete. Next session's mandatory heavy work: bounded external new-data probe → prereg → build/eval OR documented structural exhaustion + next materially different free route. No status-only output.
