# Coverage Audit — Independent Re-verification (2026-10-26T20:45Z)

Scope: mark-price (`markPriceKlines` 1h) coverage for the 5-instrument universe
BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT over the FCLR-001 window
2024-01-01..2024-03-31.

## Method

For each symbol, globbed every `*-1h-*.csv` file in the working tree (excluding
`.git`), kept only `markPriceKlines` files, parsed `open_time` from each row, and
counted timestamps falling inside 2024-01-01T00:00:00Z..2024-03-31T23:59:00Z.
Then computed the set intersection across all five symbols.

## Result

| Symbol     | mark-price timestamps Jan–Mar |
|------------|-------------------------------|
| BTCUSDT    | 2160                          |
| ETHUSDT    | 0                             |
| BNBUSDT    | 0                             |
| SOLUSDT    | 0                             |
| XRPUSDT    | 0                             |

**True intersection across all 5 symbols: 0 timestamps.**

## Discrepancy with run_manifest.json

`research_state/run_manifest.json` -> `coverage_audit_multi` reports:

- `common_panel_timestamps`: **2136**
- `common_panel_first`: `2024-01-02T00:00:00Z`
- `common_panel_last`: `2024-03-30T23:00:00Z`
- `symbols`: `["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]`

This is **not reproducible** from the current working tree. Root cause: the other
four symbols have **no mark-price CSVs dated 2024-01..2024-03** anywhere in the
repository. Their mark-price cache begins at 2024-04-01 (91 files each,
2024-04-01..2024-06-30). The 2136 figure appears to have been computed from a
panel that no longer exists in this checkout, or from a different (BTCUSDT-only)
intersection. `coverage_audit.py` does compute an intersection
(`set.intersection(*mark_sets.values())`), so the recorded number cannot be
produced by that code against the present files.

## Consequence for FCLR-001

The protocol requires a paired out-of-sample panel with **>=5 instruments**.
`scripts/run_evaluation.py` builds that panel by intersecting mark-price
timestamps across `SYMBOLS`. With four symbols having zero mark-price rows in
Jan–Mar, the intersection is empty, so the actual evaluated panel is
**BTCUSDT only** — confirmed by `scripts/_diag_panel.py`:

- FCLR-001: total eval rows 1634; per symbol `BTCUSDT: 1634`, others 0.
- FCLR-002: total eval rows 1658; per symbol `BTCUSDT: 1658`, others 0.

The reported n=70 (FCLR-001) and n=94 (FCLR-002) test rows are single-instrument
BTCUSDT forecasts. This is a **coverage/representativeness defect**, not a
leakage defect: it means the ">=5 instruments" gate was never met and the
cross-instrument block-bootstrap uncertainty is not measuring what the protocol
intended.

## What is still true

- Funding-rate CSVs for all five symbols do cover Jan–Mar (2024-01, 02, 03).
- BTCUSDT mark-price coverage is complete Jan–Jun 2024 (627 files).
- The four other symbols' mark-price coverage is complete **only from
  2024-04-01**. A 5-instrument panel is possible for any window starting
  2024-04-01, but **not** for the frozen FCLR-001 window.
- No holdout leakage, no look-ahead, no split/protocol changes were introduced
  by this audit. It is a documentation/discovery finding.

## Status

- FCLR-001 ">=5 instruments" coverage gate: **NOT MET** (1 of 5 instruments
  actually present in the evaluated panel).
- This does not change the INCONCLUSIVE verdict, but it is a more serious
  shortfall than previously recorded: the result is not only underpowered
  (single ~4-day block) but also single-instrument.