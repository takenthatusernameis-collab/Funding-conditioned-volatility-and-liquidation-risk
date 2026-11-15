# Durable Agent Handoff — sole authoritative version

**SOLE DURABLE HANDOFF — START HERE (refreshed 2026-11-15T20:35:50Z).** `NEXT_SESSION_TASK.md` points here; `NEXT_SESSION_HANDOFF.md` is a tombstone; `AGENT_HANDOFF_20261115T073240Z.md` is retired/superseded. Older revisions and `research_state/FCLR_CAMPAIGN_NEXT.md` are historical evidence only. This file is the only active handoff. Do not write status-only notes, do not re-probe exhausted families, do not reopen sealed verdicts, and do not create competing handoff files.

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION — `2026-11-15T20:35:50Z` (SOLE TASK)

> **READ THIS FIRST.** Heavy work is the DEFAULT path, NOT trigger-gated. Do **not** stop at status, do **not** re-run tested windows for the same estimand, do **not** reopen sealed/terminal families, and do **not** create parallel handoff files.

### Repo priority (from repository name)
`Funding-conditioned-volatility-and-liquidation-risk`: deliver a materially new, cache-backed confirmatory result on funding-conditioned liquidation-risk/volatility forecasting if one exists; otherwise close the next estimand honestly with timestamped evidence and immediately install the next materially different heavy cell at rank 0.

### Current state (verified 2026-11-15T20:35:50Z)
- Baseline green at verification: campaign gate 19/19 PASS; fwd-vol gate PASS; scope drift 191/191 OK; targeted suite 82/82 OK; `next_campaign_status.py` → "no feasible 3-block design in ANY domain"; `tracka_resume_check.py` PASS.
- **Prior rank-0 cell CONCLUDED `NOT_MET` (do not re-run same estimand):** `FCLR-LIQ-XSEC-ORDERING-20261115T185957Z` / `H_fclr_liq_xsec_ordering_forecast` — cross-sectional ordering of next-day liquidation intensity, C2 vs B1 on 15-coin combined metpie+ironflow panel, 3 test blocks (2025-10, 2026-01, 2026-09); C2 worse by 14.3% relative mean daily Spearman rank-IC, 95% block-bootstrap CI excludes zero in wrong direction, Holm rejects primary metric. Cross-sectional QLIKE was secondary (p=0.085, CI spans zero). Artifacts: `research_state/prereg_fclr_liq_combined_xsec_20261115T203501Z.{json,md}`, `research_state/evaluation_summary_FCLR-LIQ-XSEC-ORDERING-20261115T203507Z.{json,md}`.
- **Prior heavy cell CONCLUDED `NOT_MET`:** `FCLR-LIQ-COMBINED-PANEL-20261115T170000Z` / `H_fclr_liq_combined_panel_forecast` — time-series 24h liquidation intensity QLIKE, C2 worse by 17.1%, CI spans zero.
- Bookkeeping: both evaluation summaries present and git-tracked. Working tree clean except your own session edits.
- No sealed artifacts or `.github/workflows/*` mutated; no paid/credentialed/manual data used.

### START NOW — run this exact baseline block
```bash
git status --short --untracked-files=all && git log -1 --oneline
python3 scripts/fclr_campaign_gate.py
python3 scripts/fclr_fwd_vol_2025_disjoint_cross_gate.py
python3 scripts/check_tracka_scope_registry_drift.py
python3 -m unittest tests.test_fclr_shek_scale tests.test_active_campaign_gate tests.test_next_campaign_status tests.test_funding_correction_replication tests.test_tracka_hardening_117 tests.test_tracka_hardening_118 tests.test_fclr_liq_combined_admissibility_audit -v
python3 scripts/next_campaign_status.py
python3 scripts/tracka_resume_check.py
python3 -c "import json; f=json.load(open('research_state/experiment_frontier.json')); r=[e for e in f if e['rank']==0][0]; print('rank0:', r['task'], r['status'], r['program_status'])"
```
Confirm rank-0 is `FCLR-LIQ-XSEC-QLIKE-20261115T203550Z` (`READY_EXECUTE` / `ACTIVE`), then execute the heavy task immediately (do not stop at status).

