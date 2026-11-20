# AGENT HANDOFF — Funding-Conditioned Volatility and Liquidation Risk
**Timestamp:** 2026-11-20T01:21:04Z
**Session:** FCLR-001 frozen starter protocol (Track C: 24h forward realized variance forecasting) — heavy-work campaign, no deferral
**Campaign declared:** FCLR-STARTER-001-20261119T231806Z (start UTC 20261119T231806Z)
**Latest heavy session:** session_20261119T180650Z (RISK-12 Track A confirmatory power audit UNDERPOWERED, MDE 0.002814 > plausible 0.001; evidence_audit + fclr_risk12_* + trigger_check; terminal)

---

# INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION (timestamped 2026-11-20T01:21:04Z)

Execute FCLR-001 frozen starter protocol (Track C: 24h forward realized variance forecasting). This session completes Step 1 only:

1. **Campaign declaration (this handoff).** FCLR-STARTER-001-20261119T231806Z is the active rank-0 heavy campaign. Any session whose UTC is after 20261119T231806Z cannot satisfy the handoff heavy-work gate with prose, placeholders, or an arbitrary artifact. It must emit, under `research_state/session_<UTC>/`:
   - `fclr_starter001_protocol_freeze_<UTC>.json` + `.md` — §14 protocol freeze hash-bound to `RESEARCH_PROMPT.md` §14; `experiment_id` starts with `FCLR-STARTER-001`; `outcome_data_inspected_before_freeze=false`; `protocol_path` must NOT be `research_state/research_protocol.md` (sealed legacy FCLR-001 2024-01..03 definition consumed by `scripts/run_evaluation.py` — never overwrite it). The freeze body lives at a new timestamped path, e.g. `research_state/protocol_fclr_starter_001_<UTC>.md`, and contains §14 verbatim with matching `section14_sha256`/`protocol_sha256`.
   - `fclr_starter001_panel_freeze_<UTC>.json` + `.md` — `panel_sha256` (64 hex), non-empty `source_hashes`, `panel_frozen_before_target_generation=true`, non-empty `eligible_definition`, `cutoff_utc` (or `split_boundaries`). Panel hash recorded BEFORE any target is computed.
   - `fclr_starter001_baselines_<UTC>.py` + `.json` + `.md` — B0 persistence (RV24h) and B1 HAR OLS (log RV1h/RV24h/RV168h → log target) on development/validation; `holdout_opened=false`; `split_used` contains dev/validation; `models.B0` and `models.B1` each with numeric `qlike >= 0`; `n_obs > 0`.
   - `trigger_check_<UTC>.json` — non-empty.
   Placeholders (`{}` / zero-byte) fail closed; free-text "frozen" claims without these artifacts fail closed.

2. **Freeze `research_state/protocol_fclr_starter_001_20261119T231806Z.md` from RESEARCH_PROMPT.md §14 verbatim** — unit (eligible linear perpetual × closed UTC hourly timestamp); timing (forecast at t after closed hour t; outcomes begin t+1); universe (broadest public listing/delisting metadata, no fixed top-N); primary target (next-24h realized variance, sum of squared log returns t+1..t+24); secondary horizons (6h/72h/168h, multiplicity-declared); frozen predictors (RV1h/RV24h/RV168h, signed funding, 90-day abs-funding percentile with min-30-obs rule, mark/index premium, mark/EMA24 distance); frozen baselines (B0 persistence RV24h; B1 HAR OLS log RV1h/RV24h/RV168h → log target; C1 = B1 + funding + percentile; C2 = C1 + premium + EMA24); 60/20/20 chronological split with 7-day purge/embargo; primary metric paired OOS QLIKE C2 vs B1 with block-bootstrap CI (≥2000 reps); gate ≥2% relative QLIKE reduction + CI supports improvement + Holm over family; minimum ≥5 instruments and ≥3 non-overlapping 30-day blocks. `outcome_data_inspected_before_freeze=false`.

3. **Build panel from Hyperliquid mark/index/funding/klines data** — reuse frozen panel where possible; record source hashes, cutoff dates, eligible sample definition.

