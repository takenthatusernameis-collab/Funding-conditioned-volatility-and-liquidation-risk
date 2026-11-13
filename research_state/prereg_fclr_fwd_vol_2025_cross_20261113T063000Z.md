# Prereg — FCLR-FWD-VOL-2025-CROSS-20261113T063000Z (Track C, P2)

**Status:** `FROZEN_PRE_OUTCOMES`
**Frozen (UTC):** 2026-11-13T06:30:00Z
**Outcome data inspected before freeze:** false
**Campaign:** `FCLR-NEXT-CAMPAIGN-20261113T063000Z`
**Cell:** `FWD-VOL-2025-CROSS`

## Claim
The FCLR-011 funding-conditioned volatility PASS is period-specific to 2026-05..2026-08
and does NOT replicate on a pre-registered 2025-02..2025-05 rolling-origin walk-forward.
A CONFIRMED verdict requires ≥2% relative QLIKE reduction, 95% block-bootstrap CI
excluding zero, ≥5 instruments, 3 non-overlapping 30-day test blocks, Holm across 12
cells, LOIO ≥4/5, placebo PASS, and a no-leakage sensitivity.

## Why this is new
- The 2026-08..2026-10 forward window returned NOT_REPLICATED. This cell tests the
  complementary period: a non-overlapping 2025 window that precedes the sealed FCLR-011
  train start (2026-01-01) and is therefore genuinely out-of-sample in time.
- 2025 window is non-overlapping with the sealed test (2026-05-08..2026-08-06) and the
  forward window (2026-08..2026-10).

## Data (cached only)
- Binance 1h mark/premium/index/funding for BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT.
- Window 2024-12-01..2025-06-01; 3 × 30-day test blocks with 7-day embargo.

## Models (fixed)
- B0: `log_rv24h`.
- B1: `log_rv1h`, `log_rv24h`, `log_rv168h`.
- C1: B1 + `signed_funding`, `abs_fund_pct`.
- C2: C1 + `premium`, `ema_dist`.

## Splits
- Train start 2024-12-01; blocks test 2025-02-04..03-05, 2025-03-07..04-05,
  2025-04-07..05-06.

## Gates
- Materiality ≥ 2%; CI excludes zero; ≥5 instruments; 3 blocks.
- Bootstrap 2000 reps (day-block), seed 20261113; Holm across 12 cells.
- Placebo 200 funding permutations, seed 20261113; LOIO ≥4/5.

## Verdict rules
- `NOT_REPLICATED`: primary CI includes zero or rel reduction < 2%.
- `CONFIRMED`: all checks pass.
- `INCONCLUSIVE`: insufficient valid rows or pipeline defect.

## Artifacts
- `research_state/tracka_fwd_vol_2025_cross_panel_<UTC>.parquet`
- `research_state/tracka_fwd_vol_2025_cross_build_report_<UTC>.json`
- `research_state/evaluation_summary_FCLR-FWD-VOL-2025-CROSS-<UTC>.{md,json}`
- Gate: `scripts/fclr_fwd_vol_2025_cross_gate.py` → `GATE: PASS`.

## Bans
No network; no mutation of sealed artifacts; no threshold shopping; no core-feature fill;
2025 window must stay non-overlapping with the sealed test window.