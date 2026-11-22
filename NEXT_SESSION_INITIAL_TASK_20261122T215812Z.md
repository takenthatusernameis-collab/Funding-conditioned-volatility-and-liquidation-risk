# INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION
**Repository:** Funding-conditioned-volatility-and-liquidation-risk
**Timestamp:** 2026-11-22T21:58:12Z
**Campaign:** FCLR-LIQ-RISK-ESCALATION-09-20261122T193000Z (RANK-0 ACTIVE / READY_EXECUTE — GATE-ENFORCED)
**Campaign Start UTC:** 20261122T193000Z — **ELAPSED**
**Next Session Must Have UTC > 20261122T193000Z**

---

## WHY THIS CAMPAIGN AND NOTHING ELSE

The **funding-conditioned volatility (QLIKE) pillar is CLOSED leakage-robust**:
- FCLR-POOLED-001 → NOT_SUPPORTED (session_20261122T092003Z)
- FCLR-POOLED-AUDIT-001 → found concrete leakage/quality gaps (session_20261122T165200Z)
- FCLR-POOLED-ROBUST-002 → applied ALL remediations simultaneously → **NOT_SUPPORTED_LEAKAGE_ROBUST_NULL** (C2−B1 QLIKE = +1.011%, worse than RV baseline; Holm primary p=0.6365 vs α₂=0.00833; CI95 includes zero)

RESEARCH_PROMPT.md §9 forbids any risk overlay (forecast gate did not pass). §16/§19 require continuing after unfavorable results.

The **liquidation-risk pillar (§3.2) has NEVER been tested confirmatively on OBSERVED liquidation events**. The ironflow `liquidations` bulk stream (18 months, 2025-05..2026-10, ~2.85M wallet-level events keyed by `market`/`issuer`) is on disk, unused for a confirmatory study, and is the highest-value unfinished work. It is now **gate-enforced** so it cannot be skipped.

---

## MANDATORY DELIVERABLES (all under `research_state/session_<UTC>/`, UTC > `20261122T193000Z`, non-empty, no zero-byte placeholders)

| # | Artifact | Purpose |
|---|----------|---------|
| 1 | `fclr_risk09_prereg_<UTC>.{json,md}` | Outcome-blind prereg **frozen BEFORE any outcome is inspected** (`outcome_data_inspected_before_freeze:false`; assert input sha256; 48h purge+embargo; non-overlapping forward blocks; delisting-aware per-coin identity; RV/persistence baseline vs funding-conditioned candidate; materiality floor; Holm family; alpha-spending look) |
| 2 | `fclr_risk09_power_<UTC>.{py,json,md}` | Observed-event sparsity/coverage + minimum-detectable-effect (power) audit for rare observed-liquidation intensity (events per coin-hour, notional coverage, identity-match rate, effective sample size) |
| 3 | `fclr_risk09_recompute_<UTC>.{py,json}` | Independent stdlib recompute from stored input hashes (no pyarrow-based eval module imported), reproducing headline counts/intensities within declared tolerance |
| 4 | `fclr_risk09_evaluation_<UTC>.{py,json,md}` | Heavy label-admissibility + leakage-hardened intensity evaluation: §15 admissibility audit, `market`→`coin` identity map, hourly event-count + OI-normalized notional targets, RV-only vs funding-conditioned candidate, per-coin block-bootstrap CI95, Holm across declared family, **explicit symmetric verdict rule** (SUPPORTED / PARTIAL_POSITIVE_SIGNAL / NOT_SUPPORTED) |
| 5 | `evidence_audit_<UTC>.json` (+ `.md`) | Gate-critical alias |
| 6 | `trigger_check_<UTC>.json` | Non-empty |

**ALSO CARRY FORWARD** (pristine copies from `session_20261122T190000Z/`):
- `fclr_pooled001_*` (11 artifacts) — keeps `FCLR-POOLED` binding satisfied
- `fclr_pooled_audit001_*` (9 artifacts) — keeps `FCLR-POOLED-AUDIT` binding satisfied
- `fclr_pooled_robust002_*` (9 artifacts) — keeps `FCLR-POOLED-ROBUST` binding satisfied