### PRIMARY HEAVY TASK — `FCLR-LIQ-XSEC-QLIKE-20261115T203550Z` (execute in order, cache-only)
Materially different estimand on the **same admissible cache-backed panel** `research_state/fclr_liq_combined_panel_20261115T181405Z.parquet` (sha256 `81a100d5…`, 1,740,415 events, 7,512 daily rows, 15 coins): **daily cross-sectional QLIKE of next-day liquidation intensity** (different metric from concluded cross-sectional rank-IC; uses the 2 pristine metpie blocks + 1 estimand-novel ironflow block). No new acquisition.

1. **PREREG_FREEZE (mandatory, pre-outcomes).** Create `scripts/fclr_liq_combined_xsec_qlike_prereg.py` and freeze `research_state/prereg_fclr_liq_combined_xsec_qlike_<UTC>.{json,md}` with `outcome_data_inspected_before_freeze=false`. Fix: estimand = cross-sectional QLIKE of next-day liquidation intensity across 15 coins; models B1=`[rv24h,rv168h]`, C2=`[rv24h,rv168h,fundingRate,abs_fund_pct,premium,ema_dist]`; primary metric = mean daily cross-sectional QLIKE (C2 vs B1); secondary metrics = mean daily Spearman rank-IC, top-3 hit-rate; walk = expanding-window over 3 non-overlapping 30-day test blocks: **2 pristine metpie blocks (2025-03-22..2025-04-21, 2025-04-21..2025-05-21) + 1 estimand-novel ironflow block (2025-10-01..2025-10-31)**; purge/embargo 7d; block bootstrap ≥2000 reps deterministic seed 20261115; Holm family of 3 metrics. No threshold tuning after seeing outcomes.
2. **EVALUATION_AND_GATE.** Create `scripts/fclr_liq_combined_xsec_qlike_eval.py`; read frozen prereg + panel; emit `research_state/evaluation_summary_FCLR-LIQ-XSEC-QLIKE-<UTC>.{json,md}` with per-block cross-sectional QLIKE/rank-IC/top-3 hit-rate, block-bootstrap CI, placebo/permutation, per-coin diagnostics, Holm and gate verdict. Update `research_state/experiment_frontier.json` and `research_state/hypothesis_registry.json` (`H_fclr_liq_xsec_qlike_forecast`) with verdict. No sealed artifact mutation; no `.github/workflows/*` edits.
3. **REGISTER NEW SCRIPTS (both registries).** Add `fclr_liq_combined_xsec_qlike_prereg.py` and `fclr_liq_combined_xsec_qlike_eval.py` to BOTH `research_state/tracka_script_scope_registry.json` and `tests/test_tracka_hardening_117.py` `SCRIPT_REGISTRY` with appropriate categories; keep `python3 scripts/check_tracka_scope_registry_drift.py` and `tests.test_tracka_hardening_117/118` green.
4. **CHECKPOINT.** Run targeted tests/gates (incl. drift, 117/118, active_campaign_gate, next_campaign_status, liq_combined_admissibility_audit). Commit deliverables (new scripts, prereg/eval artifacts, registry+test updates, frontier/hypothesis updates, and this handoff refresh). Ensure exactly one active handoff remains this file.

**Acceptance:** frontier rank-0 advances with a timestamped `evaluation_summary_FCLR-LIQ-XSEC-QLIKE-*` verdict and gates/tests stay green. If NOT_MET, record null honestly and immediately install the next materially different heavy cell at rank 0 (e.g. regime-conditional cross-sectional ordering on the combined panel subject to §16/admissibility, or volatility forecasting on the pristine metpie blocks) — do not stop.

