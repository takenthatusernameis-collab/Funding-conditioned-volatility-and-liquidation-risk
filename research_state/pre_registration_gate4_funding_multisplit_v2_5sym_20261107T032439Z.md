# Pre-registration — Gate 4 Funding-Conditioned Volatility Ablations v2 (5 symbols, exploratory pilot)
**ID:** GATE4-FUND-VOL-ABLATIONS-MSPLIT-V2-5SYM
**Timestamp (UTC, frozen before outcomes):** 2026-11-07T03:24:39Z
**Status:** FROZEN (before running v2 outcomes / reading v2 result tables)
**Scope:** **EXPLORATORY PILOT ONLY.** Adds BNBUSDT to the v1 instrument set using local admissible data; v1 (`GATE4-FUND-VOL-ABLATIONS-MSPLIT-20261107`) remains unchanged. This document does **not** promote any confirmatory claim, economic value, or overlay.
**Authority:** `AGENT_HANDOFF.md` (root) is the single durable session handoff.

## 1. Research question (pilot)
Using locally available, admissible, leakage-resistant data, does adding funding-conditioned features to a direct-variance HAR baseline reduce out-of-sample QLIKE versus a realized-vol-only baseline across pre-registered chronological splits and the 5-symbol joint panel (BTC, ETH, SOL, XRP, BNB)?

## 2. Data (local only; no creds/paid/manual downloads)
- **Symbols:** `BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT, BNBUSDT` (v1 + BNBUSDT; 5 instruments total).
- **Klines:** 1h per-symbol daily zip CSVs in repo root (e.g., `SYMBOL-1h-YYYY-MM-DD.zip`) for 2024-01-01..2024-03-30 where present; merged chronologically. OHLCV schema with `open_time`.
- **Funding:** monthly `SYMBOL-fundingRate-YYYY-MM.zip` CSVs (columns include `calc_time`, `last_funding_rate`) for 2024-01..2024-03.
- **Basis/premium:** **omitted** (no aligned admissible local series verified). Do not fabricate.
- **Missing handling:** missing remains NaN/absent; **missing is never treated as zero**.

## 3. Leakage / alignment (non-negotiable)
- Chronological only. No random CV.
- Funding aligned to bar time with `merge_asof(direction="backward")`; no future funding used for current bar.
- Target is forward realized variance over `horizon=24` hours computed from **future** returns; final horizon rows excluded by construction.
- Purge/embargo: last 7 days (`168h`) of each train segment removed before contiguous test.
- Normalization: train-only means/stds; applied to val/test. Rows with NaN in required features/target dropped per ablation.

## 4. Splits (same as v1; Q1 2024 local window)
Three walk-forward splits with 14-day contiguous test windows (fits local data; **does not satisfy 30-day non-overlapping claim-worthy criterion**):
- Split 1: train ends 2024-01-29, test 2024-02-05..2024-02-18
- Split 2: train ends 2024-02-12, test 2024-02-19..2024-03-03
- Split 3: train ends 2024-02-26, test 2024-03-04..2024-03-17

## 5. Model family (primary, pre-registered)
Direct-variance HAR-style OLS (no log/exp, no neural models):
- **A (RV only):** `rv_trail_24, rv_trail_168, rv_trail_6`
- **B (+ signed funding):** A + `funding_signed`
- **C (+ abs funding):** A + `funding_abs`
- **D (+ signed + abs):** A + `funding_signed, funding_abs`
- **E (+ funding trails):** D + available `funding_pct_*` / `funding_z_*` trail features

## 6. Primary contrasts / metrics
- **Primary metric:** QLIKE on variance forecasts (lower is better).
- **Primary contrast:** E vs A (paired) with moving block bootstrap 95% CI, block=24h, reps=2000, seed=12345, joint across instruments.
- **Secondary (exploratory, not claim-bearing):** per-split paired ΔQLIKE and block-size sensitivity (12h/24h/48h) as in v1 exploratory addendum method; no new confirmatory claims from sensitivity.

## 7. Data-sufficiency / claim rules (binding)
- v2 satisfies `instruments >= 5` for the pilot dataset **if** BNBUSDT loads/aligns cleanly; record actual instrument count.
- **Still NOT claim-worthy:** Q1 2024 local data cannot fit >=3 non-overlapping **30-day** test blocks with train/purge. Verdict must remain **PILOT/INCONCLUSIVE** absent additional admissible local months and a new prereg for 30-day blocks.
- No confirmatory claim, no economic value, no liquidation overlay, no Track A conflation.

## 8. Outputs (v2-labeled; do not overwrite v1)
- `research_state/evaluation_summary_funding_v2_5sym.md`
- `research_state/pre_registration_gate4_funding_multisplit_v2_5sym_20261107T032439Z.md` (this file)
- `research_state/run_manifest_funding_v2_5sym.json`
- `research_state/leakage_audit.md` (append/update only if needed; must remain clean)
- `AGENT_HANDOFF.md` updated with v2 results and next campaign.

## 9. Integrity
Observed liquidations ≠ modeled boundary breaches ≠ volatility/stress. Track A remains guarded/no trigger. No workflow changes.
