# Durable Agent Handoff — refreshed 2026-11-15T02:22:56Z (sole authoritative version; supersedes every prior revision)

**NEXT SESSION: READ THIS FIRST.** The one and only task for the next agentic work session is `FCLR-DESIGN-FEASIBILITY-20261115T021249Z` (the campaign ID is stable; only this handoff was refreshed/re-verified at 2026-11-15T02:22:56Z). It is **unexecuted and verified-ready**: all inputs exist, `fclr_campaign_gate.py` is 19/19, `check_tracka_scope_registry_drift.py` is 183/183, the full suite is **1307 tests OK (1 skipped)**, and the working tree is clean. There is no admissible blocker. Execute the heavy work in "Required execution sequence" below — do not re-plan, do not write a status-only handoff, and do not re-probe any TERMINAL_NO_GO family.

**SOLE DURABLE HANDOFF — START HERE.** `NEXT_SESSION_HANDOFF.md` is a tombstone; `research_state/FCLR_CAMPAIGN_NEXT.md`, `research_state/next_data_discovery_plan.md` (obsolete FCLR-NEXT-001), and every older `AGENT_HANDOFF` revision are superseded historical evidence. Do not plan-only, do not write status-only notes, and do not re-probe exhausted external-data families. Execute the bounded heavy campaign below. There is exactly one first action; it is unexecuted and verified-ready (inputs present, full regression green), so there is no admissible blocker path that avoids real work.

## STATUS OF THE PREVIOUS CAMPAIGN (bottleneck removed — do NOT redo it)

**`FCLR-NEXT-002` (power/MDE calibration) is COMPLETE and GREEN. It is NOT the next task.** A prior session already executed it in full. Do not re-run `scripts/fclr_power_calibration.py`, do not re-derive the SEs, and do not rewrite its prereg/eval. Its verdicts are final and feed the campaign below:

- **Vol track — `NULL_UNDERPOWERED`.** Primary h24 C2_vs_B1: SE=0.010469953, MDE80=0.029332466 QLIKE, floor(|2%|·baseline)=0.007052315 QLIKE, achieved power at floor = **0.103** → the design could not have detected the 2% materiality floor. All four horizons (h6/h24/h72/h168) are `NULL_UNDERPOWERED` (power 0.21 / 0.10 / 0.20 / 0.15).
- **Liq track — `INCONCLUSIVE`.** Pooled SE=0.012089358, MDE80=0.033869366 IC units (above the |IC|>=0.05 floor), raw power-at-floor=0.985 (would be `NULL_INFORMATIVE`), **but the symmetry check FAILED** (`null_mid=-0.000887`, abs_frac=0.0223 > 1% threshold), so the analytic SE is deemed unstable and the verdict is correctly downgraded to `INCONCLUSIVE`. Sign consistency is met (3/3 negative ICs: -0.0409 / -0.0312 / -0.0089).
- Evidence: `research_state/evaluation_summary_FCLR-POWER-CALIBRATION-2026-11-15T01:34:12Z.{json,md}`, prereg `research_state/prereg_fclr_power_calibration_2026-11-15T01:34:12Z.json`. Script `scripts/fclr_power_calibration.py`, tests `tests/test_fclr_power_calibration.py` (15 tests OK).

**Why this unblocks the program:** the dominant remaining uncertainty is now *precisely quantified* — the vol null is an underpowered null (no conclusion about a 2% effect is possible), and the liq null's analytic SE is unstable due to asymmetric permutation quantiles. Both facts are inputs to the campaign below.

## FIRST ACTION (timestamped initial task for the next agentic work session)

**Now (handoff refreshed 2026-11-15T02:22:56Z): `FCLR-DESIGN-FEASIBILITY-20261115T021249Z` — invert the power calibration to determine whether the program is *ever* decidable on cached data.**

Both concluded nulls are now known to be non-informative *as designed*. The next high-information, agent-executable, offline task is to invert the already-persisted SEs and answer a sharp, forward-looking question: **what sample size (and what symbol/block structure) would be required to reach 80% power at each pre-specified floor, and does any admissible cached configuration reach it?** This converts "underpowered null" into either (a) a concrete decidability verdict `DECIDABLE_ON_CACHE` (a larger *cached* design could resolve the floor — name it) or (b) `UNDECIDABLE_ON_CACHE` (the cached data can never resolve the floor; the null is a permanent structural limit, not a fixable sample-size problem). Either verdict is a durable, citable result that closes the "is it underpowered or just under-sampled?" loop. Every session must produce either (a) a frozen prereg plus an executed evaluation artifact assigning each track `DECIDABLE_ON_CACHE` / `UNDECIDABLE_ON_CACHE` / `INCONCLUSIVE` with the required-n table, tests passing, and no sealed artifact mutated, or (b) a timestamped evidence-backed blocker that is a *documented last resort* with exact command, exact error text, and proof the next materially-different free route was tried and failed. A vague "external data missing" claim is NOT a valid blocker — the external-liquidation hunt is TERMINAL_NO_GO.

