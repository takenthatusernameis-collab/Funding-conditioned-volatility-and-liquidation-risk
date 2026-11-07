# AGENT_HANDOFF.md — SINGLE DURABLE HANDOFF (NEXT SESSION)

**INITIAL TASK MESSAGE (UTC 2026-11-07T04:33:17Z):** Start immediately with campaign step 1 — reproduce canonical null FCLR-003 (`FCLR_EXPERIMENT=FCLR-003 timeout 1800 python scripts/run_evaluation.py`), record git SHA + output hash. Then execute steps 2-5 in order; no status-only churn. Track A stays blocked/no trigger; do not re-probe. Final: dated session note + close negative unless new admissible data appears.
**TIMESTAMP (UTC):** 2026-11-07T04:28:41Z
**REPO (priority):** `Funding-conditioned-volatility-and-liquidation-risk` — priority per repo name: **Track C funding-conditioned volatility (P0) > Track B modeled boundary breach > Track A observed liquidations (BLOCKED, no trigger)**.
**AUTHORITY:** This file is the **only** durable session handoff. If `research_state/FCLR_CAMPAIGN_NEXT.md`, frontier entries, or stale notes conflict, follow this file and record reconciliation in durable artifacts (not status-only files).

## RECONCILED STATE (2026-11-07T04:28:41Z)

**v3 claim-worthy run executed and reconciled (pre-registered BEFORE outcomes):**
- Pre-registration frozen `2026-11-07T03:35:00Z`: `research_state/pre_registration_gate4_funding_multisplit_v3_30d_20261107T033500Z.md` (GATE4-FUND-VOL-ABLATIONS-MSPLIT-V3-30D). Run `2026-11-07T03:45:53Z`, local admissible data only, no network in run.
- Data sufficiency **MET** (pre-registered): instruments=5 (BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT, BNBUSDT); `ok_30day_splits=4` (required >=3); 2024-04-01..2024-09-30 panel; 4 non-overlapping 30-day walk-forward test blocks, 7d purge/embargo.
- Forecast skill **NOT demonstrated (null preserved):** aggregate QLIKE A_rv_only(baseline)=0.7983 (best). B_rv_signed=12.1836, CI vs A [0.4805, 32.3126] entirely positive (funding harmful). C_rv_abs CI [-0.3716, 0.2708] spans 0. D_rv_signed_abs CI [-0.2540, 7.5122] spans 0. Primary E_rv_funding_trails vs A: point +0.4879, 95% CI [-0.0422, 1.1973], n_obs=12969, n_blocks=120 — spans 0. Per-split deltas unstable in sign/scale. No contrast improves on RV-only baseline.
- Outputs: `research_state/evaluation_summary_funding_v3_30d.md`, `research_state/run_manifest_funding_v3_30d.json`. v1/v2 preserved, not overwritten. `leakage_audit.md` updated additively (clean). Block-bootstrap seed=12345, reps=2000, block=24h.

**Final program status (durable):**
- **H001 (funding-conditioned volatility forecast vs RV-only): NOT_SUPPORTED.** Forecast gate NOT_MET on every claim-worthy panel: FCLR-003 canonical (-3.78%, CI crosses zero), FCLR-008 (+4.30%, CI crosses zero), v3 (CI spans 0; funding harmful in B). No incremental skill of funding + price features over RV-only on OOS 24h realized variance.
- **Risk overlay: INELIGIBLE** (gate requires meaningful OOS improvement over RV-only baseline; not met). Do not build position-sizing/risk-reduction overlay. Do not tune on sealed holdouts.
- **Track A (observed liquidation labels): STRUCTURALLY BLOCKED, NO TRIGGER.** No admissible unauthenticated source with >=5 symbols, >=3 non-overlapping 30-day blocks, documented completeness (Binance liquidationSnapshot 404; fapi forceOrders 451 geo-restricted). Probes==2. Do not re-probe, do not inspect Track A outcomes, no Track A churn. Reopen only if NEW admissible unauthenticated data meets the GO checklist in `research_state/next_data_discovery_plan.md`.
- **Track B (modeled boundary breach): INCONCLUSIVE / closed negative** (FCLR-H003-EXT-001: no robust incremental skill after Holm across 16 cells; track separation enforced).
- No further confirmatory execution is feasible on current admissible data without a NEW admissible unauthenticated data source (RESEARCH_PROMPT.md §16).

