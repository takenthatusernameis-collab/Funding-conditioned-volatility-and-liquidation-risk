# INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION
**Repository:** Funding-conditioned-volatility-and-liquidation-risk
**Timestamp:** 2026-11-21T08:56:02Z
**Sole active campaign:** FCLR-PANEL-FE-001-20261121T085602Z (rank-0, READY_EXECUTE/ACTIVE — panel fixed-effects funding-conditioning of RV + liquidation intensity with walk-forward OOS; replaces the trigger-gated liquidation-OOS dead end)

---

## WHY THIS IS THE FOCUS (repository-name priority + bottleneck removal)

The repository name **Funding-conditioned-volatility-and-liquidation-risk** defines two scientific halves reconciled by funding conditioning:
- **(a) Does the funding rate condition volatility (RV)?**
- **(b) Does it condition liquidation risk?**

Every prior campaign answered these with **pooled cross-sectional regime contrasts** or a **3-block time-series confirmation**. Both routes are exhausted or underpowered on the frozen panels:
- The cross-sectional program (FCLR-XSEC-001..008) is terminal: associations are detectable only in specific regimes and are not homogeneous (I²≈97%) nor robust under random effects.
- The OOS forecast gate (FCLR-LIQ-OOS-FORECAST-001) FAILED (QLIKE FAIL).
- The 3-block confirmatory design is impossible: `python3 scripts/next_campaign_status.py` → **NO_FEASIBLE_3_BLOCK_DESIGN_IN_ANY_DOMAIN** (no ≥127-day untouched contiguous region in any domain).
- The prior rank-0 was a trigger-only sentinel gated on an external `NEW_OBSERVED_LIQUIDATION_SOURCE` that **cannot fire** in this closed environment, then a consolidation (CONSOLIDATORY_ONLY). Both left the next session with nothing executable → a blocked frontier.

**This bottleneck is removed** by redirecting to a **materially different, feasible design** that uses the full frozen panels (two-way coin+hour fixed effects + expanding-window walk-forward), which the 3-block frontier check does not certify as exhausted.

---

## WHAT WAS DONE THIS SESSION (bottleneck removal + de-risking — already complete)

- **Environment repaired:** numpy/pandas/scipy/pyarrow were absent (a hard blocker for any heavy eval script); reinstalled from `requirements.txt`; `numpy 2.5.5 / pandas 3.1.1 / scipy 1.18.1 / pyarrow 26.0.1` now import.
- **Schema feasibility confirmed (columns only, no outcome statistics inspected):**
  - FCLR-001 has `signed_funding, funding_asof_lag_h, rv1h, rv24h, target_rv24h, log_rv1h, …` → supports the RV half.
  - Combined liquidation panel is event-level (`notional_usd, fundingRate, …`) → aggregate to hourly count+notional per coin → supports the liquidation half.
- **Gate family wired:** `FCLR-PANEL-FE-001` added to `scripts/check_handoff_heavywork_gate.py` (constants + `_panel_fe_state` + payload key + wiring + `fclr_panelfe` in `NEW_QUANT_PREFIXES`), with regression tests in `tests/test_tracka_hardening_143.py::TestPanelFeCampaignGate` (5 tests). Post-20261121T085602Z sessions that skip the full panel-FE artifact set fail closed.

---

## THE CAMPAIGN: FCLR-PANEL-FE-001 (execute end-to-end, heavy, non-deferrable)

### Pre-registered hypotheses (freeze BEFORE inspecting outcomes)
- **H_panelfe_vol (half a):** two-way (coin + hour) FE panel on FCLR-001; coefficient on `funding_asof_lag_h`/`signed_funding` for next-hour `log_rv1h` (robustness `target_rv24h`) is non-zero and ≥2% economically material.
- **H_panelfe_liq (half b):** two-way (coin + hour) FE panel on the hourly-aggregated combined liquidation panel; coefficient on `fundingRate`/`abs_fund_pct` for `log(1+liq_count)` and `log(1+notional_usd)` is non-zero and ≥2% economically material.

### Inference & evaluation (pre-register these)
- Two-way (coin + hour) fixed effects; cluster-robust SE by coin **and** Driscoll-Kraay HAC SE; Newey-West robustness.
- Secondary regime cuts: RV tercile, UTC session bucket (Asia/EU/US).
- Walk-forward OOS: expanding-window one-step-ahead; funding-conditioned vs no-funding baseline; QLIKE (RV) and Poisson/NB deviance + QLIKE (liq intensity); Diebold-Mariano equal-predictive-accuracy test.
- 2% materiality floor preserved; nulls recorded as NOT_SUPPORTED.