### Hard constraints
- Never reopen sealed/terminal families or mutate sealed artifacts; never edit `.github/workflows/*`.
- No outcome-peeking or threshold tuning before prereg freeze; no network/paid/credentialed/manual data for outcomes.
- Never relabel exploratory as confirmatory; `H2_shek_replication` remains `EXPLORATORY_ONLY`, `promotable=false`.
- Do not poll, do not re-run tested windows for the SAME estimand, do not re-probe TERMINAL_NO_GO families.
- Exactly ONE active handoff (`AGENT_HANDOFF.md`). "No trigger → stop cleanly" is NOT completion.

### Optional preempt triggers (do NOT block default heavy campaign)
- `GATE4_BRANCH_1`: valid `research_state/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` (`status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal attestation) → Gate 4 confirmatory flow under NEW frozen prereg.
- `NEW_OBSERVED_LIQUIDATION_SOURCE`: materially new source family (not re-probe) → §16 admissibility audit BEFORE any prereg/outcomes.
- `HL_LABEL_EXTENSION`: verified post-2026-10-31 observed ironflow labels (min depth/audit) → §5/§16 audit then new design.
- Absence of a trigger is never a reason to stop.


## Bottlenecks removed / in force (do not recreate)
- **Removed/updated this refresh (2026-11-15T20:35:50Z):** XSEC ordering cell recorded as CONCLUDED NOT_MET with artifacts; next heavy cell `FCLR-LIQ-XSEC-QLIKE` installed at rank 0 using pristine metpie blocks; scope-registry drift fixed (191 scripts, green).
- **Bookkeeping (cleared this refresh):** prior `evaluation_summary_FCLR-LIQ-COMBINED-20261115T185844Z.{json,md}` and `evaluation_summary_FCLR-LIQ-XSEC-ORDERING-20261115T203507Z.{json,md}` root-bound concern resolved (files present/tracked); `tracka_resume_check` PASS. Keep new eval artifacts tracked in checkpoint commits.
- **Still in force:** phantom 3-block frontier fixed (`next_campaign_status` honest); Shek Arm A nested-cache funding fallback; invalid frontier rank-0 prevention; stop-cleanly-as-completion rejected; handoff churn rejected; sealed verdicts immutable.

## Prior sealed verdicts (unchanged — do not reopen)
- H1_primary: NOT_SUPPORTED. H2_shek_replication: EXPLORATORY_ONLY (promotable=false). H_trackb_modeled_breaches: NOT_SUPPORTED. Track A observed-liquidation (ironflow-only): expansion PASS but FRAGILE; 2026-05..2026-10 NOT_MET; 2025-11..2026-04 INCONCLUSIVE_PILOT_SHORTFALL; 010-confirm NOT_REPLICATED. Gate 4: EXTERNAL_BLOCKED. `FCLR-POWER-CALIBRATION`, `FCLR-DESIGN-FEASIBILITY`, `FCLR-SHEK-SCALE` (+sensitivity) COMPLETED_VALIDATED (demoted). Forecast 3-block frontier on 5-symbol Binance / ironflow-only: exhausted. **`H_fclr_liq_combined_panel_forecast` = NOT_MET** (terminal, same estimand). **`H_fclr_liq_xsec_ordering_forecast` = NOT_MET** (terminal, same estimand). Reopen only on `NEW_OBSERVED_LIQUIDATION_SOURCE` or `HL_LABEL_EXTENSION` as applicable.

## Completion contract
Complete by executing `FCLR-LIQ-XSEC-QLIKE-20261115T203550Z` to a recorded verdict with frozen pre-outcomes prereg, timestamped eval artifacts, both new scripts registered in both scope registries, green gates/tests/drift, and no sealed mutation — **or** by recording an evidence-backed blocker (exact command/error + proof of tried materially-different free route) and installing the next heavy cell at rank 0. "No trigger → stop cleanly" is NOT completion.

## Historical closure reference
Program-level structural closure remains documented in `research_state/fclr_final_structural_closure_20261112T212043.md` (CLOSED_TERMINAL at that time, reopen conditions unchanged). Subsequent admissible cache-backed cells (including combined-panel, xsec ordering, and this xsec QLIKE) are executed under those same constraints when materially different and free of sealed-mutation/outcome-peeking.

(End of file - total 68 lines)