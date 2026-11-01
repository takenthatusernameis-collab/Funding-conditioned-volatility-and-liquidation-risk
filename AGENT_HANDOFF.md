# AGENT_HANDOFF.md (DURABLE — FCLR-HANDOFF-019)
**TIMESTAMP (UTC):** 2026-11-01T02:49:37Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**BRANCH/HEAD:** main @ 106652ad (working tree: __pycache__ only)
**HANDOFF ID:** FCLR-HANDOFF-019-20261101T024937Z
**STATUS:** ACTIVE - INTEGRATED HEAVY CAMPAIGN (COUPLED PRIORITY BY REPO NAME)

## INITIAL TASK MESSAGE (FOR NEXT AGENTIC SESSION) — TIMESTAMPED 2026-11-01T02:49:37Z
**PRIORITY P0 | TYPE: COUPLED INTEGRATION (FUNDING-CONDITIONED VOLATILITY ∩ LIQUIDATION RISK)**

**REPO NAME IS THE SPEC:** Treat "Funding-conditioned-volatility AND liquidation-risk" as a **single coupled problem**. Do NOT silo into independent tracks - test how funding-conditioned volatility dynamics inform liquidation risk and vice versa. Prior terminal labels do not close discovery.

### MANDATORY FIRST ACTION (30s)
```bash
cd /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk
git log -1 --oneline && git status --short
python -m unittest discover -s tests -v  # MUST remain 27/27 PASS
```

### FOCUS CAMPAIGN: `FCLR-COUPLED-DISCOVERY` (FORCE HEAVY WORKING)

Execute in this exact order. **No shortcuts. No "already exhausted" without running these steps.**

#### STEP 1: LIQUIDATION RISK DISCOVERY (TRACK A) - HIGHEST BOTTLENECK
**Goal:** Find admissible observed liquidation census data (unauthenticated, no keys).
- **Read exhaustively:** `research_state/track_a_deadend_map.md`, `research_state/liquidation_source_campaign.md`, `research_state/liquidation_sources_enumeration.md`, `research_state/binance_source_probe.md`, `research_state/data_source_registry.json`
- **Probe ALL viable families:** Binance alt archives, Bybit/OKX/Deribit public data, data.binance.vision variants, GitHub raw, HuggingFace, Zenodo/OSF/arXiv, CryptoDataDownload, vendor-free mirrors. Try alternate paths/layouts/formats.
- **Rubric (MUST ALL PASS):** unauthenticated + no_keys + >=5 symbols (perp) + >=3 non-overlapping 30-day blocks + documented completeness/gaps + license OK + census/defensible event records
- **If ANY pass:** add to `data_source_registry.json` with hashes/vintages, **PRE-REGISTER** protocol before outcome inspection, freeze splits
- **If NONE pass:** write `research_state/track_a_discovery_gap_YYYYMMDDTHHMMSSZ.md` with **EVERY URL probed, HTTP status/headers, paths tried, errors, and 3-5 specific next probes** (different families/mirrors/formats). This is MANDATORY.

#### STEP 2: FUNDING-CONDITIONED VOLATILITY EXTENSION (TRACK C) - EXPAND COVERAGE
**Goal:** Find NEW admissible data to resolve FCLR-008 inconclusiveness (+4.30% but CI crosses zero).
- **Read:** `research_state/evaluation_summary_FCLR-008.md`, `research_state/research_protocol_fclr008.md`, `research_state/hypothesis_registry.json`
- **Search for:** longer/unsealed 2026 coverage, alternate symbols, different monthly layouts, delisted symbols, mark/index/funding/klines from free unauthenticated sources
- **If found:** pre-register fresh experiment ID (FCLR-009+) with `splits/frozen_before_outcomes=true` BEFORE inspecting results. Record source hashes/vintages in `run_manifest.json`
- **If NOT found:** **DO NOT** re-run existing panels. Focus on STEP 3 (integration).

#### STEP 3: COUPLED INTEGRATION TEST (FORCE PROGRESS)
**Goal:** Test the COUPLED hypothesis - funding-conditioned volatility effects on liquidation risk.
- **If STEP 1 finds admissible liquidation data:** Run integrated test H003 coupling funding-conditioned features to observed liquidation outcomes (or defensible proxies). Preserve separation (Track B modeled != observed). Apply Holm correction.
- **If ONLY STEP 2 finds data:** Run new pre-registered volatility experiment with tighter design to reduce CI width (more blocks/symbols) without threshold-shopping.
- **If NEITHER yields new admissible data:** You MUST still produce coupled analysis using existing evidence - write `research_state/coupled_integration_analysis_YYYYMMDDTHHMMSSZ.md` synthesizing FCLR-008 (+4.30% direction) with Track A blockage, H002 partial results, proposing **specific testable hypotheses** with concrete data needs and exact probe plan. No status-only report.

### BOTTLENECK REMOVAL (ENFORCED)
- **Ambiguity kills progress:** "terminal/exhausted" is ONLY acceptable if after completing ALL steps with documented evidence you prove no admissible route exists. Default = CONTINUE DISCOVERY.
- **Force heavy working:** Breadth probes required. Try 5-10 materially different source families minimum before concluding.
- **Pre-registration is a GATE:** Finding data != running. Freeze protocol/splits before outcomes. New experiment IDs for new panels.
- **No busywork:** No dashboards/orchestrators/wrappers/polling/status-only files. No `.github/workflows/*` changes. Commit nothing just for activity.
- **Integrity:** Preserve negatives, correct for multiplicity, block-aware inference. No threshold-shopping or relabeling exploratory as confirmatory.
- **Efficiency:** Remove any redundant/confusing handoff artifacts blocking next agent - keep ONLY this file as the single durable handoff reference.

### CURRENT STATE (DO NOT RE-LITIGATE)
- Tests: 27/27 PASS
- FCLR-008: INCONCLUSIVE (+4.30% C2 vs B1, CI crosses zero) - first positive direction unsealed
- Track A: BLOCKED for 2024 (all sources exhausted per evidence) - needs new source
- Track B: SEALED_NEGATIVE (no robust skill)
- H002: PARTIAL (direction matches paper, not significant)
- All prior confirmatory exhausted

### REQUIRED END-OF-SESSION OUTPUT
1. **What changed and why** (concrete files/lines)
2. **What was actually tested** (exact commands + outcomes)
3. **Evidence added** (probes with URLs/status/headers/paths tried, hashes if data found)
4. **Gate states per track** (A/B/C/H002/H003) with evidence
5. **Single highest-value next task** (executable without user intervention)
6. **Precise verify command** for next task
7. **Blockers + next materially different free route** OR proof of exhaustive search with concrete next probes

**MANDATE:** Prioritize by repo name - COUPLE funding-conditioned volatility with liquidation risk. Do heavy discovery. Never avoid heavy working.
