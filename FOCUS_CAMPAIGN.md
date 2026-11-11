# FOCUS_CAMPAIGN — Heavy-Work Execution Plan (Pointer)

**Timestamp (UTC):** 2026-11-11T03:38:37Z (refreshed)
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Program status:** `CONCLUDED_UNDER_CONSTRAINTS` — all admissible local routes exhausted with evidence.
**Single durable handoff (authoritative initial task):** `NEXT_SESSION_TASK.md` → **SINGULAR NEXT TASK: `NONE`** pending a new admissible unauthenticated source. Treat `AGENT_HANDOFF.md` and `HANDOFF_NEXT_SESSION.md` as pointers only.

## Repo-name prioritized outcome (closed under constraints)

1. **Funding-conditioned volatility (Track C/H1):** NOT_SUPPORTED (all claim-worthy local panels exhausted: FCLR-003/008/009/012-V/013/014). `research_state/final_confirmatory_verdict.md`
2. **Modeled liquidation boundary breaches (Track B, proxy only):** CONFIRMATORY_COMPLETE NOT_SUPPORTED (TB1 degenerate; TB2 gate NOT_MET, Log Loss +1.68% < 2%, CI crosses zero, Holm fails, 2 test blocks < 3). `research_state/evaluation_summary_trackb_TB2_20261110T190405Z.md`
3. **Observed liquidations (Track A):** STRUCTURALLY_BLOCKED (no admissible unauthenticated census). `research_state/track_a_structural_block.md`

## Bottlenecks

**None blocking.** Registry 127/127 aligned, handoffs consolidated to `NEXT_SESSION_TASK.md`, environment ready. Raw data zips/dirs at repo root clutter navigation but are not a blocker.

## Next campaign (only if reopened) — heavy work required

Execute only when **all** reopen conditions in `NEXT_SESSION_TASK.md` hold:
- Ingest/verify new admissible unauthenticated source with provenance, schema, coverage, and terms evidence recorded in-repo.
- Define new experiment ID and non-concluded claim; freeze preregistration/protocol (hashes/boundaries in `research_state/run_manifest.json`) **before any outcome computation**.
- Run pre-registered evaluation with leakage/split/integrity checks; record auditable verdict artifacts.

**Forbidden:** status-only work, polling, relitigation, threshold shopping, sealed-holdout reuse, Track A/B/C conflation, fabricated provenance, network/paid/manual/credentialed/bypassed data, overlay before forecast gate, `.github/workflows` edits.

If reopen conditions are not met: **stop with evidence (`NONE`).**

## Heavy-work enforcement for future agents

Any future agent that resumes this repo **must**:
1. First read `NEXT_SESSION_TASK.md` and verify reopen conditions are met
2. If not met: output evidence of why conditions are not met and stop — `NONE` is the only valid output
3. If met: produce a new preregistration in `research_state/run_manifest.json` BEFORE any computation
4. Execute the pre-registered evaluation end-to-end with full leakage/split/provenance audits
5. Produce auditable verdict artifacts in `research_state/` with timestamps and hashes
6. Update `experiment_frontier.json`, `hypothesis_registry.json`, and `run_manifest.json` atomically

**No exceptions. No shortcuts. No status-only output. Heavy work or stop.**

(End of file - total 27 lines)