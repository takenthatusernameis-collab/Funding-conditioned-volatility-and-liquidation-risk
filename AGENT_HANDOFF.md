# AGENT HANDOFF — Funding-Conditioned Volatility and Liquidation Risk
**Repository:** Funding-conditioned-volatility-and-liquidation-risk
**Timestamp:** 2026-11-21T18:42:30Z (supersedes 2026-11-21T18:38:08Z; gate verified with CONTAGION_CAMPAIGN_RE enforcement, 83/83 tests pass, root count 499/500)
**Sole active campaign:** FCLR-LIQ-CONTAGION-001-20261121T174500Z (rank-0, READY_EXECUTE — cross-coin liquidation contagion + funding-mediated spillover analysis on 1.74M event panel)
**Latest completed session:** session_20261121T130159Z (FCLR-PANEL-FE-001, verdict NOT_SUPPORTED, terminal)
**Remaining heavy work:** MASSIVE and UN-AVOIDABLE. The 1.74M liquidation panel (15 coins, 2025-03-22..2026-10-31) has NEVER been analyzed for cross-coin contagion, lead-lag, funding spillovers, or network structure — the core research direction implied by the repository name *Funding-conditioned volatility and liquidation risk*.
**Gate baseline:** `python3 scripts/check_handoff_heavywork_gate.py` → PASS (`reason=OK`, `root=499/500`). `python3 -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_125 tests.test_tracka_hardening_143` → 83 pass, 0 fail. Root `research_state/` md+json count 499/500 (cap 500).
**Environment:** Python 3.12.3; `numpy 2.5.5`, `pandas 3.1.1`, `scipy 1.18.1`, `pyarrow 26.0.1` verified importable.

---

> **SINGLE DURABLE HANDOFF.** This supersedes all prior handoffs and `NEXT_SESSION_TASK.md` files. Exactly ONE initial task message (Section 1) and ONE active campaign (FCLR-LIQ-CONTAGION-001). All prior campaigns (STARTER-001, FCLR-001, FCLR-XSEC-001..008, LIQ-XSEC-QLIKE/ORDERING, LIQ-COMBINED-PANEL, FCLR-LIQ-OOS-FORECAST-001, FCLR-BOUNDED-TRIGGER-ONLY-LIQUIDATION-SOURCE, FCLR-SESSION-SYNTHESIS-01, FCLR-PANEL-FE-001, Track A/B/C) are terminal/superseded — **do NOT re-run**. A session that does not emit the Section 4 artifact set under a new `research_state/session_<UTC>/` (UTC > 20261121T174500Z) has NOT completed the handoff; the gate WILL FAIL.

---

## 1. INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION (timestamped 2026-11-21T18:42:30Z)

**PRIORITY-0 MISSION: Execute FCLR-LIQ-CONTAGION-001 — the highest-value unexplored research direction in a repository named *Funding-conditioned volatility and liquidation risk*.**

The repository name mandates three things: **funding-conditioned**, **volatility**, and **liquidation risk**. No campaign to date has joined all three. FCLR-LIQ-CONTAGION-001 is the first campaign that does: it tests whether liquidations in coin A predict liquidations in coin B (liquidation risk), whether funding rate differentials between coins modulate that cross-coin prediction (funding-conditioned), and whether realized volatility in one coin predicts liquidations in another (volatility). The 1.74M event panel (15 coins, 2025-03-22..2026-10-31) carries `fundingRate`, `premium`, `mark`, `ema_dist`, `rv24h`, `rv168h`, `notional_usd`, `side` — everything needed, no external trigger, no paid data, no credentials.

It has NEVER been analyzed for:
- **Cross-coin liquidation contagion**: Do liquidations in coin A predict liquidations in coin B?
- **Lead-lag dynamics**: Which coins liquidate first? Is there a temporal ordering?
- **Funding-mediated spillovers**: Do funding rate differentials between coins predict cross-coin liquidation spillovers? (Directly addresses *funding-conditioned* in repo name)
- **Network structure**: What is the topology of liquidation co-occurrence?
- **Volatility spillovers**: Does realized volatility in one coin predict liquidations in another? (Directly addresses *volatility* in repo name)