### Required execution sequence

1. **Freeze the prereg before computing anything** (no model re-fit, no sealed-verdict recomputation, no outcome inspection beyond the already-persisted SEs/design counts):
   - Path: `research_state/prereg_fclr_design_feasibility_<UTC>.json` (use the session UTC).
   - Required fields: `status: FROZEN_PRE_OUTCOMES`, `frozen_before_outcomes: true`, `outcome_data_inspected_before_freeze: false`, `promotable: false`, `max_status: EXPLORATORY_ONLY`, `does_not_reopen_sealed_verdict: true`, exact input artifact paths and sha256, both tracks, the pre-specified floors, the alpha/power convention, the required-n formula, and the decidability rule.
2. **Implement `scripts/fclr_design_feasibility.py`** (deterministic, offline, no network, no writes to sealed artifacts):
   - Read only the power-calibration eval JSON (for the persisted SEs) and the two cached panels (for maximum available n only). Do NOT re-fit models, do NOT recompute any sealed contrast or IC, do NOT re-derive the SEs from raw data — take the SEs as already-persisted inputs from `FCLR-POWER-CALIBRATION-2026-11-15T01:34:12Z.json`.
   - **Required-n inversion.** For each track and floor, invert the two-sided power equation `power = Phi(|delta|/SE - 1.96) + Phi(-|delta|/SE - 1.96) = 0.80` to solve for the SE that would yield 80% power at the floor (`SE_req = |delta| / (1.96 + 0.8416212335729143)`), then convert `SE_req` into a **required-n** using the observed SE scaling. Vol: SE scales as `1/sqrt(n)` (n = pooled obs across symbols×hours×days), so `n_req = n_obs * (SE_obs / SE_req)^2`. Liq: use the same `1/sqrt(n)` scaling on pooled n. Show the derivation explicitly.
   - **Maximum available n (from panels, design counts only).** Vol panel: `n_obs = 30120` rows (5 symbols × 6168 hourly rows; the primary contrast uses n=10800 over 90 days × 5 symbols × 3 blocks × 24h). Liq panel: `n_obs = 6634` pooled (per-block 2996/1605/2033). Report both the raw row count and the contrast-level n used in the sealed design.
   - **Decidability verdict per track.** `DECIDABLE_ON_CACHE` if `n_req <= n_available` (a cached design large enough to hit 80% power at the floor exists, name the required symbol×block structure); `UNDECIDABLE_ON_CACHE` if `n_req > n_available` (no cached configuration can resolve the floor); `INCONCLUSIVE` if SE or scaling is unstable. **Liq-track specific:** the pooled SE is flagged unstable (symmetry fail, abs_frac 0.0223). Report the decidability verdict on the *analytic* SE but **also** report a symmetry-robust variant (e.g. using the larger half-width `max(|q5|,|q95|)` or the observed per-block IC SD) and flag whether the verdict flips. Do not hide the instability.
   - Known-answer self-test on a toy fixture (explicitly NOT market evidence): inject a known SE/n and assert the required-n inversion recovers the injected power. Never present as a market result.
3. **Compute the per-track verdict** with the rule frozen in the prereg (see verdict_space in `experiment_frontier.json` rank-0).
4. **Emit artifacts** (all `EXPLORATORY_ONLY`, `promotable: false`, no sealed verdict changed):
   - `research_state/evaluation_summary_FCLR-DESIGN-FEASIBILITY-<UTC>.json` and `.md`, containing the per-track decidability verdict, the required-n table (per track, per horizon for vol; pooled + per-block for liq), the maximum-available-n comparison, the liq symmetry-robustness check, input sha256, and the exact command.
   - `tests/test_fclr_design_feasibility.py` with fixture tests for: required-n inversion arithmetic, decidability boundary, liq symmetry-robustness flip detection, known-answer recovery, missing/unstable input refusal, and no-mutation of canonical artifacts.
