# Durable Agent Handoff — sole authoritative version

**SOLE DURABLE HANDOFF — START HERE (refreshed 2026-11-15T19:01:23Z).** `NEXT_SESSION_TASK.md` is a pointer to the INITIAL TASK MESSAGE below; `NEXT_SESSION_HANDOFF.md` is a tombstone; `AGENT_HANDOFF_20261115T073240Z.md` is a retired/superseded proposal (never execute its Track C funding-ablations campaign). Older handoff revisions and `research_state/FCLR_CAMPAIGN_NEXT.md` are historical evidence only. This file is the only active handoff. Do not write status-only notes, do not re-probe exhausted families, do not reopen sealed verdicts, and do not create competing handoff files.

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION — `2026-11-15T19:01:23Z` (SOLE TASK — the only active handoff)

> **REFRESHED 2026-11-15T19:01:23Z.** The prior heavy cell `FCLR-LIQ-COMBINED-PANEL-20261115T170000Z` is **CONCLUDED with verdict `NOT_MET`** (forecast gate) — executed to a frozen prereg + timestamped eval, honestly recorded, and demoted. The **next heavy cell is installed at rank 0: `FCLR-LIQ-XSEC-ORDERING-20261115T185957Z` (`READY_EXECUTE` / `ACTIVE`)**. Heavy work is mandatory/default; status-only sessions are not completion. Do not create parallel handoff files; do not stop because no trigger fired.

> **READ THIS FIRST.** This file is the single durable handoff. `NEXT_SESSION_TASK.md` points here; `NEXT_SESSION_HANDOFF.md` is a tombstone; `AGENT_HANDOFF_20261115T073240Z.md` is retired. **Heavy work is the DEFAULT path, NOT trigger-gated.** Do **not** write status-only handoff notes, do **not** re-probe exhausted families, do **not** reopen sealed verdicts, and do **not** re-edit this file's prose before producing the next campaign deliverables.

### What happened this session (`2026-11-15T19:01:23Z`) — read before starting

1. **The combined metpie+ironflow panel cell was executed to a verdict.** Context acquisition (18:10Z), panel build (18:14Z, 1,740,415 events / 7,512 daily rows / 15 coins), and prereg freeze (18:14Z) were already complete; the missing **eval** was written (`scripts/fclr_liq_combined_eval.py`), run against the frozen prereg `research_state/prereg_fclr_liq_combined_20261115T181449Z.json`, and produced **`NOT_MET`** (`research_state/evaluation_summary_FCLR-LIQ-COMBINED-20261115T185844Z.{json,md}`): C2 (funding+premium+ema) was **worse** than B1 (RV-only) by 17.1% relative QLIKE (95% block-bootstrap CI spans zero; 15 paired instruments; 3 test blocks). This is an honest null, not a bug.
2. **Two bottlenecks were removed (do not recreate):**
   - **Scope-registry drift was RED** (scripts=190, registry=187) because the three combined-panel scripts were unregistered. Fixed: registered `fclr_liq_combined_fetch_context.py`, `fclr_build_liq_combined_panel.py`, `fclr_liq_combined_prereg.py`, and `fclr_liq_combined_eval.py` in **both** `research_state/tracka_script_scope_registry.json` and the canonical `tests/test_tracka_hardening_117.py` `SCRIPT_REGISTRY` (now 191 scripts). Drift is green; `test_tracka_hardening_117`/`118` green.
   - **Stale handoff**: the previous handoff told the next session to redo steps 1–3 that were already done. This refresh corrects that: steps 1–4 of the combined-panel cell are DONE; the open heavy work is the NEW cross-sectional cell below.
3. **The concluded cell was demoted and the next heavy cell installed** so the anti-stop invariant holds (rank-0 must always be an active heavy cell — enforced by `tests/test_active_campaign_gate.py`).

### Why the next campaign (priority = repository name: funding-conditioned volatility AND liquidation risk)

The time-series per-coin QLIKE estimand on the combined panel is exhausted (NOT_MET). A **materially different, admissible, cache-backed** heavy estimand is open on the **liquidation-risk** half of the mission, requiring **no new acquisition**:

