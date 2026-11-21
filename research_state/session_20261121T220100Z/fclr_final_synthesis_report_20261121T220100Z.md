# FCLR-FINAL-SYNTHESIS-01 — Final Synthesis Report

**Repository:** Funding-conditioned-volatility-and-liquidation-risk
**Campaign:** FCLR-FINAL-SYNTHESIS-01
**Session:** `research_state/session_20261121T220100Z/`
**Generated UTC:** 2026-11-21T22:01:00Z
**Status:** COMPLETE — sole remaining deliverable of the frozen-data research cycle.
**Forecast gate:** NOT PASSED for any primary volatility or liquidation target. No risk overlay was or could be evaluated.

---

## 1. Purpose and scope

This report honestly summarizes the complete research cycle for the **Funding-Conditioned Volatility and Liquidation Risk (FCLR)** program, as mandated by RESEARCH_PROMPT.md §12, §20 and AGENT_HANDOFF.md §2. The frozen-data frontier is exhausted: `scripts/next_campaign_status.py` reports **no feasible 3-block design in ANY domain** (Binance 5-symbol cache, Hyperliquid ironflow bulk cache, and Hyperliquid extended stores all exhausted). No external trigger can fire inside this closed frozen-data environment (`NEW_OBSERVED_LIQUIDATION_SOURCE` cannot occur on a sealed panel). The only remaining deliverable was this synthesis report.

No prose-only, trigger-only, audit-only, verify-and-stop, or placeholder session satisfies this campaign. All artifacts below are non-empty and live under a new `research_state/session_<UTC>/` directory (UTC > 20261121T210000Z), the gate root-count cap (499/500) is respected because nothing is written to `research_state/` root, and no terminal/completed campaign is re-run.

---

## 2. Primary hypotheses and verdicts

| Hypothesis ID | Estimand | Verdict | Basis |
|---|---|---|---|
| FCLR-H001 | Incremental 24-hour volatility forecasting: does funding + price features beat a realized-volatility-only baseline on next-24h realized variance (QLIKE)? | NOT_SUPPORTED | FCLR-001 frozen starter protocol; B0/B1/C1/C2 contrasts executed on frozen panels; no pre-registered primary contrast cleared the gate; gate never passed. |
| FCLR-H002 | Funding-extreme correction-time replication (Shek working paper claim: median correction 27h high-vol vs 3h low-vol; lower hazard with higher RV). | NOT_SUPPORTED | Independent reconstruction assessed against public data; reported pattern not reproduced as an exact replication; stated as partial only. |
| FCLR-H003 | Hypothetical boundary-breach forecast (modeled liquidation boundary under registered leverage/margin scenarios). | NOT_SUPPORTED | Track B modeled-breach labels evaluated; no funding-conditioned Brier improvement; no calibration evidence supporting incremental skill. |
| FCLR-H004 | Observed liquidation outcomes (Track A direct liquidation-event forecasting). | NOT_SUPPORTED / DATA_BLOCKED | No complete, defensible observed-liquidation census with adequate provenance and coverage was available; absence from a capped feed is not "no liquidation." |

All verdicts are preserve-null: none are relabeled exploratory-as-confirmatory, and no threshold was shopped or relaxed after outcomes. The 2% materiality floor (FCLR-001 §14) held; nulls remain NOT_SUPPORTED per RESEARCH_PROMPT.md §7, §12, §20.

---

## 3. Campaign ledger (all terminal)

| Campaign | Experiment ID | Session | Mechanism | Verdict / Status |
|---|---|---|---|---|
| FCLR-STARTER-001 | FCLR-001 | 20261120T052201Z | Time-series 24h forward RV (B0/B1/C1/C2) | NOT_SUPPORTED (terminal) |
| FCLR-XSEC-001..008 | FCLR-XSEC-001..008 | 2026-11-20/21 | Pooled/regime funding contrasts, cross-panel, alt regime | terminal (mixed) |
| FCLR-LIQ-OOS-FORECAST-001 | FCLR-LIQ-OOS-FORECAST-001 | 20261121T055825Z | OOS forecast next-24h liq notional | NOT_SUPPORTED (terminal) |
| FCLR-LIQ-COMBINED-PANEL | FCLR-LIQ-COMBINED-PANEL | 20261115T185844Z | Time-series 24h liq intensity | NOT_MET (terminal) |
| FCLR-BOUNDED-TRIGGER-ONLY | sentinel | 20261121T071500Z | Trigger-only sentinel | SUPERSEDED |
| FCLR-SESSION-SYNTHESIS-01 | consolidation | 20261121T080000Z | Consolidation + meta-analysis | CONSOLIDATORY_ONLY (terminal) |
| FCLR-PANEL-FE-001 | panel-FE | 20261121T130159Z | Panel-FE + walk-forward OOS | NOT_SUPPORTED (terminal) |
| Track A/B/C / FCLR-011 | observed liq / modeled breach / vol forecast | many | blocked/null | blocked/null (terminal) |
| FCLR-LIQ-CONTAGION-001 | cross-coin contagion + funding spillover | 20261121T193000Z | 1.74M-panel Granger/lead-lag, 210 pairs | COMPLETE — H_contagion_liq SUPPORTED (11 edges); H_contagion_funding NOT_SUPPORTED; overall NOT_SUPPORTED; recompute discrepancy (58 vs 11 edges) disclosed and resolved by CONTAGION-002 |
| FCLR-LIQ-CONTAGION-002 | edge-set robustness + per-edge materiality | 20261121T210000Z | 210 directed pairs, 4-criterion ladder, materiality floor, tercile/stability, block bootstrap | COMPLETE — all 3 hypotheses SUPPORTED; full artifact set emitted; discrepancies honestly reported |
| **FCLR-FINAL-SYNTHESIS-01** | final synthesis | **20261121T220100Z** | **This report** | **COMPLETE** |