---

## NON-AVOIDANCE CONSTRAINTS (machine-checked by `check_handoff_heavywork_gate.py`)

- **Do NOT** write a future `session_<UTC>` id into any handoff before that directory exists
- **Do NOT** create root-level `research_state/*.md|*.json` (root count 499/500, cap enforced)
- **Do NOT** create empty/placeholder files or empty session directories
- **Do NOT** claim completion without full `fclr_risk09_*` heavy artifact set under new `session_<UTC>/` (UTC > 20261122T193000Z)
- **Do NOT** threshold-shop or relax materiality floor after outcomes; preserve nulls as NOT_SUPPORTED
- **Do NOT** re-run any terminal campaign (POOLED-001, POOLED-AUDIT-001, POOLED-ROBUST-002, LIVE-ARCHIVE-01/02, NEXT-SOURCE-VERIFY-01, LIQ-CONTAGION-001/002, PANEL-FE-001, STARTER-001, etc.)
- **Do NOT** wait for `NEW_OBSERVED_LIQUIDATION_SOURCE` — cannot fire on frozen data; not a valid excuse to idle
- **Do NOT** build a risk overlay (§9: forecast gate did not pass)
- **Do NOT** track-adulterate: never describe Track B (modeled breach) or Track C (volatility) as proof of observed liquidation forecast; never claim complete observed-liquidation census from capped feed

---

## VERIFYING COMMANDS (must all pass)

```bash
# Gate must pass with reason=OK
python3 scripts/check_handoff_heavywork_gate.py

# All 121 gate unittests must pass
python3 -m unittest \
  tests.test_tracka_hardening_143 \
  tests.test_tracka_hardening_144 \
  tests.test_active_campaign_gate \
  tests.test_fclr_heavy_confirm_gate \
  tests.test_fclr_campaign_gate \
  tests.test_fclr_starter_001_campaign_gate \
  tests.test_pooled_robust_002_campaign_gate

# Frozen 3-block domains exhausted (expected, not a blocker)
python3 scripts/next_campaign_status.py
```

---

## ON-DISK INPUTS (verified — do NOT re-derive, do NOT substitute)

| Path | Description |
|------|-------------|
| `research_state/data_cache/ironflow_bulk/candles_1h/` | 18 monthly parquet, 3.64M rows, 2025-05..2026-10 |
| `research_state/data_cache/ironflow_bulk/funding/` | 18 monthly parquet, 4.10M rows |
| `research_state/data_cache/ironflow_bulk/open_interest/` | 18 monthly parquet, 3.98M rows |
| `research_state/data_cache/ironflow_bulk/liquidations/` | 18 monthly parquet, 2.85M rows, schema: `timestamp, market, issuer, wallet, position_side, size, notional_usd, avg_price, fills, block, tx_hash` |
| Identity map | `market` `XXX-PERP` → `coin` `XXX`, join to candles/funding/OI on `coin` + UTC |

Each parquet has `.sha256` and `.accessed.json` sidecars. Assert sha256 before reading; do NOT mutate caches.

---

## SESSION CLOSE-OUT REQUIREMENTS

Before finishing, update `AGENT_HANDOFF.md` with:
1. What changed and why
2. Exact test outcomes with paths
3. Evidence added and full paths
4. State of each research gate
5. Single highest-value next task (if any)
6. Precise verifying command
7. Any blocker with next materially different route

Then record your `session_<UTC>/` id in the handoff.

---

**STATUS:** Campaign start UTC 20261122T193000Z has ELAPSED. Next session is POST-START. Gate `FCLR-LIQ-RISK-ESCALATION` (ladder-aware, binds `fclr_risk09_*`) fails closed for any session UTC > 20261122T193000Z that lacks the full heavy artifact set. A prose-only, trigger-only, audit-only, or verify-and-stop session **will trip the gate and fail closed**.