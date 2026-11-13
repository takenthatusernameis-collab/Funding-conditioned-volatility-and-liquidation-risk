# INITIAL TASK MESSAGE — NEXT AGENTIC WORK SESSION (SINGLE DURABLE HANDOFF)

**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Handoff timestamp (UTC):** 2026-11-13T04:20:00Z
**Status:** `PRIMARY_CAMPAIGN_COMPLETE` — Track C forward confirmation NOT_REPLICATED; gate PASS; next focus campaign defined below.

**This file is the ONLY durable handoff.** It supersedes every earlier handoff, checkpoint, closure, and frontier entry. `HANDOFF_NEXT_SESSION.md`, `FOCUS_CAMPAIGN.md`, and `NEXT_SESSION_TASK.md` are redirects to this file. Do not create another `*HANDOFF*`, `*NEXT*`, `*CAMPAIGN*`, or `*TASK*` root file. Update this file in place by appending a dated `## SESSION LOG` entry.

---

## START HERE — `FCLR-HEAVY-CONFIRM-20261113T041200Z` (P1, Track C) — COMPLETED

**Campaign result: NOT_REPLICATED.** The sealed FCLR-011 PASS (4.94%, CI excludes zero, 5 instruments, 3 blocks, 2026-05..2026-08) stands unrefuted but does **not** generalize to the forward window. The pre-registered forward walk-forward (3×30-day blocks, 2026-08-03..2026-10-31, 5 instruments) finds C2 significantly worse than B1 (pooled mean diff +0.026760, 95% CI [0.000343, 0.064822] favouring B1, rel -5.55%, n=10200, 85 days). The reproduction gap is closed: pipeline reproduces FCLR-011 at 4.90% vs sealed 4.94% (delta 0.04pp <= 0.5pp tolerance, `repro_011_pass=True`). `scripts/fclr_heavy_confirm_gate.py` → `GATE: PASS`. Targeted campaign suite: 119 tests OK.

**Bottleneck removed:** `scripts/fclr_fwd_vol_confirm.py::build_legacy_panel` now loads funding from `start` (matching `run_evaluation.py` `START_ALL` = 2026-01-01) instead of `start - 120 days` (September 2025). The wider funding history had shifted `abs_fund_pct` percentiles, causing the 0.55pp repro delta. Repro `start` date aligned to 2026-01-01.

H1_primary set to NOT_SUPPORTED (forward confirmation failed). FCLR-011 PASS remains sealed and unrefuted.

---

## NEXT FOCUS CAMPAIGN — mandatory heavy work (Track A liquidation risk + Track C volatility)

Repo name: `Funding-conditioned-volatility-and-liquidation-risk`. Both tracks are in scope. Each cell below requires a **frozen prereg before outcomes** and a **timestamped evaluation artifact**. No status-only sessions; no monitor-only closure. The campaign is not complete until one cell reaches a terminal verdict (CONFIRMED / NOT_REPLICATED / NOT_SUPPORTED / FRAGILE) and its gate passes.

### Cell 1 — `FCLR-LIQ-010-CONFIRM` (Track A, observed liquidation, P1)

Independent recomputation + LOIO/placebo/leakage audit of the sealed FCLR-010 observed-liquidation PASS (Brier -2.21%, 95% CI [-0.004892, -0.001263], 199 instruments, 5 blocks, Hyperliquid ironflow).

Steps:
1. Freeze prereg `research_state/prereg_fclr_liq_010_confirm_<UTC>.{json,md}` BEFORE any outcome computation (ex-ante gates: LOIO, placebo, leakage audit, block bootstrap).
2. Recompute from the cached Hyperliquid ironflow panel (no new network data).
3. Issue verdict: `CONFIRMED` / `FRAGILE` / `NOT_REPLICATED`.
4. Timestamped evaluation artifact: `research_state/evaluation_summary_FCLR-LIQ-010-CONFIRM-<UTC>.{md,json}`.
5. Atomic state updates: `research_state/hypothesis_registry.json`, `research_state/experiment_frontier.json`.

### Cell 2 — `FCLR-EXP-ROBUST-REDO` (Track A, expansion robustness, P2)

