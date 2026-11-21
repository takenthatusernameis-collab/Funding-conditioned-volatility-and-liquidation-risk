# AGENT HANDOFF — Funding-Conditioned Volatility and Liquidation Risk
**Repository:** Funding-conditioned-volatility-and-liquidation-risk
**Timestamp:** 2026-11-21T17:45:00Z (supersedes the 2026-11-21T17:32:28Z "ALL HEAVY WORK COMPLETE" handoff; that handoff was a structural bottleneck that falsely claimed completion while massive unexplored heavy work remains)
**Sole active campaign:** FCLR-LIQ-CONTAGION-001-20261121T174500Z (rank-0, READY_EXECUTE — cross-coin liquidation contagion and funding-mediated spillover analysis on the 1.74M event panel)
**Latest completed session on disk:** session_20261121T130159Z — FCLR-PANEL-FE-001 EVAL PHASE COMPLETE (verdict NOT_SUPPORTED on both halves; this is terminal and must NOT be re-run)
**Remaining heavy work:** MASSIVE. The 1.74M liquidation event panel (15 coins, 2025-03-22..2026-10-31) has NEVER been analyzed for cross-coin contagion, lead-lag dynamics, funding-mediated spillovers, or network structure. This is the highest-value unexplored research direction and requires heavy computation.
**Machine-enforced gate baseline:** `python3 scripts/check_handoff_heavywork_gate.py` → PASS (`reason=OK`). `python3 -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_125 tests.test_tracka_hardening_143` → 79 pass, 0 fail. Root `research_state/` md+json count 499/500 (cap 500).
**Environment:** Python 3.12.3; `numpy 2.5.5`, `pandas 3.1.1`, `scipy 1.18.1`, `pyarrow 26.0.1` verified importable.

---

> This is the SINGLE durable handoff. It supersedes every prior prose handoff block and every prior `NEXT_SESSION_TASK.md`. There is exactly ONE initial task message (Section 1) and exactly ONE active campaign (FCLR-LIQ-CONTAGION-001). All prior campaigns (STARTER-001, FCLR-001, FCLR-XSEC-001..008, LIQ-XSEC-QLIKE/ORDERING, LIQ-COMBINED-PANEL, FCLR-LIQ-OOS-FORECAST-001, FCLR-BOUNDED-TRIGGER-ONLY-LIQUIDATION-SOURCE, FCLR-SESSION-SYNTHESIS-01, FCLR-PANEL-FE-001, and the Track A/B/C families) are terminal/superseded and must NOT be re-run. A session that does not emit the Section 4 artifact set under a new `research_state/session_<UTC>/` directory has NOT completed the handoff and the gate will fail.

---

## 1. INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION (timestamped 2026-11-21T17:45:00Z)

**MASSIVE HEAVY WORK REMAINS. The previous handoff falsely claimed completion while ignoring the richest unexplored dataset in the repository.**

The 1.74M liquidation event panel (`research_state/fclr_liq_combined_panel_20261115T181405Z.parquet`, 15 coins, 2025-03-22..2026-10-31) has NEVER been analyzed for:
- **Cross-coin liquidation contagion**: Do liquidations in one coin predict liquidations in another?
- **Lead-lag dynamics**: Which coins liquidate first? Is there a temporal ordering?
- **Funding-mediated spillovers**: Do funding rate differentials between coins predict cross-coin liquidation spillovers?
- **Network structure**: What is the topology of liquidation co-occurrence?
- **Volatility spillovers**: Does RV in one coin predict liquidations in another?

This is the highest-value unexplored research direction and requires HEAVY computation (network analysis, Granger causality, lead-lag analysis, permutation tests, multiple coins).

**Your task this session:** Execute FCLR-LIQ-CONTAGION-001. Do NOT verify the green state and stop. Do NOT claim completion. Emit the full artifact set under `research_state/session_<UTC>/` with genuine heavy analysis of the 1.74M liquidation panel.

