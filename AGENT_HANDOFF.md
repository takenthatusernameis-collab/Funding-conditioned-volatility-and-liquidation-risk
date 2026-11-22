# AGENT HANDOFF — 2026-11-22T22:05:26Z

## Repository: Funding-conditioned-volatility-and-liquidation-risk

> This is the SOLE durable handoff. `HANDOFF_NEXT_SESSION.md` and
> `NEXT_SESSION_INITIAL_TASK_20261122T215812Z.md` were stale/contradictory and
> have been removed. Read this file and nothing else for next-session routing.
> The heavy-work gate (`scripts/check_handoff_heavywork_gate.py`) reads THIS file
> only.

---

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION

**Rank-0 campaign:** `FCLR-LIQ-RISK-ESCALATION-09-20261122T193000Z` — status
`READY_EXECUTE`, program `ACTIVE`. Campaign start UTC `20261122T193000Z` has
**ELAPSED** (now ~`20261122T220526Z`). Your new `session_<UTC>/` MUST have
UTC **> `20261122T193000Z`** and MUST be recorded in this handoff before the
gate will pass. The gate `FCLR-LIQ-RISK-ESCALATION` (risk09 family) fails closed
for any post-start session that lacks the full heavy artifact set below.

**Why this campaign and nothing else (priority by repo name + frontier):**
The funding-conditioned **VOLATILITY (QLIKE)** pillar is CLOSED leakage-robust —
`FCLR-POOLED-ROBUST-002` returned `NOT_SUPPORTED_LEAKAGE_ROBUST_NULL` (C2−B1
QLIKE = +1.011%, worse than the RV baseline; Holm primary p=0.6365 vs
α₂=0.00833; CI95 includes zero). RESEARCH_PROMPT.md §9 forbids a risk overlay
while that forecast gate has not passed, and §16/§19 require continuing after
unfavorable results. The single highest-value unfinished work is therefore the
OTHER half of RESEARCH_PROMPT.md §3.2: **do funding-conditioned features predict
OBSERVED liquidation intensity?** This is Track A (observed on-chain
liquidations), NOT a re-run of the modeled Track B breach proxy. The ironflow
`liquidations` bulk stream (18 months, 2025-05..2026-10, ~2.85M wallet-level
events) is already on disk, unused for a confirmatory study, and is now
gate-enforced so it cannot be skipped or deferred.

**Blockers: None.** No external trigger, no new data source, no network. The
liquidations/funding/candles/OI parquet caches are on disk and joinable by
market→coin identity (`liquidations.market 'XXX-PERP' -> coin 'XXX'`, join to
candles_1h/funding/open_interest on `coin` + UTC hour).

---

## FOCUS CAMPAIGN (Mandatory — heavy work, non-avoidable)

Execute **FCLR-LIQ-RISK-ESCALATION-09** in two phases, both `PENDING` in the
frontier:

1. **LIQ_LABEL_ADMISSIBILITY** — audit observed-liquidation coverage/completeness
   and the market→coin identity map per RESEARCH_PROMPT.md §15; freeze
   label-admissibility BEFORE inspecting any outcome.
2. **HEAVY_OBSERVED_LIQ_INTENSITY** — run the leakage-hardened observed
   liquidation-intensity evaluation (power/MDE + recompute + evaluation triad)
   with block bootstrap + Holm + alpha-spending.

### Required Artifact Set (ALL non-empty, under `research_state/session_<UTC>/`, UTC > 20261122T193000Z)

The gate binds the artifact family to the campaign number in this file
(`FCLR-LIQ-RISK-ESCALATION-09-20261122T193000Z` → prefix `fclr_risk09_`). Produce
every file below. Zero-byte placeholders fail closed.

