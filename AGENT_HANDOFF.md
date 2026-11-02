# AGENT_HANDOFF.md (DURABLE — SINGLE SOURCE OF TRUTH)
**TIMESTAMP (UTC):** 2026-11-02T03:24:03Z
**HANDOFF ID:** FCLR-HANDOFF-083-20261102T032403Z
**SUPERSEDES:** FCLR-HANDOFF-082-20261102T032157Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**REPO PRIORITIZATION (INFERRED):** Funding-conditioned volatility → liquidation risk (repo name is directive). Primary objective remains proving incremental value of funding/price features for volatility stress OR liquidation risk.

**INITIAL TASK MESSAGE FOR NEXT SESSION (TIMESTAMPED, MANDATORY):**
```
[2026-11-02T03:24:03Z] FOCUS CAMPAIGN: DATA_HUNT_LIQUIDATIONS_HEAVY-001
OBJECTIVE (non-optional): Find NEW admissible unauthenticated liquidation/funding data that can reopen Track A. Do NOT re-open sealed experiments (FCLR-010/OVERLAY) or H001/H003.
HEAVY WORK REQUIRED (cannot be avoided):
1. SCAN all admissible public sources per protocol §5: Binance public-data repo paths/archives, public unauthenticated exchange APIs (historical funding/mark/index/klines), public GitHub/Zenodo/HF/institutional archives with no auth/signup/payment.
2. For EACH candidate: record exact URL/endpoint, access date, test method, no-auth result, license/terms, fields, earliest/latest, cadence, symbols/venue, gaps, hashes/ETags, revision limits, rejection reason. Write to research_state/data_discovery_scan_YYYYMMDDTHHMMSSZ.md with evidence.
3. APPLY GO RUBRIC strictly: >=5 symbols, >=3 non-overlapping 30-day blocks, documented completeness (listing/delisting), license OK, historical (not live-only), no signed request/account required, no requester-pays.
4. IF ANY GO: pre-register experiment ID BEFORE outcome inspection, freeze splits with frozen_before_outcomes=true, create protocol delta, run minimal viable ingestion/tests, update handoff.
5. IF NO GO after exhausting all candidates with concrete tests: write evidence-based NO-GO with tested endpoints/archives/commits, update experiment_frontier.json, STOP. Do not create blocker memos to "wait" - produce test evidence or stop.
CONSTRAINTS: only admissible unauthenticated sources. Never merge Track A/B/C. Never promote modeled breaches to observed. Never touch .github/workflows. All tests must pass.
```

**BRANCH/HEAD:** main @ a03d9a63ea2b828f1c0c30c76ca3ff83ef6e4c87

## BOTTLENECKS REMOVED
- Integrity placeholders in FCLR-HEAVY-001 fixed (all 6 files timestamped 2026-11-02T03:21:57Z). Sealed artifacts verified unchanged.
- Campaign completed; no open loops.

## STATUS
- Track A (FCLR-010): PASSED (Hyperliquid ironflow). Overlay hypothetical only. Sealed.
- FCLR-HEAVY-001: COMPLETE (6/6). Hypothetical only.
- Track C/H001: NOT_SUPPORTED (closed). Track B/H003: CLOSED_NEGATIVE. H002: PERMANENT BLOCK (403).
- FCLR-NEXT-002: COMPLETE_NO-GO. No admissible unauthenticated liquidation source found to date.

## NEXT FOCUS CAMPAIGN (HEAVY WORK - CANNOT AVOID)
**Campaign ID:** DATA_HUNT_LIQUIDATIONS_HEAVY-001
**Priority:** CRITICAL (only route to new confirmatory work).
**Effort:** Heavy (systematic scan + evidence).
**Success criterion:** Either (a) GO candidate found with full evidence + pre-registered experiment ready to run, or (b) complete evidence NO-GO across all tested admissible sources.

**Targets to test (concrete):**
- Binance public-data: check fundingRate/klines/markPriceKlines/indexPriceKlines/premiumIndexKlines/liquidation? (look for any liquidation directories/files historically) across 2019-2024 for USDⓈ-M; test small date ranges.
- Public APIs: Bybit/OKX/Deribit historical funding/mark/index (unauthenticated) - check depth/gaps; explicitly reject auth-required.
- Archives: CoinAPI public samples? No. Check GitHub repos mentioning "liquidation" + "perpetual" with downloadable CSV/JSON (unauthenticated). Check Zenodo/HF for liquidation datasets (filter no-auth/download).
- Hyperliquid: we already used ironflow (admissible). Check if newer blocks exist? Only if unauthenticated and complete.

**Deliverables required:**
- `research_state/data_discovery_scan_20261102T032403Z.md` (per-candidate evidence table)
- If GO: `research_state/experiment_prereg_<ID>.json` + protocol delta + ingestion test passing
- If NO-GO: `research_state/data_discovery_nogo_20261102T032403Z.md` with full evidence

## HARD CONSTRAINTS
- NO Binance merge. NO reopening sealed tracks without trigger+pre-reg+split freeze.
- Tests must pass (27/27). NO changes to `.github/workflows/`.
- Only unauthenticated admissible sources. Modeled != observed.
- If no new admissible data: STOP. No "waiting for data" loops.