5. **Update state:** set `research_state/experiment_frontier.json` rank-0 to this campaign's completion (`status: COMPLETED_VALIDATED`, verdict recorded) and insert the next rank-0; keep `FCLR-POWER-CALIBRATION-...` at COMPLETED_VALIDATED; update this handoff with what changed, what was tested (exact outcomes), and the next task. Update `research_state/run_manifest.json` only if the manifest contract requires it (note: it is a git-LFS pointer — do not hand-edit).
6. **Do not** reopen sealed verdicts, re-run tested windows, re-probe exhausted source families, edit `.github/workflows/*`, add schedulers/controllers/pollers, fetch paid/credentialed/manual data, or commit raw caches.

### Inputs (read-only; verify sha256 before use)

- Power calibration eval (source of persisted SEs): `research_state/evaluation_summary_FCLR-POWER-CALIBRATION-2026-11-15T01:34:12Z.json`
- Vol panel (max available n only): `research_state/tracka_fwd_vol_2025_disjoint_cross_panel_20261114T191615Z.parquet`
- Liq panel (max available n only): `research_state/tracka_liq_xsec_forward_panel_2026-11-13T22:31:55Z.parquet`
- Cross-check/status: `scripts/next_campaign_status.py`, `scripts/fclr_campaign_gate.py`, `scripts/fclr_power_calibration.py`

Known design parameters already persisted (use to sanity-check; do not recompute outcomes): vol primary h24 C2_vs_B1 SE=0.010469953, MDE80=0.029332466 QLIKE, floor=0.007052315 QLIKE, power=0.103379, n=10800; vol panel rows=30120 (5 symbols, 90 days). liq pooled SE=0.012089358, MDE80=0.033869366 IC, floor=0.05 IC, raw power=0.985219 but symmetry FAIL (abs_frac=0.0223), pooled n=6634, per-block 2996/1605/2033, 107 coins, 3 blocks.

**Self-check anchors (the script MUST reproduce these or its arithmetic is wrong).** Use the exact persisted constants from `FCLR-POWER-CALIBRATION-2026-11-15T01:34:12Z.json` (`method.z_975=1.959963984540054`, `method.z_80=0.8416212335729143`, `method.mde80_factor=2.8015852181129683 = z_975 + z_80`; `method.z_95=1.6448536269514722`):
- Vol required-n at floor: `SE_req = 0.007052315476086073 / 2.8015852181129683 = 0.0025172590`; `n_req = 10800 * (0.010469953259366775 / 0.0025172590)^2 = 186,834.7 ≈ 187,000` contrast-obs — vastly above the 10,800 available → expect `UNDECIDABLE_ON_CACHE` for vol (the cached 5-symbol×90-day design cannot be scaled to 80% power at the 2% floor within any cached configuration).
- Liq required-n at floor (analytic SE): `SE_req = 0.05 / 2.8015852181129683 = 0.0178470388`; since `SE_obs=0.0120893578 < SE_req=0.0178470388`, the analytic SE is already small enough → `n_req < n_available` → analytic verdict `DECIDABLE_ON_CACHE` (but flag the symmetry instability; the symmetry-robust SE using `max(|q5|,|q95|)=0.020772393084283722` gives `SE_robust = 0.020772393084283722/1.6448536269514722 = 0.0126287183`, still `< SE_req`, so the decidability verdict is robust to the asymmetry — report this explicitly).
- These two anchors encode the expected story: vol is structurally underdecidable on cache; liq is decidable-but-unstable, and the instability does not flip the decidability verdict. The script must reproduce this or explain the discrepancy.

### Acceptance criteria

- Prereg exists with `status=FROZEN_PRE_OUTCOMES`, `frozen_before_outcomes=true`, `promotable=false`, `max_status=EXPLORATORY_ONLY`, and input hashes.
- `python3 scripts/fclr_design_feasibility.py` exits 0 and writes the eval JSON/MD with explicit per-track decidability verdicts and the required-n table.
- `python3 -m unittest tests.test_fclr_design_feasibility -v` passes.
- Regression green: the verification block below passes, `scripts/fclr_campaign_gate.py` remains 19/19, scope-registry drift passes, and no sealed artifact hash changed.
- The handoff records exact commands, outcomes, and the next task.

### Verification before completion

