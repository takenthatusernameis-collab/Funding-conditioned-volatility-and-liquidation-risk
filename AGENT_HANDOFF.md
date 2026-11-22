# AGENT HANDOFF — 2026-11-22T22:02:17Z

## Repository: Funding-conditioned-volatility-and-liquidation-risk

### INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION

**Rank-0 campaign:** `FCLR-LIQ-RISK-ESCALATION-09-20261122T193000Z` — status `READY_EXECUTE`, `ACTIVE`. Campaign start UTC `20261122T193000Z` has **ELAPSED**. Next session must use UTC > `20261122T193000Z`. Gate `FCLR-LIQ-RISK-ESCALATION` (risk09 family) fails closed without the full heavy artifact set.

**Why this campaign and nothing else:** The funding-conditioned VOLATILITY (QLIKE) pillar is CLOSED leakage-robust — `FCLR-POOLED-ROBUST-002` confirmed `NOT_SUPPORTED_LEAKAGE_ROBUST_NULL` (rel QLIKE +1.011%, Holm primary p=0.6365 vs α₂=0.00833). The highest-value unfinished work is the other half of RESEARCH_PROMPT.md §3.2: **do funding-conditioned features predict OBSERVED liquidation intensity?** This is NOT a re-run of the modeled Track B breach proxy. It uses observed liquidation events (hourly count + OI-normalized notional) from the ironflow bulk cache already on disk.

**Blockers: None.** No external trigger, no new data source. Ironflow liquidations bulk (18 monthly parquet + sha256 + accessed.json) already on disk, joinable to candles_1h/funding/open_interest via market→coin identity (`liquidations.market 'XXX-PERP' -> coin 'XXX'`).

### Required Artifact Set (ALL non-empty, under `research_state/session_<UTC>/` with UTC > `20261122T193000Z`)

1. **Prereg freeze** (outcome-blind, BEFORE any outcome inspection):
   - `fclr_risk09_prereg_<UTC>.{json,md}` — 48h purge+embargo, non-overlapping forward blocks, delisting-aware per-coin identity, survivors-vs-exited arm, baselines (RV/persistence), materiality floor (frozen, not relaxed), Holm family, alpha-spending (sequential k=2, α₂=0.05/(2×3)=0.00833), `outcome_data_inspected_before_freeze:false`, input sha256 asserted.
2. **Power/MDE audit**:
   - `fclr_risk09_power_<UTC>.{py,json,md}` — observed-event sparsity/coverage + minimum-detectable-effect for rare observed-liquidation intensity target.
3. **Independent stdlib recompute**:
   - `fclr_risk09_recompute_<UTC>.{py,json}` — from stored input hashes, no sklearn/pandas, stdlib+numpy+pyarrow only.
4. **Heavy evaluation triad**:
   - `fclr_risk09_evaluation_<UTC>.{py,json,md}` — label-admissibility (§15: hourly coverage, capped-sample check, wallet-level dedup, market→coin identity map, missing≠zero) + leakage-hardened intensity evaluation (count + OI-normalized notional, RV-only vs funding-conditioned, block bootstrap CI95, Holm across declared family, alpha-spending look).
5. **Evidence audit (gate-critical)**:
   - `evidence_audit_<UTC>.json` (gate-critical alias).
6. **Trigger check (non-empty)**:
   - `trigger_check_<UTC>.json`.

### Carry-Forward Bundles (pristine copies from `session_20261122T190000Z/`)
- `fclr_pooled001_*` (13 artifacts) — keeps `FCLR-POOLED-001` gate binding satisfied
- `fclr_pooled_audit001_*` (11 artifacts) — keeps `FCLR-POOLED-AUDIT-001` gate binding satisfied
- `fclr_pooled_robust002_*` (11 artifacts) — keeps `FCLR-POOLED-ROBUST-002` gate binding satisfied

### Root Constraints
- Root md+json cap: **499/500** (all new artifacts MUST go under `session_<UTC>/`). Root is at cap — do NOT add any root-level `research_state/*.md|*.json`.
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
# Must pass

python3 scripts/next_campaign_status.py --json
# Must show campaign_feasible=false for ALL kline domains
```

### Non-Avoidance Constraints (Hard)
- **No** prose-only / trigger-only / source-probe-only / audit-only / verify-and-stop / placeholder sessions.
- **No** empty session directories.
- **Do NOT** write a future `session_<UTC>` id into any handoff before that directory exists.
- **Do NOT** create root-level `research_state/*.md|*.json` (root count 499/500, cap enforced).
- **Do NOT** claim completion without full `fclr_risk09_*` heavy artifact set under new `session_<UTC>/` (UTC > 20261122T193000Z).
- **Do NOT** threshold-shop or relax materiality floor after outcomes; preserve nulls as NOT_SUPPORTED.
- **Do NOT** re-run any terminal campaign (POOLED-001, POOLED-AUDIT-001, POOLED-ROBUST-002, LIVE-ARCHIVE-01/02, NEXT-SOURCE-VERIFY-01, LIQ-CONTAGION-001/002, PANEL-FE-001, STARTER-001, etc.).
- **Do NOT** wait for `NEW_OBSERVED_LIQUIDATION_SOURCE` — cannot fire on frozen data; not a valid excuse to idle.
- **Do NOT** build a risk overlay (§9: forecast gate did not pass).
- **Do NOT** track-adulterate: never describe Track B (modeled breach) or Track C (volatility) as proof of observed liquidation forecast.

### On-Disk Inputs (verified — do NOT re-derive, do NOT substitute)
| Path | Description |
|------|-------------|
| `research_state/data_cache/ironflow_bulk/candles_1h/` | 18 monthly parquet, 3.64M rows, 2025-05..2026-10 |
| `research_state/data_cache/ironflow_bulk/funding/` | 18 monthly parquet, 4.10M rows |
| `research_state/data_cache/ironflow_bulk/open_interest/` | 18 monthly parquet, 3.98M rows |
| `research_state/data_cache/ironflow_bulk/liquidations/` | 18 monthly parquet, 2.85M rows, schema: `timestamp, market, issuer, wallet, position_side, size, notional_usd, avg_price, fills, block, tx_hash` |
| Identity map | `market` `XXX-PERP` -> `coin` `XXX`, join to candles/funding/OI on `coin` + UTC |

Each parquet has `.sha256` and `.accessed.json` sidecars. Assert sha256 before reading; do NOT mutate caches.

### Session Close-Out Requirements
Before finishing, update `AGENT_HANDOFF.md` with:
1. What changed and why
2. Exact test outcomes with paths
3. Evidence added and full paths
4. State of each research gate
5. Single highest-value next task (if any)
6. Precise verifying command
7. Any blocker with next materially different route

Then record your `session_<UTC>/` id in the handoff.

### Timestamp
**Handoff generated: 2026-11-22T22:02:17Z**
**Next session must use UTC > 20261122T193000Z** (campaign start gate)

### Bottleneck Status
- `AGENT_HANDOFF.md` missing `INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION` marker — **RESOLVED** (this handoff).
- Root md+json count 499/500 at cap — all new artifacts under `session_<UTC>/` only.
- No campaign blockers; no external triggers pending; no data frontier gaps for this domain.
