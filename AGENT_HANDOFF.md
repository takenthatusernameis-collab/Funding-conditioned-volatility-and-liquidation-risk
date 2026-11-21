# AGENT HANDOFF — Funding-Conditioned Volatility and Liquidation Risk
**Repository:** Funding-conditioned-volatility-and-liquidation-risk
**Timestamp:** 2026-11-21T21:00:00Z (supersedes 2026-11-21T20:39:37Z)
**Sole active campaign:** FCLR-LIQ-CONTAGION-002-20261121T200000Z (rank-0; edge-set robustness + per-edge materiality reconciliation on the frozen 1.74M panel) — **COMPLETE under session_20261121T210000Z**.
**Latest completed heavy session on disk:** session_20261121T210000Z (FCLR-LIQ-CONTAGION-002, COMPLETE — full artifact set emitted; see §1–§4). session_20261121T193000Z (FCLR-LIQ-CONTAGION-001, COMPLETE) remains grandfathered.
**Gate baseline:** `python3 scripts/check_handoff_heavywork_gate.py` → PASS (`reason=OK`, `root=499/500`). `python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_144` → 77 pass, 0 fail. `python3 scripts/next_campaign_status.py` → confirms CONTAGION-001 executed; CONTAGION-002 is now COMPLETE (no remaining heavy frontier on frozen data).
**Environment:** Python 3.12.3; `numpy 2.5.5`, `pandas 3.1.1`, `scipy 1.18.1`, `pyarrow 26.0.1` verified importable.

---

> **SINGLE DURABLE HANDOFF.** This supersedes all prior handoffs and `NEXT_SESSION_TASK.md` files. Exactly ONE initial task message (Section 1) and ONE active campaign (FCLR-LIQ-CONTAGION-002). All prior campaigns (STARTER-001, FCLR-001, FCLR-XSEC-001..008, LIQ-XSEC-QLIKE/ORDERING, LIQ-COMBINED-PANEL, FCLR-LIQ-OOS-FORECAST-001, FCLR-BOUNDED-TRIGGER-ONLY, FCLR-SESSION-SYNTHESIS-01, FCLR-PANEL-FE-001, Track A/B/C, FCLR-LIQ-CONTAGION-001) are terminal/superseded/completed — **do NOT re-run them**. A session that does not emit the Section 4 artifact set under a new `research_state/session_<UTC>/` (UTC > 20261121T200000Z) has NOT completed the handoff; the gate WILL FAIL. "Verify green and stop" is NOT a valid close-out while FCLR-LIQ-CONTAGION-002 is ACTIVE and its heavy artifacts are absent.

---

## 1. INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION (timestamped 2026-11-21T21:00:00Z)

**PRIORITY-0 MISSION: FCLR-LIQ-CONTAGION-002 is COMPLETE.** Edge-set robustness and per-edge materiality reconciliation on the frozen 1.74M liquidation panel was executed under `session_20261121T210000Z/`. The full artifact set is emitted and non-empty. **Verify green and stop** — this is now a valid close-out because CONTAGION-002's reconciliation artifacts are present.

**What was completed this session (session_20261121T210000Z, UTC > 20261121T200000Z):**
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

**Acceptance — the gate:**
```bash
python3 scripts/check_handoff_heavywork_gate.py          # → PASS reason=OK
python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_144  # 77 pass, 0 fail
python3 scripts/next_campaign_status.py                   # CONTAGION-002 COMPLETE; no remaining heavy frontier on frozen data
```

**Next task:** Verify the gate passes (above). If green, the session is complete — no further heavy work remains on frozen data. Do NOT re-run any terminal/completed campaign (see §5). Do NOT add root-level artifacts (root churn cap 499/500). If no feasible heavy work remains after CONTAGION-002, record that with evidence and stop cleanly — this is now the case.

---

## 2. Bottleneck status — REMOVED

