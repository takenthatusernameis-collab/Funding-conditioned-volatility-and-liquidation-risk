# AGENT HANDOFF — 2026-11-28T09:08:34Z (DURABLE SINGLE SOURCE OF TRUTH)

**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**STATUS:** HALF 1 (funding-conditioned volatility) CLOSED — all confirmatory arms NOT_SUPPORTED/NOT_MET. HALF 2 (liquidation risk) has ONE unblocked HIGH gap — EXECUTE HEAVY WORK NOW.
**SUPERSEDES:** `HANDOFF_NEXT_SESSION.md` (20261128T090746Z), `AGENT_HANDOFF.md` (all prior timestamps), `AGENT_HANDOFF_20261128T090515Z.md`, `AGENT_HANDOFF_20261128T085828Z.md`, and all `AGENT_HANDOFF_2026*.md`. This file is the only authoritative next-session instruction.

---

## 0. INITIAL TASK MESSAGE FOR THE NEXT AGENTIC SESSION (read this first)

> You are resuming the FCLR program. The repo name mandates two halves: **funding-conditioned volatility** and **liquidation risk**. The volatility half is EXHAUSTED (every confirmatory arm NOT_SUPPORTED/NOT_MET, independently recomputed). The liquidation-risk half has exactly ONE remaining pre-registered gap, `GAP-TRACKA-EARLY-OBSERVED-2025H2_2026Q1`, and **all required data is already on disk**. Your job is NOT to look for work, NOT to re-litigate closed tracks, and NOT to declare closure. Your job is to execute the 5-phase confirmatory campaign below to a verdict. Heavy work only. No planning, no discussion.
>
> **The single biggest bottleneck has been REMOVED:** the prior handoff claimed Hyperliquid 1h candles for 2025-05..2026-04 were MISSING and had to be fetched. They are NOT missing. `research_state/data_cache/ironflow_bulk/candles_1h/` already holds 18 monthly parquets (2025-05 .. 2026-10) with `.sha256` + `.accessed.json` provenance (unauthenticated, no API key, requester_pays=false, CC-BY-4.0). **Phase 1 acquisition is a NO-OP. Do NOT re-fetch. Do NOT touch 2026-05..2026-10 (sealed holdout).** Go straight to Phase 0.

---

## 1. WHY THIS IS THE PRIORITY (repo-name derived)

- **Half 1 — Funding-conditioned volatility: CLOSED.** Binance 5-symbol archive (FCLR-LIVE-ARCHIVE-01..08) + Ironflow broad panel (FCLR-VOL-BROAD/CORR/STRESS/JUMP-01..04) all COMPLETED_VALIDATED, all NOT_SUPPORTED/NOT_MET, all `all_checks_match=true`. No further volatility work is warranted.
- **Half 2 — Liquidation risk: ONE HIGH gap remains.** `GAP-TRACKA-EARLY-OBSERVED-2025H2_2026Q1` (priority HIGH, from `research_state/next_panel_gap_audit_20261111T163229Z.md`): funding-conditioned features vs RV-only baseline for **next-24h observed Hyperliquid liquidation intensity** on a window **disjoint from the sealed 2026-05..2026-10 holdout**, using **ironflow observed labels**.

---

## 2. DATA READINESS (verified on disk 2026-11-28 — no acquisition needed)

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

---

## 5. FORBIDDEN (invalidates session)

- ❌ Declaring the program "CLOSED_TERMINAL / do nothing" — that prior handoff is superseded and wrong; the liquidation gap is open and unblocked.
- ❌ Any outcome computation/panel alignment before Phase 0 freeze artifacts exist.
- ❌ Reading/scoring sealed 2026-05..2026-10 holdout.
- ❌ Re-fetching candles 2025-05..2026-04 (already cached) or using Binance/2024 data / mixing venues.
- ❌ Presenting modeled/proxy labels as observed; threshold/model/split tuning on test blocks.
- ❌ Re-scoring sealed volatility verdicts; editing `.github/workflows/*`; committing raw parquet/caches.
- ❌ Adding root-level `research_state/*.md|*.json` (root at cap 500 — all new artifacts under `session_<UTC>/`).

---

## 6. SUCCESS CRITERIA (session incomplete without all)