| # | Artifact (prefix + suffix) | Purpose |
|---|----------------------------|---------|
| 1 | `fclr_risk09_prereg_<UTC>.json` **and** `.md` | Outcome-blind prereg frozen BEFORE any outcome is inspected (`outcome_data_inspected_before_freeze:false`; assert input sha256; 48h purge+embargo; non-overlapping forward blocks; delisting-aware per-coin identity; survivors-vs-exited arm; RV/persistence baseline vs funding-conditioned candidate; materiality floor FROZEN; Holm family; alpha-spending sequential k=2, α₂=0.05/(2×3)=0.00833) |
| 2 | `fclr_risk09_power_<UTC>.py` **and** `.json` **and** `.md` | Observed-event sparsity/coverage + minimum-detectable-effect (power) audit for the rare observed-liquidation intensity target (events per coin-hour, notional coverage, identity-match rate, effective sample size) |
| 3 | `fclr_risk09_recompute_<UTC>.py` **and** `.json` | Independent stdlib recompute from stored input hashes (no pandas/sklearn; stdlib+numpy+pyarrow only) reproducing headline counts/intensities within declared tolerance |
| 4 | `fclr_risk09_evaluation_<UTC>.py` **and** `.json` **and** `.md` | Heavy label-admissibility + leakage-hardened intensity evaluation: §15 admissibility audit, market→coin identity map, hourly event-count + OI-normalized notional targets, RV-only vs funding-conditioned candidate, per-coin block-bootstrap CI95, Holm across the declared family, **explicit symmetric verdict rule** (SUPPORTED / PARTIAL_POSITIVE_SIGNAL / NOT_SUPPORTED) |
| 5 | `evidence_audit_<UTC>.json` (+ `.md`) | Gate-critical alias — required by the generic new-heavy-session check (`evidence_audit_` prefix) |
| 6 | `trigger_check_<UTC>.json` | Non-empty trigger check (required by the risk09 family) |

### Carry-Forward Bundles (pristine copies from `session_20261122T190000Z/`)
Copy these into your new `session_<UTC>/` so the older gate bindings stay
satisfied: `fclr_pooled001_*` (11 artifacts), `fclr_pooled_audit001_*`
(9 artifacts), `fclr_pooled_robust002_*` (9 artifacts). Verified on disk at
2026-11-22T22:05:26Z via
`ls research_state/session_20261122T190000Z/<prefix>_* | wc -l`.

---

## ROOT CONSTRAINTS (hard)

- Root md+json count: **499/500** — at cap. ALL new artifacts MUST go under
  `session_<UTC>/`. Do NOT add any root-level `research_state/*.md|*.json`.
- No empty files, no zero-byte placeholders.
- Do NOT threshold-shop or relax the materiality floor after outcomes.
- Preserve nulls honestly: verdict may be `NOT_SUPPORTED`,
  `PARTIAL_POSITIVE_SIGNAL` (incomplete labels), or `SUPPORTED`.
- Do NOT re-run any terminal campaign (POOLED-001, POOLED-AUDIT-001,
  POOLED-ROBUST-002, LIVE-ARCHIVE-01/02, NEXT-SOURCE-VERIFY-01,
  LIQ-CONTAGION-001/002, PANEL-FE-001, STARTER-001, etc.).
- Do NOT build a risk overlay (§9: forecast gate did not pass).
- Do NOT modify `.github/workflows`.
- Do NOT overwrite `research_state/research_protocol.md`.
- Stdlib + pyarrow only; no network; no new source; no overlay.
- Do NOT track-adulterate: never describe Track B (modeled breach) or Track C
  (volatility) as proof of observed liquidation forecast; never claim a complete
  observed-liquidation census from a capped feed.

---

## VERIFICATION (run before declaring done)

```bash
# 1. Heavy-work gate must return reason=OK (not VERIFY_AND_STOP, not BLOCKED)
python3 scripts/check_handoff_heavywork_gate.py --json

# 2. Campaign gate unittests must pass
python3 -m unittest \
  tests.test_active_campaign_gate \
  tests.test_fclr_starter_001_campaign_gate \
  tests.test_fclr_campaign_gate \
  tests.test_fclr_heavy_confirm_gate \
  tests.test_pooled_robust_002_campaign_gate

# 3. Frozen 3-block domains exhausted (expected; not a blocker for risk09)
python3 scripts/next_campaign_status.py
```

The gate fails closed if: this handoff lacks the markers, the newest on-disk
session is not recorded here, the newest session lacks `fclr_risk09_*` +
`trigger_check_*.json`, or any required file is zero bytes.

