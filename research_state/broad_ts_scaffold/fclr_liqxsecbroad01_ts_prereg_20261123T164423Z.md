# FCLR-LIQ-XSEC-BROAD-TS-01 — Temporal Stability Preregistration (FROZEN_PRE_OUTCOMES)

**Experiment ID:** FCLR-LIQ-XSEC-BROAD-TS-01
**Campaign:** FCLR-LIQ-XSEC-BROAD-TS-01-20261123T135825Z
**Session UTC:** 20261123T164423Z
**Status:** FROZEN_PRE_OUTCOMES
**frozen_before_outcomes:** true
**outcome_data_inspected_before_freeze:** false

## Question

Is the SUPPORTED broad-universe cross-sectional funding → next-hour observed liquidation-intensity association (BROAD-01, session_20261123T085507Z, SUPPORTED_GENERALIZATION) temporally stable — i.e. not dominated by one time block — per RESEARCH_PROMPT.md §17 promotion condition #4?

BROAD-01 reported only the *mean* per-block rank-IC (long arm 0.155133, CI95 [0.142081, 0.168895], short arm -0.002054). It never tested whether that association survives across ordered test blocks. This campaign reuses BROAD-01's 30 non-overlapping 168h test blocks and frozen sign convention, freezes an outcome-blind stability battery, then evaluates.

This is a stability test of a cross-sectional association, NOT a time-series forecast gate pass and NOT an observed-liquidation census (capped-sample feed).

## Frozen inputs (do NOT re-derive, do NOT substitute)

- `research_state/data_cache/ironflow_bulk/{liquidations,funding,open_interest,candles_1h}/` — 18 monthly parquet, 2025-05..2026-10. Liquidations: 2,849,452 rows, 342 coins (2025-05); instrument key is `market` — there is NO `coin` column in liquidations (coin derived via `coin_from_market()`). Each parquet has `.sha256` and `.accessed.json` sidecars — assert sha256 before reading; caches read-only.
- Block boundaries and sign convention from BROAD-01 (`session_20261123T085507Z/`): `TRAIN_FRAC=0.60`, `PURGE_EMBARGO_H=48`, `BLOCK_H=168`, `HORIZON_H=1`, `N_BOOT=2000`, `N_PERM=1000`, `N_LOIO=8`, `LOIO_PASS_THRESHOLD=6`, `SEED=20261123`, `ALPHA_K=0.05/(2*3)`, `MATERIALITY_PCT=2.0`.
- Sign convention: `relative_improvement = (baseline - candidate) / baseline`, positive = candidate better. Identical to BROAD-01.

## Stability battery (outcome-blind, pre-registered before any stability metric computed)

1. Fraction of blocks with positive rank-IC (long arm) and fraction with the BROAD-01 sign.
2. Rolling-window rank-IC (6-block rolling mean): min/median/max and 95% interval.
3. Monotone trend test across ordered blocks: Spearman/Kendall of block-index vs rank-IC, two-sided, frozen alpha_k = 0.05/6.
4. First-half vs second-half mean rank-IC gap with block-bootstrap CI95 (resample complete UTC test blocks jointly across coins).
5. Leave-one-block-out range of mean rank-IC (long arm).
6. Per-regime sign stability: RV-tercile and UTC-session bucket.

Primary arm: LONG arm (SUPPORTED in BROAD-01). Short arm reported descriptively only (null in BROAD-01); it must not drive the verdict.

## Uncertainty

Per-coin block bootstrap ≥2,000 deterministic-seed replicates (resample complete UTC time blocks jointly across coins), percentile CI95.

## Multiplicity

Holm across the declared stability family (6-arm family), report raw and adjusted p-values.

## Symmetric verdict rule (declared BEFORE outcomes)

**STABLE** iff, on the long arm:
1. Sign reproduced in ≥ 0.80 of blocks (≥ 24 of 30 blocks positive rank-IC);
2. First-half vs second-half mean rank-IC gap bootstrap CI95 excludes a sign reversal;
3. Ordered-block monotone trend test does not reject stationarity at frozen two-sided alpha_k.

**NOT_STABLE** otherwise (a genuine, durable finding: the SUPPORTED association is time-block dominated and fails §17 condition #4).

Preserve the null honestly; never relax a threshold after outcomes; never relabel. The materiality floor (2%) was already NOT met in BROAD-01; this campaign tests rank-ordering stability, NOT a time-series forecast gate, and must not be relabeled as one.

## Required artifacts (all under `research_state/session_20261123T164423Z/`, no zero-byte placeholders)

- `fclr_liqxsecbroad01_ts_prereg_20261123T164423Z.json` + `.md` (this freeze)
- `fclr_liqxsecbroad01_ts_eval_20261123T164423Z.py` + `.json` + `.md` — heavy rolling-window stability evaluation including per-block rank-IC series with block start hours
- `fclr_liqxsecbroad01_ts_recompute_20261123T164423Z.py` + `.json` — independent stdlib recompute asserting `all_checks_match:true`
- `fclr_liqxsecbroad01_ts_evidence_audit_20261123T164423Z.json` + `.md` — honest evidence audit
- `evidence_audit_20261123T164423Z.json` — gate-critical alias (non-empty)
- `trigger_check_20261123T164423Z.json` — non-empty (records no external trigger required)
