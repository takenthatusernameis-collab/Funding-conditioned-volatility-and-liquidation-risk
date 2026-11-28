# HANDOFF_NEXT_SESSION — 20261128T090141Z

**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**PRIORITY:** Repo-name dual mandate — **Volatility half EXHAUSTED; Liquidation-risk half has ONE remaining HIGH-priority gap**

---

## CURRENT STATE (authoritative)

### ✅ VOLATILITY HALF — CLOSED (all confirmatory arms NOT_SUPPORTED)
- **Binance 5-symbol archive (FCLR-LIVE-ARCHIVE-01..08)**: COMPLETED_VALIDATED 2026-11-28T07:58:00Z
  - Mean-RV QLIKE (0.840% < 2% floor)
  - Stress/tail Brier (0.458% < 2%)
  - Quantile/full-distribution (−1.102%)
  - Signed-semivariance-asymmetry (0.141% < 2%)
  - Downside-semivariance-level (0.716% < 2%)
  - All 8 campaigns: independent stdlib recompute `all_checks_match=true`
- **Ironflow bulk Hyperliquid (FCLR-VOL-BROAD-01, CORR-01, STRESS-01, JUMP-01..04)**: COMPLETED_VALIDATED
  - Broad panel (300-450+ coins, 18 months): ALL NOT_SUPPORTED
  - Program closure FCLR-LIQ-RISK-PROGRAM-CLOSURE-02 executed 2026-11-25T06:00:00Z

**No further volatility work is warranted.** All estimands closed with replicated negative results.

### ⚠️ LIQUIDATION-RISK HALF — ONE HIGH-PRIORITY GAP REMAINS
**GAP-TRACKA-EARLY-OBSERVED-2025H2_2026Q1** (from `next_panel_gap_audit_20261111T163229Z.md`, priority: HIGH)
- **Objective**: Funding-conditioned features vs RV-only baseline for **next-24h observed Hyperliquid liquidation intensity** on a **new pre-registered panel/window disjoint from evaluated 2026-05..2026-10 holdout**, using **ironflow observed labels**
- **Cached inputs READY**:
  - Observed labels: `ironflow/hyperliquid-liquidations` 2025-05..2026-04 (18 monthly parquet files, ~2.8M rows, 468 markets, CC BY 4.0)
  - Funding: `ironflow/hyperliquid-funding` 2025-05..2026-04 (9 coins, CC BY 4.0)
- **MISSING (single bounded acquisition)**:
  - **Hyperliquid 1h candles (RV context) for 2025-05..2026-04** — NOT cached (only 2026-05..2026-10 present)
  - Required: Bounded first-time unauthenticated Hyperliquid `candleSnapshot` 1h fetch+cache with provenance for prereg-specified coins/months only
- **Constraints (NON-NEGOTIABLE)**:
  1. **Pre-register BEFORE any outcome computation/panel alignment** (JSON+md: hypothesis, exact window/symbols, label def/aggregation, feature set, splits/embargo ≥7d, baselines/contrasts B1 vs C2, metric, materiality threshold, minima ≥5 instruments + ≥3 non-overlapping 30d test blocks, inclusion rules, missingness handling)
  2. Fetch candles ONLY for prereg-specified coins/months; **do not re-fetch 2026-05..2026-10**
  3. Build deterministic aligned panel; emit parquet/json + build report with hashes/coverage/leakage-guard notes
  4. Run pre-registered evaluation ONLY after freeze artifacts exist; compute splits/embargo + bootstrap CIs per prereg
  5. Update `experiment_frontier.json`, `hypothesis_registry.json`, `run_manifest.json`, `final_confirmatory_verdict.md` atomically
  6. If prereg minima unsatisfiable → emit concrete infeasibility addendum with evidence; pivot to GAP-TRACKA-SYMBOL-EXPANSION-2026M05M10 (MEDIUM-HIGH)

### 🔒 FIREWALLS (immutable)
- **Track A**: Hyperliquid ironflow observed liquidations ONLY. NO Binance merge. Modeled ≠ observed.
- **Track B**: CLOSED_NEGATIVE (modeled boundary breaches)
- **Track C**: CLOSED (volatility-only, H001 NOT_SUPPORTED confirmatory)
- **H002**: PERMANENT_BLOCK (SSRN HTTP 403)
- **Gate 4 (Branch 1)**: EXTERNAL_BLOCKER_UNRESOLVED — **do not wait, do not poll**; Branch 2 executes independently

### 📋 RESUME CONDITION (from cross_track_decision_log.md)
> New admissible unauthenticated liquidation/funding source passing rubric (≥5 symbols, ≥3 non-overlapping 30-day blocks, documented completeness, license OK) OR SSRN H002 methodology accessible — **in either case pre-register a new experiment ID BEFORE outcome inspection**. Otherwise no further confirmatory work is warranted.

---

## NEXT SESSION MANDATORY TASK SEQUENCE

