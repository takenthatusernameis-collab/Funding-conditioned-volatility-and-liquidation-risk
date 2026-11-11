# HANDOFF: Next Agentic Work Session (2026-11-11T12:00:00Z)
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk` (funding-conditioned volatility / liquidation risk)

## Single durable handoff (authoritative)
This file is the only task message to execute. `FOCUS_CAMPAIGN.md` and `NEXT_SESSION_TASK.md` point here. Do not start from older/parallel campaign notes without reconciling against this handoff.

## Hard state (do not relitigate)
- **Track B/C confirmatory program:** closed/negative on admissible 2024 data (`research_state/final_confirmatory_verdict.md`: H001 NOT_SUPPORTED). No rescue on sealed holds.
- **Gate 4 / 2025+ Binance confirmatory (Track C extension): BLOCKED (structural, external).** `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json` requires verifiable **human/legal** review of Binance Vision/Binance market-data terms. Fail-closed guards (`check_confirmatory_provenance`, `check_admissibility_package`, `scripts/fclr016_v5_preflight_summary.py`) prohibit confirmatory outcomes on 2025+ until resolved evidence exists. **No code, tests, or data work can substitute for this.**
- **Track A (observed Hyperliquid liquidations, ironflow CC BY 4.0): SOURCE GO but PANEL BLOCKED.** Prereg frozen pre-outcomes: `research_state/tracka_prereg_hyperliquid_2026.json` (2025-06..2026-10, C2 vs B1, QLIKE). Labels cached: `research_state/data_cache/ironflow_events/` (2025-05..2026-10, 2.85M rows). Alignment blocker: `research_state/tracka_hl_alignment_blocker.md` — admissible unauthenticated Hyperliquid-native context incomplete for full prereg window (fundingHistory cached 2025-11..2026-10 only; candleSnapshot/mark~2026-05..2026-10; no admissible historical index/premium/klines back to 2025-06 identified). Full prereg splits/panel not buildable as frozen.
- **Forbidden (all tracks):** no outcome inspection before (successor) prereg freeze, no Binance/2024 conflation, no modeled/proxy/synthetic labels, no threshold-shopping, no sealed-holdout reuse (FCLR-002/003/Track B/C), no `.github/workflows` edits, no network polling/redundant GETs beyond cached provenance when evidence suffices, no status-only output.

## Bottlenecks to remove (next session must execute; heavy work required)
1. **External (cannot automate):** obtain verifiable human/legal Binance terms review → create `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` (all required fields; `fabricated=false`, `status=RESOLVED_VERIFIED`, human/legal reviewer). If unavailable this session, record explicitly and continue with (2).
2. **Track A alignment closure (primary computable campaign):** bring Track A to a terminal, auditable state.
   - **(a) Exhaust path-a with evidence:** search *local/admissible cached* artifacts and documented Hyperliquid-native unauthenticated sources for mark/index/premium/klines/funding covering 2025-06..2026-10 for overlapping symbols; document provenance (URL/access date/hash/ETag/license/terms) and exact coverage in `research_state/tracka_alignment_patha_audit_<UTC>.md` (+json if useful). No Binance/2024 conflation.
   - **Decision gate:**
     - If full prereg window+context becomes admissibly complete → build aligned panel, run **pre-registered** evaluation per `tracka_prereg_hyperliquid_2026.json` (no outcome inspection before frozen inputs/checksums recorded), emit verdict artifact `research_state/evaluation_summary_TRACKA-HL-20261111T073000Z.md` and update frontier/registry/manifest/final verdict atomically.
     - If not (expected): **(b) scope-down requires NEW successor prereg before any outcome computation** — freeze `research_state/tracka_prereg_hyperliquid_successor_<UTC>.json` on the maximal overlap where labels+all required context exist (document exact window/symbols/splits/≥3 test blocks if claim-worthy), build panel, run evaluation, emit verdict artifact + atomic state updates; OR **(c) terminal closure** if no admissible aligned overlap meets prereg minimums — emit `research_state/evaluation_summary_TRACKA-HL-20261111T073000Z.md` (or successor-id) documenting alignment inadmissible/insufficient with evidence and close Track A as NOT_SUPPORTED/BLOCKED for this panel, with atomic state updates.
3. **Gate 4 promotion only after (1):** if resolved terms evidence produced, run deterministic reconciliation/promotion (frozen scope 2025-08-01..2025-10-31, 5 symbols, 5 kinds, consistent `admissibility_refs_sha256`) then:
   - `python scripts/fclr016_v5_preflight_summary.py <prov> <compl> <terms_RESOLVED> <prereg>`
   - `python scripts/fclr016_validate_v5_admissibility.py ... --expect-go`
   - `python scripts/run_funding_ablations.py --check-admissibility-package ... --expect-go`
   Only on all-green GO: execute confirmatory Track C multi-split ablation (≥7d purge/embargo, train-only normalization, block bootstrap ΔQLIKE CIs) and produce frozen evaluation artifacts. If (1) absent, do **not** fake/force GO.

## Required outputs this session (non-negotiable)
- Evidence/audit or verdict artifacts for Track A path taken (a/b/c) under `research_state/`.
- Any successor prereg (if path b) frozen **before** outcome computation, with hashes/inputs recorded.
- `run_manifest`/`experiment_frontier`/`hypothesis_registry`/final verdict updated atomically if a terminal evaluation/closure is reached.
- This handoff kept current (timestamped note of what was done, what remains, exact next command/files).

## Key refs
- Track A: `research_state/tracka_prereg_hyperliquid_2026.json`, `research_state/tracka_hl_alignment_blocker.md`, `research_state/data_cache/ironflow_events/`, `research_state/data_cache/hyperliquid_funding/`, `research_state/hl_coverage_probe.json`, `src/analysis/tracka_admissible.py`
- Gate 4: `research_state/fclr016_local_audit/fclr016_v5_*`, `scripts/fclr016_v5_preflight_summary.py`, `scripts/fclr016_validate_v5_admissibility.py`, `scripts/run_funding_ablations.py`
- Prior closeout: `research_state/final_confirmatory_verdict.md`
