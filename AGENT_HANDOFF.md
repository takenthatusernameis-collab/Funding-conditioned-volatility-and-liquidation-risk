# AGENT_HANDOFF (redirect)
**Timestamp (UTC):** 2026-11-12T09:42:33Z

Authoritative single durable handoff: **`HANDOFF_NEXT_SESSION.md`**. Read and execute it only.
- Gate 4 Branch 1 only on valid RESOLVED trigger (currently absent). Do not poll/bypass.
- Alt-source discovery completed (no new GO). No rerun without a materially new unassessed §16-admissible candidate.
- Execute campaign: Gate 4 check → bounded eligibility re-check only if plausible → triage materially new unassessed candidate → §16 audit before prereg, then prereg/build/eval/verdict under new experiment ID if admissible → else timestamped checkpoint and STOP CLEANLY. No sealed-record reopening, no status-only output.
