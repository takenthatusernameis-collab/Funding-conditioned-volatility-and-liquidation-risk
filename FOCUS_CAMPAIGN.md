# FOCUS_CAMPAIGN.md — Heavy-Work Execution Plan

**Timestamp (UTC):** 2026-11-11T02:37:44Z
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Program status:** `CONCLUDED_UNDER_CONSTRAINTS` — all admissible local routes exhausted with evidence.
**Single durable handoff (authoritative initial task):** `NEXT_SESSION_TASK.md` → `next_unfinished_task: NONE` pending a new admissible unauthenticated source.

## Repo-name prioritized outcome (closed under constraints)
1. **Funding-conditioned volatility (Track C/H1):** NOT_SUPPORTED (all claim-worthy local panels exhausted). `research_state/final_confirmatory_verdict.md`
2. **Liquidation-risk / modeled boundary breaches (Track B, proxy only):** CONFIRMATORY_COMPLETE NOT_SUPPORTED (TB1 degenerate; TB2 NOT_MET). `research_state/evaluation_summary_trackb_TB2_20261110T190405Z.md`
3. **Observed liquidations (Track A):** STRUCTURALLY_BLOCKED (no admissible unauthenticated census). `research_state/track_a_structural_block.md`

## Bottlenecks
**None blocking.** Registry 127/127 aligned, handoffs consolidated to single initial task, environment ready, concluded-state frontier recorded. No polling/status-only infrastructure required.

## Next campaign (only if reopened) — heavy work required
Execute only when ALL reopen conditions in `NEXT_SESSION_TASK.md` hold:
- **Heavy deliverable:** ingest/verify new admissible unauthenticated source with provenance+coverage+terms evidence recorded in-repo; define new experiment ID; freeze preregistration/protocol (hashes/boundaries in `research_state/run_manifest.json`) **before any outcome computation**; run pre-registered evaluation with leakage/split/integrity checks and record verdict artifacts.
- **Forbidden:** status-only work, polling, relitigation, threshold shopping, sealed-holdout reuse, Track conflation, fabricated provenance, network/paid/manual/credentialed data, overlay before forecast gate, `.github/workflows` edits.

If reopen conditions are not met: **stop with evidence (`NONE`).**