1. Prereg JSON+MD frozen before outcomes (`outcome_data_inspected_before_freeze:false`).
2. Panel built with hashes/coverage/leakage-guard notes (no acquisition).
3. Pre-registered evaluation on frozen test blocks only.
4. Independent stdlib recompute `all_checks_match=true`.
5. Evidence audit + gate alias + trigger check produced.
6. Atomic frontier/registry/manifest/verdict updates.
7. All artifacts non-empty under `research_state/session_<UTC>/`.

---

## 7. VERIFICATION COMMAND

```bash
python -c "
import json
with open('research_state/experiment_frontier.json') as f:
    data = json.load(f)
for item in data:
    if item.get('rank') == 0:
        print('Rank 0:', item['task'], '|', item.get('program_status'), '|', item.get('last_verdict'))
        print('Next heavy:', item.get('next_action_heavy'))
        print('Blockers:', item.get('blockers'))
"
```

Expected: rank-0 reflects GAP-TRACKA-EARLY-OBSERVED-2025H2_2026Q1 with `next_action_heavy` NOT "NONE" until the 5-phase campaign completes.

---

## 8. CURRENT STATE OF EVERY RESEARCH GATE

| Track / Estimand | Status | Verdict | Basis |
|---|---|---|---|
| Half 1: Funding-conditioned volatility (Binance 5-symbol archive) | CLOSED | NOT_SUPPORTED | All arms rel < 2% floor or CI crosses zero |
| Half 1: Funding-conditioned volatility (Hyperliquid ironflow_bulk) | CLOSED | NOT_SUPPORTED | Broad panel arms all < 2% floor |
| Half 2: Track A observed liquidation (`GAP-TRACKA-EARLY-OBSERVED-2025H2_2026Q1`) | OPEN | — | **UNBLOCKED HIGH gap — execute now** |
| Half 2: Track B modeled boundary-breach | CLOSED | NOT_SUPPORTED | Modeled proxy ≠ account-specific liquidation |
| Half 2: Track C volatility/stress outcome | CLOSED | NOT_SUPPORTED | No arm cleared frozen materiality floor |
| Cross-sectional regime funding → liq-intensity | CLOSED | SUPPORTED_GENERALIZATION / NOT_STABLE | 2% floor NOT MET |

---

## 9. BOTTLENECKS REMOVED

- **Data acquisition NO-OP:** `ironflow_bulk/candles_1h/2025-05..2026-04` (18 parquets + sidecars) already on disk — previously mislabeled as missing. Do NOT re-fetch.
- **No closed campaigns to re-run:** all `next_action_heavy: NONE` for closed rank 0–6 entries in `experiment_frontier.json`.
- **No threshold-shopping:** all materiality floors frozen before outcomes.
- **No track adulteration:** firewall intact — Hyperliquid (Track A) never merged with Binance (Track B/C).
- **No overlay built:** forecast gate (RESEARCH_PROMPT.md §9) never passed.
- **No root-level artifact sprawl:** all new artifacts under `session_<UTC>/`; root cap 500 enforced.

---

## 10. DURABLE HANDOFF CONTRACT (Per RESEARCH_PROMPT.md §12)

1. **What changed:** `AGENT_HANDOFF.md` refreshed as single durable source of truth superseding `HANDOFF_NEXT_SESSION.md` and all prior `AGENT_HANDOFF_*.md`. Half 1 closed; Half 2 has one unblocked HIGH gap with all data cached.
2. **What was tested:** Every confirmatory arm on both halves executed, independently recomputed, audited → NOT_SUPPORTED/NOT_MET.
3. **Evidence added:** Complete artifact sets under prior `session_<UTC>/` dirs; `experiment_frontier.json` reflects closure of Half 1 and all closed Half 2 tracks.
4. **Gate states:** All confirmatory gates RESOLVED (NOT_SUPPORTED/NOT_MET/STRUCTURALLY_BLOCKED) except `GAP-TRACKA-EARLY-OBSERVED-2025H2_2026Q1` which is OPEN and UNBLOCKED.
5. **Next task:** Execute Phase 0 of the 5-phase campaign (prereg freeze) → Phases 1–5 to verdict. Heavy work only.
6. **Verification command:** See §7.
7. **Blockers & free route:** No external blockers. Only materially different route is a NEW unauthenticated source passing the rubric (§5 of HANDOFF_NEXT_SESSION.md logic); FCLR-NEXT-002 already tested 8 source families.

---

**Timestamp:** 2026-11-28T09:08:34Z
**Session ID:** handoff_20261128T090834Z
**Git HEAD:** (run `git rev-parse HEAD` to verify)
**Next agent:** Execute Phase 0 immediately. Heavy work only.
