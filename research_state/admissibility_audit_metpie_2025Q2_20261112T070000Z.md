# §16 Admissibility Audit — metpie/hyperliquid-liquidation-events 2025-03-22..2025-05-25 joined to HL funding+candles

**Audit ID:** `admissibility_audit_metpie_2025Q2_20261112T070000Z`
**Timestamp (UTC):** 2026-11-12T07:00:00Z
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk` (priority: funding-conditioned volatility AND liquidation risk)
**Protocol:** RESEARCH_PROMPT.md §16; HANDOFF_NEXT_SESSION.md PRIMARY route step 2

## 1. Gate 4 Branch 1 trigger check

Verified absent: no `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_RESOLVED_*.json` with `status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal attestation. Highest local artifact: `fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json` (`status=EXPLICIT_BLOCKER_UNRESOLVED`, `fabricated=false`, `confirmatory_claim_go=NO_GO`). Gate 4 Branch 1 NOT executable this session; not agent-removable. Do not wait/poll.

## 2. Metpie source: hyperliquid-liquidation-events (GitHub)

| Property | Evidence |
|---|---|
| Source URL | https://github.com/metpie/hyperliquid-liquidation-events |
| API URL | https://api.github.com/repos/metpie/hyperliquid-liquidation-events (HTTP 200, public, unauthenticated) |
| Description | "346k liquidation trades across 179 Hyperliquid perp markets, Mar-May 2025 (from public node-trade data)" |
| License | CC BY 4.0 (per README, recorded in prior probes) |
| Local cache | `research_state/data_cache/metpie_liq/liquidation_events.csv.gz` (6,736,079 bytes, 346,130 rows) |
| Schema | `time` (ms), `coin`, `px`, `sz`, `side`, `liquidated_start_pos`, `hash`, `notional_usd` |
| Time range | 2025-03-22T10:56:26Z to 2025-05-25T14:23:20Z (~64.1 days) |
| Unique coins | 179 |
| Label type | Observed liquidation events (node-trade archive, `trade_dir_override = "LiquidatedMarket"`), NOT modeled/proxy/synthetic |
| Venue consistency | Hyperliquid perpetuals only |

**Symbol coverage (events per coin):**
- ≥5,000 events: BTC (84,640), ETH (43,947), SOL (32,549), HYPE (17,451), XRP (16,185), POPCAT (12,749), FARTCOIN (10,119), kPEPE (9,828), TRUMP (9,586), SUI (7,907), kBONK (5,499) → 11 coins
- ≥1,000 events: 39 coins
- ≥5 instruments with meaningful label coverage: PASS (11 coins ≥5,000 events)

## 3. Hyperliquid funding + candles for the exact window (2025-03-22..2025-05-25)

| Property | Evidence |
|---|---|
| Endpoint | https://api.hyperliquid.xyz/info (unauthenticated, POST, no API key, no signature, no requester-pays) |
| `candleSnapshot` interval=4h | HTTP 200 for all 11 top symbols; 390 rows each; complete window coverage (2025-03-22 to 2025-05-25), no gaps |
| `fundingHistory` | HTTP 200; first page capped at 500 rows (~20.8 days at hourly cadence); paginatable in 21-day chunks; BTC full window = 1,548 rows across 4 chunks with 3 minor gaps (>1.5h); range 2025-03-22 to 2025-05-25 |
| Pagination required | Yes (≥4 chunks for 64-day window); bounded, evidenced, first-time acquisition |
| Provenance recordable | `.accessed.json` + `.sha256` per coin/month, per established pattern in `scripts/tracka_hl_fetch_candles_early_4h.py` and `scripts/hyperliquid_funding_fetch.py` |

**Funding fetchability:** All 11 top symbols return fundingHistory. Full-window coverage achievable via pagination (verified for BTC: 1,548 rows, 2025-03-22..2025-05-25).

**Candle fetchability:** All 11 top symbols return 390 4h candles covering the full window.

## 4. Block-feasibility computation (§16 requirement: ≥3 non-overlapping 30-day OOS test blocks with 7d embargo)

