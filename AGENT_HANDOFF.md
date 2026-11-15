# Durable Agent Handoff — refreshed 2026-11-15T04:08:43Z (sole authoritative version)

**SOLE DURABLE HANDOFF — START HERE.** `NEXT_SESSION_HANDOFF.md` is a tombstone; older `AGENT_HANDOFF` revisions and `research_state/FCLR_CAMPAIGN_NEXT.md` (self-superseded) are historical evidence only. This file is the only active handoff. Do not write status-only notes, do not re-probe exhausted families, and do not reopen sealed verdicts.

## Baseline verified this session (2026-11-15T04:08:43Z)

- Full suite at session start: **1326 tests, 1 failure, 1 skip**. The only red test was `tests/test_active_campaign_gate.py::test_frontier_rank0_is_active_heavy_campaign` — the prior session had written rank-0 status `ACTIVE_WAITING` / program_status `WAITING_EXTERNAL_TRIGGER`, which is outside the allowed enum (`READY_EXECUTE`|`TRIGGER_ONLY` / `ACTIVE`|`BOUNDED_TRIGGER_ONLY`). **Fixed this session** (see Bottlenecks removed). That single red test was the blocker that let the prior session "stop cleanly"; it is now green.
- `python3 scripts/fclr_campaign_gate.py` → **19/19 PASS**.
- `python3 scripts/fclr_fwd_vol_2025_disjoint_cross_gate.py` → **GATE PASS**.
- `python3 scripts/check_tracka_scope_registry_drift.py` → **184/184 OK**.
- Cached-data coverage (verified, no network): Binance USDⓈ-M funding = **5 symbols × 31 months (2024-04..2026-10)**; mark/index/premium = **5 symbols × 35 months (2024-01..2026-11)**; ironflow bulk = **200 coins × 12 months (2025-05..2026-04)** for candles_1h / funding / open_interest / liquidations. Cache root `research_state/data_cache/` ≈ 733 MB.
- Prior results unchanged (do not rerun): vol FullHist `NOT_MET` (C2_vs_B1 rel QLIKE 1.19% < 2% floor; CI excludes 0; Holm-sig on t24) — statistically real, economically immaterial. Liq xsec forward `EXPLORATORY_NULL` (decidable at pooled n, null-asymmetric). `H1_primary = NOT_SUPPORTED` (terminal). `H2_shek_replication = EXPLORATORY_ONLY / PARTIAL`.

## Scope correction — "exhausted" is narrower than the prior handoff implied

`python3 scripts/next_campaign_status.py` reports **no feasible 3-block FORECAST design** in any domain. That is correct *for the vol/liq forecasting estimand* (Binance contiguous + ironflow bulk 2025-05..2026-04 + ironflow_events extended are all consumed by the FullHist + Forward campaigns). It does **not** mean "no heavy work remains." The **Shek funding-extreme correction-time event study** is a *different estimand on the same cached funding/mark data* and is still unfinished (prior partial = 88 events, Q1 2024 only). It is not a re-probe of any TERMINAL_NO_GO liquidation family and does not reopen any sealed verdict.

## NEXT FOCUS CAMPAIGN — heavy work is the DEFAULT path, not trigger-gated

**`FCLR-SHEK-SCALE-20261115T040843Z` — Funding-conditioned correction hazard under volatility regimes (scaled EXPLORATORY_ONLY partial replication of Shek, SSRN 7529458).**

This is the active rank-0 frontier entry (`research_state/experiment_frontier.json`, status `READY_EXECUTE` / `ACTIVE`). It is the primary unfinished question in `RESEARCH_PROMPT.md` §3 and is on-cache, network-free, credential-free.

