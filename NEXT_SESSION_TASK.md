# NEXT_SESSION_TASK — 2026-11-11T20:07:07Z
**Execute:** `HANDOFF_NEXT_SESSION.md` (single durable handoff, authoritative). Do not execute this file or `AGENT_HANDOFF.md`.

## Immediate objectives (heavy, no status-only)
- **Branch 1 (CONDITIONAL):** only on valid Gate 4 `RESOLVED_VERIFIED` terms artifact (all 8 fields, `fabricated=false`, human/legal attestation) run deterministic promotion + `--expect-go` validators → on all-green GO execute confirmatory Track C multi-split ablation and emit verdict + atomic state updates. **Currently absent → BLOCKED.**
- **Branch 2 (DEFAULT, PRIORITY): `GAP-TRACKA-SYMBOL-EXPANSION-2026M05M10` (TRACKA-HL-EXPANSION-20261111T195500Z, prereg frozen).**
  1. Finalize ex-ante universe selection (labels/acquirability only) and emit `research_state/tracka_hl_expansion_universe_<UTC>.json|.md`.
  2. Bounded first-time unauthenticated acquisition for missing/partial expansion-symbol funding+candles (2026-05..2026-10) with provenance; verify coverage, do not re-fetch valid cached data; emit acquisition report.
  3. Build deterministic RV-augmented expansion panel + build report.
  4. Run pre-registered C2 vs B1 evaluation (QLIKE, 7d embargo, >=3 30d blocks, >=5 instruments, bootstrap, >=2%) and emit verdict.
  5. Update `experiment_frontier.json`, `hypothesis_registry.json`, `run_manifest.json`, `final_confirmatory_verdict.md` atomically.
  6. If infeasible under prereg minima, document with evidence, update state, pivot to `GAP-VOLATILITY-UNTESTED-ADMISSIBLE-PANELS` (new prereg before outcomes).

## Known facts (verified 2026-11-11)
- Gate 4 unresolved (no RESOLVED artifact). Early Track A 2025-11..2026-04 **INADMISSIBLE**; 9-symbol Track A 2026-05..2026-10 **NOT_MET** (closed).
- Expansion prereg/probe ready: `research_state/tracka_prereg_hyperliquid_expansion_20261111T195500Z.json`, `research_state/tracka_hl_expansion_probe_report_20261111T195336Z.json`. Partial expansion caches exist for `ZEC,NEAR,UNI,AAVE,CRV,ADA,LTC,BCH` (verify funding coverage/pagination to 2026-10-31); `DOT,HBAR,FIL,TRX,ICP,ALGO,ETC` lack caches.

Obey all hard bans in `HANDOFF_NEXT_SESSION.md`.