4. **Hash and freeze eligible panel before target generation** — no target computed until panel hash is recorded.

5. **Run B0 and B1 baselines on development/validation** — record QLIKE/MAE/RMSE. Holdout NOT opened.

Do NOT inspect holdout outcomes before protocol freeze. No other task has higher expected information gain per unit of free compute. Track A is power-blocked (RISK-12 UNDERPOWERED, MDE 0.002814 > PLAUSIBLE_EFFECT_BRIER 0.001); do NOT re-run RISK-09/10/11/12. Track B is NOT_SUPPORTED (terminal). Track C volatility forecasting is the only agent-removable heavy path on admissible public mark-price data.

This is a heavy-work campaign: future agents must complete protocol freeze + panel hash + B0/B1 metrics in one continuous session; no deferral, no placeholder artifacts, no trigger-gated wait.

---

## Bottlenecks removed (this handoff)

| Blocker | Evidence | Resolution |
|---------|----------|------------|
| RISK-12 Track A confirmatory (session_20261119T180650Z) UNDERPOWERED; MDE 0.002814 > 0.001; all 6 family members NOT_MET | `research_state/session_20261119T180650Z/` (fclr_risk12_power/evaluation/recompute/prereg) + trigger_check | Terminal. Demoted; do NOT re-run RISK-09/10/11/12 variants (explicitly prohibited in RISK-12 prereg). Power limit, not data availability. |
| `research_state/research_protocol.md` holds sealed legacy 2026-11-06 protocol (4 coins, 2024-01..03), not FCLR-001 §14 spec | `research_state/research_protocol.md` frozen 2026-11-06T20:36:32Z; `scripts/run_evaluation.py:15` reads it as PROTOCOL | NOT overwritten (sealed legacy, consumed by run_evaluation.py). FCLR-001 §14 freeze written to a NEW timestamped path `research_state/protocol_fclr_starter_001_<UTC>.md` per the FCLR-STARTER-001 gate (overwriting the sealed file fails closed: PROTOCOL_FREEZE_OVERWRITES_SEALED). |
| `FCLR_HEAVY_CAMPAIGN_NEXT.md` referenced by prior frontier but missing | `research_state/experiment_frontier.json` lines 13, 48, 50, 64 | Superseded by FCLR-STARTER-001 campaign. Heavy work is protocol freeze + panel hash + B0/B1 metrics, defined in this handoff and RESEARCH_PROMPT.md §14. |
| Prior frontier rank-0 was TRIGGER_ONLY waiting on external triggers (GATE4_BRANCH_1, NEW_OBSERVED_LIQUIDATION_SOURCE, HL_LABEL_EXTENSION, EXPANSION_ROBUSTNESS_REDO) | `experiment_frontier.json` rank 0; `tests/test_active_campaign_gate.py` invariant | Rank 0 superseded: FCLR-001 is a fresh frozen protocol (§14), not a re-run of concluded cached-data estimands. Rank 0 = READY_EXECUTE / ACTIVE with concrete unfinished task + phases. All downstream campaigns remain SUPERSEDED (terminal). Invariant preserved: exactly one rank-0, non-terminal, concrete task, phases present. |

---

## 1. What changed and why

**Prior state (all terminal on cached data):**
- Track A liquidation forecasting: RISK-12 UNDERPOWERED (MDE 0.002814 > 0.001), all 6 family members NOT_MET, `models_run=false`. Track A Confirmatory-01 NOT_MET (Holm p=1.0). RISK-11 inconclusive. Power limit, not data availability.
- Track B modeled boundary breach: TB2 NOT_MET (Log Loss C2 vs B1 +1.68% rel, below 2% floor, CI crosses zero, Holm FAILS, only 2 blocks <3 required). TB1 degenerate/inadmissible. NOT_SUPPORTED, terminal.
- Track C volatility: FCLR-011 PASS (4.94% rel QLIKE, 2026-05..08) but NOT_REPLICATED on all forward/period-specificity tests. TRACKA-VOL-FAMILY NOT_MET (Holm across 12 comparisons). TRACKA-ALT-VOL NOT_MET (CI crosses zero). All terminal.

