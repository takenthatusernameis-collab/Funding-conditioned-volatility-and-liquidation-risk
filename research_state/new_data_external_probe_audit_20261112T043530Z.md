# EXTERNAL NEW-DATA ACQUISITION PROBE — AUDIT (HEAVY, EXECUTED)
**Repo:** Funding-conditioned-volatility-and-liquidation-risk (repo-name-prioritized)
**Timestamp (UTC):** 2026-11-12T04:35:30Z
**Campaign:** HANDOFF_NEXT_SESSION.md (2026-11-12T04:30:17Z) §(B) step 3 — external new-data acquisition
**Gate 4 Branch 1:** verified ABSENT 2026-11-12T04:32:39Z — no `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_RESOLVED_*` with `status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal attestation (highest: `fclr016_v5_terms_evidence_UNRESOLVED_20261108T204000Z.json`). Not agent-removable. No wait/poll.

## Scope (bounded, unauthenticated, evidenced)
Probed candidate sources for a NEW admissible claim per RESEARCH_PROMPT.md §16:
- ≥5 instruments/symbols, ≥3 non-overlapping 30-day test blocks (or sufficient horizon), train/val/test + embargo as applicable
- venue-consistent, not conflated with sealed Binance 2024 verdicts
- observed liquidation labels where required (no modeled/proxy/synthetic as observed)
- unauthenticated/public, provenance + license/terms documented
- not already sealed/exhausted

Raw evidence artifacts:
- `research_state/external_new_data_probe_20261112T043403Z.json`
- `research_state/hyperliquid_nov2026_coverage_probe_20261112T043403Z.json`
- `research_state/external_new_data_probe_followup_20261112T043437Z.json`
- Local baseline: `research_state/new_data_admissibility_audit_20261112T042738Z.md/.json`

## Probes executed & findings

| # | Candidate / endpoint | Method | Result (evidence) | Assessment |
|---|---|---|---|---|
| 1 | Hyperliquid public API `https://api.hyperliquid.xyz/info` `candleSnapshot` 1h, 2026-11-01T00:00Z..2026-11-11T00:00Z for BTC,ETH,BNB,SOL,XRP,AVAX,DOGE,LINK,SUI | POST, unauthenticated | HTTP 200; **241 hourly candles/coin** (first_t=1793491200000 2026-11-01T00:00Z, last_t=1794355200000 2026-11-11T00:00Z) for all 9 coins. Schema includes t,T,s,i,o,c,h,l,v,n. | **Feature-side FEASIBLE (candles/RV)** for 9 symbols, but coverage is ~10 days only — **INSUFFICIENT for §16** (needs ≥3 non-overlapping 30-day test blocks / ~≥100+ days with splits+embargo). Not claim-worthy now. |
| 2 | Hyperliquid public API `fundingHistory` same window/coins | POST, unauthenticated | HTTP 200; **240 records/coin** (first_t=1793491200061, last_t=1794351600008). Fields coin,fundingRate,premium,time. | **Feature-side FEASIBLE (funding/premium)**, coverage ~10 days only — **INSUFFICIENT** as standalone new claim window. |
| 3 | `ironflow/hyperliquid-liquidations` on HuggingFace (`/api/datasets/ironflow/hyperliquid-liquidations`) | GET, unauthenticated | HTTP 200. Metadata: `lastModified 2026-11-07T10:18:25Z`, description states coverage **25 May 2025 to 31 October 2026**, 2,849,452 positions, 468 markets, license `cc-by-4.0`. | **NOT NEW vs sealed cache** (local `ironflow_events/*.parquet` already cover 2025-05..2026-10). No post-2026-10-31 liquidation labels available. **INADMISSIBLE as new label source** for a new window. |
| 4 | `https://api.github.com/repos/ironflow/hyperliquid-liquidations` (+ contents, releases/latest) | GET | HTTP 404 (all). | Source repo not publicly accessible at probed paths. No additional artifacts. |
| 5 | `https://api.github.com/search/repositories?q=ironflow+liquidations` | GET | HTTP 200, `total_count: 0`. | No alternate ironflow liquidation repo. |
| 6 | `https://api.github.com/search/repositories?q=hyperliquid+liquidations+dataset` | GET | HTTP 200, 3 results. Top: `metpie/hyperliquid-liquidation-events` (346k trades, 179 markets, **Mar 22–May 25 2025**, from public node-trade archive; README/schema probed). | **metpie**: window 2025-03-22..2025-05-25 is **outside/adjoining but not a new post-sealed window** relative to exhausted Track A program (sealed Track A uses 2025-06..2026-10 / 2025-11..2026-04 contexts; early 2025-11..2026-04 inadmissible for candles but labels differ) — however it does not provide a post-2026-10-31 window, and integrating it would require full admissibility audit (provenance completeness of node-trade reconstruction, alignment to HL funding/candles, license, ≥5 symbols × ≥3x30d blocks). Not verifiably admissible as a quick new claim in this bounded session; **NOT a verified new admissible source now**. |
| 7 | `https://raw.githubusercontent.com/metpie/hyperliquid-liquidation-events/main/README.md` & contents | GET | HTTP 200. Parquet/CSV.gz present; columns time,coin,px,sz,side,liquidated_start_pos,notional_usd,hash; license file present. | Evidence captured; window/coverage insufficient for a new post-sealed multi-block claim without deeper build — **deferred (not verifiably admissible now)**. |
| 8 | `https://huggingface.co/api/datasets?search=hyperliquid%20liquidation&limit=10` | GET | HTTP 200. Returns `ironflow/hyperliquid-liquidations` as primary match. | No other liquidation dataset surfaced. |
| 9 | `https://huggingface.co/api/datasets?search=crypto%20liquidation%20parquet&limit=10` | GET | HTTP 200, empty list. | No candidate. |

