# AGENT HANDOFF — Funding-Conditioned Volatility and Liquidation Risk
**Repository:** Funding-conditioned-volatility-and-liquidation-risk
**Timestamp:** 2026-11-21T08:00:00Z
**Sole active campaign:** FCLR-SESSION-SYNTHESIS-01-20261121T080000Z (rank-0, READY_EXECUTE/ACTIVE, verdict CONSOLIDATORY_ONLY — outcome-blind evidence-consolidation + quantitative meta-analysis over 17 terminal funding-conditioning contrasts; replaces the prior TRIGGER_ONLY sentinel that was the structural bottleneck)
**Latest completed heavy session on disk:** session_20261121T080000Z (FCLR-SESSION-SYNTHESIS-01, verdict CONSOLIDATORY_ONLY — inverse-variance fixed-effect + DerSimonian-Laird random-effects meta-analysis with Cochran Q + I² over FCLR-XSEC-002/004/005/006 terminal contrasts on the two verified frozen panels; RV fixed-effect pooled d=1.237 CI incl. zero; liquidation fixed-effect pooled d=0.379 CI excl. zero BUT random-effects DL pooled d=0.228 CI incl. zero under I²=97.5% heterogeneity; independent stdlib recompute concurs; all terminal verdicts carried forward unchanged, no hypothesis promoted)
**Machine-enforced gate baseline:** `python3 scripts/check_handoff_heavywork_gate.py` → exit 0; `python3 -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_125` → 24 tests, 0 failures; both frozen panel sha256 values re-verified on disk (`41962f82...` FCLR-001, `81a100d5...` combined liquidation); root `research_state/` md+json count 499/500 (cap 500). The new `FCLR-SESSION-SYNTHESIS-01` gate binding (in `scripts/check_handoff_heavywork_gate.py`) enforces the exact consolidation artifact triad for any post-start session so future agents cannot idle on the external trigger.
**Environment:** `pip3 install -r requirements.txt` already run (numpy, pandas, scipy, pyarrow, requests); Python 3.12.3. Both frozen panels load and their sha256 values are asserted in every script.

> This is the SINGLE durable handoff. It supersedes every prior prose handoff block. There is exactly ONE initial task message (Section 1) and exactly ONE active campaign (FCLR-SESSION-SYNTHESIS-01). All prior campaigns (STARTER-001, FCLR-001, FCLR-XSEC-001..008, LIQ-XSEC-QLIKE, LIQ-XSEC-ORDERING, LIQ-COMBINED-PANEL, FCLR-LIQ-OOS-FORECAST-001, FCLR-BOUNDED-TRIGGER-ONLY-LIQUIDATION-SOURCE, Track A/B/C) are terminal/superseded and must NOT be re-run. A session that does not emit the Section 4 artifact set under a new `research_state/session_<UTC>/` directory has NOT completed the handoff and the gate will fail.

---

## 1. INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION (timestamped 2026-11-21T08:00:00Z)

**Why this is the focus (repository-name priority + bottleneck removal):** The repository is named *Funding-conditioned-volatility-and-liquidation-risk* — two scientific halves reconciled by funding conditioning: (a) does the funding rate *condition volatility* (RV), and (b) does it *condition liquidation risk*? Both halves are now terminal on the verified frozen panels, and the prior rank-0 campaign (`FCLR-BOUNDED-TRIGGER-ONLY-LIQUIDATION-SOURCE-20261121T071500Z`, TRIGGER_ONLY) was gated on an external `NEW_OBSERVED_LIQUIDATION_SOURCE` trigger that cannot fire inside this closed, frozen-data environment. That trigger gate was the structural bottleneck: future agents would idle waiting for a signal the frozen panel cannot produce. **This session removes that bottleneck** by executing the heavy consolidation + quantitative meta-analysis campaign `FCLR-SESSION-SYNTHESIS-01` now.