---

## ON-DISK INPUTS (verified — do NOT re-derive, do NOT substitute)

| Path | Description |
|------|-------------|
| `research_state/data_cache/ironflow_bulk/candles_1h/` | 18 monthly parquet, 3.64M rows, 2025-05..2026-10 |
| `research_state/data_cache/ironflow_bulk/funding/` | 18 monthly parquet, 4.10M rows |
| `research_state/data_cache/ironflow_bulk/open_interest/` | 18 monthly parquet, 3.98M rows |
| `research_state/data_cache/ironflow_bulk/liquidations/` | 18 monthly parquet, 2.85M rows. Schema: `timestamp, market, issuer, wallet, position_side, size, notional_usd, avg_price, fills, block, tx_hash`. Example market values: `BTC-PERP`, `xyz:KIOXIA-PERP` (strip prefix/suffix to coin). |
| Identity map | `market` `XXX-PERP` → `coin` `XXX`, join to candles/funding/OI on `coin` + UTC hour |

Each parquet has `.sha256` and `.accessed.json` sidecars. Assert sha256 before
reading; do NOT mutate caches.

---

## KEY FILES TO READ BEFORE STARTING

- `research_state/experiment_frontier.json` — rank-0 entry (`FCLR-LIQ-RISK-ESCALATION-09-20261122T193000Z`).
- `scripts/check_handoff_heavywork_gate.py` — gate enforcement (campaign id regex at line ~282; risk08/risk09 required set at ~285; ladder-aware family bind at ~1375).
- `RESEARCH_PROMPT.md` §15 (label admissibility), §17 (alpha-spending), §3.2 (primary question), §9 (no overlay), §16/§19 (continue after null).
- `research_state/session_20261122T190000Z/fclr_pooled_robust002_evidence_audit_20261122T190000Z.md` — precedent for artifact structure.

---

## NON-AVOIDANCE CONSTRAINTS (hard — machine-checked)

- **No** prose-only / trigger-only / source-probe-only / audit-only / verify-and-stop / placeholder sessions.
- **No** empty session directories.
- **Do NOT** write a future `session_<UTC>` id into this handoff before that directory exists.
- **Do NOT** create root-level `research_state/*.md|*.json` (root count 499/500, cap enforced).
- **Do NOT** claim completion without the full `fclr_risk09_*` heavy artifact set under a new `session_<UTC>/` (UTC > 20261122T193000Z).
- **Do NOT** threshold-shop or relax the materiality floor after outcomes; preserve nulls as NOT_SUPPORTED.
- **Do NOT** re-run any terminal campaign.
- **Do NOT** wait for `NEW_OBSERVED_LIQUIDATION_SOURCE` — cannot fire on frozen data; not a valid excuse to idle.
- **Do NOT** build a risk overlay (§9: forecast gate did not pass).
- **Do NOT** track-adulterate: never describe Track B (modeled breach) or Track C (volatility) as proof of observed liquidation forecast.

---

## SESSION CLOSE-OUT REQUIREMENTS

Before finishing, update THIS file with:
1. What changed and why
2. Exact test outcomes with paths
3. Evidence added and full paths
4. State of each research gate
5. Single highest-value next task (if any)
6. Precise verifying command
7. Any blocker with next materially different route

Then record your `session_<UTC>/` id in this handoff (append the id string
`session_<UTC>` so `_latest_handoff_session` picks it up).

---

## Bottleneck Resolution (this handoff)

- **Resolved:** three competing handoff files with contradictory priorities
  (the 21:05Z `HANDOFF_NEXT_SESSION.md` pointed at a stale Binance-2024
  Gate-4 ablations campaign that contradicts the rank-0 frontier). Consolidated
  into this single file; the two stale files were removed via `git rm`.
- **Resolved:** root md+json count 499/500 at cap — all new artifacts go under
  `session_<UTC>/` only.
- No campaign blockers; no external triggers pending; no data-frontier gap for
  the Track A domain. Heavy work is feasible TODAY on cached data.

---

**Handoff generated: 2026-11-22T22:05:26Z**
**Next session must use UTC > 20261122T193000Z** (campaign start gate).