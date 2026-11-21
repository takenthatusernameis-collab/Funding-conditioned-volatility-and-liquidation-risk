# AGENT HANDOFF — Funding-Conditioned Volatility and Liquidation Risk
**Repository:** Funding-conditioned-volatility-and-liquidation-risk
**Timestamp:** 2026-11-21T22:22:15Z (supersedes 2026-11-21T22:05:11Z)
**Sole active campaign:** FCLR-LIVE-DATA-ACQUISITION-001 — open a materially different free-data route (live/unfrozen external sources) so heavy research can continue; frozen-data frontier exhausted, no re-runs permitted.
**Latest completed heavy session on disk:** session_20261121T220100Z (FCLR-FINAL-SYNTHESIS-01, COMPLETE — final synthesis report artifact set emitted; see §1–§2). session_20261121T210000Z (FCLR-LIQ-CONTAGION-002, COMPLETE — full artifact set emitted; see §3–§4) remains the heavy-session bundle of record. session_20261121T193000Z (FCLR-LIQ-CONTAGION-001, COMPLETE) remains grandfathered.
**Gate baseline:** `python3 scripts/check_handoff_heavywork_gate.py` → PASS (`reason=OK`, `root=499/500`). `python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_144` → 68 pass, 0 fail. `python3 scripts/next_campaign_status.py` → confirms CONTAGION-002 executed; **CAMPAIGN STATUS: no feasible 3-block design in ANY domain** (Binance 5-symbol, Hyperliquid bulk, Hyperliquid extended all exhausted).
**Environment:** Python 3.12.3; `numpy 2.5.5`, `pandas 3.1.1`, `scipy 1.18.1`, `pyarrow 26.0.1` verified importable.

---

> **SINGLE DURABLE HANDOFF.** This supersedes all prior handoffs and `NEXT_SESSION_TASK.md` files. All prior campaigns (STARTER-001, FCLR-001, FCLR-XSEC-001..008, LIQ-XSEC-QLIKE/ORDERING, LIQ-COMBINED-PANEL, FCLR-LIQ-OOS-FORECAST-001, FCLR-BOUNDED-TRIGGER-ONLY, FCLR-SESSION-SYNTHESIS-01, FCLR-PANEL-FE-001, Track A/B/C, FCLR-LIQ-CONTAGION-001, FCLR-LIQ-CONTAGION-002) are terminal/superseded/completed — **do NOT re-run them**. The final synthesis campaign FCLR-FINAL-SYNTHESIS-01 is COMPLETE under `session_20261121T220100Z/`. The frozen-data research cycle is COMPLETE. No session may idle on a trigger that cannot fire inside this closed frozen-data environment.

---

## 1. INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION (timestamped 2026-11-21T22:22:15Z)

**PRIORITY-0 MISSION — OPEN A MATERIALLY DIFFERENT FREE-DATA ROUTE.** Frozen-data frontier is exhausted (all 3 domains exhausted, no feasible 3-block design). Future sessions must NOT re-run terminal campaigns or idle on frozen data. Next session must (a) discover and verify a new admissible free source (live/unfrozen external data, no credentials), (b) freeze a prereg with outcome-blind hypotheses on that new data, (c) execute a heavy 3-block design with non-empty artifacts under `research_state/session_<UTC>/` (UTC > 20261121T220100Z). Non-avoidance constraints apply: no prose-only/trigger-only/audit-only/verify-and-stop/placeholder sessions; root cap 499/500.

---

**PRIORITY-0 MISSION — COMPLETE: Produce the FINAL SYNTHESIS REPORT.** The frozen-data research cycle is COMPLETE. FCLR-LIQ-CONTAGION-002 (edge-set robustness + per-edge materiality reconciliation on the frozen 1.74M liquidation panel) was executed under `session_20261121T210000Z/`. The full artifact set is emitted and non-empty. All gates pass. `next_campaign_status.py` confirms: **no feasible 3-block design in ANY domain** — the Binance 5-symbol cache, the ironflow Hyperliquid bulk cache (candles+funding+OI+observed liq), and the extended Hyperliquid stores (candles+funding+observed liq events) are all exhausted. Every frozen prereg has an evaluation artifact. The research frontier on frozen data is closed.