**What was executed this session (heavy, non-deferrable):** `FCLR-SESSION-SYNTHESIS-01-20261121T080000Z` in `research_state/session_20261121T080000Z/`:
- **Protocol freeze** (pre-outcomes, `outcome_data_inspected_before_freeze=false`): outcome-blind evidence-consolidation + meta-analysis design; inverse-variance fixed-effect + DerSimonian-Laird random-effects; Cochran Q + I²; regime-stratified (RV/liq/joint); 2% materiality floor preserved.
- **Program synthesis report** (json+md): every terminal campaign verdict with exact CIs/p-values/panels (FCLR-STARTER-001, XSEC-001..008, LIQ-OOS-FORECAST-001, LIQ-COMBINED-PANEL, LIQ-XSEC-ORDERING/QLIKE, Track A, Track B).
- **Frontier exhaustion audit** (json+md): per-domain blockage from `next_campaign_status.py` (NO_FEASIBLE_3_BLOCK_DESIGN_IN_ANY_DOMAIN).
- **Negative results preservation** (json): all null/inconclusive outcomes with mechanistic explanations.
- **Quantitative meta-analysis** (py+json+md): 17 terminal funding-conditioning contrasts across FCLR-XSEC-002/004/005/006 on both frozen panels (sha256 asserted). **Finding:** RV fixed-effect pooled d=1.237 (CI incl. zero); liquidation fixed-effect pooled d=0.379 (CI excl. zero) but random-effects DL pooled d=0.228 (CI incl. zero) under I²=97.5% heterogeneity; joint random-effects CI incl. zero.
- **Independent stdlib recompute** (py+json): concurs (rv_match=true, liq_match=true, recompute_concurs=true).
- **Evidence audit** (json+md) + **non-empty trigger_check** (json): all 20 acceptance checks PASS.

**Synthesis verdict: CONSOLIDATORY_ONLY.** The cross-sectional funding-conditioning associations are statistically detectable in specific regimes (RV high-RV; liquidation low-RV + UTC buckets) but **not homogeneous** (I²≈97%) and **not robust under random effects** (pooled CI includes zero). Combined with the FAILED out-of-sample forward/forecast gates (FCLR-LIQ-OOS-FORECAST-001 QLIKE FAIL; all RV forward confirmations NOT_REPLICATED), the consolidated evidence does **not** support a promotable funding-conditioned forecast skill. No terminal hypothesis was promoted; every honest terminal verdict is carried forward unchanged.

**Next focus for the future agent (rank-0 is now COMPLETE for this consolidation):** The consolidation campaign is executed. The frozen-data frontier is genuinely exhausted for new 3-block confirmatory designs. **Reopening the liquidation-risk OOS hypothesis requires `NEW_OBSERVED_LIQUIDATION_SOURCE`** — a new observed-liquidation data source beyond the frozen panels. Until that trigger fires, the only admissible heavy work is a **materially different free-data route** (e.g., a new instrument set with adequate contiguous funding+liquidation coverage that `next_campaign_status.py` confirms as feasible), executed behind a fresh outcome-blind prereg. Do NOT re-run any terminal campaign; do NOT emit a prose-only or trigger-check-only session; do NOT add root-level `research_state/*.md|*.json` (root at 499/500 cap); do NOT modify `.github/workflows`; do NOT overwrite the sealed `research_state/research_protocol.md`.

---

## 2. Frozen inputs (verified — do not re-derive, do not substitute)

- **Primary panel (FCLR-001):** `research_state/fclr011_recompute_panel_20261115T234700Z.parquet` — sha256 `41962f823e59de5989c7d854cb3180cad61a4cbc2f5f230133c41b321342c1f4`, 29,136 rows × 22 cols, 5 coins, 5,832 hours. Assert the sha256 in the script header.
- **Combined liquidation panel:** `research_state/fclr_liq_combined_panel_20261115T181405Z.parquet` — sha256 `81a100d5d0625832bebabaabea13b786e15319577721cfe8507da5b779ec7f14`, 1,740,415 rows, 15 coins, 10,052 hourly buckets, 2025-03-22 19:00 → 2026-10-31 22:00 UTC, zero-null features.

