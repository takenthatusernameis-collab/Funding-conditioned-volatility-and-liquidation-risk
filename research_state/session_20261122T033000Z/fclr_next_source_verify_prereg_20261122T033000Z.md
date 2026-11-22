# FCLR-NEXT-SOURCE-VERIFY-01 Prereg (Outcome-Blind)

**Campaign:** `FCLR-NEXT-SOURCE-VERIFY-01-20261122T013100Z`
**Session:** `20261122T033000Z` (> campaign start `20261122T013100Z`)
**Generated:** `2026-11-22T03:30:00Z`

## Design
**ID:** `FCLR-NEXT-CONFIRM-001`
**Type:** confirmatory
**Prereg status:** OUTCOME_BLIND — hypotheses, analysis plan, block definition, and decision rules are specified here before any results are computed. The eval script computes results against this pre-specified plan; no post-hoc changes.

## Rationale
No materially-different free external source with live/unfrozen coverage passed the source registry sweep (`NO_NEW_ADMISSIBLE_SOURCE`). Per AGENT_HANDOFF.md section 1 item 3, idling is forbidden; a new confirmatory design is registered on the admissible local data domain (`research_state/data/raw/` BTC/ETH hourly klines + fundingRate, Jan-Mar 2024).

## Data domain
`research_state/data/raw/` — local raw CSVs, no network, stdlib-readable.

Symbols: `BTCUSDT`, `ETHUSDT`
Window: `2024-01-01T00:00:00Z .. 2024-03-31T23:00:00Z` (hourly)

Files:
- `BTCUSDT-1h-2024-01-01.csv`
- `BTCUSDT-1h-2024-01-02.csv`
- `ETHUSDT-1h-2024-01-02.csv`
- `BTCUSDT-fundingRate-2024-01.csv`
- `ETHUSDT-fundingRate-2024-01.csv`
- supplemental `btc/` and `btc_funding/` subdirs under `research_state/data/raw/` (incomplete coverage for full window)

## Sample minima note
Local domain does NOT meet the >=5 symbols / >=1 complete month / >=3 non-overlapping 30-day blocks minima. Results where minima are not met are reported as `NOT_SUPPORTED` or `INCONCLUSIVE`, never fabricated as `GO`.

## Hypotheses (outcome-blind)

**H1** — Elevated funding rate (absolute value) is associated with elevated subsequent realized volatility (1h absolute log-return), consistent with funding-conditioned volatility.
- Direction: positive association between \|funding_t\| and \|log return_{t+1}\|
- Test: Spearman rank correlation between \|funding_t\| and \|logreturn_{t+1}\| within each symbol-block; per-block p < 0.05 required; combined via Fisher across admissible blocks.

**H2** — Hours with funding rate of opposite sign to prior return (mean-reversion pressure) show reduced subsequent volatility vs same-sign funding hours.
- Direction: opposite-sign funding -> lower subsequent \|log return\|
- Test: Compare mean subsequent \|log return\| for opposite-sign vs same-sign funding hours within each admissible block; two-sample t-test per block, p < 0.05.

**H3** — No proxy for liquidation risk is computable from the local domain (no liquidation labels); any liquidation-conditioned claim is NOT_SUPPORTED by design.
- Direction: null (not computable)
- Test: Absence check: no liquidationSnapshot/liquidation column present in any local CSV.

## Analysis plan

Block definition: non-overlapping 30-day blocks aligned to calendar month boundaries where data permits; blocks must each contain >=5 symbols OR be single-symbol but with full-month coverage.

| Block | Start | End | Symbols |
|---|---|---|---|
| B1_2024-01 | 2024-01-01T00:00:00Z | 2024-01-31T23:59:59Z | BTCUSDT, ETHUSDT |
| B2_2024-02 | 2024-02-01T00:00:00Z | 2024-02-29T23:59:59Z | BTCUSDT, ETHUSDT |
| B3_2024-03 | 2024-03-01T00:00:00Z | 2024-03-31T23:59:59Z | BTCUSDT, ETHUSDT |

Block minima: each block requires >=5 symbols OR >=1 complete month with documented completeness. Local domain: 2 symbols, partial hourly coverage -> blocks likely INCONCLUSIVE/NOT_SUPPORTED.

Features:
- `log_return_t = log(close_t / close_{t-1})` per symbol per hour
- `abs_log_return_t1 = |log_return_{t+1}|` (subsequent 1h realized volatility)
- `funding_t` = funding rate at hour t (nearest prior funding timestamp <= t)
- `abs_funding_t = |funding_t|`
- `sign_funding_t = sign(funding_t)`, `sign_return_t = sign(log_return_t)`
- `opposite_sign = sign_funding_t != sign_return_t AND sign_return_t != 0`

Tests:
- `spearman_abs_funding_vs_subsequent_vol` — all admissible blocks, alpha 0.05, combine via Fisher
- `ttest_opposite_vs_same_sign_subsequent_vol` — all admissible blocks, alpha 0.05
- `liquidation_absence_check` — all blocks

Decision rules:
- `GO`: >=1 admissible block passes H1 at alpha 0.05 AND H2 direction consistent AND H3 absence confirmed
- `NOT_SUPPORTED`: no admissible block meets minima OR liquidation labels absent (H3) AND no external source available
- `INCONCLUSIVE`: admissible blocks exist but sample too small for powered test

Null handling: `NOT_SUPPORTED` and `INCONCLUSIVE` are preserved as legitimate outcomes; never coerced to `GO`.

## Recompute independence
Independent recompute script (`fclr_next_source_verify01_recompute_20261122T033000Z.py`) recomputes all statistics from raw CSVs using a separate code path; results compared for numerical agreement.

## Evidence requirements
eval json+md, recompute json, evidence audit json+md, trigger_check json, sha256 of all input CSVs.

## Artifacts
- `fclr_next_source_verify01_source_registry_20261122T033000Z.{json,md}`
- `fclr_next_source_verify01_prereg_20261122T033000Z.{json,md}`
- `fclr_next_source_verify01_eval_20261122T033000Z.{py,json,md}`
- `fclr_next_source_verify01_recompute_20261122T033000Z.{py,json}`
- `fclr_next_source_verify01_evidence_audit_20261122T033000Z.{json,md}`
- `evidence_audit_20261122T033000Z.json`
- `trigger_check_20261122T033000Z.json`

## Compliance
- Read-only artifacts: true
- Network used: false
