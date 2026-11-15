# Durable Agent Handoff — sole authoritative version

**SOLE DURABLE HANDOFF — START HERE.** `NEXT_SESSION_TASK.md` is a pointer to the INITIAL TASK MESSAGE below; `NEXT_SESSION_HANDOFF.md` is a tombstone; `AGENT_HANDOFF_20261115T073240Z.md` is a retired/superseded proposal (never execute its Track C funding-ablations campaign). Older handoff revisions and `research_state/FCLR_CAMPAIGN_NEXT.md` are historical evidence only. This file is the only active handoff. Do not write status-only notes, do not re-probe exhausted families, and do not reopen sealed verdicts.

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION — `2026-11-15T170000Z` (SOLE TASK — the only active handoff)

> **READ THIS FIRST.** This file is the single durable handoff. `NEXT_SESSION_TASK.md` points here; `NEXT_SESSION_HANDOFF.md` is a tombstone; `AGENT_HANDOFF_20261115T073240Z.md` is retired. **Heavy work is the DEFAULT path, NOT trigger-gated.** Do **not** write status-only handoff notes, do **not** re-probe exhausted families, do **not** reopen sealed verdicts, and do **not** re-edit this file's prose before producing the next campaign deliverables.

### Why this campaign (priority = repository name: funding-conditioned volatility AND liquidation risk)

The prior program exhausted (a) the 5-symbol Binance funding-conditioned volatility 3-block frontier and (b) ironflow-only Hyperliquid observed-liquidation designs. That is **not** "no heavy work remains". A genuinely new, admissible, cache-backed heavy estimand is now open on the **liquidation-risk** half of the mission:

- `research_state/data_cache/metpie_liq/liquidation_events.csv.gz` is a **materially new observed-liquidation source family** (metpie/hyperliquid-liquidation-events, CC BY 4.0, 346,130 events / 179 coins, 2025-03-22..2025-05-25) that has **never been used for any outcome** — it was only audited (INADMISSIBLE alone: 65 days < 90).
- It **abuts** the cached `ironflow_events` archive (2025-05-25..2026-10-31) within ~13 minutes on 2025-05-25, on the identical Hyperliquid coin universe (`market` = `coin` + `-PERP`). Together they form a **continuous 588.5-day Hyperliquid observed-liquidation window (2025-03-22..2026-10-31)** with 19 non-overlapping 30-day blocks (2 pristine metpie blocks) and 15 funded coins ≥5,000 events.
- The §16 admissibility + integration audit is **DONE and green**: `research_state/audits/admissibility_audit_liq_combined_metpie_ironflow_20261115T170000Z.{json,md}` → **ADMISSIBLE_PENDING_BOUNDED_ACQUISITION** (all criteria PASS except aligned market context: cached HL candles/funding cover 2025-11+ only).

This is a NEW confirmatory estimand (new source family + new estimand/window), not a re-probe of any sealed verdict.

### START NOW — run this exact command block, do not re-derive it:
```
git status --short && git log -1 --oneline
python3 scripts/fclr_campaign_gate.py
python3 scripts/fclr_fwd_vol_2025_disjoint_cross_gate.py
python3 scripts/check_tracka_scope_registry_drift.py
python3 -m unittest tests.test_fclr_shek_scale tests.test_active_campaign_gate tests.test_next_campaign_status tests.test_funding_correction_replication tests.test_tracka_hardening_117 tests.test_fclr_liq_combined_admissibility_audit -v
python3 scripts/next_campaign_status.py
python3 scripts/fclr_liq_combined_admissibility_audit.py --stdout
python3 -c "import json; f=json.load(open('research_state/experiment_frontier.json')); r=[e for e in f if e['rank']==0][0]; print('rank0:', r['task'], r['status'], r['program_status'])"
```
Baseline verified green `2026-11-15T170000Z` (campaign gate 19/19 PASS; fwd-vol gate PASS; scope drift 187/187 OK; targeted suite 64/64 OK incl. `tests.test_fclr_liq_combined_admissibility_audit`, `tests.test_active_campaign_gate`, `tests.test_next_campaign_status`, `tests.test_funding_correction_replication`, `tests.test_tracka_hardening_117`; `next_campaign_status.py` → "no feasible 3-block design in ANY domain"). Frontier rank-0 = `FCLR-LIQ-COMBINED-PANEL-20261115T170000Z` (`READY_EXECUTE` / `ACTIVE`). No cache-heavy estimand is closed; the combined liquidation panel is the open heavy cell.

### Primary heavy task (rank-0, `READY_EXECUTE`): `FCLR-LIQ-COMBINED-PANEL-20261115T170000Z`

