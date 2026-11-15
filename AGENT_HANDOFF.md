# Durable Agent Handoff — 2026-11-15T00:22:44Z

**SOLE DURABLE HANDOFF — START HERE.** `NEXT_SESSION_HANDOFF.md` is a tombstone; `research_state/FCLR_CAMPAIGN_NEXT.md` and every older `AGENT_HANDOFF` revision are superseded historical evidence. Do not plan-only, do not write status-only notes, and do not re-probe exhausted external-data families. Execute the bounded heavy campaign below.

## FIRST ACTION (timestamped initial task for next agentic work session)

**Now (2026-11-15T00:22:44Z): `FCLR-NEXT-002` — design-power and minimum-detectable-effect (MDE) calibration for the concluded nulls.** The confirmatory program is concluded with null/unsupported verdicts, but no artifact states whether the frozen designs could have detected the pre-specified materiality floors. That ambiguity is the dominant remaining uncertainty and the only agent-executable, high-information task left that does not require unavailable external data. Every session must produce either (a) a frozen pre-outcomes prereg plus an executed evaluation artifact that assigns each track a power/MDE verdict (`NULL_INFORMATIVE`, `NULL_UNDERPOWERED`, or `INCONCLUSIVE`) with tests passing and no sealed artifact mutated, or (b) a timestamped evidence-backed blocker with the exact failed precondition and the next materially different free route.

### Why this is the highest-value task (bottleneck removal)

- The prior first action (`NEW_OBSERVED_LIQUIDATION_SOURCE`, FCLR-NEXT-001) was an unbounded external-data hunt. It has now been probed exhaustively across every admissible family and is **TERMINAL_NO_GO** under this environment (evidence in `research_state/liquidation_source_campaign.md`, `research_state/track_a_deadend_map.md`). Keeping it as the first action guarantees repeated status-only sessions. It is closed below; do not reopen it without a materially new source family and a bounded probe budget.
- All cached Binance and Hyperliquid 3-block designs are exhausted (`scripts/next_campaign_status.py`: no feasible 3-block design in any domain). No new confirmatory cell can be run on cached data.
- The two live nulls are: (1) Track C funding-conditioned volatility forecast — `FCLR-FWD-VOL-2025-DISJOINT-CROSS-20261114T183000Z` (`EXPLORATORY_NULL`, corrected audit `NOT_EXPLAINED_BY_ESTIMATOR`), and (2) observed-liquidation cross-section — `TRACKA-LIQ-XSEC-FORWARD-20261113T222859Z` (`EXPLORATORY_NULL`, 107 coins, 3 blocks). Neither has a design-power statement, so "no edge" and "underpowered" are not yet distinguishable. This campaign resolves that with deterministic, offline, read-only analysis of already-persisted design quantities.

### Required execution sequence

1. **Freeze the prereg before computing anything** (no model re-fit, no sealed-verdict recomputation, no outcome inspection):
   - Path: `research_state/prereg_fclr_power_calibration_<UTC>.json` (use the session UTC).
   - Required fields: `status: FROZEN_PRE_OUTCOMES`, `frozen_before_outcomes: true`, `outcome_data_inspected_before_freeze: false`, `promotable: false`, `max_status: EXPLORATORY_ONLY`, `does_not_reopen_sealed_verdict: true`, exact input artifact paths and sha256, the two tracks, the pre-specified floors, the alpha/power convention, and the verdict rule.