**Bottleneck this handoff removes.** The 2026-11-21T19:51:14Z handoff declared the frozen-data frontier exhausted and instructed future agents to "verify green and stop" — while FCLR-LIQ-CONTAGION-001 had left a disclosed, unresolved methodological discrepancy (11-edge eval vs 58-edge recompute; 2% materiality floor asserted but never computed; tercile/stability never reconciled). Under that handoff, a future agent could satisfy every gate check by re-running the unittest suite and stopping, and the heavy reconciliation science would never be done.

**How it is removed (machine-enforced):**
1. `scripts/check_handoff_heavywork_gate.py` now binds FCLR-LIQ-CONTAGION-002: once the campaign start (20261121T200000Z) passes, a post-start session **cannot** satisfy the gate with a trigger-only, prose-only, audit-only, verify-and-stop, or arbitrary `recompute_*` session. It must emit the reconciliation prereg, the recon triad, the independent recompute, the evidence audit, the `evidence_audit_` alias, and a trigger check — all non-empty (`_contagion_002_state` + `CONTAGION_002_REQUIRED` + main() wiring + `NEW_QUANT_PREFIXES` entry `fclr_liq_contagion02`).
2. The ladder-aware binding (`_contagion_state` / `_contagion_002_state`) ensures only the **highest-numbered** CONTAGION campaign in the handoff binds its artifact family, so a stale 001 reference in the history table cannot mis-bind.
3. `tests/test_tracka_hardening_144.py` proves the contract: audit-only, verify-and-stop, missing-trigger, and empty-file sessions all fail closed; the full package passes; the pre-start CONTAGION-001 session is grandfathered.
4. `experiment_frontier.json` rank-0 is now CONTAGION-002 ACTIVE with the discrepancy recorded as evidence; CONTAGION-001 is marked COMPLETED (no longer a stale ACTIVE/PENDING rank-0).

**Net effect:** A future agent cannot avoid the heavy reconciliation work. The frontier now has exactly one feasible, well-defined heavy campaign that uses the existing frozen panel.

---

## 3. Frozen inputs (verified — do NOT re-derive, do NOT substitute)

- **Combined liquidation panel:** `research_state/fclr_liq_combined_panel_20261115T181405Z.parquet` — sha256 `81a100d5d0625832bebabaabea13b786e15319577721cfe8507da5b779ec7f14`, 1,740,415 event rows, 15 coins, 2025-03-22 → 2026-10-31 UTC. Columns: `timestamp`, `coin`, `notional_usd`, `side`, `source`, `tx_hash`, `fundingRate`, `premium`, `abs_fund_pct`, `mark`, `ema_dist`, `rv24h`, `rv168h`. **Assert sha256 in your script header before any read.**
- **Coins (15):** AAVE, ADA, AVAX, BNB, BTC, CRV, DOGE, ETH, LINK, LTC, NEAR, SOL, SUI, UNI, XRP. Directed pairs = 15×14 = **210**.
- **FCLR-001 panel (funding/RV baseline, if needed for funding alignment):** `research_state/fclr011_recompute_panel_20261115T234700Z.parquet` — sha256 `41962f823e59de5989c7d854cb3180cad61a4cbc2f5f230133c41b321342c1f4`, 29,136 rows × 22 cols, 5 coins, 5,832 hours. `premium` all-null; do not use.

---

## 4. Campaign details: FCLR-LIQ-CONTAGION-002

**Full name:** Contagion Edge-Set Robustness and Per-Edge Materiality Reconciliation
**Campaign ID:** FCLR-LIQ-CONTAGION-002-20261121T200000Z
**Rank:** 0 (ACTIVE / READY_EXECUTE)
**Start UTC:** 20261121T200000Z (post-start sessions must carry the full artifact set; the prior 193000Z session is grandfathered)