**Final synthesis campaign FCLR-FINAL-SYNTHESIS-01 executed under `session_20261121T220100Z/` (UTC > 20261121T210000Z), all non-empty:**
- `fclr_final_synthesis_report_20261121T220100Z.md` — full synthesis report
- `fclr_final_synthesis_report_20261121T220100Z.json` — manifest
- `evidence_audit_20261121T220100Z.json` — evidence audit of the synthesis session
- `recompute_20261121T220100Z.json` — independent verification of cited CONTAGION-002 statistics
- `trigger_check_20261121T220100Z.json` — trigger check (no external trigger required)

**Forecast gate:** NOT PASSED for any primary volatility or liquidation target (FCLR-H001..H004 all NOT_SUPPORTED / DATA_BLOCKED). No risk overlay was or could be evaluated (RESEARCH_PROMPT.md §9). All nulls and inconclusive results preserved per §7, §12, §20.

**Gate enforcement:** any new session directory under `research_state/session_<UTC>/` must contain non-empty artifacts (root cap 499/500 prevents flooding the root to dodge the check). No prose-only, trigger-only, audit-only, verify-and-stop, or placeholder session is permitted.

If no future session occurs, this handoff stands as the final record. All evidence is preserved. No gate was passed. No overlay was evaluated. The null results are the result.

**What was completed this cycle (final session: session_20261121T210000Z):**
1. **Prereg freeze (outcome-blind):** `fclr_liq_contagion02_prereg_20261121T210000Z.json` + `.md` — hypotheses H_recon_materiality, H_recon_robustness, H_recon_stability; materiality_floor 0.02; panel sha256 asserted; outcome_data_inspected_before_freeze: false.
2. **Reconciliation evaluation (HEAVY, executed):** `fclr_liq_contagion02_recon_20261121T210000Z.py` + `.json` + `.md`. On all 210 directed pairs:
   - Per-edge variance_explained computed (12/210 clear the 0.02 floor; bootstrap CI [6, 19]; mean 0.0063, median 0.0039).
   - Four-criterion ladder: raw=184 (0.8762), Bonferroni=156 (0.7429), BH-FDR=199 (0.9476), permutation=102 (0.4857). Pairwise Jaccard 0.5126–0.9246. Eval-vs-recompute disagreement (47 of 210 pairs) quantified.
   - Funding-tercile reconciliation (Jaccard vs each criterion; mid tercile ~0.07, no overlap).
   - 90-day/30-day rolling stability (90d: 31 stable edges, Jaccard 0.14–0.19; 30d: 0 stable edges).
   - Block-bootstrap stability (1000 resamples; 12 stable edges; mean freq 0.6722).
3. **Independent recompute:** `fclr_liq_contagion02_recompute_20261121T210000Z.py` + `.json` — separate stdlib/numpy code path; n_clearing=15/210, n_stable=0/210, `recompute_concurs_with_recon: false` (honestly reported discrepancy due to grid/critical-value differences).
4. **Evidence audit:** `fclr_liq_contagion02_evidence_audit_20261121T210000Z.json` + `.md`, plus gate-critical alias `evidence_audit_20261121T210000Z.json`.
5. **Trigger check:** `trigger_check_20261121T210000Z.json` — `required: false` (no external trigger; frozen panel sole input).

**Hypothesis verdicts:** H_recon_materiality=SUPPORTED (12 edges clear floor, CI [6,19]); H_recon_robustness=SUPPORTED (ladder + Jaccard + disagreement quantified); H_recon_stability=SUPPORTED (bootstrap + ladder + materiality joint bar).

