# Evidence audit — 2026-11-19T03:37:00Z

Campaign: `FCLR-LIQ-TRACKA-EXTENSION-01-20261119T015256Z`
Session: `session_20261119T033443Z`

## Honest status

**COMPLETE.** Track A 12-month extension is ADMISSIBLE over `2025-11 .. 2026-10`
(13 coins, 113,880 coin-hours, alignment yield 1.000, max coin-month gap 0.0,
g1..g7 PASS). The descriptive layer is produced from the frozen panel. All
mandatory carry-forward packages were copied verbatim. The confirmatory design
is registered but **was not evaluated**.

## Evidence added

- `fclr_tracka_extension01_descriptive_20261119T033443Z.{py,json,md}` —
  per-coin event totals/notional/share, top-10 liquidation hours, weekday and
  hour-of-day profiles, and within-coin funding / trailing-24h RV decile
  incidence tables with counts and Wilson 95% CIs.
- `evidence_audit_20261119T033443Z.{json,md}`
- `trigger_check_20261119T033443Z.json`
- Verbatim carry-forward: RISK-07 package + stdlib recalibration recompute,
  RISK-06 package, ROBUST-05 package, and the full Track A exploratory package
  from `session_20261118T201919Z`.

## Descriptive layer is not predictive evidence

The descriptive layer reports observed-label associations only. No model was
fit, no out-of-sample forecast was evaluated, and no predictive, causal, or
lead-lag claim is made. A zero `liq_count` hour is an hour with no observed
event in the feed; it is not proof that no liquidation occurred.

## Prohibitions respected

- No sealed Binance month was read for outcomes.
- No confirmatory evaluation was run in this campaign.
- RISK-05/06/07, ROBUST-05, and Track C QLIKE were not re-run.
- No workflow file was written.
- No heavyweight statistics package was installed.
- `pandas`/`pyarrow` were not used in this session; the descriptive layer is
  stdlib only and reads the frozen CSV panel.
- No frozen session artifact was edited; carry-forward was copy-only.
- No zero-byte artifact was written.

## Network and cache

`network_used = false`. The Ironflow/Hyperliquid bulk cache for
`2025-11 .. 2026-10` is local and hash-verified (48/48 objects OK).

## Next action

Execute `FCLR-LIQ-TRACKA-CONFIRMATORY-01-<UTC>`: a power/MDE audit first, then
the registered three-block confirmatory forecast evaluation with placebo null
and Holm correction — or an honest `UNDERPOWERED` verdict.
