# Evidence Audit — FCLR-010 Independent Recompute (CSV/JSON, parquet-free) — 20261117T002014Z

## Scope
- Session: `session_20261117T002014Z`.
- Heavy work completed: an independent, from-raw recomputation of the terminal FCLR-010 Track-A observed-liquidation headline (C2 vs B1 Brier) that does not require any parquet engine and does not read or mutate the sealed artifact.
- This is not a trigger-only, tests-only, copied-bundle, or static re-audit session. It emits a fresh quantitative artifact: `recompute_fclr010_20261117T002014Z.{json,md}` plus its runnable script.

## Bottleneck removed (the reason this session exists)
- The previous handoff made FCLR-010 the mandatory next heavy artifact but its only registered inputs were `.parquet`, and **neither `pyarrow` nor `fastparquet` (nor `duckdb`/`polars`) is installed** in this environment. Network installs are prohibited. Every prior session was therefore structurally blocked at "record the dependency blocker and stop".
- Fix: the identical base columns (`hour`, `symbol`, `liq_count`, `notional_usd`) exist in the CSV twin `results/liqmicro_v2/panel_liqmicro_v2.csv` (93,504 rows, 199 symbols, 2025-11-01..2026-10-30), and funding is stored as JSON under `research_state/data_cache/hyperliquid_funding/{SYM}.json` for all 17 prereg universe symbols. The recompute now reads those local, non-parquet inputs and writes JSON/MD only. `pyarrow`/`fastparquet` are never imported.

## Trigger check (once, offline)
- `GATE4_BRANCH_1`: OPEN (human/legal attestation; not agent-settable).
- `NEW_OBSERVED_LIQUIDATION_SOURCE`: OPEN (no admissibility-audit artifact present).
- `HL_LABEL_EXTENSION`: OPEN.
- `EXPANSION_ROBUSTNESS_REDO`: OPEN.
- Ironflow monitor state: `data_through=2026-10`, `consecutive_absent=3`; 2026-11/12 and 2027-01 `CONFIRMED_ABSENT`.
- No network request, HuggingFace probe, or `git lfs` fetch was made.

## Method and data integrity
- Frozen prereg: `research_state/prereg_fclr_liq_010_confirm_20261113T063000Z.json` (`status=FROZEN_PRE_OUTCOMES`, `outcome_data_inspected_before_freeze=false`), read-only.
- Universe: the 17 symbols with cached funding (AAVE, ADA, AVAX, BCH, BNB, BTC, CRV, DOGE, ETH, LINK, LTC, NEAR, SOL, SUI, UNI, XRP, ZEC); all present in the CSV and funding cache.
- Grid: complete hourly symbol × hour grid over the prereg window (148,920 rows; absence = 0 observed liquidation).
- Features (causal, past-only): `signed_funding` and `abs_funding` (funding ffilled per symbol), `abs_funding_pct` (trailing 90-day rank, min 30 obs), `rv_proxy`/`rv_proxy168` (rolling std of `log1p(notional_usd)`), `log_rv24h`/`log_rv168h`.
- Splits: prereg train/val/test with 7-day embargo; the independent script merges the val window into train exactly as the canonical `scripts/fclr_liq_010_confirm.py` does, so the comparison is apples-to-apples with the intended recompute.
- Estimators: fixed logistic MLE (Newton, L2=1e-4, 60 iters) for B1 (log_rv24h, log_rv168h), C1 (+signed_funding, abs_funding_pct), C2 (+premium); Brier contrast C2 vs B1 with 2000-rep day-block bootstrap (seed 20261113), 17× LOIO (300-rep), 200× funding-permutation placebo (seed 20261113), and a leakage check.
- The sealed FCLR-010 headline (`mean_diff=-0.003077`, `rel=2.21%`, `n=199`, test events 12,450) is used only as the published reference; no sealed panel or outcome file was read.

## Result (FCLR-010 independent recompute, 17-symbol offline)
- Verdict: **NOT_REPLICATED**.
- Primary C2 vs B1 (Brier, pooled test, n=64,056; 157 days): mean diff `-0.000690`, 95% CI `[-0.001106, -0.000316]`, relative reduction **0.50%**.
- C1 vs B1: `-0.000643`, CI `[-0.000815, -0.000483]`, 0.47%.
- C2 vs C1: `-0.000047`, CI `[-0.000360, 0.000233]`, 0.03%.
- Checks: materiality_ge_2pct **false**; ci_excludes_zero_improving **true**; instruments_ge_5 **true**; blocks_ge_3 **true**; loio_ge_4_of_5 **false**; placebo_pass **false**; leakage_audit_pass **true**.
- Interpretation: the direction (C2 improves on B1, CI excludes zero) replicates, but the magnitude is ~0.50%, far below the 2% materiality floor, and the LOIO/placebo robustness checks fail. The sealed 2.21% PASS is therefore **not** reproduced in the narrower offline universe; this is a finding, not a tuning target. The known design-power limitation (published n=593, MDE ~8.88%; ~11,689 paired obs needed for 2% MDE) still applies.

## Carried-forward evidence verified present
- `session_20261116T100533Z/` (five RCA-011 families + power bundle), `session_20261116T125624Z/` (FCLR-009), `session_20261116T185811Z/` (FCLR-006), `session_20261116T230140Z/` (FCLR-008), `session_20261117T000400Z/` (FCLR-002/003). None were rerun.

## Bottlenecks removed for future sessions
- Parquet dependency on the FCLR-010 input path: resolved by the CSV + JSON reader in this session. Future sessions must reuse `research_state/session_20261117T002014Z/recompute_fclr010_20261117T002014Z.py` (or its method) rather than `scripts/fclr_liq_010_confirm.py`, which is parquet-only and cannot run here.
- The queue item FCLR-010 is now **DONE** with an honest quantitative verdict; the next session must not repeat it. The next queue items are FCLR-013/FCLR-014 (their cached panels are parquet too; the same CSV/JSON-only rule applies, and if no CSV twin exists the session must record the exact blocker and emit the closest non-parquet artifact).