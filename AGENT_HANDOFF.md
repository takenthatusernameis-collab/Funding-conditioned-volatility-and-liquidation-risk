# AGENT_HANDOFF.md (DURABLE — FCLR-HANDOFF-018)
**TIMESTAMP (UTC):** 2026-11-01T02:47:43Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**BRANCH/HEAD:** main @ 3df84bb8 (working tree: __pycache__ only)
**HANDOFF ID:** FCLR-HANDOFF-018-20261101T024743Z
**STATUS:** ACTIVE - DATA-DRIVEN HEAVY CAMPAIGN (NOT TERMINAL BY DEFAULT)

## INITIAL TASK MESSAGE (FOR NEXT AGENTIC SESSION) — TIMESTAMPED 2026-11-01T02:47:43Z
**PRIORITY P0 | TYPE: INTEGRATED UNBLOCK (FUNDING-CONDITIONED VOLATILITY + LIQUIDATION RISK)**

Repo name is the priority order. Do **not** split into "if no A then skip" — treat **Funding-conditioned volatility AND liquidation risk** as coupled. The prior terminal verdict is based on exhausted 2024 confirmatory panels with current admissible data; it does **not** close discovery.

**DO THIS FIRST (60s):**
```bash
cd /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk
git log -1 --oneline && git status --short
python -m unittest discover -s tests -v  # must remain 27/27 PASS
```

**NEXT FOCUS CAMPAIGN: `FCLR-INTEGRATED-UNBLOCK`**

Execute in strict order of repo-name priority:

### 1) TRACK A + INTEGRATION (LIQUIDATION RISK) — HEAVY DISCOVERY (BLOCKING)
Treat observed liquidations as the binding gap. Do **not** fabricate/simulate to "unlock" confirmatory status.
- Read: `research_state/track_a_deadend_map.md`, `research_state/liquidation_source_campaign.md`, `research_state/liquidation_sources_enumeration.md`, `research_state/binance_source_probe.md`, `research_state/data_source_registry.json`
- Candidate families already exhausted with evidence: Binance `liquidationSnapshot` (404), `fapi/v1/forceOrders` (451/restricted), Bybit trades (not a census), OKX, Deribit, Zenodo/OSF/arXiv, GitHub raw, HuggingFace `ochinimus/crypto-liquidation-ticks` (2026-07-08..2026-08-06 only - exhausted by FCLR-005; cannot cover 2024 frozen windows / cannot form ≥3 non-overlapping 30-day blocks for confirmatory 2024)
- **Only accept**: unauthenticated download path, census-level or defensibly complete event records with venue/symbol/time, documented completeness/truncation, license/terms, provenance. If partial/capped, explicitly model incompleteness and cannot treat absence as zero.
- **Output required**: if none found → `research_state/track_a_discovery_gap.md` with exact URLs probed, HTTP/status, headers, paths tried, and concrete "next probe" list (new families). If found → add to `data_source_registry.json` with hashes/vintages and **STOP to pre-register** before any outcome inspection.

### 2) TRACK C (FUNDING-CONDITIONED VOLATILITY) — EXTEND COVERAGE, NOT RE-RUN
FCLR-008 was decisive unsealed powered but **INCONCLUSIVE** (C2 vs B1 +4.30% rel QLIKE, CI crosses zero). Do **not** re-run sealed panels or relax multiplicity/gates.
- Find **new admissible unauthenticated** mark/index/funding/klines with longer/alternate coverage (or missing symbols/eras) that can form a **new frozen panel** meeting §14: ≥5 symbols, ≥3 non-overlapping 30-day blocks, embargoed splits, common eligible sample.
- If such coverage exists → pre-register fresh experiment (new ID) in `research_state/research_protocol_fclrXXX.md` with `splits/frozen_before_outcomes=true`, record source hashes/vintages in `run_manifest.json`. Do not inspect/fit until pre-registered.
- If only existing cached data → **do not** run another confirmatory grid; focus on integration (1)+(3).

### 3) INTEGRATED TESTS (HEAVY WORK IF DATA FOUND)
Only if (1) or (2) yields admissible data:
- **H003 integration**: test funding-conditioned effects on liquidation-relevant outcomes (Track A events or defensible Track B boundary proxies) with frozen definitions, separation preserved, Holm correction.
- **H002**: SSRN 403 blocks full methodology; only pursue if full paper/method becomes accessible via admissible unauthenticated source. Otherwise keep PARTIAL/blocked.
- **Never** merge Track B into observed liquidations. Keep separation irrefutable.

## BOTTLENECK REMOVAL RULES (ENFORCED)
- **Ambiguity killed**: "terminal" is only acceptable if after exhaustive documented search **no admissible unauthenticated source** exists for (1) or (2). Do not default to terminal.
- **Force heavy working**: if no new data found after completing (1) with concrete probes, you **must** produce `research_state/track_a_discovery_gap.md` (exhaustive) and also run a **breadth probe** of funding/mark/index archives (alternate paths, delisted symbols, different monthly/daily layouts) for Track C extension before concluding.
- **Pre-registration is a gate, not paperwork**: finding data ≠ running. Must freeze protocol/splits before outcomes.
- **No busywork**: no dashboards/orchestrators/wrappers/polling/status-only files/placeholder docs. No changes to `.github/workflows/*`. Commit nothing merely to show activity.
- **Integrity**: preserve negative results, correct for multiplicity, block-aware inference. Do not threshold-shop or relabel exploratory as confirmatory.

## CURRENT EVIDENCE BASE (DO NOT RE-LITIGATE)
- Tests: 27/27 PASS (verified 2026-11-01T02:47:43Z)
- FCLR-008: FORECAST_GATE_NOT_MET, H001 INCONCLUSIVE, overlay INELIGIBLE
- Tracks: A structurally blocked (no rubric-passing observed census), B closed-negative, H002 partial/blocked
- All prior confirmatory (FCLR-001/002/003/004/005/006/007) exhausted with evidence

## REQUIRED HANDOFF OUTPUT (END OF SESSION)
1. **What changed and why** (concrete files/lines)
2. **What was actually tested** (exact commands + outcomes)
3. **Evidence added and where** (probes, URLs, status, hashes)
4. **Gate states** per track (A/B/C/H002/H003) with evidence
5. **Single highest-value next task** (must be executable without user intervention)
6. **Precise verify command** for next task
7. **Blockers + next materially different free route** (or "NO NEW ADMISSIBLE DATA FOUND" with exhaustive proof)

**DEFAULT ACTION:** Do heavy discovery. Only accept terminal after exhaustive, documented proof. Never avoid heavy working by claiming "exhausted" without running the integrated discovery above.