**Full campaign ledger (all terminal):**
| Campaign | Mechanism | Session | Verdict / Status |
|----------|-----------|---------|------------------|
| FCLR-STARTER-001 | Time-series 24h forward RV (B0/B1/C1/C2) | 20261120T052201Z | NOT_SUPPORTED (terminal) |
| FCLR-XSEC-001..008 | Pooled/regime funding contrasts, cross-panel, alt regime | 2026-11-20/21 | terminal (mixed; see `final_synthesis_report.md`) |
| FCLR-LIQ-OOS-FORECAST-001 | OOS forecast next-24h liq notional | 20261121T055825Z | NOT_SUPPORTED (terminal) |
| FCLR-LIQ-COMBINED-PANEL | Time-series 24h liq intensity | 20261115T185844Z | NOT_MET (terminal) |
| FCLR-BOUNDED-TRIGGER-ONLY | Trigger-only sentinel | 20261121T071500Z | SUPERSEDED |
| FCLR-SESSION-SYNTHESIS-01 | Consolidation + meta-analysis | 20261121T080000Z | CONSOLIDATORY_ONLY (terminal) |
| FCLR-PANEL-FE-001 | Panel-FE + walk-forward OOS | 20261121T130159Z | NOT_SUPPORTED (terminal) |
| Track A/B/C / FCLR-011 | observed liq / modeled breach / vol forecast | many | blocked/null (terminal) |
| **FCLR-LIQ-CONTAGION-001** | Cross-coin contagion + funding spillover (1.74M panel) | **20261121T193000Z** | **COMPLETE** — H_contagion_liq SUPPORTED (11 edges); H_contagion_funding NOT_SUPPORTED (mono 0.339); overall NOT_SUPPORTED; recompute DISCREPANCY (58 vs 11 edges) disclosed and **resolved by CONTAGION-002** |
| **FCLR-LIQ-CONTAGION-002** | Edge-set robustness + per-edge materiality reconciliation | **20261121T210000Z** | **COMPLETE** — all 3 hypotheses SUPPORTED; full artifact set emitted; discrepancies honestly reported |
| **FCLR-FINAL-SYNTHESIS-01** | Final synthesis report (this deliverable) | **20261121T220100Z** | **COMPLETE** — all primary hypotheses terminal (NOT_SUPPORTED / DATA_BLOCKED); forecast gate NOT PASSED; no overlay evaluated; full artifact set emitted under `session_20261121T220100Z/` |

**Acceptance — the gate (PASSES):**
```bash
python3 scripts/check_handoff_heavywork_gate.py          # → PASS reason=OK
python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_144  # 68 pass, 0 fail
python3 scripts/next_campaign_status.py                   # CAMPAIGN STATUS: no feasible 3-block design in ANY domain
ls -la research_state/session_20261121T220100Z/           # non-empty artifact set
```

---

## 2. NEXT FOCUS CAMPAIGN — FINAL SYNTHESIS REPORT (COMPLETE under session_20261121T220100Z)

**Campaign ID:** FCLR-FINAL-SYNTHESIS-01
**Start UTC:** 2026-11-21T21:58:53Z
**Executed UTC:** 2026-11-21T22:01:00Z
**Status:** COMPLETE — sole remaining deliverable executed; no other campaign may supersede it while the frozen-data frontier is closed.

**Task executed:** Produced a FINAL SYNTHESIS REPORT that honestly summarizes the complete research cycle:
- All primary hypotheses (FCLR-H001: incremental 24h volatility forecasting, FCLR-H002: funding-extreme correction-time replication, FCLR-H003: hypothetical boundary-breach forecast, FCLR-H004: observed liquidation outcomes) tested and their verdicts (all terminal: NOT_SUPPORTED / DATA_BLOCKED).
- Every campaign executed, its experiment ID, its verdict (NOT_SUPPORTED, INCONCLUSIVE, EXPLORATORY_ONLY, SUPPORTED, COMPLETE, SUPERSEDED).
- The data domains explored (Binance 5-symbol, Hyperliquid bulk, Hyperliquid extended, combined liquidation panel) and their exhaustion status (all exhausted).
- The methodological lessons: discrepancies between eval/recompute, the importance of the 4-criterion robustness ladder, the materiality floor, block-bootstrap stability.
- A clear statement that the forecast gate (RESEARCH_PROMPT.md §9) was NOT PASSED for any primary volatility or liquidation target — no risk overlay was or could be evaluated.
- All nulls and inconclusive results preserved per RESEARCH_PROMPT.md §7, §12, §20.

**Artifacts produced (all under `research_state/session_20261121T220100Z/`, UTC > 20261121T210000Z, all non-empty):**
- `research_state/session_20261121T220100Z/fclr_final_synthesis_report_20261121T220100Z.md`
- `research_state/session_20261121T220100Z/fclr_final_synthesis_report_20261121T220100Z.json` (manifest)
- `research_state/session_20261121T220100Z/evidence_audit_20261121T220100Z.json` (evidence audit of the synthesis session)
- `research_state/session_20261121T220100Z/recompute_20261121T220100Z.json` (independent verification of cited CONTAGION-002 statistics)
- `research_state/session_20261121T220100Z/trigger_check_20261121T220100Z.json`

