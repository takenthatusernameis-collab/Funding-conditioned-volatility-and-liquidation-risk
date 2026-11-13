# Prereg — FCLR-EXP-ROBUST-REDO-20261113T063000Z (Track A, P2)

**Status:** `FROZEN_PRE_OUTCOMES`
**Frozen (UTC):** 2026-11-13T06:30:00Z
**Outcome data inspected before freeze:** false
**Campaign:** `FCLR-NEXT-CAMPAIGN-20261113T063000Z`
**Cell:** `EXP-ROBUST-REDO`

## Claim
A new expansion-robustness design on the sealed expansion panel meets LOIO ≥ 6/8 AND
placebo PASS, which would upgrade the prior FRAGILE 19.04% PASS toward ROBUST. The
prior sealed 19.04% PASS (LOIO 4/8, placebo null p95 21.10% ≥ true 19.04%) is FRAGILE
and is NOT re-scored.

## Data (cached only)
- Panel: `research_state/tracka_hl_expansion_panel_20261111T202344Z.parquet`
  (sha256 `39916a72...66f699`).

## Splits (identical to sealed PASS)
- Train 2026-05-01..2026-05-31; Val 2026-06-07..2026-06-30.
- Test blocks: 2026-07-07..08-06, 2026-08-13..09-11, 2026-09-18..10-17.

## Models (fixed)
- B1: `log_rv1h`, `log_rv24h`, `log_rv168h`.
- C2: B1 + `fundingRate`, `abs_fund_pct`, `premium`, `ema_dist`.

## Gates
- LOIO ≥ 6/8; materiality ≥ 2%; CI excludes zero.
- Placebo: 2000 permutations, seed 20261113; PASS iff null p95 < true rel reduction.
- Bootstrap: 2000 reps, seed 20261113.

## Verdict rules
- `ROBUST`: LOIO ≥6/8 AND placebo PASS AND materiality AND CI excludes zero.
- `FRAGILE`: primary passes but LOIO or placebo fails.
- `INCONCLUSIVE`: insufficient valid rows / data defect.

## Artifacts
- `research_state/evaluation_summary_FCLR-EXP-ROBUST-REDO-<UTC>.{md,json}`
- Gate: `scripts/fclr_exp_robust_redo_gate.py` → `GATE: PASS`.

## Bans
No network; no mutation of the sealed panel or prior verdict; no lowered bars; no
re-scoring the FRAGILE PASS as a PASS.