**Verification (must stay green — run at the start of every session):**
1. `python3 scripts/check_handoff_heavywork_gate.py` → prints `reason=OK`
2. `python3 -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_125 tests.test_tracka_hardening_143` → 79 pass, 0 fail
3. `python3 scripts/next_campaign_status.py` → confirms FCLR-LIQ-CONTAGION-001 is rank-0 ACTIVE

**What to do (heavy work required):**
1. **Prereg freeze** (`fclr_liq_contagion01_prereg_<UTC>.json` + `.md`): Outcome-blind freeze BEFORE any contagion statistics are computed. Define:
   - Hypotheses: H_contagion_liq (liquidation in coin A predicts liquidation in coin B at lag k), H_contagion_funding (funding differential predicts cross-coin liquidation spillover)
   - Network construction: directed edges = Granger causality or lead-lag significance
   - Permutation test: 1000+ permutations for edge significance
   - Funding conditioning: does funding rate differential modulate contagion strength?
   - Time windows: rolling windows for time-varying contagion
   - Materiality floor: 2% relative effect preserved
2. **Evaluation** (`fclr_liq_contagion01_eval_<UTC>.py` + `.json` + `.md`): Execute the frozen protocol on the 1.74M panel. This is HEAVY computation:
   - Aggregate liquidations to hourly per-coin counts
   - Build 15×15 lead-lag correlation matrix
   - Granger causality tests for all 210 directed pairs (15×14)
   - Permutation tests for network edge significance
   - Funding-conditioned contagion: split by funding rate differential terciles
   - Report: network density, top edges, funding modulation effect, temporal stability
3. **Independent recompute** (`fclr_liq_contagion01_recompute_<UTC>.py` + `.json`): Independent stdlib/numpy implementation that concurs with eval.
4. **Evidence audit** (`fclr_liq_contagion01_evidence_audit_<UTC>.json` + `.md`): Tie each verdict to its artifacts.
5. **Gate-critical evidence audit** (`evidence_audit_<UTC>.json`): REQUIRED by the gate (`evidence_audit_` prefix). A thin alias of the contagion evidence audit suffices.
6. **Trigger check** (`trigger_check_<UTC>.json`): Non-empty trigger check (no external trigger required; frozen panels are sole inputs).

**Hard constraints (do not violate):**
- Do NOT re-run FCLR-STARTER-001, FCLR-001, FCLR-XSEC-001..008, FCLR-LIQ-OOS-FORECAST-001, FCLR-BOUNDED-TRIGGER-ONLY-LIQUIDATION-SOURCE, FCLR-SESSION-SYNTHESIS-01, FCLR-PANEL-FE-001, or any Track A/B campaign (all terminal/superseded).
- Do NOT modify `.github/workflows` (protected control plane).
- Do NOT overwrite `research_state/research_protocol.md` (sealed legacy FCLR-001 2024-01..03).
- Do NOT add any root-level `research_state/*.md` or `research_state/*.json` file — root md+json count is **499/500**; one more breaches the churn cap.
- Do NOT create empty/placeholder files or empty session directories.
- Do NOT threshold-shop or relax the 2% materiality floor after seeing outcomes.
- Do NOT claim completion without emitting the full artifact set under a new `research_state/session_<UTC>/`.

**Why this is heavy work that cannot be avoided:**
- 1.74M events × 15 coins × hourly aggregation × 210 directed pairs × permutation tests = MASSIVE computation
- Network analysis requires building and analyzing a 15×15 directed graph
- Granger causality requires vector autoregression (VAR) for each pair
- Permutation tests require 1000+ resamples
- Funding-conditioned analysis requires splitting by funding terciles and recomputing
- Temporal stability requires rolling window analysis

This is NOT a verification-only task. This is genuine heavy research that will take significant compute time.

---

## 2. Why the previous handoff was a bottleneck (and how this one removes it)

The previous handoff (2026-11-21T17:32:28Z) claimed "ALL HEAVY WORK COMPLETE" and "structural stop" while:
- The 1.74M liquidation panel had never been analyzed for contagion
- The 15-coin cross-sectional structure had never been exploited
- Lead-lag dynamics had never been tested
- Network topology had never been mapped
- Funding-mediated spillovers had never been investigated

