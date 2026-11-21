# AGENT HANDOFF — Funding-Conditioned Volatility and Liquidation Risk
**Repository:** Funding-conditioned-volatility-and-liquidation-risk
**Timestamp:** 2026-11-21T20:00:00Z (supersedes 2026-11-21T19:51:14Z)
**Sole active campaign:** FCLR-LIQ-CONTAGION-002-20261121T200000Z (rank-0; edge-set robustness + per-edge materiality reconciliation on the frozen 1.74M panel)
**Latest completed heavy session on disk:** session_20261121T193000Z (FCLR-LIQ-CONTAGION-001, COMPLETE — see §5)
**Gate baseline:** `python3 scripts/check_handoff_heavywork_gate.py` → PASS (`reason=OK`, `root=499/500`). `python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_144` → 77 pass, 0 fail. `python3 scripts/next_campaign_status.py` → confirms CONTAGION-001 executed; the only remaining heavy frontier is CONTAGION-002 (reconciliation), which is feasible on the frozen panel.
**Environment:** Python 3.12.3; `numpy 2.5.5`, `pandas 3.1.1`, `scipy 1.18.1`, `pyarrow 26.0.1` verified importable.

---

> **SINGLE DURABLE HANDOFF.** This supersedes all prior handoffs and `NEXT_SESSION_TASK.md` files. Exactly ONE initial task message (Section 1) and ONE active campaign (FCLR-LIQ-CONTAGION-002). All prior campaigns (STARTER-001, FCLR-001, FCLR-XSEC-001..008, LIQ-XSEC-QLIKE/ORDERING, LIQ-COMBINED-PANEL, FCLR-LIQ-OOS-FORECAST-001, FCLR-BOUNDED-TRIGGER-ONLY, FCLR-SESSION-SYNTHESIS-01, FCLR-PANEL-FE-001, Track A/B/C, FCLR-LIQ-CONTAGION-001) are terminal/superseded/completed — **do NOT re-run them**. A session that does not emit the Section 4 artifact set under a new `research_state/session_<UTC>/` (UTC > 20261121T200000Z) has NOT completed the handoff; the gate WILL FAIL. "Verify green and stop" is NOT a valid close-out while FCLR-LIQ-CONTAGION-002 is ACTIVE and its heavy artifacts are absent.

---

## 1. INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION (timestamped 2026-11-21T20:00:00Z)

**PRIORITY-0 MISSION: Execute FCLR-LIQ-CONTAGION-002 — edge-set robustness and per-edge materiality reconciliation on the frozen 1.74M liquidation panel. This is HEAVY computation. Do NOT verify and stop.**

**Why this campaign exists (the bottleneck it removes).** FCLR-LIQ-CONTAGION-001 (completed under `session_20261121T193000Z`) computed the cross-coin liquidation-contagion network but left a **disclosed, unresolved methodological discrepancy** that the previous handoff (2026-11-21T19:51:14Z) told future agents to ignore by "verifying green and stopping." That would let every future agent dodge the real science forever. The discrepancy, taken directly from the on-disk artifacts:

- `fclr_liq_contagion01_eval_*.json`: **11 final edges** (density 0.0524). Method = Granger-Bonferroni-significant (155 pairs) **INTERSECT** permutation-significant (16 pairs) = 11 edges.
- `fclr_liq_contagion01_recompute_*.json`: **58 edges** (density 0.2762). Method = empirical-p-only (300 permutations). `recompute_concurs_with_eval: false`.
- The two edge sets **disagree on 47 of 210 directed pairs**. The contagion network's edge set is therefore an artifact of an unresolved multiple-testing choice, not a stable finding.
- The **2% per-edge materiality floor** (`materiality_floor: 0.02`, `materiality_floor_respected: true`) was **asserted but never actually computed** — there is no per-edge variance-explained / R^2 field anywhere in the eval JSON. The "material" claim is unsupported by any computed quantity.
- The funding-tercile split and 90-day rolling temporal-stability results were reported descriptively but **never reconciled** against the primary edge set.

**FCLR-LIQ-CONTAGION-002 resolves exactly this.** It reuses the SAME frozen panel (no new data, no external trigger, no credentials) and does the heavy reconciliation work CONTAGION-001 skipped.