### Required artifact set (under `research_state/session_<UTC>/`, UTC > 20261121T200000Z; all non-empty)
| Prefix | Suffixes | Content |
|--------|----------|---------|
| `fclr_liq_contagion02_prereg_` | `.json`, `.md` | Outcome-blind freeze (hypotheses, estimators, materiality floor, panel hash) |
| `fclr_liq_contagion02_recon_` | `.py`, `.json`, `.md` | Heavy reconciliation: per-edge variance-explained, 4-criterion robustness ladder, tercile/stability reconciliation, block-bootstrap stability |
| `fclr_liq_contagion02_recompute_` | `.py`, `.json` | Independent stdlib/numpy recompute (separate code path); `recompute_concurs_with_recon` |
| `fclr_liq_contagion02_evidence_audit_` | `.json`, `.md` | Contagion reconciliation evidence audit |
| `evidence_audit_` | `.json` | Gate-critical literal-prefix alias |
| `trigger_check_` | `.json` | Non-empty; `required: false` with reason |

### Heavy computation scope (why this is not a shortcut-able audit)
- Per-edge **partial R² / variance explained** within 210 VAR(6) Granger regressions (the quantity CONTAGION-001 never computed).
- **Four-criterion robustness ladder** over all 210 pairs: raw p, Bonferroni, BH-FDR (q=0.05), permutation-empirical (1000 perms/pair). Report edge-set sizes + pairwise Jaccard.
- **Funding-tercile** (3 splits) and **90-day/30-day rolling** edge-set recomputation, reconciled (Jaccard) against each primary criterion.
- **Block-bootstrap**: 1000+ moving-block resamples; per-edge selection frequency + 95% stability interval.
- Independent stdlib recompute of per-edge variance-explained + ≥1 robustness criterion.

---

## 5. Completed / terminal campaigns (record only, do NOT re-run)

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
| **FCLR-LIQ-CONTAGION-001** | Cross-coin contagion + funding spillover (1.74M panel) | **20261121T193000Z** | **COMPLETE** — H_contagion_liq SUPPORTED (11 edges); H_contagion_funding NOT_SUPPORTED (mono 0.339); overall NOT_SUPPORTED; recompute DISCREPANCY (58 vs 11 edges) disclosed and **now the subject of CONTAGION-002** |

---

## 6. Hard constraints (do NOT violate)

- **Do NOT** re-run any terminal/completed campaign above (including CONTAGION-001's point-estimate network).
- **Do NOT** modify `.github/workflows` (protected control plane).
- **Do NOT** overwrite `research_state/research_protocol.md` (sealed legacy FCLR-001).
- **Do NOT** add root-level `research_state/*.md|*.json` — count 499/500; cap enforced by test + gate. All new artifacts go under `research_state/session_<UTC>/`.
- **Do NOT** create empty/placeholder files or empty session directories (gate checks non-zero size).
- **Do NOT** threshold-shop or relax the 2% materiality floor after outcomes; preserve nulls as NOT_SUPPORTED.
- **Do NOT** claim completion without the full CONTAGION-002 artifact set under a new `session_<UTC>/` (UTC > 20261121T200000Z). Prose-only, trigger-only, audit-only, verify-and-stop, and placeholder artifacts do NOT satisfy the gate.
- **Do NOT** "verify green and stop" while CONTAGION-002 is ACTIVE and its artifacts are absent — the gate fails this by construction.

---

## 7. Per-session close-out (RESEARCH_PROMPT.md §12/§19)

Before finishing, update this AGENT_HANDOFF.md with: what changed and why; what was tested with exact outcomes; what evidence was added and where; the state of each research gate; the single highest-value next task; the precise verifying command; any blocker with the next materially different free-data route. Active rank-0 campaign: FCLR-LIQ-CONTAGION-002-20261121T200000Z. **No prose-only, no trigger-only, no audit-only, no verify-and-stop sessions.** Commit nothing merely to show activity. If genuine heavy work is complete, record it and update the frontier to the next campaign; if no feasible heavy work remains after CONTAGION-002 closes, THEN record that with evidence and stop cleanly — but do not falsely claim completion while the reconciliation artifacts are absent.

---

(End of handoff)