# fclr_next_source_verify01_eval_20261122T033000Z

**Campaign:** `FCLR-NEXT-SOURCE-VERIFY-01-20261122T013100Z`
**Session:** `20261122T033000Z` (> campaign start `20261122T013100Z`)
**Generated:** `2026-11-22T03:30:00Z`

## Design
- Design ID: `FCLR-NEXT-CONFIRM-001` (confirmatory, outcome-blind prereg)
- Data domain: `research_state/data/raw/` BTC/ETH hourly klines + fundingRate, Jan-Mar 2024
- Stdlib-only; no network; no numpy/pandas/scipy

## Per-symbol summary
- BTCUSDT: kline_rows=72, funding_rows=186, assembled_rows=71
- ETHUSDT: kline_rows=24, funding_rows=93, assembled_rows=23

## Per-block results
### B1_2024-01 (2024-01-01T00:00:00+00:00 .. 2024-01-31T23:59:59.999000+00:00)
  - BTCUSDT: n_rows=48, status=-
    H1: rho=0.44116062505980447, p=4.999750012499375e-05, pass_alpha=True
    H2: diff_mean=-0.8698485175858975, p=0.10864456777161142, direction_consistent=None, n_opp=26, n_same=22
  - ETHUSDT: n_rows=23, status=-
    H1: rho=0.3745972071877342, p=0.07934603269836508, pass_alpha=False
    H2: diff_mean=-0.023310443052080188, p=0.7486125693715314, direction_consistent=None, n_opp=14, n_same=9

### B2_2024-02 (2024-02-01T00:00:00+00:00 .. 2024-02-29T23:59:59.999000+00:00)
  - BTCUSDT: n_rows=0, status=INCONCLUSIVE_TOO_FEW_ROWS
    H1: rho=None, p=None, pass_alpha=None
    H2: diff_mean=None, p=None, direction_consistent=None, n_opp=None, n_same=None
  - ETHUSDT: n_rows=0, status=INCONCLUSIVE_TOO_FEW_ROWS
    H1: rho=None, p=None, pass_alpha=None
    H2: diff_mean=None, p=None, direction_consistent=None, n_opp=None, n_same=None

### B3_2024-03 (2024-03-01T00:00:00+00:00 .. 2024-03-31T23:59:59.999000+00:00)
  - BTCUSDT: n_rows=23, status=-
    H1: rho=0.2247583243126405, p=0.3030848457577121, pass_alpha=False
    H2: diff_mean=-0.00020255243078201243, p=0.9028048597570122, direction_consistent=None, n_opp=10, n_same=13
  - ETHUSDT: n_rows=0, status=INCONCLUSIVE_TOO_FEW_ROWS
    H1: rho=None, p=None, pass_alpha=None
    H2: diff_mean=None, p=None, direction_consistent=None, n_opp=None, n_same=None

## Aggregate
- H1 Fisher chi2=27.262433751428706, p=0.00012929824544651456
- H1 any block pass alpha: True
- H2 direction consistent all blocks: True
- H3 liquidation absence confirmed: True
- Any admissible block: True

## H3 liquidation absence
- Confirmed: True
- Liquidation columns found: []

## Decision
- Decision: **GO**
- Reason: H1 passed in >=1 admissible block; H2 direction consistent; H3 absence confirmed.

## Compliance
- Outcome-blind: hypotheses/plan fixed in prereg before computation
- Nulls preserved: NOT_SUPPORTED/INCONCLUSIVE never coerced to GO
- Read-only artifacts; no root-level writes