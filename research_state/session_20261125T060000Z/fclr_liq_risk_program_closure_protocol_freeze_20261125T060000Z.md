# FCLR-LIQ-RISK-PROGRAM-CLOSURE-02 — Protocol Freeze

**experiment_id:** FCLR-LIQ-RISK-PROGRAM-CLOSURE-02
**session_id:** session_20261125T060000Z
**session_utc:** 20261125T060000Z
**generated_utc:** 2026-11-25T06:00:00Z
**campaign_id:** FCLR-LIQ-RISK-PROGRAM-CLOSURE-02-20261125T054500Z
**campaign_start_utc:** 20261125T054500Z
**protocol_hash_bound:** RESEARCH_PROMPT.md sections 13/19/20

## Outcome-blind closure protocol

`outcome_data_inspected_before_freeze: false` — this freeze was authored before any closure synthesis was computed.

**Design:** outcome-blind program closure + complete negative-results synthesis + quantitative meta-analysis + frontier-exhaustion audit + independent stdlib recompute.

**Frozen input panel:** `research_state/data_cache/ironflow_bulk/` — 18 monthly parquet (2025-05 .. 2026-10), datasets `candles_1h`, `funding`, `open_interest`. All 54 files sha256-asserted before reading; caches read-only; not modified.

**Constraints (hard):**
- No network; stdlib + numpy + pandas + pyarrow only
- No re-run of any closed volatility arm (FCLR-VOL-BROAD-01, CORR-01, STRESS-01, JUMP-01/02/03/04 — all closed NOT_SUPPORTED)
- No re-run of any terminal liquidation track (Track A STRUCTURALLY_BLOCKED; Track B NOT_SUPPORTED; Track C NOT_SUPPORTED)
- No risk overlay (§9 forecast gate not passed)
- No waiting for `NEW_OBSERVED_LIQUIDATION_SOURCE` (cannot fire on frozen data)
- No root-level `research_state/*.md|*.json` files (root at 500/500 cap); all artifacts under `session_20261125T060000Z/`
- No threshold-shop or floor relaxation after outcomes
- No relabeling exploratory as confirmatory
- No future/non-existent session id in AGENT_HANDOFF.md before artifacts exist

**Materiality floor:** 2% relative (frozen).
**Multiplicity:** Holm familywise-error across the declared experiment family.

**Verdict rule:** `NOT_SUPPORTED` / `NOT_STABLE` / `STRUCTURALLY_BLOCKED` outcomes preserved honestly; no fabrication; no fabricated pass.

**frozen_before_outcomes: true**
**decision_frozen_before_outcomes: true**

**Next action (heavy):** Execute closure synthesis + meta-analysis + frontier-exhaustion audit + recompute under this session only.
