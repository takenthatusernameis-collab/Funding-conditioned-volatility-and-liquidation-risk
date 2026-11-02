# AGENT_HANDOFF.md (DURABLE — SINGLE SOURCE OF TRUTH)
**TIMESTAMP (UTC):** 2026-11-02T04:15:01Z
**HANDOFF ID:** FCLR-HANDOFF-085-20261102T041501Z
**SUPERSEDES:** FCLR-HANDOFF-084-20261102T040600Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**REPO PRIORITIZATION (INFERRED):** Liquidation risk > funding-conditioned volatility. Repo name is directive — liquidation data gap is the binding blocker. Primary objective: find NEW admissible unauthenticated liquidation/funding data to reopen Track A; do NOT reopen sealed negative experiments without a concrete new data source meeting pre-registration requirements.

**BRANCH/HEAD:** main @ a03d9a63ea2b828f1c0c30c76ca3ff83ef6e4c87

**INITIAL TASK MESSAGE FOR NEXT SESSION (TIMESTAMPED, MANDATORY - CANNOT SKIP):**
```
[2026-11-02T04:15:01Z] FOCUS CAMPAIGN: LIQUIDATION_DATA_HUNT_HEAVY-002 (NO FREE LUNCH)
PRIORITY: CRITICAL - ONLY PATH TO CONFIRMATORY TRACK A. REPO NAME DEMANDS LIQUIDATION RISK FOCUS.

OBJECTIVE (NON-OPTIONAL, HEAVY WORK REQUIRED):
Find ANY admissible unauthenticated liquidation/funding dataset that satisfies GO criteria. Do NOT re-examine sealed tracks FCLR-010/OVERLAY, H001/H003. Do NOT tune on sealed holds. If no GO after exhaustive evidence, produce complete NO-GO and STOP cleanly.

MANDATORY EXECUTION STEPS (DO ALL):
1. READ FIRST: AGENT_HANDOFF.md, RESEARCH_PROMPT.md §5, research_state/liquidation_source_campaign.md, research_state/final_confirmatory_verdict.md, research_state/experiment_frontier.json. Treat as authoritative.
2. SYSTEMATIC SCAN (exhaustive, evidence-based): Test ALL of the following with concrete HTTP/download attempts where feasible:
   - Binance public-data (https://github.com/binance/binance-public-data) - look for liquidation/forceOrder/liquidationSnapshot under futures/um/daily/, also check data.binance.vision paths; test small ranges 2023-2024.
   - Public unauthenticated exchange archives/APIs: Bybit, OKX, Deribit, Bitget, Gate.io, KuCoin, HTX (Huobi) - check bulk historical liquidation data availability without auth/signup/payment. Explicitly reject any requiring signed requests/keys.
   - Academic/archival: Zenodo, OSF, arXiv, Figshare, ICPSR - search for "perpetual liquidation" "funding rate" datasets (2023-2025). No-auth download required.
   - Code/data repos: GitHub raw (search via web/public index), HuggingFace datasets (filter by license, no-auth), Kaggle (reject if requires login/payment).
   - Other: CryptoQuant public pages? Glassnode? Reject if payment/auth. Check if any venue has unauthenticated liquidation history.
3. EVIDENCE PER CANDIDATE (write to research_state/liquidation_hunt_002_YYYYMMDDTHHMMSSZ.md): exact URL/endpoint, access_date (UTC), test_method (curl/wget/python), HTTP status/headers/ETags/hashes, no-auth result (Y/N), license/terms, fields/schema, earliest/latest timestamps, cadence, symbols/venue/contract type, listing/delisting/completeness, gaps, file sizes/revisions, rejection reason. NO VAGUE "NOT FOUND".
4. GO RUBRIC (STRICT): >=5 symbols, >=3 non-overlapping 30-day blocks, documented completeness (listing/delisting), license allows research use, historical (not live-only), no signed request/account required, no requester-pays. ALL must hold.
5. IF ANY GO: pre-register experiment ID BEFORE inspecting any outcomes, freeze splits with frozen_before_outcomes=true, create research_state/experiment_prereg_<ID>.json + protocol delta, implement minimal ingestion outside .github/workflows with tests, update AGENT_HANDOFF.md. DO NOT SKIP PRE-REG.
6. IF NO GO AFTER EXHAUSTING ALL CANDIDATES WITH CONCRETE TEST EVIDENCE: write research_state/liquidation_hunt_002_nogo_YYYYMMDDTHHMMSSZ.md with full per-candidate evidence table, update experiment_frontier.json to reflect NO-GO with evidence, STOP CLEANLY. NO "waiting", NO retry loops without new evidence.

CONSTRAINTS: Only admissible unauthenticated sources. Never merge Track A/B/C. Never promote modeled breaches to observed liquidations. Never touch .github/workflows. Tests must pass. Keep raw data out of git. Commit only code/manifests/reports.
```

## BOTTLENECKS REMOVED
- Consolidated to single durable handoff (this file). No duplicate handoff files.
- All sealed artifacts verified intact (FCLR-HEAVY-001 integrity OK). No reopening of closed negative tracks.
- Tests: `python -m unittest discover -s tests -v` passes (27/27).
- No workflow modifications. No redundant controllers/schedulers added.

## CURRENT STATUS (AUTHORITATIVE)
- **H001 (volatility forecasting): NOT_SUPPORTED** (FCLR-003) — forecast gate failed. No risk overlay eligible.
- **Track A (observed liquidations): BLOCKED** for 2024 confirmatory window. Only exploratory 2026 HF data exists (FCLR-005) — insufficient blocks. No new admissible source found to date (FCLR-NEXT-001/002).
- **Track B (hypothetical boundary breach): CLOSED_NEGATIVE/INCONCLUSIVE** (FCLR-H003). No incremental skill.
- **H002 (paper replication): BLOCKED** (403, methodology/data not independently accessible).
- **Data exhaustion:** 2024 fully committed; 2025 limited (2 symbols); 2026 partial. No unsealed confirmatory window on existing data.

## NEXT FOCUS CAMPAIGN (HEAVY WORK - CANNOT AVOID)
**Campaign ID:** LIQUIDATION_DATA_HUNT_HEAVY-002
**Priority:** CRITICAL
**Effort:** Heavy (systematic exhaustive scan + concrete evidence)
**Success Criterion:** Either (a) GO candidate with full evidence + pre-registered experiment ready, or (b) complete evidence-based NO-GO across ALL tested admissible sources.

**HARD RULES:**
- Heavy work only. Superficial link checks insufficient — must attempt actual access/downloads where possible with evidence.
- If blocked by geo/rate limits, document with headers/status and move to next candidate (do not retry endlessly).
- Never fabricate data/sources.
- If no new admissible data exists after exhaustive search with evidence, STOP. No blocking/waiting loops.
