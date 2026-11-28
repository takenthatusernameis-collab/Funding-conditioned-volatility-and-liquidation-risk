# DURABLE HANDOFF — SINGLE SOURCE OF TRUTH — 20261128T090746Z

**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**STATUS:** LIQUIDATION-RISK HALF HAS ONE UNBLOCKED HIGH-PRIORITY GAP — EXECUTE HEAVY WORK NOW
**SUPERSEDES:** `AGENT_HANDOFF.md`, `AGENT_HANDOFF_20261128T090515Z.md` (false "CLOSED_TERMINAL / do nothing"), `AGENT_HANDOFF_20261128T085828Z.md`, `AGENT_HANDOFF_20261128T085521Z`, and all `AGENT_HANDOFF_2026*.md`. This file is the only authoritative next-session instruction.

---

## 0. INITIAL TASK MESSAGE FOR THE NEXT AGENTIC SESSION (read this first)

> You are resuming the FCLR program. The repo name mandates two halves: **funding-conditioned volatility** and **liquidation risk**. The volatility half is EXHAUSTED (every confirmatory arm NOT_SUPPORTED, independently recomputed). The liquidation-risk half has exactly ONE remaining pre-registered gap, `GAP-TRACKA-EARLY-OBSERVED-2025H2_2026Q1`, and **all required data is already on disk**. Your job is NOT to look for work, NOT to re-litigate closed tracks, and NOT to declare closure. Your job is to execute the 5-phase confirmatory campaign below to a verdict. Heavy work only. No planning, no discussion.
>
> **The single biggest bottleneck has been REMOVED:** the prior handoff claimed Hyperliquid 1h candles for 2025-05..2026-04 were MISSING and had to be fetched. They are NOT missing. `research_state/data_cache/ironflow_bulk/candles_1h/` already holds 18 monthly parquets (2025-05 .. 2026-10) with `.sha256` + `.accessed.json` provenance (unauthenticated, no API key, requester_pays=false, CC-BY-4.0). **Phase 1 acquisition is a NO-OP. Do NOT re-fetch. Do NOT touch 2026-05..2026-10 (sealed holdout).** Go straight to Phase 0.

---

## 1. WHY THIS IS THE PRIORITY (repo-name derived)

- **Half 1 — Funding-conditioned volatility: CLOSED.** Binance 5-symbol archive (FCLR-LIVE-ARCHIVE-01..08) + Ironflow broad panel (FCLR-VOL-BROAD/CORR/STRESS/JUMP-01..04) all COMPLETED_VALIDATED, all NOT_SUPPORTED, all `all_checks_match=true`. No further volatility work is warranted.
- **Half 2 — Liquidation risk: ONE HIGH gap remains.** `GAP-TRACKA-EARLY-OBSERVED-2025H2_2026Q1` (priority HIGH, from `research_state/next_panel_gap_audit_20261111T163229Z.md`): funding-conditioned features vs RV-only baseline for **next-24h observed Hyperliquid liquidation intensity** on a window **disjoint from the sealed 2026-05..2026-10 holdout**, using **ironflow observed labels**.

---

## 2. DATA READINESS (verified on disk 2026-11-28T09:07Z — no acquisition needed)

| Input | Path | State |
|---|---|---|
| Observed liquidation labels | `research_state/data_cache/ironflow_bulk/liquidations/2025-05..2026-04.parquet` (18 files) | READY |
| Funding | `research_state/data_cache/ironflow_bulk/funding/2025-05..2026-04.parquet` (18 files) | READY |
| 1h candles (RV context) | `research_state/data_cache/ironflow_bulk/candles_1h/2025-05..2026-04.parquet` (18 files + `.sha256` + `.accessed.json`) | **READY (previously mislabeled missing)** |
| Sealed holdout (DO NOT READ) | `.../candles_1h/2026-05..2026-10.parquet` | SEALED — never score |

Fetchers exist if ever needed (`scripts/fclr_ironflow_bulk.py`) but are NOT to be run for this window.

---

## 3. MANDATORY CAMPAIGN — EXECUTE IN ORDER, NO SKIPPING