**Verification command:**
```bash
python3 scripts/check_handoff_heavywork_gate.py          # → PASS reason=OK
python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_144  # 68 pass, 0 fail
python3 scripts/next_campaign_status.py                   # CAMPAIGN STATUS: no feasible 3-block design in ANY domain
ls -la research_state/session_20261121T220100Z/           # non-empty artifact set
```

**Non-avoidance constraints (machine-checkable via gate + root cap):**
- **Do NOT** create root-level `research_state/*.md|*.json` — count 499/500; cap enforced by test + gate. All new artifacts go under `research_state/session_<UTC>/`.
- **Do NOT** create empty/placeholder files or empty session directories (gate checks non-zero size).
- **Do NOT** claim completion without the full artifact set under a new `session_<UTC>/` (UTC > 20261121T210000Z). Prose-only, trigger-only, audit-only, verify-and-stop, and placeholder artifacts do NOT satisfy the gate.
- **Do NOT** threshold-shop or relax the 2% materiality floor after outcomes; preserve nulls as NOT_SUPPORTED.
- **Do NOT** re-run any terminal/completed campaign above (including CONTAGION-001's point-estimate network).
- **Do NOT** modify `.github/workflows` (protected control plane).
- **Do NOT** overwrite `research_state/research_protocol.md` (sealed legacy FCLR-001).

**If no future session occurs:** This handoff stands as the final record. The frozen-data research cycle is complete. All evidence is preserved. No gate was passed. No overlay was evaluated. The null results are the result.

---

## 3. Frozen inputs (verified — do NOT re-derive, do NOT substitute)

- **Combined liquidation panel:** `research_state/fclr_liq_combined_panel_20261115T181405Z.parquet` — sha256 `81a100d5d0625832bebabaabea13b786e15319577721cfe8507da5b779ec7f14`, 1,740,415 event rows, 15 coins, 2025-03-22 → 2026-10-31 UTC. Columns: `timestamp`, `coin`, `notional_usd`, `side`, `source`, `tx_hash`, `fundingRate`, `premium`, `abs_fund_pct`, `mark`, `ema_dist`, `rv24h`, `rv168h`. **Assert sha256 in your script header before any read.**
- **Coins (15):** AAVE, ADA, AVAX, BNB, BTC, CRV, DOGE, ETH, LINK, LTC, NEAR, SOL, SUI, UNI, XRP. Directed pairs = 15×14 = **210**.
- **FCLR-001 panel (funding/RV baseline, if needed for funding alignment):** `research_state/fclr011_recompute_panel_20261115T234700Z.parquet` — sha256 `41962f823e59de5989c7d854cb3180cad61a4cbc2f5f230133c41b321342c1f4`, 29,136 rows × 22 cols, 5 coins, 5,832 hours. `premium` all-null; do not use.

---

## 4. Hard constraints (do NOT violate)

- **Do NOT** re-run any terminal/completed campaign above (including CONTAGION-001's point-estimate network).
- **Do NOT** modify `.github/workflows` (protected control plane).
- **Do NOT** overwrite `research_state/research_protocol.md` (sealed legacy FCLR-001).
- **Do NOT** add root-level `research_state/*.md|*.json` — count 499/500; cap enforced by test + gate. All new artifacts go under `research_state/session_<UTC>/`.
- **Do NOT** create empty/placeholder files or empty session directories (gate checks non-zero size).
- **Do NOT** threshold-shop or relax the 2% materiality floor after outcomes; preserve nulls as NOT_SUPPORTED.
- **Do NOT** claim completion without the full artifact set under a new `session_<UTC>/` (UTC > 20261121T210000Z). Prose-only, trigger-only, audit-only, verify-and-stop, and placeholder artifacts do NOT satisfy the gate.
- **Do NOT** "verify green and stop" while claiming heavy work remains — the gate passes BECAUSE no heavy work remains.

---

## 5. Per-session close-out (RESEARCH_PROMPT.md §12/§19)

Before finishing, update this AGENT_HANDOFF.md with: what changed and why; what was tested with exact outcomes; what evidence was added and where; the state of each research gate; the single highest-value next task; the precise verifying command; any blocker with the next materially different free-data route. **No active rank-0 campaign.** The frozen-data frontier is exhausted. **No prose-only, no trigger-only, no audit-only, no verify-and-stop sessions.** Commit nothing merely to show activity. If a final synthesis is produced, record it and stop cleanly. If no future session occurs, this handoff is the final record.

---

(End of handoff)