2. **Implement `scripts/fclr_power_calibration.py`** (deterministic, offline, no network, no writes to sealed artifacts):
   - Read only the frozen preregs and persisted evaluation JSONs listed below; extract the already-computed standard errors / confidence intervals (vol track) and permutation-null quantiles/SD (liq track). Do not re-fit models or recompute any sealed contrast.
   - Vol track: for each horizon in `{h6,h24,h72,h168}` and per block, derive `SE` from the persisted 95% CI half-width (`SE = (ci_hi - ci_lo) / (2 * 1.96)`), then compute `MDE_80 = (1.96 + 0.8416) * SE` and achieved power at the 2.0% relative-reduction floor. Express MDE both in absolute QLIKE units and as a percentage of the implied baseline (`baseline = -mean_diff / (rel_reduction_pct/100)`). Report per horizon, per block, and pooled.
   - Liq track: for pooled and each block, derive the permutation-null `SE` from the persisted null quantiles (`SE = (null_95th - null_5th) / (2 * 1.645)`), then compute `MDE_80 = 2.8016 * SE` and achieved power at the `|IC| >= 0.05` floor, plus the sign-consistency requirement (>= 2/3 blocks).
   - Bootstrap cross-check (train-only): where train-segment residuals are available from the frozen panel, block-bootstrap the contrast SE and confirm it is consistent with the analytic SE; if unavailable, record the limitation and rely on the analytic path only.
   - Known-answer self-test on a toy fixture (explicitly NOT market evidence, used only to validate the estimator): inject a known coefficient into a small deterministic fixture and assert recovery within tolerance. This satisfies the §18 known-answer requirement and must never be presented as a market result.
3. **Compute the per-track verdict** with this rule (freeze it in the prereg):
   - `NULL_INFORMATIVE`: achieved power at the pre-specified floor >= 0.80 → the null is credible evidence against an effect of floor size.
   - `NULL_UNDERPOWERED`: achieved power < 0.80 → the null cannot exclude an effect of floor size; report the MDE.
   - `INCONCLUSIVE`: required SE/inputs missing or unstable.
4. **Emit artifacts** (all `EXPLORATORY_ONLY`, `promotable: false`, no sealed verdict changed):
   - `research_state/evaluation_summary_FCLR-POWER-CALIBRATION-<UTC>.json` and `.md`, containing the per-track verdict, per-horizon/per-block MDE and power table, input sha256, and the exact command.
   - `tests/test_fclr_power_calibration.py` with fixture tests for: analytic SE from CI, MDE/power arithmetic, train-only bootstrap parity, known-answer recovery, missing-input refusal, and no-mutation of canonical artifacts.
5. **Update state:** set `research_state/experiment_frontier.json` rank-0 to this campaign (`status: READY_EXECUTE`, `program_status: ACTIVE`, non-empty `phases`/`next_unfinished_task`); demote the old trigger-only sentinel to `SUPERSEDED`; update this handoff with what changed, what was tested (exact outcomes), and the next task. Update `research_state/run_manifest.json` only if the manifest contract requires it.
6. **Do not** reopen sealed verdicts, re-run tested windows, re-probe exhausted source families, edit `.github/workflows/*`, add schedulers/controllers/pollers, fetch paid/credentialed/manual data, or commit raw caches.

### Inputs (read-only; verify sha256 before use)

- Vol track prereg: `research_state/prereg_fclr_fwd_vol_2025_disjoint_cross_20261114T183000Z.json`
- Vol track evaluation (SE/CI source): `research_state/evaluation_summary_FCLR-FWD-VOL-2025-DISJOINT-CORRECTED-AUDIT-2026-11-15T00:12:56Z.json` (sealed reference and per-horizon contrasts carry `mean_diff`, `ci_lo`, `ci_hi`, `rel_reduction_pct`, `n_days`)
- Vol track panel (design only): `research_state/tracka_fwd_vol_2025_disjoint_cross_panel_20261114T191615Z.parquet`
- Liq track prereg: `research_state/prereg_tracka_liq_xsec_forward_2026q1q2_20261113T222859Z.json`
- Liq track evaluation (null quantiles/per-block n): `research_state/evaluation_summary_TRACKA-LIQ-XSEC-FORWARD-2026-11-13T22:31:55Z.json`
- Liq track panel (design only): `research_state/tracka_liq_xsec_forward_panel_2026-11-13T22:31:55Z.parquet`
- Cross-check/status: `scripts/next_campaign_status.py`, `scripts/fclr_campaign_gate.py`, `scripts/fclr_fwd_vol_2025_disjoint_cross_gate.py`

Known design parameters already persisted (use to sanity-check, do not recompute outcomes): vol primary `h24 C2_vs_B1` mean_diff `0.006923`, CI `[-0.013104, 0.027938]`, n `10800`, days `90`, 5 symbols, 3 blocks; liq pooled IC `-0.02512`, null 5th `-0.020772`, 95th `0.018998`, pooled n `6634`, per-block n `2996/1605/2033`, 107 coins, 3 blocks.