### PHASE 0 — PRE-REGISTRATION FREEZE (outcome-blind; FIRST action)
Create `research_state/session_<UTC>/prereg_tracka_early_observed_2025h2_2026q1_<UTC>.{json,md}`:
- Hypothesis: C2 (rv1h, rv24h, rv168h, funding_rate, abs_funding, premium, ema_dist) improves OOS next-24h observed liquidation intensity vs B1 (rv1h, rv24h, rv168h).
- Universe (frozen ex ante): 9 coins with cached funding (BTC, ETH, SOL, BNB, XRP, AVAX, DOGE, LINK, SUI).
- Window: **2025-06-01 .. 2026-04-30** (disjoint from sealed 2026-05..2026-10).
- Label: ironflow observed liquidation events → hourly intensity per market (count/volume/notional — specify).
- Splits: chronological, coin-pooled, **7d embargo**, ≥3 non-overlapping 30d test blocks.
- Primary contrast C2_vs_B1; metric QLIKE or Brier (specify); materiality floor ≥2% relative; CI circular block bootstrap 168h, 2000 reps.
- Holm family: 4 horizons (6h,24h,72h,168h) × 3 contrasts = 12 tests.
- Set `outcome_data_inspected_before_freeze:false`, `frozen_before_outcomes:true`, `pre_registered_before_outcomes:true`. Record source URLs, licenses, checksums, access timestamps.

### PHASE 1 — ACQUISITION: **NO-OP** (data cached). Verify sidecar hashes, do not fetch.

### PHASE 2 — DETERMINISTIC PANEL BUILD
Align labels + funding + candles on hourly grid; as-of backward merge, hour-floored, no forward fill, train-only standardization. Emit `..._panel_<UTC>.parquet` + `..._panel_build_report_<UTC>.json` (SHA-256, coverage, drop counts, symbol/block breakdown, leakage-guard notes).

### PHASE 3 — PRE-REGISTERED EVALUATION (frozen test blocks only)
QLIKE/Brier per model/block/horizon, paired diffs, block-bootstrap CIs, Holm. Emit `evaluation_summary_TRACKA-EARLY-OBSERVED-2025H2_2026Q1_<UTC>.{md,json}`. Verdict PROMOTE_CANDIDATE / NOT_MET / INCONCLUSIVE.

### PHASE 4 — INDEPENDENT RECOMPUTE + EVIDENCE AUDIT + GATE ALIAS + TRIGGER CHECK
Separate stdlib code path from stored input hashes → `all_checks_match=true`; leakage/subgroup (LOIO, per-coin, per-block)/calibration audit; gate alias + trigger check JSON. All under `session_<UTC>/`.

### PHASE 5 — ATOMIC STATE UPDATES
Update `experiment_frontier.json` (new entry, rank-0 if PROMOTE_CANDIDATE), `hypothesis_registry.json`, `run_manifest.json`, `final_confirmatory_verdict.md`. Preserve all prior NOT_MET and sealed records intact.

---

## 4. STOP / PIVOT
- Prereg minima unsatisfiable on audited data → emit infeasibility addendum with evidence; pivot to `GAP-TRACKA-SYMBOL-EXPANSION-2026M05M10` (MEDIUM-HIGH).
- Any source fails provenance/admissibility → do not use; document; pivot per above.
- Valid Gate-4 RESOLVED_VERIFIED external evidence appears → switch to Branch 1.

## 5. FORBIDDEN (invalidates session)
- ❌ Declaring the program "CLOSED_TERMINAL / do nothing" — that prior handoff is superseded and wrong; the liquidation gap is open and unblocked.
- ❌ Any outcome computation/panel alignment before Phase 0 freeze artifacts exist.
- ❌ Reading/scoring sealed 2026-05..2026-10 holdout.
- ❌ Re-fetching candles 2025-05..2026-04 (already cached) or using Binance/2024 data / mixing venues.
- ❌ Presenting modeled/proxy labels as observed; threshold/model/split tuning on test blocks.
- ❌ Re-scoring sealed volatility verdicts; editing `.github/workflows/*`; committing raw parquet/caches.
- ❌ Adding root-level `research_state/*.md|*.json` (root at cap 500 — all new artifacts under `session_<UTC>/`).

## 6. SUCCESS CRITERIA (session incomplete without all)
1. Prereg JSON+MD frozen before outcomes (`outcome_data_inspected_before_freeze:false`).
2. Panel built with hashes/coverage/leakage-guard notes (no acquisition).
3. Pre-registered evaluation on frozen test blocks only.
4. Independent stdlib recompute `all_checks_match=true`.
5. Evidence audit + gate alias + trigger check produced.
6. Atomic frontier/registry/manifest/verdict updates.
7. All artifacts non-empty under `research_state/session_<UTC>/`.

---
*Single durable handoff generated 2026-11-28T09:07:46Z. Execute Phase 0 immediately. Heavy work only.*