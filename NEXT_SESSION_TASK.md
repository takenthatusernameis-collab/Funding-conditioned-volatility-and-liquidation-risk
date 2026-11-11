# NEXT_SESSION_TASK — 2026-11-11T20:30:00Z
**Execute:** `HANDOFF_NEXT_SESSION.md` (single durable handoff, authoritative). Do not execute this file or `AGENT_HANDOFF.md`.

## Immediate objectives (heavy, no status-only)
- **Branch 1 (CONDITIONAL):** only on valid Gate 4 `RESOLVED_VERIFIED` terms artifact (all 8 fields, `fabricated=false`, human/legal attestation) run deterministic promotion + `--expect-go` validators → on all-green GO execute confirmatory Track C multi-split ablation and emit verdict + atomic state updates. **Currently absent → BLOCKED.**
- **Branch 2 (DEFAULT, PRIORITY): `GAP-VOLATILITY-UNTESTED-ADMISSIBLE-PANELS` (co-priority volatility).**
  1. Audit cached admissible inputs and freeze **new prereg** (`research_state/tracka_prereg_volatility_<UTC>.json|.md`) for an untested volatility-forecast claim (distinct from sealed 2024 holds) BEFORE any outcome inspection.
  2. Bounded first-time acquisition only for missing inputs (provenance, cache-first); emit acquisition/gap report if performed.
  3. Build deterministic causal panel + build report (hashes, coverage, leakage/embargo).
  4. Run pre-registered evaluation (B1 vs C2, embargo, block bootstrap, minima/materiality) and emit verdict **MET/NOT_MET/INADMISSIBLE**.
  5. Update `experiment_frontier.json`, `hypothesis_registry.json`, `run_manifest.json`, `final_confirmatory_verdict.md` atomically.
  6. If infeasible, document with evidence, update state, prereg/attempt next best admissible untested claim in-session.

## Known facts (verified 2026-11-11)
- Gate 4 unresolved (no RESOLVED artifact).
- Track A expansion `TRACKA-HL-EXPANSION-20261111T195500Z` **PASS** (recorded): C2 vs B1 19.04% QLIKE reduction, CI [-5.088,-0.478], 593 pairs, 8 instruments, 3 blocks, 2026-05..2026-10 (ZEC,NEAR,UNI,AAVE,CRV,ADA,LTC,BCH). Do not rerun/retune.
- Track A 9-symbol 2026-05..2026-10 **NOT_MET** (closed); early 2025-11..2026-04 **INADMISSIBLE**. Track B/C 2024 closed negative.

Obey all hard bans in `HANDOFF_NEXT_SESSION.md`.