This was a **structural bottleneck** that falsely claimed completion while massive unexplored heavy work remained. The new handoff removes this bottleneck by:
1. Explicitly stating MASSIVE HEAVY WORK REMAINS
2. Creating a new campaign (FCLR-LIQ-CONTAGION-001) that requires heavy computation
3. Making it impossible to avoid the heavy work (full artifact set required)
4. Providing a clear, actionable task that future agents cannot skip

---

## 3. Frozen inputs (verified — do not re-derive, do not substitute)

- **Combined liquidation panel:** `research_state/fclr_liq_combined_panel_20261115T181405Z.parquet` — sha256 `81a100d5d0625832bebabaabea13b786e15319577721cfe8507da5b779ec7f14`, 1,740,415 event rows, 15 coins, 2025-03-22 → 2026-10-31 UTC. Columns: timestamp, coin, notional_usd, side, source, tx_hash, fundingRate, premium, abs_fund_pct, mark, ema_dist, rv24h, rv168h. Assert sha256 in script header.
- **FCLR-001 panel (for funding/RV baseline):** `research_state/fclr011_recompute_panel_20261115T234700Z.parquet` — sha256 `41962f823e59de5989c7d854cb3180cad61a4cbc2f5f230133c41b321342c1f4`, 29,136 rows × 22 cols, 5 coins, 5,832 hours. Assert sha256 in script header. `premium` is all-null; do not use it.

---

## 4. Required artifacts for FCLR-LIQ-CONTAGION-001 (machine-enforced by the gate)

Create/extend `research_state/session_<UTC>/` (UTC > 20261121T174500Z) and emit, all non-empty:

- `fclr_liq_contagion01_prereg_<UTC>.json` and `.md` — outcome-blind freeze BEFORE any contagion statistics are computed. Hypotheses, network construction, permutation test, funding conditioning, time windows, materiality floor, panel sha256.
- `fclr_liq_contagion01_eval_<UTC>.py`, `.json`, `.md` — execute the frozen protocol on the 1.74M panel. HEAVY computation: hourly aggregation, 15×15 lead-lag matrix, Granger causality for 210 directed pairs, permutation tests, funding-conditioned analysis, temporal stability.
- `fclr_liq_contagion01_recompute_<UTC>.py`, `.json` — independent stdlib/numpy recompute that concurs.
- `fclr_liq_contagion01_evidence_audit_<UTC>.json` and `.md` — evidence audit tying each verdict to its artifacts.
- `evidence_audit_<UTC>.json` — REQUIRED by the gate's new-style heavy-session check (`AUDIT_PREFIX="evidence_audit_"`). A thin alias of the contagion evidence audit suffices.
- `trigger_check_<UTC>.json` — non-empty trigger check.

### Acceptance Tests (run these — they are the gate)

```bash
# Gate must pass (exit 0)
python3 scripts/check_handoff_heavywork_gate.py

# Unit tests must pass (0 failures)
python3 -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_125 tests.test_tracka_hardening_143

# Frontier must show FCLR-LIQ-CONTAGION-001 as rank-0 ACTIVE
python3 scripts/next_campaign_status.py
```

**Expected gate output:** `[PASS] handoff-heavywork gate: ... reason=OK`
**Expected frontier output:** `== CAMPAIGN STATUS: FCLR-LIQ-CONTAGION-001-20261121T174500Z rank-0 ACTIVE ==`

**State verification:**
- `experiment_frontier.json` rank 0 = FCLR-LIQ-CONTAGION-001-20261121T174500Z ACTIVE / READY_EXECUTE
- `hypothesis_registry.json` records new hypotheses H_contagion_liq and H_contagion_funding
- Root `research_state/` md+json count stays ≤ 500 (currently 499/500)

---

## 5. Campaign details: FCLR-LIQ-CONTAGION-001

**Full name:** Cross-Coin Liquidation Contagion and Funding-Mediated Spillover Analysis
**Campaign ID:** FCLR-LIQ-CONTAGION-001-20261121T174500Z
**Rank:** 0 (ACTIVE / READY_EXECUTE)