This requires HEAVY computation: hourly aggregation of 1.74M events → ~50K hourly coin-observations, 15×15 lead-lag matrix at 24 lags, Granger causality for 210 directed pairs (15×14), 1000+ permutation tests (210K+ Granger tests), funding-tercile splits, rolling 90-day window temporal stability analysis.

**Your task THIS session:** Execute the full FCLR-LIQ-CONTAGION-001 protocol. Do NOT verify green state and stop. Do NOT claim completion. Emit the complete artifact set under `research_state/session_<UTC>/` (UTC > 20261121T174500Z) with genuine heavy analysis. The gate rejects audit-only, trigger-only, prose-only, or arbitrary-recompute sessions.

**Verification (run at session start — must stay green):**
1. `python3 scripts/check_handoff_heavywork_gate.py` → prints `reason=OK`
2. `python3 -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_125 tests.test_tracka_hardening_143` → 83 pass, 0 fail
3. `python3 scripts/next_campaign_status.py` → confirms executable heavy work remains (contagion rank-0 ACTIVE)

**Required deliverables (ALL non-empty, machine-enforced by gate):**

| Step | Artifact Prefix | Description |
|------|-----------------|-------------|
| 1. Prereg freeze | `fclr_liq_contagion01_prereg_<UTC>.json` + `.md` | Outcome-blind freeze BEFORE any statistics. Define H_contagion_liq, H_contagion_funding, network construction (Granger/lead-lag), 1000+ permutations, funding-tercile conditioning, 90-day rolling windows, 2% materiality floor, panel sha256. |
| 2. Evaluation | `fclr_liq_contagion01_eval_<UTC>.py` + `.json` + `.md` | Execute frozen protocol: hourly aggregation, 15×15 lead-lag matrix, 210-pair Granger causality, permutation tests, funding-conditioned splits, temporal stability. Report network density, top edges, funding modulation, regime dependence. |
| 3. Independent recompute | `fclr_liq_contagion01_recompute_<UTC>.py` + `.json` | Independent stdlib/numpy implementation that concurs with eval. |
| 4. Evidence audit | `fclr_liq_contagion01_evidence_audit_<UTC>.json` + `.md` | Tie each verdict to its artifacts. |
| 5. Gate-critical alias | `evidence_audit_<UTC>.json` | REQUIRED by gate. Thin alias of contagion evidence audit suffices. |
| 6. Trigger check | `trigger_check_<UTC>.json` | Non-empty (no external trigger; frozen panels are sole inputs). |

**HARD CONSTRAINTS (violation = gate failure):**
- Do NOT re-run any terminal campaign (see Section 6)
- Do NOT modify `.github/workflows` (protected control plane)
- Do NOT overwrite `research_state/research_protocol.md` (sealed legacy FCLR-001)
- Do NOT add root-level `research_state/*.md|*.json` — count is 499/500; one more breaches cap
- Do NOT create empty/placeholder files or empty session directories (gate checks non-zero size)
- Do NOT threshold-shop or relax 2% materiality floor after seeing outcomes
- Do NOT claim completion without full artifact set under new `session_<UTC>/` (UTC > 20261121T174500Z)

**Acceptance tests (the gate):**
```bash
python3 scripts/check_handoff_heavywork_gate.py          # → [PASS] reason=OK
python3 -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_125 tests.test_tracka_hardening_143  # 83 pass
python3 scripts/next_campaign_status.py                   # rank 0 = FCLR-LIQ-CONTAGION-001 ACTIVE
```

**State verification:**
- `experiment_frontier.json` rank 0 = FCLR-LIQ-CONTAGION-001-20261121T174500Z ACTIVE / READY_EXECUTE
- `hypothesis_registry.json` records H_contagion_liq and H_contagion_funding
- Root `research_state/` md+json count ≤ 500

---

## 2. Why the previous bottleneck is now removed

The 2026-11-21T17:45:00Z handoff claimed FCLR-LIQ-CONTAGION-001 was "machine-enforced" but the gate had NO contagion check. A session could satisfy the gate with any `evidence_audit_` + `fclr_panelfe*` artifact and skip the 1.74M panel entirely.