### PHASE 0 — PRE-REGISTRATION FREEZE (outcome-blind, mandatory first step)
**Create**: `research_state/prereg_tracka_early_observed_2025h2_2026q1_<UTC>.json` + `.md`
- Hypothesis: Funding-conditioned features (C2: rv1h, rv24h, rv168h, funding_rate, abs_funding, premium, ema_dist) improve out-of-sample forecasting of **next-24h observed liquidation intensity** vs RV-only baseline (B1: rv1h, rv24h, rv168h) on Hyperliquid native perps
- Universe: 9 coins with cached funding (BTC, ETH, SOL, BNB, XRP, AVAX, DOGE, LINK, SUI) — **frozen ex ante**
- Window: **2025-06-01 .. 2026-04-30** (disjoint from sealed 2026-05..2026-10)
- Label: ironflow observed liquidation events aggregated to hourly intensity per market (count/volume/notional — specify in prereg)
- Splits: Chronological, coin-pooled, 7d embargo, ≥3 non-overlapping 30d test blocks (e.g., 2025-10..2025-12, 2026-01..2026-02, 2026-03..2026-04)
- Primary contrast: C2_vs_B1; Metric: QLIKE or Brier (specify); Materiality floor: ≥2% relative improvement; CI: circular block bootstrap 168h, 2000 reps
- Holm family: 4 horizons (6h, 24h, 72h, 168h) × 3 contrasts (C2_vs_B1, C1_vs_B1, C2_vs_C1) = 12 tests
- `outcome_data_inspected_before_freeze: false`, `frozen_before_outcomes: true`, `pre_registered_before_outcomes: true`
- Record all data source URLs, licenses, checksums, access timestamps

### PHASE 1 — CANDLE ACQUISITION (bounded, provenance-recorded)
**Tool**: `scripts/fclr_ironflow_bulk.py` (or equivalent unauthenticated Hyperliquid candleSnapshot fetcher)
- Fetch **only** prereg-specified coins × months 2025-05..2026-04
- Cache under `research_state/data_cache/ironflow_bulk/candles_1h/<YYYY-MM>.parquet`
- Emit provenance sidecars: `<file>.sha256`, `<file>.accessed.json` (endpoint, params, UTC access time, HTTP status, unauthenticated/no-key/no-requester-pays/signature status)
- **Do not re-fetch 2026-05..2026-10** (already cached separately)

### PHASE 2 — DETERMINISTIC PANEL BUILD
- Align: observed labels (ironflow) + funding (ironflow) + candles (newly fetched) on hourly grid
- Leakage guard: decision-time features only (as-of merge backward, hour-floored); no forward fill; train-only standardization
- Emit: `research_state/tracka_early_observed_2025h2_2026q1_panel_<UTC>.parquet` + `tracka_early_observed_2025h2_2026q1_panel_build_report_<UTC>.json` (with SHA-256, coverage, drop counts, symbol/block breakdown)

### PHASE 3 — PRE-REGISTERED EVALUATION
- Run frozen protocol on test blocks only
- Compute: QLIKE/Brier per model/block/horizon, paired differences, block-bootstrap CIs, Holm adjustment
- Emit: `research_state/evaluation_summary_TRACKA-EARLY-OBSERVED-2025H2_2026Q1_<UTC>.md` + `.json`
- Verdict: PROMOTE_CANDIDATE / NOT_MET / INCONCLUSIVE per decision rule

### PHASE 4 — INDEPENDENT RECOMPUTE + EVIDENCE AUDIT + GATE ALIAS + TRIGGER CHECK
- Separate-code-path stdlib recompute from stored input hashes → `all_checks_match=true`
- Evidence audit: leakage check, subgroup diagnostics (LOIO, per-coin, per-block), calibration
- Gate alias + trigger check JSON
- All artifacts under `research_state/session_<UTC>/`

### PHASE 5 — ATOMIC STATE UPDATES
- Update `experiment_frontier.json` (new task entry, rank-0 if PROMOTE_CANDIDATE)
- Update `hypothesis_registry.json`, `run_manifest.json`, `final_confirmatory_verdict.md`
- **Preserve all prior NOT_MET and sealed records intact**

---

## STOP / PIVOT CONDITIONS
- **Valid Gate 4 RESOLVED_VERIFIED terms evidence appears** → switch to Branch 1 immediately
- **Any required source fails admissibility/provenance verification** → do not use; document and pivot to GAP-TRACKA-SYMBOL-EXPANSION-2026M05M10
- **Prereg minima unsatisfiable on audited data** → emit infeasibility addendum with evidence; pivot per GAP-TRACKA-SYMBOL-EXPANSION rules

---

## FORBIDDEN ACTIONS (will invalidate session)
- ❌ Any outcome computation/panel alignment **before** preregistration freeze artifacts exist
- ❌ Reading/scoring sealed 2026-05..2026-10 holdout for any purpose
- ❌ Using Binance/2024 data or mixing venues in one panel
- ❌ Presenting modeled/proxy liquidation labels as observed
- ❌ Threshold/model/feature/split tuning against test blocks
- ❌ Re-scoring/re-weighting/re-labelling sealed volatility verdicts
- ❌ Using secondary-family (open-interest) results to promote any claim
- ❌ Editing `.github/workflows/*`
- ❌ Committing raw bulk parquet objects or caches
- ❌ Adding root-level `research_state/*.md|*.json` (root at cap 500 — all new artifacts under `session_<UTC>/`)

---

## SUCCESS CRITERIA (session not complete without)
1. Preregistration JSON+MD frozen **before** any outcome computation (`outcome_data_inspected_before_freeze: false`)
2. Candle acquisition provenance recorded (sidecars + manifest)
3. Deterministic panel built with hashes/coverage/leakage-guard notes
4. Pre-registered evaluation executed on frozen test blocks only
5. Independent stdlib recompute `all_checks_match=true`
6. Evidence audit + gate alias + trigger check produced
7. Atomic state updates to frontier/registry/manifest/verdict
8. All artifacts non-empty under `research_state/session_<UTC>/`

---

**This is the only remaining confirmatory path on the repo's namesake topic. Execute Phase 0 immediately. No planning, no discussion — heavy work only.**