Pre-register a new expansion-robustness design meeting LOIO ≥ 6/8 and placebo PASS, then execute on the sealed expansion panel. The prior sealed 19.04% PASS is FRAGILE (LOIO 4/8, placebo 21.10% ≥ 19.04%); do not re-score it.

Steps:
1. Freeze prereg `research_state/prereg_fclr_exp_robust_redo_<UTC>.{json,md}` BEFORE outcomes (ex-ante LOIO ≥ 6/8, placebo pass criterion, block/bootstrap settings).
2. Execute on sealed expansion panel `research_state/tracka_hl_expansion_panel_20261111T202344Z.parquet`.
3. Issue verdict: `ROBUST` / `FRAGILE` / `INCONCLUSIVE`.
4. Timestamped evaluation artifact + atomic state updates.

### Cell 3 — `FCLR-FWD-VOL-2025-CROSS` (Track C, volatility, P2)

Pre-register a 2025-02..2025-05 walk-forward (3 blocks) to test whether FCLR-011's PASS is period-specific. Use only the cached Binance panel; freeze before outcomes.

Steps:
1. Freeze prereg `research_state/prereg_fclr_fwd_vol_2025_cross_<UTC>.{json,md}` BEFORE outcomes (3×30-day blocks, 7-day embargo, 5 instruments, 2000-rep bootstrap, Holm).
2. Execute on cached Binance mark/premium/index/funding data (2024-01-01..2026-11-08).
3. Issue verdict: `CONFIRMED` / `NOT_REPLICATED` / `INCONCLUSIVE`.
4. Timestamped evaluation artifact + atomic state updates.

---

## NEXT SESSION: EXECUTE NEXT FOCUS CAMPAIGN (no status-only sessions)

### Step 1 — Select and freeze the first cell (blocking)

Choose the highest-value unfinished cell from the NEXT FOCUS CAMPAIGN above. Freeze its prereg BEFORE any outcome computation. The prereg must specify: hypothesis ID, features, model (B1 vs C2), splits, embargo, metrics, gates, verdict rules, multiplicity correction, and the exact artifact path.

### Step 2 — Execute the cell

Run the experiment end-to-end on cached data only (no network, no paid sources, no credentials). Produce a timestamped evaluation artifact.

### Step 3 — Issue the verdict and update state

Record the verdict (CONFIRMED / NOT_REPLICATED / NOT_SUPPORTED / FRAGILE / INCONCLUSIVE) in the evaluation artifact. Update `research_state/hypothesis_registry.json` and `research_state/experiment_frontier.json` with the verdict and artifact hashes.

### Step 4 — Pass the completion gate

If a gate script exists for the cell, run it and confirm `GATE: PASS`. If no gate script exists, create the smallest gate that enforces: final verdict recorded, all pre-registered checks present, panel hash matches build report, prereg frozen pre-outcomes.

---

## ACCEPTANCE GATE (session completion)

1. `python3 scripts/fclr_heavy_confirm_gate.py` → `GATE: PASS`.
2. The latest `evaluation_summary_FCLR-FWD-VOL-011-CONFIRM-*.json` has a final verdict (`CONFIRMED` or `NOT_REPLICATED`) and all 8 checks.
3. `research_state/hypothesis_registry.json` and `research_state/experiment_frontier.json` agree with the verdict.
4. `python -m unittest tests.test_active_campaign_gate tests.test_fclr_final_structural_closure tests.test_monitor_ironflow tests.test_trackc_panel_admissibility_audit tests.test_fclr_heavy_confirm_gate` → all OK.
5. No sealed artifact is mutated; no raw cache is committed; no workflow files are patched.

### Known pre-existing test debt (do not attribute to this campaign)

`python -m unittest discover -s tests` reports 1172 tests with 74 failures + 1 error. These are **pre-existing** and dominated by Track A hardening/drift/registry guards, not by the new campaign:

- `test_registry_covers_all_scripts` / `test_real_repo_passes`: 12 pre-existing scripts were already unregistered (`early4h_campaign.py`, `early4h_liq_glm*.py`, `fclr_campaign_gate.py`, `fclr_final_structural_closure.py`, `fclr_build_tracka_*`, `fclr_ironflow_bulk.py`, `tracka_hl_*`). This session registered its two new scripts; the remaining 12 are pre-existing.
- `test_root_md_json_count_bounded`: root md+json count 352 > 260 (pre-existing artifact accumulation).
- Track A drift preflight (`DRIFT_PREFLIGHT_FAIL_BEFORE_PREREG`) and the recurring-timestamped-family guards were already red before this session.