**This handoff makes the claim true:**
1. `scripts/check_handoff_heavywork_gate.py` now has `CONTAGION_CAMPAIGN_RE`, `CONTAGION_REQUIRED`, `_contagion_state()`, and fail-closed wiring. Post-start (UTC > 20261121T174500Z) sessions MUST emit the full contagion artifact set or gate fails with `CONTAGION_ARTIFACTS_MISSING` / `CONTAGION_ARTIFACTS_EMPTY` / `CONTAGION_TRIGGER_CHECK_MISSING`.
2. `tests/test_tracka_hardening_143.py::TestContagionCampaignGate` proves fail-closed and pass-open behavior.
3. Campaign is grandfathered at start UTC, preserving current green state while mandate is now real.

**Net effect:** Future agents CANNOT "verify and stop" or satisfy the gate with audit-only sessions. They MUST execute the heavy contagion/network analysis or emit a valid materially-different free-data route.

---

## 3. Frozen inputs (verified — do NOT re-derive, do NOT substitute)

- **Combined liquidation panel:** `research_state/fclr_liq_combined_panel_20261115T181405Z.parquet` — sha256 `81a100d5d0625832bebabaabea13b786e15319577721cfe8507da5b779ec7f14`, 1,740,415 event rows, 15 coins, 2025-03-22 → 2026-10-31 UTC. Columns: `timestamp`, `coin`, `notional_usd`, `side`, `source`, `tx_hash`, `fundingRate`, `premium`, `abs_fund_pct`, `mark`, `ema_dist`, `rv24h`, `rv168h`. Assert sha256 in script header.
- **FCLR-001 panel (funding/RV baseline):** `research_state/fclr011_recompute_panel_20261115T234700Z.parquet` — sha256 `41962f823e59de5989c7d854cb3180cad61a4cbc2f5f230133c41b321342c1f4`, 29,136 rows × 22 cols, 5 coins, 5,832 hours. Assert sha256 in script header. `premium` all-null; do not use.

---

## 4. Campaign details: FCLR-LIQ-CONTAGION-001

**Full name:** Cross-Coin Liquidation Contagion and Funding-Mediated Spillover Analysis
**Campaign ID:** FCLR-LIQ-CONTAGION-001-20261121T174500Z
**Rank:** 0 (ACTIVE / READY_EXECUTE)

### Hypotheses (frozen before outcomes)
- **H_contagion_liq:** Liquidation intensity in coin A at t predicts liquidation intensity in coin B at t+k (k=1..24h), controlling for B's own past liquidations and market-wide activity. Test via Granger causality on hourly aggregated counts.
- **H_contagion_funding:** Funding rate differential between coins modulates contagion strength. When funding(A) > funding(B) + threshold, liquidations in A more strongly predict liquidations in B (funding-mediated spillover). Test via funding-tercile split and interaction terms.

### Network construction
- 15×15 directed graph: nodes = coins, edges = significant Granger causality (p < 0.01 after Bonferroni for 210 tests).
- Edge weight = Granger F-statistic or lead-lag correlation coefficient.
- Permutation test: 1000+ permutations of time series for null distribution of edge weights.

### Funding conditioning
- Split sample into funding rate differential terciles (low/medium/high).
- Recompute contagion network within each tercile.
- Test whether edge weights increase monotonically with funding differential.

### Temporal stability
- Rolling window: 90-day windows, 30-day step.
- Report: network density over time, edge persistence, regime-dependent contagion.

### Materiality floor
- 2% relative effect preserved. Contagion effect must explain ≥2% of variance in coin B's liquidations to be material.

### Heavy computation scope
- Hourly aggregation: 1.74M events → ~50K hourly coin-observations
- Lead-lag matrix: 15×15 × 24 lags = 360 correlation coefficients
- Granger causality: 210 directed pairs × VAR(24) = heavy VAR estimation
- Permutation tests: 1000+ × 210 pairs = 210K+ Granger tests
- Funding-conditioned: 3 terciles × 210 pairs × Granger tests
- Temporal stability: rolling windows × network reconstruction

---

## 5. Completed campaigns (terminal — record only, do NOT re-run)

