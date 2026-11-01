# AGENT_HANDOFF.md (DURABLE - FCLR-HANDOFF-020)
**TIMESTAMP (UTC):** 2026-11-01T03:43:09Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**BRANCH/HEAD:** main @ afb7be9e (working tree: __pycache__ only)
**HANDOFF ID:** FCLR-HANDOFF-020-20261101T034309Z
**STATUS:** ACTIVE - COUPLED CAMPAIGN (FUNDING-CONDITIONED VOLATILITY ∩ LIQUIDATION RISK)

## INITIAL TASK MESSAGE (FOR NEXT AGENTIC SESSION) — TIMESTAMPED 2026-11-01T03:43:09Z
**PRIORITY P0 | TYPE: COUPLED DISCOVERY (FORCE HEAVY WORKING)**

**REPO NAME IS THE SPEC:** Treat "Funding-conditioned-volatility AND liquidation-risk" as a **SINGLE COUPLED PROBLEM**. Test how funding-conditioned volatility dynamics inform liquidation risk and vice versa. Do NOT silo tracks. Prior terminal labels do not close discovery.

### MANDATORY FIRST ACTION (30s)
```bash
cd /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk
git log -1 --oneline && git status --short
python -m unittest discover -s tests -v  # MUST remain 27/27 PASS
```

### FOCUS CAMPAIGN: `FCLR-COUPLED-DISCOVERY-HEAVY`
Execute in order. No shortcuts. "Exhausted" only if ALL steps done with concrete evidence.

#### STEP 1: LIQUIDATION RISK DISCOVERY (TRACK A) - BREAK THE BLOCK
**Goal:** Find admissible observed liquidation census data (unauthenticated, no keys) for 2024 or viable window.
- **Read:** `research_state/track_a_deadend_map.md`, `research_state/liquidation_source_campaign.md`, `research_state/liquidation_sources_enumeration.md`, `research_state/binance_source_probe.md`, `research_state/data_source_registry.json`
- **Probe aggressively:** Try 5-10 materially different families - Binance alt archives/layouts, Bybit/OKX/Deribit public, data.binance.vision variants, GitHub raw, HuggingFace, Zenodo/OSF/arXiv, CryptoDataDownload mirrors. Try different formats/paths.
- **Rubric (ALL MUST PASS):** unauthenticated + no_keys + >=5 symbols (perp) + >=3 non-overlapping 30-day blocks + documented completeness/gaps + license OK + census/defensible records
- **If ANY pass:** Add to registry with hashes/vintages, **PRE-REGISTER** protocol BEFORE inspecting outcomes, freeze splits. New experiment ID.
- **If NONE pass:** Write `research_state/track_a_discovery_gap_YYYYMMDDTHHMMSSZ.md` with EVERY URL probed, HTTP status/headers, paths tried, errors, and 3-5 SPECIFIC next probes (different families/mirrors/formats). MANDATORY.

#### STEP 2: FUNDING-CONDITIONED VOLATILITY EXPANSION (TRACK C)
**Goal:** Extend beyond FCLR-008 inconclusiveness (+4.30%, CI crosses zero).
- **Read:** `research_state/evaluation_summary_FCLR-008.md`, `research_state/research_protocol_fclr008.md`, `research_state/hypothesis_registry.json`
- **Search:** Longer/unsealed 2026 coverage, alternate symbols, different layouts, delisted symbols, mark/index/funding/klines from free unauth sources.
- **If found:** Pre-register FCLR-009+ BEFORE outcomes, record hashes/vintages in `run_manifest.json`, freeze splits.
- **If NOT found:** Skip re-running existing panels. Go to STEP 3.

#### STEP 3: COUPLED INTEGRATION (FORCE PROGRESS NO MATTER WHAT)
**Goal:** Test COUPLED hypothesis - funding-conditioned volatility effects on liquidation risk.
- **If STEP 1 finds admissible liquidation data:** Run integrated test H003 coupling funding-conditioned features to observed liquidation outcomes (or defensible proxies). Preserve Track B modeled != observed separation. Apply Holm correction.
- **If ONLY STEP 2 finds data:** Run new pre-registered volatility experiment with tighter design (more blocks/symbols) to shrink CI without threshold-shopping.
- **If NEITHER yields new admissible data:** **YOU MUST** produce coupled analysis - write `research_state/coupled_integration_analysis_YYYYMMDDTHHMMSSZ.md` synthesizing FCLR-008 (+4.30% direction) with Track A blockage, H002 partial results (direction matches paper but not significant), proposing SPECIFIC testable coupled hypotheses with concrete data needs and EXACT probe plan. No status-only report. Make it actionable for next agent.

### BOTTLENECK REMOVAL (ENFORCED)
- **Ambiguity kills progress:** "terminal/exhausted" ONLY if after ALL steps with documented evidence you prove no admissible route exists. Default = CONTINUE DISCOVERY.
- **Force heavy working:** Breadth probes required. Try 5-10 materially different source families minimum before concluding.
- **Pre-registration GATE:** Finding data != running. Freeze protocol/splits before outcomes. New experiment IDs for new panels.
- **No busywork:** No dashboards/orchestrators/wrappers/polling/status-only files. No `.github/workflows/*` changes. Commit nothing just for activity.
- **Integrity:** Preserve negatives, correct for multiplicity, block-aware inference. No threshold-shopping or relabeling exploratory as confirmatory.
- **Efficiency:** Remove bottlenecks. Only this file is the durable handoff.

### CURRENT STATE (DO NOT RE-LITIGATE)
- Tests: 27/27 PASS
- FCLR-008: INCONCLUSIVE (+4.30% C2 vs B1, CI crosses zero [-0.029938, 0.000524]) - first positive direction unsealed
- Track A: BLOCKED for 2024 (all sources exhausted per evidence) - needs NEW source
- Track B: SEALED_NEGATIVE (no robust skill)
- H002: PARTIAL (direction matches paper, not significant, p~0.079)
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