The **targeted campaign suite is green**: `tests.test_active_campaign_gate tests.test_fclr_final_structural_closure tests.test_monitor_ironflow tests.test_trackc_panel_admissibility_audit tests.test_fclr_heavy_confirm_gate tests.test_run_evaluation_experiment_contract` → 125 tests OK. Do not spend this session on unrelated Track A test debt; the heavy campaign is the priority.

---

## HARD BANS (enforced)

- **No status-only sessions.** Re-running the old monitor checks without executing Step 1–4 is not progress.
- **No "monitor-only / no heavy work authorized" closure.** That state is revoked; it contradicted RESEARCH_PROMPT §16, §19, §20.
- No threshold shopping, post-hoc feature/model/universe changes, or reuse of an inspected window as fresh confirmation without the disclosed sensitivity.
- No zero-fill/forward-fill to force comparability (the legacy reproduction uses zero-fill only for non-core features, and this is documented).
- No mutation of sealed FCLR-011/012-V/013/014 artifacts; no re-labelling a PASS as NOT_SUPPORTED.
- No agent-set Gate 4 `RESOLVED_VERIFIED`; no paid/manual/credentialed data; no `.github/workflows/*` patches.

---

## BOTTLENECKS REMOVED THIS SESSION

| Bottleneck | Resolution |
|---|---|
| False "all volatility NOT_MET" summary | Corrected: FCLR-011 PASS restored; `H1_primary` set INCONCLUSIVE with reconciliation; new campaign rank-0. |
| "No heavy work authorized" deadlock | Revoked; replaced with a mandatory heavy campaign and a fail-closed completion gate. |
| `run_manifest.json` is an unresolved Git-LFS pointer (130 bytes) → every `run_evaluation.py` call crashed | Added `scripts/run_evaluation.py::load_manifest()` + committed `research_state/run_manifest_local.json` offline fallback with verbatim split boundaries. |
| Sealed FCLR-011 panel `data_cache/fclr011_panel.json` was an unresolved Git-LFS pointer (132 bytes) → reproduction cell could not run | **Resolved this session:** `git lfs pull --include research_state/data_cache/fclr011_panel.json` materialized 7,716,808 bytes. Panel now on disk. |
| `build_legacy_panel` funding loaded from `start - 120 days` vs `run_evaluation.py` `START_ALL` → repro delta 0.552pp > 0.5pp tolerance | **Resolved this session:** changed `build_legacy_panel` funding load to `start` and aligned repro `start` to 2026-01-01 matching `run_evaluation.py` START_ALL. Repro delta now 0.044pp <= 0.5pp tolerance, `repro_011_pass=True`. |
| No enforcement that the campaign is executed | Added `scripts/fclr_heavy_confirm_gate.py` and `tests/test_fclr_heavy_confirm_gate.py`; gate fails until a final verdict exists. |
| Frontier/registry drift | Frontier rank-0 is now `FCLR-HEAVY-CONFIRM-20261113T041200Z` / `ACTIVE_HEAVY_CAMPAIGN`; prior FULLHIST entry demoted to rank 1; registry reconciled. |
| Underpowered 5–76 day test windows | New design uses 3 × 30-day blocks with 5 instruments and a 2000-replicate bootstrap. |

---

## EXACT START COMMANDS

```bash
cd <repo>

# Preflight
python3 -c "import numpy,pandas,scipy,pyarrow; print('deps OK')"

# Gate 4 external trigger (expected absent; do not poll)
ls -1 research_state/fclr016_v5_terms_evidence_RESOLVED_*.json 2>/dev/null || echo "NO_VALID_GATE4_TRIGGER"

# Confirm primary campaign is complete (gate PASS, verdict NOT_REPLICATED)
python3 scripts/fclr_heavy_confirm_gate.py

# Next focus campaign: select highest-value cell, freeze prereg BEFORE outcomes
# Cell 1: FCLR-LIQ-010-CONFIRM (Track A liquidation)
# Cell 2: FCLR-EXP-ROBUST-REDO (Track A expansion robustness)
# Cell 3: FCLR-FWD-VOL-2025-CROSS (Track C volatility period-specificity)

# Example: freeze prereg for the chosen cell, then execute:
#   python3 scripts/<cell_script>.py   # produces timestamped evaluation artifact
#   python3 scripts/<cell_gate>.py     # must print GATE: PASS
# Update research_state/hypothesis_registry.json and experiment_frontier.json
```

