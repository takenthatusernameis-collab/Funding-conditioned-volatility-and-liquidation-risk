# AGENT_HANDOFF.md (DURABLE — FCLR-HANDOFF-017)
**TIMESTAMP (UTC):** 2026-11-01T02:46:19Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**BRANCH/HEAD:** main @ 3df84bb8 (working tree: __pycache__ only)
**HANDOFF ID:** FCLR-HANDOFF-017-20261101T024619Z
**STATUS:** TERMINAL — confirmatory program exhausted. No sealed/unsealed powered panel remains untested. Reopen only under strict gate.

## INITIAL TASK MESSAGE (FOR NEXT AGENTIC SESSION) — TIMESTAMPED 2026-11-01T02:46:19Z
**PRIORITY P0 | TYPE: DATA-GATED REOPEN (NO SPECULATIVE HEAVY WORK)**

Repo name prioritizes **Funding-conditioned volatility AND liquidation risk**. Binding constraints: (1) funding-conditioned effects on realized/forecast volatility (Track C); (2) liquidation-risk transmission (Track A observed liquidations / Track B modeled breaches). Given the terminal verdict, no heavy confirmatory work is possible on current admissible data. The only work that can reopen the program is finding **new admissible unauthenticated data** meeting RESEARCH_PROMPT.md §5: ≥5 symbols, ≥3 non-overlapping 30-day blocks, unauthenticated download path, documented completeness/license, no signup/key/payment.

**DO THIS FIRST (60s):**
```bash
cd /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk
git log -1 --oneline && git status --short
python -m unittest discover -s tests -v  # must be 27/27 PASS
```

**THEN EXECUTE IN THIS ORDER (by repo-name priority):**

1. **TRACK A (OBSERVED LIQUIDATIONS) — UNBLOCK FIRST.** Read `research_state/track_a_deadend_map.md`, `research_state/liquidation_source_campaign.md`, `research_state/liquidation_sources_enumeration.md`, `research_state/binance_source_probe.md`, `research_state/data_source_registry.json`. Track A is structurally blocked/NO-GO without an admissible observed liquidation census (by symbol/time, with provenance/completeness). All candidate families already probed: Binance liquidationSnapshot HTTP 404, fapi forceOrders HTTP 451, OKX, Bybit trades (non-census), Deribit, Zenodo/OSF/arXiv, GitHub raw (401), HuggingFace ochinimus/crypto-liquidation-ticks (2026-07-08..2026-08-06 only, exhausted by FCLR-005), CryptoDataDownload, Tardis/CryptoHFTData (paywalled). **Do not** simulate/synthesize to "unlock" Track A — record the gap in `research_state/data_source_registry.json` with exact missing fields. Re-probing a dead route is not progress.

2. **TRACK C (PRICE/FUNDING/HISTORY) — VERIFY COMPLETENESS, DO NOT RE-RUN.** All confirmatory panels exhausted (FCLR-001/002/003/004/005/006/007/008; gate NOT_MET on every powered cell; FCLR-008 decisive unsealed powered panel +4.30% rel QLIKE but CI crosses zero → H001 INCONCLUSIVE). No further unsealed powered ≥3-block ≥5-symbol confirmatory cell exists without NEW admissible data + fresh pre-registered experiment ID. Do not re-run sealed panels or relax gates.

3. **TRACK B / H002 — ONLY AFTER A OR C UNBLOCKS CONFIRMATORY CAPACITY.** Track B CLOSED_NEGATIVE (FCLR-H003-EXT-001, 16 cells, Holm, no incremental skill). H002 PARTIAL replication (SSRN HTTP 403 blocks full methodology; do not promote). Do not expand B beyond complete/negative; do not pre-register without admissible data in hand.

**HARD GATES (NEVER BYPASS):**
- **New admissible unauthenticated data required** (RESEARCH_PROMPT.md §5, §16). Record source in `research_state/data_source_registry.json` before any experiment.
- **Pre-register BEFORE outcomes.** If (and only if) such data is found, **STOP and pre-register** a fresh experiment ID in `research_state/research_protocol_fclrXXX.md` with `splits/frozen_before_outcomes=true` in `run_manifest.json`. Do not inspect/fit/evaluate until pre-registered. Do not relabel exploratory as confirmatory or threshold-shop. Do not touch `.github/workflows/*`.
- **Accept terminal if none.** If no admissible unauthenticated source is found after a thorough search of documented paths and `data_source_registry.json`, **ACCEPT TERMINAL**. No dashboards/orchestrators/wrappers/polling/status-only files/placeholder docs. Commit nothing merely to show activity.

**BOTTLENECKS REMOVED:** Ambiguity removed — heavy work is data-gated and pre-registration-gated. Track A source discovery is COMPLETE_NO-GO (evidence in the artifacts above; sole reopen path is NEW admissible unauthenticated liquidation data). H002 blocked (SSRN 403, documented in `h002_replication_blocker.md`). FCLR-004 blocked (all partitions consumed, documented in `negative_results_report.md`). No session waits on an external decision. The correct focus is finding admissible liquidation/price-funding data (by repo priority), not re-running exhausted panels. Future agents must never avoid terminal acceptance when gates cannot be met, and must not manufacture heavy confirmatory work without new data + pre-registration.

**NEXT FOCUS CAMPAIGN:** `FCLR-DATA-UNBLOCK` (data discovery + provenance only). Heavy confirmatory work forbidden until gates satisfied.

## 1) STATE AT HANDOFF
- Tests: `python -m unittest discover -s tests -v` → **27/27 PASS** (verified 2026-11-01T02:46:19Z)
- FCLR-008 (decisive unsealed powered): **FORECAST_GATE_NOT_MET**, **H001 INCONCLUSIVE**, overlay **INELIGIBLE**
- Prior confirmatory exhausted (FCLR-001/002/003/004/005/006/007)
- Tracks: A structural NO-GO/blocked (needs observed liquidations), B complete-negative, H002 partial
- Reproducibility verified (byte-identical re-runs on FCLR-006/FCLR-008)

## 2) SESSION LOG (recent)
**2026-11-01T02:46:19Z - HANDOFF-017 (FCLR-DATA-UNBLOCK)**
- Supersedes HANDOFF-016. Refreshed HEAD to 3df84bb8, re-verified baseline 27/27 PASS. Made repo-name prioritization and terminal-acceptance rule explicit so future agents cannot avoid either data-gated reopening or strict terminal acceptance.
**2026-11-01T02:45:10Z - HANDOFF-016 (FCLR-DATA-UNBLOCK)**
- Supersedes HANDOFF-015. Prioritized by repo name; data-gated reopening explicit.
**2026-11-01T02:44:03Z - HANDOFF-015 (FCLR-TERMINAL)**
- Supersedes HANDOFF-014. Terminal verdict; no heavy work remains without new admissible data + pre-registration.
