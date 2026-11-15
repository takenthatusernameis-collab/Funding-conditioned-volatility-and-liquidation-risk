# Durable Agent Handoff — sole authoritative version (initial task refreshed 2026-11-15T06:03:41Z)

**SOLE DURABLE HANDOFF — START HERE.** `NEXT_SESSION_HANDOFF.md` is a tombstone; older `AGENT_HANDOFF` revisions and `research_state/FCLR_CAMPAIGN_NEXT.md` (self-superseded) are historical evidence only. This file is the only active handoff. Do not write status-only notes, do not re-probe exhausted families, and do not reopen sealed verdicts.

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION — `2026-11-15T06:03:41Z`

**Execute `FCLR-SHEK-SCALE-20261115T040843Z` now (default heavy path, not trigger-gated).** Do NOT stop for "no trigger" and do NOT chase exhausted vol/liq-forecast 3-block designs (`python3 scripts/next_campaign_status.py` correctly reports none feasible).

1. Baseline (record any material change): `git status` (HEAD `66f24902`, `main`, clean); `python3 scripts/fclr_campaign_gate.py` (19/19); `python3 scripts/fclr_fwd_vol_2025_disjoint_cross_gate.py` (PASS); `python3 scripts/check_tracka_scope_registry_drift.py` (184/184); `python3 -m unittest tests.test_active_campaign_gate tests.test_next_campaign_status tests.test_funding_correction_replication -v` (38/38); `python3 scripts/next_campaign_status.py` (no feasible 3-block design in ANY domain) — **all verified green 2026-11-15T06:03:41Z**.
2. **Freeze before outcomes:** write `research_state/prereg_fclr_shek_scale_<UTC>.json` (+`.md`) after a data-availability audit (Binance funding 2024-04..2026-10 excl. 2024-01..03; ironflow_bulk 200 coins × 12m 2025-05..2026-04; nested funding layout supported). Record exact eligible sample, exclusions, thresholds, Holm family, inference, sensitivity grid, stopping rules.
3. Heavy execution: extend registered `scripts/funding_correction_replication.py` with `--scale` (preferred; keeps scope drift 184/184) or add `scripts/fclr_shek_scale.py` + sync `research_state/tracka_script_scope_registry.json` and `tests/test_tracka_hardening_117.py`; add `tests/test_fclr_shek_scale.py` (fixture/deterministic/tmp-isolated/no network).
4. Deliver `research_state/evaluation_summary_FCLR-SHEK-SCALE-<UTC>.{json,md}` with event counts/censoring, KM medians, log-rank, cluster+block-bootstrap 95% CI, sensitivity grid, Holm p-values, explicit verdict (`REPLICATES_DIRECTION`/`NULL`/`UNDERPOWERED`/`INCONCLUSIVE`). Update `research_state/hypothesis_registry.json` `H2_shek_replication` (keep EXPLORATORY_ONLY/promotable=false). Advance frontier phases to `COMPLETED_VALIDATED` and install next heavy cell at rank 0.
5. Verify: campaign gate 19/19, scope drift OK (184/184 or synced 185/185 only if unavoidable new script), targeted + relevant suites green, `next_campaign_status.py` still honest. Commit only meaningful work. Never reopen sealed/terminal families, never mutate sealed artifacts, never edit `.github/workflows/*`, never use paid/credentialed/manual data.

**Bottlenecks:** none blocking — forecast-frontier phantom removed, nested funding cache load fixed, rank-0 `READY_EXECUTE/ACTIVE`, gates/tests/drift green. If blocked, record exact command/error + proof of a tried materially-different free route.


## Baseline verified this session (2026-11-15T06:03:41Z)

