# AGENT HANDOFF — Funding-Conditioned Volatility and Liquidation Risk

UPDATED: 2026-10-29T23:00:00Z
HEAD: c3236af1 (main)
REPO: Funding-conditioned-volatility-and-liquidation-risk

## PRIORITY (inferred from repo name): Liquidation-risk path unblocked only via source discovery

Repo title = **Funding-conditioned volatility and liquidation risk**. Forecast gate is CLOSED (NOT_MET/BLOCKED FCLR-001-004). H002 PARTIAL_REPLICATION complete. The only remaining heavy, unblocked campaign that can move the liquidation-risk pillar forward is **Track A source discovery for FCLR-H004 (observed liquidation labels)**.

## SINGLE MANDATORY INITIAL TASK FOR NEXT AGENT

**Campaign:** `H004-SOURCE-DISCOVERY-v1`
**Objective:** Find any admissible unauthenticated public source of *complete* historical forced-liquidation event records (or defensibly partial with explicit incomplete-label design) for the frozen universe (Binance USDT-M perp symbols BTCUSDT/ETHUSDT/BNBUSDT/SOLUSDT/XRPUSDT), 2024 window relevant to tests.

**You MUST execute this in order (no shortcuts):**

1. **Read evidence**: `research_state/binance_source_probe.md`, `research_state/liquidation_sources_enumeration.md`, `RESEARCH_PROMPT.md` §§5,7.2,15.
2. **Enumerate candidates** (admissible per §5): public GitHub repos with downloadable CSV/JSON/Parquet, Zenodo, HuggingFace datasets, institutional/academic archives, other venue-native public archives. Also check alternative Binance paths (different years/layouts), Bybit/OKX/Deribit public data dirs more thoroughly, CoinAPI-like public mirrors only if truly unauthenticated bulk. Explicitly reject anything requiring login/API keys/payment/manual upload.
3. **Probe each candidate** with small unauthenticated requests (curl/wget/python requests), bounded retries/backoff. For each record: exact URL/endpoint, access time (UTC), method, HTTP/code, auth required?, license/terms notes, fields/schema, earliest/latest timestamps, venue/symbol coverage, cadence, completeness indicators (gaps/truncation), file hashes/ETags if any, **rejection reason**.
4. **Write/update** `research_state/liquidation_sources_enumeration.md` with a ranked table (source, admissible Y/N, complete-census plausible Y/N, covers frozen universe/time?, quality notes, verdict). Be explicit about *completeness* - a capped sample is NOT a census; absence ≠ zero liquidations.
5. **Decision gate**: If any source passes **direct-label quality gate** (defensible provenance, temporal coverage for needed window, meaning of "observed forced liquidation" matches, completeness support or explicit incomplete-label design that is acceptable per protocol), set **FCLR-H004 Track A = VIABLE**, write `research_state/fclr_h004_tracka_viable.json` (or append to enumeration) with concrete label construction plan + next steps. If NONE pass, set **Track A = BLOCKED with structural evidence**, do **NOT** infer event-free intervals, and state Tracks B/C remain the only paths for liquidation-adjacent work.
6. **Verify constraints**: no new bulk downloads beyond small bounded probes; no credentials; no sealed holdouts; no forecast-gate re-attempts.

## BOTTLENECKS REMOVED / HARD CONSTRAINTS

- **Forecast gate is SEALED.** DO NOT re-run/re-attempt FCLR-001/FCLR-002/FCLR-003/FCLR-004 forecast evaluations. Status: NOT_MET/BLOCKED. All forecast test windows exhausted per protocol.
- **Do NOT touch `.github/workflows`.**
- **Do NOT do risk-overlay/trading/simulation/merge tracks.**
- **Preserve distinctions.** Never conflate correction-time (H002), hypothetical boundary breaches (H003/Track B), or volatility (Track C) with observed liquidations (Track A).
- **pytest note:** `pytest` unavailable; use `python -m unittest tests.test_funding_correction_replication -v` (10/10 pass).
- **H002 done:** RV-regime contrast infeasible (Jan-Mar 2024 mark prices missing, no downloads) - documented; SSRN 403 blocks full methodology - documented as PARTIAL_REPLICATION.
- **H004 blocked but actionable:** Only via source discovery above.

## IMMEDIATE ACCEPTANCE CRITERIA (for this session)

- [ ] `research_state/liquidation_sources_enumeration.md` updated with **ranked source table + concrete probes** (URLs, codes, coverage, completeness, rejection reasons)
- [ ] Explicit **Track A viability decision** recorded (VIABLE with plan OR BLOCKED with structural evidence)
- [ ] If VIABLE: concrete, minimal next steps to build labels without bulk-pulling outside admissible paths
- [ ] If BLOCKED: state this clearly; do **NOT** pivot to re-attempting forecast gates
- [ ] No workflow changes, no forecast re-runs

## CURRENT STATE SNAPSHOT

- **H001:** INCONCLUSIVE
- **H002:** PARTIAL_REPLICATION (complete 2026-10-29T22:54:25Z) - 88 events, 84 corrected/4 censored, median 8.0h; RV-regime contrast not computable
- **H003:** INCONCLUSIVE (no incremental skill over volatility baseline)
- **H004:** BLOCKED → **UNBLOCK VIA SOURCE DISCOVERY ONLY**
- **Forecast gate:** NOT_MET/BLOCKED across FCLR-001-004
- **Risk-overlay:** INELIGIBLE

## EVIDENCE FILES

- Handoff: `AGENT_HANDOFF.md` (this file)
- H002: `research_state/h002_replication_report.md`, `research_state/hypothesis_registry.json`, `research_state/run_manifest.json`
- H004: `research_state/binance_source_probe.md`, `research_state/liquidation_sources_enumeration.md`
- Protocol: `RESEARCH_PROMPT.md`, `research_state/research_protocol*.md`

**START NOW. Do heavy work on source discovery. Leave no ambiguity about next steps for the following agent.**