- **Cross-sectional liquidation ordering** on the *same* already-built 15-coin combined panel (`research_state/fclr_liq_combined_panel_20261115T181405Z.parquet`, sha256 `81a100d5…`, 1,740,415 events, all causal features present). Each day, rank coins by predicted next-day liquidation intensity and ask whether funding-conditioned features (C2) improve the **cross-sectional ordering** over RV-only (B1). This is a different unit of analysis (cross-section vs per-coin time series), a different loss/metric (rank-IC + top-k hit-rate + cross-sectional QLIKE), and a genuinely new confirmatory estimand — not a re-probe of any sealed verdict.
- If that also returns NOT_MET, install the next materially different heavy cell (e.g., cross-sectional ordering on the 179-coin metpie cross-section, subject to its own §16 admissibility check) — do not stop.

### START NOW — run this exact command block, do not re-derive it:
```
git status --short && git log -1 --oneline
python3 scripts/fclr_campaign_gate.py
python3 scripts/fclr_fwd_vol_2025_disjoint_cross_gate.py
python3 scripts/check_tracka_scope_registry_drift.py
python3 -m unittest tests.test_fclr_shek_scale tests.test_active_campaign_gate tests.test_next_campaign_status tests.test_funding_correction_replication tests.test_tracka_hardening_117 tests.test_tracka_hardening_118 tests.test_fclr_liq_combined_admissibility_audit -v
python3 scripts/next_campaign_status.py
python3 scripts/tracka_resume_check.py
python3 -c "import json; f=json.load(open('research_state/experiment_frontier.json')); r=[e for e in f if e['rank']==0][0]; print('rank0:', r['task'], r['status'], r['program_status'])"
```
Baseline verified green `2026-11-15T19:01:23Z` (campaign gate 19/19 PASS; fwd-vol gate PASS; scope drift 191/191 OK; targeted suite 82/82 OK incl. `tests.test_fclr_liq_combined_admissibility_audit`, `tests.test_active_campaign_gate`, `tests.test_next_campaign_status`, `tests.test_tracka_hardening_117`, `tests.test_tracka_hardening_118`; `next_campaign_status.py` → "no feasible 3-block design in ANY domain"). Frontier rank-0 = `FCLR-LIQ-XSEC-ORDERING-20261115T185957Z` (`READY_EXECUTE` / `ACTIVE`).

