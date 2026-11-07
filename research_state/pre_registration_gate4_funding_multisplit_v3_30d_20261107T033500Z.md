# Pre-Registration: Gate 4 Funding Multi-Split v3 (30-day non-overlapping test blocks)

**Experiment ID:** GATE4-FUND-VOL-ABLATIONS-MSPLIT-V3-30D
**Version:** v3 (claim-worthy data-sufficiency target: 30-day non-overlapping blocks)
**Status:** FROZEN BEFORE OUTCOMES — 2026-11-07T03:35:00Z
**Authoring context:** Local admissible data only; no credentials, no paid data, no auth bypass, no manual downloads, no network in run.
**Supersedes for claim-worthiness only:** v1/v2 remain preserved as pilot/inconclusive; v3 is a separate versioned run and does not overwrite v1/v2 outputs.

## Objective
Test whether funding features improve 24h forward realized-variance forecasts (QLIKE primary) beyond a direct-variance RV-only baseline using **>=3 non-overlapping 30-day test blocks** with train/purge/embargo, on locally available admissible data. Exploratory/pilot framing if any pre-registered sufficiency criterion fails; **no confirmatory claim** unless all claim-worthy criteria are met and results are stable.

## Data (local, admissible, verified present)
- **Instruments (5):** BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT, BNBUSDT (USDT-margined perpetual symbols; Binance public-archive layout files already present locally).
- **Klines:** 1h contract klines, daily zip/CSV files present under `research_state/data_cache/<SYM>_2024_MM/klines-2024-MM-DD/<SYM>-1h-2024-MM-DD.(zip|csv)` for 2024-04-01..2024-09-30 (183 common days where all 5 symbols have aligned 1h files; verified by local audit 2026-11-07T03:35Z).
- **Funding:** monthly fundingRate files present under `research_state/data_cache/<SYM>_2024_MM/*fundingRate*2024-MM*` for 2024-04..2024-09 (all 5 symbols; verified).
- **Missing handling:** missing/unaligned observations remain NaN; never zero-filled. Basis/premium omitted (no aligned admissible local series verified for this panel); NaN-omitted.
- **Provenance:** local files only; Binance public-data archive naming/schema; no network fetch in v3 run. Loader may extract local zips to a deterministic local extract directory (idempotent) as processing, not acquisition.

## Horizon / Target
- 24h forward realized variance target (same construction as v1/v2/Gate 3 RV family), computed from 1h close-to-close returns; no lookahead.

## Splits (frozen, chronological, non-overlapping 30-day tests)
All timestamps UTC. Purge/embargo >= 7 calendar days between train end and test start. Expanding train anchored at 2024-04-01.

| id | train_start | train_end | purge_gap_days | test_start | test_end | test_days |
|---:|---|---|---:|---|---|---:|
| 0 | 2024-04-01 | 2024-05-07 | 7 | 2024-05-15 | 2024-06-13 | 30 |
| 1 | 2024-04-01 | 2024-06-06 | 7 | 2024-06-14 | 2024-07-13 | 30 |
| 2 | 2024-04-01 | 2024-07-06 | 7 | 2024-07-14 | 2024-08-12 | 30 |
| 3 | 2024-04-01 | 2024-08-05 | 7 | 2024-08-13 | 2024-09-11 | 30 |

No tuning on test. Any implementation bug invalidating chronology/leakage invalidates affected results.

## Ablations (pre-registered; same family as v1/v2)
- **A_rv_only (baseline):** direct-variance OLS HAR on trailing RV features (rv_trail_24, rv_trail_168, rv_trail_6) — regression-stable form.
- **B_rv_signed:** A + funding_signed (last known at/before hour).
- **C_rv_abs:** A + funding_abs.
- **D_rv_signed_abs:** A + funding_signed + funding_abs.
- **E_rv_signed_abs_roll:** A + funding_signed + funding_abs + rolling funding stats (past-only/trailing; train-safe computation).

## Primary metric / contrasts
- **Primary metric:** QLIKE (lower is better), on jointly valid observations.
- **Primary contrast:** E vs A (pre-registered). Secondary contrasts B/C/D vs A reported but not claim-bearing unless pre-specified as confirmatory (they are not).
- **Uncertainty:** block bootstrap ΔQLIKE (alt-base) CIs, resampling whole UTC time blocks jointly across instruments; 24h block primary (seed/reps recorded in manifest). Report point, CI, n_obs, n_blocks.

## Leakage controls
- Chronological splits only; purge/embargo >= 7d.
- Train-only normalization/statistics per split.
- Funding merge uses last-known value at/before hour (`merge_asof` backward semantics via feature builder); no future funding.
- Targets are forward-looking but constructed without using test labels in training; evaluation compares predictions to realized targets only in designated windows.
- No random splits, no test tuning.

## Sufficiency / verdict rules (frozen)
Claim-worthy requires ALL: `>=5 instruments` (met by design if all 5 load), `>=3 non-overlapping 30-day test blocks` (met by design if all 4 run), leakage audit clean, and stable/evaluable contrasts with pre-registered uncertainty. If any split fails to load/evaluate, instrument coverage collapses materially, or CIs/evidence are unstable/inconclusive, verdict = **PILOT/INCONCLUSIVE** (not confirmatory). v3 does not claim economic value, overlay benefit, or Track A linkage.

## Outputs (versioned; v1/v2 preserved)
- `research_state/evaluation_summary_funding_v3_30d.md`
- `research_state/run_manifest_funding_v3_30d.json`
- `research_state/evaluation_summary.md` may receive a clearly labeled v3 section only if additive/non-destructive.
- `research_state/leakage_audit.md` updated additively with v3 traceability.

## Deviations
Any deviation from splits, instruments, data roots, ablations, metric, or leakage controls must be recorded in the manifest and treated as non-confirmatory.