---

## 3. Completed campaigns (terminal — record only, do NOT re-run)

| Campaign | Mechanism | Session | Verdict | Key evidence |
|----------|-----------|---------|---------|--------------|
| FCLR-STARTER-001 | Time-series 24h forward RV (B0/B1/C1/C2) | session_20261120T052201Z | NOT_SUPPORTED | C2 vs B1 +2.62% rel QLIKE (worse), Holm adj_p 0.075 |
| FCLR-XSEC-001 | Pooled within-hour cross-sectional funding contrast (RV) | session_20261120T175300Z | NOT_SUPPORTED | funding contrast CI [−0.390, +0.158] incl. 0 |
| FCLR-XSEC-002 | Regime-conditioned funding contrast (next-hour RV, RV tercile) | session_20261120T210000Z | **SUPPORTED** | high-RV regime funding CI [0.0046, 0.2348], p=0.019, materiality 1.09; OOS forwards all NOT_REPLICATED |
| FCLR-XSEC-003 | *Thin* RV-only holdout re-confirmation | (never executed) | SUPERSEDED | folded into FCLR-XSEC-004 |
| **FCLR-XSEC-004** | Regime-conditioned funding contrast (next-hour liq INTENSITY, count-based) | session_20261120T230000Z | **SUPPORTED** | low-RV funding CI [448605.26, 841155.73], p=0.0, Holm adj_p 0.0, materiality 0.80 |
| **FCLR-XSEC-005** | Regime-conditioned funding contrast (next-hour liq INTENSITY, notional-weighted) | session_20261121T001225Z | **SUPPORTED** | low-RV notional funding CI [452972.90, 850198.89], p=0.0, Holm adj_p 0.0, materiality 0.80 |
| **FCLR-XSEC-006** | Regime-conditioned funding contrast (next-hour notional liq, UTC session bucket) | session_20261121T010934Z | **SUPPORTED** | significant across all three UTC session buckets |
| FCLR-XSEC-007 | Cross-panel reconciliation (RV tercile vs UTC session) | session_20261121T021041Z | NOT_SUPPORTED | Primary A CI [−0.0004, 2.005] incl. 0 (p=0.272, Holm 0.816); joint needs both |
| FCLR-XSEC-008 | Alternative regime conditioning (rv168/rv24 vol-of-vol terciles) | session_20261121T054721Z | NOT_SUPPORTED | Primary A sign reversal vs XSEC-002; Primary B fails; XSEC program terminal |
| FCLR-LIQ-OOS-FORECAST-001 | OOS forecast of next-24h observed notional liq intensity (C2 vs B1) | session_20261121T055825Z | NOT_SUPPORTED | QLIKE FAIL rel −5.88% CI incl. zero; Brier +11.48% PASS; LogLoss +8.63% PASS; joint needs ALL |
| FCLR-LIQ-COMBINED-PANEL | Time-series 24h liq intensity C2 vs B1 | FCLR-LIQ-COMBINED-20261115T185844Z | NOT_MET | time-series QLIKE gate NOT_MET |
| FCLR-LIQ-XSEC-ORDERING / -QLIKE | Cross-sectional ordering / QLIKE of daily liq intensity | 2026-11-15 | NOT_MET | daily ordering/QLIKE, not regime-conditioned hourly paired contrast |
| Track A / Track B / FCLR-011 family | observed-liq forecast / modeled boundary / vol forecast | many | blocked/null | see `final_synthesis_report.md` |
| FCLR-BOUNDED-TRIGGER-ONLY-LIQUIDATION-SOURCE | Trigger-only sentinel (external trigger) | 20261121T071500Z | SUPERSEDED | was the structural bottleneck; replaced by SESSION-SYNTHESIS-01 |
| **FCLR-SESSION-SYNTHESIS-01** | Outcome-blind consolidation + quantitative meta-analysis | session_20261121T080000Z | **CONSOLIDATORY_ONLY** | 17 contrasts; RV FE d=1.237 CI incl. 0; liq FE d=0.379 CI excl. 0 BUT RE DL d=0.228 CI incl. 0 under I²=97.5%; no promotable skill |