Execute these steps in order; each is a hard deliverable with a verifiable artifact. Do not skip to a verdict without a frozen prereg.

1. **BOUNDED_CONTEXT_ACQUISITION (network, unauthenticated, idempotent, provenance-stamped).** Fetch Hyperliquid 1h/4h candles + fundingHistory for the 15 funded coins (`AAVE, ADA, AVAX, BNB, BTC, CRV, DOGE, ETH, LINK, LTC, NEAR, SOL, SUI, UNI, XRP`) over **2025-03-22..2025-10-31** (cache currently 2025-11+ only). Reuse the established patterns in `scripts/tracka_hl_fetch_candles_early_4h.py` and `scripts/hyperliquid_funding_fetch.py` (`.accessed.json` + `.sha256` per coin/month, `api.hyperliquid.xyz/info` POST, no keys/signature/requester-pays). Bounded page counts; record provenance; never fabricate.
2. **COMBINED_PANEL_BUILD.** Write `scripts/fclr_build_liq_combined_panel.py` (register it in BOTH scope registries). Load metpie + ironflow, normalize to one schema (`timestamp, coin, notional_usd, side, source`), **dedup on (coin, timestamp, notional_usd, tx-hash)**, and join causal features per coin: 1h/4h funding (signed + 90d past-only abs-funding percentile), mark/index premium, mark/EMA24 distance, RV24h/RV168h. Emit `research_state/fclr_liq_combined_panel_<UTC>.parquet` + `fclr_liq_combined_panel_build_report_<UTC>.json` (row counts before/after filters, per-coin coverage, dedup stats, hashes). No look-ahead; no zero-fill of missing.
3. **PREREG_FREEZE (pre-outcomes, mandatory).** Freeze `research_state/prereg_fclr_liq_combined_<UTC>.{json,md}` with `outcome_data_inspected_before_freeze=false`: 24h observed-liquidation-intensity QLIKE, **C2 vs B1** expanding-window walk-forward, ≥5 instruments, ≥3 non-overlapping 30-day test blocks (include the 2 pristine metpie blocks + estimand-novel 2025-05..2025-10 ironflow blocks), 7d purge/embargo, block bootstrap (≥2000 deterministic-seed reps), Holm family, 2% materiality floor. Do not tune thresholds after seeing outcomes.
4. **EVALUATION_AND_GATE.** Write `scripts/fclr_liq_combined_eval.py` (register it). Emit `research_state/evaluation_summary_FCLR-LIQ-COMBINED-<UTC>.{json,md}` with absolute + relative QLIKE, block-bootstrap CI, LOIO, placebo/permutation, per-coin and per-block diagnostics, Holm. Run the forecast gate. Update `experiment_frontier.json` + `hypothesis_registry.json` (`H_fclr_liq_combined_panel_forecast`) with the verdict. No sealed artifact mutation; no `.github/workflows` edits.

**Acceptance test:** frontier rank-0 advances with a timestamped `evaluation_summary_FCLR-LIQ-COMBINED-*` verdict and the campaign gate + full targeted suite stay green (19/19, 64/64, drift green). If the gate is NOT_MET, record the null honestly and install the next materially different heavy cell (e.g., cross-sectional liquidation ordering on the 179-coin metpie cross-section) at rank 0 — do not stop.

### Hard constraints
- No reopening sealed/terminal families or mutating sealed artifacts; never edit `.github/workflows/*`.
- No outcome-peeking or threshold tuning before the prereg freeze; no network/paid/credentialed/manual data for outcomes (bounded free unauthenticated acquisition is allowed for market context, as in prior Track A work).
- Never relabel exploratory as confirmatory; `H2_shek_replication` stays `EXPLORATORY_ONLY`, `promotable=false`.
- Do not poll, do not re-run tested windows for the SAME estimand, do not re-probe TERMINAL_NO_GO families.
- Exactly ONE active handoff (`AGENT_HANDOFF.md`); do not create competing handoff files (the churn failure mode).

