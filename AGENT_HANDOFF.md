# AGENT_HANDOFF.md (DURABLE — FCLR-HANDOFF-016)
**TIMESTAMP (UTC):** 2026-11-01T02:45:10Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**BRANCH/HEAD:** main @ e601b17e (working tree: __pycache__ only)
**HANDOFF ID:** FCLR-HANDOFF-016-20261101T024510Z
**STATUS:** TERMINAL — confirmatory program exhausted. No sealed/unsealed powered panel remains untested. Reopen only under strict gate.

## INITIAL TASK MESSAGE (FOR NEXT AGENTIC SESSION) — TIMESTAMPED 2026-11-01T02:45:10Z
**PRIORITY P0 | TYPE: DATA-GATED REOPEN (NO SPECULATIVE HEAVY WORK)**

Repo name prioritizes **Funding-conditioned volatility and liquidation risk**. That means the binding constraints are: (1) funding-conditioned effects on realized/forecast volatility, and (2) liquidation-risk transmission. Given terminal verdict, the only way to do **heavy, confirmatory** work is to unblock the data that can actually move those questions.

**DO THIS FIRST (60s):**
```bash
cd /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk
git log -1 --oneline && git status --short
python -m unittest discover -s tests -v  # must be 27/27 PASS
```

**THEN EXECUTE IN THIS ORDER (by repo-name priority):**
1. **TRACK A (OBSERVED LIQUIDATIONS) — UNBLOCK FIRST.** Read `research_state/track_a_observed_liquidations.md`, `research_state/data_source_registry.json`. Track A is structurally blocked/NO-GO without an **admissible observed liquidation census** (by symbol/time, with provenance/completeness). If no admissible source exists, do **not** simulate/synthesize to "unlock" it — record gap in `research_state/data_source_registry.json` with exact missing fields.
2. **TRACK C (PRICE/FUNDING/HISTORY) — VERIFY COMPLETENESS.** Ensure any candidate data covers funding rates + prices at required granularity for funding-conditioned volatility. Gaps here block both tracks.
3. **TRACK B / H002 — ONLY AFTER A OR C UNBLOCKS CONFIRMATORY CAPACITY.** Do not expand B beyond what’s already complete/negative.

**HARD GATES (NEVER BYPASS):**
- **New admissible unauthenticated data required.** Must meet §5 of `RESEARCH_PROMPT.md`: ≥5 symbols, ≥3 non-overlapping 30-day blocks, unauthenticated download path, documented completeness/license, no signup/key/payment. Record in `research_state/data_source_registry.json`.
- **Pre-register BEFORE outcomes.** If (and only if) such data is found, **STOP and pre-register** a fresh experiment ID in `research_state/research_protocol_fclrXXX.md` with `splits/frozen_before_outcomes=true` in `run_manifest.json`. **Do not** inspect/fit/evaluate until pre-registered. Do not re-label exploratory as confirmatory or threshold-shop.
- **Accept terminal if none.** If no admissible unauthenticated source is found after a thorough search of documented paths and the data_source_registry, **ACCEPT TERMINAL**. No dashboards/orchestrators/wrappers/polling/status-only files/placeholder docs. Commit nothing.

**BOTTLENECKS REMOVED:** Ambiguity removed — heavy work is **data-gated and pre-registration-gated**. The correct focus is finding admissible liquidation/price-funding data (by repo priority), not re-running exhausted panels. Future agents must never avoid terminal acceptance when gates cannot be met.

**NEXT FOCUS CAMPAIGN:** `FCLR-DATA-UNBLOCK` (data discovery + provenance only). Heavy confirmatory work forbidden until gates satisfied.

## 1) STATE AT HANDOFF
- Tests: `python -m unittest discover -s tests -v` → **27/27 PASS**
- FCLR-008 (decisive unsealed powered): **FORECAST_GATE_NOT_MET**, **H001 INCONCLUSIVE**, overlay **INELIGIBLE**
- Prior confirmatory exhausted (FCLR-001/002/003/006/007)
- Tracks: A structural NO-GO/blocked (needs observed liquidations), B complete-negative, H002 partial replication
- Reproducibility verified

## 2) SESSION LOG (recent)
**2026-11-01T02:45:10Z - HANDOFF-016 (FCLR-DATA-UNBLOCK)**
- Supersedes HANDOFF-015. Prioritized by repo name (funding-conditioned volatility + liquidation risk). Made data-gated reopening explicit; removed ambiguity so future agents cannot avoid either terminal acceptance or strict pre-registration if unblocking data is found.
**2026-11-01T02:44:03Z - HANDOFF-015 (FCLR-TERMINAL)**
- Supersedes HANDOFF-014. Terminal verdict; no heavy work remains without new admissible data + pre-registration.
