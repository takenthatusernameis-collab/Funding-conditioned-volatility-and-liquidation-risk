# AGENT HANDOFF — Funding-Conditioned Volatility and Liquidation Risk
**Timestamp:** 2026-11-19T19:53:21Z
**Session:** Post-mortem of RISK-12 (UNDERPOWERED) → Next: FCLR-001 frozen starter protocol (Track C volatility forecasting)

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION (timestamped 2026-11-19T19:53:21Z)
Execute FCLR-001 frozen starter protocol (Track C: 24h forward realized variance forecasting). Step 1 only this session: freeze `research_state/research_protocol.md` from RESEARCH_PROMPT.md §14 verbatim, build panel from Hyperliquid mark/index/funding/klines data reusing frozen panel where possible, hash+freeze eligible panel before target generation. Do NOT inspect holdout outcomes before freeze. No other task has higher expected information gain per unit of free compute. Track A is power-blocked; do not re-run RISK-09/10/11/12.

---

## 1. What changed and why

**RISK-12 (funding-shock transmission family) completed: UNDERPOWERED**
- Campaign: `FCLR-LIQ-RISK-ESCALATION-12-20261119T175557Z`
- Frozen panel: `session_20261119T022824Z/fclr_tracka_extension01_panel_session_20261119T022824Z.csv` (113,880 coin-hours, 13 coins, 2025-11..2026-10)
- Common-sample rule (t-25) kept 112,671 rows
- Power gate: min `mde_brier_80pct` across scored blocks at 13 coins = **0.002814** (block_3 primary)
- `PLAUSIBLE_EFFECT_BRIER = 0.001` (frozen)
- All 6 family members: **NOT_MET** (`models_run=false`, no fitting performed)
- All 11 RISK-12 artifacts emitted (evaluation JSON/MD, power JSON/MD, prereg MD/JSON, recompute py/JSON, evidence audit JSON/MD, trigger check, sealed bridge)

**Prior confirmatory results (Track A liquidation):**
- `FCLR-LIQ-TRACKA-CONFIRMATORY-01`: **NOT_MET** — funding features did not improve Brier over RV-only (Holm p=1.0)
- `RISK-11`: funding-correction replication — no clear pass
- **Track A liquidation prediction has hit statistical power limits**, not data availability. The panel and labels are complete and admissible.

---

## 2. What was actually tested, with exact outcomes

| Experiment | Status | Key Metric | Verdict |
|------------|--------|------------|---------|
| Track A Extension (descriptive) | COMPLETE | 1.13M liq events, 13 coins | Descriptive only — no forecast test |
| Track A Confirmatory-01 | COMPLETE | Brier, 3 blocks, Holm | **NOT_MET** (p_holm=1.0) |
| RISK-11 (correction-time) | COMPLETE | survival/correction | Inconclusive / no pass |
| RISK-12 (funding-shock innovations) | COMPLETE | Power gate | **UNDERPOWERED** (MDE 0.0028 > 0.001) |

**Dominating limitation:** Statistical power (sample size × effect size) for liquidation event forecasting, not data availability.

---

## 3. Evidence added and where

```
research_state/session_20261119T180650Z/
  fclr_risk12_prereg_20261119T180650Z.md/.json      # Frozen preregistration
  fclr_risk12_power_20261119T180650Z.py/.json/.md   # Power analysis (MDE=0.002814)
  fclr_risk12_evaluation_20261119T180650Z.py/.json/.md  # Empty eval (models_run=false)
  fclr_risk12_recompute_20261119T180650Z.py/.json   # Recompute script + output
  evidence_audit_20261119T180650Z.json/.md           # This audit
  trigger_check_20261119T180650Z.json                # Gate verification
  rca011_sealed_bridge_20261119T180650Z.py/.json/.md # Bridge artifact
  program_power_synthesis_20261119T180650Z.py/.json/.md # Program synthesis
```

**Verification command (must PASS):**
```bash
python3 scripts/check_handoff_heavywork_gate.py --json
python3 research_state/session_20261119T180650Z/fclr_risk12_evaluation_20261119T180650Z.py
```

---

## 4. Current state of each research gate

| Gate | Track | Status | Evidence |
|------|-------|--------|----------|
| **Source feasibility** | All | PARTIAL | Hyperliquid liquidation feed admissible; Binance public archive not yet probed for sealed months |
| **Label decision** | Track A | DECIDED | Use Hyperliquid observed labels (incomplete census, documented); Track B/C viable without Track A |
| **Protocol freeze (FCLR-001)** | Track C | **NOT_STARTED** | Protocol fully specified in RESEARCH_PROMPT.md §14 — ready to freeze |
| **Baseline first** | Track C | **NOT_STARTED** | B0 (persistence) and B1 (RV-only HAR) implemented in `src/models/baselines.py` |
| **Incremental features** | Track C | **NOT_STARTED** | Funding + price features implemented in `src/features/{funding,price,volatility}.py` |
| **Forecast gate** | Track C | **NOT_STARTED** | Requires FCLR-001 completion with ≥2% QLIKE reduction, block-bootstrap CI, Holm correction |
| **Overlay eligibility** | — | BLOCKED | Requires forecast gate pass first |

---

