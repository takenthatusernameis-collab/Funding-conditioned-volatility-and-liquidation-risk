# NEXT_SESSION_TASK — 2026-11-11T16:02:32Z
**Execute:** `HANDOFF_NEXT_SESSION.md` (single durable handoff, authoritative). Do not execute `AGENT_HANDOFF.md`.

## Immediate objectives (heavy, no status-only)
- **Track A (DONE for current prereg):** successor `TRACKA-HL-S-20261111T133430Z` fully evaluated **NOT_MET** (`research_state/evaluation_summary_TRACKA-HL-20261111T160124Z.md`); RV bottleneck removed, panel/verdict/state committed in artifacts. Do not relitigate.
- **Branch 1 — Gate 4 / Track C (CONDITIONAL, external-blocked):** only on valid `fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` (human/legal, all 8 fields, `fabricated=false`, `RESOLVED_VERIFIED`) run deterministic promotion + `--expect-go` validators → on all-green GO execute confirmatory Track C multi-split ablation and emit verdict + atomic state updates. Otherwise keep BLOCKED (no bypass/fabrication).
- **Branch 2 — DEFAULT heavy campaign (while Gate 4 blocked):** produce `research_state/next_panel_gap_audit_<UTC>.md/json` (admissible liquidation-risk/volatility gaps, cached/unexploited assets, provenance/coverage). If claim-worthy: first-time unauthenticated acquisition with provenance → **pre-register before outcomes** → build panel → evaluate → emit `evaluation_summary_*` + atomic state updates. If exhausted: emit documented exhaustion audit with resume triggers. Substantive artifact required.

Obey all hard bans in `HANDOFF_NEXT_SESSION.md`.