## Admissibility determination (this session)
- **Locally-cached data:** NO locally-admissible untested candidate (confirmed; see `research_state/new_data_admissibility_audit_20261112T042738Z.md`).
- **Externally probed now:** NO verifiably admissible external source found that satisfies §16 for a new claim **today**.
  - HL API provides fresh 2026-11 candles+funding (9+ symbols, unauthenticated) but **window too short (~10 days)** for ≥3 non-overlapping 30-day test blocks and required splits/embargo.
  - **Observed liquidation labels for post-2026-10-31 window:** not found (ironflow HF unchanged through 2026-10-31; no alternate public source verified).
  - `metpie` dataset is historical (Mar–May 2025), not a post-sealed window, and not verified admissible for a new multi-block claim in this bounded session.
- **Conclusion:** Structural exhaustion of *currently verifiable* new admissible data remains. **No prereg/fabricated experiment** created (outcome-free; no threshold-shopping). No status-only deferral — bounded probes executed and evidenced.

## Next materially different free route (concrete, executable)
1. **Primary (unblocks repo-priority liquidation+volatility claim):** When sufficient time has elapsed, run a bounded re-probe + acquisition of Hyperliquid 2026-11+ window via unauthenticated `candleSnapshot` (1h) and `fundingHistory` for ≥9 ex-ante symbols, targeting **≥100 days contiguous coverage** to allow ≥3 non-overlapping 30-day test blocks with train/val/test+7d embargo. In parallel, monitor `ironflow/hyperliquid-liquidations` (HF) for an update extending observed liquidation labels beyond 2026-10-31 (check `lastModified` and file coverage). **A claim requires both:** admissible feature window AND observed liquidation labels (or a clearly-scoped volatility-only prereg if labels unavailable — but must meet §16 and repo priority). Evidence each probe (endpoint, status, schema, counts, dates, license/terms) in `research_state/`.
2. **Secondary:** Perform a full §16 admissibility audit of `metpie/hyperliquid-liquidation-events` (Mar–May 2025) against HL funding/candles for that exact window — only if it can form a venue-consistent, ≥5-symbol, ≥3-block design not already sealed and with verified observed-label completeness/provenance; freeze prereg BEFORE outcomes.
3. **Gate 4:** If valid `fclr016_v5_terms_evidence_RESOLVED_*` appears (`RESOLVED_VERIFIED`, `fabricated=false`, human/legal attestation), execute Branch 1 deterministically.

## Hard bans respected
No outcome inspection/pre-reg leak, no Binance/2024 conflation, no modeled/proxy liquidation labels as observed, no fabricated RESOLVED, no workflow edits, no network polling loop, no reopening sealed verdicts.