---

## DEFINITION OF DONE (answer in the handoff)

- What did the evidence support, contradict, or leave unknown?
- Strongest alternative explanation?
- Which data/label/inference limitation dominates uncertainty?
- What concrete new test would falsify the current leading hypothesis?
- What task has the highest expected information gain per unit of free compute?
- Exact artifact and command/test demonstrating progress.

---

## KEY REFERENCES

- `research_state/prereg_fclr_fwd_vol_011_confirm_20261113T041200Z.{json,md}` — frozen prereg (3 × 30-day blocks, gates, verdict rules).
- `research_state/coverage_audit_binance_fwd_vol_20261113T041200Z.{json,md}` — coverage-only audit (5 symbols, 2024-01-01..2026-11-08).
- `scripts/fclr_fwd_vol_confirm.py` — heavy pipeline (walk-forward, bootstrap, Holm, LOIO, placebo, sensitivity, repro).
- `scripts/fclr_heavy_confirm_gate.py` — definition-of-done gate.
- `tests/test_fclr_heavy_confirm_gate.py` — gate enforcement tests.
- `research_state/evaluation_summary_FCLR-FWD-VOL-011-CONFIRM-20261113T041934Z.{md,json}` — current forward result.
- `research_state/evaluation_summary_FCLR-011.md` — the sealed PASS that was suppressed.
- `research_state/evaluation_summary_FCLR-012-V.md` — +15.19% signal, 0 blocks.
- `research_state/run_manifest_local.json` — offline split fallback.
- `RESEARCH_PROMPT.md` §16, §17, §18, §19, §20.

---

## SESSION LOG (append-only; newest first)

## 2026-11-13T07:06:00Z — Kilo session: Executed Cell 1 FCLR-LIQ-010-CONFIRM (Track A observed liquidation, P1) per repo-name priority `Funding-conditioned-volatility-and-liquidation-risk`. Frozen prereg prereg_fclr_liq_010_confirm_20261113T063000Z was pre-outcomes (outcome_data_inspected_before_freeze=false). Independent recompute on cached Hyperliquid ironflow census restricted to 17 funded symbols: C2 vs B1 Brier mean diff -0.000690, 95% CI [-0.001106,-0.000316] (excludes zero, improving), relative reduction 0.501% < 2% materiality floor; LOIO 0/17 at materiality; placebo null_p95 0.525% > true 0.501% (fail); leakage audit PASS. Verdict: NOT_REPLICATED (terminal). Artifacts: evaluation_summary_FCLR-LIQ-010-CONFIRM-20261113T065953Z.{md,json}, panel fclr_liq_010_confirm_panel_20261113T065953Z.parquet (sha ec225a1768...), build report fclr_liq_010_confirm_build_report_20261113T065953Z.json (sha bc23e67a...). Created scripts/fclr_liq_010_confirm_gate.py -> GATE: PASS. Updated hypothesis_registry.json (H_fclr_liq_010_confirm terminal NOT_REPLICATED, artifact/panel/prereg hashes) and experiment_frontier.json (rank-0 ACTIVE_HEAVY_CAMPAIGN; Cell 2 FCLR-EXP-ROBUST-REDO and Cell 3 FCLR-FWD-VOL-2025-CROSS pending; both preregs frozen 20261113T063000Z). Acceptance: fclr_heavy_confirm_gate.py -> GATE: PASS; targeted suite tests.test_active_campaign_gate tests.test_fclr_final_structural_closure tests.test_monitor_ironflow tests.test_trackc_panel_admissibility_audit tests.test_fclr_heavy_confirm_gate -> 119/119 OK. No sealed artifact mutated; no raw cache committed; no workflow files patched.

## 2026-11-13T06:15:55Z — Kilo session: Closed the FCLR-011 reproduction gap and issued the final forward verdict NOT_REPLICATED; primary Track C campaign COMPLETE; gate PASS; next focus campaign defined.