### Acceptance criteria

- Prereg exists with `status=FROZEN_PRE_OUTCOMES`, `frozen_before_outcomes=true`, `promotable=false`, `max_status=EXPLORATORY_ONLY`, and input hashes.
- `python3 scripts/fclr_power_calibration.py` exits 0 and writes the evaluation JSON/MD with an explicit per-track verdict and MDE/power table.
- `python3 -m unittest tests.test_fclr_power_calibration -v` passes.
- Regression green: the verification block below passes, `scripts/fclr_campaign_gate.py` remains 19/19, and no sealed artifact hash changed.
- The handoff records exact commands, outcomes, and the next task.

### Verification before completion

```bash
cd /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk
python3 scripts/fclr_power_calibration.py
python3 -m unittest tests.test_fclr_power_calibration -v
python3 scripts/next_campaign_status.py
python3 scripts/fclr_fwd_vol_2025_disjoint_cross_gate.py
python3 scripts/fclr_campaign_gate.py
python3 scripts/check_tracka_scope_registry_drift.py
python3 -m unittest tests.test_next_campaign_status tests.test_active_campaign_gate tests.test_tracka_hardening_117 tests.test_tracka_hardening_118 tests.test_tracka_hardening_119 tests.test_fclr_fwd_vol_2025_disjoint_corrected_audit tests.test_fclr_fwd_vol_2025_disjoint_reconcile tests.test_fclr_fwd_vol_2024_disjoint_2024_06 -v
```

Confirm this file remains the sole active handoff and no sealed artifact hash changed.

## Bottlenecks removed (do not recreate)

- **`NEW_OBSERVED_LIQUIDATION_SOURCE` external hunt — TERMINAL_NO_GO.** Exhausted with evidence; exact failed preconditions:
  - Binance `data/futures/um/daily/liquidationSnapshot/` → HTTP 404 (NoSuchKey); `fapi/v1/forceOrders` → HTTP 451 (geo-blocked). No admissible unauthenticated census.
  - OKX `public/liquidation-orders` → HTTP 200 but recent-only filled orders, no historical bulk census for >=3 non-overlapping 30-day blocks.
  - Bybit `public.bybit.com/trading/` → trade CSVs only, no liquidation census; trades cannot be converted to a defensible census.
  - Deribit / Zenodo / OSF / arXiv / GitHub raw / CryptoDataDownload → no matching unauthenticated liquidation census with documented completeness.
  - Hugging Face search → no new dataset; `ochinimus/crypto-liquidation-ticks` (2026-07-08..2026-08-06, CC BY 4.0) is exhausted and wrong-window.
  - metpie `hyperliquid-liquidation-events` (observed, CC BY 4.0, 346k events, 11 coins >=5k) → ~65-day window < 90 days, so 0 feasible 30-day test blocks (`admissibility_audit_metpie_2025Q2_20261112T070000Z`).
  - ironflow observed liquidations cover 2025-05..2026-10 but the contiguous untouched region is too short for a 3-block design; the forward 2026Q1Q2 cell was already executed (`EXPLORATORY_NULL`).
  - Hyperliquid alignment: `fundingHistory` responds, but mark/index/premium/klines depth gaps remain (`tracka_hl_alignment_blocker.md`, 2026-11-11); do not fabricate alignment coverage.
  - **Reopen rule:** only a materially new source family (not a re-probe of the above) with a bounded probe budget and a §16 admissibility audit *before* any prereg/outcomes.
- **Cached Binance/Hyperliquid 3-block frontier — exhausted.** No contiguous run >=127 days, no disjoint 30-day block, no untouched HL region long enough. Do not propose these windows again.
- **Frontier rank-0 realigned** to `FCLR-NEXT-002` so the next agent does not loop on the trigger-only sentinel.

## Verified state (2026-11-15T00:22:44Z)