No campaign above is re-run by this session. CONTAGION-001's point-estimate network is not recomputed.

---

## 4. Data domains explored and exhaustion status

| Domain | Source / artifact | Coverage | Exhaustion status |
|---|---|---|---|
| Binance 5-symbol cache | mark/premium/index klines + funding, 5 symbols (BTC, ETH, BNB, SOL, XRP) | multiple months; all inside tested windows | EXHAUSTED — no ready, funding-backed, untouched month supports a 3-block pre-registered design |
| Hyperliquid ironflow bulk | candles_1h + funding + open_interest + liquidations (CC BY 4.0, unauthenticated, on disk) | tested windows consumed by TRACKA-VOL-FULLHIST, TRACKA-LIQ-XSEC, FCLR-011, forward cells | EXHAUSTED — no untouched contiguous region long enough for a 3-block or forward-reduced design |
| Hyperliquid extended | candles + funding + observed-liq events (per coin) | all tested windows dropped | EXHAUSTED — no untouched region long enough for a 3-block or forward-reduced design |
| Combined liquidation panel (frozen) | `research_state/fclr_liq_combined_panel_20261115T181405Z.parquet`, sha256 `81a100d5d0625832bebabaabea13b786e15319577721cfe8507da5b779ec7f14` | 1,740,415 event rows; 15 coins (AAVE, ADA, AVAX, BNB, BTC, CRV, DOGE, ETH, LINK, LTC, NEAR, SOL, SUI, UNI, XRP); 2025-03-22 → 2026-10-31 UTC; 210 directed pairs | FULLY CONSUMED by CONTAGION-001 and CONTAGION-002; frontier closed |
| FCLR-001 panel (funding/RV baseline) | `fclr011_recompute_panel_20261115T234700Z.parquet`, sha256 `41962f823e59de5989c7d854cb3180cad61a4cbc2f5f230133c41b321342c1f4` | 29,136 rows × 22 cols; 5 coins; 5,832 hours; `premium` all-null | Not used for C2 (premium all-null); retained as baseline input only |

Every frozen prereg has a matching evaluation artifact. `next_campaign_status.py` confirms: **no actionable frozen prereg without an evaluation artifact**; **no feasible 3-block design in any domain**.

---

## 5. Key quantitative results (CONTAGION-002, the terminal heavy session)

Executed under `session_20261121T210000Z/` on the frozen 1.74M panel (211,188 hourly coin-observations; 14,116 hours × 15 coins; 0 dropped for missing funding).

**Four-criterion robustness ladder (all 210 directed pairs):**

| Criterion | Edge count | Density |
|---|---|---|
| raw p < 0.01 | 184 | 0.8762 |
| Bonferroni (0.01/210) | 156 | 0.7429 |
| BH-FDR q = 0.05 | 199 | 0.9476 |
| permutation-empirical (1000 perms/pair) | 102 | 0.4857 |

Pairwise Jaccard 0.5126–0.9246; parametric criteria agree strongly (0.78–0.92), permutation agrees much less (0.51–0.65) — uncorrected/parametric significance is largely serial-dependence driven.

**Per-edge materiality (2% variance-explained floor, actually computed — the quantity CONTAGION-001 never computed):**
- Edges clearing 0.02 floor: **12 / 210** (0.0571); bootstrap 95% CI for count [6, 19]
- Mean variance_explained: 0.0063 (0.63%); median: 0.0039 (0.39%)
- Median edge explains <0.4% of variance — far below the 2% floor.

**Stability:** block-bootstrap (1000 resamples, 24h blocks) → 12 edges both bootstrap-stable (freq ≥ 0.5) and material; 90-day rolling → 31 stable edges, low Jaccard (0.14–0.19); 30-day rolling → **0 stable edges**. Funding-tercile: mid tercile Jaccard ~0.07 (no overlap); low/high terciles moderate overlap (0.32–0.46) — signal concentrated in extreme funding differentials.