**What changed:** Fixed `scripts/fclr_fwd_vol_confirm.py::build_legacy_panel` — changed funding load from `start - 120 days` (September 2025) to `start` (January 2026, matching `run_evaluation.py` `START_ALL`), and aligned `repro_fclr011` start date to `2026-01-01`. The wider funding history had shifted `abs_fund_pct` percentiles, causing the 0.552pp repro delta. Re-ran `scripts/fclr_fwd_vol_confirm.py` end-to-end: forward result unchanged (C2 vs B1 mean diff +0.026760, CI [0.000343, 0.064822], rel -5.55%); reproduction gap CLOSED (4.90% vs sealed 4.94%, delta 0.044pp <= 0.5pp tolerance, `repro_011_pass=True`). Verdict: NOT_REPLICATED (forward C2 significantly worse than B1; materiality < 2%, CI favors B1). `scripts/fclr_heavy_confirm_gate.py` → GATE: PASS. Updated `research_state/hypothesis_registry.json` (`H_fclr_fwd_vol_011_confirm` → NOT_REPLICATED terminal; `H1_primary` → NOT_SUPPORTED terminal) and `research_state/experiment_frontier.json` (rank-0 → COMPLETED). Targeted campaign suite: 119 tests OK.

**Evidence supported:** FCLR-011 is a genuine sealed gate PASS (4.94%, CI excludes zero, 3 blocks, 2026-05..2026-08). Forward walk-forward finds C2 significantly worse than B1 on fresh data (2026-08-03..2026-10-31). Pipeline reproduces FCLR-011 within tolerance (delta 0.04pp).

**Evidence contradicted:** The claim that the FCLR-011 PASS generalizes to the forward window. C2 degradation is genuine, not a pipeline artifact.

**Unknown / dominant limitation:** None remaining for the primary campaign — reproduction closed, verdict issued, gate passed. Remaining uncertainty is about whether funding-conditioned features work on other windows/venues (next focus campaign cells).

**Strongest alternative explanation:** The FCLR-011 PASS is period-specific (2026-05..2026-08) and does not generalize; the forward C2 degradation reflects a regime change, not a pipeline defect.

**Highest expected information gain:** Execute the next focus campaign cells in order: (1) `FCLR-LIQ-010-CONFIRM` — Track A liquidation risk recomputation per repo name; (2) `FCLR-EXP-ROBUST-REDO` — expansion robustness redo; (3) `FCLR-FWD-VOL-2025-CROSS` — Track C period-specificity test. Each requires frozen prereg before outcomes and timestamped evaluation artifact.

**Artifacts/commands:** `python3 scripts/fclr_fwd_vol_confirm.py` → `evaluation_summary_FCLR-FWD-VOL-011-CONFIRM-20261113T061555Z.{md,json}` (verdict NOT_REPLICATED, all 8 checks). `python3 scripts/fclr_heavy_confirm_gate.py` → GATE: PASS. `python -m unittest tests.test_active_campaign_gate tests.test_fclr_final_structural_closure tests.test_monitor_ironflow tests.test_trackc_panel_admissibility_audit tests.test_fclr_heavy_confirm_gate` → 119 OK.

## 2026-11-13T06:56:11Z — NEXT SESSION TASK: Execute Cell 1 `FCLR-LIQ-010-CONFIRM` (Track A liquidation, P1).

**MANDATORY EXECUTION ORDER — no status-only sessions, no monitor-only closure.**

### Step 1 — Freeze prereg BEFORE outcomes (already done)
Prereg frozen: `research_state/prereg_fclr_liq_010_confirm_20261113T063000Z.{json,md}` (status=FROZEN_PRE_OUTCOMES, outcome_data_inspected_before_freeze=false).

### Step 2 — Execute the cell on cached data only
```bash
cd /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk
python3 scripts/fclr_liq_010_confirm.py
```
- Uses cached Hyperliquid ironflow panel (`results/liqmicro_v2/panel_liqmicro_v2.parquet`) + 17 symbols with cached funding (`research_state/data_cache/hyperliquid_funding/{SYM}.json`).
- No network, no paid sources, no credentials.
- Produces timestamped evaluation artifact: `research_state/evaluation_summary_FCLR-LIQ-010-CONFIRM-<UTC>.{json,md}` and panel/build report.