### Optional preempt triggers (do NOT block the default heavy campaign)
- `GATE4_BRANCH_1`: a valid `research_state/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` (`status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal attestation) → Gate 4 confirmatory flow under a NEW frozen prereg.
- `NEW_OBSERVED_LIQUIDATION_SOURCE`: a materially new source family (not a re-probe) → §16 admissibility audit BEFORE any prereg/outcomes.
- Absence of a trigger is **never** a reason to stop: the combined-liquidation-panel heavy campaign is always executable on admissible cache + bounded free context.

## Baseline verified this session (2026-11-15T170000Z)

- Campaign gate 19/19 PASS; fwd-vol gate PASS; scope drift 187/187 OK; targeted suite 64/64 OK (`tests.test_fclr_shek_scale tests.test_active_campaign_gate tests.test_next_campaign_status tests.test_funding_correction_replication tests.test_tracka_hardening_117 tests.test_fclr_liq_combined_admissibility_audit`); `next_campaign_status.py` → "no feasible 3-block design in ANY domain"; `tracka_resume_check.py` drift preflight `pass=true`. No sealed artifacts or workflows mutated; no paid/credentialed/manual data used.

## Bottlenecks removed (do not recreate) — this session `2026-11-15T170000Z`

1. **Trigger-only dead-end replaced with a real heavy campaign (CRITICAL).** Rank-0 previously held `FCLR-BOUNDED-TRIGGER-ONLY-20261115T164031Z` (`TRIGGER_ONLY`), which licensed "stop cleanly" and let sessions avoid heavy work. Fix: demoted that sentinel to `SUPERSEDED` (retained) and installed `FCLR-LIQ-COMBINED-PANEL-20261115T170000Z` at rank 0 (`READY_EXECUTE` / `ACTIVE`) with a concrete `next_unfinished_task`, phases and `next_action_heavy`. Heavy work is now the default path.
2. **Stale hypothesis-registry prose corrected.** `H_tracka_hl_funding_conditioned_volatility_fullhistory` and `H_tracka_hl_liquidation_cross_sectional_funding` claimed "no evaluation artifact / execution pending"; both were actually executed (`TRACKA-VOL-FULLHIST-2026-11-13T02:44:48Z` NOT_MET; `TRACKA-LIQ-XSEC-2026-11-13T00:33:08Z` EXPLORATORY_NULL). Evidence prose corrected; terminal/class/experiment_id/last_verdict unchanged.
3. **Pre-existing red test fixed.** `tests/test_tracka_hardening_118::test_registry_synced_with_test_117` failed on a `fclr_shek_scale.py` class mismatch (JSON `track_c_sealed_volatility` vs test_117 `test_fixture_utility`) — present at HEAD, not introduced here. Fix: aligned test_117 to `track_c_sealed_volatility` (semantically correct); 48/48 registry tests now green.
4. **Drift-preflight root-tracked guard respected.** `scripts/tracka_resume_check.py` fails closed on untracked root-level `research_state/*.{md,json}`. New §16 audit artifacts are written to `research_state/audits/` (subdir) so the guard stays green without uncommitted root churn; the audit script regenerates them deterministically.
5. **Prior bottlenecks (still in force):** phantom 3-block forecast frontier (next_campaign_status fixed); Shek Arm A nested-cache funding fallback; invalid frontier rank-0; stop-cleanly-as-completion; handoff churn; scope-registry drift; retired Track C handoff. See git history for details.

## Prior sealed verdicts (unchanged — do not reopen)

- H1_primary: NOT_SUPPORTED (FCLR-011 PASS sealed 2026-05..2026-08 but forward confirmation NOT_REPLICATED; period-specific, does not generalize). H2_shek_replication: EXPLORATORY_ONLY (Arm A TAIL_SHAPE_EFFECT, Arm B REPLICATES_DIRECTION; sensitivity grid COMPLETED_VALIDATED). H_trackb_modeled_breaches: NOT_SUPPORTED. Track A observed-liquidation (ironflow-only): expansion PASS but FRAGILE; 2026-05..2026-10 NOT_MET; 2025-11..2026-04 INCONCLUSIVE_PILOT_SHORTFALL; 010-confirm NOT_REPLICATED. Gate 4: EXTERNAL_BLOCKED (no RESOLVED_VERIFIED trigger). `FCLR-POWER-CALIBRATION`, `FCLR-DESIGN-FEASIBILITY`, `FCLR-SHEK-SCALE`, `FCLR-SHEK-SCALE-SENSITIVITY-GRID` all COMPLETED_VALIDATED (retained, demoted). Forecast 3-block frontier on 5-symbol Binance / ironflow-only: exhausted.

## Completion contract

Complete by executing `FCLR-LIQ-COMBINED-PANEL-20261115T170000Z` to a recorded verdict with a frozen pre-outcomes prereg, timestamped eval/verdict artifacts, green gates/tests (campaign 19/19, targeted suite, drift green), and no sealed mutation — **or** by recording an evidence-backed blocker citing the exact command/error and proof of a tried materially-different free route, then installing the next heavy cell at rank 0. **"No trigger → stop cleanly" is NOT completion.** Never reopen a sealed verdict, never re-probe a TERMINAL_NO_GO family, never edit `.github/workflows/*`, never use paid/credentialed/manual data for outcomes.