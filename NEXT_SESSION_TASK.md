# INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION
**Repository:** Funding-conditioned-volatility-and-liquidation-risk
**Timestamp:** 2026-11-21T08:00:00Z
**Sole active campaign:** FCLR-SESSION-SYNTHESIS-01-20261121T080000Z (rank-0, READY_EXECUTE/ACTIVE, verdict CONSOLIDATORY_ONLY — executed; outcome-blind evidence-consolidation + quantitative meta-analysis over 17 terminal funding-conditioning contrasts complete)

---

## WHY THIS IS THE FOCUS (repository-name priority + bottleneck removal)

The repository name **Funding-conditioned-volatility-and-liquidation-risk** defines two scientific halves reconciled by funding conditioning:
- **(a) Does the funding rate condition volatility (RV)?**
- **(b) Does it condition liquidation risk?**

Both halves are now **terminal on the verified frozen panels**. The prior rank-0 campaign (`FCLR-BOUNDED-TRIGGER-ONLY-LIQUIDATION-SOURCE-20261121T071500Z`, TRIGGER_ONLY) was gated on an external `NEW_OBSERVED_LIQUIDATION_SOURCE` trigger that **cannot fire inside this closed, frozen-data environment**. That trigger gate was the structural bottleneck: future agents would idle waiting for a signal the frozen panel cannot produce.

**This bottleneck has been removed** by executing the heavy consolidation + quantitative meta-analysis campaign `FCLR-SESSION-SYNTHESIS-01` in session `session_20261121T080000Z/`. The consolidation is now COMPLETE.

---

## WHAT WAS EXECUTED (heavy, non-deferrable — already done)

`FCLR-SESSION-SYNTHESIS-01-20261121T080000Z` in `research_state/session_20261121T080000Z/`:

- **Protocol freeze** (pre-outcomes, `outcome_data_inspected_before_freeze=false`): outcome-blind evidence-consolidation + meta-analysis design; inverse-variance fixed-effect + DerSimonian-Laird random-effects; Cochran Q + I²; regime-stratified (RV/liq/joint); 2% materiality floor preserved.
- **Program synthesis report** (json+md): every terminal campaign verdict with exact CIs/p-values/panels (FCLR-STARTER-001, XSEC-001..008, LIQ-OOS-FORECAST-001, LIQ-COMBINED-PANEL, LIQ-XSEC-ORDERING/QLIKE, Track A, Track B).
- **Frontier exhaustion audit** (json+md): per-domain blockage from `next_campaign_status.py` (NO_FEASIBLE_3_BLOCK_DESIGN_IN_ANY_DOMAIN).
- **Negative results preservation** (json): all null/inconclusive outcomes with mechanistic explanations.
- **Quantitative meta-analysis** (py+json+md): 17 terminal funding-conditioning contrasts across FCLR-XSEC-002/004/005/006 on both frozen panels (sha256 asserted). **Finding:** RV fixed-effect pooled d=1.237 (CI incl. zero); liquidation fixed-effect pooled d=0.379 (CI excl. zero) BUT random-effects DL pooled d=0.228 (CI incl. zero) under I²=97.5% heterogeneity; joint random-effects CI incl. zero.
- **Independent stdlib recompute** (py+json): concurs (rv_match=true, liq_match=true, recompute_concurs=true).
- **Evidence audit** (json+md) + **non-empty trigger_check** (json): all 20 acceptance checks PASS.

**Synthesis verdict: CONSOLIDATORY_ONLY.** Cross-sectional funding-conditioning associations are statistically detectable in specific regimes (RV high-RV; liquidation low-RV + UTC buckets) but **not homogeneous** (I²≈97%) and **not robust under random effects** (pooled CI includes zero). Combined with FAILED out-of-sample forward/forecast gates (FCLR-LIQ-OOS-FORECAST-001 QLIKE FAIL; all RV forward confirmations NOT_REPLICATED), the consolidated evidence does **not** support a promotable funding-conditioned forecast skill. No terminal hypothesis was promoted; every honest terminal verdict is carried forward unchanged.

---

## NEXT FOCUS FOR THE FUTURE AGENT (rank-0 is now COMPLETE for this consolidation)

**The consolidation campaign is EXECUTED.** The frozen-data frontier is genuinely exhausted for new 3-block confirmatory designs (`next_campaign_status.py` → NO_FEASIBLE_3_BLOCK_DESIGN_IN_ANY_DOMAIN).

### THE ONLY ADMISSIBLE HEAVY WORK PATHS (machine-enforced by FCLR-SESSION-SYNTHESIS-01 gate):

1. **AWAIT `NEW_OBSERVED_LIQUIDATION_SOURCE` TRIGGER** — External, not controllable from inside this session. Reopening the liquidation-risk OOS hypothesis **requires** a new observed-liquidation data source beyond the frozen panels. Until that trigger fires, no liquidation OOS campaign is admissible.

2. **EXECUTE A MATERIALLY DIFFERENT FREE-DATA ROUTE** — A new instrument set with adequate contiguous funding+liquidation coverage that `next_campaign_status.py` confirms as feasible, executed behind a **fresh outcome-blind prereg** frozen pre-outcomes. This is the ONLY path that future agents can execute to make progress without waiting for an external trigger.