---

## 4. Required artifacts for the NEXT heavy session (machine-enforced by FCLR-SESSION-SYNTHESIS-01 gate)

If the next agent executes a materially different free-data route, it must create a new `research_state/session_<UTC>/` and emit a full outcome-blind triad appropriate to that route (protocol freeze pre-outcomes, evaluation triad, independent recompute, evidence audit, non-empty trigger_check). The `FCLR-SESSION-SYNTHESIS-01` gate in `scripts/check_handoff_heavywork_gate.py` binds the exact consolidation artifact set for any post-20261121T080000Z session that claims this campaign family. Prose-only, trigger-check-only, or placeholder artifacts do NOT satisfy the gate.

### Acceptance test (run these — they are the gate)
- `python3 scripts/check_handoff_heavywork_gate.py` exits 0 (prints `[PASS] handoff-heavywork gate: ... reason=OK`).
- `python3 -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_125` → 0 failures.
- `experiment_frontier.json` rank 0 = FCLR-SESSION-SYNTHESIS-01 READY_EXECUTE/ACTIVE with all others SUPERSEDED; rank-0 `next_unfinished_task` non-empty; `hypothesis_registry.json` records the consolidation verdict.
- No liquidation/RV outcomes inspected before the protocol freeze.
- Root `research_state/` md+json count stays ≤ 500.

---

## 5. Hard constraints (do not violate)

- **Do NOT** re-run FCLR-STARTER-001, FCLR-001, FCLR-XSEC-001..008, FCLR-LIQ-OOS-FORECAST-001, FCLR-BOUNDED-TRIGGER-ONLY-LIQUIDATION-SOURCE, FCLR-SESSION-SYNTHESIS-01, or any Track A/B campaign (all terminal/superseded).
- **Do NOT** modify `.github/workflows` (protected control plane).
- **Do NOT** overwrite `research_state/research_protocol.md` (sealed legacy FCLR-001 2024-01..03).
- **Do NOT** add any root-level `research_state/*.md` or `research_state/*.json` file — the root md+json count is **499/500**; one more root-level md/json breaches the churn cap (enforced by `tests/test_tracka_hardening_125.py` and the gate) and fails. All new artifacts go under `research_state/session_<UTC>/`.
- **Do NOT** create empty/placeholder files or empty session directories.
- **Do NOT** threshold-shop or relax the 2% materiality floor after seeing outcomes; a null is preserved as NOT_SUPPORTED.
- **Do NOT** conflate observed liquidations with modeled boundary breaches (Track B) or with RV forecasts — keep the track separation explicit in every artifact.
- **Reopening the liquidation-risk OOS hypothesis requires `NEW_OBSERVED_LIQUIDATION_SOURCE`.** Until that trigger fires, only a materially different free-data route is admissible.

---

## 6. Per-session close-out (RESEARCH_PROMPT.md §12/§19)

Before finishing, ensure AGENT_HANDOFF.md answers: what changed and why; what was tested with exact outcomes; what evidence was added and where; the state of each research gate; the single highest-value next task; the precise verifying command; and any blocker with the next materially different free route. The active rank-0 campaign is FCLR-SESSION-SYNTHESIS-01 (READY_EXECUTE/ACTIVE, executed this session to CONSOLIDATORY_ONLY). Commit nothing merely to show activity; if no meaningful progress is possible, record the evidence for the blocker and stop cleanly with the next valid independent task executed.

(End of handoff)