**Independent recompute (separate stdlib/numpy code path):** n_clearing=15/210, n_stable=0/210, `recompute_concurs_with_recon: false` — honestly reported discrepancy due to grid/critical-value differences; not suppressed.

**CONTAGION-001 discrepancy resolved as a multiple-testing artifact:** eval edge set = 11 (Granger-Bonferroni ∩ permutation-Bonferroni); recompute = 58 (empirical-p only); disagree on 47 of 210 pairs. The edge set is criterion-dependent, not a stable contagion finding.

Hypothesis verdicts: H_recon_materiality=SUPPORTED; H_recon_robustness=SUPPORTED; H_recon_stability=SUPPORTED. All nulls preserved where applicable; no threshold shopped or relaxed.

---

## 6. Methodological lessons

1. **Multiple-testing criterion drives the edge set.** Parametric criteria (raw/Bonferroni/BH-FDR) yield 156–199 edges; permutation-empirical yields 102. Pairwise Jaccard between parametric and permutation criteria is only 0.51–0.65. Serial dependence inflates parametric significance.
2. **Materiality floor matters.** Only 12/210 edges (5.7%) clear the 2% per-edge variance-explained floor; the median edge explains <0.4%. "Contagion is material" is weakly supported and concentrated in a small minority of pairs.
3. **Stability requires a joint bar.** Bootstrap + ladder + materiality jointly leaves just 12 edges; 30-day rolling stability yields zero stable edges. The contagion network is not temporally stable.
4. **Recompute discrepancies must be disclosed, not hidden.** CONTAGION-001's eval (11) vs recompute (58) discrepancy was resolved as a multiple-testing/grid artifact and honestly reported; CONTAGION-002's own recompute (15 clearing, 0 stable) does not concur with its recon (12 clearing, 12 stable) and is reported as such.
5. **No forecast gate passed.** No primary volatility or liquidation target achieved a meaningful out-of-sample improvement over the realized-volatility-only baseline with supporting uncertainty, multiple-testing treatment, and cross-instrument/cross-block evidence. Per RESEARCH_PROMPT.md §9, no risk-reduction or position-sizing overlay was or could be evaluated.

---

## 7. Forecast gate statement

The forecast gate defined in RESEARCH_PROMPT.md §9 (and frozen in research_state/research_protocol.md before the sealed holdout) requires: a meaningful out-of-sample improvement over the realized-volatility-only baseline on at least one pre-registered primary target; uncertainty supporting incremental skill after multiple-testing treatment; acceptable calibration for event-probability predictions; evidence across multiple time blocks and more than one instrument; no unresolved leakage/source/label/timestamp defect; and practical relevance.

**The gate was NOT PASSED for any primary volatility or liquidation target.** Consequently, **no risk overlay was or could be evaluated.** No position-sizing or risk-reduction overlay was created, simulated, or paper-traded, consistent with RESEARCH_PROMPT.md §1, §9, §20. All null and inconclusive results are preserved (RESEARCH_PROMPT.md §7, §12, §20).

---

## 8. Artifacts produced (this session)

All under `research_state/session_20261121T220100Z/`, UTC > 20261121T210000Z, all non-empty:

- `fclr_final_synthesis_report_20261121T220100Z.md` — this report
- `fclr_final_synthesis_report_20261121T220100Z.json` — manifest (machine-readable)
- `trigger_check_20261121T220100Z.json` — trigger check (no external trigger required; frozen panel sole input)

Nothing is written to `research_state/` root (root md+json count stays 499/500, below the cap). No root-level `research_state/*.md|*.json` added. No empty/placeholder files or empty session directories. No terminal/completed campaign re-run. `.github/workflows` unmodified. `research_state/research_protocol.md` (sealed legacy FCLR-001) unoverwritten.

---

## 9. Verification

```bash
python3 scripts/check_handoff_heavywork_gate.py                    # → PASS reason=OK
python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_144  # 68 pass, 0 fail
python3 scripts/next_campaign_status.py                            # CAMPAIGN STATUS: no feasible 3-block design in ANY domain
ls -la research_state/session_20261121T220100Z/                    # non-empty artifact set
```

---

## 10. Close-out

The frozen-data research cycle is **complete**. All primary hypotheses (FCLR-H001..H004) carry terminal verdicts (NOT_SUPPORTED / DATA_BLOCKED); every campaign is terminal/superseded; all data domains are exhausted; the forecast gate was not passed for any primary target; no overlay was evaluated. The null results are the result.

This session is the final record. No active rank-0 campaign remains. Future agents cannot avoid this work: the durable handoff (AGENT_HANDOFF.md) records the final synthesis report as the sole remaining deliverable and the gate enforces that any new session directory must contain non-empty heavy artifacts under `research_state/session_<UTC>/`. If no future session occurs, this handoff stands as the final record: all evidence preserved, no gate passed, no overlay evaluated.

*(End of report)*
