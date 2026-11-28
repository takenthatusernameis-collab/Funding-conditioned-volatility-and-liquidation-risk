# FCLR-LIVE-ARCHIVE-08 Evidence Audit — session_20261128T040000Z

**Campaign:** FCLR-LIVE-ARCHIVE-08-20261127T131654Z (Track-B modeled boundary-breach forecast)
**Session:** session_20261128T040000Z
**Generated:** 2026-11-28T07:58:00Z
**Experiment ID:** FCLR-LIVE-ARCHIVE-08

## Status

PASS — audit_pass=true. Phase 3 independent stdlib recompute executed and reproduced the Phase 2 boundary-breach evaluation verdict (NOT_SUPPORTED).

## Verdict

**NOT_SUPPORTED** — C2 funding-conditioned model is worse than B1 mark-price-only baseline on all metrics:
- AUC: -5.36% relative (CI supports=False)
- Logloss: -0.38% relative (CI supports=False)
- Brier: -0.71% relative (floor 2.0% met=False; CI [-1.43%, +0.07%] supports improvement=False)

## Checks

- audit_pass: true
- verdict: NOT_SUPPORTED (reproduced from canonical eval)
- verdict_match: true
- all_checks_match: true
- recompute_all_checks_match: true
- unresolved_blockers: none

## Common support

- N=22584 timestamps
- Per-symbol: BNBUSDT=22608, BTCUSDT=22608, ETHUSDT=22608, SOLUSDT=22608, XRPUSDT=22584
- Split: train=13349, val=4450, test=4449 timestamps (test_rows_across_5_symbols=22245)
- n_test >= 500: true
- All five symbols in every block/fold: true

## Recompute

- Method: independent stdlib recompute — separate code path (csv.DictReader + os.walk + distinct feature/bootstrap/AUC paths)
- all_checks_match: true
- Recomputed metrics match canonical eval within tolerance (1e-4)

## Leakage controls

- Outcome-blind prereg frozen before any outcome computation
- Train-only model fitting and train-only standardization
- 168h purge/embargo between train/val/test
- No outcome inspection before design freeze
- Read-only cache reuse; no re-download; stdlib only; no network

## Bootstrap

- 2000 replicates, block=24, seed=20261126
- Leave-one-symbol-out: all 5 symbols tested, n_test=4449 each

## Not an overlay

Campaign-07 forecast gate did NOT pass, so per RESEARCH_PROMPT section 9 no risk overlay is authorized. Campaign-08 is forecast validation of a modeled boundary-breach target, which is permitted.