**Your task THIS session (execute the full protocol; do not shortcut):**
1. **Prereg freeze (outcome-blind, BEFORE any statistic):** Write `fclr_liq_contagion02_prereg_<UTC>.json` + `.md` under `research_state/session_<UTC>/` (UTC > 20261121T200000Z). Record: `experiment_id` starting `FCLR-LIQ-CONTAGION-002`, `outcome_data_inspected_before_freeze: false`, the frozen hypotheses (below), `materiality_floor: 0.02`, `panel_sha256: 81a100d5...`, and the exact estimator definitions. Assert the panel sha256 in the script header.
2. **Reconciliation evaluation (HEAVY):** Write `fclr_liq_contagion02_recon_<UTC>.py` + `.json` + `.md`. On the 1.74M panel (hourly-aggregated, 15 coins, 2025-03-22..2026-10-31), for **all 210 directed pairs**:
   - **Per-edge materiality:** within each VAR(6) Granger regression, compute the **R^2 / partial variance explained** by the source-coin lags (this is the quantity CONTAGION-001 never computed). Record per-edge `variance_explained` and the fraction of edges clearing the 0.02 floor.
   - **Multiple-testing robustness ladder:** re-derive the edge set under **four** criteria — (a) raw p<0.01, (b) Bonferroni across 210, (c) Benjamini-Hochberg FDR q=0.05, (d) permutation-empirical (1000 permutations/pair) — and report the **edge-set size and pairwise Jaccard agreement** across criteria. The eval-vs-recompute disagreement MUST be quantified here, not hidden.
   - **Tercile & stability reconciliation:** recompute the funding-tercile edge sets and the 90-day/30-day rolling edge sets, then report their overlap (Jaccard) with each of the four primary criteria' edge sets.
   - **Block-bootstrap edge-set stability:** 1000+ moving-block bootstrap resamples of the hourly panel; report the per-edge selection frequency and the 95% edge-set stability interval.
3. **Independent recompute:** Write `fclr_liq_contagion02_recompute_<UTC>.py` + `.json` — a **separate stdlib/numpy code path** (no shared helpers with the recon script) that independently reproduces the per-edge variance-explained and at least one robustness criterion. Report `recompute_concurs_with_recon: true|false` honestly. If it disagrees, record the discrepancy; do not suppress it.
4. **Evidence audit:** Write `fclr_liq_contagion02_evidence_audit_<UTC>.json` + `.md`, plus the gate-critical alias `evidence_audit_<UTC>.json` (literal prefix required by the gate).
5. **Trigger check:** Write `trigger_check_<UTC>.json` (non-empty; this campaign requires no external trigger — record `required: false` and the reason).

**Hypotheses to freeze (outcome-blind):**
- **H_recon_materiality:** When the 2% per-edge variance-explained floor is *actually computed*, the number of contagion edges clearing it is reported with a confidence interval, and the claim "contagion is material" is promoted or demoted accordingly (replacing CONTAGION-001's asserted-but-uncomputed flag).
- **H_recon_robustness:** The contagion edge set is characterised across raw/Bonferroni/BH-FDR/permutation-empirical criteria; the cross-criterion Jaccard agreement rate is reported, and any edge present under only one criterion is flagged as fragile.
- **H_recon_stability:** Block-bootstrap edge-set stability (per-edge selection frequency) and tercile/stability reconciliation are reported against each primary criterion; an edge is "stable" only if it survives the bootstrap AND the criterion ladder.

**Materiality floor:** 2% relative variance explained per edge — frozen, not to be relaxed after seeing outcomes.

**Acceptance — the gate WILL FAIL if any of these are missing/empty:**
```bash
python3 scripts/check_handoff_heavywork_gate.py          # → [PASS] reason=OK, contagion_002.pass=true
python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_144  # 77 pass
python3 scripts/next_campaign_status.py                   # CONTAGION-001 executed; CONTAGION-002 is the active reconciliation frontier
```

**HARD CONSTRAINTS (violation = gate failure):**
- Do NOT re-run any terminal/completed campaign (see §5). CONTAGION-001 is COMPLETE — do not recompute its point-estimate network; build on its artifacts.
- Do NOT modify `.github/workflows` (protected control plane).
- Do NOT overwrite `research_state/research_protocol.md` (sealed legacy FCLR-001).
- Do NOT add root-level `research_state/*.md|*.json` — count is 499/500; one more breaches the cap. Put all new artifacts under `research_state/session_<UTC>/`.
- Do NOT create empty/placeholder files or empty session directories (gate checks non-zero size).
- Do NOT threshold-shop or relax the 2% materiality floor after seeing outcomes. Preserve nulls as NOT_SUPPORTED.
- Do NOT claim completion without the full CONTAGION-002 artifact set under a new `session_<UTC>/` (UTC > 20261121T200000Z).
- Do NOT "verify green and stop." While CONTAGION-002 is ACTIVE and its reconciliation artifacts are absent, verify-and-stop is a gate failure by construction (see `tests/test_tracka_hardening_144.py::test_post_start_verify_and_stop_fails_closed`).

**State verification:**
- `research_state/experiment_frontier.json` rank 0 = FCLR-LIQ-CONTAGION-002-20261121T200000Z, program_status ACTIVE, phases PENDING.
- `hypothesis_registry.json` will gain H_recon_materiality, H_recon_robustness, H_recon_stability upon your prereg freeze.
- Root `research_state/` md+json count ≤ 500 (currently 499/500).

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
- Per-edge **partial R^2 / variance explained** within 210 VAR(6) Granger regressions (the quantity CONTAGION-001 never computed).
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