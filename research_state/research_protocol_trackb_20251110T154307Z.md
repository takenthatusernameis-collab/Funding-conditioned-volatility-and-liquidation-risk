# Research Protocol — Track B Modeled Liquidation Boundary Breaches (TRACKB-MODELED-BREACH-20261110T154307Z)

**Protocol ID:** trackb_20251110T154307Z
**Timestamp (UTC):** 2026-11-10T15:43:07Z
**Status:** FROZEN_BEFORE_OUTCOMES
**Track:** Track B (liquidation risk)
**Type:** Modeled/synthetic boundary proxy — **NOT observed liquidations**

## 1) Objective
Evaluate whether funding extremes / funding-conditioned features improve detection of *synthetic* mark-price boundary breaches relative to price/RV-only features, using a strict out-of-sample chronological split with no outcome inspection before freeze.

## 2) Definitions (explicit)
- **Target (synthetic):** Modeled breach of a liquidation boundary at horizon H given entry price at t, leverage L, side (long/short), maintenance margin rate m (explicit assumption). Implementation follows `scripts/synthetic_boundary_labels.py` (leakage-safe: boundary computed from entry, future min/max checked only over t+1..t+H).
- **Proxy only:** `synthetic_boundary_label` is a modeled proxy ≠ observed liquidation events, account-specific margin, or exchange execution. No inference to realized liquidation counts/rates without an admissible observed-liquefaction census.
- **Sides/scenarios (pre-specified):**
  - Primary: long @ 5x, m=0.0, H=24h (entry = mark close at t)
  - Secondary (confirmatory sanity): short @ 5x, m=0.0, H=24h; long/short @ 10x robustness
- **Materiality:** >= 2% relative improvement in primary contrast vs baseline (pre-specified floor). Multiplicity: Holm adjustment across pre-specified contrasts.

## 3) Universe & Data
- **Symbols:** BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT
- **Window (candidate):** 2025-01-01 .. 2025-10-31 (contiguous). Must satisfy provenance_verified=true, unmapped_count==0, all required series (mark/index/premium/klines) and funding schema complete.
- **Sources:** local verified cache (markPriceKlines, indexPriceKlines, premiumIndexKlines, klines, fundingRate) with adjacent sha256 sidecars / manifest-verified hashes. No network.

## 4) Splits (chronological, frozen before outcomes)
- **Rule:** 60% train / 20% validation / 20% test by time, with **7-day purge/embargo** between partitions (applied to avoid temporal leakage across split boundaries).
- **Requirement:** Test split must contain **>= 3 non-overlapping 30-day blocks**. If not satisfied by the chosen window, select the nearest earlier fully-verified local window that satisfies it and record rationale in admissibility artifact.
- **No reuse:** Do not reuse FCLR-009 inspected window (2025-06-08..2025-12-31).

## 5) Features (leakage-safe)
- Baseline B1: price/RV-only features computable from past (rolling RV, returns lags, ranges) — train-only transforms.
- C1/C2 (funding-conditioned): pre-specified funding features (funding rate, funding z/rolling extremes, time-since-funding, basis/premium/index dislocation where available) — train-only transforms/scaling. No future information.

## 6) Evaluation
- **Primary contrast:** C2 vs B1 (improvement in predicting synthetic boundary breach; metric consistent with protocol, e.g. AUC/log loss or classification performance as implemented; direction and materiality fixed before outcomes)
- **Uncertainty:** block bootstrap over time blocks (>=2000 reps), report 95% CI
- **Gates (all required):**
  1. >=5 instruments in evaluation
  2. >=3 non-overlapping 30-day blocks in test split
  3. Relative improvement >= 2% (materiality floor)
  4. 95% CI excludes null in the favorable direction (or meets pre-specified decision rule)
  5. Multiplicity controlled (Holm) across pre-specified contrasts
- **Overlay:** NOT ELIGIBLE unless all gates pass. Label as synthetic proxy throughout.

## 7) Preregistration (frozen)
- **prereg_hash:** computed from this protocol file content (sha256) before outcome/label inspection
- **Frozen flag:** `split_boundaries_trackb_20251110T154307Z.frozen_before_outcomes = true` recorded in `research_state/run_manifest.json` before computing labels/outcomes
- **Violation:** Any inspection of labels/outcomes before freeze invalidates confirmatory claim.

## 8) Handoff requirements
Write `research_state/evaluation_summary_trackb_20251110T154307Z.md` with: point estimates, 95% CI, relative change, n_instruments, n_obs, n_test_blocks, materiality/gate, Holm, provenance refs. Update hypothesis registry, experiment frontier, negative results report, AGENT_HANDOFF.md, NEXT_SESSION_TASK.md with timestamped outcomes and single `next_unfinished_task`.