**Why FCLR-001 Track C is the highest-value task:**
1. Track A is power-blocked — no credible path to a detectable effect without a materially larger panel.
2. Track B is NOT_SUPPORTED — the modeled breach proxy does not generalize.
3. Track C proceeds independently — uses mark-price data already available; no liquidation labels needed.
4. FCLR-001 is fully specified — RESEARCH_PROMPT.md §14 gives exact unit, timing, universe, target, features, baselines, splits, metrics, inference, and gate.
5. Infrastructure is complete — baselines (`src/models/baselines.py`), features (`src/features/{funding,price,volatility}.py`), eval (`src/eval/{walkforward,inference}.py`), block bootstrap (`src/volatility/block_bootstrap.py`), walk-forward splits all implemented.
6. Honest null preservation — if FCLR-001 fails, the null is preserved per protocol; no threshold shopping.

---

## 2. Current state of each research gate

| Gate | Track | Status | Evidence |
|------|-------|--------|----------|
| Source feasibility | All | PARTIAL | Hyperliquid mark/index/funding/klines admissible; Binance public archive not yet probed for sealed months |
| Label decision | Track A | DECIDED | Hyperliquid observed labels (incomplete census, documented); Track B/C viable without Track A |
| Protocol freeze (FCLR-001) | Track C | NOT_STARTED | Protocol fully specified in RESEARCH_PROMPT.md §14 — ready to freeze (this session, Step 1) |
| Baseline first | Track C | NOT_STARTED | B0 (persistence) and B1 (RV-only HAR) implemented in `src/models/baselines.py` |
| Incremental features | Track C | NOT_STARTED | Funding + price features in `src/features/{funding,price,volatility}.py` |
| Forecast gate | Track C | NOT_STARTED | Requires FCLR-001 completion with ≥2% QLIKE reduction, block-bootstrap CI, Holm correction |
| Overlay eligibility | — | BLOCKED | Requires forecast gate pass first |

---

## 3. Single highest-value next task

**Execute FCLR-001 frozen starter protocol (Track C: 24h forward realized variance forecasting), Step 1: protocol freeze + panel hash freeze + B0/B1 baselines.**

**Why:** Track A power-blocked, Track B NOT_SUPPORTED, Track C is the only viable confirmatory path. FCLR-001 §14 is fully specified; infrastructure complete; no credentials, no paid data, no network required for Step 1 (uses cached Hyperliquid panel).

**Exact FCLR-001 specification (from RESEARCH_PROMPT.md §14):**
- **Unit:** Eligible linear perpetual contract × closed UTC hourly timestamp
- **Primary target:** Next-24h realized variance of mark-price returns (sum of squared log returns over t+1..t+24)
- **Secondary horizons:** 6h, 72h, 168h (explicitly secondary, multiplicity-declared)
- **Features (causal, lagged):** RV1h, RV24h, RV168h; signed funding (latest ≤ t); funding extremeness (90-day abs percentile, min 30 obs); premium (mark/index − 1); EMA24 deviation (mark/EMA24 − 1)
- **Models (frozen):** B0 persistence (RV24h); B1 HAR OLS on log(RV1h, RV24h, RV168h) → log(target); C1 = B1 + signed funding + funding percentile; C2 = C1 + premium + EMA24 deviation
- **Split:** 60%/20%/20% chronological, 7-day purge/embargo at boundaries (168h horizon)
- **Primary metric:** Paired out-of-sample QLIKE difference (C2 vs B1), block bootstrap CI (≥2000 reps)
- **Gate:** ≥2% relative QLIKE reduction, CI supports improvement, Holm over family passes

---

## 4. Precise command/check to verify completion

**Step 1: Freeze protocol and build panel**
```bash
# 1. Create research_state/protocol_fclr_starter_001_<UTC>.md from RESEARCH_PROMPT.md §14 verbatim
#    (do NOT write research_state/research_protocol.md — sealed legacy)
# 2. Build panel from Hyperliquid data (mark, index, funding, klines) — reuse frozen panel where possible
# 3. Hash and freeze eligible panel before target generation
```