### Mandatory artifacts (under a NEW `research_state/session_<UTC>/`, UTC > 20261121T085602Z, all non-empty)
- `fclr_panelfe01_prereg_<UTC>.json` + `.md` (outcome-blind freeze, `outcome_data_inspected_before_freeze=false`, panel sha256)
- `fclr_panelfe01_eval_<UTC>.py` + `.json` + `.md` (FE estimation + walk-forward, both halves)
- `fclr_panelfe01_recompute_<UTC>.py` + `.json` (independent stdlib/numpy recompute that concurs)
- `fclr_panelfe01_evidence_audit_<UTC>.json` + `.md`
- `trigger_check_<UTC>.json` (non-empty)

---

## ACCEPTANCE TESTS (run these — they are the gate)

```bash
python3 scripts/check_handoff_heavywork_gate.py
python3 -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_125 tests.test_tracka_hardening_143
python3 scripts/next_campaign_status.py
```

**Expected gate output:** `[PASS] handoff-heavywork gate: ... reason=OK`
**Expected frontier output:** `== CAMPAIGN STATUS: no feasible 3-block design in ANY domain ==` (expected; this is why the panel route is admissible).

**State verification:**
- `experiment_frontier.json` rank 0 = FCLR-PANEL-FE-001-20261121T085602Z READY_EXECUTE/ACTIVE; all others SUPERSEDED.
- `hypothesis_registry.json` records `H_fclr_panelfe_001` FROZEN_PRE_OUTCOMES / pending.
- No liquidation/RV outcomes inspected before the prereg freeze.
- Root `research_state/` md+json count stays ≤ 500 (currently 499/500).

---

## HARD CONSTRAINTS (do not violate — machine-enforced)

- **Do NOT** re-run FCLR-STARTER-001, FCLR-001, FCLR-XSEC-001..008, FCLR-LIQ-OOS-FORECAST-001, FCLR-BOUNDED-TRIGGER-ONLY-LIQUIDATION-SOURCE, FCLR-SESSION-SYNTHESIS-01, or any Track A/B campaign (all terminal/superseded).
- **Do NOT** modify `.github/workflows` (protected control plane).
- **Do NOT** overwrite `research_state/research_protocol.md` (sealed legacy).
- **Do NOT** add any root-level `research_state/*.md` or `*.json` — root count is **499/500**; all new artifacts go under `research_state/session_<UTC>/`.
- **Do NOT** create empty/placeholder files or empty session directories.
- **Do NOT** threshold-shop or relax the 2% materiality floor after seeing outcomes.
- **Do NOT** conflate observed liquidations with modeled boundary breaches (Track B) or RV forecasts.

---

## FROZEN INPUTS (verified — do not re-derive, do not substitute)

- **Primary panel (FCLR-001):** `research_state/fclr011_recompute_panel_20261115T234700Z.parquet` — sha256 `41962f823e59de5989c7d854cb3180cad61a4cbc2f5f230133c41b321342c1f4`, 29,136 rows × 22 cols, 5 coins, 5,832 hours.
- **Combined liquidation panel:** `research_state/fclr_liq_combined_panel_20261115T181405Z.parquet` — sha256 `81a100d5d0625832bebabaabea13b786e15319577721cfe8507da5b779ec7f14`, 1,740,415 event rows, 15 coins, 2025-03-22 → 2026-10-31 UTC. Aggregate to hourly count + notional per coin.

---

## SINGLE HIGHEST-VALUE NEXT TASK (directive, non-avoidable)

**Execute FCLR-PANEL-FE-001 end-to-end** behind a fresh outcome-blind prereg and emit the full artifact set under a new `research_state/session_<UTC>/`. **Future agents cannot avoid doing heavy work:** the `FCLR-PANEL-FE-001` gate enforces it; the trigger-only idle is dead; the blocked "await external trigger" dead end is removed. If the panel-FE estimation genuinely cannot be run (e.g., a frozen panel fails to load), record that as blocker evidence with the exact error and stop cleanly — do not fabricate a placeholder.

---

**End of initial task message.** This mirrors the single durable handoff in `AGENT_HANDOFF.md` and supersedes all prior prose handoffs.