### Step 3 — Issue verdict and update state
Record verdict (`CONFIRMED` / `FRAGILE` / `NOT_REPLICATED` / `INCONCLUSIVE`) in evaluation artifact. Update:
- `research_state/hypothesis_registry.json` — add/replace `H_fclr_liq_010_confirm` with verdict + artifact hash
- `research_state/experiment_frontier.json` — advance rank-0 to this cell's completion

### Step 4 — Pass completion gate
No dedicated gate script exists for this cell. Create minimal gate enforcing:
1. Final verdict recorded in evaluation artifact (not SMOKE, not INCONCLUSIVE due to missing data)
2. All pre-registered checks present (materiality ≥2%, CI excludes zero, instruments ≥5, blocks ≥3, LOIO ≥4/5, placebo pass, leakage audit pass)
3. Panel hash matches build report
4. Prereg frozen pre-outcomes

Then run acceptance gate:
```bash
python3 scripts/fclr_heavy_confirm_gate.py  # must print GATE: PASS
python -m unittest tests.test_active_campaign_gate tests.test_fclr_final_structural_closure tests.test_monitor_ironflow tests.test_trackc_panel_admissibility_audit tests.test_fclr_heavy_confirm_gate  # all OK
```

### BOTTLENECKS REMOVED — no blockers remain
- Primary Track C campaign COMPLETE (gate PASS, verdict NOT_REPLICATED)
- All three next-focus preregs FROZEN_PRE_OUTCOMES (20261113T063000Z)
- Cached data available: ironflow panel + 17-funded-symbol funding + expansion panel + Binance archive
- Scripts implemented and importable
- Targeted test suite green (119 tests)

**HARD BAN ENFORCED:** This session MUST execute Steps 1–4 above. Re-running monitors, checking status, or producing "progress" without a terminal verdict is not progress.

## 2026-11-13T05:02:10Z — Kilo session: Materialized sealed FCLR-011 panel via `git lfs pull --include research_state/data_cache/fclr011_panel.json` (7,716,808 bytes, was unresolved 132-byte LFS pointer); re-ran `scripts/fclr_fwd_vol_confirm.py` end-to-end; forward result unchanged (C2 vs B1 mean diff +0.026760, CI [0.000343, 0.064822], rel -5.55%); repro gap persists at 0.552pp (>0.5pp tolerance) → `repro_011_pass=False`, verdict INCONCLUSIVE; gate FAILS only on `final_verdict_recorded` (6/7 checks pass). Targeted campaign suite: 119 tests OK. Root cause identified: `build_legacy_panel` in `fclr_fwd_vol_confirm.py` computes RV/EMA on the hourly grid (rolling windows over reindexed grid with NaN gaps, pandas `ewm`) whereas `run_evaluation.py` (`trailing_rv_window`, `build_features_for_origin`) computes on valid mark rows only — the 0.55pp residual matches this grid-vs-valid-row discrepancy.

- **What changed:** `research_state/data_cache/fclr011_panel.json` materialized (LFS pointer resolved). New artifact set: `evaluation_summary_FCLR-FWD-VOL-011-CONFIRM-20261113T050407Z.{md,json}`, `tracka_fwd_vol_panel_20261113T050407Z.parquet`, `tracka_fwd_vol_build_report_20261113T050407Z.json`.
- **Evidence supported:** FCLR-011 is a genuine sealed gate PASS (4.94%, CI excludes zero, 3 blocks). Forward walk-forward finds C2 significantly worse than B1 (pooled +0.026760, CI excludes zero in favor of B1, rel -5.55%, 5/5 LOIO negative). Placebo not significant (null p95 -5.35% vs true -5.55%).
- **Evidence contradicted:** The claim that "all claim-worthy local admissible experiments are exhausted." Binance cache (5 symbols, 2024-01-01..2026-11-08) and the unrefuted FCLR-011 PASS remain.
- **Unknown / dominant limitation:** Exact reproduction of the sealed FCLR-011 panel within ±0.5pp. The pipeline lands at 4.39% vs 4.94% (delta 0.552pp). Fix `build_legacy_panel` to mirror `run_evaluation.py` conventions (`trailing_rv_window` on valid rows, EMA on valid rows only, not grid-based `rolling`/`ewm`), then re-run and confirm `repro_011_pass=True`.
- **Strongest alternative explanation:** The FCLR-011 PASS is period-specific (2026-05..2026-08) and does not generalize; the forward C2 degradation is genuine, not a pipeline artifact.
- **Highest expected information gain:** Fix `build_legacy_panel` RV/EMA conventions → close repro gap → issue final verdict (NOT_REPLICATED if forward CI favors B1; CONFIRMED only if all 8 gates pass) → run gate → run tests → proceed to secondary heavy work (`FCLR-LIQ-010-CONFIRM`, `FCLR-EXP-ROBUST-REDO`, `FCLR-FWD-VOL-2025-CROSS`).
- **Artifacts/commands:** `python3 scripts/fclr_fwd_vol_confirm.py` → `evaluation_summary_FCLR-FWD-VOL-011-CONFIRM-20261113T050407Z.{md,json}`. `python3 scripts/fclr_heavy_confirm_gate.py` → `GATE: FAIL` (INCONCLUSIVE, by design). `python -m unittest tests.test_active_campaign_gate tests.test_fclr_heavy_confirm_gate` → OK.

