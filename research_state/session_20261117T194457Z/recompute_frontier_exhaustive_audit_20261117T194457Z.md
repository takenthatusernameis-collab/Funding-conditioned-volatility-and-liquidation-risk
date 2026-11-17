# Independent Exhaustive Frontier Audit — FCLR-FRONTIER-VERIFY-07 (20261117T194457Z)

- **Generated UTC:** 2026-11-17T19:45:00Z (artifact run 2026-11-17T19:52Z)
- **Campaign:** FCLR-FRONTIER-VERIFY-07-20261117T194457Z
- **Track priority:** Track C funding-conditioned volatility
- **Repository:** Funding-conditioned-volatility-and-liquidation-risk
- **Overall verdict:** `BLOCKED_ON_DESIGN`
- **Promotable:** `False`
- **FCLR-014 closed verdict reproduced:** `True`
- **Frontier verification mismatch:** `False` (`all_exact_match=true`)

## Method (deliberately independent of 193323Z)
- Stdlib-only, ZIP/CSV-aware structural reconstruction of `research_state/data_cache/`
  for `BTCUSDT`, `ETHUSDT`, `BNBUSDT`, `SOLUSDT`, `XRPUSDT`.
- Month completeness = per-symbol distinct observed UTC day coverage >= 90% of the
  month, for mark (`markPriceKlines-*`, `klines-*` fallback), index
  (`indexPriceKlines-*`) and premium (`premiumIndexKlines-*`), plus a present
  `BTCUSDT-style fundingRate-<month>` member. Day discovery reads member names only.
- Block feasibility uses month-interval arithmetic (`[train_start, test_end]`,
  30d train + 7d embargo + 30d test), not the 193323Z CSV-count heuristic.
- Mutual non-overlap is recomputed from interval intersection over `[train_start,
  test_end]`; all subsets of individually feasible test months are enumerated.
- Tested months are excluded using `TESTED_WINDOWS` parsed from
  `scripts/next_campaign_status.py` source (exclusion only; no import for the
  computation). The canonical tool was run only afterwards, as a comparison target.
- No network, no polling, no parquet, no outcome data inspected, no sealed
  artifact modified.

## Cache reconstruction
- 35 symbol-month directories inventoried (2024-01 .. 2026-11).
- Complete mark+funding months: 31 (2024-04 .. 2026-10).
- Complete full-C2 months (mark + index + premium + funding): 28.

## Full-C2 (mark + index + premium + funding)
- Individually feasible test blocks: **0**
- Max mutually non-overlapping: 0
- Overlapping pairs: 0
- Contiguous untested run >= 127d: **False** (longest 61d, 2024-04..2024-05)
- Campaign feasible: **False**

## Mark+funding-only (B0/B1/C1; no premium/index C2 terms)
- Individually feasible test months: **4** -> `2024-10`, `2024-11`, `2024-12`, `2025-01`
- Mutually non-overlapping selection: **2** -> `2024-10`, `2025-01`
- Overlapping pairs: **5** (2024-10/11, 2024-10/12, 2024-11/12, 2024-11/2025-01, 2024-12/2025-01)
- Contiguous untested run >= 127d: **False** (longest 123d, 2024-10..2025-01)
- Campaign feasible (>=3 non-overlapping): **False**

## Expected closed-world result (reproduced)
- Full-C2 0 disjoint feasible blocks / no contiguous run >=127d. OK
- Mark+funding-only 4 individually feasible / 2 mutually non-overlapping / 5 pairs /
  no >=127d run. OK
- Overall `BLOCKED_ON_DESIGN`, `promotable=false`,
  `fclr014_closed_verdict_reproduced=true`. OK

## Comparison (canonical tool + sealed certificates)
- `scripts/next_campaign_status.py --json` (`markfund_frontier`, `disjoint_block_frontier`,
  `design_feasibility`): all 9 compared fields `exact_match=true`.
- Sealed `session_20261117T072040Z/recompute_design_frontier_certificate_20261117T072040Z.json`:
  `matches_independent=true`.
- Sealed `session_20261117T193323Z/recompute_frontier_exhaustive_audit_20261117T193323Z.json`:
  `matches_independent=true`.

## Integrity
- No confirmatory estimand run or re-scored; no sealed artifact modified; no outcome
  data inspected; all four reopen triggers were `OPEN`, so no trigger-satisfied §16
  path was taken. Any future disagreement must be reported as
  `FRONTIER_VERIFICATION_MISMATCH`, not silently patched into the canonical tool.