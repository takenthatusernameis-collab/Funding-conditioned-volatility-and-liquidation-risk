# AGENT HANDOFF — 2026-11-22T22:00:07Z

## Repository: Funding-conditioned-volatility-and-liquidation-risk

### Executive Summary
The **FCLR-LIQ-RISK-ESCALATION-09** campaign (rank-0, `READY_EXECUTE`, `ACTIVE`) is the **sole executable heavy work** remaining. All other campaigns are `SUPERSEDED_TERMINAL` or `COMPLETE`. The frozen-data frontier is exhausted (`NO_FEASIBLE_3_BLOCK_DESIGN_IN_ANY_DOMAIN` per `next_campaign_status.py`), but this campaign operates on the **already-on-disk ironflow liquidations bulk parquet** (18 months, 2025-05..2026-10, `research_state/data_cache/ironflow_bulk/liquidations/`) — a DIFFERENT data domain from the exhausted Binance 5-symbol / Hyperliquid kline frontiers.

### Current Rank-0 Campaign: FCLR-LIQ-RISK-ESCALATION-09-20261122T193000Z
- **Task**: First confirmatory use of observed ironflow liquidations bulk stream (Track A) for the repository's liquidation-risk pillar.
- **Why now**: FCLR-POOLED-ROBUST-002 (completed `session_20261122T190000Z`) confirmed the funding-conditioned VOLATILITY (QLIKE) null is leakage-robust (`NOT_SUPPORTED_LEAKAGE_ROBUST_NULL`, rel QLIKE +1.011%, Holm primary p=0.6365 vs α₂=0.00833). The highest-value unfinished work is the other half of the primary question (RESEARCH_PROMPT.md §3.2): **do funding-conditioned features predict OBSERVED liquidation intensity?**
- **This is NOT** a re-run of the modeled Track B breach proxy. It uses **observed liquidation events** (hourly count + OI-normalized notional) from the ironflow bulk cache.
- **Gate**: `scripts/check_handoff_heavywork_gate.py FCLR-LIQ-RISK-ESCALATION` (risk09 family; fails closed without full heavy artifact set; start UTC 20261122T193000Z).
- **Blockers**: **None**. No external trigger, no new data source. Ironflow liquidations bulk (18 monthly parquet + sha256 + accessed.json) already on disk, joinable to candles_1h/funding/open_interest via market→coin identity (`liquidations.market 'XXX-PERP' -> coin 'XXX'`).

### Required Artifact Set (ALL non-empty, under `research_state/session_<UTC>/` with UTC > 20261122T193000Z)
1. **Prereg freeze** (outcome-blind, BEFORE any outcome inspection):
   - `fclr_risk09_prereg_<UTC>.{json,md}` — 48h purge+embargo, non-overlapping forward blocks, delisting-aware per-coin identity, survivors-vs-exited arm, baselines (RV/persistence), materiality floor (frozen, not relaxed), Holm family, alpha-spending (sequential k=2, α₂=0.05/(2×3)=0.00833), `outcome_data_inspected_before_freeze:false`, input sha256 asserted.
2. **Power/MDE audit**:
   - `fclr_risk09_power_<UTC>.{py,json,md}` — observed-event sparsity/coverage + minimum-detectable-effect for rare observed-liquidation intensity target.
3. **Independent stdlib recompute**:
   - `fclr_risk09_recompute_<UTC>.{py,json}` — from stored input hashes, no sklearn/pandas, stdlib+numpy+pyarrow only.
4. **Heavy evaluation triad**:
   - `fclr_risk09_evaluation_<UTC>.{py,json,md}` — label-admissibility (§15: hourly coverage, capped-sample check, wallet-level dedup, market→coin identity map, missing≠zero) + leakage-hardened intensity evaluation (count + OI-normalized notional, RV-only vs funding-conditioned, block bootstrap CI95, Holm across declared family, alpha-spending look).
5. **Evidence audit (gate-critical)**:
   - `evidence_audit_<UTC>.json` (alias `evidence_audit_<UTC>.json` pointing to the above, `"gate_critical": true`).
6. **Trigger check (non-empty)**:
   - `trigger_check_<UTC>.json`.

### Root Constraints
- Root md+json cap: **499/500** (all new artifacts MUST go under `session_<UTC>/`).
- No empty files, no zero-byte placeholders.
- Do NOT threshold-shop or relax materiality floor after outcomes.
- Preserve nulls honestly (verdict may be `NOT_SUPPORTED`, `PARTIAL_POSITIVE_SIGNAL` (incomplete labels), or `SUPPORTED`).
- Do NOT re-run any terminal campaign.
- Do NOT build a risk overlay (§9 gate still not passed).
- Do NOT modify `.github/workflows`.
- Do NOT overwrite `research_state/research_protocol.md`.
- Stdlib + pyarrow only; no network; no new source; no overlay.

### Two Phases (both `PENDING` in frontier)
1. **LIQ_LABEL_ADMISSIBILITY** — Audit observed-liquidation coverage/completeness and market→coin identity per RESEARCH_PROMPT.md §15; freeze label-admissibility before outcomes.
2. **HEAVY_OBSERVED_LIQ_INTENSITY** — Run leakage-hardened observed-liquidation intensity evaluation (power/MDE + recompute + evaluation triad) with block bootstrap + Holm + alpha-spending.

### Key Files to Read Before Starting
- `research_state/experiment_frontier.json` (rank-0 entry, lines 1-45)
- `scripts/next_campaign_status.py` (run with `--json` to see all frontiers exhausted)
- `scripts/check_handoff_heavywork_gate.py FCLR-LIQ-RISK-ESCALATION` (gate enforcement)
- `RESEARCH_PROMPT.md` §15 (label admissibility), §17 (alpha-spending), §3.2 (primary question)
- `research_state/session_20261122T190000Z/fclr_pooled_robust002_evidence_audit_20261122T190000Z.md` (precedent for artifact structure)

### Verification Before Declaring Done
```bash
python3 scripts/check_handoff_heavywork_gate.py FCLR-LIQ-RISK-ESCALATION
# Must return reason=OK (not VERIFY_AND_STOP, not BLOCKED)

python3 -m unittest tests.test_fclr_starter_001_campaign_gate tests.test_active_campaign_gate
# Must pass (79 tests OK precedent)

python3 scripts/next_campaign_status.py --json
# Must show campaign_feasible=false for ALL kline domains (confirms this is the only heavy work)
```

### Non-Avoidance Constraints (Hard)
- **No** prose-only / trigger-only / source-probe-only / audit-only / verify-and-stop / placeholder sessions.
- **No** empty session directories.
- **Carry forward** the complete `fclr_pooled001_*` (13), `fclr_pooled_audit001_*` (11), and `fclr_pooled_robust002_*` (11) bundles into your session dir so older gate bindings stay satisfied.

### Timestamp
**Handoff generated: 2026-11-22T22:00:07Z**
**Next session must use UTC > 20261122T193000Z** (campaign start gate)