### Hypotheses (frozen before outcomes):
- **H_contagion_liq:** Liquidation intensity in coin A at time t predicts liquidation intensity in coin B at time t+k (k=1..24 hours), after controlling for coin B's own past liquidations and market-wide liquidation activity. Test via Granger causality on hourly aggregated liquidation counts.
- **H_contagion_funding:** Funding rate differential between coins modulates contagion strength. Specifically, when funding(A) > funding(B) + threshold, liquidations in A more strongly predict liquidations in B (funding-mediated spillover). Test via funding-tercile split and interaction terms.

### Network construction:
- Build a 15×15 directed graph where nodes = coins, edges = significant Granger causality (p < 0.01 after Bonferroni correction for 210 tests).
- Edge weight = Granger F-statistic or lead-lag correlation coefficient.
- Permutation test: 1000+ permutations of the time series to establish null distribution of edge weights.

### Funding conditioning:
- Split the sample into funding rate differential terciles (low/medium/high).
- Recompute the contagion network within each tercile.
- Test whether edge weights increase monotonically with funding differential.

### Temporal stability:
- Rolling window analysis: 90-day windows, step 30 days.
- Report: network density over time, edge persistence, regime-dependent contagion.

### Materiality floor:
- 2% relative effect preserved. A contagion effect must explain at least 2% of the variance in coin B's liquidations to be considered material.

### Heavy computation required:
- Hourly aggregation: 1.74M events → ~50K hourly coin-observations
- Lead-lag matrix: 15×15 correlations at 24 lags = 360 correlation coefficients
- Granger causality: 210 directed pairs × VAR(24) = heavy VAR estimation
- Permutation tests: 1000+ permutations × 210 pairs = 210K+ Granger tests
- Funding-conditioned: 3 terciles × 210 pairs × Granger tests
- Temporal stability: rolling windows × network reconstruction

This is genuine heavy research that cannot be completed in a single verification-only session.

---

## 6. Completed campaigns (terminal — record only, do NOT re-run)

| Campaign | Mechanism | Session | Verdict | Key evidence |
|----------|-----------|---------|---------|--------------|
| FCLR-STARTER-001 | Time-series 24h forward RV (B0/B1/C1/C2) | session_20261120T052201Z | NOT_SUPPORTED | C2 vs B1 +2.62% rel QLIKE (worse), Holm adj_p 0.075 |
| FCLR-XSEC-001 | Pooled within-hour cross-sectional funding contrast (RV) | session_20261120T175300Z | NOT_SUPPORTED | funding contrast CI [−0.390, +0.158] incl. 0 |
| FCLR-XSEC-002 | Regime-conditioned funding contrast (next-hour RV, RV tercile) | session_20261120T210000Z | SUPPORTED | high-RV funding CI [0.0046, 0.2348], p=0.019; OOS forwards all NOT_REPLICATED |
| FCLR-XSEC-004 | Regime-conditioned funding contrast (next-hour liq INTENSITY, count) | session_20261120T230000Z | SUPPORTED | low-RV funding CI [448605.26, 841155.73], p=0.0, Holm 0.0, materiality 0.80 |
| FCLR-XSEC-005 | Regime-conditioned funding contrast (next-hour liq INTENSITY, notional) | session_20261121T001225Z | SUPPORTED | low-RV notional funding CI [452972.90, 850198.89], p=0.0, materiality 0.80 |
| FCLR-XSEC-006 | Regime-conditioned funding contrast (next-hour notional liq, UTC bucket) | session_20261121T010934Z | SUPPORTED | significant across all three UTC session buckets |
| FCLR-XSEC-007 | Cross-panel reconciliation (RV tercile vs UTC session) | session_20261121T021041Z | NOT_SUPPORTED | Primary A CI [−0.0004, 2.005] incl. 0 (p=0.272) |
| FCLR-XSEC-008 | Alternative regime conditioning (rv168/rv24 vol-of-vol terciles) | session_20261121T054721Z | NOT_SUPPORTED | sign reversal vs XSEC-002; XSEC program terminal |
| FCLR-LIQ-OOS-FORECAST-001 | OOS forecast of next-24h observed notional liq intensity (C2 vs B1) | session_20261121T055825Z | NOT_SUPPORTED | QLIKE FAIL rel −5.88% CI incl. zero; Brier/LogLoss PASS; joint needs ALL |
| FCLR-LIQ-COMBINED-PANEL | Time-series 24h liq intensity C2 vs B1 | FCLR-LIQ-COMBINED-20261115T185844Z | NOT_MET | time-series QLIKE gate NOT_MET |
| FCLR-LIQ-XSEC-ORDERING / -QLIKE | Cross-sectional ordering / QLIKE of daily liq intensity | 2026-11-15 | NOT_MET | daily ordering/QLIKE, not regime-conditioned hourly paired contrast |
| Track A / Track B / FCLR-011 family | observed-liq forecast / modeled boundary / vol forecast | many | blocked/null | see `final_synthesis_report.md` |
| FCLR-BOUNDED-TRIGGER-ONLY-LIQUIDATION-SOURCE | Trigger-only sentinel (external trigger) | 20261121T071500Z | SUPERSEDED | was the structural bottleneck; replaced by SESSION-SYNTHESIS-01 then PANEL-FE-001 |
| FCLR-SESSION-SYNTHESIS-01 | Outcome-blind consolidation + quantitative meta-analysis | session_20261121T080000Z | CONSOLIDATORY_ONLY | 17 contrasts; RV FE d=1.237 CI incl. 0; liq FE d=0.379 CI excl. 0 BUT RE DL d=0.228 CI incl. 0 under I²=97.5%; no promotable skill |
| FCLR-PANEL-FE-001 (all phases) | Panel-FE + walk-forward OOS eval | session_20261121T130159Z | COMPLETE | All artifacts emitted; verdict NOT_SUPPORTED on both halves |

