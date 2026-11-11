# NEXT_SESSION_TASK — 2026-11-11T13:45:00Z
**Execute:** `HANDOFF_NEXT_SESSION.md` (single durable handoff, authoritative). Do not execute `AGENT_HANDOFF.md`.

## Immediate objectives (heavy, terminal — no status-only)
- **Track A (PRIMARY):** Already terminally closed Path (c) this session (`evaluation_summary_TRACKA-HL-terminal-20261111T133430Z.md`, NOT_SUPPORTED). **Binding bottleneck:** mark-price/RV context for `2026-05-01..2026-10-31` not cached. **Remove it:** bounded, unauthenticated, first-time `candleSnapshot` acquisition for `2026-05-01..2026-10-31` (9 symbols, NOT redundant polling) → rebuild aligned panel with RV → execute pre-registered successor C2 vs B1 evaluation per `research_state/tracka_prereg_hyperliquid_successor_20261111T133430Z.json` → emit `research_state/evaluation_summary_TRACKA-HL-*` verdict + atomic frontier/registry/manifest/final-verdict updates. **OR** if minima still unmet after RV fetch: emit documented Path (c) terminal closure `evaluation_summary_TRACKA-HL-terminal-<UTC>.md` + atomic closure. Verdict artifact required; no status-only output.
- **Gate 4 / Track C:** EXTERNAL BLOCKER (human/legal). Keep BLOCKED; no bypass/fabrication. Act only on valid `fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` → deterministic `--expect-go` promotion → confirmatory multi-split ablation.

Obey all hard bans in `HANDOFF_NEXT_SESSION.md`.