| Parameter | Value |
|---|---|
| Window start | 2025-03-22T00:00:00Z |
| Window end | 2025-05-25T23:59:59Z |
| Window duration | ~64.1 days (≈65 calendar days) |
| Minimum required for 3 × 30-day blocks | 90 days (3 × 30) |
| Minimum required with 7-day embargo between blocks | 90 + 14 = 104 days (3 blocks + 2 embargoes) |
| Minimum required with train + val + 3 test blocks + embargoes | ≥90 + train + val + 3×7d embargo ≈ 150+ days |
| Feasible 30-day test blocks in window | 0 (64.1 < 90) |
| Feasible 30-day test blocks (even ignoring train/val/embargo) | 0 (64.1 < 90) |
| §16 minimum test blocks | 3 |
| §16 minimum instruments | 5 (PASS: 11 coins) |

**Determination on block feasibility:** NOT FEASIBLE. The ~65-day metpie window cannot contain 3 non-overlapping 30-day test blocks under any split configuration. Even 2 non-overlapping 30-day blocks (60 days) leave only ~5 days for train+val+embargo, which is insufficient for any claim-worthy evaluation.

## 5. RV/context features computability

| Feature | Computable? | Evidence |
|---|---|---|
| RV from 4h closes (rv_4h, rv_24h, rv_168h) | YES | 390 4h candles/coin, complete window |
| Funding rate (signed) | YES | Paginatable fundingHistory, full window |
| Mark/index premium | PARTIAL | fundingHistory `premium` field present; mark price not directly in candleSnapshot (close used as proxy, documented deviation) |
| EMA distance | YES | Computable from 4h closes |

## 6. Admissibility determination

**Result: INADMISSIBLE**

| §16 Criterion | Status | Evidence |
|---|---|---|
| Unauthenticated/public access | PASS | GitHub API + HL API, no auth required |
| Provenance + license documented | PASS | CC BY 4.0 (metpie README), HL public API |
| Observed labels (not modeled/proxy) | PASS | Node-trade liquidation events, tx hashes present |
| Venue consistency (Hyperliquid-only) | PASS | metpie + HL both Hyperliquid perps |
| ≥5 instruments with label coverage | PASS | 11 coins ≥5,000 events |
| ≥3 non-overlapping 30-day OOS test blocks | **NOT_MET** | Window ~65 days < 90 days required |
| Train/val/test + 7d embargo feasible | **NOT_MET** | Same shortfall; insufficient days |
| RV/context features from admissible candles | PASS | 4h candles complete for all top symbols |

**Primary failing criterion:** Block feasibility. The metpie 2025-03-22..2025-05-25 window (~65 days) is structurally too short to support ≥3 non-overlapping 30-day out-of-sample test blocks (≥90 days minimum). No split configuration, embargo adjustment, or symbol selection can remedy this data-window constraint.

## 7. Artifacts to produce

| Artifact | Path |
|---|---|
| This audit (MD) | `research_state/admissibility_audit_metpie_2025Q2_20261112T070000Z.md` |
| This audit (JSON) | `research_state/admissibility_audit_metpie_2025Q2_20261112T070000Z.json` |

## 8. Next step (per HANDOFF_NEXT_SESSION.md §(B) step 3)

Since INADMISSIBLE, advance to bounded reprobe/monitor only when plausibly eligible:
- HL 2026-11+ candles+funding: ~11.2 days available (2026-11-01..2026-11-12), far below ≥100-day threshold → NOT eligible
- Verified post-2026-10-31 observed liquidation labels: ironflow/hyperliquid-liquidations HF lastModified 2026-11-07T10:18:25Z, event files through 2026-10 only → NO post-2026-10-31 labels verified → NOT eligible
- **No polling.** Monitor only when either threshold plausibly crosses (HL ≥100 contiguous days AND ironflow files beyond 2026-10-31).
- Alternatively: Gate 4 Branch 1 only on valid `RESOLVED_VERIFIED` trigger.

**Compliance:** No outcome inspection before prereg freeze; no threshold-shopping; no sealed-holdout reuse; no Binance/2024 conflation; no modeled/proxy/synthetic labels as observed; no `.github/workflows` edits; no redundant network polling (bounded first-time acquisition only); no agent-set `RESOLVED_VERIFIED`/`fabricated=true`; no Gate 4 bypass.