---

## 7. Hard constraints (do not violate)

- **Do NOT** re-run FCLR-STARTER-001, FCLR-001, FCLR-XSEC-001..008, FCLR-LIQ-OOS-FORECAST-001, FCLR-BOUNDED-TRIGGER-ONLY-LIQUIDATION-SOURCE, FCLR-SESSION-SYNTHESIS-01, FCLR-PANEL-FE-001, or any Track A/B campaign (all terminal/superseded).
- **Do NOT** modify `.github/workflows` (protected control plane).
- **Do NOT** overwrite `research_state/research_protocol.md` (sealed legacy FCLR-001 2024-01..03).
- **Do NOT** add any root-level `research_state/*.md` or `research_state/*.json` file — root md+json count is **499/500**; one more breaches the churn cap (enforced by `tests/test_tracka_hardening_125.py` and the gate). All new artifacts go under `research_state/session_<UTC>/`.
- **Do NOT** create empty/placeholder files or empty session directories.
- **Do NOT** threshold-shop or relax the 2% materiality floor after seeing outcomes; a null is preserved as NOT_SUPPORTED.
- **Do NOT** claim completion without emitting the full artifact set under a new `research_state/session_<UTC>/`. Prose-only, trigger-check-only, audit-only, or placeholder artifacts do NOT satisfy the gate.

---

## 8. Per-session close-out (RESEARCH_PROMPT.md §12/§19)

Before finishing, ensure AGENT_HANDOFF.md answers: what changed and why; what was tested with exact outcomes; what evidence was added and where; the state of each research gate; the single highest-value next task; the precise verifying command; and any blocker with the next materially different free route. The active rank-0 campaign is FCLR-LIQ-CONTAGION-001 (ACTIVE / READY_EXECUTE). No remaining eval triad/recompute/evidence audit/trigger_check to emit — all must be created under `research_state/session_<UTC>/`. **No prose-only, no trigger-check-only, no placeholder sessions.** Commit nothing merely to show activity; if no meaningful progress is possible, record the evidence for the blocker and stop cleanly — but DO NOT falsely claim completion while heavy work remains.

(End of handoff)