### MANDATORY REQUIREMENTS FOR ANY NEXT HEAVY SESSION:

If executing a materially different free-data route, the session **MUST** create a new `research_state/session_<UTC>/` directory and emit the full outcome-blind triad appropriate to that route:
- Protocol freeze (pre-outcomes, `outcome_data_inspected_before_freeze=false`)
- Evaluation triad (source/result/report: .py + .json + .md)
- Independent stdlib recompute (py+json)
- Evidence audit (json+md)
- Non-empty trigger_check (json)

**The `FCLR-SESSION-SYNTHESIS-01` gate in `scripts/check_handoff_heavywork_gate.py` binds the exact consolidation artifact set for any post-20261121T080000Z session that claims this campaign family.** Prose-only, trigger-check-only, or placeholder artifacts do NOT satisfy the gate.

---

## ACCEPTANCE TESTS (run these — they are the gate)

```bash
# Gate must pass (exit 0)
python3 scripts/check_handoff_heavywork_gate.py

# Unit tests must pass (0 failures)
python3 -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_125
```

**Expected gate output:** `[PASS] handoff-heavywork gate: ... reason=OK`

**State verification:**
- `experiment_frontier.json` rank 0 = FCLR-SESSION-SYNTHESIS-01 READY_EXECUTE/ACTIVE with all others SUPERSEDED
- Rank-0 `next_unfinished_task` non-empty and points to the free-data route requirement
- `hypothesis_registry.json` records the consolidation verdict CONSOLIDATORY_ONLY
- No liquidation/RV outcomes inspected before any protocol freeze
- Root `research_state/` md+json count stays ≤ 500 (currently 499/500)

---

## HARD CONSTRAINTS (do not violate — machine-enforced)

- **Do NOT** re-run FCLR-STARTER-001, FCLR-001, FCLR-XSEC-001..008, FCLR-LIQ-OOS-FORECAST-001, FCLR-BOUNDED-TRIGGER-ONLY-LIQUIDATION-SOURCE, FCLR-SESSION-SYNTHESIS-01, or any Track A/B campaign (all terminal/superseded).
- **Do NOT** modify `.github/workflows` (protected control plane).
- **Do NOT** overwrite `research_state/research_protocol.md` (sealed legacy FCLR-001 2024-01..03).
- **Do NOT** add any root-level `research_state/*.md` or `research_state/*.json` file — root md+json count is **499/500**; one more breaches the churn cap (enforced by `tests/test_tracka_hardening_125.py` and the gate). All new artifacts go under `research_state/session_<UTC>/`.
- **Do NOT** create empty/placeholder files or empty session directories.
- **Do NOT** threshold-shop or relax the 2% materiality floor after seeing outcomes; a null is preserved as NOT_SUPPORTED.
- **Do NOT** conflate observed liquidations with modeled boundary breaches (Track B) or with RV forecasts — keep the track separation explicit in every artifact.
- **Reopening the liquidation-risk OOS hypothesis requires `NEW_OBSERVED_LIQUIDATION_SOURCE`.** Until that trigger fires, only a materially different free-data route is admissible.

---

## FROZEN INPUTS (verified — do not re-derive, do not substitute)

- **Primary panel (FCLR-001):** `research_state/fclr011_recompute_panel_20261115T234700Z.parquet` — sha256 `41962f823e59de5989c7d854cb3180cad61a4cbc2f5f230133c41b321342c1f4`, 29,136 rows × 22 cols, 5 coins, 5,832 hours. Assert the sha256 in the script header.
- **Combined liquidation panel:** `research_state/fclr_liq_combined_panel_20261115T181405Z.parquet` — sha256 `81a100d5d0625832bebabaabea13b786e15319577721cfe8507da5b779ec7f14`, 1,740,415 rows, 15 coins, 10,052 hourly buckets, 2025-03-22 19:00 → 2026-10-31 22:00 UTC, zero-null features.

---

## SINGLE HIGHEST-VALUE NEXT TASK (directive, non-avoidable)

**Execute a materially different free-data route** behind a fresh outcome-blind prereg, OR **record the blocker evidence** for `NEW_OBSERVED_LIQUIDATION_SOURCE` and stop cleanly with the next valid independent task executed.

**Future agents cannot avoid doing heavy work.** The gate enforces it. The trigger-only idle is dead. The only way forward is:
1. Find a new free data source (instrument set) with adequate contiguous funding+liquidation coverage
2. Run `next_campaign_status.py` to confirm feasibility
3. Freeze a new prereg pre-outcomes
4. Execute the full evaluation triad + independent recompute + evidence audit + trigger_check
5. Emit all artifacts under a new `research_state/session_<UTC>/`

If no such free-data route exists, the session must emit the blocker evidence in the handoff and stop cleanly — **no prose-only, no trigger-check-only, no placeholder sessions.**

---

**End of initial task message.** This is the single durable handoff for the next agentic work session. It supersedes all prior prose handoffs.