**NOTE on `tracka_resume_check.py`:** its `root_md_json_bounded` check fails closed on **untracked** root-level `research_state/*.{md,json}`. At this refresh the only red item is the two new `evaluation_summary_FCLR-LIQ-COMBINED-20261115T185844Z.{json,md}` files, which the standard end-of-session checkpoint commit tracks (HEAD already contains the prior session's `prereg_fclr_liq_combined_*` + fetch/prereg scripts). After that checkpoint the preflight is green. If it is still red when you start, run the checkpoint commit that stages `research_state/evaluation_summary_FCLR-LIQ-COMBINED-*.{json,md}`, `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json`, `research_state/tracka_script_scope_registry.json`, `tests/test_tracka_hardening_117.py`, `scripts/fclr_liq_combined_eval.py` — this is bookkeeping, not a research blocker; then proceed to heavy work.

### Primary heavy task (rank-0, `READY_EXECUTE`): `FCLR-LIQ-XSEC-ORDERING-20261115T185957Z`

Execute these steps in order; each is a hard deliverable with a verifiable artifact. Do not skip to a verdict without a frozen prereg. Reuse the existing panel — no new acquisition.

1. **PREREG_FREEZE (pre-outcomes, mandatory).** Write `scripts/fclr_liq_combined_xsec_prereg.py` and freeze `research_state/prereg_fclr_liq_combined_xsec_<UTC>.{json,md}` with `outcome_data_inspected_before_freeze=false`. Fix, pre-outcomes: **estimand** = daily cross-sectional ordering of next-day liquidation intensity across the 15 coins; **models** B1=`[rv24h,rv168h]`, C2=`[rv24h,rv168h,fundingRate,abs_fund_pct,premium,ema_dist]` (identical causal features to the prior cell); **metrics** = mean daily Spearman rank-IC vs realized next-day intensity, top-3 hit-rate, and cross-sectional QLIKE; **walk** = expanding-window walk-forward over the **same 3 non-overlapping 30-day test blocks** (2025-10-01..10-31, 2026-01-01..01-31, 2026-09-01..09-30); **purge/embargo** 7d; **block bootstrap** ≥2000 deterministic-seed reps (seed 20261115); **Holm** family; **materiality floor** ≥2% (state exactly which metric the 2% applies to). Do not tune thresholds after seeing outcomes.
2. **EVALUATION_AND_GATE.** Write `scripts/fclr_liq_combined_xsec_eval.py`; read the frozen prereg + `research_state/fclr_liq_combined_panel_20261115T181405Z.parquet`; emit `research_state/evaluation_summary_FCLR-LIQ-XSEC-ORDERING-<UTC>.{json,md}` with per-block rank-IC / top-3 hit-rate / cross-sectional QLIKE, block-bootstrap CI, placebo/permutation, per-coin diagnostics, Holm. Run the forecast gate. Update `experiment_frontier.json` + `hypothesis_registry.json` (`H_fclr_liq_xsec_ordering_forecast`) with the verdict. No sealed artifact mutation; no `.github/workflows` edits.
3. **REGISTER BOTH NEW SCRIPTS** in **both** scope registries (`research_state/tracka_script_scope_registry.json` AND `tests/test_tracka_hardening_117.py` `SCRIPT_REGISTRY`) so drift stays green (191 → 193). Re-run `python3 scripts/check_tracka_scope_registry_drift.py` and `tests.test_tracka_hardening_117/118`.

**Acceptance test:** frontier rank-0 advances with a timestamped `evaluation_summary_FCLR-LIQ-XSEC-ORDERING-*` verdict and the campaign gate + full targeted suite stay green (19/19, 82/82, drift green). If the gate is NOT_MET, record the null honestly and install the next materially different heavy cell (179-coin metpie cross-section, subject to §16) at rank 0 — do not stop.

### Hard constraints
- No reopening sealed/terminal families or mutating sealed artifacts; never edit `.github/workflows/*`.
- No outcome-peeking or threshold tuning before the prereg freeze; no network/paid/credentialed/manual data for outcomes (the 15-coin panel is already cache-backed; no new acquisition is needed for this cell).
- Never relabel exploratory as confirmatory; `H2_shek_replication` stays `EXPLORATORY_ONLY`, `promotable=false`.
- Do not poll, do not re-run tested windows for the SAME estimand, do not re-probe TERMINAL_NO_GO families.
- Exactly ONE active handoff (`AGENT_HANDOFF.md`); do not create competing handoff files (the churn failure mode).

### Optional preempt triggers (do NOT block the default heavy campaign)
- `GATE4_BRANCH_1`: a valid `research_state/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` (`status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal attestation) → Gate 4 confirmatory flow under a NEW frozen prereg.
- `NEW_OBSERVED_LIQUIDATION_SOURCE`: a materially new source family (not a re-probe) → §16 admissibility audit BEFORE any prereg/outcomes.
- Absence of a trigger is **never** a reason to stop: the cross-sectional liquidation-ordering heavy campaign is always executable on the existing admissible cache.

## Baseline verified this session (2026-11-15T19:01:23Z)

- Campaign gate 19/19 PASS; fwd-vol gate PASS; scope drift 191/191 OK; targeted suite 82/82 OK (`tests.test_fclr_shek_scale tests.test_active_campaign_gate tests.test_next_campaign_status tests.test_funding_correction_replication tests.test_tracka_hardening_117 tests.test_tracka_hardening_118 tests.test_fclr_liq_combined_admissibility_audit`); `next_campaign_status.py` → "no feasible 3-block design in ANY domain"; frontier rank-0 = `FCLR-LIQ-XSEC-ORDERING-20261115T185957Z` (`READY_EXECUTE` / `ACTIVE`). `tracka_resume_check.py` is green except `root_md_json_bounded` until the 2 new eval summaries are checkpoint-committed (see note above). No sealed artifacts or workflows mutated; no paid/credentialed/manual data used.

## Bottlenecks removed (do not recreate) — this session `2026-11-15T19:01:23Z`

1. **Scope-registry drift (RED → GREEN).** scripts=190 vs registry=187 because the three combined-panel scripts were unregistered. Fixed by registering `fclr_liq_combined_fetch_context.py` (raw_fetch_monitor_provenance), `fclr_build_liq_combined_panel.py` (track_c_or_aux_audit_utility), `fclr_liq_combined_prereg.py` (prereg_utility), and `fclr_liq_combined_eval.py` (track_c_sealed_volatility) in BOTH the JSON registry and the canonical `tests/test_tracka_hardening_117.py` `SCRIPT_REGISTRY` (191 scripts). Drift + `test_tracka_hardening_117/118` green.
2. **Missing eval script (the actual heavy gap).** `scripts/fclr_liq_combined_eval.py` did not exist; the frozen prereg + built panel had no evaluator. Written, debugged (fixed a `predict` intercept off-by-one), and executed to `NOT_MET`. This closed the combined-panel cell to a real verdict.
3. **Stale handoff (redo-loop).** The previous handoff instructed the next session to redo context-acquisition/panel-build/prereg that were already complete. This refresh records the true state and installs the next heavy cell so no session re-derives completed steps.
4. **Frontier demotion + next-cell install (anti-stop invariant).** The concluded `FCLR-LIQ-COMBINED-PANEL` cell was demoted to rank 1 (`SUPERSEDED`, terminal) and `FCLR-LIQ-XSEC-ORDERING-20261115T185957Z` installed at rank 0 (`READY_EXECUTE`/`ACTIVE`) with concrete `next_unfinished_task`, phases, and `next_action_heavy`, so rank-0 is never a terminal/empty cell.
5. **Prior bottlenecks (still in force):** phantom 3-block forecast frontier (next_campaign_status fixed); Shek Arm A nested-cache funding fallback; invalid frontier rank-0; stop-cleanly-as-completion; handoff churn; scope-registry drift; retired Track C handoff. See git history for details.

## Prior sealed verdicts (unchanged — do not reopen)

- H1_primary: NOT_SUPPORTED (FCLR-011 PASS sealed 2026-05..2026-08 but forward confirmation NOT_REPLICATED; period-specific, does not generalize). H2_shek_replication: EXPLORATORY_ONLY (Arm A TAIL_SHAPE_EFFECT, Arm B REPLICATES_DIRECTION; sensitivity grid COMPLETED_VALIDATED). H_trackb_modeled_breaches: NOT_SUPPORTED. Track A observed-liquidation (ironflow-only): expansion PASS but FRAGILE; 2026-05..2026-10 NOT_MET; 2025-11..2026-04 INCONCLUSIVE_PILOT_SHORTFALL; 010-confirm NOT_REPLICATED. Gate 4: EXTERNAL_BLOCKED (no RESOLVED_VERIFIED trigger). `FCLR-POWER-CALIBRATION`, `FCLR-DESIGN-FEASIBILITY`, `FCLR-SHEK-SCALE`, `FCLR-SHEK-SCALE-SENSITIVITY-GRID` all COMPLETED_VALIDATED (retained, demoted). Forecast 3-block frontier on 5-symbol Binance / ironflow-only: exhausted.
- **NEW this session:** `H_fclr_liq_combined_panel_forecast` = **NOT_MET** (terminal; forecast gate; C2 vs B1 on 24h observed liquidation intensity, combined metpie+ironflow 15-coin panel; eval `FCLR-LIQ-COMBINED-20261115T185844Z`; C2 worse by 17.1%, CI spans zero). Do not re-run the same estimand; reopen only on `NEW_OBSERVED_LIQUIDATION_SOURCE` or `HL_LABEL_EXTENSION`.

## Completion contract

Complete by executing `FCLR-LIQ-XSEC-ORDERING-20261115T185957Z` to a recorded verdict with a frozen pre-outcomes prereg, timestamped eval/verdict artifacts, both new scripts registered in both scope registries, green gates/tests (campaign 19/19, targeted suite 82/82, drift green), and no sealed mutation — **or** by recording an evidence-backed blocker citing the exact command/error and proof of a tried materially-different free route, then installing the next heavy cell at rank 0. **"No trigger → stop cleanly" is NOT completion.** Never reopen a sealed verdict, never re-probe a TERMINAL_NO_GO family, never edit `.github/workflows/*`, never use paid/credentialed/manual data for outcomes.