| Campaign | Mechanism | Session | Verdict | Key evidence |
|----------|-----------|---------|---------|--------------|
| FCLR-STARTER-001 | Time-series 24h forward RV (B0/B1/C1/C2) | 20261120T052201Z | NOT_SUPPORTED | C2 vs B1 +2.62% rel QLIKE (worse), Holm adj_p 0.075 |
| FCLR-XSEC-001 | Pooled within-hour funding contrast (RV) | 20261120T175300Z | NOT_SUPPORTED | funding contrast CI [−0.390, +0.158] incl. 0 |
| FCLR-XSEC-002 | Regime funding contrast (next-hour RV, RV tercile) | 20261120T210000Z | SUPPORTED | high-RV funding CI [0.0046, 0.2348], p=0.019; OOS NOT_REPLICATED |
| FCLR-XSEC-004 | Regime funding contrast (next-hour liq count) | 20261120T230000Z | SUPPORTED | low-RV funding CI [448605, 841156], p=0.0, materiality 0.80 |
| FCLR-XSEC-005 | Regime funding contrast (next-hour liq notional) | 20261121T001225Z | SUPPORTED | low-RV notional CI [452973, 850199], p=0.0, materiality 0.80 |
| FCLR-XSEC-006 | Regime funding contrast (UTC buckets) | 20261121T010934Z | SUPPORTED | significant across all three UTC buckets |
| FCLR-XSEC-007 | Cross-panel reconciliation | 20261121T021041Z | NOT_SUPPORTED | Primary CI [−0.0004, 2.005] incl. 0 (p=0.272) |
| FCLR-XSEC-008 | Alternative regime (vol-of-vol terciles) | 20261121T054721Z | NOT_SUPPORTED | sign reversal vs XSEC-002; XSEC program terminal |
| FCLR-LIQ-OOS-FORECAST-001 | OOS forecast next-24h notional liq (C2 vs B1) | 20261121T055825Z | NOT_SUPPORTED | QLIKE FAIL −5.88% CI incl. 0; Brier/LogLoss PASS; joint needs ALL |
| FCLR-LIQ-COMBINED-PANEL | Time-series 24h liq intensity (C2 vs B1) | 20261115T185844Z | NOT_MET | time-series QLIKE gate NOT_MET |
| FCLR-LIQ-XSEC-ORDERING/QLIKE | Cross-sectional daily liq intensity | 2026-11-15 | NOT_MET | daily, not regime-conditioned hourly paired |
| Track A/B / FCLR-011 | observed liq / modeled boundary / vol forecast | many | blocked/null | see `final_synthesis_report.md` |
| FCLR-BOUNDED-TRIGGER-ONLY | Trigger-only sentinel | 20261121T071500Z | SUPERSEDED | bottleneck; replaced by SYNTHESIS-01 → PANEL-FE-001 |
| FCLR-SESSION-SYNTHESIS-01 | Consolidation + meta-analysis | 20261121T080000Z | CONSOLIDATORY_ONLY | 17 contrasts; RV FE d=1.237 CI incl. 0; liq FE d=0.379 CI excl. 0 BUT RE DL d=0.228 CI incl. 0 (I²=97.5%) |
| FCLR-PANEL-FE-001 | Panel-FE + walk-forward OOS | 20261121T130159Z | COMPLETE | All artifacts emitted; verdict NOT_SUPPORTED on both halves |

---

## 6. Hard constraints (do NOT violate)

- **Do NOT** re-run any terminal campaign above
- **Do NOT** modify `.github/workflows` (protected control plane)
- **Do NOT** overwrite `research_state/research_protocol.md` (sealed legacy FCLR-001)
- **Do NOT** add root-level `research_state/*.md|*.json` — count 499/500; cap enforced by test + gate
- **Do NOT** create empty/placeholder files or empty session directories (gate checks non-zero size)
- **Do NOT** threshold-shop or relax 2% materiality floor after outcomes; null preserved as NOT_SUPPORTED
- **Do NOT** claim completion without full artifact set under new `session_<UTC>/` (UTC > 20261121T174500Z). Prose-only, trigger-only, audit-only, placeholder artifacts do NOT satisfy gate.

---

## 7. Per-session close-out (RESEARCH_PROMPT.md §12/§19)

Before finishing, update AGENT_HANDOFF.md with: what changed and why; what was tested with exact outcomes; what evidence added and where; state of each research gate; single highest-value next task; precise verifying command; any blocker with next materially different free route. Active rank-0 campaign: FCLR-LIQ-CONTAGION-001 (ACTIVE / READY_EXECUTE). **No prose-only, no trigger-only, no placeholder sessions.** Commit nothing merely to show activity; if no meaningful progress possible, record blocker evidence and stop cleanly — but DO NOT falsely claim completion while heavy work remains.

---

(End of handoff)