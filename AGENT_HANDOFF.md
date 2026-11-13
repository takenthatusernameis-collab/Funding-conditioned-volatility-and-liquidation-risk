# AGENT HANDOFF — 2026-11-13T17:19:15Z (single durable handoff)

## PROJECT
`Funding-conditioned-volatility-and-liquidation-risk` — empirical research only (no trading). Investigate whether extreme funding, realized volatility, and pre-specified delayed/smoothed-price features improve out-of-sample forecasts of future volatility / liquidation-related stress, with leakage-resistant evaluation and preserved negative results.

## SINGLE DURABLE INITIAL TASK FOR NEXT SESSION (timestamped, unambiguous)
**TASK-NEXT (effective 2026-11-13T17:19:15Z): CLEAN STOP — no heavy cached work remains and no resume trigger is satisfied.**

**Do NOT:**
- Re-run terminal cells, re-open sealed verdicts, re-score sealed results, or invent new work without new admissible evidence.
- Poll/wait for Gate 4, HL label extension, or external triggers (all `OPEN`, externally blocked, `do_not_act_until_satisfied: true`).
- Produce status-only churn, redundant wrappers, polling loops, or repeated no-op probes (alt-source scan is fresh: 2026-11-13T17:12:25Z, 0 GO).

**Resume heavy work only on materially new evidence satisfying a resume trigger (priority by repo name: liquidation-risk first).** When a trigger is satisfied, execute heavy work in order — do not stop at status: (a) §16 admissibility audit artifact, (b) prereg freeze pre-outcomes, (c) build/eval panel, (d) terminal verdict, (e) fail-closed gate, (f) atomic hypothesis/frontier/trigger updates — under a NEW experiment ID.