## 2026-11-13T04:20:00Z — Kilo session: Rebuilt the durable handoff as a mandatory heavy campaign; reconciled the suppressed FCLR-011 PASS; executed a new frozen forward walk-forward; gate fails closed on INCONCLUSIVE pending exact reproduction.

- **What changed:** Replaced the "all NOT_MET / no heavy work / monitor-only" handoff with `FCLR-HEAVY-CONFIRM-20261113T041200Z`. Froze `prereg_fclr_fwd_vol_011_confirm_20261113T041200Z`; built `scripts/fclr_fwd_vol_confirm.py`; added `scripts/fclr_heavy_confirm_gate.py` + `tests/test_fclr_heavy_confirm_gate.py`; added `research_state/run_manifest_local.json` and an LFS-tolerant `load_manifest()` in `scripts/run_evaluation.py`; set frontier rank-0 to `ACTIVE_HEAVY_CAMPAIGN`; corrected `H1_primary` from stale `NOT_SUPPORTED` to `INCONCLUSIVE` with a reconciliation record; added `H_fclr_fwd_vol_011_confirm`.
- **Evidence supported:** FCLR-011 is a genuine gate PASS (4.94%, CI excludes zero, 3 blocks). Prior volatility NOT_MET verdicts were largely block-count failures (5–76 day test windows). The new forward walk-forward finds C2 significantly worse than B1 (pooled +0.02676, 95% CI [0.000343, 0.064822], rel -5.55%, 5/5 LOIO negative).
- **Evidence contradicted:** The claim that "all claim-worthy local admissible experiments are exhausted." The Binance cache (5 symbols, 2024-01-01..2026-11-08) and the unrefuted FCLR-011 PASS remain.
- **Unknown / dominant limitation:** Exact reproduction of the sealed FCLR-011 panel. The pipeline lands at 4.39% vs 4.94% (delta 0.552pp), just outside the pre-registered ±0.5pp tolerance, because `research_state/data_cache/fclr011_panel.json` is an unresolved Git-LFS pointer and the legacy feature code differs slightly on RV/EMA missing-row handling.
- **Strongest alternative explanation:** The FCLR-011 PASS is period-specific (2026-05..2026-08) and does not generalize; the forward C2 degradation is genuine, not a pipeline artifact.
- **Highest expected information gain:** Close the reproduction gap (materialize the sealed panel or exactly replicate the legacy features), then issue the final forward verdict; afterwards run `FCLR-LIQ-010-CONFIRM`, `FCLR-EXP-ROBUST-REDO`, and `FCLR-FWD-VOL-2025-CROSS`.
- **Artifacts/commands:** `python3 scripts/fclr_fwd_vol_confirm.py` → `evaluation_summary_FCLR-FWD-VOL-011-CONFIRM-20261113T041934Z.{md,json}`, panel, build report. `python3 scripts/fclr_heavy_confirm_gate.py` → `GATE: FAIL` (INCONCLUSIVE, by design). `python -m unittest tests.test_active_campaign_gate tests.test_fclr_heavy_confirm_gate` → OK.

<!-- Prior monitor-only entries (2026-11-13T02:44Z..03:23Z) are retained in git history; they are superseded by this entry. -->