- Repo: `Funding-conditioned-volatility-and-liquidation-risk`. Do not add schedulers/redundant controllers, edit `.github/workflows/*`, fetch paid/credentialed/manual data, commit raw caches, or reopen sealed verdicts.
- Confirmatory program **CONCLUDED** (`research_state/final_synthesis_report.md`): H001 NOT_SUPPORTED on claim-worthy panels; Track A structurally blocked; no risk overlay eligible.
- Corrected-estimator audit complete (bounded negative): `FCLR-FWD-VOL-2025-DISJOINT-CORRECTED-AUDIT-2026-11-15T00:12:56Z` = `NOT_EXPLAINED_BY_ESTIMATOR` (EXPLORATORY_ONLY); sealed 2025 CROSS preserved; 2024-06 singleton `EXPLAINED_BY_ESTIMATOR`. Do not re-run completed audits on cache.
- `scripts/next_campaign_status.py`: no feasible 3-block design in any domain. `scripts/fclr_campaign_gate.py`: 19/19 pass. `scripts/fclr_fwd_vol_2025_disjoint_cross_gate.py`: GATE PASS.
- Full test suite: **1292 tests OK (1 skipped)**, 0 failures.
- **Pre-existing red baseline repaired this session:** `research_state/tracka_script_scope_registry.json` was missing `fclr_fwd_vol_2024_disjoint_2024_06.py` and `fclr_fwd_vol_2025_disjoint_corrected_audit.py`, so `scripts/check_tracka_scope_registry_drift.py` failed (7 drift tests red). Both are now registered as `track_c_or_aux_audit_utility`, `script_count` = 182, the canonical `tests/test_tracka_hardening_117.py` `SCRIPT_REGISTRY` is synced, and the drift check passes. Do not re-break this invariant.
- `data_source_registry.json` lists `hyperliquid_alignment_context` as PENDING; treat as secondary and do not fabricate coverage.

## Research-gate status (per hypothesis)

- H1_primary: NOT_SUPPORTED (terminal; reopen only via `GATE4_BRANCH_1` or a materially new observed-liquidation source).
- H2_shek_replication: EXPLORATORY_ONLY (partial, non-confirmatory).
- H_trackb_modeled_breaches: NOT_SUPPORTED.
- H_tracka_hl_liquidation_forecast: NOT_MET.
- Gate 4 (Binance v5 terms): EXTERNAL_BLOCKED (no `RESOLVED_VERIFIED` trigger; not agent-settable).
- `FCLR-NEXT-002` (this campaign): READY_EXECUTE / ACTIVE.

## §19 answers (carry forward)

- **Supported / contradicted / unknown:** Supported: null on all tested windows; no robust OOS edge. Contradicted: any claim of a generalizable funding-conditioned edge. Unknown: whether the null is a true absence of a >=2% effect or an artifact of low power (dominant uncertainty this campaign resolves).
- **Strongest alternative explanation:** forecast noise and limited block/sample size make the design unable to resolve a 2%-scale effect; the observed near-zero/wrong-sign point estimates are consistent with an underpowered null.
- **Dominant limitation:** sample size / independent block count / noise, i.e. the MDE, not model choice.
- **Falsifying test:** if analytic and bootstrap power at the floor are >=0.80 and the null persists, "no >=2% effect" is credible; if power <0.80, the null is not falsifying and the MDE must be reported.
- **Highest expected information gain per free compute:** this offline power/MDE calibration (deterministic, no network, no new data).
- **Demonstration artifact/command:** `research_state/evaluation_summary_FCLR-POWER-CALIBRATION-<UTC>.json` via `python3 scripts/fclr_power_calibration.py`.

## What must not be repeated

- Do not re-probe the exhausted liquidation-source families above without materially new evidence.
- Do not re-run tested Binance/Hyperliquid windows or completed audits on cache.
- Do not relabel exploratory results as confirmatory or mutate sealed verdicts.
- Do not emit status-only handoffs; every session must advance `FCLR-NEXT-002` or record an evidence-backed blocker.

## Completion contract

Complete only when (a) the per-track power/MDE evaluation artifact exists with explicit verdicts, tests pass, regression green, and no sealed artifact hash changed, or (b) a timestamped evidence-backed blocker with the exact failed precondition and the next materially different free route is recorded. Status-only work is not completion.