- Working tree clean at HEAD `66f24902e` (`main`).
- `python3 scripts/fclr_campaign_gate.py` → **19/19 PASS**.
- `python3 scripts/fclr_fwd_vol_2025_disjoint_cross_gate.py` → **GATE PASS**.
- `python3 scripts/check_tracka_scope_registry_drift.py` → **184/184 OK**.
- `python3 -m unittest tests.test_active_campaign_gate tests.test_next_campaign_status tests.test_funding_correction_replication -v` → **38/38 OK** (6.058s).
- `python3 scripts/next_campaign_status.py` → **no feasible 3-block design in ANY domain** (forecast frontier honestly exhausted).
- Cached-data coverage (verified, no network): Binance USDⓈ-M funding = **5 symbols × 31 months (2024-04..2026-10)** at the nested layout `research_state/data_cache/{SYM}_{YYYY_MM}/{SYM}-fundingRate-{YYYY-MM}/{SYM}-fundingRate-{YYYY-MM}.csv` (~90–93 obs/month at 8h cadence); mark/index/premium = 5 symbols × 35 months (2024-01..2026-11); ironflow bulk = **200 coins × 12 months (2025-05..2026-04)** for candles_1h / funding / open_interest / liquidations; ironflow_events = 18 months (2025-05..2026-10). Cache root `research_state/data_cache/` ≈ 733 MB.
- Prior results unchanged (do not rerun): vol FullHist `NOT_MET` (C2_vs_B1 rel QLIKE 1.19% < 2% floor; CI excludes 0; Holm-sig on t24) — statistically real, economically immaterial. Liq xsec forward `EXPLORATORY_NULL` (decidable at pooled n, null-asymmetric). `H1_primary = NOT_SUPPORTED` (terminal). `H2_shek_replication = EXPLORATORY_ONLY / PARTIAL` (88 events, Q1 2024 only; high-RV 16h vs low-RV 8h, log-rank p=0.0792 — direction matches the paper's 27h/3h claim but is underpowered).

## Scope correction — "exhausted" is narrower than the prior handoff implied

`python3 scripts/next_campaign_status.py` now reports **no feasible 3-block FORECAST design in any domain** — verified honest after this session's fix (see bottlenecks removed). That is correct *for the vol/liq forecasting estimand* (Binance contiguous + ironflow bulk + ironflow extended are all consumed by the FullHist + Forward + FCLR-011/011-confirm campaigns). It does **not** mean "no heavy work remains." The **Shek funding-extreme correction-time event study** is a *different estimand on the same cached funding/mark data* and is still unfinished (prior partial = 88 events, Q1 2024 only). It is not a re-probe of any TERMINAL_NO_GO liquidation family and does not reopen any sealed verdict.

## NEXT FOCUS CAMPAIGN — heavy work is the DEFAULT path, not trigger-gated

**`FCLR-SHEK-SCALE-20261115T040843Z` — Funding-conditioned correction hazard under volatility regimes (scaled EXPLORATORY_ONLY partial replication of Shek, SSRN 7529458).**

This is the active rank-0 frontier entry (`research_state/experiment_frontier.json`, status `READY_EXECUTE` / `ACTIVE`). It is the primary unfinished question in `RESEARCH_PROMPT.md` §3 and is on-cache, network-free, credential-free.

**Why this and not "wait for a trigger":** H2 is explicitly PARTIAL (88 events / 5 symbols / 2024-Q1; high-RV median 16h vs low-RV 8h, log-rank p=0.0792 — direction matches the paper's 27h/3h claim but is underpowered). The cache now holds ~31 months × 5 Binance symbols of funding+mark (2024-04..2026-10) and 200 coins × 12 months of ironflow funding+candles — enough to resolve the direction at a materially larger sample. This is genuine, computable, un-done heavy work. A end-to-end smoke over 3 scaled months for BTCUSDT already reconstructs events with populated RV regimes (verified 2026-11-15T05:09:18Z); the full campaign is required for adequate power.

**Pre-registered design (freeze BEFORE any outcome inspection):**
- **Frozen event definition:** reuse `research_state/h002_pre_registration.md` verbatim (trailing 90d; two-sided 5th/95th percentile nearest-rank; ≥30 valid funding obs; dedupe same-side extremes; correction = first later obs back inside the band; censor at 168h; RV regime = trailing 24h mark-price log-return terciles). Do not tune thresholds against outcomes.
- **Arm A (Binance):** 5 symbols × all funding-backed months 2024-04..2026-10, **excluding** already-reported 2024-01..2024-03 (keeps an independent sample). Inclusion rule frozen ex-ex ante: ≥30 funding obs in the trailing 90d window and mark coverage for RV; record every exclusion with a reason.
- **Arm B (ironflow cross-coin):** frozen coin universe from `research_state/data_cache/ironflow_bulk/{funding,candles_1h}/2025-05..2026-04.parquet`; freeze inclusion thresholds (e.g. ≥1000 funding obs and ≥5000 candle rows per coin) before counting.
- **Primary estimand:** high-RV vs low-RV correction-time hazard — Kaplan–Meier medians + two-sided log-rank; median-difference with **per-coin cluster** and **per-month block bootstrap** 95% CI; compare to the paper's 27h/3h and the "lower hazard at higher RV" direction.
- **Multiplicity:** Holm across the pre-specified primary family (pooled high-vs-low, positive/negative sides, per-symbol high-vs-low); Arm B is a separate, never-promotable secondary family.
- **Pre-specified sensitivity grid (reported, never used to pick the headline):** percentile 1/99 and 10/90; censor 168h and 336h; tercile and median regime splits.
- **Discipline:** no zero-fill / forward-fill / leakage; report negative and inconclusive cells; EXPLORATORY_ONLY, `promotable=false`, `sealed_artifacts_mutated=false`. Never relabel as vol/liq forecast skill, boundary-breach prediction, or observed-liquidation prediction.

**Mandatory heavy deliverables (all required to complete):**
1. `research_state/prereg_fclr_shek_scale_<UTC>.json` (+ `.md`) frozen pre-outcomes, containing the exact month/coin lists, inclusion thresholds, Holm family, inference method, sensitivity grid, and stopping rules.
2. Extend the **registered** `scripts/funding_correction_replication.py` with a `--scale` mode (preferred — no scope-registry churn; the nested-funding fallback is already fixed this session). Only if unavoidable, add `scripts/fclr_shek_scale.py` **and** sync `research_state/tracka_script_scope_registry.json` + `tests/test_tracka_hardening_117.py` `SCRIPT_REGISTRY` (+118/119) so drift stays 184/184.
3. `tests/test_fclr_shek_scale.py` — fixture-based, deterministic, tmp-isolated, no network: synthetic funding series with a known correction, censoring, dedupe, and RV-regime assignment.
4. `research_state/evaluation_summary_FCLR-SHEK-SCALE-<UTC>.{json,md}` — per-symbol/per-coin event counts, correction/censoring, KM medians, log-rank stats, cluster + block CIs, sensitivity grid, Holm-adjusted p-values, explicit verdict (`REPLICATES_DIRECTION` / `NULL` / `UNDERPOWERED` / `INCONCLUSIVE`).
5. Update `research_state/hypothesis_registry.json` `H2_shek_replication` (keep `EXPLORATORY_ONLY`; never terminal-promote).
6. Advance the frontier rank-0 through phases `DATA_AVAILABILITY_AUDIT → EVENT_RECONSTRUCTION → SURVIVAL_CONTRAST → ROBUSTNESS → COMPLETED_VALIDATED`, then install the next heavy cell at rank 0.

**Verification before any commit:** `python3 -m unittest tests.test_fclr_shek_scale tests.test_active_campaign_gate tests.test_next_campaign_status tests.test_funding_correction_replication -v`; `python3 scripts/fclr_campaign_gate.py` (19/19); `python3 scripts/check_tracka_scope_registry_drift.py` (184/184, or 185/185 only if a new script was added and all registries synced); `python3 scripts/next_campaign_status.py` (must print "no feasible 3-block design in ANY domain"); full suite green (0 failures).

## FIRST ACTION (timestamped, mandatory for the next agentic work session)

**Now: `FCLR-SHEK-SCALE-START-20261115T050918Z` (execute on session start).**
1. Read this file + `RESEARCH_PROMPT.md`; confirm working tree (`git status`, HEAD `de5710f9f`).
2. Re-run the baseline checks and record results here if materially changed: `python3 scripts/fclr_campaign_gate.py`; `python3 scripts/fclr_fwd_vol_2025_disjoint_cross_gate.py`; `python3 scripts/check_tracka_scope_registry_drift.py`; `python3 -m unittest tests.test_active_campaign_gate tests.test_next_campaign_status tests.test_funding_correction_replication -v`.
3. **Freeze the prereg first** (`prereg_fclr_shek_scale_<UTC>.json`): run the data-availability audit (funding-obs counts + mark coverage per symbol-month / per coin) and write the exact eligible sample + exclusions into the prereg **before** looking at any correction-time outcome.
4. Execute the heavy pipeline end-to-end: event reconstruction → survival contrast (KM + log-rank + cluster + block bootstrap + Holm) → pre-specified sensitivity grid → verdict.
5. Produce all deliverables (script/test/eval/registry/frontier), run the verification set, and record the exact commands + results in the execution record below.
6. Commit only if the work is meaningful (never activity-only).

**Execution record — FCLR-SHEK-SCALE-START-20261115T060341Z:** Frontier rank-0 = `FCLR-SHEK-SCALE-20261115T040843Z` (`READY_EXECUTE`/`ACTIVE`). Baseline re-verified green at HEAD `66f24902` clean: campaign gate 19/19, fwd-vol gate PASS, scope drift 184/184, targeted tests 38/38 OK, `next_campaign_status.py` reports no feasible 3-block forecast design in ANY domain. Cached coverage confirmed (Binance funding 2024-04..2026-10 nested layout; ironflow_bulk 200 coins × 12m). No blocking bottlenecks found. **Next session must execute heavy steps 3–5 now:** freeze prereg after data-availability audit, run event reconstruction → survival contrast (KM/log-rank/cluster+block bootstrap/Holm) → sensitivity grid, produce eval/verdict artifacts, update `H2_shek_replication`, advance frontier, and verify. "No trigger" is not a stop condition.

## Optional escalation triggers (do NOT block the default heavy campaign)

- `GATE4_BRANCH_1`: a valid `research_state/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` with `status=RESOLVED_VERIFIED`, `fabricated=false`, and the required human/legal attestation (not agent-settable). If present, preempt with the Gate 4 confirmatory flow.
- `NEW_OBSERVED_LIQUIDATION_SOURCE`: a materially new source family (not a re-probe of the exhausted/terminal families in `research_state/liquidation_source_campaign.md`, `research_state/track_a_deadend_map.md`) that can pass the §16 admissibility audit. If present, run the bounded probe + §16 audit **before** any prereg/outcomes.
- Absence of a trigger is **not** a reason to stop: the default heavy campaign above is always executable on cache.

## Bottlenecks removed (do not recreate) — this session 2026-11-15T05:09:18Z

1. **Phantom "feasible heavy work" in the extended Hyperliquid frontier (CRITICAL).** `scripts/next_campaign_status.py` reported `HYPERLIQUID EXTENDED FRONTIER 2026-05-01..2026-10-31 span=184d FEASIBLE` and `CAMPAIGN STATUS: executable heavy work REMAINS`. This was **false**: `FCLR-011` sealed test (2026-05-08..2026-08-06, 3 blocks) + `FCLR-FWD-VOL-011-CONFIRM` forward walk (2026-08-03..2026-10-31, NOT_REPLICATED) together consume the whole window. `BULK_TESTED_WINDOWS` listed only the two ironflow ranges, so the extended frontier (which reads `hyperliquid_candles` + `hyperliquid_funding` + `ironflow_events`) wrongly surfaced the tested window as untouched. **Fix:** added the FCLR-011 and forward-walk windows to `BULK_TESTED_WINDOWS`; `next_campaign_status.py` now correctly prints "no feasible 3-block design in ANY domain" (matching this handoff). Guarded by `tests/test_next_campaign_status.py::test_extended_frontier_excludes_fclr011_tested_windows` + `test_bulk_tested_windows_cover_fclr011`. This prevents a future agent from burning a session chasing phantom 3-block forecast work on already-tested data.
2. **Shek scaled Arm A funding silently unloaded (CRITICAL for the next campaign).** `scripts/funding_correction_replication.py`'s cache fallback expected `research_state/data_cache/{SYM}_{YYYY_MM}/fundingRate/{SYM}-fundingRate-{YYYY-MM}.csv` (flat), but the real nested layout is `research_state/data_cache/{SYM}_{YYYY_MM}/{SYM}-fundingRate-{YYYY-MM}/{SYM}-fundingRate-{YYYY-MM}.csv`. For every month outside 2024-Q1 (i.e. the entire 2024-04..2026-10 Arm A sample) this yielded **zero events** — the scaled campaign would have been un-runnable and could have been misreported as a clean NULL. **Fix:** fallback now tries the nested dir, the legacy flat dir, a recursive glob, then `data/raw`. Verified: 2024-06 / 2025-06 / 2026-01 each load ~90–93 obs and reconstruct events with populated RV regimes. Guarded by `tests/test_funding_correction_replication.py::test_nested_cache_funding_loads_for_scaled_sample` + `test_scaled_month_range_nonzero_events`.
3. **Frontier rank-0 invalid status** (prior `ACTIVE_WAITING`/`WAITING_EXTERNAL_TRIGGER`) that made `test_active_campaign_gate` red and licensed "stop cleanly" — fixed previously; rank-0 is a valid `READY_EXECUTE`/`ACTIVE` heavy campaign, sentinel demoted to `SUPERSEDED`.
4. **"Cached heavy-work frontier is exhausted / stop cleanly if no trigger"** — removed as a completion path. Exhaustion applies only to the forecast 3-block design; the Shek correction-hazard event study is a distinct, unexhausted estimand.
5. `FCLR-NEXT-002` (power calibration) — COMPLETED_VALIDATED; do not re-run.
6. `FCLR-DESIGN-FEASIBILITY` — COMPLETED_VALIDATED; do not re-run.
7. Scope-registry invariant enforced (184/184); new scripts must be added to BOTH `research_state/tracka_script_scope_registry.json` and `tests/test_tracka_hardening_117.py` `SCRIPT_REGISTRY`.
8. External liquidation hunt — **TERMINAL_NO_GO**; reopen only for a materially new source family with a §16 audit before prereg/outcomes.
9. Vol/Liq **forecast** 3-block frontier — exhausted (`scripts/next_campaign_status.py`); do not re-run tested windows for the same estimand.

## Research-gate / §19 carry-forward (unchanged)

- H1_primary: NOT_SUPPORTED (terminal absent valid trigger/new source). H2_shek_replication: EXPLORATORY_ONLY (now being scaled). H_trackb_modeled_breaches: NOT_SUPPORTED. H_tracka_hl_liquidation_forecast: NOT_MET. Gate 4: EXTERNAL_BLOCKED.
- `FCLR-POWER-CALIBRATION`: COMPLETED_VALIDATED (VOL=NULL_UNDERPOWERED, LIQ=INCONCLUSIVE). `FCLR-DESIGN-FEASIBILITY`: COMPLETED_VALIDATED (VOL=UNDECIDABLE_ON_CACHE, LIQ=DECIDABLE_ON_CACHE analytic&robust no flip).
- **Supported:** null on tested vol/liq windows; vol effect ≥2% structurally undecidable on the cached forecast design (n_req~187k vs 10.8k). Liq decidable at pooled n but sealed non-confirmatory (null asymmetry). **Contradicted:** generalizable funding-conditioned OOS forecast edge. **Unknown:** effects resolvable only with new admissible data/terms, or the Shek correction-hazard direction at scale. **Dominant limitation:** forecast-design cache; liq null-distribution asymmetry/label validity.

## Completion contract

Complete by (a) executing the `FCLR-SHEK-SCALE` heavy campaign to a recorded verdict with a frozen prereg and timestamped eval/verdict artifacts + green gates/tests and no sealed mutation, or (b) recording an evidence-backed blocker citing the exact command/error and proof of a tried materially-different free route. **"No trigger → stop cleanly" is NOT completion.** Never reopen a sealed verdict, never re-probe a TERMINAL_NO_GO family, never edit `.github/workflows/*`, never use paid/credentialed/manual data.