# Frozen Prereg — FCLR-FWD-VOL-2025-DISJOINT-CROSS-20261114T183000Z

**Status:** FROZEN_PRE_OUTCOMES
**Frozen:** 2026-11-14T18:30:00Z
**Track:** C_volatility_exploratory
**Priority:** P1
**Hypothesis:** `H_fclr_fwd_vol_2025_disjoint_cross`
**Max status:** `EXPLORATORY_ONLY` (`promotable=false`)

## Claim

The sealed FCLR-011 funding-conditioned volatility PASS (C2 vs B1, +4.94% relative QLIKE reduction, 5 instruments, 3 blocks, 2026-05..2026-08) does not produce the same direction/magnitude on three disjoint, never-tested 30-day Binance test blocks: 2025-06, 2025-11, 2025-12.

This is an exploratory transportability audit. It cannot promote H1 or claim confirmatory status while Gate 4 Binance v5 terms evidence remains unresolved.

## Why this is new

- None of the three test months has been used as a test block in prior cells.
- Test months are disjoint from every prior tested window.
- The sealed FCLR-011 artifact is not mutated or re-scored.
- No liquidation label is consumed; this arm is volatility-only.
- Train months may overlap earlier tested periods as legitimate pre-test history.
- 2024-06 is also feasible according to `scripts/next_campaign_status.py`, but is excluded to keep a single 2025 regime and avoid early-funding warm-up.

## Design

- Universe: BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT
- Features: B0, B1, C1, C2 as in FCLR-011
- Primary contrast: C2 vs B1
- Primary metric: QLIKE
- Three disjoint 30-day test blocks, each with its own 30-day train window and a 7-day embargo:

| block | train start | train end | test start | test end | days |
|---|---|---|---|---|---|
| 0 | 2025-04-25T00:00:00Z | 2025-05-24T23:00:00Z | 2025-06-01T00:00:00Z | 2025-06-30T23:00:00Z | 30 |
| 1 | 2025-09-25T00:00:00Z | 2025-10-24T23:00:00Z | 2025-11-01T00:00:00Z | 2025-11-30T23:00:00Z | 30 |
| 2 | 2025-10-25T00:00:00Z | 2025-11-23T23:00:00Z | 2025-12-01T00:00:00Z | 2025-12-31T23:00:00Z | 31 |

## Coverage audit

`research_state/coverage_audit_fwd_vol_2025_disjoint_cross_20261114T183000Z.json`

- 5 symbols, 3 blocks, 3600 test rows per block
- train rows: 2760 / 3432 / 3552
- all coverage checks pass
- no outcomes computed

## Gates

- Materiality: >= 2% relative QLIKE reduction
- 95% day-block bootstrap CI excludes zero on the improving side
- Holm across 4 horizons x 3 contrasts x 3 blocks
- LOIO >= 4/5
- Funding-permutation placebo PASS
- >= 5 instruments, >= 3 blocks
- Leakage audit PASS
- 7-day embargo between train end and test start

## Verdict space

- `EXPLORATORY_SIGNAL` — all gates pass, but `promotable=false`
- `EXPLORATORY_NULL` — materiality or CI fails with admissible data
- `INCONCLUSIVE` — data/leakage admissibility fails
- `SMOKE` — smoke run only; not evidence

No `CONFIRMED` or `PROMOTED` verdict is permitted while Gate 4 Binance v5 terms evidence is unresolved.

## Forbidden

- Mutating sealed artifacts
- Threshold shopping or feature changes after outcome inspection
- Reusing an inspected window as fresh confirmation
- Committing raw cache
- Editing `.github/workflows/*`
- Claiming confirmatory or promoted status for H1
- Treating the unresolved Binance v5 terms blocker as resolved

## Gate 4 status

- State: `EXTERNAL_BLOCKED`
- Evidence: `research_state/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json`
- Resolved trigger glob: `research_state/fclr016_v5_terms_evidence_RESOLVED_*.json`
- Resolved trigger found: false
- `promotable=false`