```bash
cd /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk
python3 scripts/fclr_design_feasibility.py
python3 -m unittest tests.test_fclr_design_feasibility -v
python3 scripts/next_campaign_status.py
python3 scripts/fclr_fwd_vol_2025_disjoint_cross_gate.py
python3 scripts/fclr_campaign_gate.py
python3 scripts/check_tracka_scope_registry_drift.py
python3 -m unittest tests.test_next_campaign_status tests.test_active_campaign_gate tests.test_tracka_hardening_117 tests.test_tracka_hardening_118 tests.test_tracka_hardening_119 tests.test_fclr_fwd_vol_2025_disjoint_corrected_audit tests.test_fclr_fwd_vol_2025_disjoint_reconcile tests.test_fclr_fwd_vol_2024_disjoint_2024_06 tests.test_fclr_power_calibration -v
```

Confirm this file remains the sole active handoff and no sealed artifact hash changed.

## Bottlenecks removed (do not recreate)

- **Stale handoff pointing at an already-executed campaign — FIXED.** The prior `AGENT_HANDOFF.md` (2026-11-15T01:22:13Z) told the next session to execute `FCLR-NEXT-002`; that was done at 01:34Z and is green. This file now records it as COMPLETED so the next session does not redo it. Do not re-list `FCLR-NEXT-002` as a pending first action.
- **Scope-registry red baseline — REPAIRED.** The prior session added `scripts/fclr_power_calibration.py` to `research_state/tracka_script_scope_registry.json` (183 scripts, drift check passes) but did NOT sync the hardcoded `SCRIPT_REGISTRY` in `tests/test_tracka_hardening_117.py`, leaving 3 registry tests red (117/118/119). Fixed in the prior refresh (2026-11-15T02:12:49Z): `fclr_power_calibration.py` added to test-117 `SCRIPT_REGISTRY` as `track_c_or_aux_audit_utility`. Do not re-break this invariant; any new script must be added to BOTH the registry JSON and test-117 `SCRIPT_REGISTRY`.
- **`NEW_OBSERVED_LIQUIDATION_SOURCE` external hunt — TERMINAL_NO_GO (do not reopen).** Evidence in `research_state/liquidation_source_campaign.md`, `research_state/track_a_deadend_map.md`. Failed preconditions: Binance `liquidationSnapshot`→404 / `forceOrders`→451 geo-block; OKX→recent-only filled orders; Bybit→trades only; Deribit/Zenodo/OSF/arXiv/GitHub/CryptoDataDownload→no admissible census; HuggingFace→exhausted wrong-window; metpie `hyperliquid-liquidation-events`→65-day window < 90 days (0 blocks); ironflow observed→contiguous untouched region too short for 3-block. **Reopen rule:** only a materially new source family (not a re-probe) with a bounded probe budget and a §16 admissibility audit *before* any prereg/outcomes.
- **Cached Binance/Hyperliquid 3-block frontier — exhausted.** No contiguous run >=127 days, no disjoint 30-day block, no untouched HL region long enough (`scripts/next_campaign_status.py`: no feasible 3-block design in any domain). Do not propose these windows again.
- **Frontier rank-0 realigned** to `FCLR-DESIGN-FEASIBILITY-20261115T021249Z` (READY_EXECUTE/ACTIVE); `FCLR-POWER-CALIBRATION-20261115T002244Z` demoted to COMPLETED_VALIDATED.

## Verified state (re-verified 2026-11-15T02:22:56Z by this session; claims below are re-run, not copied)

- Repo: `Funding-conditioned-volatility-and-liquidation-risk`. Do not add schedulers/redundant controllers, edit `.github/workflows/*`, fetch paid/credentialed/manual data, commit raw caches, or reopen sealed verdicts.
- Confirmatory program **CONCLUDED** (`research_state/final_synthesis_report.md`): H001 NOT_SUPPORTED on claim-worthy panels; Track A structurally blocked; no risk overlay eligible.
- Corrected-estimator audit complete (bounded negative): `FCLR-FWD-VOL-2025-DISJOINT-CORRECTED-AUDIT-2026-11-15T00:12:56Z` = `NOT_EXPLAINED_BY_ESTIMATOR` (EXPLORATORY_ONLY); sealed 2025 CROSS preserved; 2024-06 singleton `EXPLAINED_BY_ESTIMATOR`. Do not re-run completed audits on cache.
- Power calibration **COMPLETE**: `FCLR-POWER-CALIBRATION-2026-11-15T01:34:12Z` (VOL=NULL_UNDERPOWERED, LIQ=INCONCLUSIVE). Do not re-run.
- `scripts/next_campaign_status.py`: no feasible 3-block design in any domain. `scripts/fclr_campaign_gate.py`: 19/19 pass. `scripts/fclr_fwd_vol_2025_disjoint_cross_gate.py`: GATE PASS. `scripts/check_tracka_scope_registry_drift.py`: scripts=183 registry=183 OK.
- Full test suite: **1307 tests OK (1 skipped)**, 0 failures (re-run this session, `python3 -m unittest discover tests`, exit 0). The only test side effect (`research_state/ironflow_fastpath_cache.json` timestamp) was restored; working tree is clean.
- Sealed vol eval hash unchanged: `b829fbe90a6da05f55f4be0821716ab802494452390eb867d29ee281a64d569b`.
- `data_source_registry.json` lists `hyperliquid_alignment_context` as PENDING; treat as secondary and do not fabricate coverage.