**Step 2: Run baselines (B0, B1)**
```bash
python3 -c "
from src.volatility.features import *
from src.models.baselines import *
from src.eval.walkforward import *
# Load panel, construct features, run B0/B1 on development/validation
"
```

**Step 3: Run confirmatory evaluation on sealed holdout** (later session, after protocol freeze)
```bash
# After protocol freeze, run C1, C2 vs B1 on holdout
# Compute paired QLIKE diff, block bootstrap CI, Holm correction
# Verdict: FORECAST_GATE_PASSED or NOT_SUPPORTED
```

**Acceptance test for this session:**
- `AGENT_HANDOFF.md` carries the `INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION` section, timestamped 2026-11-20T01:21:04Z, declaring campaign FCLR-STARTER-001-20261119T231806Z
- `experiment_frontier.json` rank 0 = FCLR-001, status READY_EXECUTE / program_status ACTIVE, all 3 phases NOT_STARTED, every other entry SUPERSEDED (`python3 -m unittest tests.test_active_campaign_gate` passes)
- FCLR-STARTER-001 gate contract documented: post-campaign sessions must emit protocol freeze (json+md, §14 hash-bound, not sealed legacy file), panel freeze (json+md), baselines triad (py+json+md), trigger_check (json); placeholders fail closed (`python3 -m unittest tests.test_fclr_starter_001_campaign_gate` passes)
- `research_state/research_protocol.md` NOT overwritten (sealed legacy)
- `python3 scripts/check_handoff_heavywork_gate.py --json` returns pass
- `python3 -m unittest discover tests` returns 0 failures
- No holdout outcomes inspected before protocol freeze

---

## 5. Source/engineering blockers and next free route

| Blocker | Evidence | Next materially different free route |
|---------|----------|--------------------------------------|
| No Binance liquidation labels | Binance public archive requires manual download or requester-pays; no unauthenticated historical liquidation feed | Track C volatility forecasting — mark-price klines only (publicly available) |
| Track A power limit | RISK-12 MDE=0.0028 > plausible 0.001; 13 coins, 12 months insufficient | FCLR-001 Track C — different outcome (volatility), different baseline (RV-only), different metric (QLIKE) |
| Sealed Binance months unread | RESEARCH_PROMPT.md prohibits reading sealed months for outcomes | Use Hyperliquid panel for FCLR-001 development; register separate Binance-arm protocol if/when archive access verified |
| No historical market-cap ranks | Free point-in-time ranks unavailable | Venue-native universe — all discoverable perpetuals from public listing metadata (per FCLR-001 §Unit) |

**Do not:**
- Re-run RISK-09/10/11/12 variants (explicitly prohibited in RISK-12 prereg)
- Attempt Track A liquidation forecasting without a materially larger panel
- Modify `.github/workflows` (protected control plane)
- Create placeholder artifacts — only create when contents are meaningful
- Overwrite `research_state/research_protocol.md` (sealed legacy FCLR-001 2024-01..03)

---

## 6. Contingency ladder (if FCLR-001 blocked)

If FCLR-001 hits a structural blocker (e.g., mark-price data unavailable for adequate coverage):

1. **RISK-13** — Per RISK-12 evidence audit: advance only if MDE ≤ plausible effect via MDE-by-instrument redesign or larger panel
2. **Distinct-mechanism campaigns on frozen panel** (candidate queue):
   - (i) `liq_count` at t-1 persistence family
   - (ii) Within-hour cross-sectional funding-intensity contrast
   - (iii) UTC-hour / market-wide-RV conditioning of funding effect
3. **Track B modeled boundary-breach** — If contract specs and margin tiers verifiable from public sources

---

## 7. Next session must

Read this handoff + RESEARCH_PROMPT.md completely, inspect working tree and latest artifacts, then execute Step 1 of FCLR-STARTER-001 (protocol freeze + panel hash + B0/B1 metrics). No other task has higher expected information gain per unit of free compute. The FCLR-STARTER-001 campaign is declared in this durable handoff; the machine-enforced handoff heavy-work gate (`scripts/check_handoff_heavywork_gate.py`) requires the concrete artifact triad for any session after UTC 20261119T231806Z — future agents cannot satisfy it with prose or placeholders.

(End of file)