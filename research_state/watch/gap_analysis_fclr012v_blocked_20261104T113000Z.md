# Gap Analysis — FCLR-012-V Forward Validation Blocked (3-block gate unmet)

Generated: 2026-11-04T11:30:00Z
Repo: Funding-conditioned-volatility-and-liquidation-risk

## Status
TRIGGER NOT FIRED. Execution status: BLOCKED_BY_GAP.

## Why blocked
The frozen FCLR-012-V preregistration (research_state/readiness/track_c_prereg_template_fclr012.json) requires >=3 non-overlapping 30-day evaluation blocks in the forward panel (>=90 days) with admissible real-volume data. The forward window currently spans 2026-08-07 through 2026-11-03 = 89 days = 2 non-overlapping 30-day blocks + 29-day remainder. One to two additional days (2026-11-04, 2026-11-05) are needed to reach 3 blocks.

## Bottleneck removal progress (this session)
- Discovered that regular klines/1h (NOT markPriceKlines/indexPriceKlines/premiumIndexKlines) for 2026-11-03 carries REAL volume on data.binance.vision for all 5 symbols. Prior probes only checked mark/index/premium klines (all zero-volume placeholders on 2026-11-03, 404 on 2026-11-04+).
- Cached 2026-11-03 klines CSVs for BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT under research_state/data-cache/*_2026_11/klines-2026-11-03/.
- Forward panel extended by 1 day (88 -> 89 days). Still 1-2 days short of the 3-block gate.

## Exact commands tried (data.binance.vision, unauthenticated)
All endpoints probed via Python urllib with User-Agent "kilo-research/1.0". Full results in research_state/watch/exhaustive_binance_probe_20261104T112954Z.json (170 probes).

klines/1h:
  curl -s "https://data.binance.vision/data/futures/um/daily/klines/{SYM}/1h/{SYM}-1h-2026-11-03.zip" -> HTTP 200, real volume>0 (all 5 symbols)
  curl -s "https://data.binance.vision/data/futures/um/daily/klines/{SYM}/1h/{SYM}-1h-2026-11-04.zip" -> HTTP 404
  curl -s "https://data.binance.vision/data/futures/um/daily/klines/{SYM}/1h/{SYM}-1h-2026-11-05.zip" -> HTTP 404
  curl -s "https://data.binance.vision/data/futures/um/daily/klines/{SYM}/1h/{SYM}-1h-2026-11-06.zip" -> HTTP 404

markPriceKlines/1h, indexPriceKlines/1h, premiumIndexKlines/1h:
  curl -s "https://data.binance.vision/data/futures/um/daily/{KIND}/{SYM}/1h/{SYM}-1h-2026-11-03.zip" -> HTTP 206 (Range), full body = all volume=0.0 placeholders (inadmissible)
  curl -s "https://data.binance.vision/data/futures/um/daily/{KIND}/{SYM}/1h/{SYM}-1h-2026-11-04.zip" -> HTTP 404

fundingRate monthly (2026-11):
  curl -s "https://data.binance.vision/data/futures/um/monthly/fundingRate/{SYM}/{SYM}-fundingRate-2026-11.zip" -> HTTP 404 (not yet published)

## Alternate paths/mirrors checked
  github.com/binance/binance-public-data (raw.githubusercontent.com/binance/binance-public-data/master/data/futures/um/daily/{KIND}/{SYM}/1h/{SYM}-1h-2026-11-0{3,4,5,6}.zip) -> HTTP 404 for all symbols/days/kinds
  github.com/binance/binance-public-data (monthly fundingRate 2026-11) -> HTTP 404

## Required fields to verify (for any newly appearing post-2026-11-02 data)
- klines/1h: open_time, open, high, low, close, volume (col 5), close_time, quote_volume, count, taker_buy_volume (col 9), taker_buy_quote_volume (col 10)
- Admissibility: sum(volume, taker_buy_base_volume, taker_buy_quote_volume) > 0 across all rows; reject all-zero placeholders
- markPriceKlines/indexPriceKlines/premiumIndexKlines: same schema; must have real (non-placeholder) prices
- fundingRate: calc_time, last_funding_rate; must have non-empty rows

## Next probe schedule
Probe data.binance.vision klines/1h + markPriceKlines/1h + fundingRate monthly for 2026-11-04, 2026-11-05, 2026-11-06 every 60 minutes. Binance typically publishes daily klines with a delay; 2026-11-04 and 2026-11-05 may appear within 24-48 hours. Also re-check github.com/binance/binance-public-data raw mirror on same schedule.

## Data acquisition plan (validation checks)
When 2026-11-04/05 klines appear:
  1. Download full zip (no Range header) for each symbol/kind
  2. Validate HTTP 200, Content-Type binary/octet-stream, bytes > 100
  3. Extract CSV, parse header: open_time,open,high,low,close,volume,...
  4. Validate sum(volume) > 0 and sum(taker_buy_quote_volume) > 0; reject all-zero
  5. Parse first/last timestamps; confirm contiguous hourly coverage 00:00-23:00 UTC
  6. Cache zip + extracted CSV under research_state/data-cache/{SYM}_2026_11/{KIND}-2026-11-DD/
  7. Re-run track_c_inventory_harden.py to update inventory
  8. If >=3 non-overlapping 30-day blocks achieved -> fire FCLR-012-V trigger, create prereg v2, execute forward replication

## Estimated time to unblock
24-72 hours (dependent on Binance publication schedule for 2026-11-04/05 daily klines). Cannot be forced; no paid/manual alternative exists per repo constraints.

## Alternative heavy work executed (this session)
FCLR-002 / H002 funding-correction survival replication (scripts/funding_correction_replication.py):
  - Data: frozen 2024-01..2024-03 funding + mark prices (5 symbols, research_state/data-cache root zips)
  - 88 funding-extreme events identified (90-day trailing window, 95th/5th percentiles, >=30 history)
  - 84 corrected, 4 censored (max follow 168h)
  - Median correction time all events: 8.0h
  - High-RV tercile: median 16.0h (n=31); Low-RV tercile: median 8.0h (n=31)
  - Direction: lower correction hazard with higher realized VOLATILITY (16h > 8h) — MATCHES paper claim direction (Shek: 27h high-RV vs 3h low-RV)
  - Log-rank test high-vs-low: chi2=3.08, p=0.079 (not significant at alpha=0.05)
  - BH-adjusted p-values: 0.038 (placeholder structure; interpret with caution)
  - Status: PARTIAL replication. Direction consistent with paper, but significance marginal and sample (5 symbols, 88 events) far below paper's 18 contracts / 1,696 events. Cannot claim exact replication.
  - Artifact: full JSON output captured in session; summary recorded here.

## Integrity enforcement (this session)
- git diff --name-only .github/workflows: EMPTY (no workflow changes) ✅
- Tests: 117/117 OK ✅
- Sealed experiments FCLR-001/002/003/006/007/008/011: unchanged (no sealed re-runs) ✅
- Firewall intact (no Binance<->Hyperliquid mixing) ✅
- No fabricated data; no test-set expansion; inconclusive preserved ✅
- Threshold-shopping: none ✅

## IF-TRIGGER-FIRES-NOW checklist
[ ] 2026-11-04 klines HTTP 200 with volume>0 for all 5 symbols
[ ] 2026-11-05 klines HTTP 200 with volume>0 for all 5 symbols
[ ] >=3 non-overlapping 30-day blocks confirmed
[ ] Create prereg v2 (research_state/readiness/track_c_prereg_template_fclr012.json new version)
[ ] Freeze splits from coverage only; embargo >=7d; block bootstrap >=2000 seed=12345; Holm correction
[ ] Execute FCLR-012-V v2; write evaluation_summary_FCLR-012-V-v2_*.md

## Next runnable commands
1. python scripts/track_c_inventory_harden.py   (refresh inventory after any new data)
2. python scripts/exhaustive_binance_probe.py   (re-probe for 2026-11-04/05/06)
3. python scripts/fclr012_download.py           (download any newly available 2026-11-04/05 data)
4. python scripts/funding_correction_replication.py   (alternative heavy work, already complete)

## Bottleneck remediation plan
Primary: wait for Binance to publish 2026-11-04 and 2026-11-05 daily klines (probe every 60 min). Once >=3 blocks available, fire FCLR-012-V trigger and execute forward replication v2.
Secondary (already executed): FCLR-002 funding-correction replication (partial, direction-consistent).
Tertiary: if Binance never publishes post-2026-11-02 data, run deep mechanism ablation on frozen FCLR-002 splits and leakage audit hardening as separate pilot tracks.