## Research-gate status (per hypothesis)

- H1_primary: NOT_SUPPORTED (terminal; reopen only via `GATE4_BRANCH_1` or a materially new observed-liquidation source).
- H2_shek_replication: EXPLORATORY_ONLY (partial, non-confirmatory).
- H_trackb_modeled_breaches: NOT_SUPPORTED.
- H_tracka_hl_liquidation_forecast: NOT_MET.
- Gate 4 (Binance v5 terms): EXTERNAL_BLOCKED (no `RESOLVED_VERIFIED` trigger; not agent-settable).
- `FCLR-NEXT-002` (power calibration): **COMPLETED_VALIDATED** (VOL=NULL_UNDERPOWERED, LIQ=INCONCLUSIVE).
- `FCLR-DESIGN-FEASIBILITY-20261115T021249Z` (this campaign): READY_EXECUTE / ACTIVE.

## §19 answers (carry forward)

- **Supported / contradicted / unknown:** Supported: null on all tested windows; no robust OOS edge; both concluded nulls are now *known to be underpowered (vol) or analytic-unstable (liq)*. Contradicted: any claim of a generalizable funding-conditioned edge. Unknown (this campaign resolves): whether the underpowered vol null is a permanent structural limit on cached data or fixable by a larger cached design.
- **Strongest alternative explanation:** the vol design's sample size (5 symbols × 90 days) makes a 2%-scale effect undetectable; the liq design's permutation-null asymmetry makes the analytic SE unreliable.
- **Dominant limitation:** sample size / independent block count / noise (the MDE), now quantified.
- **Falsifying test:** if the required-n inversion shows `n_req > n_available` for the vol floor, "no detectable >=2% effect on cached data" is a structural conclusion, not a fixable power problem; if `n_req <= n_available`, a larger cached design is named as the decidability path.
- **Highest expected information gain per free compute:** this offline required-n / decidability inversion (deterministic, no network, no new data).
- **Demonstration artifact/command:** `research_state/evaluation_summary_FCLR-DESIGN-FEASIBILITY-<UTC>.json` via `python3 scripts/fclr_design_feasibility.py`.

## What must not be repeated

- Do not re-run or re-derive the power calibration (`FCLR-NEXT-002`) — it is complete and final.
- Do not re-probe the exhausted liquidation-source families above without materially new evidence.
- Do not re-run tested Binance/Hyperliquid windows or completed audits on cache.
- Do not relabel exploratory results as confirmatory or mutate sealed verdicts.
- Do not emit status-only handoffs; every session must advance `FCLR-DESIGN-FEASIBILITY` or record an evidence-backed blocker.
- Any new script must be registered in BOTH `research_state/tracka_script_scope_registry.json` and `tests/test_tracka_hardening_117.py` `SCRIPT_REGISTRY` (else 3 registry tests go red).

## Completion contract

Complete only when (a) the per-track decidability evaluation artifact exists with explicit verdicts (`DECIDABLE_ON_CACHE` / `UNDECIDABLE_ON_CACHE` / `INCONCLUSIVE` per track), the required-n arithmetic matches the self-check anchors above, `python3 -m unittest tests.test_fclr_design_feasibility -v` passes, the full regression block below is green, and no sealed artifact hash changed; **or** (b) a blocker is recorded that is a genuine last resort — it must cite the exact command, the exact error/exit text, and the already-tried next materially-different free route, and must NOT be any of the known TERMINAL_NO_GO / exhausted families. A blocker that is simply "no new data" is invalid. Status-only work, plan-only notes, and re-probing exhausted families are not completion.

**This session's directive (do not defer):** the campaign is unexecuted and verified-ready (inputs present, `fclr_campaign_gate.py` 19/19, `check_tracka_scope_registry_drift.py` pass, full suite 1307 OK, no actionable orphaned preregs). There is no admissible blocker. Execute the heavy work; do not produce a status-only handoff.