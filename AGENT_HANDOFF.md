# AGENT HANDOFF — 2026-11-13T17:12:25Z

## PROJECT
`Funding-conditioned-volatility-and-liquidation-risk` — empirical research only (no trading). Investigate whether extreme funding, realized volatility, and pre-specified delayed/smoothed-price features improve out-of-sample forecasts of future volatility / liquidation-related stress, with leakage-resistant evaluation and preserved negative results.

## STATE (durable, sealed)
- **Cached heavy-data frontier: EXHAUSTED.** All frozen preregistered cells in `FCLR-NEXT-CAMPAIGN-20261113T091500Z` (rank 0, ACTIVE_HEAVY_CAMPAIGN) are **COMPLETED, GATE PASS, terminal**:
  - FCLR-011 (2026-05..2026-08): **PASS** (rel QLIKE 4.94%, CI excludes zero).
  - FWD-VOL-011-CONFIRM (2026-08..2026-10): **NOT_REPLICATED** (rel -5.55%, CI favours B1).
  - LIQ-010-CONFIRM (17 HL symbols): **NOT_REPLICATED** (rel 0.501% < 2%, LOIO 0/17, placebo fail).
  - EXP-ROBUST / EXP-ROBUST-REDO: **FRAGILE** (LOIO 4/8, placebo fail).
  - FWD-VOL-2025-CROSS: **NOT_REPLICATED** (+0.29%, CI crosses zero).
  - FWD-VOL-2024Q4-CROSS: **NOT_REPLICATED** (-20.77%, LOIO 0/5, placebo fail).
  - FWD-VOL-2025H2-CROSS: **NOT_REPLICATED** (-8.97%, CI favours B1).
  - FWD-VOL-2025Q1Q2-CROSS: **NOT_REPLICATED** (+0.23%, CI crosses zero, LOIO 0/5, placebo fail).
- **Hypotheses:** 31 in `research_state/hypothesis_registry.json`, all `terminal: true`. **Resume triggers:** 4 in `research_state/resume_trigger_registry.json`, all `OPEN`, `do_not_act_until_satisfied: true` (GATE4_BRANCH_1, NEW_OBSERVED_LIQUIDATION_SOURCE, HL_LABEL_EXTENSION, EXPANSION_ROBUSTNESS_REDO).
- **Blocked externally:** Gate 4 Branch 1 requires valid `research_state/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` (status=RESOLVED_VERIFIED, fabricated=false, human/legal attestation) — never agent-set. HL label extension needs ≥100d depth AND verified post-2026-10-31 observed labels. Expansion robustness redo requires a newly preregistered design meeting LOIO≥6/8 AND placebo true > p95 (no re-scoring sealed 19.04%).

## THIS SESSION (heavy work completed) — TASK-20261113T162742Z
- Executed bounded alternative liquidation-label source discovery per RESEARCH_PROMPT §5/§16:
  - `python3 scripts/hunt_alternative_liquidation_sources.py` → `research_state/alt_source_scan_latest.json` (generated_utc **20261113T171152Z**, 22 candidates, HF search cache 2026-11-13T09:01:05Z, source=cache).
  - `python3 scripts/deep_review_alt_sources.py` → `research_state/alt_source_deep_review_latest.md` (**timestamp_utc 2026-11-13T17:12:25Z**, 14 fresh probes, 0 cache hits) with per-source assessment against §16 minima.
  - Probe evidence persisted in `research_state/url_probe_cache.json`.
- **Result: 0 GO / 0 admissible NEW observed-liquidation sources.**
  - Ironflow/HL: already integrated/exhausted (not new; HL extension trigger OPEN).
  - Closest: `ochinimus/crypto-liquidation-ticks` (unauth, cc-by-4.0) but coverage ~27d (<1 complete month, <3×30d blocks) — fails minima; `nick128373/crypto-liquidation-ticks` lacks evidenced coverage/instruments/blocks — fails minima. No §16 admissibility audit warranted; **no prereg/outcomes computed**.
  - Others fail: auth required (CoinAPI 401, Coinglass key-missing), commercial/restricted (Tardis/Kaiko/Glassnode), missing liquidation census paths (Bybit/OKX/Binance vision 404), DeFi lending/OEV/on-chain or heatmap/derived or non-liquidation datasets (Chainticks, carrierone, tanod, pCwOrM, PhysiAI, transcript/pension false positives), library-not-dataset (cryptofeed). Exact per-source failing minima: `research_state/alt_source_deep_review_latest.md`.
- Updated `research_state/experiment_frontier.json` rank 0 `last_checked/blockers/next_action_heavy` to reflect clean stop.

## SINGLE DURABLE INITIAL TASK FOR NEXT SESSION (timestamped, unambiguous)
**TASK-NEXT (effective 2026-11-13T17:12:25Z): CLEAN STOP — no heavy cached work remains. Do NOT re-run terminal cells, do NOT poll Gate 4/HL labels, do NOT produce status-only churn.**

Resume heavy work **only** on materially new evidence satisfying a resume trigger:
1. **NEW_OBSERVED_LIQUIDATION_SOURCE (P1):** if a specific candidate not falsified in `alt_source_deep_review_latest.md` (2026-11-13T17:12:25Z) appears, perform `research_state/<source>_admissibility_audit_<UTC>.{md,json}` proving §16 minima (unauthenticated, provenance+license, observed labels only, venue-consistent, ≥5 instruments, ≥1 complete month OR ≥3 non-overlapping 30-day blocks) **before any prereg/outcomes**. If `status=ADMISSIBLE`: freeze prereg pre-outcomes → build/eval → terminal verdict → fail-closed gate → atomic hypothesis/frontier updates. If inadmissible: record exact failing minima and stop.
2. **GATE4_BRANCH_1:** only on valid `research_state/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` (status=RESOLVED_VERIFIED, fabricated=false, human/legal attestation).
3. **HL_LABEL_EXTENSION:** only when HL/ironflow shows ≥100d depth AND verified post-2026-10-31 observed labels (no polling).
4. **EXPANSION_ROBUSTNESS_REDO:** only with a newly preregistered design meeting LOIO≥6/8 AND placebo true > p95 (never re-score sealed 19.04%).

If none satisfied: state "no trigger satisfied; cache frontier exhausted; alt-source scan 2026-11-13T17:12:25Z = 0 GO" and stop cleanly.

## KEY ARTIFACTS
- `research_state/alt_source_deep_review_latest.md` — per-source §16 evidence (this session)
- `research_state/alt_source_scan_latest.json`, `research_state/data_source_registry_alt_hunt.json`, `research_state/url_probe_cache.json`, `research_state/hf_search_cache.json`
- `research_state/experiment_frontier.json` (rank 0 updated), `research_state/hypothesis_registry.json`, `research_state/resume_trigger_registry.json`
- `scripts/hunt_alternative_liquidation_sources.py`, `scripts/deep_review_alt_sources.py`

**This is the single durable handoff. `FOCUS_CAMPAIGN.md`/`HANDOFF_NEXT_SESSION.md`/`NEXT_SESSION_TASK.md` are redirects.**