**Verification (current):** `python -m unittest discover -s tests -t .` → **725/725 OK**. `python scripts/tracka_resume_check.py` → **pass:true, 17/17, network:false**. Root `research_state` md+json under cap. No `.github/workflows` changes. No tracked bytecode churn.

## BOTTLENOCKS REMOVED
1. **Data-sufficiency bottleneck (v1/v2 shortfall: <5 instruments / <3 non-overlapping 30-day blocks) RESOLVED as NULL by v3.** v3 met sufficiency on local Apr-Sep 2024 data; result: no forecast skill. Do not re-run v1/v2 variants chasing significance — that is threshold shopping, prohibited.
2. **Track A re-probing bottleneck REMOVED.** No trigger; guarded; probes==2. No re-probing, no outcome inspection, no new probe families.
3. **Status-only churn prohibited.** Every session must produce a measurable delta (code + tests + run + durable artifact) or an evidence-backed blocker + materially different route.

## NEXT HEAVY-WORK CAMPAIGN (MANDATORY — P0, every session)
Execute the closed-loop verification campaign below each session. No session ends with only prose/status updates.

**1. Reproduce the canonical null (confirmatory):**
`FCLR_EXPERIMENT=FCLR-003 timeout 1800 python scripts/run_evaluation.py`
→ must reproduce `research_state/evaluation_summary_FCLR003.md` byte-identical on headline metrics (C2 vs B1 +0.015205 QLIKE, CI [-0.020240, 0.056734] crosses zero, gate NOT_MET). Record git SHA + output hash in the session note.

**2. Reproduce the v3 null (claim-worthy sufficiency panel):**
`python scripts/run_funding_ablations.py --symbols BTCUSDT,ETHUSDT,SOLUSDT,XRPUSDT,BNBUSDT --pre-registration research_state/pre_registration_gate4_funding_multisplit_v3_30d_20261107T033500Z.md --out-suffix _repro --experiment-id GATE4-FUND-VOL-ABLATIONS-MSPLIT-V3-30D-REPRO --skip-main-summary`
→ diff `research_state/run_manifest_funding_v3_30d.json` against regenerated manifest; key metrics must match (A=0.798319018412711; E vs A CI [-0.0422, 1.1973]; B CI entirely positive). Do not overwrite v3 outputs.

**3. Regression + integrity:**
`python -m unittest discover -s tests -t .` → 725/725 OK.
`python scripts/tracka_resume_check.py` → pass:true, 17/17.

**4. Durable negative-results consolidation (artifact, not status):**
Append v3 to `research_state/negative_results_report.md` as a new dated section (FCLR-GATE4-V3): instruments=5, 4×30-day blocks, all five contrast CIs span 0 or are positive, verdict PILOT/INCONCLUSIVE-data-sufficiency-met-but-forecast-skill-absent, null preserved, no overlay. Reference exact artifacts and hashes.

**5. Reopen-watch (only if new data appears):**
Review `research_state/next_data_discovery_plan.md` GO checklist only when NEW admissible unauthenticated data (>=5 symbols, >=3 non-overlapping 30-day blocks, provenance/license OK) appears. Do not fetch, do not use creds/paid/manual downloads. If no new data: record "no new admissible data; confirmatory program remains closed negative" and stop cleanly.

## CONSTRAINTS (NON-NEGOTIABLE)
- No trading/paper/live; no credentials/API keys; no paid data; no auth bypass; no manual downloads; local admissible files only.
- Never modify `.github/workflows/`.
- Leakage-resistant: chronological only, purge/embargo >= max horizon, train-only normalization/stats/thresholds, missing != 0.
- Observed liquidations ≠ modeled boundary breaches ≠ volatility/stress; never merge tracks.
- PREREG BEFORE OUTCOMES for any confirmatory/trigger evaluation or instrument-set change affecting claims.
- Preserve negative/inconclusive results; no cherry-picking, no threshold shopping, no relabeling exploratory as confirmatory.
- Heavy work required: measurable delta or evidence-backed blocker + materially different next route. No status-only churn.

## EXPECTED END STATE OF NEXT SESSION
A dated session note recording: (a) canonical FCLR-003 reproduction result vs stored artifact, (b) v3 reproduction diff result, (c) test suite + tracka check outcomes, (d) negative_results_report.md v3 section added or blocker evidence if a command failed, (e) reopen-watch finding. If all checks pass and no new admissible data exists, the session concludes: confirmatory program closed negative, no overlay eligible, awaiting new admissible unauthenticated data per §16.
