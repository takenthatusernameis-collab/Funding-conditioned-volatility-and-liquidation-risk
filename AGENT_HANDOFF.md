# AGENT_HANDOFF.md — Durable Handoff Pointer

**Timestamp (UTC):** 2026-11-10T21:04:08Z
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Single durable handoff (authoritative initial task):** `NEXT_SESSION_TASK.md` — **execute/read immediately**.
**Program status:** `CONCLUDED_UNDER_CONSTRAINTS` — all admissible local routes exhausted with evidence (not concluded by request).

## Current state (verified)
- **Priority 1 — Track B (modeled liquidation boundary breaches): CONFIRMATORY_COMPLETE, verdict NOT_SUPPORTED.**
  - TB1 degenerate/inadmissible (zero test breaches) — `research_state/evaluation_summary_trackb_TB1_20261110T173838Z.md`.
  - TB2 confirmatory (frozen prereg `trackb_TB2_20261110T190405Z`, 2024-01-01..2024-09-30, BTC/ETH/BNB/SOL/XRP, `synthetic_boundary_breach_h168_long_10x_m0`, modeled proxy only): event-adequate (test 619/5040, 12.3%, all 5 symbols >0) but forecast gate **NOT_MET** — Log Loss B1=0.292447→C2=0.287540 (+1.68% < 2%), 95% CI [-0.010997,0.003094] crosses zero (p=0.488), Holm fails, 2 test blocks <3. **Overlay NOT ELIGIBLE.** `research_state/evaluation_summary_trackb_TB2_20261110T190405Z.md`.
- **Priority 2 — Track C / H1 (funding-conditioned volatility):** concluded **NOT_SUPPORTED** (FCLR-003/008/009/012-V/013/014 exhausted). Overlay INELIGIBLE.
- **Priority 3 — Track A (observed liquidations):** **STRUCTURALLY_BLOCKED** (no admissible unauthenticated observed-liquidation census). Not locally repairable. Track B ≠ observed liquidations.

## `next_unfinished_task` (singular)
**NONE — pending a new admissible unauthenticated source.**
Reopen only with: (a) new admissible unauthenticated source + verifiable provenance/coverage/terms, (b) new experiment ID, (c) new prereg frozen **before** outcomes. No polling, status-only work, relitigation, threshold shopping, or sealed-holdout reuse.

## Bottlenecks addressed this session
- Repaired corrupted/stale `research_state/experiment_frontier.json` to a valid, consistent concluded-state frontier.
- Replaced/synchronized durable handoffs (`NEXT_SESSION_TASK.md`, `AGENT_HANDOFF.md`, `FOCUS_CAMPAIGN.md`) with a timestamped (2026-11-10T21:00:33Z) single unambiguous initial task: `NONE` under constraints, with explicit reopen conditions and evidence pointers.

## Constraints (NON-NEGOTIABLE)
No network/paid/manual/credentialed data; no fabricated data/provenance; no threshold shopping; no sealed-holdout reuse; no Track A/B/C conflation (Track B = modeled synthetic breach proxy only); preregister/freeze before outcomes; no risk overlay until forecast gate passes; no `.github/workflows` edits.