## 5. Single highest-value next task

**Execute FCLR-001 frozen starter protocol (Track C: 24h forward realized variance forecasting)**

**Why this is the highest-value task:**
1. **Track A is power-blocked** — RISK-12 UNDERPOWERED, no credible path to detectable effect without larger panel
2. **Track C can proceed independently** — Uses mark-price data already in the frozen panel; no liquidation labels needed
3. **FCLR-001 is fully specified** — RESEARCH_PROMPT.md §14 gives exact unit, timing, universe, target, features, baselines, splits, metrics, inference, and gate
4. **Infrastructure is complete** — Ingestion, feature engineering, baselines (B0/B1), evaluation (QLIKE/MAE/RMSE), block bootstrap, walk-forward splits all implemented
5. **Honest null preservation** — If FCLR-001 fails, the null is preserved per protocol; no threshold shopping

**Exact FCLR-001 specification (from RESEARCH_PROMPT.md §14):**
- **Unit:** Eligible linear perpetual contract × closed UTC hourly timestamp
- **Primary target:** Next-24h realized variance of mark-price returns (sum of squared log returns over t+1..t+24)
- **Secondary horizons:** 6h, 72h, 168h (explicitly secondary, multiplicity-declared)
- **Features (causal, lagged):**
  - RV1h, RV24h, RV168h (trailing realized variances)
  - Signed funding (latest ≤ t)
  - Funding extremeness: 90-day absolute funding percentile (min 30 obs)
  - Premium: mark/index - 1 (aligned timestamps)
  - EMA24 deviation: mark / EMA24 - 1
- **Models (frozen):**
  - B0: persistence (RV24h)
  - B1: HAR-style OLS on log(RV1h, RV24h, RV168h) → log(target)
  - C1: B1 + signed funding + funding percentile
  - C2: C1 + premium + EMA24 deviation
- **Split:** 60%/20%/20% chronological, 7-day purge/embargo at boundaries (168h horizon)
- **Primary metric:** Paired out-of-sample QLIKE difference (C2 vs B1), block bootstrap CI (≥2000 reps)
- **Gate:** ≥2% relative QLIKE reduction, CI supports improvement, Holm over family passes

---

## 6. Precise command/check to verify completion

**Step 1: Freeze protocol and build panel**
```bash
# 1. Create research_state/research_protocol.md from RESEARCH_PROMPT.md §14
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

**Step 3: Run confirmatory evaluation on sealed holdout**
```bash
# After protocol freeze, run C1, C2 vs B1 on holdout
# Compute paired QLIKE diff, block bootstrap CI, Holm correction
# Verdict: FORECAST_GATE_PASSED or NOT_SUPPORTED
```

**Acceptance test for this session:**
- `research_state/research_protocol.md` exists and matches RESEARCH_PROMPT.md §14 exactly
- Panel built with frozen source hashes, cutoff dates, eligible sample definition recorded
- B0 and B1 evaluated on development/validation with metrics recorded
- No holdout outcomes inspected before protocol freeze

---

## 7. Source/engineering blockers and next free route

| Blocker | Evidence | Next materially different free route |
|---------|----------|--------------------------------------|
| **No Binance liquidation labels** | Binance public archive requires manual download or requester-pays; no unauthenticated historical liquidation feed found | **Track C volatility forecasting** — uses mark-price klines only (publicly available via Binance Vision archive) |
| **Track A power limit** | RISK-12 MDE=0.0028 > plausible 0.001; 13 coins, 12 months insufficient | **FCLR-001 Track C** — different outcome (volatility), different baseline (RV-only), different metric (QLIKE) |
| **Sealed Binance months unread** | RESEARCH_PROMPT.md prohibits reading sealed months for outcomes | **Use Hyperliquid panel for FCLR-001 development**; register separate Binance-arm protocol if/when archive access verified |
| **No historical market-cap ranks** | Free point-in-time ranks unavailable | **Venue-native universe** — all discoverable perpetuals from public listing metadata (per FCLR-001 §Unit) |

**Do not:**
- Re-run RISK-09/10/11/12 variants (explicitly prohibited in RISK-12 prereg)
- Attempt Track A liquidation forecasting without a materially larger panel
- Modify `.github/workflows` (protected control plane)
- Create placeholder artifacts — only create when contents are meaningful

---

## 8. Contingency ladder (if FCLR-001 blocked)

If FCLR-001 hits a structural blocker (e.g., mark-price data unavailable for adequate coverage):

1. **RISK-13** — Per RISK-12 evidence audit: advance only if MDE ≤ plausible effect via MDE-by-instrument redesign or larger panel
2. **Distinct-mechanism campaigns on frozen panel** (candidate queue):
   - (i) `liq_count` at t-1 persistence family
   - (ii) Within-hour cross-sectional funding-intensity contrast
   - (iii) UTC-hour / market-wide-RV conditioning of funding effect
3. **Track B modeled boundary-breach** — If contract specs and margin tiers verifiable from public sources

---

**Next session must:** Read this handoff + RESEARCH_PROMPT.md completely, inspect working tree and latest artifacts, then execute Step 1 of FCLR-001 (protocol freeze + panel build). No other task has higher expected information gain per unit of free compute.