## RESUME TRIGGERS (all OPEN — check artifacts before acting)
1. **NEW_OBSERVED_LIQUIDATION_SOURCE (P1, agent-actionable on new evidence):** if a specific candidate not falsified in `research_state/alt_source_deep_review_latest.md` (2026-11-13T17:12:25Z) appears, create `research_state/<source>_admissibility_audit_<UTC>.{md,json}` proving §16 minima **before any prereg/outcomes**: unauthenticated, provenance+license, observed labels only, venue-consistent, ≥5 instruments, ≥1 complete month OR ≥3 non-overlapping 30-day blocks. `status=ADMISSIBLE` → freeze prereg pre-outcomes → build/eval → terminal verdict → fail-closed gate → atomic updates. Inadmissible → record exact failing minima and stop.
2. **GATE4_BRANCH_1 (P2, non-agent-actionable):** only on valid `research_state/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` with `status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal attestation. Agents cannot create this file; do not wait/poll.
3. **HL_LABEL_EXTENSION (P3, non-agent-actionable now):** only when HL/ironflow shows ≥100d depth AND verified post-2026-10-31 observed labels. External dependency; ineligible until evidence appears; no polling.
4. **EXPANSION_ROBUSTNESS_REDO (P4, conditional):** only with a newly preregistered design meeting LOIO≥6/8 AND placebo true > p95. Never re-score sealed 19.04%.

**If none satisfied:** state "no trigger satisfied; cache frontier exhausted; alt-source scan 2026-11-13T17:12:25Z = 0 GO" and stop cleanly.

## STATE (durable, sealed)
- **Cached heavy-data frontier: EXHAUSTED.** All frozen preregistered cells in `FCLR-NEXT-CAMPAIGN-20261113T091500Z` (rank 0, ACTIVE_HEAVY_CAMPAIGN) are **COMPLETED, GATE PASS, terminal**:
  - FCLR-011 (2026-05..2026-08): **PASS** (rel QLIKE 4.94%, CI excludes zero). Forward confirmation NOT_REPLICATED.
  - FWD-VOL-011-CONFIRM (2026-08..2026-10): **NOT_REPLICATED** (rel -5.55%, CI favours B1).
  - LIQ-010-CONFIRM (17 HL symbols): **NOT_REPLICATED** (rel 0.501% < 2%, LOIO 0/17, placebo fail).
  - EXP-ROBUST / EXP-ROBUST-REDO: **FRAGILE** (LOIO 4/8, placebo fail).
  - FWD-VOL-2025-CROSS: **NOT_REPLICATED** (+0.29%, CI crosses zero).
  - FWD-VOL-2024Q4-CROSS: **NOT_REPLICATED** (-20.77%, LOIO 0/5, placebo fail).
  - FWD-VOL-2025H2-CROSS: **NOT_REPLICATED** (-8.97%, CI favours B1).
  - FWD-VOL-2025Q1Q2-CROSS: **NOT_REPLICATED** (+0.23%, CI crosses zero, LOIO 0/5, placebo fail).
- **Hypotheses:** 31 in `research_state/hypothesis_registry.json`, all `terminal: true`.
- **Resume triggers:** 4 in `research_state/resume_trigger_registry.json`, all `OPEN`, `do_not_act_until_satisfied: true`.
- **Alt-source scan (TASK-20261113T162742Z, executed 2026-11-13T17:12:25Z): 0 GO / 0 admissible NEW observed-liquidation sources.** See `research_state/alt_source_deep_review_latest.md`. Ironflow/HL already integrated/exhausted. Closest (`ochinimus/crypto-liquidation-ticks`, ~27d coverage; `nick128373/crypto-liquidation-ticks`, no evidenced coverage/instruments/blocks) fail §16 minima. No §16 admissibility audit warranted; no prereg/outcomes computed.

## LAST HEAVY WORK (completed) — TASK-20261113T162742Z
- Executed bounded alternative liquidation-label source discovery per RESEARCH_PROMPT §5/§16:
  - `python3 scripts/hunt_alternative_liquidation_sources.py` → `research_state/alt_source_scan_latest.json` (generated_utc **20261113T171152Z**, 22 candidates, HF search cache 2026-11-13T09:01:05Z, source=cache).
  - `python3 scripts/deep_review_alt_sources.py` → `research_state/alt_source_deep_review_latest.md` (**timestamp_utc 2026-11-13T17:12:25Z**, 14 fresh probes, 0 cache hits) with per-source assessment against §16 minima.
  - Probe evidence persisted in `research_state/url_probe_cache.json`.
- **Result: 0 GO / 0 admissible NEW observed-liquidation sources.** No prereg created, no outcomes computed, no terminal cells re-run, no Gate 4/HL/external polling.
- Updated `research_state/experiment_frontier.json` rank 0 `last_checked/blockers/next_action_heavy` to reflect clean stop.

## BOTTLENECKS / NON-ACTIONABLE WAITS (must not block sessions)
- **Gate 4 Branch 1:** human/legal attestation only — agents cannot create `fclr016_v5_terms_evidence_RESOLVED_*.json`. Mark non-agent-actionable; do not wait.
- **HL label extension:** needs new observed post-2026-10-31 labels + ≥100d depth — external data dependency; ineligible until evidence appears; no polling.
- **Expansion robustness redo:** needs new preregistration with LOIO≥6/8 AND placebo > p95 — a new design, not a re-score of sealed 19.04%.

## FOCUS CAMPAIGN — NO AVOIDANCE OF HEAVY WORK
**Campaign ID:** `FCLR-NEXT-CAMPAIGN-20261113T091500Z` (rank 0, ACTIVE_HEAVY_CAMPAIGN, terminal closure on cached/known frontier confirmed).

Rule: when any resume trigger is satisfied, the next session **must** execute the full heavy-work chain (audit → prereg freeze pre-outcomes → build/eval → verdict → fail-closed gate → atomic updates) under a NEW experiment ID. Heavy work is not optional once a trigger is satisfied; status-only reports do not satisfy this campaign.

**Verification command:** `python -m unittest tests.test_active_campaign_gate tests.test_fclr_final_structural_closure tests.test_monitor_ironflow tests.test_trackc_panel_admissibility_audit tests.test_fclr_heavy_confirm_gate` (prior: 119 OK).

## KEY ARTIFACTS
- `research_state/alt_source_deep_review_latest.md` — per-source §16 evidence (latest scan)
- `research_state/alt_source_scan_latest.json`, `research_state/data_source_registry_alt_hunt.json`, `research_state/url_probe_cache.json`, `research_state/hf_search_cache.json`
- `research_state/experiment_frontier.json` (rank 0), `research_state/hypothesis_registry.json`, `research_state/resume_trigger_registry.json`

**This is the single durable handoff. `FOCUS_CAMPAIGN.md`/`HANDOFF_NEXT_SESSION.md`/`NEXT_SESSION_TASK.md` are redirects — do not execute them; read and update `AGENT_HANDOFF.md` only.**
