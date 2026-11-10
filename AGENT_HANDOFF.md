# AGENT_HANDOFF.md — Durable Handoff Pointer

**Timestamp (UTC):** 2026-11-10T19:01:16Z
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Single durable handoff (authoritative initial task):** `NEXT_SESSION_TASK.md` — **execute immediately**.
**Program status:** `ACTIVE_TRACKB_MANDATORY` — NOT concluded.

## Current state (verified)
- **Priority 1 — Track B (modeled liquidation boundary breaches): ACTIVE.** TB1 (`TRACKB-MODELED-BREACH-TB1-20261110T173838Z`, 2025-01-01..2026-10-31, 5x/24h long) **DEGENERATE/INADMISSIBLE** (frozen test split had 0 synthetic breaches). Prior `TRACKB-20251110T154307Z` NOT_MET/NOT_SUPPORTED. **Next mandatory route:** TB2 on 2024-01-01..2024-09-30 with NEW pre-freeze label+split having >0 frozen-test breaches.
- **Starting evidence (re-verify):** `research_state/trackb_TB2_admissibility.json`, `research_state/trackb_TB2_admissibility_2024q1q3.json`, `research_state/evaluation_summary_trackb_TB1_20261110T173838Z.md`.
- **Priority 2 — Track C / H1:** concluded **NOT_SUPPORTED** on claim-worthy local panels; no untested claim-worthy panels with >=3 blocks remain (`next_unfinished_task (Track C): NONE`).
- **Priority 3 — Track A (observed liquidations):** **STRUCTURALLY_BLOCKED** (no admissible unauthenticated observed-liquidation census).
- **Risk overlay:** **INELIGIBLE** until a forecast gate passes under frozen prereg.
- **Provenance:** funding lineage previously `PROVENANCE_OK 161` in `research_state/data_cache` — re-verify for all TB2 inputs.

## Bottlenecks removed
- Single mandatory TB2 execution path set in `NEXT_SESSION_TASK.md` (replaces ambiguous/TB1-stale routing).
- TB1 treated as event-adequacy failure; pre-freeze >0 frozen-test breach requirement enforced.
- No polling/status-only work; no relitigation of concluded tracks.

## `next_unfinished_task` (singular)
Execute Track B TB2 on 2024-01-01..2024-09-30 per `NEXT_SESSION_TASK.md`: re-verify admissibility/provenance, select NEW label+split with >0 frozen-test synthetic breaches, freeze NEW prereg+`prereg_hash` in `research_state/run_manifest.json` **before outcomes**, run confirmatory evaluation, propagate verdict/evidence. Fallback only if 2024Q1-Q3 proven inadmissible with evidence (pivot to next locally admissible uninspected route, new ID/prereg). Track C NOT_SUPPORTED. Track A STRUCTURALLY_BLOCKED. Overlay INELIGIBLE.

## Constraints (NON-NEGOTIABLE)
No network/paid/manual/credentialed data; no fabricated data/provenance; no threshold shopping; no sealed-holdout reuse; no Track A/B/C conflation (Track B = modeled synthetic breach proxies, never observed liquidations); preregister/freeze before outcomes; no risk overlay until forecast gate passes; no `.github/workflows` edits. Heavy, verifiable progress only.