# Evaluation Summary — FCLR-011-INDEPENDENT-RECOMPUTE-20261114T042139Z

Generated: 20261115T234700Z
Campaign: `FCLR-FUND-VOL-LIQ-REDTEAM-20261114T042139Z`
Prereg: `research_state/prereg_fclr011_recompute_20261114T042139Z.json` (status FROZEN_PRE_OUTCOMES, frozen before outcomes)

## Verdict: **INADMISSIBLE** (INADMISSIBLE)

- Promotable: `False` (audit only, never promotable)
- Sealed FCLR-011 artifacts: unchanged (read-only in this cell)
- Smoke run: `True`

## Panel

- Panel: `research_state/fclr011_recompute_panel_20261115T234700Z.parquet`
- Panel SHA-256: `41962f823e59de5989c7d854cb3180cad61a4cbc2f5f230133c41b321342c1f4`
- Rows: 7320
- Instruments: 5 ['BNBUSDT', 'BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'XRPUSDT']
- Test blocks (UTC days): 53
- Test window: ['2026-05-08T00:00:00Z', '2026-08-06T23:00:00Z']

## Coverage (test rows)

- test_rows_total: 6360
- test_rows_core_complete: 6355
- core_coverage: 0.999214

## Paired contrasts (QLIKE, lower is better)

_No contrasts computed._

## Robustness

- LOIO: None/None instruments clear the 2% materiality floor
- Placebo (funding permutation, n=None): null p95 None%, p≈None, pass=None

## Per-symbol (C2 vs B1)

| Symbol | n | B1 QLIKE | C2 QLIKE | rel reduction |
|---|---|---|---|---|

## Per-block (C2 vs B1)

| Block (UTC day) | n | rel reduction |
|---|---|---|

## Leakage audit


## Failing minima

- no complete training rows

## Comparison to the sealed FCLR-011 result

| Contrast | Sealed rel reduction | Recomputed rel reduction |
|---|---|---|
| C2_vs_B1 | 4.94% | n/a |
| C1_vs_B1 | 1.36% | n/a |
| C2_vs_C1 | 3.63% | n/a |

## Notes

- Mark/index premium is NOT computable from the cached 2026 Binance archive (no markPriceKlines/indexPriceKlines/premiumIndexKlines); C2 degrades to C1 + mark/EMA24 distance. This is a limitation of the independent recompute, not a claim about the sealed result.
- No zero-fill, no forward-fill. Funding attached by backward merge_asof (<= 24h tolerance). Target is a strictly forward 24h realized variance.