**Why this and not "wait for a trigger":** H2 is explicitly PARTIAL (88 events / 5 symbols / 2024-Q1; high-RV median 16h vs low-RV 8h, log-rank p=0.0792 — direction matches the paper's 27h/3h claim but is underpowered). The cache now holds ~31 months × 5 Binance symbols of funding+mark and 200 coins × 12 months of ironflow funding+candles — enough to resolve the direction at a materially larger sample. This is genuine, computable, un-done heavy work.

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
2. Extend the **registered** `scripts/funding_correction_replication.py` with a `--scale` mode (preferred — no scope-registry churn). Only if unavoidable, add `scripts/fclr_shek_scale.py` **and** sync `research_state/tracka_script_scope_registry.json` + `tests/test_tracka_hardening_117.py` `SCRIPT_REGISTRY` (+118/119) so drift stays 184/184.
3. `tests/test_fclr_shek_scale.py` — fixture-based, deterministic, tmp-isolated, no network: synthetic funding series with a known correction, censoring, dedupe, and RV-regime assignment.
4. `research_state/evaluation_summary_FCLR-SHEK-SCALE-<UTC>.{json,md}` — per-symbol/per-coin event counts, correction/censoring, KM medians, log-rank stats, cluster + block CIs, sensitivity grid, Holm-adjusted p-values, explicit verdict (`REPLICATES_DIRECTION` / `NULL` / `UNDERPOWERED` / `INCONCLUSIVE`).
5. Update `research_state/hypothesis_registry.json` `H2_shek_replication` (keep `EXPLORATORY_ONLY`; never terminal-promote).
6. Advance the frontier rank-0 through phases `DATA_AVAILABILITY_AUDIT → EVENT_RECONSTRUCTION → SURVIVAL_CONTRAST → ROBUSTNESS → COMPLETED_VALIDATED`, then install the next heavy cell at rank 0.

**Verification before any commit:** `python3 -m unittest tests.test_fclr_shek_scale tests.test_active_campaign_gate -v`; `python3 scripts/fclr_campaign_gate.py` (19/19); `python3 scripts/check_tracka_scope_registry_drift.py` (184/184, or 185/185 only if a new script was added and all registries synced); full suite green (0 failures).

## FIRST ACTION (timestamped, mandatory for the next agentic work session)

**Now: `FCLR-SHEK-SCALE-START-20261115T040843Z` (execute on session start).**
1. Read this file + `RESEARCH_PROMPT.md`; confirm working tree (`git status`, HEAD).
2. Re-run the baseline checks and record results here if materially changed: `python3 scripts/fclr_campaign_gate.py`; `python3 scripts/fclr_fwd_vol_2025_disjoint_cross_gate.py`; `python3 scripts/check_tracka_scope_registry_drift.py`; `python3 -m unittest tests.test_active_campaign_gate -v`.
3. **Freeze the prereg first** (`prereg_fclr_shek_scale_<UTC>.json`): run the data-availability audit (funding-obs counts + mark coverage per symbol-month / per coin) and write the exact eligible sample + exclusions into the prereg **before** looking at any correction-time outcome.
4. Execute the heavy pipeline end-to-end: event reconstruction → survival contrast (KM + log-rank + cluster + block bootstrap + Holm) → pre-specified sensitivity grid → verdict.
5. Produce all deliverables (script/test/eval/registry/frontier), run the verification set, and record the exact commands + results in the execution record below.
6. Commit only if the work is meaningful (never activity-only).

**Execution record — FCLR-SHEK-SCALE-START-20261115T040843Z:** frontier rank-0 rewritten to `FCLR-SHEK-SCALE-20261115T040843Z` (`READY_EXECUTE`/`ACTIVE`); `tests.test_active_campaign_gate` now **OK** (was the sole red test). Baseline gates green (campaign 19/19, fwd PASS, scope 184/184). Cached coverage verified for both arms. Next session executes steps 3–5.

## Optional escalation triggers (do NOT block the default heavy campaign)

- `GATE4_BRANCH_1`: a valid `research_state/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` with `status=RESOLVED_VERIFIED`, `fabricated=false`, and the required human/legal attestation (not agent-settable). If present, preempt with the Gate 4 confirmatory flow.
- `NEW_OBSERVED_LIQUIDATION_SOURCE`: a materially new source family (not a re-probe of the exhausted/terminal families in `research_state/liquidation_source_campaign.md`, `research_state/track_a_deadend_map.md`) that can pass the §16 admissibility audit. If present, run the bounded probe + §16 audit **before** any prereg/outcomes.
- Absence of a trigger is **not** a reason to stop: the default heavy campaign above is always executable on cache.

## Bottlenecks removed (do not recreate)

- **Frontier rank-0 invalid status** (prior `ACTIVE_WAITING`/`WAITING_EXTERNAL_TRIGGER`) that made `test_active_campaign_gate` red and licensed "stop cleanly" — fixed; rank-0 is now a valid `READY_EXECUTE`/`ACTIVE` heavy campaign, sentinel demoted to `SUPERSEDED`.
- **"Cached heavy-work frontier is exhausted / stop cleanly if no trigger"** — removed as a completion path. Exhaustion applies only to the forecast 3-block design; the Shek correction-hazard event study is a distinct, unexhausted estimand.
- `FCLR-NEXT-002` (power calibration) — COMPLETED_VALIDATED; do not re-run.
- `FCLR-DESIGN-FEASIBILITY` — COMPLETED_VALIDATED; do not re-run.
- Scope-registry invariant enforced (184/184, 117/118/119 synced); new scripts must be added to BOTH `research_state/tracka_script_scope_registry.json` and `tests/test_tracka_hardening_117.py` `SCRIPT_REGISTRY`.
- External liquidation hunt — **TERMINAL_NO_GO**; reopen only for a materially new source family with a §16 audit before prereg/outcomes.
- Vol/Liq **forecast** 3-block frontier — exhausted (`scripts/next_campaign_status.py`); do not re-run tested windows for the same estimand.

## Research-gate / §19 carry-forward (unchanged)

- H1_primary: NOT_SUPPORTED (terminal absent valid trigger/new source). H2_shek_replication: EXPLORATORY_ONLY (now being scaled). H_trackb_modeled_breaches: NOT_SUPPORTED. H_tracka_hl_liquidation_forecast: NOT_MET. Gate 4: EXTERNAL_BLOCKED.
- `FCLR-POWER-CALIBRATION`: COMPLETED_VALIDATED (VOL=NULL_UNDERPOWERED, LIQ=INCONCLUSIVE). `FCLR-DESIGN-FEASIBILITY`: COMPLETED_VALIDATED (VOL=UNDECIDABLE_ON_CACHE, LIQ=DECIDABLE_ON_CACHE analytic&robust no flip).
- **Supported:** null on tested vol/liq windows; vol effect ≥2% structurally undecidable on the cached forecast design (n_req~187k vs 10.8k). Liq decidable at pooled n but sealed non-confirmatory (null asymmetry). **Contradicted:** generalizable funding-conditioned OOS forecast edge. **Unknown:** effects resolvable only with new admissible data/terms, or the Shek correction-hazard direction at scale. **Dominant limitation:** forecast-design cache; liq null-distribution asymmetry/label validity.

## Completion contract

Complete by (a) executing the `FCLR-SHEK-SCALE` heavy campaign to a recorded verdict with a frozen prereg and timestamped eval/verdict artifacts + green gates/tests and no sealed mutation, or (b) recording an evidence-backed blocker citing the exact command/error and proof of a tried materially-different free route. **"No trigger → stop cleanly" is NOT completion.** Never reopen a sealed verdict, never re-probe a TERMINAL_NO_GO family, never edit `.github/workflows/*`, never use paid/credentialed/manual data.